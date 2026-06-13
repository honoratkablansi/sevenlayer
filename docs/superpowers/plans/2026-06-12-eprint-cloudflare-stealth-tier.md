# ePrint Cloudflare Stealth Tier Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a third tier to `fetch_paper()` in `scripts/fetch_references.py` that, when curl_cffi hits a Cloudflare block, uses Camoufox to clear the challenge once per origin, then reuses the harvested `cf_clearance` cookie + user-agent via curl_cffi to download the PDF — making eprint.iacr.org downloads work unattended.

**Architecture:** Pure detection helper (`_looks_like_cloudflare`) decides whether to escalate. A monkeypatchable curl seam (`_curl_get`) and a per-origin session cache (`_clear_cloudflare` wrapping `_stealth_clear`) make the escalation logic unit-testable offline. `fetch_paper` keeps its two curl_cffi attempts and only escalates on a Cloudflare-shaped failure; `_fetch_paper_stealth` does the clear-and-reuse with one re-clear retry on stale clearance.

**Tech Stack:** Python 3.14 in `C:\sevenlayer\.venv`, Scrapling 0.4.9 (`Fetcher` = curl_cffi, `StealthyFetcher` = Camoufox), pytest.

**Spec:** `docs/superpowers/specs/2026-06-12-eprint-cloudflare-stealth-tier-design.md`

> **Superseded during execution (see spec for the authoritative final design):** two premises in this plan turned out wrong and were corrected in-flight. (1) Scrapling 0.4.9 `StealthyFetcher` is **Chromium-based, not Camoufox**, and it **does** expose a `solve_cloudflare` param — `_stealth_clear` uses `solve_cloudflare=True` (the original "no solver, stealth alone" claim came from a grep that skipped the gitignored `.venv/`). (2) The clear step must target **the challenged PDF URL**, not the origin landing page — eprint's challenge is path-scoped, so the landing page is never challenged. Live verification (refs 6/17/45) passed with these corrections.

**Deferred decision (now settled):** stealth-fetched papers keep manifest status `"ok"` (not a new `ok-stealth`). Papers map to `"ok"` in `process()` today; the stealth path only changes the in-memory `how` label used for console logging. This avoids reintroducing the status mislabeling a prior review removed. No manifest schema change.

**Conventions for all tasks:**
- Working directory `C:\sevenlayer`; venv binaries explicit: `.venv\Scripts\python.exe`.
- All edits are to `scripts/fetch_references.py` and `tests/test_fetch_references.py` only.
- Commit after each task as `Charles Hoskinson <Charles.Hoskinson@gmail.com>` (already repo-local).
- The existing 7 tests must stay green throughout.
- Verified API facts (confirmed against the installed 0.4.9 source; re-confirm in Task 3 Step 1): `Fetcher.get(url, impersonate=, timeout=, cookies=<dict>, headers=<dict>)`; `StealthyFetcher.fetch(url, headless=, network_idle=, timeout=<ms>, page_action=<callable(page)>)`; its `Response` has `.status`, `.body` (bytes), `.cookies`. Installed 0.4.9 has **no** `solve_cloudflare` — Camoufox passes the managed challenge by stealth alone.

---

### Task 1: Cloudflare detection helper

**Files:**
- Modify: `scripts/fetch_references.py` (add helpers after `is_pdf`, around line 37)
- Modify: `tests/test_fetch_references.py` (append)

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_fetch_references.py`:

```python
from fetch_references import _looks_like_cloudflare, _origin


def test_looks_like_cloudflare_403_status():
    assert _looks_like_cloudflare(403, b"")
    assert _looks_like_cloudflare(403, b"<html>anything</html>")


def test_looks_like_cloudflare_interstitial_markers():
    assert _looks_like_cloudflare(200, b"<title>Just a moment...</title>")
    assert _looks_like_cloudflare(200, b"...cf-mitigated...")
    assert _looks_like_cloudflare(503, b'<div id="challenge-platform"></div>')


