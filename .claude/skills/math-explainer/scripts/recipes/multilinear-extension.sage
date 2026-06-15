import json, os
from itertools import product
os.makedirs("assets/figures", exist_ok=True)

# ---------------------------------------------------------------------------
# Multilinear extension (MLE): the UNIQUE multilinear polynomial that agrees
# with a function f:{0,1}^n -> F on every corner of the Boolean hypercube.
#
#   MLE(x) = sum_{w in {0,1}^n} f(w) * prod_i ( x_i w_i + (1-x_i)(1-w_i) )
#
# The product is the multilinear Lagrange basis chi_w(x): it equals 1 when x=w
# and 0 at every other cube corner, so the sum reproduces f on the cube and
# interpolates multilinearly (degree 1 in each variable) everywhere else.
# ---------------------------------------------------------------------------

# --- Numeric manifest: n = 3 over the small prime field GF(97) ---------------
F = GF(97)
n = 3

# A chosen f:{0,1}^3 -> F (the 2^n = 8 cube values), no trivial symmetry.
fvals = {
    (0, 0, 0): 1, (0, 0, 1): 4, (0, 1, 0): 2, (0, 1, 1): 8,
    (1, 0, 0): 3, (1, 0, 1): 5, (1, 1, 0): 7, (1, 1, 1): 6,
}
corners = list(product([0, 1], repeat=n))


def chi(w, x):
    """Multilinear Lagrange basis chi_w(x) = prod_i (x_i w_i + (1-x_i)(1-w_i))."""
    pr = F(1)
    for xi, wi in zip(x, w):
        pr *= (F(xi) * F(wi) + (F(1) - F(xi)) * (F(1) - F(wi)))
    return pr


def mle(x):
    return sum(F(fvals[w]) * chi(w, x) for w in corners)


# Correctness: the MLE must agree with f on EVERY cube corner.
agrees_on_cube = all(mle(w) == F(fvals[w]) for w in corners)
assert agrees_on_cube, "MLE failed to agree with f on the Boolean cube"

# An OFF-cube evaluation (a point not in {0,1}^3), via the formula above.
offcube_x = (2, 5, 3)
offcube_val = int(mle((F(2), F(5), F(3))))

cube_values = [int(fvals[w]) for w in corners]   # in the corners() order

# --- Figure: the n = 2 bilinear surface over the reals (heatmap) ------------
# Same interpolation idea, restricted to 2 variables so it can be drawn: the
# unit square's 4 corner values are extended to a smooth bilinear surface that
# (a) reproduces the corners and (b) is linear along each axis.
g = {(0, 0): 1, (0, 1): 4, (1, 0): 3, (1, 1): 6}  # corner values for the picture


def bil(a, b):
    return ((1 - a) * (1 - b) * g[(0, 0)] + (1 - a) * b * g[(0, 1)]
            + a * (1 - b) * g[(1, 0)] + a * b * g[(1, 1)])


fig = "assets/figures/multilinear-extension.svg"
heat = density_plot(lambda a, b: bil(a, b), (0, 1), (0, 1),
                    cmap="viridis", plot_points=120,
                    axes_labels=["x1", "x2"])
# Mark and label the four cube corners with their integer values.
labels = Graphics()
for (a, b), v in g.items():
    labels += point((a, b), color="white", size=55, zorder=5)
    labels += text(str(v), (a + (0.06 if a == 0 else -0.06),
                            b + (0.06 if b == 0 else -0.06)),
                   color="white", fontsize=16, zorder=6)
# Center point: bilinear value = average of the 4 corners = 3.5.
labels += point((0.5, 0.5), color="red", size=45, zorder=5)
labels += text("3.5", (0.5, 0.56), color="red", fontsize=14, zorder=6)
art = heat + labels
art.set_axes_range(0, 1, 0, 1)
art.save(fig, dpi=200, title="Bilinear (multilinear, n=2) extension of 4 corner values")

# Center and an edge-midpoint of the picture surface (for the manim cross-check).
bil_center = float(bil(0.5, 0.5))         # 3.5  == mean(1,4,3,6)
bil_edge_x = float(bil(0.5, 0.0))         # 2.0  == mean(g00=1, g10=3)

manifest = {
    "figure": fig,
    "n": int(n),
    "field": int(97),
    "cube_corners": [[int(c) for c in w] for w in corners],
    "cube_values": cube_values,
    "agrees_on_cube": bool(agrees_on_cube),
    "offcube_point": [int(c) for c in offcube_x],
    "offcube_mle": offcube_val,
    "picture_n": int(2),
    "picture_corner_values": [int(g[(0, 0)]), int(g[(0, 1)]),
                              int(g[(1, 0)]), int(g[(1, 1)])],
    "picture_center": bil_center,
    "picture_edge_midpoint": bil_edge_x,
}
print(json.dumps(manifest))
