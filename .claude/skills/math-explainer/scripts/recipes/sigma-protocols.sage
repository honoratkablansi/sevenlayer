import json, os
os.makedirs("assets/figures", exist_ok=True)

q = 1019
p = 2 * q + 1
assert is_prime(q) and is_prime(p)
F = GF(p)
g = F(9)
x = 321
h = g ** x
r = 412
c = 77
t = g ** r
s = (r + c * x) % q
left = g ** s
right = t * (h ** c)
verified = bool(left == right)

c2 = 203
s2 = (r + c2 * x) % q
left2 = g ** s2
right2 = t * (h ** c2)
verified2 = bool(left2 == right2)
extracted_x = ((s - s2) * inverse_mod((c - c2) % q, q)) % q

fig = "assets/figures/sigma-protocols.svg"
G = Graphics()
xs = [-2.4, 0, 2.4]
labels = ["commit t = g^r", "challenge c", "response s = r + c*x"]
colors = ["blue", "purple", "green"]
for i, xpos in enumerate(xs):
    G += circle((xpos, 0), 0.45, color=colors[i], thickness=2)
    G += text(labels[i], (xpos, 0), fontsize=8, color=colors[i])
G += line([(xs[0] + 0.5, 0), (xs[1] - 0.5, 0)], color="black")
G += line([(xs[1] + 0.5, 0), (xs[2] - 0.5, 0)], color="black")
G += text("verify: g^s = t * h^c", (0, -1.0), fontsize=11, color="black")
G += text("same t, two challenges -> extract x", (0, -1.35), fontsize=9, color="red")
G.axes(False)
G.save(fig, figsize=[7, 3], dpi=200)

print(json.dumps({
    "figure": fig,
    "p": int(p),
    "group_order": int(q),
    "g": int(g),
    "x": int(x),
    "h": int(h),
    "r": int(r),
    "c": int(c),
    "t": int(t),
    "s": int(s),
    "left": int(left),
    "right": int(right),
    "verified": verified,
    "c2": int(c2),
    "s2": int(s2),
    "verified2": verified2,
    "extracted_x": int(extracted_x),
    "special_soundness_ok": bool(extracted_x == x)
}))
