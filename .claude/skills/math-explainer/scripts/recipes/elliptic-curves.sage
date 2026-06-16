import json, os
os.makedirs("assets/figures", exist_ok=True)

p = 97
F = GF(p)
E = EllipticCurve(F, [2, 3])
P = E(3, 6)
Q = E(80, 10)
R = P + Q
a = 7
aP = a * P
acc = E(0)
for _ in range(a):
    acc += P
assert acc == aP

def coords(T):
    if T == E(0):
        return "O"
    return [int(T[0]), int(T[1])]

lam = (F(Q[1]) - F(P[1])) / (F(Q[0]) - F(P[0]))
points = []
for xx in range(p):
    rhs = F(xx) ** 3 + F(2) * F(xx) + F(3)
    for yy in range(p):
        if F(yy) ** 2 == rhs:
            points.append([int(xx), int(yy)])

fig = "assets/figures/elliptic-curves.svg"
G = Graphics()
for xx, yy in points:
    G += point((xx / 10.0, yy / 10.0), color="lightgray", size=12)
for T, col, label in [(P, "blue", "P"), (Q, "green", "Q"), (R, "red", "P+Q"), (aP, "purple", "7P")]:
    x0, y0 = coords(T)
    G += point((x0 / 10.0, y0 / 10.0), color=col, size=55)
    G += text(label, (x0 / 10.0, y0 / 10.0 + 0.45), fontsize=8, color=col)
G += text("E: y^2 = x^3 + 2x + 3 over F_97", (4.8, -0.8), fontsize=10, color="black")
G += text("finite points form a group", (4.8, -1.25), fontsize=10, color="black")
G.axes(False)
G.set_aspect_ratio(1)
G.save(fig, figsize=[6, 6], dpi=200)

print(json.dumps({
    "figure": fig,
    "field": int(p),
    "curve_a": int(2),
    "curve_b": int(3),
    "group_order": int(E.order()),
    "P": coords(P),
    "Q": coords(Q),
    "addition_slope": int(lam),
    "P_plus_Q": coords(R),
    "scalar": int(a),
    "scalar_multiple": coords(aP),
    "repeated_addition": coords(acc),
    "repeated_addition_matches": bool(acc == aP),
    "finite_point_count_without_infinity": int(len(points))
}))
