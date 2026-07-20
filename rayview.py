"""Interactive viewer for the 21 ray-sets.

    python rayview.py

Drag to rotate.  Left / right arrows (or p / n) step through the ray-sets.
"""
import numpy as np
import matplotlib.pyplot as plt
import raysets

SETS = raysets.build()
PALETTE = ["#3b7dd8", "#e8833a", "#2ca58d"]   # one colour per family

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection="3d")
i = 0


def draw():
    ax.clear()
    rs = SETS[i]
    for f, fam in enumerate(rs.families):
        c = PALETTE[f % len(PALETTE)]
        for v in fam:
            ax.plot([0, v[0]], [0, v[1]], [0, v[2]], color=c, lw=1.5)
        ax.scatter(fam[:, 0], fam[:, 1], fam[:, 2],
                   color=c, s=25, depthshade=False)
    ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_zlim(-1.1, 1.1)
    ax.set_box_aspect((1, 1, 1))
    ax.set_axis_off()
    ax.set_title(f"{raysets.label(rs)}     {raysets.count(rs)} rays\n"
                 f"[{i + 1}/{len(SETS)}]   ← / → to change", fontsize=11)
    fig.canvas.draw_idle()


def on_key(event):
    global i
    if event.key in ("right", "n", " "):
        i = (i + 1) % len(SETS); draw()
    elif event.key in ("left", "p"):
        i = (i - 1) % len(SETS); draw()


fig.canvas.mpl_connect("key_press_event", on_key)
draw()
plt.show()