def test_looks_like_cloudflare_false_for_pdf_and_404():
    assert not _looks_like_cloudflare(200, b"%PDF-1.7 ...")
    assert not _looks_like_cloudflare(404, b"<html><body>Not Found</body></html>")
    assert not _looks_like_cloudflare(0, b"")


def test_origin_strips_path():
    assert _origin("https://eprint.iacr.org/2016/260.pdf") == "https://eprint.iacr.org"
    assert _origin("https://arxiv.org/pdf/2402.15293") == "https://arxiv.org"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv\Scripts\python.exe -m pytest tests/test_fetch_references.py -k "cloudflare or origin" -v`
Expected: ImportError / FAIL (`_looks_like_cloudflare` not defined).

- [ ] **Step 3: Add the helpers**

In `scripts/fetch_references.py`, immediately after the `is_pdf` function (after line 36), insert:

```python
_CF_MARKERS = (b"just a moment", b"cf-mitigated", b"challenge-platform", b"cf-chl-")


def _looks_like_cloudflare(status: int, body: bytes) -> bool:
    """True when a failed fetch looks like a Cloudflare challenge rather than a
    plain 404/forbidden, so we only spend a browser launch when it can help."""
    if status == 403:
        return True
    head = bytes(body[:4096]).lower()
    return any(marker in head for marker in _CF_MARKERS)


def _origin(url: str) -> str:
    from urllib.parse import urlsplit

    parts = urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}"
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv\Scripts\python.exe -m pytest tests/test_fetch_references.py -v`
Expected: all pass (7 original + 4 new = 11).

- [ ] **Step 5: Commit**

```bash
git add scripts/fetch_references.py tests/test_fetch_references.py
git commit -m "Add Cloudflare-block detection helper"
```

---

### Task 2: Per-origin Camoufox session cache

**Files:**
- Modify: `scripts/fetch_references.py` (add after the Task 1 helpers)
- Modify: `tests/test_fetch_references.py` (append)

- [ ] **Step 1: Write the failing test**

Append to `tests/test_fetch_references.py`:

```python
import fetch_references as fr


def test_clear_cloudflare_caches_per_origin(monkeypatch):
    fr._CF_SESSIONS.clear()
    calls = []

    def fake_stealth_clear(origin):
        calls.append(origin)
        return {"cookies": {"cf_clearance": "abc"}, "ua": "TestUA/1.0"}

    monkeypatch.setattr(fr, "_stealth_clear", fake_stealth_clear)

    s1 = fr._clear_cloudflare("https://eprint.iacr.org")
    s2 = fr._clear_cloudflare("https://eprint.iacr.org")

    assert s1 == {"cookies": {"cf_clearance": "abc"}, "ua": "TestUA/1.0"}
    assert s2 is s1  # same cached object
    assert calls == ["https://eprint.iacr.org"]  # _stealth_clear ran exactly once


def test_clear_cloudflare_returns_none_when_unsolved(monkeypatch):
    fr._CF_SESSIONS.clear()
    monkeypatch.setattr(fr, "_stealth_clear", lambda origin: None)
    assert fr._clear_cloudflare("https://eprint.iacr.org") is None
    assert "https://eprint.iacr.org" not in fr._CF_SESSIONS  # failures are not cached
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv\Scripts\python.exe -m pytest tests/test_fetch_references.py -k clear_cloudflare -v`
Expected: FAIL (`_CF_SESSIONS` / `_clear_cloudflare` / `_stealth_clear` not defined).

- [ ] **Step 3: Add the cache and the Camoufox harvester**

In `scripts/fetch_references.py`, after the Task 1 helpers, insert:

```python
_CF_SESSIONS: dict[str, dict] = {}  # origin -> {"cookies": {...}, "ua": "..."}


