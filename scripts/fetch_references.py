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


def atomic_write(path: Path, data: bytes) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)


def save_manifest(entries: list[dict]) -> None:
    atomic_write(
        MANIFEST_PATH,
        (json.dumps(entries, indent=2, ensure_ascii=False) + "\n").encode("utf-8"),
    )


def is_pdf(data: bytes) -> bool:
    return data[:5] == b"%PDF-"


_CF_MARKERS = (b"just a moment", b"cf-mitigated", b"challenge-platform", b"cf-chl-")


def _looks_like_cloudflare(status: int, body: bytes) -> bool:
    """True when a failed fetch looks like a Cloudflare challenge rather than a
    plain 404/forbidden, so we only spend a browser launch when it can help."""
    if status == 403:
        return True
    head = bytes(body[:4096]).lower()
    return any(marker in head for marker in _CF_MARKERS)


def _origin(url: str) -> str:
    from urllib.parse import urlsplit

    parts = urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}"


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
            text = page.get_all_text(ignore_tags=("script", "style")).strip()
            if len(text) > 200:
                return str(text), "stealthy"
    except Exception as exc:  # noqa: BLE001
        print(f"    stealthy: {exc}")
    return None, ""


def process(entry: dict, entries: list[dict], force: bool, dry_run: bool) -> str:
    """Returns the new status for the entry."""
    if entry.get("duplicate_of") is not None:
        matches = [e for e in entries if e["id"] == entry["duplicate_of"]]
        if not matches:
            print(f"  warning: duplicate_of={entry['duplicate_of']} not found in entries")
            return "failed"
        target = matches[0]
        return "ok" if (REPO / target["file"]).exists() else "pending"

    out = REPO / entry["file"]
    if out.exists() and not force:
        # For paper entries, validate the stored file is a real PDF; re-download if not.
        if entry["type"] == "paper" and not is_pdf(out.read_bytes()):
            pass  # fall through to re-download
        else:
            if entry["type"] == "stub":
                return "stub"
            return entry["status"] if entry["status"] not in ("pending", "failed") else "ok"
    if dry_run:
        print(f"  would fetch [{entry['type']}] {entry.get('url', '(stub)')} -> {entry['file']}")
        return entry["status"]

    out.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()

    if entry["type"] == "stub":
        atomic_write(out, stub_markdown(entry).encode("utf-8"))
        return "stub"
    if entry["type"] == "paper":
        data, how = fetch_paper(entry["url"])
        if data is None:
            return "failed"
        atomic_write(out, data)
        return "ok"
    # web
    text, how = fetch_web_text(entry["url"])
    if text is None:
        return "failed"
    atomic_write(out, web_markdown(entry, text, how, today).encode("utf-8"))
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
        entry["status"] = process(entry, entries, args.force, args.dry_run)
        print(f"  -> {entry['status']}")
        if not args.dry_run:
            save_manifest(entries)

    selected_bad = [
        e["id"] for e in entries
        if e["status"] in ("pending", "failed") and (only is None or e["id"] in only)
    ]
    bad = [e["id"] for e in entries if e["status"] in ("pending", "failed")]
    print(f"\n{len(entries) - len(bad)}/{len(entries)} resolved; unresolved: {bad or 'none'}")
    if args.dry_run:
        return 0
    if only is not None:
        return 1 if selected_bad else 0
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
