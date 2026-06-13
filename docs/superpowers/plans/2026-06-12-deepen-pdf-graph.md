# Deep PDF Mining for the Knowledge Graph Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deeply mine the reference PDFs into many more concept/construction/theorem/assumption/citation nodes (today: 1–6 per paper), additively merged into `graphify-out/graph.json` so existing cross-edges survive, staged with a checkpoint after a 10-paper batch.

**Architecture:** A pure, unit-tested helper module (`scripts/deepen_pdfs.py`) builds extraction *jobs* (PDF + its existing anchor node IDs) and *merges* agent-produced JSON fragments into the node-link graph (union nodes by id, union edges by `(source,target,relation)`, drop dangling). One subagent per paper reads the full PDF and emits a fragment anchored to the paper's existing nodes. The graph is then rebuilt with graphify's own library functions (cluster/analyze/report/export).

**Tech Stack:** Python 3.14. Two interpreters: **venv** `C:\sevenlayer\.venv\Scripts\python.exe` (has `pytest`) runs the tests; **system** `python` (has `graphify` + `networkx`, installed from `git+https://github.com/safishamsi/graphify.git`) runs the graphify rebuild. The Agent tool does the extraction.

**Spec:** `docs/superpowers/specs/2026-06-12-deepen-pdf-graph-design.md`

**Conventions for all tasks:**
- Working directory: `C:\sevenlayer`.
- All `graphify`/`networkx` imports in `deepen_pdfs.py` are **lazy** (inside the rebuild function) so the module imports cleanly under the venv for testing — exactly how `scripts/fetch_references.py` lazily imports `scrapling`.
- Run tests with the venv python; run the `merge` rebuild with system `python`.
- `graph.json` is networkx node-link format: top-level keys `nodes` (list of `{id,label,...}`) and `links` (list of `{source,target,relation,confidence,...}`). Extraction **fragments** use `{"nodes":[...],"edges":[...]}` — `edges` map onto graph `links`.
- Commit after every code task. Author is already configured repo-local as `Charles Hoskinson <Charles.Hoskinson@gmail.com>`. Do **not** add a `Co-Authored-By` trailer.

---

### Task 1: Pure batch/anchor/stats helpers (TDD)

**Files:**
- Create: `scripts/deepen_pdfs.py`
- Create: `tests/test_deepen_pdfs.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_deepen_pdfs.py`:

```python
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from deepen_pdfs import batch_for_ids, anchors_for_source, graph_stats

MANIFEST = [
    {"id": 6, "slug": "groth16", "chapters": [2], "type": "paper",
     "file": "references/ch02/ref-06-groth16.pdf", "status": "ok"},
    {"id": 22, "slug": "frozen-heart", "chapters": [6], "type": "web",
     "file": "references/ch06/ref-22-frozen-heart.md", "status": "ok"},
    {"id": 47, "slug": "dup", "chapters": [14], "type": "paper",
     "duplicate_of": 12, "status": "ok"},
    {"id": 1, "slug": "clarke", "chapters": [1], "type": "stub",
     "file": "references/ch01/ref-01-clarke.md", "status": "stub"},
]

GRAPH = {
    "nodes": [
        {"id": "ref-06_groth16", "label": "Groth16", "source_file": "references/ch02/ref-06-groth16.pdf"},
        {"id": "concept_qap", "label": "QAP", "source_file": "references\\ch02\\ref-06-groth16.pdf"},
        {"id": "wiki_x", "label": "X", "source_file": "wiki/chapters/02.md"},
    ],
    "links": [{"source": "wiki_x", "target": "ref-06_groth16", "relation": "cites"}],
}


def test_batch_for_ids_returns_only_papers_skipping_dups_and_stubs():
    rows = batch_for_ids(MANIFEST, [6, 22, 47, 1])
    assert rows == [(6, "references/ch02/ref-06-groth16.pdf", "groth16", [2])]


def test_anchors_for_source_matches_across_path_separators():
    anchors = anchors_for_source(GRAPH, "references/ch02/ref-06-groth16.pdf")
    assert set(anchors) == {"ref-06_groth16", "concept_qap"}
    assert anchors_for_source(GRAPH, "references/ch99/missing.pdf") == []


def test_graph_stats_counts_nodes_edges_and_per_pdf():
    s = graph_stats(GRAPH)
    assert s["nodes"] == 3
    assert s["edges"] == 1
    assert s["nodes_per_pdf"]["ref-06-groth16.pdf"] == 2
    assert s["nodes_by_source_top"]["references"] == 2
    assert s["nodes_by_source_top"]["wiki"] == 1
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/test_deepen_pdfs.py -v`
Expected: FAIL (`ModuleNotFoundError: deepen_pdfs`).

