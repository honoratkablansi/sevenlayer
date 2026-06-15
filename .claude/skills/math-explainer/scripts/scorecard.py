#!/usr/bin/env python3
"""Stage 6 method-adherence gate.

Reads a bundle JSON describing an assembled concept explanation, checks it against
the Sanderson+Tao rubric, prints a report, writes <bundle_dir>/scorecard.json, and
exits 0 (pass) or 1 (fail).
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # skill root on path
from scripts.schemas import validate_accuracy_report, validate_comprehension_set  # noqa: E402


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
    pairs = bundle.get("heuristic_rigorous_pairs", [])

    def valid_pair(p):
        return (isinstance(p, (list, tuple)) and len(p) == 2
                and all(isinstance(x, str) and x.strip() for x in p))

    add("heuristic_rigorous_pairing", len(pairs) >= 1 and all(valid_pair(p) for p in pairs),
        "Each heuristic must be paired with a non-empty rigorous counterpart (Tao Maxim 2).")
    predicted = set(bundle.get("stuck_points_predicted", []))
    addressed = set(bundle.get("stuck_points_addressed", []))
    add("stuck_points_addressed", bool(predicted) and predicted.issubset(addressed),
        f"At least one stuck-point must be predicted (Stage 2) and all addressed; "
        f"missing: {sorted(predicted - addressed)}.")
    ar = bundle.get("accuracy_report")
    add("accuracy_verified",
        isinstance(ar, dict) and not validate_accuracy_report(ar) and ar.get("verified") is True,
        "Stage 4 accuracy_report must be well-formed (Sage manifest + claims) and verified == true.")
    cset = bundle.get("comprehension_set", [])
    add("comprehension_three_levels", not validate_comprehension_set(cset),
        "Comprehension set must be well-formed and cover recall/apply/transfer + rediscovery.")
    add("rediscovery_prompt",
        any(isinstance(it, dict) and it.get("level") == "rediscover" for it in cset),
        "A 'you could have invented this' rediscovery task is required (Sanderson #10).")
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
