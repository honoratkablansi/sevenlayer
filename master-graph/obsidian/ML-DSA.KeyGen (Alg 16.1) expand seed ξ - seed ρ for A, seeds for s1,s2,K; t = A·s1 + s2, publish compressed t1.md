---
source_file: "references/ch14/ref-64-fips-204.pdf"
type: "paper"
community: "Community 59"
location: "§5.1 / §6.1"
tags:
  - graphify/paper
  - graphify/EXTRACTED
  - community/Community_59
---

# ML-DSA.KeyGen (Alg 1/6.1): expand seed ξ -> seed ρ for A, seeds for s1,s2,K; t = A·s1 + s2, publish compressed t1

## Connections
- [[ExpandA  ExpandS  ExpandMask SHAKE-based pseudorandom sampling of matrix A from ρ, secrets s1s2, and mask y]] - `shares_data_with` [EXTRACTED]
- [[ML-DSA (Module-Lattice Digital Signature Algorithm)]] - `defines` [EXTRACTED]
- [[Module Learning With Errors (MLWE)]] - `assumes` [INFERRED]
- [[Power2Round  Decompose  HighBits  LowBits drop d=13 low-order bits of t and round w to multiples of α=2γ2]] - `shares_data_with` [EXTRACTED]

#graphify/paper #graphify/EXTRACTED #community/Community_59