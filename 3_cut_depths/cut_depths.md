# Cut depths

*Not written yet — a placeholder for the third investigation.*

The first two folders classify a puzzle's **directions** (16 ray-sets) and **how far
each may turn** (21 turning systems). Both counts are finite. This one is where
that ends.

Fix a ray-set, put one cut perpendicular to every ray, and slide all the cuts to the
same depth $d$. The depth is a continuous parameter, so there are infinitely many
values — but the *puzzle* only changes at finitely many critical depths, where cut
planes start or stop meeting inside the body. Between those, the piece structure is
constant.

A rough Monte-Carlo probe suggests the two behave very differently:

- **`O · 6`** — 27 cells at every depth, which is 26 pieces plus the core: the
  3x3x3, and nothing else. Its six planes are three perpendicular parallel pairs, so
  sliding $d$ never changes which planes cross which. Only at $d = 0$ exactly, where
  opposite planes collide, do you get something different — the 2x2x2.
- **`I · 12`** — a ladder of roughly six distinct regimes. At the shallow end it
  settles at 63 cells: 62 pieces plus the core, which is exactly the Megaminx. The
  deeper regimes are the other face-turning dodecahedra.

The sampling is not trustworthy in detail — small cells get missed, and some of the
apparent transitions may be noise. The work here is to replace it with an **exact
arrangement computation**: find the critical depths analytically, and count pieces
per regime exactly, for each of the 16.
