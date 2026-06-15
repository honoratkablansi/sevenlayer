# Multilinear Extension: One Smooth Surface Through the Corners

*Chapter 7 — Fingerprints · the representation the whole engine is built on*
*Target depth: rigorous · stratum: Algebra II (multivariate & multilinear)*

![The bilinear (n=2) extension of four corner values over the unit square](figures/multilinear-extension.svg)

*Figure — the four corner values `1, 4, 3, 6` on the unit square `{0,1}²`, extended to the unique smooth bilinear surface through them. It reproduces the corners, bends in the middle (a saddle), yet is straight along each axis; its center value is the average of the four corners, `3.5`.*

> **Animation:** [`animations/multilinear-extension.mp4`](animations/multilinear-extension.mp4) — four corner values are dropped on the square and the smooth surface fills in; each corner flashes to show the surface *agrees* with `f` there; a point then slides along an edge to show the value moves on a *straight line* (edge midpoint `= 2.0`), and the center lights up at `3.5`, the average of the four corners.

---

> ### Math you'll need (sidebar)
> Before this section you should be comfortable with:
> - **Multivariate polynomials** — and the difference between *total degree* and *individual (per-variable) degree*.
> - **The Boolean hypercube `{0,1}ⁿ`** — the `2ⁿ` corners, used here as an index set for a table of values.
> - **Univariate Lagrange interpolation** and the **low-degree extension (LDE)** — a table of values determines a unique low-degree polynomial through them. The MLE is the multivariate echo of this.
> - **A vector space over a field** — a basis gives unique coordinates; we count dimensions to prove uniqueness.
> - **Modular arithmetic in `F_p`** — the numeric example lives over `F₉₇`.
>
> *Carried in from earlier in Ch 7:* finite-field arithmetic, Lagrange interpolation, and the LDE; and from Ch 6, the idea that *polynomials encode the computation* and that a whole-table claim can be reduced to a claim about one random point. Schwartz–Zippel (just proved) is the tool that will later test MLE identities — here we build the object it tests.

---

## Pre-rigorous — fill in the surface

You have a function that only exists at corners. Think of a table with one number sitting on each corner of a cube: over the unit square `{0,1}²` that is four numbers — say `1`, `4`, `3`, `6` — perched at the four corners and *nothing in between*. You want a single smooth object that **passes through all four corner values** and fills in everything else, so you can probe it anywhere.

The figure shows the answer. Drop the four corner values, and there is one natural surface that flows through them: each corner is reproduced exactly, and as you move across the square the height glides smoothly. Look closer and two things stand out. First, the surface **agrees with the table on every corner** — that is the whole job. Second, it is **straight along each axis**: walk along one edge with the other coordinate held fixed and the height changes on a *straight line* (the midpoint of the bottom edge sits at `2`, exactly halfway between the corners `1` and `3`). The middle of the square ends up at `3.5` — the plain average of the four corners.

That "straight along each axis" property is the secret. It is what *multilinear* means, and it is what makes the surface the only sensible one. You did not pick it; the corners forced it. (No formula yet — we only named the corner values and watched the surface fill in.)

## Rigorous — earn the definition

Now make it precise. Let `f : {0,1}ⁿ → F` be a function on the Boolean hypercube — a table of `2ⁿ` field values, one per corner.

Call a polynomial **multilinear** if it has **degree at most 1 in each variable separately** (individual degree `≤ 1`). Crucially this is *not* total degree 1: a term like `x₁x₂x₃` is degree 1 in each variable, so it is allowed — the total degree can be as large as `n`. The multilinear monomials are exactly the products of *distinct* subsets of the `n` variables, so there are `2ⁿ` of them, and the multilinear polynomials form a **`2ⁿ`-dimensional** space over `F`.

The **multilinear extension (MLE)** of `f`, written `f̃`, is *the* multilinear polynomial that agrees with `f` on every corner of the cube. It exists and is given explicitly by

> **`f̃(x) = Σ_{w∈{0,1}ⁿ} f(w) · ∏ᵢ ( xᵢwᵢ + (1−xᵢ)(1−wᵢ) )`.**

