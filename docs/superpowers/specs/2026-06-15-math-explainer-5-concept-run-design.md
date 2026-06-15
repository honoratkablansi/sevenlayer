# Design Spec — Drafting 5 Concepts with `math-explainer` (full-pipeline test run)

**Status:** Approved design (2026-06-15). Next: writing-plans → execution.

**Goal:** Exercise the `math-explainer` skill end-to-end on the five `evals/concepts.json` concepts, producing committed, schema-valid, **scorecard-PASS** chapter-grade draft material per concept. This is a **pipeline test**: every external dependency must be installed, live, and actually invoked. There are **no fallback paths** — a missing dependency aborts the run.

## 1. The five concepts

| Concept | slug | Chapter(s) | Stratum | Depth | Figure (Sage) | Animation (manim) |
|---|---|---|---|---|---|---|
| Schwartz–Zippel lemma | `schwartz-zippel` | Ch 7 (slogan Ch 6) | S2 | I→R | agreement points of two polys over GF(101) | random-point spot-check; rare agreement |
| Multilinear extension (MLE) | `multilinear-extension` | Ch 7 | S3 | R | Boolean hypercube `{0,1}ⁿ` + unique multilinear surface | extend cube values to the continuous surface |
| Sum-Check | `sum-check` | Ch 8 | S9/3 | R | round-by-round univariate restrictions | the interactive reduction collapsing the hypercube sum |
| Pedersen commitment | `pedersen-commitment` | Ch 11 | S5 | R | `gᵐhʳ` on a cyclic/EC group; hiding via `r` | randomness `r` blurring the committed point |
| Bilinear pairings | `bilinear-pairings` | Ch 11 | S6 | R | `e(aP,bQ)=e(P,Q)^{ab}` bilinearity | pairing map two curve points → target-group element |

The concept→chapter map drives Stage 1's CHAPTER_BIBLE "Reader should already know" lookup; the stratum/depth drive `target_depth`.

## 2. Invariant — no fallbacks, all dependencies live

The entire pipeline runs in **one environment: WSL (Ubuntu-26.04)**, where **graphify + SageMath + manim are all installed and exercised**. A strict preflight aborts the run unless all three resolve. The skill's documented degraded modes (Sage-figures-only, optional manim, MATH_FOUNDATIONS-table-only when graphify is absent) are **disabled for this run** — they are not exercised and not relied upon.

## 3. Stage 0 — setup & strict preflight (runs once, before any concept)

1. **Install graphify into WSL** from its real git source (the PyPI package `graphifyy` is a flagged typosquat — do **not** use it; resolve the true source via `pip show graphify` on the existing Windows install, then replicate in WSL). Put `graphify` on the WSL PATH so it sits alongside the `sage` and `manim` wrappers.
2. **Smoke-test graphify in WSL** against the existing graph: `graphify query "Schwartz–Zippel"` (run from `/mnt/c/sevenlayer`) must return a real scoped subgraph from `graphify-out/`. The book content graph already contains all five concepts (verified: Schwartz/Multilinear/Pedersen/sum-check/pairing all appear as graph content). Run `graphify update .` only if a refresh is required. Note: `graphify query "<concept>"` is the correct concept-enrichment call; `graphify explain` requires an exact node label.
3. **Strict preflight gate:** extend `scripts/check_env.py` with a required-set mode — `check_env.py --require sage,manim,graphify` exits non-zero unless **all** named tools resolve. The run does not begin until this exits 0. (Small skill enhancement, built TDD: a `required` parameter to `main`, plus a `missing(required)` helper; existing default behavior preserved.)

## 4. Output layout (persistent, committed)

One directory per concept: `master-graph/.drafts/<slug>/`

```
master-graph/.drafts/<slug>/
  draft.md                 # phased prose (pre/rigorous/post) + "Math you'll need" sidebar
                           #   + "rediscover-it" box + the comprehension set
  concept_brief.json       # Stage 1 artifact (schema-valid)
  stuck_points.json        # Stage 2 artifact (schema-valid)
  accuracy_report.json     # Stage 4 artifact (verified == true, embeds the Sage manifest)
  comprehension_set.json   # Stage 5 artifact (schema-valid; recall/apply/transfer/rediscover)
  bundle.json              # Stage 6 input (embeds accuracy_report + comprehension_set)
  scorecard.json           # Stage 6 gate output (passed == true)
  figures/<slug>.svg       # committed copy of the Sage figure
  animations/<slug>.*      # committed manim render (frame/clip)
master-graph/.drafts/INDEX.md   # one-line pointer per concept (final consolidation)
```

