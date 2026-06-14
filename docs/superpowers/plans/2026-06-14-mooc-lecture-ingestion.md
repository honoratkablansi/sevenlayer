# MOOC Lecture Ingestion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A reusable `scripts/ingest_lecture.py` that ingests a video lecture (YouTube transcript + course slide PDF) into the `master-graph/` knowledge graph, validated on Lecture 1 of the Berkeley ZKP MOOC.

**Architecture:** A new module with pure helpers (transcript→text, chunking, slide-PDF→text, manifest, paths) that are TDD-tested, plus two CLI commands: `fetch` (venv Python — pulls transcript via `youtube-transcript-api` + slide PDF via `scrapling`, writes artifacts under `references/mooc/<label>/` and an extraction job) and `merge` (system Python — folds concept fragments into the master graph via the existing graphify pipeline). Concept extraction between the two is done by subagents reading the stored artifacts. All network/graphify/pypdf imports are lazy so the module imports under the venv for tests.

**Tech Stack:** Python 3.10+, pytest (venv), `youtube-transcript-api` + `scrapling` (venv, fetch), `graphify` + `networkx` + `pypdf` (system, merge/extract). Reuses `scripts/fetch_references.fetch_paper`, `scripts/deepen_pdfs.merge_fragment`, `scripts/build_master_graph.{_load,_export,_dump_communities,load_fragment_blob,INPUTS,MASTER_GRAPH}`.

**Conventions for every commit step:** run from `C:\sevenlayer`. Do **not** add a `Co-Authored-By` trailer. Tests run under the venv: `.\.venv\Scripts\python.exe -m pytest`. Real `fetch` runs under the venv (has scrapling + youtube-transcript-api); real `merge` runs under the system Python `C:\Python314\python.exe` (has graphify + networkx + pypdf).

---

## Phase 0 — Scaffold + dependencies

### Task 0: Module + test skeleton, venv deps, gitignore

**Files:**
- Create: `scripts/ingest_lecture.py`
- Create: `tests/test_ingest_lecture.py`
- Modify: `.gitignore`

- [ ] **Step 1: Install the two pure-python deps into the venv (test interpreter)**

Run: `.\.venv\Scripts\python.exe -m pip install --quiet pypdf youtube-transcript-api`
Expected: completes (both are pure-python; `youtube-transcript-api` may already be present).

- [ ] **Step 2: Create `scripts/ingest_lecture.py`**

```python
"""Ingest a video lecture (YouTube transcript + course slide PDF) into the
master knowledge graph.

Two interpreters (the repo's dual setup):
  - `fetch` needs the venv Python (scrapling + youtube-transcript-api).
  - `merge` needs the system Python (graphify + networkx + pypdf).
All network/graphify/pypdf imports are lazy so this module imports under the
venv for tests.

Usage (from repo root):
    .\\.venv\\Scripts\\python.exe scripts/ingest_lecture.py fetch \\
        --video uchjTIlPzFo \\
        --slides https://rdi.berkeley.edu/zk-learning/assets/Lecture1-2023-slides.pdf \\
        --label lecture01 --title "Introduction and History of ZKP"
    # ... dispatch extraction subagents -> master-graph/.mooc/frag-lecture01-*.json ...
    python scripts/ingest_lecture.py merge --label lecture01
"""
from __future__ import annotations

import json
import math
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MOOC_DIR = REPO / "references" / "mooc"
MOOC_MANIFEST = MOOC_DIR / "manifest.json"
MOOC_WORK = REPO / "master-graph" / ".mooc"


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _dump_json(path, obj) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
```

- [ ] **Step 3: Create `tests/test_ingest_lecture.py`**

```python
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import ingest_lecture as m  # noqa: E402
import pytest  # noqa: E402
```

- [ ] **Step 4: Add the mooc scratch dir to `.gitignore`**

Append to `.gitignore` (after the existing `master-graph/.thaler/` line):

```
master-graph/.mooc/
```

- [ ] **Step 5: Verify the module imports under the venv**

