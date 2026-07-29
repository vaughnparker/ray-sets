#!/usr/bin/env python3
"""Wall-independent ground truth: distinct configs on a fine uniform (dA,dB) grid.
Settles whether the true Tetra 4+6 compound count is ~37 or ~44."""
import numpy as np, sys, time
import regime_core as rc
from precompute_compound import compound_systems

NAME = "Tetrahedron - corners + edges"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 140

for nm, orbits, G in compound_systems():
    if nm != NAME:
        continue
    orbs = [r for _, r in orbits]; U = np.vstack(orbs)
    orb = np.array([k for k, o in enumerate(orbs) for _ in range(len(o))])
    perms = rc.ray_permutations(U, G)
    cfg = set(); t = time.time()
    for i in range(N):
        dA = (i + 0.5) / N
        for j in range(N):
            dB = (j + 0.5) / N
            dvec = np.array([dA if o == 0 else dB for o in orb])
            cfg.add(tuple(sorted(rc.exact_counts(U, dvec, perms).items())))
    print(f"fine grid {N}x{N}: {len(cfg)} distinct configs  ({time.time()-t:.0f}s)")
