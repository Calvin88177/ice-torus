"""Sheet 3 - Sections A-A and B-B (1:50) + construction details, A1."""
import math, sys
import numpy as np
from core import SVG, View, num, text, fmt, half_width, height_at, T_ICE, T_GAP, T_MEM, R0, sector_d, arc_d, radial_d, path_poly
import sheetkit as K
import section as S
from section import SV, rect, line, poly, circle, person, chair_side, tree_elev, dim_h, dim_v, level, leader
from plan import defs as plan_defs
from furn import Ctx
import arch1

DARK = '#262626'
SLAB = 'url(#sConc)'
FADE = '#9a9a9a'


def wall(svg, sv, x1, x2, z1, z2):
    rect(svg, sv, x1, z1, x2, z2, fill=DARK, stroke='none')


def glass_rail(svg, sv, x, z0, h=1.10):
    rect(svg, sv, x - 0.015, z0, x + 0.015, z0 + h, fill='#b9d3e6', stroke='#4f7da1', sw=0.15)
    rect(svg, sv, x - 0.04, z0 + h, x + 0.04, z0 + h + 0.05, fill='#555', stroke='none')


def bed_cut(svg, sv, x1, x2, z0, head_at='x2'):
    """bed cut across its length: x1..x2 (2.0 m), z0 floor"""
    lo, hi = min(x1, x2), max(x1, x2)
    rect(svg, sv, lo, z0, hi, z0 + 0.30, fill='#f1ece4', stroke=DARK, sw=0.25)
    rect(svg, sv, lo + 0.02, z0 + 0.30, hi - 0.02, z0 + 0.50, fill='#ffffff', stroke=DARK, sw=0.25)
    if head_at == 'x2':
        px = hi - 0.42 if x2 > x1 else lo + 0.06
    else:
        px = lo + 0.06 if x2 > x1 else hi - 0.42
    S.poly(svg, sv, [(px, z0 + 0.5), (px + 0.36, z0 + 0.5), (px + 0.33, z0 + 0.64), (px + 0.03, z0 + 0.64)], fill='#ffffff', stroke=DARK, sw=0.2)


def bed_elev(svg, sv, x1, x2, z0, head_at='x2', col=FADE):
    lo, hi = min(x1, x2), max(x1, x2)
    rect(svg, sv, lo, z0, hi, z0 + 0.50, fill='#fbfbfb', stroke=col, sw=0.15)
    line(svg, sv, lo, z0 + 0.30, hi, z0 + 0.30, stroke=col, sw=0.1)
    px = (hi - 0.42) if head_at == 'x2' else lo + 0.06
    rect(svg, sv, px, z0 + 0.5, px + 0.36, z0 + 0.62, fill='#ffffff', stroke=col, sw=0.12)


def wardrobe_cut(svg, sv, x1, x2, z0, h=2.0):
    rect(svg, sv, x1, z0, x2, z0 + h, fill='#ece7dc', stroke=DARK, sw=0.25)
    line(svg, sv, x1, z0 + h * 0.75, x2, z0 + h * 0.75, stroke=DARK, sw=0.12)


def desk_cut(svg, sv, x1, x2, z0, face=1):
    rect(svg, sv, x1, z0 + 0.72, x2, z0 + 0.76, fill=DARK, stroke='none')
    line(svg, sv, x2 - 0.05 if face > 0 else x1 + 0.05, z0, x2 - 0.05 if face > 0 else x1 + 0.05, z0 + 0.72, stroke=DARK, sw=0.3)
    # monitor
    mx = x2 - 0.12 if face > 0 else x1 + 0.12
    rect(svg, sv, mx - 0.02, z0 + 0.78, mx + 0.02, z0 + 1.15, fill='#333', stroke='none')


def ceiling(svg, sv, x1, x2, z, t=0.05):
    rect(svg, sv, min(x1, x2), z, max(x1, x2), z + t, fill='#cfcfcf', stroke=DARK, sw=0.2)


def slab(svg, sv, x1, x2):
    rect(svg, sv, min(x1, x2), 2.70, max(x1, x2), 3.00, fill=SLAB, stroke=DARK, sw=0.3)


def door_open(svg, sv, x, z0, head=2.10, top=2.70, t=0.10):
    """wall cut through a door opening: wall only above door head; leaf shown slid"""
    rect(svg, sv, x - t / 2, z0 + head, x + t / 2, z0 + (top - 0.0) if top > head else z0 + head, fill=DARK, stroke='none')
    line(svg, sv, x - t / 2, z0, x - t / 2, z0 + head, stroke='#777', sw=0.12, extra='stroke-dasharray="0.6,0.4"')
    line(svg, sv, x + t / 2, z0, x + t / 2, z0 + head, stroke='#777', sw=0.12, extra='stroke-dasharray="0.6,0.4"')


def interior_clip(svg, sv, cid):
    pts_ = [(half_width(T_ICE + T_GAP + T_MEM, z), z) for z in np.linspace(-0.02, 8.27, 120)]
    full = [(-x, z) for x, z in pts_[::-1]] + pts_
    P = [sv.p(x, z) for x, z in full]
    svg.d(f'<clipPath id="{cid}"><path d="{path_poly(P)}"/></clipPath>')
    return f'<g clip-path="url(#{cid})">'


