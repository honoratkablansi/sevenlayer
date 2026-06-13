---
source_file: "references/recursion/ch2/ref-44-supernova.pdf"
type: "paper"
community: "SuperNova Non-Uniform IVC"
location: "§1.2 (RAM machine); §4.2 (Construction 1)"
tags:
  - graphify/paper
  - graphify/EXTRACTED
  - community/SuperNova_Non-Uniform_IVC
---

# Program counter (pc): index selecting which instruction/function is run at a step; computed by control function phi and threaded between augmented circuits

## Connections
- [[Augmented function F'_j runs F_j then a verifier circuit folding u_i into U_ipc, checks public IO hash, and computes pc_{i+1} via phi]] - `assumes` [EXTRACTED]
- [[Control function phi takes (z_i, omega_i) and outputs program counter pc in {1,...,l} selecting which F_j to apply at each step]] - `defines` [EXTRACTED]
- [[Instantiations VDF machine (l=1, MinRoot) and RAM machine (RISC-V-like, program counter register, Merkle-committed memory)]] - `conceptually_related_to` [EXTRACTED]

#graphify/paper #graphify/EXTRACTED #community/SuperNova_Non-Uniform_IVC