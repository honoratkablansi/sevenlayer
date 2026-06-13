# Master Knowledge Graph Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Merge the three existing knowledge graphs into one `master-graph/`, grow it by snowballing citations out of the reference papers (bounded), and emit a ranked, per-chapter "concepts that should be in the book" report.

**Architecture:** A new `scripts/build_master_graph.py` module. Pure helpers (graph union with origin-tracking, deterministic alias dedup, citation parse/filter/dedup, concept scoring, coverage diff) are TDD-tested in `tests/test_master_graph.py`. graphify/networkx calls stay behind a lazy-import `_export` that writes to `master-graph/`. It reuses the existing path-agnostic helpers `deepen_pdfs.consolidate_nodes`, `deepen_pdfs.merge_fragment`, `deepen_pdfs.load_fragment`, and `fetch_references.py`. Subagent passes (LLM relevance judge, per-PDF concept+citation extraction) are orchestration runbook steps, not unit tests.

**Tech Stack:** Python 3.10+, pytest, the installed `graphify` package + `networkx` (system Python for builds; venv for tests since graphify imports are lazy), `scrapling` (already used by `fetch_references.py`).

**Conventions for every commit step:** run from `C:\sevenlayer`. Do **not** add a `Co-Authored-By` trailer. Tests run with the venv's Python: `python -m pytest ...`.

---

## Phase 0 — Scaffold

### Task 0: Module + test skeleton, gitignore, master-graph dir

**Files:**
- Create: `scripts/build_master_graph.py`
- Create: `tests/test_master_graph.py`
- Modify: `.gitignore`

- [ ] **Step 1: Create the module skeleton**

Create `scripts/build_master_graph.py`:

```python
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
```

- [ ] **Step 2: Create the test file skeleton**

Create `tests/test_master_graph.py`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_master_graph as m  # noqa: E402


def _g(nodes, links):
    """Minimal node-link graph dict for tests."""
    return {"directed": True, "multigraph": False, "graph": {},
            "nodes": nodes, "links": links}
```

- [ ] **Step 3: Add master-graph work dirs to .gitignore**

Append to `.gitignore`:

```
# master-graph build scratch (curated files force-added)
master-graph/.work/
master-graph/.snowball/
```

- [ ] **Step 4: Verify the module imports under the venv**

Run: `python -m pytest tests/test_master_graph.py -q`
Expected: `no tests ran` (collection succeeds, 0 tests) — confirms the import works.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_master_graph.py tests/test_master_graph.py .gitignore
git commit -m "Scaffold master-graph module + test skeleton"
```

---

## Phase 1 — Stage 1: Merge the three graphs

### Task 1: `merge_graphs` — union by id with origin tracking

**Files:**
- Modify: `scripts/build_master_graph.py`
- Test: `tests/test_master_graph.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/test_master_graph.py`:

```python
def test_merge_graphs_unions_nodes_and_tracks_origin():
    a = _g([{"id": "concept_x", "label": "X"}],
           [{"source": "concept_x", "target": "concept_x", "relation": "self"}])
    b = _g([{"id": "concept_x", "label": "X"}, {"id": "concept_y", "label": "Y"}],
           [{"source": "concept_x", "target": "concept_y", "relation": "rel"}])
    out = m.merge_graphs([("book", a), ("recursion", b)])
    ids = {n["id"]: n for n in out["nodes"]}
    assert set(ids) == {"concept_x", "concept_y"}
    assert ids["concept_x"]["origin_graphs"] == ["book", "recursion"]
    assert ids["concept_y"]["origin_graphs"] == ["recursion"]
    # self-loop edge kept once; cross edge kept; no dangling
    assert {(l["source"], l["target"]) for l in out["links"]} == \
        {("concept_x", "concept_x"), ("concept_x", "concept_y")}


def test_merge_graphs_drops_dangling_edges():
    a = _g([{"id": "n1", "label": "1"}],
           [{"source": "n1", "target": "ghost", "relation": "r"}])
    out = m.merge_graphs([("book", a)])
    assert out["links"] == []
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_master_graph.py -k merge_graphs -v`
Expected: FAIL — `AttributeError: module 'build_master_graph' has no attribute 'merge_graphs'`

- [ ] **Step 3: Implement `merge_graphs`**

Add to `scripts/build_master_graph.py`:

