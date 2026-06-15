from scripts.check_env import probe, mode

def test_probe_reports_known_tools():
    report = probe()
    assert set(report.keys()) == {"sage", "manim", "graphify"}
    assert all(isinstance(v, bool) for v in report.values())

def test_mode_consistent_with_probe():
    p = probe()
    m = mode()
    if not p["sage"]:
        assert m == "unavailable"
    elif p["manim"]:
        assert m == "full-multimodal"
    else:
        assert m == "figure-only"