# ======================================================================= A-A
def section_A(svg, sv):
    S.ground(svg, sv)
    S.shell(svg, sv)
    # light from crown strip through the slot
    S.light_cone(svg, sv, -0.6, 0.6, 8.16, 0.2, spread=0.25)
    svg.add(interior_clip(svg, sv, 'clipA'))
    # --- ground floor
    # corridor walls (cut), inner wall solid, outer wall with door opening (cut through K1 door)
    wall(svg, sv, -1.90, -1.80, 0, 2.70)
    door_open(svg, sv, 1.85, 0.0, head=2.10, top=2.70)
    # pocket door leaf (in pocket, seen) for K1
    rect(svg, sv, 1.83, 0.02, 1.87, 2.08, fill='#ffffff', stroke='#555', sw=0.12)
    # inner K5 (x -1.90..-4.90) back wall + ceiling panel
    wall(svg, sv, -5.00, -4.90, 0, 2.70)
    ceiling(svg, sv, -5.00, -4.50, 2.65)
    # outer K1 (1.90..5.20) back wall + ceiling panel
    wall(svg, sv, 5.20, 5.30, 0, 2.70)
    ceiling(svg, sv, 4.50, 5.30, 2.65)
    # K5 furniture (cut): wardrobe + bed (head at back wall)
    wardrobe_cut(svg, sv, -2.56, -1.98, 0)
    bed_cut(svg, sv, -4.85, -2.85, 0, head_at='x1')
    person(svg, sv, -3.4, 0.0, 'sit', face=1, col='#4b5b6b')
    # K1 furniture: beyond = bed (against far partition) + wardrobe (faded); cut = desk + chair + person
    bed_elev(svg, sv, 3.15, 5.15, 0, head_at='x2')
    rect(svg, sv, 1.98, 0, 2.56, 2.0, fill='#fbfbfb', stroke=FADE, sw=0.15)
    desk_cut(svg, sv, 4.55, 5.15, 0, face=1)
    chair_side(svg, sv, 4.15, 0.0, face=1, col='#555')
    person(svg, sv, 4.05, 0.0, 'sit', face=1, col='#4b5b6b')
    # low storage behind cabins
    for sgn, xa in ((-1, 5.0), (1, 5.30)):
        rect(svg, sv, sgn * xa if sgn > 0 else -6.55, 0, sgn * 6.55 if sgn > 0 else -xa, 1.10, fill='#ece7dc', stroke=DARK, sw=0.2)
    # corridor person
    person(svg, sv, -0.75, 0.0, 'walk', face=1, col='#59687a')
    # --- mezzanine slabs, rails
    slab(svg, sv, -4.50, -0.30)
    slab(svg, sv, 0.30, 4.50)
    glass_rail(svg, sv, -0.315, 3.0)
    glass_rail(svg, sv, 0.315, 3.0)
    # mezz inner K11 (x -1.42..-4.42), walls to +5.45
    wall(svg, sv, -1.42, -1.34, 3.0, 5.45)
    wall(svg, sv, -4.50, -4.42, 3.0, 5.45)
    ceiling(svg, sv, -4.50, -1.34, 5.40)
    wardrobe_cut(svg, sv, -2.08, -1.50, 3.0)
    bed_cut(svg, sv, -4.37, -2.37, 3.0, head_at='x1')
    person(svg, sv, -3.0, 3.0, 'sit', face=-1, col='#4b5b6b')
    # mezz outer K7 (1.42..4.42), walkway wall cut through door
    door_open(svg, sv, 1.38, 3.0, head=2.10, top=2.45, t=0.08)
    wall(svg, sv, 4.42, 4.50, 3.0, 5.45)
    ceiling(svg, sv, 1.34, 4.50, 5.40)
    bed_elev(svg, sv, 2.37, 4.37, 3.0, head_at='x2')
    desk_cut(svg, sv, 3.80, 4.37, 3.0, face=1)
    chair_side(svg, sv, 3.45, 3.0, face=1, col='#555')
    person(svg, sv, 3.35, 3.0, 'sit', face=1, col='#4b5b6b')
    # walkway person
    person(svg, sv, 0.85, 3.0, 'walk', face=-1, col='#59687a')
    svg.add('</g>')
    S.chase(svg, sv, 1)
    S.chase(svg, sv, -1)
    # mezzanine edge rails at outer slab edge not needed in cabin zone


XD = (-9.0, -10.15, -11.3)


def vdims(svg, sv, rows):
    """rows: list of (column index, z1, z2, label)"""
    for col, z1, z2, lab in rows:
        dim_v(svg, sv, XD[col], z1, z2, lab, size=2.0, ext_to=(-8.2 if col == 0 else None))


def levels_in(svg, sv, items):
    for x, z, lab in items:
        level(svg, sv, x, z, lab, side=1, size=1.85, line_len=3)


def right_labels(svg, sv, xt, items, y_top, y_bot, size=2.0):
    """items: list of ((x,z) target, [lines]) ; distributed between y_top..y_bot in target-z order"""
    items = sorted(items, key=lambda it: -it[0][1])
    n = len(items)
    ys = [y_top + (y_bot - y_top) * i / max(1, n - 1) for i in range(n)]
    for (pt, lines), ty in zip(items, ys):
        leader(svg, sv, pt[0], pt[1], xt, ty, lines, size=size, anchor='start')


def hw(d, z):
    return half_width(d, z)


def annotate_A(svg, sv):
    vdims(svg, sv, [(0, 0.0, 2.70, '2,70'), (0, 3.00, 5.40, '2,40'), (0, 5.40, 8.30, '2,90'),
                    (1, 0.0, 8.30, '8,30 tinggi bersih puncak'), (2, 0.0, 9.00, '9,00 puncak luar es')])
    levels_in(svg, sv, [(-6.3, 0.0, '±0,00'), (-5.85, 2.70, '+2,70'), (-5.45, 3.00, '+3,00 mezanin'),
                        (-4.25, 5.45, '+5,40 plafon kabin'), (1.0, 8.30, '+8,30'), (1.0, 9.00, '+9,00')])
    zb = -1.45
    chain = [(-8.0, -7.26, '0,74'), (-7.26, -1.80, '5,46'), (-1.80, 1.80, '3,60 koridor'), (1.80, 7.26, '5,46'), (7.26, 8.0, '0,74')]
    for x1, x2, lab in chain:
        dim_h(svg, sv, x1, x2, zb, lab, off=5, size=2.0)
    dim_h(svg, sv, -7.26, 7.26, zb, '14,52 lebar lantai bersih (muka membran)', off=10.5, size=2.1)
    dim_h(svg, sv, -8.0, 8.0, zb, '16,00 bentang kaki es (muka luar @ ±0,00)', off=16, size=2.1)
    zc = 6.35
    for x1, x2, lab in ((-1.34, -0.30, '1,04'), (-0.30, 0.30, '0,60'), (0.30, 1.34, '1,04')):
        dim_h(svg, sv, x1, x2, zc, lab, off=0, size=1.8)
    tx, ty = sv.p(0, zc + 0.5)
    svg.add(text(tx, ty - 0.6, 'selasar · slot cahaya · selasar', size=1.6, fill='#7a2a12'))
    for x, z, lab in ((-3.4, 2.25, 'K5 · lantai dasar · 3,00 × 2,44'), (3.55, 2.25, 'K1 · lantai dasar · 3,30 × 2,51'),
                      (-2.9, 4.95, 'K11 · mezanin · 3,00 × 2,49'), (2.9, 4.95, 'K7 · mezanin · 3,00 × 2,47')):
        tx, ty = sv.p(x, z)
        svg.add(text(tx, ty, lab, size=1.8, weight=700, fill='#3b2f4a'))
    tx, ty = sv.p(0, 1.95)
    svg.add(text(tx, ty, 'KORIDOR 3,60', size=1.8, weight=800, fill='#6a645a'))
    tx, ty = sv.p(0, 1.6)
    svg.add(text(tx, ty, 'h = 2,70 · bebas', size=1.5, fill='#6a645a'))


