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


import pytest
from build_book_graph import merge_extraction, reference_subgraph


def test_merge_extraction_unions_and_dedups():
    frags = [
        {"nodes": [{"id": "concept_iop", "label": "IOP"}],
         "edges": [{"source": "ch01_x", "target": "concept_iop", "relation": "defines"}]},
        {"nodes": [{"id": "concept_iop", "label": "IOP dup"},
                   {"id": "ch01_x", "label": "X"}],
         "edges": [{"source": "ch01_x", "target": "concept_iop", "relation": "defines"},  # dup
                   {"source": "ch01_x", "target": "ghost", "relation": "cites"}]},          # dangling
    ]
    out = merge_extraction(frags)
    assert sorted(n["id"] for n in out["nodes"]) == ["ch01_x", "concept_iop"]
    assert out["nodes"][0]["label"] == "IOP"        # first wins
    assert len(out["edges"]) == 1                   # dup + dangling dropped
    assert out["input_tokens"] == 0 and out["output_tokens"] == 0


def test_reference_subgraph_selects_only_reference_nodes():
    g1 = {
        "nodes": [
            {"id": "ref-06_groth16", "label": "Groth16", "source_file": "references/ch02/ref-06-groth16.pdf"},
            {"id": "concept_pairing", "label": "Pairing", "source_file": "references/ch02/ref-06-groth16.pdf"},
            {"id": "wiki_x", "label": "X", "source_file": "wiki/chapters/02.md"},
            {"id": "manu_y", "label": "Y", "source_file": "proving-nothing.md"},
        ],
        "links": [
            {"source": "ref-06_groth16", "target": "concept_pairing", "relation": "uses"},
            {"source": "wiki_x", "target": "concept_pairing", "relation": "references"},  # one end outside refs
            {"source": "wiki_x", "target": "manu_y", "relation": "x"},                     # both outside
        ],
    }
    sub = reference_subgraph(g1)
    assert sorted(n["id"] for n in sub["nodes"]) == ["concept_pairing", "ref-06_groth16"]
    assert sub["edges"] == [
        {"source": "ref-06_groth16", "target": "concept_pairing", "relation": "uses"}
    ]
