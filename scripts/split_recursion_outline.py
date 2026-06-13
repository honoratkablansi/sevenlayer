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
