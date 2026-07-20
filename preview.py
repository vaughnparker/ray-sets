"""Render the montage images.

    python preview.py

Writes raysets_preview.png  (all 21 candidates)
   and raysets_distinct.png (the 16 that survive de-duplication).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import raysets

PALETTE = ["#3b7dd8", "#e8833a", "#2ca58d"]   # one colour per family


def montage(sets, cols, path, title):
    rows = -(-len(sets) // cols)
    fig = plt.figure(figsize=(2.0 * cols, 2.2 * rows))
    for k, rs in enumerate(sets):
        ax = fig.add_subplot(rows, cols, k + 1, projection="3d")
        for f, fam in enumerate(rs.families):
            c = PALETTE[f % len(PALETTE)]
            for v in fam:
                ax.plot([0, v[0]], [0, v[1]], [0, v[2]], color=c, lw=1)
            ax.scatter(fam[:, 0], fam[:, 1], fam[:, 2],
                       color=c, s=8, depthshade=False)
        ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_zlim(-1.1, 1.1)
        ax.set_box_aspect((1, 1, 1))
        ax.set_axis_off()
        ax.set_title(f"{raysets.label(rs)}  ({raysets.count(rs)})", fontsize=8)
        ax.view_init(elev=20, azim=30)
    fig.suptitle(title, fontsize=12)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    print("wrote", path)


if __name__ == "__main__":
    sets = raysets.build()
    kept, _ = raysets.collapse(sets)
    montage(sets, 7, "raysets_preview.png", "All 21 candidate ray-sets")
    montage([sets[i] for i in kept], 4, "raysets_distinct.png",
            "The 16 distinct ray-sets")

    # The two non-polyhedral families, side by side: C_n is the same ray-set
    # every time, D_n gains two rays with every step of n.
    infinite = ([raysets.cyclic(n) for n in (3, 5, 7)] +
                [raysets.dihedral(n) for n in (2, 3, 4, 5, 6, 7)])
    montage(infinite, 3, "raysets_infinite.png",
            "The non-polyhedral families — C_n never changes, D_n grows with n")
