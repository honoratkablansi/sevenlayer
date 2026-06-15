# Outline Design — "Proving Nothing" (next iteration)
## Lens: Feynman intuition-first learning journey

---

## 1. One-paragraph thesis

The seven-layer trust-decomposition thesis is the **spine**; the **Feynman spiral is the gait**. I organize the whole book around a single repeated move: *meet every god-node concept first as a picture you can hold in your head, use that picture to do real work, then come back later and lock it down with the algebra.* Concretely, the book runs the seven layers **twice**. **Part I–II is the intuition lap**: the reader walks all seven layers using one unbroken running example (a 4×4 Sudoku) and a stable cast of physical analogies — a fingerprint, a sealed envelope, a die roll you can't redo, a snowball rolling downhill — and comes out the far side able to *narrate* how a ZK proof works end to end, with zero heavy mathematics. **Part III–IV is the rigor lap**: the same seven concepts are revisited at full mathematical depth — sum-check, MLE, the IOP-plus-commitment factorization, the KZG/pairing construction, QAP, the grand-product argument, folding and accumulation, the AGM security model — but now each one *clicks into a slot the reader already built*. Part V is the payoff: frontier systems (zkVMs, real-time Ethereum proving, post-quantum folding), the honest re-drawing of the seven floors as a dependency graph, applications, and open problems. The pedagogical claim is sharp: **a concept is first met where the analogy is cheapest, and locked down where the reader most needs the proof that the analogy was honest** — and those are deliberately *different chapters*. The intuition lap earns the reader the right to be surprised; the rigor lap pays off every surprise.

---

## 2. The full outline

**Five parts, 22 chapters.** Part I (3 ch) builds the three core properties + the whole seven-layer story as pictures. Part II (4 ch) walks the seven layers once, intuitively, on the Sudoku. Part III (6 ch) is the rigorous proof-systems core — the math the current book names but never builds. Part IV (4 ch) is recursion, primitives, and security at depth. Part V (5 ch) is frontier systems, the honest re-synthesis, applications, and the road ahead.

Legend for each chapter: **Hook** = the Feynman opening analogy/picture. **Payload** = the formal content that gets locked down (or, in the intuition lap, the picture that gets *installed* for later locking). **Graph** = the communities (C#) and god-nodes it draws from. **Spiral** = where this concept is met intuitively vs. where it is later made rigorous.

---

### PART I — THE INVITATION (intuition only; no formalism survives the part)

> Goal: by the end of Part I the reader can explain *what* a ZK proof promises, *why* trust is decomposed not deleted, and can picture all seven layers. No equations beyond `3x²+5x+7`.

#### Chapter 1 — Proving Without Showing
- **Hook:** The bouncer at the door. Six pieces of ID handed over to answer one yes/no bit ("are you 21?"). The whole book is the project of *sending the bit without the dossier.*
- **Payload (installed as pictures):** the three properties as three plain promises — *the honest always pass* (completeness), *the dishonest always fail* (soundness/knowledge-soundness), *nothing leaks* (zero-knowledge, via the simulator: "someone with no secret could have produced something that looks identical"). Prover/verifier as magician/audience. The 1985 GMR move: interaction + randomness substitute for disclosure.
- **Graph:** C22 (Zero-Knowledge Proof 117, Simulator, Knowledge Extractor, Proof of Knowledge), C7 (Interactive Proof 47, Soundness, Completeness, NP), C33 (Prover, Verifier, Knowledge-Soundness).
- **Spiral:** completeness/soundness/ZK are *met* here as promises; *locked* in Ch 9 (IP as a formal protocol) and Ch 11 (simulator/extractor definitions). Knowledge-soundness deferred to Ch 11.

#### Chapter 2 — Trust Is Not Deleted, It Is Decomposed
- **Hook:** A single load-bearing column vs. a truss. "Trustless" is marketing; the truss is the truth — one monolithic act of faith ("trust the bank") sawn into seven thin struts, each one independently testable and replaceable.
- **Payload:** the seven-layer thesis stated as the book's organizing claim (setup → language → witness → arithmetization → proof system → primitives → on-chain verifier); each layer = one trust assumption you can name, test, and swap. A first, honest warning that the layers are *organs, not floors* — dependencies will not follow the numbering (forward-pointer to Ch 17's DAG). The Sudoku puzzle and Midnight introduced as the two running examples (one in miniature, one in production).
- **Graph:** C9 (Trust Minimization — Not Trustless), the seven-layer spine across C4/C3/C1/C11/C33/C90/C53.
- **Spiral:** the seven layers are *named* here, *walked* in Part II, *re-derived as a causal DAG* in Ch 17. The "trustless is marketing" point is the thesis stated once in plain language and never softened.

