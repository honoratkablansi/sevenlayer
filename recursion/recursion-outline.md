# Recursive Proof Composition: A Three-Chapter Treatment

*Annotated outline for a book on zero-knowledge proofs. Each subsection includes a working paragraph describing its content and scope, followed by recommended references. Chapter 1 surveys recursion as a whole; Chapter 2 is a deep dive into folding schemes; Chapter 3 covers applications. Chapter 1 is self-contained — a reader may skip Chapter 2 and still follow Chapter 3.*

---

## Chapter 1: Recursive Proof Composition

### 1.1 Why Recursion? The Motivating Problems

#### 1.1.1 The verifier's dilemma

Succinct proofs solve the problem of verifying *one* large computation cheaply, but they do not by themselves solve the problem of verifying an *unbounded* sequence of computations: a blockchain that grows forever, a server that streams results indefinitely, a pipeline whose stages are produced by different parties. This subsection frames the gap precisely — verifier time and proof size may be sublinear in one statement, yet the number of statements grows without bound — and motivates the need for proofs that can absorb other proofs.

*References: Valiant, "Incrementally Verifiable Computation" (TCC 2008); Ben-Sasson, Chiesa, Tromer, Virza, "Scalable Zero Knowledge via Cycles of Elliptic Curves" (CRYPTO 2014).*

#### 1.1.2 Three core capabilities

Recursion buys three distinct things, and conflating them causes confusion later: **compression** (aggregate many independent proofs into one, shrinking on-chain or on-wire verification cost), **incrementality** (prove a long-running computation step by step, with per-step work independent of history), and **composability** (treat proofs as first-class values that other proofs can reason about, enabling multi-party and modular designs). Each capability maps to different applications in Chapter 3, and different constructions in 1.3 optimize for different ones.

*References: Bitansky, Canetti, Chiesa, Tromer, "Recursive Composition and Bootstrapping for SNARKs and Proof-Carrying Data" (STOC 2013).*

#### 1.1.3 A worked intuition: the proof of a proof

Before any formalism, the reader should see the trick concretely: a verifier is just an algorithm, an algorithm can be expressed as a circuit, and a SNARK can prove satisfiability of any circuit — including the verifier's own. We walk a toy example (proving knowledge of a chain of two facts via one outer proof) and surface the immediate obstacles: the verifier circuit must be smaller than the computation it attests to, and the arithmetic the verifier performs may not match the field the proof system natively speaks.

*References: Ben-Sasson, Chiesa, Tromer, Virza (CRYPTO 2014); Chiesa, Tromer, "Proof-Carrying Data and Hearsay Arguments from Signature Cards" (ICS 2010).*

#### 1.1.4 Historical arc

A short narrative history orients the reader: Valiant's IVC (2008) established the concept; Chiesa–Tromer's PCD (2010) generalized it; BCTV's curve cycles (2014) made full recursion plausible; Coda/Mina (design 2018, ePrint 2020, mainnet 2021) shipped the first recursive blockchain; Halo (2019) removed trusted setup via accumulation; Nova (2021) replaced SNARK verification with folding; small-field STARKs (Plonky2, 2022 onward) made hash-based recursion fast; and by 2024–26, recursion-heavy zkVMs were proving Ethereum mainnet blocks in real time. The arc shows a consistent theme: each generation moved more work out of the recursive step.

*References: Valiant (TCC 2008); Bowe, Grigg, Hopwood, "Halo: Recursive Proof Composition without a Trusted Setup" (ePrint 2019/1021); Kothapalli, Setty, Tzialla, "Nova" (CRYPTO 2022); Polygon Zero, "Plonky2" (2022); Succinct, "SP1 Hypercube" (2025).*

### 1.2 Foundations

#### 1.2.1 Incrementally Verifiable Computation (IVC)

Formal definition of IVC: for a step function F, the prover maintains a proof Π_i attesting that z_i = F^(i)(z_0); updating to Π_{i+1} requires work independent of i, and verifying any Π_i requires work independent of i. We emphasize the two independence conditions, since they are what distinguish IVC from naive "prove the whole history each time" approaches, and we discuss completeness, knowledge soundness, and the (optional) zero-knowledge property in this setting.

*References: Valiant (TCC 2008); Bitansky et al. (STOC 2013).*

#### 1.2.2 Proof-Carrying Data (PCD)

PCD generalizes IVC from a chain to a directed acyclic graph: each node in a distributed computation receives messages with attached proofs, performs local computation, and emits a message whose proof attests to the entire history behind it — across mutually distrusting parties. We define compliance predicates and show how IVC is the special case of a path graph. The chapter's running promise: Chapter 3's SBOM application (§3.3.1) is the cleanest real-world PCD instance, where the DAG is a software dependency graph.

*References: Chiesa, Tromer (ICS 2010); Bünz, Chiesa, Mishra, Spooner, "Proof-Carrying Data from Accumulation Schemes" (TCC 2020).*

#### 1.2.3 The succinctness threshold

Not every proof system can recurse. The verifier circuit must be asymptotically (and concretely!) smaller than the statements being proven, or the recursion diverges — each layer is bigger than the last. We formalize "fully succinct" verification, examine which systems clear the bar (pairing-based SNARKs trivially; FRI-based STARKs with care; bulletproof-style linear verifiers not at all without help), and preview how accumulation and folding deliberately *relax* this requirement by deferring the expensive checks.

*References: Bitansky et al. (STOC 2013); Bünz, Chiesa, Mishra, Spooner (TCC 2020); Chiesa, Ojha, Spooner, "Fractal: Post-Quantum and Transparent Recursive Proofs from Holography" (EUROCRYPT 2020).*

#### 1.2.4 Security subtleties

Recursive security arguments are weaker than they appear. Knowledge soundness is proven via an extractor, and recursion composes extractors: extraction blows up with recursion depth, so theorems typically hold only for constant or logarithmic depth. Worse, in-circuit verification requires instantiating the random oracle with a concrete hash, a heuristic with no security proof — and recent work shows it can fail catastrophically for specific protocols. This subsection is deliberately early so the reader carries appropriate skepticism through the constructions.

*References: Bitansky et al. (STOC 2013); Chiesa, Ojha, Spooner (EUROCRYPT 2020); Khovratovich, Rothblum, Soukhanov, "How to Prove False Statements: Practical Attacks on Fiat–Shamir" (ePrint 2025/118).*

### 1.3 Construction Strategies (the core taxonomy)

#### 1.3.1 Full recursion: embedding a complete verifier in-circuit

The original strategy: write the entire verifier of the inner proof system as a circuit and prove it. For pairing-based SNARKs the verifier is tiny (a few pairings), but the field-mismatch problem bites: the verifier's arithmetic lives in the base field of the curve, while the circuit's arithmetic lives in the scalar field. The classical fix is a *cycle* of elliptic curves — two curves, each one's scalar field equal to the other's base field — alternating between them at each recursion layer. We cover MNT cycles (pairing-friendly but cryptographically inefficient at high security), the Pasta curves (efficient but pairing-free, motivating accumulation), and why finding good cycles remains a hard open problem.

