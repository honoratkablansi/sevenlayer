"""Build the recursion knowledge graph from outline + reference fragments.

Usage (from repo root):
    python scripts/split_recursion_outline.py     # writes recursion-graph/.work/rcNN.md
    # ... dispatch extraction subagents -> recursion-graph/.work/frag-*.json ...
    python scripts/build_recursion_graph.py build
    python scripts/build_recursion_graph.py relabel

graphify/networkx imports are lazy (system python for build).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from build_book_graph import merge_extraction  # reuse the tested union helper

RG_DIR = REPO / "recursion-graph"
WORK = RG_DIR / ".work"
RG_GRAPH = RG_DIR / "graph.json"


def _load(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def collect_fragments(work: Path) -> dict:
    """Union every frag-*.json in `work` into one extraction dict."""
    frags = []
    for p in sorted(Path(work).glob("frag-*.json")):
        try:
            frags.append(_load(p))
        except Exception as exc:  # noqa: BLE001
            print(f"  skip {p.name}: {exc}")
    return merge_extraction(frags)


def _export(G, communities, labels, n_files: int) -> dict:
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
    RG_DIR.mkdir(parents=True, exist_ok=True)
    (RG_DIR / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
    if to_json(G, communities, str(RG_GRAPH), force=True) is False:
        raise RuntimeError("to_json refused to write recursion-graph/graph.json")
    if G.number_of_nodes() <= 5000:
        to_html(G, communities, str(RG_DIR / "graph.html"), community_labels=labels)
    to_obsidian(G, communities, str(RG_DIR / "obsidian"), community_labels=labels, cohesion=cohesion)
    return {"nodes": G.number_of_nodes(), "edges": G.number_of_edges(), "communities": len(communities)}


def _dump_communities() -> None:
    g = _load(RG_GRAPH)
    comms: dict[str, list] = {}
    for n in g["nodes"]:
        comms.setdefault(str(n.get("community")), []).append(n.get("label", n["id"]))
    (WORK / "communities.json").write_text(json.dumps(comms, indent=2, ensure_ascii=False), encoding="utf-8")


def cmd_build() -> int:
    from graphify.build import build_from_json
    extraction = collect_fragments(WORK)
    if not extraction["nodes"]:
        print("No fragments in recursion-graph/.work/; run split + extraction first.")
        return 1
    G = build_from_json(extraction)
    stats = _export(G, None, None, len(list(WORK.glob("frag-*.json"))))
    _dump_communities()
    print(f"built recursion-graph: {stats['nodes']} nodes, {stats['edges']} edges, {stats['communities']} communities")
    print(f"wrote {WORK / 'communities.json'} for labeling")
    return 0


def cmd_relabel() -> int:
    from networkx.readwrite import json_graph
    from graphify.cluster import score_all
    from graphify.analyze import god_nodes, surprising_connections, suggest_questions
    from graphify.report import generate
    from graphify.export import to_html, to_obsidian
    labels_path = WORK / "labels.json"
    if not labels_path.exists():
        print(f"no {labels_path}")
        return 1
    labels = {int(k): v for k, v in _load(labels_path).items()}
    g = _load(RG_GRAPH)
    communities: dict[int, list] = {}
    for n in g["nodes"]:
        c = n.get("community")
        if c is not None:
            communities.setdefault(int(c), []).append(n["id"])
    G = json_graph.node_link_graph(g, edges="links")
    cohesion = score_all(G, communities)
    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)
    questions = suggest_questions(G, communities, labels)
    detection = {"total_files": len(communities), "total_words": 99999, "needs_graph": True,
                 "warning": None, "files": {"code": [], "document": [], "paper": []}}
    report = generate(G, communities, cohesion, labels, gods, surprises,
                      detection, {"input": 0, "output": 0}, ".", suggested_questions=questions)
    (RG_DIR / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
    to_html(G, communities, str(RG_DIR / "graph.html"), community_labels=labels)
    to_obsidian(G, communities, str(RG_DIR / "obsidian"), community_labels=labels, cohesion=cohesion)
    print(f"relabeled {len(communities)} communities")
    return 0


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build")
    sub.add_parser("relabel")
    args = ap.parse_args()
    return cmd_build() if args.cmd == "build" else cmd_relabel()


if __name__ == "__main__":
    sys.exit(main())
