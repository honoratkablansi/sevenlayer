# Operation: Scrape / Crawl

<!-- llm-wiki-op: scrape -->

> Fetch a URL or crawl a site section into `raw/<slug>.md` using Scrapling (transport)
> and trafilatura (extraction), then hand off to the v1 ingest flow. This is an
> **optional, Claude-Code-only** on-ramp — it only prepares `raw/` files; the wiki
> itself is written by the standard v1 ingest operation.

## Table of Contents

1. [Surface gate](#1-surface-gate)
2. [Dependency bootstrap](#2-dependency-bootstrap)
3. [Routing — when to use this playbook](#3-routing--when-to-use-this-playbook)
4. [Fetch mode — single URL](#4-fetch-mode--single-url)
5. [Standalone capture](#5-standalone-capture)
6. [Crawl mode](#6-crawl-mode)
7. [Fetcher tiers and escalation](#7-fetcher-tiers-and-escalation)
8. [Provenance and is_verbatim](#8-provenance-and-is_verbatim)
9. [WebFetch fallback (Claude Code only, non-verbatim)](#9-webfetch-fallback-claude-code-only-non-verbatim)
10. [Dedup — skipping already-ingested content](#10-dedup--skipping-already-ingested-content)
11. [Manual integration checks](#11-manual-integration-checks)

---

## 1. Surface gate

**CHECK THIS FIRST before any attempt to fetch or crawl.**

Web scraping with `scrape.py` requires **local Claude Code** running with full network
access and the ability to install Python packages. It is **not available** in the
following environments:

- **Claude API sandbox** — no network, no package installation; any fetch attempt will
  fail or hang. Do not attempt it. Say: "Scraping is not available here — the API
  sandbox has no network access. I can ingest a local file if you provide one."
- **claude.ai web** — network access is unreliable and package installation is not
  possible. Do not attempt.

If you are **not** on a local Claude Code session with confirmed network access:
1. Tell the user clearly: scraping is unavailable on this surface.
2. Offer the WebFetch fallback (§9) if applicable, or ask the user to provide a local
   file in `raw/`.
3. **Stop.** Do not hang, do not attempt a browser download, do not retry.

If you are on local Claude Code: proceed to §2.

---

## 2. Dependency bootstrap

Before running any fetch or crawl, check that Scrapling and trafilatura are installed:

```bash
python3 -c "import scrapling, trafilatura" && echo "deps-ok"
```

If this prints `deps-ok`, proceed to §3.

If the import fails (ModuleNotFoundError or similar), the libraries are not installed.
Present the install commands to the user and ask them to confirm before running:

```bash
pip install --user "scrapling[fetchers]" trafilatura
scrapling install
```

Notes:
- `scrapling install` downloads a headless Chromium browser — needed for the `stealth`
  and `dynamic` tiers; not needed for `http`-only fetches.
- **Do not pre-approve `pip` or `scrapling install`** — let the tool permission system
  prompt the user (local installs can pull significant data).
- If the user declines installing, fall back to WebFetch (§9) for a single URL; crawl
  is unavailable without Scrapling.
- Surface any install errors to the user rather than masking them.

---

## 3. Routing — when to use this playbook

**This playbook is the right choice when:**

- The source the user gave is a **URL** (starts with `http://` or `https://`).
- The user explicitly says "scrape this page", "crawl this site/section", "render the
  JS on this page", "paginate and fetch all articles", or "ingest this link".
- The user wants to capture a live web page into their wiki.

**This playbook is NOT the right choice when:**

- The source is a **local file already present in `raw/`** — that case goes directly to
  `references/operations/ingest.md` (unchanged v1 default). Do not invoke scrape for a
  local file.
- The user asks to "ingest this file" pointing to a local path.
- The user is querying, linting, or initialising the wiki.

When intent is ambiguous (user says "ingest this" without specifying whether the source
is a file or URL), ask one clarifying question before routing.

---

## 4. Fetch mode — single URL

Use this for a single page. The script fetches, extracts, quality-gates, and writes
`raw/<slug>.md` in one step.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/scrape.py fetch <url> \
    --out-dir <wiki-root>/raw \
    [--tier auto|http|stealth|dynamic]
```

The script prints a JSON summary:
```json
{"path": "raw/example-com-page-abc1234567.md", "tier": "http", "low_quality": false, "status": "written", "reason": null}
```

**On success** (`status` is `written`, `path` is non-null, `low_quality` is false):
- A `raw/<slug>.md` file has been written with full provenance frontmatter.
- Continue to `references/operations/ingest.md` and ingest that file.

**On duplicate skip** (`status` is `skipped`, `reason` is `duplicate`):
- The URL, canonical URL, or extracted-content hash already exists in the output
  directory.
- Treat this as an idempotent no-op. Report the skip and do not ingest a second copy.

**On quality rejection** (`status` is `rejected`, `low_quality` is true or `path` is null):
- The page was rejected by the quality gate: paywall stub, JS shell, extraction failure,
  non-HTML response content type, or below-threshold content (default ~200 chars of
  main text).
- Tell the user what happened and offer options:
  - Try a higher tier: `--tier stealth` (bypasses basic bot detection) or
    `--tier dynamic` (full JS rendering via Chromium).
  - Ask the user to provide a local copy of the content.
  - If the page is behind a paywall, note that automated capture is not possible.

**Exit codes:** 0 = file written or duplicate skipped; 1 = quality-rejected; 3 = missing deps.

---

## 5. Standalone capture

Use this when the user wants to capture a page to `raw/` now and ingest it later (or
manually review it first).

Run the same `fetch` command as in §4, but **stop after the file is written** — do not
proceed to ingest automatically. Report the output path and frontmatter fields to the
user so they can verify the capture before ingesting.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/scrape.py fetch <url> \
    --out-dir <wiki-root>/raw
# Inspect the written file:
# cat <wiki-root>/raw/<slug>.md | head -20
```

This is useful for:
- Previewing extraction quality before committing to an ingest.
- Batch-capturing many URLs before ingesting them in a separate session.
- Letting the user edit the `raw/` file (e.g., remove boilerplate) before ingest.

---

## 6. Crawl mode

Crawl fetches multiple pages from a site section using Scrapling's Spider. **Always
use `--plan-only` first, show the plan to the user, and get explicit confirmation
before running the real crawl.** This is a runaway and cost control — do not skip it.

### Step 1: Plan-only (always first)

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/scrape.py crawl <start-url> \
    --out-dir <wiki-root>/raw \
    --max-pages 25 \
    --max-depth 2 \
    --plan-only
```

The `--plan-only` flag prints a JSON plan without making any network requests:
```json
{
  "plan": {
    "start": "https://example.com/docs",
    "max_pages": 25,
    "max_depth": 2,
    "same_domain": true,
    "obey_robots": false
  }
}
```

Show this plan to the user. Explain:
- `max_pages`: hard cap on pages fetched (cost/time guard).
- `max_depth`: how many link-hops from the start URL.
- `same_domain`: whether to stay on the same hostname (default true).
- `obey_robots`: whether to respect `robots.txt` (default false; opt-in only).

Ask the user to confirm or adjust the parameters before proceeding.

### Step 2: Confirm and run

After explicit user confirmation ("yes", "proceed", "looks good"):

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/scrape.py crawl <start-url> \
    --out-dir <wiki-root>/raw \
    --max-pages 25 \
    --max-depth 2 \
    [--include <regex>] \
    [--exclude <regex>] \
    [--delay 1.0] \
    [--tier auto] \
    [--obey-robots]
```

Available options:
- `--include <regex>` — only enqueue URLs matching this pattern (e.g., `/docs/`)
- `--exclude <regex>` — skip URLs matching this pattern (e.g., `\.pdf$`)
- `--no-same-domain` — allow following links to other domains (use cautiously)
- `--delay <float>` — seconds between requests (default 1.0)
- `--tier` — fetcher tier for all pages (default `auto`)
- `--obey-robots` — opt-in robots.txt compliance

### Step 3: Ingest produced files

After crawl completes, the script reports how many pages were written:
```json
{"pages": 18, "written": 15, "skipped": 2, "rejected": 1}
```

Ingest the produced `raw/` files **one at a time**, following `references/operations/ingest.md`
for each file. Use batch ingest mode (ingest.md §11) if the user wants to process
multiple files in sequence — still one atomic git commit per source. Skipped pages are
duplicate no-ops; rejected pages failed the quality gate and should be reviewed before
any retry. The crawl normalizes discovered relative links to absolute URLs before
same-domain, include/exclude, and dedup checks.

---

## 7. Fetcher tiers and escalation

The `--tier auto` default (recommended) escalates through three tiers based on
concrete signals from each attempt:

| Tier | Scrapling class | When used |
|---|---|---|
| `http` | `Fetcher` | First attempt — fast TLS-spoofed HTTP |
| `stealth` | `StealthyFetcher` | On HTTP 401/403/429 or a detected Cloudflare/anti-bot challenge (or an empty/JS-shell result) |
| `dynamic` | `DynamicFetcher` | After stealth, if extracted text is still near-zero (JS shell) |

Escalation is **narrow and signal-based** — not fuzzy guessing:
- `http` → `stealth`: only on HTTP 401/403/429 or a detected challenge marker.
- `stealth` → `dynamic`: on HTTP 401/403/429, a detected challenge marker, or if
  extracted main-text remains below the threshold (default 200 chars) after stealth —
  indicating a JS-rendered shell.
- `dynamic` is the terminal tier; no further escalation.

The tier that produced the final result is recorded as `fetcher:` in frontmatter.

Use `--tier http|stealth|dynamic` to force a specific tier (no escalation). Useful
when you know the site requires a browser (`--tier dynamic`) or when debugging.

Note: `stealth` and `dynamic` tiers require `scrapling install` (downloads Chromium).
The `http` tier does not require a browser.

---

## 8. Provenance and is_verbatim

Each `raw/<slug>.md` file written by `scrape.py` includes a full provenance
frontmatter block:

```yaml
---
source_type: webpage
url: <fetched url>
canonical_url: <link rel=canonical, or normalized url>
title: <metadata title>
author: <metadata author, nullable>
published: <metadata date ISO-8601, nullable>
sitename: <metadata sitename, nullable>
fetched_at: <YYYY-MM-DD>
fetcher: http | stealth | dynamic
fetch_method: scrapling | webfetch
is_verbatim: true
http_status: 200
extractor: trafilatura-<version>
content_hash: <sha256 of extracted markdown>
---
```

**`is_verbatim` is the critical provenance flag:**

- `is_verbatim: true` — Scrapling+trafilatura output is **byte-derived** from the
  live page. The extracted markdown faithfully represents the source content and
  **may be quoted verbatim** in wiki pages (with the standard provenance marker).
- `is_verbatim: false` — content was captured via the WebFetch fallback (§9), which
  is model-summarized or paraphrased, **not** a verbatim byte-level extraction.
  This content **must not be quoted verbatim** in wiki pages. It may be cited with a
  tight paraphrase and a provenance marker, but never presented as an exact quote from
  the source. See §9 for the full rule.

The v1 ingest "quote from the open raw file" rule remains fully in effect for
`is_verbatim: true` sources. For `is_verbatim: false` sources, apply the extended
rule: cite with paraphrase only.

---

## 9. WebFetch fallback (Claude Code only, non-verbatim)

If the user declines installing Scrapling, or if `scrape.py` is unavailable, you may
use the `WebFetch` tool as a last-resort fallback **for a single URL** (crawl is
unavailable without Scrapling). The WebFetch fallback is itself **Claude-Code-only** —
it is not available in the API sandbox.

### WebFetch fallback procedure

1. Use the `WebFetch` tool to retrieve the page content.
2. Manually write `raw/<slug>.md` with the following frontmatter. Use
   `slug_for_url`-style naming (hostname-lastpathseg-hash) or a descriptive slug.
3. Set these provenance fields:

```yaml
---
source_type: webpage
url: <fetched url>
canonical_url: <fetched url>
title: <title from page or user-provided>
fetched_at: <today YYYY-MM-DD>
fetch_method: webfetch
is_verbatim: false
extractor: webfetch
---
```

4. Write the page body as a **tight summary / paraphrase** of the content — not a
   direct copy-paste of the model's rendering of the page (the WebFetch result is a
   model interpretation, not a byte-level extraction).

### Non-verbatim rule (CRITICAL)

Content captured via WebFetch has `is_verbatim: false`. During the subsequent ingest:

- **Do not** quote this content verbatim in wiki page claim lines.
- **Do** cite it with a tight paraphrase and a standard provenance marker:
  `Founded in 2019.^[from [[Source Page]] — paraphrased; is_verbatim: false]`
- Note the non-verbatim status clearly in the source-summary page.

This preserves the wiki's provenance integrity: the "exact quote from the raw file"
rule holds only for verbatim sources.

---

## 10. Dedup — skipping already-ingested content

`scrape.py` performs two-level dedup before writing any `raw/` file. Both checks run
against existing markdown frontmatter in the target output directory:

1. **URL identity dedup:** `dedup_key(url)` normalizes both the fetched URL and any
   `<link rel=canonical>` the page declares, then compares against `url` and
   `canonical_url` fields in existing raw captures. Variants like `http` vs `https`,
   `www` prefix, tracking params (`utm_*`, `fbclid`, etc.), and trailing slashes are
   all normalized away — they produce the same dedup key.

2. **Content hash dedup:** `sha256` of the extracted markdown is compared against
   `content_hash` fields in existing raw captures. This catches different URLs serving
   identical content (mirrors, canonical redirects, CDN variants).

**When a skip occurs:** the script reports `status: "skipped"` and `reason:
"duplicate"`. This is a normal, expected outcome for re-runs and variant URLs — not
an error. Report the skip reason to the user.

**Idempotency:** re-fetching a URL that was already ingested (or any tracking-param
variant of it) produces a reported no-op, not a duplicate `raw/` file.

If the user wants to force a re-fetch (e.g., the page content has changed), they can:
- Manually delete the existing `raw/<slug>.md` before running `scrape.py`, or
- Run the fetch with a modified URL (include a version or date query param) —
  though the dedup key will still match if the content hash matches.

---

## 11. Manual integration checks

These checks verify that Scrapling and trafilatura are working correctly after
installation. Run these on local Claude Code after `pip install` and `scrapling install`.

### Single-page fetch verification

```bash
python3 - <<'PY'
import importlib.util, os
s = importlib.util.spec_from_file_location(
    "scrape", os.path.expanduser("~/.claude/skills/llm-wiki/scripts/scrape.py"))
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
r = m.fetch_one("https://example.com/", tier="http")
print("tier:", r["tier"], "status:", r["status"],
      "low_quality:", r["low_quality"], "chars:", len(r["markdown"]))
assert r["markdown"], "no markdown extracted"
print("INTEGRATION CHECK PASSED")
PY
```

Expected output: a line with `tier: http status: 200 low_quality: False chars: <N>`
and `INTEGRATION CHECK PASSED`. If `low_quality: True` or `chars: 0`, trafilatura
extraction is not working — check the Scrapling version and the raw HTML.

### Crawl plan-only smoke test (no network required)

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/scrape.py crawl https://example.com/docs \
    --out-dir /tmp/wiki-test/raw \
    --max-pages 5 \
    --plan-only
```

Expected: JSON plan printed to stdout, exit code 0. No network requests, no Scrapling
import (plan-only is exempt from the dep check).

### Dep gate verification (when Scrapling is NOT installed)

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/scrape.py fetch https://example.com \
    --out-dir /tmp/wiki-test/raw
echo "exit=$?"
```

Expected: the dep-gate message printed to stderr (listing missing deps and install
commands) and `exit=3`. No traceback, no hang.

### Spider API note (v0.4.x)

The `crawl_site` function in `scrape.py` uses Scrapling's Spider and a shared
`CrawlBudget` so `max_pages` caps attempted page fetches, not only accepted
results. The Spider API
must be verified against the installed Scrapling version (v0.4.x) before relying
on it:

```python
from scrapling.spiders import Spider
```

The crawl Spider symbol and attribute names (`start_urls`, `allowed_domains`,
`robots_txt_obey`, `parse` coroutine, `response.follow`) should be verified against
the installed version. Run `--plan-only` first; then run with `--max-pages 3` on a
known small site to confirm bounds, dedup, and content-hash skip behavior before
a full production crawl.

`crawl_site` returns at most `max_pages` results, and `CrawlBudget` has unit coverage
for the attempted-fetch cap. No automated test covers the full Spider runtime
(network + browser dependency); this manual integration check is the gate.
