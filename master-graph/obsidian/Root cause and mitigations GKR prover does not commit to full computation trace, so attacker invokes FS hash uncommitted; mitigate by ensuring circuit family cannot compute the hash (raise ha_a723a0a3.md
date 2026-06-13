---
source_file: "references/recursion/ch1/ref-11-khovratovich-fiat-shamir-attacks.pdf"
type: "paper"
community: "Community 12"
location: "§5, fn.4"
tags:
  - graphify/paper
  - graphify/EXTRACTED
  - community/Community_12
---

# Root cause and mitigations: GKR prover does not commit to full computation trace, so attacker invokes FS hash uncommitted; mitigate by ensuring circuit family cannot compute the hash (raise hash depth/degree, lower circuit depth, commit intermediates); Expander PR#184

## Connections
- [[Arnon-Yogev AY25 Towards a white-box secure Fiat-Shamir transformation - followup mitigation (larger hash + PoW); model fails to capture this attack]] - `cites` [EXTRACTED]
- [[GKR protocol doubly-efficient interactive proof for bounded-depth computation via layer-by-layer sumcheck reduction; prover need not commit to full trace]] - `conceptually_related_to` [EXTRACTED]
- [[In-circuit hash the FS hash function (and PCS) computed inside the GKR arithmetic circuit being proved; depth d = d_comm+d_h enables the attack]] - `conceptually_related_to` [EXTRACTED]
- [[Soundness attack producing an accepting proof for a false statement in a FS-compiled argument (adaptive and non-adaptive variants)]] - `conceptually_related_to` [EXTRACTED]

#graphify/paper #graphify/EXTRACTED #community/Community_12