# math-explainer Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `math-explainer` Claude Code skill — a six-stage, Sanderson+Tao-method pipeline that turns "explain concept X" into book-ready, dependency-aware, multimodal (Sage + manim), fact-checked material for *Proving Nothing*.

**Architecture:** A project-level skill at `.claude/skills/math-explainer/`. The pipeline is model-driven (Claude reads `SKILL.md` + reference cards and runs the six stages), backed by four deterministic Python/Sage helper scripts (dependency resolver, Sage figure runner, manim value validator, method-adherence scorecard). All deterministic logic is split into pure functions (unit-tested) and external-process wrappers (gated on Sage/manim availability). The skill reuses the project's master graph, `MATH_FOUNDATIONS.md`, the book-knowledge claim ledger, and `CHAPTER_BIBLE.md` — read-only.

**Tech Stack:** Python 3 (helper scripts + pytest), SageMath (`.sage` recipes, correct-by-construction figures), manim via MCP (animation, optional), Markdown (SKILL.md + reference cards). Tests run under the project venv: `python -m pytest`.

**Spec:** `docs/superpowers/specs/2026-06-14-math-explainer-skill-design.md`.

---

## File structure (created by this plan)

```
.claude/skills/math-explainer/
  SKILL.md                       # frontmatter + six-stage orchestration (Task 1 skeleton, Task 8 body)
  conftest.py                    # puts the skill dir on sys.path for tests (Task 1)
  references/
    sanderson-moves.md           # Method Engine card — 10 moves (Task 2)
    tao-staging.md               # Method Engine card — 3 phases + 2 maxims (Task 2)
    dependency-protocol.md       # Stage 1 protocol (Task 7)
    accuracy-protocol.md         # Stage 4 protocol (Task 7)
    pipeline.md                  # six stages in operational detail (Task 7)
  scripts/
    __init__.py                  # makes scripts importable (Task 1)
    scorecard.py                 # Stage 6 gate (Task 3)
    resolve_deps.py              # Stage 1 resolver (Task 4)
    run_sage.py                  # Stage 3/4 Sage runner (Task 5)
    recipes/schwartz_zippel.sage # sample correct-by-construction figure (Task 5)
    manim_render.py              # Stage 3 manim value validator (Task 6)
    check_env.py                 # dependency doctor (Task 10)
  evals/
    concepts.json                # eval concept list (Task 9)
    run_eval.py                  # headless eval harness (Task 9)
    sample_bundle/bundle.json    # a complete Stage-6 bundle for scorecard eval (Task 9)
  tests/
    test_structure.py            # skill layout + content lints (Tasks 1,2,7,8)
    test_scorecard.py            # Task 3
    test_resolve_deps.py         # Task 4
    test_run_sage.py             # Task 5
    test_manim_render.py         # Task 6
    fixtures/mini_foundations.md # resolver fixture (Task 4)
```

### Shared artifact schema (referenced across tasks — keep names consistent)

`bundle.json` (Stage 6 input to the scorecard) — produced by the model-driven assembly stage:
```json
{
  "concept": "Schwartz–Zippel lemma",
  "phases": {"pre_rigorous": "…", "rigorous": "…", "post_rigorous": "…"},
  "modes_order": ["analogy", "visual", "worked_example", "formal", "synthesis"],
  "led_with_visual": true,
  "motivated_before_defined": true,
  "notation_in_pre_rigorous": false,
  "heuristic_rigorous_pairs": [["random spot-check picture", "P(agreement) ≤ d/|F|"]],
  "stuck_points_predicted": ["thinks completeness needs a large field"],
  "stuck_points_addressed": ["thinks completeness needs a large field"],
  "accuracy_verified": true,
  "comprehension_levels": ["recall", "apply", "transfer", "rediscover"],
  "rediscovery_prompt_present": true
}
```

---

## Task 1: Scaffold the skill directory, SKILL.md skeleton, and structure test

**Files:**
- Create: `.claude/skills/math-explainer/SKILL.md`
- Create: `.claude/skills/math-explainer/conftest.py`
- Create: `.claude/skills/math-explainer/scripts/__init__.py`
- Create: `.claude/skills/math-explainer/tests/test_structure.py`

- [ ] **Step 1: Write the failing test**

`.claude/skills/math-explainer/tests/test_structure.py`:
```python
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]

def test_skill_md_has_frontmatter():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---"), "SKILL.md must start with YAML frontmatter"
    fm = text.split("---", 2)[1]
    assert "name: math-explainer" in fm
    assert "description:" in fm

def test_layout_dirs_exist():
    for d in ("references", "scripts", "tests"):
        assert (SKILL / d).is_dir(), f"missing dir: {d}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/skills/math-explainer/tests/test_structure.py -v`
Expected: FAIL (FileNotFoundError — SKILL.md does not exist yet).

- [ ] **Step 3: Create the directories and skeleton files**

`.claude/skills/math-explainer/SKILL.md`:
```markdown
---
name: math-explainer
description: Use when drafting a mathematical concept explanation for the "Proving Nothing" book — produces book-ready, dependency-aware, multimodal (Sage + manim), fact-checked material executing the Sanderson + Tao teaching method via a six-stage pipeline. Triggers include "explain <concept>", "draft the math for <concept>", "build the explanation for <concept>". Not for systems/applications prose, source ingestion, or interactive tutoring.
---

# math-explainer

Six-stage pipeline (full body added in Task 8). Reference cards in `references/`; helper scripts in `scripts/`.
```

`.claude/skills/math-explainer/conftest.py`:
```python
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
```

`.claude/skills/math-explainer/scripts/__init__.py`:
```python
```
(empty file — marks `scripts` as a package)

