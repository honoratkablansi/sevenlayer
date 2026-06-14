# Concepts the Book Should Cover (But Doesn't) — Synthesis

*Synthesized from 7 parallel domain-expert analyses of the master knowledge graph (2,783 nodes) cross-checked against the manuscript (`proving-nothing.md`, grep-verified) and the planned recursion outline. Each source analysis is in `master-graph/proposals/01-07*.md`. ~93 raw proposals deduplicated and ranked below.*

**The headline finding (independently reported by 4 of 7 agents):** the book *names* the canonical ZK machinery thoroughly but rarely *builds* the foundational theory underneath it. The single highest-leverage additions are the interactive-proof / commitment foundations (sumcheck, IOP, GKR, MLE, the KZG/pairing construction, QAP, the grand-product argument, the AGM security model) — each is a high-degree graph hub tagged **absent** or fragmentary, and each is the load-bearing "why it works" beneath chapters that currently assert "it works."

---

## Tier 1 — Foundational theory the book assumes but never constructs (highest priority)

These are named repeatedly yet never explained as mechanisms. Strong graph signal + flagged by multiple agents.

| Concept | Status | Why it's the highest leverage | Where |
|---|---|---|---|
| **Sum-Check Protocol** (standalone) | fragmentary (degree 95, ref 29 — 4th-largest god node) | The backbone of Spartan, HyperNova, Jolt, SP1 Hypercube. Scattered across two chapters; needs one self-contained section: round structure, soundness bound, multilinear variant. | Ch 6, before the folding genealogy |
| **Interactive Oracle Proofs (IOP/PIOP model)** | absent (degree 20, ref 9) | The unifying frame: PLONK, Marlin, Spartan, Aurora, HyperNova are all polynomial-IOP + PCS compilations. Explains *why* they share verifier structure. | Ch 6, before "The Three Families" |
| **GKR protocol** (standalone) | absent (degree 33, ref 12) | Appears only as "LogUp-GKR" (used in SP1, Stwo) but the layer-by-layer sumcheck reduction is never shown. | Ch 5 or 6 |
| **Multilinear Extension (MLE)** | absent (degree 17, ref 11) | The polynomial representation under every sumcheck-based system. Readers can't see why multilinear (not univariate) polynomials are used. | Ch 6, boxed definition |
| **KZG construction** (commit/open/verify) | thin (degree 81, ref 10) | Named ~100× as a label; the 3-equation construction (commit g^p(τ), open a quotient, verify one pairing) is never shown — so the SRS ceremony loses its anchor. | Ch 2 §SRS and/or Ch 7 §KZG |
| **Bilinear pairing mechanics + embedding degree** | thin / absent | The most-used, least-explained primitive. Why e(aP,bQ)=e(P,Q)^ab, the Miller loop, and what makes BN254/BLS12-381 "pairing-friendly" (vs secp256k1). | Ch 7 §KZG |
| **QAP construction** (R1CS → divisibility check) | thin (degree 19, ref 6) | The algebraic step that explains Groth16's 192-byte proof and what the BCTV/Pinocchio counterfeiting bug subverted. Currently dismissed in one sentence. | Ch 5 §R1CS |
| **Grand-product & permutation argument** (accumulator Z) | absent (degree 11/8) | The mechanism behind PLONK copy constraints and Plookup. The book says wires must match but never how the proof ensures it. | Ch 5 §PLONKish |
| **Algebraic Group Model / non-falsifiable assumptions** | absent (degree 14, ref 5) | Groth16/PLONK/KZG are only provably secure in the AGM; Gentry-Wichs proves SNARGs can't come from falsifiable assumptions. The book's "1-of-N honesty ⇒ secure" picture is incomplete without it. | Ch 2 or Ch 7 §hardness assumptions |

---

## Tier 2 — Recursion & folding groundwork

The author's `recursion-outline.md` is exceptional (covers ~85-90% of the canon). Two distinct gaps remain:

**(a) Vocabulary the *existing 14 chapters* lack — readers will meet the recursion chapter cold.** Add short primer boxes now:
- **Recursive proof composition** — the single highest-signal absent concept overall (degree 81, ref 30). One roadmap paragraph in Ch 1.
- **IVC formal definition** (the two-independence-condition statement) — thin (degree 56, ref 18). Box in Ch 6.
- **Proof-Carrying Data (PCD)** — absent (degree 47, ref 14). 2-page primer before the recursion chapter lands.
- **Accumulation schemes** (defer-then-discharge; split vs atomic) — absent (degree 35, ref 8). Definition box in Ch 6 before Nova.
- **Cycles of elliptic curves** (the field-mismatch problem; MNT, Pasta) — absent (degree 40, ref 12). Field-mismatch explainer in Ch 6.
- **Recursion-vs-folding distinction** — absent. "Folding ≠ a SNARK; no standalone proof until final compression." The most common conceptual error in ZK pedagogy; the book folds 152× but never draws it.

