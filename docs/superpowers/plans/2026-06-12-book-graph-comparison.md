# Second (Book) Knowledge Graph + Comparison + Reference Augmentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an independent knowledge graph from the book manuscript alone (14 chapters) into `book-graph/`, compare it to graph 1 (`graphify-out/`), then augment it with the 63 already-pulled references (reusing graph 1's mined reference nodes).

**Architecture:** Split `proving-nothing.md` by chapter → one extraction subagent per chapter → graphify `build_from_json`/cluster/export into `book-graph/`. A pure comparison module diffs the two graphs. Augmentation reuses graph 1's `references/`-sourced subgraph (no re-extraction; scrapling re-runs only to confirm the corpus). All graphify/networkx imports are lazy so helper modules import cleanly under the venv.

**Tech Stack:** Python 3.14. venv `C:\sevenlayer\.venv\Scripts\python.exe` (pytest) runs tests; system `python` (graphify + networkx, from `git+https://github.com/safishamsi/graphify.git`) runs the build/export. The Agent tool does extraction.

**Spec:** `docs/superpowers/specs/2026-06-12-book-graph-comparison-design.md`

**Conventions for all tasks:**
- Working directory `C:\sevenlayer`. Run tests with the venv python; run builds with system `python`.
- graph.json is networkx node-link format: keys `nodes` + `links`. Extraction fragments use `{"nodes":[...],"edges":[...]}`; `edges` map onto `links`.
- Commit after every code task as `Charles Hoskinson <Charles.Hoskinson@gmail.com>` (already repo-local). No `Co-Authored-By` trailer.
- Reuse `scripts/deepen_pdfs.py:merge_fragment` (additive union/dedup/drop-dangling) for the reference merge.

---

### Task 1: Manuscript chapter splitter (TDD)

**Files:**
- Create: `scripts/split_manuscript.py`
- Create: `tests/test_book_graph.py`
- Modify: `.gitignore`

- [ ] **Step 1: Ignore the book-graph scratch dir**

Append to `.gitignore`:

```
# Book-graph scratch (chapter splits, fragments, jobs)
book-graph/.work/
```

- [ ] **Step 2: Write the failing test**

Create `tests/test_book_graph.py`:

```python
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from split_manuscript import split_chapters

SAMPLE = """# Glossary of Key Terms {.unnumbered}

glossary body

# Part I: The Invitation {.unnumbered}

# Chapter 1: The Promise

intro text
more

# Chapter 2: Layer 1 -- Building the Stage

stage text

# Part II: The Craft {.unnumbered}

# Chapter 3: Choreographing the Act

act text

# Complete Bibliography {.unnumbered}

bib body
"""


def test_split_chapters_extracts_only_chapters():
    chs = split_chapters(SAMPLE)
    assert [slug for slug, _ in chs] == ["ch01", "ch02", "ch03"]


def test_split_chapter_body_spans_to_next_top_heading():
    chs = dict(split_chapters(SAMPLE))
    assert chs["ch01"].startswith("# Chapter 1: The Promise")
    assert "intro text" in chs["ch01"] and "more" in chs["ch01"]
    assert "stage text" not in chs["ch01"]          # stops before ch2
    assert "glossary body" not in chs["ch01"]        # glossary excluded


def test_split_excludes_glossary_parts_bibliography():
    bodies = "\n".join(b for _, b in split_chapters(SAMPLE))
    assert "glossary body" not in bodies
    assert "bib body" not in bodies
    assert "Part I" not in bodies and "Part II" not in bodies
```

