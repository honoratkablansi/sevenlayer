import json, os
os.makedirs("assets/figures", exist_ok=True)
F = GF(17)
z = vector(F, [1, 3, 4, 12, 15])  # [1, x, y, t, out]
A = matrix(F, [[0, 1, 0, 0, 0], [0, 1, 0, 1, 0]])
B = matrix(F, [[0, 0, 1, 0, 0], [1, 0, 0, 0, 0]])
C = matrix(F, [[0, 0, 0, 1, 0], [0, 0, 0, 0, 1]])
Az, Bz, Cz = A*z, B*z, C*z
products = vector(F, [Az[i] * Bz[i] for i in range(2)])
satisfied = bool(products == Cz)
fig = "assets/figures/r1cs.svg"
g = Graphics()
g += text("R1CS checks two rank-1 equations over F_17", (0, 1.2), fontsize=11, color="black")
g += text("row 1: x * y = t  ->  3 * 4 = 12", (0, 0.35), fontsize=10, color="blue")
g += text("row 2: (t + x) * 1 = out  ->  15 * 1 = 15", (0, -0.25), fontsize=10, color="green")
g += text("Az o Bz = Cz", (0, -1.0), fontsize=10, color="black")
g.save(fig, figsize=[6, 3], dpi=200)
print(json.dumps({
    "figure": fig,
    "field": int(17),
    "num_variables": int(5),
    "num_constraints": int(2),
    "witness": [int(v) for v in z],
    "Az": [int(v) for v in Az],
    "Bz": [int(v) for v in Bz],
    "Cz": [int(v) for v in Cz],
    "products": [int(v) for v in products],
    "satisfied": satisfied
}))
