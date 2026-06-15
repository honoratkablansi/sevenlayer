# "Proving Nothing" — Graph-Structure-Driven Outline

*Architect lens: **the knowledge graph's own topology is the curriculum.** Communities are candidate chapters; god-nodes are the backbone each chapter orbits; prerequisite edges set the reading order; the hierarchical-modular community structure dictates TOC nesting. Every chapter below cites the graph community/communities it crystallizes and the god-node(s) it is built to discharge.*

---

## 1. One-paragraph thesis

The master graph is not a flat bag of 3,000 concepts; it is a **hierarchical-modular network** whose 145 communities cluster into a handful of super-modules, bridged by a small set of very-high-degree god-nodes (SNARK, PCS, ZKP, Groth16, Folding, Sum-Check, Fiat-Shamir, KZG, Trusted Setup, R1CS). Read topologically, the graph tells you exactly how to teach the subject: a **dependency DAG** runs from the interactive-proof / commitment foundations (Communities 7, 22, 33, 80, 47, 23, 21, 8) *up through* arithmetization and the SNARK families (5, 11, 34, 20, 9) *up through* recursion and folding (5, 24, 39, 18, 37) *up through* primitives (4, 90, 16, 10, 14, 2) *out to* systems and applications (19, 29, 0, 3, 53, 15, 26, 27, 6). My design **keeps the seven-layer trust-decomposition thesis as the spine of the practitioner's journey** — but it inserts, *before* that journey, a new **foundations part** that builds the theory the current book only names. The result: the graph's centrality structure picks the backbone (the proof core = Layers 4/5/6 = the densest god-node cluster), its prerequisite edges pick the order (theory → spine → frontier), and its community structure picks the chapters. Five parts, 22 chapters. Feynman rule enforced throughout: every chapter opens with an analogy hook that *is* the picture, then locks down the formal payload the god-node demands; concepts spiral (introduced as a picture early, revisited at full rigor when the graph says the prerequisites are in place).

**Mapping legend.** Each chapter header carries `[Cxx · god-nodes]` — the graph community/communities it crystallizes and the backbone concepts it discharges. "Hook" = Feynman intuition opener. "Payload" = the formal content locked down. New-vs-current notes mark what the 14-chapter book lacked.

---

## 2. The full outline

### How the parts map to the graph's super-modules

| Part | Graph super-module (communities) | Backbone god-nodes | Role in the DAG |
|---|---|---|---|
| **I — The Phenomenon** | 22, 7, 33, 80 | ZKP, Interactive Proof, Soundness, Sigma | Roots of the DAG: what a proof *is* |
| **II — The Engine Room (Foundations)** | 47, 23, 21, 8, 2, 34, 4, 90 | Sum-Check, PCS, KZG, MLE, GKR, IOP, QAP | The "why it works" layer the book never built |
| **III — The Seven Layers (the spine)** | 4, 3, 1, 11, 5, 9, 16, 10, 14, 6, 53 | Trusted Setup, R1CS, PLONK, Groth16, STARK, Lattice, Fiat-Shamir | The book's signature trust-decomposition walk |
| **IV — Recursion & the Frontier** | 5, 24, 39, 18, 37, 0, 19, 29 | Folding, Nova, IVC, PCD, Recursive Composition, zkVM, SP1 | Composing proofs; the performance race |
| **V — Systems, Applications, Verdict** | 3, 15, 26, 27, 6, 53, 56, 87, 92 | Midnight, ZK Rollup, MPC, Verifiable Computation | Where the math meets the world |

The five-part shape **is** the graph's coarse partition: a root cluster (what a proof is), the dense theory core, the seven-layer engineering spine, the recursion/systems super-module, and the applications periphery. Reading order follows the topological sort of these super-modules.

---

## PART I — THE PHENOMENON
*Graph roots: Communities **C22** (Zero-Knowledge Proof, Simulator, Knowledge Extractor), **C7** (Interactive Proof, Soundness, Completeness, NP), **C33** (Knowledge-Soundness, Prover, Verifier, Merkle, PCP), **C80** (Sigma protocol, Commitment Scheme, Schnorr, Special Soundness). These are the in-degree roots of the dependency DAG: everything points back here.*

