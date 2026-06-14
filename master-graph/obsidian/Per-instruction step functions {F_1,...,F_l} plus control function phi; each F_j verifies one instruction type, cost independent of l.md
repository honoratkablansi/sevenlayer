---
source_file: "references/recursion/ch2/ref-44-supernova.pdf"
type: "paper"
community: "Community 46"
location: "§1.2 (computational model)"
tags:
  - graphify/paper
  - graphify/EXTRACTED
  - community/Community_46
---

# Per-instruction step functions {F_1,...,F_l} plus control function phi; each F_j verifies one instruction type, cost independent of l

## Connections
- [[Augmented function F'_j runs F_j then a verifier circuit folding u_i into U_ipc, checks public IO hash, and computes pc_{i+1} via phi]] - `assumes` [EXTRACTED]
- [[Control function phi takes (z_i, omega_i) and outputs program counter pc in {1,...,l} selecting which F_j to apply at each step]] - `conceptually_related_to` [EXTRACTED]
- [[Non-uniform IVC (NIVC) generalization of IVC where each step proves a relation chosen from a set, selected by a control function]] - `defines` [EXTRACTED]
- [[R1CS (Rank-1 Constraint Systems)]] - `assumes` [EXTRACTED]

#graphify/paper #graphify/EXTRACTED #community/Community_46