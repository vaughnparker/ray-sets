# TODO

Working list. The *why* behind these lives in [`tutorial_plan.md`](tutorial_plan.md) —
that file holds the curriculum ("The reader's path") and is the source of truth for scope
decisions. This file is just the queue.

Last reviewed: 2026-08-24.

---

## Next up

- [ ] **Write `tutorial_4_why_only_three/from_groups_to_raysets.md`** — the second half of
      stop 4: 3 symmetry families × 3 pole families = 9 candidate ray-sets, minus 2
      coincidences = **7 elementary**. The two coincidences, both verified numerically:
      - tetrahedron **edges** = cube **faces** (both are ±x, ±y, ±z)
      - tetrahedron **faces** = mirror image of tetrahedron **corners** (so "tetra faces"
        never appears as its own ray-set)
      Small, fully verified, and it closes the 3 broken links below. Highest value per hour.

- [ ] **Decide how stop 4 gets its visualization.** The prose is written; the interactive
      is not. Options: build one here, or link out to the sibling `every-way-to-spin`
      project, which already covers this theorem in depth. Decide before investing.

## The spine

Acts I–III are built. What remains:

- [ ] **The finale — the periodic table of the 91 elementary puzzles.** The thing the whole
      spine walks toward. Elementary only, by decision: compound, reductions and
      body-realizability all stay in the appendix so the table reads cleanly.
      (63 robust + 28 zero-width = 91.) Visualization ideas pending.
- [ ] **Act III hand-off paragraph.** Act III must end by telling the reader that 9 more
      ray-sets exist whose rays come in two families, each with its own depth — otherwise
      someone told "16 ray-sets" is silently shown only 7. Points at the appendix.
- [ ] **Turn `index.html` from a menu into a narrative.** It currently hands over cards
      instead of telling the story that makes a reader *want* the next chapter.
- [ ] **Group the appendix pages under their own heading in `index.html`,** clearly marked
      optional, so they don't read as part of the spine.

## Explorer polish

- [ ] **Fold `elementary-piece-explorer.html`'s missing features into
      `elementary-explorer.html`** — this is the stated condition for retiring the older page:
      - puzzle names (18 named entries sit unused in `surface_data.js` — Radio Fathom,
        Radio Nebula, …). Biggest gap: it's the bridge from "regime #7" to a real puzzle.
      - the jump table (clickable list of every config)
      - skip ◀ / ▶ to the next/previous config
      - the "EXACT" badge; line-width control

## Naming and validation

Two community sources added to [`resources.md`](resources.md) on 2026-08-24 are more than
reference material — they name and independently derive things this project currently shows
as bare numbers.

- [ ] **Adopt the external vocabulary.** Replace "regime #7" and "weight 3" with names people
      already use:
      - **[Hypercubing's cut-depths table](https://hypercubing.xyz/theory/cut-depths/)** gives
        each depth range an exact interval plus a reference puzzle (Tetraminx, Megaminx,
        Pyraminx Crystal, Starminx, …).
      - **Tetra55's Radiolarian census** names 18 piece types on a systematic
        shallow / deep / super-deep / super-super-deep scheme, across middle centers, vertices,
        midges, wings, x-centers and oblique centers.
      Feeds directly into the puzzle-names item above.

- [ ] **Cross-check `surface_data.js` against Tetra55's census.** It is a hand-derived
      piece-type table for R1.5 → R15 — the first external data granular enough to actually
      falsify this repo's computed histograms, and it was produced independently (two people,
      two charts, cross-verified). A clean match would be strong validation.
      - It also confirms non-monotonicity by hand: R9 loses pieces as cuts merge at the face
        centres, R11 at the vertices — i.e. this project's critical depths, observed by eye.
      - Known soft spots *in their table*, if a discrepancy shows up: the R8x vs "Radio
        Victoria" naming disagreement, and a "2nd deep x-centers" type the author later
        conceded does not exist.

## Appendix (all unbuilt)

- [ ] **The body matters** — which puzzles are physically buildable; why some 20-axis
      puzzles have no face-turning-icosahedron form and exist only as corner-turning
      dodecahedra.
- [ ] **The families that never stop (C_n / D_n)** — where "16" stops counting.
- [ ] **Reductions (~2^k)** — each canonical puzzle blossoming into its family of
      orbit-hidings (edge-only cube, corners-only, …), plus the dual direction
      (super/picture cube).
- [ ] **Compound systems narrative** — `tutorial_8_compound_cut_depths/` has three working
      pages but no framing.

## Known issues

- [ ] **3 broken links on GitHub**, all pointing at the unwritten `from_groups_to_raysets.md`:
      `tutorial_4_why_only_three/README.md:12`, `why_only_three.md:7`, `why_only_three.md:313`.
      Fixed by writing that file.
- [ ] **`why_only_three.md` rests on one unproved assumption** (that the poles always tile
      the sphere into identical triangles). It is flagged honestly in the text; `klein.md`
      is kept as the airtight alternative. No action required — just don't let it get
      quietly dropped.

## Deferred on purpose

- **Folder renumbering.** `tutorial_N_*` has a gap at 2 (the jamming rule merged into
  `tutorial_1_axes`). Renaming breaks already-shared URLs — a `tutorial_7_…` link is posted
  in the puzzle-builders Discord — and folder paths get no redirect. Do it in one pass, if
  ever, once the set of stops is stable.
- **The compound count.** ~1000 is still a guess; the `--all` runs are multi-week. Since
  compound moved to the appendix and the finale is elementary-only, this **blocks nothing**.
  The exact 91 carries the headline.
- **`lib/` de-duplication.** `raysets.py` and `regime_core.py` still build T/O/I separately.
  Now co-located, so unifying them is a contained refactor whenever wanted.
