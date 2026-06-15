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


FIGURE_SUFFIXES = {".svg", ".pdf"}


def validate_figure(fig: str) -> Path:
    """Validate a manifest's figure path and return it as a Path.

    Correct-by-construction figures are generated SVG/PDF assets, so a manifest may
    only point at a non-empty .svg/.pdf living under an ``assets/figures/`` directory.
    This rejects a recipe that tries to pass off an unrelated existing file (e.g.
    ``/etc/passwd``) as its figure.
    """
    if not fig:
        raise RuntimeError("manifest has no 'figure'")
    p = Path(fig)
    if p.suffix.lower() not in FIGURE_SUFFIXES:
        raise RuntimeError(f"figure must be .svg or .pdf: {fig}")
    if not (p.parent.name == "figures" and p.parent.parent.name == "assets"):
        raise RuntimeError(f"figure must live under assets/figures/: {fig}")
    if not p.exists() or p.stat().st_size == 0:
        raise RuntimeError(f"figure missing or empty: {fig}")
    return p


def run_recipe(recipe: Path, timeout: int = 300) -> dict:
    if shutil.which("sage") is None:
        raise RuntimeError("SageMath ('sage') not found on PATH")
    proc = subprocess.run(["sage", str(recipe)], capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(f"sage failed: {proc.stderr.strip()}")
    manifest = parse_manifest(proc.stdout)
    validate_figure(manifest.get("figure"))
    return manifest


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: run_sage.py <recipe.sage>", file=sys.stderr)
        return 2
    print(json.dumps(run_recipe(Path(argv[1])), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