### Chapter 1 — The Promise of Provable Secrets `[C22 · Zero-Knowledge Proof (deg 117); Recursive Composition roadmap pointer (deg 83)]`
- **Hook:** The bouncer who lets you in without seeing your ID; the cave with two passages and one door (Quisquati's Ali Baba). You convince without revealing.
- **Payload:** The three properties named precisely (completeness, soundness, zero-knowledge) as *promises*, not yet theorems. The seven-layer thesis stated as the book's spine — trust is **decomposed**, not eliminated. A one-paragraph roadmap pointer to recursion (the single highest-signal absent concept) so Part IV does not land cold.
- **Sections:** The Trick · The Seven Layers at a Glance · How to Read This Book (the DAG, not the floors).
- *Carries the existing Ch 1, but now explicitly seeds the foundations part.*

### Chapter 2 — Interactive Proofs: The Game That Cannot Be Faked `[C7 · Interactive Proof (deg 47), Soundness (27), Completeness (13), NP; C33 · Prover/Verifier]`
- **Hook:** Two colorblind friends and a red and green ball — how a skeptic forces an honest answer out of pure interaction. The graph-isomorphism / non-isomorphism game.
- **Payload:** **The interactive-proof model built from scratch** (absent in the current book despite degree-47 hub): prover–verifier protocols, the IP class, soundness as a *probabilistic* guarantee, public vs private coins, Freivalds' algorithm as the cleanest "verify faster than compute" example, argument systems (sound only vs bounded provers). This is the formal root the rest of the book reduces to.
- **Sections:** Why Randomness Beats a Liar · Freivalds and the Matrix-Multiply Check · From Proofs to Arguments (computational soundness).
- **NEW vs current book.** Discharges the absent god-nodes *Interactive Proof, Soundness, NP, Argument System*.

### Chapter 3 — Commitments, Sigma Protocols, and the Zero-Knowledge Property `[C80 · Sigma protocol, Commitment Scheme, Schnorr, Special Soundness; C22 · Simulator, Knowledge Extractor, Proof of Knowledge]`
- **Hook:** A sealed envelope you can't change but can later open (commitment); the three-coloring map you prove valid one edge at a time without revealing a single color.
- **Payload:** Commitment schemes (hiding/binding) as the universal primitive; Sigma protocols (3-move public-coin); the **simulation paradigm** made rigorous — zero-knowledge = "a simulator with no witness produces the same transcript"; knowledge extractor and proof-of-knowledge; special soundness; computational vs statistical vs perfect ZK.
- **Sections:** The Envelope (commitments) · Schnorr and the Sigma Template · The Simulator That Knows Nothing · Three Flavors of Zero-Knowledge.
- **NEW vs current book.** Discharges absent *Commitment Scheme, Sigma protocol*; builds the *Simulator / Knowledge Extractor* the current book only gestures at.

---

## PART II — THE ENGINE ROOM
*The theory the current manuscript names but never constructs. Graph super-module: **C47** (MLE, finite fields, Lagrange interpolation, LDE, doubly-efficient IP), **C23** (Sum-Check, grand-product, vanishing poly, HyperPlonk, ZeroTest), **C21** (GKR, arithmetic circuit, wiring predicate, Libra, linear-time prover), **C8** (PCS, IOP, PIOP, Marlin, Gemini), **C2** (random oracle, correlation intractability, preprocessing SNARG), **C34** (QAP, LIP, generic group model), **C4** (KZG, SRS, powers of tau), **C90** (bilinear pairing, IPA, Dory), **C74** (Reed-Solomon, Ligero, Brakedown).*

*This is the densest god-node cluster in the graph — Sum-Check (115), PCS (123), KZG (96), GKR (50), IOP (37), MLE (35) — and the one the gap analysis flags hardest. It is placed second because the topological sort demands it: every SNARK family in Part III is a PIOP + PCS compilation, and you cannot teach the compilation before its two inputs.*

### Chapter 4 — Polynomials Are Fingerprints `[C47 · Multilinear Extension (deg 35), Finite Field Arithmetic, Lagrange Interpolation, LDE; Schwartz-Zippel]`
- **Hook:** Two enormous documents; instead of comparing them line by line, evaluate each at one random point and compare a single number. If they differ anywhere, they almost surely differ there. That is the whole magic.
- **Payload:** Finite-field arithmetic; univariate Lagrange interpolation; **the Schwartz–Zippel lemma** as the engine of all soundness; low-degree extension; and the crucial pedagogical pivot — **why multilinear extensions (MLE) over the Boolean hypercube**, not univariate polynomials, underlie every sumcheck system. Reed–Solomon fingerprinting.
- **Sections:** The Random-Point Trick (Schwartz–Zippel) · Interpolation and the LDE · Univariate vs Multilinear (and why the hypercube wins).
- **NEW.** Discharges absent *MLE, Schwartz-Zippel (deepened), Lagrange interpolation, LDE, Boolean hypercube*.

### Chapter 5 — The Sum-Check Protocol `[C23 · Sum-Check (deg 115, 4th god-node), Grand Product, Vanishing Poly, #SAT IP; C21 · doubly-efficient IP]`
- **Hook:** You claim a giant spreadsheet's cells sum to a number. Rather than re-add millions of cells, the verifier plays a 1-round-per-variable guessing game that collapses the whole sum to a single random evaluation.
- **Payload:** **Sum-check built in full, standalone** (degree-115 hub, currently scattered/absent): round structure, the soundness bound `(d·v)/|F|`, completeness, the multilinear variant, and why it is *the* reduction beneath Spartan, HyperNova, Jolt, SP1, GKR. The grand-product argument (accumulator polynomial Z) and `#SAT` as the canonical application.
- **Sections:** The Spreadsheet Game · Round-by-Round Soundness · Why Sum-Check Is Everywhere (the dependency fan-out).
- **NEW (Tier-1).** Discharges the single highest-leverage absent theory god-node.

### Chapter 6 — Circuits, Layers, and the GKR Protocol `[C21 · GKR (deg 50), Arithmetic Circuit, Layered Circuit, Wiring Predicate, Libra, Linear-Time Prover, CMT]`
- **Hook:** A factory assembly line where you don't inspect every station — you check that each layer's output is consistent with the layer below, propagating one spot-check from the top down to the inputs.
- **Payload:** Arithmetic circuits and the layered model; **GKR's layer-by-layer sumcheck reduction** (the prover need not commit to the full trace); wiring predicates (add_i / mult_i); the CMT protocol; Libra's linear-time prover; doubly-efficient interactive proofs (super-efficient verifier). This is *verifiable delegation of computation* in its purest form.
- **Sections:** The Layered Circuit · Reducing Layer to Layer by Sum-Check · The Verifier That Outruns the Computation.
- **NEW (Tier-1).** Discharges absent *GKR, layered/arithmetic circuit mechanics, wiring predicate, verifiable computation (theory side)*.

### Chapter 7 — Polynomial Commitments and the IOP Frame `[C8 · PCS (deg 123), IOP/PIOP, Marlin, Gemini; C74 · Reed-Solomon, Ligero, Brakedown; C2 · random oracle, preprocessing]`
- **Hook:** Lock a polynomial inside a vault (one short hash). Later, a stranger names any point; you open just that window and prove the value — without ever revealing the rest. A commitment to an *entire function*.
- **Payload:** The **polynomial commitment scheme abstraction** (commit / open / verify) and the four families *as an interface* (pairing-, FRI-, IPA-, lattice-based — instantiated later in Part III); **the Interactive Oracle Proof / Polynomial-IOP model** as the unifying frame: *every modern SNARK = a PIOP compiled with a PCS + Fiat-Shamir.* This single idea collapses PLONK, Marlin, Spartan, STARKs into one schema. BCS transformation (IOP → non-interactive via Merkle + FS). Code-based commitments (Ligero, Brakedown) as the linear-time route.
- **Sections:** The Function Vault (PCS interface) · The PIOP + PCS Recipe (the unifying schema) · Compiling to Non-Interactive (BCS / Fiat-Shamir).
- **NEW (Tier-1).** Discharges absent *IOP/PIOP, PCS-as-interface, BCS transformation, Reed-Solomon/code-based PCS*. This chapter is the conceptual keystone — it tells the reader that the zoo of Part III is one machine wearing different hats.

### Chapter 8 — Hardness, Hashes, and the Trust You Can't See `[C2 · random oracle, correlation intractability; C34 · generic/algebraic group model, QAP, LIP; C75 · discrete log assumption]`
- **Hook:** Every magic trick rests on a "you can't do this fast" assumption. Pull on the thread and ask: what *exactly* are we betting is impossible?
- **Payload:** The discrete-log / CDH / q-SDH assumptions formalized; collision-resistant hashes; the **random oracle model** and **correlation intractability** (the property the Fiat-Shamir attack circumvents); the **Algebraic Group Model** and why Groth16/PLONK/KZG are only provably secure there; Gentry–Wichs (SNARGs cannot come from falsifiable assumptions). The **QAP construction** (R1CS → divisibility test) introduced here as the algebraic bridge that explains Groth16's 192 bytes.
- **Sections:** Three Hard Problems · The Random Oracle and Why We Pretend · The AGM and the Limits of Provable Security · QAP: From Constraints to a Divisibility Check.
- **NEW (Tier-1).** Discharges absent *AGM, random oracle / correlation intractability, discrete-log formalism, QAP construction, LIP*.

---

## PART III — THE SEVEN LAYERS
*The book's signature spine — but now standing on Part II's foundations, so each layer can be locked down at full rigor. Communities: **C4** (setup), **C3/C1** (language/witness), **C11** (arithmetization), **C5/C9** (proof systems), **C16/C10/C14** (primitives), **C53** (verification). Backbone god-nodes per layer: Trusted Setup (95), R1CS (91), PLONK (88)/Groth16 (116)/STARK (83), Fiat-Shamir (105), Lattice (79).*

*Note on order: the spine is presented in **layer order (1→7)** for narrative clarity, but the chapter openers each flag the DAG's true dependency direction (primitive → proof system → arithmetization → language → setup), keeping faith with the book's "the dependencies do not follow the numbering" insight.*

### Chapter 9 — Layer 1: Building the Stage (Trusted Setup) `[C4 · Trusted Setup (deg 95), KZG (96), Powers of Tau, SRS, Universal vs Circuit-Specific; C2 · transparent setup]`
- **Hook:** 141,416 strangers each whisper one secret into a box and burn the paper; the box works if even *one* of them truly forgot. The Ethereum KZG Summoning.
- **Payload:** Now that Part II built KZG's commit/open/verify and the AGM, the SRS gets its anchor: **the KZG construction shown in full** (commit `g^{p(τ)}`, open a quotient, verify one pairing); powers of tau and the MPC ceremony structure (contribute → prove → destroy → random beacon); **updatable/universal SRS** (the property that makes PLONK-family trust work); subversion-ZK and SRS-subversion attacks; the transparent alternative; the 1-of-N model; the Frozen-Heart-class setup risks; sim-extractability vs knowledge-soundness (Groth16 malleability). The Capex/Opex and ADOPT frameworks retained.
- **Sections:** Two Ways to Build a Stage · KZG and the Ceremony That Anchors It · Updatable, Universal, Subvertible · The Quantum Shelf Life.
- *Extends current Ch 2; now backed by the KZG construction it previously lacked.*

### Chapter 10 — Layer 2: Writing the Script (Languages & Compilers) `[C3 · Compact, Noir, ZKIR; C94 · Circom, CirC, ZoKrates; C5 · R1CS front-end]`
- **Hook:** The same recipe written in four cookbooks; one forbidden typo (`=` for `<==`) and the cake looks perfect but poisons the guest. Tornado Cash's one-character soundness break.
- **Payload:** The four DSL philosophies (Compact, Noir, Leo, plus the synthesis); program → circuit compilation; **the under-constrained circuit failure mode** (67% of audited bugs) *and its mirror, over-constrained / completeness bugs* (currently absent); the compiler-not-language thesis (CirC); ZoKrates as the origin of the DSL lineage; refinement types / CODA for compile-time prevention; non-deterministic hints. Compact's disclosure analysis as the privacy-by-compilation case.
- **Sections:** Four Philosophies · The Dominant Failure Mode (under- and over-constraint) · Compilers, Not Languages · Privacy by Compilation (Compact).
- *Extends current Ch 3; adds over-constrained bugs, ZoKrates, CODA, hints.*

### Chapter 11 — Layer 3: The Secret Backstage (Witness Generation) `[C1 · Witness, Witness Generation, NTT, MSM, side-channel, offline memory checking]`
- **Hook:** The magician rehearses alone backstage; the rehearsal — not the performance — is the slow part, and the walls can still leak the secret (a stopwatch reads Zcash's hidden amounts).
- **Payload:** Execution traces; **witness generation as the underrated bottleneck**; why it resists parallelization; the memory wall and hardware ladder; MSM/NTT as the dominant kernels; side-channel attacks (Zcash timing, Poseidon cache-timing, EM); witness–constraint divergence; **offline / algebraic memory checking** (a dominant zkVM cost). Midnight's `disclose()` witness architecture.
- **Sections:** The Hidden Bottleneck · Why It Won't Parallelize · When the Walls Leak (side channels) · Memory Checking and the Witness as a Multi-Dimensional Problem.
- *Extends current Ch 4; adds offline memory checking, witness partitioning.*

### Chapter 12 — Layer 4: Encoding the Performance (Arithmetization) `[C11 · PLONK (deg 88), Lookup (65), AIR, PLONKish, Schwartz-Zippel, permutation/grand-product; C37 · CCS]`
- **Hook:** Turning a Sudoku into a spreadsheet of equations that hold *everywhere at once* — and a magic ledger (lookup) that checks "is this value in the allowed table?" without scanning the table.
- **Payload:** R1CS / AIR / PLONKish as three dialects; **the grand-product & permutation argument** (how PLONK's copy-constraints are actually enforced — currently asserted, never shown); **CCS as the Rosetta Stone**; the lookup-argument genealogy (Plookup → LogUp → LogUp-GKR → Lasso → Jolt) now grounded in the sum-check of Ch 5; Randomized AIR (RAPs), Multilinear AIR (SP1's hypercube), Caulk/cq (KZG lookups); the 10,000×–50,000× overhead tax dissected; sparse/jagged PCS.
- **Sections:** Three Dialects, One Grammar (R1CS/AIR/PLONKish + CCS) · The Permutation Argument That Pins the Wires · The Lookup Singularity · The Overhead Tax.
- *Extends current Ch 5; adds the grand-product/permutation construction, RAPs, multilinear AIR.*

### Chapter 13 — Layer 5: Sealing the Certificate (The SNARK Families) `[C20 · SNARK (deg 139, top god-node), Linear PCP, Pinocchio, GGPR; C9 · Groth16 (116), STARK (83), FFLONK; C8/C28 · Marlin, Spartan, Aurora]`
- **Hook:** Three envelopes for the same letter — one tiny and tamper-proof but needing a special wax seal (Groth16), one reusable (PLONK), one transparent but bulky (STARK). Same letter, three trust profiles.
- **Payload:** The unifying payoff of Part II cashed in: **the SNARK taxonomy as PIOP + PCS choices.** Groth16 (the linear-PCP/QAP lineage, 192 bytes, why the AGM); the PLONK/Marlin/Sonic universal-SRS family; STARKs (FRI-based, transparent); Spartan/Aurora (sumcheck + code/IOP). The hybrid STARK-to-SNARK pipeline (1,000 tx → 192 bytes). Why "succinct" spans 192 bytes and 200 KB.
- **Sections:** From PIOP+PCS to a Named SNARK · Groth16 and the QAP Lineage · The Universal-SRS Family (PLONK/Marlin) · STARKs and the Transparent Path · The Hybrid Pipeline.
- *Extends current Ch 6's family survey; now derived, not asserted. Discharges top god-node SNARK + Linear PCP/Pinocchio/GGPR lineage.*

### Chapter 14 — Layer 6: The Cryptographic Bedrock (Primitives) `[C90 · Bilinear Pairing (deg 47), IPA, Dory; C16 · cycles of curves, embedding degree, MNT; C10/C14 · Lattice (79), Module-SIS/LWE, Ajtai, cyclotomic ring; C0 · small fields]`
- **Hook:** The laws of physics under the stage; change the floor (the field, the curve, the hardness assumption) and every act above must be re-choreographed. A one-way door.
- **Payload:** **Pairing mechanics finally shown** — why `e(aP,bQ)=e(P,Q)^{ab}`, the Miller loop, embedding degree, what makes BN254/BLS12-381 pairing-friendly vs secp256k1; the four commitment families *instantiated* (KZG / FRI / IPA-Bulletproofs / Ajtai) against the trilemma; **lattice cryptography in depth** — Ring/Module-LWE, the cyclotomic ring `Z[X]/(X^d+1)`, Ajtai commitments, ML-KEM/ML-DSA standards, LaBRADOR; small fields (BabyBear/M31/Goldilocks) and the 2-adicity reason; the quantum shelf-life and the lattice race.
- **Sections:** Three Hard Worlds (DLOG / hash / lattice) · How Pairings Actually Work · The Four Commitment Families and the Trilemma · Small Fields and the Quantum Horizon.
- *Extends current Ch 7; adds pairing mechanics, embedding degree, Ring-LWE/cyclotomic depth, ML-KEM/DSA.*

### Chapter 15 — Layer 7: The Audience's Verdict (On-Chain Verification) `[C53 · ZK Rollup, optimistic, proof compression; C33 · verifier; security taxonomy; data availability]`
- **Hook:** Six layers of mathematics, and the seventh is a committee with a multisig. Beanstalk lost $182M in 13 seconds to a system that worked exactly as designed.
- **Payload:** On-chain verifier economics; the verification-data seesaw and DA marketplace; **the systematic vulnerability taxonomy** (Chaliasos 5-class: under/over-constrained, computation-constraint mismatch, …); **the two-class Fiat-Shamir failure taxonomy** (transcript-incompleteness/Frozen-Heart vs adaptive correlation-intractability) — now explicable because Ch 8 built the ROM; governance attacks (Beanstalk, Tornado, L2Beat stages); rollup pricing/DoS amplification attacks; proof aggregation as the missing layer.
- **Sections:** The Price of a Verdict · When the Transcript Lies (the FS taxonomy) · Governance: The Achilles Heel · Pricing Attacks and Aggregation.
- *Extends current Ch 8; adds the formal FS taxonomy and rollup DoS attacks.*

---

## PART IV — RECURSION & THE FRONTIER
*The graph's second-densest super-module, and the current book's thinnest. Communities: **C5** (Nova, recursion, HyperNova, CycleFold, ProtoStar), **C24** (recursive composition, aggregation, STARK-to-SNARK), **C39** (folding scheme, accumulation), **C18** (IVC, 2-cycle, high-integrity), **C37** (CCS, multi-folding, Neo), **C0/C29** (FRI, Circle STARKs, SP1, small-field zkVMs), **C19** (zkVM, RISC Zero, continuations). God-nodes: Folding (116), Sum-Check reused, Recursive Composition (83), IVC (62), Nova (68), zkVM (59), FRI (82), SP1 (47).*

### Chapter 16 — Recursion: Proofs That Verify Proofs `[C24 · Recursive Composition (deg 83), Proof Aggregation, STARK-to-SNARK; C17 · Fiat-Shamir (105), NIZK]`
- **Hook:** Russian dolls — a proof that contains, and checks, a smaller proof inside it. Verify the outermost doll and you've verified them all.
- **Payload:** **Recursive proof composition built explicitly** (highest-signal absent concept, degree 83): the verifier-in-a-circuit idea; **Fiat-Shamir** now in full (the non-interactive transform, why the ROM, transcript hygiene); proof aggregation and STARK-to-SNARK compression; the cycle-of-curves field-mismatch problem stated.
- **Sections:** The Verifier Inside the Circuit · Fiat-Shamir, Fully · Aggregation and Compression.
- **NEW (Tier-1/2).** Discharges absent *Recursive Composition*; relocates Fiat-Shamir to where its prerequisites (ROM, Ch 8) are ready.

### Chapter 17 — IVC, PCD, and Accumulation `[C18 · IVC (deg 62), 2-cycle, SNARK composition; C26 · PCD (47), distributed proof gen; C64 · Accumulation; C16 · cycles of curves, MNT, Pasta]`
- **Hook:** A pilgrim's logbook stamped at every town — each stamp certifies the whole journey so far, without re-walking it. Incrementally verifiable computation.
- **Payload:** **IVC formal definition** (the two-independence-condition statement); **Proof-Carrying Data** as the graph generalization (a 2-page-grown primer); **accumulation schemes** (defer-then-discharge; split vs atomic); **cycles of elliptic curves** (the field-mismatch fix: MNT, Pasta, 2-cycle BN254/Grumpkin); the bootstrapping↔IVC intellectual-history link (Gentry's "circuit verifies itself").
- **Sections:** The Stamped Logbook (IVC) · From IVC to PCD · Accumulation: Defer and Discharge · The Cycle-of-Curves Fix.
- **NEW (Tier-2).** Discharges absent *IVC (formal), PCD, accumulation schemes, cycles of curves*.

### Chapter 18 — Folding: The Snowball `[C39 · Folding Scheme (deg 116), accumulation; C5 · Nova (68), HyperNova, SuperNova, ProtoStar, ProtoGalaxy, CycleFold; C37 · CCS, multi-folding, Neo, Reduction of Knowledge]`
- **Hook:** A snowball rolling downhill — each step absorbs one more instance into a single growing object; only at the bottom do you pack it into one snowball (a SNARK). Folding ≠ a proof until the final compression.
- **Payload:** **The folding scheme built on Ch 5's sum-check**; the recursion-vs-folding distinction drawn explicitly (the most common ZK pedagogy error); the Nova family genealogy (Nova → SuperNova non-uniform IVC → HyperNova generalization → ProtoStar/ProtoGalaxy → CycleFold practical fix → Sangria for PLONKish); **Reduction of Knowledge** named; **Neo** (lattice folding over small fields) as the PQ+small-field frontier; multi-folding over CCS (SuperSpartan).
- **Sections:** Folding ≠ Proving (the key distinction) · The Nova Genealogy · CCS and Multi-Folding · Crossing into Post-Quantum (LatticeFold, Neo).
- *Extends current Ch 6's folding section into a full chapter; adds Sangria, Neo, Reduction of Knowledge, the recursion-vs-folding contrast.*

### Chapter 19 — zkVMs and the Real-Time Proving Race `[C19 · zkVM (deg 59), RISC Zero, continuations; C0 · SP1 Hypercube, Circle STARKs, M31, Cairo; C29 · zkEVM, real-time proving, LogUp-GKR, jagged PCS; C9 · STARK, FRI]`
- **Hook:** A universal stage that proves *any* program — write ordinary RISC-V, get a proof for free. The dream of "just prove my code."
- **Payload:** The zkVM model (RISC-V convergence, continuations, receipts); FRI and Circle STARKs (the squaring map, 31-bit speed) as the transparent backbone; the proof-core triad (Layers 4/5/6 fused); **real-time proving formally defined** ("proof within one 12s L1 slot," the enshrined-proofs threshold); SP1 Hypercube / Stwo-Cairo / Jolt through the seven layers; the cost-collapse curve; offline memory checking and jagged PCS as the dominant costs.
- **Sections:** The Universal Stage · FRI, Circle STARKs, and Small-Field Speed · Three zkVMs Through Seven Layers · Real-Time Proving Defined.
- *Merges/extends current Ch 11; adds FRI/Circle-STARK construction, real-time-proving definition.*

---

## PART V — SYSTEMS, APPLICATIONS, AND THE VERDICT
*The graph's periphery — high real-world relevance, many nodes, currently thin. Communities: **C3** (Midnight, Poseidon, BLS12-381), **C15** (Zcash, Tornado, Privacy Pools, Bulletproofs), **C27** (MPC, TEE, FHE, eIDAS, GDPR, garbled circuits), **C26** (PCD, media provenance, C2PA), **C6** (vector commitments, SBOM, SLSA, transparency logs), **C53** (rollups, identity), **C56** (proof of solvency, Bitcoin reserves), **C87/C92** (zkBridge, verifiable computation, deVirgo).*

### Chapter 20 — Privacy-Enhancing Technologies in Composition `[C27 · MPC (deg 27), FHE, TEE, garbled circuits, eIDAS, GDPR; C15 · Zcash, Privacy Pools, Bulletproofs]`
- **Hook:** Four locks on one door — ZK, MPC, FHE, TEE — and why no single lock is enough; you compose them.
- **Payload:** The four PETs and their composition; three kinds of security (cryptographic/hardware/statistical); ZK ⊕ MPC collaborative proving; FHE + bootstrapping where it meets ZK; real deployments (SNB/Decentriq, Canton/DTCC, Privacy Pools); Kachina and Zexe architectures; the GDPR/eIDAS regulatory intersection.
- **Sections:** The Four Pillars · Composability · Real Deployments · The Regulatory Intersection.
- *Extends current Ch 9; sharpens the ZK/MPC/FHE/TEE boundaries.*

### Chapter 21 — The Application Atlas `[C92 · Verifiable Computation (deg 27); C56 · proof of solvency, Bitcoin reserves; C26 · media provenance, C2PA; C6 · SBOM, transparency logs; C87 · zkBridge; C53 · rollups, identity; ZKML; proof of personhood]`
- **Hook:** Once you can prove a computation without revealing it, the same machine sells a dozen products — a coprocessor, a bridge, a solvency attestation, a camera that proves its photo is real.
- **Payload:** **Verifiable computation / delegation** (the Goldwasser–Kalai–Rothblum grounding — the formal home for ZK coprocessors, "prove this SQL query"); ZK rollups and coprocessors; **proof of solvency/reserves** (the post-FTX flagship; range proofs over balances); **zkTLS/DECO** web-data provenance; **zkBridge / ZK light clients**; **media provenance / C2PA / image authentication** (deepfake-era, VeriTAS); **ZK SBOM / supply-chain attestation**; **proof of personhood** (the nullifier construction); **ZKML** (quantization, the prove-the-inference problem); VDFs (Wesolowski/Pietrzak — a whole graph community with zero current presence) for on-chain randomness; the prover market / proving-as-a-service.
- **Sections:** Verifiable Computation as the Master Pattern · On-Chain (rollups, coprocessors, bridges) · Off-Chain Trust (solvency, zkTLS, provenance, SBOM, personhood) · ZKML, VDFs, and the Prover Market.
- **NEW (Tier-3).** Gives homes to the absent application god-nodes: verifiable computation, proof of solvency, zkTLS, zkBridge, media provenance, SBOM, proof of personhood, VDF.

### Chapter 22 — Midnight, the Synthesis, and the Road Ahead `[C3 · Midnight (deg 79), Compact, Poseidon, BLS12-381, ZKIR; C9 · trust-minimization; Three-Path map]`
- **Hook:** One real system, walked top to bottom through all seven layers — the book's thesis made concrete — and then the honest redrawing: not seven tidy floors but a directed acyclic graph with fourteen causal edges.
- **Payload:** **Midnight as the end-to-end case study** (all seven layers in one stack: BLS12-381 ceremony → Compact → `disclose()` → ZKIR → Halo 2 four-phase → Jubjub/Poseidon → three-token verifier lifecycle); where it validates and where it challenges the model; the **trust-decomposition synthesis** (seven weaker assumptions; the cascade structure; "trustless" vs "trust-minimized"); the causal-DAG redrawing; the three frontiers (performance largely crossed; security active; privacy approaching); the seven open questions; "is seven the right number of layers?"
- **Sections:** Midnight Through Seven Layers · Three Paths, Not Two (the DAG synthesis) · Trustless vs Trust-Minimized · Open Questions and the Three Frontiers.
- *Merges current Ch 10 (Synthesis), Ch 12 (Midnight), and Ch 14 (Open Questions) into one capstone — Midnight migrates from running example to closing case study; the synthesis becomes the payoff of all five parts.*

---

## 3. Reading-order rationale (the topological sort)

The order is the **dependency DAG of the graph's super-modules**, not the seven-layer numbering:

1. **Part I (roots).** Communities C22/C7/C33/C80 are the in-degree roots — every later concept reduces to "an interactive proof with the ZK property." You cannot define a SNARK before you've defined a proof, soundness, and the simulator. Teaching these first means every later "it's sound" has a referent.
2. **Part II (theory core) before Part III (the spine).** This is the design's central move and it is **forced by the edges**: in the graph, PLONK, Marlin, Spartan, STARK, Groth16 all have prerequisite edges into Sum-Check (C23), PCS/IOP (C8), MLE (C47), GKR (C21), QAP (C34), pairings/AGM (C90/C34). A PIOP+PCS is the *definition* of a modern SNARK; you must build both inputs before the compilation. The current book teaches the spine without these inputs, which is why the gap analysis flags Tier-1 theory as "named but never built." Putting Part II second repays that debt and lets Part III be *derived* rather than asserted.
3. **Part III (the spine).** With the engine room built, the seven layers can each be locked down at full rigor — the setup chapter finally shows the KZG construction, arithmetization finally shows the permutation argument, the proof-system chapter finally *derives* the families from PIOP+PCS. The spine is presented 1→7 for narrative momentum but each opener flags the true DAG direction (primitive ⇒ proof system ⇒ arithmetization ⇒ language ⇒ setup), honoring the book's own "the dependencies don't follow the numbering" thesis.
4. **Part IV (recursion) after the spine.** Folding/IVC/PCD have prerequisite edges into sum-check (C23, built in Ch 5), accumulation, and cycles of curves — all of which need Parts II–III first. Recursion is *composition over* the objects Part III built. Fiat-Shamir is deliberately deepened here (Ch 16) where its ROM prerequisite (Ch 8) is in hand, rather than asserted early.
5. **Part V (applications) last.** The periphery communities (C92/C56/C26/C6/C87/C27) are the out-degree leaves: they consume everything above. Midnight, which threaded through the whole book as the running example, graduates to the closing capstone where every layer it touches has already been built.

**Spiral principle (Feynman):** high-degree god-nodes appear *twice* by design — once as a picture early, once at rigor when prerequisites land. Fiat-Shamir: pictured in Ch 1/named in Ch 8 (ROM)/built in Ch 16. KZG: interface in Ch 7/constructed in Ch 9. Sum-check: motivates Ch 4, built in Ch 5, reused in Ch 6/12/18. Recursion: roadmap pointer in Ch 1, built in Ch 16. This is the graph's centrality structure dictating where to revisit.

---

## 4. What's new vs the current 14-chapter book

**Structural change:** 14 → 22 chapters; 3 → 5 parts. The biggest move is the new **Part II "Engine Room"** (5 chapters, 4–8) that builds the theory the current book only names. The seven-layer spine is preserved intact as Part III. Recursion/folding is promoted from one section of old Ch 6 into a full Part IV (4 chapters). The old Synthesis + Midnight + Open-Questions chapters fuse into a single Part V capstone.

**High-signal absent/under-covered concepts and their new homes:**

| Concept (graph status) | New home |
|---|---|
| Sum-Check Protocol (deg 115, absent) | **Ch 5** (own chapter) |
| Interactive Proof / Soundness / NP (deg 47, absent) | **Ch 2** |
| Commitment Scheme / Sigma / Simulator (absent) | **Ch 3** |
| Multilinear Extension / Schwartz-Zippel / LDE (absent) | **Ch 4** |
| GKR / layered circuit / wiring predicate (deg 50, absent) | **Ch 6** |
| IOP/PIOP, PCS-as-interface, BCS, Reed-Solomon (absent) | **Ch 7** |
| AGM, random oracle, QAP, discrete-log formalism (absent) | **Ch 8** |
| KZG construction, updatable SRS, subversion-ZK (thin) | **Ch 9** |
| Over-constrained circuits, ZoKrates, CODA, hints (absent) | **Ch 10** |
| Offline memory checking (under-covered) | **Ch 11** |
| Grand-product/permutation argument, RAPs, multilinear AIR (absent) | **Ch 12** |
| Linear PCP / Pinocchio / GGPR lineage; SNARK derived (under) | **Ch 13** |
| Pairing mechanics, embedding degree, Ring-LWE, ML-KEM/DSA (absent) | **Ch 14** |
| FS two-class taxonomy, vulnerability 5-class taxonomy, rollup DoS (thin) | **Ch 15** |
| Recursive Proof Composition (deg 83, absent) | **Ch 16** |
| IVC (formal), PCD, accumulation, cycles of curves (absent) | **Ch 17** |
| Recursion-vs-folding, Sangria, Neo, Reduction of Knowledge (absent) | **Ch 18** |
| Real-time proving (formal), FRI/Circle-STARK construction (absent) | **Ch 19** |
| Verifiable computation/delegation, proof of solvency, zkTLS, zkBridge, media provenance/C2PA, SBOM, proof of personhood, VDF (absent) | **Ch 21** |

Running examples retained and re-used: the **4×4 Sudoku** now threads through Parts II–III (it becomes a circuit in Ch 6, a sum-check instance in Ch 5, 72 constraints + a permutation argument in Ch 12, a sealed SNARK in Ch 13); **Midnight** migrates from a recurring case study to the closing capstone (Ch 22).

---

## 5. Risks / tradeoffs

1. **Front-loaded theory may stall the lay reader.** Part II is the most mathematically dense stretch and it sits *second*, before the engaging seven-layer narrative. **Mitigation:** the Feynman rule is strictest here — every Part II chapter opens with a concrete picture (the random-point document comparison, the spreadsheet game, the function vault), and the Sudoku running example carries through so the abstraction always has a referent. A reader who wants the practitioner tour first can read Part I → Part III and treat Part II as a referenced appendix (the spine chapters cite back into it).
2. **Spiral revisits risk feeling repetitive.** Fiat-Shamir, KZG, and sum-check each appear 2–3 times. **Mitigation:** each revisit is at a strictly higher rigor tier and is explicitly labeled as the payoff of an earlier picture; the graph's centrality justifies the repetition (these are the highest-degree nodes — readers *will* meet them repeatedly in the literature regardless).
3. **22 chapters is long.** Risk of a 600+ page volume. **Mitigation:** the brief already chose "bigger, definitive single volume (theory + practice)"; the part structure lets readers self-route, and Part V's three-chapter fusion keeps the applications/synthesis tail tight rather than sprawling.
4. **Promoting recursion to its own part** front-runs some readers' interest but may over-weight a fast-moving research area whose specifics (Neo, Symphony, LatticeFold+) date quickly. **Mitigation:** Part IV is organized by the *stable* god-nodes (folding, IVC, PCD, recursive composition) with the volatile named systems as instances under them — the structure survives even as the leaves churn.
5. **The graph-driven mapping can over-fit to graph artifacts.** Community boundaries and degrees reflect the corpus's emphasis (heavy on Thaler + the MOOC + recursion), which may over-represent sum-check/folding relative to a general audience's needs and under-represent, say, UX or economics. **Mitigation:** Part V deliberately re-balances toward applications/economics/regulation, and the seven-layer spine (Part III) keeps the book anchored to the original trust-decomposition thesis rather than letting the graph's research bias fully dictate the narrative.
