import os, importlib.util, tempfile
import re

_spec = importlib.util.spec_from_file_location(
    "scrape", os.path.join(os.path.dirname(__file__), "scrape.py"))
scrape = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(scrape)


def test_dedup_key():
    dk = scrape.dedup_key
    assert dk("http://www.Example.com/Page/?utm_source=x&b=2&a=1#frag") == "https://example.com/Page?a=1&b=2"
    assert dk("https://example.com/index.html") == "https://example.com/"
    assert dk("https://example.com/a/b/") == "https://example.com/a/b"
    assert dk("https://example.com") == "https://example.com/"
    assert dk("https://example.com:443/x") == "https://example.com/x"
    assert dk("https://example.com/a") == dk("http://www.example.com/a/?fbclid=zz")


def test_content_hash():
    assert scrape.content_hash("abc") == scrape.content_hash("abc")
    assert scrape.content_hash("abc") != scrape.content_hash("abd")
    assert len(scrape.content_hash("x")) == 64


def test_slug_for_url():
    s = scrape.slug_for_url("https://www.example.com/blog/My-Post/?utm_source=x")
    assert s.startswith("example-com-my-post-")
    assert s.endswith(".md")
    assert re.fullmatch(r"[a-z0-9-]+\.md", s)
    assert len(s[:-3].rsplit("-", 1)[1]) == 10  # 10-char hash suffix
    # variants that dedup to the same key produce the same slug
    assert scrape.slug_for_url("https://example.com/a") == scrape.slug_for_url("http://www.example.com/a/?utm_source=y")


def test_next_tier():
    nt = scrape.next_tier
    assert nt("http", 200, False, 5000) is None       # good HTTP -> accept
    assert nt("http", 403, False, 0) == "stealth"      # blocked
    assert nt("http", 429, False, 5000) == "stealth"   # rate-limited
    assert nt("http", 200, True, 5000) == "stealth"    # cloudflare challenge
    assert nt("http", 200, False, 10) == "stealth"     # empty/JS shell -> browser
    assert nt("stealth", 200, False, 10) == "dynamic"  # still empty after stealth
    assert nt("stealth", 403, False, 5000) == "dynamic"  # blocked stealth page -> dynamic
    assert nt("stealth", 200, True, 5000) == "dynamic"   # challenge page -> dynamic
    assert nt("stealth", 200, False, 5000) is None     # stealth got content
    assert nt("dynamic", 200, False, 0) is None        # dynamic is terminal


def test_is_low_quality():
    lq = scrape.is_low_quality
    assert lq("") is True
    assert lq("short text", min_chars=200) is True
    assert lq("x" * 300) is False
    assert lq("x" * 300, content_type="application/pdf") is True
    assert lq("Please subscribe to continue reading. " * 3, min_chars=10) is True  # paywall, <1000 chars
    assert lq("real content. " * 100) is False                                     # long, no marker


def test_in_scope():
    ins = scrape.in_scope
    start = "https://example.com/docs"
    assert ins("https://example.com/docs/a", start) is True
    assert ins("https://other.com/x", start) is False
    assert ins("https://www.example.com/y", start) is True            # www normalized
    assert ins("https://example.com/blog/a", start, include=r"/docs/") is False
    assert ins("https://example.com/docs/a.pdf", start, exclude=r"\.pdf$") is False
    assert ins("https://example.com/docs/a", start, exclude=r"\.pdf$") is True


def test_frontier_dedup():
    seen = {scrape.dedup_key("https://example.com/a")}
    urls = ["https://example.com/a", "https://www.example.com/a/?utm_source=x",
            "https://example.com/b", "https://example.com/b#frag"]
    assert scrape.frontier_dedup(urls, seen) == ["https://example.com/b"]


def test_crawl_budget_caps_attempted_fetches():
    budget = scrape.CrawlBudget(2)
    assert budget.mark_fetch() is True
    assert budget.mark_fetch() is True
    assert budget.mark_fetch() is False
    assert budget.fetches == 2


def test_normalize_discovered_url():
    ndu = scrape.normalize_discovered_url
    assert ndu("/docs/a", "https://example.com/root") == "https://example.com/docs/a"
    assert ndu("b", "https://example.com/docs/a") == "https://example.com/docs/b"
    assert ndu("#section", "https://example.com/docs/a") == "https://example.com/docs/a#section"


def test_build_frontmatter():
    fm = scrape.build_frontmatter({
        "source_type": "webpage", "url": "https://x.com/a", "title": "Hello: World",
        "is_verbatim": True, "http_status": 200, "author": None,
    })
    assert fm.startswith("---\n") and fm.rstrip().endswith("---")
    assert "source_type: webpage" in fm
    assert 'url: "https://x.com/a"' in fm        # contains ':' -> quoted
    assert 'title: "Hello: World"' in fm
    assert "is_verbatim: true" in fm             # bool lowercased
    assert "http_status: 200" in fm
    assert "author:" in fm                        # null -> empty value
    # embedded newline must be escaped, not left literal (would be invalid YAML)
    fm2 = scrape.build_frontmatter({"title": "A\nB"})
    assert 'title: "A\\nB"' in fm2
    assert 'title: "A\nB"' not in fm2
    fm3 = scrape.build_frontmatter({"title": r"C:\Users\name"})
    assert r'title: "C:\\Users\\name"' in fm3


