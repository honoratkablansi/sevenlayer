# Concepts Omitted From the Outline

*Appendix to the Chapter Bible for "Proving Nothing" (2nd ed.). Cross-references the approved 22-chapter outline (`docs/superpowers/specs/2026-06-14-book-outline-design.md`) against the candidate universe (`master-graph/CONCEPTS_FOR_BOOK.md`, ~1,107 concepts) and the community rollup (`master-graph/.outline/communities.md`).*

**Method.** A concept counts as **covered** if it appears in any chapter's GRAPH line, in a chapter PAYLOAD/HOOK, or in the Section-5 "homes" table — including when folded into a broader topic (e.g., "Halo2" covers the Halo2/UltraPlonk node; "Module-SIS/LWE" covers MLWE). Everything else is a **candidate omission**, sorted below into (a) high-signal omissions worth reconsidering, (b) deliberate scope exclusions, and (c) low-signal/niche/dated drops. Degrees and communities are quoted from CONCEPTS_FOR_BOOK; "absent/under-covered/well-covered" is that file's verdict vs the *current* (1st-ed) manuscript, not vs this outline.

**Bottom line up front.** The outline's coverage of the high-signal graph is excellent — essentially every god-node above degree ~40 has an explicit home, and the new Part III/IV chapters were clearly built by walking the absent-but-high-degree list. The omissions are concentrated in two places: (1) the **foundational interactive-ZK pedagogy cluster** (Sigma protocols, Schnorr, three-coloring/graph-isomorphism, quadratic-residuosity, proof-of-knowledge) which the outline assumes rather than teaches, and (2) a long tail of deliberate scope boundaries and low-degree leaf nodes. Only one cluster is a genuine "fell through the cracks" candidate; the rest are defensible.

---

## (a) High-signal omissions worth reconsidering

These have notable degree and/or reference support and received **no explicit home** in any GRAPH line, PAYLOAD, or the Section-5 table. Flagged in rough priority order.

### A1. The foundational interactive-ZK pedagogy cluster — *the one real gap*
**Concepts (community / degree / ref-support):**
- Sigma protocol (public-coin 3-move) — C80, deg 17, ref 9, *absent*
- Schnorr Proof System / Schnorr proof of knowledge — C80/C56, *absent*
- Three-Coloring Zero-Knowledge Proof — C80, *absent*
- Graph Isomorphism (GI) — C7, *absent*
- Quadratic Residuosity (QR) / Non-Residuosity — C22, deg 9, ref 4, *absent*
- Proof of Knowledge — C22, *absent*
- Special Soundness — C80, *absent*
- Computational Zero-Knowledge — C80, *absent*
- Commitment Scheme (generic) — C80, deg 17, ref 9, *absent*; Pedersen Commitment — C56, deg 39, ref 14, *under-covered*

**Graph signal:** Strong as a *cluster*. C80 ("Sigma / commitment / Schnorr / special-soundness") is an entire community with no chapter mapped to it; the generic Commitment Scheme node (deg 17, ref 9) and Pedersen (deg 39, ref 14) are high-reference-support and unhomed. These are the canonical textbook on-ramp to ZK (GMR 1985, the cave, the three-coloring proof, Schnorr).

**Rationale for the omission:** The outline opens at *succinctness* (Ch 1 jumps straight to SNARK/completeness/soundness/ZK as "three promises") and never installs the classic Sigma-protocol / proof-of-knowledge scaffolding. It was likely judged redundant with the magician metaphor — but Pedersen commitments in particular are *used* implicitly (Bulletproofs/IPA in Ch 11, accumulation in Ch 14) without ever being built.

**Recommendation:** Add a short **"classical interlude" inside Chapter 2** (or a boxed sidebar) covering the Sigma-protocol skeleton (commit–challenge–response), Schnorr as the worked example, special soundness, and the commit-as-sealed-envelope intuition — this is the historical bridge from GMR to Fiat-Shamir (Ch 12) and gives the commitment vocabulary the later chapters silently assume. Pedersen specifically should get one named paragraph in **Ch 11** alongside KZG/FRI/IPA (IPA *is* a Pedersen-vector argument). This is the highest-value addition on the list.

