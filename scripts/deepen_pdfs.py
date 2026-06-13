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


_LINK_FIELDS = ("relation", "confidence", "source_file", "source_location", "weight")


def load_fragment(path: Path) -> dict:
    """Read + validate a subagent fragment: {"nodes":[{id,label,...}], "edges":[...]}"""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "nodes" not in data or "edges" not in data:
        raise ValueError(f"{path}: fragment needs 'nodes' and 'edges' keys")
    if not isinstance(data["nodes"], list) or not isinstance(data["edges"], list):
        raise ValueError(f"{path}: 'nodes' and 'edges' must be lists")
    for n in data["nodes"]:
        if "id" not in n or "label" not in n:
            raise ValueError(f"{path}: every node needs 'id' and 'label': {n}")
    return data


def merge_fragment(graph: dict, fragment: dict, _force_node_count: int | None = None) -> dict:
    """Additively merge a fragment into a node-link graph. Union nodes by id
    (existing wins), union edges by (source,target,relation), drop dangling edges,
    enforce the additive invariant (node count never decreases)."""
    before = len(graph["nodes"]) if _force_node_count is None else _force_node_count
    node_ids = {n["id"] for n in graph["nodes"]}
    for n in fragment["nodes"]:
        if n["id"] not in node_ids:
            graph["nodes"].append(n)
            node_ids.add(n["id"])

    seen = {(l["source"], l["target"], l.get("relation")) for l in graph["links"]}
    for e in fragment["edges"]:
        key = (e.get("source"), e.get("target"), e.get("relation"))
        if key in seen:
            continue
        if e.get("source") not in node_ids or e.get("target") not in node_ids:
            continue  # dangling
        link = {"source": e["source"], "target": e["target"]}
        for f in _LINK_FIELDS:
            if f in e:
                link[f] = e[f]
        graph["links"].append(link)
        seen.add(key)

    assert len(graph["nodes"]) >= before, "additive invariant violated"
    return graph