*References: Ben-Sasson, Chiesa, Tromer, Virza (CRYPTO 2014); Hopwood, "The Pasta Curves" (Zcash, 2020); Chiesa, Chua, Weidner, "On Cycles of Pairing-Friendly Elliptic Curves" (2019).*

#### 1.3.2 Atomic accumulation: Halo's insight

Halo observed that the expensive part of verifying an inner-product-argument proof — a large multi-scalar multiplication — need not be performed inside the circuit at each step. Instead, the claim is *accumulated*: each step folds the deferred check into a running accumulator, verified once at the very end. This subsection presents accumulation schemes as formalized by Bünz–Chiesa–Mishra–Spooner, distinguishes atomic from split accumulation, and shows how this removed the trusted setup from practical recursion. Accumulation is the conceptual bridge to folding: it defers *part* of verification; folding (Chapter 2) defers essentially all of it.

*References: Bowe, Grigg, Hopwood (ePrint 2019/1021); Bünz, Chiesa, Mishra, Spooner (TCC 2020); Bünz, Chiesa, Lin, Mishra, Spooner, "Proof-Carrying Data without Succinct Arguments" (CRYPTO 2021).*

#### 1.3.3 Folding schemes — the survey view

Folding schemes abandon the idea of producing a succinct proof at each step. Instead, a folding scheme reduces the task of checking two instances of a relation to checking a single folded instance; iterating yields IVC where the recursive circuit performs only a couple of group scalar multiplications — orders of magnitude cheaper than any in-circuit verifier. The price: no standalone proof exists mid-computation, soundness checks are deferred until a final SNARK compresses the running instance, and an additively homomorphic commitment scheme becomes a load-bearing assumption. This subsection gives the idea, the cost profile, and the position in the design space — Chapter 2 develops the machinery in full.

*References: Kothapalli, Setty, Tzialla, "Nova: Recursive Zero-Knowledge Arguments from Folding Schemes" (CRYPTO 2022); see Chapter 2 references for the family.*

#### 1.3.4 STARK recursion

FRI-based STARKs are transparent and plausibly post-quantum, and their verifiers consist mostly of hash evaluations — expensive in-circuit until the field shrank. This subsection explains why small fields (Goldilocks 2^64−2^32+1, BabyBear, Mersenne-31 via circle STARKs) plus algebraic hashes (Poseidon) and lookup arguments made FRI verification in-circuit practical, covers the Fractal lineage (the first transparent recursion) and the Plonky2/Plonky3/Stwo engineering line, and quantifies the recursion overhead that production systems now achieve.

*References: Chiesa, Ojha, Spooner, "Fractal" (EUROCRYPT 2020); Polygon Zero, "Plonky2: Fast Recursive Arguments with PLONK and FRI" (2022); Haböck, Levit, Papini, "Circle STARKs" (ePrint 2024/278); Ben-Sasson, Bentov, Horesh, Riabzev, "Scalable, Transparent, and Post-Quantum Secure Computational Integrity" (ePrint 2018/046).*

#### 1.3.5 Hybrid pipelines: the dominant production pattern

Almost every production system today is a pipeline: a fast, parallel STARK prover handles bulk execution; one or more layers of recursive STARKs shrink and aggregate the resulting proofs; and a final SNARK wrap (Groth16, PLONK, or FFLONK) produces a proof small and cheap enough for on-chain verification. We dissect the pattern, including the uncomfortable tradeoff that the final wrapper often reintroduces a trusted setup — which is exactly why Ethereum's L1 zkEVM requirements forbid trusted-setup recursive wrappers — and analyze where latency accumulates in the stack.

*References: Polygon zkEVM documentation (STARK→FFLONK pipeline); RISC Zero, "Proof System Overview"; Succinct, "SP1 Hypercube" (2025); Ethereum Foundation, "Shipping an L1 zkEVM: Realtime Proving" (2025).*

#### 1.3.6 Comparative analysis

A single table scores all five strategies — full recursion, atomic accumulation, folding, STARK recursion, hybrids — on recursive-step prover cost, final verifier cost, setup assumptions, post-quantum readiness, support for non-uniform computation, and engineering maturity. The table is the chapter's payoff and the reference point that Chapter 3's decision framework (§3.7) maps applications onto.

*References: synthesizes the per-strategy references above; Thaler, "Proofs, Arguments, and Zero-Knowledge" (survey text) for background framing.*

### 1.4 Architectural Patterns

#### 1.4.1 Aggregation trees

When the goal is compressing N independent proofs, recursion need not be a chain: arrange proofs as leaves of a tree and recursively verify pairs (or wider arities) upward. Tree shape is a tuning knob — deeper trees reduce per-node prover cost and parallelize naturally; shallower trees reduce latency and total work. We work the zkTree-style cost model, including the observed tradeoff that splitting the final wrap circuit decreases prover time while increasing on-chain verification cost.

*References: "zkTree: A Zero-Knowledge Recursion Tree with ZKP Membership Proofs" (ePrint 2023/208); Nebra, "Universal Proof Aggregation" (2023).*

#### 1.4.2 Continuations and sharding

Modern zkVMs prove enormous executions by splitting the trace into chunks ("continuations" or "shards"), proving chunks in parallel across a GPU cluster, and recursively merging chunk proofs while checking boundary consistency (registers, memory state) between adjacent chunks. This is the single most economically important recursion pattern today; we detail the consistency-checking mechanics, the memory-argument handoff between shards, and the wall-clock arithmetic that makes real-time block proving possible.

*References: RISC Zero, "Continuations" (2023); Succinct, "SP1 Hypercube" (2025); Ethereum Foundation realtime-proving blog (2025).*

#### 1.4.3 Streaming and concurrent recursion

When inputs arrive over time — signatures gossiped across a network, sensor readings, log entries — recursion can run *concurrently* with input arrival: fold or aggregate each item as it lands, so that when the batch closes, the proof is already nearly done. We analyze the latency-hiding effect and its limits, with batch signature verification as the running example.

*References: "BEATS: Batch ECDSA Transaction verification Scheme" and related IVC-based batch-verification literature; Mina's Hazook recursive rollup design (2024).*

#### 1.4.4 Recursion inside zkVMs

A vertical tour of one zkVM's proof stack, tying together 1.3 and 1.4: RISC-V execution traced and chunked; per-chunk STARKs; a recursion tree of "compress" circuits; a wrap layer switching proof systems; and a final on-chain verifier measured in hundreds of thousands of gas. The reader leaves able to read any zkVM's architecture diagram and identify which recursion strategy each layer uses and why.

