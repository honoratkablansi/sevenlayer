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


import json as _json
import pytest
from deepen_pdfs import load_fragment, merge_fragment


def test_load_fragment_rejects_bad_shape(tmp_path):
    good = tmp_path / "good.json"
    good.write_text(_json.dumps({"nodes": [{"id": "a", "label": "A"}], "edges": []}))
    assert load_fragment(good)["nodes"][0]["id"] == "a"

    bad = tmp_path / "bad.json"
    bad.write_text(_json.dumps({"nodes": [{"label": "no id"}], "edges": []}))
    with pytest.raises(ValueError):
        load_fragment(bad)

    missing = tmp_path / "missing.json"
    missing.write_text(_json.dumps({"nodes": []}))  # no "edges" key
    with pytest.raises(ValueError):
        load_fragment(missing)


def test_merge_fragment_is_additive_and_dedups():
    graph = {
        "nodes": [{"id": "ref-06_groth16", "label": "Groth16",
                   "source_file": "references/ch02/ref-06-groth16.pdf"}],
        "links": [],
    }
    fragment = {
        "nodes": [
            {"id": "ref-06_groth16", "label": "DUP — should not overwrite"},  # existing
            {"id": "concept_pairing", "label": "Pairing",
             "source_file": "references/ch02/ref-06-groth16.pdf"},            # new
        ],
        "edges": [
            {"source": "ref-06_groth16", "target": "concept_pairing", "relation": "uses"},
            {"source": "ref-06_groth16", "target": "concept_pairing", "relation": "uses"},  # dup
            {"source": "ref-06_groth16", "target": "ghost_node", "relation": "cites"},      # dangling
        ],
    }
    out = merge_fragment(graph, fragment)
    ids = [n["id"] for n in out["nodes"]]
    assert ids == ["ref-06_groth16", "concept_pairing"]          # additive, deduped
    assert out["nodes"][0]["label"] == "Groth16"                 # existing not overwritten
    assert len(out["links"]) == 1                                # dup + dangling dropped
    assert out["links"][0]["relation"] == "uses"


def test_merge_fragment_enforces_additive_invariant():
    graph = {"nodes": [{"id": "a", "label": "A"}, {"id": "b", "label": "B"}], "links": []}
    # Simulate a "before" count higher than reality (99 > 2) so the guard fires.
    with pytest.raises(AssertionError):
        merge_fragment(graph, {"nodes": [], "edges": []}, _force_node_count=99)


from deepen_pdfs import consolidate_nodes


def test_consolidate_nodes_redirects_and_drops_dups():
    graph = {
        "nodes": [
            {"id": "concept_snark", "label": "SNARKs"},
            {"id": "concept_snarks", "label": "SNARKs"},   # dup -> concept_snark
            {"id": "ref-06_groth16", "label": "Groth16"},
        ],
        "links": [
            {"source": "ref-06_groth16", "target": "concept_snarks", "relation": "introduces"},
            {"source": "ref-06_groth16", "target": "concept_snark", "relation": "introduces"},  # dup after redirect
            {"source": "concept_snarks", "target": "concept_snark", "relation": "x"},           # self-loop after redirect
        ],
    }
    out = consolidate_nodes(graph, {"concept_snarks": "concept_snark"})
    assert [n["id"] for n in out["nodes"]] == ["concept_snark", "ref-06_groth16"]
    assert out["links"] == [
        {"source": "ref-06_groth16", "target": "concept_snark", "relation": "introduces"}
    ]


def test_consolidate_nodes_drops_edges_to_missing_canonical():
    graph = {
        "nodes": [{"id": "concept_snark", "label": "SNARKs"}],
        "links": [{"source": "ghost", "target": "concept_snarks", "relation": "r"}],
    }
    out = consolidate_nodes(graph, {"concept_snarks": "concept_snark"})
    assert out["links"] == []  # source 'ghost' not a node -> dangling, dropped
