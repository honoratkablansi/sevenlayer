import json, os
os.makedirs("assets/figures", exist_ok=True)

# --- A concrete prime-order cyclic group: the order-q subgroup of (Z/pZ)* ---
# p is a safe prime (p = 2q+1), so the quadratic residues form a subgroup of
# prime order q. In a prime-order group EVERY non-identity element generates it,
# which is exactly what a Pedersen commitment needs (g, h both generate).
q = 1019                          # prime subgroup order
p = 2 * q + 1                     # 2039, also prime  => p is a "safe prime"
assert is_prime(q) and is_prime(p)

Fp = GF(p)

def QR(x):                        # square in F_p  => a quadratic residue => order divides q
    return Fp(x) ** 2

# Two independent generators of the order-q subgroup.
# h = g^a for a SECRET a; nobody knows log_g(h), which is what binding rests on.
g = QR(3)                         # 9  (a QR, hence order q since q is prime and g != 1)
a_secret = 571                    # the discrete log nobody is supposed to know
h = g ** a_secret                 # h is another generator of the same subgroup

assert g ** q == 1 and h ** q == 1 and g != 1 and h != 1

# --- The commitment: Com(m, r) = g^m * h^r  (mod p) ---
m = 42                            # the committed message  (0 <= m < q)
r = 800                           # the blinding randomness (0 <= r < q)

def commit(msg, rand):
    return g ** (Fp(msg).lift() % q if False else msg) * h ** rand

C = (g ** m) * (h ** r)           # the commitment value in the group

# --- HIDING (perfect): for the FIXED message m, sweeping r spreads Com(m,r) ---
# uniformly over the whole order-q subgroup. We show several r-values landing on
# distinct group elements; over all q choices of r the commitment is uniform, so
# C alone leaks nothing about m.
r_samples = [0, 1, 800, 17, 999]
hiding_orbit = [int((g ** m) * (h ** rr)) for rr in r_samples]
hiding_distinct = (len(set(hiding_orbit)) == len(hiding_orbit))

# Perfect hiding, made concrete: there exists an r' that opens the SAME C to a
# DIFFERENT message m'. Given any m', the unique r' is r + (m - m') * a^{-1} mod q,
# because g = h^{1/a}: g^m h^r = g^{m'} h^{r'}  <=>  r' = r + (m-m')*a^{-1}.
a_inv = inverse_mod(a_secret, q)
m_alt = 100
r_alt = (r + (m - m_alt) * a_inv) % q
C_alt = (g ** m_alt) * (h ** r_alt)
hiding_collision_ok = bool(C_alt == C)     # same commitment, different message

# --- BINDING (computational): a second opening (m', r') of the SAME C with
# m' != m would yield log_g(h). Concretely, from g^m h^r = g^{m'} h^{r'} one gets
# a = log_g(h) = (m - m') * (r' - r)^{-1} mod q. We DEMONSTRATE the extractor on
# the perfect-hiding alternate opening to show binding is exactly "knowing a".
dr = (r_alt - r) % q
extracted_a = ((m - m_alt) * inverse_mod(dr, q)) % q
binding_extracts_dlog = bool(extracted_a == a_secret)  # breaking binding == finding a

# --- Figure: the order-q subgroup drawn as a clock; mark g, h, and C, then show
# the hiding orbit { Com(m, r) : r in r_samples } scattered around the ring. ---
import math
fig = "assets/figures/pedersen-commitment.svg"
def angle(elt):                       # position an element by its discrete log base g
    return 2 * math.pi * (discrete_log(Fp(elt), g) / q)
ring = circle((0, 0), 1, color="lightgray", thickness=2)
def mark(elt, col, lbl, rad=1.0, sz=10):
    th = angle(elt)
    return point((rad * math.cos(th), rad * math.sin(th)), color=col, size=sz**2,
                 legend_label=lbl)
plt = ring
plt += mark(g, "green", "g")
plt += mark(h, "purple", "h")
plt += mark(C, "red", "C = g^m h^r")
for rr in r_samples:                  # the hiding orbit (same m, varying r)
    plt += point(
        [(0.82 * math.cos(angle((g ** m) * (h ** rr))),
          0.82 * math.sin(angle((g ** m) * (h ** rr))))],
        color="blue", size=40)
plt.axes(False)
plt.set_aspect_ratio(1)
plt.save(fig, dpi=200)

print(json.dumps({
    "figure": fig,
    "p": int(p),
    "group_order": int(q),
    "g": int(g),
    "h": int(h),
    "m": int(m),
    "r": int(r),
    "commitment": int(C),
    "hiding_orbit": [int(x) for x in hiding_orbit],
    "hiding_distinct": bool(hiding_distinct),
    "m_alt": int(m_alt),
    "r_alt": int(r_alt),
    "commitment_alt": int(C_alt),
    "hiding_collision_ok": bool(hiding_collision_ok),
    "extracted_dlog": int(extracted_a),
    "true_dlog": int(a_secret),
    "binding_extracts_dlog": bool(binding_extracts_dlog),
}))
