---
source_file: "references/ch14/ref-64-fips-204.pdf"
type: "paper"
community: "Community 45"
location: "§5.2 / §6.2"
tags:
  - graphify/paper
  - graphify/EXTRACTED
  - community/Community_45
---

# ML-DSA.Sign (Alg 2/6.2): commit w=Ay, challenge c~ from H(w1||μ), response z = y + c·s1, with rejection-sampling abort loop

## Connections
- [[Fiat-Shamir With Aborts construction (Schnorr-like signature with rejection sampling on the response)]] - `conceptually_related_to` [EXTRACTED]
- [[Hedged (default, fresh + precomputed randomness) vs deterministic signing variant; same Verify works for both]] - `conceptually_related_to` [EXTRACTED]
- [[Hint vector h ∈ R2k (MakeHintUseHint) lets verifier reconstruct high bits w1 despite t1 compression]] - `shares_data_with` [EXTRACTED]
- [[ML-DSA (Module-Lattice Digital Signature Algorithm)]] - `defines` [EXTRACTED]
- [[Message representative μ = H(H(pk)  M); signing μ not M provides BUFF  beyond-unforgeability properties]] - `shares_data_with` [EXTRACTED]
- [[NTT over R_q (q=8380417, ζ=1753 a 512th root of unity) fast module-polynomial multiplication NTT(ab)=NTT(a)∘NTT(b)]] - `shares_data_with` [EXTRACTED]
- [[Rejection sampling abort and restart with new mask y if z (or r0) coefficients fall outside bound, removing bias toward secret s1s2]] - `introduces` [EXTRACTED]
- [[SampleInBall (Alg 29) challenge polynomial c with exactly τ nonzero ±1 coefficients, derived from c~]] - `shares_data_with` [EXTRACTED]

#graphify/paper #graphify/EXTRACTED #community/Community_45