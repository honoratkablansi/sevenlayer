"""Compare the book graph (book-graph/graph.json) to graph 1 (graphify-out/graph.json).

Usage (from repo root):
    python scripts/compare_graphs.py            # writes book-graph/COMPARISON.md
"""
from __future__ import annotations

import collections
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BOOK = REPO / "book-graph" / "graph.json"
GRAPH1 = REPO / "graphify-out" / "graph.json"
OUT = REPO / "book-graph" / "COMPARISON.md"


def normalize_label(s: str) -> str:
    s = (s or "").lower().strip()
    s = re.sub(r"\s*\(.*?\)\s*", " ", s)          # drop parentheticals
    s = re.sub(r"[^a-z0-9]+", " ", s).strip()
    return " ".join(w[:-1] if (w.endswith("s") and len(w) > 3) else w for w in s.split())


def label_set(graph: dict) -> set[str]:
    return {normalize_label(n.get("label", "")) for n in graph["nodes"] if n.get("label")}


def _counts(graph: dict) -> dict:
    comms = {n.get("community") for n in graph["nodes"] if n.get("community") is not None}
    return {"nodes": len(graph["nodes"]), "edges": len(graph.get("links", [])), "communities": len(comms)}


def _god_nodes(graph: dict, top_n: int = 10) -> list[tuple[str, int]]:
    deg = collections.Counter()
    for l in graph.get("links", []):
        deg[l["source"]] += 1
        deg[l["target"]] += 1
    label = {n["id"]: n.get("label", n["id"]) for n in graph["nodes"]}
    return [(label.get(nid, nid), d) for nid, d in deg.most_common(top_n)]


def compare(g_book: dict, g1: dict) -> dict:
    b, o = label_set(g_book), label_set(g1)
    inter, union = b & o, b | o
    return {
        "book_counts": _counts(g_book),
        "graph1_counts": _counts(g1),
        "shared": sorted(inter),
        "book_only": sorted(b - o),
        "graph1_only": sorted(o - b),
        "jaccard": (len(inter) / len(union)) if union else 0.0,
    }


def write_report(cmp: dict, g_book: dict, g1: dict, out: Path) -> None:
    bc, gc = cmp["book_counts"], cmp["graph1_counts"]
    lines = [
        "# Book Graph vs Graph 1 — Comparison", "",
        "| Metric | Book graph | Graph 1 |", "|---|---|---|",
        f"| Nodes | {bc['nodes']} | {gc['nodes']} |",
        f"| Edges | {bc['edges']} | {gc['edges']} |",
        f"| Communities | {bc['communities']} | {gc['communities']} |",
        f"| Distinct concept labels | {len(label_set(g_book))} | {len(label_set(g1))} |",
        "", f"**Concept-label Jaccard similarity:** {cmp['jaccard']:.3f}",
        f"({len(cmp['shared'])} shared, {len(cmp['book_only'])} book-only, {len(cmp['graph1_only'])} graph-1-only)", "",
        "## God nodes — Book graph", "",
        *[f"{i+1}. {lab} — {d} edges" for i, (lab, d) in enumerate(_god_nodes(g_book))],
        "", "## God nodes — Graph 1", "",
        *[f"{i+1}. {lab} — {d} edges" for i, (lab, d) in enumerate(_god_nodes(g1))],
        "", "## What graph 1 knows that the book's text alone does not",
        "_(concepts present in graph 1 — from references + wiki + deep-mining — absent from the book-only graph)_", "",
        *[f"- {c}" for c in cmp["graph1_only"][:120]],
        "", "## Concepts in the book graph but not in graph 1", "",
        *[f"- {c}" for c in cmp["book_only"][:120]],
        "",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    g_book = json.loads(BOOK.read_text(encoding="utf-8"))
    g1 = json.loads(GRAPH1.read_text(encoding="utf-8"))
    cmp = compare(g_book, g1)
    write_report(cmp, g_book, g1, OUT)
    print(f"nodes book={cmp['book_counts']['nodes']} graph1={cmp['graph1_counts']['nodes']}")
    print(f"concept jaccard={cmp['jaccard']:.3f}; shared={len(cmp['shared'])}, "
          f"book_only={len(cmp['book_only'])}, graph1_only={len(cmp['graph1_only'])}")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
