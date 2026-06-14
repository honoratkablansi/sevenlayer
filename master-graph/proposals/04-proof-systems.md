# Layer 5 — Proof Systems & Polynomial Commitments: Coverage Gap Proposals

**Theme:** SNARK families, STARKs, polynomial commitment schemes, sum-check protocol, GKR, IOPs, low-degree testing, prover/verifier/proof-size tradeoffs.  
**Primary chapter:** Chapter 6 (Layer 5 — The Sealed Certificate), with secondary relevance to Chapter 5 (arithmetization) and Chapter 10 (trust decomposition).

---

## Summary of Methodology

Grep-verified actual manuscript coverage against graph signals. Chapter 6 is substantive and well-organized, covering: Groth16, PLONK/UltraPlonk/Halo2, STARKs, the hybrid pipeline, recursion vs. folding, the full folding genealogy (Nova through Symphony), Circle STARKs/Stwo, real-time Ethereum proving, and the four PCS families (KZG, FRI, IPA, Lattice/Ajtai). The chapter is genuinely strong on _what it covers_. The gaps are concentrated in (a) the interactive proof foundations that justify the protocols, (b) specific proof-system families that appear only as names in tables, and (c) the PCS design space beyond the four families.

---

## Ranked Gap Proposals

---

### 1. Interactive Oracle Proofs (IOPs) and the PIOP Model

| Field | Detail |
|---|---|
| **Status** | Absent |
| **Graph signal** | Degree 20, ref-support 9 — hub node; community 28 and community 42 both centre on this concept |
| **Why it matters** | The IOP/PIOP abstraction is the theoretical unifying frame for modern SNARKs: PLONK, Marlin, Aurora, Spartan, and HyperNova are all polynomial IOPs compiled via KZG or FRI. Without it, the reader cannot understand _why_ these proof systems have the same verifier structure or how to compare them at the right level of abstraction. The "three families" framing in Chapter 6 silently relies on IOP intuition without naming it. |
| **Evidence** | Grep for "interactive oracle proof" returns only definitional glossary hits and one reference-list entry (`[BCS16]`). The term "polynomial IOP" / "PIOP" does not appear in the prose at all. The graph places Interactive Oracle Proofs as a distinct absent hub with 9 supporting references. |
| **Where** | Chapter 6, between "The Three Families" and "The Hybrid Pipeline" — a 2–3 paragraph section explaining that Groth16/PLONK/Spartan are all PIOP+PCS compilations, which immediately clarifies the table in Chapter 2 and the comparisons throughout. |

---

### 2. The Sum-Check Protocol — Standalone Treatment

| Field | Detail |
|---|---|
| **Status** | Thin (present but buried) |
| **Graph signal** | Degree 95, ref-support 29 — 4th-largest god node in the entire graph; the graph flags it ABSENT at the top-table level but the `Sumcheck Protocol` (duplicate node, degree 9) is "well-covered." In practice: the manuscript has one solid dedicated subsection ("What Sumcheck Does," ~3 pages in Chapter 5 context) but the concept does not receive the architectural weight its graph centrality demands. |
| **Evidence** | Grep confirms: sumcheck is described as the "backbone of Spartan, HyperNova, Jolt, and SP1 Hypercube" and there is a worked explanation. However, the formal statement (the round-by-round protocol, the soundness error bound, the Schwartz-Zippel connection) is scattered across two chapters and never assembled into a self-contained section a reader can point at. The protocol's multi-linear variant — critical for understanding HyperNova and SP1 Hypercube — appears only implicitly. |
| **Where** | Chapter 6 should add a "Sum-Check: The Protocol Behind the Protocols" sidebar or section (1–2 pages) immediately before the folding genealogy, showing the round structure, the $O(n\log n)$ to $O(\log n)$ verifier reduction, and why multilinear polynomials make it efficient. The scattered current treatment should be consolidated here. |

---

### 3. GKR Protocol — Standalone Treatment

