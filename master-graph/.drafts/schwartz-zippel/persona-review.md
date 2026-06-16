# Persona review — schwartz-zippel (pilot)

**Round 1 — Soft-gate: FAIL** (`critical = 6`). **Round 2 (after revision) — Soft-gate: PASS** (`critical = 0`).

> **Re-review (post-revision).** Re-ran the four personas that held all criticals / the math + slop risk: Gottlieb **SHIP** (both prior criticals resolved: list→prose, table→sentence), Lay Reader **SHIP** (all 4 prior criticals resolved — finite field/`|F|`/root taught inline; FTA renamed to the factor theorem with intuition), Domain Expert **SHIP** ("would survive specialist review"; deg(D)≤d, "almost always" qualified, multivariate note added), AI-Slop Detector **SHIP** (em-dash overuse fixed, no new tells). The other three personas held 0 criticals in round 1 and the revision only improves their concerns. `draft_lint.py` reports CLEAN. Remaining items are advisory minors.

---

## Round 1 (original draft)

**Panel:** 7 personas (book-review skill). **Soft-gate:** FAIL — `critical = 6 > 0`. Draft must not ship as written.

| Persona | Verdict | Critical | Important | Minor |
|---|---|---|---|---|
| Robert Gottlieb (voice/cadence) | REVISE | 2 | 3 | 3 |
| Lay Reader (accessibility) | REVISE | 4 | 5 | 3 |
| Domain Expert (math accuracy) | REVISE | 0 | 4 | 3 |
| Copyeditor (mechanics) | SHIP | 0 | 0 | 6 |
| Enjoyment Reader (momentum) | REVISE | 0 | 3 | 2 |
| AI-Slop Detector | SHIP | 0 | 1 | 3 |
| First-Time Visitor (hook) | SHIP | 0 | 0 | 2 |
| **Total** | **BLOCK** | **6** | **16** | **22** |

## Critical (gate-blocking)

- **[Lay Reader] "Finite field" / `F` / `|F|` is never defined, yet the whole bound `d/|F|` and the "bigger field ⇒ more reliable" punchline rest on it.** A non-expert (the book's target) cannot feel the central formula. → Add a short paragraph defining a finite field and `|F|` = number of points (101 here) before the Rigorous section.
- **[Lay Reader] Prerequisites are listed but not supplied**, and the Rigorous section then leans on them. → Teach the 2–3 load-bearing prereqs inline (finite field, `|F|`, ≤d roots) or make the section self-contained.
- **[Lay Reader] `|F|` notation never glossed** (a generalist reads `|·|` as absolute value). → "where `|F|` is the number of points in the field."
- **[Lay Reader] "Bounded fundamental theorem of algebra" asserted with no intuition** (and it collides with the reader's half-memory of the classic FTA). Corroborated by Domain Expert (important: misleading misnomer) and First-Time Visitor (minor). → Give one sentence of intuition for "a nonzero degree-d polynomial has ≤ d roots," and rename (it is the factor/root-count theorem, not the FTA).
- **[Gottlieb] The numbered 1-2-3 in "Rigorous"** is mechanical enumeration dressed as rigor (assertions about the proof, not proof steps). → Argue in prose or cut to the one that matters.
- **[Gottlieb] The "Picture / Formal statement" table** restates a pairing the preceding sentence already made (listicle in formalwear). Corroborated by Enjoyment Reader (important). → Write out one or two pairings as prose; drop the grid.

## Convergent important themes (multiple personas)

- **Triple/quadruple repetition** of the `D = p−q` derivation across body + "Rediscover it" sidebar + comprehension item (Gottlieb, Enjoyment Reader). → Keep one home for the rediscovery; cut the others.
- **Chapter ends on a Sage "scorecard PASS" QA footer** instead of a forward-looking beat (Gottlieb, Enjoyment Reader). → End on the "sum-check/PCS are the same move" tease; move the verification note to metadata.
- **Math precision** (Domain Expert): "the cap is exactly `d`" should be `deg(D) ≤ d` (the example has deg D = 1 < 2); "almost always" is only true once `|F| ≫ d`; only the univariate case is covered (note the multivariate generalization Layer 4 actually uses).
- **"comprehension set" / "correct-by-construction"** AI-vocabulary residue in headings/footer (Gottlieb, AI-Slop Detector).

## Strengths (consensus — keep these)

- **Opening/hook is excellent** — First-Time Visitor SHIP ("one of the strongest openings I've reviewed"); Gottlieb, Enjoyment Reader, and Lay Reader all praise the forger/"one random poke" scene and the word "insolent."
- **Math is sound** — Domain Expert found 0 critical errors; the worst-case (2/101) vs realized (1/101) distinction is handled correctly and honestly.
- **Very low AI-slop** — AI-Slop Detector SHIP ("a poor target for my lens"); no promotional adjectives, listicle abstracts, hedging chains, or AI vocabulary.
- **Clean mechanics** — Copyeditor SHIP (only minor notation/spacing drift).

## Systemic note

These critical/important patterns (undefined load-bearing terms; list-itis; triple repetition; QA-footer ending; "bounded FTA" naming) are pipeline/template artifacts — the other four drafts were modeled on this pilot and very likely share them. The highest-leverage fix is to tune the skill (SKILL.md / pipeline.md guidance + possibly the scorecard) before scaling, then revise the existing five.
