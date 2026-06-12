import hashlib
import importlib.util
import json
import os
import tempfile

_spec = importlib.util.spec_from_file_location(
    "paper_vector", os.path.join(os.path.dirname(__file__), "paper_vector.py"))
paper_vector = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(paper_vector)


def _paper(pdf_name="paper.pdf", sha=None, size=None):
    return {
        "rank": 1,
        "citations": 123,
        "title": "Test Paper: A PDF Fixture",
        "year": 2026,
        "doi": "10.1234/example",
        "semantic_scholar_url": "https://www.semanticscholar.org/paper/example",
        "pdf_source_url": "https://example.com/paper.pdf",
        "file": pdf_name,
        "sha256": sha or "0" * 64,
        "bytes": size or 10,
        "pages": 2,
    }


def test_load_manifest_accepts_object_and_array():
    with tempfile.TemporaryDirectory() as tmp:
        object_path = os.path.join(tmp, "object.json")
        array_path = os.path.join(tmp, "array.json")
        paper = _paper()
        with open(object_path, "w", encoding="utf-8") as fh:
            json.dump({"papers": [paper]}, fh)
        with open(array_path, "w", encoding="utf-8") as fh:
            json.dump([paper], fh)
        assert paper_vector.load_manifest(object_path)[1][0]["title"] == paper["title"]
        assert paper_vector.load_manifest(array_path)[1][0]["title"] == paper["title"]


def test_validate_manifest_requires_fields():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "manifest.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"papers": [{"rank": 1}]}, fh)
        try:
            paper_vector.validate_manifest(path)
        except ValueError as exc:
            assert "missing" in str(exc)
            assert "title" in str(exc)
        else:
            raise AssertionError("validate_manifest should reject incomplete entries")


def test_validate_manifest_enforces_expected_count():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "manifest.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"papers": [_paper()]}, fh)
        try:
            paper_vector.validate_manifest(path, expected_count=10)
        except ValueError as exc:
            assert "expected 10 papers, found 1" in str(exc)
        else:
            raise AssertionError("validate_manifest should enforce expected_count")


def test_validate_manifest_rejects_unsafe_file_paths():
    with tempfile.TemporaryDirectory() as tmp:
        for bad in ("..\\paper.pdf", "../paper.pdf", "C:\\secret\\paper.pdf", "/tmp/paper.pdf"):
            path = os.path.join(tmp, "manifest.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump({"papers": [_paper(bad)]}, fh)
            try:
                paper_vector.validate_manifest(path)
            except ValueError as exc:
                assert "unsafe file path" in str(exc)
            else:
                raise AssertionError(f"validate_manifest should reject {bad}")


def test_validate_manifest_rejects_duplicate_slugs():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "manifest.json")
        paper1 = _paper("a.pdf")
        paper2 = _paper("b.pdf")
        paper2["doi"] = "10.1234/other"
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"papers": [paper1, paper2]}, fh)
        try:
            paper_vector.validate_manifest(path)
        except ValueError as exc:
            assert "duplicates rank" in str(exc)
            assert "duplicates slug" in str(exc)
        else:
            raise AssertionError("validate_manifest should reject duplicate rank/slug")


def test_paper_slug_is_stable_and_ranked():
    paper = _paper()
    assert paper_vector.paper_slug(paper) == "01-test-paper-a-pdf-fixture"


def test_verify_pdf_checks_header_size_and_hash():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "paper.pdf")
        data = b"%PDF-fake\nbody"
        with open(path, "wb") as fh:
            fh.write(data)
        sha = hashlib.sha256(data).hexdigest()
        assert paper_vector.verify_pdf(path, sha, len(data)) == sha


def test_build_frontmatter_escapes_backslashes():
    fm = paper_vector.build_frontmatter({
        "source_type": "paper",
        "title": r"C:\Users\name",
    })
    assert r'title: "C:\\Users\\name"' in fm


def test_extract_manifest_idempotent_with_stubbed_extractor():
    with tempfile.TemporaryDirectory() as tmp:
        pdf_name = "paper.pdf"
        pdf_path = os.path.join(tmp, pdf_name)
        data = b"%PDF-fake\nbody"
        with open(pdf_path, "wb") as fh:
            fh.write(data)
        sha = hashlib.sha256(data).hexdigest()
        manifest_path = os.path.join(tmp, "manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as fh:
            json.dump({"papers": [_paper(pdf_name, sha, len(data))]}, fh)
        out_dir = os.path.join(tmp, "raw", "papers")

        paper = _paper(pdf_name, sha, len(data))
        old_extract = paper_vector.extract_pdf_to_markdown
        old_validate = paper_vector.validate_manifest
        try:
            paper_vector.validate_manifest = lambda path, validate_assets=False: [paper]
            paper_vector.extract_pdf_to_markdown = lambda pdf_path, meta: ("## Page 1\n\nText\n\n## Page 2\n\nMore\n", 2)
            first = paper_vector.extract_manifest(manifest_path, out_dir)
            second = paper_vector.extract_manifest(manifest_path, out_dir)
        finally:
            paper_vector.extract_pdf_to_markdown = old_extract
            paper_vector.validate_manifest = old_validate

        assert first["written"] == 1
        assert first["skipped"] == 0
        assert second["written"] == 0
        assert second["skipped"] == 1
        md_path = os.path.join(out_dir, "01-test-paper-a-pdf-fixture.md")
        pdf_asset = os.path.join(tmp, "raw", "assets", "papers", "01-test-paper-a-pdf-fixture.pdf")
        assert os.path.exists(md_path)
        assert os.path.exists(pdf_asset)
        with open(md_path, "r", encoding="utf-8") as fh:
            text = fh.read()
        assert "source_type: paper" in text
        assert "pdf_asset: assets/papers/01-test-paper-a-pdf-fixture.pdf" in text
        assert "## Page 2" in text


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn(); print("ok", fn.__name__)
    print(f"ALL {len(fns)} PAPER VECTOR TESTS PASSED")
