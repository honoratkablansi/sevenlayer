#!/usr/bin/env python3
"""Dependency doctor for math-explainer: reports which external tools are available."""
import shutil
import sys


def probe() -> dict:
    return {"sage": shutil.which("sage") is not None,
            "manim": shutil.which("manim") is not None,
            "graphify": shutil.which("graphify") is not None}


def mode() -> str:
    """Report the pipeline's multimodal capability from the probe.

    - ``full-multimodal``: Sage figures + manim animation both available.
    - ``figure-only``: Sage present, manim absent (the documented fallback).
    - ``unavailable``: Sage missing, so the skill cannot produce figures.
    """
    p = probe()
    if not p["sage"]:
        return "unavailable"
    return "full-multimodal" if p["manim"] else "figure-only"


def main() -> int:
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
    return 0 if report["sage"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
