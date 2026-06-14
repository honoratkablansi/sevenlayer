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