- [ ] **Step 3: Run test to verify it fails**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/test_book_graph.py -v`
Expected: FAIL (`ModuleNotFoundError: split_manuscript`).

- [ ] **Step 4: Write the splitter**

Create `scripts/split_manuscript.py`:

```python
"""Split proving-nothing.md into its 14 chapter files for graph extraction.

Usage (from repo root):
    python scripts/split_manuscript.py
Writes book-graph/.work/ch01.md ... ch14.md
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANUSCRIPT = REPO / "proving-nothing.md"
WORK = REPO / "book-graph" / ".work"

_CHAPTER_RE = re.compile(r"^# Chapter (\d+):", re.MULTILINE)
_TOP_HEADING_RE = re.compile(r"^# ", re.MULTILINE)


def split_chapters(text: str) -> list[tuple[str, str]]:
    """Return [(slug, body), ...] for each '# Chapter N:' heading. A chapter
    spans from its heading to the next top-level '# ' heading (exclusive), so
    Part separators, the Glossary, and the Bibliography bound chapters without
    being emitted."""
    # Offsets of every top-level heading (chapter, part, glossary, bibliography).
    tops = [m.start() for m in _TOP_HEADING_RE.finditer(text)]
    out = []
    for m in _CHAPTER_RE.finditer(text):
        start = m.start()
        nxt = next((t for t in tops if t > start), len(text))
        num = int(m.group(1))
        out.append((f"ch{num:02d}", text[start:nxt].strip()))
    return out


def main() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    WORK.mkdir(parents=True, exist_ok=True)
    chapters = split_chapters(text)
    for slug, body in chapters:
        (WORK / f"{slug}.md").write_text(body + "\n", encoding="utf-8")
    print(f"wrote {len(chapters)} chapter files to {WORK}")
    for slug, body in chapters:
        first = body.splitlines()[0]
        print(f"  {slug}.md  {len(body):>6} chars  {first[:60]}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run test to verify it passes**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/test_book_graph.py -v`
Expected: 3 passed.

- [ ] **Step 6: Split the real manuscript and eyeball**

Run: `python scripts/split_manuscript.py`
Expected: `wrote 14 chapter files`, each line showing the chapter title (Chapter 1..14), no Glossary/Bibliography. Confirm `git status --short` does NOT show `book-graph/.work/`.

- [ ] **Step 7: Commit**

```bash
git add scripts/split_manuscript.py tests/test_book_graph.py .gitignore
git commit -m "Add manuscript chapter splitter for the book graph"
```

---

### Task 2: Book-graph pure helpers (TDD)

**Files:**
- Create: `scripts/build_book_graph.py`
- Modify: `tests/test_book_graph.py` (append)

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_book_graph.py`:

```python
import pytest
from build_book_graph import merge_extraction, reference_subgraph


def test_merge_extraction_unions_and_dedups():
    frags = [
        {"nodes": [{"id": "concept_iop", "label": "IOP"}],
         "edges": [{"source": "ch01_x", "target": "concept_iop", "relation": "defines"}]},
        {"nodes": [{"id": "concept_iop", "label": "IOP dup"},
                   {"id": "ch01_x", "label": "X"}],
         "edges": [{"source": "ch01_x", "target": "concept_iop", "relation": "defines"},  # dup
                   {"source": "ch01_x", "target": "ghost", "relation": "cites"}]},          # dangling
    ]
    out = merge_extraction(frags)
    assert sorted(n["id"] for n in out["nodes"]) == ["ch01_x", "concept_iop"]
    assert out["nodes"][0]["label"] == "IOP"        # first wins
    assert len(out["edges"]) == 1                   # dup + dangling dropped
    assert out["input_tokens"] == 0 and out["output_tokens"] == 0


def test_reference_subgraph_selects_only_reference_nodes():
    g1 = {
        "nodes": [
            {"id": "ref-06_groth16", "label": "Groth16", "source_file": "references/ch02/ref-06-groth16.pdf"},
            {"id": "concept_pairing", "label": "Pairing", "source_file": "references/ch02/ref-06-groth16.pdf"},
            {"id": "wiki_x", "label": "X", "source_file": "wiki/chapters/02.md"},
            {"id": "manu_y", "label": "Y", "source_file": "proving-nothing.md"},
        ],
        "links": [
            {"source": "ref-06_groth16", "target": "concept_pairing", "relation": "uses"},
            {"source": "wiki_x", "target": "concept_pairing", "relation": "references"},  # one end outside refs
            {"source": "wiki_x", "target": "manu_y", "relation": "x"},                     # both outside
        ],
    }
    sub = reference_subgraph(g1)
    assert sorted(n["id"] for n in sub["nodes"]) == ["concept_pairing", "ref-06_groth16"]
    # edges kept only if BOTH endpoints are reference nodes; mapped to 'edges'
    assert sub["edges"] == [
        {"source": "ref-06_groth16", "target": "concept_pairing", "relation": "uses"}
    ]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/test_book_graph.py -k "merge_extraction or reference_subgraph" -v`
Expected: FAIL (`ModuleNotFoundError: build_book_graph`).

- [ ] **Step 3: Write the pure helpers**

Create `scripts/build_book_graph.py`:

```python
"""Build the book knowledge graph from chapter fragments, and augment it with
graph 1's reference subgraph.

