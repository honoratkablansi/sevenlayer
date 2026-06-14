---
type: community
cohesion: 0.20
members: 11
---

# Community 101

**Cohesion:** 0.20 - loosely connected
**Members:** 11 nodes

## Members
- [[Arithmetization-friendly  low-constraint hashing over a large prime field for ZK proof circuits]] - paper - references/recursion/ch1/ref-31-poseidon.pdf
- [[Arnon-Yogev AY25 Towards a white-box secure Fiat-Shamir transformation - followup mitigation (larger hash + PoW); model fails to capture this attack]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Cited competitor Pedersen hash HBHW19 - Zcash 256-bit hash, ~1.7 constraintsbit baseline Poseidon improves on]] - paper - references/recursion/ch1/ref-31-poseidon.pdf
- [[Construction 1 flawed circuit C(w) interprets w as digest psi, computes alpha=comm(w), gamma=h(psi,y,alpha), outputs (gamma,gamma-1); self-digest-as-witness breaks circular dependency; accept_0a4cf715]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Construction 2 backdoored C via IF-THEN-ELSE gate and helper g that internally runs FS challenge; Proposition 7 shows fake transcript (u_fake) validates real evaluation since first coord of r_b94eb212]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Definition 6 adaptive soundness of FS_h(Pi_{comm,d}); adversary given spec of h and comm outputs (C,x,y,pi) with C(x,w)!=y yet verifier accepts]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[In-circuit hash the FS hash function (and PCS) computed inside the GKR arithmetic circuit being proved; depth d = d_comm+d_h enables the attack]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[R1CS constraint count 2tRF+2RP for x3, 3tRF+3RP for x5; up to 8x fewer constraintsbit than Pedersen hash]] - paper - references/recursion/ch1/ref-31-poseidon.pdf
- [[Root cause and mitigations GKR prover does not commit to full computation trace, so attacker invokes FS hash uncommitted; mitigate by ensuring circuit family cannot compute the hash (raise ha_a723a0a3]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Theorem 1 (Basic Attack) for every h (depth d_h) and comm (depth d_comm), for d = d_comm+d_h+O(1), FS_h(Pi_{comm,d}) is not adaptively sound]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Theorem 2 (Extended Attack) poly-time A turns any admissible circuit C into functionally-equivalent C (depth d+d_comm+O(d_h log l)) plus proof that C(x,w)=y for arbitrary y; soundness depends_296f75ab]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_101
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Community 13]]
- 3 edges to [[_COMMUNITY_Community 23]]
- 3 edges to [[_COMMUNITY_Community 124]]
- 1 edge to [[_COMMUNITY_Community 116]]
- 1 edge to [[_COMMUNITY_Community 85]]
- 1 edge to [[_COMMUNITY_Community 6]]
- 1 edge to [[_COMMUNITY_Community 114]]

## Top bridge nodes
- [[In-circuit hash the FS hash function (and PCS) computed inside the GKR arithmetic circuit being proved; depth d = d_comm+d_h enables the attack]] - degree 6, connects to 2 communities
- [[Arithmetization-friendly  low-constraint hashing over a large prime field for ZK proof circuits]] - degree 4, connects to 2 communities
- [[Root cause and mitigations GKR prover does not commit to full computation trace, so attacker invokes FS hash uncommitted; mitigate by ensuring circuit family cannot compute the hash (raise ha_a723a0a3]] - degree 4, connects to 2 communities
- [[Theorem 2 (Extended Attack) poly-time A turns any admissible circuit C into functionally-equivalent C (depth d+d_comm+O(d_h log l)) plus proof that C(x,w)=y for arbitrary y; soundness depends_296f75ab]] - degree 4, connects to 2 communities
- [[R1CS constraint count 2tRF+2RP for x3, 3tRF+3RP for x5; up to 8x fewer constraintsbit than Pedersen hash]] - degree 4, connects to 2 communities