# math-explainer 5-Concept Full-Pipeline Run — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Run the `math-explainer` skill end-to-end on the five `evals/concepts.json` concepts, producing committed, schema-valid, scorecard-PASS chapter-grade drafts — with graphify + Sage + manim all live in WSL and **no fallbacks**.

**Architecture:** Three small skill enhancements first (strict preflight, manim clip toggle, scenes/ + drafts/ scaffolding), then install graphify into WSL so all dependencies are live in one environment, then a strict preflight gate, then run the six-stage pipeline per concept — pilot Schwartz–Zippel in-session, then the other four as parallel Opus subagents — each producing a committed draft bundle, then consolidate.

**Tech Stack:** Python 3 (pytest via `C:\sevenlayer\.venv\Scripts\python.exe` on Windows; system `python3` in WSL), SageMath 10.9 (WSL, `/usr/local/bin/sage`), manim 0.20.1 (WSL, `/usr/local/bin/manim`), graphify 0.8.36 (`git+https://github.com/safishamsi/graphify.git`), the skill's `scripts/` (resolve_deps, run_sage, manim_render, scorecard, schemas, check_env).

**Spec:** `docs/superpowers/specs/2026-06-15-math-explainer-5-concept-run-design.md`.

---

## File structure (created/modified by this plan)

```
.claude/skills/math-explainer/
  scripts/check_env.py            # MODIFY (Task 1): add missing() + `--require` strict mode
  scripts/manim_render.py         # MODIFY (Task 2): render_scene(still=...) clip toggle
  scripts/scenes/                 # NEW dir (Task 3): manim scenes, one per concept
    .gitkeep                      # NEW (Task 3)
    schwartz_zippel.py            # NEW (Task 5, pilot)
    <slug>.py                     # NEW (Task 6, one per remaining concept)
  scripts/recipes/<slug>.sage     # NEW (Tasks 5-6; schwartz_zippel.sage already exists)
  tests/test_check_env.py         # MODIFY (Task 1)
  tests/test_manim_render.py      # MODIFY (Task 2)
master-graph/.drafts/            # NEW (Task 3): persistent committed draft output
  .gitkeep                        # NEW (Task 3)
  <slug>/...                      # NEW (Tasks 5-6): per-concept bundle (see spec §4)
  INDEX.md                        # NEW (Task 7)
```

The five slugs: `schwartz-zippel`, `multilinear-extension`, `sum-check`, `pedersen-commitment`, `bilinear-pairings`.

**Interpreter note:** the deterministic skill-enhancement tasks (1, 2) run their tests on Windows with `C:\sevenlayer\.venv\Scripts\python.exe -m pytest` (manim/graphify-gated tests skip there). The graphify install (Task 4) and all pipeline runs (Tasks 5-7) run in WSL where Sage+manim+graphify are live. Commit messages carry **no `Co-Authored-By` trailer**; **do not push**.

---

## Task 1: `check_env --require` strict preflight

**Files:**
- Modify: `.claude/skills/math-explainer/scripts/check_env.py`
- Test: `.claude/skills/math-explainer/tests/test_check_env.py`

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_check_env.py`:
```python
def test_missing_reports_known_absent(monkeypatch):
    import scripts.check_env as ce
    monkeypatch.setattr(ce, "probe", lambda: {"sage": True, "manim": False, "graphify": False})
    assert set(ce.missing(["sage", "manim", "graphify"])) == {"manim", "graphify"}

def test_missing_empty_required_is_satisfied():
    from scripts.check_env import missing
    assert missing([]) == []

def test_main_require_fails_when_missing(monkeypatch):
    import scripts.check_env as ce
    monkeypatch.setattr(ce, "probe", lambda: {"sage": True, "manim": False, "graphify": False})
    assert ce.main(["check_env.py", "--require", "sage,manim,graphify"]) == 1

def test_main_require_passes_when_all_present(monkeypatch):
    import scripts.check_env as ce
    monkeypatch.setattr(ce, "probe", lambda: {"sage": True, "manim": True, "graphify": True})
    assert ce.main(["check_env.py", "--require", "sage,manim,graphify"]) == 0
