# The six-stage pipeline (operational detail)

**Stage 1 — Scope & dependency resolution.** See `dependency-protocol.md`. Produces concept_brief.

**Stage 2 — Stuck-point prediction.** From the concept_brief prerequisites + Tao's "dumb questions" + known misconceptions, list where the reader trips and which bad intuitions the rigorous phase must destroy. Produces stuck_points = { misconceptions[], dumb_questions[], bad_intuitions_to_kill[] }.

**Stage 3 — Multimodal explanation.** Tao's three phases with Sanderson moves inside (see `sanderson-moves.md`, `tao-staging.md`):
- Pre-rigorous: concrete hook/story → lead with the Sage figure (run a recipe via `run_sage.py`) and/or a manim scene → motivate the definition → minimal notation → a "you could have invented this" prompt.
- Rigorous: earn the formal definition/theorem/proof; explicitly destroy each Stage-2 bad intuition.
- Post-rigorous: rebuild intuition on rigor; pair every picture with its formal statement; land the "aha".

**Stage 4 — Factual-accuracy verification.** See `accuracy-protocol.md`. Must reach verified == true.

**Stage 5 — Comprehension checks.** Generate a recall (pre), an apply (rigorous), a transfer/"why inevitable" (post) item, plus a Sanderson "re-derive it" task. Each targets a Stage-2 stuck-point and a learning objective, with an answer key and an on-miss route back to a Stage-1 prerequisite.

**Stage 6 — Assembly & gate.** Assemble prose + figures + "Math you'll need" sidebar + "rediscover-it" box + comprehension set + met→locked spiral pointers into a bundle, write `bundle.json`, then run `scripts/scorecard.py bundle.json`. Ship only on PASS; otherwise return to the failing stage.
