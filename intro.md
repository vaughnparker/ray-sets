## The coarse notion: ray-set

The physical constraint that makes a twisty puzzle work is this: **turning about one axis must carry the axis system onto itself.** If it didn't, a single turn would leave some other axis pointing into the middle of a piece, and the mechanism would jam. Everything follows from formalizing that.

> **Definition (ray-set).** A *ray-set* is a finite, nonempty set $R \subset S^2$ of unit vectors such that there exists a finite subgroup $G \leq SO(3)$ with
> 1. $G \cdot R = R$ (the group permutes the rays), and
> 2. every $r \in R$ is a *pole* of $G$ — i.e. $\mathrm{Stab}_G(r)$ is nontrivial (every ray is actually turnable).
>
> Two ray-sets are **identified** if some element of $O(3)$ maps one onto the other.

Three things this definition buys you:

- **Rays, not lines.** $r$ and $-r$ are distinct elements of $R$. This is your convention, and it's what makes ray-count equal feature-count uniformly, tetrahedron included.
- **Condition (2) forbids padding.** Without it you could throw an arbitrary $G$-orbit of non-pole points into $R$ and call it an axis system. Requiring nontrivial stabilizer means every listed ray corresponds to a real rotational symmetry.
- **Unions of pole orbits, automatically.** Conditions (1)+(2) together force $R$ to be a union of $G$-orbits of poles. Since a nontrivial finite $G \le SO(3)$ has at most 3 pole orbits, you immediately get "at most $2^3 - 1 = 7$ per group" — which is where the 7/7 in your count comes from, and it's the skeleton of the proof for (2).

Identifying up to $O(3)$ (not just $SO(3)$) means mirror-image systems count as the same — which is what you want, since a puzzle and its mirror have identical axis geometry.

## The finer notion: turning system

The ray-set deliberately forgets *how far* you're allowed to turn. That's exactly the information that distinguishes your tetrahedral-edge case from the face-turning cube, so the refinement is to just carry it along:

> **Definition (turning system).** A *turning system* is a pair $(R, \nu)$ where $R$ is a ray-set and $\nu: R \to \mathbb{Z}_{\geq 2}$ assigns each ray a **turn order**, subject to:
> 1. (closure) for each $r \in R$, the rotation $\rho_r$ by $2\pi/\nu(r)$ about $r$ satisfies $\rho_r(R) = R$;
> 2. (equivariance) $\nu(\rho(r)) = \nu(r)$ for every $\rho$ in $G = \langle \rho_r : r \in R\rangle$;
> 3. (finiteness) $G$ is finite.
>
> Identified up to $O(3)$, acting on $R$ and pulling back $\nu$.

$\nu(r)$ is the order of the cyclic group of *permitted* turns about $r$ — which may be a proper divisor of the order of the full stabilizer. That divisibility gap is the entire point.

The forgetful map $(R,\nu) \mapsto R$ is what relates the two notions, and it is **many-to-one**. Your tetrahedral case is precisely a fiber with more than one element:

| Turning system | $R$ | $\nu$ | Generated $G$ | Puzzle |
|---|---|---|---|---|
| $(R_6, \nu \equiv 4)$ | 6 cube-face rays | 4 | $O$, order 24 | 3x3x3 |
| $(R_6, \nu \equiv 2)$ | 6 cube-face rays | 2 | $D_2$, order 4 | tetrahedral edge-turning |
| $(R_6, \nu = 4,4,2)$ | 6 cube-face rays | mixed | $D_4$, order 8 | **3x3x2 Domino** |

Same ray-set all three times; three different turning systems. And note the third row: mixed $\nu$ within one ray-set is legal as long as equivariance holds — $\nu$ must be constant on $G$-orbits, and once two axes are restricted to 180°, the orbit structure changes to permit exactly this. That's the Domino, and it falls out of the definition rather than needing a special case.

A useful sanity check on condition (2): you cannot restrict just *one* of the three cube-face axis-pairs to 180° and leave the other two at 90°, because the 90° turns would map that axis onto the others, violating equivariance. The definition correctly predicts which bandagings-by-restriction are geometrically coherent.

## How the two notions sit together

- **Ray-set** answers *"where can material be cut?"* — it's the pure geometry, and it's what your 16 counts.
- **Turning system** answers *"what group do the legal moves generate?"* — strictly finer, and it's the right object if you care about the puzzle's state space rather than its shell.

One consequence worth flagging before we get to the enumeration: **the count of turning systems is infinite even where the count of ray-sets is finite.** For a fixed $R$, each ray can carry any $\nu(r)$ dividing its stabilizer order, so you get finitely many per ray-set — but the $C_n/D_n$ families let $n$ run unbounded, so the total is infinite in the same parameterized way. The 16 is a statement about ray-sets from $T/O/I$ specifically, and that finiteness is exactly what makes it provable.