```
And update the import line at the top of the file to:
```python
from scripts.check_env import probe, mode, missing
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `C:\sevenlayer\.venv\Scripts\python.exe -m pytest .claude\skills\math-explainer\tests\test_check_env.py -v`
Expected: FAIL — `ImportError: cannot import name 'missing'` (and `main` does not accept argv).

- [ ] **Step 3: Implement `missing()` and `--require` in `main`**

In `scripts/check_env.py`, add `missing()` after `mode()` and replace `main`:
```python
def missing(required) -> list[str]:
    """Return the subset of `required` tool names that are not available."""
    report = probe()
    return [t for t in required if not report.get(t, False)]


def main(argv=None) -> int:
    argv = list(sys.argv if argv is None else argv)
    required = []
    if len(argv) >= 3 and argv[1] == "--require":
        required = [t.strip() for t in argv[2].split(",") if t.strip()]
    report = probe()
    for tool, present in report.items():
        print(f"[{'OK ' if present else 'MISSING'}] {tool}")
    print(f"\nMODE: {mode()}")
    if not report["sage"]:
        print("\nSageMath is required for figures. Install: https://www.sagemath.org/ "
              "(or `conda install -c conda-forge sage`).")
    if not report["graphify"]:
        print("graphify is used in Stage 1 for graph-based dependency enrichment "
              "(invoke via the project's system Python per the dual-interpreter rule). "
              "Without it, Stage 1 falls back to MATH_FOUNDATIONS table lookup only.")
    if not report["manim"]:
        print("manim is optional (animation). Without it, the skill uses Sage figures only.")
    if required:
        miss = missing(required)
        if miss:
            print(f"\nREQUIRED MISSING: {', '.join(miss)} — aborting (no fallback).")
            return 1
        print(f"\nREQUIRED OK: {', '.join(required)}")
        return 0
    return 0 if report["sage"] else 1
```
(The `if __name__ == "__main__": raise SystemExit(main())` line is unchanged — `main` now defaults `argv` to `sys.argv`.)

- [ ] **Step 4: Run tests to verify they pass**

Run: `C:\sevenlayer\.venv\Scripts\python.exe -m pytest .claude\skills\math-explainer\tests\test_check_env.py -v`
Expected: PASS (all check_env tests, including the four new ones).

- [ ] **Step 5: Commit**

```bash
git -C C:\sevenlayer add .claude/skills/math-explainer/scripts/check_env.py .claude/skills/math-explainer/tests/test_check_env.py
git -C C:\sevenlayer commit -m "feat(math-explainer): check_env --require strict preflight (no-fallback gate)"
```

---

## Task 2: `render_scene(still=...)` clip toggle

**Files:**
- Modify: `.claude/skills/math-explainer/scripts/manim_render.py`
- Test: `.claude/skills/math-explainer/tests/test_manim_render.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_manim_render.py` (note the new `CLIP_SCENE` uses an actual animation so a video is produced):
```python
CLIP_SCENE = """
from manim import Scene, Circle, Create

class Clip(Scene):
    def construct(self):
        self.play(Create(Circle()))
"""

@pytest.mark.skipif(shutil.which("manim") is None, reason="manim not installed")
def test_render_scene_clip_produces_video(tmp_path):
    scene = tmp_path / "clip_scene.py"
    scene.write_text(CLIP_SCENE, encoding="utf-8")
    out = render_scene(scene, "Clip", media_dir=tmp_path / "media", still=False)
    assert out.exists() and out.suffix in {".mp4", ".gif", ".mov"} and out.stat().st_size > 0
```

- [ ] **Step 2: Run to verify it fails**

Run (Windows): `C:\sevenlayer\.venv\Scripts\python.exe -m pytest .claude\skills\math-explainer\tests\test_manim_render.py -v`
Expected: the new test is SKIPPED on Windows (manim absent) — so to see it fail, this is verified in WSL after Step 3 (`render_scene` currently has no `still` parameter → `TypeError`). On Windows, confirm collection still succeeds and the rest pass.

