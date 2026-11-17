"""Sheet 1 - Ground floor plan Arch 1 (Early Settlement), 1:100, A1."""
import math, sys
from core import SVG, View, R0, num, text, fmt, arc_d, radial_d, sector_d, upright, X_CHASE, cut_widths
from plan import defs, room_tag, ang_of, ZONE
from furn import Ctx
import furn as F
import arch1
import sheetkit as K

OY = 485
OX = 420.5


def module_labels(ctx, b1=-5, b2=125, R_tick=(36.15, 36.65), R_lab=37.15, size=1.9, nodes=((-5, 5, 'S1'), (115, 125, 'S2'))):
    v, svg = ctx.view, ctx.svg
    centres = [0.5 * (nb1 + nb2) for nb1, nb2, _ in nodes]
    for k in range(int((b2 - b1) / 5) + 1):
        b = b1 + 5 * k
        if any(abs(b - c) < 1e-6 for c in centres):
            continue                      # node centre: inside the regolith shield
        svg.add(f'<path d="{radial_d(v, b, R_tick[0], R_tick[1])}" stroke="#555" stroke-width="0.18" fill="none"/>')
    def put(bm, lab, bold=False):
        x, y = v.P(R_lab, bm)
        (tx, ty), _ = v.dirs(bm)
        ang = upright(math.degrees(math.atan2(ty, tx)))
        svg.add(text(x, y + size * 0.35, lab, size=size, weight=800 if bold else 600,
                     fill='#8c2f14' if bold else '#555', rot=ang))
    for nb1, nb2, lab in nodes:
        bm = 0.5 * (nb1 + nb2)
        put(bm - 2.6 if lab == 'S1' else bm, lab, True)      # S1: clear of the radial corridor stub
    for k in range(22):
        put(5 + 5 * k + 2.5, f'M{k + 1}')


def room_schedule(svg, x, y, rows, col_w=118, row_h=3.55, size=2.25, split=None):
    """rows: list of (code, name, area or None, note)"""
    n = len(rows)
    split = split or (n + 1) // 2
    cols = [rows[:split], rows[split:]]
    for ci, col in enumerate(cols):
        cx = x + ci * col_w
        svg.add(f'<line x1="{cx}" y1="{y - 3.0}" x2="{cx + col_w - 6}" y2="{y - 3.0}" stroke="#151515" stroke-width="0.3"/>')
        svg.add(text(cx, y - 4.0, 'NO', size=1.9, anchor='start', weight=700, fill='#555', ls='0.3'))
        svg.add(text(cx + 11, y - 4.0, 'RUANG', size=1.9, anchor='start', weight=700, fill='#555', ls='0.3'))
        svg.add(text(cx + col_w - 7, y - 4.0, 'LUAS m²', size=1.9, anchor='end', weight=700, fill='#555', ls='0.3'))
        yy = y
        for code, name, area, zone in col:
            if zone:
                svg.add(f'<rect x="{cx - 0.3}" y="{yy - 2.55}" width="9.2" height="3.2" fill="{ZONE.get(zone, "#fff")}" stroke="#bbb" stroke-width="0.1"/>')
            svg.add(text(cx + 4.3, yy, code, size=size, weight=800))
            svg.add(text(cx + 11, yy, name, size=size, anchor='start'))
            if area is not None:
                svg.add(text(cx + col_w - 7, yy, fmt(area, 1), size=size, anchor='end', weight=600))
            yy += row_h
    return y + split * row_h


