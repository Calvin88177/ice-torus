"""Generic plan drawing: shell, separator nodes, rooms, walls, doors, stairs, grid, labels."""
import math
from core import (R0, X_FLOOR, X_CHASE, X_CORR, WALL, MOD, cut_widths, num, pts, path_poly, style, text,
                  arc_d, sector_d, radial_d, fmt, upright, MEZ_EDGE)
import furn as F
from core import half_width, T_ICE, T_GAP, T_MEM

X_H240 = half_width(T_ICE + T_GAP + T_MEM, 2.40)   # clear height 2.40 to the inner membrane skin

# palette
ICE_EDGE = '#3f74a1'
ICE_CUT = '#cfe3f2'
ICE_BELOW = '#eaf3fa'
GAP_FILL = '#fbfdff'
MEM = '#163f66'
CHASE = '#ececec'
CORR = '#f1f0ec'
WALL_C = '#262626'
HATCH_C = '#b5532e'
NODE_C = '#5b5f63'
REG = '#d9c7ae'
ZONE = {
    'node': '#f3f1ee', 'tech': '#f6f1e7', 'eclss': '#eef0f6', 'res': '#eaf4f1', 'comm': '#fbf4e4',
    'grow': '#edf6e6', 'priv': '#f4eef6', 'circ': '#f1f0ec', 'make': '#f3ede8', 'edu': '#eaf1f8',
}


