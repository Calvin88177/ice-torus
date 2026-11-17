"""Sheet 5 - Wellness zones across Ring 1 (overlay on the full-ring plan), 1:150, A1."""
import sys, math
from core import SVG, View, R0, num, text, fmt, sector_d, arc_d, upright
from plan import defs
from furn import Ctx
import arch1, ring
import sheetkit as K
import sheet4 as S4

CATS = [
    ('fis', '#e4572e', 'AKTIVITAS FISIK', 'latihan harian ±2 jam melawan atrofi otot & tulang (g Mars 0,38)'),
    ('sos', '#f2a541', 'SOSIAL & KOMUNAL', 'makan bersama, berkumpul, acara — kohesi kru & anti-isolasi'),
    ('bio', '#4f9a3c', 'BIOFILIK / ALAM', 'tanaman hidup, kebun & ruang tanam yang bisa dikunjungi'),
    ('ten', '#3c7dbf', 'TENANG & RESTORATIF', 'membaca, belajar, menyendiri — pemulihan mental'),
    ('med', '#9b4dca', 'KESEHATAN MEDIS', 'klinik, isolasi, konseling & telemedis'),
    ('tid', '#c9b6dc', 'ISTIRAHAT PRIVAT', 'kabin pribadi: tidur 8 jam, privasi visual & akustik'),
]
COL = {c[0]: c[1] for c in CATS}

# (room dict key, source, category, short label)
A1W = [('14', 'g1', 'fis', 'Gym'), ('12', 'g1', 'sos', 'Makan & lounge'), ('13', 'g1', 'bio', 'Plaza & taman'),
       ('15', 'g1', 'bio', 'Hidroponik'), ('08', 'g1', 'med', 'Klinik'), ('09', 'g1', 'med', 'Isolasi'),
       ('18', 'm1', 'ten', 'R. tenang (+3,00)')]
A3W = [('G2', 'g3', 'bio', 'Ruang tanam A'), ('G9', 'g3', 'bio', 'Ruang tanam B'), ('G13', 'g3', 'ten', 'Istirahat kru')]
A2W = [('L1', 'g2', 'sos', 'Aula & kelas'), ('L2', 'g2', 'sos', 'Kafe & lounge'), ('L3', 'g2', 'ten', 'Perpustakaan'),
       ('L4', 'g2', 'bio', 'Plaza sosial & taman')]


