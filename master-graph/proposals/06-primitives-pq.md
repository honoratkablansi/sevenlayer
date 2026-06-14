# Layer 6 — Cryptographic Primitives & Post-Quantum: Coverage Gap Proposals

**Theme agent:** Layer 6 — Cryptographic Primitives & Post-Quantum (primarily Chapter 7)
**Date:** 2026-06-14
**Analyst note:** All evidence is grep-verified against `proving-nothing.md`. "Absent" means zero substantive appearances; "thin" means mentioned but not explained at a level that serves the stated audience.

---

## Quick Coverage Verdict (before proposals)

The following in-scope concepts are already **well-covered** in Chapter 7 and are NOT proposed for addition:

| Concept | Verdict | Notes |
|---|---|---|
| BN254, BLS12-381 | Well-covered | Sections on security erosion, field cascade, pairing intuition |
| Ajtai commitments / Module-SIS | Well-covered | Full section with geometric intuition |
| Goldilocks, BabyBear, Mersenne-31 | Well-covered | Performance comparison, SIMD intuition, extension fields |
| NTT | Well-covered | Bottleneck discussion, GPU parallelism, 90% of GPU time stat |
| Poseidon / Poseidon2 | Well-covered | Algebraic hash section, side-channel angle |
| LatticeFold, LatticeFold+, Neo | Well-covered | Five-stage progression, parameter cascade |
| Module-LWE | Well-covered | Glossary + FIPS 203 mention |
| Greyhound / LaBRADOR | Mentioned | Named and sized (50 KB / 58 KB) but not explained mechanically |
| FIPS 203/204/205 | Mentioned | Named with one-sentence description |
| HNDL threat | Well-covered | Full section with blockchain permanence angle |
| Shor's algorithm | Well-covered | Qubit count, timeline, cliff-edge framing |
| FHE | Mentioned (Chapter 9) | Not a Layer 6 primitive as used in the book |

---

## Ranked Proposals (most important first)

---

### 1. Bilinear Pairing Mechanics — How the Weil/Tate Pairing Actually Works

**Status:** Thin
**Why it matters:** Chapter 7 uses the pairing constantly ("one pairing equation," "two pairing evaluations") and explains *that* it works, but never shows *how* — the Miller loop, the Weil or Tate pairing definition, the target group $\mathbb{G}_T$, why $e(aP, bQ) = e(P,Q)^{ab}$ holds, or why this bilinearity implies the KZG verification equation. Readers who hit the verification equation `e(C − yG, H) = e(π, H_s − zH)` at line ~3093 have no mechanism to check it. This is the single most-used primitive in the book and the least explained one.
**Evidence:** Grep finds ~30 uses of "pairing" in Ch.7 with the word "bilinear" appearing only in a definitional sentence. The full KZG verification equation is stated (line 3093) but the two-line derivation that makes it believable is absent. Graph: "Bilinear Pairing" — under-covered (degree 38, ref support 18, Community 0 hub).
**Where:** Chapter 7, §KZG — add a 200–300 word box "How the Pairing Does the Work" after the analogy of the SRS as a ruler (currently line ~3097).

---

### 2. Embedding Degree — Why Only Certain Curves Support Pairings

**Status:** Absent
**Why it matters:** The book explains that BLS12-381 is "pairing-friendly" and BN254 is "pairing-friendly," but never says what "pairing-friendly" means. The embedding degree $k$ (the smallest integer such that $p^k \equiv 1 \pmod{r}$) governs whether an efficient Tate/Weil pairing exists, and why ordinary 256-bit curves like secp256k1 (used by Bitcoin/Ethereum key management) cannot be used for KZG. Without this, the sentence "only a handful of suitable curve pairs exist" (line 3492) is mysterious. The concept also explains the MNT and BLS curve families that the book references.
**Evidence:** Grep finds zero uses of "embedding degree." Graph: "Embedding degree k" — absent (degree 12, ref support 4); "Pairing-friendly elliptic curves" — absent (degree 9, ref support 4); "MNT curves" — absent (degree 11, ref support 4). Community 65 in the graph is the pairing-curve community and contains no Chapter 7 text nodes.
**Where:** Chapter 7, §KZG — a sidebar (100–150 words) explaining embedding degree and why it makes BLS12-381/BN254 special, contrasting with secp256k1.

