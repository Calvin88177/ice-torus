"""Full Ring 1 (Permanent Settlement): S1 + Arch 1 + S2 + Arch 3 + S3 + Arch 2 = 72 modules.

Bearings clockwise from north: S1 [-5, 5], Arch 1 [5, 115], S2 [115, 125], Arch 3 [125, 235],
S3 [235, 245], Arch 2 [245, 355]."""
import math
from core import (R0, X_CHASE, X_CORR, WALL, cut_widths, num, sector_d, arc_d, radial_d, text, fmt, upright)
from plan import (ZONE, HATCH_C, draw_ground, draw_node, draw_shell, draw_chase, node_bulkhead, wall_arc, wall_rad,
                  door_on_arc, door_on_rad, spiral_stair, ang_of, sector_area)
import furn as F
import arch1
from arch1 import (Room, fill_room, walls_room, cabin, corridor_edges, CW, XF, HG, STAIR_X, STAIR_D, fin,
                   SLOT, MZ_IN, MZ_OUT, MZ_EDGE, HM, rail_arc, rail_rad, CORR_FILL)

A1 = (5, 115)
A3 = (125, 235)
A2 = (245, 355)
NODES = ((-5, 5, 'S1'), (115, 125, 'S2'), (235, 245, 'S3'))
BACK_FILL = '#f3f2ee'


# ================================================================== programme
def arch3_rooms():
    O, I = 'O', 'I'
    L = [Room('G1', 'Pantry & gudang dingin', O, 125, 135, zone='grow'),
         Room('G2', 'Ruang tanam A — kebun vertikal LED', O, 135, 175, zone='grow', glass_corr=True),
         Room('G3', 'Dapur produksi & pengolahan pangan', O, 175, 185, zone='comm'),
         Room('G4', 'Limbah organik, kompos & bioreaktor', O, 185, 200, zone='make', acoustic=('b1',)),
         Room('G5', 'Fabrikasi & manufaktur (printer 3D, CNC)', O, 200, 225, zone='make', acoustic=('corr', 'b2')),
         Room('G6', 'Sanitasi & loker kerja', O, 225, 230, zone='priv'),
         Room('G7', 'Gudang bahan baku (feedstock regolit)', O, 230, 235, zone='tech'),
         Room('G8', 'Bank benih & gudang pangan kering', I, 125, 135, zone='grow'),
         Room('G9', 'Ruang tanam B — kebun vertikal LED', I, 135, 175, zone='grow', glass_corr=True),
         Room('G10', 'Lab pangan & kontrol hidroponik', I, 175, 185, zone='res'),
         Room('G11', 'Daur ulang air & larutan nutrien', I, 185, 200, zone='eclss', acoustic=('b1',)),
         Room('G12', 'Daur ulang material & bengkel besar', I, 200, 220, zone='make', acoustic=('corr', 'b2')),
         Room('G13', 'Ruang istirahat kru kerja', I, 220, 228, zone='comm'),
         Room('G14', 'Gudang alat & suku cadang', I, 228, 235, zone='tech')]
    return {r.rid: r for r in L}


IN_STEP = (290 - 252.4) / 6.0          # inner cabin width in degrees (6.27 deg)


def arch2_rooms():
    O, I = 'O', 'I'
    L = []
    # ---- wing A (245..290)
    L.append(Room('T5', 'Tangga spiral T5', O, 245, 248.5, x2=3.80, zone='circ', corr_wall=False, back=True))
    for k in range(6):
        b = 248.5 + 5 * k
        L.append(Room(f'K{13 + k}', f'Kabin K{13 + k}', O, b, b + 5, x2=5.20, zone='priv', back=True))
    L.append(Room('T6', 'Tangga spiral T6', O, 278.5, 282, x2=3.80, zone='circ', corr_wall=False, back=True))
    L.append(Room('L5', 'Sanitasi bersama A', O, 282, 290, zone='priv'))
    L.append(Room('L6', 'Laundry & linen A', I, 245, 248.4, zone='priv'))
    L.append(Room('T7', 'Tangga spiral T7', I, 248.4, 252.4, x2=3.80, zone='circ', corr_wall=False, back=True))
    for k in range(6):
        b = 252.4 + IN_STEP * k
        L.append(Room(f'K{19 + k}', f'Kabin K{19 + k}', I, b, b + IN_STEP, x2=4.90, zone='priv', back=True))
    # ---- social / education core (290..310)
    L.append(Room('L1', 'Aula serbaguna & ruang kelas', O, 290, 300, zone='edu'))
    L.append(Room('L2', 'Kafe & lounge sosial', O, 300, 310, zone='comm', closed=False, corr_wall=False))
    L.append(Room('L3', 'Perpustakaan & ruang belajar', I, 290, 300, zone='edu'))
    L.append(Room('L4', 'Plaza sosial & taman (void)', I, 300, 310, zone='comm', closed=False, corr_wall=False))
    # ---- wing B (310..355)
    L.append(Room('L7', 'Sanitasi bersama B', O, 310, 318, zone='priv'))
    L.append(Room('T8', 'Tangga spiral T8', O, 318, 321.5, x2=3.80, zone='circ', corr_wall=False, back=True))
    for k in range(6):
        b = 321.5 + 5 * k
        L.append(Room(f'K{37 + k}', f'Kabin K{37 + k}', O, b, b + 5, x2=5.20, zone='priv', back=True))
    L.append(Room('T9', 'Tangga spiral T9', O, 351.5, 355, x2=3.80, zone='circ', corr_wall=False, back=True))
    for k in range(6):
        b = 310 + IN_STEP * k
        L.append(Room(f'K{43 + k}', f'Kabin K{43 + k}', I, b, b + IN_STEP, x2=4.90, zone='priv', back=True))
    L.append(Room('T10', 'Tangga spiral T10', I, 347.6, 351.6, x2=3.80, zone='circ', corr_wall=False, back=True))
    L.append(Room('L8', 'Laundry & linen B', I, 351.6, 355, zone='priv'))
    return {r.rid: r for r in L}


