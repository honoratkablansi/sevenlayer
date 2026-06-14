# Layer 1 — Trusted Setup & Structured Reference Strings: Coverage Gap Proposals

**Scope:** Chapter 2 ("Building the Stage") plus relevant cross-chapter surface area.
**Analyst role:** ZK domain expert reviewing against manuscript grep results, CONCEPTS_FOR_BOOK.md graph signals, and what a complete 2026 treatment of trusted setup requires.

---

## Summary of Evidence Method

All coverage verdicts below are based on targeted Grep searches across the 5,539-line manuscript. "0 mentions" means the term and its synonyms returned no hits. "Named once" means the term appears exactly once, without explanation. Chapter 2 (lines 372–741) was read in full to assess depth of treatment.

---

## Ranked Gap Proposals

### 1. Updatable and Universal Structured Reference String (formal model)

- **Status:** absent
- **Why it matters:** The updatable-SRS concept — introduced by Groth, Kohlweiss, Maller, Meiklejohn, and Miers (CRYPTO 2018) and operationalized in Sonic (CCS 2019) and Marlin (EUROCRYPT 2020) — is the formal definition that makes PLONK-family systems work. Without understanding *updatability* (any party can contribute new randomness to an existing SRS without a fresh ceremony, and the system remains secure if any contribution is honest), the reader cannot understand why universal SNARKs can be trusted even without knowing who generated the initial SRS. The book names Sonic and Marlin but never explains the updatability property that is their key architectural innovation.
- **Evidence:** 0 mentions of "updatable" in the technical sense (references/Sonic/Marlin cited only by name in a single timeline bullet and a footnote). Graph: degree 13, ref-support 6, tagged **absent** in CONCEPTS_FOR_BOOK.md. Community 57 (Sonic-specific hub) shows Mary Maller and updatable SRS as core nodes, confirming the reference corpus treats this as foundational.
- **Where:** Chapter 2, "Universal versus Circuit-Specific Setups" section — extend to distinguish *universal* (one SRS for all circuits) from *updatable* (any party can safely refresh it later). One paragraph and a formal property statement would suffice.

---

### 2. Perpetual Powers of Tau (ongoing open ceremony infrastructure)

- **Status:** absent
- **Why it matters:** The Perpetual Powers of Tau (PPoT), maintained by Hermez/Polygon and the Ethereum community since 2019, is the de facto public infrastructure for BN254 and BLS12-381 KZG ceremonies — the ceremony most projects actually use rather than running their own. Any system not running a bespoke ceremony (Tornado Cash, Hermez, hundreds of smaller projects) used PPoT parameters. The book describes the Ethereum KZG Summoning in depth but never mentions that BN254 projects overwhelmingly rely on PPoT, which is a qualitatively different model (always-open, never-finalized, anyone-can-use).
- **Evidence:** 0 hits for "perpetual powers of tau", "PPOT", or "perpetual ceremony." The Wang–Cohney–Bonneau SoK (cited in the book) covers PPoT extensively. Graph: Powers of Tau node has degree 20, ref-support 6, tagged **under-covered** — but the specific perpetual/always-open variant is entirely absent.
- **Where:** Chapter 2, timeline section ("2019-2022 -- Proliferation" bullet). Replace or expand that bullet to explain PPoT as infrastructure, contrasting with project-specific ceremonies.

---

### 3. Algebraic Group Model (AGM) and Non-Falsifiable Assumptions for SRS-Based Systems

- **Status:** absent
- **Why it matters:** Groth16, PLONK, and KZG do not have security proofs in the standard model. Their proofs require the Algebraic Group Model (Fuchsbauer–Kiltz–Loss, CRYPTO 2018) or knowledge-of-exponent (q-PKE) assumptions — non-falsifiable assumptions that cannot be reduced to any concrete hard problem. A reader who finishes Chapter 2 believing that "1-of-N ceremony honesty implies security" has an incomplete picture: the system is also only secure *if* the AGM holds (i.e., if every adversary is algebraically constrained in how it can use group elements). This is not a footnote — it is why Gentry and Wichs (2011) proved SNARGs cannot be built from falsifiable assumptions, and it sets a hard floor under which no pairing-based setup system can claim purely standard-model security.
- **Evidence:** 0 hits for "algebraic group model", "AGM", "q-PKE", "knowledge of exponent", "non-falsifiable assumption", or "q-SDH" (except one table row referring to q-SDH without explanation). Graph: AGM has degree 14, ref-support 5, tagged **absent**. Community 32 (AD-SNARKs, black-box separations) and Community 22 (QAP/Pinocchio lineage) both cite the knowledge assumption family as a load-bearing concept.
- **Where:** Chapter 2, end of "The Structured Reference String" section, or a new sidebar: "What the security proof actually says."

