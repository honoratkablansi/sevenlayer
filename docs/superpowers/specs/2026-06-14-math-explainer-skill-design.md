# `math-explainer` Skill — Design Spec

**Status:** Approved design (2026-06-14). Ready for implementation planning (writing-plans → skill-creator build).

**Goal:** A bespoke Claude Code skill that turns a request like *"explain concept X"* into **book-ready, dependency-aware, multimodal, fact-checked explanatory material** for *Proving Nothing*, executing the combined teaching method of **Grant Sanderson (3Blue1Brown)** and **Terence Tao** on top of the project's existing knowledge assets.

**Primary consumer (locked):** the **author** (an explainer engine that produces book material), not an end-reader tutor. All seven requested capabilities — staged pipeline, comprehension checks, knowledge-dependency awareness, understanding tests, stuck-point prediction, multimodal explanation, factual accuracy — are delivered in service of writing the book.

---

## 1. Locked decisions

1. **Substrate:** pure **Claude-orchestrated** skill (markdown stages + scripts). **No Diffusion-Gemma**, no model fine-tuning, no trained component.
2. **Visualization (v1):** **SageMath** (correct-by-construction static figures) **+ manim** (animated intuition via a manim MCP server). Both ship in v1.
3. **Reuse, don't reinvent.** The skill sits on top of:
   - the **master knowledge graph** (`master-graph/` / graphify) — the knowledge-dependency substrate;
   - **`master-graph/.outline/MATH_FOUNDATIONS.md`** — the 11-stratum math ladder + the adopted Sanderson/Tao/Feynman style;
   - the **book-knowledge claim ledger** — provenance for factual-accuracy checks;
   - **`master-graph/.outline/CHAPTER_BIBLE.md`** — per-chapter assumed background + predicted reader difficulty.
4. **One new dependency:** SageMath (CAS). One optional service: a manim MCP server (with a figure-only fallback if unavailable).
5. **Out of scope (v1):** interactive/runtime tutor mode, Diffusion-Gemma, any fine-tuning, auto-generated final prose voice beyond draft material the author edits.

---

## 2. The teaching method the skill enforces (the "Method Engine")

Two reference cards are loaded on every run and act as the rubric Stages 3/5/6 must satisfy. They make the style *enforced*, not aspirational.

### 2.1 `sanderson-moves.md` — how to build the intuition
1. **Lead with the visual** — show before you tell; ownership comes from seeing first.
2. **Concrete before abstract** — a specific example precedes any general framework.
3. **Motivate before defining** — establish the "why" before notation or formal definition.
4. **Minimize notation early** — let the concept breathe; introduce symbols only when earned.
5. **Anchor on one key example** — a single meaningful case that illuminates the general.
6. **Tell a story** — tension → mystery → resolution.
7. **"You could have invented this"** — guide active rediscovery; the reader derives, not receives.
8. **Exploit symmetry/structure** — make the result feel inevitable.
9. **Leave room for the "aha"** — don't over-explain; preserve the moment of realization.
10. **Motivation > explanation quality** — the binding constraint is making the reader *want* the idea.

### 2.2 `tao-staging.md` — how to stage the rigor
- **Three phases:** **pre-rigorous** (intuition, examples, computation) → **rigorous** (precise, formal, notation now earned) → **post-rigorous** (intuition rebuilt on rigor; "both halves at once").
- **Maxim 1:** *"the point of rigour is not to destroy all intuition; it should destroy bad intuition while clarifying and elevating good intuition."*
- **Maxim 2 (goal state):** *"every heuristic argument naturally suggests its rigorous counterpart, and vice versa"* — so every picture is paired with its formal statement.
- **On-ramp tactics:** ask "dumb questions" and answer them rigorously; anthropomorphize the objects; pick the sub-step "just beyond reach."

*Sources captured in the card footers: Tao, "There's more to mathematics than rigour and proofs"; Tao MasterClass; Sanderson (Buteau distillation; Dwarkesh & Stanford Daily interviews).*

---

## 3. The pipeline (six stages)