| Field | Detail |
|---|---|
| **Status** | Absent as a standalone concept |
| **Graph signal** | Degree 33, ref-support 12 — explicit god-node entry tagged ABSENT: "doubly-efficient interactive proof for bounded-depth computation via layer-by-layer sumcheck reduction; prover need not commit to full trace" |
| **Evidence** | Grep shows GKR appears only in the context of "LogUp-GKR" (used in SP1 and Stwo to speed up lookup verification). The standalone GKR protocol — its layer-by-layer sumcheck reduction, the "doubly-efficient" prover cost, Thaler's prover optimizations — is never explained. The reader is told GKR makes LogUp-GKR's verifier logarithmic but not _how_. Community 41 ("doubly-efficient interactive proof") and Community 44 (CMT protocol/multilinear extension) are both strongly connected to GKR and show as absent. |
| **Where** | Chapter 6 or Chapter 5: a 1–2 page section on GKR as a standalone interactive proof for layered circuits, showing why it reduces verifier work from $O(n)$ to $O(\log n)$, and connecting it explicitly to (a) LogUp-GKR in SP1/Stwo and (b) the sumcheck protocol above. |

---

### 4. Multilinear Extension (MLE) — Explicit Treatment

| Field | Detail |
|---|---|
| **Status** | Absent as named concept |
| **Graph signal** | Degree 17, ref-support 11 — listed ABSENT in the top table; community 44 hub |
| **Evidence** | Grep shows "multilinear extension (MLE)" appears twice: once describing Lasso's use of MLE for table evaluation, and once in passing in the sumcheck subsection. The concept — that every function on $\{0,1\}^n$ has a unique multilinear extension over $\mathbb{F}$, and that MLE is the polynomial representation underlying Spartan, HyperNova, SP1 Hypercube, and all sumcheck-based systems — is never defined or explained. This is a foundational gap because readers cannot understand _why_ multilinear polynomials are used instead of univariate polynomials without it. |
| **Where** | Chapter 6, as a brief (1 page) boxed definition immediately before the sumcheck or folding sections. The connection "multilinear polynomial over Boolean hypercube → sumcheck verification → HyperNova/SP1 Hypercube" would unlock the logic of the entire multilinear SNARK ecosystem. |

---

### 5. Sonic and the Updatable / Universal SRS Lineage

| Field | Detail |
|---|---|
| **Status** | Absent as a named proof system |
| **Graph signal** | Community 57 is dedicated to Sonic (Maller et al.); "Updatable and Universal Structured Reference String" tagged ABSENT (degree 13, ref-support 6); "Universal vs Circuit-Specific SRS" tagged under-covered (degree 15, ref-support 5) |
| **Evidence** | Grep confirms Sonic appears only in one sentence: "every pairing-based proof system — Groth16, PLONK, Marlin, Sonic, KZG —" and in a reference-list entry. Its key contribution — the universal _and updatable_ SRS, subversion zero-knowledge, and the bivariate constraint system — is absent from the prose despite being the direct predecessor of PLONK's universal SRS design. The graph also shows "Updatable and Universal CRS" (CRYPTO 2018, Groth et al.) as absent. |
| **Where** | Chapter 6 or Chapter 2: a paragraph in the "Universal Trusted" row of the proof-system table, explaining the Sonic/PLONK lineage for updatable universal SRS. The "updatable" property (anyone can add their randomness post-ceremony) meaningfully changes the trust model and is a direct predecessor of Ethereum's approach to the KZG ceremony. |

---

### 6. Marlin — Dedicated Treatment

| Field | Detail |
|---|---|
| **Status** | Thin |
| **Graph signal** | Community 59 explicitly contains "Marlin (universal preprocessing SNARK)" as a node; the graph's proof-systems community is partly organized around the Sonic→Marlin→PLONK lineage |
| **Evidence** | Grep shows Marlin appears in: a table cell ("PLONK, Marlin — universal trusted"), one sentence listing it alongside other proof systems, and as a KZG user. Its specific contribution — the first practical universal preprocessing SNARK using the holographic IOP model, achieving $O(\sqrt{n})$ prover FFTs vs. PLONK's $O(n \log n)$ — is absent. This matters because Marlin's algebraic structure (holographic indexing, the "denominator trick") directly enabled the Spartan and CCS directions. |
| **Where** | Chapter 6, within or after the "PLONK: The Universal Workhorse" section — a paragraph on the Sonic→Marlin→PLONK design space, noting Marlin's holographic construction and connecting it to Spartan's multilinear alternative. |