MZ_A = (245.25, 290.0)
MZ_B = (310.0, 354.75)
BRIDGES2 = ((245.25, 247.7), (287.55, 290.0), (310.0, 312.45), (352.3, 354.75))


def arch2_mezz():
    O, I = 'O', 'I'
    L = []
    for k in range(6):
        b = 248.5 + 5 * k
        L.append(Room(f'K{25 + k}', f'Kabin K{25 + k}', O, b, b + 5, x1=MZ_IN, x2=MZ_OUT, zone='priv', back=True, level='M'))
    L.append(Room('L9', 'Sanitasi mezanin A', O, 282, 290, x1=MZ_IN, x2=MZ_OUT, zone='priv', back=True, level='M'))
    L.append(Room('L10', 'Gudang linen A', I, 245.25, 248.4, x1=MZ_IN, x2=MZ_OUT, zone='priv', back=True, level='M'))
    for k in range(6):
        b = 252.4 + IN_STEP * k
        L.append(Room(f'K{31 + k}', f'Kabin K{31 + k}', I, b, b + IN_STEP, x1=MZ_IN, x2=MZ_OUT, zone='priv', back=True, level='M'))
    L.append(Room('L11', 'Sanitasi mezanin B', O, 310, 318, x1=MZ_IN, x2=MZ_OUT, zone='priv', back=True, level='M'))
    for k in range(6):
        b = 321.5 + 5 * k
        L.append(Room(f'K{49 + k}', f'Kabin K{49 + k}', O, b, b + 5, x1=MZ_IN, x2=MZ_OUT, zone='priv', back=True, level='M'))
    for k in range(6):
        b = 310 + IN_STEP * k
        L.append(Room(f'K{55 + k}', f'Kabin K{55 + k}', I, b, b + IN_STEP, x1=MZ_IN, x2=MZ_OUT, zone='priv', back=True, level='M'))
    L.append(Room('L12', 'Gudang linen B', I, 351.6, 354.75, x1=MZ_IN, x2=MZ_OUT, zone='priv', back=True, level='M'))
    return {r.rid: r for r in L}


STAIRS2 = {'T5': ('O', 246.75), 'T6': ('O', 280.25), 'T7': ('I', 250.4),
           'T8': ('O', 319.75), 'T9': ('O', 353.25), 'T10': ('I', 349.6)}


# ================================================================== furniture
def _sanitation(ctx, r, n_wc=3, n_sh=3):
    v = ctx.view
    f = r.frame(v, 'b1')
    for k in range(n_wc):
        v0 = 0.25 + 1.4 * k
        F.rect(ctx, f, 0.05, v0, 1.25, v0 + 1.3, fill='#fafafa', sw=0.1)
        F.wc(ctx, f, 0.2, v0 + 0.65, ang='u-')
    depth = r.x2 - r.x1
    for k in range(n_sh):
        u0 = 1.4 + 1.12 * k
        F.shower(ctx, f, u0, depth - 1.15, u0 + 1.02, depth - 0.1)
    f2 = r.frame(v, 'b2')
    F.counter(ctx, f2, 0.05, 1.15, 0.6, 3.15, fill='#f7f7f7')
    for vv in (1.6, 2.7):
        F.sink(ctx, f2, 0.32, vv, 0.4, 0.35)


def _laundry(ctx, r):
    f = r.frame(ctx.view, 'b1')
    F.washer(ctx, f, 0.4, 1.0, 0.6)
    F.washer(ctx, f, 0.4, 1.65, 0.6)
    F.counter(ctx, f, 0.08, 2.1, 0.7, 3.2)
    F.shelves(ctx, f, 0.08, 3.4, 0.7, 4.4, n=3)


