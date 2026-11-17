# Ring 1 architectural drawings (ITB AR4155, Group 7)

Architectural development of **Ring 1** for the ITB course *AR4155 Arsitektur Antariksa — "Membuat Hunian di Mars"*.
Site: Utopia Planitia (39.95° N, 80.30° E). Drawings are in Indonesian, on six A1 sheets.

**Status:** concept design, not for construction. Geometry follows the repo baseline (axis radius 28 m, 16 m span, 9 m rise,
0.60 m ice, 0.10 m CO₂ gap, double inflatable membrane).

| Sheet | Content | Scale |
| --- | --- | --- |
| 1 | Arch 1 ground floor plan ±0.00 (cut at +1.20), room schedule, legend | 1:100 |
| 2 | Arch 1 mezzanine +3.00, 1:50 cabin details | 1:100 / 1:50 |
| 3 | Sections A–A (cabins, mezzanine, corridor) and B–B (stepped: plaza void, galley, hydroponics); details of the ice foot, wall layers, and the arch-membrane-to-node joint | 1:50 / 1:20 / 1:5 |
| 4 | Full Ring 1 (72 modules): Arch 1 Core, Arch 3 Grow & Make, Arch 2 Living, connectivity, capacity, phasing | 1:150 |
| 5 | Wellness zones (overlay) | 1:150 |
| 6 | Rodwell zone: site plan of the water supply and a schematic well section | 1:600 |

Files: [`drawings/`](drawings) (combined PDF + one SVG per sheet, Inter font embedded for browsers).

## Ring 1 layout used here

72 modules × 5.0° (≈2.44 m on the axis):

| Part | Bearing (clockwise from N) | Modules | Role |
| --- | --- | --- | --- |
| S1 | −5° to 5° | 2 | node: main EVA suit-lock + cargo/rover airlock |
| Arch 1 · Core | 5° to 115° | 22 | technical, ECLSS, control, lab, clinic, safe room (15), galley, plaza, gym, hydroponics, 12 cabins |
| S2 | 115° to 125° | 2 | node: pressure buffer, main utility shaft |
| Arch 3 · Grow & Make | 125° to 235° | 22 | vertical farms, food processing, bioreactor, water/nutrient recycling, fabrication |
| S3 | 235° to 245° | 2 | node: pressure buffer, backup EVA airlock |
| Arch 2 · Living | 245° to 355° | 22 | 48 cabins on two storeys, sanitation, hall, café, library, plaza |

- Nodes are rigid frames, not cast in ice, covered with regolith bags; each arch has its own membrane tube and CO₂ pocket clamped to the node frame. Two 1.20 m pressure hatches per node, so any arch can be isolated.
- Corridor 3.60 m clear and continuous for 360°; cabins ≥ 2.40 × 3.00 m (smallest 7.8 m²); clear height ≥ 2.40 m to x = ±6.25 m; spiral stairs Ø1.50 in recesses off the corridor.
- Ring 1 total: 60 cabins, 50–60 people, ≈ 2,340 m² floor area.

**Not yet reconciled with the engineering baseline:** this 3-arch / 3-node split of Ring 1 differs from the portal/compartment
count used in the formwork and abstract work (4 compartments in the inner ring). The Rodwell field position on sheet 6
(≈130 m at 240°, 4 wells, 15 m buffers) is a layout proposal; only the pipeline bearing comes from `scripts/torus_3d.py`.

Open items noted on the sheets: solar-storm shelter for 50–60 people (the safe room holds 15), site ice depth and overburden
(SHARAD), reactor stand-off distance, dust/perchlorate treatment of meltwater.

## Rebuild

```bash
pip install fonttools          # plus librsvg (rsvg-convert) and the Inter font
./build.sh
```

The generators are plain Python that write SVG: `core.py` (geometry, view transform), `plan.py` / `furn.py` (walls, doors,
furniture), `arch1.py` and `ring.py` (room programmes), `section.py`, `sheet1.py`–`sheet6.py` (one per sheet).
