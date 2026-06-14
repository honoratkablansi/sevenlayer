---
source_file: "references/ch10/ref-32-zkvm-compiler-optimization.pdf"
type: "paper"
community: "Community 19"
location: "§5.1, Table 2"
tags:
  - graphify/paper
  - graphify/EXTRACTED
  - community/Community_19
---

# Key cost components: dynamic instruction count and paging cycles (~1130 cycles/page-op)

## Connections
- [[Finding licm is most detrimental pass (+11.8% exec, +13.5% proving on RISC Zero; +444% paging on npb-lu)]] - `proves` [EXTRACTED]
- [[Four optimization principles (P1 paging-aware, P2 selective inlining, P3 instr-reducing unroll, P4 conservative branch elim)]] - `assumes` [EXTRACTED]
- [[Proving time (prover wall-clock cost metric)]] - `conceptually_related_to` [EXTRACTED]

#graphify/paper #graphify/EXTRACTED #community/Community_19