- [ ] **Step 3: Add the `still` parameter**

In `scripts/manim_render.py`, replace `render_scene` with:
```python
def render_scene(scene_path: Path, scene_name: str, media_dir: Path,
                 quality: str = "l", still: bool = True, timeout: int = 300) -> Path:
    """Render a manim scene and return the output media path.

    Drives a local manim install. With ``still=True`` it saves a single last frame
    (``-s``, PNG — fast, used by the smoke test); with ``still=False`` it renders a short
    clip (mp4/gif). Raises if manim is absent, the render fails, or nothing is produced.
    """
    if shutil.which("manim") is None:
        raise RuntimeError("manim not found on PATH")
    media_dir = Path(media_dir)
    cmd = ["manim", "render", f"-q{quality}"]
    if still:
        cmd.append("-s")
    cmd += ["--media_dir", str(media_dir), str(scene_path), scene_name]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(f"manim failed: {proc.stderr.strip()[-800:]}")
    patterns = ("*.png",) if still else ("*.mp4", "*.gif", "*.mov")
    outs = []
    for pat in patterns:
        outs += list(media_dir.rglob(pat))
    if not outs:
        raise RuntimeError("manim produced no output")
    return sorted(outs)[0]
```

- [ ] **Step 4: Verify on Windows (collection + still path) and in WSL (clip path)**

Run (Windows): `C:\sevenlayer\.venv\Scripts\python.exe -m pytest .claude\skills\math-explainer\tests\test_manim_render.py -v`
Expected: existing tests PASS; both manim-gated tests SKIPPED.

Run (WSL): `wsl -d Ubuntu-26.04 -- bash -lc "cd /mnt/c/sevenlayer/.claude/skills/math-explainer && python3 -m pytest tests/test_manim_render.py -v"`
Expected: all PASS including `test_manim_render_and_value_validation_end_to_end` (still=True) and `test_render_scene_clip_produces_video` (still=False).

- [ ] **Step 5: Commit**

```bash
git -C C:\sevenlayer add .claude/skills/math-explainer/scripts/manim_render.py .claude/skills/math-explainer/tests/test_manim_render.py
git -C C:\sevenlayer commit -m "feat(math-explainer): render_scene still/clip toggle for production animations"
```

---

## Task 3: Scaffold `scripts/scenes/` and `master-graph/.drafts/`

**Files:**
- Create: `.claude/skills/math-explainer/scripts/scenes/.gitkeep`
- Create: `master-graph/.drafts/.gitkeep`

- [ ] **Step 1: Create the directories with tracked placeholders**

Create the two empty files above (so the directories are tracked). No code.

- [ ] **Step 2: Commit**

```bash
git -C C:\sevenlayer add .claude/skills/math-explainer/scripts/scenes/.gitkeep master-graph/.drafts/.gitkeep
git -C C:\sevenlayer commit -m "chore(math-explainer): scaffold scripts/scenes and master-graph/.drafts"
```

---

## Task 4: Install graphify in WSL + strict preflight green

This is an ops task (commands + expected output), not TDD. All commands run in WSL.

- [ ] **Step 1: Create a dedicated graphify conda env (Python 3.13 for wheel availability)**

```bash
wsl -d Ubuntu-26.04 -u root -- bash -lc "/opt/conda/bin/mamba create -y -n graphify -c conda-forge python=3.13 pip"
```
Expected: env created at `/opt/conda/envs/graphify`.

- [ ] **Step 2: Install graphify from its git source (NOT the `graphifyy` PyPI typosquat)**

```bash
wsl -d Ubuntu-26.04 -u root -- bash -lc "/opt/conda/envs/graphify/bin/pip install 'git+https://github.com/safishamsi/graphify.git@137bc2d95139ba7b8b04e1014fe4bcf249668539' && /opt/conda/envs/graphify/bin/graphify --version"
```
Expected: prints `graphify 0.8.36`. (If the pinned commit is unavailable, drop the `@<commit>` to take the default branch.)

