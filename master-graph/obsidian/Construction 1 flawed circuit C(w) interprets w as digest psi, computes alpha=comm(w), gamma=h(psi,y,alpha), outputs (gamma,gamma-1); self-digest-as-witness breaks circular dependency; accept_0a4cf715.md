---
source_file: "references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf"
type: "paper"
community: "Community 122"
location: "Construction 1 (p.10), §3.1"
tags:
  - graphify/paper
  - graphify/EXTRACTED
  - community/Community_122
---

# Construction 1: flawed circuit C*(w) interprets w as digest psi, computes alpha=comm(w), gamma=h(psi,y*,alpha), outputs (gamma,gamma-1); self-digest-as-witness breaks circular dependency; accepts false claim with prob 1

## Connections
- [[Correlation intractability the property whose circular dependency the attack circumvents by feeding the circuit its own digest as witness]] - `conceptually_related_to` [EXTRACTED]
- [[In-circuit hash the FS hash function (and PCS) computed inside the GKR arithmetic circuit being proved; depth d = d_comm+d_h enables the attack]] - `conceptually_related_to` [EXTRACTED]
- [[Theorem 1 (Basic Attack) for every h (depth d_h) and comm (depth d_comm), for d = d_comm+d_h+O(1), FS_h(Pi_{comm,d}) is not adaptively sound]] - `proves` [EXTRACTED]

#graphify/paper #graphify/EXTRACTED #community/Community_122