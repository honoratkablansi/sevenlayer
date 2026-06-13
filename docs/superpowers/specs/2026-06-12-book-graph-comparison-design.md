# Second (Book) Knowledge Graph + Comparison + Reference Augmentation — Design Spec

**Date:** 2026-06-12
**Status:** Approved (brainstorm)

## Goal

Build a **second, independent knowledge graph from the book manuscript alone**
(`proving-nothing.md`, split into its 14 chapters), in a separate `book-graph/`
directory that never touches graph 1 (`graphify-out/`). Then **compare** it to
graph 1 to surface what graph 1's references + wiki + deep-mining add beyond the
book's own text. Finally, **augment** the book graph with the 63 bibliography
references (reusing the already-pulled corpus and graph 1's mined reference
nodes; scrapling re-runs only to confirm the corpus).

## Background

- Graph 1 (`graphify-out/`): 1,467 nodes / 4,365 links over manuscript +
  references (45/46 deep-mined) + wiki. Its manuscript contribution is shallow
  (~32 nodes) because the original build treated `proving-nothing.md` as one file.
- The manuscript is one 919 KB file. A single-file extraction extracts shallowly
  (the same problem the dense PDFs had), so we split by chapter.
- Chapter headings in the manuscript are `# Chapter N: ...` (14 of them); `# Part`
  headers and the standalone `# Glossary` / `# Complete Bibliography` are
  separators, not chapters.
- Reference fragments from the deepening already exist at
  `graphify-out/.deepen/frag-*.json`; graph 1's reference nodes are sourced under
  `references/`. These are reused for augmentation — no re-extraction.

## Non-goals

- Not re-extracting or re-pulling references from scratch (reuse the committed
  corpus + already-mined nodes). scrapling runs only as an idempotent confirm.
- Not modifying `graphify-out/`, `references/`, or graph 1 in any way.
- Not including the Glossary or Bibliography in the book graph (the bibliography
  *is* the references, added in the augmentation step).

## Architecture

Build-from-scratch, mirroring the deepening pattern: split → per-chapter agent
extraction → graphify build/cluster/export into `book-graph/`. Compare against
graph 1 with a pure analysis script. Augment by merging graph 1's reference
subgraph into the book graph and rebuilding. All graphify/networkx imports are
**lazy** so the helper modules import cleanly under the venv for testing.

## Components

1. **`scripts/split_manuscript.py`** — `split_chapters(text) -> list[(slug, body)]`.
   Pure: finds `# Chapter N:` headings; each chapter spans from its heading to the
   next top-level `# ` heading (exclusive), so Part separators / Glossary /
   Bibliography bound chapters without being emitted. CLI writes
   `book-graph/.work/ch01..ch14.md`. Unit-tested on a synthetic manuscript.

2. **Chapter extraction (Agent tool)** — one subagent per chapter file. Each reads
   its chapter and emits a graphify fragment `{nodes, edges}`: named concepts,
   entities (people, systems, curves, schemes), claims/arguments, and citations.
   Node ids: `concept_<kebab>` for shared concepts (so they align with graph 1's
   vocabulary and interlink across chapters), `ch<NN>_<kebab>` for
   chapter-specific artifacts. `source_file = "proving-nothing.md"`,
   `source_location = "Chapter N"`, `file_type = "document"`. Confidence
   EXTRACTED/INFERRED/AMBIGUOUS. Fragments → `book-graph/.work/frag-chNN.json`.

3. **`scripts/build_book_graph.py`** — pure `merge_extraction(fragments) ->
   {nodes, edges}` (union nodes by id, union edges, drop dangling) + a `build`
   step (lazy graphify import, system python): `build_from_json` → `cluster` →
   `score_all` → `god_nodes` → `surprising_connections` → `suggest_questions` →
   `generate` → `to_json`/`to_html`/`to_obsidian` into `book-graph/`. Writes
   `book-graph/cost.json`. Agent labels communities afterward (reuse the deepen
   `relabel` pattern).

4. **`scripts/compare_graphs.py`** — pure helpers + a report writer. Loads both
   `graph.json`s. Computes:
   - node/edge/community counts side by side;
   - **concept overlap** by normalized label: shared, book-only, graph-1-only
     (Jaccard similarity);
   - top god nodes in each;
   - headline lists: *concepts graph 1 has that the book's text alone does not*
     (the reference/wiki/deep-mining value-add) and *concepts prominent in the
     book graph but thin in graph 1*.
   Writes `book-graph/COMPARISON.md`. Normalization + set-ops are unit-tested.

5. **Reference augmentation** — `fetch_references.py` re-run (idempotent scrapling
   confirm: 63/63 resolved, tree clean). Then `reference_subgraph(graph1) ->
   {nodes, links}` (pure: nodes whose `source_file` is under `references/` plus
   induced edges) is merged into the book graph via `merge_fragment` (reused from
   `deepen_pdfs.py`), and the book graph is rebuilt. Shared `concept_*` ids link
   the reference knowledge to the chapter concepts. Produces the "book +
   references" graph. The comparison is re-run on this augmented graph too.

## Data flow

`proving-nothing.md` → split → 14 chapter files → 14 fragments → merge → build →
`book-graph/graph.json` (+ report/html/obsidian) → compare vs `graphify-out/graph.json`
→ `COMPARISON.md`. Then: confirm corpus (scrapling) → reference subgraph from
graph 1 → merge into book graph → rebuild → re-compare.

## Output layout

- `book-graph/graph.json`, `GRAPH_REPORT.md`, `graph.html`, `obsidian/`, `cost.json`, `COMPARISON.md` (committed).
- `book-graph/.work/` (chapter splits, fragments, jobs) and any labels/aliases scratch — gitignored; curated label maps force-tracked as in the deepening.

## Error handling

- A chapter subagent returning invalid/empty JSON → skip with a log; if >half
  fail, stop and report.
- `build_book_graph` refuses to write if the merged graph has 0 nodes.
- Comparison tolerates differing schemas (graph 1 uses `links`, fragments use
  `edges`) by normalizing on load.
- Reference merge uses the additive `merge_fragment` (dedup, drop-dangling).

## Testing (TDD)

`tests/test_book_graph.py`: `split_chapters` (14 chapters, correct boundaries,
excludes glossary/bibliography/parts); `merge_extraction` (union/dedup/dangling);
`reference_subgraph` (selects only references/-sourced nodes + induced edges);
`compare_graphs` helpers (label normalization, shared/only-A/only-B set math).
Extraction quality is judged from the built graph, not unit-tested.

## Cost

~14 chapter extraction subagents ≈ 0.5–0.7M tokens. Comparison and reference
augmentation are cheap (reuse; no new extraction). Tracked in `book-graph/cost.json`.

## Risks

- **Vocabulary drift** between the book graph and graph 1 (different `concept_*`
  ids for the same idea) would understate overlap. Mitigation: instruct subagents
  to prefer graph 1's existing concept ids where natural; the comparison
  normalizes labels (not just ids) so synonyms still match.
- **Community renumbering** on rebuild after augmentation → relabel via the
  carry-forward approach used in the deepening.
- graphify API drift → pin to installed version; reuse the deepening's verified calls.
