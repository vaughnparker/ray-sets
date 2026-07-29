#!/usr/bin/env python3
"""exact_compound_poc.py - PROTOTYPE: exact cut-regime enumeration for the smallest
2-orbit compound systems, via the analytical {pair, triple, quadruple} walls.

Goal: validate that pair+triple+quadruple is the *complete* wall set, by comparing the
configs this finds against the grid (compound_data.js). The exact set must CONTAIN every
config the grid found, and should find MORE (thin chambers the grid misses).

Method (per system, depths dA for orbit 0 and dB for orbit 1):
  - walls are curves F(dA,dB)=0 in the depth square:
      pair (i,j):   di^2 + dj^2 - 2 di dj (ui.uj) - (1 - (ui.uj)^2) = 0   (edge tangent)
      triple(i,j,k):|M^{-1} d|^2 - 1 = 0                                  (vertex on sphere)
      quad (i,j,k,l): det([U4 | d4]) = 0                                  (4 planes concurrent)
    each is degree <= 2 in dB, so at a fixed dA we recover its dB roots exactly.
  - dense sweep in dA; at each dA slice collect all wall dB-roots -> exact dB chambers;
    sample each chamber midpoint and count pieces exactly (regime_core.exact_counts).
  - the set of configs found = the regimes.

This is a proof of concept, not the production method: it is dense (not exact) in the dA
direction, so completeness rests on the sweep being fine enough (checked by refining).
"""
import numpy as np, json, os, sys, time, itertools
import regime_core as rc
from precompute_compound import compound_systems

TOL = 1e-9
SMALLEST = {"Tetrahedron - corners + edges", "Cube - faces + corners"}

# set per system
U = None; ORB = None


def build_walls(U, orb):
    """Candidate walls as lightweight descriptors; F(dA,dB) via wallF below."""
    n = len(U); walls = []
    for i, j in itertools.combinations(range(n), 2):
        g = float(U[i] @ U[j])
        if abs(abs(g) - 1) < 1e-9:
            continue
        walls.append(("P", (i, j), g, None))
    for i, j, k in itertools.combinations(range(n), 3):
        M = U[[i, j, k]]
        if abs(np.linalg.det(M)) < 1e-6:
            continue
        walls.append(("T", (i, j, k), None, np.linalg.inv(M)))
    for quad in itertools.combinations(range(n), 4):
        walls.append(("Q", quad, None, None))
    return walls


def wallF(w, dA, dB):
    d = (dA, dB); t, idx, g, M = w
    if t == "P":
        i, j = idx; di, dj = d[ORB[i]], d[ORB[j]]
        return di*di + dj*dj - 2*di*dj*g - (1 - g*g)
    if t == "T":
        dv = np.array([d[ORB[i]] for i in idx]); q = M @ dv
        return float(q @ q - 1)
    # Q: det of [U4 | d4]
    dv = np.array([d[ORB[i]] for i in idx])
    return float(np.linalg.det(np.column_stack([U[list(idx)], dv])))


def dB_roots(w, dA):
    """Roots in (0,1) of F(dA, .) — a degree<=2 poly in dB, from a 3-point fit."""
    f0 = wallF(w, dA, 0.0); fh = wallF(w, dA, 0.5); f1 = wallF(w, dA, 1.0)
    A = 2*f1 + 2*f0 - 4*fh; B = (f1 - f0) - A; C = f0
    out = []
    if abs(A) < 1e-12:
        if abs(B) > 1e-12:
            out = [-C / B]
    else:
        disc = B*B - 4*A*C
        if disc >= 0:
            s = disc**0.5; out = [(-B + s)/(2*A), (-B - s)/(2*A)]
    return [r for r in out if 1e-7 < r < 1 - 1e-7]


