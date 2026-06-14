---
source_file: "references/ch14/ref-64-fips-204.pdf"
type: "paper"
community: "Community 59"
location: "§7.4"
tags:
  - graphify/paper
  - graphify/EXTRACTED
  - community/Community_59
---

# Hint vector h ∈ R2^k (MakeHint/UseHint) lets verifier reconstruct high bits w1 despite t1 compression

## Connections
- [[ML-DSA.Sign (Alg 26.2) commit w=Ay, challenge c~ from H(w1μ), response z = y + c·s1, with rejection-sampling abort loop]] - `shares_data_with` [EXTRACTED]
- [[ML-DSA.Verify (Alg 36.3) recompute w1' via UseHint from z, t1, c; accept iff z is short and c~ matches H(w1'μ)]] - `shares_data_with` [EXTRACTED]
- [[Power2Round  Decompose  HighBits  LowBits drop d=13 low-order bits of t and round w to multiples of α=2γ2]] - `conceptually_related_to` [EXTRACTED]

#graphify/paper #graphify/EXTRACTED #community/Community_59