---

### 3. Algebraic Group Model (AGM) — The Security Framework for Pairing-Based Proofs

**Status:** Absent
**Why it matters:** The book mentions that KZG rests on "the bilinear pairing assumption" and the "q-SDH assumption" (line ~3398) but never situates these within the formal security model in which they are proved. The AGM is the standard idealized model for proving KZG's binding property and for proving Groth16 and PLONK secure. It is the lattice of arguments between "this is secure in the AGM" and "this is actually secure," and the gap matters for understanding why pairing-based proofs have known limitations (e.g., non-falsifiable assumptions). The graph explicitly flags this as high-priority absent.
**Evidence:** Grep finds zero occurrences of "algebraic group model" or "AGM." Graph: "Algebraic Group Model (AGM)" — absent (degree 14, ref support 5), Community 100. The graph also flags "Q-DLOG Assumption" as absent (degree 5, ref support 3).
**Where:** Chapter 7, §Three Hardness Assumptions — a paragraph under "The Discrete Logarithm Problem" explaining the AGM as the proof environment, distinguishing it from the generic group model, with a one-sentence note on non-falsifiability implications.

---

### 4. Ring-LWE and the Cyclotomic Ring — Why Lattice Schemes Use $\mathbb{Z}[X]/\Phi_d(X)$

**Status:** Thin
**Why it matters:** The book uses the cyclotomic ring $R_q = \mathbb{F}_q[X]/(\Phi(X))$ extensively (Neo's $\Phi_{81}$, LatticeFold's power-of-two rings) but never explains *why* these rings are used instead of plain integer lattices, or what Ring-LWE is and how it relates to Module-LWE/Module-SIS. The chapter states that "each entry in the vector is itself a polynomial — a ring element with $d$ coefficients" (line 3161) but the reader has no grounding in why the ring structure (rather than, say, a matrix of integers) is the right tool. Ring-LWE is the decisional assumption underlying ML-KEM (FIPS 203), and understanding it ties the proof system literature to the broader PQ standards.
**Evidence:** Grep finds "Ring-LWE" zero times in the main text (appears only in a comparison table label "Ring-SIS"). Graph: "Module Learning With Errors (MLWE)" — absent (degree 12, ref support 4); "Power-of-Two Cyclotomic Ring Z[X]/(X^d+1)" — absent (degree 10, ref support 3). Community 10 and 27 are the MLWE/ring communities with minimal Ch.7 text.
**Where:** Chapter 7, §Module-SIS — add 150–200 words on why the polynomial ring $R_q$ is used, what Ring-LWE is, and how Module-LWE (the FIPS 203 assumption) relates to Module-SIS (the commitment binding assumption). This would also support the FHE section in Chapter 9.

---

### 5. ML-KEM / ML-DSA — What the NIST Standards Actually Specify

