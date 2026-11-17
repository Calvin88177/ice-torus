"""Cross-sections A-A and B-B (1:50) and construction details for the ice-arch tunnel."""
import math
import numpy as np
from core import (num, text, fmt, offset_curve, z_outer, T_ICE, T_GAP, T_MEM, A_CAT, height_at, half_width,
                  path_poly, upright)

ICE_EDGE = '#3f74a1'
MEM = '#163f66'
INK = '#2a2a2a'


class SV:
    def __init__(self, ox, oy, denom):
        self.ox, self.oy, self.s = ox, oy, 1000.0 / denom

    def p(self, x, z):
        return (self.ox + x * self.s, self.oy - z * self.s)

    def L(self, m):
        return m * self.s


# ------------------------------------------------------------------ primitives
def poly(svg, sv, pts_xz, fill='none', stroke=INK, sw=0.2, extra='', close=True):
    P = [sv.p(x, z) for x, z in pts_xz]
    svg.add(f'<path d="{path_poly(P, close)}" fill="{fill}" stroke="{stroke}" stroke-width="{num(sw)}" {extra}/>')


def rect(svg, sv, x1, z1, x2, z2, fill='#fff', stroke=INK, sw=0.2, extra=''):
    poly(svg, sv, [(x1, z1), (x2, z1), (x2, z2), (x1, z2)], fill, stroke, sw, extra)


def line(svg, sv, x1, z1, x2, z2, stroke=INK, sw=0.2, extra=''):
    a, b = sv.p(x1, z1), sv.p(x2, z2)
    svg.add(f'<line x1="{num(a[0])}" y1="{num(a[1])}" x2="{num(b[0])}" y2="{num(b[1])}" stroke="{stroke}" stroke-width="{num(sw)}" {extra}/>')


def circle(svg, sv, x, z, r, fill='#fff', stroke=INK, sw=0.15):
    c = sv.p(x, z)
    svg.add(f'<circle cx="{num(c[0])}" cy="{num(c[1])}" r="{num(sv.L(r))}" fill="{fill}" stroke="{stroke}" stroke-width="{num(sw)}"/>')


def curve(d, zmin=-0.3, side=None, n=1601):
    x, z = offset_curve(d, xmax=8.7, n=n)
    m = z >= zmin
    x, z = x[m], z[m]
    if side == 'L':
        k = x <= 0
        return x[k], z[k]
    if side == 'R':
        k = x >= 0
        return x[k], z[k]
    return x, z


def curve_clip(d, zmin):
    """curve with endpoints exactly at z = zmin (interpolated)"""
    x, z = offset_curve(d, xmax=8.7, n=3001)
    out = []
    for i in range(len(x)):
        if z[i] >= zmin:
            if i > 0 and z[i - 1] < zmin:
                t = (zmin - z[i - 1]) / (z[i] - z[i - 1])
                out.append((x[i - 1] + t * (x[i] - x[i - 1]), zmin))
            out.append((x[i], z[i]))
            if i + 1 < len(x) and z[i + 1] < zmin:
                t = (zmin - z[i]) / (z[i + 1] - z[i])
                out.append((x[i] + t * (x[i + 1] - x[i]), zmin))
    return out


