import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from fetch_references import is_pdf, stub_markdown, web_markdown

ENTRY = {
    "id": 57,
    "slug": "chorus-one-zk-economics",
    "citation": "Klich, Rafal (Chorus One). The Economics of ZK-Proving. March 2025.",
    "chapters": [13],
    "type": "stub",
    "file": "references/ch13/ref-57-chorus-one-zk-economics.md",
    "status": "pending",
}

WEB_ENTRY = {
    "id": 27,
    "slug": "l2beat-stages",
    "citation": "L2Beat. Stages Framework for L2 Maturity.",
    "chapters": [8],
    "type": "web",
    "url": "https://l2beat.com/stages",
    "file": "references/ch08/ref-27-l2beat-stages.md",
    "status": "pending",
}


def test_is_pdf():
    assert is_pdf(b"%PDF-1.7 rest of file")
    assert not is_pdf(b"<!DOCTYPE html>")
    assert not is_pdf(b"")


def test_stub_markdown_carries_citation_and_id():
    md = stub_markdown(ENTRY)
    assert "ref_id: 57" in md
    assert "Klich" in md
    assert "print-only or paywalled" in md


def test_web_markdown_frontmatter():
    md = web_markdown(WEB_ENTRY, "Extracted page text.", "fetcher", "2026-06-12")
    head, body = md.split("---\n", 2)[1:]
    assert "ref_id: 27" in head
    assert "source_url: https://l2beat.com/stages" in head
    assert "fetched: 2026-06-12" in head
    assert "fetched_with: fetcher" in head
    assert "Extracted page text." in body


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


def test_stealth_clear_harvests_cookies_and_ua_via_page_action(monkeypatch):
    fr._CF_SESSIONS.clear()

    class FakeCtx:
        @staticmethod
        def cookies():
            return [{"name": "cf_clearance", "value": "tok"},
                    {"name": "other", "value": "y"}]

    class FakePage:
        context = FakeCtx()

        def evaluate(self, script):
            return "BrowserUA/2.0"

    class FakeResp:
        cookies = ()

    def fake_fetch(url, **kwargs):
        kwargs["page_action"](FakePage())  # simulate Scrapling invoking the callback
        return FakeResp()

    monkeypatch.setattr("scrapling.fetchers.StealthyFetcher.fetch", fake_fetch)
    session = fr._stealth_clear("https://eprint.iacr.org")
    assert session == {"cookies": {"cf_clearance": "tok", "other": "y"},
                       "ua": "BrowserUA/2.0"}


def test_stealth_clear_falls_back_to_response_cookies(monkeypatch):
    fr._CF_SESSIONS.clear()

    class FakeResp:
        cookies = ({"name": "cf_clearance", "value": "fromresp"},)

    def fake_fetch(url, **kwargs):
        return FakeResp()  # page_action effectively no-op (swallowed) -> empty capture

    monkeypatch.setattr("scrapling.fetchers.StealthyFetcher.fetch", fake_fetch)
    session = fr._stealth_clear("https://eprint.iacr.org")
    assert session == {"cookies": {"cf_clearance": "fromresp"}, "ua": None}


def test_stealth_clear_returns_none_without_cf_clearance(monkeypatch):
    fr._CF_SESSIONS.clear()

    class FakeResp:
        cookies = ({"name": "session", "value": "z"},)

    monkeypatch.setattr("scrapling.fetchers.StealthyFetcher.fetch",
                        lambda url, **k: FakeResp())
    assert fr._stealth_clear("https://eprint.iacr.org") is None


def test_stealth_clear_returns_none_on_browser_exception(monkeypatch):
    fr._CF_SESSIONS.clear()

    def fake_fetch(url, **kwargs):
        raise RuntimeError("browser launch failed")

    monkeypatch.setattr("scrapling.fetchers.StealthyFetcher.fetch", fake_fetch)
    assert fr._stealth_clear("https://eprint.iacr.org") is None