Usage (from repo root):
    python scripts/split_manuscript.py            # writes book-graph/.work/chNN.md
    # ... dispatch one subagent per chapter -> book-graph/.work/frag-chNN.json ...
    python scripts/build_book_graph.py build      # build book-graph/ from fragments
    python scripts/build_book_graph.py augment    # merge graph 1's references, rebuild

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
    """From a node-link graph, return {"nodes", "edges"} containing only nodes
    whose source_file is under references/ and the edges induced on them."""
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/test_book_graph.py -v`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_book_graph.py tests/test_book_graph.py
git commit -m "Add book-graph merge/reference-subgraph pure helpers"
```

---

### Task 3: Book-graph build + augment CLI

**Files:**
- Modify: `scripts/build_book_graph.py` (append build/export/CLI)

- [ ] **Step 1: Append the build, export, and CLI to `scripts/build_book_graph.py`**

```python
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
    # dump communities for labeling
    g = _load(BOOK_GRAPH)
    comms = {}
    for n in g["nodes"]:
        comms.setdefault(str(n.get("community")), []).append(n.get("label", n["id"]))
    (WORK / "communities.json").write_text(json.dumps(comms, indent=2, ensure_ascii=False), encoding="utf-8")
    _write_cost(extraction)
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
    after = (stats["nodes"], stats["edges"])
    g = _load(BOOK_GRAPH)
    comms = {}
    for n in g["nodes"]:
        comms.setdefault(str(n.get("community")), []).append(n.get("label", n["id"]))
    (WORK / "communities.json").write_text(json.dumps(comms, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"augmented with {len(refsg['nodes'])} reference nodes: "
          f"nodes {before[0]}->{after[0]}, edges {before[1]}->{after[1]}, communities {stats['communities']}")
    return 0


def relabel(labels: dict) -> int:
    """Regenerate book-graph report/html/obsidian with community names, reusing
    the existing clustering from the per-node 'community' field (no re-cluster)."""
    from networkx.readwrite import json_graph
    book = _load(BOOK_GRAPH)
    communities = {}
    for n in book["nodes"]:
        c = n.get("community")
        if c is not None:
            communities.setdefault(int(c), []).append(n["id"])
    G = json_graph.node_link_graph(book, edges="links")
    _export_with_communities(G, communities, {int(k): v for k, v in labels.items()}, len(book["nodes"]))
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


def _write_cost(extraction: dict) -> None:
    import datetime
    cost_path = BOOK_DIR / "cost.json"
    cost = _load(cost_path) if cost_path.exists() else {"runs": [], "total_input_tokens": 0, "total_output_tokens": 0}
    cost["runs"].append({"date": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                         "input_tokens": 0, "output_tokens": 0, "note": "book-graph build (see session for measured subagent tokens)"})
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
```

- [ ] **Step 2: Confirm the module still imports and tests pass**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" -c "import sys; sys.path.insert(0,'scripts'); import build_book_graph; print('ok')"`
Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/ -q`
Expected: `ok`, then all tests pass (deepen + manifest + fetch + book-graph helpers).

- [ ] **Step 3: Verify graphify build_from_json is importable (system python)**

Run: `python -c "from graphify.build import build_from_json; print('build_from_json ok')"`
Expected: `build_from_json ok`. (If the import name differs, adjust the import in `cmd_build`.)

- [ ] **Step 4: Commit**

```bash
git add scripts/build_book_graph.py
git commit -m "Add book-graph build/augment/relabel pipeline"
```

---

### Task 4: Comparison module (TDD)

**Files:**
- Create: `scripts/compare_graphs.py`
- Modify: `tests/test_book_graph.py` (append)

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_book_graph.py`:

```python
from compare_graphs import normalize_label, label_set, compare


def test_normalize_label_canonicalizes():
    assert normalize_label("Folding Schemes") == normalize_label("Folding Scheme")
    assert normalize_label("STARK (Scalable...)") == "stark"
    assert normalize_label("Zero-Knowledge Proofs") == normalize_label("zero knowledge proof")


def test_label_set_and_compare():
    g_book = {"nodes": [{"label": "Folding Schemes"}, {"label": "PLONK"}], "links": []}
    g1 = {"nodes": [{"label": "Folding Scheme"}, {"label": "KZG Commitments"}], "links": []}
    assert label_set(g_book) == {"folding scheme", "plonk"}
    cmp = compare(g_book, g1)
    assert "plonk" in cmp["book_only"]
    assert "kzg commitment" in cmp["graph1_only"]
    assert "folding scheme" in cmp["shared"]
    assert 0.0 < cmp["jaccard"] < 1.0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/test_book_graph.py -k "normalize_label or label_set" -v`
Expected: FAIL (`ModuleNotFoundError: compare_graphs`).

- [ ] **Step 3: Write the comparison module**

