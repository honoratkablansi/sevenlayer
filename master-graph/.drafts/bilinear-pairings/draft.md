# Bilinear Pairings: Multiplying Inside Hidden Exponents

*Chapter 11 — Layer 6: The Bedrock · the primitive beneath KZG and the Groth16 verifier*
*Target depth: rigorous · stratum: Elliptic curves & pairings (the prerequisite peak)*

![The pairing e: G₁ × G₂ → G_T sending two source points P, Q to one target element e(P,Q)](figures/bilinear_pairings.svg)

*Figure — the map `e: G₁ × G₂ → G_T`. A point `P` in the blue source group `G₁` and a point `Q` in the red source group `G₂` are fed to the pairing, producing a single element `e(P,Q)` in the purple target group `G_T`. Scaling the inputs raises the target element to the power `a·b`: `e(aP, bQ) = e(P, Q)^{ab}`.*

> **Animation:** [`animations/bilinear_pairings.mp4`](animations/bilinear_pairings.mp4) — the three groups appear; `P` and `Q` are paired into `e(P,Q)`; then the inputs are scaled to `aP`, `bQ` (here `a=2`, `b=4`) and the target jumps to `e(P,Q)^{a·b} = e(P,Q)^8`, with the concrete parameters `GF(23)`, `r=3`, `k=2` shown beneath the bilinearity identity.

---

> ### Math you'll need (sidebar)
> Before this section you should be comfortable with:
> - **Cyclic groups** — generators, group order, and the group operation, written additively (point addition) or multiplicatively (exponentiation `g^x`).
> - **Elliptic-curve groups** — the points of `E` form an abelian group; scalar multiplication `aP = P + P + … + P`.
> - **The discrete-logarithm problem** — given `P` and `aP`, recovering `a` is infeasible. This is the bet the whole tower rests on, and the reason a pairing must NOT recover exponents.
> - **Finite fields and extensions** — `F_q` versus `F_{q^k}`; the **embedding degree** `k` decides which extension the pairing's output lives in.
> - **The r-torsion subgroup `E[r]`** and prime-order subgroups — where the source groups `G₁, G₂` live.
> - **Roots of unity** — the `r`-th roots of unity `μ_r` in `F_{q^k}^*`, where the pairing **value** lives (it is *not* a curve point).
>
> *Carried in from Ch 9:* the polynomial-commitment interface (commit / open / verify) that pairings are about to *build*. *From Ch 2/3:* the sealed-envelope and Powers-of-Tau ceremony — pairings are the mechanism that turns `g^{p(τ)}` into a checkable commitment. The slogan you've met but not yet earned: a pairing is *"a bilinear multiplication you can do on hidden exponents."* Here we earn it.

---

## Pre-rigorous — one multiplication on hidden exponents

For two chapters you have used a polynomial commitment as a **sealed envelope**: the prover hides a value `g^x`, and later the verifier wants to be sure of some *relation* among the hidden values — say, that one hidden number is the **product** of two others — without ever opening the envelopes.

Ordinary group exponentiation can **add** hidden exponents: `g^x · g^y = g^{x+y}`. It cannot **multiply** them. A bilinear pairing is the tool that buys you exactly one multiplication on hidden exponents.

The figure shows the shape of it. There are three groups — a blue `G₁`, a red `G₂`, and a purple target `G_T` — and a map `e` that eats one point from each source group and lands a single element in the target. Drop `P` into `G₁` and `Q` into `G₂`; the pairing produces `e(P,Q)` over in `G_T`.

Now the move that matters. **Scale the inputs** — take `aP` instead of `P`, `bQ` instead of `Q` — and the target element is raised to the power `a·b`. On a tiny curve over `GF(23)` with `a = 2` and `b = 4`, the pairing of the scaled points equals the original pairing value raised to the **8th** power. You did not learn `a` or `b`; you only confirmed that the hidden multiplication `a·b` happened, sitting safely up in an exponent.

*(No formal definition yet — first the picture of "multiply inside the exponent", then the notation.)*

## Rigorous — earn the identity

A **bilinear pairing** is a map `e: G₁ × G₂ → G_T` between three groups of the same prime order `r`, with two properties:

1. **Bilinearity** — `e` is linear in each argument *separately*:
   > `e(aP, Q) = e(P, Q)^a` and `e(P, bQ) = e(P, Q)^b`.
