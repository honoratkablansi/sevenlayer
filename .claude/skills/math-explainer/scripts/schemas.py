#!/usr/bin/env python3
"""Machine-readable schemas for the six pipeline artifacts (pure validators).

Each ``validate_*`` returns a list of human-readable error strings; an empty list means
the object conforms to its schema. There is no third-party dependency — these mirror the
project's pure-function, unit-tested style and run under the pytest venv. They turn the
"JSON-ish prose" stage contracts into checks so a stage cannot pass on presence alone.

CLI: ``python schemas.py <artifact> <file.json>`` where <artifact> is one of
concept_brief | stuck_points | explanation | accuracy_report | comprehension_set | bundle.
"""
import json
import sys
from pathlib import Path

TARGET_DEPTHS = {"pre-rigorous", "rigorous", "post-rigorous"}
COMPREHENSION_LEVELS = {"recall", "apply", "transfer", "rediscover"}
SEVERITIES = {"low", "medium", "high"}


def _is_nonempty_str(v) -> bool:
    return isinstance(v, str) and bool(v.strip())


def _str_list(value, where: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{where}: expected a list")
        return
    for i, item in enumerate(value):
        if not _is_nonempty_str(item):
            errors.append(f"{where}[{i}]: expected a non-empty string")


def validate_concept_brief(d: dict) -> list[str]:
    e: list[str] = []
    if not isinstance(d, dict):
        return ["concept_brief: expected an object"]
    if not _is_nonempty_str(d.get("concept")):
        e.append("concept_brief.concept: required non-empty string")
    if not _is_nonempty_str(d.get("stratum")):
        e.append("concept_brief.stratum: required non-empty string")
    _str_list(d.get("prerequisites", []), "concept_brief.prerequisites", e)
    _str_list(d.get("assumed_background", []), "concept_brief.assumed_background", e)
    if d.get("target_depth") not in TARGET_DEPTHS:
        e.append(f"concept_brief.target_depth: must be one of {sorted(TARGET_DEPTHS)}")
    lo = d.get("learning_objectives")
    if not isinstance(lo, list) or not lo:
        e.append("concept_brief.learning_objectives: required non-empty list")
    else:
        _str_list(lo, "concept_brief.learning_objectives", e)
    return e


def validate_stuck_points(d: dict) -> list[str]:
    e: list[str] = []
    if not isinstance(d, dict):
        return ["stuck_points: expected an object"]
    misc = d.get("misconceptions")
    if not isinstance(misc, list) or not misc:
        e.append("stuck_points.misconceptions: required non-empty list")
    else:
        for i, m in enumerate(misc):
            where = f"stuck_points.misconceptions[{i}]"
            if not isinstance(m, dict):
                e.append(f"{where}: expected an object")
                continue
            if not _is_nonempty_str(m.get("claim")):
                e.append(f"{where}.claim: required non-empty string")
            if not _is_nonempty_str(m.get("why_tempting")):
                e.append(f"{where}.why_tempting: required non-empty string")
            if m.get("severity") not in SEVERITIES:
                e.append(f"{where}.severity: must be one of {sorted(SEVERITIES)}")
    _str_list(d.get("dumb_questions", []), "stuck_points.dumb_questions", e)
    _str_list(d.get("bad_intuitions_to_kill", []), "stuck_points.bad_intuitions_to_kill", e)
    return e


def validate_explanation(d: dict) -> list[str]:
    e: list[str] = []
    if not isinstance(d, dict):
        return ["explanation: expected an object"]
    phases = d.get("phases", {})
    if not isinstance(phases, dict):
        e.append("explanation.phases: expected an object")
    else:
        for p in ("pre_rigorous", "rigorous", "post_rigorous"):
            if not _is_nonempty_str(phases.get(p)):
                e.append(f"explanation.phases.{p}: required non-empty string")
    modes = d.get("modes", {})
    if not isinstance(modes, dict):
        e.append("explanation.modes: expected an object")
    else:
        for m in ("analogy", "worked_example", "formal", "synthesis"):
            if m not in modes:
                e.append(f"explanation.modes.{m}: required")
        visual = modes.get("visual")
        if not isinstance(visual, dict):
            e.append("explanation.modes.visual: required object")
        elif not _is_nonempty_str(visual.get("figure_ref")):
            e.append("explanation.modes.visual.figure_ref: required non-empty string")
    return e


def validate_accuracy_report(d: dict) -> list[str]:
    e: list[str] = []
    if not isinstance(d, dict):
        return ["accuracy_report: expected an object"]
    claims = d.get("claims")
    if not isinstance(claims, list) or not claims:
        e.append("accuracy_report.claims: required non-empty list")
    manifest = d.get("sage_manifest")
    if not isinstance(manifest, dict) or not manifest:
        e.append("accuracy_report.sage_manifest: required non-empty object")
    elif "figure" not in manifest:
        e.append("accuracy_report.sage_manifest.figure: required")
    if not isinstance(d.get("ledger_refs", []), list):
        e.append("accuracy_report.ledger_refs: expected a list")
    if not isinstance(d.get("adversarial_findings", []), list):
        e.append("accuracy_report.adversarial_findings: expected a list")
    if not isinstance(d.get("verified"), bool):
        e.append("accuracy_report.verified: required boolean")
    return e


def validate_comprehension_set(items: list) -> list[str]:
    e: list[str] = []
    if not isinstance(items, list) or not items:
        return ["comprehension_set: required non-empty list"]
    seen = set()
    for i, it in enumerate(items):
        where = f"comprehension_set[{i}]"
        if not isinstance(it, dict):
            e.append(f"{where}: expected an object")
            continue
        if it.get("level") not in COMPREHENSION_LEVELS:
            e.append(f"{where}.level: must be one of {sorted(COMPREHENSION_LEVELS)}")
        else:
            seen.add(it["level"])
        for k in ("question", "answer_key", "targets_stuck_point", "on_miss_route_to"):
            if not _is_nonempty_str(it.get(k)):
                e.append(f"{where}.{k}: required non-empty string")
    missing = COMPREHENSION_LEVELS - seen
    if missing:
        e.append(f"comprehension_set: must cover all levels; missing {sorted(missing)}")
    return e


def validate_bundle(d: dict) -> list[str]:
    e: list[str] = []
    if not isinstance(d, dict):
        return ["bundle: expected an object"]
    if not _is_nonempty_str(d.get("concept")):
        e.append("bundle.concept: required non-empty string")
    phases = d.get("phases", {})
    if not isinstance(phases, dict) or not all(
        _is_nonempty_str(phases.get(p)) for p in ("pre_rigorous", "rigorous", "post_rigorous")
    ):
        e.append("bundle.phases: requires non-empty pre_rigorous/rigorous/post_rigorous")
    if not isinstance(d.get("modes_order"), list) or not d.get("modes_order"):
        e.append("bundle.modes_order: required non-empty list")
    for flag in ("led_with_visual", "motivated_before_defined", "notation_in_pre_rigorous"):
        if not isinstance(d.get(flag), bool):
            e.append(f"bundle.{flag}: required boolean")
    pairs = d.get("heuristic_rigorous_pairs")
    if not isinstance(pairs, list) or not pairs:
        e.append("bundle.heuristic_rigorous_pairs: required non-empty list")
    else:
        for i, p in enumerate(pairs):
            if not (isinstance(p, (list, tuple)) and len(p) == 2 and all(_is_nonempty_str(x) for x in p)):
                e.append(f"bundle.heuristic_rigorous_pairs[{i}]: must be two non-empty strings")
    sp = d.get("stuck_points_predicted")
    if not isinstance(sp, list) or not sp:
        e.append("bundle.stuck_points_predicted: required non-empty list")
    if not isinstance(d.get("stuck_points_addressed", []), list):
        e.append("bundle.stuck_points_addressed: expected a list")
    e += [f"bundle.{msg}" for msg in validate_accuracy_report(d.get("accuracy_report", {}))]
    e += [f"bundle.{msg}" for msg in validate_comprehension_set(d.get("comprehension_set", []))]
    return e


VALIDATORS = {
    "concept_brief": validate_concept_brief,
    "stuck_points": validate_stuck_points,
    "explanation": validate_explanation,
    "accuracy_report": validate_accuracy_report,
    "comprehension_set": validate_comprehension_set,
    "bundle": validate_bundle,
}


def main(argv: list[str]) -> int:
    if len(argv) != 3 or argv[1] not in VALIDATORS:
        print(f"usage: schemas.py <{'|'.join(VALIDATORS)}> <file.json>", file=sys.stderr)
        return 2
    obj = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    errors = VALIDATORS[argv[1]](obj)
    for msg in errors:
        print(f"INVALID: {msg}")
    print(f"\n{argv[1].upper()}: {'VALID' if not errors else 'INVALID'}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