- [ ] **Step 3: Put graphify on the WSL PATH via a wrapper (same pattern as sage/manim)**

```bash
wsl -d Ubuntu-26.04 -u root -- bash -lc "printf '#!/bin/bash\nexec /opt/conda/envs/graphify/bin/graphify \"\$@\"\n' > /usr/local/bin/graphify && chmod +x /usr/local/bin/graphify && which graphify && graphify --version"
```
Expected: `/usr/local/bin/graphify` and `graphify 0.8.36`.
(If the heredoc/quoting is awkward through PowerShell, write the two-line wrapper to a Windows file and `tr -d '\r' < /mnt/c/... > /usr/local/bin/graphify` as was done for the sage wrapper.)

- [ ] **Step 4: Smoke-test graphify against the existing graph**

```bash
wsl -d Ubuntu-26.04 -- bash -lc "cd /mnt/c/sevenlayer && graphify query 'Schwartz-Zippel' 2>&1 | head -20"
```
Expected: a real scoped subgraph / nodes referencing the concept (NOT an error and NOT empty). If the graph needs a refresh, run `graphify update .` first. Repeat the query for `'multilinear extension'` to confirm concept coverage.

- [ ] **Step 5: Strict preflight must pass (all three live)**

```bash
wsl -d Ubuntu-26.04 -- bash -lc "cd /mnt/c/sevenlayer/.claude/skills/math-explainer && python3 scripts/check_env.py --require sage,manim,graphify; echo EXIT=$?"
```
Expected: `[OK ] sage`, `[OK ] manim`, `[OK ] graphify`, `MODE: full-multimodal`, `REQUIRED OK: sage, manim, graphify`, `EXIT=0`.
**Do not proceed to Task 5 unless EXIT=0.** A non-zero exit means a dependency is missing — fix it; do not fall back.

- [ ] **Step 6: Record the toolchain state (no commit needed; this is environment state)**

Note in the run log that graphify is now live in WSL. (The env/wrapper live in WSL, not the repo.)

---

## Task 5: Pilot — `schwartz-zippel` full pipeline → committed draft

**Goal:** Run all six `math-explainer` stages for Schwartz–Zippel in-session to produce the reference draft bundle and validate the layout + a real Sage figure + a real manim clip + a real graphify query. The Sage recipe `scripts/recipes/schwartz_zippel.sage` already exists and is reused.

**REQUIRED SUB-SKILL for execution:** read `.claude/skills/math-explainer/SKILL.md` and follow its six stages. All commands run in WSL. Output dir: `master-graph/.drafts/schwartz-zippel/`.

- [ ] **Step 1: Stage 1 — concept_brief (with live graphify)**

Run, and capture outputs into the draft dir:
```bash
wsl -d Ubuntu-26.04 -- bash -lc "cd /mnt/c/sevenlayer && \
  python3 .claude/skills/math-explainer/scripts/resolve_deps.py master-graph/.outline/MATH_FOUNDATIONS.md 'Schwartz' && \
  graphify query 'Schwartz-Zippel' | head -30"
```
Then read Chapter 7's "Reader should already know" from `master-graph/.outline/CHAPTER_BIBLE.md`. Author `master-graph/.drafts/schwartz-zippel/concept_brief.json` with `{concept, stratum, prerequisites, assumed_background, target_depth, learning_objectives}`, incorporating the graphify subgraph. Validate:
```bash
wsl -d Ubuntu-26.04 -- bash -lc "cd /mnt/c/sevenlayer/.claude/skills/math-explainer && python3 scripts/schemas.py concept_brief ../../../master-graph/.drafts/schwartz-zippel/concept_brief.json"
```
Expected: `CONCEPT_BRIEF: VALID`.

- [ ] **Step 2: Stage 2 — stuck_points**

Author `master-graph/.drafts/schwartz-zippel/stuck_points.json` ({misconceptions:[{claim,why_tempting,severity}], dumb_questions, bad_intuitions_to_kill}). Validate with `schemas.py stuck_points <path>` → `STUCK_POINTS: VALID`.

