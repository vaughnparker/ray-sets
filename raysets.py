"""Generate the 21 candidate ray-sets.

A ray-set is a bundle of unit rays from the origin: the axis system of a twisty
puzzle.  Each of the three symmetry shapes (T, O, I) has three pole families, and
a ray-set is any non-empty union of whole families.  3 shapes x (2**3 - 1)
combinations = 21 candidates.  (These collapse to 16 once mirror images are
merged; that de-duplication is deliberately not done here.)
"""
from collections import namedtuple, Counter
from itertools import combinations
import numpy as np

PHI = (1 + 5 ** 0.5) / 2                      # golden ratio, for the icosahedron
TOL = 1e-6

RaySet = namedtuple("RaySet", "shape labels families")


def rot(axis, angle):
    """Matrix that spins a ray by `angle` radians about `axis`."""
    x, y, z = np.array(axis, float) / np.linalg.norm(axis)
    c, s, C = np.cos(angle), np.sin(angle), 1 - np.cos(angle)
    return np.array([
        [x*x*C + c,   x*y*C - z*s, x*z*C + y*s],
        [y*x*C + z*s, y*y*C + c,   y*z*C - x*s],
        [z*x*C - y*s, z*y*C + x*s, z*z*C + c  ]])


def close(gens):
    """Every rotation reachable by multiplying the generators together."""
    G = [np.eye(3)]
    seen = lambda M: any(np.allclose(M, H, atol=TOL) for H in G)
    changed = True
    while changed:
        changed = False
        for A in list(G):
            for B in gens:
                M = A @ B
                if not seen(M):
                    G.append(M); changed = True
    return G


def families(G):
    """The pole families of a group: rays bucketed into orbits under G."""
    poles = []
    for M in G:
        if np.allclose(M, np.eye(3), atol=TOL):
            continue
        w, v = np.linalg.eig(M)                       # axis = eigenvector, value 1
        a = np.real(v[:, np.argmin(np.abs(w - 1))])
        a = a / np.linalg.norm(a)
        for p in (a, -a):                             # a ray points each way
            if not any(np.allclose(p, q, atol=TOL) for q in poles):
                poles.append(p)

    fams, placed = [], []
    for p in poles:
        if any(np.allclose(p, q, atol=TOL) for q in placed):
            continue
        orbit = []
        for M in G:
            q = M @ p
            if not any(np.allclose(q, r, atol=TOL) for r in orbit):
                orbit.append(q)
        fams.append(np.array(orbit)); placed += orbit
    return sorted(fams, key=len)


def _labels(sizes):
    """Name each family by its size, with a/b suffixes when sizes tie."""
    counts, used, out = Counter(sizes), {}, []
    for s in sizes:
        if counts[s] > 1:
            out.append(f"{s}{chr(ord('a') + used.get(s, 0))}")
            used[s] = used.get(s, 0) + 1
        else:
            out.append(str(s))
    return out


def build():
    """All 21 ray-sets, in shape order T, O, I."""
    groups = {
        "T": close([rot([1, 0, 0], np.pi),      rot([1, 1, 1], 2*np.pi/3)]),
        "O": close([rot([0, 0, 1], np.pi/2),    rot([1, 1, 1], 2*np.pi/3)]),
        "I": close([rot([0, 1, PHI], 2*np.pi/5), rot([0, -1, PHI], 2*np.pi/5)]),
    }
    sets = []
    for shape, G in groups.items():
        fams = families(G)
        labels = _labels([len(f) for f in fams])
        for k in (1, 2, 3):
            for combo in combinations(range(len(fams)), k):
                sets.append(RaySet(shape,
                                   [labels[i] for i in combo],
                                   [fams[i] for i in combo]))
    return sets


def cyclic(n):
    """The turntable ray-set C_n: one n-fold axis, so just two poles.

    The geometry is the same for every n — that infinitude lives in the turn
    order, which a ray-set forgets.  Compare `dihedral`.
    """
    G = close([rot([0, 0, 1], 2 * np.pi / n)])
    fams = families(G)
    return RaySet(f"C{n}", _labels([len(f) for f in fams]), fams)


