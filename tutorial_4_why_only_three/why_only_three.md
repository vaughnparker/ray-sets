# Why only three?

*A hunt for every possible arrangement of turning axes — and the moment we run out.*

This is the first half of the answer to "why are there only 7 elementary axis systems?"
The second half — turning what we find here into exactly seven — is
[`from_groups_to_raysets.md`](from_groups_to_raysets.md).

No maths beyond high school. We work in degrees, and the only formula we borrow is one
about triangles you can check yourself on a beach ball.

---

## 1. What we are hunting

We are not going to be handed a list and then check it. We are going to **go looking** —
build every axis system there is, one at a time, and keep going until we can prove to
ourselves there is nothing left to find.

It helps to know what that feels like when it works. Think about the Platonic solids. The
bad explanation is *"there are five; here is a proof there is no sixth."* The good
explanation is: **build a corner.**

> Three triangles around a point? That closes up — the tetrahedron. Four triangles? The
> octahedron. Five? The icosahedron. Six triangles? Now the angles total exactly 360°,
> the corner lies flat, and there is no solid at all. Triangles are done. Squares: three
> around a point gives the cube; four squares is 360° again, flat, dead. Pentagons: three
> gives the dodecahedron; four overshoots 360°, impossible. Hexagons: three hexagons is
> *already* 360°, dead before we start — and every shape after the hexagon is worse.

That explanation satisfies because you did not take anyone's word for it. You went
through every case and watched the door close.

We are going to do exactly that for turning axes. We need three things first: something
to build with, a way to describe what we have built, and one test that says whether it
can exist. Sections 2–5 set those up. Section 6 is the hunt.

---

## 2. The rule everything obeys

From the first chapter, a valid puzzle obeys one rule:

> **Rotate the whole puzzle about one of its own axes, and every axis must land where
> another axis already was.**

If an axis lands in empty space, a cut would run through the middle of a piece and the
puzzle jams. That is the entire physical constraint.

So the thing we are hunting is **a finite collection of rotations, where doing one after
another always gives you another rotation in the collection.** Call it a *symmetry
system*, and write $N$ for how many rotations it holds (counting "do nothing").

A cube has $N = 24$: twenty-four ways to rotate it and have it look untouched.

---

## 3. Turning rotations into dots

Rotations are awkward to count. Dots are easy.

Every rotation spins about an axis. Put a glass sphere around the puzzle and extend that
axis outward both ways: it pierces the sphere at **two points**, on opposite sides. Call
them the **poles** of that rotation — the only two points it leaves alone. Everything
else slides.

Mark every pole of every rotation and you get a finite pattern of dots on a sphere.
**The hunt for symmetry systems is now a hunt for dot patterns.**

For the cube, the dots land in three obvious places:

| Where the dot is | How many | Rotations holding it still |
|---|---|---|
| through a face centre | 6 | 4 (90°, 180°, 270°, or nothing) |
| through a corner | 8 | 3 (120°, 240°, or nothing) |
| through an edge midpoint | 12 | 2 (180°, or nothing) |

That last number is the one that matters. Call it the dot's **order**. The cube has dots
of order 4, order 3, and order 2 — and nothing else.

---

## 4. Every axis system is just three numbers

Here is the step that makes the hunt possible. It gives us our equivalent of "a corner
made of triangles" — a small thing we can try to build.

Take a cube and look at one face. Draw both diagonals, and both lines joining opposite
edge-midpoints. The face is now cut into **8 right triangles**. Do that to all six faces
and the surface carries $6 \times 8 = 48$ of them. Push them out onto the sphere and the
sphere is tiled by 48 curved triangles, all identical.

This is not special to the cube. **In every symmetry system, the poles cut the sphere
into identical triangles.** Each triangle is the smallest patch the symmetry repeats —
one tile, stamped over and over.

Now look at the corners of a tile. Every one has:

- one corner on a **face-centre** dot,
- one corner on a **corner** dot,
- one corner on an **edge-midpoint** dot.

Each tile touches one dot of each kind. And that is *why* there were exactly three kinds
of dot: **a triangle has three corners.** Never four kinds, never two.

So a symmetry system is described by **three whole numbers** — the orders of its three
kinds of dot. Call them $p$, $q$, $r$. The cube is $(2, 3, 4)$.

**Those triples are what we will hunt through**, exactly like trying triangles, then
squares, then pentagons.

