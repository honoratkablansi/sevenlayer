import json, os
os.makedirs("assets/figures", exist_ok=True)
F = GF(17)
R.<x> = PolynomialRing(F)
points = [(int(1), int(4)), (int(2), int(1)), (int(4), int(16))]
p = R.lagrange_polynomial([(F(a), F(b)) for a, b in points])
domain = list(range(17))
values = [int(p(F(a))) for a in domain]
fig = "assets/figures/lagrange-interpolation.svg"
g = list_plot([(a, values[a]) for a in domain], color="gray", size=25, legend_label="interpolating polynomial")
g += point(points, color="red", size=70, legend_label="pinned values")
g += text("three values pin one degree <= 2 polynomial over F_17", (8, 18), fontsize=10, color="black")
g.save(fig, figsize=[6, 4], dpi=200)
print(json.dumps({
    "figure": fig,
    "field": int(17),
    "point_count": int(len(points)),
    "degree_bound": int(2),
    "points": points,
    "polynomial_coefficients": [int(c) for c in p.list()],
    "value_at_7": int(p(F(7)))
}))
