"""Sheet 2 - Mezzanine plan +3.00 Arch 1 (Early Settlement), 1:100, with 1:50 cabin details."""
import math, sys
from core import SVG, View, R0, num, text, fmt, arc_d, radial_d, sector_d, upright, cut_widths, X_CHASE
from plan import defs, room_tag, ang_of
from furn import Ctx
import furn as F
import arch1
import sheetkit as K
from sheet1 import OX, OY, module_labels, key_plan, room_schedule


def view_for(denom, up, R, b, tx, ty):
    v = View(denom, 0, 0, up)
    x, y = v.P(R, b)
    return View(denom, tx - x, ty - y, up)


def cabin_detail(svg, which, cx, cy, title):
    """1:50 enlarged plan of one cabin, clipped"""
    if which == 'K1':
        r = arch1.rooms_ground()['K1']
        up = r.bm
        Rc = r.R(0.5 * (r.x1 + r.x2))
        level = 'G'
    else:
        r = arch1.rooms_mezz()[which]
        up = r.bm + 180
        Rc = r.R(0.5 * (r.x1 + r.x2))
        level = 'M'
    v = view_for(50, up, Rc, r.bm, cx, cy)
    cid = f'clip{which}'
    wbox, hbox = 100, 88
    svg.d(f'<clipPath id="{cid}"><rect x="{cx - wbox/2}" y="{cy - hbox/2 + 2}" width="{wbox}" height="{hbox}"/></clipPath>')
    svg.add(f'<g clip-path="url(#{cid})">')
    ctx = Ctx(svg, v, lw=1.35)
    if level == 'G':
        arch1.draw_ground_plan(ctx)
    else:
        arch1.draw_mezz_plan(ctx)
    # veil over neighbours
    Rin = r.R(r.x1)
    Rout = r.R(r.x2)
    room_d = sector_d(v, min(Rin, Rout), max(Rin, Rout), r.b1, r.b2)
    svg.add(f'<path d="M{cx - wbox/2},{cy - hbox/2 + 2} h{wbox} v{hbox} h{-wbox} Z {room_d}" fill="#ffffff" fill-opacity="0.62" fill-rule="evenodd"/>')
    svg.add('</g>')
    svg.add(f'<rect x="{cx - wbox/2}" y="{cy - hbox/2 + 2}" width="{wbox}" height="{hbox}" fill="none" stroke="#151515" stroke-width="0.3"/>')
    svg.add(text(cx - wbox / 2, cy - hbox / 2 - 1.5, title, size=2.5, anchor='start', weight=800))
    e1 = math.degrees(0.05 / Rin)
    e2 = math.degrees(0.05 / Rout)
    if r.band == 'O':
        p1, p2 = v.P(Rin, r.b1 + e1), v.P(Rin, r.b2 - e1)
        K.lin_dim(svg, p2, p1, 6.5, f'{fmt(r.width(0), 2)} (sisi tersempit)', size=2.15)
        p3, p4 = v.P(Rout, r.b1 + e2), v.P(Rout, r.b2 - e2)
        K.lin_dim(svg, p3, p4, 5.0, fmt(r.width(r.x2 - r.x1), 2), size=2.15)
    else:
        p1, p2 = v.P(Rout, r.b1 + e2), v.P(Rout, r.b2 - e2)
        K.lin_dim(svg, p1, p2, 5.0, f'{fmt(r.width(r.x2 - r.x1), 2)} (sisi tersempit)', size=2.15)
        p3, p4 = v.P(Rin, r.b2 - e1), v.P(Rin, r.b1 + e1)
        K.lin_dim(svg, p3, p4, 6.5, fmt(r.width(0), 2), size=2.15)
    q1 = v.P(Rin, r.b2 - e1)
    q2 = v.P(Rout, r.b2 - e2)
    K.lin_dim(svg, q1, q2, 5.5 if r.band == 'O' else -5.5, fmt(r.x2 - r.x1, 2) + ' kedalaman', size=2.15)
    items = [f'luas bersih {fmt(r.area(), 1)} m² (≥ 7,2 m²)', 'kasur built-in 2,00 × 0,90 + bantal', 'meja kerja 1,10 × 0,60 + kursi',
             'lemari pribadi 0,90 × 0,60', 'pintu geser (pocket) 0,90',
             'plafon +2,70 (sisi bawah plat mezanin)' if level == 'G' else 'tinggi bersih 2,40 (plafon +5,40)']
    K.para(svg, cx - wbox / 2, cy + hbox / 2 + 6.0, items, size=1.95, lh=1.5, bullet=True)


