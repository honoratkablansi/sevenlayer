# Knowledge Graph + Reference Corpus — Design

**Date:** 2026-06-12
**Status:** Approved (approach A, manifest-driven pipeline)
**Goal:** Download every reference cited in *Proving Nothing* per chapter using Scrapling, then build a queryable knowledge graph of the entire book (manuscript + references + wiki) using Graphify.

## Context

- The bibliography lives in `wiki/BIBLIOGRAPHY.md`: 65 numbered references grouped by chapter. Numbering has at least one gap (no ref 34) and some refs are cited in multiple chapters (e.g. 12/47, 13/48).
- Reference types: ~40 academic papers (ePrint/arXiv/conference — direct PDF URLs derivable), ~15 web pages (blogs, vendor docs, trackers), ~5 print-only or paywalled (books, proprietary reports).
- Tooling already installed in the repo `.venv`: `scrapling[fetchers]` 0.4.9 (with Camoufox/Playwright browsers) and `graphifyy` 0.8.39; the Graphify skill is registered at `.claude/skills/graphify/SKILL.md`.
- The repo has a curated wiki (`wiki/chapters`, `wiki/concepts`, `wiki/sections`, `wiki/_meta`) from the 2026-04-18 wiki project. It is part of the graph corpus.

## Decisions (user-confirmed)

1. **Corpus:** manuscript + downloaded references + existing `wiki/`.
2. **Layout:** `references/ch01` … `references/ch14`, files named `ref-NN-slug.{pdf,md}`. Multi-chapter refs are stored once (first citing chapter); the manifest records all chapters.
3. **Form:** papers as PDFs; web pages as cleaned markdown with citation front-matter; print-only/paywalled refs as stub `.md` files carrying full citation metadata (so they still become graph nodes).
4. **Persistence:** references and `graphify-out/` are committed (book is CC-BY; expect ~100–200 MB of PDFs). The fetch step is a rerunnable script.

## Components

### 1. Reference manifest — `references/manifest.json`

Source of truth, generated once by parsing `wiki/BIBLIOGRAPHY.md` and reviewed by hand. One entry per reference:

```json
{
  "id": 6,
  "slug": "groth16",
  "citation": "Groth, Jens. \"On the Size of Pairing-Based Non-interactive Arguments.\" EUROCRYPT 2016.",
  "chapters": [2],
  "type": "paper",
  "url": "https://eprint.iacr.org/2016/260.pdf",
  "file": "references/ch02/ref-06-groth16.pdf",
  "status": "pending"
}
```

- `type`: `paper` (PDF download) | `web` (fetch → markdown) | `stub` (no download; generate citation stub).
- URL resolution: ePrint IDs `YYYY/NNN` → `https://eprint.iacr.org/YYYY/NNN.pdf`; arXiv IDs → `https://arxiv.org/pdf/<id>`; explicit URLs as printed. Papers with no ePrint/arXiv ID get a resolved open-access URL during manifest curation, or fall back to `stub`.
- `status`: `pending` | `ok` | `ok-stealth` (StealthyFetcher fallback used) | `stub` | `failed`.

### 2. Fetch script — `scripts/fetch_references.py`

Runs under the repo `.venv`. Behavior:

- Iterates the manifest; skips entries whose `file` already exists (unless `--force`).
- `paper`: download with Scrapling `Fetcher` (curl_cffi browser impersonation); verify content-type/magic bytes are PDF; on 403/bot-block, retry with `StealthyFetcher` (Camoufox headless).
- `web`: fetch with the same two-tier strategy; extract main content; save as markdown with YAML front-matter holding the full citation, ref id, source URL, and fetch date.
- `stub`: write `ref-NN-slug.md` containing the citation metadata and a note that the source is print-only/paywalled.
- Writes per-entry `status` back to the manifest after each attempt; exits non-zero if any entry remains `pending`/`failed`. CLI: `--force`, `--only <id,...>`, `--dry-run`.

### 3. Graph build — Graphify

- Invoke the registered `/graphify` skill with the repo `.venv` active (the skill's self-install step calls bare `pip`; the venv must be on PATH).
- Corpus = `proving-nothing.md` + `references/` + `wiki/`. Build artifacts (fonts, `.tex`, the book's own PDF/EPUB, `src/`, build scripts) must stay out of the graph. Preferred: Graphify's ignore/exclude mechanism (check `graphify --help` at build time). Fallback: assemble a staged `corpus/` directory containing copies/links of the three inputs and run Graphify on that.
- Standard mode first (not `--mode deep`); `--update` for future incremental rebuilds.
- Outputs committed: `graphify-out/` (interactive HTML, `graph.json`, `GRAPH_REPORT.md` with EXTRACTED/INFERRED/AMBIGUOUS audit trail).

### 4. Verification

- **Manifest completeness:** every numbered reference in `wiki/BIBLIOGRAPHY.md` appears in the manifest exactly once; after the run, no entry is `pending` or `failed`; every `file` path exists on disk.
- **Fetch idempotency:** a second run downloads nothing and exits 0.
- **PDF integrity:** all `paper` files start with `%PDF` magic bytes.
- **Graph sanity:** `graphify query` spot-checks (e.g. KZG should connect chapter 2/6 content with `wiki/concepts/kzg.md` and ref 4); review `GRAPH_REPORT.md` for a reasonable EXTRACTED:INFERRED ratio and for corpus pollution (no font/build-artifact nodes).

## Error handling

- Download failures after both fetcher tiers: mark `failed` in the manifest, continue with remaining refs, report at the end. Failed web refs may be demoted to `stub` by hand so the graph still gets a node.
- Bibliography parse ambiguities (e.g. refs without URLs) are resolved during manifest curation, not silently guessed by the script.
- Graphify corpus pollution discovered in the report → switch to the staged `corpus/` fallback and rebuild.

## Out of scope

- Deep-mode graph extraction (`--mode deep`) — possible later via `--update`.
- Converting paper PDFs to markdown.
- Neo4j export, MCP server, or watch mode.
- Restructuring the existing wiki.

## Git

Milestone commits (manifest, downloads + script, graph outputs) with repo-local author `Charles Hoskinson <Charles.Hoskinson@gmail.com>`.