*References: Succinct SP1 documentation; RISC Zero technical docs; Arun, Setty, Thaler, "Jolt: SNARKs for Virtual Machines via Lookups" (ePrint 2023/1217) as a contrasting lookup-centric design.*

### 1.5 Engineering Realities and Pitfalls

#### 1.5.1 Recursion shifts cost, it doesn't eliminate it

A design that looks clean on paper can be dominated by in-circuit verification overhead, witness-size growth across layers, or prover memory pressure. This subsection builds a cost-accounting discipline: for each recursion layer, tally constraints added by the embedded verifier, commitment costs, and memory high-water marks — and compare against the non-recursive baseline of simply re-running the computation.

*References: practitioner literature on recursive circuit design (e.g., zkDev, "Designing Efficient Recursive ZK Circuits," 2026); Plonky2 whitepaper benchmarks.*

#### 1.5.2 Compatibility hell

Recursion forces alignment across layers that were never designed together: scalar fields vs. base fields, curve choices, hash functions (in-circuit-friendly Poseidon vs. native Keccak), and Fiat–Shamir transcript formats. Non-native field arithmetic can inflate a verifier circuit by orders of magnitude. We catalogue the standard mitigations — curve cycles, field towers, algebraic hashes, transcript standardization — and when each is worth its complexity.

*References: Hopwood, Pasta curves notes; Kothapalli, Setty, "CycleFold" (ePrint 2023/1192); Grassi et al., "Poseidon: A New Hash Function for Zero-Knowledge Proof Systems" (USENIX Security 2021).*

#### 1.5.3 Binding verification keys and statements safely

The soundness bugs that actually occur in recursive systems are rarely deep cryptography; they are binding failures — a circuit that verifies *a* proof but not a proof *for the intended verification key*, or public inputs spliced across layers without domain separation. We present an anatomy of real vulnerabilities and a checklist: bind VK hashes into statements, domain-separate transcripts, and treat every cross-layer interface as adversarial.

*References: Nguyen, Boneh, Setty, "Revisiting the Nova Proof System on a Cycle of Curves" (ePrint 2023/969); public audit reports of recursive provers (e.g., zkVM audit literature).*

#### 1.5.4 When *not* to recurse

Recursion is not the only aggregation tool. Batch verification, pairing-based aggregation (e.g., aggregating Groth16 proofs via SnarkPack), SNARK-friendly signature aggregation, and simply proving a bigger circuit are often simpler and faster at moderate scale. We give crossover heuristics: recursion wins when statements are heterogeneous, arrive over time, exceed single-prover memory, or must compose across parties.

*References: Gailly, Maller, Nitulescu, "SnarkPack: Practical SNARK Aggregation" (FC 2022); Thaler, "Proofs, Arguments, and Zero-Knowledge."*

#### 1.5.5 Hardware and economics

Real-time recursion is a systems problem: GPU clusters in the tens-to-hundreds of cards, six-figure cluster costs falling fast (real-time Ethereum proving went from ~200 RTX 4090s in early 2025 to 16 RTX 5090s by 2026), prover markets that commoditize the work, and the open question of whether proving centralizes. We give the cost model and the decentralization arguments on both sides.

*References: Succinct, "Real-Time Proving with 16 GPUs" (2026); Ethereum Foundation realtime-proving requirements (2025); Aligned Layer, "The Year of zkVM Real-Time Proving" (2025).*

### 1.6 Theoretical Frontiers

#### 1.6.1 Fully post-quantum recursion end to end

STARK recursion is plausibly post-quantum, but production pipelines still wrap in pairing-based SNARKs, and folding rests on discrete-log commitments. We survey what a fully PQ recursive stack requires — hash-based or lattice-based components at every layer — and the state of each gap.

*References: Chiesa, Ojha, Spooner, "Fractal" (EUROCRYPT 2020); Boneh, Chen, "LatticeFold" (ePrint 2024/257); Ethereum "Lean" roadmap materials on hash-based signature aggregation.*

#### 1.6.2 Minimizing the recursion gap

The "recursion gap" is the multiplicative overhead of proving a verifier versus just running it. We review the levers — smaller fields, better in-circuit hashes, lookup arguments, folding's near-elimination of the embedded verifier — and ask how close to zero the gap can go in principle.

*References: Plonky2/Plonky3 engineering reports; Kothapalli, Setty, "HyperNova" (ePrint 2023/573); circle-STARK literature.*

#### 1.6.3 Formalizing deep-recursion security

Extractor blowup limits theorems to bounded depth, yet deployed systems recurse thousands of times. Closing this theory–practice gap — via straight-line extraction in idealized models, or new analyses of Fiat–Shamir in recursive settings — is among the field's most important open problems, sharpened by recent concrete attacks on Fiat–Shamir instantiations.

*References: Bitansky et al. (STOC 2013); Khovratovich, Rothblum, Soukhanov (ePrint 2025/118); Chiesa–Spooner line of work on accumulation security.*

#### 1.6.4 PCD as a general-purpose programming model

If proofs can flow along arbitrary computation graphs, "verifiability" becomes a property of distributed software generally, not just blockchains. We speculate carefully: compiler support for compliance predicates, PCD-native protocols, and what standard libraries for proof-carrying computation might look like.

*References: Chiesa, Tromer (ICS 2010); Bünz, Chiesa, Lin, Mishra, Spooner (CRYPTO 2021).*

### Chapter 1 Exercises

1. Implement a toy IVC for the Fibonacci sequence in a proof framework of your choice; measure how per-step prover time scales with step count and explain the result.
2. Embed a Merkle-path verifier in-circuit using (a) a SNARK-friendly hash and (b) SHA-256; compare constraint counts and explain the gap.
3. Design an aggregation tree for N = 1,024 signatures with arity 2, 4, and 8; derive total prover work and end-to-end latency for each, assuming a fixed per-node cost model.
4. Take a published zkVM architecture diagram and label each layer with its strategy from the §1.3 taxonomy; identify which layer dominates latency and which dominates cost.

---

## Chapter 2: Folding Schemes in Depth

### 2.1 From Accumulation to Folding

#### 2.1.1 The lineage: deferring more and more

Halo deferred one expensive polynomial-commitment check per step; the natural question is how much of verification can be deferred. Folding answers: essentially all of it. This subsection traces the intellectual line from atomic accumulation (defer the MSM) through split accumulation (defer with cheaper per-step checks) to folding (defer even the proof — fold raw *instances* of the relation itself), and explains why each weakening of the per-step guarantee bought a cheaper recursive circuit.

*References: Bowe, Grigg, Hopwood, "Halo" (ePrint 2019/1021); Bünz, Chiesa, Mishra, Spooner (TCC 2020); Bünz, Chiesa, Lin, Mishra, Spooner (CRYPTO 2021); Kothapalli, Setty, Tzialla, "Nova" (CRYPTO 2022).*

