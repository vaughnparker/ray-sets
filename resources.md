# Other resources

External references on twisty puzzles and their axis systems.

- **[Twisty Puzzles catalogue](https://twisty-puzzles.weebly.com/single-cut.html)** — by Maido Remm.
  A catalogue attempting to list every non-shape-shifting Platonic-solid twisty puzzle,
  organised by number of layers.
  - Now split into separate pages for **2-layer**, **3-layer**, and **more-than-3-layer** puzzles.
  - The author's counts: **13 two-layer** (deep-cut) puzzles and **160 three-layer** (single-cut) puzzles.
  - "Single cut" means the polyhedron is cut once per semi-axis, giving 3 layers.
  - The 160 single-cut puzzles by solid: 6 tetrahedra, 11 hexahedra, 15 octahedra, 61 dodecahedra, 67 icosahedra.
  - Classified by turning axis (face / corner / edge) and cut depth in degrees, with ID codes like `4F150` (shape + axis + degree). Each entry lists names, images, inventor, and year.

- **[Puzzle Forge](https://www.puzzleforge.com/wp/)** — the design blog of Jason Smith.
  A portfolio (roughly 2007–2016) documenting his original twisty-puzzle designs, prototyping, and mechanisms.
  - Inventor of the **Radiolarians** series of face-turning icosahedra — the `I · 20` ray-set in this repository.
  - Also covers many other designs: the Petaminx, Icosamate, Rhombicultimate, Ghost Cube, and the recurring "skirting rails" mechanism, among others.
  - Strong emphasis on the mechanical engineering of new puzzles rather than cataloguing existing ones.

- **["The Radiolarian family"](https://www.reddit.com/r/twistypuzzles/comments/1ndwrh2/the_radiolarian_family/)** — a guide on r/twistypuzzles.
  A walkthrough of the 15 Radiolarians — Jason Smith's face-turning icosahedra (the `I · 20` ray-set) — with Twizzle Explorer links to play each in a simulator.
  - Effectively a **cut-depth ladder for one ray-set**: Radiolarian 1 is a shallow face cut, and each successive number cuts deeper, ending at Radiolarian 15 — the deepest cut, straight through the centre (depth 0, each turn moves half the puzzle). Directly relevant to [`tutorial_7_elementary_cut_depths`](tutorial_7_elementary_cut_depths).
  - Distinguishes two kinds of cut: **Type A** (a depth where pieces *appear* — imprecise, the exact value doesn't matter) and **Type D** (a depth where pieces *disappear* — a precise critical depth, usually irrational). This is the same appear/disappear distinction that a cut-depth phase diagram computes.
  - Lists exact critical depths for the Type-D cuts, several golden-ratio-flavoured — e.g. Radiolarian 4 = Eitan's Star at $(\sqrt5-1)/2$, Radiolarian 2 at $\sqrt5/3$, Radiolarian 9 at $1/3$.
  - Notes the 15 are a deliberately chosen subset, not every face-turning icosahedron (intermediate ones like "4.5" and "8.5" exist).

- **[VeryPuzzle — CORD and DIRT explained](https://www.verypuzzle.com/other/cord-and-dirt-explained/)** — by VeryPuzzle.
  A classification of twisty puzzles by axis system, closely parallel to this repository's ray-sets. Two master bundles, each three axis systems built from arrows on a cube or a dodecahedron:
  - **CORD** on the cube: **C** = face centres (`O · 6`), **O** = corners / octahedron faces (`O · 8`), **RD** = edge centres / rhombic-dodecahedron faces (`O · 12`).
  - **DIRT** on the dodecahedron: **D** = face centres (`I · 12`), **I** = corners / icosahedron faces (`I · 20`), **RT** = edge centres / rhombic-triacontahedron faces (`I · 30`).
  - Makes the same duality point this repo does — building the same bundles from dual solids yields nothing new — so these two families cover essentially all axis systems.
  - Compact puzzle codes: 3×3×3 = `C5`, Megaminx = `D5`, Helicopter Cube = `RD6`, Dino Cube = `O6`, Penultimate = `D12`, Big Chop = `RT56`.
  - Each axis system has a page of "**fundamental models**" — its cut-depth variants — with counts C **6**, O **8**, RD **14**, D **12**, I **24**, RT **56**. Per-system pages: [C-models](https://www.verypuzzle.com/other/c-models/), [I-models](https://www.verypuzzle.com/other/i-models/).
  - Those model counts are cut-depth regime counts, and they run **higher than what this project's cut-depth analysis expects** (e.g. face-turning cube `O · 6`: 6 here vs ~4; face-turning icosahedron `I · 20`: 24 here vs ~13). Reconciling the difference is a task for [`tutorial_7_elementary_cut_depths`](tutorial_7_elementary_cut_depths).

- **[Sphere cut visualizer](https://www.jaapsch.net/puzzles/sphere.htm)** — by Jaap Scherphuis (© 2003, 2018).
  An interactive tool showing a sphere with symmetric cut planes — essentially the same idea as this repository's [`tutorial_7_elementary_cut_depths`](tutorial_7_elementary_cut_depths), built roughly twenty years earlier.
  - Drag to rotate; per-family colour sliders adjust **cut depth**, and pushing a slider all the way removes that family's cuts.
  - Switchable between tetrahedral, octahedral, icosahedral and other symmetries; demonstrates puzzles from the 2×2×2 up to the Megaminx, Dogic, Alexander's Star, and Impossiball.
  - Shareable URLs encode a chosen configuration.

- **[LudoMiloOrb cut-depth explorer](https://ludocrypt.github.io/LudoMiloOrb/)** — by ludocrypt.
  An interactive sphere-with-cut-planes explorer, the same core idea as this repository's
  [`tutorial_7_elementary_cut_depths`](tutorial_7_elementary_cut_depths) — vary the cut depth and
  watch the piece configuration change.

- **[Group Theory for Puzzles](https://www.jaapsch.net/puzzles/groups.htm)** — by Jaap Scherphuis.
  A full group-theory course aimed at puzzles, whose classification proof closely parallels this repository's [`klein.md`](klein.md).
  - Its Theorem 6.6 classifies the finite 3-D rotation groups (cyclic, dihedral, tetrahedral, octahedral, icosahedral) by **pole counting**, exactly the argument in `klein.md`.
  - Reaches the same governing equation, $2(1 - 1/N) = \sum_i (1 - 1/k_i)$ — identical to `klein.md`'s $\sum_i (1 - 1/n_i) = 2 - 2/N$ — via the Orbit-Counting Theorem (Burnside's lemma), where `klein.md` instead does the counting by an elementary "bins" argument to avoid the machinery.

- **[Rob's Puzzle Page — rearrangement puzzles](https://www.robspuzzlepage.com/rearrangement.htm)** — by Rob (a collector).
  A large personal reference catalogue of twisty and rearrangement puzzles, spanning commercial releases and custom designs.
  - Organised by shape (tetrahedral, cubic, octahedral, dodecahedral, icosahedral, spherical, …), turning mechanic (face / vertex / edge / hybrid), order, and cutting style.
  - Covers the Rubik's Cube and hundreds of variants, with photos, patent references, solutions, and historical notes.
  - A collector's/curator's survey rather than a mathematical classification — useful for putting names and history to the puzzles the axis systems here describe.
