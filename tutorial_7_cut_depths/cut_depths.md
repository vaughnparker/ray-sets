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

## A counting convention to settle first

"How many regimes?" has more than one answer depending on what you count, so this
needs pinning down before any number is trustworthy.

VeryPuzzle's [CORD/DIRT pages](../resources.md) list "fundamental models" per axis
system — their name for cut-depth variants — with these counts:

| system | this repo's notation | VeryPuzzle | regime count we expect |
|---|---|---|---|
| C | `O · 6` | 6 | 4 |
| O | `O · 8` | 8 | 5 |
| RD | `O · 12` | 14 | 8 |
| D | `I · 12` | 12 | 7 |
| I | `I · 20` | 24 | 13 |
| RT | `I · 30` | 56 | 29 |

Every row fits **VeryPuzzle = 2·(our count) − 2** exactly. Writing $M$ for the number
of *generic* depth intervals (excluding the degenerate through-centre cut), our count
is $M + 1$ (the intervals plus $d=0$) while VeryPuzzle's is $2M$. The likely reading:
VeryPuzzle counts **both the intervals and the critical walls between them** as
separate models — the same split the [Radiolarian guide](../resources.md) draws
between "Type A" cuts (a piece appears; depth is a whole interval) and "Type D" cuts
(a piece disappears; depth is one exact wall). Neither count is wrong; they count
different objects.

Two caveats. The "regime count we expect" column comes from a separate analysis, not
from anything computed in this folder yet — so the $2M$ relationship is a **hypothesis
to verify** once the exact wall-finder exists, not a settled fact. And when we do
report a number, we should say plainly which convention it uses: distinct piece
configurations, or configurations-plus-walls.
