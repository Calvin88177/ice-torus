"""Arch 1 - Early Settlement: rooms, furniture, walls, doors (ground floor + mezzanine)."""
import math
from core import (R0, X_FLOOR, X_CHASE, X_CORR, WALL, MOD, cut_widths, num, path_poly, style, text,
                  arc_d, sector_d, radial_d, fmt, MEZ_EDGE)
from plan import (ZONE, CORR, WALL_C, HATCH_C, ang_of, Rx, wall_arc, wall_rad, glass_arc, door_on_arc, door_on_rad,
                  spiral_stair, room_tag, sector_area, draw_shell, draw_chase, draw_node, node_bulkhead, draw_ground)
import furn as F

HG = 1.2
CW = 1.85            # corridor wall centre offset
XF = 1.90            # corridor wall face (room side)
CORR_FILL = '#efeeea'

# mezzanine geometry
SLOT = 0.30          # half width of light slot
RAIL = 0.33          # railing outer face
MZ_IN = 1.42         # cabin inner face (walkway side)
MZ_OUT = 4.42        # cabin back face
MZ_EDGE = 4.50
STAIR_X = 2.75
STAIR_D = 1.50


class Room:
    def __init__(s, rid, name, band, b1, b2, x1=XF, x2=X_CHASE, zone='tech', closed=True, corr_wall=True,
                 acoustic=(), back=False, level='G', tag=None, short=None, glass_corr=False, area_x2=None):
        s.rid, s.name, s.band, s.b1, s.b2, s.x1, s.x2 = rid, name, band, b1, b2, x1, x2
        s.zone, s.closed, s.corr_wall, s.acoustic, s.back, s.level = zone, closed, corr_wall, acoustic, back, level
        s.tag, s.short, s.glass_corr = tag, short, glass_corr
        s.area_x2 = area_x2 if area_x2 is not None else x2

    @property
    def bm(s):
        return 0.5 * (s.b1 + s.b2)

    def R(s, x):
        return Rx(s.band, x)

    def area(s):
        R1, R2 = s.R(s.x1), s.R(s.area_x2)
        a = sector_area(R1, R2, s.b1, s.b2)
        # subtract half partitions on both sides
        a -= WALL / 2 * abs(R2 - R1) * 2
        return a

    def frame(s, view, side='b1', x=None):
        x = s.x1 if x is None else x
        Rf = s.R(x)
        rv = 1 if s.band == 'O' else -1
        if side == 'b1':
            return view.local(Rf, s.b1 + math.degrees((WALL / 2) / Rf), 1, rv)
        if side == 'b2':
            return view.local(Rf, s.b2 - math.degrees((WALL / 2) / Rf), -1, rv)
        return view.local(Rf, s.bm, 1, rv)

    def width(s, v):
        """clear width (m) at depth v from x1"""
        Rr = s.R(s.x1 + v)
        return math.radians(s.b2 - s.b1) * Rr - WALL


# ---------------------------------------------------------------- program (ground floor)
def rooms_ground():
    O, I = 'O', 'I'
    L = [
        Room('01', 'Dekontaminasi & Loker APD', I, 5, 11, zone='tech'),
        Room('02', 'Gudang & Logistik', O, 5, 20, zone='tech'),
        Room('03', 'Bengkel & Perawatan Peralatan', I, 11, 20, zone='tech'),
        Room('04', 'ECLSS A — Pemurnian Air & Elektrolisis O₂', O, 20, 35, zone='eclss', acoustic=('corr', 'b2')),
        Room('05', 'ECLSS B — Termal, Baterai & Distribusi Listrik', I, 20, 35, zone='eclss', acoustic=('corr', 'b2')),
        Room('06', 'Pusat Kontrol & Komunikasi', O, 35, 42.5, zone='res'),
        Room('07', 'Lab Basah & Analisis Geologi/Biologi', O, 42.5, 50, zone='res'),
        Room('08', 'Klinik Medis', I, 35, 44.5, zone='res'),
        Room('09', 'Ruang Isolasi + KM Isolasi', I, 44.5, 50, zone='res'),
        Room('10', 'Safe Room / Shelter Badai Matahari (15 org)', I, 50, 60, zone='comm'),
        Room('11', 'Galley (Dapur)', O, 50, 60, zone='comm', closed=False, corr_wall=False),
        Room('12', 'Ruang Makan Bersama & Lounge', O, 60, 75, zone='comm', closed=False, corr_wall=False),
        Room('13', 'Plaza Komunal & Taman Sosial', I, 60, 75, zone='comm', closed=False, corr_wall=False),
        Room('14', 'Gym / Ruang Olahraga', O, 75, 85, zone='comm', glass_corr=True),
        Room('15', 'Hidroponik (ruang tertutup)', I, 75, 85, zone='grow'),
        Room('16', 'Sanitasi Bersama', O, 85, 93, zone='priv'),
        Room('17', 'Laundry & Linen', I, 85, 88.0, zone='priv'),
        Room('T1', 'Tangga spiral T1', O, 93, 96.5, x2=3.80, zone='circ', corr_wall=False, back=True),
        Room('K1', 'Kabin kru K1', O, 96.5, 101.5, x2=5.20, zone='priv', back=True),
        Room('K2', 'Kabin kru K2', O, 101.5, 106.5, x2=5.20, zone='priv', back=True),
        Room('K3', 'Kabin kru K3', O, 106.5, 111.5, x2=5.20, zone='priv', back=True),
        Room('T3', 'Tangga spiral T3', O, 111.5, 115, x2=3.80, zone='circ', corr_wall=False, back=True),
        Room('T2', 'Tangga spiral T2', I, 88.0, 92.0, x2=3.80, zone='circ', corr_wall=False, back=True),
        Room('K4', 'Kabin kru K4', I, 92.0, 98.3, x2=4.90, zone='priv', back=True),
        Room('K5', 'Kabin kru K5', I, 98.3, 104.6, x2=4.90, zone='priv', back=True),
        Room('K6', 'Kabin kru K6', I, 104.6, 110.9, x2=4.90, zone='priv', back=True),
        Room('T4', 'Tangga spiral T4', I, 110.9, 115, x2=3.80, zone='circ', corr_wall=False, back=True),
    ]
    return {r.rid: r for r in L}


STAIRS = {'T1': ('O', 94.75), 'T3': ('O', 113.25), 'T2': ('I', 90.0), 'T4': ('I', 112.95)}

# storage behind stair bays / cabins (low zones)
BACK_STORES = [('O', 93, 96.5, 3.80), ('O', 111.5, 115, 3.80), ('I', 88.0, 92.0, 3.80), ('I', 110.9, 115, 3.80)]


