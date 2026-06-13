import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_master_graph as m  # noqa: E402


def _g(nodes, links):
    """Minimal node-link graph dict for tests."""
    return {"directed": True, "multigraph": False, "graph": {},
            "nodes": nodes, "links": links}
