#!/usr/bin/env python3
"""Research-paper fixture utilities for llm-wiki.

Turns a manifest of local PDF files into page-delimited raw markdown sources.
The original PDFs are copied to raw/assets/papers; markdown sources are written
to the requested raw output directory.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath


REQUIRED_PAPER_FIELDS = {
    "rank", "title", "year", "doi", "semantic_scholar_url", "pdf_source_url",
    "file", "sha256", "bytes", "pages",
}


def load_manifest(path):
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    papers = data["papers"] if isinstance(data, dict) else data
    if not isinstance(papers, list):
        raise ValueError("manifest must be an object with papers[] or a bare paper array")
    return data, papers


def validate_manifest(path, validate_assets=False, expected_count=None):
    _, papers = load_manifest(path)
    errors = []
    if expected_count is not None and len(papers) != expected_count:
        errors.append(f"expected {expected_count} papers, found {len(papers)}")
    seen_ranks = set()
    seen_slugs = set()
    manifest_dir = Path(path).parent
    for idx, paper in enumerate(papers, 1):
        missing = sorted(REQUIRED_PAPER_FIELDS - set(paper))
        if missing:
            errors.append(f"paper {idx} missing: {', '.join(missing)}")
            continue
        if not is_safe_manifest_file(paper["file"]):
            errors.append(f"paper {idx} has unsafe file path: {paper['file']}")
        rank = paper["rank"]
        if rank in seen_ranks:
            errors.append(f"paper {idx} duplicates rank: {rank}")
        seen_ranks.add(rank)
        slug = paper_slug(paper)
        if slug in seen_slugs:
            errors.append(f"paper {idx} duplicates slug: {slug}")
        seen_slugs.add(slug)
        if validate_assets:
            try:
                pdf_path = manifest_pdf_path(manifest_dir, paper["file"])
                verify_pdf(pdf_path, paper.get("sha256"), paper.get("bytes"))
                from pypdf import PdfReader
                pages = len(PdfReader(str(pdf_path)).pages)
                if pages != int(paper["pages"]):
                    errors.append(f"paper {idx} page count mismatch: manifest {paper['pages']} != pdf {pages}")
            except Exception as exc:
                errors.append(f"paper {idx} asset validation failed: {exc}")
    if errors:
        raise ValueError("; ".join(errors))
    return papers


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_pdf(path, expected_sha=None, expected_bytes=None):
    p = Path(path)
    with open(p, "rb") as fh:
        header = fh.read(5)
    if header != b"%PDF-":
        raise ValueError(f"{p} does not start with %PDF-")
    if expected_bytes is not None and p.stat().st_size != int(expected_bytes):
        raise ValueError(f"{p} byte count mismatch")
    actual_sha = sha256_file(p)
    if expected_sha and actual_sha.lower() != str(expected_sha).lower():
        raise ValueError(f"{p} sha256 mismatch")
    return actual_sha


_WIN_RESERVED = {"con", "prn", "aux", "nul"} | {f"com{i}" for i in range(1, 10)} | {f"lpt{i}" for i in range(1, 10)}


def paper_slug(paper):
    rank = int(paper["rank"])
    title = re.sub(r"[^a-z0-9]+", "-", paper["title"].lower()).strip("-")
    title = title[:72].strip("-") or "paper"
    if title in _WIN_RESERVED:
        title = f"paper-{title}"
    return f"{rank:02d}-{title}"


def is_safe_manifest_file(value):
    text = str(value)
    if Path(text).is_absolute() or PureWindowsPath(text).is_absolute() or PurePosixPath(text).is_absolute():
        return False
    parts = list(Path(text).parts) + list(PureWindowsPath(text).parts) + list(PurePosixPath(text).parts)
    if any(part in ("..", "") for part in parts):
        return False
    return True


def manifest_pdf_path(manifest_dir, filename):
    if not is_safe_manifest_file(filename):
        raise ValueError(f"unsafe manifest file path: {filename}")
    return Path(manifest_dir) / filename


def _yaml_value(value):
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    text = str(value)
    if text == "" or any(c in text for c in ':#"\n[]{}'):
        return '"' + text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'
    return text


def build_frontmatter(meta):
    ordered = [
        "source_type", "title", "year", "doi", "semantic_scholar_url",
        "pdf_source_url", "citation_count", "pdf_asset", "pdf_sha256",
        "bytes", "pages", "is_verbatim", "extractor", "extracted_at",
    ]
    lines = ["---"]
    for key in ordered:
        lines.append(f"{key}: {_yaml_value(meta.get(key))}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def extract_pdf_to_markdown(pdf_path, meta):
    """Return (body_markdown, page_count) using pypdf."""
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    sections = []
    for index, page in enumerate(reader.pages, 1):
        text = (page.extract_text() or "").strip()
        if not text:
            text = "[No extractable text on this page.]"
        sections.append(f"## Page {index}\n\n{text}")
    return "\n\n".join(sections) + "\n", len(reader.pages)


def _raw_root_for(out_dir):
    out = Path(out_dir)
    return out if out.name == "raw" else out.parent


def write_paper_source(paper, manifest_dir, out_dir):
    out = Path(out_dir)
    raw_root = _raw_root_for(out)
    asset_dir = raw_root / "assets" / "papers"
    out.mkdir(parents=True, exist_ok=True)
    asset_dir.mkdir(parents=True, exist_ok=True)

    slug = paper_slug(paper)
    src_pdf = manifest_pdf_path(manifest_dir, paper["file"])
    verify_pdf(src_pdf, paper.get("sha256"), paper.get("bytes"))

    pdf_dest = asset_dir / f"{slug}.pdf"
    md_dest = out / f"{slug}.md"
    if pdf_dest.exists() and sha256_file(pdf_dest).lower() != paper["sha256"].lower():
        raise ValueError(f"existing asset has different hash: {pdf_dest}")

    if not pdf_dest.exists():
        shutil.copyfile(src_pdf, pdf_dest)

    if md_dest.exists():
        return {"path": str(md_dest), "pdf_asset": str(pdf_dest), "status": "skipped"}

    asset_rel = pdf_dest.relative_to(raw_root).as_posix()
    meta = {
        "source_type": "paper",
        "title": paper["title"],
        "year": paper.get("year"),
        "doi": paper.get("doi"),
        "semantic_scholar_url": paper.get("semantic_scholar_url"),
        "pdf_source_url": paper.get("pdf_source_url"),
        "citation_count": paper.get("citations"),
        "pdf_asset": asset_rel,
        "pdf_sha256": paper.get("sha256"),
        "bytes": paper.get("bytes"),
        "pages": paper.get("pages"),
        "is_verbatim": True,
        "extractor": "pypdf",
        "extracted_at": datetime.date.today().isoformat(),
    }
    body, page_count = extract_pdf_to_markdown(src_pdf, meta)
    meta["pages"] = page_count
    md_dest.write_text(build_frontmatter(meta) + f"\n# {paper['title']}\n\n" + body, encoding="utf-8")
    return {"path": str(md_dest), "pdf_asset": str(pdf_dest), "status": "written"}


def extract_manifest(manifest_path, out_dir):
    papers = validate_manifest(manifest_path, validate_assets=True)
    manifest_dir = Path(manifest_path).parent
    results = [write_paper_source(paper, manifest_dir, out_dir) for paper in papers]
    return {
        "papers": len(results),
        "written": sum(1 for r in results if r["status"] == "written"),
        "skipped": sum(1 for r in results if r["status"] == "skipped"),
        "results": results,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(prog="paper_vector.py")
    sub = parser.add_subparsers(dest="cmd", required=True)
    validate = sub.add_parser("validate-manifest")
    validate.add_argument("manifest")
    validate.add_argument("--expected-count", type=int)
    extract = sub.add_parser("extract-manifest")
    extract.add_argument("manifest")
    extract.add_argument("--out-dir", required=True)
    args = parser.parse_args(argv)

    try:
        if args.cmd == "validate-manifest":
            papers = validate_manifest(args.manifest, validate_assets=True, expected_count=args.expected_count)
            print(json.dumps({"papers": len(papers), "status": "ok"}))
            return 0
        if args.cmd == "extract-manifest":
            print(json.dumps(extract_manifest(args.manifest, args.out_dir), indent=2))
            return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
