---
source_file: "references/ch14/ref-64-fips-204.pdf"
type: "paper"
community: "ML-DSA (FIPS 204)"
location: "§7.3"
tags:
  - graphify/paper
  - graphify/EXTRACTED
  - community/ML-DSA_FIPS_204
---

# ExpandA / ExpandS / ExpandMask: SHAKE-based pseudorandom sampling of matrix A from ρ, secrets s1/s2, and mask y

## Connections
- [[ML-DSA.KeyGen (Alg 16.1) expand seed ξ - seed ρ for A, seeds for s1,s2,K; t = A·s1 + s2, publish compressed t1]] - `shares_data_with` [EXTRACTED]
- [[Uses SHAKE128 and SHAKE256 (FIPS 202) as XOFs for all expansion, hashing, and challenge derivation]] - `conceptually_related_to` [EXTRACTED]

#graphify/paper #graphify/EXTRACTED #community/ML-DSA_FIPS_204