- [ ] **Step 3: Write the helpers**

Create `scripts/deepen_pdfs.py`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/test_deepen_pdfs.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/deepen_pdfs.py tests/test_deepen_pdfs.py
git commit -m "Add pure batch/anchor/stats helpers for PDF graph deepening"
```

---

### Task 2: Fragment loading + additive merge (TDD)

**Files:**
- Modify: `scripts/deepen_pdfs.py` (append helpers)
- Modify: `tests/test_deepen_pdfs.py` (append tests)

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_deepen_pdfs.py`:

```python
import json as _json
import pytest
from deepen_pdfs import load_fragment, merge_fragment


def test_load_fragment_rejects_bad_shape(tmp_path):
    good = tmp_path / "good.json"
    good.write_text(_json.dumps({"nodes": [{"id": "a", "label": "A"}], "edges": []}))
    assert load_fragment(good)["nodes"][0]["id"] == "a"

    bad = tmp_path / "bad.json"
    bad.write_text(_json.dumps({"nodes": [{"label": "no id"}], "edges": []}))
    with pytest.raises(ValueError):
        load_fragment(bad)

    missing = tmp_path / "missing.json"
    missing.write_text(_json.dumps({"nodes": []}))  # no "edges" key
    with pytest.raises(ValueError):
        load_fragment(missing)


def test_merge_fragment_is_additive_and_dedups():
    graph = {
        "nodes": [{"id": "ref-06_groth16", "label": "Groth16",
                   "source_file": "references/ch02/ref-06-groth16.pdf"}],
        "links": [],
    }
    fragment = {
        "nodes": [
            {"id": "ref-06_groth16", "label": "DUP — should not overwrite"},  # existing
            {"id": "concept_pairing", "label": "Pairing",
             "source_file": "references/ch02/ref-06-groth16.pdf"},            # new
        ],
        "edges": [
            {"source": "ref-06_groth16", "target": "concept_pairing", "relation": "uses"},
            {"source": "ref-06_groth16", "target": "concept_pairing", "relation": "uses"},  # dup
            {"source": "ref-06_groth16", "target": "ghost_node", "relation": "cites"},      # dangling
        ],
    }
    out = merge_fragment(graph, fragment)
    ids = [n["id"] for n in out["nodes"]]
    assert ids == ["ref-06_groth16", "concept_pairing"]          # additive, deduped
    assert out["nodes"][0]["label"] == "Groth16"                 # existing not overwritten
    assert len(out["links"]) == 1                                # dup + dangling dropped
    assert out["links"][0]["relation"] == "uses"


def test_merge_fragment_enforces_additive_invariant():
    graph = {"nodes": [{"id": "a", "label": "A"}, {"id": "b", "label": "B"}], "links": []}
    # Simulate a "before" count higher than reality (99 > 2) so the guard fires.
    with pytest.raises(AssertionError):
        merge_fragment(graph, {"nodes": [], "edges": []}, _force_node_count=99)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/test_deepen_pdfs.py -k "fragment" -v`
Expected: FAIL (`load_fragment` / `merge_fragment` not defined).

- [ ] **Step 3: Write the helpers**

Append to `scripts/deepen_pdfs.py`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/test_deepen_pdfs.py -v`
Expected: 6 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/deepen_pdfs.py tests/test_deepen_pdfs.py
git commit -m "Add fragment validation and additive merge for PDF graph deepening"
```

---

### Task 3: `jobs` + `merge` CLI and rebuild wiring

**Files:**
- Modify: `scripts/deepen_pdfs.py` (append CLI + rebuild)
- Modify: `.gitignore` (add `graphify-out/.deepen/`)

- [ ] **Step 1: Ignore the scratch directory**

Append to `.gitignore`:

```
# Graph deepening scratch (fragments, jobs)
graphify-out/.deepen/
```

- [ ] **Step 2: Append the CLI and rebuild to `scripts/deepen_pdfs.py`**

```python
def _load_json(path: Path) -> dict | list:
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
    to_json(G, communities, str(GRAPH_PATH))
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
```