#### 2.1.2 Folding schemes as a primitive

Formal definition: a folding scheme for a relation R is a protocol that reduces checking two instance–witness pairs to checking one, with completeness, knowledge soundness, and (optionally) zero-knowledge. The key theorem is that this strictly weaker primitive — it is not an argument of knowledge, produces no succinct proof, and convinces no one of anything in isolation — nevertheless suffices for IVC. "Weaker" is the feature: weaker primitives admit simpler, faster realizations.

*References: Kothapalli, Setty, Tzialla (CRYPTO 2022), §3 (definitions).*

#### 2.1.3 What you give up

An honest accounting of folding's costs: no standalone proof exists mid-computation (a participant cannot convince a third party of progress without running the final compression); the running instance is not succinct in the witness; an additively homomorphic commitment is mandatory, which currently means discrete-log-type assumptions and no straightforward post-quantum path; and the final compression SNARK is a substantial engineering component in its own right.

*References: Kothapalli, Setty, Tzialla (CRYPTO 2022); Boneh, Chen, "LatticeFold" (ePrint 2024/257) for the PQ gap.*

### 2.2 Preliminaries

#### 2.2.1 R1CS and why naive instances don't fold

R1CS refresher: an instance is satisfied when Az ∘ Bz = Cz for witness vector z. The obvious folding attempt — take a random linear combination z = z₁ + r·z₂ — fails because the constraint is quadratic: expanding A(z₁+r·z₂) ∘ B(z₁+r·z₂) produces cross terms A z₁ ∘ B z₂ + A z₂ ∘ B z₁ that satisfy no instance. We compute the cross term explicitly for a two-constraint example so the reader feels the problem before seeing the fix.

*References: Kothapalli, Setty, Tzialla (CRYPTO 2022), §4; Thaler, "Proofs, Arguments, and Zero-Knowledge," R1CS chapters.*

#### 2.2.2 Relaxed R1CS

The fix: enlarge the relation. Relaxed R1CS adds a scalar u and an error vector E, requiring Az ∘ Bz = u·(Cz) + E. Standard R1CS embeds as u = 1, E = 0; crucially, the relaxation is exactly shaped to absorb the cross terms — folding two relaxed instances yields a relaxed instance whose error vector accumulates the (committed) cross term. We give the geometric intuition: relaxation turns the satisfiability set into something closed under the right notion of interpolation.

*References: Kothapalli, Setty, Tzialla (CRYPTO 2022), §4.1.*

#### 2.2.3 Commitments for folding

The verifier never sees witnesses or error vectors — only additively homomorphic commitments to them (Pedersen commitments over an elliptic curve in Nova). Homomorphism is what lets the verifier fold commitments with two scalar multiplications while the prover folds the underlying vectors. We state the binding/hiding requirements, note that hiding is what makes zero-knowledge available, and flag that this is precisely where post-quantum folding gets stuck.

*References: Pedersen (CRYPTO 1991); Kothapalli, Setty, Tzialla (CRYPTO 2022); Boneh, Chen (ePrint 2024/257).*

### 2.3 Nova: The Reference Construction

#### 2.3.1 The folding protocol in full

The complete two-instance folding protocol: the prover computes the cross term T and sends a commitment to it; the verifier samples a random challenge r; both parties fold instances (u, x, com(W), com(E)) via linear combination; the prover folds witnesses correspondingly. We give both algorithms line by line and prove completeness on the spot, with knowledge soundness deferred to §2.6.1.

*References: Kothapalli, Setty, Tzialla (CRYPTO 2022), §4.2.*

#### 2.3.2 Making it non-interactive

Fiat–Shamir applied to the folding challenge: hash the instances and the cross-term commitment to derive r. This is innocuous on paper and subtle in practice — the hash runs *inside* the next step's circuit, so it must be in-circuit-friendly, and its instantiation is exactly the heuristic flagged in §1.2.4 and revisited in §2.6.3.

*References: Kothapalli, Setty, Tzialla (CRYPTO 2022); Fiat, Shamir (CRYPTO 1986).*

#### 2.3.3 From folding to IVC: the augmented circuit

The heart of Nova: the step circuit is augmented so that, in addition to computing F, it verifies the previous fold — two group scalar multiplications and a hash, roughly 10^4 constraints rather than the 10^6+ of an embedded SNARK verifier. We trace exactly what the augmented circuit checks, how the running instance and the fresh instance thread through public IO, and the bookkeeping (step counters, IO hashing) that the soundness analysis depends on — bookkeeping whose subtlety §2.6.4 makes vivid.

*References: Kothapalli, Setty, Tzialla (CRYPTO 2022), §5; Nguyen, Boneh, Setty (ePrint 2023/969).*

#### 2.3.4 Finishing the job: compression and zero knowledge

At the end of the computation, the prover holds a relaxed R1CS instance whose witness is full-sized; a final SNARK — Spartan, in the reference implementation — proves knowledge of the satisfying witness, yielding a succinct, zero-knowledge proof of the entire execution. We cover why Spartan's structure (sum-check over multilinear extensions, no FFTs) pairs naturally with Nova, and where zero-knowledge enters (the final argument, plus randomization of commitments).

*References: Setty, "Spartan: Efficient and General-Purpose zkSNARKs without Trusted Setup" (CRYPTO 2020); Kothapalli, Setty, Tzialla (CRYPTO 2022), §6.*

#### 2.3.5 A complete worked example

One example carried through every subsection above — iterated hashing (or the MinRoot VDF), chosen because the step function is trivial and all attention stays on the recursion machinery. The example appears with concrete constraint counts, commitment sizes, and prover timings at each stage, and reappears in the exercises.

*References: Khovratovich et al., "MinRoot" VDF candidate (2022); Nova reference implementation (github.com/microsoft/Nova).*

### 2.4 The Family Tree

#### 2.4.1 SuperNova: non-uniform IVC

Nova folds repeated applications of *one* step function; real machines execute *many* instruction types. SuperNova supports a set of step functions F₁…F_k with per-step cost depending only on the executed instruction, not on k — maintaining one running instance per instruction type, selected by a program counter. This is the conceptual bridge from folding to VMs, and we discuss why naive alternatives (a universal switch circuit) reintroduce exactly the costs folding was meant to kill.

*References: Kothapalli, Setty, "SuperNova: Proving Universal Machine Executions without Universal Circuits" (ePrint 2022/1758).*

#### 2.4.2 CCS and HyperNova

Customizable Constraint Systems (CCS) generalize R1CS, Plonkish, and AIR under one umbrella with higher-degree constraints; HyperNova folds CCS instances using a sum-check-based "multifolding" that keeps the verifier's work logarithmic even as constraint degree grows, and avoids committing to cross-term error vectors entirely. We present CCS first as a unifier of arithmetizations, then multifolding as the technical core, and note the practical payoff: high-degree custom gates without per-gate folding penalties.