Reusable generators live in the skill: Sage recipes at `scripts/recipes/<slug>.sage` (joining `schwartz_zippel.sage`), manim scenes at a new `scripts/scenes/<slug>.py`. Raw renders land in the skill's gitignored `assets/`; the final figure/animation is copied into the concept's draft dir and committed. (Schwartz–Zippel's recipe already exists and is reused.)

**Animations are short rendered clips, not single frames.** `render_scene` currently hardcodes `-s` (last-frame PNG, used by the E3 smoke test); for production it must render a short clip. The skill enhancement adds a `still: bool = True` parameter to `render_scene` (default preserves the smoke-test behavior); the run calls it with `still=False` for a `-ql` clip (mp4/gif) per concept.

## 5. Per-concept workflow (the six stages, concrete)

1. **Scope & dependency resolution.** `scripts/resolve_deps.py … "<concept>"` for the MATH_FOUNDATIONS row, **plus** `graphify query "<concept>"` for the live scoped subgraph (prerequisites verified against it), **plus** the target chapter's "Reader should already know" from CHAPTER_BIBLE. → `concept_brief.json` (schema-valid: concept, stratum, prerequisites, assumed_background, target_depth, learning_objectives).
2. **Stuck-point prediction.** From prerequisites + Tao "dumb questions" + known misconceptions. → `stuck_points.json`.
3. **Multimodal explanation.** Author `scripts/recipes/<slug>.sage` → `run_sage.py` → JSON manifest + SVG; author `scripts/scenes/<slug>.py` → `render_scene` (real manim). Write the three Tao phases with Sanderson moves inside.
4. **Factual-accuracy verification.** Every numeric/visual claim checked against the Sage manifest; manim displayed values checked via `validate_scene_values` (no drift); concept/historical claims cross-checked against the book-knowledge ledger + graph; an **adversarial red-team subagent** attempts to find one error. → `accuracy_report.json` with `verified == true` (embeds `sage_manifest`).
5. **Comprehension checks.** recall (pre) / apply (rigorous) / transfer (post) / rediscover items, each with an answer key, a targeted stuck-point, and an on-miss route to a Stage-1 prerequisite. → `comprehension_set.json`.
6. **Assembly & gate.** Embed accuracy_report + comprehension_set → `bundle.json`; `schemas.py bundle` valid; `scorecard.py` **PASS**; render `draft.md`. Ship the concept only on PASS.

## 6. Orchestration — pilot, then parallel

- **Pilot (in-session): `schwartz-zippel`.** Run all six stages end-to-end myself to produce the reference bundle and validate the output layout, the new `scripts/scenes/` convention, and a real Sage+manim render in WSL. This becomes the worked template.
- **Parallel (4 Opus subagents):** `multilinear-extension`, `sum-check`, `pedersen-commitment`, `bilinear-pairings`. Each subagent receives the pilot as a worked example plus concept-specific context (chapter, stratum, prerequisites, figure/animation intent), and produces its own draft dir in isolation (separate dirs → no write conflicts). Each runs its own real Sage + manim + graphify calls.
- **Consolidation:** verify all five, write `INDEX.md`, commit.

Conceptual ordering note (informational; the runs are independent because Stage 1 resolves each concept's own prerequisites): Sum-Check builds on Multilinear extension; Pedersen and Bilinear pairings are both Ch 11. Cross-references are recorded in each `draft.md`, not enforced as run-order dependencies.

## 7. Verification & done-definition (per concept)

A concept is done when, **run under real Sage + manim + graphify in WSL**:
- `schemas.py` validates `concept_brief`, `stuck_points`, `accuracy_report`, `comprehension_set`, and `bundle`;
- `scorecard.py bundle.json` → **PASS** (`scorecard.json.passed == true`);
- `run_sage.py` produced the figure under real Sage; the manim scene rendered for real; `validate_scene_values` is clean;
- **graphify was actually queried and its subgraph incorporated** into `concept_brief`;
- the draft dir is committed (local only, **no Co-Authored-By trailer, no push**).

Run-level done: strict preflight passed before any concept; all five committed; `INDEX.md` written.

## 8. Environment

Single environment: **WSL Ubuntu-26.04**, with graphify (git install), Sage 10.9 (`/usr/local/bin/sage`), and manim 0.20.1 (`/usr/local/bin/manim`) all live. No cross-host split and no capability fallback: if any dependency is missing, the run aborts at the Stage-0 preflight.

## 9. Risks & mitigations

1. **graphify WSL install** (git source + its dependencies) — the one real setup risk. Mitigated by the Stage-0 smoke test, which must return a real subgraph before any concept runs.
2. **manim render time/flakiness** — use short, low-quality (`-ql`) scenes; single-frame where motion isn't essential.
3. **Execution cost** — chapter-grade × 5, full multimodal, is a large generative effort. The plan is cheap; the generation cost is incurred at execution (run after the plan is approved).

## 10. Scope

In scope: producing the five committed drafts via the live pipeline, plus the small skill enhancements required to run it — the `check_env --require` strict-preflight mode, the `scripts/scenes/` convention, and the `render_scene(still=…)` clip toggle. Out of scope: changing the six-stage method, the scorecard rubric, or the skill's spec; publishing drafts into the manuscript; any non-math concept.