def defs(svg, s):
    """hatch patterns, scaled for view scale s (mm per m)"""
    k = s / 10.0  # 1.0 at 1:100
    svg.d(f'<pattern id="iceH" patternUnits="userSpaceOnUse" width="{num(1.6*k)}" height="{num(1.6*k)}" '
          f'patternTransform="rotate(45)"><rect width="{num(1.6*k)}" height="{num(1.6*k)}" fill="{ICE_CUT}"/>'
          f'<line x1="0" y1="0" x2="0" y2="{num(1.6*k)}" stroke="#8fb7d6" stroke-width="{num(0.18*k)}"/></pattern>')
    svg.d(f'<pattern id="gapH" patternUnits="userSpaceOnUse" width="{num(0.8*k)}" height="{num(0.8*k)}">'
          f'<rect width="{num(0.8*k)}" height="{num(0.8*k)}" fill="#fafcfe"/>'
          f'<circle cx="{num(0.4*k)}" cy="{num(0.4*k)}" r="{num(0.07*k)}" fill="#7a9cb8"/></pattern>')
    svg.d(f'<pattern id="chaseH" patternUnits="userSpaceOnUse" width="{num(1.2*k)}" height="{num(1.2*k)}" '
          f'patternTransform="rotate(-45)"><rect width="{num(1.2*k)}" height="{num(1.2*k)}" fill="{CHASE}"/>'
          f'<line x1="0" y1="0" x2="0" y2="{num(1.2*k)}" stroke="#bdbdbd" stroke-width="{num(0.12*k)}"/></pattern>')
    svg.d(f'<pattern id="regH" patternUnits="userSpaceOnUse" width="{num(3.2*k)}" height="{num(1.8*k)}">'
          f'<rect width="{num(3.2*k)}" height="{num(1.8*k)}" fill="{REG}"/>'
          f'<rect x="{num(0.1*k)}" y="{num(0.1*k)}" width="{num(1.4*k)}" height="{num(0.7*k)}" rx="{num(0.3*k)}" fill="#e6d7c2" stroke="#a88f6e" stroke-width="{num(0.08*k)}"/>'
          f'<rect x="{num(1.7*k)}" y="{num(0.1*k)}" width="{num(1.4*k)}" height="{num(0.7*k)}" rx="{num(0.3*k)}" fill="#e6d7c2" stroke="#a88f6e" stroke-width="{num(0.08*k)}"/>'
          f'<rect x="{num(0.9*k)}" y="{num(1.0*k)}" width="{num(1.4*k)}" height="{num(0.7*k)}" rx="{num(0.3*k)}" fill="#e6d7c2" stroke="#a88f6e" stroke-width="{num(0.08*k)}"/>'
          f'<rect x="{num(-0.7*k)}" y="{num(1.0*k)}" width="{num(1.4*k)}" height="{num(0.7*k)}" rx="{num(0.3*k)}" fill="#e6d7c2" stroke="#a88f6e" stroke-width="{num(0.08*k)}"/>'
          f'<rect x="{num(2.5*k)}" y="{num(1.0*k)}" width="{num(1.4*k)}" height="{num(0.7*k)}" rx="{num(0.3*k)}" fill="#e6d7c2" stroke="#a88f6e" stroke-width="{num(0.08*k)}"/></pattern>')
    svg.d(f'<pattern id="groundH" patternUnits="userSpaceOnUse" width="{num(2.0*k)}" height="{num(2.0*k)}">'
          f'<rect width="{num(2.0*k)}" height="{num(2.0*k)}" fill="#f7f1e9"/>'
          f'<circle cx="{num(0.5*k)}" cy="{num(0.6*k)}" r="{num(0.06*k)}" fill="#c9b49a"/>'
          f'<circle cx="{num(1.4*k)}" cy="{num(1.5*k)}" r="{num(0.05*k)}" fill="#c9b49a"/>'
          f'<circle cx="{num(1.6*k)}" cy="{num(0.4*k)}" r="{num(0.04*k)}" fill="#d8c6ae"/></pattern>')
    svg.d(f'<pattern id="waterH" patternUnits="userSpaceOnUse" width="{num(0.9*k)}" height="{num(0.9*k)}" '
          f'patternTransform="rotate(45)"><rect width="{num(0.9*k)}" height="{num(0.9*k)}" fill="#d7ebf8"/>'
          f'<line x1="0" y1="0" x2="0" y2="{num(0.9*k)}" stroke="#5d97c4" stroke-width="{num(0.1*k)}"/></pattern>')
    svg.d(f'<pattern id="acouH" patternUnits="userSpaceOnUse" width="{num(0.5*k)}" height="{num(0.5*k)}" '
          f'patternTransform="rotate(45)"><rect width="{num(0.5*k)}" height="{num(0.5*k)}" fill="#ffffff"/>'
          f'<line x1="0" y1="0" x2="0" y2="{num(0.5*k)}" stroke="#262626" stroke-width="{num(0.12*k)}"/></pattern>')
    svg.d(f'<pattern id="voidH" patternUnits="userSpaceOnUse" width="{num(1.4*k)}" height="{num(1.4*k)}" '
          f'patternTransform="rotate(45)"><rect width="{num(1.4*k)}" height="{num(1.4*k)}" fill="none"/>'
          f'<line x1="0" y1="0" x2="0" y2="{num(1.4*k)}" stroke="#9aa3ad" stroke-width="{num(0.08*k)}"/></pattern>')
    svg.d(f'<pattern id="roofH" patternUnits="userSpaceOnUse" width="{num(1.0*k)}" height="{num(1.0*k)}">'
          f'<rect width="{num(1.0*k)}" height="{num(1.0*k)}" fill="#f4f4f4"/>'
          f'<circle cx="{num(0.5*k)}" cy="{num(0.5*k)}" r="{num(0.05*k)}" fill="#c4c4c4"/></pattern>')
    svg.d(f'<pattern id="slabH" patternUnits="userSpaceOnUse" width="{num(1.0*k)}" height="{num(1.0*k)}" '
          f'patternTransform="rotate(45)"><rect width="{num(1.0*k)}" height="{num(1.0*k)}" fill="#e2e2e2"/>'
          f'<line x1="0" y1="0" x2="0" y2="{num(1.0*k)}" stroke="#9e9e9e" stroke-width="{num(0.1*k)}"/></pattern>')
    svg.d('<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">'
          '<path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker>')
    svg.d('<marker id="arrR" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4.5" markerHeight="4.5" orient="auto-start-reverse">'
          '<path d="M0,0 L10,5 L0,10 z" fill="#b5532e"/></marker>')


# -------------------------------------------------------------- helpers
def rad(deg):
    return math.radians(deg)


def ang_of(length, R):
    """degrees subtended by arc length at radius R"""
    return math.degrees(length / R)


def Rx(band, x):
    return R0 + x if band == 'O' else R0 - x