def rooms_mezz():
    O, I = 'O', 'I'
    L = [
        Room('18', 'Ruang Tenang / Perpustakaan Mini', O, 85, 93, x1=MZ_IN, x2=MZ_OUT, zone='priv', back=True, level='M'),
        Room('K7', 'Kabin kru K7', O, 96.5, 101.5, x1=MZ_IN, x2=MZ_OUT, zone='priv', back=True, level='M'),
        Room('K8', 'Kabin kru K8', O, 101.5, 106.5, x1=MZ_IN, x2=MZ_OUT, zone='priv', back=True, level='M'),
        Room('K9', 'Kabin kru K9', O, 106.5, 111.5, x1=MZ_IN, x2=MZ_OUT, zone='priv', back=True, level='M'),
        Room('19', 'Linen & Penyimpanan', I, 85, 88.0, x1=MZ_IN, x2=MZ_OUT, zone='priv', back=True, level='M'),
        Room('K10', 'Kabin kru K10', I, 92.0, 98.3, x1=MZ_IN, x2=MZ_OUT, zone='priv', back=True, level='M'),
        Room('K11', 'Kabin kru K11', I, 98.3, 104.6, x1=MZ_IN, x2=MZ_OUT, zone='priv', back=True, level='M'),
        Room('K12', 'Kabin kru K12', I, 104.6, 110.9, x1=MZ_IN, x2=MZ_OUT, zone='priv', back=True, level='M'),
    ]
    return {r.rid: r for r in L}


# ---------------------------------------------------------------- generic room drawing
def fill_room(ctx, r, fill=None, x2=None, op=1.0):
    v = ctx.view
    x2 = r.x2 if x2 is None else x2
    col = fill or ZONE.get(r.zone, '#ffffff')
    ctx.svg.add(f'<path d="{sector_d(v, min(r.R(r.x1), r.R(x2)), max(r.R(r.x1), r.R(x2)), r.b1, r.b2)}" fill="{col}" '
                f'stroke="none" opacity="{op}"/>')


def walls_room(ctx, r, h=HG, x_wall_end=None):
    cw = cut_widths(h)
    xe = cw['mem_in'] if x_wall_end is None else x_wall_end
    sgn = 1 if r.band == 'O' else -1
    if r.corr_wall and r.level == 'G':
        if r.glass_corr:
            glass_arc(ctx, R0 + sgn * CW, r.b1, r.b2)
        else:
            wall_arc(ctx, R0 + sgn * CW, r.b1, r.b2, t=WALL if 'corr' not in r.acoustic else 0.20,
                     acoustic='corr' in r.acoustic)
    if r.closed or r.back:
        x0 = CW - 0.05 if r.level == 'G' else MZ_IN - 0.08
        xend = r.x2 + 0.1 if r.back else xe
        for side, b in (('b1', r.b1), ('b2', r.b2)):
            ac = side in r.acoustic
            wall_rad(ctx, b, R0 + sgn * x0, R0 + sgn * xend, t=0.20 if ac else WALL, acoustic=ac)
    if r.back:
        wall_arc(ctx, r.R(r.x2 + 0.05), r.b1, r.b2)


