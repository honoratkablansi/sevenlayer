import shutil
import pytest
from scripts.manim_render import validate_scene_values, render_scene

MINIMAL_SCENE = """
from manim import Scene, Circle, Square, VGroup

class Minimal(Scene):
    def construct(self):
        self.add(VGroup(Circle(), Square()))
"""

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

def test_bool_int_drift_flagged():
    # Python's True == 1, so a bool must not silently match a numeric value either way.
    assert validate_scene_values({"flag": True}, {"flag": 1})
    assert validate_scene_values({"flag": 1}, {"flag": True})

def test_matching_bool_ok():
    assert validate_scene_values({"flag": True}, {"flag": True}) == []

@pytest.mark.skipif(shutil.which("manim") is None, reason="manim not installed")
def test_manim_render_and_value_validation_end_to_end(tmp_path):
    # 1. The manim toolchain actually renders a scene headless (full-multimodal mode).
    scene = tmp_path / "minimal_scene.py"
    scene.write_text(MINIMAL_SCENE, encoding="utf-8")
    out = render_scene(scene, "Minimal", media_dir=tmp_path / "media")
    assert out.exists() and out.stat().st_size > 0
    # 2. The animation's displayed values are validated against a Sage manifest (no drift).
    manifest = {"num_agreements": 1, "field": 101}
    assert validate_scene_values({"num_agreements": 1, "field": 101}, manifest) == []
    assert validate_scene_values({"num_agreements": 2}, manifest)  # drift is caught
