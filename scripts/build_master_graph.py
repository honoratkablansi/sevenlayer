"""Build the master knowledge graph: merge book-graph + recursion-graph +
graphify-out, snowball citations out of the reference corpus (bounded), and
extract the concepts that should be in the book.

graphify/networkx imports are lazy (inside _export/rebuild) so this module
imports under the venv for tests; run build commands with the system Python
that has graphify installed.

Usage (from repo root):
    python scripts/build_master_graph.py merge          # union 3 graphs -> master-graph/
    python scripts/build_master_graph.py consolidate    # apply .work/aliases.json, rebuild
    python scripts/build_master_graph.py relabel         # community names from .work/labels.json
    python scripts/build_master_graph.py concepts        # write CONCEPTS_FOR_BOOK.md
    python scripts/build_master_graph.py snowball-plan   # write extraction jobs for the frontier
    python scripts/build_master_graph.py snowball-merge  # fold fragments, update state, stop-check
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MASTER_DIR = REPO / "master-graph"
MASTER_GRAPH = MASTER_DIR / "graph.json"
WORK = MASTER_DIR / ".work"
SNOWBALL = MASTER_DIR / ".snowball"

INPUTS = {
    "book": REPO / "book-graph" / "graph.json",
    "recursion": REPO / "recursion-graph" / "graph.json",
    "graph1": REPO / "graphify-out" / "graph.json",
}
MANIFESTS = {
    "book": REPO / "references" / "manifest.json",
    "recursion": REPO / "references" / "recursion" / "manifest.json",
}
MANUSCRIPT = "proving-nothing.md"


def _load(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _dump(path: Path, obj) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
