"""Enumerate every turning system on the 16 polyhedral ray-sets.

A ray-set records only which directions you can turn.  A *turning system* adds
how far: a map nu assigning each ray a permitted turn order, which may be a
proper divisor of what the geometry allows.  Following `intro.md`, a pair
(R, nu) is a turning system when

  1. closure      -- spinning R about r by 2*pi/nu(r) maps R onto itself,
  2. equivariance -- nu is constant on the orbits of the generated group G,
  3. finiteness   -- G is finite.

Two turning systems are the same if some element of O(3) carries one onto the
other, matching turn orders.

Finiteness is automatic here: every generator permutes the finite set R and R
spans space, so G embeds in the permutations of R.  The real work is
equivariance, which is what rules out the assignments that look plausible but
tear themselves apart.

    python turning_systems.py
"""
import os
import sys
from itertools import combinations, product

import numpy as np

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, "1_ray_sets"))
import raysets                                                   # noqa: E402

TOL = 1e-6
MAX_ORDER = 5          # stabilisers in T/O/I have order 2, 3, 4 or 5


def preserves(M, R):
    """Does the map M send every ray of R onto some ray of R?"""
    return all(any(np.allclose(M @ a, b, atol=TOL) for b in R) for a in R)


def allowed_orders(r, R):
    """Turn orders for r that leave R intact -- the legal values of nu(r)."""
    return [k for k in range(2, MAX_ORDER + 1)
            if preserves(raysets.rot(r, 2 * np.pi / k), R)]


def index_of(v, R):
    for i, b in enumerate(R):
        if np.allclose(v, b, atol=TOL):
            return i
    raise ValueError("ray left the set")


def generated_group(R, nu):
    """Every rotation reachable from the permitted turns."""
    return raysets.close([raysets.rot(r, 2 * np.pi / n) for r, n in zip(R, nu)])


def is_equivariant(R, nu, G):
    """Turn order has to be constant on orbits of the generated group."""
    for M in G:
        for i, r in enumerate(R):
            if nu[index_of(M @ r, R)] != nu[i]:
                return False
    return True


def symmetries(R):
    """Every orthogonal map -- rotation or reflection -- carrying R onto itself."""
    for idx in combinations(range(len(R)), 3):
        P = R[list(idx)].T
        if abs(np.linalg.det(P)) > 0.1:
            break
    a1, a2, a3 = R[list(idx)]
    d12, d13, d23 = a1 @ a2, a1 @ a3, a2 @ a3
    Pinv = np.linalg.inv(P)

    found = []
    for b1 in R:
        for b2 in R:
            if abs(b1 @ b2 - d12) > TOL:
                continue
            for b3 in R:
                if abs(b1 @ b3 - d13) > TOL or abs(b2 @ b3 - d23) > TOL:
                    continue
                M = np.column_stack([b1, b2, b3]) @ Pinv
                if np.allclose(M.T @ M, np.eye(3), atol=TOL) and preserves(M, R):
                    found.append(M)
    return found


def relabel(R, nu, M):
    """The turn orders after moving the whole system by M."""
    out = [None] * len(R)
    for i, r in enumerate(R):
        out[index_of(M @ r, R)] = nu[i]
    return tuple(out)


def systems_on(rs):
    """Every turning system on one ray-set, up to symmetry of that ray-set."""
    R = raysets.rays(rs)
    choices = [allowed_orders(r, R) for r in R]

    valid = []
    for nu in product(*choices):
        G = generated_group(R, nu)
        if is_equivariant(R, nu, G):
            valid.append((nu, len(G)))

    if len(valid) <= 1:                       # nothing to deduplicate
        return valid

    syms = symmetries(R)
    seen, unique = set(), []
    for nu, order in valid:
        key = min(relabel(R, nu, M) for M in syms)
        if key not in seen:
            seen.add(key)
            unique.append((nu, order))
    return unique


def describe(rs, nu):
    """Turn orders reported family by family, e.g. '6-family: 4' ."""
    R, parts, at = raysets.rays(rs), [], 0
    for label, fam in zip(rs.labels, rs.families):
        vals = sorted({nu[at + i] for i in range(len(fam))})
        parts.append(f"{label}->{','.join(map(str, vals))}")
        at += len(fam)
    return "  ".join(parts)


def main():
    sets = raysets.build()
    kept, _ = raysets.collapse(sets)

    total = 0
    for i in kept:
        rs = sets[i]
        found = systems_on(rs)
        total += len(found)
        head = f"{raysets.label(rs)}  ({raysets.count(rs)} rays)"
        print(f"{head:<26} {len(found)} turning system(s)")
        for nu, order in found:
            print(f"      |G| = {order:>3}   {describe(rs, nu)}")
    print(f"\n16 ray-sets  ->  {total} turning systems")


if __name__ == "__main__":
    main()
