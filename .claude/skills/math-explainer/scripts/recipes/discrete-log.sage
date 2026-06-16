import json, os, math
os.makedirs("assets/figures", exist_ok=True)

q = 1019
p = 2 * q + 1
assert is_prime(q) and is_prime(p)
F = GF(p)
g = F(9)
assert g != 1 and g ** q == 1
x = 873
h = g ** x

bits = bin(x)[2:]
forward_chain_multiplications = (len(bits) - 1) + bits[1:].count("1")

brute_force_steps = None
for k in range(q):
    if g ** k == h:
        brute_force_steps = k + 1
        break
assert brute_force_steps == x + 1

first_powers = [{"exponent": int(k), "value": int(g ** k)} for k in range(12)]

fig = "assets/figures/discrete-log.svg"
G = Graphics()
G += circle((0, 0), 1, color="lightgray", thickness=2)
for item in first_powers:
    theta = 2 * math.pi * item["exponent"] / q
    G += point((math.cos(theta), math.sin(theta)), color="blue", size=35)
G += text("walk: g^0, g^1, g^2, ...", (0, 1.25), fontsize=10, color="blue")
theta_h = 2 * math.pi * x / q
G += point((math.cos(theta_h), math.sin(theta_h)), color="red", size=70)
G += text("target h = g^x", (0, -1.25), fontsize=10, color="red")
G += text("forward: short multiplication chain", (0, -1.55), fontsize=9, color="black")
G += text("backward: search the clock", (0, -1.8), fontsize=9, color="black")
G.axes(False)
G.set_aspect_ratio(1)
G.save(fig, figsize=[5, 5], dpi=200)

print(json.dumps({
    "figure": fig,
    "p": int(p),
    "group_order": int(q),
    "g": int(g),
    "x": int(x),
    "h": int(h),
    "forward_chain_multiplications": int(forward_chain_multiplications),
    "brute_force_steps": int(brute_force_steps),
    "worst_case_steps": int(q),
    "first_powers": first_powers
}))