def build(path):
    svg = SVG(K.W, K.H)
    v = View(100, OX, OY, up_bearing=60)
    defs(svg, v.s)
    ctx = Ctx(svg, v, lw=1.0)
    K.frame(svg)
    K.header(svg, 1, 'ARCH 1 — EARLY SETTLEMENT', 'DENAH LANTAI DASAR ±0,00  ·  bidang potong +1,20 m', 'SKALA 1 : 100')

    g = arch1.draw_ground_plan(ctx)
    arch1.mezz_outline(ctx)

    # --- labels for mezzanine outline
    x, y = v.P(R0 - 0.0, 99.5)
    # corridor + plaza labels
    arch1.corridor_label(ctx, 14.0)
    arch1.corridor_label(ctx, 41.5)
    arch1.corridor_label(ctx, 103.0, s='KORIDOR 3,60 m — DI BAWAH MEZANIN (h = 2,70)', size=1.7)
    x, y = v.P(R0 + 0.05, 67.5)
    (tx, ty), _ = v.dirs(67.5)
    ang = upright(math.degrees(math.atan2(ty, tx)))
    svg.add(text(x, y - 1.2, 'PLAZA KOMUNAL', size=2.4, weight=800, fill='#9a6b1f', rot=ang, ls='0.5'))
    svg.add(text(x + 0.5, y + 2.0, 'void tinggi penuh 8,30 m · lajur 3,60 m tetap bebas', size=1.7, weight=500, fill='#9a6b1f', rot=ang))

    # --- room tags
    def tag(rid, band, x, b, name=None, area=True, r=None):
        rr = g.get(rid)
        a = rr.area() if (rr is not None and area) else None
        R = R0 + x if band == 'O' else R0 - x
        room_tag(ctx, R, b, rid, a if area else None, name)

    tag('01', 'I', 3.35, 8.3, 'Dekon & APD')
    tag('02', 'O', 3.3, 10.5, 'Gudang &\nlogistik')
    tag('03', 'I', 2.85, 16.2, 'Bengkel')
    tag('04', 'O', 3.0, 27.0, 'ECLSS A')
    tag('05', 'I', 2.8, 27.6, 'ECLSS B')
    tag('06', 'O', 2.75, 41.2, 'Kontrol &\nkomunikasi')
    tag('07', 'O', 2.45, 44.7, 'Lab basah')
    tag('08', 'I', 2.65, 42.6, 'Klinik')
    tag('09', 'I', 2.35, 45.8, 'Isolasi')
    tag('10', 'I', 2.75, 54.6, 'Safe room')
    tag('11', 'O', 2.5, 57.8, 'Galley')
    tag('12', 'O', 2.45, 71.4, 'Makan & lounge')
    tag('13', 'I', 2.35, 61.4, 'Plaza & taman')
    tag('14', 'O', 2.45, 80.3, 'Gym')
    tag('15', 'I', 2.35, 79.3, 'Hidroponik')
    tag('16', 'O', 3.25, 89.4, 'Sanitasi')
    tag('17', 'I', 2.35, 86.5, None, area=False)
    for k in ('K1', 'K2', 'K3', 'K4', 'K5', 'K6'):
        r = g[k]
        f = r.frame(v, 'b1')
        px, py = f.p(1.62, 1.45)
        svg.add(f'<circle cx="{num(px)}" cy="{num(py)}" r="2.3" fill="#ffffff" stroke="#222" stroke-width="0.22"/>')
        svg.add(text(px, py + 0.8, k, size=2.1, weight=800))
        svg.add(text(px, py + 4.6, f'{fmt(r.area(), 1)} m²', size=1.55, fill='#666'))
    # stairs labels
    for k, (band, b) in arch1.STAIRS.items():
        R = R0 + arch1.STAIR_X if band == 'O' else R0 - arch1.STAIR_X
        x, y = v.P(R, b)
        svg.add(f'<circle cx="{num(x)}" cy="{num(y)}" r="2.0" fill="#ffffff" stroke="#222" stroke-width="0.2"/>')
        svg.add(text(x, y + 0.75, k, size=2.0, weight=800))
    # small KM tag in isolation room
    x, y = v.P(R0 - 5.15, 47.4)
    svg.add(text(x, y, 'KM isolasi', size=1.35, fill='#555'))
    # node tags
    for code, band, x_, b, nm in (('S1.1', 'I', 2.35, 2.2, 'Suit-lock EVA'), ('S1.2', 'O', 4.65, 3.6, 'Airlock kargo'),
                                  ('S1.3', 'O', 0.0, 0.0, 'Penyangga'), ('S2.1', 'O', 0.0, 120.0, 'Penyangga'),
                                  ('S2.2', 'O', 3.05, 122.9, 'Shaft utilitas'), ('S2.3', 'I', 2.45, 122.0, 'Darurat & APD')):
        R = R0 + x_ if band == 'O' else R0 - x_
        room_tag(ctx, R, b, code, None, nm, r_mm=2.6, size=1.85, name_size=1.55)

    # --- node / exterior annotations
    def note(R, b, s, size=1.7, color='#5a4630', weight=600, dy=0.0, radial=False):
        x, y = v.P(R, b)
        (tx, ty), (rx, ry) = v.dirs(b)
        ang = upright(math.degrees(math.atan2(ry, rx) if radial else math.atan2(ty, tx)))
        svg.add(text(x, y + dy, s, size=size, fill=color, weight=weight, rot=ang))

    note(33.7, -6.9, 'perisai karung regolit · node tidak dicor es', 1.5, radial=True)
    note(33.7, 126.9, 'perisai karung regolit · node tidak dicor es', 1.5, radial=True)
    note(21.7, -6.9, 'dinding ujung sementara', 1.5, radial=True)
    note(21.7, 126.9, 'dinding ujung sementara', 1.5, radial=True)
    # radial corridor stub from cargo airlock (outer) - covered passage through the regolith shield
    da = ang_of(1.2, 37.7)
    svg.add(f'<path d="{sector_d(v, 35.0, 38.3, 1.5 - da, 1.5 + da)}" fill="#efeeea" stroke="#555" stroke-width="0.25"/>')
    x1, y1 = v.P(35.4, 1.5)
    x2, y2 = v.P(38.55, 1.5)
    svg.add(f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" stroke="#8c2f14" stroke-width="0.35" marker-end="url(#arrR)"/>')
    note(38.9, -9.3, 'koridor radial luar (tertutup)', 1.7, '#8c2f14', 700)
    note(37.7, -9.3, '→ cincin 2 · depot · lapangan rover', 1.5, '#8c2f14', 500)
    note(36.5, -9.3, 'port docking rover bertekanan (S1.2)', 1.5, '#8c2f14', 500)
    # EVA exit to inner yard
    x1, y1 = v.P(20.6, 2.6)
    x2, y2 = v.P(17.3, 2.6)
    svg.add(f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" stroke="#8c2f14" stroke-width="0.35" marker-end="url(#arrR)"/>')
    note(17.2, -1.6, 'EVA → halaman dalam / menara', 1.5, '#8c2f14', 600)
    note(19.85, -1.9, 'suitport ×2', 1.35, '#8c2f14', 500)
    # capped hatches labels
    note(29.6, -6.85, '', 1.4)
    note(R0 - 0.2, -6.9, 'hatch 1,20 → Arch 2 (tahap permanen)', 1.5, '#8c2f14', 600, radial=True)
    note(R0 - 0.2, 126.9, 'hatch 1,20 → Arch 3 (tahap permanen)', 1.5, '#8c2f14', 600, radial=True)

    # --- module ticks + labels
    module_labels(ctx)

    # --- dimension chains
    chain = [(-5, 5, 'S1 · Portal EVA & kargo', '2 modul · 10,0° · 4,89 m'),
             (5, 20, 'Modul 1–3 · Dekontaminasi & logistik', '15,0° · 7,33 m'),
             (20, 35, 'Modul 4–6 · Infrastruktur ECLSS', '15,0° · 7,33 m'),
             (35, 50, 'Modul 7–9 · Riset, kontrol & medis', '15,0° · 7,33 m'),
             (50, 75, 'Modul 10–14 · Komunal, plaza & safe room', '25,0° · 12,22 m'),
             (75, 85, 'Modul 15–16 · Hidroponik & gym', '10,0° · 4,89 m'),
             (85, 115, 'Modul 17–22 · Privat, sanitasi & hunian', '30,0° · 14,66 m'),
             (115, 125, 'S2 · Pemisah 1–3', '2 modul · 10,0° · 4,89 m')]
    for b1, b2, top, bot in chain:
        K.arc_dim(ctx, 39.7, b1, b2, label_top=top, label_bot=bot, ext_from=38.75, size=2.05)
    K.arc_dim(ctx, 43.0, 5, 115, label_top='ARCH 1 — 22 modul × 5,0° = 110,0°  ·  53,76 m di sumbu R = 28,00 m', size=2.4, bold=True)
    K.arc_dim(ctx, 43.0, -5, 5, label_top='S1', size=2.2, bold=True)
    K.arc_dim(ctx, 43.0, 115, 125, label_top='S2', size=2.2, bold=True)
    x, y = v.P(16.6, 60)
    svg.add(text(x, y, 'TOTAL DIGAMBAR: S1 (2) + ARCH 1 (22) + S2 (2)', size=2.5, weight=800, fill=K.DIM))
    svg.add(text(x, y + 3.6, '= 26 modul = 130,0° · 63,53 m di sumbu R = 28,00 m', size=2.2, weight=600, fill=K.DIM))
    svg.add(text(x, y + 7.0, '1 modul = 5,0° = 2,44 m di sumbu · 72 modul per cincin', size=1.9, weight=500, fill='#555'))
    # module size callout
    x, y = v.P(35.3, 7.5)

    # --- radial dimension chain beyond S2 free end
    bD = 133.5
    xs = [-8.0, -7.26, -1.80, 1.80, 7.26, 8.0]
    P = [v.P(R0 + xx, bD) for xx in xs]
    labs = ['0,74', '5,46', '3,60', '5,46', '0,74']
    for i in range(5):
        K.lin_dim(svg, P[i], P[i + 1], 0.0 if False else -4.0, labs[i], size=1.9)
    K.lin_dim(svg, P[1], P[4], -10.0, '14,52 lebar lantai bersih (muka membran @ ±0,00)', size=1.9)
    K.lin_dim(svg, P[0], P[5], -16.0, '16,00 bentang kaki es (muka luar @ ±0,00)', size=1.9)
    for xx, lab in ((0.0, 'sumbu R = 28,00'),):
        pass

    # --- section markers
    from plan import ICE_EDGE
    def cutline(pts_polar):
        d = 'M' + ' L'.join(f'{num(v.P(R, b)[0])},{num(v.P(R, b)[1])}' for R, b in pts_polar)
        svg.add(f'<path d="{d}" fill="none" stroke="#c0391b" stroke-width="0.45" stroke-dasharray="5,1,0.8,1"/>')
    cutline([(17.6, 100.0), (37.75, 100.0)])
    K.sec_marker(ctx, 37.75, 100.0, 'A', -1)
    K.sec_marker(ctx, 17.6, 100.0, 'A', -1)
    # B-B jogged: outer radial at 62 -> arc at x=+1.0 -> radial at 80
    pts_ = [(37.75, 62.0), (29.0, 62.0)] + [(29.0, 62.0 + k * 1.0) for k in range(1, 19)] + [(29.0, 80.0), (17.6, 80.0)]
    cutline(pts_)
    K.sec_marker(ctx, 37.75, 62.0, 'B', -1)
    K.sec_marker(ctx, 17.6, 80.0, 'B', -1)

    # --- tower & R=28 line, north arrow, key plan, scale bar
    tx_, ty_ = v.P(0, 0)
    svg.add(f'<circle cx="{num(tx_)}" cy="{num(ty_)}" r="{num(v.L(0.55))}" fill="#3a3a3a"/>')
    svg.add(f'<circle cx="{num(tx_)}" cy="{num(ty_)}" r="{num(v.L(1.2))}" fill="none" stroke="#3a3a3a" stroke-width="0.25"/>')
    svg.add(f'<rect x="{num(tx_ - v.L(3.0))}" y="{num(ty_ - v.L(2.2))}" width="{num(v.L(6.0))}" height="{num(v.L(4.4))}" fill="none" stroke="#3a3a3a" stroke-width="0.3" stroke-dasharray="1.5,0.8"/>')
    svg.add(text(tx_, ty_ + v.L(2.2) + 4.2, 'MENARA POMPA PUSAT (0,0)', size=2.4, weight=800))
    svg.add(text(tx_, ty_ + v.L(2.2) + 7.4, 'pusat cincin · tapak 6,0 × 4,4 m (IT-PT-CDD-001)', size=1.8, fill='#555'))
    x1, y1 = v.P(1.4, 60)
    x2, y2 = v.P(R0, 60)
    svg.add(f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" stroke="#b08a50" stroke-width="0.22" stroke-dasharray="4,0.8,0.6,0.8"/>')
    xm, ym = v.P(10.5, 60)
    svg.add(f'<rect x="{num(xm - 11)}" y="{num(ym - 3)}" width="22" height="4.4" fill="#ffffff"/>')
    svg.add(text(xm, ym + 0.4, 'R = 28,00 m (sumbu)', size=2.1, weight=700, fill='#8a6a30'))
    # north arrow (direction of bearing 0)
    ax0, ay0 = v.P(0, 0)
    ax1, ay1 = v.P(1, 0)
    nang = math.degrees(math.atan2(ay1 - ay0, ax1 - ax0))
    K.north_arrow(svg, 172, 80, nang, size=8)
    svg.add(text(172, 96.5, 'utara (U)', size=1.9, fill='#555'))
    # key plan
    key_plan(svg, 88, 110, 0.85)
    K.scale_bar(svg, 700, 92, v.s, ticks=(0, 1, 2, 5, 10), label='skala grafis 1:100 (m)')

    # --- bottom band: schedule, legend, criteria, title block
    rows = [('S1.1', 'Suit-lock & airlock EVA (kontrol debu)', None, 'node'),
            ('S1.2', 'Airlock kargo & port docking rover', None, 'node'),
            ('S1.3', 'Ruang penyangga S1 (hatch 1,20 ×2)', None, 'node')]
    for rid in ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17'):
        r = g[rid]
        rows.append((rid, r.name, r.area(), r.zone))
    rows += [('K1–K3', 'Kabin kru sisi luar (3 unit, @)', g['K1'].area(), 'priv'),
             ('K4–K6', 'Kabin kru sisi dalam (3 unit, @)', g['K4'].area(), 'priv'),
             ('T1–T4', 'Tangga spiral Ø1,50 dalam ceruk', None, 'circ'),
             ('S2.1', 'Ruang penyangga S2 (hatch → Arch 3)', None, 'node'),
             ('S2.2', 'Shaft utilitas utama', None, 'node'),
             ('S2.3', 'Peralatan darurat & APD', None, 'node')]
    # node areas (sector inside node wall)
    cw = cut_widths(1.2)
    a_band = 0.5 * math.radians(10) * ((R0 + cw['mem_out']) ** 2 - (R0 + 1.9) ** 2)
    a_band_i = 0.5 * math.radians(10) * ((R0 - 1.9) ** 2 - (R0 - cw['mem_out']) ** 2)
    a_mid = 0.5 * math.radians(10) * ((R0 + 1.8) ** 2 - (R0 - 1.8) ** 2)
    fix = {'S1.1': a_band_i, 'S1.2': a_band, 'S1.3': a_mid, 'S2.1': a_mid, 'S2.2': a_band, 'S2.3': a_band_i}
    rows = [(c, n, fix.get(c, a), z) for c, n, a, z in rows]
    yb = 440
    K.section_heading(svg, 16, yb - 2, 'TABEL RUANG & LUASAN — LANTAI DASAR', 3.0, underline=None)
    yend = room_schedule(svg, 16, yb + 7.5, rows, col_w=122, row_h=3.42, size=2.1, split=15)
    # totals
    tot_rooms = sum(g[k].area() for k in g if not k.startswith('T'))
    a_corr = 0.5 * math.radians(110) * ((R0 + 1.8) ** 2 - (R0 - 1.8) ** 2)
    tot_nodes = 2 * (a_band + a_band_i + a_mid)
    ytot = yb + 7.5 + 15 * 3.42 + 2.5
    svg.add(f'<line x1="16" y1="{ytot - 2.6}" x2="254" y2="{ytot - 2.6}" stroke="#151515" stroke-width="0.25"/>')
    svg.add(text(16, ytot + 0.6, f'Ruang Arch 1: {fmt(tot_rooms,1)} m²  ·  koridor 3,60 m: {fmt(a_corr,1)} m²  ·  node S1+S2: {fmt(tot_nodes,1)} m²  ·  '
                               f'lantai dasar total ≈ {fmt(tot_rooms + a_corr + tot_nodes, 0)} m²  (+ mezanin lihat lembar 2)',
                 size=2.05, anchor='start', weight=600))
    svg.add(text(16, ytot + 4.4, 'Luas diukur sampai muka chase utilitas (x = ±6,60 m); zona rendah di balik chase dan tangga tidak dihitung.',
                 size=1.8, anchor='start', fill='#666'))

    # symbol legend
    lx, ly = 612, 440
    K.section_heading(svg, lx, ly - 2, 'LEGENDA', 3.0)
    items1 = [('ice', 'cangkang es katenari 0,60 (terpotong +1,20)'), ('icebelow', 'kaki es di bawah bidang potong'),
              ('gap', 'celah insulasi CO₂ 0,10 m'), ('mem', 'membran inflatable ganda (2 lapis)'),
              ('chase', 'chase utilitas sudut lantai–membran'), ('reg', 'perisai karung regolit (node)'),
              ('node', 'rangka node kaku / bulkhead'), ('wall', 'partisi ringan 0,10'),
              ('acou', 'dinding akustik 0,20 (ECLSS)'), ('water', 'dinding tangki air/PE (safe room)')]
    items2 = [('glass', 'partisi kaca'), ('door', 'pintu ayun 0,90–1,20'), ('slide', 'pintu geser (pocket) 0,90'),
              ('hatch', 'hatch tekanan 1,20 (≥1,00)'), ('corr', 'lajur koridor 3,60 bebas'), ('h240', 'batas tinggi bersih 2,40 m'),
              ('floor', 'tepi lantai (membran @ ±0,00)'), ('mezz', 'tepi mezanin di atas (+3,00)'), ('axis', 'sumbu cincin R = 28,00'),
              ('cut', 'garis potong (lihat lembar 3)')]
    for i, (k, lab) in enumerate(items1):
        K.legend_row(svg, lx, ly + 6 + i * 4.3, k, lab, size=2.05)
    for i, (k, lab) in enumerate(items2):
        K.legend_row(svg, lx + 108, ly + 6 + i * 4.3, k, lab, size=2.05)

    # criteria box (center bottom)
    cx, cy = 268, 532
    K.section_heading(svg, cx, cy - 2, 'KRITERIA DIMENSI (NASA-STD-3001 / HIDH · kriteria proyek)', 2.6)
    crit = ['Koridor utama 3,60 m bersih & lurus-menerus S1 → S2; tidak ada tangga/perabot di lajur koridor.',
            'Tangga spiral T1–T4 (Ø1,50) di ceruk pita ruang luar/dalam; dua jalur keluar per sisi mezanin.',
            f'Kabin ≥ 2,40 × 3,00 m: luar {fmt(g["K1"].width(0),2)} × 3,30 · dalam {fmt(g["K4"].width(3.0),2)} × 3,00 (sisi tersempit).',
            'Pintu dalam 0,90–1,20 m; klinik pintu ganda 1,20 m (tandu); hatch tekanan 1,20 m di S1/S2.',
            'Tinggi bersih: ≥2,40 m s.d. x = ±6,25 m; di bawah mezanin 2,70 m (plat +2,70/+3,00).',
            'ECLSS dipisah dinding akustik dari kontrol, klinik & kabin; sanitasi/laundry = penyangga akustik.']
    K.para(svg, cx, cy + 3.4, crit, size=2.05, lh=1.55, bullet=True)
    nx_, ny_ = 446, 400
    K.section_heading(svg, nx_, ny_ - 2, 'CATATAN', 2.6)
    notes = ['S1 & S2 = node pemisah 2 modul (10,0°): rangka kaku,',
             'tidak dicor es, ditutup karung regolit; ruang penyangga',
             'bertekanan, hatch 1,20 m di kedua sisi → bila satu arch',
             'bocor, arch lain aman & membran/CO₂ tidak terbebani.',
             'Es hanya memikul berat sendiri; tekanan kabin dipikul',
             'membran inflatable ganda yang disegel ke rangka node.',
             'Bidang potong +1,20: es tampak 0,65 m; kaki es x = ±8,00.',
             'Mezanin +3,00 hanya modul 17–22 (garis putus) → lembar 2.',
             'Potongan A–A & B–B → lembar 3 · shaft utilitas di S2.2.']
    K.para(svg, nx_, ny_ + 3.4, notes, size=2.05, lh=1.5)
    # zone colour legend (concave left)
    zx, zy = 296, 400
    K.section_heading(svg, zx, zy - 2, 'ZONASI', 2.6)
    zones = [('node', 'node pemisah S1 / S2'), ('tech', 'kotor / teknis & logistik'), ('eclss', 'infrastruktur ECLSS (bising)'),
             ('res', 'riset, kontrol & medis'), ('comm', 'komunal, plaza & safe room'), ('grow', 'hidroponik (tertutup)'),
             ('priv', 'privat: sanitasi & kabin'), ('circ', 'sirkulasi / servis')]
    for i, (z, lab) in enumerate(zones):
        K.legend_row(svg, zx, zy + 6 + i * 4.3, ZONE[z], lab, w=7, h=3.2, size=2.05)

    K.title_block(svg, 646, 525, 183, 57, 1, 'Denah Lantai Dasar ±0,00 — Arch 1 (Early Settlement)', '1 : 100 (A1)')
    svg.save(path, 'Lembar 1 - Denah Lantai Dasar Arch 1')
    return g


def key_plan(svg, cx, cy, s=1.0, highlight=('S1', 'A1', 'S2'), title='KEY PLAN CINCIN 1 (tanpa skala)'):
    """small ring key plan, north up. s = mm per m"""
    v = View(1000 / s, cx, cy, 0)
    segs = [('S1', -5, 5, '#8c2f14'), ('A1', 5, 115, '#e3b778'), ('S2', 115, 125, '#8c2f14'),
            ('A3', 125, 235, '#dfe8d5'), ('S3', 235, 245, '#9b9b9b'), ('A2', 245, 355, '#d6e2ee')]
    for name, b1, b2, col in segs:
        hl = name in highlight
        fill = col if hl else '#f3f3f3'
        svg.add(f'<path d="{sector_d(v, 20, 36, b1, b2)}" fill="{fill}" stroke="#555" stroke-width="0.18"/>')
    for name, b1, b2, col in segs:
        bm = 0.5 * (b1 + b2)
        x, y = v.P(28, bm)
        lab = {'A1': 'ARCH 1', 'A2': 'Arch 2', 'A3': 'Arch 3'}.get(name, '')
        if lab:
            svg.add(text(x, y + 0.8, lab, size=2.0, weight=800 if name in highlight else 500, fill='#222' if name in highlight else '#888'))
    for name, b in (('S1', 0), ('S2', 120), ('S3', 240)):
        x, y = v.P(39.5, b)
        svg.add(text(x, y + 0.8, name, size=1.9, weight=700, fill='#8c2f14' if name in highlight else '#888'))
    svg.add(f'<circle cx="{cx}" cy="{cy}" r="1.2" fill="#333"/>')
    svg.add(text(cx, cy - 46, title, size=2.1, weight=800))
    svg.add(text(cx, cy + 44.5, 'U ↑ (utara ke atas) · S1 = portal utama', size=1.7, fill='#555'))


if __name__ == '__main__':
    build(sys.argv[1])
