import sys
from pathlib import Path
import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import build_master_graph as m  # noqa: E402


def _g(nodes, links):
    """Minimal node-link graph dict for tests."""
    return {"directed": True, "multigraph": False, "graph": {},
            "nodes": nodes, "links": links}


def test_merge_graphs_unions_nodes_and_tracks_origin():
    a = _g([{"id": "concept_x", "label": "X"}],
           [{"source": "concept_x", "target": "concept_x", "relation": "self"}])
    b = _g([{"id": "concept_x", "label": "X"}, {"id": "concept_y", "label": "Y"}],
           [{"source": "concept_x", "target": "concept_y", "relation": "rel"}])
    out = m.merge_graphs([("book", a), ("recursion", b)])
    ids = {n["id"]: n for n in out["nodes"]}
    assert set(ids) == {"concept_x", "concept_y"}
    assert ids["concept_x"]["origin_graphs"] == ["book", "recursion"]
    assert ids["concept_y"]["origin_graphs"] == ["recursion"]
    # self-loop edge kept once; cross edge kept; no dangling
    assert {(l["source"], l["target"]) for l in out["links"]} == \
        {("concept_x", "concept_x"), ("concept_x", "concept_y")}


def test_merge_graphs_drops_dangling_edges():
    a = _g([{"id": "n1", "label": "1"}],
           [{"source": "n1", "target": "ghost", "relation": "r"}])
    out = m.merge_graphs([("book", a)])
    assert out["links"] == []


def test_merge_graphs_empty_returns_empty():
    out = m.merge_graphs([])
    assert out["nodes"] == [] and out["links"] == []


def test_merge_graphs_tolerates_missing_keys():
    bare = {"directed": True}  # no "nodes", no "links"
    a = _g([{"id": "n1", "label": "1"}], [])
    out = m.merge_graphs([("bare", bare), ("a", a)])
    assert {n["id"] for n in out["nodes"]} == {"n1"}
    assert out["links"] == []


def test_normalize_label_depluralizes_and_strips_punctuation():
    assert m.normalize_label("KZG Polynomial Commitments") == "kzg polynomial commitment"
    assert m.normalize_label("Bulletproofs") == "bulletproof"
    assert m.normalize_label("Knowledge Soundness") == "knowledge soundness"  # ss preserved
    assert m.normalize_label("STARK") == "stark"
    assert m.normalize_label("  Folding   Scheme!! ") == "folding scheme"
    assert m.normalize_label("Consensus") == "consensus"   # Latin -us kept
    assert m.normalize_label("Basis") == "basis"           # Latin -is kept
    assert m.normalize_label(None) == ""                    # None tolerated


def test_degree_map_counts_incidence():
    g = _g([{"id": "a"}, {"id": "b"}, {"id": "c"}],
           [{"source": "a", "target": "b"}, {"source": "a", "target": "c"}])
    assert m.degree_map(g) == {"a": 2, "b": 1, "c": 1}


def test_build_alias_map_collapses_variants_to_highest_degree():
    g = _g(
        [{"id": "concept_kzg-commitment", "label": "KZG Commitment"},
         {"id": "concept_kzg-commitments", "label": "KZG Commitments"},
         {"id": "concept_stark", "label": "STARK"}],
        [{"source": "concept_kzg-commitment", "target": "concept_stark"},
         {"source": "concept_kzg-commitment", "target": "concept_kzg-commitments"}],
    )
    # concept_kzg-commitment has degree 2, concept_kzg-commitments degree 1
    alias = m.build_alias_map(g)
    assert alias == {"concept_kzg-commitments": "concept_kzg-commitment"}


def test_validate_alias_map_rejects_chain():
    g = _g([{"id": "a"}, {"id": "b"}, {"id": "c"}], [])
    with pytest.raises(ValueError):
        m.validate_alias_map({"a": "b", "b": "c"}, g)


def test_validate_alias_map_rejects_unknown_id():
    g = _g([{"id": "a"}], [])
    with pytest.raises(ValueError):
        m.validate_alias_map({"a": "missing"}, g)


def test_degree_map_counts_self_loop_twice():
    g = _g([{"id": "a"}], [{"source": "a", "target": "a"}])
    assert m.degree_map(g) == {"a": 2}


def test_validate_alias_map_rejects_alias_that_is_canonical():
    g = _g([{"id": "a"}, {"id": "b"}, {"id": "c"}], [])
    with pytest.raises(ValueError):
        m.validate_alias_map({"a": "b", "c": "a"}, g)  # 'a' is alias key AND canonical


def test_build_alias_map_skips_unlabeled_nodes():
    g = _g([{"id": "concept_kzg-commitment"}, {"id": "concept_kzg_commitment"}], [])
    assert m.build_alias_map(g) == {}  # no label/norm_label -> not aliased


def test_reference_support_counts_distinct_reference_neighbors():
    g = _g(
        [{"id": "concept_a", "label": "A", "source_file": "proving-nothing.md"},
         {"id": "r1", "label": "p1", "source_file": "references/ch1/ref-01.pdf"},
         {"id": "r2", "label": "p2", "source_file": "references/ch1/ref-02.pdf"},
         {"id": "r3", "label": "p3", "source_file": "references/ch1/ref-01.pdf"}],
        [{"source": "concept_a", "target": "r1"},
         {"source": "concept_a", "target": "r2"},
         {"source": "concept_a", "target": "r3"}],
    )
    # r1 and r3 share a source_file -> 2 distinct reference files
    assert m.reference_support(g)["concept_a"] == 2


def test_score_concepts_ranks_by_degree_plus_support():
    g = _g(
        [{"id": "concept_hi", "label": "Hi", "source_file": "proving-nothing.md"},
         {"id": "concept_lo", "label": "Lo", "source_file": "proving-nothing.md"},
         {"id": "r1", "label": "p", "source_file": "references/x.pdf"}],
        [{"source": "concept_hi", "target": "r1"},
         {"source": "concept_hi", "target": "concept_lo"}],
    )
    rows = m.score_concepts(g)
    assert [r["id"] for r in rows] == ["concept_hi", "concept_lo"]
    assert rows[0]["support"] == 1 and rows[0]["degree"] == 2
