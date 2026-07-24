# Why only these shapes? Klein and the finite rotation groups

This repository keeps arriving at the same three symmetries — **T** (tetrahedral),
**O** (octahedral) and **I** (icosahedral) — plus two endlessly-repeating families,
the turntables $C_n$ and the prisms $D_n$. That short list is not a fact about
puzzles. It is a theorem about rotations in three-dimensional space, roughly a
hundred and fifty years old, and this note explains where it comes from.

No mathematics beyond high school is needed. We will go slowly at the one step that
deserves it.

## The question, made precise

Pick up a ball and spin it about its centre. That is a *rotation*. Do one rotation,
then another, and the net effect is again a single rotation about some axis — two
spins always combine into one.

Now imagine collecting some rotations together into a set with two properties:

- **Closed.** Combine any two rotations in the set, and the result is also in the
  set. (No move takes you outside the collection.)
- **Finite.** There are only finitely many rotations in it.

A collection like this is exactly what the symmetry of a solid object looks like: the
rotations that leave a cube looking unchanged form such a set, and so do the
rotations of any twisty puzzle. Mathematicians call it a **finite rotation group**;
we will just call it a **symmetry system**.

The question is simply: *what are all the possible symmetry systems?* You might
expect infinitely many wildly different answers. The surprise is:

> **Every finite symmetry system in 3D is one of five kinds:**
> the turntables $C_n$, the prisms $D_n$, and the three polyhedral systems
> $T$, $O$, $I$.

That is the theorem. Everything below is history and proof.

## A little history

That the cube, the tetrahedron and the icosahedron have beautiful rotational symmetry
was known to the Greeks. What is modern is the word *only* — the proof that this
handful is the complete list, with nothing exotic hiding.

The classification took shape in the nineteenth century. Crystallographers came at it
first, because a crystal's atoms can only be arranged with certain symmetries:
**Johann Hessel** worked out the possible point symmetries in 1830, and **Auguste
Bravais** developed the lattice side in the 1840s. Their motivation was physical —
which crystals can exist — but the underlying question was the geometric one above.

The name usually attached to the result is **Felix Klein**, whose *Lectures on the
Icosahedron* (1884) is the canonical treatment. Klein's real quarry was startling:
he tied the symmetry of the icosahedron to the problem of solving fifth-degree
equations, something no formula in radicals can do. The icosahedral group turned out
to be the hidden obstruction, and his book made the rotation groups and their
structure into a subject of their own.

Being honest about attribution: the pieces were understood by several people before
Klein wrote them down together, so "Klein's theorem" is a convenient label more than
a claim that he alone discovered it. The proof we give below is the standard modern
one and appears in any first course in group theory. It is not Klein's original
argument, but it reaches his conclusion.

The same proof, told for the same audience of puzzlers, already exists on the web:
Jaap Scherphuis's [*Group Theory for Puzzles*](https://www.jaapsch.net/puzzles/groups.htm)
classifies the finite rotation groups by the identical pole-counting argument and
arrives at the same equation. His version reaches it through Burnside's orbit-counting
lemma; below we do the counting by hand instead, to keep the machinery out of the way.

## The key idea: poles

Here is the one geometric move the whole proof rests on.

Take any rotation in our system except "do nothing." It spins about some axis — a
line through the centre. Surround the ball with a large glass sphere and extend that
axis outward in both directions until it pierces the sphere. It comes out at **two
points**, dead opposite each other.

Call them the **poles** of that rotation. They are the only two points on the sphere
that the rotation leaves exactly where they were; everything else on the sphere gets
carried along by the spin. Every rotation, however tilted its axis, has exactly two
poles.

From now on we forget the rotations' angles and just watch their poles move around on
the sphere. That turns an awkward question about rotations into a countable question
about points.

## Counting one thing two ways

Let $N$ be the total number of rotations in our system, *including* the do-nothing
one. We are going to count a certain collection of pairs in two different ways, and
because the two counts describe the very same collection, they must be equal — and an
equation drops out.

The pairs we count are: **(a rotation that is not the do-nothing one, together with a
pole it holds still).**

