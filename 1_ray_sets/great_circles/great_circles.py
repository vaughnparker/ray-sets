"""The great-circle arrangement of each ray-set.

For each ray r, the directions perpendicular to r form a great circle on the unit
sphere.  That circle is where the *deepest* cut about r — the one through the
centre — meets the surface.  Drawing every ray's great circle turns the spray of
axes into the puzzle's actual cut pattern.

Two rays that point opposite ways share a perpendicular plane, so there is one
circle per axis: half as many circles as rays.

The circles carve the sphere into regions, and those regions are the surface
pieces of the maximally-deep-cut puzzle.  For `O . 6` the three coordinate
circles cut out 8 octants — the eight pieces of a 2x2x2.  The count comes from
Euler's V - E + F = 2 and is exact.

    python great_circles.py

Prints circle / vertex / region counts and writes raysets_great_circles.png.  The
geometry is plain NumPy, so a notebook can import this without touching its
backend.
"""
import os
import sys
from itertools import combinations

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import raysets                                                   # noqa: E402

TOL = 1e-6
PALETTE = ["#3b7dd8", "#e8833a", "#2ca58d"]   # one colour per ray family


def axes(rs):
    """One (axis, colour) per circle: dedup the rays that point opposite ways."""
    out = []
    for f, fam in enumerate(rs.families):
        for r in fam:
            if not any(np.allclose(r, a, atol=TOL) or np.allclose(r, -a, atol=TOL)
                       for a, _ in out):
                out.append((r / np.linalg.norm(r), PALETTE[f % len(PALETTE)]))
    return out


def great_circle(axis, n=240):
    """Points of the great circle perpendicular to `axis`."""
    u = np.cross(axis, [1.0, 0.0, 0.0])
    if np.linalg.norm(u) < 0.1:
        u = np.cross(axis, [0.0, 1.0, 0.0])
    u = u / np.linalg.norm(u)
    w = np.cross(axis, u)
    t = np.linspace(0, 2 * np.pi, n)
    return np.cos(t)[:, None] * u + np.sin(t)[:, None] * w


def arrangement(rs):
    """(circles, vertices, edges, regions) of the great-circle arrangement.

    Two circles meet at two antipodal points; regions follow from Euler's
    V - E + F = 2.  Concurrency (many circles through one point) is handled,
    because edges are counted as vertices-per-circle rather than assuming
    circles cross in general position.
    """
    normals = [a for a, _ in axes(rs)]

    verts = []
    for a, b in combinations(normals, 2):
        d = np.cross(a, b)
        if np.linalg.norm(d) < TOL:
            continue
        d = d / np.linalg.norm(d)
        for p in (d, -d):
            if not any(np.allclose(p, q, atol=1e-5) for q in verts):
                verts.append(p)

    V = len(verts)
    E = sum(sum(abs(n @ v) < 1e-5 for v in verts) for n in normals)
    return len(normals), V, E, E - V + 2


def _cam(elev, azim):
    e, a = np.radians(elev), np.radians(azim)
    return np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])


def draw(ax, rs, elev=22, azim=30, split=True):
    """Render the arrangement onto a 3D axes.

    With `split`, near arcs are solid and far arcs faint, which reads as a
    sphere at a fixed view — use it for a still image.  Without it, every circle
    is drawn whole at one weight; use that when the view will rotate, since the
    near/far split is fixed to one camera and would otherwise freeze on drag.
    """
    for axis, colour in axes(rs):
        C = great_circle(axis)
        if not split:
            ax.plot(C[:, 0], C[:, 1], C[:, 2], color=colour, lw=1.3, alpha=0.85)
            continue
        near = C @ _cam(elev, azim) > 0
        front, back = C.copy(), C.copy()
        front[~near] = np.nan
        back[near] = np.nan
        ax.plot(back[:, 0], back[:, 1], back[:, 2], color=colour, lw=0.6, alpha=0.18)
        ax.plot(front[:, 0], front[:, 1], front[:, 2], color=colour, lw=1.4)
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
    ax.set_box_aspect((1, 1, 1))
    ax.set_axis_off()
    ax.view_init(elev=elev, azim=azim)


def the_16():
    sets = raysets.build()
    kept, _ = raysets.collapse(sets)
    return [sets[i] for i in kept]


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(14, 15))
    print(f"{'ray-set':<16}{'circles':>8}{'vertices':>9}{'regions':>8}")
    print("-" * 41)

    for n, rs in enumerate(the_16()):
        circles, V, E, F = arrangement(rs)
        print(f"{raysets.label(rs):<16}{circles:>8}{V:>9}{F:>8}")

        ax = fig.add_subplot(4, 4, n + 1, projection="3d")
        draw(ax, rs)
        ax.set_title(f"{raysets.label(rs)}   {circles} circles, {F} regions",
                     fontsize=8.5)

    fig.suptitle("The great-circle arrangement of each ray-set "
                 "(deepest cuts, and the pieces they make)", fontsize=13)
    fig.tight_layout()
    fig.savefig("raysets_great_circles.png", dpi=110)
    print("\nwrote raysets_great_circles.png")


if __name__ == "__main__":
    main()