**(b) Genuine gaps *beyond* the outline** (worth adding to the recursion chapter):
- **Neo** (lattice folding over small fields) — frontier PQ+small-field folding, not in the outline.
- **Reduction of Knowledge** — used implicitly in the soundness proofs but never named/defined.
- **Sangria** (Nova-style folding for PLONKish, not just R1CS) — missing from the family tree.
- **Bootstrapping↔IVC parallel** (Gentry's "circuit verifies itself" insight) — the intellectual-history link is undrawn.

---

## Tier 3 — Missing applications & cross-cutting (high real-world relevance, absent)

| Concept | Status | Why | Where |
|---|---|---|---|
| **Verifiable Computation / Delegation (GKR-based)** | absent (degree 27, **ref 16** — among the highest of any absent concept) | The formal grounding for ZK coprocessors and "prove SQL queries"; the Goldwasser-Kalai-Rothblum delegation model. | Ch 13 (coprocessors) |
| **Verifiable Delay Functions (VDFs)** | absent (degree 24; graph Community 7 = 49 nodes) | Wesolowski/Pietrzak; on-chain randomness beacons, time-lock crypto. A whole graph community with zero manuscript presence. | Ch 8 or 14 |
| **Proof of Solvency / Reserves** | absent (degree 12) | The post-FTX flagship ZK application; range proofs over aggregated balances. | Ch 9 or 13 |
| **zkTLS / DECO / web data provenance** | absent (degree 7; Community 11 = 42 nodes) | Prove facts from TLS sessions (bank balances, OAuth) → DeFi collateral, identity. | Ch 9 or 13 |
| **zkBridge / ZK light clients** | absent (degree 10) | Trust-minimized cross-chain via consensus proofs; bridges have lost >$2B. | Ch 8 or 13 |
| **Vulnerability taxonomy** (Chaliasos SoK: under/over-constrained, computation-constraint mismatch, …) | thin | The book serves auditors but never gives the systematic 5-class taxonomy or over-constrained (completeness) bugs. | Ch 8 |
| **Two-class Fiat-Shamir failure taxonomy** | thin | Distinguish transcript-incompleteness (Frozen Heart) from adaptive correlation-intractability attacks — explains *why* the ROM is needed. | Ch 8 |
| **Rollup pricing / DoS amplification attacks** | absent (Community 21) | Chaliasos 2025: blob-stuffing finality-delay attacks (1.45-2.73×) — the verification-data seesaw is itself an attack surface. | Ch 8 |
| **Media provenance / C2PA / image authentication** | absent (degree 10; Community 60) | Prove an image came from a specific camera with only permitted edits — deepfake-era provenance (VeriTAS). | Ch 13 |
| **ZK SBOM / supply-chain attestation** | absent (degree 8) | Prove dependency-tree compliance (EO 14028) without revealing the tree. | Ch 13 or 14 |
| **Proof of Personhood** (nullifier mechanism) | thin | World/Humanity at scale, but the nullifier-vs-biometric construction is never shown. | Ch 13 |
| **Real-time proving** (formal def + enshrined-proofs roadmap) | absent (degree 13, ref 8) | "Proof within one 12s L1 slot" — the threshold for Ethereum enshrined proofs. Used as a phrase, never defined. | Ch 8 or 11 |

---

## Tier 4 — Proof-system & arithmetization family members (named in tables, never explained)

Each appears as a name/row but lacks the paragraph that makes it legible:
- **Marlin** (holographic universal SNARK — Sonic→Marlin→PLONK lineage), **Spartan** (SPARK compiler / sparse-MLE PCS, the folding decider), **Aurora** (first efficient transparent IOP SNARK), **Gemini** (streaming/elastic multilinear-KZG — explains SP1's jagged PCS), **Sonic + updatable/universal SRS** (the property that makes PLONK-family trust work).
- **Polynomial commitments beyond the four families**: **Dory** (transparent *pairing-based* PCS — disproves "transparent ⇒ no pairings"), **Basefold** (FRI generalized to multilinear over any field), **Hyrax** (multilinear IPA, distinct from univariate Bulletproofs).
- **Arithmetization mechanics**: **Caulk/cq/Baloo** (KZG sublinear-prover lookups, parallel to Lasso), **Randomized AIR (RAPs)** (how LogUp embeds into AIR), **Multilinear AIR** (the hypercube alternative SP1 uses), **offline memory checking** (algebraic RAM — a dominant zkVM cost), **sparse/jagged PCS** (commit only occupied rows).
- **BCS transformation** (IOP → non-interactive argument via Merkle+Fiat-Shamir) — the theory that justifies the entire STARK-inside-SNARK pipeline.

---

## Tier 5 — Depth gaps in languages, compilers, primitives & setup

**Languages/compilers/witness (Ch 3-4):** ZoKrates (the first high-level ZK DSL — missing from the evolution narrative), Lurk (functional/recursive DSL), CirC (named once — the compiler-not-language thesis made concrete), refinement types / CODA (compile-time prevention of under-constrained bugs), **over-constrained circuits** (the completeness-side failure mode, entirely absent), MTZK / metamorphic compiler testing, non-deterministic hints (guess-and-check pattern), witness partitioning / segment-boundary continuations (zkVM parallelism correctness).

**Primitives / post-quantum (Ch 7):** Ring-LWE & the cyclotomic ring (why lattice schemes use R_q), ML-KEM/ML-DSA (what the FIPS 203/204 standards actually specify; transport-layer vs proof-layer migration), lattice functional commitments (Wee-Wu/BASIS — the route to succinct lattice SNARKs), LaBRADOR (commitments-to-commitments, the pre-folding ancestor), Poseidon2 vs Poseidon / Rescue, Binius / binary tower fields (4th small-field option), discrete-log assumption formalized (DLOG/CDH/q-SDH), BabyBear degree-4 extension (the 2-adicity reason).

**Trusted setup (Ch 2):** subversion ZK & SRS subversion attacks (the contribution *software* as attack vector), perpetual powers of tau (the ceremony most projects actually use), the MPC ceremony protocol structure (contribute→prove→destroy), the random-beacon finalization model (last-participant attack), simulation-extractability vs knowledge-soundness (Groth16 malleability), SRS degree bound (max circuit size), on-chain/coordinator-free ceremonies.

---

## Per-chapter rollup (where the work lands)

- **Ch 1 (intro):** recursive-composition roadmap pointer.
- **Ch 2 (setup):** KZG construction, AGM/non-falsifiable, updatable SRS, subversion ZK, MPC-ceremony structure, random beacon, perpetual powers of tau, sim-extractability, SRS degree bound.
- **Ch 3-4 (languages/witness):** ZoKrates, Lurk, CirC depth, CODA/refinement types, over-constrained circuits, MTZK, hints, witness partitioning.
- **Ch 5 (arithmetization):** QAP, grand-product/permutation argument, Caulk/cq, Randomized AIR, Multilinear AIR, offline memory checking, sparse/jagged PCS.
- **Ch 6 (proof systems):** sumcheck, IOP/PIOP, GKR, MLE, Marlin, Spartan, Aurora, Gemini, Dory, Basefold, Hyrax, BCS transformation; recursion groundwork (IVC def, PCD, accumulation, cycles, recursion-vs-folding).
- **Ch 7 (primitives):** pairing mechanics, embedding degree, Ring-LWE, ML-KEM/DSA, lattice functional commitments, LaBRADOR depth, Poseidon2/Rescue, Binius, discrete-log formalism.
- **Ch 8 (verification/security):** VDFs, vulnerability taxonomy, two-class FS taxonomy, rollup DoS attacks, zkBridge, real-time-proving definition.
- **Ch 9 / 13 (privacy/apps):** proof of solvency, zkTLS/DECO, media provenance/C2PA, SBOM, proof of personhood, verifiable computation/delegation, DPC bridge, BBS+/SD-JWT, ZKML quantization.
- **Recursion chapter:** Neo, reduction of knowledge, Sangria, bootstrapping↔IVC (the four beyond-outline gaps).

---

## Cross-theme dedup notes

Concepts independently surfaced by multiple agents (high-confidence signal): **AGM** (setup + primitives), **Dory** (setup + proof-systems), **KZG construction / pairing mechanics** (setup + primitives), **grand-product argument** (arithmetization + proof-systems), **Sonic / updatable SRS** (setup + proof-systems), **GKR / verifiable computation** (proof-systems + applications), **Fiat-Shamir / under-constrained taxonomy** (languages + applications). These merged entries are the most reliably-real gaps.