def labels_A(svg, sv, xt, y_top, y_bot):
    items = [((0.45, 8.15), ['Pita cahaya sirkadian', 'simulated daylight di puncak membran']),
             ((hw(0.30, 7.0), 7.0), ['Cangkang es katenari 0,60 m', 'dicor dalam liner film · ≤ −50 °C']),
             ((hw(0.65, 6.2), 6.2), ['Celah insulasi CO₂ 0,10 m', 'muka ε-rendah · R ≈ 4,4 m²K/W']),
             ((hw(0.71, 5.6), 5.6), ['Membran inflatable ganda', 'memikul tekanan kabin']),
             ((4.46, 5.42), ['Plafon kabin +5,40', 'tinggi bersih 2,40 m']),
             ((0.32, 3.9), ['Pagar kaca 1,10 m', 'tepi slot cahaya 0,60 m']),
             ((3.6, 2.85), ['Plat mezanin +3,00', 't = 0,30 · hanya x ≤ ±4,50 m']),
             ((6.75, 0.6), ['Chase utilitas', 'sudut lantai–membran']),
             ((5.8, -0.12), ['Lantai panggung + plenum 0,20', 'insulasi 0,10 · lantai membran']),
             ((8.02, -0.22), ['Kaki es tertanam 0,30 m', 'regolit dipadatkan']),
             ((8.9, -1.2), ['Tanah beku kaya es', 'ground ice (SHARAD)'])]
    right_labels(svg, sv, xt, items, y_top, y_bot)


# ======================================================================= B-B
def section_B(svg, sv):
    S.ground(svg, sv)
    S.shell(svg, sv)
    S.light_cone(svg, sv, -0.6, 0.6, 8.16, 2.0, spread=1.6)
    svg.add(interior_clip(svg, sv, 'clipB'))
    # ---- background (beyond) elements first
    # inner garden trees seen above hydroponics roof (b 73 / 68.5 / 63)
    tree_elev(svg, sv, -3.05, 0.0, h=4.4, w=2.0, faded=True)
    tree_elev(svg, sv, -4.15, 0.0, h=5.3, w=2.6, faded=True)
    tree_elev(svg, sv, -3.8, 0.0, h=4.9, w=2.3, faded=True)
    # far partition of the galley zone (lab wall at b = 50) - light background
    rect(svg, sv, 1.90, 0.0, 6.60, 2.70, fill='#f6f4ef', stroke='none')
    line(svg, sv, 1.90, 2.70, 6.60, 2.70, stroke='#c8c3b8', sw=0.15)
    # galley beyond (b 50..60): back counter, fridge, island + stools, person cooking
    rect(svg, sv, 5.25, 0, 5.85, 0.9, fill='#f3f3f3', stroke=FADE, sw=0.15)
    rect(svg, sv, 4.55, 0, 5.15, 1.85, fill='#eef3f6', stroke=FADE, sw=0.15)
    rect(svg, sv, 3.40, 0, 4.30, 0.92, fill='#f6efe2', stroke=FADE, sw=0.15)
    for x in (3.05,):
        line(svg, sv, x, 0, x, 0.65, stroke=FADE, sw=0.2)
        rect(svg, sv, x - 0.18, 0.65, x + 0.18, 0.7, fill=FADE, stroke='none')
    person(svg, sv, 4.75, 0.0, 'stand', face=-1, col='#b8c0c8')
    # organic planter fin (b 60.5) in front of galley
    S.poly(svg, sv, [(2.35, 0), (4.35, 0), (4.35, 1.05), (3.35, 1.25), (2.35, 1.05)], fill='#ece2d2', stroke='#8a7660', sw=0.2)
    for x in (2.7, 3.3, 3.9):
        circle(svg, sv, x, 1.35, 0.28, fill='#a8d08f', stroke='#4f8a3c', sw=0.12)
    # far mezzanine front (starts b=85, seen from b=80 looking to b<80? no - behind viewer) -> omitted
    # ---- hydroponics (inner, cut at b=80): closed room, ceiling +2.70; far wall hides the garden below +2,70
    rect(svg, sv, -6.60, 0.0, -1.90, 2.70, fill='#f2f5ee', stroke='none')
    wall(svg, sv, -1.90, -1.80, 0, 2.75)
    ceiling(svg, sv, -6.15, -1.80, 2.70, t=0.08)
    # rack (beyond, b=78): x -2.9..-5.45, 4 tiers
    for i, z in enumerate((0.15, 0.68, 1.21, 1.74, 2.27)):
        rect(svg, sv, -5.45, z, -2.90, z + 0.04, fill='#7a7a7a', stroke='none')
        if i < 4:
            for x in np.arange(-5.3, -2.95, 0.32):
                S.poly(svg, sv, [(x - 0.13, z + 0.04), (x + 0.13, z + 0.04), (x + 0.09, z + 0.30), (x - 0.09, z + 0.30)], fill='#8cbf73', stroke='#4f8a3c', sw=0.08)
            rect(svg, sv, -5.40, z + 0.45, -2.95, z + 0.47, fill='#d46ad8', stroke='none')   # LED bar
    for x in (-5.45, -2.90):
        rect(svg, sv, x - 0.03, 0, x + 0.03, 2.35, fill='#555', stroke='none')
    person(svg, sv, -2.35, 0.0, 'kneel', face=-1, col='#4b5b6b')
    rect(svg, sv, -6.55, 0, -5.75, 0.85, fill='#f2f8ee', stroke=DARK, sw=0.2)   # nutrient table (beyond, at end)
    circle(svg, sv, -6.15, 1.05, 0.18, fill='#d7ebf8', stroke='#4a86b5', sw=0.12)
    # ---- dining (outer, cut at b=62): table + 2 chairs + seated people
    rect(svg, sv, 3.30, 0.72, 4.20, 0.77, fill=DARK, stroke='none')
    line(svg, sv, 3.75, 0.0, 3.75, 0.72, stroke=DARK, sw=0.5)
    rect(svg, sv, 3.45, 0.0, 4.05, 0.04, fill=DARK, stroke='none')
    chair_side(svg, sv, 2.87, 0.0, face=-1, col='#333')
    chair_side(svg, sv, 4.63, 0.0, face=1, col='#333')
    person(svg, sv, 2.95, 0.0, 'sit', face=1, col='#4b5b6b')
    person(svg, sv, 4.55, 0.0, 'sit', face=-1, col='#4b5b6b')
    # ---- corridor / plaza
    person(svg, sv, -0.6, 0.0, 'walk', face=1, col='#59687a')
    person(svg, sv, 1.35, 0.0, 'stand', face=-1, col='#59687a')
    # jog line
    line(svg, sv, 1.0, 0.0, 1.0, 8.0, stroke='#c0391b', sw=0.25, extra='stroke-dasharray="2,1.2"')
    svg.add('</g>')
    S.chase(svg, sv, 1)
    S.chase(svg, sv, -1)