# ---------------------------------------------------------------- furniture per room
def furnish_ground(ctx, rooms):
    v = ctx.view
    g = rooms

    # 01 decon & PPE lockers (inner, 5..11)
    r = g['01']
    f = r.frame(v, 'b1')
    F.shower(ctx, f, 0.08, 0.35, 1.08, 1.35)                 # decon shower beside hatch from suit-lock
    F.label(ctx, f, 0.58, 1.55, 'dekon', 1.3)
    F.rack(ctx, f, 0.05, 1.75, 0.55, 4.45, fill='#f5efe2')    # PPE lockers along node bulkhead
    F.label(ctx, f, 0.30, 3.1, 'loker APD', 1.2, rot=90)
    f2 = r.frame(v, 'b2')
    F.rect(ctx, f2, 0.05, 2.0, 0.45, 4.0, fill='#f5efe2')   # bench
    F.sink(ctx, f2, 0.32, 1.0, 0.45, 0.4)
    F.rect(ctx, f2, 0.05, 4.2, 0.65, 4.6, fill='#eceff1')    # HEPA / dirty bin

    # 02 storage & logistics (outer 5..20)
    r = g['02']
    for b in (8.6, 12.4, 16.2):
        f = v.local(r.R(2.9), b, 1, 1)
        F.shelves(ctx, f, -0.32, 0.0, 0.32, 3.1, n=7)
    f = r.frame(v, 'b2')
    F.rect(ctx, f, 0.05, 3.0, 0.65, 4.4, fill='#f5efe2')      # pallet bay
    F.label(ctx, f, 0.35, 3.75, 'palet', 1.1, rot=90)
    F.desk(ctx, f, 0.05, 0.35, 0.65, 1.35, chair_side='u+')     # inventory desk

    # 03 workshop (inner 11..20)
    r = g['03']
    f = r.frame(v, 'b1')
    F.counter(ctx, f, 0.05, 0.6, 0.75, 3.9)                   # workbench along partition
    F.label(ctx, f, 0.4, 2.2, 'meja kerja', 1.2, rot=90)
    F.chair(ctx, f, 1.05, 1.6, back='u+')
    F.chair(ctx, f, 1.05, 3.0, back='u+')
    f2 = r.frame(v, 'b2')
    F.rack(ctx, f2, 0.05, 0.4, 0.75, 1.4, label='3D')          # 3D printer
    F.rack(ctx, f2, 0.05, 1.6, 0.75, 2.6, label='CNC')
    F.shelves(ctx, f2, 0.05, 2.8, 0.55, 4.3, n=4)              # tool cabinet
    F.suit(ctx, f, 1.9, 3.6, s=0.9, fill='#fff6e8')            # suit repair stand
    F.label(ctx, f, 1.9, 4.25, 'servis suit', 1.1)

    # 04 ECLSS A (outer 20..35): water & O2
    r = g['04']
    f = r.frame(v, 'b1')
    F.tank(ctx, f, 0.75, 1.15, 0.55, 'H₂O')
    F.tank(ctx, f, 0.75, 2.45, 0.55, 'H₂O')
    F.rack(ctx, f, 0.1, 3.3, 1.3, 4.3, fill='#e3ecf5', label='WPA')
    fm = r.frame(v, 'mid')
    F.rack(ctx, fm, -1.6, 2.4, -0.5, 3.4, fill='#e3ecf5', label='OGA')
    F.rack(ctx, fm, -0.2, 2.4, 0.9, 3.4, fill='#e3ecf5', label='CDRA')
    F.rack(ctx, fm, 1.2, 2.4, 2.3, 3.4, fill='#e3ecf5', label='SAB')
    F.rack(ctx, fm, -0.9, 3.8, 1.6, 4.4, fill='#eef0f2', label='tangki O₂/N₂', size=1.2)
    f2 = r.frame(v, 'b2')
    F.rack(ctx, f2, 0.25, 0.4, 0.95, 1.6, fill='#eef0f2', label='UPA', size=1.3)

    # 05 ECLSS B (inner 20..35): thermal, battery, power
    r = g['05']
    f = r.frame(v, 'b1')
    for k in range(3):
        F.rack(ctx, f, 0.08, 0.5 + k * 1.15, 0.78, 1.5 + k * 1.15, fill='#f1ecf7', label='BAT', size=1.2)
    fm = r.frame(v, 'mid')
    F.rack(ctx, fm, -0.9, 2.3, 0.4, 3.2, fill='#f1ecf7', label='PDU')
    F.rack(ctx, fm, 0.7, 2.3, 1.8, 3.2, fill='#e3ecf5', label='PPA')
    F.tank(ctx, fm, 0.2, 3.9, 0.38, None)
    F.label(ctx, fm, 1.15, 4.0, 'akumulator', 1.1)
    f2 = r.frame(v, 'b2')
    F.rack(ctx, f2, 0.1, 0.45, 0.8, 1.45, fill='#fdeaea', label='FSS', size=1.2)

    # 06 control & comms (outer 35..42.5): curved console along the concave outer wall
    r = g['06']
    b1, b2 = r.b1 + 1.1, r.b2 - 1.1
    Rc1, Rc2 = r.R(4.95), r.R(5.65)
    ctx.svg.add(f'<path d="{sector_d(v, Rc1, Rc2, b1, b2)}" fill="#e9edf1" stroke="#3a3a3a" stroke-width="{num(0.14*ctx.lw)}"/>')
    ctx.svg.add(f'<path d="{arc_d(v, r.R(5.62), b1 + 0.4, b2 - 0.4)}" fill="none" stroke="#4a5866" stroke-width="{num(v.L(0.06))}"/>')
    for b in (b1 + 1.25, 0.5 * (b1 + b2), b2 - 1.25):
        fc = v.local(r.R(4.55), b, 1, 1)
        F.chair(ctx, fc, 0, 0, back='v-')
    f = r.frame(v, 'b1')
    F.screen(ctx, f, 0.05, 1.0, 0.14, 2.8)
    F.rack(ctx, f, 0.05, 3.1, 0.65, 3.9, fill='#eef0f2', label='COM', size=1.2)
    fm = r.frame(v, 'mid')
    F.table_round(ctx, fm, 0.35, 1.55, 0.5, chairs=3)

    # 07 wet lab (outer 42.5..50)
    r = g['07']
    fm = r.frame(v, 'mid')
    F.counter(ctx, fm, -0.45, 1.2, 0.45, 3.2, fill='#f2f5f7')       # island bench
    F.sink(ctx, fm, 0, 2.95, 0.4, 0.3)
    for vv in (1.5, 2.3):
        F.round_chair(ctx, fm, -0.75, vv, 0.18)
        F.round_chair(ctx, fm, 0.75, vv, 0.18)
    F.glovebox(ctx, fm, -0.8, 3.75, 0.6, 4.35, gloves='v-')
    F.label(ctx, fm, -0.1, 3.52, 'glovebox regolit', 1.05)
    f = r.frame(v, 'b1')
    F.counter(ctx, f, 0.05, 0.3, 0.6, 1.0)
    F.fridge(ctx, f, 0.05, 3.6, 0.65, 4.2, lab='-80')
    f2 = r.frame(v, 'b2')
    F.rack(ctx, f2, 0.05, 0.35, 0.65, 1.2, fill='#f2f5f7', label='FH', size=1.2)

    # 08 clinic (inner 35..44.5)
    r = g['08']
    fm = r.frame(v, 'mid')
    F.rrect(ctx, fm, -0.4, 1.4, 0.4, 3.3, 0.12, fill='#ffffff', sw=0.16)     # exam bed
    F.rrect(ctx, fm, -0.3, 1.5, 0.3, 1.85, 0.08, fill='#f0f0f0', sw=0.08)
    F.label(ctx, fm, 0, 2.6, 'periksa', 1.1, rot=90)
    F.rect(ctx, fm, 0.75, 1.9, 1.25, 2.5, fill='#eef3f6')                   # diagnostic cart
    F.label(ctx, fm, 1.0, 2.75, 'USG', 1.0)
    f = r.frame(v, 'b1')
    F.shelves(ctx, f, 0.05, 0.6, 0.5, 2.6, n=4, fill='#eef3f6')
    F.sink(ctx, f, 0.3, 3.0, 0.4, 0.4)
    F.desk(ctx, f, 0.05, 3.5, 0.6, 4.3, chair_side='u+')
    F.label(ctx, fm, -0.1, 4.25, 'obat & alat', 1.0)

    # 09 isolation + bathroom (inner 44.5..50)
    r = g['09']
    f = r.frame(v, 'b2')
    F.bed(ctx, f, 0.08, 0.6, L=2.0, W=0.9, head='v+')
    F.chair(ctx, f, 1.35, 1.2, back='u+')
    f2 = r.frame(v, 'b1')
    F.wc(ctx, f2, 0.3, 4.25, ang='v+')
    F.sink(ctx, f2, 1.15, 4.3, 0.45, 0.35)
    F.shower(ctx, f2, 1.55, 3.55, 2.25, 4.4)

    # 10 safe room (inner 50..60): water-wall lining + 15 seats
    r = g['10']
    sgn = -1
    lin = 0.32
    bd1, bd2 = 58.0 - math.degrees(0.55 / r.R(XF)), 58.0 + math.degrees(0.55 / r.R(XF))
    for (ba, bb) in ((r.b1, bd1), (bd2, r.b2)):
        ctx.svg.add(f'<path d="{sector_d(v, r.R(XF + lin), r.R(XF), ba, bb)}" fill="url(#waterH)" stroke="#4a86b5" stroke-width="{num(0.1*ctx.lw)}"/>')
    ctx.svg.add(f'<path d="{sector_d(v, r.R(X_CHASE), r.R(X_CHASE - lin), r.b1, r.b2)}" fill="url(#waterH)" stroke="#4a86b5" stroke-width="{num(0.1*ctx.lw)}"/>')
    for b, d in ((r.b1, 1), (r.b2, -1)):
        bb = b + d * math.degrees(lin / r.R(4.2))
        ctx.svg.add(f'<path d="{sector_d(v, r.R(X_CHASE - lin), r.R(XF + lin), min(b, bb), max(b, bb))}" fill="url(#waterH)" stroke="#4a86b5" stroke-width="{num(0.1*ctx.lw)}"/>')
    # seats (fold-down) around the inside
    f = r.frame(v, 'b1')
    for k in range(5):
        F.rect(ctx, f, 0.40, 0.75 + k * 0.72, 0.85, 1.3 + k * 0.72, fill='#fff7e0', sw=0.08)
    f2 = r.frame(v, 'b2')
    for k in range(5):
        F.rect(ctx, f2, 0.40, 0.75 + k * 0.72, 0.85, 1.3 + k * 0.72, fill='#fff7e0', sw=0.08)
    fm = r.frame(v, 'mid', x=X_CHASE - lin - 0.05)
    for k in range(5):
        F.rect(ctx, fm, -1.45 + k * 0.62, 0.05, -0.95 + k * 0.62, -0.42, fill='#fff7e0', sw=0.08)
    fm2 = r.frame(v, 'mid')
    F.rect(ctx, fm2, -0.55, 1.6, 0.55, 2.6, fill='#eef3f6')
    F.label(ctx, fm2, 0, 2.15, 'logistik', 1.1)
    F.label(ctx, fm2, 0, 2.95, '15 kursi lipat', 1.05)

    # 11 galley (outer 50..60), open to corridor
    r = g['11']
    f = r.frame(v, 'b1')
    F.counter(ctx, f, 0.05, 0.9, 0.7, 4.3)                    # counter along partition
    F.cooktop(ctx, f, 0.38, 1.9, 0.5, 0.6)
    F.sink(ctx, f, 0.38, 3.0, 0.45, 0.5)
    F.fridge(ctx, f, 0.05, 4.4, 0.75, 4.95, lab='K')
    fb = r.frame(v, 'mid', x=5.25)
    F.counter(ctx, fb, -1.9, 0, 1.6, 0.6)                      # back counter (low headroom zone OK)
    F.fridge(ctx, fb, 1.65, 0, 2.25, 0.6, lab='B')
    F.rect(ctx, fb, -1.5, 0.05, -0.9, 0.55, fill='#ffffff', sw=0.08)   # oven
    F.label(ctx, fb, -1.2, 0.35, 'oven', 0.9)
    fm = r.frame(v, 'mid')
    F.counter(ctx, fm, -0.7, 1.5, 1.3, 2.4, fill='#f6efe2')    # island / serving counter
    F.sink(ctx, fm, 0.9, 1.95, 0.35, 0.35)
    for uu in (-0.4, 0.3, 1.0):
        F.round_chair(ctx, fm, uu, 1.18, 0.17)
    f2 = r.frame(v, 'b2')
    F.shelves(ctx, f2, 0.05, 2.6, 0.5, 4.2, n=4)              # pantry shelves

    # 12 dining & lounge (outer 60..75) - open, organic alcoves
    r = g['12']
    fm = v.local(r.R(3.75), 64.2, 1, 1)
    F.ellipse(ctx, fm, 0, 0, 1.75, 0.62, fill='#ffffff', sw=0.16)        # oval dining table (12)
    for k in range(5):
        uu = -1.4 + k * 0.7
        F.chair(ctx, fm, uu, -0.88, back='v-')
        F.chair(ctx, fm, uu, 0.88, back='v+')
    F.chair(ctx, fm, -2.1, 0, back='u-')
    F.chair(ctx, fm, 2.1, 0, back='u+')
    # curved sofa lounge alcove near the outer wall
    bL1, bL2 = 69.4, 73.6
    ctx.svg.add(f'<path d="{sector_d(v, r.R(5.15), r.R(5.85), bL1, bL2)}" fill="#efe3cf" stroke="#3a3a3a" stroke-width="{num(0.14*ctx.lw)}"/>')
    ctx.svg.add(f'<path d="{sector_d(v, r.R(5.55), r.R(5.85), bL1, bL2)}" fill="#e2d1b5" stroke="#3a3a3a" stroke-width="{num(0.08*ctx.lw)}"/>')
    fl = v.local(r.R(4.25), 71.5, 1, 1)
    F.ellipse(ctx, fl, 0, 0, 0.7, 0.4, fill='#ffffff', sw=0.12)
    F.round_chair(ctx, fl, -1.15, -0.45, 0.3)
    F.round_chair(ctx, fl, 1.15, -0.45, 0.3)
    # organic partition fins (curved planter walls) - alcoves along the wall, corridor untouched
    fin(ctx, 'O', [(2.35, 60.5), (3.3, 61.15), (4.35, 60.7)])
    fin(ctx, 'O', [(2.6, 68.0), (3.9, 68.9), (5.1, 68.35), (6.1, 68.8)])
    fin(ctx, 'O', [(2.5, 74.55), (3.8, 73.95), (4.9, 74.4)])
    for (b, x) in ((68.75, 3.15), (61.0, 4.6), (74.3, 5.15)):
        F.plant(ctx, v.local(r.R(x), b, 1, 1), 0, 0, 0.32)

    # 13 plaza garden (inner 60..75)
    r = g['13']
    for (b, x, rr) in ((62.9, 3.8, 1.0), (68.55, 4.15, 1.05), (73.2, 3.05, 0.75)):
        F.tree(ctx, v.local(r.R(x), b, 1, -1), 0, 0, rr)
    fin(ctx, 'I', [(2.45, 66.1), (3.6, 65.25), (4.8, 65.7), (6.05, 65.2)])
    fin(ctx, 'I', [(2.4, 71.3), (3.7, 72.1), (4.9, 71.55), (6.05, 72.0)])
    # bench alcoves along the wall
    for (bb1, bb2) in ((60.7, 64.7), (66.5, 70.9), (72.6, 74.6)):
        ctx.svg.add(f'<path d="{sector_d(v, r.R(5.6), r.R(6.02), bb1, bb2)}" fill="#efe3cf" stroke="#3a3a3a" stroke-width="{num(0.12*ctx.lw)}"/>')
    fk = v.local(r.R(2.75), 69.0, 1, -1)
    F.ellipse(ctx, fk, 0, 0, 0.45, 0.32, fill='#ffffff', sw=0.1)
    for a in (0, 120, 240):
        F.round_chair(ctx, fk, 0.8 * math.cos(math.radians(a)), 0.58 * math.sin(math.radians(a)), 0.19)
    for (b, x) in ((64.4, 2.55), (70.5, 5.15), (61.4, 5.1), (74.3, 4.4)):
        F.plant(ctx, v.local(r.R(x), b, 1, -1), 0, 0, 0.3)

    # 14 gym (outer 75..85)
    r = g['14']
    f = r.frame(v, 'b1')
    F.treadmill(ctx, f, 0.2, 0.9, L=2.1, W=0.85, along='v')
    F.label(ctx, f, 0.62, 3.3, 'treadmill', 1.05)
    F.label(ctx, f, 0.62, 3.55, '+ harness', 1.05)
    F.bike(ctx, f, 1.6, 1.0, along='v')
    f2 = r.frame(v, 'b2')
    F.resistance(ctx, f2, 0.15, 0.9, 1.25, 2.6)
    F.label(ctx, f2, 0.7, 2.95, 'ARED', 1.1)
    F.screen(ctx, f2, 0.05, 3.3, 0.12, 4.2)
    fm = r.frame(v, 'mid', x=5.0)
    F.mat(ctx, fm, -1.25, -0.6, 1.0, 0.75)
    F.label(ctx, fm, -0.1, 0.1, 'matras', 1.0)

    # 15 hydroponics (inner 75..85): closed, vertical tiered racks
    r = g['15']
    for b in (78.0, 80.6, 83.2):
        fr_ = v.local(r.R(2.9), b, 1, -1)
        F.hydro_rack(ctx, fr_, -0.3, 0.0, 0.3, 2.55)
    f = r.frame(v, 'b1')
    F.counter(ctx, f, 0.05, 3.6, 1.6, 4.25, fill='#f2f8ee')                 # nutrient work table
    F.label(ctx, f, 0.85, 3.95, 'meja nutrien', 1.05)
    F.tank(ctx, f, 2.25, 4.0, 0.3, None)
    fm = r.frame(v, 'mid')
    F.label(ctx, fm, 0, 4.85, 'rak tanam vertikal 4 tingkat · LED spektrum tumbuh', 1.0)

    # 16 sanitation (outer 85..93)
    r = g['16']
    f = r.frame(v, 'b1')
    # two WC cubicles along partition b1
    for k, v0 in enumerate((0.25, 1.65)):
        F.rect(ctx, f, 0.05, v0, 1.25, v0 + 1.3, fill='#fafafa', sw=0.1)
        F.wc(ctx, f, 0.2, v0 + 0.65, ang='u-')
    F.label(ctx, f, 0.75, 3.15, 'WC vakum', 1.0)
    # two showers at the back
    F.shower(ctx, f, 0.1, 3.4, 1.15, 4.45)
    F.shower(ctx, f, 1.25, 3.4, 2.3, 4.45)
    f2 = r.frame(v, 'b2')
    F.counter(ctx, f2, 0.05, 1.2, 0.6, 3.0, fill='#f7f7f7')               # vanity
    F.sink(ctx, f2, 0.32, 1.65, 0.4, 0.35)
    F.sink(ctx, f2, 0.32, 2.55, 0.4, 0.35)

    # 17 laundry (inner 85..88)
    r = g['17']
    f = r.frame(v, 'b1')
    F.washer(ctx, f, 0.4, 1.0, 0.6)
    F.washer(ctx, f, 0.4, 1.65, 0.6)
    F.counter(ctx, f, 0.08, 2.1, 0.7, 3.2)
    F.shelves(ctx, f, 0.08, 3.4, 0.7, 4.4, n=3)

    # cabins
    for k in ('K1', 'K2', 'K3'):
        cabin(ctx, g[k])
    for k in ('K4', 'K5', 'K6'):
        cabin(ctx, g[k])

    # storage behind stair bays (low zone)
    for band, b1, b2, x0 in BACK_STORES:
        sgn = 1 if band == 'O' else -1
        f = v.local(R0 + sgn * (x0 + 0.15), 0.5 * (b1 + b2), 1, sgn)
        F.shelves(ctx, f, -0.55, 0.15, 0.55, 0.65, n=3)


