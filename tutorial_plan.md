# Tutorial plan

A working outline for turning this repo into a complete, interactive lesson —
building from "what is a turning axis?" all the way to "all possible twisty-puzzle
mechanisms." Each stop is one focused visualization/page that teaches a single
idea, for a reader with only high-school maths. **Draft, not final.**

Status: **[done]** · **[to build]** · **[needs work]** · **[port]** (exists as a
notebook / matplotlib script, port to consistent HTML).

## Before the cut-depth explorer — foundations

**1. One cube, up close** — **[needs work]**
Six face-arrows from the centre; perform a turn and watch the arrows permute.
*Teaches:* an axis is a ray; a move rotates the whole bundle onto itself.

**2. The jamming rule** — **[needs work]**
Spin a bundle; a bad one sends a ray where no ray was → it jams.
*Teaches:* the single closure constraint every axis system must obey.

**3. The 16 ray-sets** — **[done]** (for now): `tutorial_3_ray_sets/ray-set-explorer.html`
Browse all 16 rotatable bundles, grouped by T / O / I; rays drawn as arrows from the
centre, coloured by family. (Shows the 16 distinct ray-sets from `systems_data.js`,
not the 21 pre-dedup candidates the matplotlib `rayview` showed.)
*Teaches:* a complete, finite list exists — the headline result.

**4. Why only these? (poles)** — **[to build]**
Poles on a sphere, orbit families, and the counting that forces T / O / I.
*Teaches:* *why* the list is short and complete.
*Note:* [`klein.md`](klein.md) is a good start; aim for an even better, more visual
proof.

**5. Ray-sets are polyhedra** — **[done]** (for now):
`tutorial_5_polyhedra/ray-set-polyhedra.html`
Interactive three.js port of the `1_ray_sets/polyhedra` matplotlib montages: pick any
of the 16 ray-sets, see its face-turning solid (a face per ray, coloured by family)
and toggle to the vertex-turning **dual**. Carries the "shell is cosmetic /
Mastermorphix" note.
*Teaches:* each axis system is a familiar solid, and the outer shell is cosmetic.

**6. How far you turn (turning systems)** — **[done]** (for now):
`tutorial_6_turning_systems/ray-set-turning.html`
Pick a ray-set and switch between its turning systems; each ray shows a turn-order
polygon (square = 4-fold, triangle = 3-fold, bar = half-turn), so the Domino's split
of the 6-family is visible. Click a ray to turn it by its own allowed step. Data from
`2_turning_systems/gen_turning.py` (wraps `turning_systems.py`).
*Teaches:* the 16 → 21 refinement (see
[`2_turning_systems`](2_turning_systems)).

## The cut-depth explorer

**7. Where you cut (regimes)** — **[done]** (for now), three views in
`tutorial_7_cut_depths/`:
- `radio-piece-explorer.html` — one system in 3-D; slide the cut depth, watch pieces
  appear and vanish; Radiolarians.
- `regime-heatmap.html` — all 7 elementary systems as depth strips; the surface lens,
  with full-width regimes, zero-width regimes, and boundaries.
- `compound-diagram.html` — the 7 two-orbit compound systems as 2-D depth maps (also
  serves stop #8).
*Teaches:* cut depth turns one axis system into many real puzzles — regimes and walls.
*Note:* the deepest cut (`d=0`) is the degenerate end of these tools already. The old
`great_circles` matplotlib view (cuts as circles on a sphere) was retired to `old/`;
that cuts-on-sphere visual could return here as an HTML view later if wanted.

## After — generalise, then the edges

**8. Compound systems** — **[needs work]**
Two or three orbits, each with its own depth; 2-D / 3-D regime maps. The 2-orbit
cut-depth view exists (`tutorial_7_cut_depths/compound-diagram.html`); still to do is
the narrative framing, the three-orbit systems, and switching it to the surface lens.
*Teaches:* combining families multiplies the space.

**9. The body matters** — **[to build]**
The same axis system realised on an icosahedron vs a dodecahedron vs a sphere, and
which regimes survive on which body.
*Teaches:* body-realizability — e.g. the shallow `I·20` regimes that exist as a
corner-turning dodecahedron but have no face-turning-icosahedron form.

**10. The families that never stop (C_n / D_n)** — **[to build]**
Prisms and turntables; why they are infinite and excluded from the 16.
*Teaches:* the boundary of the finite theorem — what "16" does and doesn't count.

**11. The puzzle gallery** — **[to build]**
The 16 (plus notable extras) mapped to physical puzzles: Rubik's Cube, Megaminx,
Skewb, Pyraminx, Helicopter, …
*Teaches:* theory → the shelf. The payoff, and the closest thing to "all possible
mechanisms."

## Notes

- Rough shape: ~6 before, the explorer, ~4 after (~11 total). A tighter **core
  spine** if that's too many: 1 → 3 → 4 → 6 → **7** → 9 → 11.
- Much of the "before" already exists — as notebooks / matplotlib (`rayview`,
  `polyhedra`) or prose (`klein.md`, `intro.md`, `what_is_a_turning_system.md`). The
  work there is largely *porting to consistent HTML*, not inventing from scratch.
- Pacing: concrete before abstract — hold one object (a single cube) for a long
  time before asking the general question.

## Migration plan (long-term)

The HTML tutorial stops are becoming the primary artifact. The eventual goal is to
retire the numbered investigation folders (`1_ray_sets`, `2_turning_systems`,
`3_cut_depths`) into the HTML flow — but **incrementally, gated on each piece having
a home**, not wholesale. Those folders hold three different kinds of thing, with
three different fates:

1. **Python source-of-truth + proofs — keep.** `raysets.py` (proves the 21→16
   collapse with explicit orthogonal maps), `turning_systems.py`, `regime_core.py`,
   and the data generators. This is the repo's rigor and it produces
   `systems_data.js` / `surface_data.js` / `compound_data.js`. Treat Python as the
   **backend** (proofs + data generation), HTML as the frontend. Ideally consolidate
   the canonical geometry into one `lib/` — T/O/I construction is currently
   **duplicated** between `raysets.py` and `tutorial_7_cut_depths/regime_core.py`.
2. **Prose `.md` explainers — fold into HTML** as the stops that host them are built
   (`turning_systems.md`, `what_is_a_turning_system.md`, `cut_depths.md`, `klein.md`).
3. **matplotlib viewers / montages — archive to `old/`** once an HTML stop supersedes
   each: `rayview` → done (stop #3), `polyhedra` → done (stop #5). These two are ready
   to retire now.

Gating per folder:
- `3_cut_depths/` — closest; just `cut_depths.md` notes, compute/viz already in
  `tutorial_7`. Fold the notes into a stop, then archive.
- `1_ray_sets/` — `great_circles` retired to `old/` (blocker gone). Remaining: archive
  the `rayview` matplotlib pieces (superseded by stop #3), and relocate `raysets.py`'s
  proof role to `lib/` (step B). `polyhedra/` can archive too (superseded by stop #5).
- `2_turning_systems/` — stop #6 built; prose (`turning_systems.md`,
  `what_is_a_turning_system.md`) moved into `tutorial_6_turning_systems/`. Only the
  Python remains (`turning_systems.py`, `gen_turning.py`) — it moves in the `lib/`
  consolidation (step B), after which this folder is empty and can go.

Retire folders as they empty out, rather than moving them before their contents have
somewhere to go.