### A2. Discrete Logarithm Problem / Assumption (the hardness world, by name)
**Concepts:** Discrete Logarithm Assumption — C75, deg 24, ref 11, *absent*; Discrete Logarithm Problem — C66, deg 10, ref 4, *absent*; Elliptic Curve / DLP — C16, deg 8, *well-covered*.
**Graph signal:** deg 24 / ref 11 is high reference support for an unhomed node.
**Rationale for omission:** Ch 11 PAYLOAD names "the three hardness worlds — discrete-log (DLOG/CDH/q-SDH formalized)" — so DLOG *is* covered as a primitive. The high-degree standalone "Discrete Logarithm Assumption" node (C75) is arguably already discharged there; the only risk is that the C75/C66 nodes carry reference mass the outline doesn't visibly claim.
**Recommendation:** No new chapter needed — just confirm Ch 11 explicitly says "discrete-log assumption" as the named bet, and footnote q-SDH/CDH. Treat as covered; listed here only because the raw node is high-degree and could read as missed.

### A3. Plonky2 / Mina–Pickles / Halo (original accumulation)
**Concepts:** Plonky2 — C55, deg 8, *absent*; Mina (Coda) / Pickles — *absent* (Ch 1 gap list); Halo / Nested Amortization Recursion — C5, deg 14, ref 4, *under-covered*.
**Graph signal:** Individually modest (deg 8–14) but collectively a notable production lineage. Plonky2 (FRI-over-Goldilocks recursion) and Mina (the recursive-SNARK blockchain) are landmark named systems.
**Rationale for omission:** The outline derives families generically (Ch 10) and names the *Nova* folding genealogy (Ch 14) and the *Halo2* PCS (Ch 10/11/20), but the **original Halo accumulation idea** and **Plonky2/Mina** as the canonical IVC-in-production exemplars are not named. They likely lost their slots to SP1/RISC Zero/Jolt (chosen as the zkVM exemplars) and Nova (chosen as the folding exemplar).
**Recommendation:** Add Plonky2 + Mina/Pickles as **named examples in Ch 13** (Recursion/IVC/PCD) — Mina is the cleanest real-world IVC story and currently the chapter has no production recursion exemplar besides "where Midnight's recursion sits." Mention the original Halo accumulation in Ch 14 as the ancestor of the accumulation line.

### A4. Pure / classical interactive-proof complexity scaffolding
**Concepts:** Interactive Proof (IP) — C7, deg 47, ref 11, *absent*; Prover / Verifier (as named nodes) — C33, deg 15 each, ref 8, *absent*; NP — C7, deg 10, *absent*; Argument System — C7, *absent*; Succinct Argument — C33, deg 25, ref 12, *absent*; Knowledge-Soundness — C33, deg 29, *under-covered*.
**Graph signal:** IP at deg 47 / ref 11 is a genuine high-degree node; Succinct Argument deg 25 / ref 12 is high-support.
**Rationale for omission:** These are almost certainly *implicitly* covered — Ch 2 builds "the interactive-proof model at intuition depth," Ch 9 defines succinctness/knowledge-soundness/MIP/PCP, and prover/verifier are the magician/audience throughout. The nodes read as "absent" only because the 1st-ed manuscript under-named them. This is **covered in substance**; flagged because the high-degree IP and Succinct-Argument nodes deserve an explicit named definition (IP in Ch 2, Succinct Argument in Ch 9) rather than being left as ambient vocabulary.
**Recommendation:** No structural change; ensure Ch 2 and Ch 9 *name* "interactive proof," "argument system," and "succinct argument" as defined terms so the high-degree nodes are visibly claimed. Low effort, closes the appearance of a gap.

### A5. deVirgo / distributed & GPU-accelerated proving (beyond the witness kernel)
**Concepts:** deVirgo (distributed ZK over M machines) — C87, deg 12, *absent*; Distributed Proof Generation — C26, *absent*; SHARP / Universal Proof Aggregation (UPA) — C24, *absent*; ZKPOG (GPU witness accel) — C1, *(in Ch 5 GRAPH)*.
**Graph signal:** Moderate (deg ~12). The *prover-market / distributed-proving* theme spans C87, C26, C24.
**Rationale for omission:** Ch 5 covers the witness-generation hardware ladder and NTT/MSM kernels; Ch 17/19 mention proof aggregation and "the prover market." But **distributed/collaborative proof generation as an architecture** (deVirgo, SHARP, prover networks) is only glancingly present.
**Recommendation:** Fold deVirgo + distributed proving into **Ch 19** ("the prover market" already there) as one paragraph, or into Ch 5's hardware-ladder close. Low priority; the theme is touched, just not named.

### A6. Number-naming leaf concepts that are high-degree but ride along
For completeness, several high-degree nodes are *covered by their parent* and need no action, but are worth confirming the bible names them: **Mersenne-31/M31** (deg 25 — in Ch 11/15 GRAPH as "M31/small fields" ✔), **Ajtai commitments** (deg 27 — Ch 11/16 ✔), **CCS** (deg 49 — Ch 6/14 ✔), **Accumulation Schemes** (deg 36 — Ch 14 ✔), **Grand Product Argument** (deg 14 — Ch 9 ✔). All confirmed covered; listed so the author can see they were checked, not missed.

