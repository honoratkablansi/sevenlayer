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
    """Return mismatch messages for keys present in both dicts.

    Keys absent from the manifest are intentionally ignored: a scene legitimately
    displays non-computed chrome (titles, axis labels) that the Sage manifest does
    not contain. Booleans are compared by exact type so a bool can never silently
    match a numeric value (Python treats ``True == 1`` / ``False == 0``).
    """
    errors: list[str] = []
    for key, sv in scene_values.items():
        if key not in manifest:
            continue
        mv = manifest[key]
        if isinstance(sv, bool) or isinstance(mv, bool):
            if type(sv) is not type(mv) or sv != mv:
                errors.append(f"{key}: scene={sv!r} != manifest={mv!r}")
        elif isinstance(sv, (int, float)) and isinstance(mv, (int, float)):
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
