import json, os
os.makedirs("assets/figures", exist_ok=True)
F = GF(101)
A = matrix(F, [[1, 2], [3, 4]])
B = matrix(F, [[2, 0], [1, 5]])
C_true = A * B
C_claim = matrix(F, [[5, 10], [10, 20]])
r = vector(F, [7, 11])
left = A * (B * r)
right = C_claim * r
error = C_claim - C_true
catches = bool(left != right)
fig = "assets/figures/freivalds.svg"
g = Graphics()
g += text("Check AB = C by testing A(Br) against Cr", (0, 1.2), fontsize=11, color="black")
g += text("A(Br) = " + str([int(v) for v in left]), (-1.2, 0.2), fontsize=10, color="blue")
g += text("Cr = " + str([int(v) for v in right]), (1.2, 0.2), fontsize=10, color="red")
g += text("different vectors expose the bad entry", (0, -0.8), fontsize=10, color="black")
g.save(fig, figsize=[6, 3], dpi=200)
print(json.dumps({
    "figure": fig,
    "field": int(101),
    "matrix_size": int(2),
    "A": [[int(v) for v in row] for row in A.rows()],
    "B": [[int(v) for v in row] for row in B.rows()],
    "true_C": [[int(v) for v in row] for row in C_true.rows()],
    "claimed_C": [[int(v) for v in row] for row in C_claim.rows()],
    "sample_r": [int(v) for v in r],
    "left_vector": [int(v) for v in left],
    "right_vector": [int(v) for v in right],
    "catches_error": catches,
    "failure_bound_num": int(1),
    "failure_bound_den": int(101)
}))