def annotate_B(svg, sv):
    vdims(svg, sv, [(0, 0.0, 2.70, '2,70'), (1, 0.0, 8.30, '8,30 void tinggi penuh'), (2, 0.0, 9.00, '9,00 puncak luar es')])
    levels_in(svg, sv, [(-6.3, 0.0, '±0,00'), (-5.6, 2.78, '+2,70 plafon hidroponik'), (1.0, 8.30, '+8,30'), (1.0, 9.00, '+9,00')])
    zb = -1.45
    for x1, x2, lab in ((-7.26, -1.80, '5,46'), (-1.80, 1.80, '3,60 lajur bebas'), (1.80, 7.26, '5,46')):
        dim_h(svg, sv, x1, x2, zb, lab, off=5, size=2.0)
    dim_h(svg, sv, -8.0, 8.0, zb, '16,00 bentang kaki es · 14,52 lantai bersih', off=10.5, size=2.1)
    for x, z, lab, sz, col in ((-4.25, 2.38, 'HIDROPONIK · ruang tertutup (b = 80°)', 1.7, '#3b3326'),
                               (3.9, 2.25, 'RUANG MAKAN (b = 62°)', 1.8, '#3b3326'),
                               (0.0, 6.0, 'PLAZA KOMUNAL · VOID 8,30 m', 2.3, '#9a6b1f')):
        tx, ty = sv.p(x, z)
        svg.add(text(tx, ty, lab, size=sz, weight=800, fill=col, ls='0.2'))
    tx, ty = sv.p(3.9, 1.9)
    svg.add(text(tx, ty, 'galley terbuka di belakang (tampak)', size=1.5, fill='#666'))
    tx, ty = sv.p(1.0, 7.6)
    svg.add(text(tx + 1.2, ty, 'lompatan garis potong', size=1.5, fill='#c0391b', anchor='start'))
    svg.add(text(tx + 1.2, ty + 2.2, 'b = 62° | 80° (x = +1,00)', size=1.5, fill='#c0391b', anchor='start'))


def labels_B(svg, sv, xt, y_top, y_bot):
    items = [((0.45, 8.15), ['Pita cahaya sirkadian', 'siklus siang–malam, spektrum penuh']),
             ((hw(0.30, 6.6), 6.6), ['Cangkang es 0,60 + celah CO₂ 0,10', 'membran ganda di sisi dalam']),
             ((4.4, 1.3), ['Partisi organik / pot tanaman', 'ceruk duduk, tak memotong koridor']),
             ((5.2, 1.6), ['Galley (tampak)', 'island, kulkas, counter belakang']),
             ((3.75, 0.76), ['Meja makan bersama (terpotong)', 'kursi & figur duduk']),
             ((6.75, 0.6), ['Chase utilitas', 'udara · air · listrik']),
             ((8.9, -1.2), ['Tanah beku kaya es', 'di bawah regolit dipadatkan'])]
    right_labels(svg, sv, xt, items, y_top, y_bot)
    # left-side labels for the inner (hydroponics) part, placed inside the void above the room
    for (x, z), (l1, l2), (tx_m, tz_m) in ((( -4.15, 5.0), ('Taman sosial (tampak)', 'pohon dalam pot · b = 63–73°'), (-5.6, 7.15)),
                                         ((-4.2, 1.5), ('Rak tanam vertikal 4 tingkat', 'LED spektrum tumbuh'), (-5.95, 4.45))):
        p = sv.p(x, z)
        q = sv.p(tx_m, tz_m)
        svg.add(f'<path d="M{num(p[0])},{num(p[1])} L{num(q[0])},{num(q[1] + 1.5)}" fill="none" stroke="#333" stroke-width="0.15" marker-start="url(#lead)"/>')
        svg.add(text(q[0], q[1], l1, size=1.9, weight=700, anchor='middle'))
        svg.add(text(q[0], q[1] - 2.4, l2, size=1.7, fill='#444', anchor='middle'))


# ======================================================================= details
def detail_foot(svg, ox, oy):
    """Detail 1 at 1:20: foot of the shell, chase and floor (outer side, x 5.9..8.6, z -0.7..1.5)"""
    sv = SV(ox, oy, 20)
    cid = 'clipD1'
    x0, z0, x1, z1 = 5.75, -0.75, 8.75, 1.55
    a, b = sv.p(x0, z1), sv.p(x1, z0)
    svg.d(f'<clipPath id="{cid}"><rect x="{num(a[0])}" y="{num(a[1])}" width="{num(b[0]-a[0])}" height="{num(b[1]-a[1])}"/></clipPath>')
    svg.add(f'<g clip-path="url(#{cid})">')
    S.ground(svg, sv, xw=12)
    S.shell(svg, sv, light=False)
    # metallised film lines (low-e) on liner inner face & membrane outer face
    for d, col in ((T_ICE - 0.004, '#9aa4ad'), (T_ICE + T_GAP + 0.003, '#9aa4ad')):
        pts_ = [(half_width(d, z), z) for z in np.linspace(-0.2, 1.6, 40)]
        S.poly(svg, sv, pts_, fill='none', stroke=col, sw=0.5, close=False)
    pts_ = [(half_width(0.004, z), z) for z in np.linspace(-0.3, 1.6, 40)]
    S.poly(svg, sv, pts_, fill='none', stroke='#555', sw=0.35, close=False, extra='stroke-dasharray="1.2,0.5"')
    # anchor strap from membrane to floor anchor
    line(svg, sv, 7.05, 0.35, 6.75, -0.18, stroke='#b5532e', sw=0.35)
    circle(svg, sv, 6.75, -0.18, 0.03, fill='#b5532e', stroke='none')
    svg.add('</g>')
    svg.add(f'<rect x="{num(a[0])}" y="{num(a[1])}" width="{num(b[0]-a[0])}" height="{num(b[1]-a[1])}" fill="none" stroke="#151515" stroke-width="0.3"/>')
    return sv, (a, b)


