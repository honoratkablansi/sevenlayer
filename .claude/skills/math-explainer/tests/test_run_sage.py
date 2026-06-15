import shutil
import pytest
from pathlib import Path
from scripts.run_sage import parse_manifest, run_recipe, validate_figure

def test_parse_manifest_takes_last_json_line():
    out = "Sage startup noise\nignored line\n{\"figure\": \"a.svg\", \"num_agreements\": 2}\n"
    m = parse_manifest(out)
    assert m["figure"] == "a.svg"
    assert m["num_agreements"] == 2

def test_parse_manifest_raises_without_json():
    with pytest.raises(ValueError):
        parse_manifest("no json here\njust text")

def test_validate_figure_rejects_absolute_nonfigure_path():
    with pytest.raises(RuntimeError):
        validate_figure("/etc/passwd")

def test_validate_figure_rejects_wrong_suffix():
    with pytest.raises(RuntimeError):
        validate_figure("assets/figures/x.txt")

def test_validate_figure_rejects_outside_assets_figures(tmp_path):
    f = tmp_path / "x.svg"
    f.write_text("<svg/>", encoding="utf-8")
    with pytest.raises(RuntimeError):
        validate_figure(str(f))

def test_validate_figure_rejects_empty_file(tmp_path):
    d = tmp_path / "assets" / "figures"
    d.mkdir(parents=True)
    f = d / "x.svg"
    f.write_text("", encoding="utf-8")
    with pytest.raises(RuntimeError):
        validate_figure(str(f))

def test_validate_figure_accepts_valid_svg(tmp_path):
    d = tmp_path / "assets" / "figures"
    d.mkdir(parents=True)
    f = d / "x.svg"
    f.write_text("<svg/>", encoding="utf-8")
    assert validate_figure(str(f)) == f

@pytest.mark.skipif(shutil.which("sage") is None, reason="SageMath not installed")
def test_run_recipe_schwartz_zippel(tmp_path, monkeypatch):
    monkeypatch.chdir(Path(__file__).resolve().parents[1])  # skill root, so assets/ path resolves
    recipe = Path("scripts/recipes/schwartz_zippel.sage")
    manifest = run_recipe(recipe)
    assert manifest["field"] == 101
    assert manifest["num_agreements"] == len(manifest["agreement_points"])
    assert manifest["num_agreements"] <= 2  # Schwartz–Zippel: two degree-2 polys agree in <= 2 points
    assert Path(manifest["figure"]).exists()
