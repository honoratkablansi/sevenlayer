# Recursion Chapters: Reference Gathering + Deep Knowledge Graph — Design Spec

**Date:** 2026-06-13
**Status:** Approved (brainstorm)

## Goal

For the three planned new chapters on **Recursive Proof Composition** (outline at
`recursion/recursion-outline.md`): gather every citeable reference into a separate
`references/recursion/` corpus via scrapling (reusing the ~8 papers already in the
main corpus), then build a **deep** knowledge graph in `recursion-graph/` from the
outline + the deeply-mined references.

This is the *first* step toward adding the chapters. Writing chapter prose and
merging into `proving-nothing.md` is out of scope here.

## Background

- The outline (currently on the user's Desktop) is an annotated 3-chapter outline:
  Ch1 surveys recursion, Ch2 is a folding deep-dive, Ch3 covers applications. Each
  of ~50 subsections carries 1–4 references.
- ~60 distinct citeable sources: mostly academic papers (ePrint/arXiv + venue
  papers from CRYPTO/S&P/CCS/STOC/TCC that resolve to open-access copies), ~20 web
  docs/blogs, ~10 vague "literature" mentions.
- **~8 papers already in the main corpus** (Nova, HyperNova, ProtoStar,
  LatticeFold, LatticeFold+, CCS, Circle STARKs, STARK, Jolt) — reuse, do not
  re-download or re-extract.
- The main-book pipeline is hardened and reused: `scripts/fetch_references.py`
  (two-tier scrapling + Camoufox Cloudflare stealth tier), the deepening pattern
  (one subagent per PDF), and `scripts/build_book_graph.py` (`merge_extraction` +
  `_export`).

## Non-goals

- No chapter prose; no edits to `proving-nothing.md`; no merge into the book.
- No cross-graph comparison (can follow later).
- No modification of the existing `references/`, `graphify-out/`, or `book-graph/`.
- No re-download or re-extraction of the ~8 overlapping papers.

## Architecture

A from-scratch corpus + deep graph, isolated under `references/recursion/` and
`recursion-graph/`, built by reusing the main-book tooling. All graphify/networkx
imports stay lazy so helper modules import under the venv for testing.

## Components

1. **Outline in-repo** — copy `recursion_book_outline.md` →
   `recursion/recursion-outline.md` (version-controlled). A splitter
   (`scripts/split_recursion_outline.py`, pure + tested) splits it into 3 chapter
   files `recursion-graph/.work/rc01..rc03.md` by `## Chapter N:` headings.

2. **`references/recursion/manifest.json`** — hand-curated from the outline.
   Entry shape mirrors the main manifest: `{id, slug, citation, chapters:[1|2|3],
   type, url?, file, status}`. Types:
   - `paper` — PDF, `url` resolved to an open-access copy (ePrint
     `eprint.iacr.org/YYYY/NNN.pdf`, `arxiv.org/pdf/<id>`, author copy).
   - `web` — docs/blogs (Polygon, RISC Zero, Succinct, Mina, Ethereum Foundation,
     SLSA/in-toto, C2PA, W3C VC, RFC 6962, library docs) → markdown capture.
   - `stub` — vague "literature" mentions and any paper with no open copy
     (e.g. possibly Valiant TCC'08, Bitansky STOC'13, Pedersen'91) → named node, no file.
   - `reuse` field — for the ~8 overlaps, points at the existing main-corpus PDF
     (e.g. `references/ch06/ref-17-nova.pdf`); fetch skips it and the graph reuses
     its existing deep fragment.
   A `tests/test_recursion_manifest.py` validates shape (unique ids/slugs, valid
   types, file-path convention `references/recursion/ch{N}/ref-{id:02d}-{slug}.{ext}`,
   reuse entries point at existing files).

3. **Fetch** — `scripts/fetch_references.py` gains a `--manifest PATH` flag (and
   derives the corpus root from it) so it runs unchanged on the recursion manifest.
   `reuse` entries are treated as already-present (no network). Existing 17 fetch
   tests stay green; one new test covers `--manifest` resolution.

4. **Deep extraction (Agent tool)** — one subagent per *new* reference PDF
   (deep-mine: constructions/theorems/assumptions/citations, `concept_<kebab>`
   shared ids aligned to the existing graphs) → `recursion-graph/.work/frag-ref-NN.json`;
   one per outline chapter (3) → `frag-rcNN.json`. For the 8 overlaps, copy their
   existing fragment from `graphify-out/.deepen/frag-NN.json` (zero re-extraction).
   Web captures get a lighter concept-extraction subagent.

5. **Build `recursion-graph/`** — `scripts/build_recursion_graph.py` reuses
   `build_book_graph.merge_extraction` to union all fragments, then graphify
   `build_from_json` → cluster → export (graph.json, GRAPH_REPORT.md, graph.html,
   obsidian) + a `relabel` step for community names. Pure merge logic is tested;
   graphify calls are lazy (system python).

## Data flow

outline → copy in-repo → split (3 chapters) ; outline references → curate manifest
→ fetch (scrapling, reuse overlaps) → corpus. Then: per-source deep extraction
(+ reuse overlap/outline fragments) → merge → build → `recursion-graph/`.

## Output layout

- `recursion/recursion-outline.md` (committed).
- `references/recursion/manifest.json` + `references/recursion/ch1|ch2|ch3/*` (committed corpus).
- `recursion-graph/graph.json`, `GRAPH_REPORT.md`, `graph.html`, `obsidian/`, `cost.json` (committed).
- `recursion-graph/.work/` (outline splits, fragments, jobs, communities) — gitignored; curated `labels.json` force-tracked.

## Error handling

- Subagent returns invalid/empty JSON → skip + log; >half fail → stop.
- Fetch failures triaged as in the main pipeline: bad URL → fix + retry; hard
  bot-wall → convert entry to `stub`.
- Build refuses to write a 0-node graph.
- `reuse`/`stub` entries never hit the network.

## Testing (TDD)

`tests/test_recursion_manifest.py` (manifest shape + reuse pointers);
`tests/test_recursion_graph.py` (outline splitter; `--manifest` root resolution in
fetch; merge of fragments). Extraction quality judged from the built graph.

## Cost

~50 new scrapling fetches + deep-mining ~50 papers ≈ 2–4M tokens. Overlap reuse (8
papers) and outline reuse avoid extra spend. Tracked in `recursion-graph/cost.json`.

## Risks

- **Open-access resolution**: some venue/older papers may lack a free copy →
  stubs, logged so coverage is honest.
- **Vocabulary drift** vs the existing graphs → subagents instructed to reuse
  standard `concept_*` ids (folding-scheme, ivc, pcd, accumulation, nova, …).
- **graphify API drift** → pin to installed version; reuse verified calls.
