#!/usr/bin/env python3
"""regime_core.py - shared geometry + fast exact piece counter for twisty-axis
cut-regime computations.

Problem primitive
-----------------
Given a set of unit rays U (n x 3) and a per-ray cut depth vector d (length n),
count the *movable pieces* of the plane arrangement {x : x.u_i = d_i} inside the
open unit ball, grouped by *weight* = number of caps (x.u_i > d_i) containing
the piece.  A "piece" is a full-dimensional cell of the arrangement that meets
the open unit ball; weight 0 (the immovable core) is not counted.

This module provides:
  * group construction (T, O, I) and orbit / ray extraction,
  * ray-permutation representation of the rotation group, used to cache the
    per-cell feasibility QP across symmetry-equivalent cells (a huge speedup:
    up to |G| = 12/24/60x fewer QP solves),
  * exact_counts(): flood-fill cell enumeration with the symmetry-cached
    feasibility test.

The feasibility test itself is an exact margin QP:
    maximize m  s.t.  s_i (x.u_i - d_i) >= m,  ||x|| <= 1.
A sign vector is a real piece iff m* > tol.  This is exact and correctly
handles full-dimensionality, open-ball intersection and strictness in one
number, including the degenerate d->0 limit.
"""
import numpy as np
from collections import deque, Counter
from scipy.optimize import minimize

PHI = (1 + 5 ** 0.5) / 2

# ----------------------------------------------------------------------------
# Rotation groups (closed from generators).
# ----------------------------------------------------------------------------
def Rmat(a, ang):
    a = np.array(a, float); a /= np.linalg.norm(a)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * (K @ K)

def _mkey(M): return tuple(np.round(M, 5).ravel())

def close(gens, cap=400):
    allg = list(gens) + [g.T for g in gens]
    E = {_mkey(np.eye(3)): np.eye(3)}; fr = [np.eye(3)]
    while fr:
        nx = []
        for M in fr:
            for g in allg:
                P = g @ M; k = _mkey(P)
                if k not in E: E[k] = P; nx.append(P)
                if len(E) > cap: return list(E.values())
        fr = nx
    return list(E.values())

T_GROUP = close([Rmat([1, 1, 1], 2 * np.pi / 3), Rmat([0, 0, 1], np.pi)])
O_GROUP = close([Rmat([0, 0, 1], np.pi / 2), Rmat([1, 0, 0], np.pi / 2)])
I_GROUP = close([Rmat([0, 1, PHI], 2 * np.pi / 5), Rmat([0, -1, PHI], 2 * np.pi / 5)])

def axis_of(R):
    ang = np.arccos(np.clip((np.trace(R) - 1) / 2, -1, 1))
    if ang < 1e-6: return None
    if abs(ang - np.pi) < 1e-4:
        M = (R + np.eye(3)) / 2
        i = int(np.argmax(np.linalg.norm(M, axis=0))); v = M[:, i]
    else:
        v = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]])
    return v / np.linalg.norm(v)

def _vkey(v): return tuple(np.round(v, 4))

def _canon_vec(v):
    for c in v:
        if abs(c) > 1e-6: return v if c > 0 else -v
    return v

def orbits(G):
    """Return the list of ray-orbits (each an (m x 3) array), sorted by size."""
    lines = {}
    for R in G:
        v = axis_of(R)
        if v is None: continue
        cv = _canon_vec(v); lines[_vkey(cv)] = cv
    rays = []
    for cv in lines.values(): rays += [cv, -cv]
    orbs, seen = [], set()
    for u in rays:
        if _vkey(u) in seen: continue
        orb = {}
        for R in G:
            w = R @ u; orb[_vkey(w)] = w
        seen |= set(orb.keys())
        orbs.append(np.array(list(orb.values())))
    return sorted(orbs, key=len)

def pick(G, n):
    for o in orbits(G):
        if len(o) == n: return o
    raise ValueError(f"no orbit of size {n}")

# ----------------------------------------------------------------------------
# Group action as ray permutations (for symmetry caching of the feasibility QP)
# ----------------------------------------------------------------------------
def ray_permutations(U, G):
    """For a ray set U (n x 3) invariant under G, return an array P of shape
    (|G|, n) with P[g][i] = index j such that  g . U[i] == U[j].
    Rows of U must be a union of full G-orbits (true for our axis systems)."""
    n = len(U)
    index = {_vkey(U[i]): i for i in range(n)}
    perms = []
    for R in G:
        pg = np.empty(n, dtype=np.int64)
        W = U @ R.T                      # rows: R . U[i]
        ok = True
        for i in range(n):
            j = index.get(_vkey(W[i]))
            if j is None:
                ok = False; break
            pg[i] = j
        if ok:
            perms.append(pg)
    P = np.array(perms, dtype=np.int64)
    # keep only distinct permutations (numerically-duplicate group elements)
    P = np.unique(P, axis=0)
    return P