**Count them by rotation.** Throw away the do-nothing rotation, leaving $N-1$ of them.
Each one holds exactly its own two poles still. So the number of pairs is

$$2(N - 1).$$

**Count them by pole.** Look at a single pole $p$. Some rotations hold it still — at
the very least the do-nothing one, but often more. Write $n_p$ for how many rotations
in the whole system fix $p$ (counting do-nothing). Then the number of *non*-do-nothing
rotations fixing $p$ is $n_p - 1$. Add that up over every pole:

$$\sum_{\text{poles } p} (n_p - 1).$$

Same pairs, so the two counts agree:

$$2(N - 1) \;=\; \sum_{\text{poles } p} (n_p - 1). \tag{$\ast$}$$

## How big is a family?

To simplify the right-hand side we need one more idea, and this is the step worth
slowing down for.

The poles come in **families**. Start at one pole and apply every rotation of the
system to it; it hops around to various other poles. All the poles reachable this way
form one family. (On a cube, the six face-poles are one family, the eight
corner-poles another, the twelve edge-poles a third — a rotation of the cube never
sends a face-pole to a corner-pole.) Every pole in a family is held still by the same
number of rotations; call it $n$ for that family.

**Claim: a family whose poles are each held still by $n$ rotations has exactly $N/n$
poles in it.**

Here is why, made concrete. Fix your eye on one pole $p$ of the family. Run through
all $N$ rotations and sort them into **bins** by where they send $p$ — one bin per
destination pole.

- The bin for "$p$ stays home" is just the rotations that hold $p$ still: there are
  $n$ of them.
- **Every other bin also has exactly $n$ rotations.** Suppose some rotation $g$ sends
  $p$ to another pole $q$. Which rotations land $p$ on $q$? Take *any* rotation $h$
  that holds $p$ still, and then do $g$ afterwards: $p$ doesn't move under $h$, then
  $g$ carries it to $q$. That is a different landing-on-$q$ rotation for each of the
  $n$ choices of $h$ — and there are no others, because if two rotations both send $p$
  to $q$, then doing one and undoing the other brings $p$ home, so they differ only by
  a hold-$p$-still rotation. So the $q$-bin has exactly $n$ rotations too.

Every bin holds $n$ rotations, and the bins account for all $N$ of them, so the number
of bins is $N/n$. And there is one bin per pole in the family. Therefore the family
has $N/n$ poles. $\blacksquare$

Quick check on the cube, where $N = 24$: the corner family has $n = 3$, and indeed
$24/3 = 8$ corners; the faces have $n = 4$ and $24/4 = 6$; the edges have $n = 2$ and
$24/2 = 12$. All three come out right.

## The equation

Now regroup the sum in $(\ast)$ family by family. A family with hold-count $n_i$
contributes (its size) $\times (n_i - 1)$ pairs, and its size is $N / n_i$. So

$$2(N - 1) \;=\; \sum_{\text{families } i} \frac{N}{n_i}\,(n_i - 1).$$

Divide both sides by $N$. On the right, $\frac{1}{n_i}(n_i - 1) = 1 - \frac{1}{n_i}$;
on the left, $\frac{2(N-1)}{N} = 2 - \frac{2}{N}$. That gives the equation the whole
argument was aiming at:

$$\boxed{\;\sum_{i} \left(1 - \frac{1}{n_i}\right) \;=\; 2 - \frac{2}{N}\;}$$

Every symmetry system, whatever it is, produces a handful of families with
hold-counts $n_1, n_2, \dots$ and a total size $N$, and those numbers are locked
together by this one relation. Notice we never used the cube, or any particular
shape — only that rotations compose, that there are finitely many, and that each has
two poles. So the equation holds for *every* finite symmetry system there is.

## Solving it

Now we just find every whole-number solution. Each $n_i$ is at least $2$ (a pole no
real rotation fixes is not a pole of the system), so each term $1 - 1/n_i$ is at least
$\tfrac12$ and less than $1$. The right side, $2 - 2/N$, is less than $2$, and — as
long as the system has more than one rotation — at least $1$.

