# Cut depths — computed and explored (tutorial stop #7)

A ray-set fixes the *axes* of a puzzle, but not where the cuts land. Slide the cut
depth and one axis system becomes **many** real puzzles: pieces appear and vanish,
and the piece configuration is constant over depth **regimes** separated by critical
depths (**walls**). This folder computes that structure and shows it three ways.

## The three views

Each is a self-contained HTML page — open it directly in a browser, no server needed.

| page | shows | data |
|---|---|---|
| **`radio-piece-explorer.html`** | One system in **3-D**: pick an axis system, slide the cut depth, watch pieces appear and vanish on the sphere. External (surface) vs total pieces; the 20-ray system's regimes carry their **Radiolarian** names. | `surface_data.js`, `systems_data.js` + vendored three.js |
| **`regime-heatmap.html`** | All 7 **elementary** systems as horizontal strips across depth (shallow → deep). A puzzle is defined by its **surface**, so cells are segmented by surface config: wide **regimes**, thin **zero-width regimes** (distinct puzzles at one exact depth, e.g. the Radiolarian Type-D puzzles), and hairline **boundaries**. | `surface_data.js` |
| **`compound-diagram.html`** | The 7 two-orbit **compound** systems as 2-D depth maps — one axis per orbit's depth — with thick walls separating regimes. Grid-sampled (a lower bound); counts are by total pieces. | `compound_data.js` |

The **surface vs total** distinction runs through all three: surface pieces are the
ones you can see and solve; total includes buried pieces. `regime-heatmap` leads with
surface (each cell hover shows both); `compound-diagram` is total-only for now
(matching the surface lens there means adding the flood-fill to
`precompute_compound.py` and re-running).

## Files

### Runtime (needed to view the pages)
| file | role |
|---|---|
| `surface_data.js` | per-regime piece configs for the 7 elementary systems (`const SURFACE_DATA`) — **generated** |
| `systems_data.js` | ray coordinates for each axis system (`const SYSTEMS`) — **generated** |
| `compound_data.js` | grid-sampled regime maps for the compound systems (`const COMPOUND`) — **generated** |
| `three.min.js` + `OrbitControls.js` | three.js r128, vendored locally (offline) — used only by `radio-piece-explorer.html` |

### Build / provenance (regenerate the data)
| file | produces | notes |
|---|---|---|
| `gen_systems.py` | `systems_data.js` | standalone (numpy + json) |
| `dump_all_surface.py` | `surface_data.js` | imports `regime_core` + `critical_depths` from `precompute_elementary`; reads regime names from `puzzle_names.json` |
| `precompute_compound.py` | `compound_data.js` | grid sample over each orbit's depth; slow for the big dodeca systems |
| `precompute_elementary.py` | — | supplies `critical_depths()` (the cut-regime walls) + a self-check |
| `regime_core.py` | — | geometry (T/O/I groups, orbits, rays) + exact symmetry-cached piece counter |
| `puzzle_names.json` | — | puzzle names per system, keyed by surface histogram; extend it to name more regimes (no code change) |
| `jsonfmt.py` | — | `jdump()`: indented JSON that keeps leaf numeric arrays on one line; used by all generators |

## Regenerate the data
Requires Python with `numpy` and `scipy`:
```bash
python gen_systems.py            # -> systems_data.js  (ray coordinates)
python dump_all_surface.py       # -> surface_data.js  (elementary piece configs; a few minutes)
python precompute_compound.py --n2=20 --dims=2   # -> compound_data.js (compound maps; slow, see below)
```

## Notes
- `surface_data.js` is a multi-system object: `{ order:[...], systems:{ name:
  {rays, maxw, walls, entries:[...]} } }`. Each entry is an interval-regime or a
  wall, with `ext_hist`/`all_hist` (external vs total piece histograms by weight)
  and, for the 20-ray system, a Radiolarian `rad`/`name`.
- `compound_data.js` per system: `{rays, labels, N, depths, method:"grid",
  regimes:[{total,hist,maxw}], count, grid}` — `grid` is an `N×N` array of regime
  ids. The count is a **lower bound**: a regime thinner than a grid line can be
  missed, and exact compound enumeration needs an extra wall class (see
  `precompute_compound.py`'s docstring).
- three.js r128 is vendored and loaded by relative path, so the pages run offline
  with no CDN.
- `precompute_compound.py` is slow. Sample output:

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