---

## (b) Deliberate scope exclusions

Whole areas the outline intentionally keeps out, touches only as a decision-matrix entry, or treats as "named, not built." State the boundary so it reads as a choice, not an oversight.

### B1. Other PETs treated only as a decision matrix — MPC / FHE / TEE / DP internals
**Concepts & communities:** Secure MPC (C27, deg 27), Fully Homomorphic Encryption (C91, deg 21), Bootstrapping/FHE (C25, deg 15, *absent*), Trusted Execution Environment (C27), Differential Privacy (C27), Garbled Circuits (C27).
**Boundary:** Ch 18 explicitly frames these as "the four PET pillars (ZK/MPC/FHE/TEE) + DP, as a decision matrix" and touches "FHE + bootstrapping where it meets ZK." **Internals are out of scope** — no MPC protocol mechanics, no FHE bootstrapping construction, no garbled-circuit gate tables, no TEE attestation internals. This is the correct boundary for a ZK book; state it in Ch 18's opening so the reader knows the omission is deliberate.

### B2. Classical / symmetric / signature cryptography internals
**Concepts:** Collision-Resistant Hash Functions (C120, *well-covered* as a primitive), Cryptographic Hash Function (C17), Number Field Sieve (C110, deg 10, *absent*), Knowledge-of-Exponent Assumption (C84, *absent*), ML-KEM/ML-DSA internals beyond naming.
**Boundary:** Hashes appear only *as primitives* (Poseidon in Ch 6/11, Merkle commitment in Ch 9). The book does **not** teach hash-function design, the Number Field Sieve (classical DLOG cryptanalysis), or KEM/signature scheme internals — ML-KEM/ML-DSA are named in Ch 16 as the NIST standards (FIPS 203/204) without construction. Correct boundary; NFS and KEA are safe drops (see also (c)).

### B3. Blockchain consensus, tokenomics, and L2 economics beyond verification
**Concepts:** Bitcoin (C56), Succinct blockchain (C18), Merkle Patricia Tree (C53), ZK-rollup *consensus/DA economics*, three-token architecture, prover-market microstructure.
**Boundary:** Ch 17 covers **on-chain verifier economics, DA seesaw, ZK-vs-optimistic, governance, rollup-DoS** — i.e., verification and its incentives — and Ch 20 covers Midnight's three-token model as a *case study*. The book does **not** cover consensus mechanics, full tokenomics, MEV, or L2 sequencing as topics in their own right. Bitcoin/Patricia-trie appear only as substrate. Reasonable; the seventh layer is "the audience's verdict," not a blockchain-design book.

### B4. Application verticals named-but-not-deep-dived
**Concepts (all in Ch 19 GRAPH/PAYLOAD):** zkBridge/light-client (C87), proof of solvency/reserves (C56), zkTLS/DECO (C17/applications), C2PA/media provenance/image authentication (C26/C89), proof of personhood (C97), ZKML (C79), SBOM/SLSA/supply-chain (C6), VDF (C12, Wesolowski/Pietrzak), range proofs (C75).
**Boundary:** These are **covered as a breadth survey in Ch 19** with maturity tiers — each gets a paragraph, none gets a chapter. That is the intended treatment ("what becomes possible at four cents"). The supply-chain/SBOM community (C6) and the verifiable-transparency-log line are the lightest-touch and could be cut to a single sentence if length forces it.

### B5. "Named, never built" SNARK lineage systems
**Concepts:** Marlin, Gemini, Sonic, Supersonic/DARK, Aurora, Spartan, Quarks/Xiphos/Kopis (C8/C20/C74/C28).
**Boundary:** The Section-5 table explicitly homes "Marlin / Spartan / Aurora / Gemini / Sonic lineage (named, never built) → Ch 9–10." They are deliberately mentioned as waypoints in the universal-SRS and sum-check-IOP lineages without full construction. Correct — building all of them would bloat Part III. The more obscure C8/C20 leaves (Quarks/Xiphos/Kopis, Progression-Free-Sets NIZK, AFGHO/Inner-Pairing-Product) are safe to leave unnamed (see (c)).

---

## (c) Low-signal / niche / dated concepts safely dropped

Brief list; each with a one-line reason. None of these warrant a home.

