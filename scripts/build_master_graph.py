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


def build_alias_map(graph: dict) -> dict[str, str]:
    """Group nodes by normalized label; within each group of 2+, the highest-degree
    node (tie: lexically smallest id) is canonical and the rest map to it."""
    deg = degree_map(graph)
    groups: dict[str, list[str]] = {}
    for n in graph["nodes"]:
        key = normalize_label(n.get("norm_label") or n.get("label") or n["id"])
        if key:
            groups.setdefault(key, []).append(n["id"])
    alias: dict[str, str] = {}
    for ids in groups.values():
        if len(ids) < 2:
            continue
        canonical = sorted(ids, key=lambda i: (-deg.get(i, 0), i))[0]
        for i in ids:
            if i != canonical:
                alias[i] = canonical
    return alias


def validate_alias_map(alias_map: dict[str, str], graph: dict) -> None:
    """Raise ValueError on unknown ids, alias-that-is-also-canonical, or chains."""
    ids = {n["id"] for n in graph["nodes"]}
    canon = set(alias_map.values())
    for a, c in alias_map.items():
        if a not in ids or c not in ids:
            raise ValueError(f"alias map references unknown id: {a}->{c}")
        if a in canon:
            raise ValueError(f"id {a} is both an alias and a canonical")
        if c in alias_map:
            raise ValueError(f"canonical {c} is itself an alias (chain)")


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