---

### 7. Spartan — Deeper Treatment

| Field | Detail |
|---|---|
| **Status** | Thin |
| **Graph signal** | Degree 39, ref-support 6 — tagged under-covered in Chapter 5; Communities 16 and 33 contain Spartan nodes; "Sparse multilinear polynomial commitment (Spartan compiler)" listed ABSENT |
| **Evidence** | Grep confirms Spartan appears in two substantive places: (1) listed as using "sumcheck to verify R1CS satisfaction directly, without FFTs" and (2) as the decider SNARK for Nova/Nightstream. But the Spartan architecture — its commitment scheme for sparse multilinear polynomials, the SPARK compiler for turning R1CS into a multilinear polynomial, and why it enables transparent SNARKs without FFTs — is not explained. The "SPARK compiler" and "sparse multilinear PCS" are absent. |
| **Where** | Chapter 6, within the sumcheck section or the folding genealogy — 1 paragraph explaining Spartan as the first "transparent, no-FFT SNARK via sumcheck over R1CS" that became the decider SNARK of choice for folding systems. |

---

### 8. Aurora (transparent SNARK via IOP)

| Field | Detail |
|---|---|
| **Status** | Absent |
| **Graph signal** | Degree 5, ref-support 3 — listed ABSENT; community 28 hub (same community as "Interactive Oracle Proofs") |
| **Evidence** | Grep: Aurora does not appear in the manuscript prose at all, only potentially in references. Aurora (Ben-Sasson et al., 2018) was the first practically efficient transparent SNARK for R1CS using an IOP approach, predating Spartan and influencing the STARK ecosystem. It is the natural "transparent IOP SNARK" counterpart to PLONK's "universal trusted SNARK." Its absence leaves a conceptual gap in the lineage from PCPs/IOPs to modern transparent proof systems. |
| **Where** | Chapter 6, in a brief lineage table or sidebar on transparent SNARKs (Aurora → Spartan → multilinear STARKs). Even a single sentence noting Aurora's role as the first efficient transparent R1CS SNARK would close this gap. |

---

### 9. Gemini Elastic SNARK

| Field | Detail |
|---|---|
| **Status** | Absent |
| **Graph signal** | Degree 5, ref-support 3 — listed ABSENT; community 28; community 40 explicitly contains "Gemini (BCHO22): small-space VM SNARK with streamed multilinear-KZG PCS" |
| **Evidence** | Grep: "Gemini" does not appear in manuscript prose. Gemini (Bootle, Chiesa, Hu, Orru, 2022) is the paper that proved multilinear KZG commitments can be computed in streaming / small-space fashion, enabling SNARKs for very long computation traces without loading the full witness into memory. This is directly relevant to the "Memory Gap" discussed in Chapter 4, and to understanding why SP1 Hypercube uses a streaming multilinear PCS. Its absence means the book cannot explain why the "jagged PCS" in SP1 works the way it does. |
| **Where** | Chapter 6, in the Four Families section under KZG or in a new "Multilinear KZG Extensions" subsection, noting Gemini as enabling streaming/elastic proving for long traces. |

---

### 10. Basefold Polynomial Commitment Scheme

| Field | Detail |
|---|---|
| **Status** | Thin |
| **Graph signal** | Community 36 explicitly contains "BaseFold" as a node; listed in the book as a planned replacement for Hyrax in Jolt-b |
| **Evidence** | Grep: "Basefold replacement is planned in Jolt-b" — a single clause. Basefold (Zeilberger, Chen, Chen, 2023) is a PCS that generalizes FRI from Reed-Solomon codes to "foldable codes" over arbitrary fields, making it the first FRI-like transparent PCS that works for multilinear polynomials over _any_ small field (not just STARK-friendly fields with smooth-order multiplicative subgroups). This makes it the enabling technology for transparent multilinear SNARKs over BabyBear or M31 — precisely the systems that dominate the book's case studies. The fact that Jolt's roadmap references it without explanation is a missed teaching opportunity. |
| **Where** | Chapter 6, "Four Families" section — a paragraph under FRI noting that Basefold generalizes FRI to multilinear polynomials over arbitrary fields, enabling transparent multilinear SNARKs. |

