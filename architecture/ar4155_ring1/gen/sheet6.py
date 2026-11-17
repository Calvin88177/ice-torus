"""Sheet 6 - Rodwell zone: site plan (water supply) + Rodwell section schematic."""
import sys, math
from core import SVG, View, num, text, fmt, sector_d, arc_d, radial_d
from plan import defs
import sheetkit as K

DEN = 600
OX, OY = 345.0, 290.0
RINGS = (28.0, 56.0, 84.0)        # axis radii (repo: 28 + n*(16+12))
HALF = 8.0                         # half span of ice foot
B_PIPE = 240.0                     # compass bearing of the buried pipeline (repo: 210 deg math = 240 deg compass)
R_FIELD = 130.0                    # centre of the Rodwell field (proposal)
WATER = '#2b7bb9'


def P(v, R, b):
    return v.P(R, b)


def poly_ring(svg, v, R, fill, stroke, dash=None, op=1.0):
    for b1, b2 in ((0, 180), (180, 360)):
        d = sector_d(v, R - HALF, R + HALF, b1, b2)
        da = f' stroke-dasharray="{dash}"' if dash else ''
        svg.add(f'<path d="{d}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="0.3"{da}/>')


def field_points():
    """4 wells on a short line across the pipe bearing, 30 m apart (proposal)"""
    cx, cy = R_FIELD * math.sin(math.radians(B_PIPE)), R_FIELD * math.cos(math.radians(B_PIPE))
    tx, ty = math.cos(math.radians(B_PIPE)), -math.sin(math.radians(B_PIPE))   # tangential unit (world x east, y north)
    pts = []
    for k, (off, st) in enumerate(((-45, 'cadangan'), (-15, 'aktif'), (15, 'aktif'), (45, 'cadangan'))):
        pts.append((cx + off * tx, cy + off * ty, f'RW{k + 1}', st))
    return (cx, cy), pts


def XY(v, x, y):
    R = math.hypot(x, y)
    b = math.degrees(math.atan2(x, y))
    return v.P(R, b)


