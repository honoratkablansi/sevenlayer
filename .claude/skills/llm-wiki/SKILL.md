---
name: llm-wiki
description: Builds and maintains a persistent, interlinked Obsidian-compatible markdown knowledge wiki in a git repo via three operations — ingest a source into linked pages, answer a question from the accumulated wiki with citations, and lint the wiki for orphans, broken links, and contradictions. Use when the user asks to ingest or add a source into their wiki or knowledge base, init or grow such a wiki, ask what their wiki says about a topic, or lint and health-check it. Do not use for ad-hoc note-taking, code comments, or querying third-party or external wikis.
compatibility: Base wiki ops need git (+ Python 3 for optional scripts). Web scraping (fetch/crawl) is optional and works only in local Claude Code with network access — install Scrapling + trafilatura + a headless browser. Paper/PDF extraction needs pypdf. Scraping is unavailable on the Claude API sandbox (no network/installs) and unreliable on claude.ai.
allowed-tools: Bash(python3 *)
metadata:
  version: "0.3.0"
  author: Charles Hoskinson
---

# LLM Wiki

Knowledge is compiled once on ingest and kept current, so synthesis, cross-references, and contradictions already exist before any question is asked — the opposite of query-time RAG, where the model re-derives everything from raw chunks on every query.

## The three layers

- **Raw sources** (`raw/`) — immutable files; capture operations may create them, then Claude reads them and never mutates them; the only ground truth.
- **The wiki** (`wiki/`) — LLM-generated, LLM-owned markdown pages derived entirely from raw sources and git history.
- **The schema** (`CLAUDE.md`) — tells Claude how this wiki is structured and which workflows to follow; co-evolves with the user.

## Finding the wiki

A directory is a wiki if and only if it contains a `CLAUDE.md` whose first non-empty line carries the marker `<!-- llm-wiki: v1 -->` **and** a `wiki/` folder. Resolution order: (1) explicit path provided by the user; (2) walk up from the current working directory to the first directory matching both conditions. The `init` operation creates a new wiki at any target path — nothing in this skill is hardcoded to a specific repo.

## Operations (router)

Read the corresponding reference file before executing any operation:

- **init** — user says "set up a wiki here", "create a wiki", or similar → read `references/operations/init.md`
- **ingest** — user says "add this source", "ingest this", "process this file/paper/PDF into my wiki" (for a local file in `raw/`) → read `references/operations/ingest.md`
- **scrape / crawl** — user says "scrape this page", "crawl this site/section", "ingest this URL", "render JS", "fetch this link" → read `references/operations/scrape.md` (plain file ingest stays on the **ingest** entry above)
- **query** — user says "what does my wiki say about X", "look up X in my wiki" → read `references/operations/query.md`
- **lint** — user says "lint the wiki", "health-check the wiki", "find orphans/broken links" → read `references/operations/lint.md`

When the intent is ambiguous, ask the user which operation they want before proceeding.

## Conventions

Before authoring any wiki page, read `references/conventions.md` for page types, link discipline, frontmatter schema, provenance markers, contradiction handling, naming/dedup rules, and MOC/index discipline. For Obsidian settings, Dataview queries, Web Clipper mapping, `.gitignore` setup, and optional Marp usage, read `references/obsidian-setup.md`.

## Skill files

This skill expects these files to exist (open them as needed; if one is missing, the skill is incomplete):

- `references/operations/{init,ingest,query,lint}.md` — one playbook per operation
- `references/operations/scrape.md` — fetch/crawl playbook (optional, Claude Code only)
- `references/conventions.md` — page types, links, frontmatter, provenance, contradictions, naming/dedup, MOC/index
- `references/obsidian-setup.md` — Obsidian/Dataview/Web Clipper/`.gitignore`/Marp
- `assets/page-templates/{source,concept,entity,synthesis,map}.md` and `assets/{schema,index,category-index,log}-template.md` — templates used by `init` and `ingest`
- `scripts/lint.py` — optional mechanical lint accelerator (lint also works manually)
- `scripts/scrape.py` — optional web fetch/crawl script (Scrapling + trafilatura; Claude Code only)
- `scripts/paper_vector.py` — optional PDF paper fixture/extraction helper (pypdf)
- `scripts/audit_checks.py` — optional local mechanical audit runner

**Changelog — v0.2.0 (additive):** optional Scrapling+trafilatura web scrape/crawl on-ramp; base v1 operations unchanged.
**Changelog — v0.3.0 (additive):** paper/PDF extraction helper, enforced scrape duplicate skips, response content-type quality gating, crawl link normalization, and repeatable audit checks.

## Core rules (always)

- **Never mutate captured files in `raw/`** — raw sources are immutable after capture; if a source needs annotation, create a `source` page in `wiki/sources/` instead.
- **Every claim on a wiki page carries an inline provenance marker** with a locator or short quote anchor (e.g., `Founded in 2019.^[from [[Source Page]] — "founded in 2019"]`); a bare source link without a locator is a lint defect (`UNSOURCED`).
- **Contradictions append, never overwrite** — when a new source disagrees with an existing sourced claim, record both positions in a conflict callout and flag `status: contested`; resolution is a human decision.
- **One atomic git commit per ingest** — the source page, all entity/concept page edits, index updates, and the log entry go into a single commit referencing the `raw/` file; this is the unit of undo and the backup mechanism.
- **Every new page gets at least one outbound `[[wikilink]]` and is registered in its category `_index.md` and at least one MOC before the commit** — orphan pages are a lint defect.
