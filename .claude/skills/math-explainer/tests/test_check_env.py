from scripts.check_env import probe

def test_probe_reports_known_tools():
    report = probe()
    assert set(report.keys()) == {"sage", "manim"}
    assert all(isinstance(v, bool) for v in report.values())
