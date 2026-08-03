# Tutorial plan

A working outline for turning this repo into a complete, interactive lesson —
building from "what is a turning axis?" all the way to "all possible twisty-puzzle
mechanisms." Each stop is one focused visualization/page that teaches a single
idea, for a reader with only high-school maths. **Draft, not final.**

Status: **[done]** · **[to build]** · **[needs work]** · **[port]** (exists as a
notebook / matplotlib script, port to consistent HTML).

---

# The reader's path (the curriculum)

*This section is the target: what the finished project is, and the order a reader meets
it. The stop-by-stop notes further down are the implementation detail for this path.*

## The goal, in one sentence

**"How many twisty puzzles could exist?" — take a question that looks infinite, and show
that it has a finite, structured answer.**

The thesis underneath it: **the classification system is the artwork.** The deliverable is
not a catalogue of puzzles; it is a *periodic table* of them.

## Who it is for

- **Primary — puzzle builders and designers.** Deep physical intuition about puzzles,
  high-school maths. They know what a Skewb is; they do not know what orbit-stabilizer
  means. Every call — degrees not radians, "family" not "orbit", concrete before
  abstract — is made for this reader.
- **Secondary — mathematically curious general readers**, who need the puzzle intuition
  supplied but will follow an argument.
- **Third, quietly — the author, as a research instrument.** This is why exhaustive and
  ugly data must exist even when it does not belong in the reader's path.

## What the finished thing looks like

A single site. A reader arrives at "how many twisty puzzles could exist?", walks about
nine interactive pages, and leaves with **a number and a map** — knowing not just *how
many* but *why the list stops*, and able to point at any puzzle on their shelf and say
where it sits in the structure.

## The path — four acts

**Spine** = the linear first read. **Reference** = valuable, but a detour on first pass.

| Act | Page | What the reader learns |
|---|---|---|
| — | `index.html` | The hook: N×N×N is infinite, yet they are all one *canonical form*. So how many forms are there? |
| **I. The rule** | `tutorial_1_axes/three-by-three.html` | A piece's kind = **how many axes grip it**. The cube and the sphere are the same object. |
| | `tutorial_1_axes/one-cube.html` | Rotate the whole cube: every axis must land on an axis, or it **jams**. Families come only in sizes 6/8/12/24 — you do not get to choose. |
| **II. The finite lists** | `tutorial_3_ray_sets/ray-set-explorer.html` | The complete list exists: **16 ray-sets**. |
| | `tutorial_4_why_only_three/` | *Why* it is complete: **you run out of room in a triangle** → only 3 symmetry families → **7 elementary** ray-sets. |
| | `tutorial_5_polyhedra/ray-set-polyhedra.html` | Each ray-set is a familiar solid; the outer shell is cosmetic. |
| | `tutorial_6_turning_systems/ray-set-turning.html` | Turn orders refine the list (16 → 21): the Domino. |
| **III. Where you cut** | `tutorial_7…/elementary-explorer.html` | One system, one depth slider: cut depth turns one axis system into many real puzzles. |
| | `tutorial_7…/elementary-regime-heatmap.html` | All 7 systems at once → **91 elementary regimes**. The payoff number. |
| | `tutorial_8…/compound-explorer.html` | Two orbits, two depths — the space multiplies. |
| **IV. Finale** *(unbuilt)* | body-realizability · C_n/D_n · the periodic table | Which puzzles are physically buildable; where "16" stops counting; and each canonical puzzle blossoming into its ~2^k reductions. |

