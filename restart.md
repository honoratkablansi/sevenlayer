# RESTART — resume after reboot (math-explainer skill build + WSL2 toolchain)

**Written:** 2026-06-14, just before the WSL2-activation reboot.
**One-line status:** WSL2 is installed but needed a reboot to activate; everything else (book outline, chapter bible, math-foundations, the `math-explainer` skill *spec + plan*) is committed. The skill **code is not built yet** — it's waiting on the WSL2 + SageMath toolchain.

**To resume, paste this to a fresh session:**
> "Continue the math-explainer build per `restart.md`: finish the WSL2 toolchain (latest Ubuntu + SageMath + Docker + NVIDIA), then execute `docs/superpowers/plans/2026-06-14-math-explainer-skill.md` with Opus 4.8 subagents and run the real tests."

---

## 1. Project context (what this is)

- Repo: `C:\sevenlayer` (branch **main**). It's the "Proving Nothing" zero-knowledge-proof book by Charles Hoskinson, plus a master knowledge graph.
- We designed a 2nd-edition book outline (5 parts / 22 chapters), a per-chapter **chapter bible**, and a **math-foundations** plan (adopted the 3Blue1Brown + Tao explainer style). All committed.
- We then designed a bespoke Claude Code skill, **`math-explainer`**: a six-stage pipeline (deps → stuck-points → Tao-staged multimodal explanation → Sage-correct-by-construction accuracy → comprehension checks → assembly with a method-adherence scorecard) that drafts book math in the Sanderson+Tao style. **Spec and implementation plan are committed; the code is not built yet.**

## 2. Host environment (verified 2026-06-14)

- Windows 11 (10.0.26200), **not** elevated by default in the agent shell.
- Python **3.14.5** system-side (too new for many sci wheels — keep Sage/manim in WSL, not native).
- Package managers present: `choco`, `winget`, `pip`. No `conda`.
- GPU: **NVIDIA GeForce RTX 5090** (32 GB) — host driver **596.49**, **CUDA 13.2**, `nvidia-smi` works on host → WSL GPU-ready. Also an Intel iGPU.
- **WSL 2.7.8** installed (kernel 6.18.33.1, default version 2). VirtualMachinePlatform enabled; **required a reboot** to activate. `HypervisorPresent=True` (virtualization is on; the `VirtualizationFirmwareEnabled=False` reading is the normal Hyper-V masking artifact).
- No WSL distro installed yet. Docker **not** installed.

## 3. What is DONE (committed on main, latest first)

| Commit | What |
|---|---|
| `ecdd9d5d` | math-explainer implementation **plan** (`docs/superpowers/plans/2026-06-14-math-explainer-skill.md`) |
| `5fb964b9` | math-explainer design **spec** (`docs/superpowers/specs/2026-06-14-math-explainer-skill-design.md`) |
| `e6e8deea` | fold-in of the commitment/Sigma on-ramp + `master-graph/.outline/MATH_FOUNDATIONS.md` |
| `d243be67` | `master-graph/.outline/CHAPTER_BIBLE.md` (+ `bible/` part files, omissions appendix) |
| `a89d832a` | 2nd-edition outline design (`master-graph/.outline/SYNTHESIS.md`, `docs/.../2026-06-14-book-outline-design.md`) |

Working tree was **clean** at restart (only this `restart.md` is new).

## 4. What is LEFT (the resume checklist)

### Step A — confirm the reboot activated WSL2
```powershell
wsl --status        # must NOT say "virtualization is not enabled"
wsl --version
```
If it still complains about virtualization: enable **Intel VT-x / Virtualization** in UEFI/BIOS, reboot again. (Unlikely — `HypervisorPresent` was True.)

### Step B — install the latest Ubuntu (26.04), non-interactively
```powershell
wsl --install -d Ubuntu-26.04 --no-launch
# initialize as root (skips the interactive username/password OOBE):
wsl -d Ubuntu-26.04 -u root -- bash -lc "apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y upgrade"
```
(Available distros listed at restart: Ubuntu, **Ubuntu-26.04**, Ubuntu-24.04, Ubuntu-22.04, …)

### Step C — verify GPU passthrough inside WSL (driver comes from the host; do NOT install a GPU driver in WSL)
```powershell
wsl -d Ubuntu-26.04 -- nvidia-smi      # should show the RTX 5090
```
Optional CUDA toolkit inside WSL (for compute; not needed for Sage/manim):
```powershell
wsl -d Ubuntu-26.04 -u root -- bash -lc "apt-get install -y nvidia-cuda-toolkit"
```

