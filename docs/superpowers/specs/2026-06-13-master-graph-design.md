# Master Knowledge Graph: Merge + Citation Snowball + Concept Extraction — Design Spec

**Date:** 2026-06-13
**Status:** Approved (brainstorm)

## Goal

Unify the three existing knowledge graphs into one **master graph** under
`master-graph/`, grow it by **snowballing citations** out of the already-fetched
reference papers, then use the master graph to **extract the main concepts that
should be in the book** — ranked, with per-chapter coverage gaps.

The three inputs:

| Graph | Nodes | Edges | Source |
|---|---|---|---|
| `book-graph/` | 1513 | 2389 | 14 manuscript chapters + graph-1 reference subgraph |
| `recursion-graph/` | 1200 | 2174 | recursion outline + recursion reference PDFs |
| `graphify-out/` (graph 1) | 1467 | 4365 | wiki + references + deep-mining |

They share the graphify NetworkX node-link schema (`nodes`/`links`, per-node
`community`, `hyperedges`), and `concept_*` ids derive from the normalized label,
so exact cross-graph concept duplicates already collapse on a union by `id`.

## Background

- Reusable, tested building blocks already exist in `scripts/`:
  - `build_book_graph.merge_extraction` — union extraction fragments by id.
  - `deepen_pdfs.merge_fragment` — additive union of a fragment into a node-link
    graph (existing-wins by id; union edges by `(source,target,relation)`; drop
    dangling; additive invariant).
  - `deepen_pdfs.consolidate_nodes(graph, alias_map)` — collapse alias ids into a
    canonical id, redirect edges, drop self-loops/dangling. **Reduces** node count.
  - `deepen_pdfs.rebuild(graph, n_files)` — re-cluster + regenerate all graphify
    outputs (graph.json, GRAPH_REPORT.md, graph.html, obsidian).
  - `graphify.analyze.god_nodes` / `surprising_connections` / `suggest_questions`.
- `scripts/fetch_references.py` fetches `paper`/`web`/`stub` entries (two-tier
  scrapling + Camoufox Cloudflare stealth tier) driven by a manifest, and accepts
  `--manifest PATH` for an alternate corpus.
- Two manifests exist: `references/manifest.json` (book chapters) and
  `references/recursion/manifest.json` (93 recursion entries). Entry shape:
  `{id, slug, citation, chapters:[...], type, url?, file, status}` (+ optional
  `reuse`/`duplicate_of`).
- All graphify/networkx imports in the scripts are **lazy** so the helper modules
  import under the venv for testing; build/rebuild run under the system Python
  that has graphify installed.

## Decisions (locked in brainstorm)

1. **Master artifact:** new `master-graph/` directory. The three inputs are left
   untouched as provenance and baselines (Approach A; rejected augmenting
   `graphify-out/` in place, which would destroy the comparison baseline and
   reproducibility).
2. **Citation expansion:** iterative snowball, bounded by
   `MAX_ROUNDS = 3`, `MIN_NEW_PER_ROUND = 10` (convergence), `HARD_CAP = 150`
   total new fetches. Stop when **any** limit is hit.
3. **Relevance filter:** hybrid — free lexical prefilter against the master graph's
   concept vocabulary + a ZK keyword list, then an LLM relevance judge on the
   survivors only.
4. **Dedup aggressiveness:** deterministic normalization for mechanical variants
   (lowercase, strip plural/possessive, collapse punctuation/whitespace) **plus**
   a bounded LLM synonym pass on high-degree (hub) nodes only.
5. **Concept-extraction output:** `master-graph/CONCEPTS_FOR_BOOK.md` — concepts
   ranked by centrality / god-node status / reference support, each tagged
   well-covered / under-covered / absent vs the manuscript, with a per-chapter
   rollup.

## Non-goals

- No chapter prose; no edits to `proving-nothing.md` or the wiki.
- No modification of `book-graph/`, `recursion-graph/`, or `graphify-out/` (read-only inputs).
- No change to how graphify itself builds the per-corpus graphs.
- Concept extraction *recommends* concepts; it does not write them into the book.

## Architecture

A new, isolated `master-graph/` workspace built by reusing the main-book tooling.
Four stages run in order; stages 1, 3, 4 are deterministic Python over node-link
JSON, stage 2 is the bounded snowball loop that mixes Python (parse/filter/fetch)
with subagent passes (LLM judge, concept extraction). All graphify/networkx
imports stay lazy.