#### Chapter 3 — Why It Took Twenty Years (and Then Two)
- **Hook:** A chess game played by mail (interactive proofs: both players online, round after round) vs. a sealed letter anyone can check later (non-interactive). The Fiat–Shamir move = "replace the human asking random questions with a hash that asks them for you."
- **Payload (pictures):** why interaction blocked deployment; Fiat–Shamir as *turning a conversation into a calculation* (full mechanism deferred to Ch 12); the succinctness miracle felt, not proved — 192 bytes certifying millions of steps ("smaller than a tweet"); the three converging forces (privacy crisis, scaling, cost collapse from \$80 → \$0.04) as the *why now*. Roadmap pointer: recursion/folding is coming ("proofs that verify proofs").
- **Graph:** C17 (Fiat-Shamir Transform 105, NIZK, CRS), C20 (SNARK 139), C9 (Groth16 116, STARK 83), C53 (ZK Rollup), god-node SNARK/Groth16/STARK at the *intuition* tier.
- **Spiral:** Fiat–Shamir *met* here as a slogan; *locked* in Ch 12 (random-oracle model, correlation intractability, the two-class failure taxonomy). Succinctness *felt* here; *defined* in Ch 9.

---

### PART II — THE SEVEN LAYERS, ONCE THROUGH (the intuition lap)

> Goal: walk all seven layers on the Sudoku end-to-end using only analogies. The reader finishes able to *narrate* a proof's life. Every concept here is deliberately under-formalized — each has a named rigor destination in Parts III–IV.

#### Chapter 4 — Layer 1: Building the Stage (Setup)
- **Hook:** A casino shuffling the deck *before anyone sits down*, in a sealed room — and then burning the room. The "toxic waste" you must trust someone destroyed.
- **Payload:** the structured reference string as shared public scaffolding; trusted ceremony vs. transparent setup as the first real fork; the **1-of-N honesty model** ("only one of 141,416 needs to have been honest"); Capex/Opex framing (pay once at setup vs. pay forever in proof size). KZG construction *named*, not built.
- **Graph:** C4 (Trusted Setup Ceremony 95, Powers of Tau, SRS, Universal vs Circuit-Specific), C2 (Transparent Setup), god-node KZG (96) as a label here.
- **Spiral:** the *ceremony* is locked here (it is genuinely a Part-II-grade idea); the **KZG construction and the AGM security model that make "1-of-N" a theorem** are deferred to Ch 10/Ch 13. This is the cleanest example of "met intuitively early, proven late."