### Step D — install the SageMath + test toolchain in WSL
```powershell
wsl -d Ubuntu-26.04 -u root -- bash -lc "DEBIAN_FRONTEND=noninteractive apt-get install -y sagemath python3 python3-pip python3-pytest ffmpeg git"
# verify:
wsl -d Ubuntu-26.04 -- bash -lc "sage --version && python3 -m pytest --version"
```
manim (optional, for the animation path — may pull many deps):
```powershell
wsl -d Ubuntu-26.04 -u root -- bash -lc "pip install --break-system-packages manim || echo 'manim optional; Sage figures still work'"
```

### Step E — install Docker Engine + NVIDIA Container Toolkit in WSL
Enable systemd first (so the docker service runs):
```powershell
wsl -d Ubuntu-26.04 -u root -- bash -lc "printf '[boot]\nsystemd=true\n' > /etc/wsl.conf"
wsl --shutdown
```
Docker Engine (official repo; if the 26.04 codename isn't published yet, fall back to `apt-get install -y docker.io docker-compose-v2`):
```powershell
wsl -d Ubuntu-26.04 -u root -- bash -lc "apt-get update && apt-get install -y ca-certificates curl gnupg && install -m0755 -d /etc/apt/keyrings && curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc && chmod a+r /etc/apt/keyrings/docker.asc && . /etc/os-release && echo \"deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \$VERSION_CODENAME stable\" > /etc/apt/sources.list.d/docker.list && apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin || apt-get install -y docker.io docker-compose-v2"
```
NVIDIA Container Toolkit (lets containers use the 5090):
```powershell
wsl -d Ubuntu-26.04 -u root -- bash -lc "curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' > /etc/apt/sources.list.d/nvidia-container-toolkit.list && apt-get update && apt-get install -y nvidia-container-toolkit && nvidia-ctk runtime configure --runtime=docker"
wsl -d Ubuntu-26.04 -u root -- bash -lc "service docker start; sleep 3; docker run --rm --gpus all nvidia/cuda:12.4.0-base-ubuntu22.04 nvidia-smi"  # should print the 5090 from inside a container
```

### Step F — build the skill (the 10-task plan) with Opus 4.8 subagents
Use **superpowers:subagent-driven-development**, dispatching the implementer/reviewer agents with **model: "opus"** (user requirement). Plan: `docs/superpowers/plans/2026-06-14-math-explainer-skill.md`. It creates `.claude/skills/math-explainer/` (SKILL.md, references/, scripts/, evals/, tests/). Tasks are sequential (shared files: `test_structure.py`, `SKILL.md`) — do **not** parallelize implementers.

### Step G — run the REAL tests (Sage now live)
The skill files are on the Windows fs; run the suite **inside WSL** so `sage` is on PATH and `run_sage.py`'s `shutil.which("sage")` finds it (on Windows it would SKIP the Sage test):
```powershell
wsl -d Ubuntu-26.04 -- bash -lc "cd /mnt/c/sevenlayer/.claude/skills/math-explainer && python3 -m pytest tests/ -v"
wsl -d Ubuntu-26.04 -- bash -lc "cd /mnt/c/sevenlayer/.claude/skills/math-explainer && python3 evals/run_eval.py"
```
Expect: all tests PASS and the Schwartz–Zippel Sage integration test runs for real (≤ 2 agreement points, SVG written to `assets/figures/`).

### Step H — finish
Run **superpowers:finishing-a-development-branch** (we're on `main`; commit the skill, do not push unless asked).

## 5. Constraints / preferences (do not violate)

- **No `Co-Authored-By` trailer** in commit messages.
- **SageMath/manim live in WSL2**, not native-Windows pip/conda (user directive).
- **Subagents on Opus 4.8** for the build.
- **Latest Ubuntu = Ubuntu-26.04.**
- **Never install a GPU driver inside WSL** — the host driver (596.49) is used automatically; inside WSL only CUDA toolkit / NVIDIA Container Toolkit.
- **Local commits only**; `main` is many commits ahead of origin — do **not** push unless explicitly asked.

## 6. Key files

- Skill spec: `docs/superpowers/specs/2026-06-14-math-explainer-skill-design.md`
- Skill plan: `docs/superpowers/plans/2026-06-14-math-explainer-skill.md`
- Skill target dir (to be created): `.claude/skills/math-explainer/`
- Book outline: `master-graph/.outline/SYNTHESIS.md`, `docs/superpowers/specs/2026-06-14-book-outline-design.md`
- Chapter bible: `master-graph/.outline/CHAPTER_BIBLE.md`
- Math foundations + concept ladder: `master-graph/.outline/MATH_FOUNDATIONS.md`
- Cross-session memory: `~/.claude/projects/C--Users-charl/memory/wsl2-sagemath-toolchain.md`
- WSL install log: `~/wsl_install.log`
