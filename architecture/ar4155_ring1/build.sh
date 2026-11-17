#!/usr/bin/env bash
# Regenerate the six A1 sheets (SVG), the combined PDF, and font-embedded SVGs.
# Needs: python3, pymupdf not required; rsvg-convert (librsvg), fonttools, and the Inter font installed.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/drawings"; TMP="$(mktemp -d)"
cd "$HERE/gen"
for i in 1 2 3 4 5 6; do python3 "sheet$i.py" "$TMP/raw$i.svg"; done
rsvg-convert -f pdf -o "$OUT/Mars_IceArch_Torus_AR4155_K7_Lembar1-6.pdf" "$TMP"/raw{1,2,3,4,5,6}.svg
names=(Lembar1_Denah_Lantai_Dasar_Arch1 Lembar2_Denah_Mezanin_Arch1 Lembar3_Potongan_AA_BB_Detail \
       Lembar4_Denah_Cincin1_Penuh Lembar5_Zona_Wellness_Cincin1 Lembar6_Zona_Rodwell)
for i in 1 2 3 4 5 6; do python3 embed_fonts.py "$TMP/raw$i.svg" "$OUT/${names[$((i-1))]}.svg"; done
echo "Written to $OUT"
