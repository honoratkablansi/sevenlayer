# Graph Report - .  (2026-06-13)

## Corpus Check
- 412 files · ~99,999 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 412 nodes · 625 edges · 14 communities
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 17 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_ZK Foundations & Framing|ZK Foundations & Framing]]
- [[_COMMUNITY_Fiat-Shamir Security & Synthesis|Fiat-Shamir Security & Synthesis]]
- [[_COMMUNITY_Proof Systems & Trusted Setup|Proof Systems & Trusted Setup]]
- [[_COMMUNITY_Verification & Rollup Economics|Verification & Rollup Economics]]
- [[_COMMUNITY_Arithmetization & ZK Languages|Arithmetization & ZK Languages]]
- [[_COMMUNITY_Commitments & Cryptographic Hardness|Commitments & Cryptographic Hardness]]
- [[_COMMUNITY_Lookups & zkVM Arithmetic|Lookups & zkVM Arithmetic]]
- [[_COMMUNITY_Midnight & Private Contracts|Midnight & Private Contracts]]
- [[_COMMUNITY_Compilation & Witness Generation|Compilation & Witness Generation]]
- [[_COMMUNITY_Circuit Security & Constraint Systems|Circuit Security & Constraint Systems]]
- [[_COMMUNITY_Open Questions & Road Ahead|Open Questions & Road Ahead]]
- [[_COMMUNITY_Privacy-Enhancing Technologies|Privacy-Enhancing Technologies]]
- [[_COMMUNITY_Trusted Execution Environments|Trusted Execution Environments]]
- [[_COMMUNITY_Market Coprocessors & ZKML|Market: Coprocessors & ZKML]]

