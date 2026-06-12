# conventions.md — llm-wiki page & link conventions

> This file governs every wiki page created or updated by the llm-wiki skill.
> It is the authoritative reference for page types, link discipline, naming,
> index/MOC structure, provenance, evolving claims, and frontmatter schema.
> See `../SKILL.md` for the operation router.

---

## Table of Contents

1. [Page types & granularity](#1-page-types--granularity)
2. [Links & naming](#2-links--naming)
3. [Index & MOCs](#3-index--mocs)
4. [Provenance (mandatory)](#4-provenance-mandatory)
5. [Evolving claims & contradictions](#5-evolving-claims--contradictions)
6. [Frontmatter schema](#6-frontmatter-schema)
7. [Dedup before create](#7-dedup-before-create)

---

## 1. Page types & granularity

Each wiki page has exactly one `type`. The five types, their granularity, and
intended role are:

| type | granularity | role |
|---|---|---|
| `source` | aggregate | One page per ingested raw source — a literature note summarising the source's claims, not a full transcript. |
| `concept` | **atomic** | One idea per page (evergreen). When a concept page accretes too many distinct sub-ideas, split it into multiple atomic pages. Splitting is correct; merging is usually wrong. |
| `entity` | one per proper-noun object | One page per person, organisation, lab, model, or named system. Kept strictly distinct from concept pages. |
| `synthesis` | aggregate | Deliberately aggregate; used for a filed-back query answer or an authorial thesis. Inherits provenance from source claims. |
| `map` (MOC) | aggregate | Topic navigation hub; a first-class graph node and optionally a Dataview dashboard. |

**Atomicity rule for concepts:** if a concept page grows to cover multiple
distinct ideas, split it. This preserves the "one page = one idea" invariant
and keeps cross-reference links precise.

---

## 2. Links & naming

### 2.1 Wikilinks — the only internal link format

All internal links use **`[[wikilinks]]`**, never bare markdown links
(`[text](path.md)`). Markdown links break Obsidian backlinks, the graph view,
and Dataview queries. This is non-negotiable.

Examples:

```
[[Transformer (architecture)]]          ← preferred
[[Transformer (architecture)|attention]] ← display-text alias, also fine
[Transformer](../concepts/transformer.md) ← FORBIDDEN for internal links
```

### 2.2 Rename / move discipline

**Claude must not rename or move pages via raw file operations.** Renaming
outside Obsidian breaks all `[[wikilinks]]` that point to the old title across
the vault. The correct flow:

- Use Obsidian's built-in rename (which auto-updates links) whenever possible.
- If a rename is unavoidable in a non-Obsidian context (e.g., a batch
  correction during ingest), update **all referrers in the same commit** as the
  rename — never split across commits.

### 2.3 Unique vault-wide titles & disambiguation

Every page has a **unique title across the entire vault**. When two distinct
concepts share a name, disambiguate with parentheticals:

```
[[Transformer (architecture)]]
[[Transformer (org)]]
```

Use `aliases` in frontmatter so authors can write naturally flowing prose:

```yaml
aliases: [transformer, attention mechanism]
```

A `[[wikilink]]` may match any alias, so `[[attention mechanism]]` will resolve
to the canonical page even when the file is named `transformer-architecture.md`.

### 2.4 Orphan prevention rule

**Before committing, every new page must have:**

1. At least one outbound `[[wikilink]]` to another page.
2. At least one entry in a relevant MOC (`maps/` page or `overview.md`).
3. At least one entry in its category `_index.md`.

A page that satisfies none of these is an orphan — a lint defect. Register the
page in the appropriate `_index.md` and at least one MOC in the same commit
that creates it.

---

## 3. Index & MOCs

### 3.1 Distinct roles

| file | role |
|---|---|
| `index.md` | **Router** — lists categories + entry counts + a one-line "what's here" + links to `wiki/<cat>/_index.md`. This is the first file read on every operation. |
| `wiki/<cat>/_index.md` | **Category catalog** — holds `[[link]] — one-liner` entries for every page in that category. |
| `wiki/overview.md` | **Root MOC / thesis** — the evolving high-level statement of what this wiki is about; the entry point for synthesis. |
| `maps/<topic>.md` | **Topic navigation** — per-topic MOC for cross-cutting navigation and Dataview dashboards. Created lazily (on first real need). |

`index.md` is a router, not a full listing — it keeps per-query token cost
roughly flat as the wiki grows.

### 3.2 MOC split threshold

Split a MOC (maps page or `_index.md`) when it reaches **≈25–30 entries**.
At that size, create a sub-MOC or a more specific topic page and redistribute
entries. This keeps any single navigational file scannable in one pass.

### 3.3 Tags vs links

- **Links = aboutness.** Use `[[wikilinks]]` to express "this page is about X"
  or "this claim comes from X".
- **Tags = context / state.** Use a small closed vocabulary:
  - the page's **type tag** — `source`, `concept`, `entity`, `synthesis`, or
    `moc` — matching the `type:` field (each page template sets this). This is
    what makes Dataview `FROM #source` queries work; the `type:` frontmatter
    field is queried instead with `WHERE type = "..."`.
  - `status/stub`, `status/draft`, `status/reviewed`, `status/stable` for state.
  - `topic/<domain>` for cross-cutting thematic grouping.

Do not use tags to express relationships that should be links. Do not use links
to express operational state that should be a tag.

---

## 4. Provenance (mandatory)

### 4.1 The rule

Every factual claim on a `concept` or `entity` page **must carry an inline
provenance marker** giving a locator or short quote anchor. A bare source link
with no locator is insufficient. The exact marker form is:

```
Founded in 2019.^[from [[Source Page]] — "founded in 2019"]
```

- The caret-bracket `^[...]` is the inline footnote / provenance anchor.
- Inside: a short lead word (e.g. `from`), then the `[[wikilink]]` to the source
  page, then ` — `, then a short verbatim quote or precise locator (section,
  timestamp, paragraph ID).
- **Do not** place the wikilink immediately after `^[` (i.e. avoid `^[[[`): the
  `^[` + `[[` adjacency collides with wikilink parsing and breaks the link. A
  lead word or a space prevents this and keeps the citation clickable.
- The quote must match the raw source file exactly or be a tight paraphrase
  clearly marked as such.

### 4.2 Un-cited claims are a lint defect

Any sentence on a `concept` or `entity` page that asserts a fact but lacks
a provenance marker is flagged as `UNSOURCED` by lint. Fix by locating the
claim in the open `raw/` file and attaching the marker.

### 4.3 Quote-from-source rule

During ingest, claims must be **quoted or tightly paraphrased from the open
`raw/` file** — never from prior model memory. The model must have the raw file
open (read in the current context) when writing claim lines. This prevents
hallucination drift from the original source.

### 4.4 Provenance on synthesis pages

`synthesis` pages contain authored claims, not raw-source claims. Each
synthesised assertion should cite the underlying concept/entity pages it
draws from (which themselves carry raw-source provenance), forming a
two-level citation chain: `synthesis → concept/entity → raw source`.

---

## 5. Evolving claims & contradictions

### 5.1 The `status` field for claims

Contestable assertions use the `status` field (in frontmatter and inline) to
track their epistemic state:

| value | meaning |
|---|---|
| `supported` | Claim is corroborated by at least one source with no known contradiction. |
| `contested` | Two or more sources disagree; both are on record; unresolved. |
| `superseded` | A newer authoritative value has replaced this claim; dated note records the old value. |
| `open` | Claim is a stated uncertainty or open question, not yet sourced. |

### 5.2 Contradiction rule — append, never overwrite

When a new source **disagrees** with an existing sourced claim, record both
versions in a callout — **do not overwrite the older claim**. The callout
syntax:

```
> [!conflict] Employee count
> - 50 — [[2024 pitch]] (2024-01)
> - 200 — [[2025 press]] (2025-06)
> Status: contested — newer source suggests growth; unresolved.
```

Use the `[!conflict]` callout type so Obsidian renders it visually and so
lint can detect it mechanically.

### 5.3 Contradiction vs supersession

These are distinct situations:

- **Contradiction:** two sources disagree and neither is definitively correct
  → keep both, add the `[!conflict]` callout, set `status: contested`.
- **Supersession:** a newer authoritative value clearly replaces an older one
  (e.g., a corrected figure, an org's official updated count) → update the
  primary claim, add a dated note documenting the old value, set
  `status: superseded`.

### 5.4 Resolution is a human decision

Claude does not resolve contradictions autonomously. Flagging, recording, and
surfacing them during lint is Claude's job. Deciding which claim is canonical
is the human author's job.

### 5.5 Optional ZES evidence tiers

For wikis that want fine-grained epistemic tracking, claims may carry ZES
strength tiers (0–3):

| tier | meaning |
|---|---|
| ZES-0 | Unverified / speculative |
| ZES-1 | Single source, not independently corroborated |
| ZES-2 | Multiple independent sources agree |
| ZES-3 | Consensus / authoritative primary source |

These are optional annotations; the core `status` field is mandatory.

---

## 6. Frontmatter schema

### 6.1 Shared core (every page)

Every page — regardless of type — opens with this frontmatter block:

```yaml
---
type:            # source | concept | entity | synthesis | map
aliases: []
tags: []
created: 2026-05-26
updated: 2026-05-26
status:          # stub | draft | reviewed | stable
---
```

Notes:
- `type` and `status` are required; leave no blank values in committed pages.
- `aliases` is the Obsidian plural built-in; always a list, never a bare
  string.
- `tags` is the Obsidian plural built-in; use namespaced closed-vocabulary
  values (see §3.3).
- `created` / `updated` are explicit ISO-8601 dates because git resets
  filesystem mtime on checkout — do not rely on `file.ctime`.
- The `created` date is set once on page creation and never changed.
- The `updated` date is bumped on every substantive edit.

### 6.2 Type-specific additions

Each type extends the shared core with additional fields:

**`source`**
```yaml
authors: []
url:
publisher:
published:       # YYYY-MM-DD
accessed:        # YYYY-MM-DD
source_type:     # article | book | gist | video | podcast | paper | post | webpage
covers: []       # [[wikilinks]] to concept/entity pages this source covers
```

**Scraped-source optional fields** (present when the source was captured via
`references/operations/scrape.md`; omit for hand-placed or non-web sources):
```yaml
canonical_url:   # <link rel=canonical> from the page, or normalized url
author:          # metadata author extracted by trafilatura (nullable)
published:       # metadata date ISO-8601 (nullable)
sitename:        # metadata sitename extracted by trafilatura (nullable)
fetched_at:      # YYYY-MM-DD date the page was fetched
fetcher:         # http | stealth | dynamic  (Scrapling tier used)
fetch_method:    # scrapling | webfetch
is_verbatim:     # true if Scrapling+trafilatura (byte-derived); false if WebFetch (model-interpreted)
http_status:     # HTTP status code returned
extractor:       # trafilatura-<version> | webfetch
content_hash:    # sha256 of extracted markdown (dedup key)
```

**Paper-source optional fields** (present when `scripts/paper_vector.py` prepared
the source from a PDF fixture):
```yaml
pdf_asset:              # raw/assets/papers/<slug>.pdf
pdf_sha256:             # sha256 of the source PDF
bytes:                  # PDF byte length
pages:                  # PDF page count
doi:
semantic_scholar_url:
pdf_source_url:
citation_count:
is_verbatim: true       # pypdf text is derived from the PDF bytes
extractor: pypdf
extracted_at:           # YYYY-MM-DD date the markdown was extracted
```

**Content with `is_verbatim: false`** (e.g. WebFetch-captured) may be tight-paraphrased
with a citation but never presented as an exact quote.

**`concept`**
```yaml
parent:          # [[parent concept]] if part of a hierarchy
related: []      # [[wikilinks]] to adjacent concepts
sources: []      # [[wikilinks]] to source pages this concept draws from
claims_status:   # supported | contested | superseded | open
```

**`entity`**
```yaml
entity_kind:     # person | org | lab | model | system
related: []      # [[wikilinks]] to related entities/concepts
sources: []      # [[wikilinks]] to source pages
```

**`synthesis`**
```yaml
question:        # the query or thesis this synthesis answers
sources: []      # [[wikilinks]] to concept/entity pages it draws from
concepts: []     # [[wikilinks]] to key concepts
confidence:      # low | medium | high
```

**`map`** (no extra required fields beyond shared core; add `topic:` freely)

Full example Dataview queries (recently-updated pages, orphan-finder,
sources-by-date, stubs list) are in `../references/obsidian-setup.md`.

---

## 7. Dedup before create

Before creating any new entity or concept page during ingest, run this
three-step check to avoid duplicate pages:

1. **Search `index.md`** — does a category entry already exist for this
   concept/entity by name or close variant?
2. **Search the category `_index.md`** — does a `[[link]]` entry already exist
   with this name or a synonym?
3. **Search `aliases` fields** — does any existing page declare this name as
   an alias?

If a match is found at any step, **reuse the existing canonical page** — add
the new claims to it (with provenance markers) rather than creating a second
page.

**Filenames = canonical titles.** A page's filename is its canonical title plus the
`.md` extension (e.g., `Transformer (architecture).md`). Obsidian resolves
`[[Transformer (architecture)]]` directly to that file, and resolution is
**case-insensitive** (`[[transformer (architecture)]]` resolves too). Do **not**
kebab-case or otherwise mangle filenames — backlinks, the graph, and link
readability depend on the filename matching the title.

- Keep titles filesystem-safe: avoid `/ \ : * ? " < > |`; use a hyphen or ` - ` in
  place of a colon.
- Titles must be unique vault-wide (disambiguate with parentheticals, §2.3).
- Re-ingest is idempotent because the canonical title maps to the same filename
  every time — which is exactly why the dedup check above must run before creating
  any page.