*References: Setty, Thaler, Wahby, "Customizable Constraint Systems for Succinct Arguments" (ePrint 2023/552); Kothapalli, Setty, "HyperNova: Recursive Arguments for Customizable Constraint Systems" (ePrint 2023/573).*

#### 2.4.3 ProtoStar and ProtoGalaxy: folding as a compiler

ProtoStar reframes folding generically: any special-sound protocol can be compiled into a folding/accumulation scheme, immediately yielding support for high-degree gates and — critically — lookup arguments with prover cost independent of table size. ProtoGalaxy refines the approach to fold many instances at once with sublinear verifier cost in the number of instances. The lesson: folding is not a bag of one-off tricks but an instance of a general transformation.

*References: Bünz, Chen, "ProtoStar: Generic Efficient Accumulation/Folding for Special-Sound Protocols" (ePrint 2023/620); Eagen, Gabizon, "ProtoGalaxy: Efficient ProtoStar-style Folding of Multiple Instances" (ePrint 2023/1106).*

#### 2.4.4 CycleFold: shrinking the second curve

Curve-cycle recursion traditionally duplicates the full augmented circuit on both curves. CycleFold's observation: the second curve is only needed for a handful of foreign-field group operations, so its circuit can shrink to a single scalar multiplication — about 1,500 multiplication gates — whose correctness is itself folded on the primary curve. This collapses the engineering surface of cycle-based folding and has been adopted across implementations.

*References: Kothapalli, Setty, "CycleFold: Folding-Scheme-Based Recursive Arguments over a Cycle of Elliptic Curves" (ePrint 2023/1192).*

#### 2.4.5 Mapping the tradeoffs

A comparison table across Nova, SuperNova, HyperNova, ProtoStar/ProtoGalaxy, and CycleFold-augmented variants: constraint-system generality, recursive-circuit size, lookup support, number of curve operations per step, prover memory, and implementation maturity. We close with guidance on which family member fits which workload — uniform iteration, VM execution, lookup-heavy circuits, many-instance aggregation.

*References: synthesizes the family references above; Sonobe library documentation (PSE/0xPARC) for implementation-level comparisons.*

### 2.5 Implementation Engineering

#### 2.5.1 Curve cycles in practice

The Pasta curves (Pallas/Vesta) as the standard non-pairing cycle; what non-native arithmetic costs when ignored (orders-of-magnitude circuit blowup); and how CycleFold changes the calculus by quarantining foreign-field work. Includes the practical checklist for choosing curves: field sizes vs. target hash functions, endomorphism availability, and ecosystem/library support.

*References: Hopwood, Pasta curves specification; Kothapalli, Setty, "CycleFold" (ePrint 2023/1192).*

#### 2.5.2 Cost anatomy of a folding step

Where the time actually goes: the prover's MSMs for witness and cross-term commitments dominate; the augmented circuit's synthesis and witness generation come second; memory is governed by the full witness vector, which folding keeps resident. We benchmark a folding step against a comparable recursive-STARK step and derive the crossover: folding wins on uniform, commitment-bound workloads; recursive STARKs win when hashing is cheap relative to MSMs or when standalone per-step proofs are required.

*References: Nova reference implementation benchmarks; Plonky2/Plonky3 benchmarks; zkVM benchmark literature (e.g., ASPLOS 2026 zkVM evaluation studies).*

#### 2.5.3 Parallel and tree-shaped folding

Chain-shaped IVC is sequential by construction — a problem for multi-core and distributed provers. We cover binary-tree folding (fold left and right halves of the computation independently, then fold the results), its relationship to PCD, the consistency conditions tree nodes must check, and the memory/latency profile compared to chains. This is also where folding meets the aggregation-tree pattern of §1.4.1.

*References: Bünz, Chen, et al. on PCD from folding; "ParaNova"-style parallel folding literature; Sonobe documentation.*

#### 2.5.4 Libraries and benchmark methodology

A tour of the implementation landscape: the Microsoft Nova reference (Rust, Pasta curves, Spartan compression), Sonobe (arkworks-based, multiple folding schemes behind one API, Nova/HyperNova/ProtoGalaxy), Halo2-ecosystem accumulation (Pickles powering Mina), and folding modules inside larger stacks. We close with benchmark hygiene: report curve, field, commitment scheme, step-circuit size, and machine — single-number comparisons across schemes are nearly always misleading.

*References: github.com/microsoft/Nova; Sonobe documentation (PSE/0xPARC); Mina "Pickles" technical documentation; Veridise Nova article series for accessible exposition.*

### 2.6 Security of Folding Schemes

#### 2.6.1 Knowledge soundness of the folding reduction

The extraction argument: rewind the prover to obtain folded witnesses under multiple challenges, then solve the resulting linear system to recover witnesses for both original instances — a forking-lemma-style proof. We present it fully for Nova's scheme, since it is short enough to teach and representative of the genre, and note where the argument strains (extraction across many sequential folds compounds, echoing §1.2.4).

*References: Kothapalli, Setty, Tzialla (CRYPTO 2022), soundness proofs; Bünz, Chen, "ProtoStar" for the special-soundness view.*

#### 2.6.2 What deferred checking does and doesn't tell you

Mid-computation, the running instance proves nothing by itself: an unsatisfiable instance is detected only at final compression. We examine the consequences — a malicious participant in a multi-party fold can poison the accumulator undetectably until the end — and the mitigations (periodic compression checkpoints, per-contribution validity proofs) along with their costs.

*References: Kothapalli, Setty, Tzialla (CRYPTO 2022); multi-party folding discussions in the PCD-from-folding literature.*

#### 2.6.3 Fiat–Shamir in the IVC setting

The random oracle must be instantiated with a concrete hash that runs inside the circuit, and the adversary controls inputs to that hash across unboundedly many recursion steps. Recent results show concrete, practical attacks on Fiat–Shamir for certain protocols when instantiated this way — making this the sharpest known theory–practice gap in deployed recursion. We present the attack template, why folding's algebraic structure is or isn't implicated, and current hardening practices.

*References: Khovratovich, Rothblum, Soukhanov, "How to Prove False Statements" (ePrint 2025/118); Canetti, Goldreich, Halevi, "The Random Oracle Methodology, Revisited" (JACM 2004).*

#### 2.6.4 Bugs in the wild

Case study: the soundness attack on Nova's original cycle-of-curves implementation (Nguyen–Boneh–Setty), which exploited insufficient binding between the two curves' running instances to forge proofs of long computations — a textbook instance of §1.5.3's binding failures arising in a system designed by experts. We reconstruct the attack, the fix, and the general lesson: folding's simplicity lives in the protocol, not in the surrounding bookkeeping.