Each stage is a unit with a defined input and a structured output (JSON-ish artifacts passed forward). The skill runs them in order; stages 3–6 consult the Method Engine.

### Stage 1 — Scope & dependency resolution  *(knowledge dependencies)*
- **Input:** a concept (e.g., "multilinear extension"), optional target chapter/depth, optional reader-background override.
- **Does:** locate the concept in the master graph (`graphify query`/`explain`/`path` for a scoped subgraph) and in the MATH_FOUNDATIONS strata; pull its prerequisite chain; read the target chapter's assumed background + predicted difficulty from CHAPTER_BIBLE; set target depth (pre-rigorous / rigorous / post-rigorous).
- **Output — `concept_brief`:** `{ concept, stratum, prerequisites[], assumed_background[], target_depth, learning_objectives[] }`.

### Stage 2 — Stuck-point prediction  *(predict where the reader gets stuck)*
- **Input:** `concept_brief`.
- **Does:** from graph prerequisite edges + known misconception patterns + **Tao's "dumb questions"**, enumerate where a reader will trip and which **bad intuitions** the rigorous phase must destroy.
- **Output — `stuck_points`:** `{ misconceptions[]: {claim, why_tempting, severity}, dumb_questions[], bad_intuitions_to_kill[] }`. Feeds Stage 3 and Stage 5.

### Stage 3 — Multimodal explanation  *(multimodal + the staged pipeline)*
Tao's three-phase arc with Sanderson moves inside each phase.
- **Pre-rigorous (Sanderson-led):** concrete hook/story → **lead with the visual** (Sage figure and/or manim scene) → motivate the definition → minimal notation → a **"you could have invented this"** rediscovery prompt. Anchored on one key example, threaded through the running **Sudoku** where it fits.
- **Rigorous (Tao-led):** earn the formal definition / theorem / proof sketch; **explicitly destroy the bad intuitions** from Stage 2; notation introduced here is paid for.
- **Post-rigorous (both):** rebuild intuition on the rigor; **pair every picture with its formal counterpart** (Tao Maxim 2); land the inevitability/"aha" (Sanderson 8–9).
- **Output — `explanation`:** phased content with modes `{ analogy, visual: {sage_code, figure_ref, manim_scene?}, worked_example, formal, synthesis }`.

### Stage 4 — Factual-accuracy verification  *(factual accuracy)*
- **Visual/numeric claims:** every figure is generated **from** a Sage computation; Sage emits a **values manifest** (the actual computed objects/values). Prose claims about those values are checked against the manifest. Because the figure is computed over the correct field/curve, it is **correct by construction**.
- **Animation:** manim scenes are validated against the Sage values manifest so the animation cannot drift from the math.
- **Conceptual/historical claims:** cross-checked against the **book-knowledge claim ledger** (provenance) and the master graph; unsupported claims are flagged, not silently kept.
- **Adversarial pass:** a red-team sub-agent attempts to find an error in the explanation/figure.
- **Output — `accuracy_report`:** `{ claims[], sage_manifest, ledger_refs[], adversarial_findings[], verified: bool }`. A failed verification blocks Stage 6.

### Stage 5 — Comprehension checks  *(checks for comprehension + testing understanding)*
- **Does:** generate diagnostic items spanning **Tao's three stages** plus a Sanderson rediscovery task: a **recall** item (pre-rigorous), an **apply** item (rigorous), a **transfer / "why is it inevitable"** item (post-rigorous), and a **"re-derive it"** rediscovery task. Each targets a predicted stuck-point and a learning objective; each carries an answer key and an **on-miss route** back to the specific prerequisite (from Stage 1) that the miss implies is weak.
- **Output — `comprehension_set`:** `[{ level: recall|apply|transfer|rediscover, question, answer_key, targets_stuck_point, on_miss_route_to }]`.

