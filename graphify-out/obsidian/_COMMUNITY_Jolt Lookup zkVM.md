---
type: community
cohesion: 0.16
members: 20
---

# Jolt Lookup zkVM

**Cohesion:** 0.16 - loosely connected
**Members:** 20 nodes

## Members
- [[All RISC-V instructions are decomposable (main technical contribution)]] - paper - references/ch03/ref-16-jolt.pdf
- [[Comparison vs RISC Zero (~34), Cairo-VM (~13), Plonk per CPU step]] - paper - references/ch03/ref-16-jolt.pdf
- [[Decomposable tables]] - paper - references/ch03/ref-16-jolt.pdf
- [[Generalized-Lasso vs Lasso auditabilityperformance tradeoff (2x-3x cost)]] - paper - references/ch03/ref-16-jolt.pdf
- [[Jolt SNARKs for Virtual Machines via Lookups]] - paper - references/ch03/ref-16-jolt.pdf
- [[Lasso]] - document - wiki/concepts/lasso.md
- [[Lasso companion paper STW23 (Setty, Thaler, Wahby 2023)]] - paper - references/ch03/ref-16-jolt.pdf
- [[Lemma 2 RS and WS are permutations iff every read returns last-written (value,count)]] - paper - references/ch03/ref-16-jolt.pdf
- [[Lemma 2 linear combinations of commitments respect right-multiplication of openings]] - paper - references/ch06/ref-21-neo.pdf
- [[Linearly homomorphic commitment]] - paper - references/ch06/ref-21-neo.pdf
- [[MLE-structured tables]] - paper - references/ch03/ref-16-jolt.pdf
- [[MSM commitment via Pippenger's algorithm]] - paper - references/ch03/ref-16-jolt.pdf
- [[Multilinear extension (MLE)]] - paper - references/ch03/ref-16-jolt.pdf
- [[Per-instruction MLE-structured evaluation tables (EQ, LTU, SLL, ANDORXOR, ADDSUB, MUL)]] - paper - references/ch03/ref-16-jolt.pdf
- [[Prover commits to ~6 256-bit field elements per RISC-V CPU step]] - paper - references/ch03/ref-16-jolt.pdf
- [[Single collation polynomial g for concatenated instruction tables]] - paper - references/ch03/ref-16-jolt.pdf
- [[Single giant 2128 RISC-V lookup table T_risc-vopcodexy]] - paper - references/ch03/ref-16-jolt.pdf
- [[Spartan applied to uniform R1CS (no commitment to A,B,C matrices)]] - paper - references/ch03/ref-16-jolt.pdf
- [[Spice-based memory-checking optimized with Lasso (max via lookup)]] - paper - references/ch03/ref-16-jolt.pdf
- [[Virtual instructions and virtual registers (MULH, DIVREM, MOVSIGN, ADVICE, ASSERT)]] - paper - references/ch03/ref-16-jolt.pdf

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Jolt_Lookup_zkVM
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_Arithmetization & CCS]]
- 7 edges to [[_COMMUNITY_Sumcheck & Small-Space zkVMs]]
- 5 edges to [[_COMMUNITY_Core Concepts & Book Spine]]
- 5 edges to [[_COMMUNITY_Lasso Lookup Arguments]]
- 4 edges to [[_COMMUNITY_Open Questions & Convergence]]
- 2 edges to [[_COMMUNITY_Witness Generation & Hashing]]
- 2 edges to [[_COMMUNITY_Succinct Arguments & Streaming PIOPs]]
- 1 edge to [[_COMMUNITY_Recursive Proofs & IVC]]
- 1 edge to [[_COMMUNITY_PLONK & Permutation Arguments]]
- 1 edge to [[_COMMUNITY_Lattice Folding (Neo)]]
- 1 edge to [[_COMMUNITY_Lattice Folding (LatticeFold)]]
- 1 edge to [[_COMMUNITY_Memory Checking & Sparse PCS]]

## Top bridge nodes
- [[Lasso]] - degree 25, connects to 7 communities
- [[Jolt SNARKs for Virtual Machines via Lookups]] - degree 25, connects to 6 communities
- [[Multilinear extension (MLE)]] - degree 7, connects to 4 communities
- [[All RISC-V instructions are decomposable (main technical contribution)]] - degree 3, connects to 1 community
- [[Spice-based memory-checking optimized with Lasso (max via lookup)]] - degree 3, connects to 1 community