def fin(ctx, band, ctrl, t=0.13, color='#5a4a3a'):
    """organic curved partition through control points (x, b) - Catmull-Rom"""
    v = ctx.view
    sgn = 1 if band == 'O' else -1
    P = [v.P(R0 + sgn * x, b) for x, b in ctrl]
    pts_ = []
    ext = [P[0]] + P + [P[-1]]
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        for k in range(12):
            tt = k / 12
            t2, t3 = tt * tt, tt * tt * tt
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * tt + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * tt + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            pts_.append((x, y))
    pts_.append(P[-1])
    d = path_poly(pts_, False)
    ctx.svg.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{num(v.L(t))}" stroke-linecap="round" stroke-linejoin="round"/>')
    ctx.svg.add(f'<path d="{d}" fill="none" stroke="#e9dcc6" stroke-width="{num(v.L(t)*0.45)}" stroke-linecap="round" stroke-linejoin="round"/>')


def cabin(ctx, r, mezz=False):
    v = ctx.view
    f = r.frame(v, 'b1')
    depth = r.x2 - r.x1
    F.wardrobe(ctx, f, 0.05, 0.08, 0.95, 0.66)
    F.bed(ctx, f, 0.05, depth - 2.05, L=2.0, W=0.9, head='v+')
    w_back = r.width(depth)
    F.desk(ctx, f, 1.15, depth - 0.62, min(2.35, w_back - 0.1), depth - 0.05)
    F.chair(ctx, f, 0.5 * (1.15 + min(2.35, w_back - 0.1)), depth - 0.95, back='v-')


