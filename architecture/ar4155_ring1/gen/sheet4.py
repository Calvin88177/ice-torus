"""Sheet 4 - Full Ring 1 plan (Permanent Settlement), 1:150, A1, + Arch 2 mezzanine inset 1:300."""
import math, sys
from core import SVG, View, R0, num, text, fmt, arc_d, radial_d, sector_d, upright, cut_widths, X_CORR, esc
from plan import defs, room_tag, ang_of, ZONE, HATCH_C
from furn import Ctx
import furn as F
import arch1
import ring
import sheetkit as K

DEN = 150
OX, OY = 300.0, 316.0
CX0, CX1 = 574.0, 829.0          # right column


def module_ring(ctx, R_tick=(36.15, 36.65), R_lab=37.2, size=1.6):
    v, svg = ctx.view, ctx.svg
    for k in range(72):
        b = 5 * k
        if b in (0, 120, 240):
            continue
        svg.add(f'<path d="{radial_d(v, b, R_tick[0], R_tick[1])}" stroke="#555" stroke-width="0.16" fill="none"/>')

    def put(bm, lab, bold=False, sz=size, R=R_lab):
        x, y = v.P(R, bm)
        (tx, ty), _ = v.dirs(bm)
        ang = upright(math.degrees(math.atan2(ty, tx)))
        svg.add(text(x, y + sz * 0.35, lab, size=sz, weight=800 if bold else 600,
                     fill='#8c2f14' if bold else '#666', rot=ang))
    for bm, lab in ((-3.0, 'S1'), (120.0, 'S2'), (240.9, 'S3')):
        put(bm, lab, True, 2.1, R=38.05)
    for a0 in (5, 125, 245):
        for k in range(22):
            put(a0 + 5 * k + 2.5, f'M{k + 1}')


def tagc(ctx, R, b, code, name=None, r_mm=1.95, size=1.95, name_size=1.5, fill='#ffffff'):
    room_tag(ctx, R, b, code, None, name, r_mm=r_mm, size=size, name_size=name_size, fill=fill)


def small_tag(svg, x, y, code, r=1.75, size=1.7):
    svg.add(f'<circle cx="{num(x)}" cy="{num(y)}" r="{num(r)}" fill="#ffffff" stroke="#222" stroke-width="0.2"/>')
    svg.add(text(x, y + size * 0.36, code, size=size if len(code) < 3 else size * 0.82, weight=800))


def name_box(ctx, R, b, code, name, size=1.9):
    v, svg = ctx.view, ctx.svg
    x, y = v.P(R, b)
    (tx, ty), _ = v.dirs(b)
    ang = upright(math.degrees(math.atan2(ty, tx)))
    w = len(name) * (size * 0.64 + 0.15) + 8.0
    svg.add(f'<g transform="rotate({num(ang)} {num(x)} {num(y)})">'
            f'<rect x="{num(x - w / 2)}" y="{num(y - 2.6)}" width="{num(w)}" height="5.2" rx="2.6" fill="#ffffff" fill-opacity="0.92" stroke="#4f8a3c" stroke-width="0.25"/>'
            f'<circle cx="{num(x - w / 2 + 2.6)}" cy="{num(y)}" r="1.95" fill="#ffffff" stroke="#222" stroke-width="0.22"/>'
            + text(x - w / 2 + 2.6, y + 0.65, code, size=1.8, weight=800)
            + text(x - w / 2 + 5.6, y + 0.68, name, size=size, anchor='start', weight=800, fill='#2f5f22', ls='0.15') + '</g>')


