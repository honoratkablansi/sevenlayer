# Operation: Ingest

<!-- llm-wiki-op: ingest -->

> Compile a raw source into linked wiki pages: source-summary → entity/concept pages →
> index updates → log line → one atomic git commit. This is the primary knowledge-accretion
> loop of the wiki. Every claim produced here must be traceable back to the open `raw/` file.

## Table of Contents

1. [Step 1 — Locate the wiki and load context](#1-locate-the-wiki-and-load-context)
2. [Step 2 — Read the source in full](#2-read-the-source-in-full)
3. [Step 3 — Discuss takeaways with the user](#3-discuss-takeaways-with-the-user)
4. [Step 4 — Dedup before create](#4-dedup-before-create)
5. [Step 5 — Plan / diff preview (multi-file ingests)](#5-plan--diff-preview-multi-file-ingests)
6. [Step 6 — Write pages (source, entities, concepts)](#6-write-pages-source-entities-concepts)
7. [Step 7 — Refresh indexes and append log line](#7-refresh-indexes-and-append-log-line)
8. [Step 8 — Lint and fix](#8-lint-and-fix)
9. [Step 9 — Atomic git commit](#9-atomic-git-commit)
10. [Definition of Done for a Page](#definition-of-done-for-a-page)
11. [Batch Ingest](#batch-ingest)
12. [Hard Rules](#hard-rules)

---

## 1. Locate the wiki and load context

**Goal:** arrive at a complete picture of what already exists before touching anything.

### URL routing (read this first)

Before locating the wiki, determine what the user's source actually is:

- **Local file in `raw/`** — proceed as normal through Steps 1–9 below (unchanged
  default behavior). No scraping involved.
- **URL** (`http://` or `https://`), or an explicit "scrape/crawl/fetch/ingest this
  link" request — **first** run the scrape playbook (`references/operations/scrape.md`)
  to produce `raw/<slug>.md`; **then** continue this ingest flow on that file.
  - Scraping is optional and **Claude-Code-only** (requires local Claude Code with
    network + Scrapling + trafilatura installed). See `references/operations/scrape.md`
    §1 for the surface gate.
  - If scraping is unavailable (wrong surface, user declines deps), see
    `references/operations/scrape.md` §9 for the WebFetch fallback, which produces
    `is_verbatim: false` content. **Content with `is_verbatim: false` must not be
    quoted verbatim** in wiki claim lines — cite with a tight paraphrase only.
  - Once `scrape.md` has produced a `raw/` file, return here and continue from Step 2.
- **Research paper/PDF fixture** — if the user points to a PDF corpus or a paper
  manifest, first use `scripts/paper_vector.py` to produce page-delimited markdown
  in `raw/papers/` and copied PDF assets in `raw/assets/papers/`; then ingest the
  produced markdown files one at a time. Do not route PDFs through Scrapling.

When intent is ambiguous (no clear file path or URL), ask one clarifying question.

1. Resolve the wiki root using the discovery contract (see `references/operations/init.md §1`):
   - If the user supplied an explicit path, use it.
   - Otherwise walk **up** from cwd until a directory containing both `CLAUDE.md`
     (first non-empty line = `<!-- llm-wiki: v1 -->`) **and** a `wiki/` subdirectory is found.
   - If no match is found, ask the user or offer to run `init`.

2. Read `CLAUDE.md` in full — it holds the domain/conventions that govern this specific wiki.

3. Read `index.md` in full — the router shows what categories exist and their current counts.

4. Read the **last ~5 `log.md` entries** to understand recent ingest history and avoid
   duplicating work:
   ```bash
   grep "^## \[" log.md | tail -5
   ```

Do not skip or abbreviate this context-loading step. Knowing what already exists prevents
duplicates and ensures the new pages fit the existing graph.

---

## 2. Read the source in full

**Goal:** have the complete raw source in the active context window before writing a single
claim — this is the guarantee against hallucination drift.

1. Identify the file in `raw/` (or the path the user indicated).
2. Read the **entire file**. Do not skim or read only excerpts; claims must be quoted or
   tightly paraphrased from the open file (see `references/conventions.md §4.3`).
   For page-delimited paper markdown produced by `paper_vector.py`, preserve page
   numbers in notes so later provenance markers can cite `p. N` precisely.
3. For image files (`.png`, `.jpg`, `.gif`, etc.) — read the image file directly rather than
   relying on embed references or filenames. Visual content matters and must be ingested as
   first-class information.
4. Note the exact filename (used in provenance markers and the commit message).

During ingest, `raw/` is **read-only** for Claude — do not create, edit, or delete any
existing file under `raw/`. Capture operations such as `scrape.py` and
`paper_vector.py` may create new raw source files before ingest begins; once captured,
those files are immutable provenance anchors.

---

## 3. Discuss takeaways with the user

**Goal:** surface the most important claims and intended coverage before writing, so the
user can redirect early rather than after pages are written.

1. Present a concise takeaway summary: the source's core thesis, the key entities mentioned
   (people, orgs, systems), the key concepts introduced or developed, and any claims that
   look notable, controversial, or likely to touch existing pages.
2. Propose the coverage plan: which entity/concept pages will be created vs. updated, which
   existing pages will gain new claims, and any pages that might need splitting.
3. **Default: one source at a time.** Do not begin writing pages until the user
   has reviewed the takeaways for this source. Batch ingest is opt-in (see §11).
4. If the user wants to adjust scope (skip certain entities, focus on specific concepts),
   incorporate that before the dedup and preview steps.

---

## 4. Dedup before create

**Goal:** ensure every candidate page maps to exactly one canonical file — re-ingesting
the same source must be idempotent.

For each entity and concept identified in Step 3, run a three-step check:

1. **Search `index.md`** — does a category entry already exist for this concept/entity by
   name or close variant?
2. **Search the relevant `wiki/<cat>/_index.md`** — does a `[[link]]` entry already exist
   with this name or a synonym?
3. **Search `aliases` fields in existing pages** — does any page declare this name as an
   alias?

If a match is found at any step → **reuse the existing canonical page**. Add the new claims
to it (with provenance markers) rather than creating a second page.

If no match is found → create a new page whose **filename is the canonical title**
plus `.md` (e.g., `Transformer (architecture).md`), so `[[Transformer (architecture)]]`
resolves directly in Obsidian. Keep titles filesystem-safe (avoid `/ \ : * ? " < > |`)
and unique vault-wide (disambiguate with parentheticals). Do not kebab-case filenames.

Full naming and dedup rules live in `references/conventions.md §7`.

---

## 5. Plan / diff preview (multi-file ingests)

**Goal:** give the user a reviewable diff-like plan before any files are written, so
mistakes can be caught at zero cost.

For **any ingest that will write or modify more than one file**, produce a written plan
listing:

| File | Action | Changes |
|---|---|---|
| `wiki/sources/<title>.md` | **create** | New source-summary page for `<Title>` |
| `wiki/concepts/<title>.md` | **create** | New concept page; claims: … |
| `wiki/entities/<title>.md` | **update** | Adding claim: "…" ^[source] |
| `wiki/concepts/_index.md` | **update** | Add entry `[[<Title>]] — one-liner` |
| `wiki/entities/_index.md` | **update** | Add entry `[[<Entity>]] — one-liner` |
| `wiki/maps/<topic>.md` | **create/update** | New or updated MOC linking the new pages |
| `index.md` | **update** | Increment concept count by N, entity count by M |
| `log.md` | **append** | `## [YYYY-MM-DD] ingest \| <Title>` |

**Get explicit user confirmation** (e.g., "yes", "proceed", "looks good") before writing
any file. If the user requests changes to the plan, revise and re-present.

For a single-file ingest (one source, one or two obvious pages), a brief verbal summary
in Step 3 satisfies this requirement — a formal table is not required unless the user
requests it.

---

## 6. Write pages (source, entities, concepts)

**Goal:** produce well-formed, fully-cited wiki pages derived entirely from the open
`raw/` source.

### 6.1 Source-summary page (`wiki/sources/<title>.md`)

One page per ingested source. Use the `source` page type from `references/conventions.md §6.2`.
The page summarises the source's claims — it is a literature note, not a full transcript.
Populate all applicable frontmatter fields (`authors`, `url`, `publisher`, `published`,
`accessed`, `source_type`, `covers`).

### 6.2 Entity and concept pages

Create or update each entity/concept page identified in Steps 3–4.

**On existing pages:** append new claims with provenance markers. Do not remove or
overwrite existing sourced claims (see contradiction rule below).

**On new pages:** include full frontmatter (`type`, `aliases`, `tags`, `created`,
`updated`, `status`, plus type-specific fields), at least one outbound `[[wikilink]]`, and
at least one entry in the corresponding MOC (`maps/` or `wiki/overview.md`).

### 6.3 Provenance is mandatory on every claim

Every factual claim on a `concept` or `entity` page must carry an inline provenance marker.
The marker form (from `references/conventions.md §4`):

```
Founded in 2019.^[from [[Source Page]] — "founded in 2019"]
```

- `^[...]` — inline footnote/provenance anchor.
- Inside: a short lead word (e.g. `from`), then the `[[wikilink]]` to the source-summary
  page, then ` — `, then a short verbatim quote or precise locator (section title,
  paragraph ID, timestamp, page number). Never place the link immediately after `^[` (avoid `^[[[`,
  which breaks link parsing).
- For paper/PDF sources, include the page locator from the page-delimited raw
  markdown, e.g. `^[from [[Groth 2016 - Pairing-Based Non-interactive Arguments]]
  p. 4 — "pairing-based non-interactive arguments"]`.
- The quote must match the open `raw/` file exactly or be a tight paraphrase marked
  as such.
- **Un-cited claims are a lint defect (`UNSOURCED`)** and must not be committed.

Claims must be quoted or tightly paraphrased from the **open raw file** — never from
prior model memory.

### 6.4 Contradictions — append, never overwrite

When a new source disagrees with an existing **sourced** claim, record both versions in a
`[!conflict]` callout — do not overwrite the older claim:

```
> [!conflict] Employee count
> - 50 — [[2024 pitch]] (2024-01)
> - 200 — [[2025 press]] (2025-06)
> Status: contested — newer source suggests growth; unresolved.
```

**Contradiction vs supersession:** if the sources genuinely disagree, keep both positions
in the `[!conflict]` callout above — resolution is a **human** decision, do not resolve it
autonomously. If instead a newer authoritative source simply *updates* a value from the
same lineage (not a genuine dispute), update the claim but leave a dated note recording the
prior value. The full callout syntax and this distinction are defined in
`references/conventions.md §5`.

---

## 7. Refresh indexes and append log line

**Goal:** keep the index layer consistent with what was just written so the next operation
(query or lint) finds everything without a repair step.

This step is **non-skippable** and must complete before the commit in Step 9.

1. **Category `_index.md`** — for every new page created, add a `[[link]] — one-liner` entry
   in the corresponding `wiki/<cat>/_index.md`. For updated pages, verify the entry is
   already present (add it if missing).

2. **Root `index.md`** — increment the entry counts for affected categories. If any
   category's count changed, update the count and the "last updated" line.

3. **`log.md`** — append exactly one new entry at the bottom of the file:
   ```
   ## [YYYY-MM-DD] ingest | <Title>
   - Source: `raw/<filename>`
   - Pages created: <list>
   - Pages updated: <list>
   ```
   Use today's ISO-8601 date (`YYYY-MM-DD`). The `log.md` is **append-only** — never
   edit or remove prior entries.

4. **MOC / `overview.md`** — if the ingest introduces a genuinely new topic area, add a
   link to the new concept or entity in `wiki/overview.md` or the relevant `maps/` page.
   Create a new `maps/<topic>.md` only when a real cross-cutting topic warrants one
   (not speculatively).

Index staleness is the top operational risk for this wiki. Do not defer index updates to
a later step or commit.

---

## 8. Lint and fix

**Goal:** catch structural defects before they enter git history.

Run the lint check on the wiki root. The optional script accelerator:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/lint.py <wiki-root>
```

The script checks (stdlib-only, no external dependencies):
- Broken `[[wikilinks]]` — target file missing.
- Orphan pages — no inbound links and not in any MOC.
- Missing or invalid frontmatter.
- Heuristic `UNSOURCED` flag — claim lines on `concept`/`entity` pages lacking a
  provenance marker.

The script is **optional** — if the environment does not support code execution, run the
lint checklist from `references/operations/lint.md` manually (the prose lint is canonical).

Fix all failures before proceeding to the commit. Common fixes:
- Missing provenance marker → locate the claim in the open `raw/` file and attach `^[...]`.
- Orphan page → add a `[[link]]` entry in the category `_index.md` and at least one MOC.
- Broken wikilink → correct the target filename or create the missing page.
- Invalid frontmatter → fill in `type` and `status` fields.

Do not commit a wiki that fails lint.

---

## 9. Atomic git commit

**Goal:** every ingest is one undoable unit — the complete set of changes lands in a
single commit or it does not land at all.

Stage and commit **all of the following together** in one atomic commit:

- The new source-summary page (`wiki/sources/<title>.md`)
- All new or updated entity pages (`wiki/entities/`)
- All new or updated concept pages (`wiki/concepts/`)
- All updated `_index.md` files
- The updated root `index.md`
- The updated `log.md`
- Any new or updated `maps/` files
- The source file in `raw/` being ingested (the provenance anchor — see note below)
- For paper/PDF sources, the copied PDF asset referenced by `pdf_asset` (usually
  `raw/assets/papers/<slug>.pdf`)

```bash
git -C <wiki-root> add \
    raw/<filename> \
    raw/assets/papers/<slug>.pdf \
    wiki/sources/<title>.md \
    wiki/entities/ \
    wiki/concepts/ \
    wiki/sources/_index.md \
    wiki/entities/_index.md \
    wiki/concepts/_index.md \
    index.md \
    log.md

git -C <wiki-root> commit -m "ingest: <Title>

Source: raw/<filename>
Pages created: <list>
Pages updated: <list>
Created by llm-wiki skill (ingest operation)."
```

**Never split an ingest across multiple commits.** Partial state (source page without
index update, or index update without log line) breaks the invariants that lint and
query depend on.

**This commit is the unit of undo.** To fully reverse an ingest:
```bash
git revert <sha>
```
`git revert` is the correct recovery mechanism — it removes the ingest changes while
preserving all subsequent history. Do not use `git reset` unless instructed by the user.

**Commit the raw source, never mutate it after capture.** The source file in `raw/` is
the provenance anchor — commit it as part of the ingest so the wiki's citations are
reproducible from the repo alone (the spec rule: every claim reconstructable from
`raw/` + git history). For paper/PDF sources, commit both the extracted markdown source
and the referenced `raw/assets/papers/` PDF unless the user explicitly chooses an
external-storage policy. Claude may create new raw files during capture, but must never
edit or delete already-captured raw files. Exception: very large binaries or
copyright-restricted sources may be added to `.gitignore` at the user's
discretion, with the explicit tradeoff that provenance is then not reproducible from the
repo alone.

---

## Definition of Done for a Page

Before a page is included in the commit, verify all five conditions:

- [ ] **Frontmatter complete** — `type`, `aliases`, `tags`, `created`, `updated`,
      `status` are all present and non-empty; type-specific fields are filled where
      applicable.
- [ ] **At least one outbound `[[wikilink]]`** — the page links to at least one other
      page in the wiki (prevents it from being a dead-end node).
- [ ] **Registered in a MOC** — the page is listed in at least one of: `wiki/overview.md`,
      a `maps/<topic>.md`, or a relevant section of a category `_index.md` that serves
      as a navigational hub.
- [ ] **Registered in its category `_index.md`** — `wiki/<cat>/_index.md` has a
      `[[link]] — one-liner` entry for this page.
- [ ] **Every claim cited** — every factual assertion carries an inline provenance marker
      `^[from [[Source Page]] — "locator or quote"]`; no `UNSOURCED` defects remain.

A page that fails any of these checks is not done and must not be committed.

---

## Batch Ingest

Batch ingest (multiple sources in one session) is **opt-in** — the user must explicitly
request it. When batch ingest is active:

- Still discuss takeaways and get confirmation **per source** (Step 3) before writing pages
  for that source.
- Still run dedup (Step 4) freshly for each source — earlier sources in the batch may have
  created pages that later sources in the same batch should reuse.
- **Commit per source** (Step 9) — each source gets its own atomic commit, even in a batch.
  Do not bundle multiple sources into one commit.

The plan/diff preview (Step 5) may be presented once for the whole batch if the user
requested a bulk plan, but confirmation is still required before writing pages for each
individual source.

---

## Hard Rules

**Never write a claim from memory.** The source file must be open (read in the current
context window) when claim lines are written. This is the primary safeguard against
hallucination drift.

**Never overwrite an existing sourced claim.** New contradictory information goes in a
`[!conflict]` callout alongside the original. Resolution is a human decision.

**Never commit a partial ingest.** Source page + all entity/concept edits + all index
updates + log line land in one commit, or nothing lands.

**Never edit files in `raw/`.** `raw/` is immutable. Claude reads it; the user owns it.

**Never skip the index update.** Index staleness silently breaks query and lint. The index
and log updates are part of the ingest, not cleanup.

**Use `[[wikilinks]]` for all internal links.** Markdown links break Obsidian backlinks,
graph view, and Dataview. See `references/conventions.md §2.1`.

**`git revert <sha>` is the undo.** For a complete rollback of a single ingest, revert
the commit. Do not surgically delete pages or edits without reverting — partial cleanup
leaves the index inconsistent.
