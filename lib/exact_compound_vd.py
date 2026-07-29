#!/usr/bin/env python3
"""exact_compound_vd.py - EXACT compound cut-regimes via vertical decomposition.

No dA gridsearch. Each wall is degree <=2 in dB, so write it as
    A(dA) dB^2 + B(dA) dB + C(dA) = 0
with A,B,C polynomials in dA (recovered by a 3x3 sampling of F). The critical dA values
(where the vertical cross-section changes) are then exact polynomial roots:
    - wall-wall intersections : resultant of two dB-quadratics = 0
    - vertical tangents        : discriminant B^2-4AC = 0
    - dB=0 / dB=1 crossings     : C=0 / A+B+C=0
Between consecutive criticals the cell structure is constant, so ONE sample per strip
cell is exact -> a definitive regime count (no dA-sampling fluctuation).

    python exact_compound_vd.py [name-substr]
"""
import numpy as np, itertools, json, os, sys, time
import regime_core as rc
from precompute_compound import compound_systems
from dump_all_surface import build_verts, unbounded, orbit_closure   # surface-piece helpers

try:                                        # optional progress bar (pip install tqdm)
    from tqdm import tqdm as _tqdm
    _TQDM = True
except ImportError:
    _TQDM = False


def surface_hist_compound(U, perms, verts, realset, dvec):
    """External (surface) piece histogram at PER-RAY depths dvec — the compound
    generalisation of dump_all_surface.surface_hist (which assumes one shared depth)."""
    n = len(U); surf = set()
    for (i, j, k, q, nq) in verts:
        V = np.linalg.solve(U[[i, j, k]], dvec[[i, j, k]])       # vertex of planes i,j,k at their depths
        if np.linalg.norm(V) < 1.0:                              # inside the sphere -> not on the surface
            continue
        base = 0
        for l in range(n):
            if l in (i, j, k):
                continue
            if U[l] @ V > dvec[l]:
                base |= (1 << l)
        for a in (0, 1):
            for b in (0, 1):
                for c in (0, 1):
                    mm = base | (a << i) | (b << j) | (c << k)
                    if mm in realset:
                        surf.add(mm)
    for m in realset:
        if m not in surf and unbounded(U, m, 0):
            surf.add(m)
    surf = orbit_closure(surf, perms, n)
    h = {}
    for m in surf:
        w = bin(m).count('1')
        if w > 0:
            h[w] = h.get(w, 0) + 1
    return dict(sorted(h.items()))

SMALLEST = {"Tetrahedron - corners + edges", "Cube - faces + corners"}
DEDUP = "--nodedup" not in sys.argv        # dedup is correct + lossless; on by default
U = None; ORB = None


def wallF(kind, idx, g, M, dA, dB):
    d = (dA, dB)
    if kind == "P":
        i, j = idx; di, dj = d[ORB[i]], d[ORB[j]]
        return di*di + dj*dj - 2*di*dj*g - (1 - g*g)
    if kind == "T":
        dv = np.array([d[ORB[i]] for i in idx]); q = M @ dv; return float(q @ q - 1)
    dv = np.array([d[ORB[i]] for i in idx])
    return float(np.linalg.det(np.column_stack([U[list(idx)], dv])))


def abc_polys(w):
    """A(dA),B(dA),C(dA) as len-3 coeff arrays (highest degree first)."""
    kind, idx, g, M = w
    def ABC(dA):
        f0 = wallF(kind, idx, g, M, dA, 0.0)
        fh = wallF(kind, idx, g, M, dA, 0.5)
        f1 = wallF(kind, idx, g, M, dA, 1.0)
        A = 2*f1 + 2*f0 - 4*fh; B = (f1 - f0) - A; C = f0
        return A, B, C
    v0 = ABC(0.0); vh = ABC(0.5); v1 = ABC(1.0)
    def fit(a, b, c):
        q2 = 2*c + 2*a - 4*b; q1 = (c - a) - q2; return np.array([q2, q1, a])
    return (fit(v0[0], vh[0], v1[0]), fit(v0[1], vh[1], v1[1]), fit(v0[2], vh[2], v1[2]))


