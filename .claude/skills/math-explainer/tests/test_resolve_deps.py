from pathlib import Path
from scripts.resolve_deps import parse_strata, resolve

FIX = Path(__file__).resolve().parent / "fixtures" / "mini_foundations.md"

def rows():
    return parse_strata(FIX.read_text(encoding="utf-8"))

def test_parse_skips_header_and_separator_rows():
    concepts = [r["concept"] for r in rows()]
    assert not any(c.lower() == "concept" for c in concepts)
    assert all(set(c) - {"-", ":"} for c in concepts)
    assert len(rows()) == 3

def test_resolve_exact_and_substring():
    rs = rows()
    sz = resolve("Schwartz", rs)
    assert sz is not None
    assert sz["stratum"].startswith("Algebra I")
    assert "polynomials" in sz["prerequisites"]
    assert "union bound" in sz["prerequisites"]

def test_resolve_pedersen_prereqs():
    p = resolve("Pedersen commitment", rows())
    assert p["first_needed"] == "Ch 11"
    assert "cyclic groups" in p["prerequisites"]
    assert "discrete log" in p["prerequisites"]

def test_resolve_unknown_returns_none():
    assert resolve("nonexistent concept", rows()) is None
