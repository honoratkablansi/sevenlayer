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
    # Drop a plural 's', but keep double-s words (soundness) and common Latin
    # singular endings (consensus, status, basis, axis, analysis, ...).
    if len(tok) > 3 and tok.endswith("s") and not tok.endswith(("ss", "us", "is")):
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
    node (tie: lexically smallest id) is canonical and the rest map to it. Nodes
    with no usable label (neither norm_label nor label) are left ungrouped."""
    deg = degree_map(graph)
    groups: dict[str, list[str]] = {}
    for n in graph["nodes"]:
        raw = n.get("norm_label") or n.get("label")
        if not raw:
            continue  # don't alias nodes we can't name (no id fallback)
        key = normalize_label(raw)
        if key:
            groups.setdefault(key, []).append(n["id"])
    alias: dict[str, str] = {}
    for ids in groups.values():
        if len(ids) < 2:
            continue
        canonical = min(ids, key=lambda i: (-deg.get(i, 0), i))
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


def _export(G, communities, labels, n_files: int) -> dict:
    """Cluster-aware export of a graphify graph G into master-graph/.
    Lazy graphify import (system python)."""
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
    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    (MASTER_DIR / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
    if to_json(G, communities, str(MASTER_GRAPH), force=True) is False:
        raise RuntimeError("to_json refused to write master-graph/graph.json")
    if G.number_of_nodes() <= 5000:
        to_html(G, communities, str(MASTER_DIR / "graph.html"), community_labels=labels)
    to_obsidian(G, communities, str(MASTER_DIR / "obsidian"), community_labels=labels, cohesion=cohesion)
    return {"nodes": G.number_of_nodes(), "edges": G.number_of_edges(), "communities": len(communities)}


def _export_reports_only(G, communities, labels, n_files: int) -> None:
    """Regenerate report/html/obsidian for an EXISTING partition without
    re-clustering or rewriting graph.json (mirrors build_book_graph
    ._export_with_communities). Lazy graphify import."""
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
    (MASTER_DIR / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
    if G.number_of_nodes() <= 5000:
        to_html(G, communities, str(MASTER_DIR / "graph.html"), community_labels=labels)
    to_obsidian(G, communities, str(MASTER_DIR / "obsidian"), community_labels=labels, cohesion=cohesion)


def _dump_communities() -> None:
    g = _load(MASTER_GRAPH)
    comms: dict[str, list] = {}
    for n in g["nodes"]:
        comms.setdefault(str(n.get("community")), []).append(n.get("label", n["id"]))
    _dump(WORK / "communities.json", comms)


def cmd_merge() -> int:
    from networkx.readwrite import json_graph
    missing = [str(p) for p in INPUTS.values() if not p.exists()]
    if missing:
        print("Missing input graphs:\n  " + "\n  ".join(missing))
        return 1
    merged = merge_graphs([(name, _load(p)) for name, p in INPUTS.items()])
    alias = build_alias_map(merged)
    validate_alias_map(alias, merged)
    _dump(WORK / "aliases.json", alias)  # deterministic aliases; hub LLM pass appends later
    G = json_graph.node_link_graph(merged, edges="links")
    stats = _export(G, None, None, len(INPUTS))
    _dump_communities()
    print(f"merged {len(INPUTS)} graphs: {stats['nodes']} nodes, {stats['edges']} edges, "
          f"{stats['communities']} communities")
    print(f"wrote {WORK / 'aliases.json'} ({len(alias)} deterministic aliases) and communities.json")
    return 0


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


def _is_reference(source_file: str | None) -> bool:
    return "references/" in (source_file or "").replace("\\", "/")


def is_concept(node: dict) -> bool:
    return str(node.get("id", "")).startswith("concept_")


def reference_support(graph: dict) -> dict[str, int]:
    """Per node: number of DISTINCT reference source_files among the node and its
    link neighbors."""
    nbrs: dict[str, set] = {n["id"]: set() for n in graph["nodes"]}
    sf = {n["id"]: n.get("source_file") for n in graph["nodes"]}
    for l in graph["links"]:
        s, t = l.get("source"), l.get("target")
        if s in nbrs and t in nbrs:
            nbrs[s].add(t)
            nbrs[t].add(s)
    support = {}
    for nid, ns in nbrs.items():
        files = set()
        for cand in (nid, *ns):
            fn = (sf.get(cand) or "").replace("\\", "/")
            if _is_reference(fn):
                files.add(fn)
        support[nid] = len(files)
    return support


def score_concepts(graph: dict, hub_top: int = 50) -> list[dict]:
    """Rank concept_* nodes by degree + 2*reference_support. Mark top hub_top by
    degree as hubs (graphify god-nodes are high-degree; degree is the pure proxy)."""
    deg = degree_map(graph)
    support = reference_support(graph)
    concepts = [n for n in graph["nodes"] if is_concept(n)]
    hub_ids = {n["id"] for n in sorted(
        concepts, key=lambda n: (-deg[n["id"]], n["id"]))[:hub_top]}
    rows = [{
        "id": n["id"], "label": n.get("label"), "community": n.get("community"),
        "degree": deg[n["id"]], "support": support.get(n["id"], 0),
        "is_hub": n["id"] in hub_ids,
        "score": deg[n["id"]] + 2 * support.get(n["id"], 0),
    } for n in concepts]
    rows.sort(key=lambda r: (-r["score"], r["id"]))
    return rows


def _in_manuscript(node: dict) -> bool:
    sf = (node.get("source_file") or "").replace("\\", "/")
    return sf == MANUSCRIPT or sf.startswith("wiki/chapters/")


def chapter_of(node: dict) -> str:
    match = re.search(r"[Cc]hapter\s+(\d+)", node.get("source_location") or "")
    return f"Chapter {match.group(1)}" if match else "Unassigned"


def coverage_diff(graph: dict, scored: list[dict], under_threshold: int = 4) -> list[dict]:
    """Tag each scored concept: absent (no manuscript node with its normalized
    label), under-covered (in manuscript but reference_support >= under_threshold),
    or well-covered."""
    covered = {normalize_label(n.get("label") or "")
               for n in graph["nodes"] if _in_manuscript(n)}
    by_id = {n["id"]: n for n in graph["nodes"]}
    out = []
    for r in scored:
        in_text = normalize_label(r["label"] or "") in covered
        if not in_text:
            verdict = "absent"
        elif r["support"] >= under_threshold:
            verdict = "under-covered"
        else:
            verdict = "well-covered"
        out.append({**r, "verdict": verdict,
                    "chapter": chapter_of(by_id.get(r["id"], {}))})
    return out


def _md_cell(value) -> str:
    """Escape a value for a markdown table/list cell (pipes break tables).
    Uses the HTML entity &#124; so that raw pipe-count checks stay at 7 columns."""
    return str(value if value is not None else "").replace("|", "&#124;").replace("\n", " ")