class XY:
    """local straight frame in sheet coords: origin o (sheet), unit u (ux,uy), unit v, scale s"""

    def __init__(self, o, u, v, s):
        self.o, self.u, self.vv, self.s = o, u, v, s
        self.v = type('V', (), {'s': s})

    def p(self, a, b):
        return (self.o[0] + (a * self.u[0] + b * self.vv[0]) * self.s,
                self.o[1] + (a * self.u[1] + b * self.vv[1]) * self.s)


def seg_frame(view, p1, p2, into):
    """frame along a straight world segment p1->p2 (world polar tuples (R,b)); v toward side `into` (+1 left/-1)"""
    a = view.P(*p1)
    b = view.P(*p2)
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    vx, vy = -uy * into, ux * into
    return XY(a, (ux, uy), (vx, vy), view.s), L / view.s


# -------------------------------------------------------------- shell
def draw_ground(ctx, b1, b2, Rin=16.0, Rout=40.0):
    v = ctx.view
    ctx.svg.add(f'<path d="{sector_d(v, Rin, Rout, b1, b2)}" fill="url(#groundH)" stroke="none"/>')


def draw_shell(ctx, b1, b2, h, show_floor_edge=True, show_h240=True, end_lines=True):
    """ice ring between bearings b1..b2, cut at height h"""
    v, svg = ctx.view, ctx.svg
    cw = cut_widths(h)
    lw = ctx.lw
    for sgn in (1, -1):
        def R(x):
            return R0 + sgn * x
        # ice below cut (foot) out to x=8.00
        svg.add(f'<path d="{sector_d(v, min(R(cw["ice_out"]), R(8.0)), max(R(cw["ice_out"]), R(8.0)), b1, b2)}" '
                f'fill="{ICE_BELOW}" stroke="none"/>')
        # cut ice
        svg.add(f'<path d="{sector_d(v, min(R(cw["ice_in"]), R(cw["ice_out"])), max(R(cw["ice_in"]), R(cw["ice_out"])), b1, b2)}" '
                f'fill="url(#iceH)" stroke="none"/>')
        # co2 gap
        svg.add(f'<path d="{sector_d(v, min(R(cw["mem_out"]), R(cw["ice_in"])), max(R(cw["mem_out"]), R(cw["ice_in"])), b1, b2)}" '
                f'fill="url(#gapH)" stroke="none"/>')
        # outlines
        svg.add(f'<path d="{arc_d(v, R(8.0), b1, b2)}" {style("none", ICE_EDGE, 0.18*lw, "stroke-dasharray=\"1.2,0.6\"")}/>')
        svg.add(f'<path d="{arc_d(v, R(cw["ice_out"]), b1, b2)}" {style("none", ICE_EDGE, 0.35*lw)}/>')
        svg.add(f'<path d="{arc_d(v, R(cw["ice_in"]), b1, b2)}" {style("none", ICE_EDGE, 0.35*lw)}/>')
        # double membrane
        svg.add(f'<path d="{arc_d(v, R(cw["mem_out"]), b1, b2)}" {style("none", MEM, 0.30*lw)}/>')
        svg.add(f'<path d="{arc_d(v, R(cw["mem_in"]), b1, b2)}" {style("none", MEM, 0.18*lw)}/>')
        if show_floor_edge and h < 2:
            svg.add(f'<path d="{arc_d(v, R(X_FLOOR), b1, b2)}" {style("none", "#7a8a99", 0.12*lw, "stroke-dasharray=\"0.8,0.6\"")}/>')
        if show_h240 and h < 2:
            svg.add(f'<path d="{arc_d(v, R(X_H240), b1, b2)}" {style("none", "#9a7b5a", 0.12*lw, "stroke-dasharray=\"2.5,0.8,0.5,0.8\"")}/>')
    if end_lines:
        for b in (b1, b2):
            for sgn in (1, -1):
                svg.add(f'<path d="{radial_d(v, b, R0 + sgn * cw["mem_out"], R0 + sgn * 8.0)}" {style("none", ICE_EDGE, 0.3*lw)}/>')


