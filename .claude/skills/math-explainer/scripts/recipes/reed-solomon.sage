import json, os
os.makedirs("assets/figures", exist_ok=True)
F = GF(17)
R.<x> = PolynomialRing(F)
p = 3 + 5*x + 2*x^2
q = 3 + 6*x + 2*x^2
domain = list(range(8))
codeword = [int(p(F(a))) for a in domain]
other_codeword = [int(q(F(a))) for a in domain]
agree = [int(a) for a in domain if p(F(a)) == q(F(a))]
distance = int(sum(1 for a in domain if p(F(a)) != q(F(a))))
fig = "assets/figures/reed-solomon.svg"
bars = [(a, codeword[i]) for i, a in enumerate(domain)]
g = bar_chart(codeword, width=0.5, color="blue")
g += point([(i + 0.5, other_codeword[i]) for i in range(len(domain))], color="red", size=50)
g += text("message [3,5,2] becomes 8 field evaluations", (3.7, 18), fontsize=10, color="black")
g += text("one changed coefficient disagrees at 7 of 8 positions", (3.7, 16.5), fontsize=10, color="red")
g.save(fig, figsize=[6, 4], dpi=200)
print(json.dumps({
    "figure": fig,
    "field": int(17),
    "message_degree_bound": int(2),
    "dimension": int(3),
    "code_length": int(8),
    "designed_min_distance": int(6),
    "message": [int(3), int(5), int(2)],
    "codeword": codeword,
    "other_message": [int(3), int(6), int(2)],
    "agreement_positions": agree,
    "realized_distance": distance
}))
