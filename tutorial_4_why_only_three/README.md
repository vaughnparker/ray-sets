# Why only these? — the finiteness proof

Tutorial stop 4. Everything answering **"why is the list short, and why is it
complete?"** lives here.

The chapter is split in two, because "why are there only 7 elementary axis systems?"
is really two questions stacked:

| File | Question | Status |
|---|---|---|
| [`why_only_three.md`](why_only_three.md) | Why only **three** symmetry families — tetrahedron, cube, dodecahedron? | draft |
| [`from_groups_to_raysets.md`](from_groups_to_raysets.md) | How do those three become exactly **seven** axis systems? | to write |
| [`klein.md`](klein.md) | The same first question, done rigorously | done |

## Two proofs of the same thing

`why_only_three.md` and `klein.md` prove the *same* theorem by different routes, and
we keep both on purpose.

- **`why_only_three.md` is the one to read first.** Its engine is geometric: the poles
  cut the sphere into identical triangles with angles 180/p, 180/q, 180/r; a spherical
  triangle's angles must add to *more* than 180°; so `1/p + 1/q + 1/r > 1`, and that
  inequality has only four solutions. It works in degrees, needs no group theory, and
  hands back the correct rotation counts (12, 24, 60) as a free sanity check.
  Its one soft spot — flagged in the text — is that it *assumes* the poles tile the
  sphere into triangles.
- **`klein.md` is the airtight version.** It assumes nothing about tilings, deriving
  the same inequality by counting the pairs (rotation, pole it holds still) two ways.
  The cost is that the counting is fiddlier to follow.

Both land on the same inequality, which is the real theorem. Greater than 1 → the
sphere (our case); equal to 1 → flat wallpaper tilings; less than 1 → hyperbolic.

## Still to build

An HTML visualization: drag `p`, `q`, `r` and watch the fundamental triangle shrink to
nothing as the angle budget runs out — the moment the list stops.