def _rack_row(ctx, r, x_from, length, pitch=1.5, w=0.6, margin=1.2):
    """radial rows of vertical grow racks at constant pitch measured at mid-depth"""
    v = ctx.view
    xm = x_from + length / 2
    Rm = r.R(xm)
    span = math.radians(r.b2 - r.b1) * Rm
    n = int((span - 2 * margin) / pitch) + 1
    start = r.b1 + math.degrees((span - (n - 1) * pitch) / 2 / Rm)
    for i in range(n):
        b = start + math.degrees(i * pitch / Rm)
        fr = v.local(r.R(x_from), b, 1, 1 if r.band == 'O' else -1)
        F.hydro_rack(ctx, fr, -w / 2, 0.0, w / 2, length)
    return n


def furnish(ctx, r):
    v = ctx.view
    rid = r.rid
    if rid.startswith('K'):
        cabin(ctx, r)
        return
    if rid.startswith('T'):
        return
    f = r.frame(v, 'b1')
    f2 = r.frame(v, 'b2')
    fm = r.frame(v, 'mid')
    sgn = 1 if r.band == 'O' else -1
    if rid in ('L5', 'L7'):
        _sanitation(ctx, r)
    elif rid in ('L6', 'L8'):
        _laundry(ctx, r)
    elif rid == 'L1':          # multipurpose hall / classroom
        F.screen(ctx, f2, 0.05, 1.0, 0.14, 3.6)
        F.rect(ctx, f2, 0.6, 0.55, 1.1, 1.0, fill='#f4f1ea')                     # lectern
        for i, uu in enumerate((1.55, 2.35, 3.15, 3.95)):
            for vv in (1.25, 1.9, 2.55, 3.2, 3.85):
                F.chair(ctx, f2, uu, vv, s=0.42, back='u+')
        F.shelves(ctx, f, 0.05, 2.6, 0.45, 4.4, n=4)                              # stacked folding tables
    elif rid == 'L2':          # cafe & lounge
        F.counter(ctx, f2, 0.05, 1.0, 0.65, 3.4, fill='#f6efe2')
        F.sink(ctx, f2, 0.35, 3.0, 0.35, 0.3)
        for vv in (1.45, 2.05, 2.65):
            F.round_chair(ctx, f2, 0.95, vv, 0.17)
        for (uu, vv) in ((-1.9, 1.35), (-0.4, 1.8), (-2.0, 3.0), (-0.5, 3.4)):
            F.table_round(ctx, fm, uu, vv, 0.38, chairs=3)
        b1_, b2_ = r.b1 + 0.9, r.b1 + 4.6
        ctx.svg.add(f'<path d="{sector_d(v, r.R(5.2), r.R(5.85), b1_, b2_)}" fill="#efe3cf" stroke="#3a3a3a" stroke-width="{num(0.14*ctx.lw)}"/>')
        F.plant(ctx, v.local(r.R(5.3), r.b2 - 1.6, 1, sgn), 0, 0, 0.32)
    elif rid == 'L3':          # library & study
        F.shelves(ctx, f, 0.05, 0.6, 0.45, 4.3, n=8)
        F.shelves(ctx, f2, 0.05, 0.6, 0.45, 3.2, n=6)
        F.table_rect(ctx, fm, -0.55, 1.4, 0.55, 2.6, chairs_v=2)
        F.round_chair(ctx, fm, 0.9, 3.6, 0.3)
        F.round_chair(ctx, fm, -0.4, 3.75, 0.3)
    elif rid == 'L4':          # social plaza & garden (open void)
        F.tree(ctx, v.local(r.R(3.7), 303.2, 1, sgn), 0, 0, 0.95)
        F.tree(ctx, v.local(r.R(3.2), 308.0, 1, sgn), 0, 0, 0.7)
        fin(ctx, 'I', [(2.45, 305.9), (3.6, 305.1), (4.8, 305.6), (6.0, 305.15)])
        for (bb1, bb2) in ((300.7, 304.9), (306.4, 309.4)):
            ctx.svg.add(f'<path d="{sector_d(v, r.R(5.6), r.R(6.02), bb1, bb2)}" fill="#efe3cf" stroke="#3a3a3a" stroke-width="{num(0.12*ctx.lw)}"/>')
        fk = v.local(r.R(2.7), 306.9, 1, sgn)
        F.ellipse(ctx, fk, 0, 0, 0.4, 0.3, fill='#ffffff', sw=0.1)
        for a in (0, 120, 240):
            F.round_chair(ctx, fk, 0.75 * math.cos(math.radians(a)), 0.55 * math.sin(math.radians(a)), 0.18)
        for (b, x) in ((301.0, 2.6), (309.3, 5.0)):
            F.plant(ctx, v.local(r.R(x), b, 1, sgn), 0, 0, 0.3)
    elif rid in ('G2', 'G9'):  # vertical farms: radial rack rows, aisles 0.90
        _rack_row(ctx, r, 2.55, 3.0 if r.band == 'O' else 2.85, pitch=1.5)
        fb = r.frame(v, 'mid', x=X_CHASE - 0.05)
        F.counter(ctx, fb, -2.2, 0.0, 2.2, -0.55, fill='#f2f8ee')                 # nutrient / harvest bench along back
    elif rid in ('G1', 'G8'):  # pantry & cold store / seed bank
        F.shelves(ctx, f, 0.05, 0.4, 0.55, 4.3, n=7)
        F.shelves(ctx, f2, 0.05, 0.4, 0.55, 4.3, n=7)
        fb = r.frame(v, 'mid', x=X_CHASE - 0.05)
        for uu in (-1.1, -0.35, 0.4) if r.band == 'O' else (-0.75, 0.0):
            F.fridge(ctx, fb, uu - 0.33, 0.0, uu + 0.33, -0.7, lab='−20' if rid == 'G1' else '−18')
        F.rect(ctx, fm, -0.55, 1.6, 0.55, 2.6, fill='#f5efe2')                    # trolley / sorting table
    elif rid == 'G3':          # production kitchen
        F.counter(ctx, f, 0.05, 0.8, 0.7, 4.3)
        F.cooktop(ctx, f, 0.38, 1.8, 0.5, 0.6)
        F.sink(ctx, f, 0.38, 3.2, 0.45, 0.45)
        F.counter(ctx, fm, -0.6, 1.5, 0.9, 2.5, fill='#f6efe2')                   # island
        F.fridge(ctx, f2, 0.05, 3.6, 0.75, 4.3, lab='K')
        F.rack(ctx, f2, 0.05, 2.4, 0.75, 3.4, fill='#eef0f2', label='FD')          # freeze dryer
        F.rack(ctx, f2, 0.05, 0.9, 0.75, 1.9, fill='#f5efe2')                      # packing
    elif rid == 'G4':          # organic waste, compost, bioreactors
        for uu in (-1.9, -0.5, 0.9):
            F.tank(ctx, fm, uu, 1.7, 0.55, 'BR', size=1.0)
        F.rack(ctx, fm, -2.1, 3.1, 1.3, 4.0, fill='#efe6d6')                      # in-vessel composter
        F.rect(ctx, f2, 0.05, 0.5, 0.65, 1.7, fill='#e9ecef')                      # bins
        F.rect(ctx, f2, 0.05, 1.9, 0.65, 3.1, fill='#e9ecef')
    elif rid == 'G11':         # water & nutrient recycling
        F.tank(ctx, fm, -1.0, 1.55, 0.5, 'H₂O', size=1.0)
        F.tank(ctx, fm, 0.4, 1.55, 0.5, 'N', size=1.0)
        F.rack(ctx, fm, -1.3, 2.7, 1.0, 3.5, fill='#e3ecf5')                       # dosing / RO rack
        F.rack(ctx, f2, 0.05, 0.5, 0.7, 1.5, fill='#e3ecf5')
    elif rid in ('G5', 'G12'): # fabrication / recycling workshop: machines along back, benches front
        n = 4 if rid == 'G5' else 3
        Rb = r.R(4.6)
        span = math.radians(r.b2 - r.b1) * Rb
        for i in range(n):
            b = r.b1 + math.degrees((i + 0.5) * span / n / Rb)
            fr = v.local(Rb, b, 1, sgn)
            F.rack(ctx, fr, -0.65, 0.0, 0.65, 1.3, fill='#e9ecef')
            fr2 = v.local(r.R(2.55), b, 1, sgn)
            F.counter(ctx, fr2, -0.85, 0.0, 0.85, 0.75)
            F.chair(ctx, fr2, 0.0, 1.05, back='v+')
        if rid == 'G12':
            F.rect(ctx, f, 0.05, 0.5, 0.65, 1.6, fill='#efe6d6')                   # shredder / sorting bins
    elif rid == 'G6':          # work sanitation & lockers
        F.rect(ctx, f, 0.05, 0.25, 1.25, 1.55, fill='#fafafa', sw=0.1)
        F.wc(ctx, f, 0.2, 0.9, ang='u-')
        F.shower(ctx, f, 0.05, 1.7, 1.1, 2.75)
        F.rack(ctx, f2, 0.05, 0.5, 0.5, 4.2, fill='#f5efe2')                      # lockers
        F.sink(ctx, f2, 0.75, 3.6, 0.4, 0.35)
    elif rid in ('G7', 'G14'): # stores
        F.shelves(ctx, f, 0.05, 0.4, 0.6, 4.3, n=7)
        F.shelves(ctx, f2, 0.05, 0.4, 0.6, 4.3, n=7)
    elif rid == 'G10':         # food lab & hydroponics control
        F.counter(ctx, f, 0.05, 0.5, 0.65, 3.0, fill='#f2f5f7')
        F.desk(ctx, f2, 0.05, 0.9, 0.65, 2.1, chair_side='u+')
        F.screen(ctx, f2, 0.05, 0.95, 0.12, 2.05)
        F.rack(ctx, f2, 0.05, 2.8, 0.65, 3.6, fill='#f2f5f7')
    elif rid == 'G13':         # crew rest
        F.table_round(ctx, fm, 0.0, 1.6, 0.5, chairs=4)
        b1_, b2_ = r.b1 + 1.0, r.b2 - 1.0
        ctx.svg.add(f'<path d="{sector_d(v, r.R(4.55), r.R(5.2), b1_, b2_)}" fill="#efe3cf" stroke="#3a3a3a" stroke-width="{num(0.12*ctx.lw)}"/>')


