#!/usr/bin/env python3
"""Stage 1: resolve a concept's stratum, prerequisites, and depth from MATH_FOUNDATIONS.md.

Parses the stratum tables and returns a concept_brief. Pure-Python (no graphify import),
so it runs under any interpreter.
"""
import json
import re
import sys
from pathlib import Path

ROW_RE = re.compile(r"^\|(.+)\|\s*$")
STRATUM_RE = re.compile(r"^###\s+Stratum\s+\d+\s+[—-]\s+(.*)$")


def parse_strata(md_text: str) -> list[dict]:
    rows: list[dict] = []
    stratum = None
    for raw in md_text.splitlines():
        line = raw.strip()
        m = STRATUM_RE.match(line)
        if m:
            stratum = m.group(1).strip()
            continue
        rm = ROW_RE.match(line)
        if not rm:
            continue
        cols = [c.strip() for c in rm.group(1).split("|")]
        if len(cols) != 4:
            continue
        concept, first_needed, depth, builds_on = cols
        if concept.lower() == "concept" or set(concept) <= {"-", ":"} or not concept:
            continue  # header or separator row
        prereqs = [p.strip() for p in re.split(r"[;,]", builds_on)
                   if p.strip() and p.strip() != "—"]
        rows.append({
            "stratum": stratum, "concept": concept, "first_needed": first_needed,
            "depth": depth, "prerequisites": prereqs,
        })
    return rows


def resolve(concept: str, rows: list[dict]) -> dict | None:
    cl = concept.lower()
    for r in rows:  # exact first
        if cl == r["concept"].lower():
            return r
    for r in rows:  # substring fallback
        if cl in r["concept"].lower():
            return r
    return None


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: resolve_deps.py <MATH_FOUNDATIONS.md> <concept>", file=sys.stderr)
        return 2
    rows = parse_strata(Path(argv[1]).read_text(encoding="utf-8"))
    brief = resolve(argv[2], rows)
    if brief is None:
        print(json.dumps({"error": f"concept not found: {argv[2]}"}))
        return 1
    print(json.dumps(brief, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