def draw_chase(ctx, b1, b2, h=1.2, sides=(1, -1)):
    v = ctx.view
    cw = cut_widths(h)
    for sgn in sides:
        r1, r2 = R0 + sgn * X_CHASE, R0 + sgn * cw['mem_in']
        ctx.svg.add(f'<path d="{sector_d(v, min(r1, r2), max(r1, r2), b1, b2)}" fill="url(#chaseH)" stroke="none"/>')
        ctx.svg.add(f'<path d="{arc_d(v, r1, b1, b2)}" {style("none", "#8d8d8d", 0.15*ctx.lw)}/>')


def draw_node(ctx, b1, b2, h=1.2, free_ends=(), shield_out=9.2, label=None):
    """separator node: rigid frame + regolith-bag shielding (no ice)."""
    v, svg, lw = ctx.view, ctx.svg, ctx.lw
    cw = cut_widths(h)
    t_node = 0.22
    for sgn in (1, -1):
        r_in = R0 + sgn * cw['mem_out']
        r_wall = R0 + sgn * (cw['mem_out'] + t_node)
        r_sh = R0 + sgn * shield_out
        svg.add(f'<path d="{sector_d(v, min(r_wall, r_sh), max(r_wall, r_sh), b1, b2)}" fill="url(#regH)" stroke="#9c8463" stroke-width="{num(0.15*lw)}"/>')
        svg.add(f'<path d="{sector_d(v, min(r_in, r_wall), max(r_in, r_wall), b1, b2)}" fill="{NODE_C}" stroke="none"/>')
    # free-end shields (temporary end walls of regolith bags)
    for bb, direction in free_ends:
        bend = bb + direction * ang_of(1.6, R0)
        svg.add(f'<path d="{sector_d(v, R0 - shield_out, R0 + shield_out, min(bb, bend), max(bb, bend))}" '
                f'fill="url(#regH)" stroke="#9c8463" stroke-width="{num(0.15*lw)}"/>')


def node_bulkhead(ctx, b, h=1.2, t=0.25):
    """radial rigid bulkhead across the full width at bearing b (thickness t in metres)"""
    v = ctx.view
    cw = cut_widths(h)
    w = v.L(t)
    svg = ctx.svg
    svg.add(f'<path d="{radial_d(v, b, R0 - cw["mem_out"] - 0.22, R0 + cw["mem_out"] + 0.22)}" '
            f'stroke="{NODE_C}" stroke-width="{num(w)}" fill="none"/>')


# -------------------------------------------------------------- walls
def wall_arc(ctx, R, b1, b2, t=WALL, color=WALL_C, acoustic=False):
    v = ctx.view
    if acoustic:
        ctx.svg.add(f'<path d="{arc_d(v, R, b1, b2)}" stroke="{color}" stroke-width="{num(v.L(t))}" fill="none"/>')
        ctx.svg.add(f'<path d="{arc_d(v, R, b1, b2)}" stroke="#ffffff" stroke-width="{num(v.L(t)*0.45)}" fill="none" stroke-dasharray="{num(v.L(0.12))},{num(v.L(0.08))}"/>')
    else:
        ctx.svg.add(f'<path d="{arc_d(v, R, b1, b2)}" stroke="{color}" stroke-width="{num(v.L(t))}" fill="none"/>')


def wall_rad(ctx, b, R1, R2, t=WALL, color=WALL_C, acoustic=False):
    v = ctx.view
    d = radial_d(v, b, R1, R2)
    ctx.svg.add(f'<path d="{d}" stroke="{color}" stroke-width="{num(v.L(t))}" fill="none" stroke-linecap="butt"/>')
    if acoustic:
        ctx.svg.add(f'<path d="{d}" stroke="#ffffff" stroke-width="{num(v.L(t)*0.45)}" fill="none" stroke-dasharray="{num(v.L(0.12))},{num(v.L(0.08))}"/>')


def glass_arc(ctx, R, b1, b2, t=0.06):
    v = ctx.view
    ctx.svg.add(f'<path d="{arc_d(v, R, b1, b2)}" stroke="#5f8fb0" stroke-width="{num(v.L(t))}" fill="none"/>')
    ctx.svg.add(f'<path d="{arc_d(v, R, b1, b2)}" stroke="#ffffff" stroke-width="{num(v.L(t)*0.35)}" fill="none"/>')