Also create the empty dirs `references/` and `tests/fixtures/` (add a `.gitkeep` to each so they are tracked):
- `.claude/skills/math-explainer/references/.gitkeep` (empty)
- `.claude/skills/math-explainer/tests/fixtures/.gitkeep` (empty)

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/skills/math-explainer/tests/test_structure.py -v`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/math-explainer
git commit -m "feat(math-explainer): scaffold skill dir, SKILL.md skeleton, structure test"
```

---

## Task 2: Method Engine cards (sanderson-moves.md, tao-staging.md)

**Files:**
- Create: `.claude/skills/math-explainer/references/sanderson-moves.md`
- Create: `.claude/skills/math-explainer/references/tao-staging.md`
- Modify: `.claude/skills/math-explainer/tests/test_structure.py`

- [ ] **Step 1: Add failing tests for the cards**

Append to `.claude/skills/math-explainer/tests/test_structure.py`:
```python
def test_method_cards_exist_and_have_content():
    s = (SKILL / "references" / "sanderson-moves.md").read_text(encoding="utf-8")
    # ten numbered moves
    for n in range(1, 11):
        assert f"{n}." in s, f"sanderson-moves.md missing move {n}"
    t = (SKILL / "references" / "tao-staging.md").read_text(encoding="utf-8")
    for phase in ("pre-rigorous", "rigorous", "post-rigorous"):
        assert phase in t.lower(), f"tao-staging.md missing phase: {phase}"
    assert "destroy bad intuition" in t.lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/skills/math-explainer/tests/test_structure.py::test_method_cards_exist_and_have_content -v`
Expected: FAIL (FileNotFoundError).

- [ ] **Step 3: Write the cards**

`.claude/skills/math-explainer/references/sanderson-moves.md`:
```markdown
# Sanderson moves — how to build the intuition

Apply these in the pre-rigorous and post-rigorous phases. The binding constraint is motivation, not polish.

1. **Lead with the visual.** Show before you tell; ownership comes from seeing first.
2. **Concrete before abstract.** A specific example precedes any general framework.
3. **Empower the learner.** Frame so the reader feels they could have discovered it.
4. **Motivate before defining.** Establish the "why" before notation or formal definition.
5. **Anchor on one key example.** A single meaningful case (use the running Sudoku when it fits).
6. **Tell a story.** Tension → mystery → resolution.
7. **Minimize notation early.** Introduce symbols only when earned.
8. **Exploit symmetry/structure.** Make the result feel inevitable.
9. **Leave room for the "aha".** Don't over-explain; preserve the realization.
10. **Invite active rediscovery.** "You could have invented this" — the reader derives, not receives.

Sources: Sanderson via the Buteau distillation; Dwarkesh & Stanford Daily interviews.
```

`.claude/skills/math-explainer/references/tao-staging.md`:
```markdown
# Tao staging — how to stage the rigor

Stage every explanation in three phases.

- **Pre-rigorous** — intuition, examples, computation. Sanderson moves dominate.
- **Rigorous** — precise definitions, theorems, proof sketch; notation is now *earned*.
- **Post-rigorous** — intuition rebuilt on rigor; use "both halves at once".

**Maxim 1.** The point of rigour is not to destroy all intuition; it should **destroy bad intuition** while clarifying and elevating good intuition. (Use the rigorous phase to kill the Stage-2 bad intuitions explicitly.)

**Maxim 2 (goal state).** Every heuristic argument naturally suggests its rigorous counterpart, and vice versa — so **pair every picture with its formal statement** in the post-rigorous phase.

**On-ramp tactics.** Ask "dumb questions" and answer them rigorously; anthropomorphize the objects; target the sub-step just beyond reach.

Source: Tao, "There's more to mathematics than rigour and proofs"; Tao MasterClass.
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/skills/math-explainer/tests/test_structure.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/math-explainer/references .claude/skills/math-explainer/tests/test_structure.py
git commit -m "feat(math-explainer): add Sanderson and Tao method cards + lint"
```

---

## Task 3: scorecard.py — the method-adherence gate (Stage 6)

**Files:**
- Create: `.claude/skills/math-explainer/scripts/scorecard.py`
- Test: `.claude/skills/math-explainer/tests/test_scorecard.py`

- [ ] **Step 1: Write the failing test**

`.claude/skills/math-explainer/tests/test_scorecard.py`:
```python
import json
from scripts.scorecard import evaluate

def complete_bundle():
    return {
        "concept": "Schwartz–Zippel lemma",
        "phases": {"pre_rigorous": "a", "rigorous": "b", "post_rigorous": "c"},
        "modes_order": ["analogy", "visual", "worked_example", "formal", "synthesis"],
        "led_with_visual": True,
        "motivated_before_defined": True,
        "notation_in_pre_rigorous": False,
        "heuristic_rigorous_pairs": [["picture", "P ≤ d/|F|"]],
        "stuck_points_predicted": ["big-field misconception"],
        "stuck_points_addressed": ["big-field misconception"],
        "accuracy_verified": True,
        "comprehension_levels": ["recall", "apply", "transfer", "rediscover"],
        "rediscovery_prompt_present": True,
    }

def test_complete_bundle_passes_all_checks():
    checks = evaluate(complete_bundle())
    assert all(c["ok"] for c in checks), [c for c in checks if not c["ok"]]

def test_missing_visual_fails_that_check():
    b = complete_bundle()
    b["led_with_visual"] = False
    checks = {c["id"]: c["ok"] for c in evaluate(b)}
    assert checks["led_with_visual"] is False

def test_unaddressed_stuck_point_fails():
    b = complete_bundle()
    b["stuck_points_addressed"] = []
    checks = {c["id"]: c["ok"] for c in evaluate(b)}
    assert checks["stuck_points_addressed"] is False

def test_abstract_before_concrete_fails():
    b = complete_bundle()
    b["modes_order"] = ["formal", "analogy", "worked_example"]
    checks = {c["id"]: c["ok"] for c in evaluate(b)}
    assert checks["concrete_before_abstract"] is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/skills/math-explainer/tests/test_scorecard.py -v`