> **One thing we take on trust.** That the sphere always splits into identical triangles
> is the single fact we will not prove. It is true, and you can see it on any real solid —
> but proving it in general needs heavier machinery than this page wants. The classic
> proof (Klein's) avoids the assumption at the cost of being much fiddlier; it is in
> [`klein.md`](klein.md) if you want the airtight version.

---

## 5. The one test

We need to know which triples can exist. One test decides it.

**First, the tile's angles.** Look at a face-centre dot on the cube and count the tiles
meeting around it. Each of the 4 quarters of the face holds 2 of them, so **8 tiles** meet
there, sharing the full 360° evenly:

$$\frac{360°}{8} = 45°.$$

That dot had order 4, and $8 = 2 \times 4$ — twice the order, because tiles come in
mirror-image pairs, a left-handed and a right-handed one for each rotation. That holds
everywhere:

> **A dot of order $p$ has $2p$ tiles around it, so the tile's angle there is
> $\dfrac{360°}{2p} = \dfrac{180°}{p}$.**

Check it on the cube:

| Dot | order | tiles meeting | angle |
|---|---|---|---|
| face centre | 4 | 8 | $180/4 = 45°$ |
| corner | 3 | 6 | $180/3 = 60°$ |
| edge midpoint | 2 | 4 | $180/2 = 90°$ |

So the cube's tile is a triangle with angles **45°, 60°, 90°**. It is on any real cube; go
find it.

**Second, when can such a triangle exist?** Add the cube's up: $45 + 60 + 90 = 195°$. More
than 180°. On flat paper that is impossible — but this triangle is on a sphere, and
spherical triangles bulge.

Here is the borrowed fact, and it is easy to believe:

> **A spherical triangle's angles always overshoot 180°, and the overshoot *is* its size.**
> A triangle whose angles total $S$ covers
> $$\frac{S - 180°}{720°}$$
> of the sphere.

**Check it yourself.** On a globe: start at the north pole, go down to the equator, turn
90°, travel a quarter of the way round, turn 90°, go back up to the pole. Three right
angles, $S = 270°$. The formula says $(270-180)/720 = 1/8$ of the sphere — and it is
exactly one octant. ✓

Two consequences, and they are the whole test:

- The overshoot **must be greater than zero.** A tile with no area is not a tile.
- The overshoot tells you **how many tiles fit**: $720° \div \text{overshoot}$.

Cube: overshoot $= 195 - 180 = 15°$, so $720/15 = 48$ tiles — the 48 we drew. ✓ And since
tiles come in mirror pairs, the number of *rotations* is half that: **24**, exactly the
cube's 24 rotations. The test hands us the answer for free.

**That is the whole toolkit.** Pick three numbers, add $180/p + 180/q + 180/r$, and ask:
is it more than 180°?

---

## 6. The hunt

Now we go looking. Each number is at least 2 — a dot no real rotation holds still is not a
pole. Write them smallest first, $p \le q \le r$, and start at the bottom.

**Try $(2,2,2)$.** Angles $90 + 90 + 90 = 270°$. Overshoot 90°, so $720/90 = 8$ tiles and
4 rotations. It works — the symmetry of a brick: three perpendicular half-turn axes. Real,
but nothing in it has order 3 or more.

**Try $(2,2,3)$, then $(2,2,4)$, then $(2,2,5)$…** Angles $90 + 90 + 180/r$, which is
*always* more than 180°, however big $r$ gets:

| | angles | sum | tiles | rotations |
|---|---|---|---|---|
| $(2,2,3)$ | 90, 90, 60 | 240° | 12 | 6 |
| $(2,2,4)$ | 90, 90, 45 | 225° | 16 | 8 |
| $(2,2,5)$ | 90, 90, 36 | 216° | 20 | 10 |
| $(2,2,n)$ | 90, 90, $180/n$ | $>180°$ | $4n$ | $2n$ |

**This family never ends.** These are the turntables and prisms: one main axis of any
order you like, ringed by half-turn axes. A hexagonal pencil; a stop sign on a spindle.
They are real, and there are infinitely many — but notice what they share: **one special
axis, with everything else in a ring around it.** They are not really three-dimensional
arrangements; they are a wheel.

That is what "polyhedral" rules out, and it is the honest reason we set them aside: we
want systems where **at least two axes have order 3 or more**, so no single axis is in
charge. That means $q \ge 3$. Onward.

**Try $(2,3,3)$.** $90 + 60 + 60 = 210°$. Overshoot 30°, so $720/30 = 24$ tiles and **12
rotations** — exactly the number of ways to rotate a **tetrahedron**. Found one.

**Try $(2,3,4)$.** $90 + 60 + 45 = 195°$. Overshoot 15°, so 48 tiles and **24 rotations** —
the **cube**. Two.

**Try $(2,3,5)$.** $90 + 60 + 36 = 186°$. Overshoot 6°, so 120 tiles and **60 rotations** —
the **dodecahedron**. Three.

Watch the overshoot shrinking: 30°, 15°, 6°. The room is running out.

**Try $(2,3,6)$.** $90 + 60 + 30 = 180°$ **exactly.** Overshoot zero. The tile is flat and
has no area — there is no such spherical triangle. **Dead**, in precisely the way six
triangles around a point was dead.

**Try $(2,3,7)$.** $90 + 60 + 25\frac{5}{7} = 175\frac{5}{7}°$. *Below* 180. Worse than
dead — negative area.

**Back up; try a bigger middle number.** $(2,4,4)$: $90 + 45 + 45 = 180°$. Flat, dead.
$(2,4,5)$: $90 + 45 + 36 = 171°$. Dead.

**Try making the smallest number 3.** $(3,3,3)$: $60 + 60 + 60 = 180°$. Flat, dead.
$(3,3,4)$: $60 + 60 + 45 = 165°$. Dead.

And that is everything.

---

## 7. Why we can stop looking

We tried a dozen triples; there are infinitely many. How do we know nothing is hiding
further out?

Because of one simple fact: **$180/p$ gets *smaller* as $p$ gets bigger.** A 5-fold dot
contributes 36°; a 9-fold dot contributes 20°. Raising any of the three numbers only ever
*shrinks* the total.

So failure is permanent. Once a triple falls to 180° or below, **every triple with larger
numbers fails too** — you can only be making it worse. $(2,3,6)$ died, so $(2,3,7)$,
$(2,3,8)$, … are dead unchecked. $(2,4,4)$ died, so everything from there on is dead.
$(3,3,3)$ died, so every triple starting with 3 or more is dead.

We never had to look far. The survivors sit in a tiny corner near the bottom, and we
walked the whole corner:

| | verdict |
|---|---|
| $(2,2,n)$ | works forever — turntables and prisms, one axis in charge, set aside |
| $(2,3,3)$ | **works — tetrahedron**, 12 rotations |
| $(2,3,4)$ | **works — cube**, 24 rotations |
| $(2,3,5)$ | **works — dodecahedron**, 60 rotations |
| $(2,3,6)$, $(2,4,4)$, $(3,3,3)$ | flat — no area, impossible |
| everything else | worse still |

**Three.** Not because someone said so — because we went through the cases and there was
nowhere left to go.

---

## 8. The three that failed are not nothing

The near misses are the best part. Look at what died *exactly*:

$$(2,3,6): 90+60+30 = 180° \qquad (2,4,4): 90+45+45 = 180° \qquad (3,3,3): 60+60+60 = 180°$$

All three land on 180° on the nose. Zero overshoot means zero curvature — these tiles do
not fit on a sphere because they are **flat**. And flat tiles tile a **floor**: those three
are precisely the three ways to tile an infinite plane with identical triangles. You have
stood on all three in bathrooms and pavements.

Go past them and the overshoot turns negative, which needs a surface curving the *other*
way — a saddle. That is where the endlessly repeating patterns in Escher's prints live.

The same three numbers govern all of it:

$$\frac{180}{p} + \frac{180}{q} + \frac{180}{r} \;\begin{cases} > 180° & \text{sphere — our puzzles, finitely many} \\ = 180° & \text{flat floor — wallpaper patterns} \\ < 180° & \text{saddle — Escher} \end{cases}$$

Our list is short for a simple reason, worth saying plainly:

> **A sphere is a small place. You run out of room in a triangle.**

---

## 9. What we found, and what is next

Three symmetry families that are genuinely three-dimensional:

| | rotations | tile angles |
|---|---|---|
| **tetrahedron** | 12 | 90°, 60°, 60° |
| **cube** | 24 | 90°, 60°, 45° |
| **dodecahedron** | 60 | 90°, 60°, 36° |

(Plus the infinite turntable/prism family, set aside as not polyhedral; it returns in the
appendix.)

You may be wondering where the octahedron and icosahedron went. They are already here: an
octahedron has exactly the same rotations as a cube, and an icosahedron the same as a
dodecahedron. Each pair are **duals** — the corners of one point at the faces of the other —
so they share a symmetry system. Three systems, five solids.

That is still not "7 axis systems," because each family gives *several*: one for each of
its three kinds of dot — its faces, its corners, its edges. Three families times three
kinds is nine. Two of those nine turn out to be duplicates in disguise, which is why the
answer is **seven**.

That is the next file: [`from_groups_to_raysets.md`](from_groups_to_raysets.md).