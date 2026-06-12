# Operation: Init

<!-- llm-wiki-op: init -->

> Create a new wiki skeleton in the target directory. This operation is domain-agnostic and reusable — nothing is hardcoded to any specific wiki theme.

## Table of Contents

1. [Discovery Contract](#1-discovery-contract)
2. [Pre-flight Checks](#2-pre-flight-checks)
3. [Skeleton Creation Steps](#3-skeleton-creation-steps)
4. [Git Init and First Commit](#4-git-init-and-first-commit)
5. [Post-Init Checklist](#5-post-init-checklist)
6. [Hard Rules](#6-hard-rules)

---

## 1. Discovery Contract

A directory is recognized as a wiki **iff** it satisfies both conditions:

1. It contains a `CLAUDE.md` whose **first non-empty line** is exactly:
   ```
   <!-- llm-wiki: v1 -->
   ```
2. It contains a `wiki/` subdirectory.

**Resolution order** when an operation is invoked:
1. Explicit path provided by the user → use it.
2. No explicit path → walk **up** from cwd, directory by directory, stopping at the first directory that satisfies both conditions above.
3. No match found → ask the user where the wiki root is, or offer to run `init` in the current directory.

`init` creates a fresh wiki that satisfies this contract. After `init` completes, every subsequent operation (`ingest`, `query`, `lint`) will auto-discover the wiki via this contract without additional configuration.

---

## 2. Pre-flight Checks

Before creating any files:

1. Confirm the **target directory** (explicit path or cwd). If the user did not specify one, ask.
2. Ask for the **wiki domain/theme** — a one-sentence description of what this wiki will cover (e.g., "agentic civilization and AI futures"). This fills the domain slot in `CLAUDE.md` and `overview.md`.
3. Warn if the target directory already contains a `CLAUDE.md` with the `<!-- llm-wiki: v1 -->` marker — this wiki is already initialized. Offer to abort or re-scaffold missing pieces only.
4. Do **not** warn about non-wiki files already in the directory; `init` only creates the skeleton files and leaves existing content alone.

---

## 3. Skeleton Creation Steps

Create the following tree. Execute the steps in order; each step is described below.

```
<wiki-root>/
├── CLAUDE.md                        # schema (marker + conventions + workflows)
├── index.md                         # ROUTER → category indexes
├── log.md                           # append-only chronological record
├── .gitignore                       # Obsidian noise exclusions
├── raw/                             # immutable sources (never edited by Claude)
│   └── assets/                      # downloaded images for sources
│       └── .gitkeep
├── wiki/
│   ├── sources/
│   │   └── _index.md                # category index for source pages
│   ├── entities/
│   │   └── _index.md                # category index for entity pages
│   ├── concepts/
│   │   └── _index.md                # category index for concept pages
│   ├── syntheses/
│   │   └── _index.md                # category index for synthesis pages
│   ├── maps/
│   │   └── .gitkeep                 # empty until first real topic MOC is created
│   └── overview.md                  # evolving thesis / root MOC
```

### Step 3.1 — `CLAUDE.md`

Copy from `assets/schema-template.md` and fill in:
- The `<!-- llm-wiki: v1 -->` marker **must be the very first line**.
- Replace the `{{DOMAIN}}` placeholder with the user-supplied domain description.
- Replace the `{{DATE}}` placeholder with today's date (ISO 8601: `YYYY-MM-DD`).

This file is the schema that governs all future operations on this wiki. Do not abbreviate it.

### Step 3.2 — `index.md`

Copy from `assets/index-template.md`. The index is a **router** — it lists categories, counts, and one-line descriptions, and links to each `wiki/<cat>/_index.md`. At init time, counts are all `0` and category descriptions are the template defaults.

### Step 3.3 — `wiki/{sources,entities,concepts,syntheses}/_index.md`

For each of the four categories (`sources`, `entities`, `concepts`, `syntheses`), create `wiki/<cat>/_index.md` by copying from `assets/category-index-template.md` and filling in:
- `{{CATEGORY}}` → the category name (e.g., `sources`).
- `{{DATE}}` → today's date.

These files start empty (no entries) and are populated during `ingest`.

### Step 3.4 — `wiki/maps/` (empty directory)

Create `wiki/maps/.gitkeep` so git tracks the directory. Maps (topic MOCs) are created lazily — **only when the first real topic warrants one**, during an `ingest` or `query` operation, never during `init`.

### Step 3.5 — `wiki/overview.md`

Create with a **one-line thesis placeholder only**. Do not write faux content, invented examples, or fabricated claims. The placeholder must make clear it is to be filled in:

```markdown
# Overview

> Thesis placeholder — replace with a one-sentence summary of what this wiki is building toward, after the first ingest.
```

Do **not** put the `<!-- llm-wiki: v1 -->` marker in `overview.md` — the discovery contract depends solely on `CLAUDE.md`. The overview will evolve into the root MOC (Map of Content) as real pages accumulate. It is **not** populated during `init`.

### Step 3.6 — `log.md`

Copy from `assets/log-template.md` (this provides the header), then **append** the init entry below it. The log is **append-only**; entries are always added at the bottom. At init time the log contains only the header and this init entry:

```
## [YYYY-MM-DD] init | <wiki-root-name>
- Created wiki skeleton.
- Domain: <user-supplied domain>
```

### Step 3.7 — `.gitignore`

Create `.gitignore` with exactly these entries (Obsidian workspace noise + trash):

```
.obsidian/workspace*.json
.obsidian/cache
.trash/
```

These three entries keep Obsidian's per-machine workspace state out of the repo while **preserving** `.obsidian/app.json`, `hotkeys.json`, and plugin config — those travel with the repo so Obsidian behavior is consistent across machines.

### Step 3.8 — `raw/` and `raw/assets/`

Create both directories. Place a `.gitkeep` in `raw/assets/` so git tracks it. The `raw/` directory holds immutable source files (PDFs, text files, clippings). **Claude must never edit files in `raw/`** — it is read-only for Claude; the user places sources there manually or via Web Clipper.

---

## 4. Git Init and First Commit

### Step 4.1 — Initialize git if needed

Check whether the target directory is already inside a git repository:

```bash
git -C <wiki-root> rev-parse --is-inside-work-tree 2>/dev/null
```

- If the command exits `0` (already a git repo) → skip `git init`, proceed to commit.
- If the command fails or exits non-zero → run `git init <wiki-root>`.

### Step 4.2 — Stage all skeleton files

```bash
git -C <wiki-root> add CLAUDE.md index.md log.md .gitignore \
    raw/assets/.gitkeep \
    wiki/sources/_index.md \
    wiki/entities/_index.md \
    wiki/concepts/_index.md \
    wiki/syntheses/_index.md \
    wiki/maps/.gitkeep \
    wiki/overview.md
```

### Step 4.3 — First commit

```bash
git -C <wiki-root> commit -m "init: create wiki skeleton

Domain: <user-supplied domain>
Created by llm-wiki skill (init operation)."
```

The first commit captures the empty skeleton. It is the baseline for all future atomic ingest commits and the recovery point if anything goes wrong.

---

## 5. Post-Init Checklist

Verify each item is satisfied before reporting success to the user:

- [ ] `CLAUDE.md` first line is exactly `<!-- llm-wiki: v1 -->`.
- [ ] `wiki/` directory exists.
- [ ] `wiki/sources/_index.md`, `wiki/entities/_index.md`, `wiki/concepts/_index.md`, `wiki/syntheses/_index.md` — all four exist.
- [ ] `wiki/maps/.gitkeep` exists (no real map files were created).
- [ ] `wiki/overview.md` exists and contains only the placeholder — no fabricated content.
- [ ] `raw/` and `raw/assets/.gitkeep` exist.
- [ ] `.gitignore` contains all three required entries.
- [ ] `log.md` exists with the init log entry.
- [ ] The directory is a git repo with at least one commit (the init commit).
- [ ] **No concept, entity, source, or synthesis stub pages were created** — the category indexes are empty.

---

## 6. Hard Rules

**Do not create concept/entity/source/synthesis stub pages during init.** The skeleton is structure only. The first real wiki page comes from the first `ingest` operation. Fabricating content during `init` violates provenance requirements (§5.3 of conventions) because there is no `raw/` source to cite.

**Do not populate `wiki/maps/`** with real MOC files. Maps are created lazily, on-demand, when a real topic warrants one. During `init`, `maps/` contains only `.gitkeep`.

**Do not edit `raw/` files.** `raw/` is immutable. If a file must be placed there, the user does it — Claude only reads from `raw/`.

**`overview.md` gets a placeholder, not faux content.** Writing a fake thesis about a domain Claude has not yet researched is a fabrication. The placeholder text signals clearly that it is to be replaced after the first ingest.

**`CLAUDE.md` first line must be the exact marker.** The discovery contract depends on this. If the marker is absent or mis-formatted, no operation will recognize the directory as a wiki.

**`git init` + first commit are mandatory.** The wiki is a git repo from day one. Atomic commits are the undo mechanism, the backup strategy, and the provenance audit trail. A wiki without git history is missing a critical safety layer.