Expected: FAIL (ModuleNotFoundError: scripts.scorecard).

- [ ] **Step 3: Write scorecard.py**

`.claude/skills/math-explainer/scripts/scorecard.py`:
```python
#!/usr/bin/env python3
"""Stage 6 method-adherence gate.

Reads a bundle JSON describing an assembled concept explanation, checks it against
the Sanderson+Tao rubric, prints a report, writes <bundle_dir>/scorecard.json, and
exits 0 (pass) or 1 (fail).
"""
import json
import sys
from pathlib import Path

TAO_LEVELS = {"recall", "apply", "transfer"}


def evaluate(bundle: dict) -> list[dict]:
    checks: list[dict] = []

    def add(cid, ok, msg):
        checks.append({"id": cid, "ok": bool(ok), "msg": msg})

    modes = bundle.get("modes_order", [])

    def idx(m):
        return modes.index(m) if m in modes else 10 ** 6

    add("led_with_visual", bundle.get("led_with_visual") is True,
        "Pre-rigorous phase must open with a visual (Sanderson #1).")
    add("concrete_before_abstract", min(idx("analogy"), idx("worked_example")) < idx("formal"),
        "A concrete mode must precede the formal mode (Sanderson #2).")
    add("motivated_before_defined", bundle.get("motivated_before_defined") is True,
        "Motivation must precede the formal definition (Sanderson #4).")
    add("notation_earned", bundle.get("notation_in_pre_rigorous") is False,
        "No formal notation in the pre-rigorous phase (Sanderson #7).")
    phases = bundle.get("phases", {})
    add("staged_pre_rigorous_to_post",
        all(phases.get(p) for p in ("pre_rigorous", "rigorous", "post_rigorous")),
        "All three Tao phases must be present and non-empty.")
    add("heuristic_rigorous_pairing", len(bundle.get("heuristic_rigorous_pairs", [])) >= 1,
        "At least one heuristic paired with its rigorous counterpart (Tao Maxim 2).")
    predicted = set(bundle.get("stuck_points_predicted", []))
    addressed = set(bundle.get("stuck_points_addressed", []))
    add("stuck_points_addressed", predicted.issubset(addressed),
        f"All predicted stuck-points must be addressed; missing: {sorted(predicted - addressed)}.")
    add("accuracy_verified", bundle.get("accuracy_verified") is True,
        "Stage 4 must report verified == true.")
    levels = set(bundle.get("comprehension_levels", []))
    add("comprehension_three_levels", TAO_LEVELS.issubset(levels) and "rediscover" in levels,
        "Comprehension set must cover recall/apply/transfer + a rediscovery task.")
    add("rediscovery_prompt", bundle.get("rediscovery_prompt_present") is True,
        "A 'you could have invented this' rediscovery prompt is required (Sanderson #10).")
    return checks


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: scorecard.py <bundle.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    bundle = json.loads(path.read_text(encoding="utf-8"))
    checks = evaluate(bundle)
    passed = all(c["ok"] for c in checks)
    (path.parent / "scorecard.json").write_text(
        json.dumps({"concept": bundle.get("concept"), "passed": passed, "checks": checks}, indent=2),
        encoding="utf-8",
    )
    for c in checks:
        print(f"[{'PASS' if c['ok'] else 'FAIL'}] {c['id']}: {c['msg']}")
    print(f"\nSCORECARD: {'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/skills/math-explainer/tests/test_scorecard.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/math-explainer/scripts/scorecard.py .claude/skills/math-explainer/tests/test_scorecard.py
git commit -m "feat(math-explainer): scorecard gate (Stage 6) + tests"
```

---

## Task 4: resolve_deps.py — dependency resolver (Stage 1)

**Files:**
- Create: `.claude/skills/math-explainer/scripts/resolve_deps.py`
- Create: `.claude/skills/math-explainer/tests/fixtures/mini_foundations.md`
- Test: `.claude/skills/math-explainer/tests/test_resolve_deps.py`

- [ ] **Step 1: Write the fixture and the failing test**

`.claude/skills/math-explainer/tests/fixtures/mini_foundations.md`:
```markdown
### Stratum 2 — Algebra I

| Concept | First needed | Depth | Builds on |
|---|---|---|---|
| **Finite fields** `F_p` | Ch 6 | I→R | modular arithmetic |
| **Schwartz–Zippel lemma** (roots are rare) | Ch 7 | R | polynomials; union bound |

### Stratum 5 — Groups

| Concept | First needed | Depth | Builds on |
|---|---|---|---|
| **Pedersen commitment** (vector form) | Ch 11 | R | cyclic groups, discrete log |
```

`.claude/skills/math-explainer/tests/test_resolve_deps.py`:
```python
from pathlib import Path
from scripts.resolve_deps import parse_strata, resolve

FIX = Path(__file__).resolve().parent / "fixtures" / "mini_foundations.md"

def rows():
    return parse_strata(FIX.read_text(encoding="utf-8"))

def test_parse_skips_header_and_separator_rows():
    concepts = [r["concept"] for r in rows()]
    assert not any(c.lower() == "concept" for c in concepts)
    assert all(set(c) - {"-", ":"} for c in concepts)
    assert len(rows()) == 3

def test_resolve_exact_and_substring():
    rs = rows()
    sz = resolve("Schwartz", rs)
    assert sz is not None
    assert sz["stratum"].startswith("Algebra I")
    assert "polynomials" in sz["prerequisites"]
    assert "union bound" in sz["prerequisites"]

def test_resolve_pedersen_prereqs():
    p = resolve("Pedersen commitment", rows())
    assert p["first_needed"] == "Ch 11"
    assert "cyclic groups" in p["prerequisites"]
    assert "discrete log" in p["prerequisites"]

def test_resolve_unknown_returns_none():
    assert resolve("nonexistent concept", rows()) is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/skills/math-explainer/tests/test_resolve_deps.py -v`
