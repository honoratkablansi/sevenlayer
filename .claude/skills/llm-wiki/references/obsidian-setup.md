# Obsidian Setup Reference

This file covers Obsidian configuration, image handling, `.gitignore`, Web Clipper templating, Dataview dashboard queries, and Marp usage for llm-wiki wikis.

## Table of Contents

1. [Files & Links Settings](#1-files--links-settings)
2. [Image Handling](#2-image-handling)
3. [.gitignore](#3-gitignore)
4. [Web Clipper → `source` Frontmatter](#4-web-clipper--source-frontmatter)
5. [Dataview Dashboard Queries](#5-dataview-dashboard-queries)
6. [Marp (Optional Slides)](#6-marp-optional-slides)

---

## 1. Files & Links Settings

Open **Settings → Files & Links** in Obsidian and apply these three settings:

| Setting | Value |
|---|---|
| Use `[[Wikilinks]]` | **ON** |
| Automatically update internal links on rename | **ON** |
| Default location for new attachments | `raw/assets/` |

**Why wikilinks:** Markdown links (`[text](path)`) break Obsidian backlinks, graph view, and Dataview queries. Standardizing on `[[wikilinks]]` keeps all three working correctly.

**Why `raw/assets/`:** Attachments (downloaded images, PDFs) are source-accompanying files. Placing them under `raw/assets/` keeps them co-located with their immutable source material rather than scattered across the wiki.

**Rename warning:** Claude must not rename or move pages via raw file operations. Renames must go through Obsidian (which auto-updates links) or, if unavoidable outside Obsidian, all referrers must be updated in the same atomic commit.

---

## 2. Image Handling

**Embed syntax:** Always use the Obsidian wikilink embed form:

```
![[image-filename.png]]
```

Never use standard markdown image syntax (`![alt](path)`) — it bypasses Obsidian's link graph.

**Mandatory caption rule:** Every image embed must be followed immediately by a text caption on the next line. Example:

```markdown
![[figure-1-architecture.png]]
*Figure 1: Transformer architecture overview from Vaswani et al. 2017. ^[from [[attention-is-all-you-need]] — Fig. 1]*
```

A bare embed with no caption is a lint defect.

**Reading image content:** When the content of an image matters (diagrams, charts, screenshots with data), read the image file directly — do not rely only on the surrounding markdown text. Single-pass markdown reads do not ingest pixels.

---

## 3. .gitignore

Add the following block to the wiki root `.gitignore` (the `init` operation writes this automatically):

```gitignore
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache
.trash/
```

**Keep tracked** (do not gitignore): `.obsidian/app.json`, `.obsidian/hotkeys.json`, and all plugin config files under `.obsidian/plugins/`. Tracking these ensures that Obsidian settings, keybindings, and plugin configuration travel with the repo when it is cloned on another machine.

---

## 4. Web Clipper → `source` Frontmatter

Use the [Obsidian Web Clipper](https://obsidian.md/clipper) browser extension to capture web sources directly into the wiki. Configure a template that maps to the `source` page type frontmatter schema.

**Template mapping:**

| Web Clipper field | Frontmatter field | Notes |
|---|---|---|
| Title | `title` | Page/article title |
| Author(s) | `authors` | List format: `[Author Name]` |
| URL | `url` | Canonical source URL |
| Published date | `published` | ISO date: `YYYY-MM-DD` |
| Clipped date | `accessed` | ISO date: `YYYY-MM-DD` |
| *(fixed)* | `type: source` | Always set to `source` |

**Save location:** Configure the Web Clipper to save clipped notes into `wiki/sources/`.

**Example clipped frontmatter result:**

```yaml
---
type: source
title: "LLM Wiki"
authors: [Andrej Karpathy]
url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
published: 2025-04-01
accessed: 2026-05-26
status: stub
tags: []
aliases: []
created: 2026-05-26
updated: 2026-05-26
---
```

After clipping, run the **ingest** operation to process the captured source into linked wiki pages.

---

## 5. Dataview Dashboard Queries

Install the [Dataview plugin](https://blacksmithgu.github.io/obsidian-dataview/) and create a dashboard note (e.g., `wiki/maps/dashboard.md`) containing the queries below. Each query is in a fenced `dataview` code block so it executes live in Obsidian's reading view.

### Recently Updated

Shows the 20 most recently touched pages across the entire vault:

````markdown
```dataview
TABLE type, status, updated FROM "" WHERE updated SORT updated DESC LIMIT 20
```
````

### Orphan Finder

Lists pages with no inbound links and no outbound links — these are prime lint candidates:

````markdown
```dataview
LIST FROM "" WHERE length(file.inlinks) = 0 AND length(file.outlinks) = 0
```
````

### Sources by Date

Shows all source pages sorted by publication date, newest first:

````markdown
```dataview
TABLE authors, published, status FROM #source SORT published DESC
```
````

### Stubs and Drafts

Lists pages that still need work, sorted oldest-updated first (prioritizes neglected pages):

````markdown
```dataview
TABLE type, updated FROM "" WHERE status = "stub" OR status = "draft" SORT updated ASC
```
````

---

## 6. Marp (Optional Slides)

[Marp](https://marp.app/) can generate slide decks from markdown. It is **entirely optional** and used only on demand — not a standard part of the wiki workflow.

**Rules:**

- Slide decks live in a separate `slides/` directory at the wiki root. They are not part of `wiki/` or `raw/`.
- **Never** add `marp: true` to any standard page template (source, concept, entity, synthesis, map). Wikilinks (`[[...]]`) and embeds (`![[...]]`) do not render in Marp, so mixing Marp frontmatter into regular wiki pages breaks the reading experience.
- To create a deck, copy relevant content from wiki pages into a new file under `slides/`, add `marp: true` to that file's frontmatter, and render it separately.
- Slide files are not ingested, indexed, or linted as wiki content.
