# Coverage-Gap Proposals: Layers 2-3 — Languages, Compilers & Witness Generation

**Theme scope:** ZK DSLs (Circom, Cairo, Noir, Lurk, Compact, Leo, ZoKrates), compiler infrastructure (CirC, nanopass), witness generation, under-constrained circuits & circuit vulnerabilities, formal verification of circuits (CODA/refinement types, Picus), circuit testing (differential / property-based / fuzzing), compiler-not-language thesis.

**Chapters primarily affected:** 3 (*Choreographing the Act*) and 4 (*The Secret Performance*).

**Method:** Targeted grep of `proving-nothing.md` for each concept term; findings cross-referenced against `CONCEPTS_FOR_BOOK.md` graph signals (degree + reference support) and domain-expert judgment about what a complete 2026 treatment of ZK languages/compilers/witness requires.

---

## Ranked Proposals

### 1. ZoKrates — the historical first-generation high-level ZK DSL

| Field | Detail |
|---|---|
| **Status** | absent |
| **Why it matters** | ZoKrates (Eberhardt & Tai, 2018) was the first widely used high-level ZK language, predating Circom's public tooling by months and directly inspiring the "hide the constraints" thesis. Omitting it leaves the evolutionary narrative (Chapter 3, "From Circuits to Virtual Machines") without its actual first act; readers cannot understand *why* Circom's dual-track model felt like an improvement, or why CirC later unified the field, without understanding what ZoKrates got right and wrong. |
| **Evidence** | `grep ZoKrates proving-nothing.md` → zero hits. CONCEPTS_FOR_BOOK.md does not list it explicitly, but the graph community 49 ("Proof System Compiler", "Existentially Quantified Circuit", "SMT solving over finite fields") contains CirC-adjacent nodes that presuppose ZoKrates context. |
| **Where** | Chapter 3, §"From Circuits to Virtual Machines" — add one paragraph situating ZoKrates as the bridge between raw-circuit Pinocchio/libsnark workflows and the Circom/Cairo generation. |

---

### 2. Lurk — the functional/Lisp-based recursive ZK language

| Field | Detail |
|---|---|
| **Status** | absent |
| **Why it matters** | Lurk (Protocol Labs, Filecoin) is the only production-targeted ZK language built on a functional core (Lisp/Scheme semantics + SNARK back-end) and designed from the ground up for proof recursion at the language level. It offers a qualitatively different approach from all four of Chapter 3's "philosophies" and is relevant to both the compiler-not-language thesis and Chapter 6's IVC discussion. Its absence makes the DSL taxonomy feel artificially narrow. |
| **Evidence** | `grep -i lurk proving-nothing.md` → zero matches. Graph signal: absent from CONCEPTS_FOR_BOOK.md, though community 9 "Verifiable Computation / Delegation" and community 53 "Succinctness" both touch themes central to Lurk's design. |
| **Where** | Chapter 3, §"The Four Philosophies" — a brief paragraph noting Lurk as a fifth thread (Philosophy E: functional/recursive DSL), or a sidebar in Chapter 6 linking it to IVC. |

---

### 3. CirC compiler infrastructure — named, but not explained

| Field | Detail |
|---|---|
| **Status** | thin |
| **Why it matters** | CirC (Ozdemir, Brown, Wahby, IEEE S&P 2022) is the single most important piece of ZK compiler *infrastructure* research: it demonstrated that constraint-system compilation is structurally equivalent to SMT solving and software verification, enabling shared optimization passes across Circom R1CS, zkALI, and EzPC. The book currently name-drops CirC in exactly one sentence (line 1065) without explaining *how* the unification works or *why* shared compiler infrastructure matters. This is the "compiler-not-language thesis" in its most concrete form, and the book's own framing calls the compiler "the part that matters" — yet CirC gets one line. |
| **Evidence** | Single mention at line 1065: "CirC, a unifying compiler infrastructure from Stanford… demonstrated that the compilation problem for ZK circuits shares fundamental structure with SMT solving and software verification." No follow-through. CONCEPTS_FOR_BOOK.md shows Community 54 includes "CirC-compiler implementation" as a graph node with degree/reference support, indicating the reference corpus treats it as substantive. |
| **Where** | Chapter 3, §"The Developer's Actual Experience" (Step 2: Compile) — expand the CirC reference into at least two paragraphs covering the EQC intermediate representation, the multi-target backend (R1CS, ABY, SMT), and the practical payoff of shared optimization infrastructure. |

