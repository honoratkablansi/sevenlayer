"""Download the book's references per chapter, driven by references/manifest.json.

Usage (from repo root, venv active):
    python scripts/fetch_references.py [--dry-run] [--force] [--only 6,17,42]
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO / "references" / "manifest.json"


def load_manifest() -> list[dict]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def save_manifest(entries: list[dict]) -> None:
    MANIFEST_PATH.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def is_pdf(data: bytes) -> bool:
    return data[:5] == b"%PDF-"


def stub_markdown(entry: dict) -> str:
    chapters = ", ".join(str(c) for c in entry["chapters"])
    return (
        "---\n"
        f"ref_id: {entry['id']}\n"
        f"chapters: [{chapters}]\n"
        "type: stub\n"
        "---\n\n"
        f"# Reference {entry['id']}: {entry['slug']}\n\n"
        f"{entry['citation']}\n\n"
        "This source is print-only or paywalled; no electronic copy is stored. "
        "This stub exists so the reference appears as a node in the knowledge graph.\n"
    )


def web_markdown(entry: dict, text: str, fetched_with: str, date: str) -> str:
    chapters = ", ".join(str(c) for c in entry["chapters"])
    return (
        "---\n"
        f"ref_id: {entry['id']}\n"
        f"chapters: [{chapters}]\n"
        "type: web\n"
        f"source_url: {entry['url']}\n"
        f"fetched: {date}\n"
        f"fetched_with: {fetched_with}\n"
        f"citation: '{entry['citation'].replace(chr(39), chr(39) * 2)}'\n"
        "---\n\n"
        f"# {entry['citation']}\n\n"
        f"{text}\n"
    )
