"""Sage recipe for the Sum-Check protocol (Chapter 8).

Correct-by-construction. Takes a small multivariate polynomial g(x1,x2,x3) over
GF(97), forms the claimed sum H = sum_{x in {0,1}^3} g(x), then runs the sum-check
rounds with FIXED (reproducible, non-random) challenges r1, r2, r3. Each round i emits
the univariate polynomial g_i(X) obtained by fixing the earlier variables to the chosen
challenges r_1..r_{i-1} and summing the later variables over {0,1}.

Verifies the sum-check identities exactly:
  round 1:  g_1(0) + g_1(1) == H
  round i:  g_i(0) + g_i(1) == g_{i-1}(r_{i-1})   for i = 2, 3
and the final fold  g_3(r_3) == g(r_1, r_2, r_3).

Emits a one-line JSON manifest with a `figure` (an .svg under assets/figures/) plus the
claimed sum H, each round's univariate coefficients, the fixed challenges, and the
running claims. All Sage Integer values are wrapped in int(...) so the JSON is plain.
"""
import json, os
os.makedirs("assets/figures", exist_ok=True)

P = 97
F = GF(P)
R3 = PolynomialRing(F, 3, names=("x1", "x2", "x3"))
x1, x2, x3 = R3.gens()

# A small multivariate polynomial. Per-variable degrees: deg_{x1}=2, deg_{x2}=1, deg_{x3}=1.
# This makes the round-1 univariate quadratic (degree 2) and rounds 2,3 linear (degree 1),
# so the protocol is genuinely non-multilinear in x1 and the per-round degree bound matters.
g = 2 * x1**2 * x2 + 3 * x2 * x3 + x1 + 5

# --- The claimed sum over the Boolean hypercube {0,1}^3 ---
H = F(0)
for a1 in (0, 1):
    for a2 in (0, 1):
        for a3 in (0, 1):
            H += g(a1, a2, a3)

# Fixed, reproducible challenges (NO randomness): the verifier's "random" points, pinned.
r = {1: F(2), 2: F(3), 3: F(4)}

# Univariate ring for the round polynomials g_i(X).
Ru = PolynomialRing(F, "X")
X = Ru.gen()


def round_poly(i):
    """g_i(X): fix x_1..x_{i-1} to r_1..r_{i-1}, set x_i = X, sum x_{i+1}..x_3 over {0,1}."""
    acc = Ru(0)
    later = list(range(i + 1, 4))  # variables summed over the cube this round
    for bits in range(2 ** len(later)):
        # assemble the substitution point for g
        vals = []
        for v in (1, 2, 3):
            if v < i:
                vals.append(r[v])          # fixed earlier challenge
            elif v == i:
                vals.append(X)             # the free univariate variable
            else:
                # one of the later (summed) variables: read its bit
                pos = later.index(v)
                vals.append(F((bits >> pos) & 1))
        acc += g(vals[0], vals[1], vals[2])
    return Ru(acc)

g1 = round_poly(1)
g2 = round_poly(2)
g3 = round_poly(3)

# --- Sum-check identities (exact, over GF(97)) ---
assert g1(0) + g1(1) == H,            "round 1: g1(0)+g1(1) != H"
assert g2(0) + g2(1) == g1(r[1]),     "round 2: g2(0)+g2(1) != g1(r1)"
assert g3(0) + g3(1) == g2(r[2]),     "round 3: g3(0)+g3(1) != g2(r2)"
# Final fold: the last univariate at its challenge equals g at the full random point.
assert g3(r[3]) == g(r[1], r[2], r[3]), "final: g3(r3) != g(r1,r2,r3)"


def coeffs(poly):
    """Ascending-order coefficient list [c0, c1, ...] as plain ints."""
    return [int(c) for c in poly.list()]


# --- Figure: the round-by-round collapse of the hypercube claim ---
# Plot the running claim value at each round as the sum-check ladder narrows
# 8 hypercube terms -> one evaluation. Round 0 = H; round i = g_i(r_i).
ladder = [
    (0, int(H)),
    (1, int(g1(r[1]))),
    (2, int(g2(r[2]))),
    (3, int(g3(r[3]))),
]
fig = "assets/figures/sum_check.svg"
plt = line([(k, v) for k, v in ladder], color="purple", thickness=2,
           legend_label="running claim")
plt += points([(k, v) for k, v in ladder], color="purple", size=40)
# annotate how many hypercube terms remain folded into the claim at each step
remaining = {0: 8, 1: 4, 2: 2, 3: 1}
for k, v in ladder:
    plt += text("%d terms" % remaining[k], (k, v + 3), color="gray", fontsize=10)
plt.axes_labels(["round (variables fixed)", "claim value in GF(97)"])
plt.save(fig, dpi=200)

manifest = {
    "figure": fig,
    "field": int(P),
    "num_vars": int(3),
    "polynomial": "2*x1^2*x2 + 3*x2*x3 + x1 + 5",
    "H": int(H),
    "challenges": {"r1": int(r[1]), "r2": int(r[2]), "r3": int(r[3])},
    "rounds": [
        {"i": int(1), "coeffs": coeffs(g1), "g_at_0": int(g1(0)), "g_at_1": int(g1(1)),
         "sum_0_1": int(g1(0) + g1(1)), "expected_claim": int(H),
         "g_at_r": int(g1(r[1]))},
        {"i": int(2), "coeffs": coeffs(g2), "g_at_0": int(g2(0)), "g_at_1": int(g2(1)),
         "sum_0_1": int(g2(0) + g2(1)), "expected_claim": int(g1(r[1])),
         "g_at_r": int(g2(r[2]))},
        {"i": int(3), "coeffs": coeffs(g3), "g_at_0": int(g3(0)), "g_at_1": int(g3(1)),
         "sum_0_1": int(g3(0) + g3(1)), "expected_claim": int(g2(r[2])),
         "g_at_r": int(g3(r[3]))},
    ],
    "final_eval": int(g(r[1], r[2], r[3])),
    "degree_bound_per_round": int(2),
    "soundness_bound": "d*v/|F| = 2*3/97 = 6/97",
    "identities_hold": True,
}
print(json.dumps(manifest))
