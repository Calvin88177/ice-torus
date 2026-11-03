# Ice Torus

**Ice as the concrete of space.** Design studies for habitats whose structure and radiation shield are made of water ice, frozen in place inside inflatable bag-moulds.

The project started as a Mars surface habitat: concentric ring vaults of ice built around a central robotic pumping tower in Arcadia Planitia. The same material system extends to rotating stations in orbit, where fibre-reinforced, prestressed ice can carry spin loads.

![Concentric torus habitat](figures/T1_torus_3d.png)

## Core ideas

- **Water is the material.** It is the best radiation shield per kilogram (hydrogen-rich, few secondary particles), it is cast like concrete, and in the shade of space or on Mars, freezing it costs almost nothing.
- **Shape it to be squeezed.** Ice is strong in compression (crushes above ~5 MPa) but cracks at ~1 MPa in tension. Catenary arches keep it in pure compression.
- **Keep it cold.** Creep, not melting, limits the structure. Insulation sits *between* the warm habitat and the ice, so the ice stays at about −50 °C or colder.
- **Prestress it for spin.** In a rotating ring, carbon-fibre hoops tensioned after freezing pre-squeeze the ice, so at full spin the ice sits at zero stress. For a 224 m ring at 1 g the fibre is under 0.5% of the ice mass.

## Figures

| File | Content |
| --- | --- |
| `T1_torus_3d` | Concentric ring habitat with the central pumping tower |
| `T2_section_plan` | Section through the tower and plan of three rings |
| `T4_arch_options` | Precast vs. cast-in-place whole arches |
| `T5_travelling_formwork` | Travelling formwork, water-only filling, freeze cycle |
| `T6_compass_cables` | Guiding formwork with cables from the tower base |
| `T7_leapfrog_rails` | Split formwork and leapfrog rails |
| `ice_properties` | Ice as insulation, radiation shield and structure |
| `Y1_prestressed_ice` | Why plain ice fails in a spinning ring, and how prestressing fixes it |
| `Y2_icering1` | IceRing-1: a small-satellite test of prestressed ice in orbit |

## Structural analysis

`analysis/structural_integrity_EN.pdf` checks ice vaults of 16–40 m span on Mars: compressive stress, Glen-law creep over 30 years, creep buckling, heat flow from the habitat, and inner-surface melting.

| Span | Ice thickness | Max. stress | Buckling FS |
| --- | --- | --- | --- |
| 16 m | 0.6 m | 46 kPa | 23.6 |
| 24 m | 0.6 m | 69 kPa | 3.3 |
| 32 m | 1.25 m | 92 kPa | 2.6 |
| 40 m | 3.4 m | 115 kPa | 2.5 |

All numbers are concept-level estimates; see the report's limitations section.

## Reproduce

```bash
pip install -r requirements.txt
python scripts/run_all.py                     # all figures -> figures/
cd analysis && latexmk -pdf structural_integrity_EN.tex
```

## Status

Concept stage. Next steps: a tabletop freeze-forming test, then a cold spin rig for fibre-prestressed ice rings.

## Origin

The Mars ring-habitat concept was developed in the ITB course AR4155 *Topik Khusus E: Arsitektur Antariksa* (Space Architecture).