---

### 4. KZG Polynomial Commitment Scheme (structural explanation)

- **Status:** thin (named frequently, never explained as a commitment scheme)
- **Why it matters:** KZG appears ~100 times in the manuscript but almost always as a label ("KZG commitments," "KZG ceremony") rather than as a construction. The manuscript never explains *why* the SRS enables commitment and evaluation: that committing to polynomial p(x) as C = g^{p(τ)} in G₁ is binding because recovering τ requires solving DLP, and that an evaluation proof at point z is a single group element π = g^{(p(τ)−p(z))/(τ−z)} checkable via one pairing equation. This omission means readers cannot reason about what the SRS actually encodes (powers of τ in G₁ and G₂), why it must be generated with MPC, or why it is structured rather than random. The graph flags this as **absent** with the highest ref-support (10) and degree (81) of any absent concept in the theme.
- **Evidence:** Structural explanation: 0 hits. The closest approach is a one-paragraph section at line 3079–3099 in Chapter 7 (commitment scheme chapter), which covers the scheme but does not connect it back to the SRS generation process. Graph: "KZG Polynomial Commitments from pairings (with trusted setup); Dory transparent pairing-based scheme" — degree 81, ref-support 10, **absent** in per-chapter rollup (unassigned).
- **Where:** Chapter 2, "The Structured Reference String" section. A concrete 3-equation walk-through (commit, open, verify) would let the ceremony description in the same section land with full force.

---

### 5. Subversion Zero-Knowledge and SRS Subversion Attacks

- **Status:** absent
- **Why it matters:** Even a perfectly run ceremony can be subverted if the *software used to generate contributions* is compromised — a "subversion attack" where the prover software embeds a backdoor in the SRS itself (Bellare–Fuchsbauer–Scafuro, 2016; Abdolmaleki–Baghery–Lipmaa–Zajac, 2017). Subversion-ZK is the property that proves remain zero-knowledge even if the SRS was maliciously generated — a strictly stronger guarantee than standard ZK. Systems like Groth–Maller (2017) and later Abdolmaleki et al. achieve subversion-ZK; most systems (including Groth16 and PLONK) do not. The book treats ceremony participants as the only trust surface, never raising the possibility that the contribution *software* could be the attack vector.
- **Evidence:** 0 hits for "subversion", "subversion zero-knowledge", "SRS subversion", or "subversion resistance." The Wang–Cohney–Bonneau SoK (cited at line 666) covers subversion threats extensively. Community 32 in the graph ("Subversion Zero-Knowledge" is a named node in that community) confirms this is present in the reference corpus but absent from the manuscript.
- **Where:** Chapter 2, after the ceremony trust discussion. A paragraph on the distinction between ceremony trust (who generated the SRS) and software trust (whether the generation code was honest), with a pointer to Groth–Maller as the only widely deployed subversion-ZK scheme.

---

### 6. Multi-Party Computation Setup Ceremony (formal MPC protocol structure)

- **Status:** thin
- **Why it matters:** The book describes what ceremonies *achieve* (1-of-N honesty) and who *attends* them (vividly) but never explains the underlying MPC *protocol*: that each participant i holds a secret τᵢ, computes their contribution as a transformation of the previous participant's SRS (raising each element to the power τᵢ), produces a proof of correct computation (typically a Schnorr proof of knowledge of τᵢ), and then discards τᵢ. The final SRS encodes τ = τ₁·τ₂·…·τₙ without any participant knowing τ. Without this structure, readers cannot understand why the "1-of-N" claim holds mathematically, nor why contribution *order* matters, nor why the random beacon at the end of BGM17 ceremonies is necessary.
- **Evidence:** The BGM17 framework is named at line 438 without explanation of its structure. "Proof of correct computation" appears 0 times. Graph: "Multi-Party Computation Setup Ceremony" has degree 11, ref-support 4, tagged **absent**. The Secure Multi-Party Computation node (degree 27, ref-support 5) is tagged **under-covered** in the unassigned section.
- **Where:** Chapter 2, "The Trusted Stage: Ceremonies and the 1-of-N Model" section. A box or sidebar showing the three-step MPC protocol (contribute → prove → destroy) would give the 1-of-N claim a rigorous foundation.

---

### 7. Random Beacon Model for Ceremony Finalization

