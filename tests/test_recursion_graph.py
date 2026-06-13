import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from split_recursion_outline import split_chapters

SAMPLE = """# Recursive Proof Composition: A Three-Chapter Treatment

intro blurb

## Chapter 1: Recursive Proof Composition

### 1.1 Why Recursion?
ch1 body

## Chapter 2: Folding Schemes in Depth

ch2 body

## Chapter 3: Applications of Recursive Proving

ch3 body

## Backmatter Notes (for the full manuscript)

backmatter
"""


def test_split_chapters_returns_three():
    chs = split_chapters(SAMPLE)
    assert [slug for slug, _ in chs] == ["rc01", "rc02", "rc03"]


def test_split_chapter_bodies_bounded():
    chs = dict(split_chapters(SAMPLE))
    assert "ch1 body" in chs["rc01"] and "ch2 body" not in chs["rc01"]
    assert "backmatter" not in chs["rc03"]   # backmatter excluded
    assert "intro blurb" not in chs["rc01"]  # title preamble excluded


import fetch_references as fr


def test_process_reuse_entry_no_network(tmp_path, monkeypatch):
    existing = tmp_path / "existing.pdf"
    existing.write_bytes(b"%PDF-1.7 x")
    monkeypatch.setattr(fr, "REPO", tmp_path)

    def boom(*a, **k):
        raise AssertionError("reuse entry must not fetch")

    monkeypatch.setattr(fr, "fetch_paper", boom)
    ok = {"id": 1, "slug": "nova", "type": "paper", "chapters": [1],
          "file": "references/recursion/ch1/ref-01-nova.pdf",
          "reuse": "existing.pdf", "status": "pending"}
    assert fr.process(ok, [ok], force=False, dry_run=False) == "ok"
    missing = dict(ok, reuse="nope.pdf")
    assert fr.process(missing, [missing], force=False, dry_run=False) == "pending"


def test_manifest_path_is_overridable(tmp_path, monkeypatch):
    m = tmp_path / "m.json"
    m.write_text('[{"id": 1, "slug": "x"}]', encoding="utf-8")
    monkeypatch.setattr(fr, "MANIFEST_PATH", m)
    assert fr.load_manifest()[0]["slug"] == "x"