**Reference / deep dives** (kept, but off the spine — to be grouped under their own heading
in `index.html`):
`tutorial_7…/elementary-piece-explorer.html` (still the only view that shows **puzzle
names** — 18 named entries in `surface_data.js` — plus the jump table and skip-to-next-config;
stays on the spine's shelf until `elementary-explorer.html` absorbs those),
`tutorial_8…/compound-exact-vd.html` (the chambers-vs-regimes explanation is good teaching and
may earn its way onto the spine once stop 8 has a narrative),
`tutorial_8…/compound-gridsearch-heatmap.html`.

## Known holes in the path (2026-08-03)

1. **The spine breaks at stop 4.** The reader is told "here are 16!" and the *why* is a
   markdown file. Biggest hole; prose is drafted, HTML still to build.
2. **`index.html` is a menu, not a narrative.** It hands over cards instead of telling the
   story that makes a reader *want* stop 4. Deferred, but it is what turns a set of pages
   into one experience.
3. **Act IV does not exist yet** — body-realizability, the C_n/D_n boundary, and the
   periodic table are all unbuilt.
4. **The compound count is unfinished** (~1000 is still a guess; the `--all` runs are
   multi-week and deferred). The elementary 91 is exact and can carry the headline for now.

---

## Before the cut-depth explorer — foundations

**0. A cube and a sphere** — **[done]** (for now): `tutorial_1_axes/three-by-three.html`.
The gentlest entry: a real 3×3 (26 cubies) beside the *same* cuts drawn on a sphere, with
**one shared camera** so dragging either rotates both. Cubies are coloured **by piece type**
using the explorers' palette (centres red / edges blue / corners yellow), because a piece's
type is exactly **how many axes grip it** — which is its nonzero-coordinate count, and also
the sphere shader's weight `w`. Verified: 6 + 12 + 8 = 26 on both sides.
- "Rotate 90°" turns the whole cube; an outlined piece shows it always lands in a slot of its
  own kind, while the sphere is visibly unchanged (the cuts land back on themselves).
- A depth slider (0.03–0.56, inside the first regime — verified the regime ends at
  1/√3 ≈ 0.577) shows the cuts moving while the puzzle stays the 3×3×3: the first taste of a
  **regime**.
*Teaches:* piece type = number of gripping axes; the cube and the sphere are one object;
"lands on its own kind" as the intuition the jamming rule will formalise.

**1 + 2. One cube, up close / the jamming rule** — **[done]** (for now):
`tutorial_1_axes/one-cube.html`. Built as **one page, two acts**, since they share all
machinery (cube + six face-arrows + turn animation) and form a single argument.
*Note:* the test is a **whole-cube rotation**, not a face turn — a U face turn leaves the
F/R/B/L centres untouched, so it does not permute the axes; rotating the whole cube does.
- *Act 1 — the bundle:* six face-arrows from the centre; turn about any one (menu or click
  an arrow) and watch the arrows permute, with the permutation printed (`F → R`, …).
- *Act 2 — the jamming rule:* add a seventh axis aimed anywhere (tilt/spin sliders), turn,
  and see it land where no axis was → **✕ it jams**. "Add its whole family" then closes the
  bundle by adding the full orbit — and the family is only ever **6, 8, 12 or 24**
  (verified: the cube's rotation group has order 24; orbit sizes are 24/|stabilizer|).
*Teaches:* an axis is a ray; a move permutes the bundle; closure is the one constraint —
and you cannot choose a family's size, which is exactly why only finitely many bundles exist.

**3. The 16 ray-sets** — **[done]** (for now): `tutorial_3_ray_sets/ray-set-explorer.html`
Browse all 16 rotatable bundles, grouped by T / O / I; rays drawn as arrows from the
centre, coloured by family. (Shows the 16 distinct ray-sets from `systems_data.js`,
not the 21 pre-dedup candidates the matplotlib `rayview` showed.)
*Teaches:* a complete, finite list exists — the headline result.

**4. Why only these?** — **[prose drafted, visualization to build]**, in
`tutorial_4_why_only_three/`.
*Teaches:* *why* the list is short and complete.
- `why_only_three.md` — **[draft]** the accessible proof, chosen over klein.md's counting
  argument: poles → the sphere splits into identical triangles → angles 180/p, 180/q, 180/r
  → a spherical triangle must overshoot 180° → **1/p + 1/q + 1/r > 1** → only (2,2,n),
  (2,3,3), (2,3,4), (2,3,5). Uses degrees, no radians, no group-theory vocabulary; falls out
  with the right rotation counts (12 / 24 / 60) as a free check. Known soft spot, flagged
  in-text: it *assumes* the poles tile the sphere into triangles (klein.md avoids that
  assumption but is fiddlier).
- `klein.md` — the rigorous pole-counting proof, kept as the airtight appendix.
- `from_groups_to_raysets.md` — **[to write]** 3 groups × 3 pole families = 9, minus 2
  coincidences (tetra edges = cube faces; tetra faces = mirror of tetra corners) = **7**.
- Then the HTML: drag p/q/r and watch the triangle shrink to nothing when the budget runs out.

**5. Ray-sets are polyhedra** — **[done]** (for now):
`tutorial_5_polyhedra/ray-set-polyhedra.html`
Interactive three.js port of the `polyhedra` matplotlib montages (retired to `old/`): pick any
of the 16 ray-sets, see its face-turning solid (a face per ray, coloured by family)
and toggle to the vertex-turning **dual**. Carries the "shell is cosmetic /
Mastermorphix" note.
*Teaches:* each axis system is a familiar solid, and the outer shell is cosmetic.

**6. How far you turn (turning systems)** — **[done]** (for now):
`tutorial_6_turning_systems/ray-set-turning.html`
Pick a ray-set and switch between its turning systems; each ray shows a turn-order
polygon (square = 4-fold, triangle = 3-fold, bar = half-turn), so the Domino's split
of the 6-family is visible. Click a ray to turn it by its own allowed step. Data from
`lib/gen_turning.py` (wraps `lib/turning_systems.py`).
*Teaches:* the 16 → 21 refinement.

## The cut-depth explorer

**7. Where you cut (regimes)** — **[done]** (for now), two views in
`tutorial_7_elementary_cut_depths/` (the **7 elementary** systems, computed **exactly**):
- `elementary-piece-explorer.html` — one system in 3-D; slide the cut depth, watch
  pieces appear and vanish; Radiolarians.
- `elementary-regime-heatmap.html` — all 7 systems as depth strips; the surface lens,
  with full-width regimes, zero-width regimes, and boundaries.
*Teaches:* cut depth turns one axis system into many real puzzles — regimes and walls.
*Note:* the deepest cut (`d=0`) is the degenerate end of these tools already. The old
`great_circles` matplotlib view (cuts as circles on a sphere) was retired to `old/`;
that cuts-on-sphere visual could return here as an HTML view later if wanted.

## After — generalise, then the edges

**8. Compound systems** — **[needs work]**, in `tutorial_8_compound_cut_depths/`.
Two or three orbits, each with its own depth; 2-D / 3-D regime maps. The 2-orbit
cut-depth view exists (`compound-gridsearch-heatmap.html`, grid-sampled = a lower
bound); still to do is the narrative framing, the three-orbit systems, and switching
it to the surface lens.
*Teaches:* combining families multiplies the space.

**9. The body matters** — **[to build]**
The same axis system realised on an icosahedron vs a dodecahedron vs a sphere, and
which regimes survive on which body.
*Teaches:* body-realizability — e.g. the shallow `I·20` regimes that exist as a
corner-turning dodecahedron but have no face-turning-icosahedron form.

**10. The families that never stop (C_n / D_n)** — **[to build]**
Prisms and turntables; why they are infinite and excluded from the 16.
*Teaches:* the boundary of the finite theorem — what "16" does and doesn't count.

**11. The puzzle gallery / "all possible puzzles"** — **[to build]**
The 16 (plus notable extras) mapped to physical puzzles: Rubik's Cube, Megaminx,
Skewb, Pyraminx, Helicopter, … The finale frames this as *"here are all the twisty
puzzles that can exist"* — under the fenced scope in README's "Scope, honestly":
mechanism-not-exterior, polyhedral-only (no C_n/D_n), exactly one cut per ray, and
**no jumbling / no bandaging**. "All puzzles" = every {ray-set × turning system ×
one-cut depth regime}.
*Teaches:* theory → the shelf. The payoff, and the closest thing to "all possible
mechanisms."

## Notes

- **Folder numbering — deferred renumber (2026-08-03).** The `tutorial_N_*` folders currently
  have gaps: **2** (the jamming rule merged into `tutorial_1_axes/one-cube.html` as Act 2) and
  **4** (poles, unbuilt). Renaming would break already-shared URLs — the
  `tutorial_7_elementary_cut_depths/elementary-piece-explorer.html` link is posted in the
  puzzle-builders Discord. Decision: **leave the numbering alone for now, renumber in the far
  future** (in one pass, once the set of stops is stable).
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
   **backend** (proofs + data generation), HTML as the frontend. `lib/` now holds the
   whole backend; but `raysets.py` and `regime_core.py` still carry **separate** copies
   of the T/O/I construction — unifying them is the one remaining de-dup.
2. **Prose `.md` explainers — fold into HTML** as the stops that host them are built
   (`turning_systems.md`, `what_is_a_turning_system.md`, `cut_depths.md`, `klein.md`).
3. **matplotlib viewers / montages — archive to `old/`** once an HTML stop supersedes
   each: `rayview` → done (stop #3), `polyhedra` → done (stop #5). These two are ready
   to retire now.

**Done (2026-07-27):** the whole Python backend now lives in `lib/` — `raysets.py`,
`turning_systems.py`, `regime_core.py`, and every generator (`gen_turning`,
`gen_systems`, `dump_all_surface`, `precompute_elementary`, `precompute_compound`,
`jsonfmt`, `puzzle_names.json`); the generators write their `*_data.js` into the tutorial
folders. `1_ray_sets`, `2_turning_systems`, `3_cut_depths` removed (montage PNGs → to
`tutorial_3` / `tutorial_5`); prose moved to its stop. matplotlib retired to `old/`.
The cut-depth stop was split: `tutorial_7_elementary_cut_depths/` (exact, 2 views) and
`tutorial_8_compound_cut_depths/` (grid). HTML files renamed to elementary-/compound- .

**Remaining (one de-dup):** `raysets.py` and `regime_core.py` still build T/O/I
separately — now co-located in `lib/`, so unifying them into one group module is a
contained refactor whenever wanted.