def tags_ring(ctx, g1, g3, g2):
    v, svg = ctx.view, ctx.svg

    def at(band, x, b):
        return (R0 + x if band == 'O' else R0 - x), b
    # ---- Arch 1 (positions from sheet 1, short names)
    A1 = [('01', 'I', 3.3, 8.2, 'Dekon'), ('02', 'O', 3.3, 10.6, 'Gudang'), ('03', 'I', 2.9, 16.0, 'Bengkel'),
          ('04', 'O', 3.0, 27.0, 'ECLSS A'), ('05', 'I', 2.8, 27.6, 'ECLSS B'), ('06', 'O', 2.75, 41.0, 'Kontrol'),
          ('07', 'O', 2.45, 44.8, 'Lab'), ('08', 'I', 2.65, 42.4, 'Klinik'), ('09', 'I', 2.35, 45.9, 'Isolasi'),
          ('10', 'I', 2.75, 54.4, 'Safe room'), ('11', 'O', 2.5, 57.8, 'Galley'), ('12', 'O', 2.45, 71.4, 'Makan'),
          ('13', 'I', 2.35, 61.5, 'Plaza'), ('14', 'O', 2.45, 80.3, 'Gym'), ('15', 'I', 2.35, 79.3, 'Hidroponik'),
          ('16', 'O', 3.25, 89.3, 'Sanitasi'), ('17', 'I', 2.4, 86.5, None)]
    for code, band, x, b, nm in A1:
        R, bb = at(band, x, b)
        tagc(ctx, R, bb, code, nm)
    # ---- Arch 3
    A3 = [('G1', 'O', 2.9, 128.6, 'Pantry'), ('G3', 'O', 2.75, 181.6, 'Dapur prod.'),
          ('G4', 'O', 3.15, 197.4, 'Bioreaktor'), ('G5', 'O', 3.75, 212.6, 'Fabrikasi'), ('G6', 'O', 3.5, 227.5, None),
          ('G7', 'O', 2.55, 232.5, None), ('G8', 'I', 2.75, 128.0, 'Bank benih'),
          ('G10', 'I', 2.45, 180.6, 'Lab pangan'), ('G11', 'I', 3.4, 191.0, 'Daur air'),
          ('G12', 'I', 3.55, 210.5, 'Daur material'), ('G13', 'I', 2.6, 224.0, 'Istirahat'), ('G14', 'I', 2.5, 231.6, None)]
    for code, band, x, b, nm in A3:
        R, bb = at(band, x, b)
        tagc(ctx, R, bb, code, nm)
    # big room names (vertical farms): label boxes over the rack field
    for band, b, code, s_ in (('O', 155.0, 'G2', 'RUANG TANAM A · KEBUN VERTIKAL LED'),
                              ('I', 155.0, 'G9', 'RUANG TANAM B · KEBUN VERTIKAL LED')):
        R, bb = at(band, 4.05 if band == 'O' else 3.9, b)
        name_box(ctx, R, bb, code, s_)
    # ---- Arch 2
    A2 = [('L1', 'O', 2.6, 293.0, 'Aula & kelas'), ('L2', 'O', 2.6, 301.6, 'Kafe'), ('L3', 'I', 3.45, 296.9, 'Perpustakaan'),
          ('L4', 'I', 2.6, 301.2, 'Plaza'), ('L5', 'O', 2.75, 286.6, 'Sanitasi A'), ('L6', 'I', 3.1, 246.7, None),
          ('L7', 'O', 2.75, 313.4, 'Sanitasi B'), ('L8', 'I', 3.1, 353.3, None)]
    for code, band, x, b, nm in A2:
        R, bb = at(band, x, b)
        tagc(ctx, R, bb, code, nm)
    # cabins (ground)
    for gg, keys in ((g1, ('K1', 'K2', 'K3', 'K4', 'K5', 'K6')),
                     (g2, tuple(f'K{n}' for n in list(range(13, 25)) + list(range(37, 49))))):
        for k in keys:
            r = gg[k]
            f = r.frame(v, 'b1')
            px, py = f.p(1.62, 1.45)
            small_tag(svg, px, py, k)
    # stairs
    st = dict(arch1.STAIRS)
    st.update(ring.STAIRS2)
    for k, (band, b) in st.items():
        R = R0 + arch1.STAIR_X if band == 'O' else R0 - arch1.STAIR_X
        x, y = v.P(R, b)
        small_tag(svg, x, y, k, r=1.55, size=1.55)
    # nodes
    for code, band, x_, b, nm in (('S1.1', 'I', 2.5, 2.3, 'Suit-lock'), ('S1.2', 'O', 4.7, 3.6, 'Kargo'),
                                  ('S1.3', 'O', 0.0, 0.0, None), ('S2.1', 'O', 0.0, 120.0, None),
                                  ('S2.2', 'O', 2.45, 122.6, 'Shaft'), ('S2.3', 'I', 2.45, 122.0, 'Darurat'),
                                  ('S3.1', 'O', 0.0, 240.0, None), ('S3.2', 'O', 5.3, 240.0, 'EVA darurat'),
                                  ('S3.3', 'I', 2.7, 236.6, 'Darurat')):
        R = R0 + x_ if band == 'O' else R0 - x_
        tagc(ctx, R, b, code, nm, r_mm=2.25, size=1.7, name_size=1.4)


def corridor_labels(ctx):
    for b, s in ((32.0, 'KORIDOR UTAMA 3,60 m'), (157.0, 'KORIDOR UTAMA 3,60 m — LOOP 360°'),
                 (268.0, 'KORIDOR 3,60 m · DI BAWAH MEZANIN'), (333.0, 'KORIDOR 3,60 m · DI BAWAH MEZANIN'),
                 (100.0, 'DI BAWAH MEZANIN'), (212.0, 'KORIDOR UTAMA 3,60 m')):
        arch1.corridor_label(ctx, b, s=s, size=1.6)


