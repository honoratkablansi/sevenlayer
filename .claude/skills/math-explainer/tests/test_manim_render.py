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
