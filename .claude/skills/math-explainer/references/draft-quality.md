# Draft-quality rules (what makes the prose ship-worthy)

The scorecard gates *method structure*; these rules gate *reader experience*. They come from
editorial-panel findings. Apply them while writing Stage 3 prose and assembling Stage 6, and
run `scripts/draft_lint.py <draft.md>` before shipping (it must report CLEAN).

1. **Teach load-bearing terms inline — don't just list prerequisites.** The "Math you'll need"
   sidebar must *explain* the two or three facts the proof actually rests on (e.g. what a finite
   field is, that `|F|` is its number of elements, the ≤d-roots fact) in a sentence each. A
   curious non-expert must be able to follow the rigorous section without leaving the page. A bare
   list of things "you should be comfortable with" is a fail. **Define every term the draft USES,
   not only the term it is ABOUT** — each draft stands alone, so even if a sibling chapter defines
   the finite field / `F_p`, "linear combination", "root", etc., re-define it here at first use
   (one plain sentence) the moment the worked example depends on it. The recurring failure is a
   worked example over `F_p` whose arithmetic "wraps mod p" is never stated, so the numbers look
   wrong to a generalist.

2. **Gloss notation at first use.** `|F|` = "the number of elements in the field"; "root" = "an
   input where the polynomial is zero"; "uniformly at random" = "each element equally likely".
   One short gloss per symbol, the first time it carries weight.

3. **Name things correctly, with one line of intuition.** Never invent a misnomer (e.g. do not
   call the ≤d-roots bound the "fundamental theorem of algebra"). Use the standard name and give
   one sentence of *why* for any fact the proof leans on.

4. **Prose over lists and tables.** Do not dress assertions-about-the-proof as a numbered list to
   look rigorous, and do not restate a slogan→formula pairing as a grid the prose already made.
   Reserve lists for genuinely enumerable items; argue reasoning in sentences.

5. **One home for each derivation.** Derive a result once. Do not repeat the same derivation
   across the body, a sidebar, and a comprehension item — pick the single best location.

6. **End on a forward beat, not a QA footer.** Close with momentum — what this unlocks next —
   not a verification/build note. Pipeline and build vocabulary (scorecard, correct-by-construction,
   manifest, `bundle.json`, script names) MUST NOT appear in reader-facing prose; keep it in
   metadata/front-matter. (`scripts/draft_lint.py` enforces this.)

7. **Be precise about the math.** Distinguish a degree *bound* `d` from an actual degree
   (`deg(D) ≤ d`); qualify probabilistic claims ("almost always" only once `|F| ≫ d`); label
   worst-case vs realized values explicitly so neither reads as a typo of the other.

8. **Headings are reader-facing.** "Check yourself", not "comprehension set". No machine vocabulary
   in any heading or body line.

9. **Vary your sentences; don't enumerate in disguise.** No anaphora — do not stack clauses or bullets
   in identical shape ("It is false that… It is false that…", or a column of bolded "The X is…" stubs).
   When you convert a list to prose, vary the openings. Prefer a short flowing paragraph over a bulleted
   glossary box for "Math you'll need", and never announce a roadmap ("the facts you'll need, one
   sentence each"). A checklist in sentence costume still reads as a list.

10. **Notation must match the prose and the artifacts.** A subscript names exactly what the words say —
    the discrete log of `h` to base `g` is `log_g(h)` (subscript `g`, the base), never `log_m(h)`. Check
    every symbol against the sentence that defines it, use one symbol per quantity (don't drift between
    `n` and `v` for the same count), and match the Stage-4 manifest/ledger.

11. **Cross-chapter references must agree, and each draft has ONE home chapter.** Put a single chapter
    number in the header — never a "Ch 6/7" range (that is the MATH_FOUNDATIONS "first needed" code, not a
    chapter title). A draft must not cite its own home chapter as an external dependency, and a forward beat
    must point to a *later* chapter (check the CHAPTER_BIBLE ordering — e.g. in Ch 7, Freivalds precedes
    Reed–Solomon, so Reed–Solomon's "next" cannot be Freivalds). A shared motif cited in two chapters must
    name the same origin chapter in each.