#### Chapter 5 — Layers 2 & 3: The Script and the Backstage (Language + Witness)
- **Hook:** A recipe vs. the act of cooking. The *language* is the recipe (what you're allowed to write); the *witness* is the private cooking — you actually make the dish backstage, recording every step, and only the finished plate leaves the kitchen.
- **Payload:** programs → circuits (the front-end idea); the witness as the private execution trace; the dominant real-world failure mode made vivid — **under-constrained circuits** (`=` where `<==` was needed broke Tornado Cash); witness generation as the *underestimated* bottleneck; a first look at side channels ("the walls leak" — the Zcash stopwatch).
- **Graph:** C94 (Circom, DSL, Constraint Compiler), C1 (Witness, Witness Generation, Side-Channel, MSM), C72 (Under-Constrained Circuit), C19 (zkVM as a forward pointer).
- **Spiral:** under-constrained circuits *met* here as a bug story; the *completeness-side dual* (over-constrained) and the full 5-class vulnerability taxonomy locked in Ch 14. RISC-V/zkVM front-ends deferred to Ch 18.

#### Chapter 6 — Layer 4: Encoding the Performance (Arithmetization), the Picture
- **Hook:** A spreadsheet where every row must satisfy the same rule, and a magic property: *if you fill even one cell wrong, a randomly chosen checksum almost certainly catches it.* That "almost certainly" is the whole game.
- **Payload (pictures):** turning rules into polynomial equations (`3x²+5x+7`); the **Schwartz–Zippel intuition** stated as a slogan — "two different low-degree polynomials can agree in only a few places, so a random spot-check almost never lies"; the Sudoku becomes 72 constraints; R1CS / AIR / PLONKish introduced as *three dialects of one idea* (don't memorize, just feel the spread); the 10,000×–50,000× overhead tax named as a felt cost.
- **Graph:** C11 (Arithmetization, R1CS-as-label, AIR, PLONKish, Schwartz-Zippel, Lookup Argument 65), C23 (Vanishing Polynomial), C37 (CCS — the "Rosetta Stone").
- **Spiral:** Schwartz–Zippel *met* as a slogan here; *proved* in Ch 8. R1CS/AIR/PLONKish *met* as dialects; **QAP, the grand-product/permutation argument, and the sum-check that actually checks these constraints** are locked in Ch 8 and Ch 10. Lookups met here, genealogy locked in Ch 14/18.

#### Chapter 7 — Layers 5, 6, 7: Sealing, Bedrock, Verdict (the rest of the stack, intuitively)
- **Hook:** Three sealed envelopes of different sizes that all say the same true thing (Groth16 the tiny one with a wax seal that needed a ceremony; STARK the bigger transparent one sealed only with hashing; PLONK the universal one). Then: the *paper the envelopes are made of* (hardness assumptions), and the *public notary* who stamps them (the on-chain verifier).
- **Payload:** SNARK vs STARK as a size-vs-ceremony tradeoff (both "succinct"); the polynomial **commitment** as "sealing a polynomial in a tamper-proof envelope you can later open at one spot"; the three hardness worlds (discrete log, hash collisions, lattices) as "three different laws of physics your security could rest on"; verification as a *social/economic* act (gas, governance, data availability) — the Beanstalk governance attack as the punchline that code-correct ≠ safe.
- **Graph:** C9/C20 (SNARK, Groth16, STARK), C8 (Polynomial Commitment Scheme 123), C90 (Bilinear Pairing, IPA), C10/C14 (Lattice, Module-SIS), C33 (Merkle Tree), C53 (ZK Rollup), god-nodes PCS/KZG/FRI as labels.
- **Spiral:** *every* primitive here is met as a picture and locked later — commitments → Ch 10 (PCS taxonomy) and Ch 13 (KZG/pairing/FRI construction); pairings → Ch 13; lattices → Ch 13; Fiat–Shamir/verifier failures → Ch 12/Ch 14. This is the chapter that *maximizes* the intuition-rigor gap on purpose: the reader now holds the whole picture and is hungry for the proof.

> **End of intuition lap.** Interlude (½ page, end of Ch 7): "You can now narrate a proof end to end. Everything that follows answers the question you should now be asking — *but why does the spot-check actually work?* — and the answer is one protocol, met next."

---

### PART III — THE PROOF-SYSTEMS CORE (the rigor lap begins)

> Goal: build, rigorously, the machinery Part II only pictured. This is the part the current book is missing entirely (Tier-1 of PROPOSED_CONCEPTS). The spiral pays off here: each section slots into a Part-II picture.

#### Chapter 8 — The One Idea Under Everything: Sum-Check
- **Hook:** You claim you added up a billion numbers correctly. I don't want to re-add them. So I ask you about a *random blend* of them, one coordinate at a time — and if you lied anywhere, the blend betrays you within a few questions. That's sum-check.
- **Payload (locked):** the **sum-check protocol** in full — round-by-round structure, the degree-bound, the soundness error `≤ d·v/|F|`; **Schwartz–Zippel proved** (the slogan from Ch 6 becomes a lemma); **multilinear extension (MLE)** and the boolean hypercube as *the* representation; why multilinear, not univariate. Freivalds' / counting-triangles as warmups.
- **Graph:** C23 (Sum-Check 115, ZeroTest, #SAT IP), C47 (MLE 35, Univariate Lagrange Interpolation, Low-Degree Extension, doubly-efficient IP), C7 (Interactive Proof, Soundness).
- **Spiral:** this *is* the rigor destination for Ch 6's spot-check slogan and Ch 1's "random questions." Everything downstream (GKR, Spartan, HyperNova, Jolt, SP1) now has its engine on the table. **Highest-leverage single chapter in the book** — the 4th-largest god node, currently absent.

#### Chapter 9 — Interactive Proofs, Arguments, and What "Succinct" Means
- **Hook:** A skeptical king and a vizier who claims to have counted the kingdom's grain. The king can't recount — but with a few clever random challenges he can be 99.9999% sure. Now bound the vizier's *computational* power and the game changes (proof → argument).
- **Payload (locked):** IP / argument / MIP / PCP / IOP **taxonomy**; soundness vs. knowledge-soundness; **succinctness defined**; **PCPs and the Merkle-commit compilation** (PCP → succinct argument); the **IOP/PIOP model** as the unifying frame — "every modern system is a polynomial-IOP compiled by a commitment scheme." Doubly-efficient IPs (the delegation idea).
- **Graph:** C7 (IP 47, Argument System, NP, Freivalds), C33 (Succinct Argument, PCP, Knowledge-Soundness, MIP, low-degree testing, proximity), C8 (Interactive Oracle Proofs 37, Polynomial IOP), C20 (Taxonomy of SNARKs).
- **Spiral:** locks Ch 1's three properties as *formal* definitions and Ch 3's "succinct" slogan. Installs the **IOP+PCS factorization** that organizes Ch 10–11.

#### Chapter 10 — Polynomial Commitments: The Envelope, Opened
- **Hook:** Back to Ch 7's envelope — but now we *build four kinds of envelope* and see exactly what each trusts. A wax seal that needed a ceremony (KZG), a tamper-evident woven pattern from pure hashing (FRI), a folded-in-half-repeatedly seal (IPA), a quantum-proof seal (lattice/Ajtai).
- **Payload (locked):** the **PCS as the load-bearing god node** (degree 123); commit/open/verify abstractly; the four families compared (KZG, FRI, IPA/Bulletproofs, lattice); **GKR** built here as the canonical sum-check application (layer-by-layer reduction; LogUp-GKR named); Reed–Solomon / low-degree extension as the substrate; **the commitment trilemma** (no ceremony / small proofs / post-quantum — pick two) and its partial dissolution.
- **Graph:** C8 (PCS 123, Marlin, Gemini, masking poly), C47 (MLE, multilinear PCS), C21 (GKR 50, layered circuit, wiring predicate, Libra, linear-time prover), C74 (Reed-Solomon, Ligero, Brakedown, Orion, Aurora), C0 (FRI 82), C90 (IPA, Dory — *transparent pairing-based*, kills the "transparent ⇒ no pairings" myth).
- **Spiral:** locks Ch 7's "tamper-proof envelope" and Ch 4's KZG-as-label. GKR is the rigor home for Ch 6's "checking a circuit." Sets up Ch 13 (the *number-theoretic* guts of each envelope).

#### Chapter 11 — The Three Families, Built: Groth16, PLONK, STARK
- **Hook:** Three master locksmiths shown the same safe. One files a single perfect key for *this* safe (Groth16: circuit-specific, tiny). One cuts a master key that opens any safe of a standard make (PLONK: universal SRS). One builds a lock that needs no factory at all (STARK: transparent).
- **Payload (locked):** **QAP** (R1CS → divisibility check — the algebraic step behind Groth16's 192 bytes, and exactly what the BCTV/Pinocchio counterfeiting bug subverted); **the grand-product / permutation argument** (the accumulator polynomial `Z` that makes PLONK's copy-constraints actually bind — Part II said "wires must match," here is *how*); PLONKish + custom gates + lookups formally; STARK = AIR + FRI; **simulator and knowledge-extractor** constructions (locking Ch 1's ZK and the "K" in SNARK).
- **Graph:** C34 (QAP 25, LIP, GGPR, selector/master polynomials, Type-III pairings), C20 (Pinocchio, Linear PCP, GGPR), C11 (PLONK 88, permutation argument, Halo2/UltraPlonk, lookups), C9 (Groth16 116, STARK 83), C22 (Simulator, Extractor), C28 (Spartan — sum-check-based, the bridge to Part IV).
- **Spiral:** the convergence point — Ch 8's sum-check + Ch 9's IOP + Ch 10's PCS now *assemble into named systems*. Locks Ch 7's three envelopes. Spartan introduced here is the hinge to folding.

#### Chapter 12 — Making It Non-Interactive: Fiat–Shamir Done Honestly
- **Hook:** Ch 3 said "replace the human with a hash." Now: *what if the hash is predictable in just the wrong way?* A magician who gets to see the audience's "random" question before committing to the trick. That is the Frozen Heart bug.
- **Payload (locked):** the **Fiat–Shamir transform** rigorously; the **random-oracle model** and why it's needed; **correlation intractability** (feeding the circuit its own digest); the **two-class FS failure taxonomy** — transcript-incompleteness (Frozen Heart) vs. adaptive/correlation attacks (Last-Challenge, Solana ElGamal); the **BCS transformation** (IOP → non-interactive via Merkle + FS) that justifies the entire STARK pipeline.
- **Graph:** C17 (Fiat-Shamir 105, NIZK, CRS, VDF), C2 (Random Oracle Model, Correlation Intractability, Holographic IOP), C129 (FS soundness attacks).
- **Spiral:** the rigor home for Ch 3's slogan and Ch 7's verifier-failure foreshadowing. Hands off the *security-model* baton to Ch 13 (hardness) and Ch 14 (deployed attacks).

#### Chapter 13 — The Bedrock: Hardness Assumptions and the Pairing/Lattice Machinery
- **Hook:** Every envelope is made of *paper*, and paper is made of an assumption nobody has broken yet. Three papers: a maze with one-way doors (discrete log), a tangle no comb can undo (hash collisions), a fog of small errors (lattices). What does it take to tear each one?
- **Payload (locked):** discrete-log / CDH / q-SDH formalized; **bilinear pairing mechanics** — why `e(aP,bQ)=e(P,Q)^{ab}`, the Miller loop, **embedding degree**, and what makes BN254/BLS12-381 "pairing-friendly" vs. secp256k1; **the KZG construction in full** (commit `g^{p(τ)}`, open a quotient, verify one pairing) — the anchor Ch 4's ceremony was missing; the **Algebraic Group Model** and **Gentry–Wichs** (SNARGs can't come from falsifiable assumptions) — why "1-of-N honesty ⇒ secure" needs the AGM to be a theorem; **Ring-LWE / Module-SIS / Ajtai**, the cyclotomic ring, ML-KEM/ML-DSA, **Shor's algorithm** and the quantum shelf-life; small fields (Goldilocks, BabyBear, M31, Binius) and why the choice is a one-way door.
- **Graph:** C90 (Bilinear Pairing 47, embedding degree), C16 (pairing-friendly curves, MNT, CM, cycles), C4 (KZG construction 96), C109 (AGM), C14/C10 (Lattice 79, Module-SIS/LWE, Ajtai, Power-of-2 cyclotomic, LaBRADOR), C2 (LWE, post-quantum/QROM), C0 (small fields).
- **Spiral:** the deepest rigor floor — locks Ch 4 (KZG/AGM make the ceremony a theorem), Ch 7 (the three hardness worlds), Ch 10 (what each envelope's security *rests on*). Sets up Ch 16 (post-quantum folding).

---

### PART IV — RECURSION, ACCUMULATION, AND SECURITY AT DEPTH

> Goal: the highest-signal *absent* concept (Recursive Proof Composition, degree 83) and its family, plus the security/audit layer at full rigor. The reader has the engine (Part III) and now learns to make proofs verify proofs.

#### Chapter 14 — When the Verifier Lies, the Circuit Is Wrong, or the Walls Leak: Security at Depth
- **Hook:** A bank vault with a flawless door — and a ventilation duct nobody modeled. Most ZK failures are not broken math; they are *unmodeled ducts* (a missing constraint, a leaked timing, a governance backdoor).
- **Payload (locked):** the full **5-class vulnerability taxonomy** (Chaliasos SoK: under-constrained, over-constrained/completeness bugs, computation–constraint mismatch, …); **over-constrained circuits** (the completeness-side failure, entirely absent today); side channels at depth (Zcash timing, Poseidon cache-timing, EM); **governance as the Achilles heel** (Beanstalk \$182M, Tornado Cash governance, L2Beat stages); **rollup pricing/DoS attacks** (blob-stuffing finality delay); **proof aggregation** as the missing economic layer; **real-time proving** defined (proof within one 12s slot).
- **Graph:** C72 (Under-Constrained), C1 (side channels), C15 (Tornado Cash, Beanstalk, L2Beat), C53 (ZK Rollup), C24 (Proof Aggregation 31), C29 (Real-Time Proving).
- **Spiral:** locks Ch 5's bug story (now both *sides* of the constraint coin) and Ch 7's "verification is social." Real-time proving defined here is the threshold Part V's frontier chapters race against.

#### Chapter 15 — Proofs That Verify Proofs: Recursion, IVC, and PCD
- **Hook:** A Russian doll (each proof contains a verifier for the one inside it) vs. a hall of mirrors. Then the deeper idea: a proof that says "everything *up to here* was correct, and I checked the previous certificate of that" — induction, in cryptography.
- **Payload (locked):** **recursive proof composition** (the #1 absent god node, degree 83); **IVC** with its two-independence-condition definition; **PCD** (the graph generalization); the **bootstrapping ↔ IVC parallel** (Gentry's "circuit verifies itself"); **cycles of elliptic curves** and the field-mismatch problem (why you need a 2-cycle — BN254/Grumpkin, Pasta, MNT); STARK-to-SNARK recursion and proof compression.
- **Graph:** C24 (Recursive Proof Composition 83, STARK-to-SNARK, recursive STARK/SNARK), C18 (IVC 62, 2-cycle, SNARK composition, succinct blockchain), C26 (PCD 47, distributed proof gen), C16 (cycles of curves 40, embedding degree).
- **Spiral:** Ch 3's "proofs that verify proofs" pointer and Ch 12's recursion-via-FS now fully built. Sets up folding as the *cheaper* alternative to recursion.

#### Chapter 16 — The Snowball: Folding, Accumulation, and Nova
- **Hook:** Recursion is a Russian doll (you pay to verify at every nesting). Folding is a **snowball rolling downhill** — you mash each new instance into the running ball and defer the one real proof to the very bottom of the hill. Crucial Feynman correction: *the snowball is not yet a proof; nothing is finished until you melt it down at the end.* (Recursion-vs-folding is the most common conceptual error in ZK pedagogy — drawn explicitly.)
- **Payload (locked):** **folding schemes** (god node 116) and **accumulation schemes** (defer-then-discharge; split vs. atomic) defined; **Nova** and the relaxed-R1CS trick; **CCS / SuperSpartan / HyperNova** (generalizing beyond R1CS); **reduction of knowledge** (the soundness primitive, never named today); **CycleFold**, ProtoStar/ProtoGalaxy, Sangria; the **recursion-vs-folding distinction** stated as a theorem-shaped claim ("folding ≠ a SNARK").
- **Graph:** C39 (Folding Scheme 116, accumulation, split-accumulation, Layer-6 commitment trilemma), C5 (Nova 68, HyperNova, CycleFold, ProtoStar, R1CS), C37 (CCS 49, SuperSpartan, multi-folding), C44 (Reduction of Knowledge), C64 (Accumulation Schemes).
- **Spiral:** locks Ch 7/Ch 11's Spartan and the "snowball" picture; the post-quantum variant is held for Ch 17.

#### Chapter 17 — Post-Quantum Folding and the Lattice Frontier
- **Hook:** Everything in Ch 16 rolled downhill on *elliptic-curve* ground that Shor's algorithm can melt. Can you build the same snowball on *lattice* ground that survives the quantum thaw?
- **Payload (locked):** lattice folding lineage (Greyhound → **LatticeFold/LatticeFold+** → **Neo** small-field lattice folding → Symphony); Module-SIS/Module-LWE as the folding substrate; LaBRADOR (commitments-to-commitments, the pre-folding ancestor); the structural advantage of lattices for folding; maturity/readiness honest assessment.
- **Graph:** C10 (LatticeFold 26, Neo, Goldilocks, Ajtai, Frozen Heart), C14 (Module-SIS/LWE, LaBRADOR, cyclotomic ring, Shor), C37 (Neo, Symphony, multi-folding).
- **Spiral:** the rigor convergence of Ch 13 (lattices) + Ch 16 (folding). This is the book's deepest frontier point and the bridge into Part V's "security race."

---

### PART V — SYSTEMS, SYNTHESIS, AND THE ROAD AHEAD

> Goal: cash everything in. Frontier systems, the honest re-drawing of the model, real applications, and what's still open.

#### Chapter 18 — The Universal Stage: zkVMs
- **Hook:** Instead of building a custom proving circuit per program (a bespoke instrument per song), build *one* prover for a whole CPU and just feed it the program (a piano that plays any score). That's a zkVM.
- **Payload (locked):** **zkVM** architecture; RISC-V as the won battle; **Jolt** (the lookup-singularity — "just look everything up"), **SP1 Hypercube**, **RISC Zero**, Cairo; continuations / witness partitioning / segment-boundary correctness; **offline memory checking** (algebraic RAM — a dominant cost); where layers fuse (Jolt merges witness+arithmetization).
- **Graph:** C19 (zkVM 59, RISC Zero, continuations, receipts), C15 (Jolt, Lasso), C29 (SP1 Hypercube, LogUp-GKR, zkEVM), C0 (Cairo, SP1, RISC Zero), C99 (offline memory checking), C92 (RAM verification, Von Neumann).
- **Spiral:** every Part III–IV concept (sum-check, lookups, GKR, folding, recursion) now appears *as deployed engineering*. The payoff chapter for the rigor lap.

#### Chapter 19 — Winning the Speed Race: Real-Time Ethereum Proving
- **Hook:** A pit crew changing four tires in under two seconds. Proving an entire Ethereum block before the next one arrives (12s) is the same problem: massive parallelism against a hard deadline.
- **Payload (locked):** real-time proving as the frontier; SP1 Hypercube's GPU sharding; **Circle STARKs / Stwo** (the circle group, the squaring map, 31-bit arithmetic); small-field arithmetic end-to-end; the speed-race → security-race pivot (the EF's "128-bit by end of 2026").
- **Graph:** C0 (Circle STARKs, Stwo, M31, SP1 Hypercube, RISC Zero), C29 (Real-Time Proving, SP1 Hypercube, jagged PCS), C9 (FRI, small fields).
- **Spiral:** locks Ch 13's small-fields-as-one-way-door and Ch 14's real-time-proving definition into a concrete race. Hands the baton to Ch 20's synthesis.

#### Chapter 20 — The Honest Picture: Seven Floors Become a Graph
- **Hook:** The seven-layer "building" was a *teaching lie* — useful scaffolding, now retired. The honest picture is a **wiring diagram**: a directed acyclic graph where the choice of primitive (Layer 6) cascades up and reshapes everything above it.
- **Payload (locked):** the seven layers redrawn as a DAG with ~14 causal edges; the "proof core" (Layers 4-5-6 inseparable); the three real paths (hybrid STARK-to-SNARK, pure transparent, post-quantum folding) — *three paths, not two*; where layers collapse in practice (Jolt, Cairo). This is the synthesis the current book does at Ch 10, now arriving *after* the rigor so the edges are earned, not asserted.
- **Graph:** the whole spine re-integrated; C9/C0/C39 for the three paths.
- **Spiral:** the explicit *retirement* of the Part-I scaffolding. The book's one moment of "here is where the analogy broke, and here is the truer model."

#### Chapter 21 — What It's All For: Applications
- **Hook:** A drawer full of keys, each cut for a real lock the world is currently trying to pick — solvency after FTX, deepfakes, bridges that lost \$2B, identity at the scale of 450M EU citizens.
- **Payload:** **proof of solvency/reserves** (post-FTX; range proofs over balances); **zkTLS/DECO** (prove facts from TLS sessions); **zkBridge / ZK light clients** (trust-minimized cross-chain); **media provenance / C2PA / image authentication** (deepfake-era); **ZK SBOM / supply-chain attestation**; **proof of personhood** (the nullifier construction); **verifiable computation / delegation** (the GKR-grounded ZK-coprocessor); **ZKML** (quantization); privacy PETs (MPC/FHE/DP/TEE composability), Midnight's three-token architecture; regulatory intersection (eIDAS 2.0, GDPR).
- **Graph:** C56 (proof of solvency, Pedersen, Bitcoin reserves), C26 (PCD, media provenance, C2PA), C87 (zkBridge, deVirgo, light client), C6 (SBOM, supply chain, compliance predicate), C27 (MPC, eIDAS, DP, TEE, garbled circuits), C53 (rollups, identity), C3 (Midnight 79, Poseidon), C92 (verifiable computation), C97 (proof of personhood).
- **Spiral:** every application is now *legible* because the reader holds the machinery. Verifiable computation lands as "GKR you already met," not a black box.

#### Chapter 22 — Open Questions and the Road Ahead
- **Hook:** The map's edge, marked "here be dragons" — but now you can read the terrain well enough to guess what the dragons are.
- **Payload:** the security race (128-bit provable security by 2026); formal verification of circuits and provers; the post-quantum migration (HNDL, transport-vs-proof-layer); prover decentralization / prover markets; the enshrined-proofs roadmap; what a "prove everything" world costs and breaks.
- **Graph:** C2 (post-quantum), C73 (formal verification, static analysis), C29 (real-time/enshrined), C24 (proof markets), C95 (HNDL).
- **Spiral:** closes the spiral — the reader now stands where the field stands.

---

## 3. Reading-order rationale

1. **Two laps, not one pass.** The single biggest pedagogical decision: walk the seven layers *intuitively* (Parts I–II) before walking them *rigorously* (Parts III–IV). The current book interleaves intuition and math layer-by-layer, which forces a reader to absorb (say) the KZG ceremony and the AGM in the same breath. Splitting the laps lets the reader build a *complete mental model* with zero math first, so that when the math arrives every theorem has a pre-built slot. This is the Feynman move at book scale.

2. **Sum-check first in the rigor lap (Ch 8), not buried.** The graph says sum-check is the 4th-largest god node and currently *absent*. It is the literal engine under GKR, Spartan, HyperNova, Jolt, and SP1. Teaching it *first* in Part III means every later system is "sum-check plus a wrapper," which collapses an enormous amount of apparent complexity into one idea the reader already trusts (because Ch 6 installed the spot-check picture).

3. **IOP + PCS factorization before the named families.** Ch 9 (IOP) and Ch 10 (PCS) before Ch 11 (Groth16/PLONK/STARK) means the families arrive as *compositions of two things you understand* rather than three monoliths to memorize. "PLONK = polynomial-IOP + KZG; STARK = AIR-IOP + FRI" is only a sentence once both halves exist.

4. **Hardness bedrock (Ch 13) after the systems that use it.** Deliberately *late*. A reader does not need the Miller loop to understand what KZG *does* (Ch 10); they need it to understand *why it's safe* and *what the ceremony bought* (Ch 13). Putting the number theory after the constructions respects "intuition before formalism" even inside the rigor lap.

5. **Recursion/folding (Part IV) after the core, before systems.** zkVMs and real-time proving (Part V) are *applications of* recursion and folding, so those must be locked first. Folding-after-recursion (Ch 16 after Ch 15) lets the snowball be taught as "the cheaper alternative to the Russian doll you just learned."

6. **Security at depth (Ch 14) opens Part IV, not Part V.** Auditors and skeptics are a core audience; placing the full vulnerability taxonomy right after the core math (while it's fresh) and *before* recursion means recursion's extra attack surface lands on prepared ground.

7. **Synthesis (Ch 20) after rigor, not at the midpoint.** The current book redraws the DAG at Ch 10/midbook; here it lands at Ch 20 so the 14 causal edges are *derived from* machinery the reader has built, not asserted as a promise.

---

## 4. What's new vs. the current 14-chapter book

**Structural change:** 14 → **22 chapters / 5 parts**, and the seven layers are walked **twice** (intuition lap = Parts I–II; rigor lap = Parts III–IV). The current book walks them once, mixing intuition and math per layer.

**Six genuinely new chapters of foundational theory** (the Tier-1 gap — concepts the current book *names but never builds*):
- **Ch 8 — Sum-Check** (god node, absent today): round structure, soundness bound, MLE, boolean hypercube, Schwartz–Zippel *proved*.
- **Ch 9 — IP/Argument/IOP taxonomy** (absent): succinctness defined, PCP→argument compilation, the unifying PIOP frame.
- **Ch 10 — Polynomial Commitments + GKR** (PCS under-built; GKR absent): four-family PCS, GKR as canonical sum-check app, Dory, Reed–Solomon substrate.
- **Ch 11 — QAP + grand-product argument** (both thin/absent): the algebraic step behind Groth16's 192 bytes; the accumulator `Z` behind PLONK copy-constraints; simulator/extractor constructions.
- **Ch 13 — Pairing mechanics + KZG construction + AGM** (KZG construction absent; AGM absent): the Miller loop, embedding degree, the 3-equation KZG, Gentry–Wichs / non-falsifiable assumptions.
- **Ch 15 — Recursion/IVC/PCD** (Recursive Proof Composition is the #1 absent god node): IVC's two-condition definition, PCD, cycles of curves, bootstrapping↔IVC.

**High-signal absent concepts, placed:**
- Recursive Proof Composition (deg 83) → Ch 15. Sum-Check (115) → Ch 8. KZG construction (96) → Ch 13. GKR (50) → Ch 10. MLE (35) → Ch 8. IOP (37) → Ch 9. PCD (47) → Ch 15. Cycles of curves (40) → Ch 15. Accumulation schemes (36) → Ch 16. QAP (25) → Ch 11. Grand-product argument → Ch 11. AGM (15) → Ch 13. Merkle/commitment/Sigma → Ch 9–10. Reduction of knowledge → Ch 16. Verifiable computation (deg 27, ref 16!) → Ch 21. VDFs → Ch 22/Ch 14. Reed–Solomon/Ligero/Brakedown → Ch 10. Linear PCP/Pinocchio/GGPR → Ch 11. Over-constrained circuits → Ch 14.
- **New applications** (Tier-3, absent): proof of solvency, zkTLS/DECO, zkBridge, media provenance/C2PA, ZK SBOM, proof of personhood, verifiable delegation — all in Ch 21.
- **New depth** (Tier-4/5): Marlin/Spartan/Aurora/Gemini (Ch 9–11), Dory/Basefold/Hyrax (Ch 10), offline memory checking + jagged PCS (Ch 18), BCS transformation + two-class FS taxonomy (Ch 12), Ring-LWE/ML-KEM/ML-DSA/LaBRADOR/Binius (Ch 13/17), Neo/Sangria (Ch 16/17), subversion-ZK/perpetual-powers-of-tau/sim-extractability (Ch 4/Ch 11).

**Pedagogical change:** every chapter now carries an explicit **Hook → Payload** pair and a named **spiral destination**, so "where met intuitively" and "where locked rigorously" are different, tracked, and deliberate.

---

## 5. Risks / tradeoffs

1. **The two-lap structure risks redundancy.** Walking the layers twice could feel repetitive to an expert reader. *Mitigation:* Parts I–II are deliberately thin and fast (analogy-only, ~7 chapters of light reading); the spiral pointers make the rigor lap feel like *payoff*, not repetition. A "Skip to Part III" note can serve experts.

2. **Delayed gratification for practitioners.** A reader who wants to *write a circuit today* must pass through Parts I–II first. *Mitigation:* the Sudoku is end-to-end-runnable by end of Part II; the language/witness practicalities (Ch 5) and zkVMs (Ch 18) give hands-on anchors. But this book optimizes *understanding*, not quick-start — an explicit tradeoff.

3. **Big intuition-rigor gaps can frustrate.** Ch 7 maximizes the gap on purpose (whole stack pictured, nothing proved). A reader who dislikes "trust me, proof later" may chafe for ~150 pages. *Mitigation:* every Part-II concept carries a visible forward-pointer to its exact rigor chapter, so the debt is always explicitly tracked, never hidden.

4. **22 chapters is long.** Risk of a doorstop. *Mitigation:* Parts I–II chapters are short; the length lives in Parts III–IV where it belongs (the rigorous core the book was missing). The five-part skeleton keeps navigation tractable.

5. **Sum-check-first is a bet.** If a reader bounces off Ch 8, the whole rigor lap is at risk since everything downstream leans on it. *Mitigation:* Ch 6 pre-installs the spot-check picture and Ch 8 opens with the "random blend of a billion numbers" hook and Freivalds warmup before any multilinear algebra — the gentlest possible on-ramp to the hardest load-bearing idea.

6. **Midnight as running example carries author-bias risk** (author founded it). *Mitigation:* inherited from the current book — Midnight claims stay public-doc-verifiable; Sudoku carries the *teaching* weight, Midnight carries the *production-reality* weight.
