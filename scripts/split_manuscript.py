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