def doors(ctx, r):
    if not r.closed or r.rid.startswith('T') or not r.corr_wall:
        return
    R = R0 + CW if r.band == 'O' else R0 - CW
    into = 1 if r.band == 'O' else -1
    t = 0.2 if 'corr' in r.acoustic else WALL
    if r.rid.startswith('K'):
        bd = r.b1 + math.degrees(1.75 / R)
        door_on_arc(ctx, R, bd, 0.9, into, kind='slide', t=t)
        return
    big = r.rid in ('G2', 'G9', 'G5', 'G12', 'G4', 'L1', 'G1')
    w = 1.6 if big else (0.9 if r.rid in ('L5', 'L7', 'L6', 'L8', 'G6', 'G7', 'G14') else 1.0)
    kind = 'double' if big else ('slide' if r.rid in ('L6', 'L8', 'G7', 'G14') else 'swing')
    # door position: near the side that keeps furniture clear
    near_b2 = r.rid in ('L5', 'L1', 'G3', 'G10', 'G13', 'G1', 'G8')
    off = math.degrees((w / 2 + 0.75) / R)
    bd = (r.b2 - off) if near_b2 else (r.b1 + off)
    if r.rid in ('G2', 'G9', 'G5', 'G12'):
        bd = r.b1 + math.degrees(1.6 / R) if r.rid in ('G5', 'G12') else 0.5 * (r.b1 + r.b2)
    if r.rid == 'L7':
        bd = r.b1 + math.degrees(1.1 / R)
    if r.rid == 'L5':
        bd = r.b2 - math.degrees(1.1 / R)
    hinge = '+' if near_b2 else '-'
    door_on_arc(ctx, R, bd, w, into, kind=kind, hinge=hinge, t=t)