### Stage 6 — Assembly & integration  *(deliver into the book)*
- **Does:** package everything as book-ready material: phased prose draft + figure files (SVG/PDF) + optional animation + a **"Math you'll need"** sidebar (from Stage 1 prerequisites) + a **"rediscover-it"** box + the comprehension set + **met→locked spiral pointers** (per MATH_FOUNDATIONS).
- **Method-adherence scorecard (release gate):** led with a visual? concrete-before-abstract? motivated before defined? notation earned? staged pre→rigorous→post? every heuristic paired with its rigorous counterpart? every predicted stuck-point addressed? accuracy `verified == true`? A failing scorecard returns to the relevant stage rather than shipping.
- **Output:** a concept bundle directory + a `scorecard.json`.

---

## 4. Skill file structure (skill-creator conventions)

```
math-explainer/
  SKILL.md                      # frontmatter (name, description) + pipeline orchestration
  references/
    pipeline.md                 # the six stages in operational detail
    sanderson-moves.md          # Method Engine card (§2.1)
    tao-staging.md              # Method Engine card (§2.2)
    accuracy-protocol.md        # Stage 4 protocol (Sage manifest + ledger + adversarial)
    dependency-protocol.md      # Stage 1 protocol (graphify queries + strata + bible)
  scripts/
    resolve_deps.py             # Stage 1: query graph + MATH_FOUNDATIONS strata + bible → concept_brief
    sage_figure.sage            # Stage 3/4: compute the object over the right field, plot, emit figure + values manifest
    manim_render.py             # Stage 3: drive the manim MCP (or local manim); validate against the Sage manifest
    scorecard.py                # Stage 6: method-adherence gate
  assets/figures/               # generated figures (gitignored build output)
  evals/                        # concept test set (§6)
```

The pipeline is model-driven (Claude reads SKILL.md and the reference cards and executes the stages), with the four scripts handling the deterministic/external work (graph queries, Sage, manim, scorecard).

---

## 5. Dependencies & environment

- **SageMath** (required) — invoked headless (`sage script.sage`); figures to SVG/PDF; emits a JSON values manifest. Custom plot params (point size, dpi, SVG) to fix the known low-res elliptic-curve-over-finite-field rendering.
- **manim MCP server** (optional but enabled in v1) — drives 3Blue1Brown-style animation; if unreachable, the skill falls back to Sage figures only and notes it.
- **graphify** + the master graph JSON — already present; used read-only via `graphify query/explain/path`.
- **book-knowledge claim ledger** — already present; used read-only for provenance.
- No network model calls beyond the host Claude; no Diffusion-Gemma.

---

## 6. Testing & evaluation

- **Eval concept set** (skill-creator evals): a handful of representative concepts at different strata — e.g. **Schwartz–Zippel** (S2), **multilinear extension** (S3), **sum-check** (S9/3), **bilinear pairing** (S6), **Pedersen commitment** (S5).
- **Per-concept assertions:** Stage 1 resolves the known prerequisites; Stage 2 surfaces at least the known canonical misconception(s); the Sage script **runs and emits a valid figure + manifest**; Stage 4 `verified == true`; the Stage 6 scorecard passes all items; the comprehension set covers all three Tao levels + a rediscovery task.
- **Method-adherence is testable**, because the scorecard is an explicit checklist with pass/fail per item.

---

## 7. Risks & mitigations

1. **Sage figure quality** (default EC-over-finite-field plots are low-res). → Custom point-size/dpi/SVG plotting helpers in `sage_figure.sage`.
2. **manim setup/latency** (MCP dependency, render time). → Optional; figure-only fallback; a "fast path" flag skips animation.
3. **Auto-generated Sage/manim code correctness.** → It either runs or fails; Stage 4 executes it and validates outputs against the manifest, so silent-wrong figures are caught.
4. **Pipeline cost per concept** (six stages + adversarial pass). → Stages are skippable via flags for quick drafts; the full pipeline is reserved for chapter-grade material.
5. **Scope creep toward a runtime tutor.** → Explicitly out of scope; the artifacts are book material, not an interactive app.
6. **Graph/ledger drift** (a recalled prerequisite no longer exists). → Stage 1 verifies resolved nodes against the live graph before use.

---

## 8. Out of scope (v1)

Interactive/real-time reader tutor; Diffusion-Gemma or any fine-tuned model; auto-publishing into the manuscript without author review; non-math (systems/applications) explanation — though the pipeline could later generalize.