# ---------------------------------------------------------------- doors (ground)
def doors_ground(ctx, g):
    v = ctx.view
    RO, RI = R0 + CW, R0 - CW

    def dc(r, b, w, kind='swing', hinge='-'):
        R = RO if r.band == 'O' else RI
        into = 1 if r.band == 'O' else -1
        door_on_arc(ctx, R, b, w, into, kind=kind, hinge=hinge, t=0.2 if 'corr' in r.acoustic else WALL)

    dc(g['01'], 9.4, 1.0, 'swing', '+')
    dc(g['02'], 17.4, 1.6, 'double')
    dc(g['03'], 13.2, 1.2, 'swing', '-')
    dc(g['04'], 22.8, 1.2, 'double')
    dc(g['05'], 23.0, 1.0, 'swing', '-')
    dc(g['06'], 37.2, 0.9, 'swing', '-')
    dc(g['07'], 48.0, 1.0, 'swing', '+')
    dc(g['08'], 37.6, 1.2, 'double')           # stretcher access 1.20
    dc(g['10'], 58.0, 1.0, 'swing', '+')
    dc(g['14'], 76.9, 1.0, 'swing', '-')
    dc(g['15'], 83.0, 1.0, 'slide')
    dc(g['16'], 91.0, 0.9, 'swing', '+')
    dc(g['17'], 86.5, 0.9, 'slide')
    for k in ('K1', 'K2', 'K3', 'K4', 'K5', 'K6'):
        r = g[k]
        R = RO if r.band == 'O' else RI
        bd = r.b1 + math.degrees(1.75 / R)
        dc(r, bd, 0.9, 'slide')
    # clinic -> isolation (partition 44.5)
    r = g['08']
    door_on_rad(ctx, 44.5, R0 - 3.6, R0 - 2.6, into=1, kind='swing', hinge='+')
    # isolation bathroom partition + door
    wall_arc(ctx, R0 - 4.35, 44.5, 50.0)
    door_on_arc(ctx, R0 - 4.35, 46.2, 0.8, -1, kind='slide')


def hatches_nodes(ctx, g):
    """pressure hatches through node bulkheads and node internal doors"""
    # S1/Arch1 bulkhead at b=5
    door_on_rad(ctx, 5, R0 - 0.6, R0 + 0.6, into=-1, kind='hatch', hinge='-', t=0.25)       # main 1.20
    door_on_rad(ctx, 5, R0 - 3.7, R0 - 2.5, into=-1, kind='hatch', hinge='+', t=0.25)       # suit-lock -> decon
    door_on_rad(ctx, 5, R0 + 2.4, R0 + 3.6, into=-1, kind='hatch', hinge='-', t=0.25)       # cargo -> storage
    # S1 far end (to Arch 2 - capped in early settlement)
    door_on_rad(ctx, -5, R0 - 0.6, R0 + 0.6, into=1, kind='hatch', hinge='+', t=0.25)
    # S2 bulkheads
    door_on_rad(ctx, 115, R0 - 0.6, R0 + 0.6, into=1, kind='hatch', hinge='-', t=0.25)
    door_on_rad(ctx, 125, R0 - 0.6, R0 + 0.6, into=-1, kind='hatch', hinge='+', t=0.25)