# ================================================================== nodes
def node_s3(ctx):
    v = ctx.view
    cw = cut_widths(HG)
    xm = cw['mem_out']
    for sgn in (1, -1):
        wall_arc(ctx, R0 + sgn * CW, 235, 245, t=0.16, color='#4a4a4a')
    # outer: emergency / backup EVA airlock (ante-room + chamber)
    wall_arc(ctx, R0 + 3.95, 235, 245, t=0.16, color='#4a4a4a')
    door_on_arc(ctx, R0 + CW, 240.0, 1.2, 1, kind='hatch', hinge='-', t=0.16)          # vestibule -> ante-room
    door_on_arc(ctx, R0 + 3.95, 242.3, 1.2, 1, kind='hatch', hinge='-', t=0.16)        # ante-room -> chamber
    door_on_arc(ctx, R0 + xm + 0.11, 238.0, 1.2, -1, kind='hatch', hinge='+', t=0.22)  # exterior hatch, opens inward
    for b in (236.1, 237.3):
        F.suit(ctx, v.local(R0 + 3.15, b, 1, 1), 0, 0, s=0.9)
    F.rect(ctx, v.local(R0 + 2.35, 243.6, 1, 1), -0.75, -0.2, 0.75, 0.2, fill='#f5efe2')   # bench
    F.rack(ctx, v.local(R0 + 5.6, 243.4, 1, 1), -0.45, -0.3, 0.45, 0.3, fill='#f5efe2')    # dust bin / tools
    # inner: emergency equipment & PPE
    door_on_arc(ctx, R0 - CW, 238.6, 1.0, -1, kind='hatch', hinge='-', t=0.16)
    f = v.local(R0 - 3.4, 240, 1, -1)
    F.shelves(ctx, f, -2.0, -0.6, -1.4, 1.6, n=4)
    F.shelves(ctx, f, 1.4, -0.6, 2.0, 1.6, n=4)
    F.circ(ctx, f, 0, 0.2, 0.18, fill='#e05a4f', stroke='#7a2a22', sw=0.08)
    F.suit(ctx, v.local(R0 - 5.3, 239.0, 1, -1), 0, 0, s=0.9)
    F.suit(ctx, v.local(R0 - 5.3, 241.0, 1, -1), 0, 0, s=0.9)


