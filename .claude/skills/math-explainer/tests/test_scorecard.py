from scripts.scorecard import evaluate

def complete_bundle():
    levels = ["recall", "apply", "transfer", "rediscover"]
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
        "accuracy_report": {
            "claims": ["two degree-2 polys over GF(101) agree at exactly 1 point"],
            "sage_manifest": {"figure": "assets/figures/schwartz_zippel.svg", "num_agreements": 1},
            "ledger_refs": ["claim:sz-bound"],
            "adversarial_findings": [],
            "verified": True,
        },
        "comprehension_set": [
            {"level": lv, "question": f"q-{lv}", "answer_key": f"a-{lv}",
             "targets_stuck_point": "big-field misconception", "on_miss_route_to": "finite fields"}
            for lv in levels
        ],
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

def test_self_asserted_accuracy_without_report_fails():
    # The old gameable form: a bare boolean instead of a real accuracy_report.
    b = complete_bundle()
    del b["accuracy_report"]
    b["accuracy_verified"] = True
    checks = {c["id"]: c["ok"] for c in evaluate(b)}
    assert checks["accuracy_verified"] is False

def test_unverified_accuracy_report_fails():
    b = complete_bundle()
    b["accuracy_report"]["verified"] = False
    checks = {c["id"]: c["ok"] for c in evaluate(b)}
    assert checks["accuracy_verified"] is False

def test_accuracy_report_without_manifest_fails():
    b = complete_bundle()
    del b["accuracy_report"]["sage_manifest"]
    checks = {c["id"]: c["ok"] for c in evaluate(b)}
    assert checks["accuracy_verified"] is False

def test_missing_comprehension_level_fails():
    b = complete_bundle()
    b["comprehension_set"] = [it for it in b["comprehension_set"] if it["level"] != "rediscover"]
    checks = {c["id"]: c["ok"] for c in evaluate(b)}
    assert checks["comprehension_three_levels"] is False
    assert checks["rediscovery_prompt"] is False

def test_comprehension_item_missing_answer_key_fails():
    b = complete_bundle()
    b["comprehension_set"][0]["answer_key"] = ""
    checks = {c["id"]: c["ok"] for c in evaluate(b)}
    assert checks["comprehension_three_levels"] is False
