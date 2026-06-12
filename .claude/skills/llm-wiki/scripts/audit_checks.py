#!/usr/bin/env python3
"""Mechanical audit checks for llm-wiki skill development."""
import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def _run(name, cmd, cwd=None):
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    return {
        "name": name,
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "status": "passed" if proc.returncode == 0 else "failed",
    }


def _dependency_check():
    mods = ["scrapling", "trafilatura", "pypdf"]
    found = {m: importlib.util.find_spec(m) is not None for m in mods}
    return {
        "name": "dependency check",
        "cmd": ["python", "-c", "import importlib.util"],
        "returncode": 0 if all(found.values()) else 1,
        "stdout": json.dumps(found, sort_keys=True),
        "stderr": "",
        "status": "passed" if all(found.values()) else "failed",
    }


def run_checks(wiki_root):
    wiki = Path(wiki_root)
    py = sys.executable
    checks = [
        _dependency_check(),
        _run("scrape unit tests", [py, str(SCRIPT_DIR / "test_scrape.py")]),
        _run("lint unit tests", [py, str(SCRIPT_DIR / "test_lint.py")]),
        _run("paper vector unit tests", [py, str(SCRIPT_DIR / "test_paper_vector.py")]),
        _run("wiki lint", [py, str(SCRIPT_DIR / "lint.py"), str(wiki)]),
        _run("scrape crawl plan-only", [
            py, str(SCRIPT_DIR / "scrape.py"), "crawl", "https://example.com",
            "--out-dir", str(wiki / "raw"), "--max-pages", "2", "--max-depth", "1", "--plan-only",
        ]),
    ]
    manifest = wiki / "raw" / "test-vectors" / "zero-knowledge-papers" / "manifest.json"
    if manifest.exists():
        checks.append(_run("paper manifest validation", [
            py, str(SCRIPT_DIR / "paper_vector.py"), "validate-manifest", str(manifest),
            "--expected-count", "10",
        ]))
        checks.append(_paper_vector_temp_idempotency(py, manifest))
    return checks


def _paper_vector_temp_idempotency(py, manifest):
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        src_dir = manifest.parent
        data = json.loads(manifest.read_text(encoding="utf-8-sig"))
        papers = data["papers"] if isinstance(data, dict) else data
        tmp_manifest = tmp_path / "manifest.json"
        tmp_manifest.write_text(json.dumps(data), encoding="utf-8")
        for paper in papers:
            shutil.copyfile(src_dir / paper["file"], tmp_path / paper["file"])
        out_dir = tmp_path / "raw" / "papers"
        first = _run("paper vector temp first extract", [
            py, str(SCRIPT_DIR / "paper_vector.py"), "extract-manifest", str(tmp_manifest),
            "--out-dir", str(out_dir),
        ])
        second = _run("paper vector temp second extract", [
            py, str(SCRIPT_DIR / "paper_vector.py"), "extract-manifest", str(tmp_manifest),
            "--out-dir", str(out_dir),
        ])
        status = "failed"
        stdout = json.dumps({"first": first, "second": second})
        if first["returncode"] == 0 and second["returncode"] == 0:
            try:
                first_json = json.loads(first["stdout"])
                second_json = json.loads(second["stdout"])
                if (first_json.get("written") == len(papers) and first_json.get("skipped") == 0 and
                        second_json.get("written") == 0 and second_json.get("skipped") == len(papers)):
                    status = "passed"
            except json.JSONDecodeError:
                pass
        return {
            "name": "paper vector temp idempotency",
            "cmd": [py, str(SCRIPT_DIR / "paper_vector.py"), "extract-manifest", str(tmp_manifest), "--out-dir", str(out_dir)],
            "returncode": 0 if status == "passed" else 1,
            "stdout": stdout,
            "stderr": "",
            "status": status,
        }


def main(argv=None):
    parser = argparse.ArgumentParser(prog="audit_checks.py")
    parser.add_argument("wiki_root")
    args = parser.parse_args(argv)

    checks = run_checks(args.wiki_root)
    print(json.dumps({"checks": checks}, indent=2))
    return 0 if all(c["status"] == "passed" for c in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