- [ ] **Step 3: Confirm the full suite still passes**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/ -v`
Expected: all pass (21 fetch/manifest tests + 6 deepen tests = 27).

- [ ] **Step 4: Smoke-test `jobs` against the real graph (no graphify needed)**

Run: `python scripts/deepen_pdfs.py jobs --only 4,6,7,8,9,12,16,17,18,20`
Expected: `Wrote 10 jobs ...`, each line showing a non-zero anchor count (every batch-1 paper already has at least a `ref-NN_slug` node). Confirm `graphify-out/.deepen/jobs.json` exists and is git-ignored (`git status --short` shows no `.deepen/` entry).

- [ ] **Step 5: Commit**

```bash
git add scripts/deepen_pdfs.py .gitignore
git commit -m "Add jobs/merge CLI and graphify rebuild for PDF deepening"
```

---

### Task 4: Dispatch batch-1 extraction subagents

**Files:**
- Create (runtime, git-ignored): `graphify-out/.deepen/frag-04.json` … `frag-20.json`

This task uses the **Agent tool** (one subagent per paper). It produces data, not a commit. Read `graphify-out/.deepen/jobs.json` (written in Task 3) for the per-paper `id`, `pdf`, `chapters`, `anchors`, and `frag_out`.

- [ ] **Step 1: Dispatch one subagent per batch-1 paper**

For each job, dispatch a subagent with this exact prompt (substitute `PDF_PATH`, `REF_ID`, `SLUG`, `CHAPTERS`, `ANCHORS`, `FRAG_OUT` from the job). Dispatch in parallel in batches (e.g., 3–4 at a time) to stay within tool limits:

```
You are a graphify deep-extraction subagent for one cryptography paper.

Read the FULL PDF at: PDF_PATH  (use the Read tool; page through the whole file).
This is reference REF_ID (SLUG), cited in book chapter(s) CHAPTERS.

Existing graph anchor node ids for this paper (link your new nodes to these):
ANCHORS

Extract a DEEP knowledge-graph fragment: the paper's key constructions, schemes,
protocols, theorems/lemmas, security assumptions, hardness assumptions,
complexity/efficiency claims, and the named prior works it cites. Aim for 10–25
nodes for this paper.

Node id rules:
- General/shared concepts (likely to appear in other papers too): id = "concept_<kebab-name>"
  (e.g. "concept_fiat-shamir", "concept_pairing"). Use precise names so distinct
  concepts do not collide.
- Artifacts specific to THIS paper: id = "ref-REF_ID_<kebab-name>".
- Every node MUST set "source_file": "PDF_PATH".

Edge rules:
- Link every new node to one of the ANCHORS (or to another node you emit) with a
  relation in {defines, introduces, proves, assumes, cites, conceptually_related_to,
  shares_data_with}.
- confidence: EXTRACTED (stated in the paper) | INFERRED | AMBIGUOUS.
- Set "source_location" to the section or page (e.g. "§3.2" or "p. 7").

Output ONLY this JSON (no prose, no markdown fences):
{"nodes":[{"id":"...","label":"Human Readable","file_type":"paper","source_file":"PDF_PATH","source_location":null,"source_url":null,"captured_at":null,"author":null,"contributor":null}],"edges":[{"source":"node_id","target":"node_id","relation":"...","confidence":"EXTRACTED|INFERRED|AMBIGUOUS","source_file":"PDF_PATH","source_location":null,"weight":1.0}]}

After producing the JSON, WRITE it to the file FRAG_OUT (use the Write tool) and
reply with just the node and edge counts.
```

- [ ] **Step 2: Verify each fragment exists and is well-formed**

Do **not** merge yet. First validate every fragment's shape:

```bash
python - <<'EOF'
import json, pathlib, sys
sys.path.insert(0, "scripts")
from deepen_pdfs import load_fragment
import glob
for f in sorted(glob.glob("graphify-out/.deepen/frag-*.json")):
    d = load_fragment(pathlib.Path(f))
    print(f, len(d["nodes"]), "nodes", len(d["edges"]), "edges")
