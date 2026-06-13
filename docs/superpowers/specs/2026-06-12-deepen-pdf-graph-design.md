# Deep PDF Mining for the Knowledge Graph — Design Spec

**Date:** 2026-06-12
**Status:** Approved (brainstorm)

## Goal

Enrich `graphify-out/graph.json` by deeply mining the reference PDFs. Each paper
is currently reduced to 1–6 nodes; mine them into many more
concept / construction / theorem / assumption / citation nodes. The pass is
**additive** (no existing node or edge is removed, so chapter→paper cross-edges
survive) and **staged** (a checkpoint after batch 1 gates the rest).

## Background

- Current graph: **502 nodes / 2,573 links**. References contribute **152 nodes
  across 46 PDFs** (1–6 each); wiki 318, manuscript 32.
- The original build was a single run (**693k input / 239k output tokens**, 238
  files) that chunked 20–25 files per subagent with a generic prompt. Dense
  cryptography papers (e.g. LatticeFold+, Neo, Symphony → 1 node each) were
  reduced to a citation marker rather than mined for content.
- Observed node scheme: each paper has a primary node `ref-NN_slug` (label = full
  title) plus a few shared `concept_<kebab>` nodes linked to it
  (e.g. `ref-07_plonk` ← `concept_permutation-argument`). Shared `concept_*`
  IDs are how distinct papers interlink — the source of cross-paper "surprising
  connections."

## Non-goals

- No re-extraction of the wiki or manuscript (already adequate).
- No global `graphify --mode deep` re-run — it re-spends on wiki+manuscript and
  its merge is additive-only, so it does not target the PDF gap.
- No change to `references/` or `references/manifest.json` (the source-pulling
  artifact stays byte-stable).
- No OCR of scanned/image-only PDFs in batch 1 (the 18 MB GMR scan is deferred
  to a vision-based follow-up).

## Architecture — additive, anchored extraction

1. **Select** a batch of ref ids → resolve to PDF paths via `references/manifest.json`.
2. **Anchors:** for each paper, look up existing node IDs in `graph.json` — the
   primary `ref-NN_slug` plus any `concept_*` already linked to it.
3. **Extract:** dispatch one Agent per paper (parallel, capped by the runtime).
   Each reads the full PDF and emits a JSON fragment `{nodes, edges}` matching
   graphify's schema, linking new nodes to the anchors and to shared
   `concept_<kebab>` nodes.
4. **Merge** fragments additively into a working copy of the graph: union nodes
   (dedup by id), union edges (dedup by `(source, target, relation)`), drop edges
   whose endpoints are absent.
5. **Rebuild** via graphify's own library functions (`cluster`, `score_all`,
   `god_nodes`, `surprising_connections`, `generate`, `to_json`, `to_html`,
   `to_obsidian`) — clustering/reporting is not reimplemented.
6. **Bookkeep:** refresh `graphify-out/manifest.json` semantic_hash for mined
   PDFs; append a run to `graphify-out/cost.json`.
7. **Checkpoint:** emit a delta report; the user decides on the remaining papers.

## Components

- `scripts/deepen_pdfs.py` — pure helpers + a thin orchestrator that consumes
  pre-collected fragment files. Pure, unit-tested helpers:
  - `batch_for_ids(manifest, ids)` → `[(id, pdf_path, slug, chapters)]`; skips
    `duplicate_of` and non-`paper` entries.
  - `anchors_for_source(graph, source_file)` → list of existing node IDs for that PDF.
  - `merge_fragment(graph, fragment)` → merged graph (union/dedup/drop-dangling;
    enforces the additive invariant: node count never decreases).
  - `graph_stats(graph)` → `{nodes, edges, nodes_by_source_top, nodes_per_pdf}`.
