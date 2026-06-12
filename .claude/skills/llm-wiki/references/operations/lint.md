---
operation: lint
skill: llm-wiki
version: 0.1.0
---

# Operation: Lint

## Table of Contents
1. [Purpose](#purpose)
2. [Canonical Lint: Prose Semantic Pass](#canonical-lint-prose-semantic-pass)
3. [Optional Accelerator: lint.py](#optional-accelerator-lintpy)
4. [The Fix Loop](#the-fix-loop)
5. [Handling Contradictions and Stale Claims](#handling-contradictions-and-stale-claims)
6. [Output Format](#output-format)

---

## Purpose

Lint health-checks the wiki for structural defects, semantic inconsistencies, and coverage gaps. It produces a categorized report so the maintainer can decide what to fix and in what order.

**The canonical lint is the LLM's prose semantic pass.** The optional `lint.py` script accelerates the mechanical subset but is never required — on surfaces without code execution (e.g., Claude.ai web), lint works fully by reasoning alone.

---

## Canonical Lint: Prose Semantic Pass

This is the primary and authoritative lint. Perform these checks by reading the wiki pages directly.

### 1. Contradictions across pages

Read concept and entity pages for claims that contradict one another. A contradiction occurs when two pages assert incompatible facts about the same thing, or when a concept page and a source-summary page disagree on a key point that has not already been flagged with a `[!conflict]` callout.

Flag each contradiction with:
- The two (or more) pages involved
- The conflicting claims verbatim or near-verbatim
- The sources cited on each side (if any)

Do **not** auto-resolve. See [Handling Contradictions and Stale Claims](#handling-contradictions-and-stale-claims).

### 2. Stale or superseded claims

Identify claims on concept or entity pages whose `status` field is `supported` but whose cited source is older than a newer source in the wiki that addresses the same topic. If a newer source supersedes the claim, flag it as a candidate for `superseded` status. Again, do **not** overwrite — flag for human decision.

### 3. Concepts mentioned but lacking a page

While reading, note every `[[wikilink]]` that resolves to a page that does not exist (a dangling wikilink), as well as inline mentions of concepts or entities that are clearly significant but have not been linked at all. Both are coverage gaps.

### 4. Missing cross-references

Identify pairs of pages that discuss closely related ideas but do not link to each other. A concept page that never mentions a tightly coupled sibling concept, or an entity page that does not link to the concepts it is associated with, is a cross-reference gap.

### 5. Index ↔ reality consistency

This check ensures the index accurately mirrors what actually exists in the wiki — no more, no less.

- **Every wiki page must have an index entry.** Walk `wiki/sources/`, `wiki/entities/`, `wiki/concepts/`, `wiki/syntheses/`, and `wiki/maps/`. For each page found, verify it appears in its category `_index.md` and is reachable from the root `index.md` router.
- **Every index entry must point to a real page.** For each entry in `index.md` and each `_index.md`, verify the target page file exists.
- **Category counts in `index.md` must match the actual file counts** in each `wiki/<category>/` directory (excluding `_index.md` itself).
- **Orphan check:** any page reachable only through its `_index.md` entry but having zero inbound `[[wikilinks]]` from other pages (and not listed in any MOC) is a structural orphan.

Flag each discrepancy with the specific page or entry causing the mismatch.

### 6. Suggested new sources and questions

After reviewing the coverage, suggest:
- Topics or claims that are asserted but not backed by any source currently in `raw/` — these are ingest candidates.
- Open questions the wiki raises that no existing page answers — these are synthesis or future-query candidates.

---

## Optional Accelerator: lint.py

The script `${CLAUDE_SKILL_DIR}/scripts/lint.py` performs the mechanical subset of the lint automatically. It checks only stable, structural properties and will not drift from prose conventions.

### Running the script

```
python3 ${CLAUDE_SKILL_DIR}/scripts/lint.py <wiki-root>
```

Replace `<wiki-root>` with the path to the wiki directory (the one containing `CLAUDE.md` and `wiki/`).

The script exits non-zero if any findings are present and prints a categorized report covering four categories:

| Category | What it catches |
|---|---|
| `broken_links` | `[[wikilinks]]` whose target file does not exist in the vault |
| `orphans` | Pages with no inbound links and not listed in any MOC |
| `missing_frontmatter` | Pages with no YAML frontmatter block, or whose frontmatter lacks a `type` field |
| `unsourced_claims` | Claim lines on `concept`/`entity` pages that lack a provenance marker (heuristic flagging of `UNSOURCED` defects per `conventions.md §4`) |

Navigation scaffolding files — `index.md`, the category `_index.md` files, `overview.md`, and `log.md` — are exempt from `missing_frontmatter` and `broken_links` (they are catalogs/navigation, not content pages) and from `orphans`. Their outbound links still count toward other pages' inbound totals.

### Graceful degradation

The script is **optional**. If Python 3 is unavailable or code execution is not possible on the current surface, perform the same four mechanical checks by reasoning:

- Scan wikilinks by reading pages and checking whether each `[[target]]` corresponds to a file that exists.
- Identify orphans by noting which pages are never referenced in other pages or MOCs.
- Check frontmatter completeness by reading each page's YAML block.
- Flag un-cited claims by scanning concept and entity pages for claim lines without a `^[` provenance marker.

The prose semantic pass (§ above) must always be performed regardless of whether the script runs.

---

## The Fix Loop

Lint is iterative. After producing the initial report, work through findings in this loop:

```
run checks  →  prioritize findings  →  fix  →  re-run checks  →  confirm clean
```

**Step 1 — Run checks.** Execute the prose semantic pass. Optionally run `lint.py` first for a fast mechanical baseline.

**Step 2 — Prioritize findings.** Address in this order:
1. Broken links and missing frontmatter (structural blockers)
2. Index ↔ reality inconsistencies (navigation correctness)
3. Orphaned pages (discoverability)
4. Un-cited claims (`UNSOURCED` defects, provenance integrity)
5. Contradictions and stale claims (semantic accuracy — flag only, do not resolve)
6. Missing cross-references and coverage gaps (enrichment)

**Step 3 — Fix.** Apply fixes for categories 1–4 directly. For categories 5–6, produce a flagged report for human review.

**Step 4 — Re-run checks.** After fixes, re-run the full lint (prose pass + script if available) to confirm no regressions and that all targeted findings are resolved.

**Step 5 — Confirm clean.** Report the final state: findings resolved, findings flagged for human decision, and any new suggestions.

---

## Handling Contradictions and Stale Claims

When the lint surfaces a contradiction between sourced claims, do **not** auto-resolve. Follow the append-and-flag protocol from `references/conventions.md §5`:

- Record both claims in a `[!conflict]` callout on the relevant page, preserving provenance for each side.
- Set `status: contested` on the affected claim block.
- Add the page to the lint report under "Contradictions — human decision required."

The human maintainer decides which claim to promote, demote, or leave contested. Claude does not overwrite an existing sourced claim with a newer one unilaterally.

For supersession candidates (newer authoritative value makes the old one obsolete), flag as `status: superseded` candidate and present both values with dates — again, human decides.

---

## Output Format

Return the lint report in this structure:

```
## Lint Report — <wiki-root> — <date>

### Mechanical findings (script / reasoning)
- broken_links: <count> — [list]
- orphans: <count> — [list]
- missing_frontmatter: <count> — [list]
- unsourced_claims: <count> — [list]

### Semantic findings (prose pass)
- Contradictions: <count> — [details, pages, claims]
- Stale/superseded candidates: <count> — [details]
- Dangling wikilinks (concept gaps): <count> — [list]
- Missing cross-references: <count> — [pairs]
- Index ↔ reality inconsistencies: <count> — [details]

### Suggestions
- Ingest candidates: [topics/sources not yet in raw/]
- Open questions / synthesis candidates: [list]

### Summary
<N> findings require fixes. <M> findings flagged for human decision. Wiki is [clean / needs attention].
```