def test_already_ingested():
    ai = scrape.already_ingested
    existing = [{"url": "https://example.com/a", "canonical_url": "https://example.com/a", "content_hash": "abc"}]
    assert ai("https://www.example.com/a/?utm_source=z", None, "xyz", existing) is True   # url variant match
    assert ai("https://example.com/b", None, "abc", existing) is True                      # content-hash match
    assert ai("https://example.com/b", "https://example.com/a", "zzz", existing) is True   # canonical match
    assert ai("https://example.com/b", None, "zzz", existing) is False


def test_load_existing_sources():
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, "source.md"), "w", encoding="utf-8") as fh:
            fh.write(
                "---\n"
                "url: \"https://example.com/a\"\n"
                "canonical_url: \"https://example.com/canonical\"\n"
                "content_hash: abc\n"
                "---\n"
                "# Source\n"
            )
        assert scrape.load_existing_sources(tmp) == [{
            "url": "https://example.com/a",
            "canonical_url": "https://example.com/canonical",
            "content_hash": "abc",
        }]


def test_write_or_skip_raw_duplicate_url_does_not_overwrite():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, scrape.slug_for_url("https://example.com/a"))
        original = (
            "---\n"
            "url: \"https://example.com/a\"\n"
            "canonical_url: \"https://example.com/a\"\n"
            "content_hash: oldhash\n"
            "---\n"
            "# Existing\n"
        )
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(original)
        res = {
            "url": "http://www.example.com/a?utm_source=x",
            "tier": "http",
            "status": 200,
            "markdown": "new content " * 30,
            "meta": {"canonical_url": None, "title": "New"},
            "low_quality": False,
        }
        out = scrape.write_or_skip_raw(res, tmp)
        assert out["status"] == "skipped"
        with open(path, "r", encoding="utf-8") as fh:
            assert fh.read() == original


def test_write_or_skip_raw_duplicate_content_hash_does_not_write():
    with tempfile.TemporaryDirectory() as tmp:
        text = "same content " * 30
        with open(os.path.join(tmp, "old.md"), "w", encoding="utf-8") as fh:
            fh.write(
                "---\n"
                "url: \"https://example.com/old\"\n"
                "canonical_url: \"https://example.com/old\"\n"
                f"content_hash: {scrape.content_hash(text)}\n"
                "---\n"
                "# Existing\n"
            )
        res = {
            "url": "https://example.com/new",
            "tier": "http",
            "status": 200,
            "markdown": text,
            "meta": {"canonical_url": None, "title": "New"},
            "low_quality": False,
        }
        out = scrape.write_or_skip_raw(res, tmp)
        assert out["status"] == "skipped"
        assert not os.path.exists(os.path.join(tmp, scrape.slug_for_url("https://example.com/new")))


def test_write_or_skip_raw_rejects_low_quality():
    with tempfile.TemporaryDirectory() as tmp:
        out = scrape.write_or_skip_raw({
            "url": "https://example.com/a",
            "tier": "http",
            "status": 200,
            "markdown": "",
            "meta": {},
            "low_quality": True,
        }, tmp)
        assert out == {"path": None, "status": "rejected", "reason": "low_quality"}


def test_fetch_one_non_html_content_type_rejected_without_extract():
    calls = {"extract": 0}
    old_fetch, old_extract = scrape._scrapling_fetch, scrape._extract
    try:
        scrape._scrapling_fetch = lambda url, tier: ("%PDF-1.7", 200, False, "application/pdf")

        def fake_extract(html, url):
            calls["extract"] += 1
            return "x" * 300, {}

        scrape._extract = fake_extract
        res = scrape.fetch_one("https://example.com/a.pdf", tier="http")
        assert res["content_type"] == "application/pdf"
        assert res["low_quality"] is True
        assert calls["extract"] == 0
    finally:
        scrape._scrapling_fetch, scrape._extract = old_fetch, old_extract


def test_fetch_one_html_content_type_accepts_good_extraction():
    old_fetch, old_extract = scrape._scrapling_fetch, scrape._extract
    try:
        scrape._scrapling_fetch = lambda url, tier: ("<html></html>", 200, False, "text/html; charset=utf-8")
        scrape._extract = lambda html, url: ("real content " * 30, {"title": "Example"})
        res = scrape.fetch_one("https://example.com/a", tier="http")
        assert res["content_type"] == "text/html; charset=utf-8"
        assert res["low_quality"] is False
        assert res["meta"]["title"] == "Example"
    finally:
        scrape._scrapling_fetch, scrape._extract = old_fetch, old_extract


def test_missing_deps_message():
    msg = scrape.missing_deps_message(["scrapling", "trafilatura"])
    assert "pip install --user" in msg
    assert "scrapling install" in msg
    assert "Claude Code" in msg


if __name__ == "__main__":
    import sys
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn(); print("ok", fn.__name__)
    print(f"ALL {len(fns)} SCRAPE TESTS PASSED")