---

### 4. Refinement types for circuit verification (CODA/Liu et al.)

| Field | Detail |
|---|---|
| **Status** | absent |
| **Why it matters** | CODA (Liu et al., "Certifying Zero-Knowledge Circuits with Refinement Types," IEEE S&P 2024) is the closest thing the field has to a type-theoretic foundation for circuit correctness: it types circuit signals with SMT-dischargeable predicates (refinement types), proves type preservation under circuit evaluation, and automatically catches under-constrained signals that ZKAP misses. It is methodologically distinct from SMT-direct tools like Picus, and represents the "compile-time prevention" half of the correctness stack the book advocates. Chapter 3 and Chapter 4 both mention the aspiration but never describe a concrete mechanism. |
| **Evidence** | `grep -i "refinement type" proving-nothing.md` → zero content hits (the term appears only in a reference list citation at line 5506). `grep -i Coda proving-nothing.md` → one mention at line 5275 in a parenthetical list ("Picus, ZKAP, Coda"). Graph community 56 ("Refinement Types", "SMT solving over finite fields", "BigLessThan motivating example") has high cohesion (0.12) and dedicated nodes, indicating the reference corpus treats CODA substantively. |
| **Where** | Chapter 3, §"Closing the Correctness Gap" (or a new subsection after the ZKAP/Picus paragraph) — explain the refinement-type approach: how signal types carry predicates, how the type checker discharges them via cvc5/Z3, and what classes of bug it catches that dynamic fuzzing cannot. |

---

### 5. Over-constrained circuits — the completeness-side failure mode

| Field | Detail |
|---|---|
| **Status** | absent |
| **Why it matters** | The book correctly emphasizes under-constrained circuits (too few constraints → prover can lie) but never names or analyzes the dual failure mode: *over-constrained* circuits (too many constraints → valid witnesses are rejected, causing completeness failures). Over-constrainedness is the dominant failure mode in halo2/Plonky3 PLONKish circuits, where selector polynomial misconfiguration produces spurious constraint violations on legitimate inputs. Omitting it gives a systematically one-sided picture of the correctness problem. |
| **Evidence** | `grep -i "over-constrained\|over constrained\|completeness.*circuit" proving-nothing.md` → zero hits. The book mentions "completeness bug" at line 1481 but does not explain the mechanism or give any examples. CONCEPTS_FOR_BOOK.md does not list over-constrainedness explicitly, but the "Soundness" and "Completeness" nodes (Community 15, Community 78) both appear and the asymmetry in treatment is stark. |
| **Where** | Chapter 3, §"Under-Constrained Circuits: The Dominant Failure Mode" — rename the section to "The Correctness Spectrum" and add a parallel treatment of over-constrained circuits with a PLONKish example (e.g., a selector polynomial that rejects a valid assignment). |

---

### 6. MTZK and compiler-level metamorphic testing

