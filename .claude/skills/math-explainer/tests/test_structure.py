from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]

def test_skill_md_has_frontmatter():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---"), "SKILL.md must start with YAML frontmatter"
    fm = text.split("---", 2)[1]
    assert "name: math-explainer" in fm
    assert "description:" in fm

def test_layout_dirs_exist():
    for d in ("references", "scripts", "tests"):
        assert (SKILL / d).is_dir(), f"missing dir: {d}"

def test_method_cards_exist_and_have_content():
    s = (SKILL / "references" / "sanderson-moves.md").read_text(encoding="utf-8")
    # ten numbered moves
    for n in range(1, 11):
        assert f"{n}." in s, f"sanderson-moves.md missing move {n}"
    t = (SKILL / "references" / "tao-staging.md").read_text(encoding="utf-8")
    for phase in ("pre-rigorous", "rigorous", "post-rigorous"):
        assert phase in t.lower(), f"tao-staging.md missing phase: {phase}"
    assert "destroy bad intuition" in t.lower()

def test_reference_docs_exist():
    for name in ("dependency-protocol.md", "accuracy-protocol.md", "pipeline.md", "draft-quality.md"):
        p = SKILL / "references" / name
        assert p.exists() and p.read_text(encoding="utf-8").strip(), f"empty/missing: {name}"

def test_pipeline_lists_six_stages():
    text = (SKILL / "references" / "pipeline.md").read_text(encoding="utf-8").lower()
    for n in range(1, 7):
        assert f"stage {n}" in text, f"pipeline.md missing Stage {n}"

def test_skill_body_references_stages_and_scripts():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
    for n in range(1, 7):
        assert f"stage {n}" in text, f"SKILL.md missing Stage {n}"
    for script in ("resolve_deps.py", "run_sage.py", "manim_render.py", "scorecard.py"):
        assert script in text, f"SKILL.md does not reference {script}"
    for card in ("sanderson-moves.md", "tao-staging.md"):
        assert card in text, f"SKILL.md does not reference {card}"
