---
source_file: "references/recursion/ch2/ref-44-supernova.pdf"
type: "paper"
community: "Community 55"
location: "§4.1 (augmented function); §4.2"
tags:
  - graphify/paper
  - graphify/EXTRACTED
  - community/Community_55
---

# Augmented function F'_j: runs F_j then a verifier circuit folding u_i into U_i[pc], checks public IO hash, and computes pc_{i+1} via phi

## Connections
- [[Construction 1 SuperNova NIVC scheme (G,K,P,V) built from non-interactive folding scheme NIFS for committed relaxed R1CS plus a hash]] - `defines` [EXTRACTED]
- [[Multiple running instances, one per instruction type; incoming step instance folded into the running instance selected by pc (U_ipc)]] - `conceptually_related_to` [EXTRACTED]
- [[Optimization offlineMerkle memory-checking reduces F'_j circuit dependence on l from O(l) to O(log l) then to O(1) constraints]] - `conceptually_related_to` [EXTRACTED]
- [[Per-instruction step functions {F_1,...,F_l} plus control function phi; each F_j verifies one instruction type, cost independent of l]] - `assumes` [EXTRACTED]
- [[Program counter (pc) index selecting which instructionfunction is run at a step; computed by control function phi and threaded between augmented circuits]] - `assumes` [EXTRACTED]

#graphify/paper #graphify/EXTRACTED #community/Community_55