Expected: FAIL (ModuleNotFoundError: scripts.resolve_deps).

- [ ] **Step 3: Write resolve_deps.py**

`.claude/skills/math-explainer/scripts/resolve_deps.py`:
```python
#!/usr/bin/env python3
"""Stage 1: resolve a concept's stratum, prerequisites, and depth from MATH_FOUNDATIONS.md.

Parses the stratum tables and returns a concept_brief. Pure-Python (no graphify import),
so it runs under any interpreter.
"""
import json
import re
import sys
from pathlib import Path

ROW_RE = re.compile(r"^\|(.+)\|\s*$")
STRATUM_RE = re.compile(r"^###\s+Stratum\s+\d+\s+[—-]\s+(.*)$")


def parse_strata(md_text: str) -> list[dict]:
    rows: list[dict] = []
    stratum = None
    for raw in md_text.splitlines():
        line = raw.strip()
        m = STRATUM_RE.match(line)
        if m:
            stratum = m.group(1).strip()
            continue
        rm = ROW_RE.match(line)
        if not rm:
            continue
        cols = [c.strip() for c in rm.group(1).split("|")]
        if len(cols) != 4:
            continue
        concept, first_needed, depth, builds_on = cols
        if concept.lower() == "concept" or set(concept) <= {"-", ":"} or not concept:
            continue  # header or separator row
        prereqs = [p.strip() for p in re.split(r"[;,]", builds_on)
                   if p.strip() and p.strip() != "—"]
        rows.append({
            "stratum": stratum, "concept": concept, "first_needed": first_needed,
            "depth": depth, "prerequisites": prereqs,
        })
    return rows


def resolve(concept: str, rows: list[dict]) -> dict | None:
    cl = concept.lower()
    for r in rows:  # exact first
        if cl == r["concept"].lower():
            return r
    for r in rows:  # substring fallback
        if cl in r["concept"].lower():
            return r
    return None


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: resolve_deps.py <MATH_FOUNDATIONS.md> <concept>", file=sys.stderr)
        return 2
    rows = parse_strata(Path(argv[1]).read_text(encoding="utf-8"))
    brief = resolve(argv[2], rows)
    if brief is None:
        print(json.dumps({"error": f"concept not found: {argv[2]}"}))
        return 1
    print(json.dumps(brief, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/skills/math-explainer/tests/test_resolve_deps.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Verify it works against the real MATH_FOUNDATIONS.md**

Run: `python .claude/skills/math-explainer/scripts/resolve_deps.py master-graph/.outline/MATH_FOUNDATIONS.md "Multilinear extension"`
Expected: JSON with `"stratum"` containing "Multivariate & multilinear" and a non-empty `prerequisites` list.

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/math-explainer/scripts/resolve_deps.py .claude/skills/math-explainer/tests/test_resolve_deps.py .claude/skills/math-explainer/tests/fixtures/mini_foundations.md
git commit -m "feat(math-explainer): MATH_FOUNDATIONS dependency resolver (Stage 1) + tests"
```

---

## Task 5: run_sage.py + sample recipe — correct-by-construction figures (Stage 3/4)

**Files:**
- Create: `.claude/skills/math-explainer/scripts/run_sage.py`
- Create: `.claude/skills/math-explainer/scripts/recipes/schwartz_zippel.sage`
- Test: `.claude/skills/math-explainer/tests/test_run_sage.py`

- [ ] **Step 1: Write the failing test (unit-test the pure parser)**

`.claude/skills/math-explainer/tests/test_run_sage.py`:
```python
import shutil
import pytest
from pathlib import Path
from scripts.run_sage import parse_manifest, run_recipe

def test_parse_manifest_takes_last_json_line():
    out = "Sage startup noise\nignored line\n{\"figure\": \"a.svg\", \"num_agreements\": 2}\n"
    m = parse_manifest(out)
    assert m["figure"] == "a.svg"
    assert m["num_agreements"] == 2

def test_parse_manifest_raises_without_json():
    with pytest.raises(ValueError):
        parse_manifest("no json here\njust text")

@pytest.mark.skipif(shutil.which("sage") is None, reason="SageMath not installed")
def test_run_recipe_schwartz_zippel(tmp_path, monkeypatch):
    monkeypatch.chdir(Path(__file__).resolve().parents[1])  # skill root, so assets/ path resolves
    recipe = Path("scripts/recipes/schwartz_zippel.sage")
    manifest = run_recipe(recipe)
    assert manifest["field"] == 101
    assert manifest["num_agreements"] == len(manifest["agreement_points"])
    assert manifest["num_agreements"] <= 2  # Schwartz–Zippel: two degree-2 polys agree in <= 2 points
    assert Path(manifest["figure"]).exists()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/skills/math-explainer/tests/test_run_sage.py -v`
Expected: FAIL (ModuleNotFoundError: scripts.run_sage). The Sage test is skipped if `sage` is absent.

- [ ] **Step 3: Write run_sage.py and the recipe**