def build(U_, orb):
    """Distinct walls as (A,B,C) dA-polys, deduped by normalized signature."""
    global U, ORB; U, ORB = U_, orb; n = len(U); cand = []
    for i, j in itertools.combinations(range(n), 2):
        g = float(U[i] @ U[j])
        if abs(abs(g) - 1) < 1e-9:
            continue
        cand.append(("P", (i, j), g, None))
    for i, j, k in itertools.combinations(range(n), 3):
        M = U[[i, j, k]]
        if abs(np.linalg.det(M)) < 1e-6:
            continue
        cand.append(("T", (i, j, k), None, np.linalg.inv(M)))
    for q in itertools.combinations(range(n), 4):
        cand.append(("Q", q, None, None))
    polys = []
    for w in cand:
        A, B, C = abc_polys(w)
        m = np.max(np.abs(np.concatenate([A, B, C])))
        if m < 1e-9:                                            # identically-trivial: not a wall
            continue
        polys.append((A / m, B / m, C / m))                    # normalise so tolerances are absolute
    if not DEDUP:
        return polys
    pm, ps = np.polymul, np.polysub
    def same_curve(w1, w2):
        (A1, B1, C1), (A2, B2, C2) = w1, w2
        for cr in (ps(pm(A1, B2), pm(A2, B1)), ps(pm(A1, C2), pm(A2, C1)), ps(pm(B1, C2), pm(B2, C1))):
            if np.max(np.abs(cr)) > 1e-6:                       # cross-product non-zero -> different curve
                return False
        return True
    reps = []
    for w in polys:
        if not any(same_curve(w, r) for r in reps):
            reps.append(w)
    return reps


def roots01(coeffs):
    coeffs = np.trim_zeros(np.asarray(coeffs, float), "f")
    if len(coeffs) <= 1:
        return []
    return [float(x.real) for x in np.roots(coeffs)
            if abs(x.imag) < 1e-7 and 1e-6 < x.real < 1 - 1e-6]


def dbdeg(A, B, C):
    """degree of the wall in dB: 2 (conic), 1 (linear), 0 (dB-independent / vertical)."""
    if np.max(np.abs(A)) > 1e-9: return 2
    if np.max(np.abs(B)) > 1e-9: return 1
    return 0


def resultant(w1, w2):
    """dA-polynomial whose roots are where the two walls share a dB-root — correct even
    when one/both are linear in dB (the quadruple walls are)."""
    pm, pa, ps = np.polymul, np.polyadd, np.polysub
    A1, B1, C1 = w1; A2, B2, C2 = w2
    d1, d2 = dbdeg(*w1), dbdeg(*w2)
    if d1 < 1 or d2 < 1:
        return None                                            # a dB-independent wall has no dB-root
    if d1 == 2 and d2 == 2:
        t1 = ps(pm(A1, C2), pm(A2, C1)); t2 = ps(pm(A1, B2), pm(A2, B1)); t3 = ps(pm(B1, C2), pm(B2, C1))
        return ps(pm(t1, t1), pm(t2, t3))
    if d1 == 1 and d2 == 1:
        return ps(pm(C1, B2), pm(C2, B1))                      # two lines: c1 b2 - c2 b1
    # one linear (bl,cl), one quadratic (aq,bq,cq): aq cl^2 - bl bq cl + bl^2 cq
    (bl, cl), (aq, bq, cq) = ((B1, C1), (A2, B2, C2)) if d1 == 1 else ((B2, C2), (A1, B1, C1))
    return pa(ps(pm(aq, pm(cl, cl)), pm(bl, pm(bq, cl))), pm(pm(bl, bl), cq))