- **Number Field Sieve** (C110, deg 10) — classical DLOG cryptanalysis; out of a ZK book's scope.
- **Knowledge-of-Exponent Assumption** (C84, deg 5) — subsumed by AGM treatment in Ch 12; KEA is the older, clunkier framing.
- **Quadratic Residuosity / QNR** (C22, deg 9) — historical GM-encryption / first-ZK-proof artifact; pedagogically nice but covered in spirit by the three-promises framing. (Could ride along in the A1 interlude if added.)
- **Counting Triangles IP / Super-Efficient MatMult IP / CMT protocol** (C47/C71) — specific doubly-efficient-IP worked examples; Freivalds (Ch 7) and GKR/Libra (Ch 8) already carry that load.
- **Quarks / Xiphos / Kopis, Supersonic/DARK, Progression-Free-Sets NIZK, AFGHO / Inner-Pairing-Product, Signatures of Correct Computation** (C8/C20/C90) — deep PCS/IPP leaves; Dory + IPA in Ch 11 represent the family.
- **Pasta / 2-cycle (BN254/Grumpkin) / MNT as separate nodes** (C16/C18/C123) — all subsumed by Ch 11's "cycles of elliptic curves (MNT, Pasta, BN254/Grumpkin)" ✔ — listed only because they appear as separate high-ish-degree rows.
- **LLVM / Souper / superoptimization / Von Neumann architecture / Circuit Generator / Pantry / Verifiable State Machine** (C19/C92) — zkVM/compiler-infrastructure plumbing; Ch 15 covers the architecture without this tooling layer.
- **HyperPlonk, Plonky2 (as a node), Airbender, Orion, Stwo-as-node, ZeroTest, Vanishing Polynomial-as-node** — implementation/leaf nodes mostly subsumed by their families (Stwo/Circle-STARKs ✔ Ch 15; ZeroTest/grand-product ✔ Ch 9; Airbender is a recent zkVM, optional name-drop in Ch 15).
- **eIDAS 2.0 / GDPR as standalone rows** (C27) — covered in Ch 18's regulatory paragraph ✔; the *standalone* deg-13 eIDAS node is a citation artifact.
- **Verifiable transparency logs / Certificate Transparency / SLSA-as-node** (C6) — supply-chain leaves; one sentence in Ch 19 suffices.
- **MinRoot VDF, Repeated/sequential squaring, unknown-order groups** (C12) — VDF internals; Ch 19 names Wesolowski/Pietrzak, the rest is detail.
- **Mangrove, "Accessible exposition of Nova/folding," Home Proving, Realtime-Proving-Standardized-Definition** — these are *exposition/meta* nodes in C39/C28, not technical concepts; correctly ignored.
- **Sudoku running example (deg 14, "absent")** — flagged *absent* by the tool only because it is new apparatus; it is in fact the spine of the whole outline. False positive.

---

## Coverage summary

**The outline captures the high-signal graph very well.** Of the ~60 concepts above degree 40 (the "god-node" band), **essentially all have an explicit home** — the new Part III (Ch 7–12) and Part IV (Ch 13–16) were visibly engineered against the absent-but-high-degree list (Sum-Check 115, Folding 116, Recursion 83, KZG-construction 96, GKR 50, IVC 62, PCD 47, MLE 35, Cycles-of-curves 40, IOP 37, Accumulation 36 — all now homed). The Section-5 table is an honest, near-complete map of the formerly-absent high-degree nodes.

Rough capture rate:
- **Degree ≥ 40 (god-nodes):** ~98% homed. The only genuinely unhomed high-degree nodes are **Pedersen (39)** and the **generic Commitment Scheme (17, ref 9)** / **Sigma cluster** — i.e., gap **A1**.
- **Degree 15–40:** ~85% homed; the misses are A1 (Sigma/Schnorr/QR/proof-of-knowledge), the standalone DLOG-assumption node (A2, covered in substance), and the Plonky2/Mina lineage (A3).
- **Degree < 15:** long tail, mostly deliberate scope cuts (b) or leaf nodes subsumed by parents (c).

**Net assessment:** One cluster (A1 — foundational interactive-ZK / Sigma-protocol / commitment vocabulary) is a real candidate for reinstatement, ideally as a short Ch 2 interlude plus a named Pedersen paragraph in Ch 11; it is the only place where load-bearing vocabulary (commitments) is *used downstream but never built*. Everything else is either covered-in-substance (A2, A4, A6), a minor exemplar add (A3, A5), or a defensible scope boundary (b)/(c). The outline did **not** leave the high-signal graph with holes; it left the *classical on-ramp* implicit, which is a pedagogical choice worth revisiting given the book's Feynman-first promise.
