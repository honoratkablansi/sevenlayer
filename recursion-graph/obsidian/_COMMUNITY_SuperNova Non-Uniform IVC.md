---
type: community
cohesion: 0.21
members: 13
---

# SuperNova Non-Uniform IVC

**Cohesion:** 0.21 - loosely connected
**Members:** 13 nodes

## Members
- [[Augmented function F'_j runs F_j then a verifier circuit folding u_i into U_ipc, checks public IO hash, and computes pc_{i+1} via phi]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Construction 1 SuperNova NIVC scheme (G,K,P,V) built from non-interactive folding scheme NIFS for committed relaxed R1CS plus a hash]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Control function phi takes (z_i, omega_i) and outputs program counter pc in {1,...,l} selecting which F_j to apply at each step]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Instantiations VDF machine (l=1, MinRoot) and RAM machine (RISC-V-like, program counter register, Merkle-committed memory)]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Lemma 1  Assumption 1 non-interactive folding scheme for committed relaxed R1CS (Nova 21); prover O(n), verifier and communication O(1), via Fiat-Shamir in plain model]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Lemma 2 (Completeness) Construction 1 is an NIVC scheme satisfying perfect completeness]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Lemma 3 (Knowledge soundness) Construction 1 satisfies knowledge soundness via inductive extractor reduction to folding-scheme soundness]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Lemma 4 (Efficiency) F'_j = phi + F_j + o(2G + 2H + R); prover cost dominated by two multiexponentiations sized to the executed instruction]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Multiple running instances, one per instruction type; incoming step instance folded into the running instance selected by pc (U_ipc)]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Non-uniform IVC (NIVC) generalization of IVC where each step proves a relation chosen from a set, selected by a control function]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Optimization offlineMerkle memory-checking reduces F'_j circuit dependence on l from O(l) to O(log l) then to O(1) constraints]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Per-instruction step functions {F_1,...,F_l} plus control function phi; each F_j verifies one instruction type, cost independent of l]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Program counter (pc) index selecting which instructionfunction is run at a step; computed by control function phi and threaded between augmented circuits]] - paper - references/recursion/ch2/ref-44-supernova.pdf

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SuperNova_Non-Uniform_IVC
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_SuperNova vs Universal Circuits]]
- 2 edges to [[_COMMUNITY_Folding Schemes (LatticeFold)]]
- 2 edges to [[_COMMUNITY_Relaxed R1CS & Cross-Terms]]
- 1 edge to [[_COMMUNITY_IVC Foundations (Valiant)]]
- 1 edge to [[_COMMUNITY_Nova & the Cycle-of-Curves Bug]]
- 1 edge to [[_COMMUNITY_zkVMs & Real-Time Proving]]

## Top bridge nodes
- [[Construction 1 SuperNova NIVC scheme (G,K,P,V) built from non-interactive folding scheme NIFS for committed relaxed R1CS plus a hash]] - degree 8, connects to 2 communities
- [[Non-uniform IVC (NIVC) generalization of IVC where each step proves a relation chosen from a set, selected by a control function]] - degree 5, connects to 2 communities
- [[Lemma 1  Assumption 1 non-interactive folding scheme for committed relaxed R1CS (Nova 21); prover O(n), verifier and communication O(1), via Fiat-Shamir in plain model]] - degree 4, connects to 2 communities
- [[Per-instruction step functions {F_1,...,F_l} plus control function phi; each F_j verifies one instruction type, cost independent of l]] - degree 4, connects to 1 community
- [[Instantiations VDF machine (l=1, MinRoot) and RAM machine (RISC-V-like, program counter register, Merkle-committed memory)]] - degree 3, connects to 1 community