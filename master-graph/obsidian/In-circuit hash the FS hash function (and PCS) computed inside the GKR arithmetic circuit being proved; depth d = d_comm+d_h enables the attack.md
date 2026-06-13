---
source_file: "references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf"
type: "paper"
community: "Community 12"
location: "§1.1.2, §5"
tags:
  - graphify/paper
  - graphify/EXTRACTED
  - community/Community_12
---

# In-circuit hash: the FS hash function (and PCS) computed inside the GKR arithmetic circuit being proved; depth d >= d_comm+d_h enables the attack

## Connections
- [[Arithmetization-friendly  low-constraint hashing over a large prime field for ZK proof circuits]] - `conceptually_related_to` [EXTRACTED]
- [[Construction 1 flawed circuit C(w) interprets w as digest psi, computes alpha=comm(w), gamma=h(psi,y,alpha), outputs (gamma,gamma-1); self-digest-as-witness breaks circular dependency; accept_0a4cf715]] - `conceptually_related_to` [EXTRACTED]
- [[Construction 2 backdoored C via IF-THEN-ELSE gate and helper g that internally runs FS challenge; Proposition 7 shows fake transcript (u_fake) validates real evaluation since first coord of r_b94eb212]] - `conceptually_related_to` [EXTRACTED]
- [[Poseidon Hash_1]] - `conceptually_related_to` [EXTRACTED]
- [[Recursive Proof Composition_1]] - `conceptually_related_to` [EXTRACTED]
- [[Root cause and mitigations GKR prover does not commit to full computation trace, so attacker invokes FS hash uncommitted; mitigate by ensuring circuit family cannot compute the hash (raise ha_a723a0a3]] - `conceptually_related_to` [EXTRACTED]

#graphify/paper #graphify/EXTRACTED #community/Community_12