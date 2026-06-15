---
name: math-explainer
description: Use when drafting a mathematical concept explanation for the "Proving Nothing" book — produces book-ready, dependency-aware, multimodal (Sage + manim), fact-checked material executing the Sanderson + Tao teaching method via a six-stage pipeline. Triggers include "explain <concept>", "draft the math for <concept>", "build the explanation for <concept>". Not for systems/applications prose, source ingestion, or interactive tutoring.
---

# math-explainer

Turn "explain <concept>" into book-ready material that executes the **Sanderson + Tao** method. Run the six stages in order; do not skip the Stage 6 gate.

**Load first:** `references/sanderson-moves.md` and `references/tao-staging.md` (the method rubric), then `references/pipeline.md`.

## The pipeline

- **Stage 1 — Scope & dependency resolution.** Follow `references/dependency-protocol.md`. Run `scripts/resolve_deps.py master-graph/.outline/MATH_FOUNDATIONS.md "<concept>"`. Output: concept_brief.
- **Stage 2 — Stuck-point prediction.** From the prerequisites + Tao's "dumb questions", list misconceptions and the bad intuitions the rigorous phase must destroy.
- **Stage 3 — Multimodal explanation.** Tao's three phases with Sanderson moves inside (`references/pipeline.md`). Produce figures with `scripts/run_sage.py <recipe.sage>`; validate any animation values with `scripts/manim_render.py`.
- **Stage 4 — Factual-accuracy verification.** Follow `references/accuracy-protocol.md`; reach verified == true.
- **Stage 5 — Comprehension checks.** Recall (pre), apply (rigorous), transfer (post), and a "re-derive it" task; each with an answer key and on-miss route to a prerequisite.
- **Stage 6 — Assembly & gate.** Assemble the bundle (embedding the Stage-4 `accuracy_report` and Stage-5 `comprehension_set`), write `bundle.json`, run `scripts/scorecard.py bundle.json`. The scorecard binds its accuracy/comprehension checks to those embedded artifacts (validated by `scripts/schemas.py`), so a self-asserted flag cannot pass. Ship only on PASS.

## Method rubric (enforced by the Stage 6 scorecard)

Led with a visual; concrete before abstract; motivated before defined; notation earned; staged pre→rigorous→post; every heuristic paired with its rigorous counterpart; every predicted stuck-point addressed; accuracy verified; comprehension covers all three Tao levels + rediscovery; a "you could have invented this" prompt present.

## Dependencies

SageMath (`sage` on PATH) for figures; manim (optional) for animation — driven by a manim MCP server or a local manim install via `scripts/manim_render.py` (`render_scene`); fall back to Sage figures if unavailable. Run `scripts/check_env.py` to verify the tools (`sage`, `manim`, `graphify`) and the pipeline `MODE` (full-multimodal / figure-only). The master graph, `MATH_FOUNDATIONS.md`, the book-knowledge ledger, and `CHAPTER_BIBLE.md` are read-only inputs.