`.claude/skills/math-explainer/scripts/run_sage.py`:
```python
#!/usr/bin/env python3
"""Stage 3/4: run a Sage recipe, capture its JSON values manifest, confirm the figure exists.

A recipe must print, as its last stdout line, a one-line JSON object with at least a
"figure" key (path to the saved figure). The manifest is the source of truth for every
numeric/visual claim downstream (correct-by-construction).
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path


def parse_manifest(stdout: str) -> dict:
    """Return the last stdout line that parses as a JSON object."""
    for line in reversed(stdout.strip().splitlines()):
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    raise ValueError("no JSON manifest found in Sage output")


def run_recipe(recipe: Path, timeout: int = 300) -> dict:
    if shutil.which("sage") is None:
        raise RuntimeError("SageMath ('sage') not found on PATH")
    proc = subprocess.run(["sage", str(recipe)], capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(f"sage failed: {proc.stderr.strip()}")
    manifest = parse_manifest(proc.stdout)
    fig = manifest.get("figure")
    if not fig or not Path(fig).exists():
        raise RuntimeError(f"manifest figure missing: {fig}")
    return manifest


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: run_sage.py <recipe.sage>", file=sys.stderr)
        return 2
    print(json.dumps(run_recipe(Path(argv[1])), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

`.claude/skills/math-explainer/scripts/recipes/schwartz_zippel.sage`:
```python
import json, os
os.makedirs("assets/figures", exist_ok=True)
F = GF(101)
R.<x> = PolynomialRing(F)
p = 3*x^2 + 5*x + 7
q = 3*x^2 + 2*x + 7              # differs from p in exactly the linear term
agree = sorted(int(a) for a in F if p(a) == q(a))
fig = "assets/figures/schwartz_zippel.svg"
plt = point([(int(a), int(p(a))) for a in F], color="blue", size=18, legend_label="p")
plt += point([(int(a), int(q(a))) for a in F], color="red", size=18, legend_label="q")
plt.save(fig, dpi=200)
print(json.dumps({"figure": fig, "field": 101,
                  "agreement_points": agree, "num_agreements": len(agree)}))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/skills/math-explainer/tests/test_run_sage.py -v`
Expected: PASS (2 passed; the Sage integration test passes if `sage` is installed, otherwise SKIPPED).

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/math-explainer/scripts/run_sage.py .claude/skills/math-explainer/scripts/recipes/schwartz_zippel.sage .claude/skills/math-explainer/tests/test_run_sage.py
git commit -m "feat(math-explainer): Sage figure runner + Schwartz-Zippel recipe (Stage 3/4) + tests"
```

---

## Task 6: manim_render.py — value validator (Stage 3)

**Files:**
- Create: `.claude/skills/math-explainer/scripts/manim_render.py`
- Test: `.claude/skills/math-explainer/tests/test_manim_render.py`

- [ ] **Step 1: Write the failing test**

`.claude/skills/math-explainer/tests/test_manim_render.py`:
```python
from scripts.manim_render import validate_scene_values

def test_matching_values_no_errors():
    manifest = {"field": 101, "num_agreements": 2, "agreement_points": [12, 88]}
    scene = {"field": 101, "num_agreements": 2}
    assert validate_scene_values(scene, manifest) == []

def test_numeric_mismatch_reported():
    manifest = {"num_agreements": 2}
    scene = {"num_agreements": 3}
    errs = validate_scene_values(scene, manifest)
    assert len(errs) == 1 and "num_agreements" in errs[0]

def test_keys_absent_from_manifest_are_ignored():
    manifest = {"field": 101}
    scene = {"title": "Schwartz-Zippel"}
    assert validate_scene_values(scene, manifest) == []

def test_list_mismatch_reported():
    manifest = {"agreement_points": [12, 88]}
    scene = {"agreement_points": [12, 87]}
    assert validate_scene_values(scene, manifest)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/skills/math-explainer/tests/test_manim_render.py -v`
Expected: FAIL (ModuleNotFoundError: scripts.manim_render).

- [ ] **Step 3: Write manim_render.py**

`.claude/skills/math-explainer/scripts/manim_render.py`:
```python
#!/usr/bin/env python3
"""Stage 3: validate a manim scene's displayed values against the Sage values manifest.

The actual render is performed by the manim MCP (a model-driven step described in
references/pipeline.md). This module owns the *validation* so an animation can never
drift from the math: every value the scene shows must match the Sage manifest.
"""
import json
import sys
from pathlib import Path


def validate_scene_values(scene_values: dict, manifest: dict, tol: float = 1e-9) -> list[str]:
    """Return mismatch messages for keys present in both dicts."""
    errors: list[str] = []
    for key, sv in scene_values.items():
        if key not in manifest:
            continue
        mv = manifest[key]
        if isinstance(sv, (int, float)) and isinstance(mv, (int, float)) \
                and not isinstance(sv, bool) and not isinstance(mv, bool):
            if abs(float(sv) - float(mv)) > tol:
                errors.append(f"{key}: scene={sv} != manifest={mv}")
        elif sv != mv:
            errors.append(f"{key}: scene={sv!r} != manifest={mv!r}")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: manim_render.py <scene_values.json> <manifest.json>", file=sys.stderr)
        return 2
    scene = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    manifest = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    errors = validate_scene_values(scene, manifest)
    for e in errors:
        print(f"MISMATCH: {e}")
    print(f"\nMANIM VALIDATION: {'PASS' if not errors else 'FAIL'}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/skills/math-explainer/tests/test_manim_render.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/math-explainer/scripts/manim_render.py .claude/skills/math-explainer/tests/test_manim_render.py
git commit -m "feat(math-explainer): manim value validator (Stage 3) + tests"
```

---

## Task 7: Protocol & pipeline reference docs

**Files:**
- Create: `.claude/skills/math-explainer/references/dependency-protocol.md`
- Create: `.claude/skills/math-explainer/references/accuracy-protocol.md`
- Create: `.claude/skills/math-explainer/references/pipeline.md`
- Modify: `.claude/skills/math-explainer/tests/test_structure.py`

- [ ] **Step 1: Add failing test for the reference docs**

