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