def detail_layers(svg, x, y, w_mm_per_m=200):
    """Detail 2 at 1:5: straight build-up through the wall, outside (left) -> inside (right)"""
    s = w_mm_per_m
    layers = [('liner luar', 0.006, '#cfcfcf'), ('es', 0.600, 'url(#sIce)'), ('liner dalam ε-rendah', 0.006, '#b7c0c8'),
              ('CO₂', 0.100, 'url(#sGap)'), ('membran luar', 0.006, '#163f66'), ('celah pantau', 0.013, '#e8eef4'),
              ('membran dalam', 0.006, '#2e5f8f')]
    H = 28
    xx = x
    xs = []
    for name, t, fill in layers:
        wd = max(t * s, 1.2)
        svg.add(f'<rect x="{num(xx)}" y="{num(y)}" width="{num(wd)}" height="{H}" fill="{fill}" stroke="#333" stroke-width="0.2"/>')
        xs.append((xx, wd, name, t))
        xx += wd
    # exterior / interior tints
    svg.add(f'<rect x="{num(x - 14)}" y="{num(y)}" width="14" height="{H}" fill="#f7e9de"/>')
    svg.add(f'<rect x="{num(xx)}" y="{num(y)}" width="16" height="{H}" fill="#fffaf0"/>')
    svg.add(text(x - 7, y + H / 2, 'LUAR', size=2.0, weight=800, fill='#8c2f14', rot=-90))
    svg.add(text(xx + 8, y + H / 2, 'DALAM', size=2.0, weight=800, fill='#163f66', rot=-90))
    return xs, xx


# ======================================================================= detail 3: arch membrane <-> node frame
def detail_node_joint(svg, X0, Y0, scale=20, U=(-0.7, 1.3), Wr=(6.45, 7.75)):
    """plan detail at +1.20 of the junction Arch 1 / node S1 (outer side). u: tangential from bulkhead axis
    (+ into the arch), w: radial offset from the ring axis (+ outward, drawn upward)."""
    from core import cut_widths
    from plan import NODE_C, HATCH_C
    k = 1000.0 / scale
    U0, U1 = U
    W0, W1 = Wr

    def P(u, w):
        return (X0 + (u - U0) * k, Y0 - (w - W1) * k)

    def R(u1, w1, u2, w2, fill, stroke='none', sw=0.0, extra=''):
        a, b = P(min(u1, u2), max(w1, w2)), P(max(u1, u2), min(w1, w2))
        svg.add(f'<rect x="{num(a[0])}" y="{num(a[1])}" width="{num(b[0]-a[0])}" height="{num(b[1]-a[1])}" fill="{fill}" '
                f'stroke="{stroke}" stroke-width="{num(sw)}" {extra}/>')

    def L(u1, w1, u2, w2, col='#333', sw=0.2, extra=''):
        a, b = P(u1, w1), P(u2, w2)
        svg.add(f'<line x1="{num(a[0])}" y1="{num(a[1])}" x2="{num(b[0])}" y2="{num(b[1])}" stroke="{col}" stroke-width="{num(sw)}" {extra}/>')

    cw = cut_widths(1.2)
    m_in, m_out, i_in, i_out = cw['mem_in'], cw['mem_out'], cw['ice_in'], cw['ice_out']
    nw = m_out + 0.22                 # node outer wall face
    tb = 0.125                        # bulkhead half thickness
    a, b = P(U0, W1), P(U1, W0)
    cid = 'clipD3'
    svg.d(f'<clipPath id="{cid}"><rect x="{num(a[0])}" y="{num(a[1])}" width="{num(b[0]-a[0])}" height="{num(b[1]-a[1])}"/></clipPath>')
    svg.add(f'<g clip-path="url(#{cid})">')
    R(U0, W0, U1, W1, '#ffffff')
    # exterior beyond the ice (Mars atmosphere, ground seen below)
    R(0.75, i_out, U1, W1, '#f7f1e9')
    # regolith bag shield of the node, lapping over the joint
    R(U0, nw, tb, W1, '#d9c7ae')
    R(tb, i_out, 0.75, W1, '#d9c7ae')
    for row in range(4):
        wb = nw + 0.02 + row * 0.27
        off = 0.0 if row % 2 == 0 else 0.26
        for col in range(6):
            u1 = U0 - 0.2 + off + col * 0.52
            u2 = u1 + 0.48
            w1, w2 = wb, wb + 0.24
            # clip bags to the shield outline
            if w1 < i_out and u2 > tb:
                u2 = min(u2, tb - 0.01)
            if u1 >= u2:
                continue
            if u1 > 0.75:
                continue
            u2 = min(u2, 0.74)
            if w2 > W1 + 0.3:
                continue
            a_, b_ = P(u1, w2), P(u2, w1)
            svg.add(f'<rect x="{num(a_[0])}" y="{num(a_[1])}" width="{num(b_[0]-a_[0])}" height="{num(b_[1]-a_[1])}" rx="{num(0.07*k)}" '
                    f'fill="#e6d7c2" stroke="#a88f6e" stroke-width="0.18"/>')
    # ice shell (cut) with liner films, ending at the joint
    R(0.55, i_in, U1, i_out, 'url(#sIce)', '#3f74a1', 0.25)
    L(0.55, i_in, U1, i_in, '#9aa4ad', 0.45)
    L(0.55, i_out, U1, i_out, '#555', 0.3, 'stroke-dasharray="1.2,0.5"')
    L(0.55, i_in, 0.55, i_out, '#555', 0.3, 'stroke-dasharray="1.2,0.5"')
    # CO2 pocket of the arch (closed at the node end)
    R(0.55, m_out, U1, i_in, 'url(#sGap)')
    # expansion joint filler: closes the CO2 pocket end, lets the ice creep/move
    R(tb, m_out + 0.036, 0.55, i_out, '#fff3c4', '#b08a50', 0.2)
    R(0.43, m_out, 0.55, m_out + 0.036, '#fff3c4', '#b08a50', 0.2)
    for uu in [0.17 + 0.09 * i for i in range(5)]:
        for ww in [m_out + 0.09 + 0.1 * j for j in range(7)]:
            x, y = P(uu, ww)
            svg.add(f'<circle cx="{num(x)}" cy="{num(y)}" r="0.55" fill="none" stroke="#c9a96a" stroke-width="0.15"/>')
    # node frame: outer wall + bulkhead (cut, solid)
    R(U0, m_out, -tb, nw, NODE_C)
    R(-tb, W0, tb, nw, NODE_C)
    # collar welded to the bulkhead (membrane seat)
    R(tb, m_in - 0.032, 0.45, m_in, '#8d939a', '#3a3a3a', 0.2)
    # double membrane (restraint + bladder), drawn slightly thickened, wrapped on the collar
    R(0.14, m_in, U1, m_out, '#e9f0f6')
    L(0.14, m_out, U1, m_out, '#163f66', 0.55)
    L(0.14, m_in, U1, m_in, '#2e5f8f', 0.35)
    x, y = P(0.155, m_in + 0.0135)
    svg.add(f'<circle cx="{num(x)}" cy="{num(y)}" r="{num(0.016*k)}" fill="#163f66"/>')          # keder bead
    # clamp band + bolts, O-rings
    R(0.17, m_out, 0.43, m_out + 0.036, '#b5532e', '#7a3216', 0.2)
    for uu in (0.24, 0.36):
        x, y = P(uu, m_out + 0.018)
        svg.add(f'<circle cx="{num(x)}" cy="{num(y)}" r="{num(0.011*k)}" fill="#ffffff" stroke="#3a1a0e" stroke-width="0.15"/>')
    for uu in (0.21, 0.39):
        x, y = P(uu, m_in - 0.004)
        svg.add(f'<circle cx="{num(x)}" cy="{num(y)}" r="{num(0.008*k)}" fill="#151515"/>')
    svg.add('</g>')
    svg.add(f'<rect x="{num(a[0])}" y="{num(a[1])}" width="{num(b[0]-a[0])}" height="{num(b[1]-a[1])}" fill="none" stroke="#151515" stroke-width="0.3"/>')
    # side captions
    x, y = P(-0.42, 6.58)
    svg.add(text(x, y, 'S1 · node', size=2.0, weight=800, fill='#5b5f63'))
    svg.add(text(x, y + 2.8, 'ruang bertekanan', size=1.7, fill='#666'))
    x, y = P(0.95, 6.58)
    svg.add(text(x, y, 'ARCH 1', size=2.0, weight=800, fill='#163f66'))
    svg.add(text(x, y + 2.8, 'ruang bertekanan', size=1.7, fill='#666'))
    x, y = P(1.05, 7.67)
    svg.add(text(x, y, 'eksterior', size=1.7, fill='#8a6a30', weight=600))
    # numbered markers
    marks = [(1, -0.42, 6.90), (2, 0.30, 6.66), (3, 0.82, 6.715), (4, 0.30, 6.905), (5, 0.95, 6.848),
             (6, 0.34, 7.25), (7, 1.0, 7.25), (8, -0.35, 7.44)]
    for n_, uu, ww in marks:
        x, y = P(uu, ww)
        svg.add(f'<circle cx="{num(x)}" cy="{num(y)}" r="1.75" fill="#ffffff" stroke="#151515" stroke-width="0.22"/>')
        svg.add(text(x, y + 0.65, str(n_), size=1.85, weight=800))
    return (a, b)


