# Evals — triggering and behavior checks

Lightweight evaluation set for the `llm-wiki` skill. Use these to check that the
skill triggers when it should, stays quiet when it shouldn't, and that each
operation behaves correctly. Re-run after editing the description or playbooks.

## Triggering — should fire (one per operation)

1. **Ingest** — "Add this article to my agenticcivthoughts wiki" / "ingest this paper into my knowledge base."
2. **Query** — "What does my wiki say about the LLM Wiki pattern?" / "look up RAG vs persistent KB in my wiki."
3. **Lint** — "Lint my wiki" / "health-check the knowledge base for orphans and broken links."
4. **Init** — "Set up a new llm-wiki here" / "create a wiki for my research."

## Triggering — should NOT fire (negative cases)

- "Summarize this PDF for me." (one-off summary, no wiki)
- "Add a note to this function." (code comment)
- "What does the Kubernetes wiki say about ingress?" (third-party/external wiki)
- "Take meeting notes." (ad-hoc note-taking)

## Self-check for triggering

Ask the model: *"When would you use the llm-wiki skill?"* It should quote the
description and correctly include the four positive cases above and exclude the
negative ones. If it over- or under-triggers, tighten the `description` in
`SKILL.md` (add/clarify trigger phrases or negative triggers).

## Behavioral checks (per operation)

- **Ingest** produces, in ONE atomic commit: a `source` page + ≥1 linked
  `concept`/`entity` page + category `_index.md` updates + a `log.md` line, with
  every claim carrying a provenance marker; `lint.py` reports `0 finding(s)`.
- **Query** reads the index first, answers only from wiki pages with `[[wikilink]]`
  citations, and **abstains** ("I don't have enough in the wiki…") when the wiki
  lacks evidence rather than guessing.
- **Lint** reports the mechanical findings (broken links, orphans, missing
  frontmatter, un-cited claims) and the semantic findings (contradictions, stale
  claims, missing pages, index↔reality drift).
- **Init** creates the skeleton with a schema-marked `CLAUDE.md` and NO stub pages.

## Models

Sanity-check triggering across a small and a large model where feasible (e.g.
Haiku and a frontier model); the description should be unambiguous enough that
both route correctly.

## Scrape / crawl (v0.2.0)

**Should fire scrape/crawl:**
- "Scrape this page into my wiki: <url>" / "ingest this URL and render its JS."
- "Crawl the docs section of <site> into my wiki."
- A bare URL given as the thing to ingest ("add https://… to my wiki").

**Should NOT fire scrape (stays on base ingest):**
- "Ingest this local file `raw/notes.md`." (a file already in `raw/` → base ingest, no scraping)

**Surface gate (negative, critical):**
- On a surface with no network / not local Claude Code (e.g. the API code-execution
  sandbox), a scrape/crawl request must **refuse cleanly** ("scraping needs local Claude
  Code with network") and must NOT hang attempting a browser download.

**Behavioral checks:**
- A fetched page yields a clean `raw/<slug>.md` with `is_verbatim: true`, rich
  frontmatter (`url`, `canonical_url`, `title`, `fetcher`, `content_hash`…), and **no
  boilerplate** (nav/ads/cookie banners stripped by trafilatura).
- A paywalled / JS-empty / non-HTML page is **rejected by the quality gate** (reported,
  not silently written to `raw/`).
- Re-fetching an already-ingested URL (or a `utm_`/`www`/canonical variant, or identical
  content under a different URL) is a **reported skip** (dedup).
- A `crawl` first shows a `--plan-only` plan and waits for confirmation before fetching;
  the real crawl respects `--max-pages`/`--max-depth`/same-domain.
- WebFetch-captured content is stamped `is_verbatim: false` and is **never quoted
  verbatim** in wiki claim lines.

## Paper / PDF route (v0.3.0)

**Should fire paper/PDF preparation:**
- "Extract this paper fixture manifest into raw sources."
- "Prepare these PDFs for ingestion into my wiki."
- "Use `raw/test-vectors/zero-knowledge-papers/manifest.json` as a paper ingest vector."

**Should NOT route PDFs through Scrapling:**
- A direct `.pdf` source is handled by the paper/PDF helper or by local-file ingest
  after extraction, not by `scrape.py fetch`.

**Behavioral checks:**
- `paper_vector.py validate-manifest <manifest> --expected-count 10` reports ten
  valid papers for the Zero Knowledge fixture and fails if any file is missing,
  hash-invalid, non-PDF, page-count-mismatched, path-unsafe, or count-mismatched.
- `paper_vector.py extract-manifest <manifest> --out-dir <wiki>/raw/papers` writes
  page-delimited markdown with `source_type: paper`, copied PDF assets under
  `raw/assets/papers/`, `pdf_sha256`, `pages`, DOI, Semantic Scholar URL, and
  `is_verbatim: true`.
- Re-running `extract-manifest` reports `written: 0` and `skipped: 10` for the same
  fixture.
- Paper claim provenance uses page locators (`p. N`) from the extracted raw markdown.

## Mechanical audit runner

Run this after editing scripts or playbooks:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/audit_checks.py <wiki-root>
```

Expected: direct script tests pass, wiki lint reports `0 finding(s)`, scrape
`crawl --plan-only` succeeds without network, and the paper fixture validates. Manual
model-triggering checks above are still required when changing `SKILL.md` routing text.
