import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from split_recursion_outline import split_chapters

SAMPLE = """# Recursive Proof Composition: A Three-Chapter Treatment

intro blurb

## Chapter 1: Recursive Proof Composition

### 1.1 Why Recursion?
ch1 body

## Chapter 2: Folding Schemes in Depth

ch2 body

## Chapter 3: Applications of Recursive Proving

ch3 body

## Backmatter Notes (for the full manuscript)

backmatter
"""


def test_split_chapters_returns_three():
    chs = split_chapters(SAMPLE)
    assert [slug for slug, _ in chs] == ["rc01", "rc02", "rc03"]


def test_split_chapter_bodies_bounded():
    chs = dict(split_chapters(SAMPLE))
    assert "ch1 body" in chs["rc01"] and "ch2 body" not in chs["rc01"]
    assert "backmatter" not in chs["rc03"]   # backmatter excluded
    assert "intro blurb" not in chs["rc01"]  # title preamble excluded