def build(path):
    svg = SVG(K.W, K.H)
    v = View(S4.DEN, S4.OX, S4.OY, 0)
    defs(svg, v.s)
    svg.d('<pattern id="leakH" patternUnits="userSpaceOnUse" width="1.6" height="1.6"><rect width="1.6" height="1.6" fill="#fff"/></pattern>')
    for key, col, _, _ in CATS:
        svg.d(f'<pattern id="mz_{key}" patternUnits="userSpaceOnUse" width="1.4" height="1.4" patternTransform="rotate(45)">'
              f'<rect width="1.4" height="1.4" fill="{col}" fill-opacity="0.25"/><line x1="0" y1="0" x2="0" y2="1.4" stroke="{col}" stroke-width="0.45"/></pattern>')
    ctx = Ctx(svg, v, lw=0.85, labels=False)
    K.frame(svg)
    K.header(svg, 5, 'CINCIN 1 — ZONA WELLNESS',
             'PETA ZONA KESEHATAN FISIK & MENTAL KRU · DENAH CINCIN PENUH ±0,00 (overlay)', 'SKALA 1 : 150')
    g1, g3, g2 = ring.draw_ring(ctx)
    S4.module_ring(ctx)
    src = {'g1': g1, 'g3': g3, 'g2': g2, 'm1': arch1.rooms_mezz(), 'm2': ring.arch2_mezz()}
    # veil over the whole plan, then colour the wellness rooms
    ring._annulus(ctx, 16.9, 38.6, '#ffffff', 'fill-opacity="0.62" stroke="none"')
    areas = {c[0]: 0.0 for c in CATS}
    tags = []
    for lst in (A1W, A3W, A2W):
        for rid, s, cat, lab in lst:
            r = src[s][rid]
            sg = 1 if r.band == 'O' else -1
            Ra, Rb = sorted((R0 + sg * r.x1, R0 + sg * r.x2))
            fill = f'url(#mz_{cat})' if s.startswith('m') else COL[cat]
            op = '1' if s.startswith('m') else '0.55'
            svg.add(f'<path d="{sector_d(v, Ra, Rb, r.b1, r.b2)}" fill="{fill}" fill-opacity="{op}" stroke="{COL[cat]}" stroke-width="0.5"/>')
            areas[cat] += r.area()
            tags.append((r, cat, lab, s))
    # cabins: private rest
    for d in (g1, g2, src['m1'], src['m2']):
        for rid, r in d.items():
            if rid.startswith('K') and (d in (g1, g2)):
                sg = 1 if r.band == 'O' else -1
                Ra, Rb = sorted((R0 + sg * r.x1, R0 + sg * r.x2))
                svg.add(f'<path d="{sector_d(v, Ra, Rb, r.b1, r.b2)}" fill="{COL["tid"]}" fill-opacity="0.55" stroke="#8f78a8" stroke-width="0.25"/>')
            if rid.startswith('K'):
                areas['tid'] += r.area()
    # circadian light strip along the membrane crown (all arches)
    for b1, b2 in ring.A1, ring.A3, ring.A2:
        svg.add(f'<path d="{arc_d(v, R0, b1 + 0.5, b2 - 0.5)}" fill="none" stroke="#f4c430" stroke-width="1.6" stroke-opacity="0.85" stroke-dasharray="3,1.2"/>')
    # labels
    for r, cat, lab, s in tags:
        sg = 1 if r.band == 'O' else -1
        x, y = v.P(R0 + sg * (r.x1 + r.x2) / 2, r.bm)
        w = (len(lab) + len(r.rid) + 1) * 1.2 + 4
        svg.add(f'<rect x="{num(x - w/2)}" y="{num(y - 2.3)}" width="{num(w)}" height="4.2" rx="2.1" fill="#ffffff" stroke="{COL[cat]}" stroke-width="0.4"/>')
        svg.add(text(x, y + 0.75, f'{r.rid} {lab}', size=1.95, weight=800, fill='#222'))
    # yard captions
    tx, ty = v.P(0, 0)
    svg.add(f'<circle cx="{num(tx)}" cy="{num(ty)}" r="{num(v.L(0.55))}" fill="#3a3a3a"/>')
    svg.add(text(tx, ty + 6, 'MENARA POMPA PUSAT (0,0)', size=2.2, weight=800))
    for b, t1, t2 in ((60, 'ARCH 1 · CORE', 'gym, klinik, plaza, makan bersama'),
                      (180, 'ARCH 3 · GROW & MAKE', 'ruang tanam yang bisa dikunjungi'),
                      (300, 'ARCH 2 · LIVING', 'kafe, plaza, perpustakaan, aula')):
        x, y = v.P(10.5, b)
        svg.add(text(x, y, t1, size=3.2, weight=800))
        svg.add(text(x, y + 3.6, t2, size=2.0, fill='#555'))
    x, y = v.P(14.2, 0)
    svg.add(text(x, y, 'garis kuning = pita cahaya sirkadian di puncak membran (menerus di tiap arch)', size=1.8, fill='#9a7400', weight=700))
    K.north_arrow(svg, 34, 72, -90, size=8)
    K.scale_bar(svg, 22, 566, v.s, ticks=(0, 1, 2, 5, 10, 20), label='skala grafis 1:150 (m)')

    # ---- right column: legend + table + principles
    x0, x1 = S4.CX0, S4.CX1
    y = 54
    K.section_heading(svg, x0, y, 'KATEGORI ZONA WELLNESS', 3.0)
    y += 7
    for key, col, t, d in CATS:
        svg.add(f'<rect x="{x0}" y="{num(y - 3)}" width="9" height="5" fill="{col}" fill-opacity="0.55" stroke="{col}" stroke-width="0.4"/>')
        svg.add(text(x0 + 12, y, t, size=2.7, anchor='start', weight=800))
        svg.add(text(x0 + 12, y + 3.6, d, size=2.2, anchor='start', fill='#444'))
        y += 11
    svg.add(f'<rect x="{x0}" y="{num(y - 3)}" width="9" height="4.4" fill="url(#mz_ten)" stroke="{COL["ten"]}" stroke-width="0.4"/>')
    svg.add(text(x0 + 12, y, 'arsir = di mezanin +3,00 (bukan lantai dasar)', size=2.0, anchor='start', weight=600))
    y += 7
    svg.add(f'<line x1="{x0}" y1="{num(y-0.8)}" x2="{x0+9}" y2="{num(y-0.8)}" stroke="#f4c430" stroke-width="1.6" stroke-dasharray="3,1.2"/>')
    svg.add(text(x0 + 12, y, 'pita cahaya sirkadian (spektrum pagi → sore → malam)', size=2.0, anchor='start', weight=600))
    y += 10

    K.section_heading(svg, x0, y, 'DAFTAR RUANG WELLNESS', 3.0)
    y += 7
    cols = [('NO', 14, 'start'), ('RUANG', 70, 'start'), ('ARCH', 26, 'start'), ('KATEGORI', 90, 'start'), ('m²', 20, 'end')]
    rows = []
    names = {'g1': 'Arch 1', 'm1': 'Arch 1', 'g3': 'Arch 3', 'g2': 'Arch 2'}
    catname = {c[0]: c[2].title() for c in CATS}
    for r, cat, lab, s in tags:
        rows.append((r.rid, lab, names[s], catname[cat], fmt(r.area(), 1)))
    rows.append(('K1–K60', '60 kabin pribadi', '1 & 2', catname['tid'], fmt(areas['tid'], 0)))
    y = S4.table(svg, x0, y, cols, rows, size=2.25, row_h=4.4) + 3
    tot = sum(areas.values())
    svg.add(text(x0, y, f'Total ruang wellness ±{fmt(tot, 0)} m² (termasuk kabin) · tanpa kabin ±{fmt(tot - areas["tid"], 0)} m² ≈ '
                 f'{fmt((tot - areas["tid"]) / 60, 1)} m²/orang untuk 60 penghuni', size=2.1, anchor='start', weight=700))
    y += 10

    K.section_heading(svg, x0, y, 'PRINSIP PENEMPATAN', 3.0)
    notes = ['Setiap arch punya minimal satu ruang komunal + satu ruang hijau → tak ada penghuni yang jauh dari wellness.',
             'Gym di Arch 1 bersebelahan dengan sanitasi/shower (16) dan jauh dari kabin & ruang tenang (bising, getar).',
             'Ruang tenang (18, L3, G13) dipisah dari zona bising ECLSS & fabrikasi oleh dinding akustik / jarak.',
             'Plaza 13 & L4 = void tinggi penuh 8,30 m di bawah pita cahaya sirkadian → "ruang luar" semu.',
             'Ruang tanam G2/G9 dirancang bisa dikunjungi (dinding kaca ke koridor) sebagai terapi hortikultura.',
             'Klinik & isolasi (08–09) di sisi koridor untuk akses tandu; konseling/telemedis di klinik.',
             'Loop koridor 3,60 m 360° (±176 m) juga berfungsi sebagai lintasan jalan/lari ringan.']
    K.para(svg, x0, y + 6.5, notes, size=2.15, lh=1.6, bullet=True)
    K.title_block(svg, 646, 525, 183, 57, 5, 'Zona Wellness Cincin 1 — overlay denah ±0,00', '1 : 150 (A1)')
    svg.save(path, 'Lembar 5 - Zona Wellness Cincin 1')


if __name__ == '__main__':
    build(sys.argv[1])