- [ ] **Step 3: Stage 3 — figure (existing recipe) + manim clip + phased prose**

Figure (recipe exists):
```bash
wsl -d Ubuntu-26.04 -- bash -lc "cd /mnt/c/sevenlayer/.claude/skills/math-explainer && sage scripts/recipes/schwartz_zippel.sage"
```
Expected: JSON manifest `{"figure": "assets/figures/schwartz_zippel.svg", "field": 101, "agreement_points": [0], "num_agreements": 1}`.

Author the manim scene `scripts/scenes/schwartz_zippel.py` (a `Scene` named `SchwartzZippel` animating the random-point spot-check: two degree-2 polynomials over a small field and the rare agreement point). Render a clip:
```bash
wsl -d Ubuntu-26.04 -- bash -lc "cd /mnt/c/sevenlayer/.claude/skills/math-explainer && python3 -c \"from scripts.manim_render import render_scene; from pathlib import Path; print(render_scene(Path('scripts/scenes/schwartz_zippel.py'),'SchwartzZippel',Path('assets/manim'),still=False))\""
```
Expected: a path to a non-empty `.mp4`. Copy the SVG and the clip into `master-graph/.drafts/schwartz-zippel/figures/` and `.../animations/`. Write the three Tao phases (pre/rigorous/post) of prose into `draft.md`.

- [ ] **Step 4: Stage 4 — accuracy_report**

Every numeric claim in the prose must match the Sage manifest (field 101, exactly 1 agreement point). Build `scene_values` for the manim scene and check no drift:
```bash
wsl -d Ubuntu-26.04 -- bash -lc "cd /mnt/c/sevenlayer/.claude/skills/math-explainer && python3 -c \"from scripts.manim_render import validate_scene_values; print(validate_scene_values({'num_agreements':1,'field':101},{'num_agreements':1,'field':101}))\""
```
Expected: `[]`. Dispatch an adversarial red-team check on the explanation. Author `accuracy_report.json` `{claims, sage_manifest, ledger_refs, adversarial_findings, verified:true}` embedding the manifest; validate with `schemas.py accuracy_report <path>` → VALID.

- [ ] **Step 5: Stage 5 — comprehension_set**

Author `comprehension_set.json`: recall/apply/transfer/rediscover items, each `{level, question, answer_key, targets_stuck_point, on_miss_route_to}`. Validate with `schemas.py comprehension_set <path>` → VALID.

- [ ] **Step 6: Stage 6 — assemble bundle + gate**

Assemble `master-graph/.drafts/schwartz-zippel/bundle.json` embedding `accuracy_report` + `comprehension_set` (+ phases, modes_order, led_with_visual, motivated_before_defined, notation_in_pre_rigorous, heuristic_rigorous_pairs, stuck_points_predicted/addressed). Then:
```bash
wsl -d Ubuntu-26.04 -- bash -lc "cd /mnt/c/sevenlayer/.claude/skills/math-explainer && \
  python3 scripts/schemas.py bundle ../../../master-graph/.drafts/schwartz-zippel/bundle.json && \
  python3 scripts/scorecard.py ../../../master-graph/.drafts/schwartz-zippel/bundle.json"
```
Expected: `BUNDLE: VALID` and `SCORECARD: PASS` (writes `scorecard.json` with `passed: true`). Finalize `draft.md` (add "Math you'll need" sidebar from prerequisites + "rediscover-it" box + the comprehension set).

- [ ] **Step 7: Commit the pilot**

```bash
git -C C:\sevenlayer add .claude/skills/math-explainer/scripts/scenes/schwartz_zippel.py master-graph/.drafts/schwartz-zippel
git -C C:\sevenlayer commit -m "drafts(schwartz-zippel): chapter-grade math-explainer bundle (pilot)"
```

**Definition of done:** all five artifacts schema-VALID; `SCORECARD: PASS`; real Sage figure + real manim clip produced; graphify was queried and reflected in `concept_brief`; committed. This pilot is the worked template for Task 6.

---

## Task 6: Four concepts in parallel (Opus subagents)