2. **Non-degeneracy** — if `P, Q` are generators then `e(P, Q) ≠ 1`, so the map is not trivial.

Apply linearity in each slot in turn:

> **`e(aP, bQ) = e(P, bQ)^a = (e(P, Q)^b)^a = e(P, Q)^{ab}`.**

That single line is the whole identity. The product `a·b` lands in the exponent because `e` is linear in *each* argument.

Now locate the groups concretely so none of this is mystical. Take the supersingular curve `E: y² = x³ − x` over `GF(23)`. It has an `r = 3` torsion subgroup, and its **embedding degree is `k = 2`** — `3` divides `23² − 1 = 528` but not `23 − 1 = 22`, so the full 3-torsion `E[3] ≅ ℤ/3 × ℤ/3` and the target group only appear once you pass to the extension field `GF(23²)`.

- `G₁` and `G₂` are independent order-3 lines inside `E[3]`.
- `G_T` is the group `μ₃` of **cube roots of unity** inside `GF(23²)*`.

Take `P = (2, 12)` and `Q = (14t+9, 22t+22)`. The Weil pairing gives

> `e(P, Q) = 19t + 15`,

an element of `GF(23²)*` of multiplicative **order 3** — *not* a curve point. With `a = 2`, `b = 4`:

> `e(aP, bQ) = 4t + 7` and `e(P, Q)^{a·b} = (19t+15)^8 = 4t + 7`.

They are equal. **Bilinearity holds exactly, with no error term.**

This destroys the tempting bad intuitions, explicitly:

1. **The output is NOT a curve point.** It lives in the multiplicative group of a field extension (`μ_r ≤ F_{q^k}^*`), which is exactly why the operation on it is *exponentiation*, not scalar multiplication.
2. **The scalars MULTIPLY in the exponent.** `a·b = 8`, not `a+b = 6`. That is what "linear in *each* argument" forces — pull `a` out of the first slot and `b` out of the second, and they compose multiplicatively.
3. **You learned `a·b` only as an exponent, never `a` or `b`.** Recovering `a` from `aP` is the discrete-log problem, which is assumed infeasible. A pairing checks a multiplicative relation; it never inverts one.

> **Note (worked exponent vs reduced exponent).** The scene shows the honest exponent `a·b = 8`. Because `e(P,Q)` has order 3, `e^8 = e^2` — so `8 mod 3 = 2` is a *consequence* of the order, not a contradiction. Both `4t+7 = (19t+15)^8` and `4t+7 = (19t+15)^2` are true and name the same element.

## Post-rigorous — both halves at once

Rebuild the intuition on the rigor. "Multiply inside the hidden exponent" **is** the identity `e(aP, bQ) = e(P, Q)^{ab}`: the picture of two scaled source points feeding one boosted target element is precisely linearity applied in each slot. Pair each picture with its statement:

| Picture (heuristic) | Formal statement |
|---|---|
| A pairing multiplies two hidden exponents | `e` bilinear ⇒ `e(aP, bQ) = (e(P,Q)^b)^a = e(P,Q)^{ab}` |
| The answer is not a curve point — you raise it to powers | `G_T = μ_r ≤ F_{q^k}^*`; `e(P,Q) = 19t+15` has order 3 in `GF(23²)^*` |
| Scaling inputs multiplies (not adds) the exponent | linear in *each* slot ⇒ `e(2P, 4Q) = e(P,Q)^{2·4} = e(P,Q)^8 = 4t+7`, not `^{2+4}` |
| It checks the product without revealing the secrets, on the right curves | recovering `a` from `aP` is discrete-log (hard); `e` is computable only for small embedding degree `k` |

Now the **book role** is obvious. A verifier who wants to check a multiplicative relation among hidden exponents compares two pairing values — this is the **single pairing-product verification equation** behind KZG's opening check and the **Groth16 verifier** (a few group elements, one pairing equation).

Two boundaries stay sharp:

- **A pairing CHECKS a multiplicative relation; it never INVERTS one.** It does not recover exponents, so it does not break discrete log — if it did, the whole tower would fall.
- **This only works on pairing-friendly curves.** The embedding degree `k` must be *small* so `G_T` lives in a small extension `F_{q^k}` where `e` is computable. **BN254** and **BLS12-381** are engineered for small `k`; **secp256k1**'s `k` is astronomically large, so it has no usable pairing. That constraint — plus the attack that *sizes* these curves, the Extended Tower Number Field Sieve — is why Layer 6 names BLS12-381 specifically.

