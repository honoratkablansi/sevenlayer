# Math-explainer concept drafts

Chapter-grade draft bundles produced by the `math-explainer` skill (full six-stage pipeline; live Sage + manim + graphify; every bundle schema-valid with a **scorecard PASS**, a **CLEAN** prose lint, and a **7-persona editorial soft-gate PASS**). Each `<slug>/` holds `draft.md` (three Tao phases + "Math you'll need" + "rediscover-it" box + comprehension set), the five stage artifacts as JSON, a correct-by-construction Sage figure under `figures/`, and a manim animation under `animations/`.

## Chapter 6 — Arithmetization
- [R1CS](r1cs/draft.md) — a computation as rows of `(A·z)∗(B·z) = (C·z)` that a witness must satisfy.

## Chapter 7 — Fingerprints (why polynomials catch liars)
- [Finite fields](finite-fields/draft.md) — the arithmetic floor: `F_p`, arithmetic mod p with add/subtract/multiply/divide.
- [Freivalds' algorithm](freivalds/draft.md) — the first fingerprint: verify `AB = C` with one random vector, error ≤ `1/|F|`.
- [Reed–Solomon encoding](reed-solomon/draft.md) — a message as a low-degree polynomial evaluated at many points; distinct messages disagree almost everywhere.
- [Lagrange interpolation](lagrange-interpolation/draft.md) — the bridge from a table of values to the unique low-degree polynomial through them.
- [Multilinear extension (MLE)](multilinear-extension/draft.md) — the unique multilinear polynomial agreeing with a table on the Boolean hypercube.
- [Schwartz–Zippel lemma](schwartz-zippel/draft.md) — why a low-degree polynomial's roots are rare: one random spot-check catches a liar.

## Chapter 8 — The one idea
- [Sum-Check protocol](sum-check/draft.md) — collapse an exponential hypercube sum to a single random evaluation, one variable per round.

## Chapter 9 — IOPs, commitments, and the SNARK recipe
- [Sigma protocols](sigma-protocols/draft.md) — commit→challenge→response proof of knowledge (Schnorr); two transcripts extract the witness (special soundness).
- [Merkle trees](merkle-trees/draft.md) — hash a list of leaves into one root; an authentication path proves one leaf without revealing the rest.

## Chapter 11 — The bedrock (groups, curves, pairings, commitments)
- [Discrete logarithm problem](discrete-log/draft.md) — given `g` and `h = g^x` in a prime-order group, recovering `x` is believed infeasible: the one-way street under DLog crypto.
- [Elliptic-curve groups](elliptic-curves/draft.md) — the chord-and-tangent group law over a finite field; fast forward (`aP`), hard reverse (the EC discrete log).
- [Pedersen commitment](pedersen-commitment/draft.md) — `gᵐhʳ`: perfectly hiding, computationally binding (breaking binding solves the discrete log).
- [Bilinear pairings](bilinear-pairings/draft.md) — `e(aP,bQ) = e(P,Q)^{ab}`: a verifier checks a multiplicative relation among hidden exponents.
- [FRI low-degree testing](fri/draft.md) — one folding round halves a polynomial's degree and domain, testing low-degreeness without reading the whole codeword.

## Editorial status

All **15** drafts pass the 7-persona editorial soft-gate (`critical = 0`), via three review→revise→re-review QA cycles (each hardened the skill before the next batch):
- **Cycle 1** (5, Claude-drafted): undefined load-bearing terms, list-itis, a `logₘ`-vs-`log_g` notation bug, `n`/`v` drift, QA-footer endings.
- **Batch B1** (5, Codex-drafted, Claude-audited): terms used-but-not-defined (finite field, linear combination), a count-announce tic, chapter-number/self-reference defects, a jargon-wall payoff, unreliable graphify exact-label matches.
- **Batch B2** (5, Codex-drafted, Claude-audited): **two-moduli confusion** (prose naming only `q` while showing mod-`p` elements), undefined `subgroup`/`oracle`/`the reverse problem`, coordinate/notation drift, a FRI label that didn't resolve.

The skill grew with each cycle: `references/draft-quality.md` (12 rules, incl. two-moduli + a named recurring-offender list), `references/dependency-protocol.md` (graph-evidence + label-alias protocol), and `scripts/draft_lint.py` (now catches pipeline/QA vocabulary, count/roadmap/anaphora tics, and self-chapter-references — 61 skill tests). Drafter reports: [`_audit/B1.json`](_audit/B1.json), [`_audit/B2.json`](_audit/B2.json); the pilot's full review record: [`schwartz-zippel/persona-review.md`](schwartz-zippel/persona-review.md).

*Generators live in the skill: Sage recipes at `.claude/skills/math-explainer/scripts/recipes/<slug>.sage`, manim scenes at `.claude/skills/math-explainer/scripts/scenes/<slug>.py`.*
