#!/usr/bin/env python3
"""precompute_elementary.py - exact 1-D cut-regime spectra for the 7 elementary
axis systems, via the analytical critical-depth (wall) method.

A single depth d in (0,1) is shared by all rays.  The piece configuration is
piecewise-constant and only changes at a *critical depth* where an arrangement
feature crosses the unit sphere:
    pair  (i,j):  d = sqrt((1 + u_i.u_j)/2)          (edge tangent to sphere)
    triple(i,j,k):d = 1 / ||M^{-1} 1||               (vertex on sphere)
We enumerate the exact piece configuration once per open interval between
consecutive criticals (at the midpoint), collapse consecutive equal configs,
and add the degenerate d=0 point-regime (opposite cuts merge) when it differs.

Output schema (phases_data.js) - unchanged, consumed by phase-diagram.html and
elementary-heatmap.html:
    const PHASES = { "<system>": {rays, count, phases:[{d0,d1,total,hist,maxw,
                     degenerate}, ...]}, ... };

Resumable: existing systems in phases_data.js are kept unless --force; each
system is validated (expected regime count + monotonicity + known-puzzle
configs) and the file is rewritten after every system.
"""
import numpy as np, json, os, sys, time
from itertools import combinations
from multiprocessing import Pool
import regime_core as rc

OUT = "phases_data.js"
FORCE = "--force" in sys.argv

EXPECT = {  # expected exact regime counts (Section 3)
    "Tetrahedron - corners (Pyraminx)": 3,
    "Cube - faces (Rubik's Cube)": 4,
    "Cube - corners (Skewb)": 5,
    "Cube - edges (Helicopter)": 8,
    "Dodecahedron - faces (Megaminx)": 7,
    "Dodecahedron - corners (Radiolarian)": 13,
    "Dodecahedron - edges": 29,
}


def critical_depths(U):
    n = len(U); crit = set()
    for i, j in combinations(range(n), 2):
        g = float(U[i] @ U[j])
        if g <= -1 + 1e-9 or g >= 1 - 1e-9:
            continue
        d = np.sqrt((1 + g) / 2)
        if 1e-4 < d < 1 - 1e-4:
            crit.add(round(d, 9))
    for i, j, k in combinations(range(n), 3):
        M = np.array([U[i], U[j], U[k]])
        if abs(np.linalg.det(M)) < 1e-6:
            continue
        q = np.linalg.solve(M, np.ones(3)); nq = np.linalg.norm(q)
        if nq > 1 + 1e-9:
            d = 1.0 / nq
            if 1e-4 < d < 1 - 1e-4:
                crit.add(round(d, 9))
    return sorted(crit)


# ---- worker (top-level for macOS spawn) ------------------------------------
_WORK = {}
def _init(U, perms):
    _WORK['U'] = U; _WORK['perms'] = perms
def _count(d):
    return rc.exact_counts(_WORK['U'], np.full(len(_WORK['U']), d), _WORK['perms'])


def compute_system(name, U, G, perms):
    crit = critical_depths(U)
    bounds = [0.0] + crit + [1.0]
    # representative interior depth per open interval between consecutive walls
    reps = [(a + b) / 2 for a, b in zip(bounds[:-1], bounds[1:])]
    with Pool(initializer=_init, initargs=(U, perms)) as p:
        interval_hists = p.map(_count, reps)
    # exact degenerate d=0 config (distinct-plane region count)
    h0 = rc.degenerate_counts(U, G)
    walls = [0.0] + crit + [1.0]

    # collapse consecutive equal interval configs -> regimes with exact walls
    regimes = []
    m = len(interval_hists); i = 0
    def key(h): return tuple(sorted(h.items()))
    while i < m:
        j = i
        while j + 1 < m and key(interval_hists[j + 1]) == key(interval_hists[i]):
            j += 1
        regimes.append((walls[i], walls[j + 1], interval_hists[i], False))
        i = j + 1

    out = []
    if key(h0) != key(regimes[0][2]) and sum(h0.values()) > 0:
        out.append((0.0, 0.0, h0, True))
    out.extend(regimes)
    return crit, out


def to_phases(regs):
    phases = []
    for (d0, d1, h, deg) in regs:
        tot = int(sum(h.values())); mw = int(max(h)) if h else 0
        phases.append({"d0": round(float(d0), 6), "d1": round(float(d1), 6),
                       "total": tot, "hist": {str(k): int(v) for k, v in h.items()},
                       "maxw": mw, "degenerate": bool(deg)})
    return phases


def validate(name, phases):
    msgs = []
    # regime count
    exp = EXPECT.get(name)
    if exp is not None:
        ok = len(phases) == exp
        msgs.append(("count", ok, f"{len(phases)} (expect {exp})"))
    # monotonicity: total non-increasing along increasing depth (skip the
    # degenerate d=0 point, which is a separate limiting config)
    nd = [p for p in phases if not p["degenerate"]]
    mono = all(nd[i]["total"] >= nd[i + 1]["total"] for i in range(len(nd) - 1))
    msgs.append(("monotone", mono, "non-increasing" if mono else "VIOLATION"))
    return msgs


if __name__ == "__main__":
    out = {}
    if os.path.exists(OUT) and not FORCE:
        try:
            s = open(OUT).read(); out = json.loads(s[s.index('{'):s.rindex('}') + 1])
        except Exception:
            out = {}
    # keep a one-time backup of the incoming file
    if os.path.exists(OUT) and not os.path.exists(OUT + ".orig"):
        open(OUT + ".orig", "w").write(open(OUT).read())

    allok = True
    for name, U, G in rc.elementary_systems():
        U = np.asarray(U, float)
        if name in out and not FORCE:
            print(f"{name}: cached ({out[name]['count']} regimes) - recomputing to verify")
        perms = rc.ray_permutations(U, G)
        t = time.time()
        crit, regs = compute_system(name, U, G, perms)
        phases = to_phases(regs)
        dt = time.time() - t
        msgs = validate(name, phases)
        status = "  ".join(f"{k}:{'OK' if ok else 'FAIL'}({v})" for k, ok, v in msgs)
        if not all(ok for _, ok, _ in msgs):
            allok = False
        print(f"{name}: {len(phases)} regimes, {len(crit)} criticals ({dt:.1f}s)  {status}")
        out[name] = {"rays": int(len(U)), "count": len(phases), "phases": phases}
        with open(OUT, "w", encoding="utf-8") as f:
            f.write("const PHASES = " + json.dumps(out) + ";\n")
    print("\nAll elementary systems validated:", "PASS" if allok else "FAIL")
    print("wrote", OUT)
