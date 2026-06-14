---
type: community
cohesion: 0.13
members: 22
---

# Community 55

**Cohesion:** 0.13 - loosely connected
**Members:** 22 nodes

## Members
- [[A la carte cost profile per-step proving cost proportional only to the circuit size of the invoked instruction, independent of k (number of instruction types)]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Augmented function F'_j runs F_j then a verifier circuit folding u_i into U_ipc, checks public IO hash, and computes pc_{i+1} via phi]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Avoiding universal switch circuits SuperNova never builds a circuit summing all instruction circuits; per-step cost depends only on the executed instruction]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Buffet 34 a-la-carte cost via line-by-line compilation to non-uniform circuits, but not incremental and needs static execution bounds]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Compression to succinct zero-knowledge apply a general-purpose zkSNARK (e.g., Spartan) over a valid NIVC proof, as in Nova]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Construction 1 SuperNova NIVC scheme (G,K,P,V) built from non-interactive folding scheme NIFS for committed relaxed R1CS plus a hash]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Control function phi takes (z_i, omega_i) and outputs program counter pc in {1,...,l} selecting which F_j to apply at each step]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Instantiations VDF machine (l=1, MinRoot) and RAM machine (RISC-V-like, program counter register, Merkle-committed memory)]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Kothapalli, Setty, Tzialla, Nova (CRYPTO 2022)]] - document - recursion/recursion-outline.md
- [[Lemma 1  Assumption 1 non-interactive folding scheme for committed relaxed R1CS (Nova 21); prover O(n), verifier and communication O(1), via Fiat-Shamir in plain model]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Lemma 2 (Completeness) Construction 1 is an NIVC scheme satisfying perfect completeness]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Lemma 3 (Knowledge soundness) Construction 1 satisfies knowledge soundness via inductive extractor reduction to folding-scheme soundness]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Lemma 4 (Efficiency) F'_j = phi + F_j + o(2G + 2H + R); prover cost dominated by two multiexponentiations sized to the executed instruction]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[MIRAGE 20 adapts vRAM techniques to Groth's SNARK; still relies on whole-trace invariants, incompatible with incremental proving]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Multiple running instances, one per instruction type; incoming step instance folded into the running instance selected by pc (U_ipc)]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Non-uniform IVC (NIVC) generalization of IVC where each step proves a relation chosen from a set, selected by a control function]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Optimization offlineMerkle memory-checking reduces F'_j circuit dependence on l from O(l) to O(log l) then to O(1) constraints]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Per-instruction step functions {F_1,...,F_l} plus control function phi; each F_j verifies one instruction type, cost independent of l]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[Program counter (pc) index selecting which instructionfunction is run at a step; computed by control function phi and threaded between augmented circuits]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[SuperNova (Non-Uniform IVC)]] - document - proving-nothing.md
- [[Universal circuit single circuit executing any supported instruction (fetch-decode-execute); per-step cost scales with sum of all instruction circuit sizes]] - paper - references/recursion/ch2/ref-44-supernova.pdf
- [[vRAM 37 trimmed universal circuit for vnTinyRAM via fingerprinting over the trace; not incremental, not zero-knowledge]] - paper - references/recursion/ch2/ref-44-supernova.pdf

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_55
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Community 22]]
- 4 edges to [[_COMMUNITY_Community 25]]
- 3 edges to [[_COMMUNITY_Community 15]]
- 2 edges to [[_COMMUNITY_Community 10]]
- 1 edge to [[_COMMUNITY_Community 1]]
- 1 edge to [[_COMMUNITY_Community 29]]

## Top bridge nodes
- [[SuperNova (Non-Uniform IVC)]] - degree 15, connects to 5 communities
- [[Universal circuit single circuit executing any supported instruction (fetch-decode-execute); per-step cost scales with sum of all instruction circuit sizes]] - degree 4, connects to 2 communities
- [[Lemma 1  Assumption 1 non-interactive folding scheme for committed relaxed R1CS (Nova 21); prover O(n), verifier and communication O(1), via Fiat-Shamir in plain model]] - degree 4, connects to 2 communities
- [[Construction 1 SuperNova NIVC scheme (G,K,P,V) built from non-interactive folding scheme NIFS for committed relaxed R1CS plus a hash]] - degree 8, connects to 1 community
- [[Non-uniform IVC (NIVC) generalization of IVC where each step proves a relation chosen from a set, selected by a control function]] - degree 5, connects to 1 community