Read the inner factor one coordinate at a time: `xᵢwᵢ + (1−xᵢ)(1−wᵢ)` is `xᵢ` when `wᵢ = 1` and `1−xᵢ` when `wᵢ = 0` — it is the one-variable indicator *"is `xᵢ` equal to `wᵢ`?"*. The product `χ_w(x) = ∏ᵢ(…)` is therefore **`1` at corner `w` and `0` at every other corner**. So at any corner `x = w` the sum collapses to the single term `f(w)`, and `f̃` reproduces `f` on the cube. Each `χ_w` is multilinear, so `f̃` is multilinear. (`χ_w` is the multivariate echo of the univariate Lagrange basis you already know.)

This destroys the tempting bad intuitions, explicitly:

1. **"The extension is non-unique / arbitrary" is false.** Among *all* polynomials there are infinitely many through `2ⁿ` points — but among *multilinear* ones there is exactly one. The space is `2ⁿ`-dimensional and the `2ⁿ` corner constraints form an invertible system (the `χ_w` are a basis), so `f̃` is **unique**.
2. **"Multilinear means flat / total degree 1" is false.** Our `n=3` example has individual degree `1` in each variable but **total degree `3`**, with all `8` subset-monomials present. The surface bends; it is only straight *along each axis*.
3. **"The MLE only lives on the cube" is false.** `f̃` is a polynomial defined at every point of `Fⁿ`. Over `F₉₇`, our example evaluates **off the cube** to `f̃(2, 5, 3) = 5` — a genuine value the verifier will later query at a random point.

For our concrete `n=3` table `f(000…111) = [1,4,2,8,3,5,7,6]` over `F₉₇`, the formula reproduces all eight corners and gives the off-cube value `f̃(2,5,3) = 5` (verified two independent ways: the basis sum, and `f̃` built as an explicit polynomial in `F₉₇[x₀,x₁,x₂]`).

## Post-rigorous — both halves at once

Rebuild the intuition on the rigor. The "smooth surface through the corners" picture **is** the formula `f̃ = Σ_w f(w)·χ_w`, with each `χ_w` the bump that is `1` at corner `w` and `0` elsewhere. Pair each picture with its statement:

| Picture (heuristic) | Formal statement |
|---|---|
| One smooth surface flows through the four corner values | `f̃(x) = Σ_w f(w)·χ_w(x)`, `χ_w(w)=1`, `χ_w(w')=0` for `w'≠w` |
| The surface reproduces the table on every corner | At `x=w` the sum collapses to `f(w)`; `f̃|_{cube} = f` |
| Straight along each axis, but it bends in the middle | Individual degree `≤ 1` per variable (multilinear), total degree up to `n` |
| There is only *one* such surface | Multilinear space is `2ⁿ`-dimensional; `2ⁿ` corner constraints ⇒ unique `f̃` |
| The center is the average of the corners | `f̃(½,…,½) = 2⁻ⁿ Σ_w f(w)` (here `3.5 = mean(1,4,3,6)`) |

Now the design choice is obvious: **why multilinear, not univariate?** You *could* flatten `2ⁿ` values onto a single univariate degree-`(2ⁿ−1)` interpolant — but then the verifier has one rigid high-degree object with no handle. The MLE keeps `n` variables at degree `1` each, so a verifier can **strip one variable at a time**. That is exactly the move sum-check makes in Ch 8: an `n`-variable claim becomes an `(n−1)`-variable claim, round by round, down to a single evaluation that Ch 7's random-point machinery finishes off. The MLE is *the form in which a claim about a whole table becomes a claim about a polynomial* — the object sum-check consumes, and the structure (per the live graph, community 30) that lets Lasso/Jolt evaluate a giant lookup table's MLE in `O(log N)` time without anyone committing to it.

Keep one boundary sharp: multilinear is a statement about *individual* degree, not *total* degree. Confusing the two (thinking "multilinear = flat plane") collapses the very bending that makes the object expressive.

---

> ### Rediscover it (you could have invented this)
> You have `f` on the `2ⁿ` corners of `{0,1}ⁿ` and want one polynomial that reproduces `f` on the corners and is as simple as possible.
>
> For one variable, the indicator *"`x` equals `w`"* is `x` when `w=1` and `(1−x)` when `w=0` — that is `xw+(1−x)(1−w)`. Multiply these across the `n` coordinates:
> - `χ_w(x) = ∏ᵢ(xᵢwᵢ+(1−xᵢ)(1−wᵢ))` is `1` at corner `w` and `0` at every other corner.
> - So `f̃(x) = Σ_w f(w)·χ_w(x)` reproduces `f` on the cube by construction, and is multilinear (each `χ_w` is).
>
> Why is it the *only* answer? The multilinear polynomials in `n` variables form a `2ⁿ`-dimensional space, and the `2ⁿ` corner constraints are an invertible system — so exactly one multilinear polynomial fits. **You have rediscovered the multilinear extension: the multivariate echo of Lagrange interpolation.** You derived it; you did not receive it.