Append to `.claude/skills/math-explainer/tests/test_structure.py`:
```python
def test_reference_docs_exist():
    for name in ("dependency-protocol.md", "accuracy-protocol.md", "pipeline.md"):
        p = SKILL / "references" / name
        assert p.exists() and p.read_text(encoding="utf-8").strip(), f"empty/missing: {name}"

def test_pipeline_lists_six_stages():
    text = (SKILL / "references" / "pipeline.md").read_text(encoding="utf-8").lower()
    for n in range(1, 7):
        assert f"stage {n}" in text, f"pipeline.md missing Stage {n}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/skills/math-explainer/tests/test_structure.py -v`
Expected: FAIL (the two new tests fail — files missing).

- [ ] **Step 3: Write the reference docs**

`.claude/skills/math-explainer/references/dependency-protocol.md`:
```markdown
# Stage 1 — dependency protocol

1. Run `scripts/resolve_deps.py master-graph/.outline/MATH_FOUNDATIONS.md "<concept>"` to get the stratum, depth, first-needed chapter, and prerequisite list (concept_brief).
2. Enrich with the master graph for cross-file links: `graphify explain "<concept>"` (or `graphify path "<A>" "<B>"`) for a scoped subgraph. Verify every resolved prerequisite still exists in the live graph; drop stale ones.
3. Read the target chapter's "Reader should already know" line in `master-graph/.outline/CHAPTER_BIBLE.md` to set assumed background and predicted difficulty.
4. Set target depth (pre-rigorous / rigorous / post-rigorous) from MATH_FOUNDATIONS depth code (I / R / A) and the chapter's role.
Output: concept_brief = { concept, stratum, first_needed_chapter, depth, prerequisites[], assumed_background[], target_depth }.
```

`.claude/skills/math-explainer/references/accuracy-protocol.md`:
```markdown
# Stage 4 — factual-accuracy protocol

1. **Visual/numeric claims (correct-by-construction).** Every figure is produced by a Sage recipe via `scripts/run_sage.py`, which returns a values manifest. Extract every numeric/quantitative claim in the draft prose and confirm it matches the manifest. If a claim is not backed by the manifest, recompute it in Sage or remove it.
2. **Animation.** For any manim scene, collect the values it displays into scene_values.json and run `scripts/manim_render.py scene_values.json manifest.json`; it must report PASS (no drift from the Sage manifest).
3. **Conceptual/historical claims.** Cross-check against the book-knowledge claim ledger for provenance; cite the supporting claim(s). Flag any claim with no ledger/graph support rather than keeping it.
4. **Adversarial pass.** Dispatch a red-team check ("find one error in this explanation or figure"); resolve anything it finds.
Output: accuracy_report = { manifest_ref, claim_checks[], ledger_refs[], adversarial_findings[], verified: bool }. `verified` must be true before Stage 6.
```

`.claude/skills/math-explainer/references/pipeline.md`:
```markdown
# The six-stage pipeline (operational detail)

**Stage 1 — Scope & dependency resolution.** See `dependency-protocol.md`. Produces concept_brief.

**Stage 2 — Stuck-point prediction.** From the concept_brief prerequisites + Tao's "dumb questions" + known misconceptions, list where the reader trips and which bad intuitions the rigorous phase must destroy. Produces stuck_points = { misconceptions[], dumb_questions[], bad_intuitions_to_kill[] }.

**Stage 3 — Multimodal explanation.** Tao's three phases with Sanderson moves inside (see `sanderson-moves.md`, `tao-staging.md`):
- Pre-rigorous: concrete hook/story → lead with the Sage figure (run a recipe via `run_sage.py`) and/or a manim scene → motivate the definition → minimal notation → a "you could have invented this" prompt.
- Rigorous: earn the formal definition/theorem/proof; explicitly destroy each Stage-2 bad intuition.
- Post-rigorous: rebuild intuition on rigor; pair every picture with its formal statement; land the "aha".

**Stage 4 — Factual-accuracy verification.** See `accuracy-protocol.md`. Must reach verified == true.

**Stage 5 — Comprehension checks.** Generate a recall (pre), an apply (rigorous), a transfer/"why inevitable" (post) item, plus a Sanderson "re-derive it" task. Each targets a Stage-2 stuck-point and a learning objective, with an answer key and an on-miss route back to a Stage-1 prerequisite.

**Stage 6 — Assembly & gate.** Assemble prose + figures + "Math you'll need" sidebar + "rediscover-it" box + comprehension set + met→locked spiral pointers into a bundle, write `bundle.json`, then run `scripts/scorecard.py bundle.json`. Ship only on PASS; otherwise return to the failing stage.
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/skills/math-explainer/tests/test_structure.py -v`
Expected: PASS (all structure tests pass).

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/math-explainer/references .claude/skills/math-explainer/tests/test_structure.py
git commit -m "feat(math-explainer): dependency/accuracy/pipeline protocol docs + lint"
```

---

## Task 8: SKILL.md full orchestration body

**Files:**
- Modify: `.claude/skills/math-explainer/SKILL.md`
- Modify: `.claude/skills/math-explainer/tests/test_structure.py`

- [ ] **Step 1: Add failing test for the body**

Append to `.claude/skills/math-explainer/tests/test_structure.py`:
```python
def test_skill_body_references_stages_and_scripts():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
    for n in range(1, 7):
        assert f"stage {n}" in text, f"SKILL.md missing Stage {n}"
    for script in ("resolve_deps.py", "run_sage.py", "manim_render.py", "scorecard.py"):
        assert script in text, f"SKILL.md does not reference {script}"
    for card in ("sanderson-moves.md", "tao-staging.md"):
        assert card in text, f"SKILL.md does not reference {card}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/skills/math-explainer/tests/test_structure.py::test_skill_body_references_stages_and_scripts -v`
Expected: FAIL (skeleton body lacks stage/script references).

- [ ] **Step 3: Replace SKILL.md with the full body (keep the frontmatter)**