def critical_dA(walls):
    pm, pa, ps = np.polymul, np.polyadd, np.polysub
    crit = set()
    for A, B, C in walls:
        if dbdeg(A, B, C) == 2:
            for r in roots01(ps(pm(B, B), pm([4.0], pm(A, C)))):  # vertical tangent
                crit.add(round(r, 7))
        for r in roots01(C):                                       # dB=0 (also the vertical walls)
            crit.add(round(r, 7))
        for r in roots01(pa(pa(A, B), C)):                         # dB=1
            crit.add(round(r, 7))
    for w1, w2 in itertools.combinations(walls, 2):
        R = resultant(w1, w2)
        if R is not None:
            for r in roots01(R):
                crit.add(round(r, 7))
    return sorted(crit)


def dB_bps(walls, dA):
    bps = {0.0, 1.0}
    for A, B, C in walls:
        a = np.polyval(A, dA); b = np.polyval(B, dA); c = np.polyval(C, dA)
        if abs(a) < 1e-12:
            if abs(b) > 1e-12:
                x = -c / b
                if 1e-7 < x < 1 - 1e-7: bps.add(x)
        else:
            disc = b*b - 4*a*c
            if disc >= 0:
                s = disc**0.5
                for x in ((-b + s)/(2*a), (-b - s)/(2*a)):
                    if 1e-7 < x < 1 - 1e-7: bps.add(x)
    return sorted(bps)


def canon(h):
    return tuple(sorted((int(k), int(v)) for k, v in h.items()))


def grid_configs(name):
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "tutorial_8_compound_cut_depths", "compound_data.js")
    s = open(p, encoding="utf-8").read(); D = json.loads(s[s.index('{'):s.rindex('}') + 1])
    return {canon(r["hist"]) for r in D[name]["regimes"]}


def sample_column(U_, orb, perms, walls, dA):
    """distinct configs found in one dA column (exact dB cells)."""
    got = set()
    bps = dB_bps(walls, dA)
    for lo, hi in zip(bps[:-1], bps[1:]):
        dvec = np.array([dA if o == 0 else (lo + hi)/2 for o in orb])
        got.add(canon(rc.exact_counts(U_, dvec, perms)))
    return got


def finescan(U_, orb, perms, walls, K=400):
    """independent reference: dense dA, exact dB, ALL walls (no criticals)."""
    configs = set()
    for dA in np.linspace(0, 1, K + 2)[1:-1]:
        configs |= sample_column(U_, orb, perms, walls, float(dA))
    return configs


def chamber_polys(walls, aL, aR, ncell, M=7):
    """Polygons for the ncell dB-cells of one strip, edges sampled along the true wall
    arcs across (aL,aR) -> smooth boundaries. Returns [(cell_index, [[dA,dB],...]), ...]."""
    eps = (aR - aL) * 1e-3
    cols = []                                                 # (dA, sorted breakpoints)
    for t in np.linspace(0.0, 1.0, M):
        dA = aL + (aR - aL) * t                               # polygon x spans the FULL strip
        dAe = min(max(dA, aL + eps), aR - eps)                # but eval breakpoints just inside (dodge criticals)
        cols.append((dA, dB_bps(walls, dAe)))
    out = []
    for k in range(ncell):
        low, high = [], []
        for dA, bps in cols:
            if k + 1 < len(bps):                              # guard against numerical count drift
                low.append([round(dA, 5), round(bps[k], 5)])
                high.append([round(dA, 5), round(bps[k + 1], 5)])
        if len(low) >= 2:
            out.append((k, low + high[::-1]))                 # bottom L->R, top R->L
    return out