def dihedral(n):
    """The prism ray-set D_n: an n-fold axis plus n perpendicular 2-fold axes.

    Families come out as sizes 2, n, n — so the geometry really does grow with
    n, and this family is genuinely infinite.
    """
    G = close([rot([0, 0, 1], 2 * np.pi / n), rot([1, 0, 0], np.pi)])
    fams = families(G)
    return RaySet(f"D{n}", _labels([len(f) for f in fams]), fams)


def label(rs):
    return f"{rs.shape} · " + "+".join(rs.labels)


def count(rs):
    return sum(len(f) for f in rs.families)


def rays(rs):
    """All of a ray-set's rays, as one array."""
    return np.vstack(rs.families)


def fingerprint(R, decimals=6):
    """Sorted pairwise dot products — unchanged by rotation and by reflection.

    Two ray-sets that differ here are certainly different.  Matching, though, is
    only a hint: the signature is invariant, not injective, so a match has to be
    confirmed by `align`.
    """
    return tuple(np.round(np.sort((R @ R.T).ravel()), decimals))


def align(A, B):
    """An orthogonal map carrying ray-set A onto ray-set B, or None if none exists.

    Reflections count: a puzzle and its mirror image have the same axis geometry.
    Pick three independent rays of A, try every triple of B that has the same
    pairwise dots as a possible image, and keep the map only if it is orthogonal
    and lands every ray of A on a ray of B.
    """
    if len(A) != len(B):
        return None
    for idx in combinations(range(len(A)), 3):
        P = A[list(idx)].T
        if abs(np.linalg.det(P)) > 0.1:
            break
    else:
        return None
    a1, a2, a3 = A[list(idx)]
    d12, d13, d23 = a1 @ a2, a1 @ a3, a2 @ a3
    Pinv = np.linalg.inv(P)
    for i, b1 in enumerate(B):
        for j, b2 in enumerate(B):
            if abs(b1 @ b2 - d12) > TOL:
                continue
            for b3 in B:
                if abs(b1 @ b3 - d13) > TOL or abs(b2 @ b3 - d23) > TOL:
                    continue
                M = np.column_stack([b1, b2, b3]) @ Pinv
                if not np.allclose(M.T @ M, np.eye(3), atol=TOL):
                    continue
                if all(any(np.allclose(M @ a, b, atol=TOL) for b in B) for a in A):
                    return M
    return None


def collapse(sets):
    """De-duplicate the candidates: 21 ray-sets down to 16.

    Returns (kept, merged): `kept` is the list of surviving indices, `merged`
    maps each dropped index to (surviving index, the map that proves it).
    Every merge is backed by an explicit orthogonal map, so a coincidental
    fingerprint collision could not silently fuse two genuinely different sets.
    """
    R = [rays(s) for s in sets]
    fps = [fingerprint(r) for r in R]
    # Prefer O and I as the survivor, so a cross-shape duplicate keeps the more
    # familiar name (O · 6 is the 3x3x3; T · 6 is the same thing relabelled).
    prefer = {"O": 0, "I": 1, "T": 2}
    order = sorted(range(len(sets)), key=lambda i: prefer.get(sets[i].shape, 3))
    kept, merged = [], {}
    for i in order:
        for r in kept:
            if fps[i] == fps[r]:
                M = align(R[i], R[r])
                if M is not None:
                    merged[i] = (r, M)
                    break
        else:
            kept.append(i)
    return sorted(kept), merged


if __name__ == "__main__":
    sets = build()
    print(f"{len(sets)} candidate ray-sets\n")
    for rs in sets:
        print(f"  {label(rs):16} {count(rs):>3} rays")

    kept, merged = collapse(sets)
    print(f"\n{len(sets)} -> {len(kept)} distinct\n")
    print("  merged away (each confirmed by an explicit map):")
    for i, (r, M) in sorted(merged.items()):
        kind = "rotation" if np.linalg.det(M) > 0 else "reflection"
        print(f"    {label(sets[i]):14} = {label(sets[r]):14} via {kind}")
    print("\n  the distinct ray-sets:")
    for r in kept:
        print(f"    {label(sets[r]):14} {count(sets[r]):>3} rays")