Dispatch **one Opus subagent per concept**, in parallel (independent draft dirs → no conflicts). Each subagent repeats Task 5's six-stage process for its concept, authoring its own `scripts/recipes/<slug>.sage` and `scripts/scenes/<slug>.py`. Provide each subagent the pilot (`master-graph/.drafts/schwartz-zippel/`) as the worked template, plus the concept-specific context below.

**Per-concept targets** (figure = what the Sage recipe must compute correct-by-construction + required manifest keys; animation = what the manim scene must show):

| slug | Chapter / stratum / depth | Sage recipe must compute (manifest keys) | manim scene |
|---|---|---|---|
| `multilinear-extension` | Ch 7 / S3 / R | the unique multilinear extension of a function on `{0,1}ⁿ` (n=2 or 3): emit `figure`, `n`, the cube values, and at least one off-cube evaluation matching the MLE formula | extend the cube's corner values to the continuous multilinear surface |
| `sum-check` | Ch 8 / S9·3 / R | one or more sum-check rounds over a small multivariate polynomial: emit `figure`, the claimed sum `H`, and each round's univariate polynomial coefficients so `g_i(0)+g_i(1)` matches | the round-by-round reduction collapsing the hypercube sum |
| `pedersen-commitment` | Ch 11 / S5 / R | a Pedersen commitment `g^m·h^r` in a concrete cyclic group (e.g. a prime-order subgroup mod p): emit `figure`, group order, `m`, `r`, and the commitment value; demonstrate the hiding/binding numerically | randomness `r` blurring/translating the committed point |
| `bilinear-pairings` | Ch 11 / S6 / R | a bilinear pairing on a small pairing-friendly curve in Sage: emit `figure` and values verifying `e(aP,bQ) == e(P,Q)^(ab)` | the pairing sending two source-group points to a target-group element; bilinearity |

**For each subagent (template prompt):**

- [ ] **Dispatch (one per slug):** "You are running the `math-explainer` skill end-to-end for the concept **<concept>** (slug `<slug>`). Read `C:\sevenlayer\.claude\skills\math-explainer\SKILL.md` and follow its six stages exactly. A complete worked example is at `C:\sevenlayer\master-graph\.drafts\schwartz-zippel\` — mirror its structure. Output to `C:\sevenlayer\master-graph\.drafts\<slug>\`. All Sage/manim/graphify commands run in WSL: `wsl -d Ubuntu-26.04 -- bash -lc '...'` from `/mnt/c/sevenlayer`. ENV is no-fallback — confirm `python3 scripts/check_env.py --require sage,manim,graphify` exits 0 first; if not, STOP and report BLOCKED. Author `scripts/recipes/<slug>.sage` (compute the figure correct-by-construction; emit the manifest keys in the targets table) and `scripts/scenes/<slug>.py` (the animation in the targets table); render a clip with `render_scene(..., still=False)`. Produce concept_brief.json (incorporate a live `graphify query '<concept>'`), stuck_points.json, accuracy_report.json (verified true, embedding the Sage manifest; run an adversarial self-check), comprehension_set.json, and bundle.json. Gate: every artifact must pass `python3 scripts/schemas.py <artifact> <path>` and `python3 scripts/scorecard.py <bundle>` must print `SCORECARD: PASS`. Write `draft.md` (three Tao phases + 'Math you'll need' sidebar + 'rediscover-it' box + comprehension set). Commit with `git -C C:\sevenlayer add master-graph/.drafts/<slug> .claude/skills/math-explainer/scripts/recipes/<slug>.sage .claude/skills/math-explainer/scripts/scenes/<slug>.py` then `git -C C:\sevenlayer commit -m 'drafts(<slug>): chapter-grade math-explainer bundle'` — **NO Co-Authored-By trailer, do not push.** Report: per-stage status, the scorecard result, the figure/clip paths, the commit SHA, and the exact `graphify query` invocation used."

