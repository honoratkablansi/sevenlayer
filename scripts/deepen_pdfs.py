"""Deepen the knowledge graph by mining reference PDFs.

Two interpreters: tests + jobs run under any Python; the `merge` rebuild needs
the system Python that has `graphify` installed. All graphify/networkx imports
are lazy (inside `rebuild`) so this module imports cleanly under the venv.

Usage (from repo root):
    python scripts/deepen_pdfs.py jobs  --only 4,6,7,8,9,12,16,17,18,20
    # ... dispatch one subagent per job (writes graphify-out/.deepen/frag-NN.json) ...
    python scripts/deepen_pdfs.py merge --only 4,6,7,8,9,12,16,17,18,20
"""
from __future__ import annotations

import collections
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO / "references" / "manifest.json"
GRAPH_PATH = REPO / "graphify-out" / "graph.json"
DEEPEN_DIR = REPO / "graphify-out" / ".deepen"


def _norm(p: str | None) -> str:
    return (p or "").replace("\\", "/")


def batch_for_ids(manifest: list[dict], ids: list[int]) -> list[tuple]:
    """Resolve ref ids to (id, file, slug, chapters), papers only.
    Skips duplicate_of entries, stubs, and web captures."""
    wanted = set(ids)
    rows = []
    for e in manifest:
        if e["id"] not in wanted:
            continue
        if e.get("duplicate_of") is not None or e.get("type") != "paper":
            continue
        rows.append((e["id"], e["file"], e["slug"], e["chapters"]))
    return rows


def anchors_for_source(graph: dict, source_file: str) -> list[str]:
    """Existing node ids whose source_file is this PDF (separator-insensitive)."""
    target = _norm(source_file)
    return [n["id"] for n in graph["nodes"] if _norm(n.get("source_file")) == target]


def graph_stats(graph: dict) -> dict:
    per_pdf = collections.Counter()
    by_top = collections.Counter()
    for n in graph["nodes"]:
        sf = _norm(n.get("source_file"))
        if not sf:
            continue
        by_top[sf.split("/")[0]] += 1
        if sf.endswith(".pdf"):
            per_pdf[sf.split("/")[-1]] += 1
    return {
        "nodes": len(graph["nodes"]),
        "edges": len(graph["links"]),
        "nodes_per_pdf": dict(per_pdf),
        "nodes_by_source_top": dict(by_top),
    }
