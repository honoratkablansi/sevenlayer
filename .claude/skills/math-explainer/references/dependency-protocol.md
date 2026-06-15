# Stage 1 — dependency protocol

`scripts/resolve_deps.py` is a **pure** MATH_FOUNDATIONS parser (no graphify import, so it
runs under the pytest venv). It produces only the table-derived fields; the model assembles
the full `concept_brief` by performing steps 2–4 (graphify and CHAPTER_BIBLE are read via the
project's system Python, per the dual-interpreter rule).

1. Run `scripts/resolve_deps.py master-graph/.outline/MATH_FOUNDATIONS.md "<concept>"` to get
   `{ concept, stratum, first_needed, depth, prerequisites[] }`. Matching is exact-first, then
   substring; if a short query matches more than one row by substring it resolves to the first
   match, so pass the full concept label to disambiguate.
2. Enrich with the master graph for cross-file links: `graphify explain "<concept>"` (or
   `graphify path "<A>" "<B>"`) for a scoped subgraph. Verify every resolved prerequisite still
   exists in the live graph; drop stale ones.
3. Read the target chapter's "Reader should already know" line in
   `master-graph/.outline/CHAPTER_BIBLE.md` to set assumed background and predicted difficulty.
4. Set target depth (pre-rigorous / rigorous / post-rigorous) from the MATH_FOUNDATIONS depth
   code (I / R / A) and the chapter's role, and derive the concept's learning objectives.

Output — `concept_brief` (assembled across steps 1–4):
`{ concept, stratum, first_needed, depth, prerequisites[], assumed_background[], target_depth, learning_objectives[] }`.