- [ ] **After each subagent returns:** independently verify in WSL:
```bash
wsl -d Ubuntu-26.04 -- bash -lc "cd /mnt/c/sevenlayer/.claude/skills/math-explainer && \
  for a in concept_brief stuck_points accuracy_report comprehension_set bundle; do \
    python3 scripts/schemas.py \$a ../../../master-graph/.drafts/<slug>/\$a.json; done && \
  python3 scripts/scorecard.py ../../../master-graph/.drafts/<slug>/bundle.json"
```
Expected: every artifact `VALID` and `SCORECARD: PASS`. If a subagent reports BLOCKED or a gate fails, re-dispatch with the specific gap (do not accept a partial bundle).

---

## Task 7: Consolidation + index

**Files:**
- Create: `master-graph/.drafts/INDEX.md`

- [ ] **Step 1: Full re-verification across all five concepts**

```bash
wsl -d Ubuntu-26.04 -- bash -lc "cd /mnt/c/sevenlayer/.claude/skills/math-explainer && \
  for s in schwartz-zippel multilinear-extension sum-check pedersen-commitment bilinear-pairings; do \
    echo \"== \$s ==\"; python3 scripts/scorecard.py ../../../master-graph/.drafts/\$s/bundle.json | tail -1; done"
```
Expected: `SCORECARD: PASS` for all five.

- [ ] **Step 2: Write the index**

Create `master-graph/.drafts/INDEX.md` with one line per concept: slug → chapter, one-sentence summary, and links to `draft.md`, `figures/`, `animations/`. Example line:
```markdown
- [Schwartz–Zippel lemma](schwartz-zippel/draft.md) — Ch 7 — why a low-degree polynomial's roots are rare (figure + animation, scorecard PASS).
```

- [ ] **Step 3: Confirm the skill's own suite still passes (no regressions from Tasks 1-2)**

```bash
wsl -d Ubuntu-26.04 -- bash -lc "cd /mnt/c/sevenlayer/.claude/skills/math-explainer && python3 -m pytest tests/ 2>&1 | tail -2"
```
Expected: all PASS (0 skipped in WSL).

- [ ] **Step 4: Commit and finish**

```bash
git -C C:\sevenlayer add master-graph/.drafts/INDEX.md
git -C C:\sevenlayer commit -m "drafts: index for the 5 math-explainer concept bundles"
```
Then run **superpowers:finishing-a-development-branch** (on `main`, local only; do not push unless asked).

---

## Self-review (completed by plan author)

**Spec coverage:** no-fallback invariant → Task 4 strict preflight (`--require`) + every pipeline step runs live in WSL. Stage 0 setup → Tasks 1-4. Output layout (spec §4) → Tasks 3, 5, 6 (per-slug dirs + artifacts). Six-stage workflow (spec §5) → Task 5 steps 1-6 and the Task 6 per-concept process. graphify genuinely invoked (spec §3/§7 done-def) → Task 4 smoke test + Stage 1 in Tasks 5/6 + the required `graphify query` report. Pilot→parallel (spec §6) → Tasks 5 then 6. Verification/done (spec §7) → Task 5 DoD, Task 6 per-subagent verify, Task 7. Single-env WSL (spec §8) → all run commands target WSL. Skill enhancements (spec §10) → Task 1 (`--require`), Task 2 (`render_scene(still=…)`), Task 3 (`scripts/scenes/`).

**Placeholder scan:** Tasks 1-2 give full test+impl code; Task 4 gives exact commands + expected output. Tasks 5-6 are model-driven skill executions (the prose, Sage recipes, and manim scenes are produced by the pipeline at run time, by design) — each is pinned by exact verification gates (schemas.py per artifact + scorecard.py PASS) and concrete figure/animation targets, which is the correct altitude for a generative pipeline run rather than a placeholder.

**Type/name consistency:** `missing()`/`probe()`/`mode()` (check_env) used consistently in Task 1 tests and impl; `render_scene(..., still=…)` signature in Task 2 matches its call sites in Tasks 5-6; artifact names (`concept_brief`, `stuck_points`, `accuracy_report`, `comprehension_set`, `bundle`) match `schemas.py` validators exactly; slugs are identical across Tasks 3/5/6/7.