# ---------------------------------------------------------------- nodes interior
def node_s1(ctx, h=HG):
    v = ctx.view
    cw = cut_widths(h)
    xm = cw['mem_out']
    # vestibule walls (pressure walls inside node)
    for sgn in (1, -1):
        wall_arc(ctx, R0 + sgn * CW, -5, 5, t=0.16, color='#4a4a4a')
    # internal pressure wall in suit-lock (EVA chamber) and cargo lock
    wall_arc(ctx, R0 - 4.65, -5, 5, t=0.16, color='#4a4a4a')
    wall_arc(ctx, R0 + 3.75, -5, 5, t=0.16, color='#4a4a4a')
    # doors
    door_on_arc(ctx, R0 - CW, -2.2, 1.0, -1, kind='hatch', hinge='-', t=0.16)        # vestibule -> suit-lock
    door_on_arc(ctx, R0 + CW, -2.0, 1.2, 1, kind='hatch', hinge='-', t=0.16)         # vestibule -> cargo
    door_on_arc(ctx, R0 - 4.65, 1.3, 1.2, -1, kind='hatch', hinge='-', t=0.16)       # donning -> EVA chamber
    door_on_arc(ctx, R0 + 3.75, -0.6, 1.5, 1, kind='hatch', hinge='+', t=0.16)       # staging -> cargo chamber
    # exterior: EVA hatch (inner wall) + 2 suitports; cargo door + rover docking port (outer wall)
    door_on_arc(ctx, R0 - xm - 0.11, 2.6, 1.2, 1, kind='hatch', hinge='+', t=0.22)     # opens inward (pressure-seated)
    door_on_arc(ctx, R0 + xm + 0.11, 1.5, 1.5, -1, kind='hatch', hinge='-', t=0.22)
    door_on_arc(ctx, R0 + xm + 0.11, -3.0, 1.2, -1, kind='hatch', hinge='+', t=0.22)
    # suitports
    for b in (-3.2, -0.7):
        f = v.local(R0 - xm - 0.11, b, 1, -1)
        F.circ(ctx, f, 0, 0, 0.42, fill='#ffffff', stroke=HATCH_C, sw=0.2)
        F.suit(ctx, v.local(R0 - xm - 0.85, b, 1, -1), 0, 0, s=1.0, fill='#fff3e3')
    # dust control zone (electrostatic air shower)
    ctx.svg.add(f'<path d="{sector_d(v, R0 - 6.2, R0 - 4.85, -4.3, 0.0)}" fill="#f6eedf" stroke="#b08a50" '
                f'stroke-width="{num(0.1*ctx.lw)}" stroke-dasharray="0.8,0.5"/>')
    f = v.local(R0 - 2.6, -0.5, 1, -1)
    F.rect(ctx, f, -1.6, 0.35, 1.4, 0.75, fill='#f5efe2')             # bench
    F.label(ctx, f, -0.1, 0.55, 'bangku lepas-pakai', 1.05)
    for k, b in enumerate((-3.6, -2.3)):
        F.suit(ctx, v.local(R0 - 4.15, b, 1, -1), 0, 0, s=0.9)
    F.rack(ctx, v.local(R0 - 2.4, 3.2, 1, -1), -0.35, -0.3, 0.35, 0.95, fill='#f5efe2')
    # cargo: pallet + jack
    f = v.local(R0 + 4.85, 0.0, 1, 1)
    F.rect(ctx, f, -1.6, -0.6, -0.2, 0.6, fill='#f5efe2')
    F.label(ctx, f, -0.9, 0.05, 'kargo', 1.1)
    f = v.local(R0 + 2.75, 1.5, 1, 1)
    F.rect(ctx, f, -0.55, -0.4, 0.55, 0.4, fill='#f5efe2')
    F.label(ctx, f, 0, 0.05, 'staging', 1.05)
    # docking collar for rover
    f = v.local(R0 + xm + 0.6, -3.0, 1, 1)
    F.rect(ctx, f, -0.75, -0.35, 0.75, 0.35, fill='#ffffff', stroke=HATCH_C, sw=0.18)


def node_s2(ctx, h=HG):
    v = ctx.view
    for sgn in (1, -1):
        wall_arc(ctx, R0 + sgn * CW, 115, 125, t=0.16, color='#4a4a4a')
    door_on_arc(ctx, R0 + CW, 118.6, 1.0, 1, kind='hatch', hinge='-', t=0.16)
    door_on_arc(ctx, R0 - CW, 118.6, 1.0, -1, kind='hatch', hinge='-', t=0.16)
    # utility shaft risers (outer)
    f = v.local(R0 + 3.6, 120.0, 1, 1)
    for k, (uu, vv, lab) in enumerate(((-1.4, 0.2, 'air'), (-0.5, 0.2, 'O₂'), (0.4, 0.2, 'N₂'), (1.3, 0.2, 'term'),
                                       (-1.0, 1.4, 'listrik'), (0.9, 1.4, 'data'))):
        F.circ(ctx, f, uu, vv, 0.32, fill='#eef3f6', sw=0.14)
        F.label(ctx, f, uu, vv - 0.02, lab, 0.95)
    F.rect(ctx, v.local(R0 + 6.0, 120, 1, 1), -1.3, -0.15, 1.3, 0.35, fill='#e9ecef')
    # emergency equipment (inner)
    f = v.local(R0 - 3.4, 120, 1, -1)
    F.shelves(ctx, f, -1.5, -0.6, -0.9, 1.6, n=4)
    F.shelves(ctx, f, 0.9, -0.6, 1.5, 1.6, n=4)
    F.suit(ctx, v.local(R0 - 5.4, 119.0, 1, -1), 0, 0, s=0.9)
    F.suit(ctx, v.local(R0 - 5.4, 121.0, 1, -1), 0, 0, s=0.9)
    F.circ(ctx, f, 0, 0.2, 0.18, fill='#e05a4f', stroke='#7a2a22', sw=0.08)


# ---------------------------------------------------------------- corridor
def corridor(ctx, b1, b2, label_bs=(), mezz_cover=None):
    v = ctx.view
    ctx.svg.add(f'<path d="{sector_d(v, R0 - X_CORR, R0 + X_CORR, b1, b2)}" fill="{CORR_FILL}" stroke="none"/>')
    # module joints
    b = math.ceil(b1 / MOD) * MOD
    while b <= b2 + 1e-6:
        ctx.svg.add(f'<path d="{radial_d(v, b, R0 - X_CORR, R0 + X_CORR)}" stroke="#c9c6bd" stroke-width="{num(0.1*ctx.lw)}" '
                    f'stroke-dasharray="0.6,0.5"/>')
        b += MOD
    # ring axis
    ctx.svg.add(f'<path d="{arc_d(v, R0, b1, b2)}" fill="none" stroke="#b08a50" stroke-width="{num(0.12*ctx.lw)}" '
                f'stroke-dasharray="4,0.8,0.6,0.8"/>')


def corridor_edges(ctx, b1, b2):
    """3.60 m clear path marking (dashed) where the corridor has no walls"""
    v = ctx.view
    for sgn in (1, -1):
        ctx.svg.add(f'<path d="{arc_d(v, R0 + sgn * X_CORR, b1, b2)}" fill="none" stroke="#8a8478" '
                    f'stroke-width="{num(0.14*ctx.lw)}" stroke-dasharray="1.2,0.7"/>')


def corridor_label(ctx, b, s='KORIDOR UTAMA 3,60 m — BEBAS HAMBATAN', size=1.9):
    v = ctx.view
    x, y = v.P(R0 + 0.55, b)
    (tx, ty), _ = v.dirs(b)
    ang = math.degrees(math.atan2(ty, tx))
    from core import upright
    ctx.svg.add(text(x, y, s, size=size, fill='#7d776a', weight=600, rot=upright(ang), ls='0.25'))