# ----------------------------------------------------------------------------
# Feasibility: exact margin QP (max-min over the ball).  m* > tol  <=>  real.
# ----------------------------------------------------------------------------
def cell_margin(U, dvec, Sbool):
    """max over ||x||<=1 of  min_i s_i (x.u_i - d_i),  with s_i = +/-1 per S."""
    n = len(U)
    s = np.where(Sbool, 1.0, -1.0)
    A = s[:, None] * U
    rhs = s * dvec
    cons = []
    for i in range(n):
        Ai = A[i]; ri = rhs[i]
        cons.append({'type': 'ineq',
                     'fun': (lambda z, Ai=Ai, ri=ri: Ai @ z[:3] - ri - z[3]),
                     'jac': (lambda z, Ai=Ai: np.array([Ai[0], Ai[1], Ai[2], -1.0]))})
    cons.append({'type': 'ineq',
                 'fun': lambda z: 1.0 - z[:3] @ z[:3],
                 'jac': lambda z: np.array([-2 * z[0], -2 * z[1], -2 * z[2], 0.0])})
    r = minimize(lambda z: -z[3], np.array([0, 0, 0, -1.0]),
                 jac=lambda z: np.array([0, 0, 0, -1.0]),
                 constraints=cons, method='SLSQP',
                 options={'ftol': 1e-10, 'maxiter': 200})
    return -r.fun

# ----------------------------------------------------------------------------
# Fast exact counts with symmetry caching of the feasibility test.
# ----------------------------------------------------------------------------
def exact_counts(U, dvec, perms=None, tol=1e-6, seeds=60, rng_seed=1,
                 return_masks=False):
    """Histogram {weight: count} of movable pieces at per-ray depths dvec.

    perms : (|G| x n) ray-permutation array.  If given, the feasibility QP is
            solved once per *symmetry orbit* of sign vectors: on the first QP
            for a cell we pre-fill the feasibility result for the whole group
            orbit (all |G| images), so no symmetric cell is ever re-solved.
    Flood-fill BFS over sign vectors (Python-int bitmasks); a cell is expanded
    across its facet-neighbours only if it is a real piece.  Per-mask work is
    just a dict lookup + int.bit_count() + neighbour XORs; bits are unpacked
    only when an actual QP is required (rare).
    """
    U = np.asarray(U, float)
    dvec = np.asarray(dvec, float)
    n = len(U)
    bitw = [1 << i for i in range(n)]

    use_sym = perms is not None and len(perms) > 1
    if use_sym:
        Pinv = np.argsort(perms, axis=1)           # bits'[j] = bits[Pinv[g][j]]
        pow2 = np.array([1 << i for i in range(n)], dtype=object)

        def orbit_keys(mask):
            bits = np.array([(mask >> i) & 1 for i in range(n)], dtype=object)
            imgs = bits[Pinv]                       # (|G|, n)
            return set(int(k) for k in (imgs @ pow2))

    known = {}          # mask -> feasible(bool)   (orbit-prefilled when use_sym)

    def feasible(mask):
        v = known.get(mask)
        if v is not None:
            return v
        Sbool = np.array([(mask >> i) & 1 for i in range(n)], dtype=bool)
        v = cell_margin(U, dvec, Sbool) > tol
        if use_sym:
            for k in orbit_keys(mask):
                known[k] = v
        else:
            known[mask] = v
        return v

    def mask_of_point(x):
        b = (U @ x) > dvec
        m = 0
        for i in range(n):
            if b[i]: m |= bitw[i]
        return m

    seen = set(); q = deque(); pieces = Counter()
    masks = [] if return_masks else None
    rng = np.random.default_rng(rng_seed)
    start_pts = [np.zeros(3)]
    for _ in range(seeds):
        g = rng.standard_normal(3); g /= np.linalg.norm(g)
        start_pts.append(g * (rng.random() ** (1 / 3)))
    for x in start_pts:
        m = mask_of_point(x)
        if m not in seen:
            seen.add(m); q.append(m)

    while q:
        mask = q.popleft()
        if not feasible(mask):
            continue
        w = mask.bit_count()
        if w > 0:
            pieces[w] += 1
            if return_masks: masks.append(mask)
        for b in bitw:
            nb = mask ^ b
            if nb not in seen:
                seen.add(nb); q.append(nb)

    hist = dict(sorted(pieces.items()))
    return (hist, masks) if return_masks else hist


