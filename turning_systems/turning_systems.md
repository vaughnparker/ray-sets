# Turning systems

**The 16 polyhedral ray-sets carry exactly 21 turning systems.**

A ray-set records only *which directions you can turn*. A **turning system** adds
*how far*: an assignment $\nu$ giving each ray a permitted turn order, which is
allowed to be a proper divisor of what the geometry would permit. It is the finer
classification defined in [`../intro.md`](../intro.md), and it is what separates a
3x3x3 from a 3x3x2 Domino — same six rays, different turn orders.

```bash
python turning_systems.py
```

## The result

Eleven of the sixteen ray-sets admit exactly one turning system. All the freedom
lives in the four ray-sets built on **O's 6-family** — the cube's face axes:

| ray-set | turning systems | $\lvert G\rvert$ | turn orders |
|---|---|---|---|
| `O · 6` | **3** | 4 | all rays order 2 |
| | | 8 | one axis-pair at 4, two pairs at 2 — **the Domino** |
| | | 24 | all rays order 4 — **the 3x3x3** |
| `O · 6+8` | **2** | 12 | 6-family at 2, 8-family at 3 |
| | | 24 | 6-family at 4, 8-family at 3 |
| `O · 6+12` | **2** | 24 | 6-family at 2, 12-family at 2 |
| | | 24 | 6-family at 4, 12-family at 2 |
| `O · 6+8+12` | **2** | 24 | 6-family at 2, rest forced |
| | | 24 | 6-family at 4, rest forced |
| the other 11 | **1** each | — | fully forced |

$12 \times 1 + 3 + 2 + 2 + 2 = 21$.

## Why the freedom is so scarce

This is settled before any code runs. A turn order must divide the order of the
ray's stabiliser, and in $T$, $O$ and $I$ stabilisers have order only **2, 3, 4 or
5**. Of those, **4 is the only one with a proper divisor $\ge 2$** — you can halve a
quarter-turn to a half-turn, but a 3-fold or 5-fold axis has nowhere to go, and an
axis already at 2 cannot be reduced further.

So the only ray that can ever be *dialled down* is a 4-fold one, and 4-fold rays
occur in exactly one place: O's 6-family. Every other ray in all sixteen ray-sets
has its turn order forced by geometry.

## What rules out the rest

Given that freedom, `O · 6` has $2^6 = 64$ raw assignments. Only three survive, and
the condition that kills the others is **equivariance**: $\nu$ must be constant on
the orbits of the group the turns generate.

The instructive failure is trying to leave *two* axis-pairs at 90° and restrict the
third to 180°. It looks reasonable and it is not legal: a 90° turn about $x$ carries
the $y$ axis onto the $z$ axis, so those two rays lie in one orbit and must share a
turn order. The restriction contradicts itself.

Turn it around — restrict *two* pairs to 180° and keep one at 90° — and nothing is
carried anywhere it shouldn't be. That survivor is the Domino, and the physical
puzzle matches: a 3x3x2 has two square 3x3 layers that turn 90° about the short
axis, while its four side faces are 3x2 rectangles and manage only 180°.

## Two things worth noticing

**Same group, different system.** Both turning systems on `O · 6+12` generate a
group of order 24. They are still genuinely different systems, because $\nu$ differs
— in one, face axes may only be half-turned, even though 90° rotations exist inside
the generated group. What you are *permitted* to turn is not the same as what your
moves generate.

**Turning systems still do not determine the puzzle.** A Skewb and a Dino Cube are
the same ray-set *and* the same turning system — `O · 8` with every ray at order 3 —
yet they are different puzzles, because their cuts sit at different depths. Turn
order and cut depth are independent refinements; neither contains the other.

| object | records | count |
|---|---|---|
| ray-set | directions | **16** |
| turning system | directions + how far | **21** |
| puzzle | directions + how far + where you cut | infinite |

## Method

For each ray-set the script computes, for every ray, the turn orders that leave the
ray-set intact; enumerates all assignments; builds the generated group by closure;
and keeps those where $\nu$ is constant on the group's orbits. Survivors are then
de-duplicated up to $O(3)$ using the symmetries of that ray-set, so that "the 4-fold
axis is $z$" and "the 4-fold axis is $x$" are not counted twice.

Finiteness — condition (3) in `intro.md` — costs nothing here. Every permitted turn
permutes the finite set $R$, and $R$ spans space, so the generated group embeds in
the permutations of $R$ and is finite automatically.
