#!/usr/bin/env python3
"""Headless smoke-eval for the deterministic core of math-explainer.

Checks: every eval concept resolves against MATH_FOUNDATIONS; the sample bundle passes
the scorecard; and (if Sage is installed) the sample recipe produces a valid manifest.
"""
import json
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL))
from scripts.resolve_deps import parse_strata, resolve          # noqa: E402
from scripts.scorecard import evaluate                          # noqa: E402
from scripts.run_sage import run_recipe                         # noqa: E402

ROOT = SKILL.parents[2]


def main() -> int:
    ok = True
    md = (ROOT / "master-graph" / ".outline" / "MATH_FOUNDATIONS.md").read_text(encoding="utf-8")
    rows = parse_strata(md)
    for c in json.loads((SKILL / "evals" / "concepts.json").read_text(encoding="utf-8")):
        found = resolve(c, rows) is not None
        ok &= found
        print(f"[{'OK ' if found else 'MISS'}] resolve: {c}")

    bundle = json.loads((SKILL / "evals" / "sample_bundle" / "bundle.json").read_text(encoding="utf-8"))
    card_ok = all(x["ok"] for x in evaluate(bundle))
    ok &= card_ok
    print(f"[{'OK ' if card_ok else 'FAIL'}] scorecard: sample bundle")

    if shutil.which("sage"):
        import os
        os.chdir(SKILL)
        m = run_recipe(Path("scripts/recipes/schwartz_zippel.sage"))
        sage_ok = m["num_agreements"] <= 2 and Path(m["figure"]).exists()
        ok &= sage_ok
        print(f"[{'OK ' if sage_ok else 'FAIL'}] sage: schwartz_zippel ({m['num_agreements']} agreements)")
    else:
        print("[SKIP] sage not installed")

    print("\nEVAL:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
