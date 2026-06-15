#!/usr/bin/env python3
"""Stage 3: validate a manim scene's displayed values against the Sage values manifest.

The render is normally performed by the manim MCP (a model-driven step described in
references/pipeline.md). This module owns the *validation* so an animation can never
drift from the math: every value the scene shows must match the Sage manifest. It also
exposes ``render_scene`` to drive a local manim install directly (the "full-multimodal"
mode), so the animation path can be exercised end-to-end without the MCP.
"""
import json
import shutil
import subprocess
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
