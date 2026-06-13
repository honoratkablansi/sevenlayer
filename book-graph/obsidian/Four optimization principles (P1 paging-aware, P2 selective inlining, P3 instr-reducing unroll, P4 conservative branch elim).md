---
source_file: "references/ch10/ref-32-zkvm-compiler-optimization.pdf"
type: "paper"
community: "zkVM Compiler Optimization"
location: "§5.2"
tags:
  - graphify/paper
  - graphify/EXTRACTED
  - community/zkVM_Compiler_Optimization
---

# Four optimization principles (P1 paging-aware, P2 selective inlining, P3 instr-reducing unroll, P4 conservative branch elim)

## Connections
- [[Key cost components dynamic instruction count and paging cycles (~1130 cyclespage-op)]] - `assumes` [EXTRACTED]
- [[zkVM-aware LLVM modifications (100 LOC cost model, heuristics, disabled passes); +45% RISC Zero, +4.6% avg]] - `assumes` [EXTRACTED]

#graphify/paper #graphify/EXTRACTED #community/zkVM_Compiler_Optimization