| Field | Detail |
|---|---|
| **Status** | thin |
| **Why it matters** | MTZK (Xiao et al., "Testing and Exploring Bugs in Zero-Knowledge Compilers," NDSS 2025) found 21 bugs across four industrial ZK compilers using metamorphic relations — a qualitatively different test target than circuit-level tools. The book mentions MTZK at line 1087 in a dense list but does not explain *what metamorphic testing is* or *why testing the compiler rather than the circuit changes the threat model*. This distinction matters enormously: a compiler bug silently corrupts every circuit the compiler produces, whereas a circuit bug affects only one application. |
| **Evidence** | MTZK appears in a single parenthetical clause at line 1087 without explanation. The concept "compiler correctness" and "formally verified compiler" return zero content hits. Community 54's CirC-adjacent nodes and the graph's "Proof System Compiler" community (49) both reinforce that compiler-level testing is underserved. |
| **Where** | Chapter 3, §"Closing the Correctness Gap" — add a paragraph on compiler-vs-circuit test targets, explaining metamorphic testing (apply semantics-preserving transformations to circuit source; the compiled output should satisfy the same witnesses) and why the 21 MTZK findings are categorically more dangerous than the 66 zkFuzz circuit-level findings. |

---

### 7. Circom's dual-track model vs. single-track alternatives — a comparative taxonomy

| Field | Detail |
|---|---|
| **Status** | thin |
| **Why it matters** | The book explains the Circom dual-track problem (separate `<--` computation and `===` constraint operators) well, but never systematically compares it to *single-track* alternatives that eliminate the gap by construction: (a) Compact's ZKIR where the compiler synthesizes all constraints automatically; (b) halo2's "advice" columns with explicit region-level constraint application; (c) PLONKish "copy constraints" that enforce wiring without developer-authored polynomial identities. This comparative framing is the payoff of the compiler-not-language thesis, and without it the thesis remains asserted rather than demonstrated. |
| **Evidence** | The dual-track concept is explained at lines 1073-1088. The single-track alternatives are scattered across the text but never systematically contrasted. The graph's Community 49 ("Proof System Compiler", "Existentially Quantified Circuit") and Community 56 (refinement types, SMT) together cover the design space the book should synthesize. |
| **Where** | Chapter 3, §"Compact's Disclosure Analysis" (after the nanopass pipeline explanation) — a comparison table: Circom dual-track vs. Compact single-track (compiler generates constraints) vs. halo2 region-based vs. Noir ACIR (annotation-controlled). |

---

### 8. Non-deterministic hints: the design pattern and its security implications

| Field | Detail |
|---|---|
| **Status** | thin |
| **Why it matters** | Non-deterministic hints (also called "oracles" or "advice values" in zkVM literature) are the canonical technique for replacing expensive in-circuit computation with cheap out-of-circuit guessing + cheap in-circuit verification. The pattern is ubiquitous — square roots, division, bit decomposition, sorting — and is the source of the *majority* of over-constrainedness bugs when the verification predicate is incomplete. The book introduces the concept at line 1497 in exactly one paragraph and then drops it. A full treatment should cover: the pattern's formal name, its connection to witness non-determinism, the "guess-and-check" security condition, and the tooling needed to verify completeness of the checking predicate. |
| **Evidence** | One paragraph at lines 1496-1497 introduces "non-deterministic hints" and promises the concept will "recur in Chapter 5" — but Chapter 5 does not deliver a substantive treatment (the grep of Chapter 5 confirms this). CONCEPTS_FOR_BOOK.md has no dedicated "non-deterministic hint" node, suggesting the concept lacks an explicit home. |
| **Where** | Chapter 3, §"Under-Constrained Circuits" — add a "Hints and the Guess-and-Check Pattern" subsection covering: formal definition, canonical examples (square root, bit decomposition), security condition (the checking constraints must be *complete*, not just sound), and connection to ZKAP's "constraint-computation discrepancy" root cause. |

---

### 9. ZK-aware LLVM optimization passes