`.claude/skills/math-explainer/SKILL.md`:
```markdown
---
name: math-explainer
description: Use when drafting a mathematical concept explanation for the "Proving Nothing" book — produces book-ready, dependency-aware, multimodal (Sage + manim), fact-checked material executing the Sanderson + Tao teaching method via a six-stage pipeline. Triggers include "explain <concept>", "draft the math for <concept>", "build the explanation for <concept>". Not for systems/applications prose, source ingestion, or interactive tutoring.
---

# math-explainer

Turn "explain <concept>" into book-ready material that executes the **Sanderson + Tao** method. Run the six stages in order; do not skip the Stage 6 gate.

**Load first:** `references/sanderson-moves.md` and `references/tao-staging.md` (the method rubric), then `references/pipeline.md`.

## The pipeline

- **Stage 1 — Scope & dependency resolution.** Follow `references/dependency-protocol.md`. Run `scripts/resolve_deps.py master-graph/.outline/MATH_FOUNDATIONS.md "<concept>"`. Output: concept_brief.
- **Stage 2 — Stuck-point prediction.** From the prerequisites + Tao's "dumb questions", list misconceptions and the bad intuitions the rigorous phase must destroy.
- **Stage 3 — Multimodal explanation.** Tao's three phases with Sanderson moves inside (`references/pipeline.md`). Produce figures with `scripts/run_sage.py <recipe.sage>`; validate any animation values with `scripts/manim_render.py`.
- **Stage 4 — Factual-accuracy verification.** Follow `references/accuracy-protocol.md`; reach verified == true.
- **Stage 5 — Comprehension checks.** Recall (pre), apply (rigorous), transfer (post), and a "re-derive it" task; each with an answer key and on-miss route to a prerequisite.
- **Stage 6 — Assembly & gate.** Assemble the bundle, write `bundle.json`, run `scripts/scorecard.py bundle.json`. Ship only on PASS.

## Method rubric (enforced by the Stage 6 scorecard)

Led with a visual; concrete before abstract; motivated before defined; notation earned; staged pre→rigorous→post; every heuristic paired with its rigorous counterpart; every predicted stuck-point addressed; accuracy verified; comprehension covers all three Tao levels + rediscovery; a "you could have invented this" prompt present.

## Dependencies

SageMath (`sage` on PATH) for figures; a manim MCP server (optional) for animation — fall back to Sage figures if unavailable. Run `scripts/check_env.py` to verify. The master graph, `MATH_FOUNDATIONS.md`, the book-knowledge ledger, and `CHAPTER_BIBLE.md` are read-only inputs.
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/skills/math-explainer/tests/test_structure.py -v`
Expected: PASS (all structure tests pass).

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/math-explainer/SKILL.md .claude/skills/math-explainer/tests/test_structure.py
git commit -m "feat(math-explainer): full SKILL.md six-stage orchestration body"
```

---

## Task 9: Eval set, sample bundle, and headless eval harness

**Files:**
- Create: `.claude/skills/math-explainer/evals/concepts.json`
- Create: `.claude/skills/math-explainer/evals/sample_bundle/bundle.json`
- Create: `.claude/skills/math-explainer/evals/run_eval.py`
- Test: `.claude/skills/math-explainer/tests/test_eval.py`

- [ ] **Step 1: Write the eval fixtures and the failing test**

`.claude/skills/math-explainer/evals/concepts.json`:
```json
["Schwartz", "Multilinear extension", "Pedersen commitment", "Bilinear pairings", "Sum-Check"]
```

`.claude/skills/math-explainer/evals/sample_bundle/bundle.json`:
```json
{
  "concept": "Schwartz–Zippel lemma",
  "phases": {"pre_rigorous": "random spot-check picture", "rigorous": "P(agreement) <= d/|F|", "post_rigorous": "why a random point almost never lies"},
  "modes_order": ["analogy", "visual", "worked_example", "formal", "synthesis"],
  "led_with_visual": true,
  "motivated_before_defined": true,
  "notation_in_pre_rigorous": false,
  "heuristic_rigorous_pairs": [["random spot-check", "P(agreement) <= d/|F|"]],
  "stuck_points_predicted": ["thinks a large field is needed for completeness"],
  "stuck_points_addressed": ["thinks a large field is needed for completeness"],
  "accuracy_verified": true,
  "comprehension_levels": ["recall", "apply", "transfer", "rediscover"],
  "rediscovery_prompt_present": true
}
```

`.claude/skills/math-explainer/tests/test_eval.py`:
```python
import json
from pathlib import Path
from scripts.resolve_deps import parse_strata, resolve
from scripts.scorecard import evaluate

SKILL = Path(__file__).resolve().parents[1]
ROOT = SKILL.parents[2]  # repo root: .claude/skills/math-explainer -> repo

def test_all_eval_concepts_resolve():
    md = (ROOT / "master-graph" / ".outline" / "MATH_FOUNDATIONS.md").read_text(encoding="utf-8")
    rows = parse_strata(md)
    concepts = json.loads((SKILL / "evals" / "concepts.json").read_text(encoding="utf-8"))
    unresolved = [c for c in concepts if resolve(c, rows) is None]
    assert unresolved == [], f"unresolved eval concepts: {unresolved}"

def test_sample_bundle_passes_scorecard():
    bundle = json.loads((SKILL / "evals" / "sample_bundle" / "bundle.json").read_text(encoding="utf-8"))
    assert all(c["ok"] for c in evaluate(bundle))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/skills/math-explainer/tests/test_eval.py -v`
Expected: FAIL (run_eval.py / fixtures not yet present, or import path — confirm the two tests fail because files are missing).

- [ ] **Step 3: Write the eval harness**

`.claude/skills/math-explainer/evals/run_eval.py`:
```python
#!/usr/bin/env python3
"""Headless smoke-eval for the deterministic core of math-explainer.

Checks: every eval concept resolves against MATH_FOUNDATIONS; the sample bundle passes
the scorecard; and (if Sage is installed) the sample recipe produces a valid manifest.
"""
import json
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL))
from scripts.resolve_deps import parse_strata, resolve          # noqa: E402
from scripts.scorecard import evaluate                          # noqa: E402
from scripts.run_sage import run_recipe                         # noqa: E402

