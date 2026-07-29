"""Emit turning_data.js for the interactive turning-system viewer (tutorial stop #6).

For each of the 16 ray-sets, writes its rays (with family index) and every valid
turning system on it — a per-ray turn order `nu`, the generated group order |G|, and
a name for the famous ones. The enumeration is `turning_systems.systems_on`; this file
only packages its output for the browser.  Names match tutorial_7_elementary_cut_depths/systems_data.js.

    python gen_turning.py        # -> turning_data.js
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import raysets                                                   # noqa: E402
import turning_systems as tsy                                    # noqa: E402

# the viewer that consumes this data lives one level up, in the tutorial folder
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "tutorial_6_turning_systems", "turning_data.js")

# ray-set key (shape + family labels) -> friendly name used by the other viewers
FRIENDLY = {
    "T 4a": "Tetrahedron - corners (Pyraminx)",
    "T 4a+6": "Tetrahedron - corners + edges",
    "O 6": "Cube - faces (Rubik's Cube)",
    "O 8": "Cube - corners (Skewb)",
    "O 12": "Cube - edges (Helicopter)",
    "O 6+8": "Cube - faces + corners",
    "O 6+12": "Cube - faces + edges",
    "O 8+12": "Cube - corners + edges",
    "O 6+8+12": "Cube - faces + corners + edges",
    "I 12": "Dodecahedron - faces (Megaminx)",
    "I 20": "Dodecahedron - corners (Radiolarian)",
    "I 30": "Dodecahedron - edges",
    "I 12+20": "Dodeca - faces + corners",
    "I 12+30": "Dodeca - faces + edges",
    "I 20+30": "Dodeca - corners + edges",
    "I 12+20+30": "Dodeca - faces + corners + edges",
}

# the three turning systems that share O's 6 face-rays are genuinely different puzzles
NAMES = {
    ("O 6", (("6", (4,)),)): "3x3x3 Rubik's Cube",
    ("O 6", (("6", (2, 4)),)): "3x3x2 Domino",
    ("O 6", (("6", (2,)),)): "Tetrahedral edge-turning cube",
}


def keyof(rs):
    return f"{rs.shape} " + "+".join(rs.labels)


def orders_by_family(rs, nu):
    """[(family label, sorted distinct turn orders), ...] in ray order."""
    out, at = [], 0
    for label, fam in zip(rs.labels, rs.families):
        vals = tuple(sorted({nu[at + i] for i in range(len(fam))}))
        out.append((label, vals))
        at += len(fam)
    return out


def main():
    sets = raysets.build()
    kept, _ = raysets.collapse(sets)

    out = {}
    for i in kept:
        rs = sets[i]
        R = raysets.rays(rs)
        fam = [f for f, famrays in enumerate(rs.families) for _ in range(len(famrays))]

        systems = []
        for nu, G in tsy.systems_on(rs):
            obf = orders_by_family(rs, nu)
            systems.append({
                "nu": [int(x) for x in nu],
                "G": int(G),
                "name": NAMES.get((keyof(rs), tuple(obf))),
                "orders": [{"label": lab, "vals": list(vals)} for lab, vals in obf],
            })
        systems.sort(key=lambda s: -s["G"])          # fullest puzzle first (default)

        out[FRIENDLY[keyof(rs)]] = {
            "shape": rs.shape,
            "rays": [[round(float(x), 6) for x in r] for r in R],
            "fam": fam,
            "labels": list(rs.labels),
            "systems": systems,
        }

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("const TURNING = " + json.dumps(out, indent=2, ensure_ascii=False) + ";\n")

    total = sum(len(v["systems"]) for v in out.values())
    print(f"{len(out)} ray-sets  ->  {total} turning systems; wrote turning_data.js")


if __name__ == "__main__":
    main()