def yard(ctx, svg, v):
    """inner court: tower, bearing rays, arch spans, arch titles"""
    tx, ty = v.P(0, 0)
    # bearing rays to node centres
    for b, lab in ((0, 'S1 · 0°'), (120, 'S2 · 120°'), (240, 'S3 · 240°')):
        x1, y1 = v.P(1.6, b)
        x2, y2 = v.P(16.6, b)
        svg.add(f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" stroke="#b08a50" stroke-width="0.22" stroke-dasharray="4,0.8,0.6,0.8"/>')
        xl, yl = v.P(12.4, b)
        (dx, dy), (rx, ry) = v.dirs(b)
        ang = upright(math.degrees(math.atan2(ry, rx)))
        svg.add(f'<rect x="{num(xl - 7.5)}" y="{num(yl - 2.2)}" width="15" height="3.4" fill="#ffffff" transform="rotate({num(ang)} {num(xl)} {num(yl)})"/>')
        svg.add(text(xl, yl + 0.6, lab, size=1.9, weight=700, fill='#8a6a30', rot=ang))
    # tower
    svg.add(f'<circle cx="{num(tx)}" cy="{num(ty)}" r="{num(v.L(0.55))}" fill="#3a3a3a"/>')
    svg.add(f'<circle cx="{num(tx)}" cy="{num(ty)}" r="{num(v.L(1.2))}" fill="none" stroke="#3a3a3a" stroke-width="0.25"/>')
    svg.add(f'<rect x="{num(tx - v.L(3.0))}" y="{num(ty - v.L(2.2))}" width="{num(v.L(6.0))}" height="{num(v.L(4.4))}" fill="none" stroke="#3a3a3a" stroke-width="0.3" stroke-dasharray="1.5,0.8"/>')
    svg.add(text(tx, ty + v.L(2.2) + 4.0, 'MENARA POMPA PUSAT (0,0)', size=2.4, weight=800))
    svg.add(text(tx, ty + v.L(2.2) + 7.0, 'pusat cincin · tapak 6,0 × 4,4 m', size=1.8, fill='#555'))
    svg.add(f'<rect x="{num(tx - 30)}" y="{num(ty - v.L(2.2) - 5.6)}" width="60" height="3.6" fill="#ffffff"/>')
    svg.add(text(tx, ty - v.L(2.2) - 3.0, 'R sumbu = 28,00 m · keliling sumbu 175,93 m', size=1.8, fill='#8a6a30', weight=600))
    # arch titles
    for b, t1, t2, t3 in ((60, 'ARCH 1 · CORE', 'Early Settlement (tahap 1)', '12 kabin · 10–15 org · safe room 15'),
                          (180, 'ARCH 3 · GROW & MAKE', 'pangan, daur ulang & fabrikasi', 'tanpa kabin · area kerja'),
                          (300, 'ARCH 2 · LIVING', 'hunian 2 lantai + sosial/edukasi', '48 kabin · 48 org')):
        x, y = v.P(9.6, b)
        if b == 180:
            y += 2
        svg.add(text(x, y, t1, size=3.4, weight=800, fill='#151515', ls='0.3'))
        svg.add(text(x, y + 3.8, t2, size=2.05, weight=600, fill=K.ACC))
        svg.add(text(x, y + 6.8, t3, size=1.85, weight=500, fill='#555'))
    # span dims (inside the court)
    for b1, b2, top in ((5, 115, 'ARCH 1 · 22 modul × 5,0° = 110,0° · 53,76 m di sumbu'),
                        (125, 235, 'ARCH 3 · 22 modul = 110,0° · 53,76 m'),
                        (245, 355, 'ARCH 2 · 22 modul = 110,0° · 53,76 m')):
        K.arc_dim(ctx, 15.3, b1, b2, label_bot=top, ext_from=16.9, size=2.0)
    for b1, b2, lab in ((-5, 5, 'S1 · 2 modul'), (115, 125, 'S2 · 2 modul'), (235, 245, 'S3 · 2 modul')):
        K.arc_dim(ctx, 15.3, b1, b2, label_bot=lab, ext_from=16.9, size=1.9)


def outside_notes(ctx, svg, v):
    def note(R, b, s, size=1.7, color='#8c2f14', weight=600, radial=False, dy=0.0):
        x, y = v.P(R, b)
        (tx, ty), (rx, ry) = v.dirs(b)
        ang = upright(math.degrees(math.atan2(ry, rx) if radial else math.atan2(ty, tx)))
        svg.add(text(x, y + dy, s, size=size, fill=color, weight=weight, rot=ang))
    # S1: radial covered corridor (outer) + EVA to yard (inner)
    da = ang_of(1.2, 37.7)
    svg.add(f'<path d="{sector_d(v, 35.0, 38.6, 1.5 - da, 1.5 + da)}" fill="#efeeea" stroke="#555" stroke-width="0.25"/>')
    x1, y1 = v.P(35.4, 1.5)
    x2, y2 = v.P(40.2, 1.5)
    svg.add(f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" stroke="#8c2f14" stroke-width="0.4" marker-end="url(#arrR)"/>')
    x, y = v.P(40.6, 0)
    svg.add(text(x + 4, y - 1.2, 'S1 · PORTAL UTAMA EVA & KARGO', size=2.2, anchor='start', weight=800, fill='#8c2f14'))
    svg.add(text(x + 4, y + 1.9, 'koridor radial tertutup → cincin 2 · depot · lapangan rover', size=1.75, anchor='start', weight=500, fill='#8c2f14'))
    x1, y1 = v.P(20.4, 2.6)
    x2, y2 = v.P(17.4, 2.6)
    svg.add(f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" stroke="#8c2f14" stroke-width="0.35" marker-end="url(#arrR)"/>')
    x, y = v.P(18.6, 5.2)
    svg.add(text(x, y + 0.6, 'EVA → halaman dalam / menara', size=1.6, anchor='start', weight=600, fill='#8c2f14'))
    # S3: backup EVA exit through the shield
    da = ang_of(1.0, 36.0)
    svg.add(f'<path d="{sector_d(v, 35.0, 37.4, 238.0 - da, 238.0 + da)}" fill="#efeeea" stroke="#555" stroke-width="0.22"/>')
    x1, y1 = v.P(35.3, 238.0)
    x2, y2 = v.P(39.6, 238.0)
    svg.add(f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" stroke="#8c2f14" stroke-width="0.4" marker-end="url(#arrR)"/>')
    x, y = v.P(40.2, 238.0)
    svg.add(text(x - 1.5, y + 2.6, 'S3 · airlock darurat /', size=1.9, anchor='end', weight=800, fill='#8c2f14'))
    svg.add(text(x - 1.5, y + 5.2, 'EVA cadangan (jalur keluar ke-2)', size=1.7, anchor='end', weight=500, fill='#8c2f14'))
    # S2: utility shaft note
    x, y = v.P(40.0, 120.0)
    svg.add(text(x + 1.0, y + 2.2, 'S2 · pemisah 1–3', size=1.9, anchor='start', weight=800, fill='#8c2f14'))
    svg.add(text(x + 1.0, y + 4.8, 'shaft utilitas utama (S2.2)', size=1.7, anchor='start', weight=500, fill='#8c2f14'))


def section_refs(ctx, svg, v):
    def cutline(pts_polar):
        d = 'M' + ' L'.join(f'{num(v.P(R, b)[0])},{num(v.P(R, b)[1])}' for R, b in pts_polar)
        svg.add(f'<path d="{d}" fill="none" stroke="#c0391b" stroke-width="0.35" stroke-dasharray="4,1,0.7,1"/>')
    cutline([(17.6, 100.0), (38.3, 100.0)])
    pts_ = [(38.3, 62.0), (29.0, 62.0)] + [(29.0, 62.0 + k * 1.0) for k in range(1, 19)] + [(29.0, 80.0), (17.6, 80.0)]
    cutline(pts_)
    for R, b, L in ((38.3, 100.0, 'A'), (17.6, 100.0, 'A'), (38.3, 62.0, 'B'), (17.6, 80.0, 'B')):
        K.sec_marker(ctx, R, b, L, -1)


def legend_block(svg, x, y):
    K.section_heading(svg, x, y, 'LEGENDA', 2.8)
    items1 = [('ice', 'cangkang es 0,60 (potong +1,20)'), ('gap', 'celah CO₂ 0,10'), ('mem', 'membran inflatable ganda'),
              ('chase', 'chase utilitas lantai–membran'), ('reg', 'perisai karung regolit (node)'),
              ('node', 'rangka node kaku / bulkhead'), ('wall', 'partisi 0,10'), ('acou', 'dinding akustik 0,20')]
    items2 = [('glass', 'partisi kaca (ruang tanam, gym)'), ('door', 'pintu ayun / ganda'), ('slide', 'pintu geser (pocket) 0,90'),
              ('hatch', 'hatch tekanan 1,20'), ('corr', 'lajur koridor 3,60 bebas'), ('mezz', 'tepi mezanin +3,00 di atas'),
              ('axis', 'sumbu cincin R = 28,00'), ('cut', 'garis potong (lembar 3)')]
    for i, (k, lab) in enumerate(items1):
        K.legend_row(svg, x, y + 6 + i * 4.15, k, lab, w=8, h=3.3, size=1.95)
    for i, (k, lab) in enumerate(items2):
        K.legend_row(svg, x + 126, y + 6 + i * 4.15, k, lab, w=8, h=3.3, size=1.95)
    return y + 6 + 8 * 4.15


def zone_block(svg, x, y):
    K.section_heading(svg, x, y, 'ZONASI', 2.8)
    zones = [('node', 'node pemisah S1–S3'), ('tech', 'teknis, logistik & gudang'), ('eclss', 'ECLSS & daur ulang air'),
             ('res', 'riset, kontrol, medis, lab'), ('comm', 'komunal, kafe, plaza'), ('grow', 'pangan: tanam, benih, pantry'),
             ('make', 'fabrikasi & daur ulang'), ('edu', 'edukasi: aula, perpustakaan'), ('priv', 'privat: kabin & sanitasi'),
             ('circ', 'sirkulasi / tangga')]
    for i, (z, lab) in enumerate(zones):
        col, row = divmod(i, 5)
        K.legend_row(svg, x + col * 126, y + 6 + row * 4.15, ZONE[z], lab, w=7, h=3.1, size=1.95)
    return y + 6 + 5 * 4.15


def table(svg, x, y, cols, rows, size=1.95, row_h=3.35, head=True, bold_last=False, zebra=False):
    """cols: list of (title, width, anchor)"""
    if head:
        xx = x
        for t, w, a in cols:
            tx = xx if a == 'start' else (xx + w if a == 'end' else xx + w / 2)
            svg.add(text(tx, y, t, size=1.7, anchor=a, weight=700, fill='#666', ls='0.2'))
            xx += w
        svg.add(f'<line x1="{x}" y1="{num(y + 1.2)}" x2="{num(x + sum(c[1] for c in cols))}" y2="{num(y + 1.2)}" stroke="#151515" stroke-width="0.3"/>')
        y += 1.2 + row_h
    for i, row in enumerate(rows):
        last = bold_last and i == len(rows) - 1
        if last:
            svg.add(f'<line x1="{x}" y1="{num(y - row_h + 0.9)}" x2="{num(x + sum(c[1] for c in cols))}" y2="{num(y - row_h + 0.9)}" stroke="#151515" stroke-width="0.25"/>')
        xx = x
        for (t, w, a), cell in zip(cols, row):
            if isinstance(cell, tuple):        # (zone swatch, text)
                z, cell = cell
                svg.add(f'<rect x="{num(xx)}" y="{num(y - 2.45)}" width="7.6" height="3.0" fill="{ZONE.get(z, "#fff")}" stroke="#bbb" stroke-width="0.1"/>')
                svg.add(text(xx + 3.8, y, cell, size=size, weight=800))
            else:
                tx = xx if a == 'start' else (xx + w if a == 'end' else xx + w / 2)
                svg.add(text(tx, y, cell, size=size, anchor=a, weight=700 if last else 400))
            xx += w
        y += row_h
    return y


def inset_mezz(svg, x0, y0, x1, y1, den=250):
    """Arch 2 mezzanine +3.00, rainbow orientation (bearing 300 up), fitted into the box"""
    v0 = View(den, 0, 0, 300)
    pts_ = [v0.P(R, b) for R in (19.6, 36.4) for b in [242 + 2 * k for k in range(59)]]
    xs = [p[0] for p in pts_]
    ys = [p[1] for p in pts_]
    w = max(xs) - min(xs)
    ox = (x0 + x1) / 2 - (min(xs) + w / 2)
    oy = y0 - min(ys)
    v = View(den, ox, oy, 300)
    ctx = Ctx(svg, v, lw=0.65, labels=False)
    cid = 'clipMz'
    svg.d(f'<clipPath id="{cid}"><rect x="{x0}" y="{y0 - 1}" width="{x1 - x0}" height="{y1 - y0 + 2}"/></clipPath>')
    svg.add(f'<g clip-path="url(#{cid})">')
    g2, mz = ring.draw_arch2_mezz(ctx)
    svg.add('</g>')
    for r in mz.values():
        if r.rid.startswith('K'):
            f = r.frame(v, 'b1')
            px, py = f.p(1.55, 1.15)
            svg.add(text(px, py + 0.55, r.rid, size=1.45, weight=800, fill='#222'))
    for rid, band, x, b in (('L9', 'O', 2.9, 285.6), ('L11', 'O', 2.9, 314.4), ('L10', 'I', 2.9, 246.8), ('L12', 'I', 2.9, 353.2)):
        R = R0 + x if band == 'O' else R0 - x
        px, py = v.P(R, b)
        svg.add(text(px, py + 0.55, rid, size=1.45, weight=800, fill='#222'))
    for k, (band, b) in ring.STAIRS2.items():
        R = R0 + arch1.STAIR_X if band == 'O' else R0 - arch1.STAIR_X
        px, py = v.P(R, b)
        small_tag(svg, px, py, k, r=1.35, size=1.3)
    px, py = v.P(R0, 300)
    svg.add(text(px, py - 0.8, 'inti sosial tinggi penuh', size=1.6, weight=700, fill='#666'))
    svg.add(text(px, py + 1.9, '(L1–L4 tanpa mezanin)', size=1.45, weight=500, fill='#666'))
    for b, s_ in ((267.6, 'SAYAP A · K25–K36'), (332.4, 'SAYAP B · K49–K60')):
        px, py = v.P(R0, b)
        (tx, ty), _ = v.dirs(b)
        ang = upright(math.degrees(math.atan2(ty, tx)))
        svg.add(f'<rect x="{num(px - 13)}" y="{num(py - 1.7)}" width="26" height="2.8" fill="#eef1f4" transform="rotate({num(ang)} {num(px)} {num(py)})"/>')
        svg.add(text(px, py + 0.55, s_, size=1.6, weight=800, fill='#3c5a74', rot=ang))
    for b, lab in ((241.6, 'S3'), (358.4, 'S1')):
        px, py = v.P(R0, b)
        svg.add(text(px, py + 0.8, lab, size=2.2, weight=800, fill='#8c2f14'))
    return v, g2, mz


def connect_diagram(svg, cx, cy, r_mid=21.0):
    """schematic ring: arches, nodes, corridor loop, 6 hatches, EVA exits, shaft, isolation scenario"""
    den = 1000 * R0 / r_mid
    v = View(den, cx, cy, 0)
    k = v.s
    Ro, Ri = R0 + 6.8 / (k / 0.75 * 1.0) if False else R0 + 7.5, R0 - 7.5
    cols = {'A1': '#f2dcb0', 'A3': '#d9eacb', 'A2': '#d6e2ee'}
    for name, b1, b2 in (('A1', 5, 115), ('A3', 125, 235), ('A2', 245, 355)):
        svg.add(f'<path d="{sector_d(v, Ri, Ro, b1, b2)}" fill="{cols[name]}" stroke="#555" stroke-width="0.2"/>')
    # isolation scenario on Arch 3: hatched red
    svg.add(f'<path d="{sector_d(v, Ri, Ro, 125, 235)}" fill="url(#leakH)" stroke="#c0391b" stroke-width="0.35"/>')
    for b1, b2 in ((-5, 5), (115, 125), (235, 245)):
        svg.add(f'<path d="{sector_d(v, Ri - 1.0, Ro + 1.0, b1, b2)}" fill="#5b5f63" stroke="none"/>')
    # corridor loop
    RL = R0 - 4.2
    for b1, b2 in ((0, 180), (180, 360)):
        svg.add(f'<path d="{arc_d(v, RL, b1, b2)}" fill="none" stroke="#151515" stroke-width="0.35" stroke-dasharray="1.6,0.9"/>')
    for b, d in ((40, 1), (80, -1), (160, 1), (200, -1), (280, 1), (320, -1)):
        x1, y1 = v.P(RL, b)
        x2, y2 = v.P(RL, b + d * 4)
        svg.add(f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" stroke="#151515" stroke-width="0.35" marker-end="url(#arr)"/>')
    # 6 hatches (closed ones in red for the scenario)
    for b in (-5, 5, 115, 125, 235, 245):
        closed = b in (115, 245) or b in (125, 235)
        col = '#c0391b' if b in (125, 235) else HATCH_C
        x1, y1 = v.P(RL - 2.2, b)
        x2, y2 = v.P(RL + 2.2, b)
        svg.add(f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" stroke="{col}" stroke-width="{1.0 if b in (125, 235) else 0.6}"/>')
    # labels
    for b, t1, t2 in ((60, 'ARCH 1', 'CORE'), (180, 'ARCH 3', 'GROW & MAKE'), (300, 'ARCH 2', 'LIVING')):
        x, y = v.P(R0 + 2.6, b)
        svg.add(text(x, y - 0.6, t1, size=1.9, weight=800))
        svg.add(text(x, y + 1.7, t2, size=1.45, weight=700, fill='#444'))
    for b, lab in ((-9.0, 'S1'), (120, 'S2'), (247.0, 'S3')):
        x, y = v.P(R0 + 12.0, b)
        svg.add(text(x, y + 0.8, lab, size=2.0, weight=800, fill='#8c2f14'))
    # EVA exits: S1 outward (main) + inward (yard), S3 outward (backup)
    for b, Ra, Rb, w in ((1.5, R0 + 8.5, R0 + 15.5, 0.5), (2.5, R0 - 8.5, R0 - 14.5, 0.4), (238.5, R0 + 8.5, R0 + 15.0, 0.4)):
        x1, y1 = v.P(Ra, b)
        x2, y2 = v.P(Rb, b)
        svg.add(f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" stroke="#8c2f14" stroke-width="{w}" marker-end="url(#arrR)"/>')
    x, y = v.P(R0 + 16.5, 12)
    svg.add(text(x + 1, y, 'EVA utama', size=1.55, anchor='start', weight=700, fill='#8c2f14'))
    x, y = v.P(R0 + 15.8, 228)
    svg.add(text(x - 1, y + 1.5, 'EVA cadangan', size=1.55, anchor='end', weight=700, fill='#8c2f14'))
    # shaft at S2
    x, y = v.P(R0 + 3.8, 120)
    svg.add(f'<circle cx="{num(x)}" cy="{num(y)}" r="0.9" fill="#ffffff" stroke="#1d4f73" stroke-width="0.3"/>')
    # tower
    svg.add(f'<circle cx="{num(cx)}" cy="{num(cy)}" r="1.0" fill="#3a3a3a"/>')
    svg.add(text(cx, cy + 3.6, 'menara (0,0)', size=1.45, fill='#555'))
    # scenario caption
    x, y = v.P(R0 + 9.8, 180)
    svg.add(text(x, y + 3.2, 'contoh: Arch 3 bocor → hatch S2 & S3 ditutup', size=1.5, weight=700, fill='#c0391b'))
    svg.add(text(x, y + 5.6, 'Arch 1 ↔ Arch 2 tetap terhubung lewat S1', size=1.5, weight=500, fill='#c0391b'))


def phase_icons(svg, x0, y0, w):
    """three mini rings: stage 1 (Arch 1), stage 2 (+Arch 3), stage 3 (closed ring)"""
    stages = [('TAHAP 1', 'Arch 1 + S1 + S2', '10–15 org · ujung sementara', ('S1', 'A1', 'S2')),
              ('TAHAP 2 (usulan)', '+ Arch 3 + S3', 'pangan & fabrikasi lokal', ('S1', 'A1', 'S2', 'A3', 'S3')),
              ('TAHAP 3 (usulan)', '+ Arch 2 → cincin tertutup', '50–60 org · ekspansi cincin 2', ('S1', 'A1', 'S2', 'A3', 'S3', 'A2'))]
    segs = [('S1', -5, 5, '#5b5f63'), ('A1', 5, 115, '#e3b778'), ('S2', 115, 125, '#5b5f63'),
            ('A3', 125, 235, '#b9d6a3'), ('S3', 235, 245, '#5b5f63'), ('A2', 245, 355, '#a9c3dc')]
    cw = w / 3
    for i, (t, l1, l2, on) in enumerate(stages):
        cx = x0 + cw * i + 17
        cy = y0 + 17
        v = View(1000 * R0 / 11.5, cx, cy, 0)
        for name, b1, b2, col in segs:
            fill = col if name in on else '#f1f1f1'
            st = '#555' if name in on else '#c9c9c9'
            svg.add(f'<path d="{sector_d(v, R0 - 9, R0 + 9, b1, b2)}" fill="{fill}" stroke="{st}" stroke-width="0.18"/>')
        svg.add(f'<circle cx="{num(cx)}" cy="{num(cy)}" r="0.7" fill="#3a3a3a"/>')
        svg.add(text(cx - 16.5, cy + 22.0, t, size=2.05, anchor='start', weight=800, fill='#151515'))
        svg.add(text(cx - 16.5, cy + 25.3, l1, size=1.85, anchor='start', weight=600, fill=K.ACC))
        svg.add(text(cx - 16.5, cy + 28.4, l2, size=1.75, anchor='start', fill='#444'))


def build(path):
    svg = SVG(K.W, K.H)
    v = View(DEN, OX, OY, 0)
    defs(svg, v.s)
    svg.d('<pattern id="leakH" patternUnits="userSpaceOnUse" width="1.6" height="1.6" patternTransform="rotate(45)">'
          '<rect width="1.6" height="1.6" fill="#f7d9cf"/><line x1="0" y1="0" x2="0" y2="1.6" stroke="#c0391b" stroke-width="0.35"/></pattern>')
    ctx = Ctx(svg, v, lw=0.85, labels=False)
    K.frame(svg)
    K.header(svg, 4, 'CINCIN 1 — PERMANENT SETTLEMENT',
             'DENAH CINCIN PENUH ±0,00 · 72 MODUL = 3 ARCH × 22 + 3 NODE PEMISAH × 2',
             'SKALA 1 : 150')
    g1, g3, g2 = ring.draw_ring(ctx)
    corridor_labels(ctx)
    module_ring(ctx)
    tags_ring(ctx, g1, g3, g2)
    yard(ctx, svg, v)
    outside_notes(ctx, svg, v)
    section_refs(ctx, svg, v)

    # ---- north arrow, orientation, scale (left free corners)
    K.north_arrow(svg, 34, 72, -90, size=8)
    K.para(svg, 50, 66, ['Utara (U) ke atas · S1 di 0° (utara),',
                         'S2 di 120°, S3 di 240° dari menara (0,0);',
                         'Arch 1 searah jarum jam dari S1 (5°–115°).'], size=1.9, lh=1.5, color='#444')
    K.scale_bar(svg, 22, 566, v.s, ticks=(0, 1, 2, 5, 10, 20), label='skala grafis 1:150 (m)')

    # ---- right column
    x0, x1 = CX0, CX1
    K.section_heading(svg, x0, 53, 'DENAH MEZANIN +3,00 — ARCH 2 LIVING (inset)', 2.8)
    svg.add(text(x1, 53, '1 : 250', size=2.5, anchor='end', weight=800))
    inset_mezz(svg, x0 + 1, 57, x1 - 1, 163, den=250)
    yc = 166.5
    svg.add(text(x0, yc, 'Mezanin +3,00 hanya di sayap hunian (M1–M9 & M14–M22): 24 kabin atas K25–K36 / K49–K60, sanitasi bertumpuk', size=1.85, anchor='start', fill='#444'))
    svg.add(text(x0, yc + 3.0, 'L9/L11 di atas L5/L7; 2 jembatan per sayap → tiap walkway mezanin punya 2 jalan keluar (tangga T5–T10).', size=1.85, anchor='start', fill='#444'))

    # capacity & areas
    m1 = arch1.rooms_mezz()
    m2 = ring.arch2_mezz()
    a1g, a1m = ring.area_of(g1.values()), ring.area_of(m1.values())
    a3 = ring.area_of(g3.values())
    a2g, a2m = ring.area_of(g2.values()), ring.area_of(m2.values())
    a_corr = ring.corridor_area(330)
    a_node = 3 * ring.node_area()
    tot = a1g + a1m + a3 + a2g + a2m + a_corr + a_node
    y = 178
    K.section_heading(svg, x0, y, 'KAPASITAS & LUAS LANTAI CINCIN 1', 2.8)
    cols = [('BAGIAN', 48, 'start'), ('FUNGSI UTAMA', 108, 'start'), ('KABIN', 22, 'middle'), ('ORANG', 24, 'middle'),
            ('LUAS m²', 53, 'end')]
    rows = [('Arch 1 · Core', 'teknis, ECLSS, medis, kontrol, komunal, safe room', '12', '10–15', f'{fmt(a1g, 0)} + {fmt(a1m, 0)} mz'),
            ('Arch 3 · Grow & Make', 'ruang tanam, pangan, daur ulang, fabrikasi', '—', 'kerja', fmt(a3, 0)),
            ('Arch 2 · Living', 'kabin 2 lantai, sanitasi, aula, kafe, perpustakaan', '48', '48', f'{fmt(a2g, 0)} + {fmt(a2m, 0)} mz'),
            ('Node S1 · S2 · S3', 'portal EVA/kargo, penyangga, shaft, darurat', '—', '—', fmt(a_node, 0)),
            ('Koridor loop 3,60', 'menerus 360°, 6 hatch 1,20 di bulkhead node', '—', '—', fmt(a_corr, 0)),
            ('TOTAL CINCIN 1', '72 modul · 3 arch + 3 node', '60', '50–60', fmt(tot, 0))]
    y = table(svg, x0, y + 6.5, cols, rows, size=2.0, row_h=3.65, bold_last=True)
    svg.add(text(x0, y + 0.2, 'Luas sampai muka chase utilitas (±6,60 m); mz = mezanin +3,00 (kabin, sanitasi, linen; walkway tidak dihitung).', size=1.7, anchor='start', fill='#666'))

    # programme lists
    y = y + 8.0
    K.section_heading(svg, x0, y, 'PROGRAM RUANG ARCH 3 & ARCH 2', 2.8)
    svg.add(text(x1, y, 'Arch 1 (01–19, K1–K12, T1–T4) → lembar 1–2', size=1.8, anchor='end', fill='#666'))
    y0p = y + 6.5
    c3 = [('NO', 11, 'start'), ('ARCH 3 · GROW & MAKE', 98, 'start'), ('m²', 13, 'end')]
    rows3 = [((r.zone, r.rid), r.name, fmt(r.area(), 1)) for r in g3.values()]
    table(svg, x0, y0p, c3, rows3, size=1.95, row_h=3.5)
    c2 = [('NO', 11, 'start'), ('ARCH 2 · LIVING', 98, 'start'), ('m²', 13, 'end')]
    rows2 = []
    for rid in ('L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8'):
        r = g2[rid]
        rows2.append(((r.zone, rid), r.name, fmt(r.area(), 1)))
    for rid in ('L9', 'L10', 'L11', 'L12'):
        r = m2[rid]
        rows2.append(((r.zone, rid), r.name + ' (+3,00)', fmt(r.area(), 1)))
    rows2 += [(('priv', 'K'), 'K13–18, K37–42 kabin luar ±0,00 (@)', fmt(g2['K13'].area(), 1)),
              (('priv', 'K'), 'K19–24, K43–48 kabin dalam ±0,00 (@)', fmt(g2['K19'].area(), 1)),
              (('priv', 'K'), 'K25–30, K49–54 kabin luar +3,00 (@)', fmt(m2['K25'].area(), 1)),
              (('priv', 'K'), 'K31–36, K55–60 kabin dalam +3,00 (@)', fmt(m2['K31'].area(), 1)),
              (('circ', 'T'), 'T5–T10 tangga spiral Ø1,50 dalam ceruk', '—')]
    table(svg, x0 + 132, y0p, c2, rows2, size=1.95, row_h=3.5)
    y = y0p + 1.2 + 3.5 * (len(rows2) + 1) + 3.5

    # connectivity: diagram + flows
    K.section_heading(svg, x0, y, 'KETERHUBUNGAN ANTAR-ARCH & KESELAMATAN', 2.8)
    connect_diagram(svg, x0 + 31, y + 36, r_mid=19.0)
    flows = [('①', 'Pangan', 'ruang tanam G2/G9 → dapur produksi G3 → galley 11 (Arch 1) & kafe L2 (Arch 2)'),
             ('②', 'Limbah & air kelabu', 'Arch 1/2 → bioreaktor G4 & daur ulang air G11 → nutrien kembali ke G2/G9'),
             ('③', 'Air, O₂ & daya', 'ECLSS A/B (04/05) → seluruh cincin via shaft S2.2 & trunk bawah lantai'),
             ('④', 'Material', 'fabrikasi G5 / daur ulang G12 ⇄ bengkel 03 & gudang 02 (suku cadang)'),
             ('⑤', 'Kru', 'kabin Arch 2 → kerja di Arch 1 (kontrol, lab, klinik) & Arch 3 (tanam, fabrikasi)'),
             ('⑥', 'Darurat', 'koridor loop dua arah; EVA utama S1, EVA cadangan S3; safe room 10 (15 org)')]
    fx = x0 + 66
    fy = y + 6.5
    for i, (n_, t_, d_) in enumerate(flows):
        yy = fy + i * 6.6
        svg.add(text(fx, yy, n_, size=2.3, anchor='start', weight=800, fill=K.ACC))
        svg.add(text(fx + 4.2, yy, t_, size=2.0, anchor='start', weight=800))
        svg.add(text(fx + 4.2, yy + 2.9, d_, size=1.8, anchor='start', fill='#333'))
    yy = fy + 6 * 6.6 + 0.6
    K.para(svg, fx, yy, ['Tiap arch dapat diisolasi (2 hatch 1,20 per node) tanpa memutus dua arch lain.',
                         'Node = rangka kaku + karung regolit; membran tiap arch disegel ke rangka node.',
                         'Catatan terbuka: shelter badai matahari 50–60 org perlu tambahan (usulan: L1 + L3',
                         'dilapis panel air) — verifikasi dosis pada tahap pengembangan.'], size=1.8, lh=1.5, color='#333')
    y = y + 76

    # legend & zones
    y = legend_block(svg, x0, y) + 2.5
    y = zone_block(svg, x0, y + 2) + 2.5
    K.section_heading(svg, x0, y + 1.5, 'TAHAPAN PEMBANGUNAN CINCIN 1', 2.8)
    phase_icons(svg, x0, y + 4.5, x1 - x0)
    K.title_block(svg, 646, 525, 183, 57, 4, 'Denah Cincin 1 Penuh ±0,00 — Permanent Settlement (72 modul)', '1 : 150 (A1) · inset 1 : 250')
    svg.save(path, 'Lembar 4 - Denah Cincin 1 Penuh')
    return y


if __name__ == '__main__':
    print(build(sys.argv[1]))