# ---------------------------------------------------------------- full plans
def draw_ground_plan(ctx, tags=True, detail=True):
    v = ctx.view
    draw_ground(ctx, -8, 128, 17.5, 39.0)
    draw_node(ctx, -5, 5, free_ends=((-5, -1),))
    draw_node(ctx, 115, 125, free_ends=((125, 1),))
    draw_shell(ctx, 5, 115, HG)
    cw = cut_widths(HG)
    for b1, b2 in ((-5, 5), (115, 125)):
        ctx.svg.add(f'<path d="{sector_d(v, R0 - cw["mem_out"], R0 + cw["mem_out"], b1, b2)}" fill="{ZONE["node"]}" stroke="none"/>')
    ctx.svg.add(f'<path d="{sector_d(v, R0 - cw["mem_in"], R0 + cw["mem_in"], 5, 115)}" fill="#ffffff" stroke="none"/>')
    return draw_interior(ctx, detail=detail, draw_corridor=True)


def draw_interior(ctx, detail=True, draw_corridor=True):
    v = ctx.view
    g = rooms_ground()
    cw = cut_widths(HG)
    for r in g.values():
        fill_room(ctx, r)
    for band, b1, b2, x0 in BACK_STORES:
        rr = Room('x', 'x', band, b1, b2, x1=x0 + 0.1, x2=X_CHASE, zone='circ')
        fill_room(ctx, rr, fill='#f3f2ee')
    for k, xb in (('K1', 5.30), ('K2', 5.30), ('K3', 5.30), ('K4', 5.0), ('K5', 5.0), ('K6', 5.0)):
        r = g[k]
        rr = Room('x', 'x', r.band, r.b1, r.b2, x1=xb, x2=X_CHASE, zone='circ')
        fill_room(ctx, rr, fill='#f3f2ee')
    if draw_corridor:
        corridor(ctx, -5, 125)
    draw_chase(ctx, 5, 115, HG)
    ctx.svg.add(f'<path d="{sector_d(v, R0 - X_CORR, R0 + X_CORR, 50, 75)}" fill="#fbf4e4" stroke="none" opacity="0.75"/>')
    corridor_edges(ctx, 50, 75)
    for rid in ('T1', 'T2', 'T3', 'T4'):          # stair recesses open to the corridor: clear lane stays marked
        r = g[rid]
        sg = 1 if r.band == 'O' else -1
        ctx.svg.add(f'<path d="{arc_d(v, R0 + sg * X_CORR, r.b1, r.b2)}" fill="none" stroke="#8a8478" '
                    f'stroke-width="{num(0.14*ctx.lw)}" stroke-dasharray="1.2,0.7"/>')
    if detail:
        furnish_ground(ctx, g)
        node_s1(ctx)
        node_s2(ctx)
    for r in g.values():
        walls_room(ctx, r)
    for band, b1, b2, x0 in BACK_STORES:
        sgn = 1 if band == 'O' else -1
        wall_rad(ctx, b1, R0 + sgn * x0, R0 + sgn * cw['mem_in'])
        wall_rad(ctx, b2, R0 + sgn * x0, R0 + sgn * cw['mem_in'])
    for k, xb in (('K1', 5.25), ('K2', 5.25), ('K3', 5.25), ('K4', 4.95), ('K5', 4.95), ('K6', 4.95)):
        r = g[k]
        sgn = 1 if r.band == 'O' else -1
        wall_rad(ctx, r.b1, R0 + sgn * xb, R0 + sgn * cw['mem_in'])
        wall_rad(ctx, r.b2, R0 + sgn * xb, R0 + sgn * cw['mem_in'])
    for b in (-5, 5, 115, 125):
        node_bulkhead(ctx, b)
    doors_ground(ctx, g)
    hatches_nodes(ctx, g)
    for band, b1, b2, x0 in BACK_STORES:
        sgn = 1 if band == 'O' else -1
        door_on_arc(ctx, R0 + sgn * (x0 + 0.05), 0.5 * (b1 + b2), 0.7, sgn, kind='slide')
    for k, (band, b) in STAIRS.items():
        sgn = 1 if band == 'O' else -1
        spiral_stair(ctx, R0 + sgn * STAIR_X, b, d=STAIR_D, label=None)
    return g


def mezz_outline(ctx, dashed=True, color='#5a5a5a'):
    """outline of the mezzanine slab (drawn on ground plan, dashed)"""
    v = ctx.view
    for sgn in (1, -1):
        d = sector_d(v, R0 + sgn * SLOT, R0 + sgn * MZ_EDGE, 85, 114.75) if sgn > 0 else \
            sector_d(v, R0 - MZ_EDGE, R0 - SLOT, 85, 114.75)
        ctx.svg.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{num(0.18*ctx.lw)}" '
                    f'stroke-dasharray="{"2.2,1.0" if dashed else "none"}"/>')


# ================================================================ mezzanine +3.00 (cut +4.20)
HM = 4.20


def rail_arc(ctx, R, b1, b2):
    v = ctx.view
    ctx.svg.add(f'<path d="{arc_d(v, R, b1, b2)}" stroke="#4f7da1" stroke-width="{num(v.L(0.05))}" fill="none"/>')
    ctx.svg.add(f'<path d="{arc_d(v, R, b1, b2)}" stroke="#2c4d66" stroke-width="{num(0.08*ctx.lw)}" fill="none" stroke-dasharray="0.4,0.9"/>')


def rail_rad(ctx, b, R1, R2):
    v = ctx.view
    ctx.svg.add(f'<path d="{radial_d(v, b, R1, R2)}" stroke="#4f7da1" stroke-width="{num(v.L(0.05))}" fill="none"/>')
    ctx.svg.add(f'<path d="{radial_d(v, b, R1, R2)}" stroke="#2c4d66" stroke-width="{num(0.08*ctx.lw)}" fill="none" stroke-dasharray="0.4,0.9"/>')


B_MZ1, B_MZ2 = 85.0, 114.75
BRIDGES = ((85.0, 87.45), (112.3, 114.75))


