import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "references" / "manifest.json"

EXPECTED_IDS = sorted(set(range(1, 66)) - {34, 54})  # curated bibliography gaps
VALID_TYPES = {"paper", "web", "stub"}
VALID_STATUS = {"pending", "ok", "ok-stealth", "stub", "failed"}


def load():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def curated():
    """Hand-curated bibliography entries (snowball discoveries excluded)."""
    return [e for e in load() if "snowball_round" not in e]


def snowball():
    """Auto-discovered entries appended by the citation snowball."""
    return [e for e in load() if "snowball_round" in e]


def test_every_bibliography_ref_present_exactly_once():
    # The curated bibliography mirrors the book exactly; ids are globally unique.
    assert sorted(e["id"] for e in curated()) == EXPECTED_IDS
    all_ids = [e["id"] for e in load()]
    assert len(all_ids) == len(set(all_ids))


def test_entry_shape():
    for e in curated():
        assert e["status"] in VALID_STATUS
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


def test_snowball_entries_shape():
    # Snowball entries share the manifest but follow the looser references/snowball/
    # convention and carry provenance. They may re-discover an already-curated paper
    # (slug/url collisions are tolerated), so only basic shape is enforced here.
    for e in snowball():
        assert e["status"] in VALID_STATUS, e
        assert e["type"] in VALID_TYPES, e
        assert e["citation"].strip()
        assert e["snowball_round"] >= 0
        assert e["file"].startswith("references/snowball/book/"), e["file"]
        assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", e["slug"]), e["slug"]
        if e["type"] in ("paper", "web") and "url" in e:
            assert e["url"].startswith("http")


def test_slugs_are_kebab_case_and_unique():
    # Curated slugs are unique; snowball slugs are title-derived and may repeat.
    slugs = [e["slug"] for e in curated() if e.get("duplicate_of") is None]
    assert len(slugs) == len(set(slugs))
    for s in slugs:
        assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", s), s


def test_urls_unique():
    # Curated urls are unique; snowball may re-resolve an already-curated url.
    urls = [e["url"] for e in curated() if "url" in e]
    assert len(urls) == len(set(urls))