| Field | Detail |
|---|---|
| **Status** | thin |
| **Why it matters** | The Gassmann et al. (arXiv 2508.17518, 2026) result — that a ZK-aware LLVM cost model yields up to 45% proving-cost reduction on individual benchmarks, with 1-4% average across a broad suite — is a significant empirical finding about the compiler layer that the book mentions in one sentence (line 1039) without explaining what the cost model does or why standard LLVM passes are misaligned with ZK proof cost. This is a textbook example of the compiler-not-language thesis in action: a compiler-level optimization improves every language that compiles via LLVM to a zkVM. |
| **Evidence** | One-sentence mention at line 1039. No explanation of what "ZK-aware cost model" means (ZK proof cost is proportional to constraint count and memory access count, not instruction count or cache behavior — so LLVM's default cost model actively mis-optimizes). CONCEPTS_FOR_BOOK.md does not have a dedicated "ZK-aware LLVM" entry. |
| **Where** | Chapter 3, §"The Developer's Actual Experience" (Step 2: Compile) — expand to explain: why standard LLVM cost models are wrong for ZK (they minimize cycles/cache-misses, not constraint-count); what a ZK-aware cost model minimizes (field multiplications, memory accesses with Poseidon-hash overhead); and the practical implication (compiler optimization is a first-class tool for proving-cost reduction, not an afterthought). |

---

### 10. Formal verification of compiler correctness (not just of circuits)

| Field | Detail |
|---|---|
| **Status** | absent |
| **Why it matters** | The book's correctness narrative focuses on verifying *circuits* (ZKAP, Picus, CODA, NAVe). But the 21 MTZK compiler bugs point to a deeper problem: if the *compiler* is unsound, every circuit it produces is potentially unsound regardless of circuit-level verification. Formally verified compilers — a research direction drawing on CompCert methodology — are a genuine frontier for ZK. The analogy to CompCert (the formally verified C compiler) is apt and accessible; it would give readers a framework for thinking about compiler trust. |
| **Evidence** | `grep -i "compiler correctness\|correct compiler\|verified compiler" proving-nothing.md` → zero hits. The MTZK finding (21 compiler bugs, 15 patched) is mentioned once but the implication — that compiler trust is a distinct, unresolved problem — is never drawn. CONCEPTS_FOR_BOOK.md Community 49 contains "Proof System Compiler" and related nodes without addressing compiler soundness. |
| **Where** | Chapter 3, end of §"Closing the Correctness Gap" or a new §"The Compiler Trust Problem" — introduce the compiler-correctness gap as distinct from the circuit-correctness gap; reference MTZK; draw the CompCert analogy; identify formally verified ZK compiler as an open research frontier. |

---

### 11. Witness extension and sub-witness patterns in zkVMs

| Field | Detail |
|---|---|
| **Status** | absent |
| **Why it matters** | Modern zkVMs (RISC Zero's segment-based proving, SP1's shard architecture, Jolt's uniform block-diagonal R1CS) all divide the execution trace into independently-provable sub-witnesses that are later stitched together via continuation proofs or lookup arguments. The *design* of witness partitioning — how to split a sequential trace into parallel-provable segments without creating soundness gaps at segment boundaries — is a central engineering problem not explained anywhere in the book. It directly determines the parallelism available during witness generation (the dominant bottleneck identified in Chapter 4) and has been a source of bugs in every major zkVM. |
| **Evidence** | The book mentions "continuations" (RISC Zero) and "sharding" only in passing. `grep -i "segment\|shard\|continuation" proving-nothing.md` (conceptually implied by the existing content on streaming witness generation) shows the *performance* motivation but not the *security/correctness* implications of boundary handling. CONCEPTS_FOR_BOOK.md's Chapter 3/4 gaps include zkVM (under-covered, support 16) without naming the witness-partitioning sub-problem. |
| **Where** | Chapter 4, after §"Why Witness Generation Resists Parallelization" — add a section "Segment Boundaries and Continuation Proofs" explaining how witness partitioning enables parallelism, the correctness conditions a boundary continuation proof must satisfy, and the known vulnerability class at segment boundaries (register-state continuity constraints). |

---

### 12. Disclosure analysis generalized: information-flow type systems for ZK

| Field | Detail |
|---|---|
| **Status** | absent |
| **Why it matters** | Compact's disclosure analysis pass is introduced as a Midnight-specific feature, but it is actually an instance of a well-studied program analysis technique: *information-flow typing* (taint analysis / IFC). The broader concept — attaching security labels to values and enforcing non-interference at type-check time — has a 50-year literature (Denning & Denning 1977; Volpano-Smith 1996; the FlowCaml, Jif, and SecType lineages). Grounding Compact's analysis in this literature would: (a) give readers a transferable mental model; (b) explain *why* the analysis is sound; (c) open the question of whether other ZK languages could adopt similar type systems without being Midnight-specific. |
| **Evidence** | `grep -i "information flow\|IFC\|taint" proving-nothing.md` → zero hits. The disclosure analysis is explained at lines 1097-1149 in detail, but entirely as a Midnight-specific mechanism. The graph community 56 has "Refinement Types" but not the broader IFC literature. The connection between "disclosure analysis" and "non-interference" is a standard PL result that the book is one citation away from making. |
| **Where** | Chapter 3, §"Compact's Disclosure Analysis" (add a closing paragraph) — connect the disclosure analysis to information-flow typing non-interference, cite the lineage, and pose the open question: can backend-agnostic IFC types be added to Noir or Leo without redesigning the whole language? |

---

## Summary Table

| # | Concept | Status | Priority | Suggested Chapter/Section |
|---|---|---|---|---|
| 1 | ZoKrates (first-gen high-level ZK DSL) | absent | High | Ch 3 §Evolution |
| 2 | Lurk (functional/recursive ZK language) | absent | High | Ch 3 §Four Philosophies or Ch 6 |
| 3 | CirC compiler infrastructure (depth) | thin | High | Ch 3 §Step 2: Compile |
| 4 | Refinement types for circuits (CODA) | thin | High | Ch 3 §Closing the Correctness Gap |
| 5 | Over-constrained circuits (completeness failures) | absent | High | Ch 3 §Correctness Spectrum |
| 6 | MTZK / metamorphic compiler testing | thin | High | Ch 3 §Closing the Correctness Gap |
| 7 | Dual-track vs. single-track comparative taxonomy | thin | Medium | Ch 3 §Compact Disclosure Analysis |
| 8 | Non-deterministic hints: pattern + security | thin | Medium | Ch 3 §Under-Constrained Circuits |
| 9 | ZK-aware LLVM optimization passes | thin | Medium | Ch 3 §Step 2: Compile |
| 10 | Formally verified ZK compilers (compiler trust gap) | absent | Medium | Ch 3 §Compiler Trust Problem |
| 11 | Witness partitioning / segment-boundary continuations | absent | Medium | Ch 4 §Parallelization |
| 12 | Information-flow typing as framework for disclosure analysis | absent | Low | Ch 3 §Compact Disclosure Analysis |

---

## What the Book Already Covers Well (not proposed)

- **Circom dual-track problem** — well-explained with Tornado Cash example and statistics
- **ZKAP** (Circuit Dependence Graph, F1=0.82) — well-covered at lines 1079-1091
- **zkFuzz** — adequately cited
- **Noir, Leo, Compact, Cairo** — all covered in §Four Philosophies
- **Witness generation costs** (50-70% share, ZKPoG, BatchZK, streaming) — Chapter 4 treats this substantially
- **Side-channel attacks on witness generation** (timing, cache, EM) — Chapter 4 is strong here
- **Picus** — named at lines 1087, 5275, 5389 (thin but present)
- **MTZK** — named but not explained (hence proposal #6 for depth, not for adding it)
- **Nanopass compilation** (Compact's 26-pass pipeline) — well described at line 888, 1037-1038
- **LLM-assisted circuit generation** (ZK-Coder) — one paragraph (line 1063), adequate
