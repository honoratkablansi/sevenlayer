#!/usr/bin/env python3
"""Stage 6 method-adherence gate.

Reads a bundle JSON describing an assembled concept explanation, checks it against
the Sanderson+Tao rubric, prints a report, writes <bundle_dir>/scorecard.json, and
exits 0 (pass) or 1 (fail).
"""
import json
import sys
from pathlib import Path

TAO_LEVELS = {"recall", "apply", "transfer"}


def evaluate(bundle: dict) -> list[dict]:
    checks: list[dict] = []

    def add(cid, ok, msg):
        checks.append({"id": cid, "ok": bool(ok), "msg": msg})

    modes = bundle.get("modes_order", [])

    def idx(m):
        return modes.index(m) if m in modes else 10 ** 6

    add("led_with_visual", bundle.get("led_with_visual") is True,
        "Pre-rigorous phase must open with a visual (Sanderson #1).")
    add("concrete_before_abstract", min(idx("analogy"), idx("worked_example")) < idx("formal"),
        "A concrete mode must precede the formal mode (Sanderson #2).")
    add("motivated_before_defined", bundle.get("motivated_before_defined") is True,
        "Motivation must precede the formal definition (Sanderson #4).")
    add("notation_earned", bundle.get("notation_in_pre_rigorous") is False,
        "No formal notation in the pre-rigorous phase (Sanderson #7).")
    phases = bundle.get("phases", {})
    add("staged_pre_rigorous_to_post",
        all(phases.get(p) for p in ("pre_rigorous", "rigorous", "post_rigorous")),
        "All three Tao phases must be present and non-empty.")
    add("heuristic_rigorous_pairing", len(bundle.get("heuristic_rigorous_pairs", [])) >= 1,
        "At least one heuristic paired with its rigorous counterpart (Tao Maxim 2).")
    predicted = set(bundle.get("stuck_points_predicted", []))
    addressed = set(bundle.get("stuck_points_addressed", []))
    add("stuck_points_addressed", predicted.issubset(addressed),
        f"All predicted stuck-points must be addressed; missing: {sorted(predicted - addressed)}.")
    add("accuracy_verified", bundle.get("accuracy_verified") is True,
        "Stage 4 must report verified == true.")
    levels = set(bundle.get("comprehension_levels", []))
    add("comprehension_three_levels", TAO_LEVELS.issubset(levels) and "rediscover" in levels,
        "Comprehension set must cover recall/apply/transfer + a rediscovery task.")
    add("rediscovery_prompt", bundle.get("rediscovery_prompt_present") is True,
        "A 'you could have invented this' rediscovery prompt is required (Sanderson #10).")
    return checks


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: scorecard.py <bundle.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    bundle = json.loads(path.read_text(encoding="utf-8"))
    checks = evaluate(bundle)
    passed = all(c["ok"] for c in checks)
    (path.parent / "scorecard.json").write_text(
        json.dumps({"concept": bundle.get("concept"), "passed": passed, "checks": checks}, indent=2),
        encoding="utf-8",
    )
    for c in checks:
        print(f"[{'PASS' if c['ok'] else 'FAIL'}] {c['id']}: {c['msg']}")
    print(f"\nSCORECARD: {'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
