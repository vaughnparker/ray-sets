# What is a turning system?

A **ray-set** answers one question about a twisty puzzle: *which directions can you
turn around?* It is a bundle of rays and nothing else — it deliberately forgets the
colours, the cuts, and how far each turn goes.

A **turning system** puts back one of those forgotten things: *how far* you are
allowed to turn about each ray.

## The one new number

Give each ray a **turn order** — the number of equal steps a turn about it comes in.
Order 4 means quarter turns (90°), order 3 means thirds (120°), order 2 means half
turns only (180°).

The turn order is allowed to be *smaller* than the geometry would permit: you can
always choose to turn an axis less freely than it could go, restricting a
quarter-turn axis to half-turns only. That single freedom is the whole difference
between a ray-set and a turning system.

## Why it is more than a ray-set

Take the six face-axes of a cube — one ray-set. Three different puzzles live on it:

| turn orders | puzzle |
|---|---|
| all 4 | 3×3×3 Rubik's Cube |
| all 2 | tetrahedral edge-turning cube |
| one axis-pair at 4, the other two pairs at 2 | 3×3×2 Domino |

The same six rays every time. What separates the puzzles is only how far each face is
allowed to turn. The ray-set cannot tell them apart; the turning system can.

## The two rules

Not every assignment of turn orders is legal. Two conditions have to hold:

- **Closure.** Turning a ray by its allowed step must land the whole ray-set back on
  itself — the same landing-on-itself rule a ray-set already obeys.
- **Constant on families.** Rays that symmetry treats as interchangeable must be given
  the *same* turn order. You cannot quarter-turn one cube face while half-turning its
  neighbour, because a quarter turn carries one face onto the next: they belong to the
  same family, so they must share a turn order.

The Domino passes this test — its two square faces (one axis) turn 90°, and its four
side faces (a different family) turn 180°. Restricting *two* opposite face-pairs to
half-turns is consistent; restricting only *one* is not.

## How many are there?

Across the 16 ray-sets there are exactly **21 turning systems**. All but four ray-sets
force a single choice; the freedom lives entirely in the four built on the cube's face
axes — the only ones with a 4-fold axis, which is the only turn order with any room to
shrink.

The full enumeration, with the table of all 21 and why the rest are forced, is in
[turning_systems.md](turning_systems.md). For the formal definitions see
[../intro.md](../intro.md); for why only these symmetries exist at all,
[../tutorial_4_why_only_three/klein.md](../tutorial_4_why_only_three/klein.md).
