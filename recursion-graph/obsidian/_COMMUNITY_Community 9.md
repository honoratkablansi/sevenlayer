---
type: community
cohesion: 0.08
members: 39
---

# Community 9

**Cohesion:** 0.08 - loosely connected
**Members:** 39 nodes

## Members
- [[Arnon-Yogev AY25 Towards a white-box secure Fiat-Shamir transformation - followup mitigation (larger hash + PoW); model fails to capture this attack]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Augmented constraint systems R1 and R2 (Fig 1a1b) each folds opposite-field instance, hashes carry public IO across the cycle]] - paper - references/recursion/ch1/ref-32-nguyen-boneh-setty-nova-cycle.pdf
- [[Canetti-Goldreich-Halevi CGH04 The random oracle methodology, revisited - RO-uninstantiable primitives; diagonalization basis of attack]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Committed relaxed R1CS over the ring R = F1 x F2 (binding, additively-homomorphic, succinct commitments)]] - paper - references/recursion/ch1/ref-32-nguyen-boneh-setty-nova-cycle.pdf
- [[Construction 1 flawed circuit C(w) interprets w as digest psi, computes alpha=comm(w), gamma=h(psi,y,alpha), outputs (gamma,gamma-1); self-digest-as-witness breaks circular dependency; accept_0a4cf715]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Construction 2 backdoored C via IF-THEN-ELSE gate and helper g that internally runs FS challenge; Proposition 7 shows fake transcript (u_fake) validates real evaluation since first coord of r_b94eb212]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Definition 6 adaptive soundness of FS_h(Pi_{comm,d}); adversary given spec of h and comm outputs (C,x,y,pi) with C(x,w)!=y yet verifier accepts]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Diagonalization-based uninstantiability craft a self-referential prover message yielding a favorable verifier challenge (CGH04 lineage; Kleene recursion  quines)]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Fix remove pair (u(1)_i, w(1)_i) from IVC proof and shift hash check to u(2)_i.x0 = H1(vk,i,z0,zi,U(2)_i)]] - paper - references/recursion/ch1/ref-32-nguyen-boneh-setty-nova-cycle.pdf
- [[General binding lesson every claimed running instance must be cryptographically bound (via hashcopy constraints) to the witness actually folded into it]] - paper - references/recursion/ch1/ref-32-nguyen-boneh-setty-nova-cycle.pdf
- [[Goldwasser-Kalai-Rothblum GKR15 Delegating computation interactive proofs for Muggles - the GKR protocol]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[IVC proof compression a final fold (without SNARK) plus Spartan zkSNARK over R_sat yields the CompressedSNARK]] - paper - references/recursion/ch1/ref-32-nguyen-boneh-setty-nova-cycle.pdf
- [[In-circuit hash the FS hash function (and PCS) computed inside the GKR arithmetic circuit being proved; depth d = d_comm+d_h enables the attack]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Insufficient binding the extra instance-witness pair u(1)_i in the proof was not constrained to be the one folded into running instance U(1)_i]] - paper - references/recursion/ch1/ref-32-nguyen-boneh-setty-nova-cycle.pdf
- [[Khovratovich, Maller, Tiwari — MinRoot candidate sequential function for Ethereum VDF (2022) 9]] - paper - references/recursion/ch1/ref-32-nguyen-boneh-setty-nova-cycle.pdf
- [[Khovratovich-Rothblum-Soukhanov How to Prove False Statements - Practical Attacks on Fiat-Shamir (ePrint 2025118)]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Kothapalli, Setty, Tzialla — Nova Recursive zero-knowledge arguments from folding schemes (CRYPTO 2022) 11]] - paper - references/recursion/ch1/ref-32-nguyen-boneh-setty-nova-cycle.pdf
- [[Modified 2-cycle Nova IVC scheme shorter proofs (eliminates one R1CS instance-witness pair), proven sound; adopted upstream (PR 167)]] - paper - references/recursion/ch1/ref-32-nguyen-boneh-setty-nova-cycle.pdf
- [[Multilinear polynomial commitment scheme (MLPCS) short commitment to a multilinear polynomial with succinct evaluation proofs]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Nova IVC proofs are malleable attacker mauls final z_i to z'_i (different last aux) without knowing earlier aux values]] - paper - references/recursion/ch1/ref-32-nguyen-boneh-setty-nova-cycle.pdf
- [[PoC forged Nova proof of 275 Minroot VDF rounds in 1.46 s on a laptop (NovaBreakingTheCycleAttack fork)]] - paper - references/recursion/ch1/ref-32-nguyen-boneh-setty-nova-cycle.pdf
- [[Polyhedra Network Expander Pol24 - deployed GKR-based system affected; authors notified designers, mitigations introduced]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Prior FS uninstantiability counterexamples Barak Bar01, Goldwasser-Kalai GK03, and Bartusek et al. BBH+19 On the (in)security of Kilian-based SNARGs]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Protocol Pi_{comm,d} GKR + MLPCS succinct argument for non-deterministic depth-d circuit C(x,w)=y; FS-compiled as FS_h(Pi_{comm,d}); challenge r=h(C,x,y,alpha)]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Recursive composition prior work Valiant Val08 IVC, Bitansky-Canetti-Chiesa-Tromer BCCT13 PCD, Ben-Sasson-Chiesa-Tromer-Virza BCTV14 cycles of elliptic curves]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Revisiting the Nova Proof System on a Cycle of Curves (Nguyen, Boneh, Setty, ePrint 2023969)]] - paper - references/recursion/ch1/ref-32-nguyen-boneh-setty-nova-cycle.pdf
- [[Root cause and mitigations GKR prover does not commit to full computation trace, so attacker invokes FS hash uncommitted; mitigate by ensuring circuit family cannot compute the hash (raise ha_a723a0a3]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Setty — Spartan efficient general-purpose zkSNARKs without trusted setup (CRYPTO 2020) 16]] - paper - references/recursion/ch1/ref-32-nguyen-boneh-setty-nova-cycle.pdf
- [[Soundness attack producing an accepting proof for a false statement in a FS-compiled argument (adaptive and non-adaptive variants)]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Theorem 1 (Basic Attack) for every h (depth d_h) and comm (depth d_comm), for d = d_comm+d_h+O(1), FS_h(Pi_{comm,d}) is not adaptively sound]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Theorem 10 (informal) universal GKR circuit unsound for any additively-homomorphic commitment (EC or lattice) since comm(w)=comm(wC)+comm(win); also batched FRI]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Theorem 1 if the folding scheme is knowledge-sound and the hash is collision-resistant, the modified 2-cycle Nova IVC is knowledge-sound]] - paper - references/recursion/ch1/ref-32-nguyen-boneh-setty-nova-cycle.pdf
- [[Theorem 2 (Extended Attack) poly-time A turns any admissible circuit C into functionally-equivalent C (depth d+d_comm+O(d_h log l)) plus proof that C(x,w)=y for arbitrary y; soundness depends_296f75ab]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Theorem 9 family T'(N,M) unsound for any commitment with sub-input-size code and any hash; uses an f-quine (Lemma 8, p=f+c via Kleene recursion) passed as witness; commitment-independent]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Three malleability mitigations zkSNARK compression (simulation-extractable), context in vk, and incremental context (range-keyed vk swap)]] - paper - references/recursion/ch1/ref-32-nguyen-boneh-setty-nova-cycle.pdf
- [[Two parallel IVC chains over a curve cycle that must be linked (R1CS(1)R1CS(2) over ring R = F1 x F2)]] - paper - references/recursion/ch1/ref-32-nguyen-boneh-setty-nova-cycle.pdf
- [[Two-stage forged-proof construction run honest prover with adversarial u(1)_{i-1}U(2)_perp inputs to produce convincing proof for false statement]] - paper - references/recursion/ch1/ref-32-nguyen-boneh-setty-nova-cycle.pdf
- [[Underconstrained additional R1CS instance-witness pair (u(1)_i, w(1)_i) carried in the old IVC proof]] - paper - references/recursion/ch1/ref-32-nguyen-boneh-setty-nova-cycle.pdf
- [[Universal Computation Attack (§4) fixed circuits independent of crypto primitives via universal Turing machine circuit and quines; violates non-adaptive soundness]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_9
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Community 21]]
- 3 edges to [[_COMMUNITY_Community 23]]
- 3 edges to [[_COMMUNITY_Community 35]]
- 3 edges to [[_COMMUNITY_Community 17]]
- 2 edges to [[_COMMUNITY_Community 32]]
- 2 edges to [[_COMMUNITY_Community 12]]
- 2 edges to [[_COMMUNITY_Community 5]]
- 1 edge to [[_COMMUNITY_Community 3]]

## Top bridge nodes
- [[Khovratovich-Rothblum-Soukhanov How to Prove False Statements - Practical Attacks on Fiat-Shamir (ePrint 2025118)]] - degree 11, connects to 2 communities
- [[In-circuit hash the FS hash function (and PCS) computed inside the GKR arithmetic circuit being proved; depth d = d_comm+d_h enables the attack]] - degree 6, connects to 2 communities
- [[Protocol Pi_{comm,d} GKR + MLPCS succinct argument for non-deterministic depth-d circuit C(x,w)=y; FS-compiled as FS_h(Pi_{comm,d}); challenge r=h(C,x,y,alpha)]] - degree 6, connects to 2 communities
- [[Kothapalli, Setty, Tzialla — Nova Recursive zero-knowledge arguments from folding schemes (CRYPTO 2022) 11]] - degree 3, connects to 2 communities
- [[Modified 2-cycle Nova IVC scheme shorter proofs (eliminates one R1CS instance-witness pair), proven sound; adopted upstream (PR 167)]] - degree 5, connects to 1 community