def render_concepts_md(rows: list[dict], top: int = 200) -> str:
    lines = ["# Concepts for the Book", "",
             "Ranked by `degree + 2*reference_support` over the master graph. "
             "Verdict vs the manuscript: **well-covered** / **under-covered** "
             "(in the book but heavily cited in the literature) / **absent** "
             "(in the references, not in the book).", "",
             "| Concept | Community | Degree | Ref support | Hub | Verdict |",
             "|---|---|---|---|---|---|"]
    for r in rows[:top]:
        lines.append(f"| {_md_cell(r['label'] or r.get('id'))} | {r['community']} | {r['degree']} | "
                     f"{r['support']} | {'yes' if r['is_hub'] else ''} | {r['verdict']} |")
    lines += ["", "## Per-chapter gaps", "",
              "Concepts the literature emphasizes that each chapter under-covers or omits. "
              "Some entries here fall below the top-200 shown in the table above.", ""]
    gaps = [r for r in rows if r["verdict"] in ("under-covered", "absent")]
    by_ch: dict[str, list] = {}
    for r in gaps:
        by_ch.setdefault(r["chapter"], []).append(r)
    for ch in sorted(by_ch, key=lambda c: (c == "Unassigned", c)):
        lines.append(f"### {ch}")
        for r in sorted(by_ch[ch], key=lambda r: -r["score"])[:30]:
            lines.append(f"- **{_md_cell(r['label'] or r.get('id'))}** — {r['verdict']} "
                         f"(support {r['support']}, degree {r['degree']})")
        lines.append("")
    return "\n".join(lines)