Run: `.\.venv\Scripts\python.exe -m pytest tests/test_ingest_lecture.py -q`
Expected: `no tests ran` (collection succeeds, 0 tests) — confirms the import works.

- [ ] **Step 6: Commit**

```bash
git add scripts/ingest_lecture.py tests/test_ingest_lecture.py .gitignore
git commit -m "Scaffold ingest_lecture module + test skeleton"
```

---

## Phase 1 — Pure helpers (TDD)

### Task 1: `transcript_to_text`

**Files:**
- Modify: `scripts/ingest_lecture.py`
- Test: `tests/test_ingest_lecture.py`

- [ ] **Step 1: Write the failing test**

```python
def test_transcript_to_text_joins_and_inserts_markers():
    segs = [{"start": 0, "dur": 2, "text": "Hi"},
            {"start": 65, "dur": 2, "text": "world"}]
    assert m.transcript_to_text(segs, marker_every=1) == "[00:00] Hi [01:05] world"


def test_transcript_to_text_no_markers_and_strips():
    segs = [{"start": 0, "text": "a\n"}, {"start": 1, "text": " b "}]
    assert m.transcript_to_text(segs, marker_every=0) == "a b"
```

- [ ] **Step 2: Run to verify it fails**

Run: `.\.venv\Scripts\python.exe -m pytest tests/test_ingest_lecture.py -k transcript_to_text -v`
Expected: FAIL — `AttributeError: module 'ingest_lecture' has no attribute 'transcript_to_text'`

- [ ] **Step 3: Implement**

Add to `scripts/ingest_lecture.py`:

```python
def transcript_to_text(segments: list[dict], marker_every: int = 40) -> str:
    """Join transcript segments into clean prose. When marker_every > 0, insert a
    [mm:ss] timestamp marker before every marker_every-th segment (supports chunked
    extraction)."""
    out: list[str] = []
    for i, s in enumerate(segments):
        if marker_every and i % marker_every == 0:
            t = int(s.get("start", 0))
            out.append(f"[{t // 60:02d}:{t % 60:02d}]")
        txt = (s.get("text") or "").replace("\n", " ").strip()
        if txt:
            out.append(txt)
    return " ".join(out)
```

- [ ] **Step 4: Run to verify it passes**