Create `scripts/compare_graphs.py`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/test_book_graph.py -v`
Expected: all book-graph tests pass (7 total).

- [ ] **Step 5: Commit**

```bash
git add scripts/compare_graphs.py tests/test_book_graph.py
git commit -m "Add book-vs-graph1 comparison module"
```

---

### Task 5: Build the book graph (extraction + build + label)

**Files:**
- Create (runtime, git-ignored): `book-graph/.work/chNN.md`, `frag-chNN.json`, `communities.json`
- Create: `book-graph/graph.json`, `GRAPH_REPORT.md`, `graph.html`, `obsidian/`, `cost.json`

- [ ] **Step 1: Split the manuscript**

Run: `python scripts/split_manuscript.py`
Expected: 14 chapter files in `book-graph/.work/`.

- [ ] **Step 2: Dispatch one extraction subagent per chapter (Agent tool)**

For each `book-graph/.work/chNN.md` (NN = 01..14), dispatch a subagent with this exact prompt (substitute `NN`, `TITLE`, the absolute path):

```
You are a graphify extraction subagent for ONE chapter of a book on zero-knowledge proofs.

Read the chapter file at: C:\sevenlayer\book-graph\.work\chNN.md  (use the Read tool).
This is Chapter NN ("TITLE") of "Proving Nothing".

Extract a knowledge-graph fragment of what THIS chapter covers: the named concepts,
schemes, systems, people, curves, and the claims/arguments the chapter makes, plus
any works it cites. Aim for 15-30 nodes.

Node id rules:
- General/shared concepts (likely shared with other chapters and with the reference
  graph): id = "concept_<kebab-name>" using PRECISE, standard names (e.g.
  "concept_kzg-commitment", "concept_fiat-shamir", "concept_folding-scheme",
  "concept_plonk") so they merge across chapters and align with the existing graph.
