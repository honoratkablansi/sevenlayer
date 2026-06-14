---
type: community
cohesion: 0.29
members: 8
---

# Community 125

**Cohesion:** 0.29 - loosely connected
**Members:** 8 nodes

## Members
- [[Arithmetization-friendly  low-constraint hashing over a large prime field for ZK proof circuits]] - paper - references/recursion/ch1/ref-31-poseidon.pdf
- [[Arnon-Yogev AY25 Towards a white-box secure Fiat-Shamir transformation - followup mitigation (larger hash + PoW); model fails to capture this attack]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Construction 1 flawed circuit C(w) interprets w as digest psi, computes alpha=comm(w), gamma=h(psi,y,alpha), outputs (gamma,gamma-1); self-digest-as-witness breaks circular dependency; accept_0a4cf715]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Construction 2 backdoored C via IF-THEN-ELSE gate and helper g that internally runs FS challenge; Proposition 7 shows fake transcript (u_fake) validates real evaluation since first coord of r_b94eb212]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[In-circuit hash the FS hash function (and PCS) computed inside the GKR arithmetic circuit being proved; depth d = d_comm+d_h enables the attack]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Root cause and mitigations GKR prover does not commit to full computation trace, so attacker invokes FS hash uncommitted; mitigate by ensuring circuit family cannot compute the hash (raise ha_a723a0a3]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Theorem 1 (Basic Attack) for every h (depth d_h) and comm (depth d_comm), for d = d_comm+d_h+O(1), FS_h(Pi_{comm,d}) is not adaptively sound]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf
- [[Theorem 2 (Extended Attack) poly-time A turns any admissible circuit C into functionally-equivalent C (depth d+d_comm+O(d_h log l)) plus proof that C(x,w)=y for arbitrary y; soundness depends_296f75ab]] - paper - references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_125
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Community 129]]
- 2 edges to [[_COMMUNITY_Community 3]]
- 2 edges to [[_COMMUNITY_Community 96]]
- 1 edge to [[_COMMUNITY_Community 120]]
- 1 edge to [[_COMMUNITY_Community 24]]
- 1 edge to [[_COMMUNITY_Community 21]]
- 1 edge to [[_COMMUNITY_Community 2]]
- 1 edge to [[_COMMUNITY_Community 63]]

## Top bridge nodes
- [[Arithmetization-friendly  low-constraint hashing over a large prime field for ZK proof circuits]] - degree 4, connects to 3 communities
- [[In-circuit hash the FS hash function (and PCS) computed inside the GKR arithmetic circuit being proved; depth d = d_comm+d_h enables the attack]] - degree 6, connects to 2 communities
- [[Root cause and mitigations GKR prover does not commit to full computation trace, so attacker invokes FS hash uncommitted; mitigate by ensuring circuit family cannot compute the hash (raise ha_a723a0a3]] - degree 4, connects to 2 communities
- [[Theorem 1 (Basic Attack) for every h (depth d_h) and comm (depth d_comm), for d = d_comm+d_h+O(1), FS_h(Pi_{comm,d}) is not adaptively sound]] - degree 4, connects to 2 communities
- [[Theorem 2 (Extended Attack) poly-time A turns any admissible circuit C into functionally-equivalent C (depth d+d_comm+O(d_h log l)) plus proof that C(x,w)=y for arbitrary y; soundness depends_296f75ab]] - degree 4, connects to 2 communities