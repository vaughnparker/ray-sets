#!/usr/bin/env python3
"""precompute_compound.py - grid-sampled cut-regime maps for the 9 compound
axis systems.

A compound system is 2 or 3 elementary orbits combined, and each orbit carries
its OWN cut depth - so the parameter space is a 2-D square (two orbits) or a 3-D
cube (three orbits) rather than the interval (0,1) of precompute_elementary.py.

This file uses a GRID: it samples the depth square/cube on an N-per-axis grid,
counts pieces exactly at each sample (regime_core), and groups equal configs
into regimes.  The regime COUNT is therefore a LOWER BOUND - a thin regime
between grid lines can be missed - and only interior points are sampled (the
degenerate d=0 boundaries are not).

Why not the exact analytical-wall method (as in precompute_elementary.py)?  We
tried it and it is genuinely harder here, for two reasons found by validation:

  1. An extra class of walls.  In 1-D all planes share one depth, so scaling d
     just scales the plane arrangement uniformly - its combinatorial type never
     changes and only *sphere* events matter (pair edge tangent, triple vertex
     on sphere).  With per-orbit depths the ratio dA/dB reshapes the arrangement
     itself, adding INTERIOR events: a vertex (3 planes) crossing a 4th plane.
     These "quadruple" walls are lines in depth space and must be included; an
     exact method with only pair+triple walls silently misses chambers.
  2. Cost.  Exact vertical decomposition creates O(walls^2) cells and needs a
     full piece count at each, which is slower than the grid for big systems and
     infeasible for the 50-/62-ray dodeca systems without an *incremental*
     counter (compute once, update by +/-1 across each wall).

So the exact compound method = {pair, triple, quadruple} walls + incremental
counting + chamber enumeration.  That is a real project; the grid is the honest
stand-in until it exists.

Output schema (compound_data.js), consumed by compound-gridsearch-heatmap.html:
    const COMPOUND = { "<system>": {
        rays:[nA,nB(,nC)], labels:[...], N, depths:[...], method:"grid",
        regimes:[{total,hist,maxw},...], count,
        grid: N x N (x N) array of regime ids } , ... };

Resumable: existing systems in compound_data.js are kept unless --force; the
file is rewritten after each system completes.
"""
import numpy as np, json, os, sys, time, itertools
import regime_core as rc
from jsonfmt import jdump

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "tutorial_8_compound_cut_depths", "compound_data.js")
FORCE = "--force" in sys.argv
ONLY_2D = "--dims=2" in sys.argv        # skip the two 3-orbit systems


def _argval(flag, default):
    for a in sys.argv[1:]:
        if a.startswith(flag + "="):
            return int(a.split("=", 1)[1])
    return default


# Grid resolution per axis (override with --n2=N / --n3=N).  Runtime is
# (samples) x (per-sample count), and the per-sample count is slow for the big
# dodeca systems (~tens of seconds at 50-62 rays), so a fine grid there is hours.
N2 = _argval("--n2", 7)        # 2-orbit systems  (N^2 samples)
N3 = _argval("--n3", 5)        # 3-orbit systems  (N^3 samples)

NAME = {"O": {6: "faces", 8: "corners", 12: "edges"},
        "I": {12: "faces", 20: "corners", 30: "edges"},
        "T": {4: "corners", 6: "edges"}}


def _orbit(fam, size):
    G = {"O": rc.O_GROUP, "T": rc.T_GROUP, "I": rc.I_GROUP}[fam]
    return f"{NAME[fam][size]} ({size})", np.asarray(rc.pick(G, size), float), G


def compound_systems():
    """(name, [(label, rays), ...], G); names/labels match systems_data.js."""
    def make(name, fam, sizes):
        orbs = [_orbit(fam, s) for s in sizes]
        return name, [(lab, rays) for lab, rays, _ in orbs], orbs[0][2]
    return [
        make("Tetrahedron - corners + edges", "T", [4, 6]),
        make("Cube - faces + corners", "O", [6, 8]),
        make("Cube - faces + edges", "O", [6, 12]),
        make("Cube - corners + edges", "O", [8, 12]),
        make("Cube - faces + corners + edges", "O", [6, 8, 12]),
        make("Dodeca - faces + corners", "I", [12, 20]),
        make("Dodeca - faces + edges", "I", [12, 30]),
        make("Dodeca - corners + edges", "I", [20, 30]),
        make("Dodeca - faces + corners + edges", "I", [12, 20, 30]),
    ]


def compute_system(name, orbits, G, N):
    labels = [lab for lab, _ in orbits]
    orbs = [rays for _, rays in orbits]
    U = np.vstack(orbs)
    orb_of = np.array([k for k, o in enumerate(orbs) for _ in range(len(o))])
    perms = rc.ray_permutations(U, G)
    depths = [(i + 0.5) / N for i in range(N)]     # interior grid samples

    reg_id, regimes = {}, []
    grid = np.empty((N,) * len(orbs), dtype=int)
    for idx in itertools.product(range(N), repeat=len(orbs)):
        dvec = np.array([depths[idx[orb_of[i]]] for i in range(len(U))])
        h = rc.exact_counts(U, dvec, perms)
        key = tuple(sorted(h.items()))
        if key not in reg_id:
            reg_id[key] = len(regimes)
            regimes.append({"total": int(sum(h.values())),
                            "hist": {str(k): int(v) for k, v in h.items()},
                            "maxw": int(max(h)) if h else 0})
        grid[idx] = reg_id[key]

    return {"rays": [len(o) for o in orbs], "labels": labels, "N": N,
            "depths": [round(d, 6) for d in depths], "method": "grid",
            "regimes": regimes, "count": len(regimes), "grid": grid.tolist()}


if __name__ == "__main__":
    out = {}
    if os.path.exists(OUT) and not FORCE:
        try:
            s = open(OUT).read(); out = json.loads(s[s.index('{'):s.rindex('}') + 1])
        except Exception:
            out = {}

    for name, orbits, G in compound_systems():
        if ONLY_2D and len(orbits) == 3:
            continue
        if name in out and not FORCE:
            print(f"{name}: cached ({out[name]['count']} regimes) - skipping")
            continue
        N = N3 if len(orbits) == 3 else N2
        t = time.time()
        rec = compute_system(name, orbits, G, N)
        print(f"{name}: {rec['count']} regimes  rays={rec['rays']}  N={N}  "
              f"(lower bound, {time.time() - t:.1f}s)")
        out[name] = rec
        with open(OUT, "w", encoding="utf-8") as f:
            f.write("const COMPOUND = " + jdump(out) + ";\n")
    print("wrote", OUT)
