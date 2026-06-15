import json
from pathlib import Path
from scripts.resolve_deps import parse_strata, resolve
from scripts.scorecard import evaluate

SKILL = Path(__file__).resolve().parents[1]
ROOT = SKILL.parents[2]  # repo root: .claude/skills/math-explainer -> repo

def test_all_eval_concepts_resolve():
    md = (ROOT / "master-graph" / ".outline" / "MATH_FOUNDATIONS.md").read_text(encoding="utf-8")
    rows = parse_strata(md)
    concepts = json.loads((SKILL / "evals" / "concepts.json").read_text(encoding="utf-8"))
    unresolved = [c for c in concepts if resolve(c, rows) is None]
    assert unresolved == [], f"unresolved eval concepts: {unresolved}"

def test_sample_bundle_passes_scorecard():
    bundle = json.loads((SKILL / "evals" / "sample_bundle" / "bundle.json").read_text(encoding="utf-8"))
    assert all(c["ok"] for c in evaluate(bundle))
