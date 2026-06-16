#!/usr/bin/env python3
"""Prose-hygiene lint for a draft's `draft.md`.

Flags pipeline/QA/build vocabulary and machine-vocabulary residue that leaked into
book prose — the kind of thing the editorial panel marks (e.g. a chapter ending on a
"scorecard PASS" verification footer, or a "comprehension set" heading). Pure function
`lint_draft(text) -> list[str]` (each "L<n>: ..."); CLI exits 1 on any finding.

This is a deterministic guard on the *generated prose*, not a self-attested flag — it
reads the actual draft text, so it cannot be gamed by metadata.
"""
import sys
from pathlib import Path

# Pipeline / QA / build vocabulary that must never appear in reader-facing prose.
PIPELINE_TERMS = [
    "scorecard",
    "correct-by-construction",
    "sage manifest",
    "values manifest",
    "bundle.json",
    "validate_scene_values",
    "run_sage",
    "scorecard.py",
    "schemas.py",
    "concept_brief",
    "eval: pass",
]
# Machine/AI-vocabulary residue (especially in headings).
AI_TERMS = [
    "comprehension set",
]


def lint_draft(text: str) -> list[str]:
    """Return prose-hygiene findings as 'L<line>: <issue>' strings (empty == clean)."""
    findings: list[str] = []
    for i, line in enumerate(text.splitlines(), start=1):
        low = line.lower()
        for term in PIPELINE_TERMS:
            if term in low:
                findings.append(f"L{i}: pipeline/QA vocabulary in prose: '{term}'")
        for term in AI_TERMS:
            if term in low:
                findings.append(f"L{i}: AI-vocabulary residue: '{term}'")
    return findings


def main(argv=None) -> int:
    argv = list(sys.argv if argv is None else argv)
    if len(argv) != 2:
        print("usage: draft_lint.py <draft.md>", file=sys.stderr)
        return 2
    findings = lint_draft(Path(argv[1]).read_text(encoding="utf-8"))
    for f in findings:
        print(f"LINT: {f}")
    print(f"\nDRAFT LINT: {'CLEAN' if not findings else str(len(findings)) + ' issue(s)'}")
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