def defs_section(svg, k=1.0):
    svg.d(f'<pattern id="sIce" patternUnits="userSpaceOnUse" width="{num(2.2*k)}" height="{num(2.2*k)}" patternTransform="rotate(35)">'
          f'<rect width="{num(2.2*k)}" height="{num(2.2*k)}" fill="#d3e6f4"/>'
          f'<line x1="0" y1="0" x2="0" y2="{num(2.2*k)}" stroke="#9cc2de" stroke-width="{num(0.22*k)}"/></pattern>')
    svg.d(f'<pattern id="sGap" patternUnits="userSpaceOnUse" width="{num(0.9*k)}" height="{num(0.9*k)}">'
          f'<rect width="{num(0.9*k)}" height="{num(0.9*k)}" fill="#f7fbfe"/>'
          f'<circle cx="{num(0.45*k)}" cy="{num(0.45*k)}" r="{num(0.09*k)}" fill="#6d93b2"/></pattern>')
    svg.d(f'<pattern id="sReg" patternUnits="userSpaceOnUse" width="{num(3.0*k)}" height="{num(3.0*k)}">'
          f'<rect width="{num(3.0*k)}" height="{num(3.0*k)}" fill="#e9dcc9"/>'
          f'<circle cx="{num(0.6*k)}" cy="{num(0.8*k)}" r="{num(0.18*k)}" fill="#c8b293"/>'
          f'<circle cx="{num(2.1*k)}" cy="{num(1.9*k)}" r="{num(0.26*k)}" fill="#c3ab8a"/>'
          f'<circle cx="{num(1.5*k)}" cy="{num(0.4*k)}" r="{num(0.1*k)}" fill="#b49a77"/>'
          f'<circle cx="{num(0.5*k)}" cy="{num(2.5*k)}" r="{num(0.12*k)}" fill="#b49a77"/></pattern>')
    svg.d(f'<pattern id="sPerma" patternUnits="userSpaceOnUse" width="{num(3.0*k)}" height="{num(3.0*k)}">'
          f'<rect width="{num(3.0*k)}" height="{num(3.0*k)}" fill="#dfe3e0"/>'
          f'<circle cx="{num(0.7*k)}" cy="{num(0.9*k)}" r="{num(0.2*k)}" fill="#b9c3c4"/>'
          f'<line x1="{num(1.2*k)}" y1="{num(2.1*k)}" x2="{num(2.6*k)}" y2="{num(1.6*k)}" stroke="#a7b8c4" stroke-width="{num(0.15*k)}"/>'
          f'<circle cx="{num(2.3*k)}" cy="{num(0.5*k)}" r="{num(0.12*k)}" fill="#a7b8c4"/></pattern>')
    svg.d(f'<pattern id="sIns" patternUnits="userSpaceOnUse" width="{num(1.4*k)}" height="{num(1.0*k)}">'
          f'<rect width="{num(1.4*k)}" height="{num(1.0*k)}" fill="#fff6d6"/>'
          f'<path d="M0,{num(0.5*k)} Q{num(0.35*k)},0 {num(0.7*k)},{num(0.5*k)} T{num(1.4*k)},{num(0.5*k)}" fill="none" stroke="#c9a94a" stroke-width="{num(0.12*k)}"/></pattern>')
    svg.d(f'<pattern id="sConc" patternUnits="userSpaceOnUse" width="{num(1.2*k)}" height="{num(1.2*k)}" patternTransform="rotate(45)">'
          f'<rect width="{num(1.2*k)}" height="{num(1.2*k)}" fill="#e4e4e4"/>'
          f'<line x1="0" y1="0" x2="0" y2="{num(1.2*k)}" stroke="#9a9a9a" stroke-width="{num(0.12*k)}"/></pattern>')
    svg.d(f'<pattern id="sWater" patternUnits="userSpaceOnUse" width="{num(1.0*k)}" height="{num(1.0*k)}" patternTransform="rotate(45)">'
          f'<rect width="{num(1.0*k)}" height="{num(1.0*k)}" fill="#d7ebf8"/>'
          f'<line x1="0" y1="0" x2="0" y2="{num(1.0*k)}" stroke="#5d97c4" stroke-width="{num(0.1*k)}"/></pattern>')
    svg.d('<linearGradient id="gLight" x1="0" y1="0" x2="0" y2="1">'
          '<stop offset="0" stop-color="#fff2b3" stop-opacity="0.85"/><stop offset="1" stop-color="#fff2b3" stop-opacity="0"/></linearGradient>')
    svg.d('<linearGradient id="gSky" x1="0" y1="0" x2="0" y2="1">'
          '<stop offset="0" stop-color="#fffbe8"/><stop offset="1" stop-color="#ffffff"/></linearGradient>')
    svg.d('<marker id="lead" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="2.4" markerHeight="2.4">'
          '<circle cx="5" cy="5" r="4" fill="#222"/></marker>')


# ------------------------------------------------------------------ shell, ground, floor
Z_INS = -0.30
Z_MFLOOR = -0.20


def ground(svg, sv, xw=9.6, zb=-1.45, zp=-0.95):
    # subgrade & permafrost
    rect(svg, sv, -xw, zb, xw, zp, fill='url(#sPerma)', stroke='none')
    rect(svg, sv, -xw, zp, xw, 0.0, fill='url(#sReg)', stroke='none')
    pts_ = [(x, zp + 0.06 * math.sin(x * 1.7)) for x in np.linspace(-xw, xw, 60)]
    poly(svg, sv, pts_, fill='none', stroke='#8f9da3', sw=0.18, close=False, extra='stroke-dasharray="1.2,0.8"')
    line(svg, sv, -xw, 0.0, -8.0, 0.0, stroke='#7a6447', sw=0.35)
    line(svg, sv, 8.0, 0.0, xw, 0.0, stroke='#7a6447', sw=0.35)
    # torn edges (break lines) at the ends
    for sgn in (1, -1):
        x = sgn * xw
        pts_ = [(x, 0.15), (x, -0.3), (x + 0.12 * sgn, -0.5), (x - 0.12 * sgn, -0.7), (x, -0.9), (x, zb)]
        poly(svg, sv, pts_, fill='none', stroke='#777', sw=0.18, close=False)


