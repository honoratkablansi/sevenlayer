# ePrint Cloudflare Stealth Tier — Design

**Date:** 2026-06-12
**Status:** Approved (approach A — Camoufox clears the wall, curl_cffi reuses the session)
**Goal:** Give `scripts/fetch_references.py` a durable, unattended way to download eprint.iacr.org (and similarly Cloudflare-walled) paper PDFs, so `--force` reruns, future-edition references, and fresh clones on other machines all succeed without a manual cookie-harvest.

## Context

- `fetch_paper()` currently makes two curl_cffi attempts (`Fetcher.get` with chrome then firefox impersonation). eprint.iacr.org sits behind a Cloudflare managed challenge that returns HTTP 403 to all curl_cffi impersonation profiles, so all 31 ePrint PDFs fail this path.
- Task 4 worked around it manually: `StealthyFetcher` (Scrapling's Chromium-based stealth browser) loaded an eprint page with `solve_cloudflare=True`, passed the challenge through real browser execution, and the harvested `cf_clearance` cookie + browser user-agent were fed to curl_cffi to pull the actual PDF bytes. The 31 PDFs are committed; this design makes that workaround a permanent code path.
- **`StealthyFetcher` is Chromium-based, not Camoufox** (an earlier draft of this spec wrongly said Camoufox; `camoufox` is not even importable in this venv). **Scrapling 0.4.9 DOES expose `solve_cloudflare: bool`** — a validated param that "solves all types of Cloudflare's Turnstile/Interstitial challenges before returning the response" (it requires `timeout >= 60000ms`). The clearing step uses `solve_cloudflare=True`, which is what the manual Task 4 workaround actually used. (A prior claim here that the package had "no Cloudflare code" came from a grep that silently skipped the gitignored `.venv/`; reading the source directly confirms the solver exists.)
- Verified 0.4.9 API surface (read directly from the installed source, not via a gitignore-respecting grep):
  - `StealthyFetcher.fetch(url, **kwargs)` accepts `cookies`, `page_action` (a `Callable` receiving the live page, validated as callable), `network_idle`, `solve_cloudflare` (bool), `useragent`, `wait_selector`, `timeout` (milliseconds).
  - Its `Response` exposes `.status`, `.body` (bytes), and `.cookies` (tuple of cookie dicts / dict).
  - `Fetcher.get(url, **kwargs)` accepts `impersonate`, `timeout` (seconds), and `cookies`.

## Design

### Component: a stealth tier inside `fetch_paper()` (`scripts/fetch_references.py`)

`fetch_paper(url)` keeps its current two curl_cffi attempts. New behavior: if both attempts fail **and the failure looks like a Cloudflare block** (HTTP 403, or a non-PDF body whose content sniffs as a Cloudflare interstitial — e.g. contains `cf-mitigated`, `Just a moment`, or `challenge-platform`), escalate to a stealth tier:

1. **Clear the wall once per run (module-level cached session).** On first escalation, call `StealthyFetcher.fetch` on **the actual failing PDF URL** with `solve_cloudflare=True`, `network_idle=True`, and a `page_action` that, after the challenge is solved, harvests from the live page. (An earlier draft cleared the origin landing page `https://eprint.iacr.org/` to dodge the browser's download-vs-render problem — but live testing showed eprint's challenge is scoped to the PDF asset paths, so the landing page returns 200 with no challenge and never mints `cf_clearance`. Clearing the challenged PDF URL is what the proven manual workaround did, and `solve_cloudflare` handles the interstitial before any download begins.) The `page_action` harvests:
   - the `cf_clearance` cookie (and any other cookies the origin set), via the page's context cookies;
   - the exact `navigator.userAgent` string the stealth browser presented (cf_clearance is bound to this UA). **UA-binding (live-verified OK):** the concern was that curl_cffi's `impersonate` might override the harvested User-Agent on the reuse call and break the UA↔cf_clearance binding. Live verification (refs 6/17/45) confirmed the reuse is accepted with HTTP 200, so this risk did not materialize against eprint; the documented fallback if a stricter host ever rejects it is to fetch the PDF bytes through the browser's own request context.

   Store `(cookies, user_agent)` in a module-level cache keyed by origin, so the browser launches at most once per origin per process. If `page_action` harvesting proves awkward, fall back to reading `Response.cookies` plus a UA captured via a one-line `page.evaluate("navigator.userAgent")` inside `page_action`.

2. **Download the PDF with the cleared session via curl_cffi.** Call `Fetcher.get(url, impersonate="chrome", cookies=<harvested cookies>, headers/UA=<harvested UA>, timeout=90)`. curl_cffi with a valid `cf_clearance` + matching UA passes the wall. Validate `is_pdf(body)` as today.

3. **One retry on stale clearance.** If the cleared-session download still 403s (clearance expired mid-run), invalidate the cached session for that origin, re-clear once, retry once. If it still fails, return failure for that entry.

Return contract is unchanged: `fetch_paper` returns `(pdf_bytes | None, how)`. The `how` label gains a value for the stealth path (e.g. `"fetcher-stealth"`). `process()` maps any successful paper fetch to status `"ok"` today; this design keeps papers as `"ok"` but the design spec's `ok-stealth` status MAY be applied to stealth-fetched papers if we want the manifest to record which papers needed the wall — decided in the plan. (Default: keep `"ok"` for papers to avoid reintroducing the mislabeling the Task 3 review removed; the `how` string is for logging only.)

### Boundaries

- The stealth tier is internal to `fetch_paper`. `fetch_web_text`, `process`, `main`, the manifest schema, and the CLI flags are unchanged. No new top-level functions are exposed beyond small private helpers (`_looks_like_cloudflare(status, body)`, `_clear_cloudflare(origin)`).
- The pure helpers (`is_pdf`, `stub_markdown`, `web_markdown`) and their tests are untouched.
- No new files, no new dependencies — Camoufox is already installed.

## Error handling

- **Camoufox unavailable / launch failure** (browser binaries missing, headless crash): catch, log, return failure for the entry — never abort the whole run. A `--force` rerun of one ref must isolate its own failure exactly as the current per-entry isolation does.
- **Challenge not passed** (Camoufox itself gets a challenge page, e.g. network change to a stricter Cloudflare mode): the harvested cookies won't contain `cf_clearance`; detect that and return failure with a clear log line ("Cloudflare challenge not cleared for <origin>") rather than handing curl_cffi a useless session.
- **Non-Cloudflare 403** (genuinely forbidden, dead link): `_looks_like_cloudflare` must be specific enough that a plain 403/404 does NOT trigger a pointless browser launch. When in doubt, the stealth tier still runs but fails fast and cheap on the cleared-session download.
- **Idempotency preserved:** the stealth tier only runs during an actual download attempt; existing-file skip logic and atomic writes are unchanged, so reruns over a complete corpus remain no-ops.

## Testing

- **Unit (offline, no network) — the only tests that gate the plan:**
  - `_looks_like_cloudflare`: true for (403, b""), true for a body containing `Just a moment` / `cf-mitigated` / `challenge-platform`, false for a real PDF body, false for a plain 404 HTML page.
  - Session cache: a `_clear_cloudflare` stubbed (monkeypatched) to a fake harvester is called at most once per origin across multiple `fetch_paper` calls in one process; the cached `(cookies, ua)` is reused.
  - `fetch_paper` escalation logic with `Fetcher`/`StealthyFetcher` monkeypatched: curl_cffi-success path never launches the browser; curl_cffi-403 path triggers exactly one clear + one cleared-session download; stale-clearance path triggers exactly one re-clear then gives up.
  - All existing 7 tests still pass.
- **Integration (network, manual, not in the gated suite):** `--force --only <one eprint id>` actually downloads a valid PDF via the stealth tier; then a byte-for-byte (or `%PDF` + size) check that the stealth-fetched file matches the committed copy. Run for a small sample (e.g. refs 5, 17, 45), not all 31, to respect Cloudflare and time. Document that this step requires the Camoufox binaries and live network.

## Verification

- Full unit suite green.
- Manual: temporarily move one committed eprint PDF aside, run `--force --only <id>`, confirm the stealth tier repopulates a valid PDF, confirm a second run is a no-op. Restore from git if the redownload differs only in PDF metadata (eprint serves byte-stable PDFs, so an exact match is expected).
- `--dry-run` still does no network and creates no files.

## Out of scope

- Re-downloading all 31 ePrint PDFs in bulk (they are committed and byte-stable; the manual integration sample is enough to prove the tier).
- A persistent on-disk `user_data_dir` cookie cache across runs (approach C) — the per-process cache is sufficient for `--force` and edition refreshes.
- Proxy rotation, CAPTCHA-solving services, or handling Cloudflare modes stricter than the current managed challenge.
- Applying the stealth tier to `fetch_web_text` (web pages already have a working StealthyFetcher fallback).

## Git

Single feature branch, milestone commits (Cloudflare-detection helper + tests, stealth tier wired into `fetch_paper`, manual integration verification notes). Repo-local author `Charles Hoskinson <Charles.Hoskinson@gmail.com>`.

## Verification results

**Date:** 2026-06-12. Live-network manual verification against `eprint.iacr.org`'s Cloudflare wall, using the real Scrapling `StealthyFetcher` headless Chromium browser with `solve_cloudflare=True`.

**Outcome: the stealth tier did NOT clear the wall.** Ref **id 6** (`https://eprint.iacr.org/2016/260.pdf` → `references/ch02/ref-06-groth16.pdf`) was force-re-downloaded with `python scripts/fetch_references.py --force --only 6`. Console flow observed:

- curl_cffi attempt 1 (`chrome` impersonation): `status=403, pdf=False`.
- curl_cffi attempt 2 (`firefox` impersonation): `status=403, pdf=False`.
- `cloudflare detected -> escalating to Camoufox stealth tier` (the 403 from the PDF path correctly triggered escalation).
- The headless browser then loaded the origin landing page: `INFO: Fetched (200) <GET https://eprint.iacr.org/>` — **status 200, no challenge**. Immediately before it, Scrapling logged `ERROR: No Cloudflare challenge found.`
- Result: `stealth-clear: challenge not cleared for https://eprint.iacr.org` → entry status `failed` → process exit code **1**.

**Root cause of the negative result.** This is not the UA↔`cf_clearance` binding risk the design flagged at the reuse step — the reuse step was never reached. The failure is upstream, in the *clearing* step: the design clears the wall by visiting the HTML landing page `https://eprint.iacr.org/` (chosen to avoid the browser's download-vs-render problem on a `.pdf` URL). But that landing page is **not** Cloudflare-walled — it serves 200 with no Turnstile/interstitial challenge, so `solve_cloudflare=True` finds nothing to solve (`No Cloudflare challenge found`) and never mints a `cf_clearance` cookie. Only the `*.pdf` paths return 403. Clearing `/` therefore cannot produce the clearance cookie the PDF path requires, and `_stealth_clear` correctly reports `cf_clearance` absent and returns `None`. The two-attempt re-clear loop in `_fetch_paper_stealth` cannot help because the clear itself yields no challenge to solve.

**Implication for the design.** The "clear a lightweight HTML page of the same origin, reuse the cookie via curl_cffi" approach (approach A) does not hold for eprint.iacr.org as currently configured: the origin's challenge is applied per-path (on the PDF assets), not on the landing page, so there is no same-origin HTML page that mints the needed `cf_clearance`. Options to pursue in a follow-up: (a) run `solve_cloudflare` directly against the `.pdf` URL and capture bytes from the browser's own response/request context rather than reusing the cookie via curl_cffi; (b) point the clearing fetch at an HTML path that *is* itself challenged; or (c) accept that the committed corpus must be refreshed by a human-attended browser session. Cloudflare may also have moved eprint to a stricter/differently-scoped mode since the original manual harvest that produced the committed PDFs.

**Outputs / integrity.**
- No valid PDF was produced by the stealth tier for ref 6 (the only ref tested end-to-end). Because `fetch_paper` returned `None`, `process()` never wrote the file, so the committed PDF was never overwritten: `references/ch02/ref-06-groth16.pdf` retained valid magic `b'%PDF-'` and its original size **404221 bytes** throughout (matching the pre-test backup byte-for-byte by size).
- The only working-tree change from the run was `references/manifest.json` (entry 6 status flipped to `failed`); it was restored via `git checkout -- references/manifest.json`.
- **Cache amortization across refs 17/45 was NOT tested** — Step 5 is gated on Step 2 succeeding, and Step 2 failed to clear the wall, so there was no cached session to amortize. (All three refs share the `https://eprint.iacr.org` origin, so the amortization path is exercisable once clearing works.)
- **Corpus restored unchanged:** after `git checkout -- references/ch02/ref-06-groth16.pdf references/manifest.json`, `git status --porcelain` reported the `references/` tree clean (only this spec doc differs).

### 2026-06-12 (after clear-URL fix, commit 02bb441)

Re-ran the same live-network verification on branch `eprint-cloudflare-stealth-tier` with HEAD at commit `02bb441` ("Clear Cloudflare on the challenged PDF URL, not the landing page"). The fix corrects the root cause identified above: the stealth tier now runs `solve_cloudflare` directly against the challenged `*.pdf` URL instead of the unchallenged landing page `/`.

**Outcome: the stealth tier CLEARED the wall and produced a valid byte-matching PDF.** Ref **id 6** (`https://eprint.iacr.org/2016/260.pdf` → `references/ch02/ref-06-groth16.pdf`) was force-re-downloaded with `python scripts/fetch_references.py --force --only 6`. Console flow observed:

- curl_cffi `chrome` attempt: `status=403, pdf=False`; curl_cffi `firefox` attempt: `status=403, pdf=False`.
- `cloudflare detected -> escalating to Camoufox stealth tier`.
- The headless browser now loaded the **PDF URL itself** and was challenged: `INFO: The turnstile version discovered is "managed"`, then (after a re-solve pass) `INFO: Cloudflare captcha is solved`.
- `INFO: Fetched (307) <GET https://eprint.iacr.org/2016/260.pdf>` → `Fetched (200) <GET https://eprint.iacr.org/2016/260.pdf>` (×2).
- Entry status: `-> ok`. Summary line: `63/63 resolved; unresolved: none`.

This is neither failure sub-case from the prior run: the challenge **did** present on the PDF URL to the headless browser, the solve succeeded, and the curl_cffi reuse was **not** rejected — the UA↔`cf_clearance` binding risk flagged in the design did not materialize on this run.

**Valid PDF produced.** Post-download integrity check (`open(...,'rb').read()`): magic `b'%PDF-'`, size **404221 bytes** — an exact byte-size match to the committed baseline (404221) and to the pre-test backup. The stealth tier fetched a genuine, correct PDF.

**Cache amortization (refs 17/45) tested and confirmed.** With ref 6 succeeding, Step 5 ran `python scripts/fetch_references.py --force --only 17,45`. Both share the `https://eprint.iacr.org` origin. Observed:

- Ref **17** (`2021/370.pdf`): two curl 403s → `cloudflare detected -> escalating` → full browser Turnstile solve (`turnstile version "managed"` … `Cloudflare captcha is solved`) → 307 → 200 → 200 → `-> ok`.
- Ref **45** (`2025/611.pdf`): two curl 403s → **no browser solve at all** (no `turnstile`/`solving`/`captcha` log lines) → immediate `Fetched (200)` → `-> ok`. The second ref reused the cached origin session minted by ref 17.
- The browser solve happened **exactly once** across both refs, confirming the cache amortizes the expensive Turnstile solve across same-origin fetches.

**Corpus restored clean.** After each test phase, `git checkout -- references/` was run; `git status --porcelain` reported the `references/` tree clean both times (only this spec doc differs). The temp backup was removed. No committed corpus file was permanently modified.