```python
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
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest tests/test_master_graph.py -k merge_graphs -v`
Expected: PASS (2 tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/build_master_graph.py tests/test_master_graph.py
git commit -m "master-graph: merge_graphs union with origin tracking"
```

---

### Task 2: `normalize_label` + `degree_map`

**Files:**
- Modify: `scripts/build_master_graph.py`
- Test: `tests/test_master_graph.py`

- [ ] **Step 1: Write the failing test**

```python
def test_normalize_label_depluralizes_and_strips_punctuation():
    assert m.normalize_label("KZG Polynomial Commitments") == "kzg polynomial commitment"
    assert m.normalize_label("Bulletproofs") == "bulletproof"
    assert m.normalize_label("Knowledge Soundness") == "knowledge soundness"  # ss preserved
    assert m.normalize_label("STARK") == "stark"
    assert m.normalize_label("  Folding   Scheme!! ") == "folding scheme"


def test_degree_map_counts_incidence():
    g = _g([{"id": "a"}, {"id": "b"}, {"id": "c"}],
           [{"source": "a", "target": "b"}, {"source": "a", "target": "c"}])
    assert m.degree_map(g) == {"a": 2, "b": 1, "c": 1}
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_master_graph.py -k "normalize_label or degree_map" -v`
Expected: FAIL — attributes not defined.

- [ ] **Step 3: Implement**

Add to `scripts/build_master_graph.py`:

```python
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
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest tests/test_master_graph.py -k "normalize_label or degree_map" -v`
Expected: PASS (2 tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/build_master_graph.py tests/test_master_graph.py
git commit -m "master-graph: normalize_label + degree_map helpers"
```

---

### Task 3: `build_alias_map` + `validate_alias_map`

**Files:**
- Modify: `scripts/build_master_graph.py`
- Test: `tests/test_master_graph.py`

- [ ] **Step 1: Write the failing test**

```python
import pytest  # add at top of file if not present


def test_build_alias_map_collapses_variants_to_highest_degree():
    g = _g(
        [{"id": "concept_kzg-commitment", "label": "KZG Commitment"},
         {"id": "concept_kzg-commitments", "label": "KZG Commitments"},
         {"id": "concept_stark", "label": "STARK"}],
        [{"source": "concept_kzg-commitment", "target": "concept_stark"},
         {"source": "concept_kzg-commitment", "target": "concept_kzg-commitments"}],
    )
    # concept_kzg-commitment has degree 2, concept_kzg-commitments degree 1
    alias = m.build_alias_map(g)
    assert alias == {"concept_kzg-commitments": "concept_kzg-commitment"}


def test_validate_alias_map_rejects_chain():
    g = _g([{"id": "a"}, {"id": "b"}, {"id": "c"}], [])
    with pytest.raises(ValueError):
        m.validate_alias_map({"a": "b", "b": "c"}, g)


def test_validate_alias_map_rejects_unknown_id():
    g = _g([{"id": "a"}], [])
    with pytest.raises(ValueError):
        m.validate_alias_map({"a": "missing"}, g)
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_master_graph.py -k alias_map -v`
Expected: FAIL — attributes not defined.

- [ ] **Step 3: Implement**

Add to `scripts/build_master_graph.py`:

```python
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
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest tests/test_master_graph.py -k alias_map -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/build_master_graph.py tests/test_master_graph.py
git commit -m "master-graph: build_alias_map + validate_alias_map"
```

---

### Task 4: `_export` + `cmd_merge` (lazy graphify, writes master-graph/)

**Files:**
- Modify: `scripts/build_master_graph.py`

- [ ] **Step 1: Implement `_export` (mirrors build_book_graph._export, MASTER_DIR paths)**

Add to `scripts/build_master_graph.py`:

```python
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


def _dump_communities() -> None:
    g = _load(MASTER_GRAPH)
    comms: dict[str, list] = {}
    for n in g["nodes"]:
        comms.setdefault(str(n.get("community")), []).append(n.get("label", n["id"]))
    _dump(WORK / "communities.json", comms)
```

- [ ] **Step 2: Implement `cmd_merge`**

```python
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
```

- [ ] **Step 3: Run the real merge (system Python with graphify)**

Run: `python scripts/build_master_graph.py merge`
Expected: prints a node/edge/community count (nodes well under the 1513+1200+1467 raw sum, because `concept_*` ids collapse on union); creates `master-graph/graph.json`, `GRAPH_REPORT.md`, `graph.html`, `obsidian/`, `.work/aliases.json`, `.work/communities.json`.

- [ ] **Step 4: Sanity-check the output**

Run: `python -c "import json; g=json.load(open('master-graph/graph.json',encoding='utf-8')); print(len(g['nodes']),'nodes',len(g['links']),'links'); print('origin sample:', g['nodes'][0].get('origin_graphs'))"`
Expected: node/link counts print; `origin_graphs` is a non-empty list.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_master_graph.py master-graph/graph.json master-graph/GRAPH_REPORT.md master-graph/graph.html master-graph/obsidian
git commit -m "master-graph: build merged graph from 3 inputs (Stage 1)"
```

---

### Task 5: Hub LLM synonym pass + `cmd_consolidate` + `cmd_relabel`

**Files:**
- Modify: `scripts/build_master_graph.py`

- [ ] **Step 1: Implement `top_hub_nodes` and `cmd_consolidate` / `cmd_relabel`**

Add to `scripts/build_master_graph.py`:

```python
def top_hub_nodes(graph: dict, n: int = 100) -> list[dict]:
    """The n highest-degree concept nodes, for the LLM synonym pass."""
    deg = degree_map(graph)
    concepts = [x for x in graph["nodes"] if str(x.get("id", "")).startswith("concept_")]
    return sorted(concepts, key=lambda x: (-deg.get(x["id"], 0), x["id"]))[:n]


def cmd_consolidate() -> int:
    """Apply .work/aliases.json (deterministic + any appended hub-LLM aliases),
    re-cluster, and rebuild master-graph/."""
    import sys as _sys
    _sys.path.insert(0, str(REPO / "scripts"))
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
    per-node community field (no re-cluster)."""
    from networkx.readwrite import json_graph
    labels_path = WORK / "labels.json"
    if not labels_path.exists():
        print(f"no {labels_path}")
        return 1
    labels = {int(k): v for k, v in _load(labels_path).items()}
    graph = _load(MASTER_GRAPH)
    communities: dict[int, list] = {}
    for n in graph["nodes"]:
        c = n.get("community")
        if c is not None:
            communities.setdefault(int(c), []).append(n["id"])
    G = json_graph.node_link_graph(graph, edges="links")
    _export(G, communities, labels, len(INPUTS))
    _dump_communities()
    print(f"relabeled {len(communities)} communities")
    return 0
```

- [ ] **Step 2: Generate the hub list for the LLM pass**

Run: `python -c "import sys; sys.path.insert(0,'scripts'); import build_master_graph as m, json; g=m._load(m.MASTER_GRAPH); hubs=[{'id':n['id'],'label':n.get('label')} for n in m.top_hub_nodes(g,100)]; m._dump(m.WORK/'hubs.json', hubs); print(len(hubs),'hubs ->', m.WORK/'hubs.json')"`
Expected: writes `master-graph/.work/hubs.json` with 100 `{id,label}` rows.

- [ ] **Step 3: Dispatch ONE LLM synonym-judge subagent (Agent tool)**

Dispatch a subagent (Agent tool, `general-purpose`) with this prompt; it returns aliases to append:

> You are deduplicating concept nodes in a zero-knowledge-proof knowledge graph. Input is a JSON list of `{id,label}` hub nodes (read `master-graph/.work/hubs.json`). Find groups where two or more DIFFERENT-looking labels denote the **same** concept (e.g. "KZG Commitment" ≡ "Kate Commitment"; "IVC" ≡ "Incrementally Verifiable Computation"). Do NOT merge related-but-distinct concepts (e.g. "folding" vs "recursion" stay separate). For each group pick the most standard label's id as canonical. Output ONLY JSON: `{"aliases": {"<alias_id>": "<canonical_id>"}}`. Every id must appear in the input. Your final message is the JSON, nothing else.

- [ ] **Step 4: Append the judged aliases to the deterministic alias map**

After saving the subagent's `aliases` object to `master-graph/.work/hub-aliases.json`, merge it in:

Run: `python -c "import sys; sys.path.insert(0,'scripts'); import build_master_graph as m; det=m._load(m.WORK/'aliases.json'); hub=m._load(m.WORK/'hub-aliases.json').get('aliases',{}); det.update({a:c for a,c in hub.items() if a not in det.values()}); g=m._load(m.MASTER_GRAPH); m.validate_alias_map(det,g); m._dump(m.WORK/'aliases.json',det); print('alias map now',len(det))"`
Expected: prints the combined alias count; raises if the LLM proposed an invalid/cyclic merge (fix the bad pair in `hub-aliases.json` and rerun).

- [ ] **Step 5: Consolidate + rebuild, then commit**

Run: `python scripts/build_master_graph.py consolidate`
Expected: node count DECREASES by roughly the alias count; communities recomputed.

```bash
git add scripts/build_master_graph.py master-graph/graph.json master-graph/GRAPH_REPORT.md master-graph/graph.html master-graph/obsidian master-graph/.work/aliases.json master-graph/.work/hubs.json master-graph/.work/hub-aliases.json
git commit -m "master-graph: hub LLM synonym pass + consolidate/relabel (Stage 1 dedup)"
```

(`.work/` is gitignored; force-add the curated alias/hub files so the dedup is reproducible: `git add -f master-graph/.work/aliases.json master-graph/.work/hub-aliases.json master-graph/.work/hubs.json`.)

---

## Phase 2 — Stage 4: Concept extraction → CONCEPTS_FOR_BOOK.md

### Task 6: `reference_support` + `score_concepts`

**Files:**
- Modify: `scripts/build_master_graph.py`
- Test: `tests/test_master_graph.py`

- [ ] **Step 1: Write the failing test**

```python
def test_reference_support_counts_distinct_reference_neighbors():
    g = _g(
        [{"id": "concept_a", "label": "A", "source_file": "proving-nothing.md"},
         {"id": "r1", "label": "p1", "source_file": "references/ch1/ref-01.pdf"},
         {"id": "r2", "label": "p2", "source_file": "references/ch1/ref-02.pdf"},
         {"id": "r3", "label": "p3", "source_file": "references/ch1/ref-01.pdf"}],
        [{"source": "concept_a", "target": "r1"},
         {"source": "concept_a", "target": "r2"},
         {"source": "concept_a", "target": "r3"}],
    )
    # r1 and r3 share a source_file -> 2 distinct reference files
    assert m.reference_support(g)["concept_a"] == 2


def test_score_concepts_ranks_by_degree_plus_support():
    g = _g(
        [{"id": "concept_hi", "label": "Hi", "source_file": "proving-nothing.md"},
         {"id": "concept_lo", "label": "Lo", "source_file": "proving-nothing.md"},
         {"id": "r1", "label": "p", "source_file": "references/x.pdf"}],
        [{"source": "concept_hi", "target": "r1"},
         {"source": "concept_hi", "target": "concept_lo"}],
    )
    rows = m.score_concepts(g)
    assert [r["id"] for r in rows] == ["concept_hi", "concept_lo"]
    assert rows[0]["support"] == 1 and rows[0]["degree"] == 2
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_master_graph.py -k "reference_support or score_concepts" -v`
Expected: FAIL — attributes not defined.

- [ ] **Step 3: Implement**

```python
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
            f = sf.get(cand)
            if _is_reference(f):
                files.add(f.replace("\\", "/"))
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
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest tests/test_master_graph.py -k "reference_support or score_concepts" -v`
Expected: PASS (2 tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/build_master_graph.py tests/test_master_graph.py
git commit -m "master-graph: reference_support + score_concepts"
```

---

### Task 7: `coverage_diff` + `chapter_of`

**Files:**
- Modify: `scripts/build_master_graph.py`
- Test: `tests/test_master_graph.py`

- [ ] **Step 1: Write the failing test**

```python
def test_coverage_diff_tags_absent_under_and_well_covered():
    g = _g(
        [{"id": "concept_a", "label": "A", "source_file": "proving-nothing.md",
          "source_location": "Chapter 3"},
         {"id": "concept_b", "label": "B", "source_file": "references/x.pdf",
          "source_location": "Recursion Chapter 1"}],
        [],
    )
    scored = [
        {"id": "concept_a", "label": "A", "degree": 9, "support": 5, "community": 1, "is_hub": True, "score": 19},
        {"id": "concept_b", "label": "B", "degree": 3, "support": 1, "community": 2, "is_hub": False, "score": 5},
    ]
    out = {r["id"]: r for r in m.coverage_diff(g, scored, under_threshold=4)}
    assert out["concept_a"]["verdict"] == "under-covered"   # in manuscript, heavy support
    assert out["concept_b"]["verdict"] == "absent"          # refs-only


def test_chapter_of_reads_source_location():
    assert m.chapter_of({"source_location": "Chapter 7"}) == "Chapter 7"
    assert m.chapter_of({"source_location": "Recursion Chapter 2"}) == "Chapter 2"
    assert m.chapter_of({"source_location": None}) == "Unassigned"
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_master_graph.py -k "coverage_diff or chapter_of" -v`
Expected: FAIL — attributes not defined.

- [ ] **Step 3: Implement**

```python
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
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest tests/test_master_graph.py -k "coverage_diff or chapter_of" -v`
Expected: PASS (2 tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/build_master_graph.py tests/test_master_graph.py
git commit -m "master-graph: coverage_diff + chapter_of"
```

---

### Task 8: `render_concepts_md` + `cmd_concepts`

**Files:**
- Modify: `scripts/build_master_graph.py`
- Test: `tests/test_master_graph.py`

- [ ] **Step 1: Write the failing test**

```python
def test_render_concepts_md_has_table_and_rollup():
    rows = [
        {"label": "A", "community": 1, "degree": 9, "support": 5, "is_hub": True,
         "score": 19, "verdict": "under-covered", "chapter": "Chapter 3"},
        {"label": "B", "community": 2, "degree": 3, "support": 1, "is_hub": False,
         "score": 5, "verdict": "absent", "chapter": "Unassigned"},
    ]
    md = m.render_concepts_md(rows)
    assert "| Concept |" in md                 # ranked table header
    assert "under-covered" in md and "absent" in md
    assert "## Per-chapter gaps" in md          # rollup section
    assert "Chapter 3" in md
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_master_graph.py -k render_concepts_md -v`
Expected: FAIL — attribute not defined.

- [ ] **Step 3: Implement `render_concepts_md` and `cmd_concepts`**

```python
def render_concepts_md(rows: list[dict], top: int = 200) -> str:
    lines = ["# Concepts for the Book", "",
             "Ranked by `degree + 2*reference_support` over the master graph. "
             "Verdict vs the manuscript: **well-covered** / **under-covered** "
             "(in the book but heavily cited in the literature) / **absent** "
             "(in the references, not in the book).", "",
             "| Concept | Community | Degree | Ref support | Hub | Verdict |",
             "|---|---|---|---|---|---|"]
    for r in rows[:top]:
        lines.append(f"| {r['label']} | {r['community']} | {r['degree']} | "
                     f"{r['support']} | {'yes' if r['is_hub'] else ''} | {r['verdict']} |")
    lines += ["", "## Per-chapter gaps", "",
              "Concepts the literature emphasizes that each chapter under-covers or omits.", ""]
    gaps = [r for r in rows if r["verdict"] in ("under-covered", "absent")]
    by_ch: dict[str, list] = {}
    for r in gaps:
        by_ch.setdefault(r["chapter"], []).append(r)
    for ch in sorted(by_ch, key=lambda c: (c == "Unassigned", c)):
        lines.append(f"### {ch}")
        for r in sorted(by_ch[ch], key=lambda r: -r["score"])[:30]:
            lines.append(f"- **{r['label']}** — {r['verdict']} "
                         f"(support {r['support']}, degree {r['degree']})")
        lines.append("")
    return "\n".join(lines)


def cmd_concepts() -> int:
    graph = _load(MASTER_GRAPH)
    scored = score_concepts(graph)
    rows = coverage_diff(graph, scored)
    (MASTER_DIR / "CONCEPTS_FOR_BOOK.md").write_text(render_concepts_md(rows), encoding="utf-8")
    n_absent = sum(1 for r in rows if r["verdict"] == "absent")
    n_under = sum(1 for r in rows if r["verdict"] == "under-covered")
    print(f"wrote {MASTER_DIR / 'CONCEPTS_FOR_BOOK.md'}: {len(rows)} concepts, "
          f"{n_under} under-covered, {n_absent} absent")
    return 0
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest tests/test_master_graph.py -k render_concepts_md -v`
Expected: PASS

- [ ] **Step 5: Generate the report on the real merged graph**

Run: `python scripts/build_master_graph.py concepts`
Expected: writes `master-graph/CONCEPTS_FOR_BOOK.md`; prints counts. Open it and confirm absent/under-covered concepts look sane (e.g. lattice/folding terms from references showing as absent if the manuscript lacks them).

- [ ] **Step 6: Commit**

```bash
git add scripts/build_master_graph.py tests/test_master_graph.py master-graph/CONCEPTS_FOR_BOOK.md
git commit -m "master-graph: concept extraction report (Stage 4)"
```

---

## Phase 3 — Stage 2: Citation snowball (bounded)

### Task 9: Citation parse + lexical filter + dedup helpers

**Files:**
- Modify: `scripts/build_master_graph.py`
- Test: `tests/test_master_graph.py`

- [ ] **Step 1: Write the failing test**

```python
def test_parse_citations_normalizes_and_drops_untitled():
    raw = [{"title": "  Nova  ", "url": "https://eprint.iacr.org/2021/370"},
           {"authors": ["X"]}]  # no title -> dropped
    out = m.parse_citations(raw)
    assert len(out) == 1 and out[0]["title"] == "Nova"


def test_lexical_keep_uses_keywords_and_vocab():
    vocab = {"sumcheck"}
    assert m.lexical_keep({"title": "A folding scheme for R1CS"}, vocab) is True   # keyword
    assert m.lexical_keep({"title": "Sumcheck revisited", "venue": ""}, vocab) is True  # vocab
    assert m.lexical_keep({"title": "Gardening tips for tomatoes"}, vocab) is False


def test_dedup_candidates_against_existing_keys():
    existing = {m.citation_key({"url": "https://eprint.iacr.org/2021/370"})}
    cands = [{"title": "Nova", "url": "https://eprint.iacr.org/2021/370"},
             {"title": "HyperNova", "url": "https://eprint.iacr.org/2023/573"}]
    out = m.dedup_candidates(cands, existing)
    assert [c["title"] for c in out] == ["HyperNova"]
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_master_graph.py -k "parse_citations or lexical_keep or dedup_candidates" -v`
Expected: FAIL — attributes not defined.

- [ ] **Step 3: Implement**

```python
ZK_KEYWORDS = {
    "zero", "knowledge", "snark", "stark", "proof", "circuit", "commitment",
    "polynomial", "lattice", "folding", "recursion", "recursive", "arithmetization",
    "witness", "verifier", "prover", "soundness", "ivc", "pcd", "accumulation",
    "sumcheck", "plonk", "groth", "kzg", "fri", "pairing", "elliptic", "curve",
    "field", "hash", "fiat", "shamir", "zkvm", "rollup", "halo", "nova", "bulletproof",
}


def vocab_from_graph(graph: dict) -> set[str]:
    toks: set[str] = set()
    for n in graph["nodes"]:
        for t in normalize_label(n.get("label") or "").split():
            if len(t) > 2:
                toks.add(t)
    return toks


def parse_citations(raw: list[dict]) -> list[dict]:
    """Normalize subagent citation records; drop entries with no title."""
    out = []
    for r in raw or []:
        title = (r.get("title") or "").strip()
        if not title:
            continue
        out.append({"title": title, "authors": r.get("authors") or [],
                    "venue": (r.get("venue") or "").strip(),
                    "year": r.get("year"), "url": (r.get("url") or "").strip()})
    return out


def lexical_keep(candidate: dict, vocab: set[str], keywords: set[str] = ZK_KEYWORDS) -> bool:
    toks = set(normalize_label(
        f"{candidate.get('title','')} {candidate.get('venue','')}").split())
    return bool(toks & keywords) or bool(toks & vocab)


def citation_key(c: dict) -> str:
    url = (c.get("url") or "").strip().lower()
    if url:
        return "url:" + re.sub(r"^https?://(www\.)?", "", url).rstrip("/")
    return "title:" + normalize_label(c.get("title") or c.get("citation") or "")


def manifest_keys(manifest: list[dict]) -> set[str]:
    keys = set()
    for e in manifest:
        if e.get("url"):
            keys.add(citation_key({"url": e["url"]}))
        keys.add(citation_key({"citation": e.get("citation", "")}))
    return keys


def dedup_candidates(cands: list[dict], existing_keys: set[str]) -> list[dict]:
    out, seen = [], set(existing_keys)
    for c in cands:
        k = citation_key(c)
        if k in seen:
            continue
        seen.add(k)
        out.append(c)
    return out
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest tests/test_master_graph.py -k "parse_citations or lexical_keep or dedup_candidates" -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/build_master_graph.py tests/test_master_graph.py
git commit -m "master-graph: citation parse + lexical filter + dedup"
```

---

### Task 10: Snowball state + stop-check

**Files:**
- Modify: `scripts/build_master_graph.py`
- Test: `tests/test_master_graph.py`

- [ ] **Step 1: Write the failing test**

```python
def test_should_stop_enforces_all_three_limits():
    assert m.should_stop({"round": 0, "total_fetched": 150, "new_relevant_last_round": None})[0] is True   # hard cap
    assert m.should_stop({"round": 3, "total_fetched": 0, "new_relevant_last_round": None})[0] is True      # max rounds
    assert m.should_stop({"round": 1, "total_fetched": 0, "new_relevant_last_round": 4})[0] is True          # converged
    assert m.should_stop({"round": 1, "total_fetched": 0, "new_relevant_last_round": 20})[0] is False
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_master_graph.py -k should_stop -v`
Expected: FAIL — attribute not defined.

- [ ] **Step 3: Implement state + stop-check**

```python
MAX_ROUNDS, MIN_NEW_PER_ROUND, HARD_CAP = 3, 10, 150


def load_state() -> dict:
    path = SNOWBALL / "state.json"
    if path.exists():
        return _load(path)
    return {"round": 0, "total_fetched": 0, "new_relevant_last_round": None,
            "mined_files": [], "frontier": []}


def save_state(state: dict) -> None:
    _dump(SNOWBALL / "state.json", state)


def should_stop(state: dict, max_rounds: int = MAX_ROUNDS,
                min_new: int = MIN_NEW_PER_ROUND, hard_cap: int = HARD_CAP) -> tuple[bool, str]:
    if state["total_fetched"] >= hard_cap:
        return True, "hard_cap"
    if state["round"] >= max_rounds:
        return True, "max_rounds"
    nr = state.get("new_relevant_last_round")
    if nr is not None and nr < min_new:
        return True, "converged"
    return False, ""
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest tests/test_master_graph.py -k should_stop -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/build_master_graph.py tests/test_master_graph.py
git commit -m "master-graph: snowball state + bounded stop-check"
```

---

### Task 11: `cmd_snowball_plan` — choose frontier, emit extraction jobs

**Files:**
- Modify: `scripts/build_master_graph.py`

- [ ] **Step 1: Implement frontier selection + job emission**

`snowball-plan` selects the papers to mine this round (round 0: every `type:paper` entry across both manifests with a fetched PDF; later rounds: the persisted frontier) and writes one job per PDF for the extraction subagents.

```python
def _all_papers() -> list[dict]:
    """Every fetched paper across both manifests, as {id, manifest, file, chapters}."""
    rows = []
    for name, mpath in MANIFESTS.items():
        if not mpath.exists():
            continue
        for e in _load(mpath):
            if e.get("type") == "paper" and e.get("duplicate_of") is None:
                f = REPO / e["file"]
                if f.exists() and f.read_bytes()[:5] == b"%PDF-":
                    rows.append({"id": e["id"], "manifest": name,
                                 "file": e["file"], "chapters": e.get("chapters", [])})
    return rows


def cmd_snowball_plan() -> int:
    state = load_state()
    stop, why = should_stop(state)
    if stop:
        print(f"snowball stopped: {why} (round={state['round']}, fetched={state['total_fetched']})")
        return 0
    if state["round"] == 0 and not state["frontier"]:
        frontier = _all_papers()
    else:
        fset = set(state["frontier"])
        frontier = [p for p in _all_papers() if p["file"] in fset]
    frontier = [p for p in frontier if p["file"] not in set(state["mined_files"])]
    jobs = [{"file": p["file"], "manifest": p["manifest"], "chapters": p["chapters"],
             "frag_out": f"master-graph/.snowball/frag-r{state['round']}-{i:03d}.json"}
            for i, p in enumerate(frontier)]
    _dump(SNOWBALL / "jobs.json", jobs)
    print(f"round {state['round']}: {len(jobs)} papers to mine -> {SNOWBALL / 'jobs.json'}")
    return 0
```

- [ ] **Step 2: Run the planner**

Run: `python scripts/build_master_graph.py snowball-plan`
Expected: writes `master-graph/.snowball/jobs.json` with one job per unmined fetched PDF; prints the count.

- [ ] **Step 3: Commit**

```bash
git add scripts/build_master_graph.py
git commit -m "master-graph: snowball-plan (frontier selection + extraction jobs)"
```

---

### Task 12: Run one snowball round (orchestration runbook)

This task is orchestration — no new code. It runs once per round; repeat until `snowball-plan`/`snowball-merge` report a stop.

**Per-PDF extraction subagent prompt (Agent tool, one per job in `jobs.json`):**

> Extract a knowledge-graph fragment AND the bibliography from this paper. Read the PDF at `<job.file>`. Output ONLY JSON with two keys:
> `"fragment"`: `{"nodes": [{"id": "concept_<kebab>", "label": "...", "file_type": "paper", "source_file": "<job.file>", "source_location": "<section>"}], "edges": [{"source": "...", "target": "...", "relation": "...", "source_file": "<job.file>"}]}` — reuse existing `concept_<kebab>` ids for standard ZK concepts (folding-scheme, ivc, pcd, accumulation, nova, kzg-polynomial-commitment, …) so nodes align across the graph.
> `"citations"`: `[{"title": "...", "authors": ["..."], "venue": "...", "year": 2021, "url": "<pdf or eprint/arxiv url if known, else empty>"}]` — every work in the references section.
> Write the whole JSON to `<job.frag_out>`. Your final message is just the path you wrote.

Dispatch these in parallel (see superpowers:dispatching-parallel-agents). Then:

- [ ] **Step 1: Collect candidate citations, filter, judge, dedup, append to manifests**

Run this helper command (added in Task 13) after all extraction fragments are written:

Run: `python scripts/build_master_graph.py snowball-merge`

`snowball-merge` (Task 13) does: load each `frag-r<round>-*.json`; `merge_fragment` the `fragment` into the master; collect `citations`; `parse_citations` → `lexical_keep` (vs `vocab_from_graph(master)`) → `dedup_candidates` (vs both manifests + prior snowball entries). It writes the lexical survivors to `master-graph/.snowball/judge-in.json` and pauses for the relevance judge.

- [ ] **Step 2: Dispatch ONE relevance-judge subagent (Agent tool)**

> You are judging whether papers belong in a book on zero-knowledge proof systems (setup, languages, witness, arithmetization, proof systems, primitives, on-chain verification, recursion/folding). Read `master-graph/.snowball/judge-in.json` (a list of `{title, authors, venue, year, url}`). Keep a paper only if its subject is squarely ZK/cryptographic-proof relevant to those topics; drop survey-adjacent or tangential works. Output ONLY JSON: `{"keep": [<same objects you keep, unchanged>]}`. Write it to `master-graph/.snowball/judge-out.json`. Final message: the path.

- [ ] **Step 3: Finalize the round (append manifest entries, fetch, update state)**

Run: `python scripts/build_master_graph.py snowball-merge --finalize`

This reads `judge-out.json`, appends kept papers as new manifest entries (recursion-origin → `references/recursion/manifest.json`, else `references/manifest.json`) with provenance, fetches them, updates `state.json` (`round += 1`, `total_fetched += fetched`, `new_relevant_last_round = len(kept)`, frontier = newly fetched files, mark this round's PDFs mined), and prints the stop check. **The HARD_CAP is enforced here**: if appending would exceed 150 total, the remainder is dropped and logged.

- [ ] **Step 4: Re-extract the newly fetched papers and merge**

Run `snowball-plan` again (it now selects the new frontier), dispatch the per-PDF extraction subagents (Step prompt above), and `snowball-merge` to fold them in. Repeat Task 12 until the stop check fires.

- [ ] **Step 5: Commit the round**

```bash
git add references/manifest.json references/recursion/manifest.json references/ master-graph/graph.json master-graph/GRAPH_REPORT.md master-graph/graph.html master-graph/obsidian
git add -f master-graph/.snowball/state.json
git commit -m "master-graph: snowball round <N> (<K> new papers)"
```

---

### Task 13: `cmd_snowball_merge` (fragment merge + candidate pipeline + finalize)

**Files:**
- Modify: `scripts/build_master_graph.py`

- [ ] **Step 1: Implement the merge + candidate pipeline + finalize**

```python
def _append_manifest_entries(kept: list[dict], state: dict) -> int:
    """Append kept papers as manifest entries with provenance, honoring HARD_CAP.
    Returns the number actually appended."""
    room = HARD_CAP - state["total_fetched"]
    if room <= 0:
        print("HARD_CAP reached; dropping all candidates this round (logged).")
        return 0
    if len(kept) > room:
        print(f"HARD_CAP: appending {room} of {len(kept)} candidates; dropping {len(kept) - room} (logged).")
        kept = kept[:room]
    appended = 0
    for name, mpath in MANIFESTS.items():
        manifest = _load(mpath)
        next_id = max((e["id"] for e in manifest), default=0) + 1
        for c in kept:
            target = "recursion" if c.get("_origin") == "recursion" else "book"
            if name != target:
                continue
            url = c.get("url") or ""
            slug = re.sub(r"[^a-z0-9]+", "-", (c["title"][:48]).lower()).strip("-")
            ext = "pdf" if url.endswith(".pdf") or "eprint.iacr.org" in url or "arxiv.org" in url else "md"
            entry = {"id": next_id, "slug": slug,
                     "citation": c["title"] + (f" ({c['venue']} {c['year']})" if c.get("venue") else ""),
                     "chapters": c.get("_chapters", []),
                     "type": "paper" if ext == "pdf" else ("web" if url else "stub"),
                     "file": f"references/snowball/{name}/ref-{next_id:03d}-{slug}.{ext}",
                     "status": "pending",
                     "discovered_from": c.get("_from"), "snowball_round": state["round"]}
            if url:
                entry["url"] = url
            manifest.append(entry)
            next_id += 1
            appended += 1
        _dump(mpath, manifest)
    return appended


def cmd_snowball_merge(finalize: bool) -> int:
    import sys as _sys
    _sys.path.insert(0, str(REPO / "scripts"))
    from deepen_pdfs import merge_fragment
    from networkx.readwrite import json_graph

    state = load_state()
    if not finalize:
        graph = _load(MASTER_GRAPH)
        jobs = _load(SNOWBALL / "jobs.json")
        cands_raw: list[dict] = []
        mined = []
        for j in jobs:
            fp = REPO / j["frag_out"]
            if not fp.exists():
                print(f"  no fragment: {j['frag_out']}, skipped")
                continue
            blob = _load(fp)
            try:
                frag = load_fragment_blob(blob)  # validates {nodes,edges}
            except ValueError as exc:
                print(f"  bad fragment {fp.name}: {exc}, skipped")
                continue
            merge_fragment(graph, frag)
            for c in parse_citations(blob.get("citations", [])):
                c["_from"] = j["file"]
                c["_origin"] = "recursion" if "recursion" in j["manifest"] else "book"
                c["_chapters"] = j.get("chapters", [])
                cands_raw.append(c)
            mined.append(j["file"])
        # rebuild master with the newly merged fragment nodes
        G = json_graph.node_link_graph(graph, edges="links")
        _export(G, None, None, len(INPUTS))
        # candidate pipeline: lexical filter + dedup vs both manifests
        vocab = vocab_from_graph(graph)
        existing = set().union(*(manifest_keys(_load(p)) for p in MANIFESTS.values() if p.exists()))
        survivors = dedup_candidates(
            [c for c in cands_raw if lexical_keep(c, vocab)], existing)
        _dump(SNOWBALL / "judge-in.json", survivors)
        state["mined_files"] = sorted(set(state["mined_files"]) | set(mined))
        save_state(state)
        print(f"merged {len(mined)} fragments; {len(cands_raw)} citations -> "
              f"{len(survivors)} lexical survivors -> {SNOWBALL / 'judge-in.json'}")
        print("Now run the relevance judge, then: snowball-merge --finalize")
        return 0

    # finalize: append kept entries, fetch, update state + stop-check
    kept = _load(SNOWBALL / "judge-out.json").get("keep", [])
    # carry provenance from judge-in (judge returns the same objects)
    appended = _append_manifest_entries(kept, state)
    fetched = 0
    if appended:
        import subprocess
        for name, mpath in MANIFESTS.items():
            ids = [e["id"] for e in _load(mpath)
                   if e.get("snowball_round") == state["round"] and e.get("status") == "pending"]
            if not ids:
                continue
            subprocess.run([_sys.executable, str(REPO / "scripts" / "fetch_references.py"),
                            "--manifest", str(mpath), "--only", ",".join(map(str, ids))],
                           cwd=str(REPO))
            fetched += sum(1 for e in _load(mpath)
                           if e.get("snowball_round") == state["round"]
                           and e.get("status") in ("ok", "ok-stealth"))
    new_files = []
    for mpath in MANIFESTS.values():
        if mpath.exists():
            new_files += [e["file"] for e in _load(mpath)
                          if e.get("snowball_round") == state["round"]
                          and e.get("status") in ("ok", "ok-stealth")]
    state["round"] += 1
    state["total_fetched"] += fetched
    state["new_relevant_last_round"] = len(kept)
    state["frontier"] = new_files
    save_state(state)
    stop, why = should_stop(state)
    print(f"round {state['round'] - 1}: appended {appended}, fetched {fetched}, "
          f"total_fetched {state['total_fetched']}. "
          + (f"STOP ({why})." if stop else "continue: snowball-plan."))
    return 0


def load_fragment_blob(blob: dict) -> dict:
    """Validate an inline {nodes,edges} fragment (the 'fragment' key of a subagent
    blob, or a bare fragment)."""
    frag = blob.get("fragment", blob)
    if not isinstance(frag, dict) or "nodes" not in frag or "edges" not in frag:
        raise ValueError("fragment needs 'nodes' and 'edges'")
    for n in frag["nodes"]:
        if "id" not in n or "label" not in n:
            raise ValueError(f"node missing id/label: {n}")
    return frag
```

- [ ] **Step 2: Add a unit test for `load_fragment_blob` + `_append_manifest_entries` cap**

Add to `tests/test_master_graph.py`:

```python
def test_load_fragment_blob_accepts_nested_and_bare():
    bare = {"nodes": [{"id": "a", "label": "A"}], "edges": []}
    assert m.load_fragment_blob(bare)["nodes"][0]["id"] == "a"
    nested = {"fragment": bare, "citations": []}
    assert m.load_fragment_blob(nested)["nodes"][0]["id"] == "a"
    import pytest
    with pytest.raises(ValueError):
        m.load_fragment_blob({"citations": []})
```

- [ ] **Step 3: Run the new unit test**

Run: `python -m pytest tests/test_master_graph.py -k load_fragment_blob -v`
Expected: PASS

- [ ] **Step 4: Wire the CLI (Task 14 adds `main`); commit**

```bash
git add scripts/build_master_graph.py tests/test_master_graph.py
git commit -m "master-graph: snowball-merge (fragment merge + candidate pipeline + finalize)"
```

---

### Task 14: CLI `main()` wiring

**Files:**
- Modify: `scripts/build_master_graph.py`

- [ ] **Step 1: Implement `main()`**

Add at the end of `scripts/build_master_graph.py`:

```python
def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("merge", "consolidate", "relabel", "concepts", "snowball-plan"):
        sub.add_parser(name)
    sm = sub.add_parser("snowball-merge")
    sm.add_argument("--finalize", action="store_true")
    args = ap.parse_args()
    dispatch = {
        "merge": cmd_merge, "consolidate": cmd_consolidate, "relabel": cmd_relabel,
        "concepts": cmd_concepts, "snowball-plan": cmd_snowball_plan,
    }
    if args.cmd == "snowball-merge":
        return cmd_snowball_merge(args.finalize)
    return dispatch[args.cmd]()


if __name__ == "__main__":
    import sys
    sys.exit(main())
```

- [ ] **Step 2: Smoke-test the CLI surface**

Run: `python scripts/build_master_graph.py --help`
Expected: usage lists `merge`, `consolidate`, `relabel`, `concepts`, `snowball-plan`, `snowball-merge`.

- [ ] **Step 3: Run the full test suite**

Run: `python -m pytest tests/test_master_graph.py -v`
Expected: all tests PASS.

- [ ] **Step 4: Commit**

```bash
git add scripts/build_master_graph.py
git commit -m "master-graph: CLI wiring"
```

---

## Phase 4 — Stage 3: Final re-consolidate + refreshed concepts

### Task 15: Re-dedup the grown graph and regenerate the report

**Files:** none new (reuses Phase 1 + Phase 2 commands).

- [ ] **Step 1: Rebuild the deterministic alias map over the grown graph**

Run: `python -c "import sys; sys.path.insert(0,'scripts'); import build_master_graph as m; g=m._load(m.MASTER_GRAPH); a=m.build_alias_map(g); m.validate_alias_map(a,g); m._dump(m.WORK/'aliases.json',a); print(len(a),'aliases')"`
Expected: prints the new alias count (snowball added variant labels).

- [ ] **Step 2: Optional hub LLM pass on the grown graph**

Repeat Task 5 Steps 2–4 (regenerate `hubs.json`, dispatch the synonym-judge subagent, append to `aliases.json`) if the grown graph's hubs warrant it.

- [ ] **Step 3: Consolidate + regenerate concepts report**

Run: `python scripts/build_master_graph.py consolidate && python scripts/build_master_graph.py concepts`
Expected: node count drops by the alias count; `CONCEPTS_FOR_BOOK.md` refreshed with the snowball-enriched reference support.

- [ ] **Step 4: Full test suite + final commit**

Run: `python -m pytest tests/ -v`
Expected: all tests PASS (new `test_master_graph.py` plus the existing suite unaffected).

```bash
git add master-graph/ scripts/build_master_graph.py
git add -f master-graph/.work/aliases.json master-graph/.snowball/state.json
git commit -m "master-graph: final re-consolidate + refreshed CONCEPTS_FOR_BOOK.md (Stage 3+4)"
```

- [ ] **Step 5: Update the graphify-tracked graph if desired**

The master graph is a new artifact; the CLAUDE.md graphify rules still point at `graphify-out/`. If you want `graphify query` to use the master, that is a follow-up (re-point or symlink) — out of scope for this plan. Note it in the commit body if you do it.

---

## Self-review notes (for the implementer)

- **Spec coverage:** Stage 1 = Tasks 1–5; Stage 4 = Tasks 6–8; Stage 2 = Tasks 9–14; Stage 3 = Task 15. Dedup (deterministic + hub LLM) = Tasks 3 + 5. Bounds (3 rounds / 10-new / 150-cap) = Task 10 + `_append_manifest_entries`. Hybrid relevance (lexical + LLM judge) = Task 9 + Task 12 Step 2. Manifest routing + provenance = `_append_manifest_entries`. Per-chapter rollup = Task 8.
- **Known limitation (from spec):** manifest dedup compares a candidate title against the existing entry `citation` string via `normalize_label`; near-miss wording can slip a duplicate through. The LLM judge and the per-round commit review are the backstop. Acceptable per the spec's "best-effort" note.
- **`new_relevant_last_round` semantics:** set to the count the judge KEEPS (post-filter relevant papers), which is what the convergence gate (`MIN_NEW_PER_ROUND`) should measure.
- **Cost:** bounded by the 150-paper hard cap enforced on persisted state; a crash/resume cannot exceed it.
