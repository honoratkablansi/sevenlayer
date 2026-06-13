---
source_file: "references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf"
type: "paper"
community: "Community 24"
location: "Theorem 1 (p.4)"
tags:
  - graphify/paper
  - graphify/EXTRACTED
  - community/Community_24
---

# Theorem 1 (Basic Attack): for every h (depth d_h) and comm (depth d_comm), for d >= d_comm+d_h+O(1), FS_h(Pi_{comm,d}) is not adaptively sound

## Connections
- [[Construction 1 flawed circuit C(w) interprets w as digest psi, computes alpha=comm(w), gamma=h(psi,y,alpha), outputs (gamma,gamma-1); self-digest-as-witness breaks circular dependency; accept_0a4cf715]] - `proves` [EXTRACTED]
- [[Definition 6 adaptive soundness of FS_h(Pi_{comm,d}); adversary given spec of h and comm outputs (C,x,y,pi) with C(x,w)!=y yet verifier accepts]] - `proves` [EXTRACTED]
- [[Soundness attack producing an accepting proof for a false statement in a FS-compiled argument (adaptive and non-adaptive variants)]] - `proves` [EXTRACTED]
- [[Theorem 2 (Extended Attack) poly-time A turns any admissible circuit C into functionally-equivalent C (depth d+d_comm+O(d_h log l)) plus proof that C(x,w)=y for arbitrary y; soundness depends_296f75ab]] - `conceptually_related_to` [EXTRACTED]

#graphify/paper #graphify/EXTRACTED #community/Community_24