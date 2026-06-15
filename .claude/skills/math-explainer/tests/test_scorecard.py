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

def test_no_predicted_stuck_points_fails():
    # An empty predicted set is vacuously "all addressed"; the gate must require Stage 2 ran.
    b = complete_bundle()
    b["stuck_points_predicted"] = []
    b["stuck_points_addressed"] = []
    checks = {c["id"]: c["ok"] for c in evaluate(b)}
    assert checks["stuck_points_addressed"] is False

def test_malformed_heuristic_pair_fails():
    b = complete_bundle()
    b["heuristic_rigorous_pairs"] = [["only-one-element"]]
    checks = {c["id"]: c["ok"] for c in evaluate(b)}
    assert checks["heuristic_rigorous_pairing"] is False

def test_empty_string_heuristic_pair_fails():
    b = complete_bundle()
    b["heuristic_rigorous_pairs"] = [["picture", "  "]]
    checks = {c["id"]: c["ok"] for c in evaluate(b)}
    assert checks["heuristic_rigorous_pairing"] is False
