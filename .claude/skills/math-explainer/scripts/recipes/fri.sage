import json, os
os.makedirs("assets/figures", exist_ok=True)

p = 97
F = GF(p)
R.<X> = PolynomialRing(F)
f = F(7) + F(11)*X + F(5)*X**2 + F(3)*X**3
beta = F(29)
omega = F(64)
assert omega ** 8 == 1 and omega ** 4 == -1
domain = [omega ** i for i in range(8)]
half_domain = [omega ** (2*i) for i in range(4)]
codeword = [f(x) for x in domain]

S.<Y> = PolynomialRing(F)
f_even = F(7) + F(5)*Y
f_odd = F(11) + F(3)*Y
folded = f_even + beta * f_odd
folded_codeword = [folded(y) for y in half_domain]

consistency = []
for i in range(4):
    x = domain[i]
    y = x ** 2
    fx = f(x)
    fneg = f(-x)
    even_val = (fx + fneg) / F(2)
    odd_val = (fx - fneg) / (F(2) * x)
    folded_from_pair = even_val + beta * odd_val
    consistency.append(bool(folded_from_pair == folded(y)))

fig = "assets/figures/fri.svg"
G = Graphics()
for i, val in enumerate(codeword):
    G += point((-3.0 + i * 0.55, 0.8), color="blue", size=35)
for i, val in enumerate(folded_codeword):
    G += point((-1.2 + i * 0.8, -0.75), color="green", size=45)
for i in range(4):
    G += line([(-3.0 + i * 0.55, 0.65), (-1.2 + i * 0.8, -0.55)], color="gray")
    G += line([(-3.0 + (i + 4) * 0.55, 0.65), (-1.2 + i * 0.8, -0.55)], color="gray")
G += text("8 evaluations of degree 3 polynomial", (0, 1.35), fontsize=10, color="blue")
G += text("fold with beta = 29", (0, 0.0), fontsize=11, color="black")
G += text("4 evaluations of degree 1 polynomial", (0, -1.25), fontsize=10, color="green")
G.axes(False)
G.save(fig, figsize=[7, 4], dpi=200)

print(json.dumps({
    "figure": fig,
    "field": int(p),
    "omega": int(omega),
    "domain_size": int(len(domain)),
    "folded_domain_size": int(len(half_domain)),
    "degree_before": int(f.degree()),
    "degree_bound_before": int(4),
    "degree_after": int(folded.degree()),
    "degree_bound_after": int(2),
    "beta": int(beta),
    "polynomial_coefficients": [int(7), int(11), int(5), int(3)],
    "folded_coefficients": [int(c) for c in folded.list()],
    "codeword": [int(v) for v in codeword],
    "folded_codeword": [int(v) for v in folded_codeword],
    "consistency_checks": consistency,
    "consistency_check": bool(all(consistency))
}))
