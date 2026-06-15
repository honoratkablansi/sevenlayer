# Outline Design — "Proving Nothing", THEORY-CORE LENS

*Architect lens: the rigorous proof-systems theory core, built in correct dependency order. Each result is constructed from the one before it, so the machinery the current book only names is finally assembled on the page.*

---

## 1. One-paragraph thesis

The current book is a brilliant **map of the territory** that never lets you **walk the road**: it names sum-check, IOPs, GKR, MLE, KZG, QAP, the grand-product argument, and the AGM as landmarks, but a reader can finish all fourteen chapters without ever seeing a single one of them *built*. My lens fixes exactly that. I keep Hoskinson's seven-layer trust-decomposition thesis as the book's organizing spine and its narrative bookends — but I insert, between "what trust is decomposed into" and "how the industry ships it," a **single rigorously ordered technical heart** (Part III, *The Engine*) in which every result is the literal input to the next. The chain is forced, not curated: you cannot state Schwartz–Zippel without low-degree polynomials; you cannot run sum-check without the multilinear extension; you cannot get GKR without sum-check; you cannot get a SNARK without first separating the *information-theoretic* object (the IOP/polynomial-IOP) from the *cryptographic* compiler (the polynomial commitment), and you cannot trust that compiler without the hardness assumptions and the security model (AGM, ROM) that justify it. The thesis of the lens is therefore a **claim about pedagogy as architecture**: the seven layers tell you *where* trust hides; the engine tells you *why the math forces it to hide there and nowhere else.* Feynman governs every chapter — analogy and picture first, then the construction is locked down — but the engine's chapters additionally obey a second law: **no chapter may use a tool a prior chapter has not already constructed.** The payoff is that by the time the reader reaches Groth16's 192-byte proof, the recursion/folding genealogy, or Midnight as a case study, every one of those is a *recombination of parts the reader has personally assembled*, not a brand name to be trusted.

---

## 2. The full outline

**Book shape: 5 Parts, 22 chapters.** Part III (*The Engine*) is the theory core this lens owns; it is 9 chapters built in a strict dependency chain. The other four parts keep and reorganize the existing seven-layer material so the engine has somewhere to plug in.

Legend for each chapter: **[Hook]** = Feynman intuition/analogy opener · **[Payload]** = the formal object locked down · **[Graph]** = communities / god-nodes drawn from · **DEP** = what earlier chapter(s) it consumes (engine chapters only).

---

### PART I — THE INVITATION (why provable secrets, and the seven-layer claim)
*2 chapters. Keeps the book's on-ramp; plants the roadmap pointers the current Ch.1 lacks.*

**Chapter 1 — The Promise of Provable and Programmable Secrets**
- §1.1 The trick at the door (the existing cave/ali-baba-style hook) · §1.2 The phenomenon and three converging forces · §1.3 **The roadmap pointer the book is missing**: a one-page "you will *build* this engine" promise naming the chain ahead (randomness → polynomials → sum-check → IOP+PCS = SNARK → recursion).
- **[Hook]** A sealed verdict that convinces you of a fact while telling you nothing else.
- **[Payload]** Working definitions of completeness, soundness, knowledge-soundness, zero-knowledge as *promises to be redeemed later* — stated informally now, flagged for rigorous redemption in Ch. 8–9 and 12.
- **[Graph]** Zero-Knowledge Proof (117), SNARK (139); C22, C7. Places absent concepts *Prover*, *Verifier*, *Succinctness*, *Recursive-composition roadmap pointer*.

