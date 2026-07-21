"""The face-turning polyhedron of each ray-set.

For a ray-set R, take the body

    P = { x : r . x <= 1  for every ray r in R }

Every ray contributes exactly one face, tangent to the unit sphere at the point
where that ray pierces it.  So P has as many faces as R has rays, and
face-turning P is precisely turning about the rays: P is the canonical puzzle
shape for that ray-set.  `O . 6` gives a cube, `O . 8` an octahedron, `I . 12`
a dodecahedron — the Megaminx.

    python polyhedra.py

Prints the face/vertex/edge counts and writes raysets_polyhedra.png.  The
geometry below is plain NumPy, so a notebook can import this module without
disturbing its own plotting backend.
"""
import os
import sys
from itertools import combinations

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import raysets                                                   # noqa: E402

TOL = 1e-5
PALETTE = ["#3b7dd8", "#e8833a", "#2ca58d"]   # one colour per ray family


def corners(R):
    """Every vertex of P — solve each triple of planes, keep the feasible points."""
    out = []
    for i, j, k in combinations(range(len(R)), 3):
        A = R[[i, j, k]]
        if abs(np.linalg.det(A)) < 1e-9:
            continue
        p = np.linalg.solve(A, np.ones(3))
        if np.all(R @ p <= 1 + TOL):
            if not any(np.allclose(p, q, atol=TOL) for q in out):
                out.append(p)
    return np.array(out)


def face(r, V):
    """The vertices lying on face r, wound in order around the ray."""
    on = np.array([v for v in V if abs(r @ v - 1) < TOL])
    u = np.cross(r, [1.0, 0.0, 0.0])
    if np.linalg.norm(u) < 0.1:
        u = np.cross(r, [0.0, 1.0, 0.0])
    u = u / np.linalg.norm(u)
    w = np.cross(r, u)
    centred = on - on.mean(axis=0)
    return on[np.argsort(np.arctan2(centred @ w, centred @ u))]


def polyhedron(rs):
    """(faces, colours, vertices) for one ray-set — a face per ray, coloured by family."""
    V = corners(raysets.rays(rs))
    faces, colours = [], []
    for f, fam in enumerate(rs.families):
        for r in fam:
            faces.append(face(r, V))
            colours.append(PALETTE[f % len(PALETTE)])
    return faces, colours, V


def the_16():
    """The 16 distinct ray-sets, in reading order."""
    sets = raysets.build()
    kept, _ = raysets.collapse(sets)
    return [sets[i] for i in kept]


def draw(ax, rs, faces=None, colours=None, V=None):
    """Render one polyhedron onto a 3D axes."""
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    if faces is None:
        faces, colours, V = polyhedron(rs)
    ax.add_collection3d(Poly3DCollection(
        faces, facecolors=colours, edgecolors="white", linewidths=0.6, alpha=0.95))
    lim = np.abs(V).max() * 1.05
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim)
    ax.set_box_aspect((1, 1, 1))
    ax.set_axis_off()


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(14, 15))
    print(f"{'ray-set':<16}{'faces':>6}{'verts':>7}{'edges':>7}")
    print("-" * 36)

    for n, rs in enumerate(the_16()):
        faces, colours, V = polyhedron(rs)
        edges = sum(len(f) for f in faces) // 2
        print(f"{raysets.label(rs):<16}{len(faces):>6}{len(V):>7}{edges:>7}")

        ax = fig.add_subplot(4, 4, n + 1, projection="3d")
        draw(ax, rs, faces, colours, V)
        ax.set_title(f"{raysets.label(rs)}  ({len(faces)} faces)", fontsize=9)
        ax.view_init(elev=22, azim=30)

    fig.suptitle("The face-turning polyhedron of each ray-set", fontsize=13)
    fig.tight_layout()
    fig.savefig("raysets_polyhedra.png", dpi=110)
    print("\nwrote raysets_polyhedra.png")


if __name__ == "__main__":
    main()
