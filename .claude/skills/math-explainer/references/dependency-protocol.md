# Stage 1 — dependency protocol

1. Run `scripts/resolve_deps.py master-graph/.outline/MATH_FOUNDATIONS.md "<concept>"` to get the stratum, depth, first-needed chapter, and prerequisite list (concept_brief).
2. Enrich with the master graph for cross-file links: `graphify explain "<concept>"` (or `graphify path "<A>" "<B>"`) for a scoped subgraph. Verify every resolved prerequisite still exists in the live graph; drop stale ones.
3. Read the target chapter's "Reader should already know" line in `master-graph/.outline/CHAPTER_BIBLE.md` to set assumed background and predicted difficulty.
4. Set target depth (pre-rigorous / rigorous / post-rigorous) from MATH_FOUNDATIONS depth code (I / R / A) and the chapter's role.
Output: concept_brief = { concept, stratum, first_needed_chapter, depth, prerequisites[], assumed_background[], target_depth }.