def site(svg, v):
    s = v.s
    # terrain
    svg.add(f'<rect x="12" y="46" width="548" height="535" fill="#f7f1e9"/>')
    # ring 1 (built), rings 2-3 (future)
    poly_ring(svg, v, RINGS[0], '#cfe3f2', '#3f74a1')
    for b1, b2, c in ((-5, 5, '#5b5f63'), (115, 125, '#5b5f63'), (235, 245, '#5b5f63')):
        svg.add(f'<path d="{sector_d(v, RINGS[0] - HALF - 1.2, RINGS[0] + HALF + 1.2, b1, b2)}" fill="{c}"/>')
    for R in RINGS[1:]:
        poly_ring(svg, v, R, '#ffffff', '#8aa6bf', dash='3,1.5', op=0.6)
    # gaps = rover roads
    for R in (RINGS[0] + 14, RINGS[1] + 14):
        for b1, b2 in ((0, 180), (180, 360)):
            svg.add(f'<path d="{arc_d(v, R, b1, b2)}" fill="none" stroke="#c9b89c" stroke-width="{num(v.L(6))}" stroke-opacity="0.35"/>')
    # boom reach
    for b1, b2 in ((0, 180), (180, 360)):
        svg.add(f'<path d="{arc_d(v, 95, b1, b2)}" fill="none" stroke="#8c2f14" stroke-width="0.3" stroke-dasharray="1.5,1.2"/>')
    x, y = v.P(95, 300)
    svg.add(text(x - 2, y - 2, 'jangkauan boom ±95 m', size=2.0, anchor='end', fill='#8c2f14', weight=600))
    # tower + buffer tank
    tx, ty = v.P(0, 0)
    svg.add(f'<circle cx="{num(tx)}" cy="{num(ty)}" r="2.2" fill="#3a3a3a"/>')
    svg.add(f'<rect x="{num(tx + 1.5)}" y="{num(ty - 5.5)}" width="{num(v.L(6))}" height="{num(v.L(4))}" fill="#cfe3ee" stroke="#222" stroke-width="0.25"/>')
    svg.add(text(tx, ty + 6.5, 'MENARA POMPA PUSAT (0,0)', size=2.3, weight=800))
    svg.add(text(tx, ty + 9.5, '+ tangki penyangga & pompa (terkubur)', size=1.9, fill=WATER, weight=600))
    # Rodwell field
    (fx, fy), wells = field_points()
    # subsidence buffer around the field
    for wx, wy, lab, st in wells:
        X, Y = XY(v, wx, wy)
        svg.add(f'<circle cx="{num(X)}" cy="{num(Y)}" r="{num(v.L(15))}" fill="#e05a4f" fill-opacity="0.07" stroke="#e05a4f" stroke-width="0.25" stroke-dasharray="1.2,0.8"/>')
    for wx, wy, lab, st in wells:
        X, Y = XY(v, wx, wy)
        svg.add(f'<circle cx="{num(X)}" cy="{num(Y)}" r="{num(v.L(9))}" fill="{WATER}" fill-opacity="0.18" stroke="{WATER}" stroke-width="0.25"/>')
        svg.add(f'<circle cx="{num(X)}" cy="{num(Y)}" r="1.5" fill="{WATER if st == "aktif" else "#ffffff"}" stroke="#123" stroke-width="0.35"/>')
        svg.add(text(X, Y - 3.0, lab, size=2.1, weight=800))
        svg.add(text(X, Y + 4.4, st, size=1.7, fill='#555'))
    # wellhead shelter / heat exchanger skid at field centre (inner side)
    hx, hy = fx * 0.88, fy * 0.88
    X, Y = XY(v, hx, hy)
    svg.add(f'<rect x="{num(X - 4)}" y="{num(Y - 2.6)}" width="8" height="5.2" fill="#ffffff" stroke="#222" stroke-width="0.3"/>')
    svg.add(text(X, Y + 0.7, 'HX', size=1.9, weight=800))
    # manifold from wells to HX
    for wx, wy, lab, st in wells:
        a, b = XY(v, wx, wy), XY(v, hx, hy)
        svg.add(f'<line x1="{num(a[0])}" y1="{num(a[1])}" x2="{num(b[0])}" y2="{num(b[1])}" stroke="{WATER}" stroke-width="0.4" stroke-dasharray="1.5,0.8"/>')
    # buried heated pipeline HX -> tower (along bearing 240, passes under node S3)
    a, b = XY(v, hx, hy), v.P(1.0, B_PIPE)
    svg.add(f'<line x1="{num(a[0])}" y1="{num(a[1])}" x2="{num(b[0])}" y2="{num(b[1])}" stroke="{WATER}" stroke-width="1.1" stroke-dasharray="3,1.2"/>')
    x, y = v.P(70, B_PIPE)
    svg.add(f'<g transform="rotate({num(-30)} {num(x)} {num(y)})"><rect x="{num(x - 34)}" y="{num(y - 5.6)}" width="68" height="4" fill="#f7f1e9"/>'
            + text(x, y - 2.6, 'pipa air terkubur + kabel pemanas (trace heating)', size=2.0, fill=WATER, weight=700) + '</g>')
    x, y = v.P(RINGS[0], B_PIPE)
    svg.add(f'<circle cx="{num(x)}" cy="{num(y)}" r="5.2" fill="none" stroke="#8c2f14" stroke-width="0.35"/>')
    svg.add(text(x + 6, y + 9, 'lintas di bawah node S3', size=1.9, anchor='start', fill='#8c2f14', weight=700))
    svg.add(text(x + 6, y + 11.8, '(rangka kaku, tidak dicor es)', size=1.7, anchor='start', fill='#8c2f14'))
    # reactor (off sheet, break line)
    rx, ry = XY(v, fx * 1.30, fy * 1.30)
    a = XY(v, fx * 1.08, fy * 1.08)
    svg.add(f'<line x1="{num(a[0])}" y1="{num(a[1])}" x2="{num(rx)}" y2="{num(ry)}" stroke="#c0391b" stroke-width="0.6" stroke-dasharray="3,1.2"/>')
    svg.add(f'<path d="M{num(rx-3)},{num(ry-2)} l2,1.5 l-1,1 l3,1.5" fill="none" stroke="#c0391b" stroke-width="0.5"/>')
    svg.add(text(rx - 1, ry + 6, '→ REAKTOR FISI (Flight 1)', size=2.2, anchor='middle', fill='#c0391b', weight=800))
    svg.add(text(rx - 1, ry + 9, 'panas buang → air panas ke sumur', size=1.8, fill='#c0391b'))
    svg.add(text(rx - 1, ry + 11.6, 'jarak & berm perisai belum ditetapkan', size=1.8, fill='#c0391b'))
    # labels for rings
    for R, t in ((RINGS[0], 'CINCIN 1 (R 28 m)'), (RINGS[1], 'cincin 2 (R 56 m, rencana)'), (RINGS[2], 'cincin 3 (R 84 m, rencana)')):
        x, y = v.P(R, 30)
        svg.add(f'<rect x="{num(x-17)}" y="{num(y-2.6)}" width="34" height="3.8" fill="#ffffff" fill-opacity="0.9"/>')
        svg.add(text(x, y + 0.4, t, size=2.0, weight=800 if R == RINGS[0] else 600, fill='#163f66' if R == RINGS[0] else '#5e7a92'))
    for b, t in ((0, 'S1'), (120, 'S2'), (240, 'S3')):
        x, y = v.P(RINGS[0] - HALF - 4, b)
        svg.add(text(x, y + 0.8, t, size=2.0, weight=800, fill='#8c2f14'))
    x, y = v.P(RINGS[0] + 14, 150)
    svg.add(text(x, y, 'jalan rover 12 m', size=1.8, fill='#7a6648'))
    X, Y = XY(v, fx, fy)
    svg.add(text(X - 20, Y + 62, 'ZONA RODWELL', size=4.6, weight=800, fill=WATER, anchor='middle'))
    svg.add(text(X - 20, Y + 67.5, 'R ±130 m · arah 240° (BD) dari menara', size=2.4, fill='#333', anchor='middle'))
    svg.add(text(X - 20, Y + 71.2, 'di luar cincin 3 & jangkauan boom ±95 m', size=2.4, fill='#333', anchor='middle'))
    svg.add(text(X - 20, Y + 74.9, 'lingkaran merah = penyangga ±15 m (bebas bangunan)', size=2.2, fill='#c0391b', anchor='middle'))
    # dimensions
    a, b = v.P(0, 0), v.P(R_FIELD, B_PIPE + 6)
    svg.add(f'<line x1="{num(a[0])}" y1="{num(a[1])}" x2="{num(b[0])}" y2="{num(b[1])}" stroke="#555" stroke-width="0.2" marker-end="url(#arr)"/>')
    m = v.P(R_FIELD * 0.55, B_PIPE + 6)
    svg.add(text(m[0] + 1, m[1] + 4, '±130 m', size=2.0, weight=700, fill='#555'))