New module: `scripts/build_master_graph.py` with subcommands
`merge` / `consolidate` / `snowball-plan` / `snowball-merge` / `relabel` /
`concepts`, mirroring the existing builders. Pure helpers live alongside the
graphify-dependent commands and are unit-tested.

## Components

### Stage 1 — Merge → `master-graph/`

1. Load the three `graph.json`. Start from an empty node-link graph; fold each
   input in with `merge_fragment` (treating each input's `nodes` + `links` as a
   fragment). Exact-id duplicates collapse automatically.
2. Build a deterministic `alias_map`: group nodes by a normalized label key
   (lowercase; strip trailing `s`/`'s`/`(s)`; collapse non-alphanumerics to single
   space; trim); within a group, the highest-degree node is canonical, the rest
   are aliases. Pure function `build_alias_map(graph) -> dict`, unit-tested.
3. **Hub LLM synonym pass:** for the top-N highest-degree nodes (default N=100),
   an LLM judge proposes additional same-concept merges across *different*
   normalized keys (e.g. "KZG commitment" ≡ "Kate commitment"). Output appended to
   `alias_map`; persisted to `master-graph/.work/aliases.json` for review/replay.
4. `consolidate_nodes(graph, alias_map)` then `rebuild` → `master-graph/`
   (`graph.json`, `GRAPH_REPORT.md`, `graph.html`, `obsidian/`), plus
   `.work/communities.json` for labeling and a `relabel` command for names.

Provenance: every merged node keeps its origin via a new `origin_graphs: []`
field (which inputs contributed it); `merge_fragment` is extended to record this
without changing its additive invariant.

### Stage 2 — Citation snowball (bounded loop)

State persisted in `master-graph/.snowball/state.json`:
`{round, total_fetched, mined_files: [...], frontier: [...]}` so rounds are
resumable and the hard cap is enforced across rounds.

Per round:

1. **Parse citations.** Extend the concept-extraction subagent output schema to
   also emit `citations: [{title, authors?, venue?, year?, url?}]`. The frontier
   (papers fetched in the previous round, or all existing papers on round 0) is
   mined for both concepts and citations in one pass. `parse_citations` (pure)
   normalizes raw subagent output into candidate records.
2. **Lexical prefilter** (pure, free): keep a candidate iff its title/venue hits
   the master graph's concept vocabulary or a curated ZK keyword list. Drops
   obvious off-topic works before any API spend.
3. **LLM relevance judge** (subagent) on survivors only → keep/drop with a reason.
4. **Manifest dedup** (pure): drop candidates whose normalized title or URL
   already appears in either manifest or in earlier snowball entries.
5. **Append entries** to the relevant manifest (recursion candidates →
   `references/recursion/manifest.json`; others → `references/manifest.json`) with
   the standard shape plus provenance `discovered_from: <ref_id>`,
   `snowball_round: <n>`. `paper` if a PDF URL resolves, else `web`, else `stub`.
6. **Fetch** the new entries via `fetch_references.py --manifest <path> --only <ids>`.
7. **Extract** concepts+citations from newly fetched papers (one subagent per PDF;
   web captures get the lighter extractor) → fragments under
   `master-graph/.snowball/frag-*.json`; `merge_fragment` each into the master.
8. **Update state** and **check stop:** `round+1 == MAX_ROUNDS` OR
   `new_relevant_this_round < MIN_NEW_PER_ROUND` OR `total_fetched >= HARD_CAP`.
   The frontier for the next round = papers fetched this round. When the cap is
   hit mid-round, remaining candidates are dropped and **logged** (no silent
   truncation).

### Stage 3 — Re-consolidate + rebuild

After the loop, rerun the Stage-1 dedup (deterministic + hub LLM pass) over the
grown master and `rebuild`, since snowball adds new variant labels worth
collapsing once at the end.

### Stage 4 — Concept extraction → `master-graph/CONCEPTS_FOR_BOOK.md`

1. **Score** each concept node by a blend of: degree centrality, god-node status
   (`graphify.analyze.god_nodes`), and **reference support** = count of distinct
   reference `source_file`s linked to the concept. `score_concepts` (pure over the
   node-link dict) returns a ranked table.
2. **Coverage diff:** a concept is *covered* if a node with its normalized label
   has `source_file == proving-nothing.md` or a `wiki/chapters/*` file. Map each
   concept to chapters via its linked chapter/`chNN`/source-location nodes.
   Verdict: **well-covered** (in manuscript, high support), **under-covered** (in
   manuscript but thin support / many refs), **absent** (refs-only, not in
   manuscript). `coverage_diff` is pure and unit-tested.