def build(path):
    svg = SVG(K.W, K.H)
    v = View(100, OX, OY, up_bearing=60)
    defs(svg, v.s)
    ctx = Ctx(svg, v, lw=1.0)
    K.frame(svg)
    K.header(svg, 2, 'ARCH 1 — EARLY SETTLEMENT', 'DENAH LANTAI MEZANIN +3,00  ·  bidang potong +4,20 m', 'SKALA 1 : 100')
    gr, mz = arch1.draw_mezz_plan(ctx)
    module_labels(ctx)

    def note(R, b, s, size=1.7, color='#5a4630', weight=600, radial=False):
        x, y = v.P(R, b)
        (tx, ty), (rx, ry) = v.dirs(b)
        ang = upright(math.degrees(math.atan2(ry, rx) if radial else math.atan2(ty, tx)))
        svg.add(text(x, y, s, size=size, fill=color, weight=weight, rot=ang))

    # big void labels
    for b, s1, s2 in ((32.0, 'VOID — TERBUKA KE LANTAI DASAR', 'atap ruang tertutup di bawah: +2,70'),
                      (67.5, 'VOID PLAZA · TINGGI PENUH 8,30 m', 'lampu sirkadian di puncak membran')):
        x, y = v.P(R0, b)
        (tx, ty), _ = v.dirs(b)
        ang = upright(math.degrees(math.atan2(ty, tx)))
        svg.add(f'<g transform="rotate({num(ang)} {num(x)} {num(y)})"><rect x="{num(x - 33)}" y="{num(y - 4.6)}" width="66" height="8.4" fill="#ffffff" opacity="0.88"/></g>')
        svg.add(text(x, y - 0.6, s1, size=2.6, weight=800, fill='#5b6670', rot=ang, ls='0.3'))
        svg.add(text(x, y + 2.7, s2, size=1.8, weight=500, fill='#5b6670', rot=ang))
    # tags
    for k in ('K7', 'K8', 'K9', 'K10', 'K11', 'K12'):
        r = mz[k]
        f = r.frame(v, 'b1')
        px, py = f.p(1.62, 1.35)
        svg.add(f'<circle cx="{num(px)}" cy="{num(py)}" r="2.3" fill="#ffffff" stroke="#222" stroke-width="0.22"/>')
        svg.add(text(px, py + 0.8, k, size=2.0 if len(k) < 3 else 1.75, weight=800))
        svg.add(text(px, py + 4.6, f'{fmt(r.area(), 1)} m²', size=1.55, fill='#666'))
    room_tag(ctx, R0 + 2.55, 87.0, '18', mz['18'].area(), 'Ruang tenang /\nperpustakaan', name_size=1.6)
    room_tag(ctx, R0 - 2.4, 86.5, '19', None, None, r_mm=2.1, size=1.9)
    for k, (band, b) in arch1.STAIRS.items():
        R = R0 + arch1.STAIR_X if band == 'O' else R0 - arch1.STAIR_X
        x, y = v.P(R, b)
        svg.add(f'<circle cx="{num(x)}" cy="{num(y)}" r="2.0" fill="#ffffff" stroke="#222" stroke-width="0.2"/>')
        svg.add(text(x, y + 0.75, k, size=2.0, weight=800))
    # walkway / slot labels
    for b in (99.0,):
        for sgn, lab in ((1, 'selasar 1,01'), (-1, 'selasar 1,01')):
            x, y = v.P(R0 + sgn * 0.85, b)
            (tx, ty), _ = v.dirs(b)
            ang = upright(math.degrees(math.atan2(ty, tx)))
            svg.add(text(x, y + 0.6, lab, size=1.5, fill='#6a645a', weight=600, rot=ang))
    x, y = v.P(R0, 104.0)
    (tx, ty), _ = v.dirs(104.0)
    svg.add(text(x, y + 0.55, 'slot cahaya 0,60', size=1.35, fill='#5b6670', weight=700, rot=upright(math.degrees(math.atan2(ty, tx)))))
    note(R0 + 0.0, 86.25, 'jembatan', 1.3, '#555', 700)
    note(R0 + 0.0, 113.5, 'jembatan', 1.3, '#555', 700)
    note(R0 + 4.95, 100.0, 'atap kabin bawah +2,70', 1.3, '#777', 500)
    note(R0 - 4.95, 101.5, 'atap kabin bawah +2,70', 1.3, '#777', 500)
    # node labels
    for b, s in ((0.0, 'S1 — node satu lantai (tanpa mezanin)'), (120.0, 'S2 — node satu lantai (tanpa mezanin)')):
        note(R0 + 0.0, b, s, 1.5, '#5a4630', 700, radial=True)

    # dims: mezzanine extent + radial dims at A-A
    K.arc_dim(ctx, 39.7, 85, 114.75, label_top='MEZANIN +3,00 — modul 17–22 (30,0°)', label_bot='14,54 m di sumbu', ext_from=38.75, size=2.2)
    K.arc_dim(ctx, 39.7, -5, 5, label_top='S1', size=2.0)
    K.arc_dim(ctx, 39.7, 5, 85, label_top='Modul 1–16: tanpa mezanin (void / atap ruang bawah)', size=2.0, ext_from=38.75)
    K.arc_dim(ctx, 39.7, 115, 125, label_top='S2', size=2.0)
    bD = 133.5
    xs = [-4.50, -4.42, -1.42, -1.34, -0.30, 0.30, 1.34, 1.42, 4.42, 4.50]
    P = [v.P(R0 + xx, bD) for xx in xs]
    labs = {(2, 3): None}
    pairs = [(1, 2, '3,00 kabin'), (3, 4, '1,04'), (4, 5, '0,60'), (5, 6, '1,04'), (7, 8, '3,00 kabin')]
    for i, j, lab in pairs:
        K.lin_dim(svg, P[i], P[j], -4.0, lab, size=1.85)
    K.lin_dim(svg, P[0], P[9], -10.0, '9,00 plat mezanin (x = ±4,50)', size=1.9)
    note(R0 + 0.0, bD + 2.3, 'tanpa skala: dimensi radial mezanin (m)', 1.4, '#7a2a12', 500, radial=True)

    # section markers (same lines as sheet 1)
    def cutline(pts_polar):
        d = 'M' + ' L'.join(f'{num(v.P(R, b)[0])},{num(v.P(R, b)[1])}' for R, b in pts_polar)
        svg.add(f'<path d="{d}" fill="none" stroke="#c0391b" stroke-width="0.45" stroke-dasharray="5,1,0.8,1"/>')
    cutline([(17.6, 100.0), (37.75, 100.0)])
    K.sec_marker(ctx, 37.75, 100.0, 'A', -1)
    K.sec_marker(ctx, 17.6, 100.0, 'A', -1)
    pts_ = [(37.75, 62.0), (29.0, 62.0)] + [(29.0, 62.0 + k * 1.0) for k in range(1, 19)] + [(29.0, 80.0), (17.6, 80.0)]
    cutline(pts_)
    K.sec_marker(ctx, 37.75, 62.0, 'B', -1)
    K.sec_marker(ctx, 17.6, 80.0, 'B', -1)

    # north, key plan, scale bar
    ax0, ay0 = v.P(0, 0)
    ax1, ay1 = v.P(1, 0)
    nang = math.degrees(math.atan2(ay1 - ay0, ax1 - ax0))
    K.north_arrow(svg, 172, 80, nang, size=8)
    svg.add(text(172, 96.5, 'utara (U)', size=1.9, fill='#555'))
    K.scale_bar(svg, 700, 92, v.s, ticks=(0, 1, 2, 5, 10), label='skala grafis 1:100 (m)')
    key_plan(svg, 88, 110, 0.85)

    # direction to the central pump tower (the tower itself lies behind the 1:50 details)
    xt0, yt0 = v.P(17.0, 60)
    xt1, yt1 = v.P(8.8, 60)
    svg.add(f'<line x1="{num(xt0)}" y1="{num(yt0)}" x2="{num(xt1)}" y2="{num(yt1)}" stroke="#b08a50" stroke-width="0.3" '
            f'stroke-dasharray="4,0.8,0.6,0.8" marker-end="url(#arr)"/>')
    svg.add(f'<rect x="{num(xt0 - 31)}" y="{num(yt0 + 9)}" width="62" height="7.6" fill="#ffffff"/>')
    svg.add(text(xt0, yt0 + 12.2, 'MENARA POMPA PUSAT (0,0) ↓', size=2.3, weight=800, fill='#5a4630'))
    svg.add(text(xt0, yt0 + 15.4, 'pusat cincin · R sumbu = 28,00 m (lihat lembar 1)', size=1.8, fill='#666'))

    # cabin details 1:50 in the concave region
    cabin_detail(svg, 'K1', 362, 440, 'DETAIL KABIN K1 · LANTAI DASAR · 1:50')
    cabin_detail(svg, 'K11', 480, 440, 'DETAIL KABIN K11 · MEZANIN · 1:50')
    K.scale_bar(svg, 391, 517, 20, ticks=(0, 1, 2, 3), label='skala grafis detail 1:50 (m)')

    # bottom band: mezzanine schedule, legend, notes, title block
    rows = [('18', mz['18'].name, mz['18'].area(), 'priv'), ('19', mz['19'].name, mz['19'].area(), 'priv')]
    for k in ('K7', 'K8', 'K9', 'K10', 'K11', 'K12'):
        rows.append((k, mz[k].name + (' (sisi luar)' if mz[k].band == 'O' else ' (sisi dalam)'), mz[k].area(), 'priv'))
    a_walk = 2 * 0.5 * math.radians(114.75 - 85) * ((R0 + arch1.MZ_IN - 0.08) ** 2 - (R0 + arch1.SLOT) ** 2)
    a_walk_i = 0.5 * math.radians(114.75 - 85) * ((R0 - arch1.SLOT) ** 2 - (R0 - arch1.MZ_IN + 0.08) ** 2)
    a_walk = 0.5 * a_walk + a_walk_i
    a_br = sum(0.5 * math.radians(b2 - b1) * ((R0 + 0.3) ** 2 - (R0 - 0.3) ** 2) for b1, b2 in arch1.BRIDGES)
    rows.append(('—', 'Selasar 2 × 1,01 m + 2 jembatan', a_walk + a_br, 'circ'))
    rows.append(('T1–T4', 'Bukaan tangga spiral Ø1,50 (turun)', None, 'circ'))
    yb = 440
    K.section_heading(svg, 16, yb - 2, 'TABEL RUANG & LUASAN — MEZANIN +3,00', 3.0)
    room_schedule(svg, 16, yb + 7.5, rows, col_w=122, row_h=3.6, size=2.15, split=6)
    tot = sum(r.area() for r in mz.values()) + a_walk + a_br
    svg.add(f'<line x1="16" y1="{yb + 7.5 + 6*3.6 + 0.4}" x2="254" y2="{yb + 7.5 + 6*3.6 + 0.4}" stroke="#151515" stroke-width="0.25"/>')
    svg.add(text(16, yb + 7.5 + 6 * 3.6 + 4.2, f'Total mezanin ≈ {fmt(tot, 1)} m²  ·  12 kabin Arch 1 = 6 di lantai dasar (K1–K6) + 6 di mezanin (K7–K12)',
                 size=2.05, anchor='start', weight=600))
    cx, cy = 16, 488
    K.section_heading(svg, cx, cy - 2, 'KETENTUAN MEZANIN', 2.6)
    crit = ['Plat mezanin +3,00 (tebal 0,30; sisi bawah +2,70) hanya di dalam x = ±4,50 m dari sumbu busur.',
            'Tinggi bersih di tepi plat x = 4,50: membran +5,43 → 2,43 m ≥ 2,40 m; plafon kabin +5,40.',
            'Slot cahaya 0,60 m di atas sumbu koridor; pagar kaca 1,10 m di tepi slot, ujung mezanin & bukaan tangga.',
            'Tiap sisi mezanin punya 2 tangga (T1+T3 luar, T2+T4 dalam) + 2 jembatan → evakuasi dua arah.',
            'Kabin mezanin 3,00 (radial) × ≥2,47 m; pintu geser 0,90 ke selasar 1,01 m.',
            'Koridor lantai dasar di bawah mezanin tetap 3,60 m bersih (h = 2,70 m).']
    K.para(svg, cx, cy + 3.4, crit, size=2.05, lh=1.55, bullet=True)
    lx, ly = 612, 440
    K.section_heading(svg, lx, ly - 2, 'LEGENDA', 3.0)
    items1 = [('ice', 'cangkang es (terpotong +4,20)'), ('icebelow', 'permukaan luar es di bawah potongan'),
              ('gap', 'celah CO₂ 0,10'), ('mem', 'membran inflatable ganda'), ('reg', 'perisai karung regolit (node)'),
              ('wall', 'partisi kabin 0,08–0,10'), ('door', 'pintu ayun'), ('slide', 'pintu geser (pocket) 0,90')]
    items2 = [('#ffffff', 'plat mezanin +3,00'), ('#efeeea', 'selasar & jembatan'), ('void', 'void / terbuka ke bawah'),
              ('roof', 'atap ruang tertutup bawah (+2,70)'), ('glass', 'pagar kaca 1,10 m'), ('cut', 'garis potong (lembar 3)'),
              ('#f4eef6', 'zona privat / hunian')]
    for i, (k, lab) in enumerate(items1):
        K.legend_row(svg, lx, ly + 6 + i * 4.3, k, lab, size=2.05)
    for i, (k, lab) in enumerate(items2):
        K.legend_row(svg, lx + 108, ly + 6 + i * 4.3, k, lab, size=2.05)
    K.title_block(svg, 646, 525, 183, 57, 2, 'Denah Lantai Mezanin +3,00 — Arch 1 (Early Settlement)', '1 : 100 · detail 1 : 50 (A1)')
    svg.save(path, 'Lembar 2 - Denah Mezanin Arch 1')


if __name__ == '__main__':
    build(sys.argv[1])