def shell(svg, sv, light=True):
    out = curve_clip(0.0, Z_INS)
    inn = curve_clip(T_ICE, Z_INS)
    ice = out + inn[::-1]
    poly(svg, sv, ice, fill='url(#sIce)', stroke=ICE_EDGE, sw=0.35)
    gap_o = curve_clip(T_ICE, Z_MFLOOR)
    gap_i = curve_clip(T_ICE + T_GAP, Z_MFLOOR)
    poly(svg, sv, gap_o + gap_i[::-1], fill='url(#sGap)', stroke='none')
    # membrane double
    m1 = curve_clip(T_ICE + T_GAP, Z_MFLOOR)
    m2 = curve_clip(T_ICE + T_GAP + T_MEM, Z_MFLOOR + 0.03)
    poly(svg, sv, m1, fill='none', stroke=MEM, sw=0.45, close=False)
    poly(svg, sv, m2, fill='none', stroke=MEM, sw=0.25, close=False)
    # floor build-up
    xl = m1[0][0]
    xr = m1[-1][0]
    rect(svg, sv, -8.1, Z_INS - 0.0, 8.1, Z_INS, fill='none', stroke='none')
    xin = half_width(T_ICE, Z_INS)
    rect(svg, sv, -xin, Z_INS, xin, Z_MFLOOR, fill='url(#sIns)', stroke='#a58a2f', sw=0.15)
    line(svg, sv, xl, Z_MFLOOR, xr, Z_MFLOOR, stroke=MEM, sw=0.45)
    line(svg, sv, xl + 0.03, Z_MFLOOR + 0.03, xr - 0.03, Z_MFLOOR + 0.03, stroke=MEM, sw=0.25)
    # raised floor: panel + pedestals
    xf = half_width(T_ICE + T_GAP, 0.0)
    rect(svg, sv, -xf + 0.05, -0.04, xf - 0.05, 0.0, fill='#cfcfcf', stroke=INK, sw=0.2)
    for x in np.arange(-6.6, 6.61, 0.6):
        rect(svg, sv, x - 0.025, Z_MFLOOR + 0.03, x + 0.025, -0.04, fill='#888', stroke='none')
    # under-floor main utility trunk under corridor
    for x, r, col in ((-0.45, 0.075, '#e6f1fa'), (-0.2, 0.05, '#e6f1fa'), (0.15, 0.065, '#fde9d9'), (0.45, 0.05, '#eaeaea')):
        circle(svg, sv, x, -0.11, r, fill=col, stroke='#555', sw=0.12)
    # chase at both corners
    for sgn in (1, -1):
        chase(svg, sv, sgn)
    if light:
        crown_light(svg, sv)


def mem_pts(sgn, z0, z1, d=None, n=40):
    d = T_ICE + T_GAP + T_MEM if d is None else d
    zs = np.linspace(z0, z1, n)
    return [(sgn * half_width(d, z), z) for z in zs]


def chase(svg, sv, sgn, ztop=0.90, xa=6.60):
    pts_ = [(sgn * xa, 0.0)] + mem_pts(sgn, 0.0, ztop) + [(sgn * xa, ztop)]
    poly(svg, sv, pts_, fill='#efefef', stroke='#555', sw=0.25)
    for (dx, dz, r, col) in ((0.17, 0.62, 0.12, '#e6f1fa'), (0.17, 0.27, 0.085, '#fde9d9'), (0.41, 0.22, 0.055, '#e6f1fa')):
        circle(svg, sv, sgn * (xa + dx), dz, r, fill=col, stroke='#555', sw=0.12)


def crown_light(svg, sv):
    zc = 8.30 - 0.06
    rect(svg, sv, -0.65, zc - 0.12, 0.65, zc - 0.04, fill='#fff7c9', stroke='#b29a3a', sw=0.2)
    for x in (-0.65, 0.65):
        line(svg, sv, x * 0.7, zc - 0.04, x * 0.7, zc + 0.02, stroke='#777', sw=0.12)


