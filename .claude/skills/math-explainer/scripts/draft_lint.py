#!/usr/bin/env python3
"""Prose-hygiene lint for a draft's `draft.md`.

Flags pipeline/QA/build vocabulary and machine-vocabulary residue that leaked into
book prose — the kind of thing the editorial panel marks (e.g. a chapter ending on a
"scorecard PASS" verification footer, or a "comprehension set" heading). Pure function
`lint_draft(text) -> list[str]` (each "L<n>: ..."); CLI exits 1 on any finding.

This is a deterministic guard on the *generated prose*, not a self-attested flag — it
reads the actual draft text, so it cannot be gamed by metadata.
"""
import re
import sys
from collections import Counter
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

# "Announce the count, then tick it off" tic (draft-quality rule 9): a number immediately
# before a rhetorical-count noun, e.g. "kills three bad instincts", "rests on two premises".
COUNT_TIC = re.compile(
    r"\b(two|three|four|five|six|seven|eight|nine|ten|\d+)\s+(bad\s+|tempting\s+)?"
    r"(instinct|intuition|misconception|premise)s?\b",
    re.IGNORECASE,
)
# Roadmap announcements before a glossary box (rule 9).
ROADMAP = re.compile(r"one sentence each|facts you'?ll need", re.IGNORECASE)


def _anaphora(text: str) -> list[str]:
    """Flag paragraphs where >=3 sentences open with the same first three words."""
    findings: list[str] = []
    for para in re.split(r"\n\s*\n", text):
        sents = re.split(r"(?<=[.!?])\s+", para.strip())
        openers = []
        for s in sents:
            words = re.findall(r"[A-Za-z']+", s)
            if len(words) >= 3:
                openers.append(" ".join(words[:3]).lower())
        for opener, n in Counter(openers).items():
            if n >= 3:
                findings.append(f"anaphora: {n} sentences open with '{opener}...' — vary the openings")
    return findings


def _self_chapter_ref(text: str) -> list[str]:
    """Flag body references to the draft's own home chapter (rule 11).

    The home chapter is the first 'Chapter N' (the subtitle); any later 'Ch N' / 'Chapter N'
    is the draft citing itself as an external dependency, which the editorial Copyeditor marks
    critical.
    """
    findings: list[str] = []
    lines = text.splitlines()
    home = None
    home_line = 0
    for i, line in enumerate(lines, start=1):
        m = re.search(r"\bChapter\s+(\d+)", line)
        if m:
            home, home_line = m.group(1), i
            break
    if not home:
        return findings
    ref = re.compile(r"\b(?:Ch\.?|Chapter)\s+" + re.escape(home) + r"\b")
    for i, line in enumerate(lines, start=1):
        if i == home_line:
            continue
        if ref.search(line):
            findings.append(f"L{i}: self-reference to own home chapter (Ch {home}) — use 'this chapter' (rule 11)")
    return findings


def lint_draft(text: str) -> list[str]:
    """Return prose-hygiene findings as strings (empty == clean)."""
    findings: list[str] = []
    for i, line in enumerate(text.splitlines(), start=1):
        low = line.lower()
        for term in PIPELINE_TERMS:
            if term in low:
                findings.append(f"L{i}: pipeline/QA vocabulary in prose: '{term}'")
        for term in AI_TERMS:
            if term in low:
                findings.append(f"L{i}: AI-vocabulary residue: '{term}'")
        m = COUNT_TIC.search(line)
        if m:
            findings.append(f"L{i}: count-announcement tic (rule 9): '{m.group(0).strip()}' — drop the number, argue in prose")
        if ROADMAP.search(line):
            findings.append(f"L{i}: roadmap announcement (rule 9): never pre-announce a glossary list")
    findings.extend(_anaphora(text))
    findings.extend(_self_chapter_ref(text))
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
