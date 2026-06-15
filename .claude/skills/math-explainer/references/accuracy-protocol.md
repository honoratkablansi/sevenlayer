# Stage 4 — factual-accuracy protocol

1. **Visual/numeric claims (correct-by-construction).** Every figure is produced by a Sage recipe via `scripts/run_sage.py`, which returns a values manifest. Extract every numeric/quantitative claim in the draft prose and confirm it matches the manifest. If a claim is not backed by the manifest, recompute it in Sage or remove it.
2. **Animation.** For any manim scene, collect the values it displays into scene_values.json and run `scripts/manim_render.py scene_values.json manifest.json`; it must report PASS (no drift from the Sage manifest).
3. **Conceptual/historical claims.** Cross-check against the book-knowledge claim ledger for provenance; cite the supporting claim(s). Flag any claim with no ledger/graph support rather than keeping it.
4. **Adversarial pass.** Dispatch a red-team check ("find one error in this explanation or figure"); resolve anything it finds.
Output: accuracy_report = { manifest_ref, claim_checks[], ledger_refs[], adversarial_findings[], verified: bool }. `verified` must be true before Stage 6.
