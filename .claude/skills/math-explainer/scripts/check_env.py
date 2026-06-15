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