- **Agent extraction** (per graphify's mandate to use the Agent tool): subagents
  dispatched with a fixed prompt (schema + anchors + depth instructions).
  Fragments persisted to `graphify-out/.deepen/frag-refNN.json` (gitignored).
- **Rebuild step** — a scripted call into graphify's library mirroring SKILL.md
  Steps 4–6 and 9, operating on the merged graph.

## Subagent extraction contract

Each subagent receives: the PDF repo-relative path, the paper's anchor node IDs,
its chapter numbers, and the exact node/edge JSON schema. It must:

- Read the **full** PDF (page ranges as needed for length).
- Emit nodes for the paper's key **constructions, schemes, theorems/lemmas,
  security assumptions, complexity/efficiency claims, and named prior works it
  cites**.
- Use `concept_<kebab>` IDs for general/shared concepts (so they merge across
  papers via dedup) and `ref-NN_<kebab>` IDs for paper-specific artifacts.
- Emit an edge linking every new node to an anchor — relation in
  {`defines`, `introduces`, `proves`, `assumes`, `cites`, `conceptually_related_to`,
  `shares_data_with`} — with confidence `EXTRACTED|INFERRED|AMBIGUOUS` and a
  `source_location` (section or page).
- Set `source_file` = the PDF's repo-relative path on every node.
- Target ~10–25 nodes/paper. Output ONLY JSON — no prose, no fences.

## Merge semantics (testable)

- **Nodes:** dict keyed by `id`. On conflict, keep the existing node but fill
  missing fields from the fragment (anchors preserved). New IDs are added.
- **Edges:** set keyed by `(source, target, relation)`; deduped; any edge whose
  `source` or `target` is not in the merged node set is dropped.
- **Determinism:** stable ordering so `graph.json` diffs are reviewable.
- **Invariant:** merged node count ≥ prior node count, else fail loudly.

## Error handling

- Subagent returns invalid/empty JSON → skip that paper, log it, continue. If
  more than half a batch fails, stop and report.
- Anchor missing for a paper → still add nodes; anchor to `ref-NN_slug` if
  present, else synthesize it from the manifest citation.
- Scanned/image-only PDF → excluded from batch 1; flagged for vision follow-up.
- Rebuild refuses to write outputs if the additive invariant is violated.

## Testing (TDD)

`tests/test_deepen_pdfs.py`, written failing-first:
- `batch_for_ids` resolution, incl. `duplicate_of` and stub skip.
- `anchors_for_source` returns the right IDs and `[]` for unknown sources.
- `merge_fragment` union, dedup, dangling-edge drop, and additive-invariant
  enforcement.
- `graph_stats` counts (total, per-PDF, by-top-source).

Extraction *quality* is judged at the checkpoint, not unit-tested.

## Staging & checkpoint

**Batch 1** = ref ids `[4, 6, 7, 8, 9, 12, 16, 17, 18, 20]` — KZG, Groth16,
PLONK, STARK, Bulletproofs, under-constrained circuits, Jolt, Nova, HyperNova,
LatticeFold (dense, text-native ePrint papers across chapters 2, 3, 6).

After merge + rebuild, report:
- total nodes/edges before→after; nodes-per-paper before→after for the 10;
- new god nodes; new cross-community edges; sample surprising connections;
- estimated token cost (appended to `cost.json`; approximate — the Agent tool
  does not return exact per-subagent counts);
- two sanity queries, e.g. `graphify explain "PLONK"` and
  `graphify query "What soundness assumptions do the folding schemes rely on?"`.

**Gate:** proceed to the remaining ~36 PDFs only on user approval.

## Cost

Batch 1 ≈ 200–400k tokens (10 papers × full read + structured output). Full
corpus ≈ ~1M tokens if continued. Tracked in `cost.json`.

## Reproducibility

Fragments persist under `graphify-out/.deepen/` (gitignored). `deepen_pdfs.py`
is rerunnable with `--only <ids>`; merge is idempotent (re-merging the same
fragment is a no-op via dedup).

## Risks

- **Over-generation** of low-value nodes → cap ~25/paper, require
  `source_location`, tag uncertain edges `AMBIGUOUS`.
- **Shared-concept collisions** are usually desirable (cross-links), but two
  distinct concepts sharing a kebab name would merge wrongly → subagents use
  precise concept names.
- **graphify API drift** → pin to the installed version; the rebuild mirrors the
  SKILL.md calls.
