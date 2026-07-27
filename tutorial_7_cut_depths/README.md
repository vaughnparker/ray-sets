# Radiolarian / Elementary Cut-Regime Explorer — minimal standalone

Interactive visualization of the **cut-regime structure** of the 7 elementary
polyhedral twisty-puzzle axis systems, on the **sphere** body, counting
**external (surface)** pieces vs **total** pieces. For the 20-ray face-turning
icosahedron the regimes are labeled with their **Radiolarian** puzzle names.

## Run it
Open **`radio-piece-explorer.html`** in a browser. Fully self-contained — three.js
r128 and OrbitControls are vendored in this folder, so it runs offline.

## Files

### Runtime (needed to view the page)
| file | role |
|---|---|
| `radio-piece-explorer.html` | the visualization |
| `surface_data.js` | exact per-regime piece configs (`const SURFACE_DATA`) — **generated** |
| `systems_data.js` | ray coordinates for each axis system (`const SYSTEMS`) — **generated** |
| `three.min.js` + `OrbitControls.js` | three.js r128, vendored locally (offline) |

### Build / provenance (regenerate the two data files)
| file | produces | notes |
|---|---|---|
| `dump_all_surface.py` | `surface_data.js` | imports `regime_core` + `critical_depths` from `precompute_elementary`; reads regime names from `puzzle_names.json` |
| `puzzle_names.json` | — | puzzle names per system, keyed by surface histogram; extend it to name more regimes (no code change) |
| `regime_core.py` | — | geometry (T/O/I groups, orbits, rays) + exact symmetry-cached piece counter |
| `precompute_elementary.py` | — | supplies `critical_depths()` (the cut-regime walls) |
| `gen_systems.py` | `systems_data.js` | standalone (numpy + json) |
| `jsonfmt.py` | — | `jdump()`: indented JSON that keeps leaf numeric arrays (rays, histogram rows) on one line; used by both generators |

## Regenerate the data
Requires Python with `numpy` and `scipy`:
```bash
python gen_systems.py        # -> systems_data.js  (ray coordinates)
python dump_all_surface.py   # -> surface_data.js  (piece configs; a few minutes)
```

## Notes
- `surface_data.js` is a multi-system object: `{ order:[...], systems:{ name:
  {rays, maxw, walls, entries:[...]} } }`. Each entry is an interval-regime or a
  wall, with `ext_hist`/`all_hist` (external vs total piece histograms by weight)
  and, for the 20-ray system, a Radiolarian `rad`/`name`.
- three.js r128 (`three.min.js`) and `OrbitControls.js` are vendored in this
  folder and loaded by relative path, so the page runs offline with no CDN.
- It can take a long time for `precompute_compound.py` to run. Sample output:

```
Tetrahedron - corners + edges: 34 regimes  rays=[4, 6]  N=20  (lower bound, 8.6s)
Cube - faces + corners: 49 regimes  rays=[6, 8]  N=20  (lower bound, 16.9s)
Cube - faces + edges: 100 regimes  rays=[6, 12]  N=20  (lower bound, 76.1s)
Cube - corners + edges: 166 regimes  rays=[8, 12]  N=20  (lower bound, 138.7s)
Dodeca - faces + corners: 279 regimes  rays=[12, 20]  N=20  (lower bound, 646.3s)
Dodeca - faces + edges: 344 regimes  rays=[12, 30]  N=20  (lower bound, 1524.6s)
Dodeca - corners + edges: 385 regimes  rays=[20, 30]  N=20  (lower bound, 2777.7s)
wrote compound_data.js
```