def section(svg, x0, y0, w, h):
    """Rodwell schematic section (not to scale)"""
    g = y0 + 14                 # ground
    it = g + 14                 # ice table
    svg.add(f'<rect x="{x0}" y="{y0}" width="{w}" height="{g - y0}" fill="#ffffff"/>')
    svg.add(f'<rect x="{x0}" y="{g}" width="{w}" height="{it - g}" fill="#d9c7ae"/>')
    svg.add(f'<rect x="{x0}" y="{it}" width="{w}" height="{y0 + h - it}" fill="url(#iceSec)"/>')
    svg.add(f'<line x1="{x0}" y1="{g}" x2="{x0 + w}" y2="{g}" stroke="#222" stroke-width="0.4"/>')
    cx = x0 + w * 0.45
    # casing through overburden
    svg.add(f'<rect x="{num(cx - 3)}" y="{g}" width="6" height="{num(it - g + 6)}" fill="#8d939a" stroke="#222" stroke-width="0.3"/>')
    # melt bulb (growing)
    for k, (rw, col, op) in enumerate(((10, WATER, 0.25), (17, WATER, 0.18), (24, WATER, 0.12))):
        cy = it + 26 + k * 7
        svg.add(f'<ellipse cx="{num(cx)}" cy="{num(cy)}" rx="{rw}" ry="{num(12 + k * 6)}" fill="{col}" fill-opacity="{op}" stroke="{WATER}" stroke-width="0.25" stroke-dasharray="{"none" if k == 0 else "1.2,0.8"}"/>')
    # pipes
    svg.add(f'<line x1="{num(cx - 1.2)}" y1="{y0 + 6}" x2="{num(cx - 1.2)}" y2="{num(it + 30)}" stroke="#c0391b" stroke-width="0.7"/>')
    svg.add(f'<line x1="{num(cx + 1.2)}" y1="{y0 + 6}" x2="{num(cx + 1.2)}" y2="{num(it + 40)}" stroke="{WATER}" stroke-width="0.7"/>')
    svg.add(f'<rect x="{num(cx - 7)}" y="{y0 + 2}" width="14" height="6" fill="#ffffff" stroke="#222" stroke-width="0.3"/>')
    svg.add(text(cx, y0 + 6, 'kepala sumur', size=1.6, weight=700))
    svg.add(f'<circle cx="{num(cx + 1.2)}" cy="{num(it + 41)}" r="1.4" fill="#123"/>')
    lab = [(g + 7, 'lapisan penutup regolit (overburden) — dibor & di-casing'),
           (it + 4, 'muka es tanah (ice table)'),
           (it + 22, 'air panas disemprot → es meleleh'),
           (it + 34, 'kolam air leleh (bulb) membesar tiap hari'),
           (it + 43, 'pompa submersibel → air ke permukaan'),
           (y0 + h - 4, 'es tanah Utopia Planitia (dengan debu/perklorat)')]
    for yy, t in lab:
        svg.add(f'<line x1="{num(cx + 27)}" y1="{num(yy - 0.7)}" x2="{num(x0 + w * 0.70)}" y2="{num(yy - 0.7)}" stroke="#888" stroke-width="0.15"/>')
        svg.add(text(x0 + w * 0.71, yy, t, size=2.1, anchor='start', fill='#222'))
    svg.add(text(cx - 3, y0 + 11.5, 'merah = air panas masuk · biru = air leleh keluar', size=1.6, anchor='end', fill='#555'))
    svg.add(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" stroke="#151515" stroke-width="0.3"/>')


def build(path):
    svg = SVG(K.W, K.H)
    v = View(DEN, OX, OY, 0)
    defs(svg, v.s)
    svg.d('<pattern id="iceSec" patternUnits="userSpaceOnUse" width="3" height="3" patternTransform="rotate(45)">'
          '<rect width="3" height="3" fill="#e3eef7"/><line x1="0" y1="0" x2="0" y2="3" stroke="#a9c6de" stroke-width="0.3"/></pattern>')
    K.frame(svg)
    site(svg, v)
    K.header(svg, 6, 'ZONA RODWELL — SUMBER AIR',
             'DENAH TAPAK: SUMUR RODWELL, REAKTOR, PIPA KE MENARA POMPA · CINCIN 1–3', 'SKALA 1 : 600')
    K.north_arrow(svg, 34, 72, -90, size=8)
    K.scale_bar(svg, 22, 570, v.s, ticks=(0, 10, 20, 50, 100), label='skala grafis 1:600 (m)')

    x0, x1 = 574.0, 829.0
    K.section_heading(svg, x0, 56, 'POTONGAN SKEMATIK SUMUR RODWELL (tanpa skala)', 2.9)
    section(svg, x0, 61, x1 - x0, 120)
    y = 196
    K.section_heading(svg, x0, y, 'ALIRAN AIR', 2.9)
    steps = ['1  Reaktor → panas buang memanaskan air injeksi (HX di tepi zona sumur)',
             '2  Air panas disemprot di dasar sumur → es tanah meleleh, kolam (bulb) membesar',
             '3  Pompa submersibel mengangkat air → manifold → HX',
             '4  Pipa terkubur ber-trace heating ±130 m → tangki penyangga di kaki menara',
             '5  Riser menara → boom ±95 m → selang ke bekisting (cor cangkang es)',
             '6  Tahap huni: cabang ke ECLSS A (Arch 1) lewat node S3 → air minum & O₂']
    K.para(svg, x0, y + 6.5, steps, size=2.3, lh=1.6)
    y += 6.5 + 6 * 2.3 * 1.6 + 6
    K.section_heading(svg, x0, y, 'DATA DARI REPO ice-torus', 2.9)
    cols = [('PARAMETER', 120, 'start'), ('NILAI', 135, 'start')]
    rows = [('Kebutuhan air pengecoran', '±25 t/hari (6 set bekisting)'),
            ('Air per arch', '±35 t'),
            ('Siklus beku per set', '±5–8 hari → ±8 hari'),
            ('Lama pengecoran cincin 1 · 2 · 3', '±3 · 6,5 · 9,5 bulan'),
            ('Sumber panas', 'panas buang reaktor fisi'),
            ('Flight 1', 'hanya reaktor + sumur Rodwell'),
            ('Mau lebih cepat?', 'tambah set bekisting + sumur')]
    from sheet4 import table
    y = table(svg, x0, y + 6, cols, rows, size=2.3, row_h=4.6) + 6
    K.section_heading(svg, x0, y, 'KETENTUAN ZONA (USULAN)', 2.9)
    notes = ['Zona sumur di luar cincin 3 (R ≥ ±110 m) & di luar jangkauan boom: rongga leleh',
             'tidak boleh berada di bawah cangkang es atau jalur rover (risiko amblas).',
             'Radius penyangga ±15 m per sumur (lingkaran merah putus-putus) — bebas bangunan.',
             '2 sumur aktif + 2 cadangan, jarak ±30 m; sumur baru dibor saat bulb terlalu dalam.',
             'Arah 240° (BD) sesuai jalur pipa di repo; pipa melintas di bawah node S3 yang tidak',
             'dicor es, sehingga cangkang es arch tidak dibongkar.',
             'Belum ditentukan: kedalaman es & tebal overburden di tapak (data SHARAD), jarak',
             'aman reaktor, dan pengolahan debu/perklorat sebelum air dipakai ECLSS.']
    K.para(svg, x0, y + 6.5, notes, size=2.2, lh=1.6, bullet=False)
    K.title_block(svg, 646, 525, 183, 57, 6, 'Zona Rodwell — denah tapak sumber air & potongan skematik sumur', '1 : 600 · potongan tanpa skala')
    svg.save(path, 'Lembar 6 - Zona Rodwell')


if __name__ == '__main__':
    build(sys.argv[1])
