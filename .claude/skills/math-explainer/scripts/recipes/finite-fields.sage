import json, math, os
os.makedirs("assets/figures", exist_ok=True)
F = GF(17)
modulus = int(17)
add_a, add_b = int(14), int(5)
add_result = int(F(add_a) + F(add_b))
mul_a, mul_b = int(5), int(7)
mul_result = int(F(mul_a) * F(mul_b))
inverse_of = int(5)
inverse_value = int(F(inverse_of)^(-1))
fig = "assets/figures/finite-fields.svg"
g = Graphics()
coords = []
for k in range(modulus):
    theta = 2 * math.pi * k / modulus
    coords.append((math.cos(theta), math.sin(theta)))
g += circle((0, 0), 1, color="gray", thickness=1)
for k, (cx, cy) in enumerate(coords):
    color = "red" if k in [add_a, add_result] else ("blue" if k == add_b else "black")
    size = 45 if k in [add_a, add_b, add_result] else 18
    g += point((cx, cy), color=color, size=size)
    if k in [0, 1, 2, 5, 7, 14, 16]:
        g += text(str(k), (1.16 * cx, 1.16 * cy), fontsize=8, color=color)
g += arrow(coords[add_a], coords[add_result], color="red", width=1)
g += text("14 + 5 wraps to 2 in F_17", (0, -1.45), fontsize=10, color="red")
g += text("5 * 7 = 1, so 7 is inverse of 5", (0, -1.65), fontsize=10, color="blue")
g.save(fig, figsize=[5, 5], dpi=200)
print(json.dumps({
    "figure": fig,
    "field": modulus,
    "modulus": modulus,
    "add_a": add_a,
    "add_b": add_b,
    "add_result": add_result,
    "mul_a": mul_a,
    "mul_b": mul_b,
    "mul_result": mul_result,
    "inverse_of": inverse_of,
    "inverse_value": inverse_value
}))