3. **Render** `CONCEPTS_FOR_BOOK.md`: a ranked master table (concept, community,
   support, centrality, verdict) followed by a per-chapter rollup listing each
   chapter's under-covered and absent concepts. Generalizes the hand-built
   "what graph 1 knows that the book does not" section of `book-graph/COMPARISON.md`.

## Data flow

```
book-graph + recursion-graph + graphify-out
   → merge_fragment (union by id)
   → build_alias_map (+ hub LLM pass)
   → consolidate_nodes → rebuild → master-graph/        [Stage 1]

frontier papers → extract (concepts + citations)
   → lexical prefilter → LLM judge → manifest dedup
   → append manifest entries → fetch_references
   → extract new papers → merge_fragment → (loop) [Stage 2, ≤3 rounds / 150 cap]

grown master → re-consolidate → rebuild                  [Stage 3]
   → score_concepts + coverage_diff → CONCEPTS_FOR_BOOK.md [Stage 4]
```

## Output layout

- `master-graph/graph.json`, `GRAPH_REPORT.md`, `graph.html`, `obsidian/`,
  `cost.json`, `CONCEPTS_FOR_BOOK.md` (committed).
- `master-graph/.work/` (aliases.json, communities.json) — gitignored; curated
  `labels.json` force-tracked.
- `master-graph/.snowball/` (state.json, fragments, judge logs) — gitignored;
  `state.json` force-tracked for provenance.
- New `references/**` entries + fetched files (committed corpus growth).
- `scripts/build_master_graph.py`, `tests/test_master_graph.py`.

## Error handling

- Subagent returns invalid/empty JSON → skip + log; >half fail in a round → stop the loop.
- Fetch failures triaged as in the main pipeline: bad URL → fix + retry; hard
  bot-wall → convert the entry to `stub` (concept still enters the graph as a node).
- `consolidate_nodes` never drops a canonical node; alias maps are validated
  (no canonical that is itself an alias; no cycles) before consolidation.
- `rebuild` refuses to write a 0-node graph.
- Hard cap and convergence are enforced on persisted state, so a crashed/resumed
  run cannot exceed 150 fetches.

## Testing (TDD)

`tests/test_master_graph.py` covers the pure helpers:
- `merge_fragment` origin-tracking + additive invariant across the three inputs.
- `build_alias_map` (plural/punctuation normalization; canonical = highest degree).
- alias-map validation (rejects cycles / alias-as-canonical).
- `parse_citations` and the lexical prefilter (keyword/vocabulary hit logic).
- manifest dedup (normalized title/URL collision).
- `score_concepts` and `coverage_diff` (covered / under-covered / absent verdicts).

graphify-dependent commands (`merge`/`consolidate`/`relabel`/`concepts` rebuild)
stay behind the lazy-import boundary and are exercised by a smoke build, not unit
tests. LLM judge and extraction subagents are orchestration, judged from outputs.

## Cost

Stage 1 + hub LLM pass: ~150 judge prompts (small). Stage 2: ≤3 rounds, ≤150 new
fetches, one LLM-judge call per lexical survivor + one extraction subagent per new
paper — order 1–4M tokens depending on how fast the frontier dries up. Cap of 150
papers bounds the worst case. Tracked in `master-graph/cost.json`.

Execution dispatches extraction/judge subagents via the Agent tool (the existing
"one subagent per job" pattern). If the user opts into multi-agent orchestration,
the snowball rounds can instead run as a single Workflow (fan-out fetch+extract per
round, barrier at the stop-check); not assumed here.

## Risks

- **Snowball drift** — citations pull the graph toward tangential subfields. Mitigated
  by the hybrid relevance gate and the 150 cap; the LLM judge is given book context.
- **Open-access resolution** — some cited papers have no free copy → `stub` nodes,
  logged so coverage is honest.
- **Vocabulary drift** vs the existing graphs → extraction subagents instructed to
  reuse standard `concept_*` ids; the dedup pass absorbs residual variants.
- **Over-merging in dedup** — the hub LLM pass could merge distinct concepts.
  Mitigated by persisting `aliases.json` for review before the final rebuild and by
  limiting the LLM pass to hub nodes.
- **graphify API drift** → pin to the installed version; reuse already-verified calls.