## God Nodes (most connected - your core abstractions)
1. `Groth16` - 25 edges
2. `Midnight (Privacy Blockchain)` - 18 edges
3. `STARK` - 16 edges
4. `Trusted Setup Ceremony` - 15 edges
5. `ZK Rollup` - 13 edges
6. `KZG Polynomial Commitment` - 13 edges
7. `BLS12-381 Curve` - 12 edges
8. `Folding Scheme` - 12 edges
9. `FRI Commitment Scheme` - 11 edges
10. `Fiat-Shamir Transform` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Groth16` --compares--> `Post-Quantum Security`  [INFERRED]
  proving-nothing.md → proving-nothing.md  _Bridges community 1 → community 5_
- `BLS12-381 Curve` --conceptually_related_to--> `Polynomial Commitment Scheme`  [INFERRED]
  proving-nothing.md → proving-nothing.md  _Bridges community 1 → community 7_
- `Goldilocks Field` --conceptually_related_to--> `Circle STARKs`  [INFERRED]
  proving-nothing.md → proving-nothing.md  _Bridges community 0 → community 4_
- `BN254 (alt_bn128) Curve` --references--> `Zcash Sapling Ceremony (2018, BGM17 MMORPG)`  [INFERRED]
  proving-nothing.md → proving-nothing.md  _Bridges community 4 → community 1_
- `Cairo (StarkWare ZK-native ISA)` --conceptually_related_to--> `Offline Memory Checking`  [INFERRED]
  proving-nothing.md → proving-nothing.md  _Bridges community 7 → community 4_

## Import Cycles
- None detected.

## Communities (14 total, 0 thin omitted)

### Community 9 - "ZK Foundations & Framing"
Cohesion: 0.12
Nodes (20): Zero-Knowledge Proof, Completeness, Soundness, Knowledge-Soundness, Interactive Proof System, Prover and Verifier, Selective Disclosure, Stage Magic Metaphor (Magician/Audience) (+12 more)

### Community 12 - "Fiat-Shamir Security & Synthesis"
Cohesion: 0.15
Nodes (17): Fiat-Shamir Transform, Fiat & Shamir, Crypto '86 (LNCS 263), Frozen Heart / Fiat-Shamir Vulnerability Class, Frozen Heart Vulnerability (2022), Last Challenge Attack (2024), Solana ZK ElGamal Bug (2025), Three Paths, Not Two (Synthesis), Seven-Layer Causal Web (DAG, 14 edges) (+9 more)

### Community 1 - "Proof Systems & Trusted Setup"
Cohesion: 0.07
Nodes (45): SNARK (Succinct Non-interactive ARgument of Knowledge), STARK, Groth16, Quadratic Arithmetic Programs (QAP), BLS12-381 Curve, Trusted Setup Ceremony, Ethereum KZG Summoning of 2023 (141,416 participants), Gennaro, Gentry, Parno, Raykova — QAP (Eurocrypt 2013) (+37 more)

### Community 3 - "Verification & Rollup Economics"
Cohesion: 0.06
Nodes (38): ZK Rollup, eIDAS 2.0, Three Converging Forces (privacy, scaling, cost), Claim: Proving Cost Collapse $80 to $0.04 (2023-2025), Succinct SP1 Hypercube Prover, Layer 7 -- The Verdict, On-Chain Verifier, Proof Verification (+30 more)

### Community 7 - "Arithmetization & ZK Languages"
Cohesion: 0.10
Nodes (29): Arithmetization, Polynomial Commitment Scheme, The Seven-Layer ZK Stack Model, 4x4 Sudoku Running Example, Finite Field Arithmetic, Cairo (StarkWare ZK-native ISA), RISC-V zkVMs, zkEVM / EVM-Compatible Proving (+21 more)

### Community 0 - "Commitments & Cryptographic Hardness"
Cohesion: 0.06
Nodes (52): Goldilocks Field, Structured Reference String (SRS), KZG Polynomial Commitment, Bilinear Pairing, Elliptic Curve / Discrete Logarithm Problem, Arithmetic Circuit, Shor's Algorithm / Quantum Threat, Lattice-Based Cryptography (+44 more)

### Community 4 - "Lookups & zkVM Arithmetic"
Cohesion: 0.07
Nodes (38): Circle STARKs, BN254 (alt_bn128) Curve, Tower NFS Erosion of BN254 Security, zkVM, Lookup Argument, Plookup, LogUp, LogUp-GKR (+30 more)

### Community 8 - "Midnight & Private Contracts"
Cohesion: 0.09
Nodes (28): Midnight (Privacy Blockchain), Compact (Midnight/IOG DSL), Disclosure Analysis (Compact), ZKIR (Zero-Knowledge Intermediate Representation), Compact 26-Pass Nanopass Compilation Pipeline, Halo 2 / UltraPlonk, Midnight Three-Token Architecture (Night, Shielded, DUST), Private Smart Contracts (+20 more)

### Community 2 - "Compilation & Witness Generation"
Cohesion: 0.06
Nodes (42): Chapter 3: Choreographing the Act (Layer 2 - Language), Witness (private execution trace/inputs), Six-Step Developer Lifecycle (Write-Compile-Test-Prove-Deploy-Monitor), 4x4 Sudoku Proof (Running Example), Claim: The compiler, not the language, is the part that matters, Ozdemir, Brown, Wahby, CirC: Compiler Infrastructure for Proof Systems, IEEE S&P 2022, Gassmann et al., Evaluating Compiler Optimization Impacts on zkVM Performance, arXiv 2508.17518, Witness Generation (+34 more)

### Community 5 - "Circuit Security & Constraint Systems"
Cohesion: 0.08
Nodes (33): Under-Constrained Circuits, Circom, R1CS (Rank-1 Constraint Systems), Tornado Cash Under-Constraint Bug, Wen et al., ZKAP: Practical Security Analysis of ZK Proof Circuits, USENIX Security 2024, Pailoor et al., Picus/QED2: Automated Detection of Under-Constrained Circuits, PLDI 2023, Takahashi et al., zkFuzz: Fuzzing of Zero-Knowledge Circuits, IEEE S&P 2026, Xue et al., ZK-Coder: LLMs for ZK Proof Code Generation, arXiv 2509.11708 (+25 more)

### Community 11 - "Open Questions & Road Ahead"
Cohesion: 0.16
Nodes (18): Constant-Time Implementation, Open Questions and the Road Ahead (Ch14), Q3: When Will Stage 2 Bind, Q4: When Will Trustless Become Real, Q6: Practical Constant-Time ZK Proving, Q7: Is Seven the Right Number of Layers, The Three Frontiers (Performance, Security, Privacy), Zeno's Paradox of Trust (Conjunction Effect) (+10 more)

### Community 6 - "Privacy-Enhancing Technologies"
Cohesion: 0.08
Nodes (31): Chapter 9: Privacy-Enhancing Technologies, Privacy-Enhancing Technologies (PETs), Zero-Knowledge Proofs (ZKPs), Secure Multi-Party Computation (MPC), Fully Homomorphic Encryption (FHE), Differential Privacy (DP), Garbled Circuits, Oblivious Transfer (+23 more)

### Community 13 - "Trusted Execution Environments"
Cohesion: 0.67
Nodes (3): Trusted Execution Environment (TEE), Intel SGX, Heuristic Security

### Community 10 - "Market: Coprocessors & ZKML"
Cohesion: 0.12
Nodes (18): ZK Coprocessor, ZKML (Zero-Knowledge Machine Learning), Proving-as-a-Service, Tokenization of Assets, Trust Relocation vs Trust Minimization, Argument: Follow the Money, Watch the Trust, Axiom (ZK Coprocessor, $20M Series A), Brevis (Coprocessor + Pico Prism zkVM, ProverNet) (+10 more)

## Knowledge Gaps
- **121 isolated node(s):** `Stage Magic Metaphor (Magician/Audience)`, `Ethereum KZG Summoning of 2023 (141,416 participants)`, `Fiat & Shamir, Crypto '86 (LNCS 263)`, `Gennaro, Gentry, Parno, Raykova — QAP (Eurocrypt 2013)`, `Groth 2016 (ePrint 2016/260)` (+116 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Midnight (Privacy Blockchain)` connect `Midnight & Private Contracts` to `Verification & Rollup Economics`, `ZK Foundations & Framing`, `Open Questions & Road Ahead`, `Proof Systems & Trusted Setup`?**
  _High betweenness centrality (0.304) - this node is a cross-community bridge._
- **Why does `Groth16` connect `Proof Systems & Trusted Setup` to `Commitments & Cryptographic Hardness`, `Compilation & Witness Generation`, `Verification & Rollup Economics`, `Lookups & zkVM Arithmetic`, `Circuit Security & Constraint Systems`, `Fiat-Shamir Security & Synthesis`?**
  _High betweenness centrality (0.243) - this node is a cross-community bridge._
- **Why does `Selective Disclosure` connect `ZK Foundations & Framing` to `Midnight & Private Contracts`, `Verification & Rollup Economics`?**
  _High betweenness centrality (0.163) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Groth16` (e.g. with `CVE-2019-7167 BCTV14 Counterfeiting Bug` and `Post-Quantum Security`) actually correct?**
  _`Groth16` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Stage Magic Metaphor (Magician/Audience)`, `Ethereum KZG Summoning of 2023 (141,416 participants)`, `Fiat & Shamir, Crypto '86 (LNCS 263)` to the rest of the system?**
  _121 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ZK Foundations & Framing` be split into smaller, more focused modules?**
  _Cohesion score 0.11578947368421053 - nodes in this community are weakly interconnected._
- **Should `Fiat-Shamir Security & Synthesis` be split into smaller, more focused modules?**
  _Cohesion score 0.14705882352941177 - nodes in this community are weakly interconnected._