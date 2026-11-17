import math
W, H = 440, 210
o = []
def a(s): o.append(s)
def T(x, y, s, size=3.2, anchor='middle', w=500, fill='#1d1d1d', it=False, ls=0):
    a(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" text-anchor="{anchor}" font-weight="{w}" fill="{fill}"'
      f' letter-spacing="{ls}"{" font-style=\"italic\"" if it else ""}>{s}</text>')
def L(x1, y1, x2, y2, c='#2a2a2a', w=0.4, extra=''):
    a(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{c}" stroke-width="{w}" stroke-linecap="round" {extra}/>')
def P(pts, fill='none', c='#2a2a2a', w=0.4, close=True, extra=''):
    d = 'M' + ' L'.join(f'{x:.2f},{y:.2f}' for x, y in pts) + (' Z' if close else '')
    a(f'<path d="{d}" fill="{fill}" stroke="{c}" stroke-width="{w}" stroke-linejoin="round" {extra}/>')
WATER, WD, HOT, INK, STEEL = '#2f86c9', '#1d5f94', '#e0532f', '#232323', '#7d8892'
G = 132
a('''<defs>
<linearGradient id="iceG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d7e8f5"/><stop offset="1" stop-color="#b9d4ea"/></linearGradient>
<pattern id="iceH" patternUnits="userSpaceOnUse" width="5" height="5" patternTransform="rotate(40)"><rect width="5" height="5" fill="url(#iceG)"/><line x1="0" y1="0" x2="0" y2="5" stroke="#ffffff" stroke-opacity="0.55" stroke-width="0.6"/></pattern>
<linearGradient id="regG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e3c9a3"/><stop offset="1" stop-color="#cfae82"/></linearGradient>
<pattern id="regH" patternUnits="userSpaceOnUse" width="6" height="4"><rect width="6" height="4" fill="url(#regG)"/><circle cx="1.2" cy="1" r="0.4" fill="#a98762"/><circle cx="4.3" cy="2.8" r="0.3" fill="#a98762"/><circle cx="3" cy="0.6" r="0.2" fill="#b89670"/></pattern>
<linearGradient id="archG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9f3fb"/><stop offset="1" stop-color="#c5ddf0"/></linearGradient>
<radialGradient id="bulbG" cx="0.5" cy="0.45" r="0.6"><stop offset="0" stop-color="#5aa6dc"/><stop offset="1" stop-color="#2f86c9" stop-opacity="0.75"/></radialGradient>
<linearGradient id="tankG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8f2f9"/><stop offset="1" stop-color="#a9cbe5"/></linearGradient>
<linearGradient id="vesG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c7ccd1"/><stop offset="0.5" stop-color="#f1f3f5"/><stop offset="1" stop-color="#aab1b8"/></linearGradient>
<marker id="aw" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4.2" markerHeight="4.2" orient="auto"><path d="M0,0.5 L10,5 L0,9.5 z" fill="#2f86c9"/></marker>
<marker id="ah" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4.2" markerHeight="4.2" orient="auto"><path d="M0,0.5 L10,5 L0,9.5 z" fill="#e0532f"/></marker>
</defs>''')
# ---------------- ground
OB = G + 11
gx0, gx1 = 6, W - 6
brk = 172
def ground_seg(x0, x1):
    a(f'<rect x="{x0}" y="{G}" width="{x1-x0}" height="{OB-G}" fill="url(#regH)"/>')
    a(f'<rect x="{x0}" y="{OB}" width="{x1-x0}" height="{H-14-OB}" fill="url(#iceH)"/>')
    L(x0, G, x1, G, INK, 0.7)
    L(x0, OB, x1, OB, '#9fbad1', 0.4, 'stroke-dasharray="2,1.2"')
ground_seg(gx0, brk - 4)
ground_seg(brk + 4, gx1)
for x in (brk - 4, brk + 4):
    zz = [(x, G - 2)]
    y = G - 2
    k = 0
    while y < H - 14:
        y = min(y + 4, H - 14); k += 1
        zz.append((x + (1.6 if k % 2 else -1.6) * (1 if x < brk else -1), y))
    P(zz, c='#8a8a8a', w=0.35, close=False)
# fade the bottom edge
T(146, G + 10.2, 'REGOLITH OVERBURDEN', 2.2, 'middle', 700, '#7a5c38', ls=0.4)
T(gx0 + 3, H - 18, 'GROUND ICE · UTOPIA PLANITIA', 2.4, 'start', 700, '#3d6b91', ls=0.4)
# distance bracket
L(110, G - 46, 238, G - 46, '#666', 0.3)
for x in (110, 238): L(x, G - 48, x, G - 44, '#666', 0.3)
a(f'<rect x="{brk-10}" y="{G-49}" width="20" height="5.5" fill="#ffffff"/>')
T(brk, G - 45, '≈ 130 m', 3.0, w=700, fill='#555')
# ---------------- reactor (buried vessel + berm + radiator)
rx = 30
P([(rx - 18, G), (rx - 8, G - 7), (rx + 10, G - 7), (rx + 20, G)], fill='url(#regH)', c='#a98762', w=0.4)
a(f'<rect x="{rx-6}" y="{G-4}" width="14" height="{OB-G+12}" rx="7" fill="url(#vesG)" stroke="{INK}" stroke-width="0.5"/>')
a(f'<circle cx="{rx+1}" cy="{G+9}" r="3.2" fill="#f2c84b" stroke="{INK}" stroke-width="0.4"/>')
for ang in (90, 210, 330):
    t = math.radians(ang)
    P([(rx + 1, G + 9), (rx + 1 + 3.2 * math.cos(t - 0.5), G + 9 - 3.2 * math.sin(t - 0.5)), (rx + 1 + 3.2 * math.cos(t + 0.5), G + 9 - 3.2 * math.sin(t + 0.5))], fill=INK, c='none', w=0)
# radiator mast + panels
L(rx + 1, G - 7, rx + 1, G - 30, STEEL, 1.0)
for s in (-1, 1):
    pts = [(rx + 1, G - 28), (rx + 1 + s * 17, G - 22), (rx + 1 + s * 17, G - 13), (rx + 1, G - 19)]
    P(pts, fill='#eef1f4', c=INK, w=0.45)
    for i in range(1, 6):
        f = i / 6
        L(rx + 1 + s * 17 * f, G - 28 + 6 * f, rx + 1 + s * 17 * f, G - 19 + 6 * f, '#9aa4ad', 0.25)
# ---------------- rodwell rig + HX
wx = 92
hx0 = 66
a(f'<rect x="{hx0}" y="{G-10}" width="14" height="10" rx="1" fill="#ffffff" stroke="{INK}" stroke-width="0.5"/>')
for i in range(5): L(hx0 + 2.5 + i * 2.2, G - 8.5, hx0 + 2.5 + i * 2.2, G - 1.5, '#9aa4ad', 0.35)
T(hx0 + 7, G - 12, 'HX', 2.4, w=800, fill='#555')
# tripod derrick
for dx in (-7, 7): L(wx + dx, G, wx, G - 24, STEEL, 0.9)
L(wx, G, wx, G - 24, STEEL, 0.6)
a(f'<rect x="{wx-2}" y="{G-26}" width="4" height="2.5" fill="{INK}"/>')
a(f'<rect x="{wx-3}" y="{G-6}" width="6" height="6" fill="#9aa1a8" stroke="{INK}" stroke-width="0.4"/>')
# heat line reactor -> HX (insulated, red)
a(f'<path d="M{rx+8},{G-3} C{rx+20},{G-3} {hx0-12},{G-5} {hx0-1},{G-5}" fill="none" stroke="{HOT}" stroke-width="1.2" marker-end="url(#ah)"/>')
# HX -> wellhead hot line
L(hx0 + 14, G - 4, wx - 3, G - 4, HOT, 1.0)
# casing + pipes down
cas_bot = OB + 9
a(f'<rect x="{wx-2}" y="{G}" width="4" height="{cas_bot-G}" fill="#9aa1a8" stroke="{INK}" stroke-width="0.4"/>')
by_ = OB + 30
a(f'<ellipse cx="{wx}" cy="{by_+3}" rx="27" ry="19" fill="none" stroke="{WATER}" stroke-width="0.45" stroke-dasharray="2,1.3" opacity="0.8"/>')
a(f'<path d="M{wx-20},{by_-6} Q{wx-22},{by_+14} {wx},{by_+17} Q{wx+22},{by_+14} {wx+20},{by_-6} Q{wx},{by_-15} {wx-20},{by_-6} Z" fill="url(#bulbG)" stroke="{WD}" stroke-width="0.5"/>')
a(f'<path d="M{wx-19},{by_-4} Q{wx},{by_-8} {wx+19},{by_-4}" fill="none" stroke="#ffffff" stroke-opacity="0.7" stroke-width="0.5"/>')
L(wx - 0.9, G - 4, wx - 0.9, by_ - 2, HOT, 0.9)
L(wx + 0.9, by_ + 10, wx + 0.9, G - 6, '#123c5e', 0.9)
a(f'<rect x="{wx-0.6}" y="{by_+9}" width="3" height="4" rx="0.8" fill="#123c5e"/>')
for k in range(3):
    for s in (-1, 1):
        a(f'<path d="M{wx-0.9},{by_-1+k*1.6} q{s*3},{1} {s*(5+2*k)},{2.5+k}" fill="none" stroke="{HOT}" stroke-width="0.45"/>')
T(wx + 31, by_ + 19, 'melt bulb grows over months', 2.4, 'start', 600, WD, it=True)
# ---------------- buried insulated pipeline
py = G + 5.5
x_tank = 248
def pipe(x0, x1):
    a(f'<rect x="{x0}" y="{py-1.9}" width="{x1-x0}" height="3.8" rx="1.9" fill="#d9dde1" stroke="#8a949c" stroke-width="0.35"/>')
    a(f'<rect x="{x0+0.6}" y="{py-0.9}" width="{x1-x0-1.2}" height="1.8" rx="0.9" fill="{WATER}"/>')
L(wx + 3, G - 3, wx + 6, G - 3, WATER, 1.6)
a(f'<rect x="{wx+5.2}" y="{G-3.9}" width="1.8" height="{py-G+3.9}" fill="{WATER}"/>')
pipe(wx + 5, brk - 4)
pipe(brk + 4, x_tank - 8)
for x in (125, 150, 200, 225):
    a(f'<path d="M{x-2},{py} l4,0" stroke="#ffffff" stroke-width="0.6" marker-end="url(#aw)"/>')
# trace heating zigzag on pipe
for x0, x1 in ((wx + 8, brk - 5), (brk + 5, x_tank - 9)):
    pts = []; x = x0; k = 0
    while x < x1:
        pts.append((x, py - 1.9 if k % 2 else py + 1.9)); x += 2.2; k += 1
    P(pts, c=HOT, w=0.22, close=False, extra='opacity="0.8"')
# ---------------- buffer tank
a(f'<rect x="{x_tank-9}" y="{G+1.5}" width="20" height="9" rx="4.5" fill="url(#tankG)" stroke="{INK}" stroke-width="0.5"/>')
a(f'<rect x="{x_tank-8}" y="{G+6}" width="18" height="4" rx="2" fill="{WATER}" opacity="0.55"/>')
# ---------------- tower
tx = 262
top = 22
mw = 4.0
a(f'<rect x="{tx-7}" y="{G-2}" width="14" height="2" fill="{INK}"/>')
for s in (-1, 1):
    L(tx + s * 2, G - 2, tx + s * 13, G, INK, 0.9)
    a(f'<rect x="{tx+s*13-2}" y="{G-0.6}" width="4" height="0.9" fill="{INK}"/>')
L(tx - mw / 2, G - 2, tx - mw / 2, top, INK, 0.55)
L(tx + mw / 2, G - 2, tx + mw / 2, top, INK, 0.55)
y = G - 2; k = 0
while y - 4 > top:
    L(tx - mw / 2 if k % 2 == 0 else tx + mw / 2, y, tx + mw / 2 if k % 2 == 0 else tx - mw / 2, y - 4, '#6b747c', 0.25)
    L(tx - mw / 2, y - 4, tx + mw / 2, y - 4, '#6b747c', 0.2)
    y -= 4; k += 1
a(f'<rect x="{tx-2.6}" y="{top-3}" width="5.2" height="3" fill="{INK}"/>')
# riser
L(x_tank + 9, G + 4, tx, G + 4, WATER, 1.2)
L(tx, G + 4, tx, top + 2, WATER, 1.1, 'stroke-dasharray="0"')
for y in (110, 80, 50):
    a(f'<path d="M{tx},{y+2} l0,-4" stroke="{WATER}" stroke-width="1.1" marker-end="url(#aw)"/>')
# boom truss
by0 = 78
bend = 432
def by(x): return by0 - (x - tx) * 0.035
bh = 2.4
L(tx, by(tx), bend, by(bend), INK, 0.6)
L(tx, by(tx) + bh, bend - 3, by(bend - 3) + bh, INK, 0.6)
x = tx; k = 0
while x + 4 < bend - 3:
    L(x, by(x) + (0 if k % 2 == 0 else bh), x + 4, by(x + 4) + (bh if k % 2 == 0 else 0), '#6b747c', 0.22)
    x += 4; k += 1
# counter jib + CW bag
L(tx, by0, tx - 30, by0, INK, 0.6); L(tx, by0 + bh, tx - 30, by0 + bh, INK, 0.6)
x = tx - 30; k = 0
while x + 4 <= tx:
    L(x, by0 + (0 if k % 2 == 0 else bh), x + 4, by0 + (bh if k % 2 == 0 else 0), '#6b747c', 0.22); x += 4; k += 1
a(f'<path d="M{tx-31},{by0+bh} l-1.5,9 q4.5,3 9,0 l-1.5,-9 z" fill="#9cc0de" stroke="{INK}" stroke-width="0.45"/>')
T(tx - 28.3, by0 + bh + 15.5, 'water ballast', 2.1, w=600, fill='#555')
# stays
L(tx, top, tx - 30, by0, '#555', 0.25)
for xs in range(tx + 25, bend + 1, 25):
    L(tx, top, xs, by(xs), '#555', 0.22)
# water line along boom
L(tx + 2, by(tx + 2) + 1.2, bend - 8, by(bend - 8) + 1.2, WATER, 0.9, 'marker-end="url(#aw)"')
# ---------------- arches
def catenary(cx, span, h):
    aa = 4.5643 * span / 16
    def z(x): return h * (1 - (math.cosh(x / aa) - 1) / (math.cosh(span / 2 / aa) - 1))
    return z
def arch(cx, span=30, h=17, t=2.0, mode='done'):
    zo = catenary(cx, span, h)
    zi = catenary(cx, span - 2 * t * 1.15, h - t)
    out = [(cx + x, G - zo(x)) for x in [-span / 2 + span * i / 60 for i in range(61)]]
    sp_i = span - 2 * t * 1.15
    inn = [(cx + x, G - zi(x)) for x in [-sp_i / 2 + sp_i * i / 60 for i in range(61)]]
    if mode == 'done':
        P(out + inn[::-1], fill='url(#archG)', c='#3f74a1', w=0.55)
        # habitat membrane inside
        zm = catenary(cx, sp_i - 2, h - t - 1.2)
        sp_m = sp_i - 2
        mem = [(cx + x, G - zm(x)) for x in [-sp_m / 2 + sp_m * i / 40 for i in range(41)]]
        P(mem, c='#b0533a', w=0.35, close=False, extra='stroke-dasharray="1.4,0.8"')
    else:
        # liner partially filled: water to level, rest empty
        lvl = G - 6.5
        P(out + inn[::-1], fill='#ffffff', c='#3f74a1', w=0.5)
        a(f'<clipPath id="lv"><rect x="{cx-span}" y="{lvl}" width="{2*span}" height="{G-lvl}"/></clipPath>')
        a('<g clip-path="url(#lv)">')
        P(out + inn[::-1], fill=WATER, c='none', w=0)
        a('</g>')
        L(cx - span / 2 + 1, lvl, cx - span / 2 + 3.5, lvl, '#ffffff', 0.4)
        # outer clamp staves
        oc = [(x - (0 if x == cx else 0), y - 1.4) for x, y in out]
        P([(x, y) for x, y in out][::1], c='#b5532e', w=1.1, close=False, extra='transform="translate(0,-1.3)"')
        # centering truss inside
        zc = catenary(cx, sp_i - 0.5, h - t - 0.3)
        spc = sp_i - 0.5
        cen = [(cx + x, G - zc(x)) for x in [-spc / 2 + spc * i / 40 for i in range(41)]]
        P(cen, c=STEEL, w=0.6, close=False)
        for i in range(0, 41, 4):
            x, y = cen[i]
            L(x, y, cx + (x - cx) * 0.55, G - 2, STEEL, 0.22)
        a(f'<rect x="{cx-12}" y="{G-2}" width="24" height="1.6" fill="{INK}"/>')
        for x in (cx - 10, cx + 10): a(f'<circle cx="{x}" cy="{G-0.3}" r="1.2" fill="{INK}"/>')
    return out
arch(300, mode='done')
arch(344, mode='done')
fx = 392
out = arch(fx, mode='cast')
T(300, G + 6, 'RING 1', 2.4, w=800, fill='#163f66', ls=0.4)
T(344, G + 6, 'RING 2', 2.4, w=800, fill='#163f66', ls=0.4)
T(fx, G + 6, 'RING 3 · CASTING', 2.4, w=800, fill=WD, ls=0.4)
# boom robot + hose to crown port
rx_ = fx + 3
a(f'<rect x="{rx_-4.5}" y="{by(rx_)+bh+0.3}" width="9" height="3.6" rx="0.8" fill="{INK}"/>')
for x in (rx_ - 3, rx_ + 3): a(f'<circle cx="{x}" cy="{by(rx_)+bh+0.3}" r="0.9" fill="#555"/>')
crown_y = G - 17 - 1.3
a(f'<path d="M{rx_},{by(rx_)+bh+4} C{rx_+6},{by(rx_)+18} {fx+4},{crown_y-14} {fx},{crown_y-1.2}" fill="none" stroke="{WATER}" stroke-width="1.1" marker-end="url(#aw)"/>')
# ---------------- callouts
def num(n, x, y, tx_=None, ty_=None):
    if tx_ is not None: L(x, y, tx_, ty_, '#444', 0.3)
    a(f'<circle cx="{x}" cy="{y}" r="3.4" fill="{INK}"/>')
    T(x, y + 1.2, str(n), 3.3, w=800, fill='#ffffff')
num(1, rx + 1, G - 38, rx + 1, G - 31)
num(2, wx - 30, by_ - 4, wx - 21, by_ - 2)
num(3, wx + 14, G - 30, wx + 3, G - 22)
num(4, 113, G + 17, 113, py + 2)
num(5, x_tank, G + 21, x_tank, G + 11)
num(6, tx + 14, top + 2, tx + 3, top + 4)
num(7, fx + 26, G - 34, fx + 6, G - 20)
# ---------------- title + steps
lx, ly = 10, 13
T(lx, ly, 'ISRU WATER CHAIN', 5.2, 'start', 800, INK, ls=0.6)
T(lx, ly + 5.8, 'from ground ice to a cast ice arch · schematic, not to scale', 2.8, 'start', 500, '#666')
steps = [('Fission reactor', 'waste heat drives the well'),
         ('Rodwell', 'hot water melts ground ice; a pump lifts the meltwater'),
         ('Wellhead heat exchanger', 'reheats injection water; meltwater is filtered'),
         ('Buried, trace-heated pipeline', 'well field to the tower base, ≈ 130 m'),
         ('Buffer tank + pump', 'at the foot of the pumping tower'),
         ('Riser + ≈ 90 m boom', 'a robot on the boom plugs the hose in'),
         ('Travelling formwork', 'liner filled in stages; the arch freezes in ≈ 6 sols')]
for i, (t1, t2) in enumerate(steps):
    y = ly + 15 + i * 8.4
    a(f'<circle cx="{lx+2.8}" cy="{y-1.1}" r="2.8" fill="{INK}"/>')
    T(lx + 2.8, y, str(i + 1), 2.9, w=800, fill='#ffffff')
    T(lx + 8, y - 0.7, t1, 3.0, 'start', 700)
    T(lx + 8, y + 2.9, t2, 2.55, 'start', 400, '#4a4a4a')
# key
ky = H - 6
a(f'<rect x="300" y="{ky-2.6}" width="12" height="3" rx="1.5" fill="#d9dde1" stroke="#8a949c" stroke-width="0.3"/><rect x="300.6" y="{ky-1.9}" width="10.8" height="1.6" rx="0.8" fill="{WATER}"/>')
T(315, ky, 'water', 2.6, 'start', 600)
L(338, ky - 1.1, 350, ky - 1.1, HOT, 1.1)
T(353, ky, 'heat / hot injection water', 2.6, 'start', 600)
L(400, ky - 1.1, 412, ky - 1.1, '#b0533a', 0.4, 'stroke-dasharray="1.4,0.8"')
T(415, ky, 'habitat membrane', 2.6, 'start', 600)
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">'
       '<style>text{font-family:Inter,Helvetica,Arial,sans-serif}</style>' + ''.join(o) + '</svg>')
import os
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures", "ISRU_water_chain.svg")
open(out, "w").write(svg)
