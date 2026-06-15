from scripts.check_env import probe, mode, missing

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

def test_missing_reports_known_absent(monkeypatch):
    import scripts.check_env as ce
    monkeypatch.setattr(ce, "probe", lambda: {"sage": True, "manim": False, "graphify": False})
    assert set(ce.missing(["sage", "manim", "graphify"])) == {"manim", "graphify"}

def test_missing_empty_required_is_satisfied():
    from scripts.check_env import missing
    assert missing([]) == []

def test_main_require_fails_when_missing(monkeypatch):
    import scripts.check_env as ce
    monkeypatch.setattr(ce, "probe", lambda: {"sage": True, "manim": False, "graphify": False})
    assert ce.main(["check_env.py", "--require", "sage,manim,graphify"]) == 1

def test_main_require_passes_when_all_present(monkeypatch):
    import scripts.check_env as ce
    monkeypatch.setattr(ce, "probe", lambda: {"sage": True, "manim": True, "graphify": True})
    assert ce.main(["check_env.py", "--require", "sage,manim,graphify"]) == 0
