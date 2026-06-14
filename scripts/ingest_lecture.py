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
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def transcript_to_text(segments: list[dict], marker_every: int = 40) -> str:
    """Join transcript segments into clean prose. When marker_every > 0, insert a
    [mm:ss] timestamp marker before every marker_every-th segment (supports chunked
    extraction)."""
    out: list[str] = []
    for i, s in enumerate(segments):
        if marker_every > 0 and i % marker_every == 0:
            t = int(s.get("start") or 0)
            out.append(f"[{t // 60:02d}:{t % 60:02d}]")
        txt = (s.get("text") or "").replace("\n", " ").strip()
        if txt:
            out.append(txt)
    return " ".join(out)


def chunk_text(text: str, n_chunks: int) -> list[str]:
    """Split text into up to n_chunks roughly-equal chunks on whitespace
    boundaries (never mid-word). Empty text -> []."""
    words = text.split()
    if not words:
        return []
    n_chunks = max(1, n_chunks)
    size = math.ceil(len(words) / n_chunks)
    return [" ".join(words[i:i + size]) for i in range(0, len(words), size)]


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
    entries.sort(key=lambda e: e.get("label", ""))
    MOOC_DIR.mkdir(parents=True, exist_ok=True)
    MOOC_MANIFEST.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return entries


def slide_pdf_pages(path) -> list[str]:
    """One extracted-text string per PDF page (lazy pypdf import)."""
    import pypdf
    reader = pypdf.PdfReader(str(path))
    return [(p.extract_text() or "") for p in reader.pages]


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
        return [{"start": d.get("start", 0), "dur": d.get("duration", 0), "text": d["text"]}
                for d in data]


def fetch_slides(url: str, dest: Path) -> str:
    """Fetch a slide PDF via the hardened paper fetcher (curl_cffi -> Camoufox
    stealth on a Cloudflare wall); verify %PDF- magic; atomic write. Returns how."""
    import sys as _sys
    scripts_dir = str(REPO / "scripts")
    if scripts_dir not in _sys.path:
        _sys.path.insert(0, scripts_dir)
    from fetch_references import fetch_paper
    data, how = fetch_paper(url)
    if data is None:
        raise RuntimeError(f"failed to fetch slides PDF: {url}")
    if data[:5] != b"%PDF-":
        raise RuntimeError(f"slides response is not a PDF: {url}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(dest)
    return how


def cmd_fetch(video_id: str, slides_url: str, label: str, title: str) -> int:
    paths = lecture_paths(label)
    paths["dir"].mkdir(parents=True, exist_ok=True)
    # Both network fetches first, so a fetch failure leaves no partial artifacts.
    segments = fetch_transcript(video_id)
    how = fetch_slides(slides_url, paths["slides"])
    text = transcript_to_text(segments)
    nwords = len(text.split())
    _dump_json(paths["transcript_json"], segments)
    paths["transcript_txt"].write_text(text, encoding="utf-8")
    manifest_upsert({
        "label": label, "title": title, "video_id": video_id,
        "video_url": f"https://www.youtube.com/watch?v={video_id}",
        "slides_url": slides_url, "transcript_segments": len(segments),
        "transcript_words": nwords, "slides_fetched_via": how,
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
    print(f"fetched {label}: {len(segments)} segments ({nwords} words); "
          f"slides via {how} -> {paths['dir']}")
    return 0