**Status:** Thin
**Why it matters:** FIPS 203 (ML-KEM), 204 (ML-DSA), and 205 (SLH-DSA) are mentioned in one paragraph (line 3288) but receive no technical content: what algorithm families they instantiate, what their key/ciphertext sizes are, how they relate to the ZK proof systems in the book, and crucially — what it means for a ZK system to use them vs. merely coexist with them. Practitioners need to understand that ML-KEM replaces classical key exchange at the *transport layer* while lattice-based ZK schemes replace the *proof layer*, and these are separate migration concerns.
**Evidence:** Grep finds "ML-KEM" in only two places (one glossary entry, one paragraph with the standards list). "ML-DSA" appears in one place (the same paragraph). Graph: "ML-KEM Key-Encapsulation Mechanism" — absent (degree 12, ref support 3); "ML-DSA (Module-Lattice Digital Signature Algorithm)" — absent (degree 21, ref support 2), with Community 45 being the ML-DSA community entirely absent from Ch.7. FIPS 204 is referenced in endnote 64 but not discussed in the text.
**Where:** Chapter 7, §Quantum Threat Horizon — expand the NIST standards paragraph to 250–300 words with (a) concrete parameter sizes for ML-KEM-768, (b) the distinction between transport-layer PQ migration and proof-system PQ migration, (c) why no equivalent ZK standard exists yet.

---

### 6. Lattice Functional Commitments (Wee-Wu / BASIS) — The Missing Link to Succinct Lattice SNARKs

**Status:** Absent
**Why it matters:** The book covers Ajtai commitments (vector commitments) and traces the LatticeFold line, but the parallel research program of *functional* lattice commitments (Wee and Wu, ASIACRYPT 2023; the BASIS and Evasive-LWE line) is completely absent. Functional commitments allow committing to a function $f$ and opening at input $x$ — this is the lattice analogue of KZG's polynomial evaluation proof, and it is the ingredient needed to build succinct lattice SNARKs for arbitrary NP (as opposed to folding-based IVC). The book references Wee-Wu in endnote 62 but never mentions it in the text. This is a significant gap in the "lattice revolution" narrative.
**Evidence:** Grep finds "lattice functional commit" zero times in body text (one endnote citation only). Graph: "Functional Commitment" — absent (degree 9, ref support 2); "Lattice Commitment" — absent (degree 4, ref support 4); "BASIS_struct Assumption" — Community 26, absent from Ch.7 text. Community 26 contains 22 nodes on lattice functional commitments with zero Ch.7 coverage.
**Where:** Chapter 7, §Lattice-Based Proving — add a paragraph or mini-section after Stage 5 (Symphony) on the functional-commitment parallel track, explaining how it complements folding-based schemes and what "succinct" lattice SNARKs would require.

---

### 7. Poseidon Security Analysis — Parameter Revisions and the Maturity Gap

**Status:** Thin
**Why it matters:** The book mentions in passing that "Poseidon has seen parameter revisions in response to improved attacks" and that the Bouvier et al. (2022) Gröbner basis attack tightened round counts (line 3477). But this is buried in the algebraic hash section and underweights the ongoing cryptanalysis story: Rescue-Prime and its improved security argument, the differences between Poseidon (2019) and Poseidon2 (a round-count-optimized redesign), and why the field (pun intended) has not converged on one algebraic hash. The security argument for algebraic hashes vs. SHA-256 is a live research debate with real deployment stakes (Midnight bets on Poseidon; Neo bets on Ring-SIS).
**Evidence:** Grep finds "Poseidon2" in two places (Nightstream codebase reference, performance benchmark) but no explanation of what Poseidon2 is or why it differs from Poseidon. "Rescue" appears zero times in the body text (glossary entry: "Rescue" — absent). Graph: "Poseidon Hash" — under-covered (degree 46, ref support 4), assigned to Chapter 12 in the gap report but architecturally belongs to Ch.7's algebraic hash section.
**Where:** Chapter 7, §Algebraic vs. Traditional Hash Functions — add 150–200 words comparing Poseidon (2019) and Poseidon2 (2023) design differences, and note Rescue/Rescue-Prime as the main alternative with a stronger security argument at the cost of performance.

---

### 8. BabyBear Extension Field — Why Degree 4 and Not Degree 2

