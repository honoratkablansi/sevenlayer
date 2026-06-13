---
type: community
cohesion: 0.13
members: 22
---

# ML-DSA (FIPS 204)

**Cohesion:** 0.13 - loosely connected
**Members:** 22 nodes

## Members
- [[ExpandA  ExpandS  ExpandMask SHAKE-based pseudorandom sampling of matrix A from ρ, secrets s1s2, and mask y]] - paper - references/ch14/ref-64-fips-204.pdf
- [[FIPS 204 Module-Lattice-Based Digital Signature Standard]] - paper - references/ch14/ref-64-fips-204.pdf
- [[FIPS 204 Module-Lattice-Based Digital Signature Standard (ML-DSA), published 2024-08-13]] - paper - references/ch14/ref-64-fips-204.pdf
- [[Fiat-Shamir With Aborts construction (Schnorr-like signature with rejection sampling on the response)]] - paper - references/ch14/ref-64-fips-204.pdf
- [[HashML-DSA domain-separated pre-hash variant signing PH(M) for largestreamed messages]] - paper - references/ch14/ref-64-fips-204.pdf
- [[Hedged (default, fresh + precomputed randomness) vs deterministic signing variant; same Verify works for both]] - paper - references/ch14/ref-64-fips-204.pdf
- [[Hint vector h ∈ R2k (MakeHintUseHint) lets verifier reconstruct high bits w1 despite t1 compression]] - paper - references/ch14/ref-64-fips-204.pdf
- [[ML-DSA (Module-Lattice Digital Signature Algorithm)]] - document - references/ch14/ref-64-fips-204.pdf
- [[ML-DSA derived from CRYSTALS-DILITHIUM v3.1 (Round-3 PQC selection); differences in Appendix D]] - paper - references/ch14/ref-64-fips-204.pdf
- [[ML-DSA-44 parameter set (k,ℓ)=(4,4), η=2, τ=39, λ=128, Category 2; pk 1312 B, sk 2560 B, sig 2420 B]] - paper - references/ch14/ref-64-fips-204.pdf
- [[ML-DSA-65 parameter set (k,ℓ)=(6,5), η=4, τ=49, λ=192, Category 3; pk 1952 B, sk 4032 B, sig 3309 B]] - paper - references/ch14/ref-64-fips-204.pdf
- [[ML-DSA-87 parameter set (k,ℓ)=(8,7), η=2, τ=60, λ=256, Category 5; pk 2592 B, sk 4896 B, sig 4627 B]] - paper - references/ch14/ref-64-fips-204.pdf
- [[ML-DSA.KeyGen (Alg 16.1) expand seed ξ - seed ρ for A, seeds for s1,s2,K; t = A·s1 + s2, publish compressed t1]] - paper - references/ch14/ref-64-fips-204.pdf
- [[ML-DSA.Sign (Alg 26.2) commit w=Ay, challenge c~ from H(w1μ), response z = y + c·s1, with rejection-sampling abort loop]] - paper - references/ch14/ref-64-fips-204.pdf
- [[ML-DSA.Verify (Alg 36.3) recompute w1' via UseHint from z, t1, c; accept iff z is short and c~ matches H(w1'μ)]] - paper - references/ch14/ref-64-fips-204.pdf
- [[Message representative μ = H(H(pk)  M); signing μ not M provides BUFF  beyond-unforgeability properties]] - paper - references/ch14/ref-64-fips-204.pdf
- [[NTT over R_q (q=8380417, ζ=1753 a 512th root of unity) fast module-polynomial multiplication NTT(ab)=NTT(a)∘NTT(b)]] - paper - references/ch14/ref-64-fips-204.pdf
- [[Power2Round  Decompose  HighBits  LowBits drop d=13 low-order bits of t and round w to multiples of α=2γ2]] - paper - references/ch14/ref-64-fips-204.pdf
- [[Rejection sampling abort and restart with new mask y if z (or r0) coefficients fall outside bound, removing bias toward secret s1s2]] - paper - references/ch14/ref-64-fips-204.pdf
- [[SampleInBall (Alg 29) challenge polynomial c with exactly τ nonzero ±1 coefficients, derived from c~]] - paper - references/ch14/ref-64-fips-204.pdf
- [[Strong existential unforgeability under chosen-message attack (SUF-CMA) plus BUFF properties]] - paper - references/ch14/ref-64-fips-204.pdf
- [[Uses SHAKE128 and SHAKE256 (FIPS 202) as XOFs for all expansion, hashing, and challenge derivation]] - paper - references/ch14/ref-64-fips-204.pdf

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ML-DSA_FIPS_204
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Folding & Lattice Crypto]]
- 3 edges to [[_COMMUNITY_ML-KEM (FIPS 203)]]
- 3 edges to [[_COMMUNITY_PQC Transition (NIST IR 8547)]]
- 2 edges to [[_COMMUNITY_Core Concepts & Book Spine]]
- 1 edge to [[_COMMUNITY_Witness Generation & Hashing]]

## Top bridge nodes
- [[ML-DSA (Module-Lattice Digital Signature Algorithm)]] - degree 18, connects to 3 communities
- [[FIPS 204 Module-Lattice-Based Digital Signature Standard]] - degree 5, connects to 2 communities
- [[Fiat-Shamir With Aborts construction (Schnorr-like signature with rejection sampling on the response)]] - degree 4, connects to 1 community
- [[ML-DSA.KeyGen (Alg 16.1) expand seed ξ - seed ρ for A, seeds for s1,s2,K; t = A·s1 + s2, publish compressed t1]] - degree 4, connects to 1 community
- [[ML-DSA derived from CRYSTALS-DILITHIUM v3.1 (Round-3 PQC selection); differences in Appendix D]] - degree 2, connects to 1 community