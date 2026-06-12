<!-- llm-wiki: v1 -->
# {{WIKI_NAME}} — wiki schema

**Domain:** {{DOMAIN}}

This repository is an LLM-maintained knowledge wiki (Karpathy "LLM Wiki" pattern).
The `llm-wiki` skill operates it. Humans curate sources and ask questions; the
LLM writes and maintains all pages.

## Layout
- `raw/` — immutable source documents (never edited). `raw/assets/` for images.
- `wiki/sources|entities|concepts|syntheses/` — LLM-generated pages (+ `_index.md` each).
- `wiki/maps/` — topic MOCs. `wiki/overview.md` — evolving thesis (root MOC).
- `index.md` — router to category indexes. `log.md` — append-only history.

## Workflows
- Ingest / Query / Lint / Init are defined by the `llm-wiki` skill. Follow it.

## Conventions (summary; full rules in the skill's references/conventions.md)
- `[[wikilinks]]`; unique titles; every page ≥1 link + in a MOC + category index.
- Every claim carries an inline provenance marker to a `raw/` source.
- Contradictions append + flag (`status:` + `> [!conflict]`), never overwrite.
- One atomic git commit per ingest.
- Scraped sources (produced by the optional scrape op) carry `url`, `canonical_url`, `fetched_at`, and `is_verbatim` provenance fields; `is_verbatim: false` sources (WebFetch) may be paraphrased but never quoted verbatim.