# ======================================================================= key plan
def mini_plan(svg, cx, cy, denom=700):
    v = View(denom, 0, 0, 60)
    x0, y0 = v.P(0, 0)
    xt, yt = v.P(28, 60)
    v = View(denom, cx - (xt - x0), cy - (yt - y0) + 0, 60)
    from core import cut_widths
    for b1, b2, col in ((-5, 5, '#d9c7ae'), (115, 125, '#d9c7ae')):
        svg.add(f'<path d="{sector_d(v, 19.5, 36.5, b1, b2)}" fill="{col}" stroke="#777" stroke-width="0.15"/>')
    svg.add(f'<path d="{sector_d(v, 20, 36, 5, 115)}" fill="#d9e9f5" stroke="#3f74a1" stroke-width="0.2"/>')
    svg.add(f'<path d="{sector_d(v, 20.74, 35.26, 5, 115)}" fill="#ffffff" stroke="none"/>')
    svg.add(f'<path d="{sector_d(v, 26.2, 29.8, 5, 115)}" fill="#efeeea" stroke="none"/>')
    g = arch1.rooms_ground()
    from plan import ZONE
    for r in g.values():
        R1, R2 = r.R(r.x1), r.R(r.x2)
        svg.add(f'<path d="{sector_d(v, min(R1, R2), max(R1, R2), r.b1, r.b2)}" fill="{ZONE.get(r.zone)}" stroke="#777" stroke-width="0.12"/>')
    svg.add(f'<path d="{sector_d(v, R0 + 0.3, R0 + 4.5, 85, 114.75)}" fill="none" stroke="#555" stroke-width="0.2" stroke-dasharray="1,0.6"/>')
    svg.add(f'<path d="{sector_d(v, R0 - 4.5, R0 - 0.3, 85, 114.75)}" fill="none" stroke="#555" stroke-width="0.2" stroke-dasharray="1,0.6"/>')
    def P(R, b):
        return v.P(R, b)
    def cl(pts_):
        d = 'M' + ' L'.join(f'{num(P(R, b)[0])},{num(P(R, b)[1])}' for R, b in pts_)
        svg.add(f'<path d="{d}" fill="none" stroke="#c0391b" stroke-width="0.4" stroke-dasharray="2.4,0.6,0.5,0.6"/>')
    cl([(17.5, 100), (38.5, 100)])
    cl([(38.5, 62), (29, 62)] + [(29, 62 + k) for k in range(1, 19)] + [(29, 80), (17.5, 80)])
    for R, b, lab in ((40.5, 100, 'A'), (16.0, 100, 'A'), (40.5, 62, 'B'), (16.0, 80, 'B')):
        x, y = P(R, b)
        svg.add(f'<circle cx="{num(x)}" cy="{num(y)}" r="2.2" fill="#fff" stroke="#c0391b" stroke-width="0.3"/>')
        svg.add(text(x, y + 0.8, lab, size=2.2, weight=800, fill='#c0391b'))
    x, y = P(37.5, -5)
    svg.add(text(x - 2, y + 1, 'S1', size=2.0, weight=700, fill='#8c2f14', anchor='end'))
    x, y = P(37.5, 125)
    svg.add(text(x + 2, y + 1, 'S2', size=2.0, weight=700, fill='#8c2f14', anchor='start'))
    return v


