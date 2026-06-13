import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "references" / "recursion" / "manifest.json"
VALID_TYPES = {"paper", "web", "stub"}


def load():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_ids_unique_and_sorted():
    ids = [e["id"] for e in load()]
    assert ids == sorted(ids)
    assert len(ids) == len(set(ids))


def test_entry_shape():
    for e in load():
        assert e["type"] in VALID_TYPES, e
        assert e["citation"].strip()
        assert e["chapters"] and all(c in (1, 2, 3) for c in e["chapters"]), e
        if "reuse" in e:
            # overlap with the main corpus: references an existing file there.
            assert (REPO / e["reuse"]).exists(), f"reuse target missing: {e['reuse']}"
            continue
        ext = "pdf" if e["type"] == "paper" else "md"
        expected = f"references/recursion/ch{e['chapters'][0]}/ref-{e['id']:02d}-{e['slug']}.{ext}"
        assert e["file"] == expected, f"ref {e['id']}: {e['file']} != {expected}"
        if e["type"] in ("paper", "web"):
            assert e["url"].startswith("http"), e


def test_slugs_kebab_and_unique():
    slugs = [e["slug"] for e in load()]
    assert len(slugs) == len(set(slugs))
    for s in slugs:
        assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", s), s
