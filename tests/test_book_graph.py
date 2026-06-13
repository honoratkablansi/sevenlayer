import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from split_manuscript import split_chapters

SAMPLE = """# Glossary of Key Terms {.unnumbered}

glossary body

# Part I: The Invitation {.unnumbered}

# Chapter 1: The Promise

intro text
more

# Chapter 2: Layer 1 -- Building the Stage

stage text

# Part II: The Craft {.unnumbered}

# Chapter 3: Choreographing the Act

act text

# Complete Bibliography {.unnumbered}

bib body
"""


def test_split_chapters_extracts_only_chapters():
    chs = split_chapters(SAMPLE)
    assert [slug for slug, _ in chs] == ["ch01", "ch02", "ch03"]


def test_split_chapter_body_spans_to_next_top_heading():
    chs = dict(split_chapters(SAMPLE))
    assert chs["ch01"].startswith("# Chapter 1: The Promise")
    assert "intro text" in chs["ch01"] and "more" in chs["ch01"]
    assert "stage text" not in chs["ch01"]          # stops before ch2
    assert "glossary body" not in chs["ch01"]        # glossary excluded


def test_split_excludes_glossary_parts_bibliography():
    bodies = "\n".join(b for _, b in split_chapters(SAMPLE))
    assert "glossary body" not in bodies
    assert "bib body" not in bodies
    assert "Part I" not in bodies and "Part II" not in bodies
