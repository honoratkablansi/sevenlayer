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
    entries.sort(key=lambda e: e["label"])
    MOOC_DIR.mkdir(parents=True, exist_ok=True)
    MOOC_MANIFEST.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return entries