**Chapter 2 — Trust Is Not Destroyed, It Is Decomposed (The Seven Layers)**
- §2.1 The seesaw: you never remove trust, you move it · §2.2 The seven layers named (setup → language → witness → arithmetization → proof system → primitives → verifier) · §2.3 The causal DAG, not a stack · §2.4 "Trustless" vs "trust-minimized."
- **[Hook]** A magic trick isn't magic — it's misdirection you can *audit* once you know where to look.
- **[Payload]** The seven-layer decomposition as the book's coordinate system; each layer gets a "this is where the engine will explain *why*" forward-pointer.
- **[Graph]** Trust Minimization (Not Trustless), seven-layer thesis (C9, C10's Frozen Heart preview). This is the existing spine, pulled forward to Part I so the engine can refer back to it.

---

### PART II — THE STAGE AND THE STATEMENT (the front end: from program to a thing you can prove)
*3 chapters. The "before the math" plumbing: what statement are we even proving, and in what form.*

**Chapter 3 — Languages and the Front End (Layer 2)**
- §3.1 The four philosophies (Compact / Noir / Leo / circuit-DSL) · §3.2 The compiler-not-language thesis (CirC) · §3.3 Under- and **over**-constrained circuits as the dominant failure mode.
- **[Hook]** You don't prove "the program ran" — you prove "these numbers satisfy these equations." Someone has to translate.
- **[Payload]** Circuit-SAT front ends; the program→circuit pipeline; witness vs instance separation; the constraint-as-contract view.
- **[Graph]** C94 (Circom/CirC/ZoKrates), C3 (Compact/Noir), C72 (under-constrained). Adds absent: ZoKrates, CODA/refinement types, over-constrained circuits.

**Chapter 4 — The Witness and the Execution Trace (Layer 3)**
- §4.1 The secret performance: the trace nobody sees · §4.2 Witness generation as the hidden bottleneck · §4.3 Non-deterministic hints; witness partitioning / continuations.
- **[Hook]** The witness is the actor's private script — the audience sees only that the play was internally consistent.
- **[Payload]** Witness = private satisfying assignment; the witness-constraint divergence bug class; the `disclose()` boundary as a worked example.
- **[Graph]** C1 (Witness/Witness-Generation/Side-Channel), C19 (Continuations). Adds witness partitioning, hints.

**Chapter 5 — Arithmetization: Turning Logic into Algebra (Layer 4, part 1 — the encodings)**
- §5.1 The spreadsheet metaphor and where it breaks · §5.2 R1CS → AIR → PLONKish as a dialect evolution · §5.3 CCS as the Rosetta Stone (one grammar over all three).
- **[Hook]** A computation is a story; arithmetization is rewriting the story as a system of polynomial equations that is true *iff* the story is.
- **[Payload]** R1CS (Az∘Bz=Cz), AIR transition+boundary constraints, PLONKish gates+selectors, CCS as the degree-parameterized generalization. **The algebra is *stated* here; the proof that these encodings are sound is deferred to the engine.**
- **[Graph]** C11 (PLONKish/AIR/Arithmetization), C5 (R1CS), C37 (CCS). god-nodes R1CS (91), CCS (49), Arithmetization (30).

> **Hand-off to the engine:** Part II leaves the reader with a *statement* in algebraic form (an R1CS/AIR/PLONKish/CCS instance) and a *witness*. Part III's entire job is to answer: **how do you prove a witness exists, succinctly, without revealing it — and why is each step sound?**

---

### PART III — THE ENGINE (the rigorous proof-systems core) ★ THIS LENS OWNS THIS PART ★
*9 chapters, built in a strict dependency chain. This is the technical heart the current book names but never constructs. Every chapter's payload is the explicit input to the next. The dependency arrows below are load-bearing, not decorative.*

**The chain at a glance (each → means "is literally used to build"):**
`Ch6 randomness/fingerprinting → Ch7 low-degree & multilinear extensions → Ch7 Schwartz–Zippel → Ch8 Sum-Check → Ch8 GKR/IPs → Ch9 MIP → Ch9 PCP → Ch10 IOP & polynomial-IOP → Ch11 polynomial commitments (KZG/IPA/FRI/Brakedown-Ligero/Dory) → Ch12 the IOP+PCS=SNARK recipe → Ch13 Linear-PCP/QAP/GGPR/Groth16 → Ch14 Fiat-Shamir/ROM/AGM → (hands to Part IV recursion/folding).`

---

**Chapter 6 — Randomness as a Detector: Fingerprinting and Freivalds (the engine's first principle)**
- §6.1 Catching a liar by spot-checking · §6.2 Reed–Solomon fingerprinting: hash two long objects to one field element · §6.3 Freivalds' algorithm: verify a matrix product in O(n²) by multiplying by a random vector.
- **[Hook]** To check if two enormous books are identical, you don't read them — you ask a random page-and-line and compare one character. Disagreement *somewhere* becomes disagreement *here* with high probability.
- **[Payload]** The probabilistic-checking primitive: equality of large objects reduces to one random evaluation; the union bound and the role of field size in the error. This is the *seed* every later soundness bound grows from.
- **[Graph]** C7 (Freivalds, Interactive Proof, Soundness, Completeness, NP, Argument System). god-nodes Soundness (27), Completeness (13). Adds absent: Freivalds' Algorithm, Reed–Solomon Fingerprinting, Argument System.
- **DEP:** none (foundation). **PRODUCES:** the "random evaluation catches inequality" lemma used by every subsequent chapter.

**Chapter 7 — Polynomials Are the Right Language: Low-Degree & Multilinear Extensions, and Schwartz–Zippel**
- §7.1 Why polynomials: a low-degree polynomial is *rigid* — pin a few points and it can't wiggle · §7.2 Univariate Lagrange interpolation and the low-degree extension (LDE) · §7.3 The **multilinear extension (MLE)** of a function on the Boolean hypercube: the unique multilinear polynomial agreeing on {0,1}ⁿ · §7.4 **Schwartz–Zippel**: a nonzero degree-d polynomial vanishes at ≤ d/|F| random points.
- **[Hook]** Two distinct low-degree curves can kiss at only a few points; pick a random point and they almost surely disagree. Fingerprinting (Ch.6) was the d=0 shadow of this.
- **[Payload]** LDE and MLE constructions (the MLE multilinear-Lagrange formula), the Boolean hypercube as index set, Schwartz–Zippel with proof, and the **"reduce a claim about a whole table to a claim about one random point"** paradigm.
- **[Graph]** C47 (MLE, Finite Field Arithmetic, LDE, Univariate Lagrange Interpolation, Boolean Hypercube), C11 (Schwartz–Zippel). Adds absent: MLE, LDE, Lagrange interpolation, Boolean Hypercube, Schwartz–Zippel (rigorous).
- **DEP:** Ch.6 (random-evaluation lemma). **PRODUCES:** MLE + Schwartz–Zippel — the two objects sum-check requires.

**Chapter 8 — The Sum-Check Protocol and GKR: Interactive Proofs That Beat Reading the Whole Thing**
- §8.1 Interactive proofs defined: prover, verifier, public coins, soundness as a probability · §8.2 **Sum-Check**: prove Σ over the hypercube of a low-degree polynomial equals a claimed value, round by round, each round shrinking the claim by one variable · §8.3 Soundness of sum-check from Schwartz–Zippel; the multilinear/CMT variant · §8.4 **GKR**: chain sum-checks layer-by-layer up an arithmetic circuit so the prover never commits the full trace; the wiring predicate (add_i/mult_i); doubly-efficient delegation.
- **[Hook]** Instead of re-summing a billion numbers, you make the prover defend the sum one variable at a time; each round you challenge a single random coordinate, and a liar's lie has to survive every round — it can't.
- **[Payload]** The full round structure and soundness bound of sum-check; GKR as repeated sum-check up a layered circuit; the linear-time prover (Libra) and the doubly-efficient interactive proof.
- **[Graph]** C23 (Sum-Check, Grand-Product, #SAT IP), C21 (GKR, Layered Arithmetic Circuit, Wiring Predicate, Libra, Linear-Time Prover), C7 (Interactive Proof). god-node Sum-Check (115), GKR (50). The single highest-leverage absent concept set in the whole graph.
- **DEP:** Ch.7 (MLE, Schwartz–Zippel). **PRODUCES:** sum-check as a reusable subroutine; GKR as the first *practical, no-commitment* proof — the template for everything succinct.

**Chapter 9 — From One Prover to None: MIPs, PCPs, and the Theory of Succinctness**
- §9.1 Multi-prover interactive proofs (MIP): two provers who can't collude let the verifier cross-examine · §9.2 The PCP theorem as a destination, not a detour: a proof you can verify by reading O(1) random bits · §9.3 Low-degree testing and proximity as the bridge from "a function" to "close to a low-degree polynomial" · §9.4 Compiling a PCP into a succinct argument via Merkle commitment (the first time "commit then open random spots" appears as a *paradigm*).
- **[Hook]** A PCP is a confession written so that any lie corrupts a constant fraction of it — so spot-checking a few random words exposes it. MIP is two suspects in separate rooms whose stories can't both be consistent and false.
- **[Payload]** MIP and PCP models; the proximity/low-degree-testing idea; the Merkle-commitment compilation of a PCP — the conceptual ancestor of every IOP-based SNARK.
- **[Graph]** C33 (PCP, MIP, Succinct Argument, Knowledge-Soundness, Merkle Tree, Proximity Test, Low-Degree Testing, Prover, Verifier, Circuit-SAT front ends). Adds absent: MIP, PCP (rigorous), Succinct Argument, Low-Degree Testing, Merkle Tree, Proximity Test.
- **DEP:** Ch.8 (sum-check/GKR machinery; soundness via Schwartz–Zippel). **PRODUCES:** the "spot-check a committed object" paradigm and the formal notion of *succinctness/knowledge-soundness* that the IOP framework will modularize.

**Chapter 10 — Interactive Oracle Proofs and the Polynomial-IOP: The Modular Frame**
- §10.1 The IOP model: rounds of oracles the verifier may query at a few points (PCP + interaction generalized) · §10.2 The **polynomial IOP**: oracles *are* low-degree polynomials; the verifier "evaluates" them · §10.3 The grand unification: PLONK, Marlin, Spartan, Aurora, HyperNova all = a polynomial-IOP + a way to realize the oracles · §10.4 The grand-product / permutation argument and the zero-test as reusable polynomial-IOP gadgets.
- **[Hook]** Imagine the prover hands you an *idealized* magic polynomial you can poke anywhere for free, but can't read. Design the whole protocol assuming that genie exists — then later (Ch.11) buy the genie cheaply with cryptography.
- **[Payload]** IOP and polynomial-IOP definitions; the *separation of concerns* that is this lens's keystone — information-theoretic protocol vs cryptographic realization; permutation/grand-product and ZeroTest as PIOP building blocks.
- **[Graph]** C8 (Polynomial Commitment Scheme, Interactive Oracle Proofs, Polynomial-IOP, Marlin, Gemini, Supersonic), C23 (Grand-Product, Vanishing Polynomial, ZeroTest, HyperPlonk), C28 (Spartan). Adds absent: IOP, Polynomial-IOP, Grand-Product Argument, Permutation Argument, Marlin/Spartan/Aurora paragraphs.
- **DEP:** Ch.9 (oracle/spot-check paradigm), Ch.8 (sum-check inside many PIOPs). **PRODUCES:** the abstract "polynomial-IOP" — the left half of the SNARK recipe.

**Chapter 11 — Polynomial Commitments: Buying the Genie (KZG · IPA/Bulletproofs · FRI · Ligero/Brakedown · Dory)**
- §11.1 The contract a PCS must sign: commit to a polynomial, later prove p(z)=y, in less space/time than sending p · §11.2 **KZG** from pairings: commit g^{p(τ)}, open the quotient (p(x)−y)/(x−z), verify in one pairing — needs a trusted SRS · §11.3 **IPA/Bulletproofs**: transparent, log-sized, from discrete log; Halo's amortization · §11.4 **FRI**: transparent, hash-based, post-quantum, from Reed–Solomon proximity (calls back to Ch.9 low-degree testing) · §11.5 **Ligero/Brakedown**: linear-time, code-based · §11.6 **Dory**: transparent *pairing-based* (kills the "transparent ⇒ no pairings" myth); Basefold/Hyrax as the multilinear cousins.
- **[Hook]** The polynomial genie of Ch.10 was free but imaginary. A polynomial commitment is the genie's *price list*: four different currencies (pairings, discrete log, hashes, codes), each buying the same poke-it-anywhere power with a different trust/size/PQ tradeoff.
- **[Payload]** Each scheme's commit/open/verify; the security each rests on (Ch.14 will formalize); the **Layer-6 trilemma** (size vs transparency vs PQ) now derived rather than asserted; pairing mechanics and embedding degree shown explicitly for KZG.
- **[Graph]** C4 (KZG, SRS, Powers of Tau, Multilinear KZG), C90 (Bilinear Pairing, IPA, Dory, AFGHO), C0/C9 (FRI), C74 (Ligero, Brakedown, Reed–Solomon, Orion, Aurora), C15 (Bulletproofs). god-nodes PCS (123), KZG (96), FRI (82), Bilinear Pairing (47). Adds absent: KZG construction, pairing mechanics, Dory, Brakedown, Ligero, Reed–Solomon, Hyrax, Basefold.
- **DEP:** Ch.10 (the oracle it realizes), Ch.9 (FRI uses low-degree testing), Ch.7 (polynomials), Ch.6 (random-evaluation soundness). **PRODUCES:** the right half of the SNARK recipe — a *real* (committable, openable) polynomial oracle.

**Chapter 12 — The Recipe: IOP + PCS = SNARK**
- §12.1 The assembly: take a polynomial-IOP (Ch.10), replace each idealized oracle with a polynomial commitment (Ch.11), make it non-interactive (Ch.14) — out comes a succinct argument · §12.2 Why the four PCS choices generate the whole SNARK zoo (PLONK=PIOP+KZG; STARK=AIR-IOP+FRI; Spartan=sum-check-PIOP+any-PCS) · §12.3 Adding zero-knowledge: masking polynomials and randomized oracles · §12.4 The cost ledger: where prover time, proof size, and verifier time actually come from.
- **[Hook]** You have built both halves with your own hands. Snapping them together is the moment a "convince me interactively" protocol becomes a "192-byte certificate anyone can check" — and you can now read any new SNARK paper as a choice of *which IOP × which PCS.*
- **[Payload]** The compilation theorem (informally: soundness of IOP + binding of PCS ⇒ knowledge-soundness of the argument); the zero-knowledge masking construction; a taxonomy table the reader can now *derive* rather than memorize.
- **[Graph]** C20 (SNARK, Taxonomy of SNARKs IP/MIP/IOP), C8 (PCS), C2 (Preprocessing SNARK, Holographic IOP), C33 (Succinct Argument). god-node SNARK (139). Adds absent: zk-SNARK construction, masking polynomial, the explicit recipe.
- **DEP:** Ch.10 (IOP) + Ch.11 (PCS), the two halves. **PRODUCES:** a general SNARK — the object the rest of the book ships, audits, and recurses.

**Chapter 13 — The Other Road: Linear PCPs, QAP, GGPR, and Groth16's 192 Bytes**
- §13.1 A second, historically-first route to SNARKs that does *not* go through IOPs: the linear PCP · §13.2 **QAP**: turn an R1CS instance (Ch.5) into a single polynomial divisibility check — does the target polynomial divide? · §13.3 GGPR/Pinocchio: encrypt the linear-PCP queries with a pairing-based SRS · §13.4 **Groth16**: the optimized three-pairing verifier, the constant-size proof, and exactly what the BCTV/Pinocchio counterfeiting bug subverted.
- **[Hook]** There's an older path to the same summit. Instead of "commit to polynomials and poke them," you compress the entire computation into one question — *does this polynomial divide that one?* — and answer it in encrypted form so the prover can't cheat or peek.
- **[Payload]** Linear-PCP and LIP models; the QAP construction from R1CS; GGPR's pairing encoding; Groth16's verification equation; why it needs a circuit-specific trusted setup and why its proof is 192 bytes; simulation-extractability vs knowledge-soundness.
- **[Graph]** C20 (Linear PCP, GGPR, Pinocchio, Front End), C34 (QAP, LIP, Generic Bilinear Group Model, Selector/Master Polynomial), C9 (Groth16). god-nodes Groth16 (116), R1CS (91). Adds absent/thin: Linear PCP, QAP construction, GGPR, Pinocchio, LIP.
- **DEP:** Ch.5 (R1CS to arithmetize), Ch.11 (pairings/SRS), Ch.6–7 (polynomials, divisibility, Schwartz–Zippel). **PRODUCES:** the pairing-SNARK lineage and the *contrast case* that makes the IOP route legible by negation.

**Chapter 14 — Making It Non-Interactive and Provably Secure: Fiat–Shamir, the ROM, and the AGM**
- §14.1 **Fiat–Shamir**: replace the verifier's coins with a hash of the transcript — interaction dies, the proof posts to a chain · §14.2 The **random oracle model**: the idealization that makes FS sound, and correlation intractability as the real assumption underneath · §14.3 The **two-class FS failure taxonomy**: transcript-incompleteness (Frozen Heart) vs adaptive correlation attacks · §14.4 The **AGM and Gentry–Wichs**: why Groth16/PLONK/KZG are only provably secure in idealized models, and why SNARGs *provably can't* come from falsifiable assumptions.
- **[Hook]** The last interactive step is a coin the verifier flips. Fiat–Shamir says: let the *transcript itself* flip the coin via a hash — but if you hash the wrong things, you hand the prover the coin, and the Frozen Heart bug is exactly that mistake.
- **[Payload]** The FS transform and its soundness in the ROM; correlation intractability; the failure taxonomy as a security checklist; the AGM as the model in which the engine's cryptographic claims actually hold; the falsifiable-assumptions impossibility result that bounds what we can hope to prove.
- **[Graph]** C17 (Fiat–Shamir, NIZK, Common Reference String), C2 (ROM, Correlation Intractability, Transparent Setup), C109 (AGM), C129 (FS soundness attack). god-node Fiat–Shamir (105). Adds absent: ROM, correlation intractability, AGM, two-class FS taxonomy, Gentry–Wichs.
- **DEP:** Ch.12 & Ch.13 (it non-interactivizes *both* SNARK routes), Ch.6 (random coins). **PRODUCES:** non-interactive, deployable, security-modeled SNARKs — and hands the baton to recursion (Part IV), which needs FS-in-circuit and the AGM/cycle machinery.

> **The engine, complete.** A reader who has finished Part III has personally built: the random-evaluation detector → polynomial extensions + Schwartz–Zippel → sum-check + GKR → MIP/PCP → IOP/PIOP → all four PCS families → the SNARK recipe → the QAP/Groth16 alternative → Fiat–Shamir/ROM/AGM. Every later brand name is now a *recombination*, not a leap of faith.

---

### PART IV — SCALING THE ENGINE (recursion, folding, and the post-quantum frontier)
*4 chapters. Now legitimate: every tool these chapters fold and recurse was constructed in Part III.*

**Chapter 15 — Recursion, IVC, and PCD: Proofs That Verify Proofs**
- §15.1 Russian dolls: a proof whose statement is "I verified a proof" · §15.2 IVC's two-independence definition; PCD as the DAG generalization · §15.3 The field-mismatch problem and **cycles of elliptic curves** (MNT, Pasta, BN254/Grumpkin) · §15.4 Bootstrapping ↔ IVC (Gentry's "circuit verifies itself" parallel).
- **[Hook]** To prove an endless computation, prove each step *and* that you checked the previous proof — a snake eating its tail, but every bite is verified.
- **[Payload]** Recursive proof composition (verifier-in-circuit, needs FS-in-circuit from Ch.14); IVC and PCD formal defs; why two curves are needed and how cycles solve it.
- **[Graph]** C24 (Recursive Proof Composition, Aggregation, STARK-to-SNARK), C18 (IVC, 2-cycle), C26 (PCD), C16 (Cycles of Elliptic Curves, embedding degree, MNT). god-nodes Recursive Composition (83), IVC (62), PCD (47).
- **DEP:** Ch.12 (the SNARK being recursed), Ch.14 (FS-in-circuit), Ch.11 (the PCS the inner verifier runs).

**Chapter 16 — Folding Schemes: Deferring the Proof (Nova and the Genealogy)**
- §16.1 The snowball vs the Russian doll: fold many instances into one, prove *once* at the end · §16.2 Folding ≠ a SNARK — the single most common ZK pedagogy error, drawn explicitly · §16.3 Accumulation (split vs atomic), reduction of knowledge · §16.4 The genealogy: Nova → SuperNova → HyperNova → ProtoStar/ProtoGalaxy → CycleFold → Sangria; CCS-folding (SuperSpartan).
- **[Hook]** Don't verify each snowflake — pack them into one snowball and weigh it once. The snowball never "is" a proof until the very end; that's the whole trick and the whole danger.
- **[Payload]** The folding reduction (combine two R1CS/CCS instances into one with a random challenge — Schwartz–Zippel again); accumulation schemes; the recursion-vs-folding distinction stated precisely.
- **[Graph]** C39 (Folding Scheme, Accumulation, Mangrove), C5 (Nova, HyperNova, CycleFold, ProtoStar), C37 (CCS-folding, SuperSpartan), C46 (SuperNova), C44 (Reduction of Knowledge). god-nodes Folding (116), Nova (68), CCS (49).
- **DEP:** Ch.15 (IVC, which folding instantiates), Ch.5 (R1CS/CCS being folded), Ch.7 (random-linear-combination soundness).

**Chapter 17 — Primitives and Hardness (Layer 6): Pairings, Discrete Log, Hashes, and Lattices**
- §17.1 The three worlds the engine can be built in: pairing/DLOG, hash, lattice · §17.2 Discrete-log/CDH/q-SDH formalized; pairing-friendly curves and the small-field migration (BabyBear/M31/Goldilocks) · §17.3 Algebraic hashes (Poseidon/Poseidon2/Rescue) · §17.4 **Lattices and post-quantum**: Ring-LWE, Module-SIS, Ajtai commitments, LaBRADOR, LatticeFold/Neo, ML-KEM/ML-DSA.
- **[Hook]** Every certificate in this book rests on a problem we *believe* is hard. Here are the three bets — factor-style pairings, hash collisions, lattice vectors — and which ones survive a quantum computer.
- **[Payload]** The hardness assumptions made explicit (forward ref from Ch.11/14); pairing internals (Miller loop, embedding degree); the PQ transition; lattice commitments as the post-quantum engine substrate.
- **[Graph]** C10 (Lattice, PQ, Goldilocks, Ajtai, LatticeFold, Neo), C14 (Module-SIS/LWE, LaBRADOR, cyclotomic ring, Shor), C16 (pairing-friendly curves), C3 (Poseidon, BLS12-381). god-nodes Lattice (79), PQ (47).
- **DEP:** Ch.11 (which assumptions each PCS used), Ch.13 (pairings). *Placed after the engine so the assumptions are motivated by the schemes that need them, not front-loaded.*

**Chapter 18 — The Setup Layer Revisited (Layer 1), Now With Teeth**
- §18.1 The fair-shuffle problem and the structured reference string · §18.2 The MPC ceremony protocol (contribute→prove→destroy), perpetual powers of tau, random-beacon finalization, the 1-of-N model · §18.3 Universal/updatable SRS (Sonic) vs circuit-specific; subversion-ZK and SRS-subversion attacks · §18.4 Transparent setup as the alternative the engine already enables (FRI/IPA from Ch.11).
- **[Hook]** Someone has to build the stage before the show — and if they keep a copy of the key (toxic waste), they can forge every proof. The ceremony is how thousands of strangers build a stage no one of them can unlock.
- **[Payload]** The SRS and its trust model with the KZG construction (Ch.11) as the concrete anchor; ceremony structure; updatable-SRS property; subversion resistance; SRS degree bound.
- **[Graph]** C4 (Trusted Setup, Powers of Tau, SRS, Universal vs Circuit-Specific), C58 (MPC Ceremony), C69 (Updatable Universal SRS), C2 (Transparent Setup). god-node Trusted Setup (95).
- **DEP:** Ch.11 (KZG/SRS), Ch.13 (Groth16's circuit-specific setup). *Layer 1 is told last in the engine arc because the SRS only makes sense once you know what it's an SRS for.*

---

### PART V — THE SYSTEM IN THE WORLD (verification, privacy, applications, the road ahead)
*4 chapters. The seven-layer payoff: now that the engine is built, show it deployed, attacked, and applied.*

**Chapter 19 — The Verdict (Layer 7) and the Security of the Whole Stack**
- §19.1 On-chain verification: the social layer and the price of a verdict · §19.2 The verification-data seesaw and DA marketplace · §19.3 The five-class vulnerability taxonomy (Chaliasos SoK) spanning all seven layers · §19.4 Governance as the real attack surface (Beanstalk, Tornado Cash, rollup DoS/pricing attacks); VDFs and randomness beacons.
- **[Hook]** The proof is perfect; the *deployment* is where money is lost. A verdict is only as trustworthy as the contract, the governance, and the data that surround it.
- **[Payload]** On-chain verifier mechanics; the cross-layer bug taxonomy; pricing/DoS attacks; VDFs as a Community-7 gap finally filled.
- **[Graph]** C33 (Verifier), C53 (ZK/Optimistic Rollup, DA), C15 (Tornado Cash, Beanstalk, L2Beat), C12 (VDF). Adds absent: VDFs, vulnerability taxonomy, rollup DoS.
- **DEP:** the whole engine (each bug class maps to a layer the reader now understands).

**Chapter 20 — Privacy as a Cross-Cutting Concern (PETs, and How ZK Composes With Them)**
- §20.1 The four pillars (ZK, MPC, FHE, TEE/DP) and where each fits · §20.2 Composability: Kachina, Zexe, collaborative/threshold proving · §20.3 The regulatory intersection (GDPR immutability paradox, eIDAS 2.0) · §20.4 Selective disclosure, nullifiers, proof of personhood.
- **[Hook]** Zero-knowledge hides *one* thing well; real privacy needs a wardrobe. Here's how the four privacy technologies dress a system together.
- **[Payload]** PET comparison and composition; selective-disclosure and nullifier constructions; the regulatory drivers.
- **[Graph]** C27 (MPC, FHE, TEE, DP, eIDAS, GDPR, garbled circuits), C22 (ZKP, Simulator). Adds: nullifier mechanism, BBS+/SD-JWT, collaborative proving.
- **DEP:** Ch.12 (zk-SNARK), Ch.4 (the witness being hidden).

**Chapter 21 — The Applications: zkVMs, Rollups, Coprocessors, Identity, and Provenance**
- §21.1 zkVMs as the universal stage (SP1, Stwo/Cairo, Jolt) through the seven layers · §21.2 Rollups and the proving-as-a-service market · §21.3 Verifiable computation/delegation: ZK coprocessors, zkTLS/DECO, proof of solvency, zkBridge · §21.4 Media provenance/C2PA, ZK SBOM, ZKML.
- **[Hook]** The engine, productized: instead of writing a circuit by hand, you prove an entire RISC-V program ran — and suddenly the whole software world becomes provable.
- **[Payload]** zkVM architecture (continuations, offline memory checking, lookup-centric design — all now legible from the engine); the application catalogue with each app named to the layer/primitive it leans on.
- **[Graph]** C19/C29 (zkVM, RISC Zero, SP1, zkEVM, LogUp-GKR), C0 (Cairo, RISC Zero), C15 (Jolt, Lasso), C92 (Verifiable Computation), C26 (PCD/media provenance), C87 (zkBridge), C56 (proof of solvency). god-nodes zkVM (59), SP1 (47). Adds absent: verifiable computation/delegation, zkTLS, zkBridge, proof of solvency, media provenance, SBOM.
- **DEP:** Ch.8 (GKR/LogUp), Ch.11 (the PCS each zkVM picks), Ch.12 (the SNARK), Ch.16 (folding for IVC-based zkVMs).

**Chapter 22 — Midnight as the Integrating Case Study, and the Road Ahead**
- §22.1 Midnight through all seven layers, end to end (BLS12-381 ceremony → Compact → disclose() → ZKIR → Halo2/UltraPlonk → Poseidon/Jubjub → three-token verifier) · §22.2 Where Midnight validates the seven-layer model and where it challenges it · §22.3 The three frontiers (performance largely crossed, security active, privacy approaching) · §22.4 The seven open questions; is "seven" the right number?
- **[Hook]** One real system, dissected layer by layer, with every layer now something you can *build*, not just name — the book's promise, redeemed on a live target.
- **[Payload]** The full Midnight mapping as capstone; the open-problems agenda; the coda returning to the trust-decomposition thesis with the engine behind it.
- **[Graph]** C3 (Midnight, Compact, ZKIR, Poseidon, BLS12-381), C11 (Halo2/UltraPlonk). god-node Midnight (79). Keeps the book's signature running case study, now as a *synthesis* rather than a recurring aside.
- **DEP:** all prior parts (capstone).

---

## 3. Reading-order rationale (prerequisite / learning-path logic)

The book has **two interleaved orderings**, and the design makes both monotone:

1. **The narrative ordering (the seven layers).** Parts I→V walk the layers in roughly their causal order — setup, language, witness, arithmetization, proof system, primitives, verifier — so the reader keeps Hoskinson's mental model. *But* the layers are deliberately **resequenced** around the engine: Layer 1 (setup) and Layer 6 (primitives) are pulled to *after* the engine (Ch.17–18) because an SRS and a hardness assumption only make sense once you know the scheme they serve. This fixes a latent bug in the current book, which explains the trusted-setup ceremony (Ch.2) before the reader knows what KZG even is.

2. **The dependency ordering (the engine).** Part III is a **topological sort of the proof-systems literature**. The invariant — *no chapter uses a tool an earlier chapter has not built* — is what forces the chain:
   - You cannot test polynomial equality (Ch.7) without the random-evaluation idea (Ch.6).
   - You cannot run sum-check (Ch.8) without the MLE and Schwartz–Zippel (Ch.7).
   - You cannot appreciate PCP/MIP succinctness (Ch.9) without an interactive proof to compress (Ch.8).
   - You cannot define an IOP (Ch.10) without the oracle/spot-check paradigm (Ch.9).
   - You cannot realize an IOP's oracles (Ch.11) without first having the abstract IOP (Ch.10).
   - You cannot state IOP+PCS=SNARK (Ch.12) without *both* halves (Ch.10, Ch.11).
   - You cannot contrast Groth16's QAP route (Ch.13) without the IOP route to contrast it against (Ch.12) and the R1CS to arithmetize (Ch.5).
   - You cannot make either route non-interactive and security-modeled (Ch.14) without the routes (Ch.12–13) and the random coins (Ch.6).
   - You cannot recurse or fold (Part IV) without a finished, non-interactive SNARK and FS-in-circuit (Ch.12, 14).

The front matter (Parts I–II) is **intuition + statement**: it gives the reader the *thing to be proved* (a constraint system + witness) and the *promises* (completeness/soundness/ZK) before any machinery, satisfying Feynman globally — the whole engine is motivated before a single proof appears. Parts IV–V are **recombination + deployment**: nothing new is built from scratch; everything is the engine reused, scaled, attacked, or applied.

---

## 4. What's new vs the current 14-chapter book

**Structural changes.** The current book is 14 chapters / 3 parts, organized *purely* by the seven layers, with the proof system (Layer 5) compressed into one chapter (Ch.6) that *names* sum-check, recursion, folding, the three families, and Fiat–Shamir in a few pages each. My design promotes that single overloaded chapter into a **9-chapter engine (Part III)** and resequences setup/primitives to follow it. Net: 14→22 chapters, 3→5 parts.

**The Tier-1 "named but never built" concepts — each now has a constructed home:**

| Tier-1 absent/fragmentary concept | Was | Now built in |
|---|---|---|
| Sum-Check Protocol (god-node, deg 115, absent as standalone) | one ½-page aside in Ch.5 | **Ch.8 §8.2–8.3**, full round structure + soundness |
| Interactive Oracle Proof / Polynomial-IOP (absent) | not present | **Ch.10**, the modular frame |
| GKR (absent except "LogUp-GKR") | name only | **Ch.8 §8.4**, layer-by-layer sum-check |
| Multilinear Extension (absent) | not present | **Ch.7 §7.3**, constructed |
| KZG construction (deg 96, absent as construction) | label only | **Ch.11 §11.2** + anchored in **Ch.18** SRS |
| Bilinear pairing mechanics (thin) | asserted | **Ch.11 §11.2 / Ch.17 §17.2**, Miller loop + embedding degree |
| QAP construction (thin) | one sentence | **Ch.13 §13.2**, R1CS→divisibility |
| Grand-product / permutation argument (absent) | "wires must match" | **Ch.10 §10.4**, the accumulator Z |
| AGM / non-falsifiable assumptions (absent) | not present | **Ch.14 §14.4**, with Gentry–Wichs |
| MIP / PCP / low-degree testing / Merkle compilation (absent) | not present | **Ch.9**, the succinctness theory |
| Schwartz–Zippel (under-covered) | mentioned | **Ch.7 §7.4**, proved and reused everywhere |
| Reed–Solomon fingerprinting / Freivalds (absent) | not present | **Ch.6**, the engine's first principle |
| Linear PCP / GGPR / Pinocchio / LIP (absent) | not present | **Ch.13**, the pairing-SNARK lineage |
| Fiat–Shamir soundness / ROM / correlation intractability (thin) | bug stories only | **Ch.14**, the transform + its security model |
| Dory / Brakedown / Ligero / Hyrax / Basefold (absent) | not present | **Ch.11 §11.5–11.6** |
| The IOP+PCS=SNARK recipe (absent as a stated theorem) | implicit | **Ch.12**, the explicit assembly |

**Tier-2 recursion groundwork** (recursive composition deg 83, IVC, PCD, accumulation, cycles of curves, recursion-vs-folding) gets a proper **2-chapter Part IV (Ch.15–16)** instead of a few pages in Ch.6, and the reader arrives *warm* because Ch.1 plants the roadmap pointer the current book lacks.

**Tier-3/4/5 applications and family members** are rehomed into Part V (Ch.19–21): VDFs, zkTLS, proof of solvency, zkBridge, media provenance/C2PA, ZK SBOM, verifiable delegation, the five-class vulnerability taxonomy, real-time proving — all currently absent — plus Marlin/Spartan/Aurora/Gemini and the four "beyond-the-outline" folding gaps (Neo, reduction of knowledge, Sangria, bootstrapping↔IVC).

**What's preserved.** The seven-layer thesis, the trust-decomposition framing, the Midnight running case study (now the *capstone* Ch.22 rather than scattered asides), the four-philosophy DSL taxonomy, the Layer-6 trilemma (now *derived* in Ch.11), and the open-questions coda.

---

## 5. Risks / tradeoffs of this structure

1. **Difficulty spike in Part III.** Nine consecutive theory chapters are the steepest stretch in the book; a casual reader could stall at Ch.8–11. *Mitigations:* every engine chapter still opens with a Feynman analogy and a worked toy (the 4×4 Sudoku and a 3-gate circuit thread through as running examples); each chapter ends with a "what you can now build" recap; Parts I–II and IV–V are readable largely on intuition, so a non-specialist can skim the engine's hooks and skip the payloads on a first pass. A explicit "two reading tracks" note (practitioner vs theorist) belongs in Ch.1 §How-to-read.

2. **Resequencing the seven layers risks reader disorientation.** Pulling setup (L1) and primitives (L6) to *after* the engine departs from the book's existing 1→7 march. *Mitigation:* Ch.2 presents the layers as a *causal DAG, not a stack* (the current book already argues this), which licenses non-linear ordering; each engine chapter cross-references the layer it serves.

3. **The two-route presentation (IOP-SNARK in Ch.12, QAP/Groth16 in Ch.13) could read as redundant.** *Mitigation:* this is deliberate and high-value — Groth16 is the single most-deployed system (god-node deg 116) and teaching it *as a contrast* to the IOP route is what makes both legible. The risk is length, not coherence.

4. **Frontier volatility.** Lattice folding (Neo, Symphony, LatticeFold+), small-field zkVMs, and real-time proving move fast; concrete chapters (17, 21) will date. *Mitigation:* the engine (Ch.6–14) is essentially timeless mathematics and ages slowly; volatility is quarantined in Parts IV–V where it can be revised without touching the core.

5. **Page budget.** 22 chapters with a rigorous engine is a large book (likely 500+ pages). *Mitigation:* the engine chapters are short and dense (a sum-check chapter is ~15 pages, not 40); the seven-layer chapters already exist in draft and need rehoming, not rewriting. If a cut is forced, Ch.13 (Groth16/QAP) and Ch.9 (MIP/PCP) are the candidates to compress, since the IOP route (Ch.10–12) is the load-bearing one for modern systems — but cutting either weakens the "built from first principles" guarantee that is this lens's entire value proposition.

6. **Single-author voice across a theory core.** The engine demands sustained mathematical exposition that must stay in Hoskinson's voice rather than drifting into textbook register (the graph ingested Thaler's textbook — the temptation to lift its structure is real). *Mitigation:* the analogy-first mandate and the running examples are the voice-anchors; each chapter's hook must be authored before its payload.