**How many families can there be?** If there were four or more, the left side would be
at least $4 \times \tfrac12 = 2$, too big. If there were only one, the left side would
be below $1$, too small. So there are **two or three families**.

**Two families.** The equation becomes $\frac{1}{n_1} + \frac{1}{n_2} = \frac{2}{N}$.
Since neither hold-count can exceed $N$, the only way two such fractions add to
$2/N$ is $n_1 = n_2 = N$. Two families, each a single pole fixed by everything: the
two ends of one axis. Every rotation shares that axis — this is the **turntable**
$C_N$, and it exists for every $N$.

**Three families.** Now $\frac{1}{n_1} + \frac{1}{n_2} + \frac{1}{n_3} = 1 +
\frac{2}{N}$, which is more than $1$. Order them $n_1 \le n_2 \le n_3$.

- If the smallest were $3$ or more, three such fractions couldn't exceed $1$. So
  $n_1 = 2$. That leaves $\frac{1}{n_2} + \frac{1}{n_3} = \frac12 + \frac{2}{N}$.
- If $n_2$ were $4$ or more, the left side couldn't clear $\tfrac12$. So $n_2$ is
  $2$ or $3$.
  - $n_2 = 2$ gives $\frac{1}{n_3} = \frac{2}{N}$, so $n_3 = N/2$: two half-turn
    families and one more. This is the **prism** $D_{N/2}$, one for every even $N$.
  - $n_2 = 3$ gives $\frac{1}{n_3} = \frac16 + \frac{2}{N}$, which is more than
    $\tfrac16$, so $n_3$ is $3$, $4$, or $5$ — and each pins $N$ to a single value:

$$(2,3,3)\Rightarrow N=12,\qquad (2,3,4)\Rightarrow N=24,\qquad (2,3,5)\Rightarrow N=60.$$

And that is the entire list. Beyond the two endless families, there are exactly three
special solutions, and nothing can hide above $N = 60$ — the arithmetic leaves no
room.

## Reading the answers as shapes

The three special solutions arrive as bare numbers, but they are shapes in disguise.
Turn each hold-count $n_i$ into a family size $N/n_i$:

| solution | $N$ | family sizes | the shape it is |
|---|---|---|---|
| $(2,3,3)$ | 12 | 6, 4, 4 | **tetrahedron** — 6 edges, 4 corners, 4 faces |
| $(2,3,4)$ | 24 | 12, 8, 6 | **cube / octahedron** — 12 edges, 8 corners, 6 faces |
| $(2,3,5)$ | 60 | 30, 20, 12 | **dodecahedron / icosahedron** — 30 edges, 20 corners, 12 faces |

The Platonic solids fall out of one equation in whole numbers, without a polyhedron
ever being drawn. These three symmetry systems are the $T$, $O$ and $I$ that the rest
of this repository builds on.

(One quirk to notice, because it matters elsewhere: the tetrahedron's list has *two*
families of size 4 — its corners and its faces. On a cube, a corner sits opposite a
face across one axis, so they share a family; on a tetrahedron, a corner sits opposite
a *face*, and no rotation ever swaps the two, so they stay separate. See
[`intro.md`](intro.md) and the de-duplication in [`1_ray_sets/`](1_ray_sets).)

## A last echo

The turning point in the proof was the inequality
$\frac{1}{n_1} + \frac{1}{n_2} + \frac{1}{n_3} > 1$. That same inequality shows up
whenever mathematicians ask which symmetric tilings are possible. Greater than $1$
gives the finitely many patterns that fit on a **sphere** — our polyhedral groups.
Exactly equal to $1$ gives the patterns that tile a flat **plane** — the seventeen
wallpaper symmetries. Less than $1$ opens onto the infinite world of tilings of the
**hyperbolic plane**, Escher's shrinking angels and devils among them.

So the shortness of our list is not a quirk of puzzles at all. It is the sphere
being a small, tightly constrained place to live — and this repository is a tour of
the sixteen ways to cut it.
