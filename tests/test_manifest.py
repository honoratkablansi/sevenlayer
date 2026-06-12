import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "references" / "manifest.json"

EXPECTED_IDS = sorted(set(range(1, 66)) - {34, 54})  # bibliography gaps
VALID_TYPES = {"paper", "web", "stub"}


def load():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_every_bibliography_ref_present_exactly_once():
    ids = [e["id"] for e in load()]
    assert sorted(ids) == EXPECTED_IDS
    assert len(ids) == len(set(ids))


def test_entry_shape():
    for e in load():
        assert e["type"] in VALID_TYPES
        assert e["citation"].strip()
        assert e["chapters"] and all(1 <= c <= 14 for c in e["chapters"])
        if e.get("duplicate_of") is None:
            if e["type"] in ("paper", "web"):
                assert e["url"].startswith("http")
            ext = "pdf" if e["type"] == "paper" else "md"
            expected = f"references/ch{e['chapters'][0]:02d}/ref-{e['id']:02d}-{e['slug']}.{ext}"
            assert e["file"] == expected, f"ref {e['id']}: {e['file']} != {expected}"
        else:
            assert e["duplicate_of"] in EXPECTED_IDS
            assert "file" not in e


def test_slugs_are_kebab_case_and_unique():
    entries = [e for e in load() if e.get("duplicate_of") is None]
    slugs = [e["slug"] for e in entries]
    assert len(slugs) == len(set(slugs))
    for s in slugs:
        assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", s), s
