import json, os
os.makedirs("assets/figures", exist_ok=True)
F = GF(101)
R.<x> = PolynomialRing(F)
p = 3*x^2 + 5*x + 7
q = 3*x^2 + 2*x + 7              # differs from p in exactly the linear term
agree = sorted(int(a) for a in F if p(a) == q(a))
fig = "assets/figures/schwartz_zippel.svg"
plt = point([(int(a), int(p(a))) for a in F], color="blue", size=18, legend_label="p")
plt += point([(int(a), int(q(a))) for a in F], color="red", size=18, legend_label="q")
plt.save(fig, dpi=200)
print(json.dumps({"figure": fig, "field": 101,
                  "agreement_points": agree, "num_agreements": len(agree)}))
