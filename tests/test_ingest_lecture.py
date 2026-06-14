import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import ingest_lecture as m  # noqa: E402
import pytest  # noqa: E402


def test_transcript_to_text_joins_and_inserts_markers():
    segs = [{"start": 0, "dur": 2, "text": "Hi"},
            {"start": 65, "dur": 2, "text": "world"}]
    assert m.transcript_to_text(segs, marker_every=1) == "[00:00] Hi [01:05] world"


def test_transcript_to_text_no_markers_and_strips():
    segs = [{"start": 0, "text": "a\n"}, {"start": 1, "text": " b "}]
    assert m.transcript_to_text(segs, marker_every=0) == "a b"