def compute_boundaries(walls, strips):
    """Regime-boundary polylines (in dA,dB): the arcs/segments where the regime changes.
    strips: list of (aL, aR, [cid per dB-cell])."""
    bnds = []
    # within a strip: internal breakpoint arcs where the cid changes across them
    for aL, aR, cids in strips:
        e = (aR - aL) * 1e-3
        for k in range(len(cids) - 1):
            if cids[k] == cids[k + 1]:
                continue
            arc = []
            for t in np.linspace(0, 1, 7):
                dA = aL + (aR - aL) * t
                bps = dB_bps(walls, min(max(dA, aL + e), aR - e))
                if k + 1 < len(bps):
                    arc.append([round(dA, 5), round(bps[k + 1], 5)])
            if len(arc) >= 2:
                bnds.append(arc)
    # between strips: vertical segments at the critical where the cid changes across it
    def cell_cid(bps, cids, dB):
        for m in range(len(bps) - 1):
            if bps[m] <= dB <= bps[m + 1]:
                return cids[m] if m < len(cids) else None
        return None
    for (aL, aR, cidsL), (aL2, aR2, cidsR) in zip(strips[:-1], strips[1:]):
        a = aR
        bpsL = dB_bps(walls, a - 1e-4); bpsR = dB_bps(walls, a + 1e-4)
        marks = sorted(set(bpsL) | set(bpsR)); seg = None
        for lo, hi in zip(marks[:-1], marks[1:]):
            mid = (lo + hi) / 2
            cl = cell_cid(bpsL, cidsL, mid); cr = cell_cid(bpsR, cidsR, mid)
            diff = cl is not None and cr is not None and cl != cr
            if diff:
                seg = [seg[0], hi] if seg else [lo, hi]
            elif seg:
                bnds.append([[round(a, 5), round(seg[0], 5)], [round(a, 5), round(seg[1], 5)]]); seg = None
        if seg:
            bnds.append([[round(a, 5), round(seg[0], 5)], [round(a, 5), round(seg[1], 5)]])
    return bnds


def run(name, orbits, G, want_ref=False, want_poly=False):
    global U, ORB
    orbs = [rays for _, rays in orbits]; U_ = np.vstack(orbs)
    orb = np.array([k for k, o in enumerate(orbs) for _ in range(len(o))])
    walls = build(U_, orb); U, ORB = U_, orb
    perms = rc.ray_permutations(U_, G); verts = build_verts(U_) if want_poly else None
    if want_poly:
        print(f"    {len(walls)} walls; computing critical depths...", flush=True)
    t = time.time(); crit = critical_dA(walls); t_crit = time.time() - t
    xs = [0.0] + crit + [1.0]
    cfgid = {}; cfg_table = []; ncells = 0; chambers = []; strips = []   # cfgid: canon-config -> regime id
    _items = list(enumerate(zip(xs[:-1], xs[1:])))
    _loop = _tqdm(_items, desc="    strips", unit="strip", leave=False) if (want_poly and _TQDM) else _items
    for si, (aL, aR) in _loop:
        dA = (aL + aR) / 2
        bps = dB_bps(walls, dA)
        cell_cfg = {}
        for k in range(len(bps) - 1):
            dvec = np.array([dA if o == 0 else (bps[k] + bps[k + 1]) / 2 for o in orb])
            h = rc.exact_counts(U_, dvec, perms)
            key = canon(h); ncells += 1
            if key not in cfgid:
                rec = {"total": int(sum(h.values())), "maxw": int(max(h)) if h else 0,
                       "hist": {str(w): int(c) for w, c in h.items()}}
                if want_poly:                                   # add the external (surface) histogram
                    _, masks = rc.exact_counts(U_, dvec, perms, return_masks=True, seeds=300)
                    eh = surface_hist_compound(U_, perms, verts, set(masks), dvec)
                    rec.update({"ext_total": int(sum(eh.values())),
                                "ext_hist": {str(w): int(c) for w, c in eh.items()}})
                cfgid[key] = len(cfg_table); cfg_table.append(rec)
            cell_cfg[k] = cfgid[key]
        strips.append((aL, aR, [cell_cfg[k] for k in range(len(bps) - 1)]))
        if want_poly:
            for k, poly in chamber_polys(walls, aL, aR, len(bps) - 1):
                if k in cell_cfg:
                    cid = cell_cfg[k]; r = cfg_table[cid]
                    chambers.append({"poly": poly, "cid": cid, "total": r["total"], "maxw": r["maxw"]})
        if want_poly and not _TQDM and (si % 5 == 0):
            print(f"    strip {si+1}/{len(_items)}", flush=True)
    # renumber regimes so lower id = fewer pieces
    order = sorted(range(len(cfg_table)), key=lambda i: (cfg_table[i]["total"], cfg_table[i]["maxw"]))
    remap = {old: new for new, old in enumerate(order)}
    cfg_table = [cfg_table[i] for i in order]
    for c in chambers:
        c["cid"] = remap[c["cid"]]
    strips = [(aL, aR, [remap[c] for c in cids]) for aL, aR, cids in strips]
    bounds = compute_boundaries(walls, strips) if want_poly else []
    ref = finescan(U_, orb, perms, walls, K=400) if want_ref else None
    return walls, crit, set(cfgid), ncells, t_crit, ref, chambers, cfg_table, bounds


OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "tutorial_8_compound_cut_depths", "exact_vd_data.js")

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    filt = args[0] if args else None
    want_ref = "--ref" in sys.argv
    want_poly = "--poly" in sys.argv
    want_all = "--all" in sys.argv            # all seven 2-orbit systems, not just the two smallest
    data = {}
    if want_poly and os.path.exists(OUT):
        try:
            s = open(OUT, encoding="utf-8").read(); data = json.loads(s[s.index('{'):s.rindex('}') + 1])
        except Exception:
            data = {}
    for name, orbits, G in compound_systems():
        if len(orbits) != 2:                  # this VD is 2-D (skip the two 3-orbit systems)
            continue
        if filt:                              # a name filter selects ALL matching 2-orbit systems
            if filt.lower() not in name.lower():
                continue
        elif not want_all and name not in SMALLEST:   # no filter: default to the two smallest unless --all
            continue
        print(f"\n=== {name}  rays={[len(r) for _, r in orbits]}  (dedup={DEDUP}) ===", flush=True)
        t = time.time()
        walls, crit, configs, ncells, t_crit, ref, chambers, cfg_table, bounds = run(name, orbits, G, want_ref, want_poly)
        dt = time.time() - t
        grid = grid_configs(name); missing = grid - configs
        print(f"  {len(walls)} walls, {len(crit)} critical dA, {ncells} VD cells, {dt:.1f}s")
        print(f"  EXACT regimes: {len(configs)}   grid: {len(grid)}   "
              f"grid found: {len(grid & configs)}/{len(grid)} {'OK' if not missing else 'MISSING'}")
        if want_ref:
            rm = ref - configs
            print(f"  fine-scan ref: {len(ref)}   VD misses {len(rm)} of it"
                  f"   {'(criticals incomplete)' if rm else '(criticals complete)'}")
        if want_poly:
            orbs = [r for _, r in orbits]
            data[name] = {"labels": [lab for lab, _ in orbits], "rays": [len(r) for _, r in orbits],
                          "count": len(configs), "grid_count": len(grid),
                          "ray_xyz": [[round(float(x), 6) for x in v] for o in orbs for v in o],
                          "orb": [k for k, o in enumerate(orbs) for _ in range(len(o))],
                          "regimes": cfg_table, "chambers": chambers, "boundaries": bounds}
            with open(OUT, "w", encoding="utf-8") as f:
                f.write("const EXACT_VD = " + json.dumps(data) + ";\n")
            print(f"  wrote {len(chambers)} chambers, {len(cfg_table)} regimes, "
                  f"{len(bounds)} boundary lines -> exact_vd_data.js", flush=True)