def light_cone(svg, sv, x1, x2, z_top, z_bot, spread=0.0):
    poly(svg, sv, [(x1, z_top), (x2, z_top), (x2 + spread, z_bot), (x1 - spread, z_bot)], fill='url(#gLight)', stroke='none')


# ------------------------------------------------------------------ people
def person(svg, sv, x, z, kind='stand', face=1, h=1.75, col='#3d4a57'):
    s = h / 1.75
    def P(dx, dz):
        return sv.p(x + face * dx * s, z + dz * s)
    if kind in ('stand', 'walk'):
        head = P(0, 1.62)
        svg.add(f'<circle cx="{num(head[0])}" cy="{num(head[1])}" r="{num(sv.L(0.105*s))}" fill="{col}"/>')
        torso = [(-0.17, 1.47), (0.15, 1.47), (0.18, 0.92), (-0.16, 0.92)]
        if kind == 'walk':
            legs = [(-0.13, 0.92), (0.12, 0.92), (0.33, 0.0), (0.2, 0.0), (0.0, 0.55), (-0.2, 0.0), (-0.34, 0.0)]
            arms = [(-0.16, 1.43), (-0.33, 0.98), (-0.25, 0.95), (-0.08, 1.35)]
            arms2 = [(0.13, 1.43), (0.30, 1.0), (0.22, 0.97), (0.06, 1.35)]
        else:
            legs = [(-0.15, 0.92), (0.15, 0.92), (0.13, 0.0), (0.02, 0.0), (0.0, 0.6), (-0.02, 0.0), (-0.13, 0.0)]
            arms = [(-0.17, 1.45), (-0.24, 0.85), (-0.17, 0.85), (-0.11, 1.35)]
            arms2 = [(0.15, 1.45), (0.23, 0.85), (0.16, 0.85), (0.10, 1.35)]
        for shape in (torso, legs, arms, arms2):
            svg.add(f'<path d="{path_poly([P(a, b) for a, b in shape])}" fill="{col}"/>')
    elif kind == 'sit':
        head = P(0.02, 1.22)
        svg.add(f'<circle cx="{num(head[0])}" cy="{num(head[1])}" r="{num(sv.L(0.105*s))}" fill="{col}"/>')
        torso = [(-0.13, 1.08), (0.15, 1.08), (0.12, 0.5), (-0.14, 0.5)]
        legs = [(-0.14, 0.5), (0.36, 0.5), (0.4, 0.0), (0.3, 0.0), (0.28, 0.4), (-0.12, 0.4)]
        arm = [(0.1, 1.04), (0.38, 0.78), (0.36, 0.72), (0.06, 0.92)]
        for shape in (torso, legs, arm):
            svg.add(f'<path d="{path_poly([P(a, b) for a, b in shape])}" fill="{col}"/>')
    elif kind == 'kneel':
        head = P(0.05, 1.12)
        svg.add(f'<circle cx="{num(head[0])}" cy="{num(head[1])}" r="{num(sv.L(0.105*s))}" fill="{col}"/>')
        torso = [(-0.12, 0.98), (0.16, 0.98), (0.1, 0.45), (-0.16, 0.45)]
        legs = [(-0.16, 0.45), (0.3, 0.45), (0.32, 0.0), (-0.2, 0.0)]
        arm = [(0.1, 0.94), (0.42, 0.8), (0.42, 0.74), (0.06, 0.84)]
        for shape in (torso, legs, arm):
            svg.add(f'<path d="{path_poly([P(a, b) for a, b in shape])}" fill="{col}"/>')


def chair_side(svg, sv, x, z, face=1, col='#666'):
    rect(svg, sv, x - 0.22, z + 0.42, x + 0.22, z + 0.48, fill=col, stroke='none')
    line(svg, sv, x - 0.2 * face, z + 0.45, x - 0.2 * face, z + 0.95, stroke=col, sw=0.35)
    line(svg, sv, x - 0.15, z, x - 0.15, z + 0.42, stroke=col, sw=0.2)
    line(svg, sv, x + 0.15, z, x + 0.15, z + 0.42, stroke=col, sw=0.2)


