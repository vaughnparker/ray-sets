#!/usr/bin/env python3
"""Fast wall/dedup diagnostic (no piece counting). For Tetra 4+6:
counts candidate/non-trivial/distinct walls, and compares the dB-breakpoint set at a few
dA values using ALL non-trivial walls vs the DEDUPED set. If deduped has fewer
breakpoints, the dedup is merging distinct curves."""
import numpy as np, itertools
from precompute_compound import compound_systems

NAME = "Tetrahedron - corners + edges"
for nm, orbits, G in compound_systems():
    if nm != NAME:
        continue
    orbs = [r for _, r in orbits]; U = np.vstack(orbs)
    orb = np.array([k for k, o in enumerate(orbs) for _ in range(len(o))]); n = len(U)

    def wallF(w, dA, dB):
        kind, idx, g, M = w; d = (dA, dB)
        if kind == "P":
            i, j = idx; di, dj = d[orb[i]], d[orb[j]]; return di*di+dj*dj-2*di*dj*g-(1-g*g)
        if kind == "T":
            dv = np.array([d[orb[i]] for i in idx]); q = M @ dv; return float(q@q-1)
        dv = np.array([d[orb[i]] for i in idx]); return float(np.linalg.det(np.column_stack([U[list(idx)], dv])))

    cand = []
    for i, j in itertools.combinations(range(n), 2):
        g = float(U[i] @ U[j])
        if abs(abs(g)-1) < 1e-9: continue
        cand.append(("P", (i, j), g, None))
    for i, j, k in itertools.combinations(range(n), 3):
        M = U[[i, j, k]]
        if abs(np.linalg.det(M)) < 1e-6: continue
        cand.append(("T", (i, j, k), None, np.linalg.inv(M)))
    for q in itertools.combinations(range(n), 4):
        cand.append(("Q", q, None, None))

    def abc(w):
        def ABC(dA):
            f0 = wallF(w, dA, 0.0); fh = wallF(w, dA, 0.5); f1 = wallF(w, dA, 1.0)
            A = 2*f1+2*f0-4*fh; B = (f1-f0)-A; C = f0; return A, B, C
        v0, vh, v1 = ABC(0.0), ABC(0.5), ABC(1.0)
        def fit(a, b, c): q2 = 2*c+2*a-4*b; return np.array([q2, (c-a)-q2, a])
        return tuple(fit(v0[t], vh[t], v1[t]) for t in range(3))

    polys = []
    for w in cand:
        A, B, C = abc(w); m = np.max(np.abs(np.concatenate([A, B, C])))
        if m >= 1e-9: polys.append((A/m, B/m, C/m))

    pm, ps = np.polymul, np.polysub
    def same(w1, w2):
        (A1, B1, C1), (A2, B2, C2) = w1, w2
        for cr in (ps(pm(A1, B2), pm(A2, B1)), ps(pm(A1, C2), pm(A2, C1)), ps(pm(B1, C2), pm(B2, C1))):
            if np.max(np.abs(cr)) > 1e-6: return False
        return True
    reps = []
    for w in polys:
        if not any(same(w, r) for r in reps): reps.append(w)

    def roots(w, dA):
        A, B, C = w; a = np.polyval(A, dA); b = np.polyval(B, dA); c = np.polyval(C, dA); out = []
        if abs(a) < 1e-12:
            if abs(b) > 1e-12:
                x = -c/b
                if 1e-7 < x < 1-1e-7: out.append(round(x, 6))
        else:
            disc = b*b-4*a*c
            if disc >= 0:
                s = disc**0.5
                for x in ((-b+s)/(2*a), (-b-s)/(2*a)):
                    if 1e-7 < x < 1-1e-7: out.append(round(x, 6))
        return out

    def roots_exact(w, dA):
        """dB-roots from the TRUE F at this dA (PoC-style 3-point dB fit)."""
        f0 = wallF(w, dA, 0.0); fh = wallF(w, dA, 0.5); f1 = wallF(w, dA, 1.0)
        A = 2*f1+2*f0-4*fh; B = (f1-f0)-A; C = f0; out = []
        if abs(A) < 1e-12:
            if abs(B) > 1e-12:
                x = -C/B
                if 1e-7 < x < 1-1e-7: out.append(round(x, 6))
        else:
            disc = B*B-4*A*C
            if disc >= 0:
                s = disc**0.5
                for x in ((-B+s)/(2*A), (-B-s)/(2*A)):
                    if 1e-7 < x < 1-1e-7: out.append(round(x, 6))
        return out

    print(f"{NAME}:  {len(cand)} candidate, {len(polys)} non-trivial, {len(reps)} distinct (dedup)")
    for dA in (0.23, 0.37, 0.51, 0.68, 0.82):
        be = {r for w in cand for r in roots_exact(w, dA)}    # PoC-style, exact F, all candidates
        ba = {r for w in polys for r in roots(w, dA)}         # all non-trivial via fitted polys
        bd = {r for w in reps for r in roots(w, dA)}          # deduped via fitted polys
        f1 = "" if be == ba else "  <-- poly-fit != exact F"
        f2 = "" if ba == bd else "  <-- dedup LOST breakpoints"
        print(f"  dA={dA}: breakpoints  exactF={len(be)}  allPoly={len(ba)}  deduped={len(bd)}{f1}{f2}")
