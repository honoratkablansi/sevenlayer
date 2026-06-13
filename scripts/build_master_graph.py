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


def _depluralize(tok: str) -> str:
    for suf in ("'s", "(s)"):
        if tok.endswith(suf):
            return tok[: -len(suf)]
    if len(tok) > 3 and tok.endswith("s") and not tok.endswith("ss"):
        return tok[:-1]
    return tok


def normalize_label(label: str | None) -> str:
    """Lowercase, strip punctuation to single spaces, depluralize each token.
    Used as the dedup key and the coverage/vocabulary key."""
    s = re.sub(r"[^a-z0-9]+", " ", (label or "").lower()).strip()
    return " ".join(_depluralize(t) for t in s.split())


def degree_map(graph: dict) -> dict[str, int]:
    deg = {n["id"]: 0 for n in graph["nodes"]}
    for l in graph["links"]:
        if l.get("source") in deg:
            deg[l["source"]] += 1
        if l.get("target") in deg:
            deg[l["target"]] += 1
    return deg


def merge_graphs(named_inputs: list[tuple[str, dict]]) -> dict:
    """Union (name, node-link dict) inputs. Nodes union by id (first wins for
    attributes; origin_graphs accumulates contributor names in input order).
    Links union by (source, target, relation); dangling edges dropped. Returns a
    node-link dict shaped like the first input."""
    base, nodes, order = None, {}, []
    for name, g in named_inputs:
        if base is None:
            base = {k: v for k, v in g.items() if k not in ("nodes", "links")}
        for n in g.get("nodes", []):
            nid = n["id"]
            if nid not in nodes:
                merged = dict(n)
                merged["origin_graphs"] = [name]
                nodes[nid] = merged
                order.append(nid)
            else:
                og = nodes[nid].setdefault("origin_graphs", [])
                if name not in og:
                    og.append(name)
    node_ids = set(nodes)
    links, seen = [], set()
    for _name, g in named_inputs:
        for l in g.get("links", []):
            key = (l.get("source"), l.get("target"), l.get("relation"))
            if key in seen:
                continue
            if l.get("source") not in node_ids or l.get("target") not in node_ids:
                continue
            seen.add(key)
            links.append(dict(l))
    out = dict(base or {})
    out["nodes"] = [nodes[i] for i in order]
    out["links"] = links
    return out
