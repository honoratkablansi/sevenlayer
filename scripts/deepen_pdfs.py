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


def _load_json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def cmd_jobs(ids: list[int]) -> None:
    """Write graphify-out/.deepen/jobs.json describing the extraction batch."""
    manifest = _load_json(MANIFEST_PATH)
    graph = _load_json(GRAPH_PATH)
    DEEPEN_DIR.mkdir(parents=True, exist_ok=True)
    jobs = []
    for rid, file, slug, chapters in batch_for_ids(manifest, ids):
        jobs.append({
            "id": rid,
            "slug": slug,
            "pdf": file,
            "chapters": chapters,
            "anchors": anchors_for_source(graph, file),
            "frag_out": f"graphify-out/.deepen/frag-{rid:02d}.json",
        })
    (DEEPEN_DIR / "jobs.json").write_text(json.dumps(jobs, indent=2), encoding="utf-8")
    print(f"Wrote {len(jobs)} jobs to {DEEPEN_DIR / 'jobs.json'}")
    for j in jobs:
        print(f"  [{j['id']:02d}] {j['slug']:28} anchors={len(j['anchors'])} -> {j['frag_out']}")


def rebuild(graph: dict, n_files: int) -> dict:
    """Re-cluster the merged graph and regenerate all graphify outputs.
    Lazy imports: needs the system Python that has graphify + networkx."""
    from networkx.readwrite import json_graph
    from graphify.cluster import cluster, score_all
    from graphify.analyze import god_nodes, surprising_connections, suggest_questions
    from graphify.report import generate
    from graphify.export import to_json, to_html, to_obsidian

    G = json_graph.node_link_graph(graph, edges="links")
    communities = cluster(G)
    cohesion = score_all(G, communities)
    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)
    labels = {cid: f"Community {cid}" for cid in communities}
    detection = {"total_files": n_files, "total_words": 99999, "needs_graph": True,
                 "warning": None, "files": {"code": [], "document": [], "paper": []}}
    tokens = {"input": 0, "output": 0}
    questions = suggest_questions(G, communities, labels)

    report = generate(G, communities, cohesion, labels, gods, surprises,
                      detection, tokens, ".", suggested_questions=questions)
    (REPO / "graphify-out" / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
    wrote = to_json(G, communities, str(GRAPH_PATH), force=True)
    if wrote is False:
        raise RuntimeError("graphify to_json refused to write graph.json")
    if G.number_of_nodes() <= 5000:
        to_html(G, communities, str(REPO / "graphify-out" / "graph.html"),
                community_labels=labels)
    to_obsidian(G, communities, str(REPO / "graphify-out" / "obsidian"),
                community_labels=labels, cohesion=cohesion)
    return {"nodes": G.number_of_nodes(), "edges": G.number_of_edges(),
            "communities": len(communities)}


def cmd_merge(ids: list[int]) -> int:
    import datetime

    jobs = _load_json(DEEPEN_DIR / "jobs.json")
    jobs = [j for j in jobs if j["id"] in set(ids)] if ids else jobs
    graph = _load_json(GRAPH_PATH)
    before = graph_stats(graph)

    merged_ids = []
    for j in jobs:
        frag_path = REPO / j["frag_out"]
        if not frag_path.exists():
            print(f"  [{j['id']:02d}] {j['slug']}: no fragment, skipped")
            continue
        try:
            frag = load_fragment(frag_path)
        except ValueError as exc:
            print(f"  [{j['id']:02d}] {j['slug']}: bad fragment ({exc}), skipped")
            continue
        merge_fragment(graph, frag)
        merged_ids.append(j["id"])

    if not merged_ids:
        print("No fragments merged; nothing to rebuild.")
        return 1

    manifest = _load_json(MANIFEST_PATH)
    n_files = len(manifest)
    stats = rebuild(graph, n_files)
    after = graph_stats(_load_json(GRAPH_PATH))

    # NOTE: graphify-out/manifest.json (the graph file-manifest of mtimes/hashes)
    # is deliberately left untouched. The PDFs on disk are unchanged, so a future
    # `graphify --update` sees them as unchanged and will NOT re-extract — which
    # preserves these deep-mined nodes. Rewriting the hashes here with a non-
    # graphify scheme would instead trigger a wasteful re-extract that overwrites them.

    # Append an estimated-cost run (Agent tool gives no exact per-subagent counts).
    cost_path = REPO / "graphify-out" / "cost.json"
    cost = _load_json(cost_path) if cost_path.exists() else {
        "runs": [], "total_input_tokens": 0, "total_output_tokens": 0}
    est_in = sum((REPO / j["pdf"]).stat().st_size for j in jobs if j["id"] in merged_ids) // 3
    cost["runs"].append({"date": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                         "input_tokens": est_in, "output_tokens": 0,
                         "files": len(merged_ids), "note": "deepen_pdfs estimate"})
    cost["total_input_tokens"] += est_in
    cost_path.write_text(json.dumps(cost, indent=2), encoding="utf-8")

    print(f"\nMerged refs {merged_ids}")
    print(f"  nodes {before['nodes']} -> {after['nodes']}   edges {before['edges']} -> {after['edges']}   communities {stats['communities']}")
    for j in jobs:
        if j["id"] in merged_ids:
            name = j["pdf"].split("/")[-1]
            print(f"  {name:34} {before['nodes_per_pdf'].get(name,0):>2} -> {after['nodes_per_pdf'].get(name,0):>3} nodes")
    return 0


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("jobs", "merge"):
        p = sub.add_parser(name)
        p.add_argument("--only", help="comma-separated ref ids", default="")
    args = ap.parse_args()
    ids = [int(x) for x in args.only.split(",") if x.strip()]
    if args.cmd == "jobs":
        cmd_jobs(ids)
        return 0
    return cmd_merge(ids)


if __name__ == "__main__":
    import sys
    sys.exit(main())
