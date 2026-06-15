# Outline Design Brief — "Proving Nothing", next iteration

You are one of several expert architects independently designing a full **outline + table of contents** for the next iteration of a book on zero-knowledge proofs, **"Proving Nothing"** by Charles Hoskinson. Your design will be synthesized with the other architects' designs, so be opinionated and complete.

## The decision already made (scope)
A **bigger, definitive single volume** (theory + practice), ~18–24 chapters across ~5 parts. It keeps the book's signature **seven-layer trust-decomposition thesis** (ZK proofs don't eliminate trust — they decompose it into seven independently-breakable layers: setup → language → witness → arithmetization → proof system → primitives → on-chain verifier) but now also delivers the **rigorous proof-systems core** the enlarged knowledge graph supports.

## NON-NEGOTIABLE pedagogical principle (Feynman)
Every part, chapter, and major concept must **establish conceptual understanding and analogy FIRST, then lock down the mathematics.** Intuition before formalism, always. Favor a **spiral**: a concept is introduced with an analogy/picture, used, and then revisited later at full rigor. For each chapter your outline should name (a) the opening **intuition/analogy hook**, then (b) the **formal payload** that follows.

## The knowledge graph driving this (the source of truth)
A master knowledge graph: **3,000 concept nodes / 8,008 edges / 145 communities**, built by merging the original manuscript + a recursion corpus + the wiki + 101 snowballed foundational papers + Thaler's textbook *Proofs, Arguments, and Zero-Knowledge* + the full Berkeley ZKP MOOC (13 lectures). Use it as the backbone.

**Top god-node concepts (by degree — the backbone the book must orbit):**
SNARK (139), Polynomial Commitment Scheme (123), Zero-Knowledge Proof (117), Groth16 (116), Folding Scheme (116), Sum-Check Protocol (115), Fiat-Shamir Transform (105), KZG (96), Trusted Setup Ceremony (95), R1CS (91), PLONK (88), STARK (83), Recursive Proof Composition (83), FRI (82), Midnight (79), Lattice Cryptography (79), Nova (68), Lookup Argument (65), IVC (62), zkVM (59), GKR (50), CCS (49), Bilinear Pairing (47), Post-Quantum (47), SP1 (47), PCD (47), Interactive Proof (47), Poseidon (46).

**Files you MUST read to ground your design (in C:\sevenlayer):**
- `master-graph/.outline/communities.md` — the graph's ~40 largest communities = candidate chapter clusters (each line lists its top member concepts).
- `master-graph/CONCEPTS_FOR_BOOK.md` — 1,107 concepts ranked by degree+reference-support, each tagged well-covered / under-covered / **absent** vs the current manuscript, with a per-chapter gap rollup. (Your outline should give homes to the high-signal absent/under-covered concepts.)
- `master-graph/proposals/PROPOSED_CONCEPTS.md` — a prior synthesis of the biggest gaps (Tier-1 = foundational theory the book names but never builds: sum-check, IOP, GKR, MLE, KZG construction, QAP, grand-product, AGM; Tier-2 recursion; Tier-3 applications; etc.). Read this — it tells you exactly what the current book is missing.
- `proving-nothing.md` — skim the current manuscript's chapter headings (grep `^#` ) to see what exists today (14 chapters, the 7-layer spine, running examples: a 4×4 Sudoku proof, and Midnight as a case study).

## What to produce
Write your full design to the output path you are given, as markdown:
1. **One-paragraph thesis** for how YOUR lens organizes the book.
2. **The full outline**: Parts → Chapters (numbered) → 2–4 key sections each. For every chapter give: a one-line **intuition hook/analogy** (Feynman opener) and the **formal payload** (what gets locked down), plus the **graph communities/god-nodes** it draws from.
3. **Reading order rationale** — why this sequence (prerequisite/learning-path logic).
4. **What's new vs the current 14-chapter book**, and which high-signal absent concepts you placed where.
5. **Risks/tradeoffs** of your structure.
Be concrete and complete — a real TOC someone could write from.
