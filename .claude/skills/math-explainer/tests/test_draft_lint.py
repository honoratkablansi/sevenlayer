from scripts.draft_lint import lint_draft

CLEAN = """# Schwartz-Zippel: Why Polynomials Catch Liars

A forger hands you a giant spreadsheet. You point at one random cell and check only that.

## Rigorous

Let F be a finite field — for us, the 101 numbers 0..100 with arithmetic that wraps at 101.
A nonzero polynomial of degree d has at most d roots.

## Check yourself

1. Recall: state the bound.

This trick is the engine under the proof systems we build next.
"""

PIPELINE_LEAK = """# Concept

Some prose.

## Verification

This figure is correct-by-construction; the scorecard reports SCORECARD: PASS and the
sage manifest in bundle.json was validated by validate_scene_values.
"""

AI_HEADING = """# Concept

Intro.

## Check yourself (comprehension set)

1. Recall.
"""


def test_clean_prose_has_no_findings():
    assert lint_draft(CLEAN) == []


def test_pipeline_vocab_in_prose_is_flagged():
    findings = lint_draft(PIPELINE_LEAK)
    joined = " ".join(findings).lower()
    assert findings  # non-empty
    assert "scorecard" in joined
    assert "correct-by-construction" in joined
    assert "bundle.json" in joined


def test_findings_carry_line_numbers():
    findings = lint_draft(PIPELINE_LEAK)
    assert any(":" in f and any(ch.isdigit() for ch in f.split(":")[0]) for f in findings)


def test_ai_vocab_heading_flagged():
    findings = lint_draft(AI_HEADING)
    assert any("comprehension set" in f.lower() for f in findings)
