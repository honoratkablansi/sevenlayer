# Gap Proposals: Recursion, Folding & Aggregation

**Theme agent:** Recursion, Folding & Aggregation
**Date:** 2026-06-14
**Scope:** Incrementally Verifiable Computation (IVC), Proof-Carrying Data (PCD), the folding family (Nova, SuperNova, HyperNova, ProtoStar, ProtoGalaxy, CycleFold, Mangrove, Sangria, Neo), accumulation schemes, cycles of elliptic curves, proof aggregation (SnarkPack), lattice folding (LatticeFold/LatticeFold+), recursion-vs-folding distinction, Halo/Halo2/Halo-Infinite, reductions of knowledge, Valiant's IVC, bootstrapping.

## Evidence key
- **grep(N)** = N occurrences in `proving-nothing.md`
- **outline** = present/absent/thin in `recursion/recursion-outline.md`
- **graph** = signal from `CONCEPTS_FOR_BOOK.md`

---

## Ranked Proposals

### 1. Proof-Carrying Data (PCD) — ABSENT

**Status:** Absent from manuscript

**Why it matters:** PCD is the generalization of IVC from chains to DAGs — it is the formalism that makes supply-chain attestation, software SBOM verification, media provenance, and multi-party composition of proofs rigorous. Without it, the applications chapter of the recursion treatment (§3.3–3.4) lacks a theoretical grounding; the author's own recursion outline promises SBOM/PCD as its "canonical PCD instance" throughout.

**Evidence:**
- grep(PCD) = 4 — essentially absent; likely passing mentions only
- grep("proof.carrying data") = 4 (same hits)
- graph: ABSENT, degree=47, ref-support=14 — high-signal gap flagged as unassigned
- outline: Planned in full depth: §1.2.2, §1.6.4, §3.3.1, §3.5.4, §3.6.2, §3.7 — the recursion chapter already covers this extensively

**Verdict:** The recursion outline *thoroughly* plans PCD. This proposal is therefore directed at the **existing 14 chapters** of the manuscript — the current book has almost no treatment of PCD and the recursion chapter must land in an otherwise bare context. The book needs a brief PCD primer (even 2 pages) somewhere in the non-recursion chapters so the concept is not meeting readers cold.

**Where:** New sidebar or box in whatever chapter currently introduces IVC (likely the closest existing discussion around folding in Ch. 6 per the graph). Or a dedicated concept-block in Ch. 2 / Ch. 5.

---

### 2. Accumulation Schemes (formal) — ABSENT

**Status:** Absent from manuscript; thin in current chapters

**Why it matters:** Accumulation schemes are the formal primitive that underlies Halo, Halo2, and the conceptual bridge between full in-circuit recursion and folding. Without understanding what accumulation *is* (defer one expensive check per step, discharge it once at the end), readers cannot distinguish Halo-style recursion from Nova-style folding — they blur into "recursive SNARKs." The distinction is load-bearing for understanding CycleFold, Halo-Infinite, and why folding is strictly weaker yet faster.

