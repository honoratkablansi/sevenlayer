import shutil
import pytest
from pathlib import Path
from scripts.run_sage import parse_manifest, run_recipe

def test_parse_manifest_takes_last_json_line():
    out = "Sage startup noise\nignored line\n{\"figure\": \"a.svg\", \"num_agreements\": 2}\n"
    m = parse_manifest(out)
    assert m["figure"] == "a.svg"
    assert m["num_agreements"] == 2

def test_parse_manifest_raises_without_json():
    with pytest.raises(ValueError):
        parse_manifest("no json here\njust text")

@pytest.mark.skipif(shutil.which("sage") is None, reason="SageMath not installed")
def test_run_recipe_schwartz_zippel(tmp_path, monkeypatch):
    monkeypatch.chdir(Path(__file__).resolve().parents[1])  # skill root, so assets/ path resolves
    recipe = Path("scripts/recipes/schwartz_zippel.sage")
    manifest = run_recipe(recipe)
    assert manifest["field"] == 101
    assert manifest["num_agreements"] == len(manifest["agreement_points"])
    assert manifest["num_agreements"] <= 2  # Schwartz–Zippel: two degree-2 polys agree in <= 2 points
    assert Path(manifest["figure"]).exists()