---

## Check yourself (comprehension set)

**Recall.** What does it mean for a polynomial in `n` variables to be multilinear, and how many coefficients does the space of multilinear polynomials in `n` variables have?
> *Answer:* Individual degree at most `1` in each variable separately, so each monomial is a product of a distinct subset of the `n` variables — `2ⁿ` of them, a `2ⁿ`-dimensional space. This is **not** total degree `1`: terms like `x₁x₂x₃` are allowed, so total degree can reach `n`.
> *If you miss this →* revisit **multivariate polynomials; total degree vs individual (per-variable) degree**.

**Apply.** Let `f:{0,1}³→F₉₇` have cube values `f(000…111) = [1,4,2,8,3,5,7,6]`. Using `f̃(x)=Σ_w f(w)·∏ᵢ(xᵢwᵢ+(1−xᵢ)(1−wᵢ))`, what is `f̃(2,5,3)` over `F₉₇`, and does `f̃` reproduce `f` on the corners?
> *Answer:* `f̃(2,5,3) = 5` over `F₉₇`. Each basis term is `1` at corner `w` and `0` elsewhere, so on any corner the sum collapses to `f(w)` — `f̃` agrees with `f` at all eight corners. At the off-cube point `(2,5,3)` the basis terms are no longer `0/1`; the weighted sum evaluates to `5`.
> *If you miss this →* revisit **univariate Lagrange interpolation and the low-degree extension (LDE)**.

**Transfer.** A verifier holds a table of `2ⁿ` values and wants to reduce a claim about the whole table to a claim about one polynomial it can probe at a random point. Why is the MLE the right object, and why multilinear rather than a single univariate degree-`(2ⁿ−1)` interpolant?
> *Answer:* The MLE is the unique low-degree polynomial encoding the table — it agrees on the cube and is defined everywhere, so a random-point query (Schwartz–Zippel) tests the whole table at once. Multilinear is chosen because the per-variable structure lets the verifier strip **one variable per round** (sum-check, Ch 8), reducing an `n`-variable claim to an `(n−1)`-variable claim down to a single evaluation; a high-degree univariate object has no such handle. (The same structure makes Lasso/Jolt tables evaluable in `O(log N)`.)
> *If you miss this →* revisit **the Boolean hypercube `{0,1}ⁿ` as an index set**.

**Rediscover.** You have `f` only on the `2ⁿ` corners of `{0,1}ⁿ` and want one polynomial that reproduces `f` and is as simple as possible. Derive the extension and argue it is unique — what basis do you build, and why is there exactly one answer?
> *Answer:* The one-variable indicator "`x` equals `w`" is `xw+(1−x)(1−w)`; multiply across coordinates to get `χ_w(x)=∏ᵢ(xᵢwᵢ+(1−xᵢ)(1−wᵢ))`, which is `1` at `w` and `0` at every other corner. Then `f̃=Σ_w f(w)·χ_w` reproduces `f` and is multilinear. Uniqueness: the multilinear space is `2ⁿ`-dimensional and the `2ⁿ` corner constraints form an invertible system, so exactly one multilinear polynomial fits — the multilinear extension.
> *If you miss this →* revisit **the idea of a vector space over a field (a basis spans uniquely)**.

---

*Verification: all numeric claims match the Sage manifest (`n 3`, `field 97`, `cube_values [1,4,2,8,3,5,7,6]`, `agrees_on_cube true`, `offcube_mle 5` at `(2,5,3)`; picture `corner_values [1,4,3,6]`, `center 3.5`, `edge_midpoint 2.0`); the manim scene's displayed values pass `validate_scene_values` with no drift; scorecard PASS. Figure and animation generated correct-by-construction by `scripts/recipes/multilinear-extension.sage` and `scripts/scenes/multilinear-extension.py`.*
