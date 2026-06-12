#!/usr/bin/env python3
"""Mechanical lint for an llm-wiki. Optional accelerator; prose lint is canonical.
Checks: broken [[wikilinks]], orphan pages, missing frontmatter, un-cited claims.
Usage: python3 lint.py <wiki-root>
"""
import re, sys, pathlib

LINK = re.compile(r"\[\[([^\]]+)\]\]")
SKIP_STEMS = {"_index", "index", "overview", "log"}

def _target(raw):  # [[Page|alias]] / [[Page#heading]] -> "Page"
    return raw.split("|")[0].split("#")[0].strip()

def _has_frontmatter(text):
    return text.startswith("---") and "\n---" in text[3:]

def _ftype(text):
    if not _has_frontmatter(text): return None
    fm = text[3:text.index("\n---", 3)]
    m = re.search(r"^type:\s*(\S+)", fm, re.M)
    return m.group(1) if m else None

def lint(root):
    root = pathlib.Path(root)
    pages = list((root/"wiki").rglob("*.md"))
    # Obsidian resolves [[wikilinks]] case-insensitively, so match on lowercased stems.
    stems = {p.stem.lower() for p in pages}
    inbound = {p.stem.lower(): 0 for p in pages}
    findings = {"broken_links": [], "orphans": [], "missing_frontmatter": [], "unsourced_claims": []}
    for p in pages:
        text = p.read_text(encoding="utf-8")
        ftype = _ftype(text)
        # index/_index/overview/log are navigation scaffolding: exempt them from the
        # frontmatter and broken-link checks, but still count their outbound links.
        is_scaffold = p.stem.lower() in SKIP_STEMS
        if ftype is None and not is_scaffold:
            findings["missing_frontmatter"].append((str(p), p.stem))
        for m in LINK.finditer(text):
            raw_tgt = _target(m.group(1))
            tgt = raw_tgt.lower()
            if tgt in stems and tgt != p.stem.lower():
                inbound[tgt] = inbound.get(tgt, 0) + 1
            elif tgt not in stems and not is_scaffold:
                findings["broken_links"].append((str(p), raw_tgt))
        if ftype in ("concept", "entity"):
            for line in text.splitlines():
                s = line.strip()
                if s.startswith("- ") and "^[" not in s and "[[" not in s and "<!--" not in s:
                    findings["unsourced_claims"].append((str(p), s[:60]))
    for p in pages:
        if p.stem.lower() in SKIP_STEMS or _ftype(p.read_text(encoding="utf-8")) == "map":
            continue
        if inbound.get(p.stem.lower(), 0) == 0:
            findings["orphans"].append((str(p), p.stem))
    return findings

def main(argv):
    if len(argv) != 2:
        print("usage: lint.py <wiki-root>"); return 2
    f = lint(argv[1]); total = sum(len(v) for v in f.values())
    for k, items in f.items():
        if items:
            print(f"\n[{k}] ({len(items)})")
            for path, info in items: print(f"  {path} :: {info}")
    print(f"\n{total} finding(s).")
    return 1 if total else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