**Status:** Thin
**Why it matters:** The book correctly states that BabyBear requires a degree-4 extension (not degree 2) and provides the correct technical reason ("BabyBear's structure does not provide enough security separation at that extension level," line 3247). But the explanation is brief and relies on the reader knowing what 2-adicity means and why it affects extension-field security. This is one of the most common points of confusion for practitioners moving from BLS12-381 to BabyBear, and the book is positioned to give the clearest account available. The M31 extension is also stated (degree 4) but not explained.
**Evidence:** Grep finds "degree-4 extension" and the correct reasoning at line 3247, but no explanation of why degree-2 falls short specifically (the answer: $p-1 = 2^{27} \cdot 15$ means the quadratic extension $\mathbb{F}_{p^2}$ has order $p^2-1$ with 2-adic valuation only ~54 bits, too small for 128-bit NTT slots; this is actually stated implicitly in the text but not made explicit). Graph: "BabyBear" — absent from unassigned (degree 22, ref support 1), meaning the graph sees more citation depth here than the text provides.
**Where:** Chapter 7, §Small Fields — expand the extension-field paragraph with a two- or three-sentence concrete explanation of why BabyBear's 2-adicity of 27 forces degree 4, and connect this back to why security parameters depend on NTT domain structure.

---

### 9. LaBRADOR — The Pre-Folding Lattice Argument System

**Status:** Thin
**Why it matters:** LaBRADOR (CRYPTO 2023) is mentioned twice — once as achieving "58-kilobyte proofs" (line 4446) and once as part of the lattice folding lineage (line 3316: "LaBRADOR (2023) demonstrated large-scale lattice argument systems before folding was on the table"). But it is never explained: what problem it solves (proving knowledge of a vector satisfying inner-product relations over a module lattice), what "commitments-to-commitments" means (its key technique), or why it is the direct predecessor that made LatticeFold possible. Without this, the historical narrative jumps from "lattice commitments exist" to "LatticeFold appeared" without the intermediate engineering step.
**Evidence:** Grep finds LaBRADOR in 3 places, all as a name drop. Graph: "LaBRADOR Proof System" — absent (degree 12, ref support 2), Community 77; "LaBRADOR [BS23] (commitments-to-commitments, short proofs)" — Community 10, zero Ch.7 coverage.
**Where:** Chapter 7, §Lattice-Based Proving, Stage 1 — expand to a half-page that explains LaBRADOR's commitments-to-commitments technique and why it was necessary before the folding breakthrough.

---

### 10. Cryptographic Migration — What "Crypto-Agility" Actually Requires

**Status:** Thin
**Why it matters:** The book correctly demolishes the crypto-agility fiction ("largely a fiction for zero-knowledge systems," line 3451) but does not provide a positive framework for what a real migration looks like. Given that NIST IR 8547 mandates federal migration by 2035, practitioners need more than "it is hard": a realistic migration taxonomy (field swap, commitment scheme swap, full redesign), estimated costs for each, and the one partial exception (hybrid architectures that run classical and post-quantum proof systems in parallel). Graph has "Cryptographic Migration" as absent (degree 5, ref support 3), Community 48.
**Evidence:** Grep finds "Cryptographic Migration" as a glossary entry only. "crypto-agility" appears once (line 3308, dismissing it) and once (line 3451, calling it fiction). No positive migration guidance exists. The Midnight case study (§Case Study: Midnight) ends with "it would be a new system" without elaboration.
**Where:** Chapter 7, §One-Way Door — add 200 words developing a three-tier migration cost taxonomy: (a) parameter-only (swap hash, not viable for ZK), (b) commitment-only (e.g., replace KZG with FRI in a compatible system), (c) full architectural redesign. Estimate effort and illustrate with the STARK-inside-SNARK hybrid that RISC Zero / SP1 already use as a partial hedge.

---

### 11. Binius / Binary Tower Fields — The Missing Small-Field Option

