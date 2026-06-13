import sys
from pathlib import Path

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


def test_degree_map_counts_incidence():
    g = _g([{"id": "a"}, {"id": "b"}, {"id": "c"}],
           [{"source": "a", "target": "b"}, {"source": "a", "target": "c"}])
    assert m.degree_map(g) == {"a": 2, "b": 1, "c": 1}