Run: `.\.venv\Scripts\python.exe -m pytest tests/test_ingest_lecture.py -k transcript_to_text -v`
Expected: PASS (2 tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/ingest_lecture.py tests/test_ingest_lecture.py
git commit -m "ingest_lecture: transcript_to_text"
```

---

### Task 2: `chunk_text`

**Files:**
- Modify: `scripts/ingest_lecture.py`
- Test: `tests/test_ingest_lecture.py`

- [ ] **Step 1: Write the failing test**

```python
def test_chunk_text_splits_evenly_without_losing_words():
    text = " ".join(str(i) for i in range(10))
    chunks = m.chunk_text(text, 3)
    assert len(chunks) == 3
    assert " ".join(chunks).split() == text.split()  # no words lost or reordered


def test_chunk_text_edge_cases():
    assert m.chunk_text("", 3) == []
    assert m.chunk_text("one two", 5) == ["one", "two"]  # fewer words than chunks
```

- [ ] **Step 2: Run to verify it fails**

Run: `.\.venv\Scripts\python.exe -m pytest tests/test_ingest_lecture.py -k chunk_text -v`
Expected: FAIL — attribute not defined.

- [ ] **Step 3: Implement**

```python
def chunk_text(text: str, n_chunks: int) -> list[str]:
    """Split text into up to n_chunks roughly-equal chunks on whitespace
    boundaries (never mid-word). Empty text -> []."""
    words = text.split()
    if not words:
        return []
    n_chunks = max(1, n_chunks)
    size = math.ceil(len(words) / n_chunks)
    return [" ".join(words[i:i + size]) for i in range(0, len(words), size)]
```

- [ ] **Step 4: Run to verify it passes**

Run: `.\.venv\Scripts\python.exe -m pytest tests/test_ingest_lecture.py -k chunk_text -v`
Expected: PASS (2 tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/ingest_lecture.py tests/test_ingest_lecture.py
git commit -m "ingest_lecture: chunk_text"
```

---

### Task 3: `lecture_paths` + manifest helpers

**Files:**
- Modify: `scripts/ingest_lecture.py`
- Test: `tests/test_ingest_lecture.py`

- [ ] **Step 1: Write the failing test**

```python
def test_lecture_paths_layout():
    p = m.lecture_paths("lecture01")
    assert p["slides"].name == "slides.pdf"
    assert p["transcript_txt"].name == "transcript.txt"
    assert p["transcript_json"].name == "transcript.json"
    assert p["dir"].name == "lecture01"
    assert "references/mooc" in str(p["dir"]).replace("\\", "/")


def test_manifest_upsert_is_idempotent_by_label(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "MOOC_DIR", tmp_path)
    monkeypatch.setattr(m, "MOOC_MANIFEST", tmp_path / "manifest.json")
    m.manifest_upsert({"label": "lecture01", "title": "A"})
    m.manifest_upsert({"label": "lecture01", "title": "B"})  # replaces
    m.manifest_upsert({"label": "lecture02", "title": "C"})
    entries = m.load_manifest()
    assert [e["label"] for e in entries] == ["lecture01", "lecture02"]
    assert entries[0]["title"] == "B"
```

- [ ] **Step 2: Run to verify it fails**

Run: `.\.venv\Scripts\python.exe -m pytest tests/test_ingest_lecture.py -k "lecture_paths or manifest" -v`
Expected: FAIL — attributes not defined.

- [ ] **Step 3: Implement**

```python
def lecture_paths(label: str) -> dict:
    d = MOOC_DIR / label
    return {"dir": d, "transcript_json": d / "transcript.json",
            "transcript_txt": d / "transcript.txt", "slides": d / "slides.pdf"}


def load_manifest() -> list[dict]:
    if MOOC_MANIFEST.exists():
        return json.loads(MOOC_MANIFEST.read_text(encoding="utf-8"))
    return []


def manifest_upsert(entry: dict) -> list[dict]:
    """Insert or replace (by 'label') a lecture entry; persist sorted by label."""
    entries = [e for e in load_manifest() if e.get("label") != entry["label"]]
    entries.append(entry)
    entries.sort(key=lambda e: e["label"])
    MOOC_DIR.mkdir(parents=True, exist_ok=True)
    MOOC_MANIFEST.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return entries
```

- [ ] **Step 4: Run to verify it passes**

Run: `.\.venv\Scripts\python.exe -m pytest tests/test_ingest_lecture.py -k "lecture_paths or manifest" -v`
Expected: PASS (2 tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/ingest_lecture.py tests/test_ingest_lecture.py
git commit -m "ingest_lecture: lecture_paths + manifest helpers"
```

---

### Task 4: `slide_pdf_pages`

**Files:**
- Modify: `scripts/ingest_lecture.py`
- Test: `tests/test_ingest_lecture.py`

- [ ] **Step 1: Write the failing test**

```python
def test_slide_pdf_pages_one_entry_per_page(tmp_path):
    import pypdf
    w = pypdf.PdfWriter()
    w.add_blank_page(width=200, height=200)
    w.add_blank_page(width=200, height=200)
    pdf = tmp_path / "deck.pdf"
    with open(pdf, "wb") as f:
        w.write(f)
    pages = m.slide_pdf_pages(pdf)
    assert len(pages) == 2
    assert all(isinstance(p, str) for p in pages)
```

- [ ] **Step 2: Run to verify it fails**

Run: `.\.venv\Scripts\python.exe -m pytest tests/test_ingest_lecture.py -k slide_pdf_pages -v`
Expected: FAIL — attribute not defined.

- [ ] **Step 3: Implement**

```python
def slide_pdf_pages(path) -> list[str]:
    """One extracted-text string per PDF page (lazy pypdf import)."""
    import pypdf
    reader = pypdf.PdfReader(str(path))
    return [(p.extract_text() or "") for p in reader.pages]
```

- [ ] **Step 4: Run to verify it passes**

Run: `.\.venv\Scripts\python.exe -m pytest tests/test_ingest_lecture.py -k slide_pdf_pages -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/ingest_lecture.py tests/test_ingest_lecture.py
git commit -m "ingest_lecture: slide_pdf_pages"
```

---

## Phase 2 — Fetch (network) + cmd_fetch

### Task 5: `fetch_transcript` + `fetch_slides` + `cmd_fetch`

**Files:**
- Modify: `scripts/ingest_lecture.py`
- Test: `tests/test_ingest_lecture.py`

- [ ] **Step 1: Write the failing test (cmd_fetch wiring, network monkeypatched)**

```python
def test_cmd_fetch_writes_artifacts_and_manifest(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "MOOC_DIR", tmp_path / "references" / "mooc")
    monkeypatch.setattr(m, "MOOC_MANIFEST", tmp_path / "references" / "mooc" / "manifest.json")
    monkeypatch.setattr(m, "MOOC_WORK", tmp_path / ".mooc")
    monkeypatch.setattr(m, "REPO", tmp_path)
    monkeypatch.setattr(m, "fetch_transcript",
                        lambda vid: [{"start": 0, "dur": 1, "text": "hello zk"}])
    monkeypatch.setattr(m, "fetch_slides", lambda url, dest: dest.write_bytes(b"%PDF-1.4 x") or "fetcher-chrome")
    rc = m.cmd_fetch("vid123", "http://x/s.pdf", "lecture01", "Intro")
    assert rc == 0
    paths = m.lecture_paths("lecture01")
    assert paths["transcript_json"].exists()
    assert "hello zk" in paths["transcript_txt"].read_text(encoding="utf-8")
    entry = m.load_manifest()[0]
    assert entry["label"] == "lecture01" and entry["video_id"] == "vid123"
    job = m._load(m.MOOC_WORK / "lecture01-job.json")
    assert job["source_file"] == "references/mooc/lecture01/slides.pdf"
```

(Note: the test's `fetch_slides` stub must accept `(url, dest)` and write the bytes; the real one returns a `how` string — the stub returns `"fetcher-chrome"`.)

- [ ] **Step 2: Run to verify it fails**

Run: `.\.venv\Scripts\python.exe -m pytest tests/test_ingest_lecture.py -k cmd_fetch -v`
Expected: FAIL — `cmd_fetch` / `fetch_transcript` / `fetch_slides` not defined.

- [ ] **Step 3: Implement the fetch helpers and `cmd_fetch`**

```python
def fetch_transcript(video_id: str) -> list[dict]:
    """Return [{start, dur, text}], preferring a manually-created English track
    over an auto-generated one. Tolerates both new and classic
    youtube-transcript-api shapes."""
    from youtube_transcript_api import YouTubeTranscriptApi
    try:
        api = YouTubeTranscriptApi()
        listing = api.list(video_id)
        try:
            tr = listing.find_manually_created_transcript(["en"])
        except Exception:  # noqa: BLE001
            tr = listing.find_generated_transcript(["en"])
        fetched = tr.fetch()
        return [{"start": round(float(s.start), 3),
                 "dur": round(float(s.duration), 3), "text": s.text} for s in fetched]
    except Exception:  # noqa: BLE001 - fall back to the classic classmethod API
        data = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        return [{"start": d["start"], "dur": d.get("duration", 0), "text": d["text"]}
                for d in data]


def fetch_slides(url: str, dest: Path) -> str:
    """Fetch a slide PDF via the hardened paper fetcher (curl_cffi -> Camoufox
    stealth on a Cloudflare wall); verify %PDF- magic; atomic write. Returns how."""
    import sys as _sys
    _sys.path.insert(0, str(REPO / "scripts"))
    from fetch_references import fetch_paper
    data, how = fetch_paper(url)
    if data is None:
        raise RuntimeError(f"failed to fetch slides PDF: {url}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(dest)
    return how


def cmd_fetch(video_id: str, slides_url: str, label: str, title: str) -> int:
    paths = lecture_paths(label)
    paths["dir"].mkdir(parents=True, exist_ok=True)
    segments = fetch_transcript(video_id)
    _dump_json(paths["transcript_json"], segments)
    text = transcript_to_text(segments)
    paths["transcript_txt"].write_text(text, encoding="utf-8")
    how = fetch_slides(slides_url, paths["slides"])
    manifest_upsert({
        "label": label, "title": title, "video_id": video_id,
        "video_url": f"https://www.youtube.com/watch?v={video_id}",
        "slides_url": slides_url, "transcript_segments": len(segments),
        "transcript_words": len(text.split()), "slides_fetched_via": how,
        "license": "CC", "course": "Berkeley ZKP MOOC",
    })
    MOOC_WORK.mkdir(parents=True, exist_ok=True)
    _dump_json(MOOC_WORK / f"{label}-job.json", {
        "label": label, "title": title,
        "slides": f"references/mooc/{label}/slides.pdf",
        "transcript": f"references/mooc/{label}/transcript.txt",
        "source_file": f"references/mooc/{label}/slides.pdf",
        "frag_glob": f"master-graph/.mooc/frag-{label}-*.json",
    })
    print(f"fetched {label}: {len(segments)} segments ({len(text.split())} words); "
          f"slides via {how} -> {paths['dir']}")
    return 0
```

- [ ] **Step 4: Run to verify it passes**

Run: `.\.venv\Scripts\python.exe -m pytest tests/test_ingest_lecture.py -k cmd_fetch -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/ingest_lecture.py tests/test_ingest_lecture.py
git commit -m "ingest_lecture: fetch_transcript + fetch_slides + cmd_fetch"
```

---

## Phase 3 — Merge + CLI

### Task 6: `cmd_merge` + `main()`

**Files:**
- Modify: `scripts/ingest_lecture.py`

- [ ] **Step 1: Implement `cmd_merge` and `main`**

Add to `scripts/ingest_lecture.py`:

```python
def cmd_merge(label: str) -> int:
    import glob
    import sys as _sys
    _sys.path.insert(0, str(REPO / "scripts"))
    import build_master_graph as bmg
    from deepen_pdfs import merge_fragment
    from networkx.readwrite import json_graph

    graph = bmg._load(bmg.MASTER_GRAPH)
    before = (len(graph["nodes"]), len(graph["links"]))
    frags = sorted(glob.glob(str(MOOC_WORK / f"frag-{label}-*.json")))
    if not frags:
        print(f"no fragments at {MOOC_WORK / ('frag-' + label + '-*.json')}")
        return 1
    merged = 0
    for f in frags:
        blob = bmg._load(Path(f))
        try:
            frag = bmg.load_fragment_blob(blob)
        except ValueError as exc:
            print(f"  bad fragment {f}: {exc}, skipped")
            continue
        merge_fragment(graph, frag)
        merged += 1
    if not merged:
        print("no valid fragments merged")
        return 1
    G = json_graph.node_link_graph(graph, edges="links")
    stats = bmg._export(G, None, None, len(bmg.INPUTS))
    bmg._dump_communities()
    print(f"merged {merged} fragments: nodes {before[0]}->{stats['nodes']}, "
          f"edges {before[1]}->{stats['edges']}, communities {stats['communities']}")
    return 0


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch")
    f.add_argument("--video", required=True)
    f.add_argument("--slides", required=True)
    f.add_argument("--label", required=True)
    f.add_argument("--title", default="")
    mg = sub.add_parser("merge")
    mg.add_argument("--label", required=True)
    args = ap.parse_args()
    if args.cmd == "fetch":
        return cmd_fetch(args.video, args.slides, args.label, args.title)
    return cmd_merge(args.label)


if __name__ == "__main__":
    import sys
    sys.exit(main())
```

- [ ] **Step 2: Confirm the module still imports under the venv (lazy imports intact)**

Run: `.\.venv\Scripts\python.exe -c "import sys; sys.path.insert(0,'scripts'); import ingest_lecture; print('import ok')"`
Expected: `import ok`

- [ ] **Step 3: Smoke-test the CLI surface and merge guard**

Run: `python scripts/ingest_lecture.py --help`
Expected: usage lists `fetch` and `merge`.

Run: `python scripts/ingest_lecture.py merge --label nope 2>&1`
Expected: prints `no fragments at ...master-graph\.mooc\frag-nope-*.json` and exits non-zero (must NOT crash).

- [ ] **Step 4: Full suite**

Run: `.\.venv\Scripts\python.exe -m pytest tests/ -q`
Expected: all pass (existing suite + new `test_ingest_lecture.py`).

- [ ] **Step 5: Commit**

```bash
git add scripts/ingest_lecture.py
git commit -m "ingest_lecture: cmd_merge + CLI"
```

---

## Phase 4 — Run on Lecture 1 (orchestration runbook)

This phase has no new code. It runs the pipeline end-to-end on Lecture 1.

### Task 7: Fetch Lecture 1 artifacts

- [ ] **Step 1: Fetch (venv Python — has scrapling + youtube-transcript-api)**

Run:
```
.\.venv\Scripts\python.exe scripts/ingest_lecture.py fetch --video uchjTIlPzFo --slides https://rdi.berkeley.edu/zk-learning/assets/Lecture1-2023-slides.pdf --label lecture01 --title "Introduction and History of ZKP"
```
Expected: prints `fetched lecture01: ~2134 segments (~16459 words); slides via fetcher-... -> ...references\mooc\lecture01`. Creates `references/mooc/lecture01/{transcript.json,transcript.txt,slides.pdf}`, `references/mooc/manifest.json`, and `master-graph/.mooc/lecture01-job.json`.

- [ ] **Step 2: Sanity-check the artifacts**

Run: `python -c "import pypdf; print('slide pages:', len(pypdf.PdfReader('references/mooc/lecture01/slides.pdf').pages))"`
Expected: a page count (> 10). And confirm `references/mooc/lecture01/transcript.txt` is non-trivial: `python -c "print(len(open('references/mooc/lecture01/transcript.txt',encoding='utf-8').read().split()),'words')"` → ~16k.

### Task 8: Extract concept fragments (Agent tool)

Dispatch THREE extraction subagents. Each writes a fragment to `master-graph/.mooc/frag-lecture01-*.json` in the shape `{"nodes":[{id,label,file_type,source_file,source_location}],"edges":[...]}` with `source_file = "references/mooc/lecture01/slides.pdf"`. Reuse standard `concept_<kebab>` ids: concept_zero-knowledge-proof, concept_interactive-proof, concept_gmr, concept_simulation-paradigm, concept_soundness, concept_completeness, concept_knowledge-soundness, concept_sigma-protocol, concept_commitment-scheme, concept_graph-non-isomorphism, concept_np, concept_polynomial-time, concept_prover, concept_verifier, concept_witness. Otherwise `concept_<kebab-of-label>`.

- [ ] **Step 1: Slides subagent** — prompt:
> Read `references/mooc/lecture01/slides.pdf` (Berkeley ZKP MOOC Lecture 1, "Introduction and History of ZKP", by Shafi Goldwasser) via pypdf in page sub-ranges (`python -c "import pypdf; r=pypdf.PdfReader('references/mooc/lecture01/slides.pdf'); print('\n'.join(p.extract_text() for p in r.pages[:15]))"` then the rest). If a page's text is empty/diagram-only, read that page as an image with the Read tool (vision). Extract the structured concept skeleton: named protocols, definitions, theorems, problems. Write `master-graph/.mooc/frag-lecture01-slides.json` with `{"nodes":[...],"edges":[...]}`, every node `source_file="references/mooc/lecture01/slides.pdf"`, `source_location="ZKP MOOC Lecture 1 (slides)"`, reusing the standard concept ids listed above. Report node/edge counts.

- [ ] **Step 2: Transcript subagents (two)** — read `references/mooc/lecture01/transcript.txt`. Agent A takes the first half, Agent B the second half (split on the `[mm:ss]` markers). Prompt each:
> Read your half of `references/mooc/lecture01/transcript.txt` (Goldwasser's lecture). Extract concepts AND especially the **narrative relationships**: history (who/when/why ZKP was invented), motivation, intuition, and how ideas connect — these become edges the slides don't carry. Write `master-graph/.mooc/frag-lecture01-transcript-<A|B>.json` with `{"nodes":[...],"edges":[...]}`, every node `source_file="references/mooc/lecture01/slides.pdf"`, `source_location="ZKP MOOC Lecture 1 (transcript)"`, reusing the standard concept ids. Report node/edge counts.

- [ ] **Step 3: Verify fragments exist and validate**

Run: `python -c "import sys,glob,json; sys.path.insert(0,'scripts'); import build_master_graph as b; [print(f, 'ok' if 'nodes' in b.load_fragment_blob(json.load(open(f,encoding='utf-8'))) else 'bad') for f in glob.glob('master-graph/.mooc/frag-lecture01-*.json')]"`
Expected: each frag file prints `ok`.

### Task 9: Merge + consolidate + report + commit

- [ ] **Step 1: Merge (system Python — has graphify)**

Run: `python scripts/ingest_lecture.py merge --label lecture01`
Expected: prints node/edge/community deltas (graph grows by the lecture's new concepts; many merge into existing ZK hubs).

- [ ] **Step 2: Dedup + refresh the concept report (reuse the existing pipeline)**

Run:
```
python -c "import sys; sys.path.insert(0,'scripts'); import build_master_graph as m; g=m._load(m.MASTER_GRAPH); a=m.build_alias_map(g); m.validate_alias_map(a,g); m._dump(m.WORK/'aliases.json',a); print(len(a),'aliases')"
python scripts/build_master_graph.py consolidate
python scripts/build_master_graph.py concepts
```
Expected: consolidate prints node/edge/community deltas; concepts prints the refreshed total/under/absent counts.

- [ ] **Step 3: Full test suite**

Run: `.\.venv\Scripts\python.exe -m pytest tests/ -q`
Expected: all pass.

- [ ] **Step 4: Commit (artifacts + graph; `.mooc/` scratch is gitignored)**

```bash
git add references/mooc/ master-graph/graph.json master-graph/GRAPH_REPORT.md master-graph/graph.html master-graph/obsidian master-graph/CONCEPTS_FOR_BOOK.md
git add -f master-graph/.work/aliases.json
git commit -m "Ingest ZKP MOOC Lecture 1 (Goldwasser): transcript + slides -> master graph"
```

- [ ] **Step 5: Report results**

Print a short summary: new concept count, which existing hubs were reinforced (zero-knowledge-proof, interactive-proof, GMR, simulation-paradigm), and the refreshed `CONCEPTS_FOR_BOOK.md` totals. Note that lectures 2–14 can now be ingested by re-running Tasks 7–9 with their `--video` id and `--slides` url.

---

## Self-review notes (for the implementer)

- **Spec coverage:** fetch (transcript + slides + manifest + job) = Task 5/7; pure helpers = Tasks 1–4; merge via graphify = Task 6/9; provenance under `references/mooc/` = Tasks 5/7/9; reuse `fetch_references.fetch_paper` / `merge_fragment` / `build_master_graph` = Tasks 5/6; slide-PDF-not-frames and one-fragment-set-per-lecture = Task 8; pypdf+youtube-transcript-api in venv = Task 0.
- **Interpreter discipline:** `fetch` (Task 7) MUST run under `.\.venv\Scripts\python.exe` (scrapling + youtube-transcript-api); `merge`/`consolidate`/`concepts` (Task 9) under system `python` (graphify). Tests always under the venv.
- **Type consistency:** `fetch_transcript` returns `[{start,dur,text}]`; `transcript_to_text`/`chunk_text` consume that; `fetch_slides(url, dest)->str`; `cmd_fetch`/`cmd_merge` return int rc; fragment shape `{nodes,edges}` validated by `build_master_graph.load_fragment_blob`.
- **Known limitation:** transcript-derived nodes share `source_file = slides.pdf` (one canonical lecture source) to avoid double-counting reference-support; `source_location` distinguishes slide vs transcript origin.