def draw_mezz_plan(ctx, detail=True):
    v, svg = ctx.view, ctx.svg
    gr = rooms_ground()
    mz = rooms_mezz()
    cw = cut_widths(HM)
    xm = cw['mem_in']
    draw_ground(ctx, -8, 128, 17.5, 39.0)
    draw_node(ctx, -5, 5, h=HM, free_ends=((-5, -1),))
    draw_node(ctx, 115, 125, h=HM, free_ends=((125, 1),))
    draw_shell(ctx, 5, 115, HM, show_floor_edge=False, show_h240=False)
    # node interiors (single volume, no mezzanine) - roof of internal rooms below
    for b1, b2 in ((-5, 5), (115, 125)):
        svg.add(f'<path d="{sector_d(v, R0 - cw["mem_out"], R0 + cw["mem_out"], b1, b2)}" fill="url(#roofH)" stroke="none"/>')
        for sgn in (1, -1):
            svg.add(f'<path d="{arc_d(v, R0 + sgn * CW, b1, b2)}" stroke="#a9a9a9" stroke-width="{num(0.15*ctx.lw)}" fill="none"/>')
    # interior seen below: open voids vs roofs of closed rooms (+2,70)
    svg.add(f'<path d="{sector_d(v, R0 - xm, R0 + xm, 5, 115)}" fill="#fbfbfa" stroke="none"/>')
    svg.add(f'<path d="{sector_d(v, R0 - xm, R0 + xm, 5, 115)}" fill="url(#voidH)" stroke="none"/>')
    for r in gr.values():
        x2 = min(r.x2, xm)
        if r.x1 >= x2:
            continue
        R1, R2 = r.R(r.x1), r.R(x2)
        if r.closed and not r.rid.startswith('T'):
            svg.add(f'<path d="{sector_d(v, min(R1, R2), max(R1, R2), r.b1, r.b2)}" fill="url(#roofH)" stroke="#9c9c9c" stroke-width="{num(0.15*ctx.lw)}"/>')
        else:
            svg.add(f'<path d="{sector_d(v, min(R1, R2), max(R1, R2), r.b1, r.b2)}" fill="none" stroke="#b9b9b9" stroke-width="{num(0.12*ctx.lw)}" stroke-dasharray="1,0.7"/>')
    # cabin back zones / stores below (roofs)
    for band, b1, b2, x0 in BACK_STORES:
        rr = Room('x', 'x', band, b1, b2, x1=x0, x2=xm)
        svg.add(f'<path d="{sector_d(v, min(rr.R(x0), rr.R(xm)), max(rr.R(x0), rr.R(xm)), b1, b2)}" fill="url(#roofH)" stroke="#9c9c9c" stroke-width="{num(0.15*ctx.lw)}"/>')
    # corridor marking below (open)
    for sgn in (1, -1):
        svg.add(f'<path d="{arc_d(v, R0 + sgn * X_CORR, 5, 85)}" fill="none" stroke="#a7a39a" stroke-width="{num(0.14*ctx.lw)}" stroke-dasharray="1.2,0.7"/>')
    # trees below (plaza) as ghost
    for (b, x, rr_) in ((62.9, -3.8, 1.0), (68.55, -4.15, 1.05), (73.2, -3.05, 0.75)):
        f = v.local(R0 + x, b, 1, 1)
        F.circ(ctx, f, 0, 0, rr_, fill='none', stroke='#7fb26b', sw=0.18)
    # ---------------- mezzanine slab
    for sgn in (1, -1):
        d = sector_d(v, R0 + sgn * SLOT if sgn > 0 else R0 - MZ_EDGE, R0 + MZ_EDGE if sgn > 0 else R0 - SLOT, B_MZ1, B_MZ2)
        svg.add(f'<path d="{d}" fill="#ffffff" stroke="#262626" stroke-width="{num(0.3*ctx.lw)}"/>')
    for b1, b2 in BRIDGES:
        svg.add(f'<path d="{sector_d(v, R0 - SLOT - 0.02, R0 + SLOT + 0.02, b1, b2)}" fill="#ffffff" stroke="none"/>')
        for sgn in (1, -1):
            pass
    # slot void hatch
    for b1, b2 in ((BRIDGES[0][1], BRIDGES[1][0]),):
        svg.add(f'<path d="{sector_d(v, R0 - SLOT, R0 + SLOT, b1, b2)}" fill="#eef1f4" stroke="none"/>')
        svg.add(f'<path d="{sector_d(v, R0 - SLOT, R0 + SLOT, b1, b2)}" fill="url(#voidH)" stroke="none"/>')
    # walkway floor tint
    for sgn in (1, -1):
        d = sector_d(v, R0 + sgn * SLOT if sgn > 0 else R0 - MZ_IN + 0.08, R0 + MZ_IN - 0.08 if sgn > 0 else R0 - SLOT, B_MZ1, B_MZ2)
        svg.add(f'<path d="{d}" fill="{CORR_FILL}" stroke="none"/>')
    for b1, b2 in BRIDGES:
        svg.add(f'<path d="{sector_d(v, R0 - SLOT, R0 + SLOT, b1, b2)}" fill="{CORR_FILL}" stroke="none"/>')
    # rooms
    for r in mz.values():
        fill_room(ctx, r)
    if detail:
        for k in ('K7', 'K8', 'K9', 'K10', 'K11', 'K12'):
            cabin(ctx, mz[k])
        # library / quiet room
        r = mz['18']
        f = r.frame(v, 'b1')
        F.shelves(ctx, f, 0.05, 0.35, 0.45, 2.85, n=6)
        f2 = r.frame(v, 'b2')
        F.shelves(ctx, f2, 0.05, 0.8, 0.45, 2.85, n=5)
        fb = r.frame(v, 'mid', x=MZ_OUT - 0.05)
        F.shelves(ctx, fb, -1.5, -0.45, 1.5, -0.05, n=7)
        fm = r.frame(v, 'mid')
        F.table_rect(ctx, fm, -0.75, 1.15, 0.45, 1.85, chairs_u=2)
        F.round_chair(ctx, fm, 1.15, 1.0, 0.3)
        F.round_chair(ctx, fm, 1.2, 1.85, 0.3)
        # linen store
        r = mz['19']
        f = r.frame(v, 'b1')
        F.shelves(ctx, f, 0.05, 0.6, 0.55, 2.9, n=5)
    for r in mz.values():
        walls_room(ctx, r, h=HM)
    # railings: slot edges, mezzanine end at b=85, open slab edges near stairs
    for sgn in (1, -1):
        rail_arc(ctx, R0 + sgn * (SLOT + 0.015), BRIDGES[0][1], BRIDGES[1][0])
        rail_rad(ctx, B_MZ1 + 0.06, R0 + sgn * SLOT if sgn > 0 else R0 - MZ_EDGE, R0 + MZ_EDGE if sgn > 0 else R0 - SLOT)
    rail_rad(ctx, B_MZ1 + 0.06, R0 - SLOT, R0 + SLOT)
    for band, b1, b2 in (('O', 93, 96.5), ('O', 111.5, 114.75), ('I', 88.0, 92.0), ('I', 110.9, 114.75)):
        sgn = 1 if band == 'O' else -1
        rail_arc(ctx, R0 + sgn * (MZ_EDGE - 0.03), b1, b2)
    # doors (pocket) on walkway side
    for k in ('K7', 'K8', 'K9', 'K10', 'K11', 'K12'):
        r = mz[k]
        sgn = 1 if r.band == 'O' else -1
        R = R0 + sgn * (MZ_IN - 0.04)
        bd = r.b1 + math.degrees(1.75 / R)
        door_on_arc(ctx, R, bd, 0.9, sgn, kind='slide', t=0.08)
    door_on_arc(ctx, R0 + MZ_IN - 0.04, 89.0, 0.9, 1, kind='swing', hinge='-', t=0.08)
    door_on_arc(ctx, R0 - MZ_IN + 0.04, 86.5, 0.8, -1, kind='slide', t=0.08)
    # stairs (down)
    for k, (band, b) in STAIRS.items():
        sgn = 1 if band == 'O' else -1
        f = v.local(R0 + sgn * STAIR_X, b)
        F.circ(ctx, f, 0, 0, STAIR_D / 2 + 0.06, fill='#ffffff', stroke='#262626', sw=0.25)
        spiral_stair(ctx, R0 + sgn * STAIR_X, b, d=STAIR_D, up=False, start=180)
    return gr, mz
