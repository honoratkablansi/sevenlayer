# Gap Proposals — Layer 7 + Applications + Cross-cutting (Chapters 8–14)

Analyst: Layer 7 / Applications / Cross-cutting agent  
Date: 2026-06-14  
Scope: Book Chapters 8–14 (on-chain verification, zkVMs, rollups, proof markets, privacy apps, ZKML, identity, zkTLS/oracles, VDFs, proof of solvency, security taxonomy, governance, economics).

---

## Summary of Well-Covered Ground (do NOT re-propose)

The book already handles these solidly — confirmed by grep:

- **Frozen Heart / Fiat-Shamir vulnerability class** — Chapter 8 has a dedicated, detailed section covering Frozen Heart (2022), the Last Challenge Attack (2024), and Solana ZK ElGamal (2025). Well done.
- **Midnight** — Community 13 is the densest in the graph (cohesion 0.17); the book has extensive Midnight coverage throughout.
- **Proof market / Proving-as-a-Service economics** — Chapter 13 has a rich section with margin analysis, Succinct, RISC Zero Boundless, Aligned Layer, cost structure, and trust analysis.
- **ZKML** — Chapter 13 covers DeepProve, EZKL, the overhead tax, and the "proven inference ≠ trustworthy AI" distinction.
- **ZK Identity / eIDAS 2.0 / selective disclosure** — Chapter 9 has eIDAS 2.0, GDPR, zKYC, World/Humanity Protocol, Privacy Pools, and the credential issuance trust surface.
- **Kachina and Zexe** — Chapter 9 has dedicated subsections with formal properties and comparison table.
- **Gas costs and on-chain verification economics** — Chapter 8 covers Groth16/FFLONK gas, EIP-4844/Pectra/Fusaka blob markets, and the verification-data seesaw in detail.
- **Privacy Pools** — mentioned multiple times; well-covered in Chapters 9 and 13.
- **ZK Coprocessors** — Chapter 13 covers Axiom, Brevis, Lagrange, and the trust model shift.
- **Side-channel attacks** (electromagnetic, timing) — discussed in context of witness generation (Chapter 4 area); marked well-covered in graph.
- **Zcash / Sprout / Sapling ceremonies** — used throughout as motivating examples.
- **Rollup DA landscape** (Celestia, EigenDA, Avail) — Chapter 8 covers DA marketplace thoroughly.

---

## Ranked Gap Proposals

### Priority 1 — HIGH IMPACT, ABSENT

---

**1. Verifiable Delay Functions (VDFs)**

| Field | Detail |
|---|---|
| **Status** | Absent |
| **Why it matters** | VDFs are the canonical application of sequential computation + proof: Wesolowski and Pietrzak (2018-2019) constructions enable on-chain randomness beacons and time-lock cryptography that are impossible to manipulate even with parallel compute. Ethereum's beacon chain randomness design explicitly referenced VDFs. They are the clearest illustration of "proof of elapsed time" — a use case orthogonal to correctness proofs but closely related in mechanism. Without VDFs, the book's application survey has a notable blind spot. |
| **Evidence** | Grep for "VDF", "verifiable delay function", "sequential squaring", "randomness beacon" returns zero matches. Graph Community 7 (49 nodes, cohesion 0.07) is entirely devoted to VDFs: Wesolowski, Pietrzak, Cohen & Pietrzak PoSW, repeated squaring in RSA/class groups, and randomness beacon applications — none of this appears in the manuscript. CONCEPTS_FOR_BOOK.md marks "Verifiable delay function (VDF)" as **absent** (degree 24, ref support 3). |
| **Where** | Chapter 8 (Layer 7 / cross-cutting applications) or Chapter 14 (open questions). A 3–4 page treatment of Wesolowski's construction, proof of elapsed time semantics, the randomness beacon application, and why post-quantum VDFs remain open would fill this gap. |

---

**2. Proof of Solvency / Financial Compliance Proofs**