def _stealth_clear(origin: str) -> dict | None:
    """Launch Camoufox on the origin landing page, pass the Cloudflare managed
    challenge by stealth, and harvest the cf_clearance cookie + matching UA.
    Returns {"cookies": {name: value, ...}, "ua": str} or None if not cleared."""
    from scrapling.fetchers import StealthyFetcher

    captured: dict = {}

    def grab(page):
        # cf_clearance is bound to this exact UA; capture both together.
        captured["ua"] = page.evaluate("navigator.userAgent")
        captured["cookies"] = {c["name"]: c["value"] for c in page.context.cookies()}
        return page

    try:
        page = StealthyFetcher.fetch(
            origin + "/",
            headless=True,
            network_idle=True,
            timeout=120000,
            page_action=grab,
        )
    except Exception as exc:  # noqa: BLE001 - browser launch/challenge failure
        print(f"    stealth-clear: {exc}")
        return None

    cookies = captured.get("cookies")
    if not cookies:  # page_action didn't run; fall back to the response cookies
        raw = page.cookies if page is not None else None
        cookies = {c["name"]: c["value"] for c in (raw or ())} if raw else {}
    if "cf_clearance" not in cookies:
        print(f"    stealth-clear: challenge not cleared for {origin}")
        return None
    return {"cookies": cookies, "ua": captured.get("ua")}


def _clear_cloudflare(origin: str) -> dict | None:
    """Cached wrapper: clear an origin at most once per process. Failures are
    not cached, so a later entry can retry."""
    cached = _CF_SESSIONS.get(origin)
    if cached is not None:
        return cached
    session = _stealth_clear(origin)
    if session is not None:
        _CF_SESSIONS[origin] = session
    return session
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv\Scripts\python.exe -m pytest tests/test_fetch_references.py -v`
Expected: all pass (11 + 2 = 13).

- [ ] **Step 5: Commit**

```bash
git add scripts/fetch_references.py tests/test_fetch_references.py
git commit -m "Add per-origin Camoufox Cloudflare-clearing session cache"
```

---

### Task 3: Wire the stealth tier into `fetch_paper`

**Files:**
- Modify: `scripts/fetch_references.py` (replace `fetch_paper`, add `_curl_get` and `_fetch_paper_stealth`)
- Modify: `tests/test_fetch_references.py` (append)

- [ ] **Step 1: Re-confirm the curl/stealth API kwargs in this environment**

Run:

```bash
.venv\Scripts\python.exe -c "from scrapling.fetchers import Fetcher; from scrapling.engines.static import GetRequestParams; import typing; print([k for k in GetRequestParams.__annotations__])"
```

Confirm `cookies` and `headers` appear in the keys. (Already verified present; if a name differs, use the actual name consistently in Step 3's `_curl_get`.) No network call here.

- [ ] **Step 2: Write the failing tests**

Append to `tests/test_fetch_references.py`:

```python
class FakeResp:
    def __init__(self, status, body):
        self.status = status
        self.body = body


def test_fetch_paper_curl_success_never_escalates(monkeypatch):
    fr._CF_SESSIONS.clear()

    def fake_curl(url, impersonate, cookies=None, headers=None):
        return FakeResp(200, b"%PDF-1.7 real pdf")

    def boom(origin):
        raise AssertionError("must not escalate on curl success")

    monkeypatch.setattr(fr, "_curl_get", fake_curl)
    monkeypatch.setattr(fr, "_clear_cloudflare", boom)

    data, how = fr.fetch_paper("https://eprint.iacr.org/2016/260.pdf")
    assert data == b"%PDF-1.7 real pdf"
    assert how == "fetcher-chrome"


def test_fetch_paper_escalates_on_cloudflare_then_reuses_session(monkeypatch):
    fr._CF_SESSIONS.clear()
    clear_calls = []

    def fake_curl(url, impersonate, cookies=None, headers=None):
        if cookies is None:
            return FakeResp(403, b"Just a moment")  # both curl_cffi attempts blocked
        return FakeResp(200, b"%PDF-1.7 cleared")  # cleared-session download wins

    def fake_clear(origin):
        clear_calls.append(origin)
        return {"cookies": {"cf_clearance": "x"}, "ua": "UA/1"}

    monkeypatch.setattr(fr, "_curl_get", fake_curl)
    monkeypatch.setattr(fr, "_clear_cloudflare", fake_clear)

    data, how = fr.fetch_paper("https://eprint.iacr.org/2016/260.pdf")
    assert data == b"%PDF-1.7 cleared"
    assert how == "fetcher-stealth"
    assert clear_calls == ["https://eprint.iacr.org"]  # cleared exactly once