**Status:** Thin
**Why it matters:** The book mentions Binius exactly once, in a bullet point: "Binius (Irreducible, 2025) reduces embedding overhead by 100x for bit-heavy workloads by working directly over binary tower fields" (line 2175). This is a significant architectural alternative — not just a performance tweak — that directly competes with BabyBear and M31 for bit-heavy zkVM workloads (hashes, boolean circuits, AES). Chapter 7's §Small Fields is where this belongs, positioned as a fourth option alongside BabyBear, M31, and Goldilocks, with an explanation of why a single bit is a native field element in $\mathbb{F}_2$ and what that means for constraint overhead.
**Evidence:** Grep finds "Binius" only at line 2175 (performance bullet) and nowhere in Chapter 7. The field chapter (§Small Fields) covers three fields; a fourth option with 100x advantage for an important workload class is missing. Graph: "BabyBear" is tagged "absent" in the graph's unassigned section, suggesting the graph's field-coverage community sees Binius-adjacent material as under-represented.
**Where:** Chapter 7, §Small Fields, after the M31 and BabyBear sub-sections — add a 150-word "Binary Tower Fields (Binius)" sub-section explaining the 100x claim, the workload class it targets, and why it is not used for lattice-based schemes.

---

### 12. Discrete Logarithm Assumption — Formal Statement Missing

**Status:** Absent (formal treatment)
**Why it matters:** The DLP is the foundational assumption for the entire first half of Chapter 7 — KZG, Groth16, IPA — but the book never formally states it. The informal description ("given $g$ and $h = g^x$, find $x$," line 3043) is correct but elides the group-theoretic setting (what group? what generator? what does "hard" mean formally?). The chapter would be significantly stronger if it stated the CDH/DDH/DLOG hierarchy explicitly: computational Diffie-Hellman is what KZG actually reduces to (via q-SDH), which implies DLOG but is not equivalent. This one page of formalism would ground all subsequent security claims and is absent from the book.
**Evidence:** Grep finds "discrete logarithm" in ~15 places, always informally. "CDH" and "DDH" appear zero times. Graph: "Discrete Logarithm Assumption" — absent (degree 17, ref support 7); "Discrete Logarithm Problem" — absent (degree 10, ref support 4), Community 31 (with Number Field Sieve, Tower NFS, etc.).
**Where:** Chapter 7, §Discrete Logarithm Problem — add a 100-word box formalizing DLOG, CDH, and q-SDH in a group $\mathbb{G}$ with generator $g$, with a one-sentence note on the generic group model as the framework where these reductions are proved.

---

## Summary Table

| # | Concept | Status | Priority | Chapter 7 Section |
|---|---|---|---|---|
| 1 | Bilinear pairing mechanics (Weil/Tate, Miller loop) | Thin | Critical | §KZG |
| 2 | Embedding degree $k$ — why pairing-friendly curves are special | Absent | High | §KZG sidebar |
| 3 | Algebraic Group Model (AGM) — security framework | Absent | High | §Three Hardness Assumptions |
| 4 | Ring-LWE / cyclotomic ring motivation | Thin | High | §Module-SIS |
| 5 | ML-KEM / ML-DSA — what the NIST standards actually specify | Thin | High | §Quantum Threat Horizon |
| 6 | Lattice functional commitments (Wee-Wu, BASIS) | Absent | Medium | §Lattice-Based Proving |
| 7 | Poseidon2 vs. Poseidon / Rescue — algebraic hash family | Thin | Medium | §Algebraic Hash Functions |
| 8 | BabyBear degree-4 extension — NTT security explained | Thin | Medium | §Small Fields |
| 9 | LaBRADOR — commitments-to-commitments, pre-folding ancestor | Thin | Medium | §Lattice-Based Proving |
| 10 | Cryptographic migration taxonomy (positive framework) | Thin | Medium | §One-Way Door |
| 11 | Binius / binary tower fields as a fourth small-field option | Thin | Low-Medium | §Small Fields |
| 12 | Discrete Logarithm Assumption — formal CDH/q-SDH hierarchy | Absent | Low-Medium | §Discrete Logarithm Problem |