| Field | Detail |
|---|---|
| **Status** | Absent |
| **Why it matters** | After the FTX collapse (November 2022), proof-of-solvency became one of the most discussed real-world ZK applications: proving an exchange holds sufficient reserves to cover liabilities without revealing individual customer balances or the full balance sheet. The Maxwell Merkle-tree approach (pre-ZK) and ZK extensions (Chaum-Pedersen discrete-log proofs, range proofs over aggregated balances) are both referenced in the graph's Community 39. This is a production-relevant, high-stakes application that the book entirely omits despite covering enterprise finance extensively. |
| **Evidence** | Grep for "proof of solvency", "proof of reserves", "solvency", "Merkle proof of liabilities" returns zero matches in the manuscript. CONCEPTS_FOR_BOOK.md marks "Proof of solvency / financial compliance" as **absent** (degree 12, ref support 3). Graph Community 39 (23 nodes, cohesion 0.14) contains: Maxwell Merkle-tree proof of reserves, Chaum-Pedersen proofs, Schnorr proofs of discrete log, Neff mix-nets as prior work. Also listed as a gap for Chapter 3. |
| **Where** | Chapter 9 (Privacy) or Chapter 13 (Market / Applications). A 2–3 page section connecting the FTX moment to the ZK solution, covering the range-proof approach to balance aggregation and the privacy-compliance tradeoff, would be high-value. |

---

**3. zkTLS / DECO / Web Data Provenance**

| Field | Detail |
|---|---|
| **Status** | Absent |
| **Why it matters** | DECO (Zhang et al., CCS 2020) and its descendants (TLSNotary, Reclaim Protocol, zkEmail) allow a user to prove facts derived from TLS-secured web sessions — bank account balances, OAuth logins, medical records — without revealing the full session or requiring server cooperation. This unlocks an enormous class of "prove what you saw on the web" applications: DeFi collateral from bank statements, proof of income, verifiable credentials from existing web infrastructure. The graph has a dedicated 9-node community (Community 11) for this. Community 12 (proof markets) and Community 20 (identity) both have edges into TLS oracle concepts. |
| **Evidence** | Grep for "zkTLS", "DECO", "TLSNotary", "web provenance", "zkEmail" returns no matches in the manuscript. CONCEPTS_FOR_BOOK.md marks "zkTLS / zkEmail web and email provenance" as **absent** (degree 7, ref support 3). Graph Community 11 (42 nodes, cohesion 0.07) has: TLS handshake + record protocol, decentralized oracle for TLS, blockchain oracle protocol, universally composable security via ideal functionality. The snowball surfaced DECO explicitly as a key reference paper. |
| **Where** | Chapter 9 (Privacy applications) or a dedicated subsection in Chapter 13 (Applications). 2–3 pages on the DECO oracle construction, TLSNotary's 2-party MPC approach, privacy tradeoffs, and link to zkTLS for identity/DeFi use cases. |

---

**4. zkBridge / ZK Light Clients / Cross-Chain Proof Aggregation**

| Field | Detail |
|---|---|
| **Status** | Absent |
| **Why it matters** | zkBridge (Xie et al., CCS 2022) and successors (Succinct's SP1-based light clients, Lagrange's cross-chain state proofs) use ZK proofs of consensus to enable trust-minimized cross-chain communication — the same cryptographic technique that backs Ethereum's blob-fee market now enables bridges that don't require honest majority of a multisig. This is one of the highest-value, highest-risk application categories (bridges have lost >$2 billion to hacks). The book covers Lagrange's coprocessor but not the bridge primitive. |
| **Evidence** | Grep for "zkBridge", "light client", "cross-chain bridge", "consensus proof" returns only a single tangential mention of Avail's light-client verification model. CONCEPTS_FOR_BOOK.md marks "zkBridge" as **absent** (degree 10, ref support 2) and "Cross-chain proof aggregation and interop" as **absent** (degree 6, ref support 3). The snowball explicitly surfaced "zkBridge" as a key reference paper. Graph Community 9 has "Distributed Proof Generation" and "Verifiable Computation / Delegation" nodes. |
| **Where** | Chapter 8 (Layer 7 / on-chain verification) or Chapter 13 (Applications). A 2–3 page section distinguishing multisig bridges from ZK light-client bridges, with the attack surface comparison and the cost-security tradeoff, would significantly strengthen the applications survey. |

---

**5. Under-Constrained Circuit Vulnerability Taxonomy (deepened)**