# ======================================================================= sheet
def build(path):
    svg = SVG(K.W, K.H)
    plan_defs(svg, 10)
    S.defs_section(svg, 1.0)
    K.frame(svg)
    K.header(svg, 3, 'ARCH 1 — EARLY SETTLEMENT', 'POTONGAN ARSITEKTURAL A–A & B–B  ·  detail lapisan es – CO₂ – membran & sambungan node', 'SKALA 1 : 50')

    # --- Section A-A
    svA = SV(252, 252, 50)
    section_A(svg, svA)
    annotate_A(svg, svA)
    labels_A(svg, svA, 437, 70, 280)
    K.section_heading(svg, 22, 52, 'POTONGAN A–A', 4.2, color='#c0391b')
    svg.add(text(22, 57.8, 'b = 100° (modul 20) · kabin 2 lantai + mezanin + koridor', size=2.2, anchor='start', fill='#444'))
    svg.add(text(22, 61.8, 'arah pandang ke S1 · skala 1:50', size=2.1, anchor='start', fill='#777'))

    # --- Section B-B
    svB = SV(252, 512, 50)
    section_B(svg, svB)
    annotate_B(svg, svB)
    labels_B(svg, svB, 437, 336, 540)
    K.section_heading(svg, 22, 312, 'POTONGAN B–B (bertingkat)', 4.2, color='#c0391b')
    svg.add(text(22, 317.8, 'luar: makan/galley b = 62° · tengah: plaza void · dalam: hidroponik b = 80°', size=2.2, anchor='start', fill='#444'))
    svg.add(text(22, 321.8, 'arah pandang ke S1 · skala 1:50', size=2.1, anchor='start', fill='#777'))

    # --- right column
    rx = 500
    K.section_heading(svg, rx, 62, 'KEY PLAN — POSISI POTONGAN', 3.0)
    mini_plan(svg, rx + 160, 88, denom=480)
    svg.add(text(rx, 134, 'denah lantai dasar Arch 1 (±1:480) — garis potong sama dengan lembar 1 & 2', size=1.9, anchor='start', fill='#555'))

    # Detail 1
    K.section_heading(svg, rx, 146, 'DETAIL 1 — KAKI CANGKANG, CHASE & LANTAI  (1:20)', 3.0)
    svD, (a, b) = detail_foot(svg, rx + 1 - 5.75 * 50 + 0, 150 + 1.55 * 50)
    # labels for detail 1 (sorted by height so leaders do not cross)
    tx = b[0] + 4
    items = [((half_width(0.30, 0.95), 0.95), 'cangkang es 600 · dicor dalam liner film'),
             ((half_width(0.0, 0.42), 0.42), 'liner luar = penghalang sublimasi'),
             ((half_width(0.65, 1.22), 1.22), 'celah CO₂ 100 · muka aluminized (ε rendah)'),
             ((half_width(0.712, 1.45), 1.45), 'membran ganda: restraint + bladder'),
             ((6.72, 0.66), 'chase utilitas: udara, air, listrik'),
             ((6.75, -0.18), 'strap angkur membran ke lantai'),
             ((6.25, -0.02), 'lantai panggung + plenum 0,20'),
             ((6.25, -0.25), 'insulasi lantai 0,10'),
             ((8.0, -0.30), 'kaki es tertanam 0,30'),
             ((8.5, -0.6), 'regolit dipadatkan / urugan')]
    items.sort(key=lambda it: -it[0][1])
    n = len(items)
    for i, ((x, z), lab) in enumerate(items):
        p = svD.p(x, z)
        ty = a[1] + 4 + i * ((b[1] - a[1] - 6) / (n - 1))
        svg.add(f'<path d="M{num(p[0])},{num(p[1])} L{num(tx - 2)},{num(ty - 0.7)} L{num(tx - 0.6)},{num(ty - 0.7)}" fill="none" stroke="#333" stroke-width="0.15" marker-start="url(#lead)"/>')
        svg.add(text(tx, ty, lab, size=2.0, anchor='start'))

    # Detail 2 layers: strip + numbered list
    K.section_heading(svg, rx, 276, 'DETAIL 2 — SUSUNAN LAPISAN DINDING  (1:5, tegak lurus permukaan)', 3.0)
    ys = 292
    xs, xend = detail_layers(svg, rx + 18, ys, 200)
    labs = [('liner film luar', 'penghalang sublimasi (tak berskala)'), ('ES AIR 600 mm', 'struktur + perisai radiasi · ≤ −50 °C'),
            ('liner film dalam', 'muka aluminized, ε rendah (tak berskala)'), ('CELAH CO₂ 100 mm', 'gas Mars ±0,6 kPa · R ≈ 4,4 m²K/W'),
            ('membran luar', 'gas barrier + restraint'), ('celah antar-lapis', 'pemantauan kebocoran'), ('membran dalam', 'bladder + liner interior')]
    for i, (x0, wd, name, t) in enumerate(xs):
        xc = x0 + wd / 2
        yb = ys - 2.2 - (i % 2) * 3.4 if i >= 4 else ys - 2.2
        svg.add(f'<line x1="{num(xc)}" y1="{num(ys)}" x2="{num(xc)}" y2="{num(yb + 0.9)}" stroke="#333" stroke-width="0.12"/>')
        svg.add(f'<circle cx="{num(xc)}" cy="{num(yb - 0.6)}" r="1.45" fill="#fff" stroke="#333" stroke-width="0.18"/>')
        svg.add(text(xc, yb + 0.05, str(i + 1), size=1.7, weight=800))
    svg.add(text(xs[1][0] + xs[1][1] / 2, ys + 17, 'ES AIR 600', size=2.6, weight=800, fill='#1f3d55'))
    svg.add(text(xs[3][0] + xs[3][1] / 2, ys + 17, 'CO₂ 100', size=2.0, weight=800, fill='#1f3d55'))
    lx2 = xend + 20
    for i, (l1, l2) in enumerate(labs):
        yy = ys + 1.0 + i * 4.3
        svg.add(text(lx2, yy, f'{i+1}', size=2.0, weight=800, anchor='start'))
        svg.add(text(lx2 + 3.6, yy, l1, size=2.0, weight=700, anchor='start'))
        svg.add(text(lx2 + 30.5, yy, l2, size=1.85, anchor='start', fill='#444'))
    K.lin_dim(svg, (xs[1][0], ys + 34), (xs[1][0] + xs[1][1], ys + 34), -0.1, '600', size=1.9)
    K.lin_dim(svg, (xs[3][0], ys + 34), (xs[3][0] + xs[3][1], ys + 34), -0.1, '100', size=1.9)
    svg.add(text(rx, 348, 'Tekanan kabin hanya dipikul membran; es & celah CO₂ berada pada tekanan atmosfer Mars.', size=1.95, anchor='start', fill='#333'))
    svg.add(text(rx, 352, 'Setiap arch punya tabung membran sendiri yang disegel ke rangka node S1/S2 (pemisah).', size=1.95, anchor='start', fill='#333'))

    # materials legend + notes
    ly = 370
    K.section_heading(svg, rx, ly, 'LEGENDA MATERIAL POTONGAN', 3.0)
    mats = [('url(#sIce)', 'es air (dicor in-situ)'), ('url(#sGap)', 'celah gas CO₂'), ('#163f66', 'membran inflatable ganda'),
            ('url(#sConc)', 'plat mezanin komposit'), ('url(#sIns)', 'insulasi lantai'), ('url(#sReg)', 'regolit dipadatkan / urugan'),
            ('url(#sPerma)', 'tanah beku kaya es'), ('#262626', 'dinding/partisi terpotong'), ('#b9d3e6', 'pagar kaca 1,10 m'),
            ('#fff7c9', 'pita cahaya sirkadian')]
    for i, (fill, lab) in enumerate(mats):
        col = i // 5
        row = i % 5
        xx = rx + col * 160
        yy = ly + 7 + row * 4.6
        svg.add(f'<rect x="{xx}" y="{yy - 3.0}" width="9" height="3.6" fill="{fill}" stroke="#555" stroke-width="0.15"/>')
        svg.add(text(xx + 11.5, yy, lab, size=2.0, anchor='start'))
    ny = 404
    K.section_heading(svg, rx, ny, 'CATATAN POTONGAN', 3.0)
    notes = ['Profil cangkang: katenari z = 9,00 − a·(cosh(x/a) − 1), a = 4,564 m; bentang 16,00 & tinggi 9,00 (muka luar).',
             'Muka dalam es +8,40; membran di puncak +8,30 = tinggi bersih maksimum (void plaza).',
             'Tinggi bersih ≥ 2,40 m sampai x = ±6,25 m; di bawah plat mezanin 2,70 m; kabin mezanin 2,40 m.',
             'A–A dan B–B sesuai garis potong pada lembar 1 & 2 (B–B bertingkat di x = +1,00 m).',
             'Figur manusia tinggi 1,75 m (pakaian kasual) sebagai skala; gravitasi Mars 0,38 g.',
             'Utilitas utama di plenum bawah koridor & chase kedua sisi; shaft utama di node S2.']
    K.para(svg, rx, ny + 6, notes, size=1.95, lh=1.55, bullet=True)

    # Detail 3: arch membrane <-> node frame joint
    dy = 440
    K.section_heading(svg, rx, dy, 'DETAIL 3 — SAMBUNGAN ARCH ↔ RANGKA NODE  (denah +1,20 · 1:20 · konsep)', 3.0)
    (a3, b3) = detail_node_joint(svg, rx + 1, dy + 4.5, scale=20)
    K.scale_bar(svg, rx + 1, b3[1] + 6.5, 50, ticks=(0, 0.5, 1.0), label='skala detail 1:20 (m)')
    items3 = ['Rangka node kaku: dinding luar 0,22 + bulkhead 0,25 — tidak dicor es',
              'Kerah baja dilas ke bulkhead, keliling penampang arch (dudukan membran)',
              'Membran ganda Arch 1 (restraint + bladder) — memikul tekanan kabin',
              'Pita penjepit + baut; paking O-ring ×2; ujung membran ber-keder (tali tepi)',
              'Kantong CO₂ Arch 1 ditutup di ujung → tidak tersambung ke node / arch lain',
              'Bantalan sambungan ekspansi (busa sel tertutup + liner): gerak termal & rangkak es',
              'Cangkang es 600: hanya memikul berat sendiri; ujung dicor ke bekisting liner',
              'Perisai karung regolit node, menutup sambungan dari luar']
    lx3 = b3[0] + 7
    for i, t_ in enumerate(items3):
        yy = dy + 8.0 + i * 5.0
        svg.add(f'<circle cx="{num(lx3 + 1.6)}" cy="{num(yy - 0.7)}" r="1.7" fill="#ffffff" stroke="#151515" stroke-width="0.2"/>')
        svg.add(text(lx3 + 1.6, yy - 0.05, str(i + 1), size=1.8, weight=800))
        svg.add(text(lx3 + 5.0, yy, t_, size=1.95, anchor='start', fill='#222'))
    K.para(svg, lx3, dy + 8.0 + 8 * 5.0 + 1.5,
           ['Tiap arch = tabung membran + kantong CO₂ sendiri yang dijepit ke rangka node.',
            'Bila satu arch bocor: hatch node ditutup, arch lain tetap bertekanan & tidak terbebani.'],
           size=1.95, lh=1.5, color=K.ACC, weight=600)
    K.title_block(svg, 646, 525, 183, 57, 3, 'Potongan A–A & B–B + detail lapisan & sambungan node — Arch 1', '1 : 50 · detail 1 : 20 & 1 : 5 (A1)')
    svg.save(path, 'Lembar 3 - Potongan A-A dan B-B')


if __name__ == '__main__':
    build(sys.argv[1])