---

> ### Rediscover it (you could have invented this)
> You want one **multiplication** on hidden exponents, so a verifier can check a product relation without learning the secrets. Demand a map `e: G₁ × G₂ → G_T` that is **linear in each argument**:
> - `e(aP, Q) = e(P, Q)^a`
> - `e(P, bQ) = e(P, Q)^b`
>
> Apply both in turn:
> > `e(aP, bQ) = e(P, bQ)^a = (e(P, Q)^b)^a = e(P, Q)^{ab}`.
>
> The product in the exponent is **forced**, not chosen. Add **non-degeneracy** (`e(P,Q) ≠ 1`) so the comparison means something, and you have invented the bilinear pairing: a verifier confirms `a·b` in the exponent by comparing `e(aP, bQ)` with `e(P, Q)^{ab}`, learning the *relation* without learning the *secrets*. **You derived it; you did not receive it.**

---

## Check yourself (comprehension set)

**Recall.** What is a bilinear pairing? Name its domain and codomain, and state the one identity that makes it "bilinear".
> *Answer:* A non-degenerate map `e: G₁ × G₂ → G_T` between three prime-order groups, linear in each argument, with `e(aP, bQ) = e(P, Q)^{ab}`. `G₁, G₂` are `r`-torsion subgroups of an elliptic curve over `F_q`; `G_T` is the group of `r`-th roots of unity `μ_r` in `F_{q^k}^*`.
> *If you miss this →* revisit **roots of unity (`μ_r` in `F_{q^k}^*`, where the pairing value lives)**.

**Apply.** On `E: y² = x³ − x` over `GF(23)` with `r = 3` and `k = 2`, `e(P, Q) = 19t+15` (order 3). For `a = 2`, `b = 4`, what is `e(aP, bQ)`, and why is it `e(P, Q)^8` rather than `e(P, Q)^6`?
> *Answer:* `e(aP, bQ) = e(P, Q)^{a·b} = e(P, Q)^8 = (19t+15)^8 = 4t+7`. The **product** `a·b = 8`, not the **sum** `a+b = 6`, because the pairing is linear in each argument separately. (Order 3 makes `e^8 = e^2`, the same element.)
> *If you miss this →* revisit **cyclic groups (generators, order, additive vs multiplicative operation)**.

**Transfer.** A KZG / Groth16 verifier wants to confirm a multiplicative relation among hidden exponents without learning them. Why is a bilinear pairing the right tool, and what does it crucially NOT let the verifier do?
> *Answer:* Encode secrets as exponents (`g^x = xP`); the pairing turns exponent multiplication into a check on visible elements: `e(aP, bQ) = e(P, Q)^{ab}`, the single pairing-product equation behind KZG opening and Groth16 verify. It does **not** recover `a` or `b` (that is the discrete-log problem, assumed hard) — it checks a relation, never inverts one. Only small-`k` pairing-friendly curves (BN254/BLS12-381) make it computable.
> *If you miss this →* revisit **the discrete-logarithm problem (given `P`, `aP`, recovering `a` is infeasible)**.

**Rediscover.** You want an operation that "multiplies hidden exponents" so a verifier can check a product relation without learning the exponents. What three properties must it have, and how do they force `e(aP, bQ) = e(P, Q)^{ab}`?
> *Answer:* (1) `e: G₁ × G₂ → G_T` (one element from each source group into a third); (2) linear in the first argument: `e(aP, Q) = e(P, Q)^a`; (3) linear in the second: `e(P, bQ) = e(P, Q)^b`. Apply (2) then (3): `e(aP, bQ) = (e(P, Q)^b)^a = e(P, Q)^{ab}` — the product is forced. Add non-degeneracy (`e(P, Q) ≠ 1`) and you have the bilinear pairing.
> *If you miss this →* revisit **elliptic-curve groups (points form an abelian group; `aP = P+…+P`)**.

---

*Verification: all numeric claims match the Sage manifest (`q=23`, `r=3`, `k=2`, `a=2`, `b=4`, `e(P,Q)=19t+15`, `e(aP,bQ)=4t+7`, `bilinear_holds=true`); the manim scene's displayed values pass `validate_scene_values` with no drift; scorecard PASS. Figure and animation generated correct-by-construction by `scripts/recipes/bilinear-pairings.sage` and `scripts/scenes/bilinear-pairings.py`.*
