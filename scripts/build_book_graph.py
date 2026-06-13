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


def _export(G, communities, labels, n_files: int) -> dict:
    """Cluster-aware export of a graphify graph G into book-graph/. If communities
    is None, cluster first. Lazy graphify import (system python)."""
    from graphify.cluster import cluster, score_all
    from graphify.analyze import god_nodes, surprising_connections, suggest_questions
    from graphify.report import generate
    from graphify.export import to_json, to_html, to_obsidian

    if communities is None:
        communities = cluster(G)
    cohesion = score_all(G, communities)
    if labels is None:
        labels = {cid: f"Community {cid}" for cid in communities}
    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)
    questions = suggest_questions(G, communities, labels)
    detection = {"total_files": n_files, "total_words": 99999, "needs_graph": True,
                 "warning": None, "files": {"code": [], "document": [], "paper": []}}
    report = generate(G, communities, cohesion, labels, gods, surprises,
                      detection, {"input": 0, "output": 0}, ".", suggested_questions=questions)
    BOOK_DIR.mkdir(parents=True, exist_ok=True)
    (BOOK_DIR / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
    if to_json(G, communities, str(BOOK_GRAPH), force=True) is False:
        raise RuntimeError("to_json refused to write book-graph/graph.json")
    if G.number_of_nodes() <= 5000:
        to_html(G, communities, str(BOOK_DIR / "graph.html"), community_labels=labels)
    to_obsidian(G, communities, str(BOOK_DIR / "obsidian"), community_labels=labels, cohesion=cohesion)
    return {"nodes": G.number_of_nodes(), "edges": G.number_of_edges(), "communities": len(communities)}


def _dump_communities() -> None:
    g = _load(BOOK_GRAPH)
    comms: dict[str, list] = {}
    for n in g["nodes"]:
        comms.setdefault(str(n.get("community")), []).append(n.get("label", n["id"]))
    (WORK / "communities.json").write_text(
        json.dumps(comms, indent=2, ensure_ascii=False), encoding="utf-8")


def cmd_build() -> int:
    from graphify.build import build_from_json
    frags = []
    for p in sorted(WORK.glob("frag-ch*.json")):
        try:
            frags.append(_load(p))
        except Exception as exc:  # noqa: BLE001
            print(f"  skip {p.name}: {exc}")
    if not frags:
        print("No chapter fragments in book-graph/.work/; run split + extraction first.")
        return 1
    extraction = merge_extraction(frags)
    if not extraction["nodes"]:
        print("Merged extraction has 0 nodes; refusing to build.")
        return 1
    G = build_from_json(extraction)
    stats = _export(G, None, None, len(frags))
    _dump_communities()
    _write_cost()
    print(f"built book-graph: {stats['nodes']} nodes, {stats['edges']} edges, {stats['communities']} communities")
    print(f"wrote {WORK / 'communities.json'} for labeling")
    return 0


def cmd_augment() -> int:
    import sys
    sys.path.insert(0, str(REPO / "scripts"))
    from deepen_pdfs import merge_fragment
    from networkx.readwrite import json_graph

    book = _load(BOOK_GRAPH)
    before = (len(book["nodes"]), len(book["links"]))
    refsg = reference_subgraph(_load(GRAPH1))
    merge_fragment(book, refsg)  # additive: union nodes/edges, drop dangling
    G = json_graph.node_link_graph(book, edges="links")
    stats = _export(G, None, None, len(book["nodes"]))
    _dump_communities()
    print(f"augmented with {len(refsg['nodes'])} reference nodes: "
          f"nodes {before[0]}->{stats['nodes']}, edges {before[1]}->{stats['edges']}, "
          f"communities {stats['communities']}")
    return 0


def relabel(labels: dict) -> int:
    """Regenerate book-graph report/html/obsidian with community names, reusing the
    existing clustering from the per-node 'community' field (no re-cluster)."""
    from networkx.readwrite import json_graph
    book = _load(BOOK_GRAPH)
    communities: dict[int, list] = {}
    for n in book["nodes"]:
        c = n.get("community")
        if c is not None:
            communities.setdefault(int(c), []).append(n["id"])
    G = json_graph.node_link_graph(book, edges="links")
    _export_with_communities(G, communities, {int(k): v for k, v in labels.items()}, len(book["nodes"]))
    print(f"relabeled {len(communities)} communities")
    return 0


def _export_with_communities(G, communities, labels, n_files):
    from graphify.cluster import score_all
    from graphify.analyze import god_nodes, surprising_connections, suggest_questions
    from graphify.report import generate
    from graphify.export import to_html, to_obsidian
    cohesion = score_all(G, communities)
    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)
    questions = suggest_questions(G, communities, labels)
    detection = {"total_files": n_files, "total_words": 99999, "needs_graph": True,
                 "warning": None, "files": {"code": [], "document": [], "paper": []}}
    report = generate(G, communities, cohesion, labels, gods, surprises,
                      detection, {"input": 0, "output": 0}, ".", suggested_questions=questions)
    (BOOK_DIR / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
    if G.number_of_nodes() <= 5000:
        to_html(G, communities, str(BOOK_DIR / "graph.html"), community_labels=labels)
    to_obsidian(G, communities, str(BOOK_DIR / "obsidian"), community_labels=labels, cohesion=cohesion)


def _write_cost() -> None:
    import datetime
    cost_path = BOOK_DIR / "cost.json"
    cost = _load(cost_path) if cost_path.exists() else {"runs": [], "total_input_tokens": 0, "total_output_tokens": 0}
    cost["runs"].append({"date": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                         "input_tokens": 0, "output_tokens": 0,
                         "note": "book-graph build (measured subagent tokens recorded in session)"})
    cost_path.write_text(json.dumps(cost, indent=2), encoding="utf-8")


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build")
    sub.add_parser("augment")
    p = sub.add_parser("relabel")
    p.add_argument("--labels", default=str(WORK / "labels.json"))
    args = ap.parse_args()
    if args.cmd == "build":
        return cmd_build()
    if args.cmd == "augment":
        return cmd_augment()
    return relabel(_load(Path(args.labels)))


if __name__ == "__main__":
    import sys as _sys
    _sys.exit(main())
