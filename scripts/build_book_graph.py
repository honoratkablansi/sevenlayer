"""Build the book knowledge graph from chapter fragments, and augment it with
graph 1's reference subgraph.

Usage (from repo root):
    python scripts/split_manuscript.py            # writes book-graph/.work/chNN.md
    # ... dispatch one subagent per chapter -> book-graph/.work/frag-chNN.json ...
    python scripts/build_book_graph.py build      # build book-graph/ from fragments
    python scripts/build_book_graph.py augment    # merge graph 1's references, rebuild
    python scripts/build_book_graph.py relabel    # regenerate report with community names

graphify/networkx imports are lazy (inside build/export) so this module imports
under the venv for tests; run build/augment with the system python that has graphify.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BOOK_DIR = REPO / "book-graph"
WORK = BOOK_DIR / ".work"
BOOK_GRAPH = BOOK_DIR / "graph.json"
GRAPH1 = REPO / "graphify-out" / "graph.json"
_LINK_FIELDS = ("relation", "confidence", "source_file", "source_location", "weight")


def merge_extraction(fragments: list[dict]) -> dict:
    """Union chapter fragments into one extraction dict for build_from_json:
    union nodes by id (first wins), union edges, drop edges with missing endpoints."""
    nodes, node_ids = [], set()
    for f in fragments:
        for n in f.get("nodes", []):
            if n["id"] not in node_ids:
                nodes.append(n)
                node_ids.add(n["id"])
    edges, seen = [], set()
    for f in fragments:
        for e in f.get("edges", []):
            key = (e.get("source"), e.get("target"), e.get("relation"))
            if key in seen:
                continue
            if e.get("source") not in node_ids or e.get("target") not in node_ids:
                continue
            seen.add(key)
            edges.append(e)
    return {"nodes": nodes, "edges": edges, "input_tokens": 0, "output_tokens": 0}


def reference_subgraph(graph: dict) -> dict:
    """From a node-link graph, return {"nodes", "edges"} containing only nodes whose
    source_file is under references/ and the edges induced on them."""
    def is_ref(n):
        return "references/" in (n.get("source_file") or "").replace("\\", "/")
    nodes = [n for n in graph["nodes"] if is_ref(n)]
    ids = {n["id"] for n in nodes}
    edges = []
    for l in graph["links"]:
        if l["source"] in ids and l["target"] in ids:
            e = {"source": l["source"], "target": l["target"]}
            for fld in _LINK_FIELDS:
                if fld in l:
                    e[fld] = l[fld]
            edges.append(e)
    return {"nodes": nodes, "edges": edges}


def _load(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))