| Field | Detail |
|---|---|
| **Status** | Thin (under-covered in the book's security material) |
| **Why it matters** | The Chaliasos et al. SoK (USENIX Security 2024) provides the first systematic taxonomy of ZK circuit vulnerabilities: under-constrained, over-constrained, computation/constraint mismatch, incorrect public input handling, and library misuse. Chapter 3 mentions under-constrained bugs and the Tornado Cash `===` vs `<==` error, and Chapter 8 covers Fiat-Shamir vulnerabilities in depth. But the full taxonomy — including over-constrained bugs (where valid proofs are rejected), constraint-computation mismatches, and the relationship to formal verification — is absent. Given the book's stated goal of serving auditors, this is a significant gap. |
| **Evidence** | Grep for "SoK.*snark", "Chaliasos", "ARGUZZ", "vulnerability taxonomy", "over-constrained" returns zero matches. CONCEPTS_FOR_BOOK.md marks "Under-Constrained Circuit / Missing Constraint" as **under-covered** (degree 31, ref support 4) and assigns it to Chapter 4. The graph has "Chaliasos et al. — SoK: Understanding Security Vulnerabilities in SNARKs (USENIX Security 2024)" as an explicit node in Community 5 with connections to CVE-2019-7167. |
| **Where** | Chapter 8 (security) or a new Chapter 8 subsection titled "The Vulnerability Taxonomy." 3–4 pages covering all five classes with one concrete example each, keyed to the Chaliasos taxonomy structure. |

---

**6. Rollup Pricing and DoS / Amplification Attacks**

| Field | Detail |
|---|---|
| **Status** | Absent from manuscript |
| **Why it matters** | Chaliasos et al. (2025) identified that ZK rollups with multi-dimensional fee markets (L2 gas + L1 DA + settlement/verification) can be attacked asymmetrically: an adversary can inflate blob consumption to delay finality by 1.45–2.73x the cost of direct L1 blob-stuffing. This is a concrete economic security vulnerability unique to ZK rollup architecture. The book covers the blob fee market and the verification-data seesaw, but not adversarial exploitation of that seesaw. |
| **Evidence** | Grep for "Chaliasos", "amplified finality", "blob stuffing", "griefing", "finality delay attack" returns zero matches in the manuscript. CONCEPTS_FOR_BOOK.md does not list this explicitly, but Graph Community 21 (29 nodes, cohesion 0.10) contains: "Amplified finality-delay attack (1.45x–2.73x over direct L1 blob-stuffing)", "Chaliasos et al. Rollup Pricing Attacks Study (2025)", "Rollup multi-dimensional TFM", "Congestion/Griefing Attack", "Perez & Livshits 'Broken Metre'". Also in Community 17 (security). |
| **Where** | Chapter 8 (Layer 7, gas/economics section). A 1–2 page subsection after "The Verification-Data Seesaw" on multi-dimensional fee-market attacks, explaining why the seesaw itself creates an amplification vector and how rollup sequencers should price to close it. |

---

### Priority 2 — MEDIUM IMPACT, THIN OR ABSENT

---

**7. W3C Verifiable Credentials Standard + SD-JWT / BBS+ (Credential Formats)**

| Field | Detail |
|---|---|
| **Status** | Thin |
| **Why it matters** | The book covers eIDAS 2.0 and selective disclosure conceptually, but does not discuss the actual credential formats: W3C Verifiable Credentials 2.0, SD-JWT (selective-disclosure JWTs), BBS+ signatures (pairing-based, enabling ZK-proofs of possession of subsets of signed attributes), and ISO/IEC 18013-5 (mDL). These are the implementation standards that identity wallet developers actually use, and understanding which cryptography underpins each format matters for the trust analysis. BBS+ is the only format with native ZK properties; SD-JWT relies on hash-based selective disclosure without ZK. The difference is not cosmetic. |
| **Evidence** | Grep for "W3C", "SD-JWT", "BBS+", "mDL", "ISO 18013" returns zero matches. CONCEPTS_FOR_BOOK.md has "Electronic Attestation of Attributes", "European Digital Identity Wallet" and "Selective Disclosure" as under-covered (degree 22, ref support 8); graph Community 29 (25 nodes, cohesion 0.11) contains European Digital Identity Wallet, Qualified Trust Services, Unlinkability, Levels of assurance, Authentic sources. The eIDAS 2.0 section would be materially strengthened by one concrete page on the BBS+ vs. SD-JWT tradeoff. |
| **Where** | Chapter 9 (Privacy) inside the eIDAS 2.0 / ZK Identity section. 1–2 pages on BBS+, SD-JWT, and mDL as the three dominant credential formats, with a table comparing ZK properties. |

---

**8. Proof of Personhood (deepened technical treatment)**

| Field | Detail |
|---|---|
| **Status** | Thin |
| **Why it matters** | The book covers World (Worldcoin) and Humanity Protocol at a business level. It does not discuss the cryptographic mechanism: a Proof of Personhood (PoH) requires a nullifier scheme that prevents double-registration while hiding identity — the same primitive as Zcash's nullifiers, applied to biometric commitments. The threat model (Sybil resistance vs. privacy, the "one person one wallet" guarantee, and the biometric hash binding) deserves technical treatment. With World at tens of millions of users, this is not hypothetical. |
| **Evidence** | CONCEPTS_FOR_BOOK.md marks "Proof of Personhood" as **under-covered** (degree 10, ref support 4) and assigns it to Chapter 13. Graph Community 20 (30 nodes, cohesion 0.10) has: "Proof of Human (PoH)", nullifier, iris biometrics uniqueness properties (FMR beyond 2.5e-14), iris biometrics stability. The manuscript discusses World/Worldcoin at the product level without explaining the nullifier construction. |
| **Where** | Chapter 13 (Applications / Market), inside the ZK Identity section. 1–2 pages connecting the PoH nullifier scheme to Zcash-style nullifiers and explaining the Sybil-resistance vs. privacy tradeoff formally. |

---

**9. Real-Time Proving: Definition, Benchmarks, and Standardization**

| Field | Detail |
|---|---|
| **Status** | Absent (as a formal concept) |
| **Why it matters** | The book mentions "real-time proving is operational" and "16 GPUs" in passing, but does not define the concept formally or discuss the standardization efforts around it. Real-time proving means generating a proof within a single L1 slot (12 seconds for Ethereum), which is the threshold for enshrined proofs (Ethereum roadmap Phase 3). Succinct published a specific benchmark (16 GPUs, 12-second slot); the Ethereum Foundation's "provable security at 128-bit strength by end of 2026" goal is connected to this. The book raises the topic but leaves it technically undefined. |
| **Evidence** | CONCEPTS_FOR_BOOK.md marks "Real-Time Proving" as **absent** (degree 13, ref support 8) and "Realtime Proving Standardized Definition" as **absent** (degree 5, ref support 4). Graph Community 19 has "Enshrined proofs (phase 3 of proving roadmap)" and Community 30 has "Succinct, 'Real-Time Proving with 16 GPUs' (2026)". The manuscript uses the phrase "real-time proving is operational" (line 2990) but never formally defines it. |
| **Where** | Chapter 11 (zkVMs) or Chapter 8 (Layer 7). A 1–2 page box defining real-time proving, the 12-second threshold, the hardware path to achieving it, and the connection to Ethereum's enshrined proofs roadmap. |

---

**10. Verifiable Computation / ZK Coprocessors — Formal Delegation Model**

| Field | Detail |
|---|---|
| **Status** | Thin |
| **Why it matters** | The book describes ZK coprocessors well at the product level (Axiom, Brevis, Lagrange) but does not connect to the formal verifiable computation / delegation model: a delegation scheme is a protocol where a weak client outsources computation to an untrusted server and verifies correctness with less work than re-executing. This is the theoretical grounding for coprocessors, GKR-based proofs for data queries, and the entire "prove SQL queries" space (Verifiable databases and analytics). The GKR protocol — doubly-efficient for bounded-depth circuits — is the theoretical engine behind many coprocessor approaches and is marked entirely absent. |
| **Evidence** | CONCEPTS_FOR_BOOK.md marks "Verifiable computation" as **absent** (degree 27, ref support 16 — high ref support!), "GKR protocol" as **absent** (degree 33, ref support 12), "Delegation of computation" as **absent** (degree 7, ref support 2), and "Verifiable databases and analytics" as **absent** (degree 7, ref support 3). Graph Community 9 has "Verifiable Computation / Delegation" and Community 44 has "Verifiable databases and analytics" and "Outsourced and streaming computation". The ref support of 16 for Verifiable Computation is especially significant — among the highest for absent concepts. |
| **Where** | Chapter 13 (Applications), inside or adjacent to the ZK Coprocessors section. 1–2 pages connecting the Goldwasser-Kalai-Rothblum delegation framework and the GKR protocol to coprocessor products, and gesturing at the theoretical minimum for verifiable database queries. |

---

**11. ZKML — Floating-Point and Quantization Approaches (technical deepening)**

| Field | Detail |
|---|---|
| **Status** | Thin |
| **Why it matters** | The book's ZKML section covers the overhead problem and the DeepProve/EZKL tools but does not explain the primary technical mitigation: quantization (replacing 32-bit floats with 8-bit integers) to reduce the field arithmetic overhead, and the tradeoff with model accuracy. It also omits the zkCNN / Mystique line of work (convolution-specific proof circuits), and the CNN-to-circuit compilation problem that makes image-classification proofs tractable. These details matter for readers who want to understand when ZKML might become practical. |
| **Evidence** | CONCEPTS_FOR_BOOK.md marks "ZKML" as **under-covered** (degree 24, ref support 4) and assigns it to Chapter 13. Grep confirms the manuscript covers DeepProve and EZKL but the overhead section (line 5065) says only that "neural network arithmetic is optimized for floating-point hardware that has no analogue in finite field circuits" without discussing quantization as the standard mitigation. The snowball surfaced "zkCNN" and "ARGUZZ" as key references. Graph Community 117 (the ZKML community) contains "Verifiable / trustless DNN inference" as absent. |
| **Where** | Chapter 13 (ZKML section). Extend the existing section by 1–2 pages: add quantization as the primary mitigation, discuss accuracy-vs-provability tradeoff, and mention zkCNN/Mystique for convolutional networks. |

---

**12. Soundness Attack Taxonomy via Fiat-Shamir (deepened)**

| Field | Detail |
|---|---|
| **Status** | Thin |
| **Why it matters** | Chapter 8's Fiat-Shamir section is excellent on case studies but does not present the formal taxonomy: the difference between *transcript incompleteness* (omitting values from the hash — Frozen Heart class) and *adaptive soundness attacks* via correlation intractability failure (the CGGH04/Ganesh et al. class). The latter is a more subtle attack where the FS hash function is instantiated with a function that is breakable via a circuit-specific chosen-message attack. This distinction matters for understanding *why* the random oracle model is used and what the QROM provides. Community 37 in the graph is devoted to this. |
| **Evidence** | CONCEPTS_FOR_BOOK.md marks "Soundness attack: producing an accepting proof for a false statement in a FS-compiled argument (adaptive and non-adaptive variants)" as **absent** (degree 12, ref support 2). Also marks "Correlation intractability: the property whose circular dependency the attack circumvents" as **absent** (degree 8, ref support 3). Graph Community 37 has both "Frozen Heart / Fiat-Shamir Vulnerability Class" and "Last Challenge Attack (2024)" already well covered, plus correlation intractability as a distinct concept. The existing text conflates both classes as "Fiat-Shamir transcript incompleteness." |
| **Where** | Chapter 8 (Fiat-Shamir section). Add a 1-page "Two classes of Fiat-Shamir failure" box: (1) transcript incompleteness → Frozen Heart / Last Challenge; (2) adaptive soundness attacks via correlation intractability failure → explains why ROM is necessary and what QROM adds. |

---

**13. Media Provenance and C2PA / Image Authentication**

| Field | Detail |
|---|---|
| **Status** | Absent |
| **Why it matters** | The C2PA (Coalition for Content Provenance and Authenticity) standard — backed by Adobe, Microsoft, Google, BBC — defines a cryptographically attested provenance chain for images and video. ZK proofs extend this: they allow a journalist to prove an image was captured by a specific camera model and has undergone only permitted edits (crop, color correction), without revealing metadata that could identify the journalist. This is the "image authentication" use case surfaced by the graph. In the deepfake era, this application may prove more societally important than any DeFi use. |
| **Evidence** | CONCEPTS_FOR_BOOK.md marks "Media provenance" as **absent** (degree 10, ref support 4) and "Image Authentication (IA)" as **absent** (degree 8, ref support 3). Graph Community 60 (19 nodes, cohesion 0.13) is entirely about C2PA: C2PA Manifest, C2PA assertions, Executive Order 14028, in-toto supply-chain framework, provenance attestation. Community 9 lists "Media provenance" as an explicit node. The snowball surfaced "VeriTAS" as a key paper on verifiable image authentication. |
| **Where** | Chapter 13 (Applications). A 2-page section on C2PA + ZK image authentication, connecting to the DECO/zkTLS section (both are "prove facts about captured data"). Would make a strong pair with the VDF randomness-beacon application as "proving what happened in the physical world." |

---

**14. Software Bill of Materials (SBOM) and ZK Supply-Chain Attestation**

| Field | Detail |
|---|---|
| **Status** | Absent |
| **Why it matters** | Executive Order 14028 (May 2021) and subsequent CISA guidance mandated SBOMs for federal software procurement. ZK proofs enable a company to prove to a regulator or customer that its software's dependency tree satisfies compliance requirements (no sanctioned components, no known CVEs above a severity threshold, license compatibility) without revealing the full dependency graph — a trade secret. This application neatly combines the verifiable computation theme with supply-chain security and is being actively prototyped (VeriTAS, ARGUZZ). |
| **Evidence** | CONCEPTS_FOR_BOOK.md marks "Software Bill of Materials (SBOM)" as **absent** (degree 8, ref support 4) and "Software supply chain" as **absent** (degree 9, ref support 3). Graph Community 60 has: "Build integrity and artifact verification", "C2PA Manifest", "Executive Order 14028", "in-toto supply-chain framework", "Component inventory and dependency relationships". Graph Community 55 (20 nodes, cohesion 0.18) models a ZK SBOM prototype (Circom/Poseidon, Nova folding, Spartan wrapper). The snowball surfaced "ARGUZZ" (audit-chain via ZK) as a key reference. |
| **Where** | Chapter 13 (Applications) or Chapter 14 (Open Questions). A 1–2 page section on ZK SBOMs: the SBOM mandate, the privacy problem (full dependency graph as trade secret), the ZK solution (dual-tree architecture), and current prototype status. |

---

**15. Decentralized Identity Protocol Stack (DPC / Compliant Predicates)**

| Field | Detail |
|---|---|
| **Status** | Absent |
| **Why it matters** | The Decentralized Private Computation (DPC) scheme from Bowe et al. / Aleo provides a formal model for user-defined private computation over records, with a compliance predicate that ensures transactions obey public rules while keeping data private. This is the theoretical underpinning of privacy-first blockchains like Aleo, and it sits directly between Zexe (which the book covers) and Midnight (which the book covers extensively). The missing link — how do you compose user-defined functions with protocol-level compliance? — is exactly what DPC formalizes. |
| **Evidence** | CONCEPTS_FOR_BOOK.md marks "Decentralized Private Computation (DPC) scheme" as **absent** (degree 10, ref support 1) and "Compliance predicate / local property of distributed computation" as **absent** (degree 8, ref support 4). Graph Community 43 (22 nodes, cohesion 0.15) is devoted to DPC: records nano-kernel, birth/death predicates, applications (private DEXs, regulation-friendly stablecoins), and comparisons to Hawk, Coda, Groth-Maller. |
| **Where** | Chapter 9 (Privacy Architectures), as a bridge paragraph after the Zexe section and before Midnight: 1 page explaining how DPC generalizes Zexe's records model with an explicit compliance predicate, and how Midnight's `disclose()` mechanism is a practical instantiation of that predicate. |

---

## Summary Table

| # | Concept | Status | Priority | Chapter |
|---|---|---|---|---|
| 1 | Verifiable Delay Functions (VDFs) | Absent | High | Ch 8 or 14 |
| 2 | Proof of Solvency / Reserves | Absent | High | Ch 9 or 13 |
| 3 | zkTLS / DECO / Web Data Provenance | Absent | High | Ch 9 or 13 |
| 4 | zkBridge / ZK Light Clients | Absent | High | Ch 8 or 13 |
| 5 | Under-Constrained Vulnerability Taxonomy (full) | Thin | High | Ch 8 |
| 6 | Rollup Pricing / DoS / Amplification Attacks | Absent | High | Ch 8 |
| 7 | W3C VCs / SD-JWT / BBS+ Credential Formats | Thin | Medium | Ch 9 |
| 8 | Proof of Personhood (nullifier mechanism) | Thin | Medium | Ch 13 |
| 9 | Real-Time Proving (formal definition + roadmap) | Thin | Medium | Ch 8 or 11 |
| 10 | Verifiable Computation / GKR / Delegation (formal) | Thin | Medium | Ch 13 |
| 11 | ZKML: Quantization / zkCNN (technical depth) | Thin | Medium | Ch 13 |
| 12 | Soundness Attack Taxonomy (two FS failure classes) | Thin | Medium | Ch 8 |
| 13 | Media Provenance / C2PA / Image Authentication | Absent | Medium | Ch 13 |
| 14 | SBOM / ZK Supply-Chain Attestation | Absent | Medium | Ch 13 or 14 |
| 15 | DPC / Compliance Predicate (bridge Zexe → Midnight) | Absent | Lower | Ch 9 |
