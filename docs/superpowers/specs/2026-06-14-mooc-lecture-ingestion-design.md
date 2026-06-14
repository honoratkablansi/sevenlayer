# MOOC Lecture Ingestion: Transcript + Slides → Master Graph — Design Spec

**Date:** 2026-06-14
**Status:** Approved (brainstorm)

## Goal

Build a **reusable, parameterized pipeline** that ingests a video lecture (YouTube
transcript + course slide PDF) into the `master-graph/` knowledge graph as concept
nodes/edges. Validate it by running on **Lecture 1** of the Berkeley ZKP MOOC
("Introduction and History of ZKP", Shafi Goldwasser, CC-licensed,
`https://www.youtube.com/watch?v=uchjTIlPzFo`). The same command runs the other 13
lectures on demand.

## Background (feasibility — probed 2026-06-14)

- **Transcript:** `youtube-transcript-api` (pure-python, installed in the venv)
  pulls the full transcript reliably — **2,134 segments / 16,459 words**, with
  per-segment timestamps and speaker labels, preferring the human-made "English -
  CC" track over auto-generated. (Direct scrapling fetches of the `timedtext`
  endpoint return an empty body, so scrapling alone is **not** sufficient for the
  transcript body — it does get the page metadata and confirms the caption tracks.)
- **Slides:** the course publishes clean slide PDFs at
  `https://rdi.berkeley.edu/zk-learning/assets/Lecture1-2023-slides.pdf` (and
  `lecture2..14`), fetchable with `scrapling`. No video-frame extraction / OCR /
  ffmpeg required (none are installed).
- **Graph assembly:** reuses the proven path from the Thaler-textbook ingestion —
  concept fragments (`{nodes, edges}`, standard `concept_<kebab>` ids) →
  `deepen_pdfs.merge_fragment` → graphify re-cluster/rebuild
  (`build_master_graph._export`) → dedup + refresh `CONCEPTS_FOR_BOOK.md`.