ROOT = SKILL.parents[2]


def main() -> int:
    ok = True
    md = (ROOT / "master-graph" / ".outline" / "MATH_FOUNDATIONS.md").read_text(encoding="utf-8")
    rows = parse_strata(md)
    for c in json.loads((SKILL / "evals" / "concepts.json").read_text(encoding="utf-8")):
        found = resolve(c, rows) is not None
        ok &= found
        print(f"[{'OK ' if found else 'MISS'}] resolve: {c}")

    bundle = json.loads((SKILL / "evals" / "sample_bundle" / "bundle.json").read_text(encoding="utf-8"))
    card_ok = all(x["ok"] for x in evaluate(bundle))
    ok &= card_ok
    print(f"[{'OK ' if card_ok else 'FAIL'}] scorecard: sample bundle")

    if shutil.which("sage"):
        import os
        os.chdir(SKILL)
        m = run_recipe(Path("scripts/recipes/schwartz_zippel.sage"))
        sage_ok = m["num_agreements"] <= 2 and Path(m["figure"]).exists()
        ok &= sage_ok
        print(f"[{'OK ' if sage_ok else 'FAIL'}] sage: schwartz_zippel ({m['num_agreements']} agreements)")
    else:
        print("[SKIP] sage not installed")

    print("\nEVAL:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/skills/math-explainer/tests/test_eval.py -v`
Expected: PASS (2 passed).

- [ ] **Step 5: Run the eval harness end-to-end**

Run: `python .claude/skills/math-explainer/evals/run_eval.py`
Expected: each eval concept `OK`, scorecard `OK`, sage line `OK` (or `SKIP` if Sage absent), final `EVAL: PASS`.

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/math-explainer/evals .claude/skills/math-explainer/tests/test_eval.py
git commit -m "feat(math-explainer): eval set, sample bundle, headless eval harness + tests"
```

---

## Task 10: Dependency doctor + full integration pass

**Files:**
- Create: `.claude/skills/math-explainer/scripts/check_env.py`
- Test: `.claude/skills/math-explainer/tests/test_check_env.py`

- [ ] **Step 1: Write the failing test**

`.claude/skills/math-explainer/tests/test_check_env.py`:
```python
from scripts.check_env import probe

def test_probe_reports_known_tools():
    report = probe()
    assert set(report.keys()) == {"sage", "manim"}
    assert all(isinstance(v, bool) for v in report.values())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/skills/math-explainer/tests/test_check_env.py -v`
Expected: FAIL (ModuleNotFoundError: scripts.check_env).

- [ ] **Step 3: Write check_env.py**

`.claude/skills/math-explainer/scripts/check_env.py`:
```python
#!/usr/bin/env python3
"""Dependency doctor for math-explainer: reports which external tools are available."""
import shutil
import sys


def probe() -> dict:
    return {"sage": shutil.which("sage") is not None,
            "manim": shutil.which("manim") is not None}


def main() -> int:
    report = probe()
    for tool, present in report.items():
        print(f"[{'OK ' if present else 'MISSING'}] {tool}")
    if not report["sage"]:
        print("\nSageMath is required for figures. Install: https://www.sagemath.org/ "
              "(or `conda install -c conda-forge sage`).")
    if not report["manim"]:
        print("manim is optional (animation). Without it, the skill uses Sage figures only.")
    return 0 if report["sage"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/skills/math-explainer/tests/test_check_env.py -v`
Expected: PASS (1 passed).

- [ ] **Step 5: Full suite + integration**

Run: `python -m pytest .claude/skills/math-explainer/tests/ -v`
Expected: ALL PASS (Sage integration test SKIPPED if `sage` absent).

Run: `python .claude/skills/math-explainer/scripts/check_env.py`
Expected: prints `sage`/`manim` availability; exit 0 if Sage present.

Run: `python .claude/skills/math-explainer/evals/run_eval.py`
Expected: `EVAL: PASS`.

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/math-explainer/scripts/check_env.py .claude/skills/math-explainer/tests/test_check_env.py
git commit -m "feat(math-explainer): env doctor + full integration pass"
```

---

## Self-review (completed by plan author)

**Spec coverage:** seven required capabilities → Stage 1 (deps, Task 4), Stage 2 stuck-points (pipeline.md, Task 7), Stage 3 multimodal incl. Sage+manim (Tasks 5–6), Stage 4 accuracy (Task 7 + Tasks 5/6 manifest), Stage 5 comprehension (pipeline.md, Task 7), Stage 6 gate (Task 3), Method Engine (Task 2). Reuse of graph/MATH_FOUNDATIONS/ledger/bible → Stage 1 + accuracy protocol. No Diffusion-Gemma; Sage+manim v1 → Tasks 5–6. Evals → Task 9.

**Placeholder scan:** none — every code/markdown file is given in full; every command has expected output.

**Type/name consistency:** `bundle.json` keys are identical across Task 3 (scorecard), Task 9 (sample bundle), and the schema block. `parse_strata`/`resolve`, `parse_manifest`/`run_recipe`, `validate_scene_values`, `evaluate`, `probe` are each defined once and imported by the same name in tests/evals. Script paths and the `scripts.` import package are consistent throughout.

**Note on interpreters (Windows / dual-interpreter):** the helper scripts are pure Python (no graphify import) and run under the project venv used for pytest; `sage` recipes run via the `sage` executable; the optional manim render runs via the manim MCP. `graphify explain` (Stage 1 enrichment) runs via system Python per the project rule.