def gap_arc(ctx, R, b, width, t=WALL + 0.04):
    """white opening in an arc wall centred at bearing b"""
    v = ctx.view
    da = ang_of(width / 2, R)
    ctx.svg.add(f'<path d="{arc_d(v, R, b - da, b + da)}" stroke="#ffffff" stroke-width="{num(v.L(t))}" fill="none"/>')


def gap_rad(ctx, b, R1, R2, t=WALL + 0.04):
    v = ctx.view
    ctx.svg.add(f'<path d="{radial_d(v, b, R1, R2)}" stroke="#ffffff" stroke-width="{num(v.L(t))}" fill="none"/>')


# -------------------------------------------------------------- doors
def _arcpts(f, cx, cy, r, a0, a1, n=16):
    return [f.p(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


def door_on_arc(ctx, R, b, width, into, kind='swing', hinge='-', t=WALL):
    """door in an arc wall at radius R, centre bearing b. into=+1 opens toward larger R, -1 toward smaller R.
    kind: swing | slide | hatch | double | open"""
    v, svg, lw = ctx.view, ctx.svg, ctx.lw
    gap_arc(ctx, R, b, width, t + 0.04)
    if kind == 'open':
        return
    da = ang_of(width / 2, R)
    bh = b - da if hinge == '-' else b + da
    tu = 1 if hinge == '-' else -1
    f = v.local(R, bh, tu=tu, rv=into)
    _door_leaf(ctx, f, width, kind, t)


def door_on_rad(ctx, b, R1, R2, into, kind='swing', hinge='-', t=WALL):
    """door in a radial wall at bearing b between radii R1<R2 (opening). into=+1 opens toward larger bearing."""
    v = ctx.view
    gap_rad(ctx, b, R1, R2, t + 0.04)
    if kind == 'open':
        return
    width = R2 - R1
    Rh = R1 if hinge == '-' else R2
    other = R2 if hinge == '-' else R1
    a = v.P(Rh, b)
    c = v.P(other, b)
    L = math.hypot(c[0] - a[0], c[1] - a[1])
    ux, uy = (c[0] - a[0]) / L, (c[1] - a[1]) / L
    (tx, ty), _ = v.dirs(b)
    vx, vy = tx * into, ty * into
    f = XY(a, (ux, uy), (vx, vy), v.s)
    _door_leaf(ctx, f, width, kind, t)


def _door_leaf(ctx, f, w, kind, t):
    svg, lw = ctx.svg, ctx.lw
    if kind == 'swing':
        P = _arcpts(f, 0, 0, w, 90, 0)
        svg.add(f'<path d="{path_poly(P, False)}" fill="none" stroke="#555" stroke-width="{num(0.1*lw)}" stroke-dasharray="0.6,0.4"/>')
        a, b_ = f.p(0, 0), f.p(0, w)
        svg.add(f'<line x1="{num(a[0])}" y1="{num(a[1])}" x2="{num(b_[0])}" y2="{num(b_[1])}" stroke="#222" stroke-width="{num(0.25*lw)}"/>')
    elif kind == 'double':
        h = w / 2
        for (o, s0, s1, sgn) in ((0, 90, 0, 1), (w, 90, 180, -1)):
            P = _arcpts(f, o, 0, h, s0, s1)
            svg.add(f'<path d="{path_poly(P, False)}" fill="none" stroke="#555" stroke-width="{num(0.1*lw)}" stroke-dasharray="0.6,0.4"/>')
            a, b_ = f.p(o, 0), f.p(o, h)
            svg.add(f'<line x1="{num(a[0])}" y1="{num(a[1])}" x2="{num(b_[0])}" y2="{num(b_[1])}" stroke="#222" stroke-width="{num(0.25*lw)}"/>')
    elif kind == 'slide':
        # pocket door: leaf half-retracted into the wall pocket (dashed)
        P = [f.p(-0.55 * w, -0.03), f.p(0.45 * w, -0.03), f.p(0.45 * w, 0.03), f.p(-0.55 * w, 0.03)]
        svg.add(f'<path d="{path_poly(P)}" fill="#ffffff" stroke="#222" stroke-width="{num(0.14*lw)}"/>')
        P2 = [f.p(-w, -t / 2), f.p(0, -t / 2), f.p(0, t / 2), f.p(-w, t / 2)]
        svg.add(f'<path d="{path_poly(P2)}" fill="none" stroke="#777" stroke-width="{num(0.08*lw)}" stroke-dasharray="0.5,0.4"/>')
        a, b_ = f.p(0.15 * w, 0.18), f.p(0.75 * w, 0.18)
        svg.add(f'<line x1="{num(b_[0])}" y1="{num(b_[1])}" x2="{num(a[0])}" y2="{num(a[1])}" stroke="#666" stroke-width="{num(0.08*lw)}" marker-end="url(#arr)"/>')
    elif kind == 'hatch':
        # pressure hatch: heavy frame blocks + heavy leaf + swing
        for uu in (-0.12, w):
            P = [f.p(uu, -t / 2 - 0.06), f.p(uu + 0.12, -t / 2 - 0.06), f.p(uu + 0.12, t / 2 + 0.06), f.p(uu, t / 2 + 0.06)]
            svg.add(f'<path d="{path_poly(P)}" fill="{HATCH_C}" stroke="none"/>')
        P = _arcpts(f, 0, 0, w, 90, 0)
        svg.add(f'<path d="{path_poly(P, False)}" fill="none" stroke="{HATCH_C}" stroke-width="{num(0.12*lw)}" stroke-dasharray="0.7,0.4"/>')
        P = [f.p(-0.03, 0), f.p(0.07, 0), f.p(0.07, w), f.p(-0.03, w)]
        svg.add(f'<path d="{path_poly(P)}" fill="{HATCH_C}" stroke="#7a3216" stroke-width="{num(0.06*lw)}"/>')


# -------------------------------------------------------------- stairs
def spiral_stair(ctx, R, b, d=1.6, up=True, label=None, n=14, start=0.0):
    v, svg, lw = ctx.view, ctx.svg, ctx.lw
    f = v.local(R, b)
    r = d / 2
    F.circ(ctx, f, 0, 0, r, fill='#ffffff', sw=0.2)
    F.circ(ctx, f, 0, 0, 0.09, fill='#555', sw=0.08)
    for k in range(n):
        a = math.radians(start + 360 * k / n)
        F.line(ctx, f, 0.09 * math.cos(a), 0.09 * math.sin(a), r * math.cos(a), r * math.sin(a), sw=0.07)
    # direction arc
    P = _arcpts(f, 0, 0, r * 0.62, start + 10, start + 300, 24)
    svg.add(f'<path d="{path_poly(P, False)}" fill="none" stroke="#333" stroke-width="{num(0.12*lw)}" marker-end="url(#arr)"/>')
    if label:
        x, y = f.p(0, 0)
        svg.add(text(x, y - v.L(r) - 0.8, label, size=2.2 * min(1.0, v.s / 10) if v.s < 10 else 2.2, weight=700, fill='#222'))


# -------------------------------------------------------------- labels
def room_tag(ctx, R, b, num_s, area=None, name=None, r_mm=2.4, size=2.4, fill='#ffffff', stroke='#222', name_size=1.7):
    v, svg = ctx.view, ctx.svg
    x, y = v.P(R, b)
    svg.add(f'<circle cx="{num(x)}" cy="{num(y)}" r="{num(r_mm)}" fill="{fill}" stroke="{stroke}" stroke-width="0.22"/>')
    svg.add(text(x, y + size * 0.36, num_s, size=size if len(num_s) < 3 else size * 0.82, weight=700))
    yy = y + r_mm + name_size * 1.15
    if name:
        for line in name.split('\n'):
            svg.add(text(x, yy, line, size=name_size, weight=500, fill='#333'))
            yy += name_size * 1.15
    if area is not None:
        svg.add(text(x, yy, f"{fmt(area, 1)} m²", size=name_size * 0.95, fill='#666'))


def sector_area(R1, R2, b1, b2):
    return 0.5 * math.radians(abs(b2 - b1)) * abs(R2 ** 2 - R1 ** 2)
