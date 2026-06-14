import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import ingest_lecture as m  # noqa: E402


def test_transcript_to_text_joins_and_inserts_markers():
    segs = [{"start": 0, "dur": 2, "text": "Hi"},
            {"start": 65, "dur": 2, "text": "world"}]
    assert m.transcript_to_text(segs, marker_every=1) == "[00:00] Hi [01:05] world"


def test_transcript_to_text_no_markers_and_strips():
    segs = [{"start": 0, "text": "a\n"}, {"start": 1, "text": " b "}]
    assert m.transcript_to_text(segs, marker_every=0) == "a b"


def test_chunk_text_splits_evenly_without_losing_words():
    text = " ".join(str(i) for i in range(10))
    chunks = m.chunk_text(text, 3)
    assert len(chunks) == 3
    assert " ".join(chunks).split() == text.split()


def test_chunk_text_edge_cases():
    assert m.chunk_text("", 3) == []
    assert m.chunk_text("one two", 5) == ["one", "two"]


def test_chunk_text_clamps_zero_or_negative_n():
    assert m.chunk_text("a b c", 0) == ["a b c"]
    assert m.chunk_text("a b c", -5) == ["a b c"]


def test_lecture_paths_layout():
    p = m.lecture_paths("lecture01")
    assert p["slides"].name == "slides.pdf"
    assert p["transcript_txt"].name == "transcript.txt"
    assert p["transcript_json"].name == "transcript.json"
    assert p["dir"].name == "lecture01"
    assert "references/mooc" in str(p["dir"]).replace("\\", "/")


def test_manifest_upsert_is_idempotent_by_label(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "MOOC_DIR", tmp_path)
    monkeypatch.setattr(m, "MOOC_MANIFEST", tmp_path / "manifest.json")
    m.manifest_upsert({"label": "lecture01", "title": "A"})
    m.manifest_upsert({"label": "lecture01", "title": "B"})  # replaces
    m.manifest_upsert({"label": "lecture02", "title": "C"})
    entries = m.load_manifest()
    assert [e["label"] for e in entries] == ["lecture01", "lecture02"]
    assert entries[0]["title"] == "B"


def test_slide_pdf_pages_one_entry_per_page(tmp_path):
    import pypdf
    w = pypdf.PdfWriter()
    w.add_blank_page(width=200, height=200)
    w.add_blank_page(width=200, height=200)
    pdf = tmp_path / "deck.pdf"
    with open(pdf, "wb") as f:
        w.write(f)
    pages = m.slide_pdf_pages(pdf)
    assert len(pages) == 2
    assert all(isinstance(p, str) for p in pages)