def tree_elev(svg, sv, x, z, h=4.0, w=2.2, col='#9cc983', faded=False):
    op = 0.55 if faded else 1.0
    line(svg, sv, x, z, x, z + h * 0.55, stroke='#7a5a3c', sw=0.6, extra=f'opacity="{op}"')
    n = 18
    P = []
    for k in range(n * 2):
        a = math.pi * k / n
        rr = (1.0 if k % 2 == 0 else 0.9)
        P.append((x + 0.5 * w * rr * math.cos(a), z + h * 0.62 + 0.42 * h * rr * math.sin(a) * 0.9))
    poly(svg, sv, P, fill=col, stroke='#4f8a3c', sw=0.2, extra=f'opacity="{op}"')
    rect(svg, sv, x - 0.55, z, x + 0.55, z + 0.55, fill='#e5d9c6', stroke='#8a7660', sw=0.2, extra=f'opacity="{op}"')


# ------------------------------------------------------------------ annotations
def dim_h(svg, sv, x1, x2, z, label, off=0.0, size=2.3, color='#7a2a12', ext_to=None):
    a, b = sv.p(x1, z), sv.p(x2, z)
    y = a[1] + off
    svg.add(f'<line x1="{num(a[0])}" y1="{num(y)}" x2="{num(b[0])}" y2="{num(y)}" stroke="{color}" stroke-width="0.18"/>')
    for xx in (a[0], b[0]):
        svg.add(f'<line x1="{num(xx-1.2)}" y1="{num(y+1.2)}" x2="{num(xx+1.2)}" y2="{num(y-1.2)}" stroke="{color}" stroke-width="0.32"/>')
        if ext_to is not None:
            ye = sv.p(0, ext_to)[1]
            svg.add(f'<line x1="{num(xx)}" y1="{num(min(y, ye) - 0.0)}" x2="{num(xx)}" y2="{num(max(y, ye))}" stroke="{color}" stroke-width="0.1"/>')
    svg.add(text((a[0] + b[0]) / 2, y - 1.0, label, size=size, fill=color, weight=600))


def dim_v(svg, sv, x, z1, z2, label, off=0.0, size=2.3, color='#7a2a12', side=-1, ext_to=None):
    a, b = sv.p(x, z1), sv.p(x, z2)
    xx = a[0] + off
    svg.add(f'<line x1="{num(xx)}" y1="{num(a[1])}" x2="{num(xx)}" y2="{num(b[1])}" stroke="{color}" stroke-width="0.18"/>')
    for yy in (a[1], b[1]):
        svg.add(f'<line x1="{num(xx-1.2)}" y1="{num(yy+1.2)}" x2="{num(xx+1.2)}" y2="{num(yy-1.2)}" stroke="{color}" stroke-width="0.32"/>')
        if ext_to is not None:
            xe = sv.p(ext_to, 0)[0]
            svg.add(f'<line x1="{num(min(xx, xe))}" y1="{num(yy)}" x2="{num(max(xx, xe))}" y2="{num(yy)}" stroke="{color}" stroke-width="0.1"/>')
    my = (a[1] + b[1]) / 2
    tx = xx + side * 1.1
    svg.add(text(tx, my, label, size=size, fill=color, weight=600, rot=-90, extra=''))


def level(svg, sv, x, z, label, side=1, color='#151515', size=2.3, line_len=6):
    p = sv.p(x, z)
    t = 1.6
    svg.add(f'<path d="M{num(p[0])},{num(p[1])} l{num(-t)},{num(-t*1.3)} h{num(2*t)} Z" fill="{color}"/>')
    svg.add(f'<line x1="{num(p[0] - line_len*0)}" y1="{num(p[1])}" x2="{num(p[0] + side*line_len)}" y2="{num(p[1])}" stroke="{color}" stroke-width="0.2"/>')
    svg.add(text(p[0] + side * 1.2, p[1] - 2.6, label, size=size, anchor='start' if side > 0 else 'end', weight=700, fill=color))


def leader(svg, sv, x, z, tx, ty, lines, size=2.15, anchor='start', color='#1f1f1f', bold_first=True):
    """leader from point (x,z) in section to sheet text position (tx,ty)"""
    p = sv.p(x, z)
    kx = tx - (2.0 if anchor == 'start' else -2.0)
    svg.add(f'<path d="M{num(p[0])},{num(p[1])} L{num(kx)},{num(ty - size*0.35)} L{num(tx - (0.8 if anchor=="start" else -0.8))},{num(ty - size*0.35)}" '
            f'fill="none" stroke="#333" stroke-width="0.15" marker-start="url(#lead)"/>')
    for i, ln in enumerate(lines):
        svg.add(text(tx, ty + i * size * 1.3, ln, size=size if i == 0 else size * 0.9, anchor=anchor,
                     weight=700 if (i == 0 and bold_first) else 400, fill=color if i == 0 else '#444'))