def vertical_dAs(walls):
    """dA of walls that don't depend on dB (orbit-0-only) — vertical lines."""
    xs = []
    for w in walls:
        if abs(wallF(w, 0.37, 0.19) - wallF(w, 0.37, 0.81)) < 1e-12:   # dB-independent
            f0 = wallF(w, 0.0, 0.5); fh = wallF(w, 0.5, 0.5); f1 = wallF(w, 1.0, 0.5)
            A = 2*f1 + 2*f0 - 4*fh; Bc = (f1 - f0) - A; C = f0
            if abs(A) < 1e-12:
                if abs(Bc) > 1e-12: xs.append(-C/Bc)
            else:
                disc = Bc*Bc - 4*A*C
                if disc >= 0:
                    s = disc**0.5
                    xs += [(-Bc+s)/(2*A), (-Bc-s)/(2*A)]
    return sorted(x for x in xs if 1e-6 < x < 1 - 1e-6)


def canon(h):
    return tuple(sorted((int(k), int(v)) for k, v in h.items()))


def enumerate_exact(U_, orb, G, K=240):
    global U, ORB
    U, ORB = U_, orb
    perms = rc.ray_permutations(U, G)
    walls = build_walls(U, orb)
    # dA sample columns: dense linspace + straddles of vertical walls
    xs = set(np.linspace(0.0, 1.0, K + 2)[1:-1])
    for v in vertical_dAs(walls):
        xs.add(v - 1e-4); xs.add(v + 1e-4)
    configs = {}                              # canon-config -> a representative (dA,dB)
    columns = []                              # per dA-column, the exact dB cells (for the viewer)
    for dA in sorted(x for x in xs if 0 < x < 1):
        bps = {0.0, 1.0}
        for w in walls:
            for r in dB_roots(w, dA):
                bps.add(r)
        bps = sorted(bps)
        cells = []
        for lo, hi in zip(bps[:-1], bps[1:]):
            dB = (lo + hi) / 2
            dvec = np.array([dA if o == 0 else dB for o in orb])
            h = rc.exact_counts(U, dvec, perms)
            configs.setdefault(canon(h), (round(dA, 4), round(dB, 4)))
            cells.append([round(lo, 5), round(hi, 5), int(sum(h.values())), int(max(h)) if h else 0])
        columns.append([round(dA, 5), cells])
    return configs, len(walls), columns


def grid_configs(name):
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "tutorial_8_compound_cut_depths", "compound_data.js")
    s = open(p, encoding="utf-8").read(); D = json.loads(s[s.index('{'):s.rindex('}') + 1])
    return {canon(r["hist"]) for r in D[name]["regimes"]}


OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "tutorial_8_compound_cut_depths", "exact_compound_data.js")

if __name__ == "__main__":
    filt = sys.argv[1] if len(sys.argv) > 1 else None
    K = int(sys.argv[2]) if len(sys.argv) > 2 else 240
    data = {}
    if os.path.exists(OUT):                    # keep other systems already computed
        try:
            s = open(OUT, encoding="utf-8").read(); data = json.loads(s[s.index('{'):s.rindex('}') + 1])
        except Exception:
            data = {}
    for name, orbits, G in compound_systems():
        if name not in SMALLEST:
            continue
        if filt and filt.lower() not in name.lower():
            continue
        orbs = [rays for _, rays in orbits]
        U_ = np.vstack(orbs)
        orb = np.array([k for k, o in enumerate(orbs) for _ in range(len(o))])
        t = time.time()
        exact, nwalls, columns = enumerate_exact(U_, orb, G, K=K)
        dt = time.time() - t
        grid = grid_configs(name)
        missing = grid - set(exact)            # grid configs the exact method failed to find
        extra = set(exact) - grid              # thin regimes the grid missed
        print(f"\n=== {name}  rays={[len(o) for o in orbs]}  ({nwalls} candidate walls) ===")
        print(f"  exact: {len(exact)} configs   grid: {len(grid)} configs   ({dt:.1f}s)")
        print(f"  grid configs found by exact: {len(grid & set(exact))}/{len(grid)}"
              f"   {'OK (superset)' if not missing else 'MISSING ' + str(len(missing))}")
        print(f"  extra configs exact found (grid missed): {len(extra)}")
        data[name] = {"labels": [lab for lab, _ in orbits], "rays": [len(o) for o in orbs],
                      "exact_count": len(exact), "grid_count": len(grid), "columns": columns}
        with open(OUT, "w", encoding="utf-8") as f:
            f.write("const EXACT_COMPOUND = " + json.dumps(data) + ";\n")
    print("wrote", OUT)