*References: Nguyen, Boneh, Setty, "Revisiting the Nova Proof System on a Cycle of Curves" (ePrint 2023/969).*

### 2.7 Folding Frontiers

#### 2.7.1 Lattice-based and post-quantum folding

LatticeFold and successors replace Pedersen commitments with Ajtai-style lattice commitments, confronting the core obstacle: lattice commitments are only homomorphic for *short* vectors, and folding's random linear combinations destroy shortness. We cover the decomposition techniques that manage norm growth, current performance gaps versus discrete-log folding, and what remains before a fully PQ folding pipeline is practical.

*References: Boneh, Chen, "LatticeFold: A Lattice-Based Folding Scheme and its Applications" (ePrint 2024/257); "LatticeFold+" (ePrint 2025/247).*

#### 2.7.2 Folding without curve cycles

Directions that drop elliptic curves entirely: folding over hash-based commitments, small-field folding compatible with STARK pipelines, and hybrid designs that fold where cheap and hash where necessary. The section is frankly exploratory — we mark what is published, what is folklore, and what is open.

*References: emerging literature on hash-based/small-field accumulation (e.g., Arc and related ePrint work); circle-STARK-adjacent folding proposals.*

#### 2.7.3 Streaming provers and memory-optimal folding

Folding keeps the full witness in memory; for very large steps this becomes the binding constraint. We survey streaming-prover techniques, witness-decomposition approaches, and the theoretical limits of memory-efficient IVC.

*References: streaming-prover literature for sum-check-based SNARKs; Nova memory-profile analyses in the implementation literature.*

#### 2.7.4 Open questions

A closing list with commentary: folding-based PCD with high in-degree nodes; lookup-heavy workloads at parity with lookup-native STARKs; formal verification of augmented circuits; tight security for unbounded-depth folding; and standardized transcripts enabling cross-implementation proof exchange.

*References: open-problem discussions in HyperNova, ProtoStar, and LatticeFold papers.*

### Chapter 2 Exercises

1. For the R1CS instance encoding x³ + x + 5 = 35, derive the cross term T for two satisfying assignments by hand and verify that the relaxed folded instance is satisfied.
2. Implement Nova's folding verifier as a circuit and count constraints; identify the fraction due to group operations vs. hashing.
3. Extend the worked example of §2.3.5 to two alternating step functions using SuperNova's program-counter mechanism; measure per-step overhead vs. single-function Nova.
4. Profile prover memory for chain-shaped vs. binary-tree folding over 2^10 steps; explain the difference using §2.5.3's model.
5. Re-derive the Nguyen–Boneh–Setty attack on a simplified two-curve Nova variant and state the precise binding property whose absence enables it.

---

## Chapter 3: Applications of Recursive Proving

### 3.1 Reading This Chapter: A Maturity Gradient

The chapter's four clusters are ordered by maturity: blockchain infrastructure (production-proven at billions of dollars of secured value), software/systems integrity and data/AI (actively crossing over from research to deployment), and identity/society (emerging). Two through-lines recur. First, a pipeline shape: chunk the computation, prove chunks in parallel, recurse or fold the results, wrap for the target verifier. Second, a mapping discipline: every application is tagged with the Chapter 1 strategy and, where relevant, the Chapter 2 family member that fits it best — folding for uniform incremental workloads (zkML, streaming, SBOM-style DAGs), hybrid STARK pipelines for heterogeneous high-throughput execution (rollups, zkVMs). A roadmap table at the section's end makes the tagging explicit.

*References: cross-references to §1.3.6 and §2.4.5 tables.*

### 3.2 Blockchain Infrastructure (production-proven)

#### 3.2.1 Rollups and proof compression