def test_fetch_paper_non_cloudflare_failure_does_not_escalate(monkeypatch):
    fr._CF_SESSIONS.clear()

    def fake_curl(url, impersonate, cookies=None, headers=None):
        return FakeResp(404, b"<html>Not Found</html>")

    def boom(origin):
        raise AssertionError("404 must not trigger a browser launch")

    monkeypatch.setattr(fr, "_curl_get", fake_curl)
    monkeypatch.setattr(fr, "_clear_cloudflare", boom)

    data, how = fr.fetch_paper("https://eprint.iacr.org/9999/999.pdf")
    assert data is None
    assert how == ""


def test_fetch_paper_stale_clearance_reclears_once_then_gives_up(monkeypatch):
    fr._CF_SESSIONS.clear()
    clear_calls = []

    def fake_curl(url, impersonate, cookies=None, headers=None):
        if cookies is None:
            return FakeResp(403, b"cf-mitigated")
        return FakeResp(403, b"cf-mitigated")  # cleared session also rejected (stale)

    def fake_clear(origin):
        clear_calls.append(origin)
        return {"cookies": {"cf_clearance": "x"}, "ua": "UA/1"}

    monkeypatch.setattr(fr, "_curl_get", fake_curl)
    monkeypatch.setattr(fr, "_clear_cloudflare", fake_clear)

    data, how = fr.fetch_paper("https://eprint.iacr.org/2016/260.pdf")
    assert data is None
    assert how == ""
    assert len(clear_calls) == 2  # initial clear + one re-clear after stale
```

- [ ] **Step 3: Replace `fetch_paper` and add the seam + stealth helper**

In `scripts/fetch_references.py`, replace the entire existing `fetch_paper` function (currently lines 71-84) with:

```python
def _curl_get(url: str, impersonate: str, cookies: dict | None = None,
              headers: dict | None = None):
    """Single curl_cffi GET. Isolated so tests can monkeypatch the network."""
    from scrapling.fetchers import Fetcher

    kwargs: dict = {"impersonate": impersonate, "timeout": 90}
    if cookies:
        kwargs["cookies"] = cookies
    if headers:
        kwargs["headers"] = headers
    return Fetcher.get(url, **kwargs)


def _fetch_paper_stealth(url: str) -> bytes | None:
    """Clear the origin's Cloudflare wall with Camoufox, then download the PDF
    via curl_cffi reusing the cleared cookie + UA. One re-clear on stale state."""
    origin = _origin(url)
    for attempt in (1, 2):
        session = _clear_cloudflare(origin)
        if session is None:
            return None
        ua = session.get("ua")
        try:
            page = _curl_get(
                url,
                "chrome",
                cookies=session["cookies"],
                headers={"User-Agent": ua} if ua else None,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"    stealth-reuse: {exc}")
            return None
        if page.status == 200 and is_pdf(page.body):
            return page.body
        print(f"    stealth-reuse attempt {attempt}: status={page.status}")
        _CF_SESSIONS.pop(origin, None)  # invalidate; loop re-clears once
    return None


def fetch_paper(url: str) -> tuple[bytes | None, str]:
    """curl_cffi (chrome, firefox); on a Cloudflare block, escalate to a
    Camoufox-cleared session reused via curl_cffi. Returns (pdf_bytes, how)."""
    last_status, last_body = 0, b""
    for impersonate in ("chrome", "firefox"):
        try:
            page = _curl_get(url, impersonate)
        except Exception as exc:  # noqa: BLE001 - report and try next tier
            print(f"    {impersonate}: {exc}")
            continue
        if page.status == 200 and is_pdf(page.body):
            return page.body, f"fetcher-{impersonate}"
        last_status, last_body = page.status, page.body
        print(f"    {impersonate}: status={page.status}, pdf={is_pdf(page.body)}")

    if not _looks_like_cloudflare(last_status, last_body):
        return None, ""

    print("    cloudflare detected -> escalating to Camoufox stealth tier")
    data = _fetch_paper_stealth(url)
    return (data, "fetcher-stealth") if data is not None else (None, "")