- **Interpreters** (the repo's established dual setup): the venv
  (`.venv\Scripts\python.exe`) has `scrapling` + `youtube-transcript-api` →
  used for the `fetch` step; the system Python (`C:\Python314`) has
  `graphify` + `networkx` + `pypdf` → used for the `merge`/rebuild step.

## Decisions (locked in brainstorm)

1. **Reusable pipeline**, run on Lecture 1 now; lectures 2–14 on demand.
2. **Slides from the course PDF**, not video frames (all lectures have slide PDFs;
   ffmpeg/OCR/frame-extraction is explicitly out of scope).
3. **Reuse the existing graphify merge pipeline** (no new graph engine).
4. **One fragment set per lecture** combining slides (concept skeleton) + transcript
   (history/intuition/relationships); reuse standard `concept_<kebab>` ids so
   nodes merge into existing hubs.
5. **Commit the transcript + slide PDF** under `references/mooc/<label>/` for
   provenance and reproducibility.

## Non-goals

- No video/audio download, frame extraction, OCR, or ASR/Whisper fallback.
- No new graph engine; no change to how graphify clusters/exports.
- No automatic batch run of all 14 lectures (the pipeline supports it; this spec
  validates Lecture 1).
- Lecture slide PDFs are NOT added to the snowball `references/manifest.json` /
  `references/recursion/manifest.json` (they live in a separate `references/mooc/`
  manifest, so `_all_papers()`/snowball never touches them).

## Architecture

A new focused module `scripts/ingest_lecture.py`. Pure helpers (transcript→text,
chunking, slide-PDF→text, manifest shape, fragment validation) are unit-tested in
`tests/test_ingest_lecture.py`. Network fetches (`youtube-transcript-api`,
`scrapling`) and graphify imports stay lazy/isolated so the module imports under
the venv for tests. Concept extraction is done by subagents (Agent tool) reading
the stored artifacts; the module provides `fetch` (produce artifacts + jobs) and
`merge` (fold fragments into the graph) — extraction sits between them.

CLI:
```
python scripts/ingest_lecture.py fetch --video <id> --slides <url> \
       --label lecture01 --title "Introduction and History of ZKP"   # venv python
# ... dispatch extraction subagents -> master-graph/.mooc/frag-<label>-*.json ...
python scripts/ingest_lecture.py merge --label lecture01                # system python
```

## Components

### 1. Fetch (`cmd_fetch`, venv python)

- `fetch_transcript(video_id) -> list[dict]`: via `youtube_transcript_api`; prefer
  a manual (non-`asr`) English track, else auto. Each segment `{start, dur, text}`.
  Lazy import; network-isolated so tests can monkeypatch.
- `fetch_slides(url, dest_path)`: `scrapling` Fetcher (chrome impersonate); on a
  Cloudflare/403 wall escalate to the StealthyFetcher path (reuse the pattern in
  `fetch_references.py`); verify `%PDF-` magic; atomic write.
- Writes, under `references/mooc/<label>/`:
  - `transcript.json` — the raw timestamped segments.
  - `transcript.txt` — `transcript_to_text(...)` (clean prose with periodic
    `[mm:ss]` markers every ~N segments to support chunked extraction).
  - `slides.pdf` — the fetched deck.
- Appends/updates `references/mooc/manifest.json` with the lecture entry:
  `{label, title, video_id, video_url, slides_url, duration_s, transcript_words,
  fetched, license: "CC", course: "Berkeley ZKP MOOC"}`.
- Writes `master-graph/.mooc/<label>-job.json` describing the extraction job
  (paths to slides.pdf, transcript.txt, the target frag outputs, the lecture
  source-tag string).

### 2. Concept extraction (Agent tool, orchestration)

Per lecture, a small set of subagents read the stored artifacts and emit fragments
to `master-graph/.mooc/frag-<label>-*.json` in the standard shape
`{"nodes":[{id,label,file_type,source_file,source_location}], "edges":[...]}`:

- **Slides subagent(s):** read `slides.pdf` via `pypdf` (context-economical
  per-page sub-chunks); a **vision fallback** (Read tool on a slide page rendered
  to image) only if a page's text layer is sparse/diagram-only. Extract the
  structured skeleton: named protocols, definitions, theorems, the lecture's
  concept list.
- **Transcript subagent(s):** read `transcript.txt` in ~3–5 chunks; extract the
  narrative the slides don't carry — **history, motivation, intuition, and
  relationships between ideas** (rich source of edges). Reuse standard ids.
- All nodes set `source_file = references/mooc/<label>/slides.pdf` (so they count
  as reference-supported, like other corpus sources) and
  `source_location = "ZKP MOOC <Label>: <slide section | transcript topic>"`.
  Reuse standard `concept_<kebab>` ids (zero-knowledge-proof, interactive-proof,
  gmr, simulation-paradigm, soundness, completeness, …) so concepts merge into
  existing hubs rather than duplicating.

### 3. Merge (`cmd_merge`, system python)

- Load `master-graph/graph.json`; for each `master-graph/.mooc/frag-<label>-*.json`,
  validate via `build_master_graph.load_fragment_blob` and
  `deepen_pdfs.merge_fragment` it in (additive, dedup edges, drop dangling).
- Rebuild via `build_master_graph._export` (graphify cluster/god-nodes/report/
  html/obsidian) + `_dump_communities`.
- Print node/edge/community deltas. Dedup + report refresh are a follow-up via the
  existing `build_master_graph.py consolidate` and `concepts` commands (the
  established final step), so this module stays focused on lecture fetch+merge.

### Pure helpers (unit-tested)

- `transcript_to_text(segments, marker_every=40) -> str`
- `chunk_text(text, n_chunks) -> list[str]` (split on segment/marker boundaries)
- `slide_pdf_pages(path) -> list[str]` (lazy pypdf; one entry per page)
- `lecture_paths(label) -> dict` (artifact path helpers under references/mooc/)
- `manifest_upsert(entry)` / `load_manifest()` for `references/mooc/manifest.json`
- fragment validation reuses `build_master_graph.load_fragment_blob`

## Data flow

```
video_id  --youtube_transcript_api-->  transcript.json + transcript.txt
slides_url --scrapling-->              slides.pdf                         [fetch]
   -> references/mooc/<label>/ + references/mooc/manifest.json + .mooc/<label>-job.json

slides.pdf + transcript.txt --extraction subagents--> frag-<label>-*.json [extract]

frags --merge_fragment--> master-graph + graphify rebuild                 [merge]
   -> build_master_graph consolidate + concepts  (refresh CONCEPTS_FOR_BOOK.md)
```

## Output layout

- `references/mooc/<label>/transcript.json`, `transcript.txt`, `slides.pdf` (committed).
- `references/mooc/manifest.json` (committed; lecture provenance list).
- `scripts/ingest_lecture.py`, `tests/test_ingest_lecture.py`.
- `master-graph/.mooc/` (jobs + fragments) — gitignored scratch.
- Updated `master-graph/` artifacts + `CONCEPTS_FOR_BOOK.md` (committed).

## Error handling

- No manual caption track → use auto (`asr`); no transcript at all → fail with a
  clear message naming the video (no ASR/Whisper fallback in scope).
- Slide fetch: 403/Cloudflare → stealth-tier escalation; non-PDF body → fail clearly.
- Subagent fragment invalid/empty → skip + log; >half fail → stop the merge.
- `merge` refuses to write a 0-node graph (graphify `to_json` guard).
- `fetch` is idempotent: re-running overwrites artifacts atomically; manifest
  upsert is keyed by `label`.

## Testing (TDD)

`tests/test_ingest_lecture.py`:
- `transcript_to_text` (segment join, marker insertion, whitespace).
- `chunk_text` (n chunks, boundary preservation, short input).
- `slide_pdf_pages` on a tiny generated 1–2 page PDF fixture.
- `manifest_upsert` (insert + idempotent update by label; shape).
- fragment validation (nested/bare/invalid).

Network fetches and graphify rebuild stay behind lazy imports / isolation and are
exercised by the real Lecture-1 run, not unit tests.

**Test interpreter dependency:** `pytest` runs under the venv, and the
`slide_pdf_pages` test needs `pypdf` — which the venv currently lacks (only the
system Python has it). The plan installs `pypdf` into the venv (pure-python,
alongside `youtube-transcript-api`). `youtube-transcript-api` and `scrapling`
imports in the module are lazy so the rest of the suite imports cleanly.

## Cost

Per lecture: transcript (free) + slides fetch (free) + ~3–6 extraction subagents
(modest tokens) + graphify rebuild (no API). Lecture 1 is small. All 14 lectures
≈ 14× the extraction.

## Risks

- **Transcript availability** varies per video → manual/auto fallback; honest
  failure if neither exists.
- **YouTube datacenter-IP blocking** of `youtube-transcript-api` → if it returns a
  block, fall back to scrapling-StealthyFetcher fetching the `timedtext` URL inside
  a real browser session. (L1 succeeded on the first try.)
- **Slide PDF text layer** may be sparse on diagram-heavy decks → vision fallback
  on those pages.
- **Vocabulary drift** vs existing graph → extraction subagents instructed to reuse
  standard `concept_*` ids; the dedup pass absorbs residual variants.
- **graphify API drift** → pinned/verified calls, reused from the existing pipeline.
