#!/usr/bin/env python3
"""dump_all_surface.py - exact external (surface) + total (all-cell) regime data
for ALL 7 elementary ray-sets, on the SPHERE body, written to surface_data.js as
a multi-system object.  Method (per system): critical-depth walls; per interval
midpoint and per wall (+center) compute the external histogram (pieces reaching
the sphere: bounded cell with a vertex at radius>=1, or unbounded cell) and the
total histogram (all movable cells); both orbit-closed for symmetry-valid counts.
Regime names come from puzzle_names.json (matched by surface histogram, per
system); currently only the 20-ray face-turning icosahedron is named there.
"""
import os, sys, json, time
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE)); sys.path.insert(0, _HERE)
import numpy as np
from itertools import combinations
from scipy.optimize import linprog
import regime_core as rc
from precompute_elementary import critical_depths
from jsonfmt import jdump

# ---- Puzzle names for regimes (from puzzle_names.json) ----
# A named regime is identified by its surface (external) histogram, per system.
# To name regimes of other systems, add them to puzzle_names.json - no code change.
def _load_names():
    try:
        data = json.load(open(os.path.join(_HERE, "puzzle_names.json"), encoding="utf-8"))
    except FileNotFoundError:
        return {}
    return {sysname: {frozenset((int(k), int(v)) for k, v in e["ext_hist"].items()):
                      (e.get("id"), e["name"]) for e in named}
            for sysname, named in data.items()}

NAMES = _load_names()

def name_for(namemap, hist):
    if not namemap:
        return (None, None)
    return namemap.get(frozenset((int(a), int(b)) for a, b in hist.items()), (None, None))

def orbit_closure(masks, perms, n):
    P = perms.astype(int); out = set()
    for m in masks:
        bits = [i for i in range(n) if (m >> i) & 1]
        for g in range(len(P)):
            nm = 0; pg = P[g]
            for i in bits: nm |= (1 << int(pg[i]))
            out.add(nm)
    return out

def build_verts(U):
    n = len(U); V = []
    for i, j, k in combinations(range(n), 3):
        M = np.array([U[i], U[j], U[k]])
        if abs(np.linalg.det(M)) < 1e-9: continue
        q = np.linalg.solve(M, np.ones(3)); V.append((i, j, k, q, np.linalg.norm(q)))
    return V

def unbounded(U, mask, d):
    n = len(U)
    s = np.array([1.0 if (mask >> l) & 1 else -1.0 for l in range(n)])
    A = -(s[:, None] * U)
    for e in np.eye(3).tolist() + (-np.eye(3)).tolist():
        r = linprog(-np.array(e), A_ub=A, b_ub=np.zeros(n), bounds=[(-1, 1)] * 3, method='highs')
        if r.success and -r.fun > 1e-7: return True
    return False

def surface_hist(U, perms, verts, d, realset):
    n = len(U); surf = set()
    for (i, j, k, q, nq) in verts:
        if d * nq < 1.0: continue
        V = d * q; base = 0
        for l in range(n):
            if l in (i, j, k): continue
            if U[l] @ V > d: base |= (1 << l)
        for a in (0, 1):
            for b in (0, 1):
                for c in (0, 1):
                    mm = base | (a << i) | (b << j) | (c << k)
                    if mm in realset: surf.add(mm)
    for m in realset:
        if m not in surf and unbounded(U, m, d): surf.add(m)
    surf = orbit_closure(surf, perms, n)
    h = {}
    for m in surf:
        w = bin(m).count('1')
        if w > 0: h[w] = h.get(w, 0) + 1
    return dict(sorted(h.items()))

def all_hist(realset, perms, n):
    masks = orbit_closure(realset, perms, n)
    h = {}
    for m in masks:
        w = bin(m).count('1')
        if w > 0: h[w] = h.get(w, 0) + 1
    return dict(sorted(h.items()))

def hjs(h): return {str(k): int(v) for k, v in h.items()}

def compute_system(name, U, G):
    U = np.asarray(U, float); n = len(U)
    namemap = NAMES.get(name)
    perms = rc.ray_permutations(U, G); verts = build_verts(U)
    crit = critical_depths(U); bounds = [0.0] + crit + [1.0]

    def hists(d):   # one flood-fill per depth, shared by both histograms
        _, masks = rc.exact_counts(U, np.full(n, d), perms, return_masks=True, seeds=300)
        realset = set(masks)
        return surface_hist(U, perms, verts, d, realset), all_hist(realset, perms, n)

    entries = []
    for a, b in zip(bounds[:-1], bounds[1:]):
        m = (a + b) / 2
        he, ha = hists(m)
        num, nm = name_for(namemap, he)
        entries.append({"kind": "interval", "d_lo": round(a, 6), "d_hi": round(b, 6),
                        "d_rep": round(m, 6), "rad": num, "name": nm,
                        "ext_total": int(sum(he.values())), "ext_hist": hjs(he),
                        "all_total": int(sum(ha.values())), "all_hist": hjs(ha)})
    for w in crit:
        he, ha = hists(w)
        num, nm = name_for(namemap, he)
        entries.append({"kind": "wall", "d": round(w, 6), "rad": num, "name": nm,
                        "ext_total": int(sum(he.values())), "ext_hist": hjs(he),
                        "all_total": int(sum(ha.values())), "all_hist": hjs(ha)})
    hc = rc.degenerate_counts(U, G)
    num, nm = name_for(namemap, hc)
    entries.append({"kind": "wall", "d": 0.0, "rad": num, "name": nm,
                    "ext_total": int(sum(hc.values())), "ext_hist": hjs(hc),
                    "all_total": int(sum(hc.values())), "all_hist": hjs(hc)})
    maxw = max(int(k) for e in entries for k in
               list(e["ext_hist"].keys()) + list(e["all_hist"].keys()))
    return {"rays": n, "maxw": maxw, "is_radiolarian": (n == 20),
            "walls": [round(c, 6) for c in crit], "entries": entries}

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(_HERE), "tutorial_7_elementary_cut_depths", "surface_data.js")
    existing = {"order": [], "systems": {}}
    systems = {}; order = []
    for name, U, G in rc.elementary_systems():
        t = time.time()
        systems[name] = compute_system(name, U, G)
        order.append(name)
        with open(out, "w", encoding="utf-8") as f:   # write incrementally (resumable/crash-safe)
            f.write("const SURFACE_DATA = " + jdump({"order": order, "systems": systems}) + ";\n")
        print(f"{name}: {len(U)} rays, {len(systems[name]['entries'])} features, "
              f"maxw {systems[name]['maxw']}  ({time.time()-t:.1f}s)")
    print("wrote", out, "with", len(order), "systems")