---

### 11. Dory Commitment Scheme (transparent pairing-based)

| Field | Detail |
|---|---|
| **Status** | Absent |
| **Graph signal** | The KZG entry in the top table explicitly names "Dory transparent pairing-based scheme" as a second concept, tagged ABSENT (degree 81, ref-support 10 for the combined entry — high signal) |
| **Evidence** | Grep: "Dory" does not appear in the manuscript. Dory (Lee, 2021) is a pairing-based PCS with no trusted setup, achieving $O(\sqrt{n})$ verification (better than IPA's $O(n)$ but worse than KZG's $O(1)$). It is the "transparent pairing" option that sits between KZG and IPA in the design space, and was used as the original commitment scheme in HyperKZG (Mercury). Its absence means the four-families table misses an important fifth option that disproves the claim that "transparent + pairing = impossible." |
| **Where** | Chapter 6, Four Families section — a paragraph or table row noting Dory as a transparent pairing-based PCS, clarifying that transparency does not require abandoning pairings entirely. |

---

### 12. Hyrax Commitment Scheme — Explicit Treatment

| Field | Detail |
|---|---|
| **Status** | Thin |
| **Graph signal** | Degree 7, ref-support 2 — ABSENT in top table; appears in community 2 area |
| **Evidence** | Grep: "Hyrax is an inner-product-argument polynomial commitment scheme that requires only a random group-element generator, not a ceremony" — a single sentence in the Jolt case study. The Hyrax commitment (Wahby, Tzialla, shelat, Thaler, Walfish, 2018) is the multilinear variant of IPA, adapted for matrix-structured commitments that enable sublinear verification via batching. It is the PCS that makes Jolt and Spartan efficient without a trusted setup. The four-families table subsumes it under "IPA/Bulletproofs" but this obscures the distinction between univariate IPA (Bulletproofs) and multilinear IPA (Hyrax). |
| **Where** | Chapter 6, Four Families section under IPA/Bulletproofs — a note distinguishing univariate IPA (Bulletproofs, logarithmic proofs, linear verification) from multilinear IPA (Hyrax, matrix-structured, used by Spartan and Jolt). |

---

### 13. STARK-to-SNARK Recursion and the IOP-to-Argument Compilation

| Field | Detail |
|---|---|
| **Status** | Absent as named concept |
| **Graph signal** | "STARK-to-SNARK Recursion" listed ABSENT (degree 5, ref-support 4); "BCS transformation (IOP → SNARG via Merkle trees / Fiat-Shamir)" present in community 6 but absent from prose; "Probabilistically Checkable Proofs (PCPs)" listed ABSENT (degree 6, ref-support 4) |
| **Evidence** | Chapter 6 describes the hybrid STARK-inside-SNARK-outside pipeline excellently but never explains _why_ this works at the theoretical level. The BCS (Ben-Sasson, Chiesa, Spooner) transformation — "compile any IOP into a non-interactive argument via Merkle commitments + Fiat-Shamir" — is the formal justification for the entire hybrid pipeline. Without it, the "glass envelope then paper envelope" analogy is vivid but unfounded. Similarly, the PCP-to-SNARK path (Kilian 1992, Micali 1994) is the historical root that explains why SNARKs can exist at all. |
| **Where** | Chapter 6, after "The Hybrid Pipeline" — a 1-page section "Why the Pipeline Works: The BCS Transformation" explaining that every STARK is an IOP compiled to a non-interactive argument, and that SNARK wrapping is just adding a second compilation step. This grounds the engineering in theory. |

---

### 14. Grand Product Argument

