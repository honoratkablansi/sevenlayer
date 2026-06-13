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