# ================================================================== full ring ground floor
def _annulus(ctx, Rin, Rout, fill, extra='stroke="none"'):
    v = ctx.view
    for b1, b2 in ((0, 180), (180, 360)):
        ctx.svg.add(f'<path d="{sector_d(v, Rin, Rout, b1, b2)}" fill="{fill}" {extra}/>')


def corridor_ring(ctx):
    v, svg = ctx.view, ctx.svg
    _annulus(ctx, R0 - X_CORR, R0 + X_CORR, CORR_FILL)
    for k in range(72):
        b = 5 * k
        svg.add(f'<path d="{radial_d(v, b, R0 - X_CORR, R0 + X_CORR)}" stroke="#c9c6bd" stroke-width="{num(0.1*ctx.lw)}" stroke-dasharray="0.6,0.5"/>')
    for b1, b2 in ((0, 180), (180, 360)):
        svg.add(f'<path d="{arc_d(v, R0, b1, b2)}" fill="none" stroke="#b08a50" stroke-width="{num(0.12*ctx.lw)}" stroke-dasharray="4,0.8,0.6,0.8"/>')


def one_side_edge(ctx, band, b1, b2):
    v = ctx.view
    sgn = 1 if band == 'O' else -1
    ctx.svg.add(f'<path d="{arc_d(v, R0 + sgn * X_CORR, b1, b2)}" fill="none" stroke="#8a8478" '
                f'stroke-width="{num(0.14*ctx.lw)}" stroke-dasharray="1.2,0.7"/>')


def mezz_outline2(ctx, color='#5a5a5a'):
    v = ctx.view
    for (b1, b2) in (MZ_A, MZ_B):
        for sgn in (1, -1):
            d = sector_d(v, R0 + SLOT, R0 + MZ_EDGE, b1, b2) if sgn > 0 else sector_d(v, R0 - MZ_EDGE, R0 - SLOT, b1, b2)
            ctx.svg.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{num(0.18*ctx.lw)}" stroke-dasharray="2.2,1.0"/>')


def draw_ring(ctx, detail=True):
    v, svg = ctx.view, ctx.svg
    cw = cut_widths(HG)
    _annulus(ctx, 17.0, 38.5, 'url(#groundH)')
    for b1, b2, _ in NODES:
        draw_node(ctx, b1, b2)
    for b1, b2 in (A1, A3, A2):
        draw_shell(ctx, b1, b2, HG, show_h240=False)
    for b1, b2, _ in NODES:
        svg.add(f'<path d="{sector_d(v, R0 - cw["mem_out"], R0 + cw["mem_out"], b1, b2)}" fill="{ZONE["node"]}" stroke="none"/>')
    for b1, b2 in (A1, A3, A2):
        svg.add(f'<path d="{sector_d(v, R0 - cw["mem_in"], R0 + cw["mem_in"], b1, b2)}" fill="#ffffff" stroke="none"/>')
    g3 = arch3_rooms()
    g2 = arch2_rooms()
    others = list(g3.values()) + list(g2.values())
    for r in others:
        fill_room(ctx, r)
        if r.back:
            xb = r.x2 + 0.1
            fill_room(ctx, Room('x', 'x', r.band, r.b1, r.b2, x1=xb, x2=X_CHASE), fill=BACK_FILL)
    corridor_ring(ctx)
    for b1, b2 in (A3, A2):
        draw_chase(ctx, b1, b2, HG)
    # open social zone (cafe + plaza) - corridor lane stays marked
    svg.add(f'<path d="{sector_d(v, R0 - X_CORR, R0 + X_CORR, 300, 310)}" fill="#fbf4e4" stroke="none" opacity="0.75"/>')
    corridor_edges(ctx, 300, 310)
    for r in others:
        if r.rid.startswith('T'):
            one_side_edge(ctx, r.band, r.b1, r.b2)
    # Arch 1 interior (identical to sheets 1-2)
    g1 = arch1.draw_interior(ctx, detail=detail, draw_corridor=False)
    if detail:
        for r in others:
            furnish(ctx, r)
        node_s3(ctx)
        for r in others:
            if r.rid.startswith('T'):
                sgn = 1 if r.band == 'O' else -1
                f = v.local(R0 + sgn * (3.95), r.bm, 1, sgn)
                F.shelves(ctx, f, -0.55, 0.15, 0.55, 0.65, n=3)
    for r in others:
        walls_room(ctx, r)
        if r.back:
            sgn = 1 if r.band == 'O' else -1
            xb = r.x2 + 0.05
            wall_rad(ctx, r.b1, R0 + sgn * xb, R0 + sgn * cw['mem_in'])
            wall_rad(ctx, r.b2, R0 + sgn * xb, R0 + sgn * cw['mem_in'])
    for b in (235, 245):
        node_bulkhead(ctx, b)
    door_on_rad(ctx, 235, R0 - 0.6, R0 + 0.6, into=-1, kind='hatch', hinge='-', t=0.25)
    door_on_rad(ctx, 245, R0 - 0.6, R0 + 0.6, into=1, kind='hatch', hinge='+', t=0.25)
    for r in others:
        doors(ctx, r)
        if r.rid.startswith('T'):
            sgn = 1 if r.band == 'O' else -1
            door_on_arc(ctx, R0 + sgn * (r.x2 + 0.05), r.bm, 0.7, sgn, kind='slide')
    for rid, (band, b) in STAIRS2.items():
        sgn = 1 if band == 'O' else -1
        spiral_stair(ctx, R0 + sgn * STAIR_X, b, d=STAIR_D)
    mezz_outline2(ctx)
    arch1.mezz_outline(ctx)
    return g1, g3, g2


