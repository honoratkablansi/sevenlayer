# Schwartz–Zippel: Why Polynomials Catch Liars

*Chapter 7 — Fingerprints · the probabilistic-checking primitive beneath Layer 4*
*Target depth: rigorous · stratum: Algebra I (fields & univariate polynomials)*

![Two degree-2 polynomials over F_101 agreeing at exactly one point](figures/schwartz_zippel.svg)

*Figure — `p(x)=3x²+5x+7` (blue) and `q(x)=3x²+2x+7` (red) plotted over all of F_101. They coincide at exactly one of the 101 points, x = 0.*

> **Animation:** [`animations/schwartz_zippel.mp4`](animations/schwartz_zippel.mp4) — the random-point spot-check: blue dots (p) and red dots (q) are dropped point by point; the single green flash marks the one agreement (x = 0), and the bound `d/|F| = 2/101` appears as the worst-case failure probability.

---

> ### Math you'll need (sidebar)
> Before this section you should be comfortable with:
> - **Polynomials over a finite field** — degree, roots, and evaluation at a point.
> - **The bounded fundamental theorem of algebra** — a *nonzero* polynomial of degree `d` over a field has **at most `d` roots**. This single fact carries the whole proof.
> - **The union bound** and basic probability ("almost always").
> - **Modular arithmetic in F_p** / finite fields: arithmetic wraps around `|F|`.
> - **Big-O / counting.**
>
> *Carried in from Ch 6:* arithmetization and the spreadsheet metaphor, with Schwartz–Zippel met as a slogan — *"checking one random cell catches a forged table."* Here we prove it.

---

## Pre-rigorous — one random poke

Picture a forger who hands you a giant filled-out spreadsheet and swears every cell obeys the rules. Re-checking the whole sheet is hopeless. So you do something almost insolent: you point at **one random cell** and check only that.

The figure shows why this works. Encode each side of a claim as a polynomial; two honest sides give the *same* polynomial, a forged side gives a *different* one. Two different low-degree polynomials are like two curves that can cross only a few times — over F_101 our blue `p` and red `q` touch at **exactly one point** (x = 0) out of 101. So a finger dropped at random almost always lands where they disagree, and the lie is exposed. You did not need to read the whole sheet; you needed one lucky-by-design poke.

*(No symbols yet beyond naming p and q — the "why" comes before the notation.)*

## Rigorous — earn the bound

Let `F` be a finite field, and let `p, q` be polynomials over `F` of degree at most `d`, with `p ≠ q`.

Form the difference **`D = p − q`**. Because `p ≠ q`, `D` is a **nonzero** polynomial of degree at most `d`. By the bounded fundamental theorem of algebra, a nonzero degree-`≤d` polynomial has **at most `d` roots** in `F`. Every agreement point of `p` and `q` is exactly a root of `D`, so:

> **p and q agree at no more than `d` of the `|F|` field points.**

Now draw `r` uniformly at random from `F`. Then

