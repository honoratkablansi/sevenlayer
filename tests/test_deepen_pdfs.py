import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from deepen_pdfs import batch_for_ids, anchors_for_source, graph_stats

MANIFEST = [
    {"id": 6, "slug": "groth16", "chapters": [2], "type": "paper",
     "file": "references/ch02/ref-06-groth16.pdf", "status": "ok"},
    {"id": 22, "slug": "frozen-heart", "chapters": [6], "type": "web",
     "file": "references/ch06/ref-22-frozen-heart.md", "status": "ok"},
    {"id": 47, "slug": "dup", "chapters": [14], "type": "paper",
     "duplicate_of": 12, "status": "ok"},
    {"id": 1, "slug": "clarke", "chapters": [1], "type": "stub",
     "file": "references/ch01/ref-01-clarke.md", "status": "stub"},
]

GRAPH = {
    "nodes": [
        {"id": "ref-06_groth16", "label": "Groth16", "source_file": "references/ch02/ref-06-groth16.pdf"},
        {"id": "concept_qap", "label": "QAP", "source_file": "references\\ch02\\ref-06-groth16.pdf"},
        {"id": "wiki_x", "label": "X", "source_file": "wiki/chapters/02.md"},
    ],
    "links": [{"source": "wiki_x", "target": "ref-06_groth16", "relation": "cites"}],
}


def test_batch_for_ids_returns_only_papers_skipping_dups_and_stubs():
    rows = batch_for_ids(MANIFEST, [6, 22, 47, 1])
    assert rows == [(6, "references/ch02/ref-06-groth16.pdf", "groth16", [2])]


def test_anchors_for_source_matches_across_path_separators():
    anchors = anchors_for_source(GRAPH, "references/ch02/ref-06-groth16.pdf")
    assert set(anchors) == {"ref-06_groth16", "concept_qap"}
    assert anchors_for_source(GRAPH, "references/ch99/missing.pdf") == []


def test_graph_stats_counts_nodes_edges_and_per_pdf():
    s = graph_stats(GRAPH)
    assert s["nodes"] == 3
    assert s["edges"] == 1
    assert s["nodes_per_pdf"]["ref-06-groth16.pdf"] == 2
    assert s["nodes_by_source_top"]["references"] == 2
    assert s["nodes_by_source_top"]["wiki"] == 1