- **Status:** absent
- **Why it matters:** The BGM17 ceremony protocol (used in Zcash Sapling and cited in the book) requires a *random beacon* — a publicly verifiable source of randomness published after all contributions are complete — to finalize the SRS and prevent last-participant attacks (where the final contributor, seeing all previous contributions, could bias the output). The book mentions the BGM17 "MMORPG" framework at line 438 without explaining what a random beacon is, why it is needed, or how it is instantiated (e.g., Bitcoin block hashes, NIST randomness beacon). This is not a niche detail: it is a core security mechanism that explains why the transcript includes a finalization step.
- **Evidence:** 0 hits for "random beacon", "randomness beacon", "beacon model", or "last participant attack." Community 7 in the graph is a full hub (49 nodes) dedicated to VDFs, randomness beacons, and groups of unknown order — confirming the reference corpus treats these as important. BGM17 is cited but its key mechanism goes unexplained.
- **Where:** Chapter 2, "The Trusted Stage" section, when BGM17 is introduced. One paragraph explaining the last-participant bias problem and the random beacon solution.

---

### 8. On-Chain Ceremony Verification / Coordinator-Free Ceremonies

- **Status:** thin (one bullet, no explanation)
- **Why it matters:** Nikolaenko–Ragsdale–Bonneau–Boneh (ACNS 2024 / ePrint 2022/1592) is cited at line 441 as "2025+ — on-chain ceremonies" but the citation does nothing. The concept is consequential: on-chain ceremony verification replaces the trusted coordinator with a smart contract that enforces correct contribution ordering and rejects invalid contributions in real time. This eliminates the coordinator as a trust surface entirely (solving the "D" of the ADOPT framework) while remaining compatible with the 1-of-N security model. As of 2026, this represents the state of the art for ceremony design and is directly relevant to readers evaluating whether to trust any existing SRS.
- **Evidence:** Single line mention at line 441, zero explanation of mechanism. The ADOPT framework discussion at lines 664–680 notes coordinator dependence as a failure mode without connecting it back to the on-chain solution already cited. Graph: Community 5 contains the Ethereum KZG Summoning node with strong connections to Nikolaenko et al.
- **Where:** Chapter 2, expand the 2025+ timeline bullet into a substantive paragraph; connect it to the ADOPT "D" (decentralization) criterion already in the chapter.

---

### 9. Dory and Transparent Pairing-Based Polynomial Commitments

