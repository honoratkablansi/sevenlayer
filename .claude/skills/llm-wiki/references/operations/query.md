# Operation: Query

<!-- llm-wiki-op: query -->

> Answer a question from the accumulated wiki — index-first, citation-grounded,
> honest about what the wiki does and does not contain. Abstain when evidence is
> absent. Optionally file a good answer back as a `synthesis` page.

## Table of Contents

1. [Step 1 — Index-first read path](#1-index-first-read-path)
2. [Step 2 — Answer only from wiki evidence](#2-answer-only-from-wiki-evidence)
3. [Step 3 — Wikilink citations on factual sentences](#3-wikilink-citations-on-factual-sentences)
4. [Step 4 — Abstain when the wiki lacks evidence](#4-abstain-when-the-wiki-lacks-evidence)
5. [Step 5 — Label parametric (non-wiki) knowledge](#5-label-parametric-non-wiki-knowledge)
6. [Step 6 — Offer to file back as a synthesis page](#6-offer-to-file-back-as-a-synthesis-page)
7. [Hard Rules](#hard-rules)

---

## 1. Index-first read path

**Goal:** navigate to relevant wiki pages efficiently without reading the entire
vault — keep token cost roughly flat as the wiki grows.

Follow this three-level drill-down:

### Level 1 — Root index

Read `index.md` in full. This is the router; it lists categories (sources,
entities, concepts, syntheses, maps), current entry counts, a one-line
"what's here" per category, and links to each `wiki/<cat>/_index.md`.

Identify which category or categories are most likely to contain evidence
for the question.

### Level 2 — Category index

Read the relevant `wiki/<cat>/_index.md` file(s). Each category index holds a
`[[link]] — one-liner` entry per page in that category. Scan the one-liners to
identify the candidate pages most likely to address the question.

If the question spans multiple categories (e.g., an entity that is also the
subject of several concepts), read all relevant category indexes.

### Level 3 — Page(s) and cited raw sources

Read the candidate pages identified in Level 2. When a page's evidence feels
thin or a specific claim needs verification, also read the raw source it cites
(the file in `raw/` named in the page's provenance markers). Reading the raw
source is optional but authoritative when precision matters.

**Do not skip Level 1.** Going directly to a page without checking the index
risks missing a more relevant page and produces an answer grounded in an
incomplete picture of the wiki.

---

## 2. Answer only from wiki evidence

**Goal:** every substantive claim in the answer must be traceable to a wiki
page (or its cited raw source) read in the current session.

- Construct the answer exclusively from the pages read in Step 1.
- Do not inject claims from model memory without explicitly labeling them
  (see Step 5).
- If the pages contain conflicting information (a `[!conflict]` callout),
  surface both positions in the answer — do not silently pick one. Note that
  the conflict is unresolved in the wiki.
- If a page's `status` is `stub` or `draft`, note the lower confidence level.

---

## 3. Wikilink citations on factual sentences

**Goal:** every factual sentence in the answer is attributable to a specific
wiki page, so the user can navigate to the source.

Attach a `[[wikilink]]` citation after each factual sentence, referencing the
page the claim was drawn from:

```
The architecture relies on self-attention, not recurrence. [[Transformer (architecture)]]

The organization was founded in 2019 and employs approximately 200 people. [[OpenAI]] [[2025 Press Coverage]]
```

Rules:
- One citation per factual sentence minimum. Multiple citations are fine when
  the sentence synthesises across pages.
- The wikilink points to the **wiki page**, not to the `raw/` file directly.
  The page's own provenance markers chain back to the raw source.
- Do not cite a page you did not read during the index-first navigation (§1).
  If you believe a page exists but did not read it, go back and read it before
  citing it.
- Interpretive or framing sentences that do not assert a fact do not need a
  citation. When in doubt, cite anyway.

---

## 4. Abstain when the wiki lacks evidence

**Goal:** be honest about the limits of the wiki's coverage rather than filling
gaps with model memory.

**Trigger:** after completing the index-first read path (Step 1), if no
relevant page was found — or if the pages found do not contain evidence
bearing on the specific question — do the following:

1. State the abstention explicitly:

   > "I don't have enough in the wiki to answer that."

2. Describe what was checked: which category indexes were read, what candidate
   pages (if any) were found, and what the gap is.

3. Suggest a concrete next step — a source to ingest that would likely provide
   the evidence needed:

   > "You could ingest [source name or type] to build coverage on this topic.
   > Once ingested, re-ask this question and I can answer from the wiki."

**Partial evidence:** if the wiki contains *some* relevant information but not
enough for a full answer, answer the parts that are evidenced, state the
abstention for the parts that are not, and suggest a source for the gap.
Do not blend partial evidence with unacknowledged model memory.

**Never fabricate:** do not generate a plausible-sounding answer and then cite
a wiki page you did not read or that does not contain the claimed information.
If uncertain whether a page contains the needed information, read it — if it
does not, abstain for that claim.

---

## 5. Label parametric (non-wiki) knowledge

**Goal:** make it unambiguous to the user which parts of the answer come from
the wiki and which come from the model's general training.

There are legitimate uses for model knowledge in a query response — framing
a question, explaining a domain concept that the wiki treats as assumed
background, or noting that a topic exists without asserting wiki-sourced facts
about it. When any such knowledge is used:

**Label it explicitly and visibly:**

```
[general knowledge, not from wiki] The transformer architecture was originally
described in the 2017 "Attention Is All You Need" paper — but this wiki does
not yet have a source page for that paper. [[Transformer (architecture)]] covers
the concept at a high level, drawn from ingested sources.
```

The label must:
- Appear adjacent to the non-wiki content (not buried in a footnote).
- Be unambiguous — "not from wiki", "general knowledge", or "from training,
  not from a wiki source" are all acceptable phrasings.
- Not be used as a license to expand the answer with large blocks of model
  memory. If the wiki lacks coverage, Step 4 (abstain and suggest an ingest)
  is the primary response.

---

## 6. Offer to file back as a synthesis page

**Goal:** when the query produces a well-evidenced, useful answer that draws
across multiple wiki pages, preserve it as a first-class `synthesis` page so
future queries can use it directly.

After delivering the answer, offer to file it back:

> "This answer synthesises [[Page A]], [[Page B]], and [[Page C]]. Would you
> like me to file it as a synthesis page so it's available for future queries?"

If the user accepts, create a `synthesis` page following the conventions in
`references/conventions.md §1` and the frontmatter schema in
`references/conventions.md §6.2`:

```yaml
---
type: synthesis
aliases: []
tags: [synthesis]
created: <today>
updated: <today>
status: draft
question:   # the query that generated this answer
sources: [] # [[wikilinks]] to the concept/entity pages it draws from
concepts: [] # [[wikilinks]] to key concepts
confidence: # low | medium | high
---
```

**Provenance on a synthesis page** follows the two-level chain described in
`references/conventions.md §4.4`: each synthesised claim cites the
concept/entity page it draws from (e.g., `[[Transformer (architecture)]]`),
which in turn carries the raw-source provenance marker back to `raw/`. Do not
attach raw-source markers directly to synthesis claims — cite the intermediate
wiki page.

**"Derived" marker:** add a callout at the top of the synthesis page to make
its status clear:

```
> [!note] Derived page
> This synthesis was generated from a query answer on <date>. It is derived
> from the wiki pages listed in frontmatter and inherits their provenance.
> It has not been independently verified against raw sources.
```

**File and commit:** the mechanics of writing the page, registering it in
`wiki/syntheses/_index.md` and `index.md`, appending a log line, and committing
follow the ingest write path — see `references/operations/ingest.md §6`–`§9`
for the commit mechanics. The synthesis page must meet the same "definition of
done" checks as any ingest-produced page (frontmatter complete, ≥1 outbound
wikilink, registered in its category index and at least one MOC).

**When not to offer:** do not offer a synthesis file-back for:
- Answers that consist primarily of labeled non-wiki (parametric) knowledge.
- Answers where the abstention path was taken (no wiki evidence found).
- Trivial or very short answers (a single sentence drawn from a single page).

---

## Hard Rules

**Index first, always.** Never answer directly from a cached or guessed page
name. Read `index.md` → category `_index.md` → page(s) in order. This is the
primary safeguard against stale or missing coverage going unnoticed.

**No unacknowledged model memory.** Every claim either carries a `[[wikilink]]`
citation to a page read in this session, or is labeled as non-wiki knowledge,
or triggers the abstention behavior. There is no third option.

**Abstain honestly.** "I don't have enough in the wiki to answer that" is a
correct and complete answer when the wiki lacks evidence. It is always
preferable to a confident answer drawn from model memory.

**Surface conflicts, don't resolve them.** If the wiki contains a `[!conflict]`
callout for a claim relevant to the question, report both sides. Resolution is
a human decision — see `references/conventions.md §5.4`.

**Cite pages, not raw files.** Wikilink citations in the answer point to wiki
pages, not to `raw/` files. The chain from wiki page to raw source is encoded
in the page's provenance markers.

**Synthesis pages are ingest-grade writes.** Filing back an answer as a
`synthesis` page is a real wiki write — it must follow all page conventions
(frontmatter, wikilinks, index registration, log line, atomic commit). Do not
write a synthesis page without running through the ingest write and commit
steps in `references/operations/ingest.md`.
