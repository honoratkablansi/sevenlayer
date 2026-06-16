# Math-explainer concept drafts

Chapter-grade draft bundles produced by the `math-explainer` skill (full six-stage pipeline; live Sage + manim + graphify; every bundle schema-valid with a **scorecard PASS** and a **CLEAN** prose lint). Each `<slug>/` holds `draft.md` (three Tao phases + "Math you'll need" + "rediscover-it" box + comprehension set), the five stage artifacts as JSON, a correct-by-construction Sage figure under `figures/`, and a manim animation under `animations/`.

## Chapter 6 — Arithmetization
- [R1CS](r1cs/draft.md) — rank-1 constraint system: a computation written as rows of `(A·z)∗(B·z) = (C·z)` that a witness must satisfy. ([figure](r1cs/figures/r1cs.svg) · [animation](r1cs/animations/r1cs.mp4))

## Chapter 7 — Fingerprints (why polynomials catch liars)
- [Finite fields](finite-fields/draft.md) — the engine's arithmetic floor: a finite number system (`F_p`, arithmetic mod p) where you can add, subtract, multiply, and divide. ([figure](finite-fields/figures/finite-fields.svg) · [animation](finite-fields/animations/finite-fields.mp4))
- [Freivalds' algorithm](freivalds/draft.md) — the first fingerprint: verify `AB = C` with one random vector, failing to catch an error with probability ≤ `1/|F|`. ([figure](freivalds/figures/freivalds.svg) · [animation](freivalds/animations/freivalds.mp4))
- [Reed–Solomon encoding](reed-solomon/draft.md) — encode a message as a low-degree polynomial evaluated at many points; distinct messages disagree almost everywhere (distance). ([figure](reed-solomon/figures/reed-solomon.svg) · [animation](reed-solomon/animations/reed-solomon.mp4))
- [Lagrange interpolation](lagrange-interpolation/draft.md) — the bridge from a table of values to the unique low-degree polynomial running through them. ([figure](lagrange-interpolation/figures/lagrange-interpolation.svg) · [animation](lagrange-interpolation/animations/lagrange-interpolation.mp4))
- [Multilinear extension (MLE)](multilinear-extension/draft.md) — the unique multilinear polynomial agreeing with a table on the Boolean hypercube, extended to the whole space. ([figure](multilinear-extension/figures/multilinear-extension.svg) · [animation](multilinear-extension/animations/multilinear-extension.mp4))
- [Schwartz–Zippel lemma](schwartz-zippel/draft.md) — why a low-degree polynomial's roots are rare: one random spot-check catches a liar with overwhelming probability. ([figure](schwartz-zippel/figures/schwartz_zippel.svg) · [animation](schwartz-zippel/animations/schwartz_zippel.mp4))

## Chapter 8 — The one idea
- [Sum-Check protocol](sum-check/draft.md) — collapse an exponential hypercube sum to a single random evaluation, one variable per round. ([figure](sum-check/figures/sum_check.svg) · [animation](sum-check/animations/sum_check.mp4))

## Chapter 11 — The bedrock (pairings & commitments)
- [Pedersen commitment](pedersen-commitment/draft.md) — `gᵐhʳ`: perfectly hiding, computationally binding (breaking binding solves the discrete log). ([figure](pedersen-commitment/figures/pedersen-commitment.svg) · [animation](pedersen-commitment/animations/pedersen-commitment.mp4))
- [Bilinear pairings](bilinear-pairings/draft.md) — `e(aP,bQ) = e(P,Q)^{ab}`: a verifier checks a multiplicative relation among hidden exponents. ([figure](bilinear-pairings/figures/bilinear_pairings.svg) · [animation](bilinear-pairings/animations/bilinear_pairings.mp4))

## Editorial status

All **10** drafts pass the 7-persona editorial soft-gate (`critical = 0`), via two review→revise→re-review QA cycles:
- **Cycle 1** (first 5, Claude-drafted): surfaced undefined load-bearing terms, list-itis, a `logₘ`-vs-`log_g` notation bug, `n`/`v` drift, QA-footer endings.
- **Cycle 2 / batch B1** (Codex-drafted, Claude-audited): surfaced load-bearing terms used-but-not-defined (finite field, linear combination), a count-announce tic, chapter-number/self-reference defects, a jargon-wall payoff, and an unreliable graphify exact-label match.

Each cycle hardened the skill so the next batch is generated against a better skill: `references/draft-quality.md` (11 rules), `references/dependency-protocol.md` (graph-evidence protocol), and `scripts/draft_lint.py` (now catches pipeline/QA vocabulary, count/roadmap/anaphora tics, and self-chapter-references). The pilot's full review record is in [`schwartz-zippel/persona-review.md`](schwartz-zippel/persona-review.md); the B1 drafter report is in [`_audit/B1.json`](_audit/B1.json).

*Generators live in the skill: Sage recipes at `.claude/skills/math-explainer/scripts/recipes/<slug>.sage`, manim scenes at `.claude/skills/math-explainer/scripts/scenes/<slug>.py`.*