- **Status:** absent
- **Why it matters:** The book presents a clean binary: KZG (pairing-based, requires trusted setup) vs. FRI/IPA (transparent, no pairings). This is a false dichotomy. Dory (Lee, 2020) achieves *transparent* polynomial commitments using pairings — the SRS is a set of random group elements that need not be secret, so no ceremony is required. This closes an important conceptual gap: pairings are not intrinsically ceremony-requiring; the ceremony requirement is specific to the *structured* (powers-of-tau) form of KZG. Dory is currently impractical for production (verifier is O(log n) pairings vs. KZG's O(1)), but it shows the design space is richer than the book implies, and it is the reference the CONCEPTS_FOR_BOOK.md graph tags as absent alongside KZG.
- **Evidence:** 0 hits for "Dory", "transparent pairing", or "pairing without setup." Graph: "KZG Polynomial Commitments from pairings (with trusted setup); Dory transparent pairing-based scheme" is a single graph node — degree 81, ref-support 10, **absent**. The ref corpus groups them deliberately, signaling the contrast is analytically important.
- **Where:** Chapter 2, "The Transparent Alternative" or "The Setup Tradeoff" section. One paragraph noting Dory as proof that pairings and ceremonies are separable, with the caveat that Dory's current performance makes it research rather than production.

---

### 10. Circuit-Specific Setup Security Properties (simulation-extractability and the Groth16 bound)

- **Status:** absent
- **Why it matters:** Groth16 is the most deployed circuit-specific SNARK, but its security property is *knowledge soundness* under the AGM — not the stronger *simulation-extractability* (SE) required for composable protocols. Groth–Maller (2017) showed that without SE, Groth16 proofs are malleable: an adversary who sees a valid proof can produce a different valid proof for the same statement. This is not merely theoretical: in composable systems (where proofs are inputs to other proofs), malleability creates attack surfaces. The book mentions Groth16's 192-byte compactness repeatedly but never its malleability limitation, which is directly relevant to Chapter 6 (recursion) and the discussion of why PLONK-family systems are preferred for composable architectures.
- **Evidence:** 0 hits for "simulation-extractable", "simulation extractability", "malleable", "non-malleable." Groth16 is named ~30 times in the manuscript, always for its compactness. Graph: Knowledge-Soundness has degree 12, ref-support 6, tagged **under-covered** — but this specific property of simulation-extractability is absent. Community 5 nodes (Groth16, Chaliasos SoK) are strongly connected, and the SoK reference discusses malleability explicitly.
- **Where:** Chapter 2, "Universal versus Circuit-Specific Setups" section, as the final cost item in the Groth16 trade-off analysis (per-circuit ceremony + malleability vs. universality + malleability-resistance).

---

### 11. SRS Degree Bound and Its Operational Consequences

- **Status:** absent
- **Why it matters:** Every KZG SRS supports circuits only up to a maximum size equal to the degree of the powers-of-tau sequence encoded in it. The Ethereum KZG SRS supports polynomials of degree up to 2²³ ≈ 8M. If a circuit exceeds this bound, it cannot use that SRS — it needs a new, larger ceremony. The book mentions "65 million curve points" at line 412 without explaining this is a degree bound, what it constrains, or how projects choose their SRS size. This operational fact determines whether a given SRS is reusable for a project and is a key input to the "capital expenditure" metaphor the book uses.
- **Evidence:** 0 hits for "degree bound", "SRS size bound", "maximum degree", or "maximum circuit size." The phrase "65 million curve points" at line 412 is the only quantitative reference, without explanation of what that number controls. This is a pure operational gap affecting practitioners reading the book.
- **Where:** Chapter 2, "The Structured Reference String" section, when the 65-million-point figure is introduced. A sentence connecting that number to the maximum circuit size it supports and the consequence of exceeding it.

---

### 12. Ceremony Transcript Preservation and Long-Term Auditability

- **Status:** thin
- **Why it matters:** The ADOPT framework's "P" (persistent) criterion is briefly noted at line 671 and 676, but the book does not explain *why* transcript persistence matters technically: if intermediate contributions are lost, no one can verify that the final SRS is consistent with all contributions, undermining the 1-of-N security argument in retrospect. Hermez's lost transcripts (noted at line 676) are cited as a data point without unpacking the security implication. For a reader evaluating whether to trust a given SRS, understanding the auditability chain from individual contributions to the final output is essential.
- **Evidence:** Lines 671 and 676 mention persistence and Hermez transcript loss without technical explanation. The Wang–Cohney–Bonneau SoK is cited as the source, but its finding is reduced to a one-line observation. This is thin coverage, not absent, but the gap between what is said and what matters is large.
- **Where:** Chapter 2, ADOPT Framework section — extend the "P" bullet to explain the cryptographic consequence of lost transcripts, not just the archival failure.

---

## Coverage Verdict Summary

| # | Concept | Status | Priority |
|---|---------|--------|----------|
| 1 | Updatable SRS (formal model) | absent | critical |
| 2 | Perpetual Powers of Tau | absent | high |
| 3 | AGM / Non-Falsifiable Assumptions | absent | critical |
| 4 | KZG structural explanation (commit/open/verify) | thin | critical |
| 5 | Subversion ZK and SRS subversion attacks | absent | high |
| 6 | MPC ceremony protocol structure | thin | high |
| 7 | Random Beacon Model for finalization | absent | high |
| 8 | On-chain / coordinator-free ceremony | thin | medium |
| 9 | Dory (transparent pairing-based PCS) | absent | medium |
| 10 | Simulation-extractability vs. knowledge-soundness | absent | medium |
| 11 | SRS degree bound and operational consequences | absent | medium |
| 12 | Ceremony transcript preservation (auditability chain) | thin | low-medium |

---

## Deliberately Excluded (well-covered)

- **1-of-N trust model** — thoroughly explained with sociological depth (lines 431–591)
- **ADOPT framework** — present with five criteria and Zcash/Ethereum case studies
- **Quantum shelf life / HNDL** — well-covered with option-value analysis
- **BN254 security erosion (Tower NFS)** — detailed coverage at lines 651–659
- **Toxic waste metaphor** — central to Chapter 2, thoroughly developed
- **Transparent vs. trusted binary** — clearly presented with STARK alternative
- **Hybrid architecture (transparent inner / trusted outer)** — well-explained at lines 391–393 and 543–545
- **Ethereum KZG Summoning** — extensive coverage, including social/operational dimensions

---

*Generated: 2026-06-14. Grepped against proving-nothing.md (5539 lines). Graph signals from master-graph/CONCEPTS_FOR_BOOK.md and GRAPH_REPORT.md.*