def cmd_concepts() -> int:
    if not MASTER_GRAPH.exists():
        print(f"master graph not found at {MASTER_GRAPH} — run merge first")
        return 1
    graph = _load(MASTER_GRAPH)
    scored = score_concepts(graph)
    rows = coverage_diff(graph, scored)
    (MASTER_DIR / "CONCEPTS_FOR_BOOK.md").write_text(render_concepts_md(rows), encoding="utf-8")
    n_absent = sum(1 for r in rows if r["verdict"] == "absent")
    n_under = sum(1 for r in rows if r["verdict"] == "under-covered")
    print(f"wrote {MASTER_DIR / 'CONCEPTS_FOR_BOOK.md'}: {len(rows)} concepts, "
          f"{n_under} under-covered, {n_absent} absent")
    return 0


def top_hub_nodes(graph: dict, n: int = 100) -> list[dict]:
    """The n highest-degree concept nodes, for the LLM synonym pass."""
    deg = degree_map(graph)
    concepts = [x for x in graph["nodes"] if is_concept(x)]
    return sorted(concepts, key=lambda x: (-deg.get(x["id"], 0), x["id"]))[:n]


def cmd_consolidate() -> int:
    """Apply .work/aliases.json (deterministic + any appended hub-LLM aliases),
    re-cluster, and rebuild master-graph/."""
    import sys
    sys.path.insert(0, str(REPO / "scripts"))
    from deepen_pdfs import consolidate_nodes
    from networkx.readwrite import json_graph

    graph = _load(MASTER_GRAPH)
    alias = _load(WORK / "aliases.json") if (WORK / "aliases.json").exists() else {}
    validate_alias_map(alias, graph)
    before = (len(graph["nodes"]), len(graph["links"]))
    consolidate_nodes(graph, alias)
    G = json_graph.node_link_graph(graph, edges="links")
    stats = _export(G, None, None, len(INPUTS))
    _dump_communities()
    print(f"consolidated {len(alias)} aliases: nodes {before[0]}->{stats['nodes']}, "
          f"edges {before[1]}->{stats['edges']}, communities {stats['communities']}")
    return 0


def cmd_relabel() -> int:
    """Regenerate report/html/obsidian from .work/labels.json, reusing the existing
    per-node community partition (no re-cluster, graph.json untouched)."""
    import sys
    sys.path.insert(0, str(REPO / "scripts"))
    from deepen_pdfs import _communities_from_graph
    from networkx.readwrite import json_graph
    labels_path = WORK / "labels.json"
    if not labels_path.exists():
        print(f"no {labels_path}")
        return 1
    labels = {int(k): v for k, v in _load(labels_path).items()}
    graph = _load(MASTER_GRAPH)
    communities = _communities_from_graph(graph)
    if not communities:
        print("no community assignments in graph.json; run merge/consolidate first")
        return 1
    G = json_graph.node_link_graph(graph, edges="links")
    _export_reports_only(G, communities, labels, len(INPUTS))
    print(f"relabeled {len(labels)} of {len(communities)} communities")
    return 0


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("merge", "consolidate", "relabel", "concepts"):
        sub.add_parser(name)
    args = ap.parse_args()
    dispatch = {"merge": cmd_merge, "consolidate": cmd_consolidate,
                "relabel": cmd_relabel, "concepts": cmd_concepts}
    return dispatch[args.cmd]()


if __name__ == "__main__":
    import sys
    sys.exit(main())