# ----------------------------------------------------------------------------
# Exact degenerate (d -> 0) configuration.
# ----------------------------------------------------------------------------
# At exactly d=0 every cut plane passes through the origin, and antipodal rays
# share the SAME plane.  Single-bit-flip flood-fill then cannot traverse
# between cones (flipping one bit of an antipodal pair gives an infeasible
# "both-off" signature), so cones become isolated and a seeded flood-fill under-
# counts.  We instead enumerate the full-dim cones of the arrangement of the
# DISTINCT planes (antipodal normals merged), which IS single-flip connected,
# then map each cone back to its weight in the original ray system.
def distinct_planes(U):
    """Return (Pn, mapping): distinct plane normals and, per original ray,
    a (plane_index, sign) pair with  U[i] == sign * Pn[plane_index]."""
    U = np.asarray(U, float)
    reps = []; mapping = []
    for u in U:
        f = None
        for pi, pn in enumerate(reps):
            if np.linalg.norm(u - pn) < 1e-6: f = (pi, 1); break
            if np.linalg.norm(u + pn) < 1e-6: f = (pi, -1); break
        if f is None:
            reps.append(np.array(u, float)); f = (len(reps) - 1, 1)
        mapping.append(f)
    return np.array(reps), mapping


def degenerate_counts(U, G=None, seeds=400, tol=1e-6):
    """Exact {weight: count} at d=0 (the deep-cut-through-center limit)."""
    U = np.asarray(U, float)
    Pn, mapping = distinct_planes(U)
    m = len(Pn)
    dvec = np.zeros(m)
    bitw = [1 << i for i in range(m)]
    perms = ray_permutations(Pn, G) if G is not None else None
    use_sym = perms is not None and len(perms) > 1
    if use_sym:
        Pinv = np.argsort(perms, axis=1)
        pow2 = np.array([1 << i for i in range(m)], dtype=object)
        def orbit_keys(mask):
            bits = np.array([(mask >> i) & 1 for i in range(m)], dtype=object)
            return set(int(k) for k in (bits[Pinv] @ pow2))
    known = {}
    def feasible(mask):
        v = known.get(mask)
        if v is not None: return v
        Sbool = np.array([(mask >> i) & 1 for i in range(m)], dtype=bool)
        v = cell_margin(Pn, dvec, Sbool) > tol
        if use_sym:
            for k in orbit_keys(mask): known[k] = v
        else:
            known[mask] = v
        return v

    # enumerate ALL full-dim cones (any weight over the distinct planes)
    seen = set(); q = deque(); cones = []
    rng = np.random.default_rng(1)
    for _ in range(seeds):
        g = rng.standard_normal(3); g /= np.linalg.norm(g)
        b = (Pn @ g) > 0
        mask = 0
        for i in range(m):
            if b[i]: mask |= bitw[i]
        if mask not in seen: seen.add(mask); q.append(mask)
    while q:
        mask = q.popleft()
        if not feasible(mask): continue
        cones.append(mask)
        for bb in bitw:
            nb = mask ^ bb
            if nb not in seen: seen.add(nb); q.append(nb)

    # map each cone to its weight in the original ray system
    pieces = Counter()
    for mask in cones:
        w = 0
        for (pi, sgn) in mapping:
            bit = (mask >> pi) & 1
            w += bit if sgn > 0 else (1 - bit)
        if w > 0:
            pieces[w] += 1
    return dict(sorted(pieces.items()))


# ----------------------------------------------------------------------------
# The seven elementary systems (name, ray-orbit).
# ----------------------------------------------------------------------------
def elementary_systems():
    return [
        ("Tetrahedron - corners (Pyraminx)", pick(T_GROUP, 4), T_GROUP),
        ("Cube - faces (Rubik's Cube)", pick(O_GROUP, 6), O_GROUP),
        ("Cube - corners (Skewb)", pick(O_GROUP, 8), O_GROUP),
        ("Cube - edges (Helicopter)", pick(O_GROUP, 12), O_GROUP),
        ("Dodecahedron - faces (Megaminx)", pick(I_GROUP, 12), I_GROUP),
        ("Dodecahedron - corners (Radiolarian)", pick(I_GROUP, 20), I_GROUP),
        ("Dodecahedron - edges", pick(I_GROUP, 30), I_GROUP),
    ]


if __name__ == "__main__":
    # quick smoke test of geometry + orbit sizes
    for G, nm in [(T_GROUP, "T"), (O_GROUP, "O"), (I_GROUP, "I")]:
        print(nm, "|G| =", len(G), " orbit sizes:", [len(o) for o in orbits(G)])