**Evidence:**
- grep("accumulation") = 7 — nearly absent; not defined or explained in the manuscript
- grep("split accumulation") = 0, grep("atomic accumulation") = 0 — key sub-concepts entirely missing
- graph: ABSENT, degree=35, ref-support=8 (flagged as unassigned high-priority)
- outline: Planned in §1.3.2 (atomic accumulation as Halo's insight), §2.1.1 (lineage), §2.6.1 — the recursion chapter handles this well

**Verdict:** Gap is in current chapters, not the planned recursion chapter. The manuscript discusses Halo many times (grep=46) without ever formally introducing what an accumulation scheme is. This leaves a dangling concept that the recursion chapter will need readers to understand.

**Where:** Ch. 6 (currently covers IVC, Nova, Halo2) — add a 1-page definition box: "What is an accumulation scheme?" explaining the defer-then-discharge pattern before Nova is introduced.

---

### 3. Recursive Proof Composition — ABSENT (from existing chapters)

**Status:** Absent from current manuscript; fully planned in recursion outline

**Why it matters:** This is the top-ranked *absent* concept in the graph (degree=81, ref-support=30) and the central topic of the planned recursion chapter. However the current 14 chapters of the book apparently do not frame the concept at all — readers arrive at the recursion chapter without the vocabulary.

**Evidence:**
- grep("Recursive [Pp]roof [Cc]omposition") = 11 — these 11 hits are likely chapter-outline text or section headers already present in draft recursion content, not explanatory exposition
- graph: ABSENT, Community 23, degree=81, ref-support=30 — highest-signal absent concept overall
- outline: The entire 3-chapter treatment is planned around this; it is the *title* of the outline

**Verdict:** The recursion outline covers this completely. The gap is that existing chapters do not lay groundwork. Even a single paragraph in the introduction or Ch. 1 mentioning that "proofs can verify other proofs — a theme developed fully in Part X" would pay off the reader's patience.

**Where:** Book introduction or Ch. 1's roadmap section.

---

### 4. Cycles of Elliptic Curves (MNT, Pasta) — ABSENT

**Status:** Absent from manuscript; planned in recursion outline

**Why it matters:** You cannot explain how Nova or Halo2 achieves recursion without cycles. The field-mismatch problem — why you can't just embed a pairing-based verifier in any curve — is the technical reason cycles exist. MNT4/MNT6 cycles, the Pasta cycle (Pallas/Vesta), and why pairing-friendly cycles are hard to find are all load-bearing for understanding CycleFold's innovation.

**Evidence:**
- grep("cycle[s]? of [eE]lliptic|MNT curve|Pasta curve|Pallas|Vesta") = 5 — nearly absent
- graph: ABSENT, degree=40, ref-support=12 (flagged as unassigned)
- graph also flags: MNT curves = absent (degree=11, ref-support=4); Pasta Cycle = absent (degree=9, ref-support=4)
- outline: Planned in §1.3.1 (full recursion via cycles), §2.5.1 (Pasta curves in practice), §2.4.4 (CycleFold) — well-covered in planned chapter

**Verdict:** Recursion outline handles this. Gap is that existing Halo2 / Nova coverage in Ch. 6 doesn't explain *why* two curves are needed. Add 1–2 paragraphs to Ch. 6 on the field-mismatch problem before the recursion chapter elaborates.

**Where:** Ch. 6 (Nova/Halo2 section) — brief field-mismatch explainer. Also: whenever elliptic curves are introduced (Ch. 2 or wherever BN254/BLS12-381 appear), mention the cycle concept as a forward pointer.

---

### 5. IVC (Incrementally Verifiable Computation) — THIN in current chapters

**Status:** Under-covered in existing manuscript; well-planned in recursion outline

**Why it matters:** IVC is the core formal concept that all of Nova, SuperNova, HyperNova, Halo, Plonky2 recursion, and zkVM sharding instantiate. With only 11 hits in the manuscript (many likely incidental), readers lack the definition needed to engage with the folding family.

**Evidence:**
- grep("IVC|incrementally verifiable") = 11 — thin; the graph flags Ch. 6 as the assigned chapter but under-covered (degree=56, ref-support=18)
- graph: under-covered, Community 25
- outline: Planned thoroughly in §1.2.1 (formal definition with the two independence conditions), exercises in all three chapters

**Verdict:** Recursion outline plans this fully. What's missing is a minimal definition in the current Ch. 6 or wherever Nova first appears — currently readers see "IVC" as a label without a formal statement.

**Where:** Ch. 6 — add the two-independence-condition definition (verifier time and per-step prover work both independent of history) as a boxed definition before discussing Nova.

---

### 6. Recursion-vs-Folding Distinction — ABSENT

**Status:** Absent (the distinction is not drawn anywhere in the manuscript)

**Why it matters:** Conflating folding with recursion is the most common conceptual error in ZK education material. Nova does *not* produce a succinct proof at each step — it produces a running relaxed instance. A folding scheme is strictly weaker than a recursive argument, yet it is faster because of this weakness. Without this distinction, readers misread Nova benchmarks, misunderstand what CycleFold optimizes, and cannot evaluate production pipelines that mix both.

**Evidence:**
- grep("recursion.vs.folding|recursion vs fold|folding vs recursion") = 0 — entirely absent
- grep("folding") = 152 — folding appears often but apparently never contrasted with full recursion
- outline: §2.1.2 addresses this under "Folding schemes as a primitive" and §2.1.3 "What you give up" — planned but only in the deep-dive chapter

**Verdict:** The planned Chapter 2 on folding handles this. But the current manuscript, which discusses folding 152 times, apparently never draws the distinction. This is a conceptual clarity gap in existing content that does not require the recursion chapter to be written — it should be fixed now.

**Where:** Wherever folding is first introduced in existing chapters (likely Ch. 6 or Ch. 5 per graph). Add a "What folding is NOT" box: no standalone proof until final compression, soundness deferred, not a SNARK.

---

### 7. Halo-Infinite and the Accumulation Scheme Family — ABSENT

**Status:** Absent from manuscript

**Why it matters:** Halo-Infinite (Bünz, Chiesa, Lin, Mishra, Spooner, CRYPTO 2021) is the paper that formalized accumulation schemes as a standalone primitive usable without succinct arguments — separating the concept from both Halo (2019) and Nova (2022). It is the theoretical bridge that explains *why* accumulation generalizes and how PCD can be obtained from accumulation without any SNARK. Missing this leaves an intellectual gap between Halo and Nova.

**Evidence:**
- grep("Halo Infinite|halo infinite|Halo-Infinite") = 1 — single mention
- grep("Halo") = 46 — Halo is discussed but apparently not Halo-Infinite specifically
- graph: "Halo Infinite" = absent (degree=5, ref-support=3); "Halo / Nested Amortization Recursion" = well-covered (Community 9)
- graph also flags: "Proof-Carrying Data without Succinct Arguments" (Bünz et al. CRYPTO 2021) is referenced in the outline as load-bearing
- outline: Referenced in §1.3.2, §2.1.1, §2.6.1 — the recursion chapter cites it in its proper lineage position

**Verdict:** A short mention in existing Ch. 6 Halo coverage ("Halo-Infinite (2021) formalized accumulation as a primitive independent of any specific proof system") is needed to close the gap. The recursion chapter will elaborate.

**Where:** Ch. 6, Halo/Halo2 discussion.

---

### 8. Valiant's IVC (2008) and the Historical Lineage — ABSENT

**Status:** Absent from manuscript

**Why it matters:** Valiant's TCC 2008 paper is the origin of IVC — the concept did not exist before it. A book on ZK proving that discusses IVC without crediting its origin misses a formative intellectual moment. The theoretical lineage (Valiant → Chiesa-Tromer PCD → BCTV cycles → Halo accumulation → Nova folding) is itself a story about how the community progressively cheapened recursion over 15 years.

**Evidence:**
- grep("Valiant") = 1 — single occurrence
- grep("Valiant.*IVC|IVC.*Valiant") = 1 — same hit; not explained
- outline: Referenced in §1.1.1, §1.1.4, §1.2.1 — the recursion chapter properly places it in the historical arc

**Verdict:** The recursion outline handles history well. The current manuscript's single Valiant mention is insufficient to prime readers. This is a background-building gap, not a topic gap per se.

**Where:** Whatever existing historical or foundational section touches SNARKs or IVC (Ch. 1 or Ch. 2 per the graph).

---

### 9. SnarkPack and Aggregation Layers — THIN

**Status:** Under-covered in manuscript (9 hits, no deep treatment)

**Why it matters:** SnarkPack (Gailly, Maller, Nitulescu, FC 2022) is the most important *non-recursive* proof aggregation scheme: it aggregates n Groth16 proofs in O(log n) verifier work using inner-product arguments and pairings, with no recursion. Understanding when to use SnarkPack vs. recursive aggregation is a critical practitioner decision — and it is the main example in the recursion outline's §1.5.4 "When NOT to recurse."

**Evidence:**
- grep("SnarkPack|snarkpack") = 9 — present but not given a dedicated treatment
- grep("proof aggregation|Proof [Aa]ggregation") = 9 — similarly surface-level
- graph: "Proof Aggregation" = under-covered (degree=27, ref-support=5, Ch. 8); "SnarkPack" not separately listed but implied by Proof Aggregation node
- outline: Planned in §1.5.4 as the "when not to recurse" example and in §3.7.2

**Verdict:** Recursion outline covers SnarkPack in context. But the current Ch. 8 treatment (per graph) is thin — SnarkPack deserves a half-page dedicated explanation: what it does, why it's O(log n), what it requires (Groth16, structured SRS), and when it beats recursion. This does NOT require the recursion chapter to be written.

**Where:** Ch. 8 (proof aggregation) — deepen SnarkPack explanation with verifier cost model and comparison to recursive aggregation.

---

### 10. Compliance Predicates (PCD's Local Property) — ABSENT

**Status:** Absent from manuscript

**Why it matters:** A compliance predicate is the local property each node in a PCD computation must verify — it specifies what "correct behavior" means for one party in a distributed protocol, together with any proofs received from predecessors. Without this concept, the SBOM, supply-chain, credential, and financial-compliance applications in the recursion chapter's §3.3–3.5 are described without the formal vocabulary that makes them ZK proofs rather than just ordinary attestations.

**Evidence:**
- grep("compliance predicate|local property.*distributed") = 0 — entirely absent
- graph: "Compliance predicate / local property of distributed computation" = absent (degree=8, ref-support=4; flagged in Community 55)
- outline: Used extensively in §1.2.2, §3.3.1, §3.5.1, §3.6.2 — the recursion chapter depends on it but never defines it separately from PCD

**Verdict:** Not covered by the recursion outline as a standalone definition; it is assumed to be explained alongside PCD. Since PCD itself is absent from the current manuscript, compliance predicates are doubly absent. A short definition should be placed wherever PCD is introduced.

**Where:** Same section as the PCD primer proposed in #1.

---

### 11. LatticeFold / LatticeFold+ — SURFACE COVERAGE, DEPTH NEEDED

**Status:** Listed as "well-covered" in graph (38 occurrences for "Neo" pattern, LatticeFold well-covered), but conceptual depth is likely missing

**Why it matters:** LatticeFold (Boneh-Chen, ePrint 2024/257) and LatticeFold+ (2025) are the only published routes to post-quantum folding. The core technical challenge — that random linear combinations of short lattice vectors are NOT short, destroying the homomorphism that folding depends on — and the decomposition trick that solves it are non-obvious and worth 2–3 paragraphs of explanation. Without them, "LatticeFold is post-quantum folding" is a label without understanding.

**Evidence:**
- grep("LatticeFold|lattice fold") = 38 (via Neo pattern which catches related lattice material) — present, but depth unclear
- graph: LatticeFold/LatticeFold+ = "well-covered"; Neo (Lattice Folding over Small Fields) = absent (degree=14)
- outline: Planned in §2.7.1 with explicit mention of norm growth and decomposition techniques — the recursion chapter is the right home for depth

**Verdict:** The recursion outline plans this well. The current manuscript's LatticeFold coverage needs verification — if it lacks the norm-growth/decomposition explanation, that is the gap to fill in the recursion chapter's §2.7.1, not elsewhere.

**Where:** Recursion Ch. 2, §2.7.1 — ensure norm-growth problem and decomposition solution are explained, not just labeled.

---

### 12. Neo (Lattice Folding over Small Fields) — ABSENT

**Status:** Absent from manuscript

**Why it matters:** Neo extends lattice-based folding to work over small prime fields (compatible with STARK pipelines), combining two major trends: the shift to small fields for efficient recursion (BabyBear, Mersenne-31) and the push toward post-quantum security. As of 2025–26, Neo represents the frontier of what a fully PQ + small-field folding pipeline could look like.

**Evidence:**
- grep("Neo folding|Neo.*lattice|lattice.*small field") = 0 — absent
- graph: "Neo (Lattice Folding over Small Fields)" = absent (degree=14, ref-support=0 — very recent work)
- outline: Not mentioned explicitly in the recursion outline — this is a genuine gap even in the planned chapter

**Verdict:** This goes BEYOND the recursion outline's planned content. §2.7.2 ("Folding without curve cycles") is the natural home — the outline marks it as "frankly exploratory" and mentions hash-based/small-field accumulation, but Neo specifically should be named and described as the lattice approach to the same goal.

**Where:** Recursion Ch. 2, §2.7.2 — add Neo as the lattice-based path to hash-friendly, PQ-compatible folding over small fields.

---

### 13. Reduction of Knowledge — ABSENT

**Status:** Absent from manuscript

**Why it matters:** A "reduction of knowledge" (RoK) is the generalization of a proof of knowledge to protocols that reduce one relation to another rather than directly extracting a witness. Folding schemes are reductions of knowledge: they reduce "know witnesses for two R1CS instances" to "know a witness for one relaxed R1CS instance." The concept is needed to state precisely what soundness a folding scheme achieves and why it composes into IVC. Without it, security discussions remain informal.

**Evidence:**
- grep("reduction of knowledge|reductions of knowledge") = 1 — single mention, not explained
- graph: "Reduction of Knowledge" = absent (degree=8, ref-support=4; Community 34)
- outline: Not named explicitly, but §2.6.1 uses forking-lemma / extractor language that presupposes this concept

**Verdict:** Goes BEYOND the recursion outline (not mentioned by name). Add a short definition in the recursion Chapter 2, §2.6.1, before the knowledge soundness proof: "A reduction of knowledge reduces checking (inst₁, wit₁) and (inst₂, wit₂) to checking (inst_folded, wit_folded); extractor runs the RoK protocol and solves a linear system."

**Where:** Recursion Ch. 2, §2.6.1.

---

### 14. Sangria (Folding for PLONK) — ABSENT

**Status:** Absent from manuscript and recursion outline

**Why it matters:** Sangria (Nick, Stefanovska, 2022) extends the relaxed-instance trick from R1CS to Plonkish arithmetization, enabling Nova-style folding for PLONK-based circuits without rewriting them as R1CS. Given that PLONK and UltraPlonk are among the most widely used constraint systems in production, Sangria is a practically important member of the folding family tree that connects §2.2's R1CS-specific machinery to the broader ecosystem.

**Evidence:**
- grep("Sangria") = 1 — single hit, not explained
- graph: Not listed separately, but Folding Scheme is a god node and PLONK is under-covered in the folding context
- outline: Not mentioned in the recursion outline — genuine gap in planned content

**Verdict:** Goes BEYOND the recursion outline. Should be added to §2.4 (The Family Tree) as a short entry alongside ProtoStar/ProtoGalaxy: "Sangria applies Nova's relaxation to Plonkish constraint systems, removing the need to compile PLONK circuits to R1CS before folding."

**Where:** Recursion Ch. 2, §2.4 — add as a short entry in the family tree table (§2.4.5).

---

### 15. Bootstrapping (Recursion from FHE / Gentry's Trick) — ABSENT

**Status:** Absent from manuscript; tangentially planned in recursion outline

**Why it matters:** Bootstrapping in the ZK/IVC sense refers to Gentry's 2009 trick of encoding a decryption circuit inside itself — the original instance of a circuit that verifies its own computation. While bootstrapping in FHE and in IVC are different concepts, the underlying "encode verification in-circuit" idea is shared, and the BCTV recursion paper (STOC 2013) explicitly draws this parallel. A book on ZK recursion that doesn't acknowledge this intellectual history misses a formative connection.

**Evidence:**
- grep("bootstrapping|Bootstrapping") = 4 — present but apparently in FHE context only, not ZK recursion context
- graph: "Bootstrapping (FHE)" = absent (degree=15, ref-support=5)
- outline: §1.6.1 ("Fully post-quantum recursion") references FHE components; §2.7.1 references LatticeFold. The IVC-bootstrapping conceptual link is not in the outline.

**Verdict:** Goes partially BEYOND the recursion outline. The outline does not explicitly discuss the IVC-bootstrapping intellectual parallel. A single paragraph in §1.1.3 ("A worked intuition: the proof of a proof") noting "this idea of a circuit verifying itself is the same insight Gentry used for FHE bootstrapping" would add valuable context.

**Where:** Recursion Ch. 1, §1.1.3 — brief historical note connecting Gentry bootstrapping to SNARK recursion's "proof of a proof" intuition.

---

## Summary Table

| # | Concept | Status | Graph Priority | Outline Coverage | Target Location |
|---|---------|--------|---------------|-----------------|-----------------|
| 1 | Proof-Carrying Data (PCD) | Absent from current chapters | HIGH (absent, ref=14) | Full (all 3 planned chapters) | Existing Ch. 6 primer box; recursion Ch. 1 §1.2.2 |
| 2 | Accumulation Schemes (formal) | Absent from current chapters | HIGH (absent, ref=8) | Full (§1.3.2, §2.1.1) | Existing Ch. 6 definition box |
| 3 | Recursive Proof Composition | Absent from current chapters | HIGHEST (absent, ref=30) | Full (entire outline) | Book intro / Ch. 1 roadmap |
| 4 | Cycles of Elliptic Curves | Absent from current chapters | HIGH (absent, ref=12) | Full (§1.3.1, §2.5.1) | Existing Ch. 6 field-mismatch explainer |
| 5 | IVC formal definition | Thin in current chapters | HIGH (under-covered, ref=18) | Full (§1.2.1) | Existing Ch. 6 definition box |
| 6 | Recursion-vs-Folding Distinction | Absent from manuscript | HIGH (implied by both topics) | Planned Ch. 2 §2.1.2–3 | Existing chapter where folding first appears |
| 7 | Halo-Infinite / accumulation primitive | Absent from manuscript | MEDIUM (absent, ref=3) | Referenced in §1.3.2, §2.1.1 | Existing Ch. 6 Halo section |
| 8 | Valiant's IVC historical lineage | Absent from manuscript | MEDIUM (1 mention) | Full (§1.1.1, §1.1.4) | Existing historical / foundational section |
| 9 | SnarkPack & aggregation layers | Thin (9 hits, no depth) | MEDIUM (under-covered, ref=5) | §1.5.4, §3.7.2 | Existing Ch. 8 — deepen |
| 10 | Compliance Predicates | Absent from manuscript | MEDIUM (absent, ref=4) | Used throughout Ch. 1–3 | Same as PCD primer (#1) |
| 11 | LatticeFold depth (norm growth) | Surface label only | Present (well-covered label) | §2.7.1 | Recursion Ch. 2 §2.7.1 |
| 12 | Neo (lattice + small fields) | Absent from manuscript & outline | LOW-NEW (absent, very recent) | NOT in outline — new gap | Recursion Ch. 2 §2.7.2 |
| 13 | Reduction of Knowledge | Absent from manuscript | MEDIUM (absent, ref=4) | NOT named in outline — new gap | Recursion Ch. 2 §2.6.1 |
| 14 | Sangria (PLONK folding) | Absent from manuscript & outline | MEDIUM (absent, implied) | NOT in outline — new gap | Recursion Ch. 2 §2.4 family tree |
| 15 | Bootstrapping (IVC parallel) | Present in FHE sense only | LOW (absent ZK sense, ref=5) | NOT in outline — new gap | Recursion Ch. 1 §1.1.3 |

---

## Outline Coverage Assessment

The recursion outline (`recursion/recursion-outline.md`) is **exceptionally comprehensive** — it covers approximately 85–90% of the canonical recursion/folding canon. Specifically:

**Well-planned by the outline (do NOT re-propose):**
- IVC formal definition (§1.2.1)
- PCD and compliance predicates (§1.2.2, §3.3.1, §1.6.4)
- Accumulation schemes / Halo / atomic vs. split (§1.3.2, §2.1.1)
- Full recursion via curve cycles / field-mismatch (§1.3.1)
- Nova complete protocol (§2.3)
- SuperNova / HyperNova / CCS (§2.4.1–2.4.2)
- ProtoStar / ProtoGalaxy (§2.4.3)
- CycleFold (§2.4.4)
- LatticeFold / LatticeFold+ (§2.7.1)
- STARK recursion / Plonky2 / Fractal (§1.3.4)
- Hybrid STARK-to-SNARK pipelines (§1.3.5)
- SnarkPack as "when not to recurse" (§1.5.4)
- Security: extractor blowup, FS in recursive settings (§1.2.4, §2.6.1–2.6.3)
- Mina / Pickles (§3.2.4, §3.6.3)
- zkVM sharding / continuations (§1.4.2, §3.2.3)
- All major applications: rollups, SBOM, zkML, media provenance, identity (§3.2–3.5)

**Genuine gaps BEYOND the outline (proposals #12–15):**
- **Neo** (lattice folding over small fields) — not mentioned; very recent
- **Reduction of Knowledge** — used implicitly in §2.6.1 but not named or defined
- **Sangria** (PLONK-specific folding) — absent from the family tree
- **Bootstrapping/IVC parallel** — the intellectual connection to Gentry is not drawn

**What the existing 14 chapters need BEFORE the recursion chapter lands (proposals #1–10):**
The current manuscript is thin on the foundational vocabulary. The recursion chapter assumes readers arrive with some grasp of IVC, PCD, accumulation, and cycle arithmetic — but grep counts confirm the manuscript gives them almost none. The most urgent pre-recursion additions are: a PCD primer, an IVC definition box, a field-mismatch/cycles explainer, and the recursion-vs-folding distinction — all in existing Ch. 5/6.
