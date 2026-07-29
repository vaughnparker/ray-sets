# Elementary cut depths (tutorial stop #7)

A ray-set fixes the *axes* of a puzzle, but not where the cuts land. Slide the cut
depth and one axis system becomes **many** real puzzles: pieces appear and vanish, and
the piece configuration is constant over depth **regimes** separated by critical depths
(**walls**). This folder covers the **7 elementary** (single-orbit) axis systems, where
the regimes are computed **exactly** (analytically). The compound systems get their own
folder, [`tutorial_8_compound_cut_depths/`](../tutorial_8_compound_cut_depths).

## The two views

Each is a self-contained HTML page — open it directly in a browser, no server needed.

| page | shows | data |
|---|---|---|
| **`elementary-piece-explorer.html`** | One system in **3-D**: pick an axis system, slide the cut depth, watch pieces appear and vanish on the sphere. External (surface) vs total pieces; the 20-ray system's regimes carry their **Radiolarian** names. | `surface_data.js`, `systems_data.js` + vendored three.js |
| **`elementary-regime-heatmap.html`** | All 7 systems as horizontal strips across depth (shallow → deep). A puzzle is defined by its **surface**, so cells are segmented by surface config: wide **regimes**, thin **zero-width regimes** (distinct puzzles at one exact depth, e.g. the Radiolarian Type-D puzzles), and hairline **boundaries**. | `surface_data.js` |

The **surface vs total** distinction runs through both: surface pieces are the ones you
can see and solve; total includes buried pieces. The heatmap leads with surface (each
cell hover shows both).

**Why exact?** With one shared depth, raising it just *uniformly scales* the plane
arrangement, so its combinatorial type never changes — the configuration can only change
when an arrangement feature crosses the unit sphere (an edge tangent = a **pair** wall,
a vertex on the sphere = a **triple** wall). Enumerating all pairs and triples is
therefore complete. (This is exactly what fails for compound systems, which is why those
fall back to a grid.)

## Files

### Runtime (needed to view the pages)
| file | role |
|---|---|
| `surface_data.js` | per-regime piece configs for the 7 elementary systems (`const SURFACE_DATA`) — **generated** |
| `systems_data.js` | ray coordinates for each axis system (`const SYSTEMS`) — **generated** |
| `three.min.js` + `OrbitControls.js` | three.js r128, vendored locally (offline) — used only by `elementary-piece-explorer.html` |

### Provenance
The Python backend lives in [`../lib/`](../lib). Run from there:
```bash
cd ../lib
python gen_systems.py        # -> tutorial_7_elementary_cut_depths/systems_data.js  (fast)
python dump_all_surface.py   # -> tutorial_7_elementary_cut_depths/surface_data.js  (a few minutes)
```
- `gen_systems.py` — the 16 ray coordinate sets (standalone numpy).
- `dump_all_surface.py` — exact per-regime piece configs; imports `regime_core` and
  `critical_depths` from `precompute_elementary`, and reads regime names from
  `puzzle_names.json`.
- `precompute_elementary.py` — supplies `critical_depths()` (the exact pair/triple walls)
  and a self-check (`EXPECT` regime counts + monotonicity).

## Notes
- `surface_data.js` is a multi-system object: `{ order:[...], systems:{ name:
  {rays, maxw, walls, entries:[...]} } }`. Each entry is an interval-regime or a wall,
  with `ext_hist`/`all_hist` (external vs total piece histograms by weight) and, for the
  20-ray system, a Radiolarian `rad`/`name`.
- three.js r128 is vendored and loaded by relative path, so the pages run offline.
