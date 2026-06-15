import json, os
os.makedirs("assets/figures", exist_ok=True)

# --- A small, reproducible, pairing-friendly elliptic curve ----------------------
# E: y^2 = x^3 - x  is supersingular over GF(23). It carries an r=3 torsion subgroup,
# and its embedding degree for r=3 is k=2 (3 | 23^2 - 1 = 528 but 3 does NOT divide
# 23 - 1 = 22), so the FULL 3-torsion E[3] ~ Z/3 x Z/3 lives in GF(23^2). That is the
# smallest field where the Weil pairing e: E[r] x E[r] -> mu_r (the cube roots of unity
# in GF(23^2)*) is defined and non-degenerate. Everything below is fixed by a seed so
# the manifest is reproducible.
set_random_seed(11)
q = 23                              # base prime
r = 3                              # prime order of the source groups G1, G2
k = 2                              # embedding degree: target group lives in GF(q^k)

Fx = GF(q^k, name="t")            # GF(23^2), where E[r] and mu_r live
E  = EllipticCurve(Fx, [0, 0, 0, -1, 0])   # y^2 = x^3 - x
N  = E.order()                     # 576 = 3^2 * 64
cof = N // (r * r)                 # cofactor mapping a random point into E[r]

def torsion_point():
    """Return a random point of exact order r (a generator of a line in E[r])."""
    for _ in range(5000):
        R = cof * E.random_point()
        if (not R.is_zero()) and R.order() == r:
            return R
    raise RuntimeError("no r-torsion point found")

# P generates G1; Q generates an INDEPENDENT line G2 (e(P,Q) != 1 certifies independence,
# i.e. the pairing is non-degenerate on this pair).
P = torsion_point()
Q = None
for _ in range(5000):
    cand = torsion_point()
    if P.weil_pairing(cand, r) != 1:
        Q = cand
        break
if Q is None:
    raise RuntimeError("no independent second generator found")

# Concrete scalars. a*b = 8, and 8 mod r = 2, so e(P,Q)^(ab) is a NON-trivial power
# of the pairing value (not the trivial 1) -- a genuine illustration of bilinearity.
a, b = 2, 4

e_PQ    = P.weil_pairing(Q, r)                 # e(P, Q) in mu_r <= GF(23^2)*
e_aPbQ  = (a * P).weil_pairing(b * Q, r)       # e(aP, bQ)
e_pow   = e_PQ ** (a * b)                       # e(P, Q)^(a*b)
bilinear_holds = bool(e_aPbQ == e_pow)          # the bilinearity identity

# --- Figure: the pairing as an arrow from two source points to a target element -----
# manim handles the animated version; the Sage figure is a static schematic of the same
# map e: G1 x G2 -> G_T, with the three concrete values printed beside their groups.
fig = "assets/figures/bilinear_pairings.svg"
g1 = circle((-3, 1.4), 1.05, edgecolor="blue",  thickness=2)
g2 = circle((-3, -1.4), 1.05, edgecolor="red",   thickness=2)
gt = circle(( 3, 0.0), 1.25, edgecolor="purple", thickness=2)
g1 += text("G1", (-3, 2.75), color="blue",  fontsize=14)
g2 += text("G2", (-3, -2.75), color="red",   fontsize=14)
gt += text("G_T", (3, 1.55), color="purple", fontsize=14)
g1 += point([(-3, 1.4)], color="blue", size=45)
g2 += point([(-3, -1.4)], color="red",  size=45)
gt += point([(3, 0.0)], color="purple", size=45)
g1 += text("P", (-2.55, 1.7), color="blue",  fontsize=12)
g2 += text("Q", (-2.55, -1.1), color="red",  fontsize=12)
gt += text("e(P,Q)", (3.0, -0.45), color="purple", fontsize=11)
arrows  = arrow((-2.0, 1.2), (1.7, 0.25), color="gray", width=1)
arrows += arrow((-2.0, -1.2), (1.7, -0.25), color="gray", width=1)
arrows += text("e :  G1 x G2  ->  G_T", (0, 2.6), color="black", fontsize=13)
arrows += text("e(aP, bQ) = e(P, Q)^(ab)", (0, -2.8), color="black", fontsize=13)
plt = g1 + g2 + gt + arrows
plt.axes(False)
plt.save(fig, figsize=[8, 5])

manifest = {
    "figure": fig,
    "q": int(q),
    "r": int(r),
    "k": int(k),
    "a": int(a),
    "b": int(b),
    "ab": int(a * b),
    "ab_mod_r": int((a * b) % r),
    "P": str(P[0]) + ", " + str(P[1]),
    "Q": str(Q[0]) + ", " + str(Q[1]),
    "e_PQ": str(e_PQ),
    "e_aPbQ": str(e_aPbQ),
    "e_PQ_pow_ab": str(e_pow),
    "bilinear_holds": bilinear_holds,
}
print(json.dumps(manifest))
