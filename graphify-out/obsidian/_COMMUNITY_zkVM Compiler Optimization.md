---
type: community
cohesion: 0.13
members: 20
---

# zkVM Compiler Optimization

**Cohesion:** 0.13 - loosely connected
**Members:** 20 nodes

## Members
- [[58-program benchmark suite (PolyBench, NPB, SPEC CPU 2017, a16z, Succinct, RSP, crypto)]] - paper - references/ch10/ref-32-zkvm-compiler-optimization.pdf
- [[BinTuner (Ren et al.) OpenTuner-based study of compiler-opt impact on binary diff]] - paper - references/ch10/ref-32-zkvm-compiler-optimization.pdf
- [[Cost-model mismatch zkVM uniform-cost constraints vs CPU hardware heuristics (cachebranch-predILP)]] - paper - references/ch10/ref-32-zkvm-compiler-optimization.pdf
- [[Finding -Ox gains (40%) on zkVMs far smaller than on traditional x86 CPUs]] - paper - references/ch10/ref-32-zkvm-compiler-optimization.pdf
- [[Finding inline is most beneficial pass (~22-30% gains, +28.4% RISC Zero exec)]] - paper - references/ch10/ref-32-zkvm-compiler-optimization.pdf
- [[Finding licm is most detrimental pass (+11.8% exec, +13.5% proving on RISC Zero; +444% paging on npb-lu)]] - paper - references/ch10/ref-32-zkvm-compiler-optimization.pdf
- [[Four optimization principles (P1 paging-aware, P2 selective inlining, P3 instr-reducing unroll, P4 conservative branch elim)]] - paper - references/ch10/ref-32-zkvm-compiler-optimization.pdf
- [[Genetic autotuning via OpenTuner (cycle-count fitness; up to 2.2x speedup over -O3)]] - paper - references/ch10/ref-32-zkvm-compiler-optimization.pdf
- [[Key cost components dynamic instruction count and paging cycles (~1130 cyclespage-op)]] - paper - references/ch10/ref-32-zkvm-compiler-optimization.pdf
- [[LLVM Compiler Infrastructure]] - paper - references/ch10/ref-32-zkvm-compiler-optimization.pdf
- [[Methodology 71 optimization profiles (64 LLVM passes, 6 -Ox levels, 1 baseline) x 2 zkVMs]] - paper - references/ch10/ref-32-zkvm-compiler-optimization.pdf
- [[Precompiles built-in circuits for hashingEC ops limiting autotuning crypto gains]] - paper - references/ch10/ref-32-zkvm-compiler-optimization.pdf
- [[Proving time (prover wall-clock cost metric)]] - paper - references/ch10/ref-32-zkvm-compiler-optimization.pdf
- [[RISC Zero zkVM (evaluated, v1.2.4)]] - paper - references/ch10/ref-32-zkvm-compiler-optimization.pdf
- [[SP1 zkVM (evaluated, v4.1.4)]] - paper - references/ch10/ref-32-zkvm-compiler-optimization.pdf
- [[Security-critical bug SP1 silently aborts mid-run yet proof verifies (false-correctness; reported and patched)]] - paper - references/ch10/ref-32-zkvm-compiler-optimization.pdf
- [[Superoptimization (e.g. Souper) for zkVM guest code]] - paper - references/ch10/ref-32-zkvm-compiler-optimization.pdf
- [[Surprising result strength reduction (div to shift-add) 3.5x faster on x86 but 40% slower proving on RISC Zero]] - paper - references/ch10/ref-32-zkvm-compiler-optimization.pdf
- [[Three zkVM metrics cycle count, executor time, proving time]] - paper - references/ch10/ref-32-zkvm-compiler-optimization.pdf
- [[zkVM-aware LLVM modifications (100 LOC cost model, heuristics, disabled passes); +45% RISC Zero, +4.6% avg]] - paper - references/ch10/ref-32-zkvm-compiler-optimization.pdf

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/zkVM_Compiler_Optimization
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_zkVM Design Philosophy]]
- 1 edge to [[_COMMUNITY_CirC Compiler Infrastructure]]

## Top bridge nodes
- [[LLVM Compiler Infrastructure]] - degree 6, connects to 2 communities
- [[Methodology 71 optimization profiles (64 LLVM passes, 6 -Ox levels, 1 baseline) x 2 zkVMs]] - degree 6, connects to 1 community
- [[RISC Zero zkVM (evaluated, v1.2.4)]] - degree 3, connects to 1 community
- [[SP1 zkVM (evaluated, v4.1.4)]] - degree 3, connects to 1 community
- [[Cost-model mismatch zkVM uniform-cost constraints vs CPU hardware heuristics (cachebranch-predILP)]] - degree 3, connects to 1 community