```

- [ ] **Step 4: Run the full test suite**

Run: `.venv\Scripts\python.exe -m pytest tests/ -v`
Expected: all pass (13 + 4 = 17). Note `process()` is unchanged — it still maps any non-None paper fetch to `"ok"`, so the `"fetcher-stealth"` label only affects console output.

- [ ] **Step 5: Confirm dry-run still does no network**

Run: `.venv\Scripts\python.exe scripts/fetch_references.py --dry-run`
Expected: 63 entries, exit 0, `git status --porcelain` shows no manifest change.

- [ ] **Step 6: Commit**

```bash
git add scripts/fetch_references.py tests/test_fetch_references.py
git commit -m "Escalate fetch_paper to Camoufox stealth tier on Cloudflare blocks"
```

---

### Task 4: Manual integration verification (network)

**Files:**
- Modify: `docs/superpowers/specs/2026-06-12-eprint-cloudflare-stealth-tier-design.md` (append a short "Verification results" note) — or create `references/STEALTH_TIER_NOTES.md` if you prefer keeping it next to the corpus. Use the spec file.

This task touches the live network and Cloudflare. It is NOT part of the gated unit suite. Requires the Camoufox binaries (already installed) and a working connection.

- [ ] **Step 1: Pick one eprint ref and stash its committed PDF**

```bash
cp references/ch02/ref-06-groth16.pdf /tmp/ref-06-groth16.pdf.bak
```
(Use `$env:TEMP` on PowerShell, or any path outside the repo. The point is a known-good copy to compare against.)

- [ ] **Step 2: Force a re-download through the stealth tier**

Run: `.venv\Scripts\python.exe scripts/fetch_references.py --force --only 6`
Expected console: the two curl_cffi attempts report a 403/Cloudflare status, then `cloudflare detected -> escalating to Camoufox stealth tier`, a one-time browser clear, `-> ok`. Exit 0.

If escalation instead reports `challenge not cleared`: Camoufox did not pass the wall from this network. Record that outcome in the notes (the unit-tested logic is still correct); do not mark the task failed — the spec accounts for stricter Cloudflare modes. Then restore the stashed file (Step 4) and stop.

- [ ] **Step 3: Verify the re-downloaded PDF is valid and matches**

```bash
.venv/Scripts/python.exe - <<'EOF'
import pathlib
new = pathlib.Path("references/ch02/ref-06-groth16.pdf").read_bytes()
assert new[:5] == b"%PDF-", "not a PDF"
print("size", len(new))
EOF
```
Compare size to the backup (`ls -l`); eprint serves byte-stable PDFs, so sizes should match. A differing-but-valid PDF is acceptable (metadata variance) — note it.

- [ ] **Step 4: Restore the committed copy and confirm a clean tree**

```bash
git checkout -- references/ch02/ref-06-groth16.pdf references/manifest.json
git status --porcelain   # references/ should be clean
```
(Restoring keeps the committed corpus byte-identical; we only needed to prove the path works.)

- [ ] **Step 5: Optionally repeat for two more ids to confirm the cache amortizes**

Run: `.venv\Scripts\python.exe scripts/fetch_references.py --force --only 17,45`
Expected: the browser clears the eprint origin only once across both (the second ref reuses the cached session — look for a single clear log, not two). Restore afterward as in Step 4.

- [ ] **Step 6: Record results and commit the note**

Append to the spec file a dated "## Verification results" section stating: which ids were tested, whether Camoufox cleared the wall, whether re-downloaded PDFs matched the committed bytes, and that the corpus was restored unchanged. Then:

```bash
git add docs/superpowers/specs/2026-06-12-eprint-cloudflare-stealth-tier-design.md
git commit -m "Record stealth-tier integration verification results"
```
