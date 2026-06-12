#!/usr/bin/env python3
"""llm-wiki scraper: fetch/crawl URLs -> clean markdown in raw/ (optional, Claude Code only).

Pure functions are stdlib-only and import-safe without Scrapling/trafilatura.
Network/extraction/crawl functions defer those imports so the unit tests run anywhere.
Usage: python3 scrape.py fetch <url> --out-dir <wiki-root>/raw [--tier auto|http|stealth|dynamic]
       python3 scrape.py crawl <start-url> --out-dir <wiki-root>/raw [--max-pages 25] ...
"""
import hashlib
import os
import re
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode, urljoin

_TRACKING_PREFIXES = ("utm_",)
_TRACKING_KEYS = {"fbclid", "gclid", "mc_eid", "igshid", "sessionid", "sid", "phpsessid"}
_INDEX_FILES = ("index.html", "index.htm", "index.php", "default.aspx")


def dedup_key(url):
    """Normalize a URL to a canonical dedup key (stdlib-only, deterministic)."""
    parts = urlsplit(url.strip())
    host = (parts.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    netloc = host
    if parts.port and parts.port not in (80, 443):
        netloc = f"{host}:{parts.port}"
    path = parts.path or "/"
    for idx in _INDEX_FILES:
        if path.endswith("/" + idx):
            path = path[: -len(idx)]
            break
    if len(path) > 1 and path.endswith("/"):
        path = path.rstrip("/")
    if not path:
        path = "/"
    q = [(k, v) for (k, v) in parse_qsl(parts.query, keep_blank_values=True)
         if not k.lower().startswith(_TRACKING_PREFIXES) and k.lower() not in _TRACKING_KEYS]
    q.sort()
    return urlunsplit(("https", netloc, path, urlencode(q), ""))


_WIN_RESERVED = {"con", "prn", "aux", "nul"} | {f"com{i}" for i in range(1, 10)} | {f"lpt{i}" for i in range(1, 10)}


def content_hash(text):
    """sha256 hex of the extracted markdown (content-level dedup)."""
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def slug_for_url(url):
    """Deterministic, collision-resistant, filesystem-safe filename for a URL: <stem>-<hash>.md"""
    key = dedup_key(url)
    parts = urlsplit(key)
    host = parts.netloc.split(":")[0]
    segs = [s for s in parts.path.split("/") if s]
    last = segs[-1] if segs else "home"
    stem = re.sub(r"[^a-z0-9]+", "-", f"{host}-{last}".lower()).strip("-")[:60].strip("-")
    if not stem or stem in _WIN_RESERVED:
        stem = f"page-{stem}".strip("-")
    return f"{stem}-{content_hash(key)[:10]}.md"


def next_tier(current, status, has_challenge, extracted_len, min_len=200):
    """Decide the next fetcher tier from concrete signals, or None to accept the result.

    Escalation is linear http -> stealth -> dynamic. We escalate on an unambiguous
    block (401/403/429 or a detected anti-bot challenge) or on too-little extracted
    text (a JS shell that needs a real browser to render). dynamic is terminal.
    """
    blocked = status in (401, 403, 429) or has_challenge
    empty = (extracted_len or 0) < min_len
    if current == "http":
        return "stealth" if (blocked or empty) else None
    if current == "stealth":
        return "dynamic" if (blocked or empty) else None
    return None


_PAYWALL_MARKERS = (
    "subscribe to continue", "subscribe to read", "create a free account",
    "sign in to read", "this content is for subscribers", "accept cookies",
    "enable javascript", "please enable js",
)


def is_low_quality(text, content_type="text/html", min_chars=200):
    """True if an extraction should be rejected/flagged rather than written to raw/."""
    if content_type and "html" not in content_type.lower():
        return True
    t = (text or "").strip()
    if len(t) < min_chars:
        return True
    low = t.lower()
    if len(t) < 1000 and any(m in low for m in _PAYWALL_MARKERS):
        return True
    return False


def in_scope(url, start_url, same_domain=True, include=None, exclude=None):
    """Crawl scope filter: same-domain (normalized) + optional include/exclude regexes."""
    if same_domain and urlsplit(dedup_key(url)).netloc != urlsplit(dedup_key(start_url)).netloc:
        return False
    if include and not re.search(include, url):
        return False
    if exclude and re.search(exclude, url):
        return False
    return True


def frontier_dedup(urls, seen):
    """Return urls whose dedup_key is not already in `seen` and not duplicated within the batch."""
    out, local = [], set(seen)
    for u in urls:
        k = dedup_key(u)
        if k in local:
            continue
        local.add(k)
        out.append(u)
    return out


class CrawlBudget:
    """Shared crawl budget for attempted page fetches."""
    def __init__(self, max_pages):
        self.max_pages = max_pages
        self.fetches = 0

    def can_fetch(self):
        return self.fetches < self.max_pages

    def mark_fetch(self):
        if not self.can_fetch():
            return False
        self.fetches += 1
        return True


def normalize_discovered_url(href, base_url):
    """Resolve a crawled href against the page URL before scope/dedup checks."""
    return urljoin(base_url, href or "")


_FRONTMATTER_ORDER = [
    "source_type", "url", "canonical_url", "title", "author", "published",
    "sitename", "fetched_at", "fetcher", "fetch_method", "is_verbatim",
    "http_status", "extractor", "content_hash",
]


def build_frontmatter(meta):
    """Render a YAML frontmatter block (stable field order; None -> empty; quote risky strings)."""
    lines = ["---"]
    for k in _FRONTMATTER_ORDER:
        v = meta.get(k)
        if v is None:
            lines.append(f"{k}:")
        elif isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        else:
            s = str(v)
            if s == "" or any(c in s for c in ':#"\n'):
                s = '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'
            lines.append(f"{k}: {s}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def already_ingested(url, html_canonical, chash, existing_sources):
    """True if this URL (or its canonical) or its content hash already exists in the wiki."""
    keys = {dedup_key(url)}
    if html_canonical:
        keys.add(dedup_key(html_canonical))
    for src in existing_sources:
        for field in ("url", "canonical_url"):
            v = src.get(field)
            if v and dedup_key(v) in keys:
                return True
        if chash and src.get("content_hash") == chash:
            return True
    return False


def _read_frontmatter(path):
    with open(path, "r", encoding="utf-8-sig") as fh:
        text = fh.read(8192)
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fields = {}
    for line in text[3:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] == '"':
            value = value[1:-1].replace('\\"', '"').replace("\\n", "\n")
        fields[key.strip()] = value
    return fields


def load_existing_sources(out_dir):
    """Load URL/canonical/hash fields from existing raw markdown frontmatter."""
    if not os.path.isdir(out_dir):
        return []
    sources = []
    for name in sorted(os.listdir(out_dir)):
        if not name.endswith(".md"):
            continue
        meta = _read_frontmatter(os.path.join(out_dir, name))
        if meta:
            sources.append({
                "url": meta.get("url"),
                "canonical_url": meta.get("canonical_url"),
                "content_hash": meta.get("content_hash"),
            })
    return sources


import datetime


def _content_type_from_page(page):
    for obj in (page, getattr(page, "response", None)):
        headers = getattr(obj, "headers", None)
        if not headers:
            continue
        getter = getattr(headers, "get", None)
        if getter:
            for key in ("content-type", "Content-Type", "CONTENT-TYPE"):
                value = getter(key)
                if value:
                    return str(value)
        try:
            for key, value in headers.items():
                if str(key).lower() == "content-type":
                    return str(value)
        except AttributeError:
            pass
    return ""


def _scrapling_fetch(url, tier):
    """Fetch raw HTML via Scrapling. Returns (html, status, has_challenge, content_type). Network — not unit-tested.
    NOTE: verify method names against the installed Scrapling version (v0.4.x): browser tiers use .fetch()."""
    from scrapling.fetchers import Fetcher, StealthyFetcher, DynamicFetcher
    if tier == "http":
        page = Fetcher.get(url)
        html = page.html_content
        challenge = "just a moment" in (html or "").lower() or "cf-challenge" in (html or "").lower()
        return html, getattr(page, "status", 200), challenge, _content_type_from_page(page)
    if tier == "stealth":
        page = StealthyFetcher.fetch(url, solve_cloudflare=True)
        return page.html_content, getattr(page, "status", 200), False, _content_type_from_page(page)
    page = DynamicFetcher.fetch(url)  # dynamic
    return page.html_content, getattr(page, "status", 200), False, _content_type_from_page(page)


def _extract(html, url):
    """HTML -> (markdown, meta dict) via trafilatura. Not unit-tested."""
    import trafilatura
    # with_metadata=False here: metadata goes in our own frontmatter via bare_extraction
    # below; leaving it True makes trafilatura prepend a second YAML block inside the body.
    md = trafilatura.extract(
        html, output_format="markdown", with_metadata=False, favor_precision=True,
        include_comments=False, deduplicate=True, url=url,
    ) or ""
    doc = trafilatura.bare_extraction(html, with_metadata=True, url=url) or {}
    g = (lambda k: doc.get(k) if isinstance(doc, dict) else getattr(doc, k, None))
    meta = {
        "title": g("title"), "author": g("author"), "published": g("date"),
        "sitename": g("sitename"), "canonical_url": g("url"),
        "extractor": f"trafilatura-{getattr(trafilatura, '__version__', '?')}",
    }
    return md, meta


def fetch_one(url, tier="auto", min_chars=200):
    """Fetch + extract one URL with tier escalation. Returns a result dict (network — integration only)."""
    order = {"http": ["http"], "stealth": ["stealth"], "dynamic": ["dynamic"],
             "auto": ["http", "stealth", "dynamic"]}[tier]
    html, status, challenge, content_type, used = "", 0, False, "", order[0]
    md, meta = "", {}
    for used in order:
        html, status, challenge, content_type = _scrapling_fetch(url, used)
        if content_type and "html" not in content_type.lower():
            md, meta = "", {}
            break
        md, meta = _extract(html, url)
        if tier != "auto":
            break
        nxt = next_tier(used, status, challenge, len(md), min_chars)
        if nxt is None:
            break
    md_clean = (md or "").strip()
    return {
        "url": url, "tier": used, "status": status, "markdown": md_clean, "meta": meta,
        "content_type": content_type,
        "low_quality": is_low_quality(md_clean, content_type or "text/html", min_chars),
    }


def crawl_site(start_url, max_pages=25, max_depth=2, same_domain=True,
               include=None, exclude=None, delay=1.0, tier="auto", obey_robots=False):
    """Bounded crawl via Scrapling's Spider. Yields fetch_one-style result dicts. Network — integration only.

    Delegates queueing/concurrency/checkpointing to Scrapling's Spider (do NOT hand-roll BFS).
    VERIFY the Spider API against the installed Scrapling version (v0.4.x):
    `from scrapling.spiders import Spider` with `start_urls`, `allowed_domains`, `robots_txt_obey`,
    and a `parse` coroutine that yields `response.follow(link)` for in-scope links.
    """
    from urllib.parse import urlsplit as _us
    from scrapling.spiders import Spider  # noqa: F401  (verify exact symbol at impl time)

    domain = _us(dedup_key(start_url)).netloc
    seen, results, budget = {dedup_key(start_url)}, [], CrawlBudget(max_pages)

    class _WikiSpider(Spider):
        name = "llm_wiki_crawl"
        start_urls = [start_url]
        allowed_domains = [domain] if same_domain else []
        robots_txt_obey = obey_robots
        download_delay = delay

        async def parse(self, response):
            page_url = getattr(response, "url", start_url)
            if not budget.mark_fetch():
                return
            res = fetch_one(page_url, tier=tier)
            if not res["low_quality"]:
                results.append(res)
            if len(results) >= max_pages:
                return
            depth = (response.meta or {}).get("depth", 0) if hasattr(response, "meta") else 0
            if depth >= max_depth:
                return
            links = [normalize_discovered_url(link, page_url)
                     for link in response.css("a::attr(href)").getall()]
            for link in frontier_dedup(links, seen):
                if in_scope(link, start_url, same_domain, include, exclude):
                    seen.add(dedup_key(link))
                    yield response.follow(link, callback=self.parse)

    spider = _WikiSpider()
    spider.start()
    return results[:max_pages]


import argparse
import json
import sys


def missing_deps_message(missing):
    return (
        "Web scraping requires local Claude Code with network access.\n"
        f"Missing: {', '.join(missing)}.\n"
        'Install locally:  pip install --user "scrapling[fetchers]" trafilatura\n'
        "Then browsers:    scrapling install\n"
        "(Not available on the Claude API sandbox: no network / no installs.)"
    )


def _check_deps():
    import importlib.util
    return [m for m in ("scrapling", "trafilatura") if importlib.util.find_spec(m) is None]


def _write_raw(res, out_dir, fetch_method="scrapling"):
    """Write a result dict to out_dir/<slug>.md with frontmatter. Returns the path or None if low quality."""
    if res["low_quality"]:
        return None
    md = res["markdown"]
    meta = dict(res["meta"])
    meta.update({
        "source_type": "webpage", "url": res["url"],
        "fetched_at": datetime.date.today().isoformat(),
        "fetcher": res["tier"], "fetch_method": fetch_method,
        "is_verbatim": fetch_method == "scrapling",
        "http_status": res["status"], "content_hash": content_hash(md),
    })
    # Direct assignment (not setdefault): _extract may have set canonical_url=None,
    # which setdefault would not overwrite, leaving the dedup_key fallback dead.
    meta["canonical_url"] = meta.get("canonical_url") or dedup_key(res["url"])
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, slug_for_url(res["url"]))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(build_frontmatter(meta) + "\n# " + (meta.get("title") or res["url"]) + "\n\n" + md + "\n")
    return path


def write_or_skip_raw(res, out_dir, fetch_method="scrapling"):
    """Write raw markdown unless quality or dedup gates reject it."""
    if res["low_quality"]:
        return {"path": None, "status": "rejected", "reason": "low_quality"}
    md = res["markdown"]
    meta = dict(res["meta"])
    canonical = meta.get("canonical_url") or dedup_key(res["url"])
    chash = content_hash(md)
    if already_ingested(res["url"], canonical, chash, load_existing_sources(out_dir)):
        return {"path": None, "status": "skipped", "reason": "duplicate"}
    path = _write_raw(res, out_dir, fetch_method=fetch_method)
    if path:
        return {"path": path, "status": "written", "reason": None}
    return {"path": None, "status": "rejected", "reason": "low_quality"}


def main(argv=None):
    p = argparse.ArgumentParser(prog="scrape.py", description="Fetch/crawl URLs into a wiki's raw/ dir.")
    sub = p.add_subparsers(dest="cmd", required=True)
    pf = sub.add_parser("fetch"); pf.add_argument("url"); pf.add_argument("--out-dir", required=True)
    pf.add_argument("--tier", default="auto", choices=["auto", "http", "stealth", "dynamic"])
    pc = sub.add_parser("crawl"); pc.add_argument("url"); pc.add_argument("--out-dir", required=True)
    pc.add_argument("--max-pages", type=int, default=25); pc.add_argument("--max-depth", type=int, default=2)
    pc.add_argument("--include"); pc.add_argument("--exclude"); pc.add_argument("--delay", type=float, default=1.0)
    pc.add_argument("--tier", default="auto", choices=["auto", "http", "stealth", "dynamic"])
    pc.add_argument("--no-same-domain", action="store_true"); pc.add_argument("--obey-robots", action="store_true")
    pc.add_argument("--plan-only", action="store_true")
    args = p.parse_args(argv)

    missing = _check_deps()
    if missing and not (args.cmd == "crawl" and args.plan_only):
        print(missing_deps_message(missing), file=sys.stderr)
        return 3

    if args.cmd == "fetch":
        res = fetch_one(args.url, tier=args.tier)
        write_result = write_or_skip_raw(res, args.out_dir)
        print(json.dumps({"path": write_result["path"], "tier": res["tier"],
                          "low_quality": res["low_quality"], "status": write_result["status"],
                          "reason": write_result["reason"]}))
        return 1 if write_result["status"] == "rejected" else 0

    if args.cmd == "crawl":
        if args.plan_only:
            print(json.dumps({"plan": {"start": args.url, "max_pages": args.max_pages,
                                       "max_depth": args.max_depth, "same_domain": not args.no_same_domain,
                                       "obey_robots": args.obey_robots}}))
            return 0
        results = crawl_site(args.url, max_pages=args.max_pages, max_depth=args.max_depth,
                             same_domain=not args.no_same_domain, include=args.include,
                             exclude=args.exclude, delay=args.delay, tier=args.tier, obey_robots=args.obey_robots)
        writes = [write_or_skip_raw(r, args.out_dir) for r in results]
        print(json.dumps({"pages": len(results),
                          "written": sum(1 for w in writes if w["status"] == "written"),
                          "skipped": sum(1 for w in writes if w["status"] == "skipped"),
                          "rejected": sum(1 for w in writes if w["status"] == "rejected")}))
        return 0


if __name__ == "__main__":
    sys.exit(main())