The original killer app: a rollup executes thousands of transactions off-chain and posts one validity proof to the base layer. Recursion appears twice — aggregating per-transaction or per-batch proofs, and compressing the final proof for cheap on-chain verification (the canonical STARK-to-SNARK squeeze, e.g., Polygon zkEVM's STARK→recursive aggregation→FFLONK pipeline). We work the gas arithmetic that justifies each recursion layer.

*References: Polygon zkEVM architecture documentation; StarkWare, "Recursive STARKs" (2022); Ethereum rollup-centric roadmap materials.*

#### 3.2.2 Cross-chain aggregation and interop

The newer pattern: recursively merge proofs from *many chains* before settlement, amortizing verification cost across an ecosystem and enabling near-instant cross-chain state claims. We study aggregation layers (Polygon AggLayer, Aligned, Nebra-style universal aggregation) as recursion trees whose leaves are entire chains, including the economic logic of shared verification.

*References: Polygon AggLayer documentation; Aligned Layer technical blog; Nebra UPA whitepaper.*

#### 3.2.3 Real-time L1 proving

Ethereum's L1 zkEVM roadmap replaces validator re-execution with verification of succinct proofs, requiring block proofs in under ~10–12 seconds. Recursion is the latency-critical layer: execution is sharded across GPUs, shard proofs are recursively merged, and protocol requirements constrain the shape (proof size under 300 KiB; no trusted-setup recursive wrappers; 128-bit security targets). We chart the race — from ~200-GPU clusters proving 93% of blocks in 2025 to 16-GPU real-time proving in 2026 — and what it implies for prover decentralization.

*References: Ethereum Foundation, "Shipping an L1 zkEVM #1: Realtime Proving" (2025); ethereum.org zkEVM roadmap page; Succinct, "SP1 Hypercube" and "Real-Time Proving with 16 GPUs" (2025–26); LambdaClass/ethproofs reporting on Pico Prism and ethrex.*

#### 3.2.4 Succinct blockchains

Mina is recursion in its purest form: the entire chain state is attested by one constant-size proof, updated recursively with each block, so any participant verifies the chain from genesis in milliseconds. We study the Coda/Mina design — including Pickles, its accumulation-based recursion layer — as both an existence proof and a study in the protocol design freedoms and constraints recursion imposes.

*References: Bonneau, Meckler, Rao, Shapiro, "Coda: Decentralized Cryptocurrency at Scale" (ePrint 2020/352); Mina "Pickles" documentation.*

#### 3.2.5 Consensus, signatures, and light clients

Three related uses. SNARK-aggregated signatures: post-quantum hash-based signatures are large, but a recursive proof that thousands verified is small — the core of Ethereum's "Lean" consensus direction. Light clients and bridges: a recursive proof over a chain's consensus history lets a resource-constrained verifier (a phone, a foreign chain's contract) trustlessly track another chain. Batch verification: IVC folding signatures concurrently as they arrive over the network.

*References: Ethereum "Lean" roadmap materials on hash-based signature aggregation; Xie et al., "zkBridge: Trustless Cross-chain Bridges Made Practical" (CCS 2022); IVC batch-signature-verification literature (BEATS and successors).*

#### 3.2.6 Governance and voting

Recursive rollups suit voting's bursty load profile: ballots fold into a running tally proof as they arrive, on-demand proving capacity absorbs the last-hours surge, and the final proof attests the tally without revealing individual votes. We treat this as a case study in streaming recursion (§1.4.3) plus zero-knowledge, with Mina-ecosystem designs as worked examples.

*References: Mina Hazook recursive zkRollup design (2024); academic literature on end-to-end verifiable voting with ZK tallies.*

### 3.3 Software and Systems Integrity (crossing over)

#### 3.3.1 Software supply chain and SBOMs

A Software Bill of Materials is a dependency DAG — and dependency DAGs are PCD graphs. Each component's proof attests local properties (license, version, absence of known CVEs) *and* folds in the proofs of its own dependencies; the top-level artifact carries one proof over the entire transitive closure, disclosable without revealing proprietary composition. We develop the compliance predicates, the disclosure tradeoffs, and the update story when a CVE lands — this is the chapter's canonical PCD instance, promised back in §1.2.2 and instantiated with §2.5.3's tree folding.

*References: "VeriSBOM: Secure and Verifiable SBOM Sharing via Zero-Knowledge Proofs" (arXiv, 2026); Chiesa, Tromer (ICS 2010); NTIA/CISA SBOM minimum-elements documents for domain context.*

#### 3.3.2 Verifiable build pipelines and attestation chains

Upstream of the SBOM: proofs that a binary was compiled from attested source through attested toolchains, composed recursively across CI/CD stages — source attestation folds into compile attestation folds into packaging attestation. We connect to existing supply-chain frameworks (SLSA, in-toto) and analyze what recursion adds beyond signature chains: succinctness, predicate richness, and selective disclosure.

*References: in-toto and SLSA framework documentation; reproducible-builds literature; PCD framing from Bünz et al. (CRYPTO 2021).*

#### 3.3.3 Verifiable logs and transparency systems

Append-only logs (certificate transparency, binary transparency, audit trails) currently rely on Merkle proofs plus gossip; recursion upgrades them to a single evolving proof of *global* consistency — every epoch's proof folds the previous one, so a verifier checks the latest proof alone and inherits the full history. We cover consistency predicates, the interaction with witness/monitor ecosystems, and incremental-verification costs.

*References: Laurie et al., RFC 6962 (Certificate Transparency) for the baseline; research literature on SNARK-backed transparency logs and verifiable log-structured storage.*

#### 3.3.4 High-integrity and embedded systems

Control systems demand both continuous operation and auditability; IVC proofs of control-loop execution provide tamper-evident audit trails with constant-size verification — feasible for constrained verifiers. We examine the flight-control case study from the literature (90× prover-time improvement over baseline via recursion-friendly arithmetization) and the certification questions that arise when proofs enter safety-critical toolchains.

*References: published IVC flight-control benchmark work (real-time high-integrity flight control via recursive SNARKs); avionics certification literature (DO-178C) for context.*

### 3.4 Data, AI, and Computation (crossing over)

#### 3.4.1 Verifiable AI (zkML)

Neural networks are long chains of structurally similar layers — exactly IVC's shape — so folding proves inference layer by layer (or token by token) with bounded memory. We distinguish three claims of increasing difficulty: proof of *inference* (this output came from this committed model), proof of *model provenance* (this model hashes to a registered checkpoint), and proof of *training* (this model resulted from this data and procedure — vastly harder), and survey practical systems on the inference end.

*References: Kang, Hashimoto, Stoica, Sun, "Scaling up Trustless DNN Inference with Zero-Knowledge Proofs" (2022); Liu, Xie, Zhang, "zkCNN" (CCS 2021); Nova-based zkML folding literature; EZKL and Modulus systems documentation.*

#### 3.4.2 Verifiable databases and analytics

Recursive proofs over query execution: each operator (filter, join, aggregate) proves its step and folds the proof of its inputs, yielding one proof that a result is correct with respect to a committed database. We trace the lineage from vSQL to modern designs and treat the privacy variant — proving aggregate statistics over data no one may see — as the bridge to §3.5's compliance applications.

*References: Zhang, Genkin, Katz, Papadopoulos, Papamanthou, "vSQL" (S&P 2017); subsequent verifiable-database and zk-analytics literature.*

#### 3.4.3 Outsourced and streaming computation

The classical verifiable-outsourcing dream, made incremental: a client delegates a long computation and verifies cheaply at any checkpoint; sensors and IoT devices attest data streams with proofs folded concurrently as readings arrive. We analyze the latency-hiding property (proving overlaps with data arrival) and constrained-device realities — who proves, who verifies, and on what hardware.

*References: Goldwasser, Kalai, Rothblum, "Delegating Computation" (STOC 2008) for lineage; IVC streaming literature; §1.4.3 cross-reference.*

#### 3.4.4 Media provenance

Each edit to a camera-signed original (crop, resize, redact) is proven correct and folded onto the chain of prior edits, so a published image carries one proof of legitimate derivation from an authentic capture — without revealing the original. The idea is old (PhotoProof, built on PCD, 2016) and newly urgent (deepfakes, C2PA's signature-based ecosystem); we compare recursion-based provenance with C2PA's approach and examine the performance frontier for full-resolution images.

*References: Naveh, Tromer, "PhotoProof: Cryptographic Image Authentication for Any Set of Permissible Transformations" (S&P 2016); Datta, Boneh et al., "VerITAS: Verifying Image Transformations at Scale" (2024); C2PA specification for ecosystem context.*

#### 3.4.5 Verifiable delay functions

VDFs require provably *sequential* work; IVC provides the proof layer — each squaring or hash step folds into a running proof that N sequential steps occurred. We cover the MinRoot-style designs, recursion's role versus algebraic VDF constructions (Wesolowski, Pietrzak), and the randomness-beacon applications that motivate the whole area.

*References: Boneh, Bonneau, Bünz, Fisch, "Verifiable Delay Functions" (CRYPTO 2018); Wesolowski (EUROCRYPT 2019); Khovratovich et al., "MinRoot" (2022).*

### 3.5 Identity, Privacy, and Society (emerging)

#### 3.5.1 Identity and credentials

Credential ecosystems are delegation chains — issuer to holder to presentation — and recursion composes them: a proof about a passport folds into a proof of an application-specific predicate ("over 18, EU resident, not on list L") without revealing the document; multiple credentials compose into one selective-disclosure proof. We survey deployed document-proof systems and the PCD framing of delegatable anonymous credentials.

*References: Chase, Lysyanskaya, "Delegatable Anonymous Credentials" lineage (CRYPTO 2009 onward); zkPassport and Anon-Aadhaar style systems documentation; W3C Verifiable Credentials for ecosystem context.*

#### 3.5.2 Web and email provenance

zkTLS/zkEmail-style systems prove facts about authenticated sessions or DKIM-signed messages; recursion composes such atomic proofs into higher-level claims — "I received a payroll deposit each of the last six months" folds six email proofs into one — and amortizes the heavy TLS/DKIM verification circuits via aggregation. We cover the trust models (notary vs. MPC vs. native), which determine what the proofs actually mean.

*References: zkEmail technical documentation; TLSNotary project documentation; DECO (Zhang et al., CCS 2020) for the oracle-protocol lineage.*

#### 3.5.3 Financial compliance

Proof of solvency is recursive aggregation over an account tree: per-account inclusion and balance proofs fold upward into one proof that assets exceed liabilities, revealing neither individual accounts nor totals beyond the predicate. We trace the line from Provisions to modern Summa-style systems, then generalize to regulatory reporting — proving compliance predicates (reserve ratios, exposure limits) over private books, with honest discussion of what proofs cannot establish (off-book liabilities).

*References: Dagher, Bünz, Bonneau, Clark, Boneh, "Provisions: Privacy-preserving Proofs of Solvency for Bitcoin Exchanges" (CCS 2015); Summa proof-of-solvency documentation.*

#### 3.5.4 Private multi-party applications

PCD as a gameplay and collaboration substrate: parties take turns extending a shared proof — private state channels settle on-chain with one proof over the whole channel history; incomplete-information games (fog-of-war strategy, mental poker descendants) enforce rules over hidden state; autonomous-world designs let independent actors extend a shared verifiable reality off-chain. This is the chapter's most speculative section and is labeled as such, with deployed examples separated from designs on paper.

*References: Bowe, Chiesa, Green, Miers, Mishra, Wu, "Zexe: Enabling Decentralized Private Computation" (S&P 2020); Dark Forest and zk-gaming ecosystem writeups; state-channel literature.*

### 3.6 Case Studies (deep dives tying applications to Chapters 1–2)

#### 3.6.1 Anatomy of a real-time zkVM pipeline

End to end through a production-grade stack: an Ethereum block's execution traced in a RISC-V zkVM, sharded across GPUs, shard STARKs recursively merged, wrapped for on-chain verification — every stage labeled with its §1.3 strategy, with real latency and cost numbers, and the protocol constraints (§3.2.3) shown shaping engineering choices.

*References: Succinct SP1 technical documentation; Ethereum Foundation realtime-proving requirements; ethproofs.org benchmark data.*

#### 3.6.2 SBOM verification as PCD

The worked DAG: a three-level dependency tree diagrammed node by node — what each node's compliance predicate checks, what folds upward, what the top-level proof attests — instantiated concretely with Chapter 2's tree folding (§2.5.3) and including the re-proving cost when one leaf dependency changes.

*References: VeriSBOM (2026); §1.2.2 and §2.5.3 cross-references.*

#### 3.6.3 Mina end to end

What a constant-size blockchain actually stores, proves, and verifies: the recursive state-update circuit, Pickles' accumulation machinery, scan-state parallelization of transaction proving, and the protocol-design consequences — what becomes easy (instant sync) and what becomes hard (proving latency in the critical path).

*References: Bonneau, Meckler, Rao, Shapiro, "Coda" (ePrint 2020/352); Mina protocol architecture documentation.*

#### 3.6.4 A zkML inference proof with folding

A small model proven layer by layer with Nova-style IVC: arithmetizing each layer, folding across layers, compressing at the end — with concrete constraint counts, per-layer fold times, memory profile, and an honest comparison against a monolithic (non-recursive) proof of the same inference. This is where Chapter 2's machinery visibly pays off in an application.

*References: Nova-based zkML folding literature; EZKL benchmarks for the monolithic baseline.*

### 3.7 Choosing a Recursion Strategy for Your Application

#### 3.7.1 A decision framework

Five questions determine the design: Is the computation a chain or a DAG? What is the latency budget (real-time, interactive, batch)? What is the verifier environment (L1 contract, phone, embedded device, another proof)? What trust assumptions are acceptable (trusted setup, discrete log, PQ requirements)? Is the workload uniform or heterogeneous? We present the framework as a decision tree with explicit thresholds where the literature supports them and marked judgment calls where it does not.

*References: synthesizes §1.3.6 and §2.4.5; practitioner design literature on recursion strategy selection.*

#### 3.7.2 Mapping the framework back

Each §3.2–3.5 application cluster is run through the decision tree, recovering the strategy choices observed in deployed systems — a consistency check that doubles as a summary. We close with the cases where the right answer is *no recursion*: moderate-scale batching, homogeneous signature aggregation, and one-shot computations that fit a single prover.

*References: cross-references throughout; SnarkPack (FC 2022) for the no-recursion alternatives.*

### 3.8 Outlook: Applied Frontiers

Three trajectories close the book. Recursion as infrastructure: prover markets commoditize proving the way cloud commoditized compute, with open questions about centralization and pricing. The migration out of blockchain: supply-chain, media-provenance, and audit applications import recursion without importing chains, suggesting the technology's second decade looks less like cryptocurrency and more like systems engineering. And the PCD-native horizon: if compliance predicates become a standard software artifact, "where did this data come from and what touched it" becomes a checkable property of ordinary computing — the strongest version of the claim that recursion changes what software can promise.

*References: Aligned Layer and prover-market analyses; §1.6.4 cross-reference; PCD literature (Chiesa–Tromer; Bünz et al.).*

### Chapter 3 Exercises

1. Design a PCD scheme for a three-level dependency tree: specify each node's compliance predicate, the message format, and exactly what the root proof attests. Then compute what must be re-proven when one leaf changes.
2. Two scenarios — an L1 rollup posting hourly and an embedded attestation device with 256 KB of RAM verifying daily — run both through the §3.7.1 decision tree and justify a recursion strategy (or none) for each.
3. Sketch the proof pipeline for a media-provenance system supporting crop, resize, and redaction; choose folding or a hybrid pipeline and defend the choice with the cost anatomy of §2.5.2.
4. For a proof-of-solvency system with 10 million accounts, design the aggregation tree: choose arity, estimate prover work and proof latency, and identify which claims the proof does *not* establish.
5. Take one application from §3.3–3.5 not covered in the case studies and write a one-page design memo mapping it onto the Chapter 1 taxonomy and Chapter 2 family tree.

---

## Backmatter Notes (for the full manuscript)

- **Notation appendix**: unify symbols across chapters (instances, witnesses, folding challenges, IVC proofs) — recursion literature is notationally inconsistent and the book should not be.
- **Annotated bibliography**: the per-subsection references above, consolidated and annotated with one-line guidance on reading order.
- **Errata policy for a fast-moving field**: performance numbers (GPU counts, latencies, costs) in §1.5.5, §3.2.3, and §3.6.1 are snapshots circa 2025–26 and should be framed in the text as such, with a companion web page for updates.