- Artifacts specific to THIS chapter (a narrative section, a worked example, the
  chapter's framing/metaphor): id = "ch<NN>_<kebab-name>".
- Every node MUST set "source_file": "proving-nothing.md", "source_location":
  "Chapter NN", "file_type": "document".

Edge rules:
- Link every node to another emitted node (or a shared concept). relation in
  {defines, introduces, explains, references, conceptually_related_to, cites,
  compares}. confidence in {EXTRACTED, INFERRED, AMBIGUOUS}.

Output ONLY this JSON (no prose, no fences) and WRITE it to
C:\sevenlayer\book-graph\.work\frag-chNN.json using the Write tool:
{"nodes":[{"id":"...","label":"Human Readable","file_type":"document","source_file":"proving-nothing.md","source_location":"Chapter NN","source_url":null,"captured_at":null,"author":null,"contributor":null}],"edges":[{"source":"...","target":"...","relation":"...","confidence":"EXTRACTED","source_file":"proving-nothing.md","source_location":"Chapter NN","weight":1.0}]}

Final reply: node count, edge count, frag path.
```

Dispatch in batches (e.g. 5 at a time). The chapter titles are: 1 The Promise of Provable and Programmable Secrets; 2 Layer 1 -- Building the Stage; 3 Choreographing the Act; 4 The Secret Performance; 5 Encoding the Performance; 6 Layer 5 -- The Sealed Certificate; 7 Layer 6 -- The Deep Craft; 8 Layer 7 -- The Verdict; 9 Privacy-Enhancing Technologies; 10 The Synthesis -- Three Paths, Not Two; 11 zkVMs -- The Universal Stage; 12 Midnight -- The Privacy Theater; 13 The Market Landscape; 14 Open Questions and the Road Ahead.

- [ ] **Step 3: Validate the fragments**

```bash
python - <<'EOF'
import json, glob, pathlib
n=e=0
for f in sorted(glob.glob("book-graph/.work/frag-ch*.json")):
    d=json.loads(pathlib.Path(f).read_text(encoding="utf-8"))
    assert isinstance(d.get("nodes"),list) and isinstance(d.get("edges"),list), f
    print(pathlib.Path(f).name, len(d["nodes"]), "nodes", len(d["edges"]), "edges")
    n+=len(d["nodes"]); e+=len(d["edges"])
print("total", n, "nodes", e, "edges across", len(glob.glob("book-graph/.work/frag-ch*.json")), "chapters")
EOF
```
Expected: 14 fragments, each ~15-30 nodes. Re-dispatch any missing/tiny (<8 nodes) chapter.

- [ ] **Step 4: Build the book graph (system python)**

Run: `python scripts/build_book_graph.py build`
Expected: `built book-graph: N nodes, M edges, K communities` (N roughly 200-350 after dedup), and `book-graph/.work/communities.json` written.

- [ ] **Step 5: Label communities**

Read `book-graph/.work/communities.json`; for each community id write a 2-5 word name based on its members. Write `book-graph/.work/labels.json` (`{"0":"Name", ...}`), then:
Run: `python scripts/build_book_graph.py relabel`
Expected: report/html/obsidian regenerated with names.

- [ ] **Step 6: Commit the book graph**

```bash
git add book-graph/graph.json book-graph/GRAPH_REPORT.md book-graph/graph.html book-graph/obsidian book-graph/cost.json
git add -f book-graph/.work/labels.json
git commit -m "Build book knowledge graph from 14 chapters (graph 2)"
```

---

### Task 6: Compare book graph to graph 1

**Files:**
- Create: `book-graph/COMPARISON.md`

- [ ] **Step 1: Run the comparison**

Run: `python scripts/compare_graphs.py`
Expected: prints node counts for both, concept Jaccard, and shared/book-only/graph1-only counts; writes `book-graph/COMPARISON.md`.

- [ ] **Step 2: Sanity-check the report**

Open `book-graph/COMPARISON.md`. Confirm: graph 1 has many more nodes; the "what graph 1 knows that the book's text alone does not" list is populated with reference/implementation concepts (e.g. specific theorems, lattice/PQC internals, tool names) that the prose book doesn't name; the book-only list is small (book framing/metaphor nodes). If the book-only list is huge, vocabulary drifted — note it (the labels still compare on normalized text, so this is informational).

- [ ] **Step 3: Commit**

```bash
git add book-graph/COMPARISON.md
git commit -m "Add book-graph vs graph-1 comparison report"
```

---

### Task 7: Augment the book graph with the references

**Files:**
- Modify: `book-graph/graph.json`, `GRAPH_REPORT.md`, `graph.html`, `obsidian/`, `COMPARISON.md`

- [ ] **Step 1: Confirm the reference corpus with scrapling (idempotent)**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" scripts/fetch_references.py`
Expected: `63/63 resolved; unresolved: none`, exit 0, `git status --porcelain references/` empty (no re-downloads).

- [ ] **Step 2: Back up the book graph, then augment (system python)**

```bash
cp book-graph/graph.json "$TEMP/book-graph.json.bak"
python scripts/build_book_graph.py augment
```
Expected: `augmented with <~900> reference nodes: nodes A->B, edges C->D, communities K`. B should be roughly book-nodes + graph-1 reference-nodes.

- [ ] **Step 3: Verify additive integrity**

```bash
python - <<'EOF'
import json, os
new=json.load(open("book-graph/graph.json",encoding="utf-8"))
old=json.load(open(os.path.join(os.environ["TEMP"],"book-graph.json.bak"),encoding="utf-8"))
oldids={n["id"] for n in old["nodes"]}
assert oldids <= {n["id"] for n in new["nodes"]}, "book nodes lost in augment"
print("ok: book nodes preserved;", len(old["nodes"]), "->", len(new["nodes"]))
EOF
```
Expected: `ok:` with node count increased.

- [ ] **Step 4: Relabel the augmented communities**

Read the refreshed `book-graph/.work/communities.json`, write updated `book-graph/.work/labels.json`, then:
Run: `python scripts/build_book_graph.py relabel`
Expected: report/html/obsidian regenerated.

- [ ] **Step 5: Re-run the comparison on the augmented graph**

Run: `python scripts/compare_graphs.py`
Expected: Jaccard with graph 1 is now much higher than in Task 6 (the book graph now contains the reference knowledge); `COMPARISON.md` updated. The remaining graph-1-only set is mostly wiki-layer concepts.

- [ ] **Step 6: Verify tests and commit**

```bash
& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/ -q
git add book-graph/graph.json book-graph/GRAPH_REPORT.md book-graph/graph.html book-graph/obsidian book-graph/COMPARISON.md
git add -f book-graph/.work/labels.json
git commit -m "Augment book graph with reference subgraph; refresh comparison"
rm -f "$TEMP/book-graph.json.bak"
```
Expected: all tests pass; tree clean.

- [ ] **Step 7: Final report to the user**

Summarize: book-graph node/edge/community counts (book-only and after augmentation), the headline comparison numbers (Jaccard before/after, what graph 1 knew that the book text didn't), and total measured extraction cost. Note `book-graph/` and `book-graph/COMPARISON.md` as deliverables. Offer to push.