| Field | Detail |
|---|---|
| **Status** | Absent |
| **Graph signal** | Degree 11, ref-support 4 — ABSENT; "Grand Product Check" appears in community 54 |
| **Evidence** | Grep: the "grand product" phrase appears only in a lookup-comparison table cell (Plookup uses "grand product"). The grand product argument — the accumulator polynomial $Z$ encoding the product of all wire values, used in PLONK's permutation check and Plookup — is the mechanism that makes copy constraints and lookup arguments efficient. Chapter 6 explains _what_ PLONKish copy constraints do (correctly) but not _how_ the permutation argument works at the polynomial level. This gap makes PLONK's construction opaque: the reader is told wires must match but not how the proof ensures this. |
| **Where** | Chapter 6, within the PLONK section — a paragraph on how the grand product argument encodes the permutation check as a polynomial identity, giving the reader the "Z(X)" intuition that makes PLONK's construction self-contained. |

---

### 15. Prover/Verifier/Proof-Size Tradeoffs: The Complexity Taxonomy

| Field | Detail |
|---|---|
| **Status** | Thin |
| **Graph signal** | "Algebraic Query Complexity" and "Linear PCP" listed as concepts in community 36 and 22 respectively; "Succinct Argument" ABSENT (degree 6, ref-support 3) |
| **Evidence** | Chapter 6's four-families table gives concrete numbers (48 bytes, 50–200 KB, etc.) but provides no framework for understanding _why_ different proof systems achieve different tradeoffs. The complexity-theoretic picture — why linear PCPs produce constant-size proofs, why IOPs produce polylogarithmic proofs, why IPA produces logarithmic-size but linear-time verification — is absent. A reader cannot predict what class a new proof system belongs to without this framework. The Thaler "Proofs, Arguments, and Zero-Knowledge" framework would fit here. |
| **Where** | Chapter 6, a sidebar or short section after the four-families table — "Reading the Tradeoff Table: Why These Numbers" — giving the complexity-theoretic origin of each size/verifier-cost combination. Even 3–4 paragraphs would transform the table from a lookup chart into a legible design space. |

---

## Summary Table

| # | Concept | Status | Priority |
|---|---------|--------|----------|
| 1 | Interactive Oracle Proofs (IOP/PIOP model) | Absent | Critical |
| 2 | Sum-Check Protocol — standalone section | Thin | Critical |
| 3 | GKR Protocol — standalone section | Absent | High |
| 4 | Multilinear Extension (MLE) | Absent | High |
| 5 | Sonic + Updatable/Universal SRS lineage | Absent | High |
| 6 | Marlin — dedicated treatment | Thin | High |
| 7 | Spartan — SPARK compiler / sparse MLE PCS | Thin | High |
| 8 | Aurora (transparent IOP SNARK) | Absent | Medium |
| 9 | Gemini Elastic SNARK (streaming multilinear-KZG) | Absent | Medium |
| 10 | Basefold PCS (FRI generalized to multilinear) | Thin | Medium |
| 11 | Dory (transparent pairing-based PCS) | Absent | Medium |
| 12 | Hyrax (multilinear IPA, vs. univariate Bulletproofs) | Thin | Medium |
| 13 | BCS Transformation / IOP-to-argument compilation | Absent | Medium |
| 14 | Grand Product Argument (PLONK permutation check) | Absent | Medium |
| 15 | Complexity taxonomy: why these proof-size/verifier tradeoffs exist | Thin | Low-Medium |

---

## What Is Already Well-Covered (Do Not Propose)

- Groth16 architecture, 192-byte proofs, per-circuit ceremony, BN254 security
- PLONK and PLONKish arithmetization, Halo2, UltraPlonk
- STARKs, FRI (excellent 3-page treatment), AIR constraints
- Hybrid STARK-inside-SNARK-outside pipeline (concrete worked example)
- Recursion vs. folding distinction (the "Russian doll vs. snowball" framing is very effective)
- Full Nova→SuperNova→HyperNova→ProtoStar/ProtoGalaxy→CycleFold→LatticeFold→Neo→Symphony genealogy
- Circle STARKs and Stwo (circle group math is explained well)
- Real-time Ethereum proving benchmarks and cost trajectory
- Four PCS families: KZG, FRI, IPA/Bulletproofs, Lattice/Ajtai — each with substantial treatment
- The cryptographic primitives trilemma framing
- Small fields (BabyBear, M31, Goldilocks) and their performance advantages
- LogUp-GKR (covered in context, though standalone GKR is absent)
- CCS unification (good treatment)
- Sumcheck (present but thin — treated above as needing consolidation, not full addition)
