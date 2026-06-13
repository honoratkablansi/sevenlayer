# Recursion Chapters: Reference Gathering + Deep Graph Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Gather every reference cited in the 3-chapter recursion outline into a separate `references/recursion/` corpus via scrapling (reusing the 9 papers already in the main corpus), then deep-mine the outline + references into a new `recursion-graph/`.

**Architecture:** Copy the outline in-repo and split by chapter; curate `references/recursion/manifest.json`; reuse the hardened `fetch_references.py` (add `--manifest`) to pull the corpus; deep-mine each new PDF + each outline chapter with one subagent apiece (reuse the 9 overlaps' existing deep fragments); build with graphify into `recursion-graph/`. All graphify/networkx imports stay lazy.

**Tech Stack:** Python 3.14. venv `C:\sevenlayer\.venv\Scripts\python.exe` (pytest + scrapling) runs tests/fetch; system `python` (graphify) runs the build. The Agent tool does extraction.

**Spec:** `docs/superpowers/specs/2026-06-13-recursion-graph-design.md`

**Conventions for all tasks:**
- Working directory `C:\sevenlayer`. Tests + fetch use the venv python; the graph build uses system `python`.
- Commit after each code task as `Charles Hoskinson <Charles.Hoskinson@gmail.com>` (repo-local). No `Co-Authored-By` trailer.
- Reuse: `deepen_pdfs.merge_fragment`, `build_book_graph.merge_extraction`, `compare_graphs` patterns.
- The 9 overlap papers and their existing deep fragments:

  | slug | reuse PDF (main corpus) | existing fragment |
  |---|---|---|
  | nova | references/ch06/ref-17-nova.pdf | graphify-out/.deepen/frag-17.json |
  | hypernova | references/ch06/ref-18-hypernova.pdf | graphify-out/.deepen/frag-18.json |
  | protostar | references/ch06/ref-19-protostar.pdf | graphify-out/.deepen/frag-19.json |
  | latticefold | references/ch06/ref-20-latticefold.pdf | graphify-out/.deepen/frag-20.json |
  | latticefold-plus | references/ch02/ref-11-latticefold-plus.pdf | graphify-out/.deepen/frag-11.json |
  | ccs | references/ch03/ref-14-ccs-customizable-constraints.pdf | graphify-out/.deepen/frag-14.json |
  | circle-starks | references/ch06/ref-23-circle-starks.pdf | graphify-out/.deepen/frag-23.json |
  | stark | references/ch02/ref-08-stark.pdf | graphify-out/.deepen/frag-08.json |
  | jolt | references/ch03/ref-16-jolt.pdf | graphify-out/.deepen/frag-16.json |

---

### Task 1: Bring the outline in-repo + chapter splitter (TDD)

**Files:**
- Create: `recursion/recursion-outline.md` (copy of the Desktop outline)
- Create: `scripts/split_recursion_outline.py`
- Create: `tests/test_recursion_graph.py`
- Modify: `.gitignore`

- [ ] **Step 1: Copy the outline into the repo + ignore the scratch dir**

```bash
cp "/c/Users/charl/OneDrive/Desktop/recursion_book_outline.md" recursion/recursion-outline.md
```
(PowerShell: `New-Item -ItemType Directory -Force recursion; Copy-Item "$env:USERPROFILE\OneDrive\Desktop\recursion_book_outline.md" recursion\recursion-outline.md`.)
Append to `.gitignore`:
```
# Recursion-graph scratch (chapter splits, fragments, jobs)
recursion-graph/.work/
```

- [ ] **Step 2: Write the failing test**

Create `tests/test_recursion_graph.py`:

```python
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from split_recursion_outline import split_chapters

SAMPLE = """# Recursive Proof Composition: A Three-Chapter Treatment

intro blurb

## Chapter 1: Recursive Proof Composition

### 1.1 Why Recursion?
ch1 body

## Chapter 2: Folding Schemes in Depth

ch2 body

## Chapter 3: Applications of Recursive Proving

ch3 body

## Backmatter Notes (for the full manuscript)

backmatter
"""


def test_split_chapters_returns_three():
    chs = split_chapters(SAMPLE)
    assert [slug for slug, _ in chs] == ["rc01", "rc02", "rc03"]


def test_split_chapter_bodies_bounded():
    chs = dict(split_chapters(SAMPLE))
    assert "ch1 body" in chs["rc01"] and "ch2 body" not in chs["rc01"]
    assert "backmatter" not in chs["rc03"]   # backmatter excluded
    assert "intro blurb" not in chs["rc01"]  # title preamble excluded
```

- [ ] **Step 3: Run test to verify it fails**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/test_recursion_graph.py -v`
Expected: FAIL (`ModuleNotFoundError: split_recursion_outline`).

- [ ] **Step 4: Write the splitter**

Create `scripts/split_recursion_outline.py`:

```python
"""Split recursion/recursion-outline.md into its 3 chapter files for extraction.

Usage (from repo root):
    python scripts/split_recursion_outline.py
Writes recursion-graph/.work/rc01.md ... rc03.md
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUTLINE = REPO / "recursion" / "recursion-outline.md"
WORK = REPO / "recursion-graph" / ".work"

_CHAPTER_RE = re.compile(r"^## Chapter (\d+):", re.MULTILINE)
_H2_RE = re.compile(r"^## ", re.MULTILINE)


def split_chapters(text: str) -> list[tuple[str, str]]:
    """Return [(slug, body), ...] for each '## Chapter N:' heading. A chapter
    spans from its heading to the next '## ' heading (exclusive), so the title
    preamble and the '## Backmatter Notes' section bound chapters."""
    h2s = [m.start() for m in _H2_RE.finditer(text)]
    out = []
    for m in _CHAPTER_RE.finditer(text):
        start = m.start()
        nxt = next((h for h in h2s if h > start), len(text))
        out.append((f"rc{int(m.group(1)):02d}", text[start:nxt].strip()))
    return out


def main() -> None:
    text = OUTLINE.read_text(encoding="utf-8")
    WORK.mkdir(parents=True, exist_ok=True)
    chapters = split_chapters(text)
    for slug, body in chapters:
        (WORK / f"{slug}.md").write_text(body + "\n", encoding="utf-8")
    print(f"wrote {len(chapters)} chapter files to {WORK}")
    for slug, body in chapters:
        print(f"  {slug}.md  {len(body):>6} chars  {body.splitlines()[0][:60]}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run test + split the real outline**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/test_recursion_graph.py -v` → 2 passed.
Run: `python scripts/split_recursion_outline.py` → `wrote 3 chapter files`, titles = Chapters 1/2/3. Confirm `git status --short` shows no `recursion-graph/.work/`.

- [ ] **Step 6: Commit**

```bash
git add recursion/recursion-outline.md scripts/split_recursion_outline.py tests/test_recursion_graph.py .gitignore
git commit -m "Add recursion outline in-repo + chapter splitter"
```

---

### Task 2: Parameterize fetch_references.py (--manifest + reuse) (TDD)

**Files:**
- Modify: `scripts/fetch_references.py`
- Modify: `tests/test_recursion_graph.py` (append)

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_recursion_graph.py`:

```python
import fetch_references as fr


def test_process_reuse_entry_no_network(tmp_path, monkeypatch):
    # a reuse entry resolves from an existing main-corpus file, never hitting network
    existing = tmp_path / "existing.pdf"
    existing.write_bytes(b"%PDF-1.7 x")
    monkeypatch.setattr(fr, "REPO", tmp_path)
    def boom(*a, **k):
        raise AssertionError("reuse entry must not fetch")
    monkeypatch.setattr(fr, "fetch_paper", boom)
    ok = {"id": 1, "slug": "nova", "type": "paper", "chapters": [1],
          "file": "references/recursion/ch1/ref-01-nova.pdf",
          "reuse": "existing.pdf", "status": "pending"}
    assert fr.process(ok, [ok], force=False, dry_run=False) == "ok"
    missing = dict(ok, reuse="nope.pdf")
    assert fr.process(missing, [missing], force=False, dry_run=False) == "pending"


def test_manifest_path_is_overridable(tmp_path, monkeypatch):
    m = tmp_path / "m.json"
    m.write_text('[{"id": 1, "slug": "x"}]', encoding="utf-8")
    monkeypatch.setattr(fr, "MANIFEST_PATH", m)
    assert fr.load_manifest()[0]["slug"] == "x"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/test_recursion_graph.py -k "reuse or overridable" -v`
Expected: FAIL (`test_process_reuse_entry_no_network` — reuse not handled).
(`test_manifest_path_is_overridable` may already pass since MANIFEST_PATH is module-level; keep it as a guard.)

- [ ] **Step 3: Add `reuse` handling in `process()`**

In `scripts/fetch_references.py`, at the top of `process()` (right after the docstring line `"""Returns the new status for the entry."""`, before the `duplicate_of` check), insert:

```python
    if entry.get("reuse") is not None:
        # Overlap with the main corpus: the file already exists elsewhere; never fetch.
        return "ok" if (REPO / entry["reuse"]).exists() else "pending"
```

- [ ] **Step 4: Add `--manifest` to `main()`**

In `main()`, after `args = ap.parse_args()`, add the arg and override the module global. Replace the arg block + parse with:

```python
    ap.add_argument("--force", action="store_true", help="re-download existing files")
    ap.add_argument("--only", help="comma-separated ref ids")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--manifest", help="path to a manifest other than the default")
    args = ap.parse_args()

    if args.manifest:
        global MANIFEST_PATH
        MANIFEST_PATH = Path(args.manifest)
```

(Entry `file` paths are repo-relative, so they resolve under `REPO` regardless of which manifest is loaded.)

- [ ] **Step 5: Run the full test suite**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/ -q`
Expected: all pass (the existing 17 fetch tests + the new ones).

- [ ] **Step 6: Commit**

```bash
git add scripts/fetch_references.py tests/test_recursion_graph.py
git commit -m "fetch_references: add --manifest flag and reuse (overlap) handling"
```

---

### Task 3: Curate references/recursion/manifest.json

**Files:**
- Create: `references/recursion/manifest.json`
- Create: `tests/test_recursion_manifest.py`

This task curates the corpus manifest as DATA from the outline. The manifest is
hand-built (URL resolution is verified in Task 4's dry-run + triage, exactly as
the main corpus was). Schema per entry:
`{"id", "slug", "citation", "chapters":[1|2|3], "type":"paper|web|stub", "url"?,
"file", "status":"pending", "reuse"?}`.

- [ ] **Step 1: Write the manifest test**

Create `tests/test_recursion_manifest.py`:

```python
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "references" / "recursion" / "manifest.json"
VALID_TYPES = {"paper", "web", "stub"}


def load():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_ids_unique_and_contiguous():
    ids = [e["id"] for e in load()]
    assert ids == sorted(ids)
    assert len(ids) == len(set(ids))


def test_entry_shape():
    for e in load():
        assert e["type"] in VALID_TYPES, e
        assert e["citation"].strip()
        assert e["chapters"] and all(c in (1, 2, 3) for c in e["chapters"])
        ext = "pdf" if e["type"] == "paper" else "md"
        expected = f"references/recursion/ch{e['chapters'][0]}/ref-{e['id']:02d}-{e['slug']}.{ext}"
        assert e["file"] == expected, f"ref {e['id']}: {e['file']} != {expected}"
        if e["type"] in ("paper", "web") and "reuse" not in e:
            assert e["url"].startswith("http"), e
        if "reuse" in e:
            assert (REPO / e["reuse"]).exists(), f"reuse target missing: {e['reuse']}"


def test_slugs_kebab_and_unique():
    slugs = [e["slug"] for e in load()]
    assert len(slugs) == len(set(slugs))
    for s in slugs:
        assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", s), s
```

- [ ] **Step 2: Build the manifest from this inventory**

Create `references/recursion/manifest.json` as a JSON array. Use **status `"pending"`** everywhere. Resolution rules: printed ePrint `YYYY/NNN` → `https://eprint.iacr.org/YYYY/NNN.pdf`; arXiv id → `https://arxiv.org/pdf/<id>`; venue-only papers → the authors' ePrint/preprint copy if one exists, else `type:"stub"`; docs/blogs → `type:"web"` with the page URL; vague "literature"/"practitioner" mentions → `type:"stub"`. The 9 overlaps use `"reuse"` (table in Conventions) and no `url`.

Inventory (id order; chapter = first citing chapter; dedupe repeats across subsections):

*Reuse (9, type paper, `reuse` set, no url):* nova, hypernova, protostar, latticefold, latticefold-plus, ccs, circle-starks, stark, jolt.

*Papers — resolve to ePrint/arXiv (type paper):* valiant-ivc (TCC'08 — stub if no open copy), bctv-cycles (eprint 2014/595), bitansky-pcd (eprint 2012/095), chiesa-tromer-pcd (ICS'10 — stub if none), halo (eprint 2019/1021), bcms-pcd-accumulation (eprint 2020/499), fractal (eprint 2019/1076), fs-attacks (eprint 2025/118), pasta-curves (web/github), cycles-pairing-friendly (eprint 2019/1135 — verify, else stub), bclms-pcd-no-succinct (eprint 2020/1618), zktree (eprint 2023/208), cyclefold (eprint 2023/1192), poseidon (eprint 2019/458), revisiting-nova-cycle (eprint 2023/969), snarkpack (eprint 2021/529), pedersen (stub), fiat-shamir (stub or open scan), spartan (eprint 2019/550), minroot (eprint 2022/1626), supernova (eprint 2022/1758), protogalaxy (eprint 2023/1106), ro-methodology (eprint/IACR — stub if none), coda-mina (eprint 2020/352), zkbridge (eprint 2022/433), verisbom (arxiv — resolve id), trustless-dnn (arxiv 2210.08674), zkcnn (eprint 2021/673), vsql (eprint 2017/1146), delegating-computation (STOC'08 — stub if none), photoproof (S&P'16 — stub if none), veritas (eprint 2024/1066), vdf (eprint 2018/601), wesolowski-vdf (eprint 2018/623), delegatable-anon-creds (CRYPTO'09 — stub if none), deco (eprint 2019/1300), provisions (eprint 2015/1008), zexe (eprint 2018/962), plonky2 (web/github pdf).

*Web (type web):* sp1-hypercube, risc-zero-proof-overview, risc-zero-continuations, ef-realtime-proving, ef-zkevm-roadmap, polygon-zkevm-docs, polygon-agglayer, aligned-layer, nebra-upa, mina-pickles, sonobe-docs, veridise-nova, ezkl-docs, starkware-recursive-starks, in-toto, slsa, rfc-6962, c2pa-spec, w3c-vc, zkemail-docs, tlsnotary-docs, summa-docs, ethproofs, ntia-cisa-sbom, ethereum-lean-roadmap, anon-aadhaar, dark-forest, reproducible-builds.

*Stub (type stub, no url):* paranova, streaming-prover-lit, multi-party-folding, verifiable-voting-lit, ivc-flight-control, state-channel-lit, recursive-prover-audits, zkvm-benchmark-asplos, hash-based-accumulation-arc, do-178c — plus any paper above with no resolvable open copy.

Build the array following the test's `file` convention. Save it.

- [ ] **Step 3: Run the manifest test**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/test_recursion_manifest.py -v`
Expected: 3 passed. Fix slug/file/url shape until green.

- [ ] **Step 4: Commit**

```bash
git add references/recursion/manifest.json tests/test_recursion_manifest.py
git commit -m "Add curated recursion reference manifest"
```

---

### Task 4: Fetch the recursion corpus

**Files:**
- Create (downloads): `references/recursion/ch1|ch2|ch3/*`
- Modify: `references/recursion/manifest.json` (statuses)

- [ ] **Step 1: Dry-run (no network)**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" scripts/fetch_references.py --manifest references/recursion/manifest.json --dry-run`
Expected: one line per entry, exit 0, reuse entries shown as already-present, no files written.

- [ ] **Step 2: Smoke-test one paper + one web + one reuse**

Run: `& "...\python.exe" scripts/fetch_references.py --manifest references/recursion/manifest.json --only <halo-id>,<sp1-hypercube-id>,<nova-id>`
Expected: the ePrint paper downloads (starts `%PDF`), the web page captures to `.md`, the reuse (nova) resolves `ok` without network.

- [ ] **Step 3: Full fetch**

Run: `& "...\python.exe" scripts/fetch_references.py --manifest references/recursion/manifest.json`
Expected: several minutes (Camoufox launches for eprint Cloudflare + JS docs). Final line reports resolved count and lists failures.

- [ ] **Step 4: Triage failures**

For each `failed`/`pending` (non-reuse) entry: wrong/dead URL → find the correct open-access URL, edit the manifest, rerun `--only <id> --force`; hard bot-wall or no open copy → change `type` to `stub` (and `file` ext to `.md`), rerun `--only <id>`. Repeat until the run exits 0. Log which papers became stubs.

- [ ] **Step 5: Verify + manifest test still green + commit**

```bash
& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/test_recursion_manifest.py -q
git add references/recursion
git commit -m "Fetch recursion reference corpus (papers, web captures, stubs)"
```

---

### Task 5: Recursion graph builder (TDD)

**Files:**
- Create: `scripts/build_recursion_graph.py`
- Modify: `tests/test_recursion_graph.py` (append)

- [ ] **Step 1: Write the failing test**

Append to `tests/test_recursion_graph.py`:

```python
from build_recursion_graph import collect_fragments


def test_collect_fragments_unions_outline_and_refs(tmp_path):
    work = tmp_path / ".work"; work.mkdir()
    (work / "frag-rc01.json").write_text(
        '{"nodes":[{"id":"concept_ivc","label":"IVC"}],'
        '"edges":[{"source":"rc01_x","target":"concept_ivc","relation":"defines"}]}',
        encoding="utf-8")
    (work / "frag-ref-01.json").write_text(
        '{"nodes":[{"id":"concept_ivc","label":"IVC dup"},{"id":"rc01_x","label":"X"}],'
        '"edges":[{"source":"rc01_x","target":"ghost","relation":"cites"}]}',
        encoding="utf-8")
    merged = collect_fragments(work)
    assert sorted(n["id"] for n in merged["nodes"]) == ["concept_ivc", "rc01_x"]
    assert merged["nodes"][0]["label"] == "IVC"     # first wins
    assert len(merged["edges"]) == 1                # dangling 'ghost' dropped
```

- [ ] **Step 2: Run test to verify it fails**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/test_recursion_graph.py -k collect_fragments -v`
Expected: FAIL (`ModuleNotFoundError: build_recursion_graph`).

- [ ] **Step 3: Write the builder**

Create `scripts/build_recursion_graph.py`:

```python
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
    gods = god_nodes(G); surprises = surprising_connections(G, communities)
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
    g = _load(RG_GRAPH); comms: dict[str, list] = {}
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
        print(f"no {labels_path}"); return 1
    labels = {int(k): v for k, v in _load(labels_path).items()}
    g = _load(RG_GRAPH)
    communities: dict[int, list] = {}
    for n in g["nodes"]:
        c = n.get("community")
        if c is not None:
            communities.setdefault(int(c), []).append(n["id"])
    G = json_graph.node_link_graph(g, edges="links")
    cohesion = score_all(G, communities); gods = god_nodes(G)
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
    sub.add_parser("build"); sub.add_parser("relabel")
    args = ap.parse_args()
    return cmd_build() if args.cmd == "build" else cmd_relabel()


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests + import check**

Run: `& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/test_recursion_graph.py -v` → all pass.
Run: `python -c "from graphify.build import build_from_json; print('ok')"` → `ok`.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_recursion_graph.py tests/test_recursion_graph.py
git commit -m "Add recursion-graph builder (reuses merge_extraction)"
```

---

### Task 6: Deep extraction (outline chapters + references)

**Files:**
- Create (runtime, git-ignored): `recursion-graph/.work/frag-rc01..03.json`, `frag-ref-NN.json`

- [ ] **Step 1: Seed the 9 overlap fragments (reuse, no extraction)**

For each overlap, copy its existing deep fragment into the recursion work dir under the ref id it has in the recursion manifest (so node ids carry over and merge):
```bash
# example: if nova is recursion ref id 01, reuse main fragment frag-17
cp graphify-out/.deepen/frag-17.json recursion-graph/.work/frag-ref-01.json   # nova
# ... repeat per the overlap table, mapping each recursion ref id -> main frag ...
```
(The node ids in these fragments are already `concept_*`/`ref-NN_*`; they merge by id with the new fragments.)

- [ ] **Step 2: Dispatch one subagent per outline chapter (3)**

For `recursion-graph/.work/rc01.md` (and rc02, rc03), dispatch a subagent with the book-chapter extraction prompt adapted for the recursion outline: read the chapter, extract 20-35 nodes (concepts, schemes, the subsection claims, cited works), `concept_<kebab>` shared ids aligned to the existing graphs (e.g. `concept_ivc`, `concept_pcd`, `concept_folding-scheme`, `concept_accumulation`, `concept_nova`), chapter artifacts `rc<NN>_<kebab>`, `source_file="recursion/recursion-outline.md"`, `source_location="Recursion Chapter N"`, `file_type="document"`; write JSON to `recursion-graph/.work/frag-rcNN.json`.

- [ ] **Step 3: Dispatch one subagent per NEW reference (deep-mine papers, lighter for web)**

For each non-reuse `paper`/`web`/`stub` entry whose file exists, dispatch a deep-extraction subagent (paper: full read, 15-25 nodes of constructions/theorems/assumptions/citations; web: 8-15 nodes; stub: 2-4 nodes from the citation), `concept_<kebab>` shared ids, artifacts `ref-<NN>_<kebab>`, `source_file` = the entry's `file`, `file_type` = paper/document, writing `recursion-graph/.work/frag-ref-NN.json`. Dispatch in batches of ~6. Skip the 9 reuse ids (already seeded in Step 1).

- [ ] **Step 4: Validate fragments**

```bash
python - <<'EOF'
import json, glob, pathlib
n=e=0
for f in sorted(glob.glob("recursion-graph/.work/frag-*.json")):
    d=json.loads(pathlib.Path(f).read_text(encoding="utf-8"))
    assert isinstance(d.get("nodes"),list) and isinstance(d.get("edges"),list), f
    n+=len(d["nodes"]); e+=len(d["edges"])
print(len(glob.glob("recursion-graph/.work/frag-*.json")),"fragments,",n,"nodes,",e,"edges")
EOF
```
Expected: (3 outline + 9 reuse + N new) fragments; re-dispatch any missing/tiny (<5 nodes) source.

---

### Task 7: Build the recursion graph + label + commit

**Files:**
- Create: `recursion-graph/graph.json`, `GRAPH_REPORT.md`, `graph.html`, `obsidian/`, `cost.json`

- [ ] **Step 1: Build (system python)**

Run: `python scripts/build_recursion_graph.py build`
Expected: `built recursion-graph: N nodes, M edges, K communities`; `communities.json` written. N roughly 600-900.

- [ ] **Step 2: Label communities**

Read `recursion-graph/.work/communities.json`; write 2-5 word names to `recursion-graph/.work/labels.json`; run `python scripts/build_recursion_graph.py relabel`.

- [ ] **Step 3: Record measured extraction cost**

Write `recursion-graph/cost.json` with a run entry recording the measured subagent token total from this session (sum the subagent_tokens reported during Task 6).

- [ ] **Step 4: Verify + commit**

```bash
& "C:\sevenlayer\.venv\Scripts\python.exe" -m pytest tests/ -q
python -c "import json; g=json.load(open('recursion-graph/graph.json',encoding='utf-8')); print('recursion-graph:',len(g['nodes']),'nodes',len(g['links']),'links')"
git add recursion-graph/graph.json recursion-graph/GRAPH_REPORT.md recursion-graph/graph.html recursion-graph/obsidian recursion-graph/cost.json
git add -f recursion-graph/.work/labels.json
git commit -m "Build deep recursion knowledge graph from outline + references"
```

- [ ] **Step 5: Report to the user**

Summarize: corpus counts (papers/web/stubs/reuse, how many fetched vs stubbed), recursion-graph node/edge/community counts, top god nodes, a couple of cross-source surprising connections, and measured cost. Note deliverables (`references/recursion/`, `recursion/recursion-outline.md`, `recursion-graph/`). Offer to push and to compare this graph to graph 1 / the book graph.
