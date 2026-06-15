from scripts.schemas import (
    validate_concept_brief,
    validate_stuck_points,
    validate_explanation,
    validate_accuracy_report,
    validate_comprehension_set,
    validate_bundle,
)


def good_concept_brief():
    return {
        "concept": "Schwartz–Zippel lemma",
        "stratum": "Algebra I",
        "prerequisites": ["polynomials", "union bound"],
        "assumed_background": ["modular arithmetic"],
        "target_depth": "rigorous",
        "learning_objectives": ["state the bound", "apply it to identity testing"],
    }


def good_accuracy_report():
    return {
        "claims": ["two degree-2 polys over GF(101) agree at exactly 1 point"],
        "sage_manifest": {"figure": "assets/figures/schwartz_zippel.svg", "num_agreements": 1},
        "ledger_refs": ["claim:sz-bound"],
        "adversarial_findings": [],
        "verified": True,
    }


def good_comprehension_set():
    levels = ["recall", "apply", "transfer", "rediscover"]
    return [
        {"level": lv, "question": f"q-{lv}", "answer_key": f"a-{lv}",
         "targets_stuck_point": "big-field misconception", "on_miss_route_to": "finite fields"}
        for lv in levels
    ]


def test_concept_brief_valid():
    assert validate_concept_brief(good_concept_brief()) == []


def test_concept_brief_requires_learning_objectives():
    b = good_concept_brief()
    b["learning_objectives"] = []
    errs = validate_concept_brief(b)
    assert any("learning_objectives" in m for m in errs)


def test_concept_brief_bad_target_depth():
    b = good_concept_brief()
    b["target_depth"] = "sorta-rigorous"
    assert any("target_depth" in m for m in validate_concept_brief(b))


def test_stuck_points_valid_and_invalid():
    good = {"misconceptions": [{"claim": "c", "why_tempting": "w", "severity": "high"}],
            "dumb_questions": ["why?"], "bad_intuitions_to_kill": ["x"]}
    assert validate_stuck_points(good) == []
    bad = {"misconceptions": [], "dumb_questions": [], "bad_intuitions_to_kill": []}
    assert any("misconceptions" in m for m in validate_stuck_points(bad))


def test_explanation_requires_visual_figure_ref():
    good = {
        "phases": {"pre_rigorous": "p", "rigorous": "r", "post_rigorous": "s"},
        "modes": {"analogy": "a", "visual": {"figure_ref": "assets/figures/x.svg", "sage_code": "..."},
                  "worked_example": "w", "formal": "f", "synthesis": "s"},
    }
    assert validate_explanation(good) == []
    bad = {"phases": good["phases"], "modes": dict(good["modes"], visual={"sage_code": "..."})}
    assert any("figure_ref" in m for m in validate_explanation(bad))


def test_accuracy_report_valid_and_invalid():
    assert validate_accuracy_report(good_accuracy_report()) == []
    bad = good_accuracy_report()
    bad["verified"] = "true"  # string, not bool
    assert any("verified" in m for m in validate_accuracy_report(bad))
    nomani = good_accuracy_report()
    del nomani["sage_manifest"]
    assert any("sage_manifest" in m for m in validate_accuracy_report(nomani))


def test_comprehension_set_requires_all_levels_and_fields():
    assert validate_comprehension_set(good_comprehension_set()) == []
    missing_level = good_comprehension_set()[:3]  # drop rediscover
    assert any("missing" in m for m in validate_comprehension_set(missing_level))
    no_answer = good_comprehension_set()
    no_answer[0]["answer_key"] = ""
    assert any("answer_key" in m for m in validate_comprehension_set(no_answer))


def test_bundle_aggregates_subschemas():
    bundle = {
        "concept": "Schwartz–Zippel lemma",
        "phases": {"pre_rigorous": "a", "rigorous": "b", "post_rigorous": "c"},
        "modes_order": ["analogy", "visual", "worked_example", "formal", "synthesis"],
        "led_with_visual": True,
        "motivated_before_defined": True,
        "notation_in_pre_rigorous": False,
        "heuristic_rigorous_pairs": [["picture", "P ≤ d/|F|"]],
        "stuck_points_predicted": ["big-field misconception"],
        "stuck_points_addressed": ["big-field misconception"],
        "accuracy_report": good_accuracy_report(),
        "comprehension_set": good_comprehension_set(),
    }
    assert validate_bundle(bundle) == []
    bundle["accuracy_report"]["verified"] = False  # still well-formed, just not verified
    assert validate_bundle(bundle) == []  # schema validity is independent of the verified flag
    del bundle["accuracy_report"]
    assert any("sage_manifest" in m for m in validate_bundle(bundle))
