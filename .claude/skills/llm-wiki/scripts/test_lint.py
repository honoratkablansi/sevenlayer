import os, tempfile, importlib.util, pathlib

spec = importlib.util.spec_from_file_location(
    "lint", os.path.join(os.path.dirname(__file__), "lint.py"))
lint = importlib.util.module_from_spec(spec); spec.loader.exec_module(lint)

def build(tmp):
    w = pathlib.Path(tmp); (w/"wiki/concepts").mkdir(parents=True)
    (w/"wiki/maps").mkdir(parents=True)
    # good concept: has frontmatter, a cited claim, links to hub
    (w/"wiki/concepts/good.md").write_text(
        "---\ntype: concept\n---\n# Good\n- X holds.^[from [[Hub]] — \"x\"]\n[[Hub]]\n", encoding="utf-8")
    # orphan: frontmatter ok, nothing links to it, links nowhere
    (w/"wiki/concepts/orphan.md").write_text(
        "---\ntype: concept\n---\n# Orphan\n", encoding="utf-8")
    # missing frontmatter
    (w/"wiki/concepts/nofm.md").write_text("# NoFM\n[[Good]]\n", encoding="utf-8")
    # unsourced claim bullet on a concept page
    (w/"wiki/concepts/unsourced.md").write_text(
        "---\ntype: concept\n---\n# U\n- A bare claim with no citation.\n[[Good]]\n", encoding="utf-8")
    # hub links to good + a broken target
    (w/"wiki/maps/Hub.md").write_text(
        "---\ntype: map\n---\n# Hub\n[[Good]] [[Nonexistent]]\n", encoding="utf-8")

with tempfile.TemporaryDirectory() as tmp:
    build(tmp)
    r = lint.lint(tmp)
    names = lambda k: {pathlib.Path(p).name for p,_ in r[k]}
    assert "Nonexistent" in {t for _,t in r["broken_links"]}, r["broken_links"]
    assert "orphan.md" in names("orphans"), r["orphans"]
    assert "nofm.md" in names("missing_frontmatter"), r["missing_frontmatter"]
    assert "unsourced.md" in names("unsourced_claims"), r["unsourced_claims"]
    # good.md must NOT be flagged anywhere
    for k in ("orphans","missing_frontmatter","unsourced_claims"):
        assert "good.md" not in names(k), (k, r[k])
    print("ALL LINT TESTS PASSED")