> **Pr[ p(r) = q(r) ] = Pr[ D(r) = 0 ] = (#roots of D) / |F| ≤ d / |F|.**

This destroys the tempting bad intuitions, explicitly:

1. **"Passed one check ⇒ equal" is false.** Acceptance only bounds the error by `d/|F|`; it never *proves* equality.
2. **"Distinct degree-d polynomials can agree arbitrarily often" is false.** The cap is exactly `d`, the degree of `D`.
3. **The randomness lives in `r`, not in `p` or `q`.** The polynomials are arbitrary, fixed, adversarial choices; only the evaluation point is random.

For our concrete pair, `D = p − q = 3x`, which has degree 1, so it has **at most one root** — realized at `x = 0` — and the realized error is `1/101`, comfortably under the degree-2 worst-case bound `2/101 ≈ 1.98%`.

> **Note (worst case vs realized).** `2/101` is the worst-case Schwartz–Zippel bound for *any* distinct degree-2 pair. `1/101` is what *this* pair actually achieves, because its difference happens to be degree 1. They are different numbers and neither is a typo of the other.

## Post-rigorous — both halves at once

Rebuild the intuition on the rigor. The "random cell catches a forged table" slogan **is** the inequality `Pr ≤ d/|F|`, with the spreadsheet's algebraic identity playing the role of `D`. Pair each picture with its statement:

| Picture (heuristic) | Formal statement |
|---|---|
| Checking one random cell catches a forged spreadsheet | `Pr_{r∈F}[p(r)=q(r)] = Pr[D(r)=0] ≤ d/|F|`, `D = p−q` |
| Two different low-degree curves cross only a few times | `D` nonzero of degree `≤ d` ⇒ `≤ d` roots ⇒ `≤ d` agreements |
| A bigger field makes the test more reliable | `p, q` fixed; only `|F|` grows, so `(#roots)/|F| ≤ d/|F|` shrinks |
| Our pair almost never agrees (one green point in 101) | `D = 3x` ⇒ one root `x=0`; realized `1/101 ≤ 2/101` |

Now the **soundness knob** is obvious: to shrink the error you either grow `|F|` (the denominator rises while the `≤ d` bad points stay put) or lower the encoding degree `d`. This is precisely the primitive beneath Layer 4 — a whole-table claim (R1CS / AIR / PLONKish) collapses to one random evaluation, and sum-check and polynomial commitments are built on the same move.

Keep one boundary sharp: this is an **unconditional, root-counted** collision bound — *not* a computational, assumption-based cryptographic hash. Ch 11/12 need the other kind, and conflating them corrupts those security models.

---

> ### Rediscover it (you could have invented this)
> Suppose you know only one fact: *a nonzero degree-`d` polynomial has at most `d` roots.* You want a cheap test that two polynomials `p, q` are equal.
>
> Form `D = p − q`. If `p = q` then `D ≡ 0`. If `p ≠ q` then `D` is nonzero of degree `≤ d`, so it has `≤ d` roots. Pick `r` uniformly in `F` and test `D(r) = 0`:
> - `D(r) ≠ 0` ⇒ you are **certain** `p ≠ q`.
> - `D(r) = 0` ⇒ you accept `p = q`, wrong only if `r` landed on one of the `≤ d` roots — probability `≤ d/|F|`.
>
> You have just rediscovered Schwartz–Zippel: **one random evaluation, error `≤ d/|F|`, driven down by a bigger field.** You derived it; you did not receive it.

---

## Check yourself (comprehension set)

**Recall.** State the univariate Schwartz–Zippel bound: if `p` is a nonzero polynomial of degree `d` over a finite field `F`, what is the probability that `p(r) = 0` for a uniformly random `r ∈ F`, and why?
> *Answer:* At most `d/|F|`. A nonzero degree-`d` polynomial has at most `d` roots, and `r` is drawn uniformly from `|F|` points, so the chance of hitting a root is `(#roots)/|F| ≤ d/|F|`.
> *If you miss this →* revisit **the bounded fundamental theorem of algebra (≤ d roots)**.

**Apply.** Let `p(x) = 3x² + 5x + 7` and `q(x) = 3x² + 2x + 7` over F_101. At how many points do they agree, which point(s), and what is the chance a single random evaluation fails to distinguish them?
> *Answer:* They agree where `p − q = 3x = 0`, i.e. only at `x = 0` — exactly 1 agreement point. A single random `r` fails to distinguish them with probability `1/101 ≈ 0.99%` (never more than the degree-2 worst-case `2/101 ≈ 1.98%`).
> *If you miss this →* revisit **polynomials over a finite field (degree, roots, evaluation)**.

**Transfer.** A prover claims a giant computation's whole constraint table is satisfied. Why does checking one random field point catch a cheating prover with high probability, and what makes the guarantee shrink toward zero error?
> *Answer:* The table identity is encoded as a polynomial identity `P = 0`; a cheating prover's `P` is a nonzero low-degree polynomial, nonzero at all but `≤ d` of the `|F|` points, so a random challenge exposes the cheat with probability `≥ 1 − d/|F|`. Error shrinks by enlarging `|F|` (denominator grows, `≤ d` bad points fixed) or lowering the encoding degree `d`.
> *If you miss this →* revisit **the union bound (basic probability)**.

**Rediscover.** Knowing only that a nonzero degree-`d` polynomial has at most `d` roots, derive a cheap test that two polynomials `p, q` are equal, and give its failure probability — what do you evaluate, and how confident are you after one random check?
> *Answer:* Form `D = p − q`. If `p = q`, `D ≡ 0`; if `p ≠ q`, `D` is nonzero of degree `≤ d` with `≤ d` roots. Pick `r` uniformly in `F`, test `D(r) = 0`. `D(r) ≠ 0` ⇒ certain `p ≠ q`. `D(r) = 0` ⇒ accept `p = q`, wrong only if `r` is one of the `≤ d` roots — probability `≤ d/|F|`. That is Schwartz–Zippel.
> *If you miss this →* revisit **modular arithmetic in F_p / finite fields**.

---

*Verification: all numeric claims match the Sage manifest (`field 101`, `agreement_points [0]`, `num_agreements 1`); the manim scene's displayed values pass `validate_scene_values` with no drift; scorecard PASS. Figure and animation generated correct-by-construction by `scripts/recipes/schwartz_zippel.sage` and `scripts/scenes/schwartz_zippel.py`.*
