"""Download the book's references per chapter, driven by references/manifest.json.

Usage (from repo root, venv active):
    python scripts/fetch_references.py [--dry-run] [--force] [--only 6,17,42]
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO / "references" / "manifest.json"


def load_manifest() -> list[dict]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def save_manifest(entries: list[dict]) -> None:
    MANIFEST_PATH.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def is_pdf(data: bytes) -> bool:
    return data[:5] == b"%PDF-"


def stub_markdown(entry: dict) -> str:
    chapters = ", ".join(str(c) for c in entry["chapters"])
    return (
        "---\n"
        f"ref_id: {entry['id']}\n"
        f"chapters: [{chapters}]\n"
        "type: stub\n"
        "---\n\n"
        f"# Reference {entry['id']}: {entry['slug']}\n\n"
        f"{entry['citation']}\n\n"
        "This source is print-only or paywalled; no electronic copy is stored. "
        "This stub exists so the reference appears as a node in the knowledge graph.\n"
    )


def web_markdown(entry: dict, text: str, fetched_with: str, date: str) -> str:
    chapters = ", ".join(str(c) for c in entry["chapters"])
    return (
        "---\n"
        f"ref_id: {entry['id']}\n"
        f"chapters: [{chapters}]\n"
        "type: web\n"
        f"source_url: {entry['url']}\n"
        f"fetched: {date}\n"
        f"fetched_with: {fetched_with}\n"
        f"citation: '{entry['citation'].replace(chr(39), chr(39) * 2)}'\n"
        "---\n\n"
        f"# {entry['citation']}\n\n"
        f"{text}\n"
    )


def fetch_paper(url: str) -> tuple[bytes | None, str]:
    """Two attempts with curl_cffi impersonation. Returns (pdf_bytes, fetcher_name)."""
    from scrapling.fetchers import Fetcher

    for impersonate in ("chrome", "firefox"):
        try:
            page = Fetcher.get(url, impersonate=impersonate, timeout=90)
        except Exception as exc:  # noqa: BLE001 - report and try next tier
            print(f"    {impersonate}: {exc}")
            continue
        if page.status == 200 and is_pdf(page.body):
            return page.body, f"fetcher-{impersonate}"
        print(f"    {impersonate}: status={page.status}, pdf={is_pdf(page.body)}")
    return None, ""


def fetch_web_text(url: str) -> tuple[str | None, str]:
    """Fetcher first; StealthyFetcher (Camoufox) for bot-blocked/JS pages."""
    from scrapling.fetchers import Fetcher, StealthyFetcher

    try:
        page = Fetcher.get(url, impersonate="chrome", timeout=90)
        if page.status == 200:
            text = page.get_all_text(ignore_tags=("script", "style")).strip()
            if len(text) > 200:  # tiny bodies = JS shell or block page
                return str(text), "fetcher"
    except Exception as exc:  # noqa: BLE001
        print(f"    fetcher: {exc}")
    try:
        page = StealthyFetcher.fetch(url, headless=True, network_idle=True, timeout=120000)
        if page.status == 200:
            return str(page.get_all_text(ignore_tags=("script", "style")).strip()), "stealthy"
    except Exception as exc:  # noqa: BLE001
        print(f"    stealthy: {exc}")
    return None, ""


def process(entry: dict, force: bool, dry_run: bool) -> str:
    """Returns the new status for the entry."""
    if entry.get("duplicate_of") is not None:
        target = next(e for e in load_manifest() if e["id"] == entry["duplicate_of"])
        return "ok" if (REPO / target["file"]).exists() else "pending"

    out = REPO / entry["file"]
    if out.exists() and not force:
        return entry["status"] if entry["status"] not in ("pending", "failed") else "ok"
    if dry_run:
        print(f"  would fetch [{entry['type']}] {entry.get('url', '(stub)')} -> {entry['file']}")
        return entry["status"]

    out.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()

    if entry["type"] == "stub":
        out.write_text(stub_markdown(entry), encoding="utf-8")
        return "stub"
    if entry["type"] == "paper":
        data, how = fetch_paper(entry["url"])
        if data is None:
            return "failed"
        out.write_bytes(data)
        return "ok" if how == "fetcher-chrome" else "ok-stealth"
    # web
    text, how = fetch_web_text(entry["url"])
    if text is None:
        return "failed"
    out.write_text(web_markdown(entry, text, how, today), encoding="utf-8")
    return "ok" if how == "fetcher" else "ok-stealth"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true", help="re-download existing files")
    ap.add_argument("--only", help="comma-separated ref ids")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    entries = load_manifest()
    only = {int(x) for x in args.only.split(",")} if args.only else None
    for entry in entries:
        if only and entry["id"] not in only:
            continue
        print(f"[{entry['id']:02d}] {entry['slug']} ({entry['type']})")
        entry["status"] = process(entry, args.force, args.dry_run)
        print(f"  -> {entry['status']}")
        if not args.dry_run:
            save_manifest(entries)

    bad = [e["id"] for e in entries if e["status"] in ("pending", "failed")]
    print(f"\n{len(entries) - len(bad)}/{len(entries)} resolved; unresolved: {bad or 'none'}")
    return 1 if (bad and not args.dry_run and not only) else 0


if __name__ == "__main__":
    sys.exit(main())
