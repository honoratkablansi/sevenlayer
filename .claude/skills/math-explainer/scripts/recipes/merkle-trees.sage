import json, os, hashlib
os.makedirs("assets/figures", exist_ok=True)

leaves = ["row0:alice:7", "row1:bob:2", "row2:carol:9", "row3:dave:5"]

def H(tag, data):
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(tag.encode() + b":" + data).hexdigest()

def node(left, right):
    return H("node", (left + right).encode())

leaf_hashes = [H("leaf", leaf) for leaf in leaves]
level1 = [node(leaf_hashes[0], leaf_hashes[1]), node(leaf_hashes[2], leaf_hashes[3])]
root = node(level1[0], level1[1])

target_index = 2
auth_path = [
    {"level": 0, "side": "right", "sibling": leaf_hashes[3]},
    {"level": 1, "side": "left", "sibling": level1[0]},
]
auth_path_json = [{"level": int(step["level"]), "side": step["side"], "sibling": step["sibling"]} for step in auth_path]

def verify_path(leaf, index, path, expected_root):
    cur = H("leaf", leaf)
    idx = index
    for step in path:
        sib = step["sibling"]
        if step["side"] == "right":
            cur = node(cur, sib)
        else:
            cur = node(sib, cur)
        idx //= 2
    return cur == expected_root, cur

verified, recomputed_root = verify_path(leaves[target_index], target_index, auth_path, root)
tampered_leaves = list(leaves)
tampered_leaves[target_index] = "row2:carol:10"
tampered_leaf_hashes = [H("leaf", leaf) for leaf in tampered_leaves]
tampered_level1 = [node(tampered_leaf_hashes[0], tampered_leaf_hashes[1]), node(tampered_leaf_hashes[2], tampered_leaf_hashes[3])]
tampered_root = node(tampered_level1[0], tampered_level1[1])

fig = "assets/figures/merkle-trees.svg"
G = Graphics()
coords = {
    "root": (0, 1.6),
    "n0": (-1.6, 0.5),
    "n1": (1.6, 0.5),
    "l0": (-2.4, -0.7),
    "l1": (-0.8, -0.7),
    "l2": (0.8, -0.7),
    "l3": (2.4, -0.7),
}
for a, b in [("root", "n0"), ("root", "n1"), ("n0", "l0"), ("n0", "l1"), ("n1", "l2"), ("n1", "l3")]:
    col = "red" if (a, b) in [("root", "n1"), ("n1", "l2")] else "gray"
    G += line([coords[a], coords[b]], color=col, thickness=2)
for name, pos in coords.items():
    col = "red" if name in ["root", "n1", "l2"] else "lightgray"
    G += circle(pos, 0.28, color=col, thickness=2)
    label = root[:6] if name == "root" else name
    if name.startswith("l"):
        label = leaves[int(name[1])].split(":")[0]
    G += text(label, pos, fontsize=8, color="black")
G += text("one leaf opens through two sibling hashes", (0, -1.45), fontsize=10, color="black")
G += text("tamper a leaf -> root changes", (0, -1.75), fontsize=10, color="red")
G.axes(False)
G.save(fig, figsize=[7, 4], dpi=200)

print(json.dumps({
    "figure": fig,
    "hash": "SHA-256",
    "leaves": leaves,
    "leaf_hashes": leaf_hashes,
    "root": root,
    "root_prefix": root[:12],
    "target_index": int(target_index),
    "auth_path": auth_path_json,
    "path_length": int(len(auth_path)),
    "recomputed_root": recomputed_root,
    "verified": bool(verified),
    "tampered_leaf": tampered_leaves[target_index],
    "tampered_root": tampered_root,
    "tampered_root_prefix": tampered_root[:12],
    "root_changed": bool(tampered_root != root)
}))