EOF
```

Expected: 10 fragments, each with roughly 10–25 nodes. Re-dispatch any paper whose fragment is missing, tiny (<5 nodes), or invalid before proceeding.

---

### Task 5: Merge batch 1, rebuild, verify, relabel

**Files:**
- Modify: `graphify-out/graph.json`, `GRAPH_REPORT.md`, `graph.html`, `obsidian/`, `manifest.json`, `cost.json`

- [ ] **Step 1: Back up the committed graph**

```bash
cp graphify-out/graph.json "$TEMP/graph.json.bak"
```
(PowerShell: `Copy-Item graphify-out/graph.json "$env:TEMP/graph.json.bak"`.)

- [ ] **Step 2: Merge + rebuild (system python — has graphify)**

Run: `python scripts/deepen_pdfs.py merge --only 4,6,7,8,9,12,16,17,18,20`
Expected: prints `Merged refs [4, 6, 7, 8, 9, 12, 16, 17, 18, 20]`, total nodes up by ~80–200, and each batch-1 PDF moving from 1–6 nodes to ~10–25. Exit 0.

- [ ] **Step 3: Confirm the additive invariant held on disk**

```bash
python - <<'EOF'
import json
new = json.load(open("graphify-out/graph.json", encoding="utf-8"))
old = json.load(open(__import__("os").path.join(__import__("os").environ["TEMP"], "graph.json.bak"), encoding="utf-8"))
assert len(new["nodes"]) >= len(old["nodes"]), "nodes decreased!"
assert len(new["links"]) >= len(old["links"]), "links decreased!"
print("ok: nodes", len(old["nodes"]), "->", len(new["nodes"]),
      "| links", len(old["links"]), "->", len(new["links"]))
EOF
```
Expected: `ok:` with both counts non-decreasing.

- [ ] **Step 4: Sanity queries against the deepened graph**

```bash
graphify explain "PLONK"
graphify query "What soundness or knowledge assumptions do the folding schemes rely on?"
```
Expected: `explain "PLONK"` now lists several new constructions/assumptions (permutation argument, grand-product, KZG, Fiat-Shamir, etc.), not just the title node; the folding query touches Nova/HyperNova/LatticeFold nodes. If a query returns nothing new, a fragment failed to merge — re-check Task 4.

- [ ] **Step 5: Relabel communities (agent step)**

Open `graphify-out/GRAPH_REPORT.md`, read the community membership, and replace the auto `Community N` names with 2–5 word labels by editing the `labels` dict and re-running just the report+html. Use a one-off inline script mirroring the SKILL's Step 5 (`graphify.report.generate` with your `labels` dict). Skip if the auto labels are acceptable for the checkpoint.

- [ ] **Step 6: Commit the deepened graph**

```bash
git add graphify-out/graph.json graphify-out/GRAPH_REPORT.md graphify-out/graph.html graphify-out/obsidian graphify-out/cost.json
git commit -m "Deepen knowledge graph: batch 1 (10 core papers) deep-mined"
```
(`graphify-out/manifest.json` is intentionally **not** staged — see the note in `cmd_merge`.)

- [ ] **Step 7: Clean up the backup**

```bash
rm -f "$TEMP/graph.json.bak"
```

---

### Task 6: Checkpoint report and gate

**Files:**
- None (reporting only)

- [ ] **Step 1: Produce the checkpoint summary**

Report to the user, from the Task 5 output:
- total nodes/edges before → after; communities count;
- per-paper node growth for the 10 (before 1–6 → after target 10–25);
- new god nodes and 2–3 sample new cross-paper "surprising connections" from `GRAPH_REPORT.md`;
- estimated token cost for the batch (from the appended `cost.json` run);
- the two sanity-query results.

- [ ] **Step 2: Gate the remaining ~36 PDFs**

Ask the user whether to continue. If yes, repeat Tasks 4–5 with the next batch of ref ids (e.g. the remaining ePrint papers: 5, 10, 11, 14, 15, 19, 21, 23, 28, 29, 30, 32, 33, 35, 36, 37, 38, 45, 46, 50, 51, 56, 60, 62, 63, 65, plus NIST/standards PDFs 25, 26, 64 and the World/eIDAS PDFs), in batches of ~10. The 18 MB scanned GMR (ref 2) needs a vision-based read — handle it last and individually.

> **Do NOT run `graphify update .` to "refresh" this graph.** The `CLAUDE.md`
> rule about `graphify update` is for code/AST graphs. This is a content graph
> built over manuscript + references + wiki with explicit excludes; running
> update from the repo root would pollute it with `scripts/` and `tests/` tooling
> code. The `merge` command already rebuilds the graph correctly.
