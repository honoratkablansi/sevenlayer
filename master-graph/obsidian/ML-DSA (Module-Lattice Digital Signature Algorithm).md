---
source_file: "references/ch14/ref-64-fips-204.pdf"
type: "document"
community: "Community 81"
location: "Abstract"
tags:
  - graphify/document
  - graphify/EXTRACTED
  - community/Community_81
---

# ML-DSA (Module-Lattice Digital Signature Algorithm)

## Connections
- [[FIPS 204 (ML-DSA Standard)]] - `defines` [EXTRACTED]
- [[FIPS 204 Module-Lattice-Based Digital Signature Standard]] - `defines` [EXTRACTED]
- [[FIPS 204 Module-Lattice-Based Digital Signature Standard (ML-DSA), published 2024-08-13]] - `defines` [EXTRACTED]
- [[Fiat-Shamir With Aborts construction (Schnorr-like signature with rejection sampling on the response)]] - `introduces` [EXTRACTED]
- [[Five Post-Quantum Security Categories (1-5; AES-128 to AES-256, SHA-256SHA3-384)]] - `conceptually_related_to` [EXTRACTED]
- [[HashML-DSA domain-separated pre-hash variant signing PH(M) for largestreamed messages]] - `introduces` [EXTRACTED]
- [[Hedged (default, fresh + precomputed randomness) vs deterministic signing variant; same Verify works for both]] - `introduces` [EXTRACTED]
- [[ML-DSA derived from CRYSTALS-DILITHIUM v3.1 (Round-3 PQC selection); differences in Appendix D]] - `conceptually_related_to` [EXTRACTED]
- [[ML-DSA-44 parameter set (k,ℓ)=(4,4), η=2, τ=39, λ=128, Category 2; pk 1312 B, sk 2560 B, sig 2420 B]] - `defines` [EXTRACTED]
- [[ML-DSA-65 parameter set (k,ℓ)=(6,5), η=4, τ=49, λ=192, Category 3; pk 1952 B, sk 4032 B, sig 3309 B]] - `defines` [EXTRACTED]
- [[ML-DSA-87 parameter set (k,ℓ)=(8,7), η=2, τ=60, λ=256, Category 5; pk 2592 B, sk 4896 B, sig 4627 B]] - `defines` [EXTRACTED]
- [[ML-DSA.KeyGen (Alg 16.1) expand seed ξ - seed ρ for A, seeds for s1,s2,K; t = A·s1 + s2, publish compressed t1]] - `defines` [EXTRACTED]
- [[ML-DSA.Sign (Alg 26.2) commit w=Ay, challenge c~ from H(w1μ), response z = y + c·s1, with rejection-sampling abort loop]] - `defines` [EXTRACTED]
- [[ML-DSA.Verify (Alg 36.3) recompute w1' via UseHint from z, t1, c; accept iff z is short and c~ matches H(w1'μ)]] - `defines` [EXTRACTED]
- [[PQC signature replacements ML-DSA-446587, SLH-DSA, LMSHSS, XMSS]] - `introduces` [EXTRACTED]
- [[Post-Quantum Cryptography]] - `conceptually_related_to` [EXTRACTED]
- [[Security based on Module-LWE over R_q plus SelfTargetMSIS, a nonstandard variant of Module-SIS]] - `assumes` [EXTRACTED]
- [[Strong existential unforgeability under chosen-message attack (SUF-CMA) plus BUFF properties]] - `proves` [INFERRED]

#graphify/document #graphify/EXTRACTED #community/Community_81