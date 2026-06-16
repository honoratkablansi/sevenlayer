import hashlib
from manim import *

LEAVES = ["row0:alice:7", "row1:bob:2", "row2:carol:9", "row3:dave:5"]


def H(tag, data):
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(tag.encode() + b":" + data).hexdigest()


def node(left, right):
    return H("node", (left + right).encode())


LEAF_HASHES = [H("leaf", leaf) for leaf in LEAVES]
LEVEL1 = [node(LEAF_HASHES[0], LEAF_HASHES[1]), node(LEAF_HASHES[2], LEAF_HASHES[3])]
ROOT = node(LEVEL1[0], LEVEL1[1])
TARGET_INDEX = 2
AUTH_PATH = [
    {"level": 0, "side": "right", "sibling": LEAF_HASHES[3]},
    {"level": 1, "side": "left", "sibling": LEVEL1[0]},
]
TAMPERED = list(LEAVES)
TAMPERED[TARGET_INDEX] = "row2:carol:10"
TAMPERED_HASHES = [H("leaf", leaf) for leaf in TAMPERED]
TAMPERED_LEVEL1 = [node(TAMPERED_HASHES[0], TAMPERED_HASHES[1]), node(TAMPERED_HASHES[2], TAMPERED_HASHES[3])]
TAMPERED_ROOT = node(TAMPERED_LEVEL1[0], TAMPERED_LEVEL1[1])

SCENE_VALUES = {
    "root": ROOT,
    "root_prefix": ROOT[:12],
    "target_index": TARGET_INDEX,
    "path_length": len(AUTH_PATH),
    "verified": True,
    "tampered_root": TAMPERED_ROOT,
    "tampered_root_prefix": TAMPERED_ROOT[:12],
    "root_changed": TAMPERED_ROOT != ROOT,
}


class MerkleTreesScene(Scene):
    def construct(self):
        title = Text("Merkle tree: one root, one opened path", font_size=32).to_edge(UP)
        self.play(Write(title))
        positions = {
            "root": UP * 1.6,
            "n0": LEFT * 2 + UP * 0.2,
            "n1": RIGHT * 2 + UP * 0.2,
            "l0": LEFT * 3 + DOWN * 1.5,
            "l1": LEFT * 1 + DOWN * 1.5,
            "l2": RIGHT * 1 + DOWN * 1.5,
            "l3": RIGHT * 3 + DOWN * 1.5,
        }
        edges = VGroup()
        for a, b in [("root", "n0"), ("root", "n1"), ("n0", "l0"), ("n0", "l1"), ("n1", "l2"), ("n1", "l3")]:
            color = RED if (a, b) in [("root", "n1"), ("n1", "l2")] else GREY
            edges.add(Line(positions[a], positions[b], color=color))
        self.play(Create(edges))
        nodes = VGroup()
        for name, pos in positions.items():
            color = RED if name in ["root", "n1", "l2"] else BLUE
            dot = Dot(pos, color=color, radius=0.12)
            lab = Text(ROOT[:8] if name == "root" else name, font_size=18, color=color).next_to(dot, DOWN, buff=0.08)
            nodes.add(VGroup(dot, lab))
        self.play(FadeIn(nodes))
        path = Text("leaf 2 opens with two sibling hashes", font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(FadeIn(path))
        tamper = Text(f"tamper -> root {TAMPERED_ROOT[:8]}", font_size=23, color=RED).next_to(path, UP, buff=0.25)
        self.play(FadeIn(tamper), Flash(nodes[5][0], color=RED))
        self.wait(0.7)