# ================================================================== Arch 2 mezzanine (+3.00, cut +4.20)
def draw_arch2_mezz(ctx, detail=True):
    v, svg = ctx.view, ctx.svg
    cw = cut_widths(HM)
    xm = cw['mem_in']
    g2 = arch2_rooms()
    mz = arch2_mezz()
    draw_ground(ctx, 238, 362, 18.5, 37.0)
    draw_node(ctx, 238, 245, h=HM)
    draw_node(ctx, 355, 362, h=HM)
    draw_shell(ctx, 245, 355, HM, show_floor_edge=False, show_h240=False)
    for b1, b2 in ((238, 245), (355, 362)):
        svg.add(f'<path d="{sector_d(v, R0 - cw["mem_out"], R0 + cw["mem_out"], b1, b2)}" fill="url(#roofH)" stroke="none"/>')
    svg.add(f'<path d="{sector_d(v, R0 - xm, R0 + xm, 245, 355)}" fill="#fbfbfa" stroke="none"/>')
    svg.add(f'<path d="{sector_d(v, R0 - xm, R0 + xm, 245, 355)}" fill="url(#voidH)" stroke="none"/>')
    # roofs of closed rooms in the full-height social core
    for rid in ('L1', 'L3'):
        r = g2[rid]
        R1, R2 = r.R(r.x1), r.R(min(r.x2, xm))
        svg.add(f'<path d="{sector_d(v, min(R1, R2), max(R1, R2), r.b1, r.b2)}" fill="url(#roofH)" stroke="#9c9c9c" stroke-width="{num(0.15*ctx.lw)}"/>')
    for rid in ('L2', 'L4'):
        r = g2[rid]
        R1, R2 = r.R(r.x1), r.R(min(r.x2, xm))
        svg.add(f'<path d="{sector_d(v, min(R1, R2), max(R1, R2), r.b1, r.b2)}" fill="none" stroke="#b9b9b9" stroke-width="{num(0.12*ctx.lw)}" stroke-dasharray="1,0.7"/>')
    F.circ(ctx, v.local(R0 - 3.7, 303.2, 1, 1), 0, 0, 0.95, fill='none', stroke='#7fb26b', sw=0.18)
    F.circ(ctx, v.local(R0 - 3.2, 308.0, 1, 1), 0, 0, 0.7, fill='none', stroke='#7fb26b', sw=0.18)
    for sgn in (1, -1):
        svg.add(f'<path d="{arc_d(v, R0 + sgn * X_CORR, 290, 310)}" fill="none" stroke="#a7a39a" stroke-width="{num(0.14*ctx.lw)}" stroke-dasharray="1.2,0.7"/>')
    # slabs
    for b1, b2 in (MZ_A, MZ_B):
        for sgn in (1, -1):
            d = sector_d(v, R0 + SLOT, R0 + MZ_EDGE, b1, b2) if sgn > 0 else sector_d(v, R0 - MZ_EDGE, R0 - SLOT, b1, b2)
            svg.add(f'<path d="{d}" fill="#ffffff" stroke="#262626" stroke-width="{num(0.3*ctx.lw)}"/>')
        # walkway tint
        for sgn in (1, -1):
            d = sector_d(v, R0 + SLOT, R0 + MZ_IN - 0.08, b1, b2) if sgn > 0 else sector_d(v, R0 - MZ_IN + 0.08, R0 - SLOT, b1, b2)
            svg.add(f'<path d="{d}" fill="{CORR_FILL}" stroke="none"/>')
    for b1, b2 in BRIDGES2:
        svg.add(f'<path d="{sector_d(v, R0 - SLOT, R0 + SLOT, b1, b2)}" fill="{CORR_FILL}" stroke="#262626" stroke-width="{num(0.12*ctx.lw)}"/>')
    for b1, b2 in ((BRIDGES2[0][1], BRIDGES2[1][0]), (BRIDGES2[2][1], BRIDGES2[3][0])):
        svg.add(f'<path d="{sector_d(v, R0 - SLOT, R0 + SLOT, b1, b2)}" fill="#eef1f4" stroke="none"/>')
        svg.add(f'<path d="{sector_d(v, R0 - SLOT, R0 + SLOT, b1, b2)}" fill="url(#voidH)" stroke="none"/>')
    for r in mz.values():
        fill_room(ctx, r)
    if detail:
        for r in mz.values():
            if r.rid.startswith('K'):
                cabin(ctx, r)
            elif r.rid in ('L9', 'L11'):
                f = r.frame(v, 'b1' if r.rid == 'L9' else 'b2')
                f2 = r.frame(v, 'b2' if r.rid == 'L9' else 'b1')
                for k in range(2):
                    v0 = 0.2 + 1.35 * k
                    F.rect(ctx, f, 0.05, v0, 1.2, v0 + 1.25, fill='#fafafa', sw=0.1)
                    F.wc(ctx, f, 0.2, v0 + 0.62, ang='u-')
                F.shower(ctx, f, 1.35, 1.85, 2.35, 2.85)
                F.counter(ctx, f2, 0.05, 0.9, 0.6, 2.6, fill='#f7f7f7')
                F.sink(ctx, f2, 0.32, 1.35, 0.4, 0.35)
                F.sink(ctx, f2, 0.32, 2.2, 0.4, 0.35)
            elif r.rid in ('L10', 'L12'):
                f = r.frame(v, 'b2' if r.rid == 'L10' else 'b1')
                F.shelves(ctx, f, 0.05, 0.5, 0.55, 2.9, n=5)
    for r in mz.values():
        walls_room(ctx, r, h=HM)
    # railings: slot edges between bridges, slab ends facing the full-height core, stair openings
    for (b1, b2) in ((BRIDGES2[0][1], BRIDGES2[1][0]), (BRIDGES2[2][1], BRIDGES2[3][0])):
        for sgn in (1, -1):
            rail_arc(ctx, R0 + sgn * (SLOT + 0.015), b1, b2)
    for bb in (MZ_A[1] - 0.06, MZ_B[0] + 0.06):
        rail_rad(ctx, bb, R0 - MZ_EDGE, R0 - SLOT)
        rail_rad(ctx, bb, R0 + SLOT, R0 + MZ_EDGE)
        rail_rad(ctx, bb, R0 - SLOT, R0 + SLOT)
    for rid, (band, b) in STAIRS2.items():
        r = g2[rid]
        sgn = 1 if band == 'O' else -1
        lo, hi = (MZ_A if r.b1 < 300 else MZ_B)
        rail_arc(ctx, R0 + sgn * (MZ_EDGE - 0.03), max(r.b1, lo), min(r.b2, hi))
    for r in mz.values():
        sgn = 1 if r.band == 'O' else -1
        R = R0 + sgn * (MZ_IN - 0.04)
        if r.rid.startswith('K'):
            bd = r.b1 + math.degrees(1.75 / R)
            door_on_arc(ctx, R, bd, 0.9, sgn, kind='slide', t=0.08)
        elif r.rid in ('L9', 'L11'):
            door_on_arc(ctx, R, r.bm, 0.9, sgn, kind='swing', hinge='-' if r.rid == 'L9' else '+', t=0.08)
        else:
            door_on_arc(ctx, R, r.bm, 0.8, sgn, kind='slide', t=0.08)
    for rid, (band, b) in STAIRS2.items():
        sgn = 1 if band == 'O' else -1
        f = v.local(R0 + sgn * STAIR_X, b)
        F.circ(ctx, f, 0, 0, STAIR_D / 2 + 0.06, fill='#ffffff', stroke='#262626', sw=0.25)
        spiral_stair(ctx, R0 + sgn * STAIR_X, b, d=STAIR_D, up=False, start=180)
    for b in (245, 355):
        node_bulkhead(ctx, b, h=HM)
    return g2, mz


# ================================================================== areas
def area_of(rooms):
    return sum(r.area() for r in rooms if not r.rid.startswith('T'))


def corridor_area(deg):
    return 0.5 * math.radians(deg) * ((R0 + X_CORR) ** 2 - (R0 - X_CORR) ** 2)


def node_area():
    cw = cut_widths(HG)
    return 0.5 * math.radians(10) * ((R0 + cw['mem_out']) ** 2 - (R0 - cw['mem_out']) ** 2)
