"""Furniture & equipment symbols in local frames (metres). All draw into ctx.svg."""
import math
from core import num, pts, path_poly, style, text

INK = '#3a3a3a'
FUR_FILL = '#ffffff'
GREEN = '#8cbf73'
GREEN_D = '#4f8a3c'
GREEN_L = '#cfe5c3'
WATER = '#cfe6f5'
WATER_D = '#4a86b5'
STEEL = '#d9dde1'


class Ctx:
    def __init__(self, svg, view, lw=1.0, detail=1, labels=True):
        self.svg, self.view, self.lw, self.detail = svg, view, lw, detail
        self.labels = labels

    def w(self, base):
        return base * self.lw


def poly(ctx, f, uv, fill=FUR_FILL, stroke=INK, sw=0.13, extra='', close=True):
    P = [f.p(u, v) for u, v in uv]
    ctx.svg.add(f'<path d="{path_poly(P, close)}" {style(fill, stroke, ctx.w(sw), extra)}/>')


def rect(ctx, f, u1, v1, u2, v2, fill=FUR_FILL, stroke=INK, sw=0.13, extra=''):
    poly(ctx, f, [(u1, v1), (u2, v1), (u2, v2), (u1, v2)], fill, stroke, sw, extra)


def line(ctx, f, u1, v1, u2, v2, stroke=INK, sw=0.1, extra=''):
    x1, y1 = f.p(u1, v1)
    x2, y2 = f.p(u2, v2)
    ctx.svg.add(f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" stroke="{stroke}" '
                f'stroke-width="{num(ctx.w(sw))}" {extra}/>')


def circ(ctx, f, u, v, r, fill=FUR_FILL, stroke=INK, sw=0.13, extra=''):
    x, y = f.p(u, v)
    ctx.svg.add(f'<circle cx="{num(x)}" cy="{num(y)}" r="{num(r * ctx.view.s)}" {style(fill, stroke, ctx.w(sw), extra)}/>')


def rrect(ctx, f, u1, v1, u2, v2, r, fill=FUR_FILL, stroke=INK, sw=0.13, n=5):
    """rounded rectangle via polyline"""
    uu1, uu2 = min(u1, u2), max(u1, u2)
    vv1, vv2 = min(v1, v2), max(v1, v2)
    r = min(r, (uu2 - uu1) / 2, (vv2 - vv1) / 2)
    P = []
    for cu, cv, a0 in ((uu2 - r, vv1 + r, -90), (uu2 - r, vv2 - r, 0), (uu1 + r, vv2 - r, 90), (uu1 + r, vv1 + r, 180)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n)
            P.append((cu + r * math.cos(a), cv + r * math.sin(a)))
    poly(ctx, f, P, fill, stroke, sw)


def ellipse(ctx, f, u, v, ru, rv, fill=FUR_FILL, stroke=INK, sw=0.13, n=28):
    P = [(u + ru * math.cos(2 * math.pi * k / n), v + rv * math.sin(2 * math.pi * k / n)) for k in range(n)]
    poly(ctx, f, P, fill, stroke, sw)


# ------------------------------------------------------------------ items
def bed(ctx, f, u, v, L=2.0, W=0.9, head='v-'):
    """bed with lower-left corner (u,v); length along v (head at v side given)"""
    if head in ('v-', 'v+'):
        rect(ctx, f, u, v, u + W, v + L, sw=0.15)
        if head == 'v+':
            rrect(ctx, f, u + 0.08, v + L - 0.42, u + W - 0.08, v + L - 0.08, 0.06)
            line(ctx, f, u, v + L * 0.55, u + W, v + L * 0.48, sw=0.08)
            line(ctx, f, u, v + L * 0.48, u + W, v + L * 0.48, sw=0.08)
        else:
            rrect(ctx, f, u + 0.08, v + 0.08, u + W - 0.08, v + 0.42, 0.06)
            line(ctx, f, u, v + L * 0.45, u + W, v + L * 0.52, sw=0.08)
            line(ctx, f, u, v + L * 0.52, u + W, v + L * 0.52, sw=0.08)
    else:  # length along u
        rect(ctx, f, u, v, u + L, v + W, sw=0.15)
        if head == 'u+':
            rrect(ctx, f, u + L - 0.42, v + 0.08, u + L - 0.08, v + W - 0.08, 0.06)
            line(ctx, f, u + L * 0.55, v, u + L * 0.48, v + W, sw=0.08)
            line(ctx, f, u + L * 0.48, v, u + L * 0.48, v + W, sw=0.08)
        else:
            rrect(ctx, f, u + 0.08, v + 0.08, u + 0.42, v + W - 0.08, 0.06)
            line(ctx, f, u + L * 0.45, v, u + L * 0.52, v + W, sw=0.08)
            line(ctx, f, u + L * 0.52, v, u + L * 0.52, v + W, sw=0.08)


def chair(ctx, f, u, v, s=0.45, back='v+'):
    rrect(ctx, f, u - s / 2, v - s / 2, u + s / 2, v + s / 2, 0.08, sw=0.1)
    b = 0.1
    if back == 'v+':
        rect(ctx, f, u - s / 2, v + s / 2 - b, u + s / 2, v + s / 2, fill='#e6e6e6', sw=0.08)
    elif back == 'v-':
        rect(ctx, f, u - s / 2, v - s / 2, u + s / 2, v - s / 2 + b, fill='#e6e6e6', sw=0.08)
    elif back == 'u+':
        rect(ctx, f, u + s / 2 - b, v - s / 2, u + s / 2, v + s / 2, fill='#e6e6e6', sw=0.08)
    else:
        rect(ctx, f, u - s / 2, v - s / 2, u - s / 2 + b, v + s / 2, fill='#e6e6e6', sw=0.08)


def round_chair(ctx, f, u, v, r=0.22):
    circ(ctx, f, u, v, r, sw=0.1)


def desk(ctx, f, u1, v1, u2, v2, chair_side=None):
    rect(ctx, f, u1, v1, u2, v2, sw=0.13)
    if chair_side:
        uc, vc = (u1 + u2) / 2, (v1 + v2) / 2
        if chair_side == 'v-':
            chair(ctx, f, uc, v1 - 0.25, back='v-')
        elif chair_side == 'v+':
            chair(ctx, f, uc, v2 + 0.25, back='v+')
        elif chair_side == 'u-':
            chair(ctx, f, u1 - 0.25, vc, back='u-')
        else:
            chair(ctx, f, u2 + 0.25, vc, back='u+')


def wardrobe(ctx, f, u1, v1, u2, v2):
    rect(ctx, f, u1, v1, u2, v2, fill='#f2f2f2', sw=0.13)
    line(ctx, f, u1, v1, u2, v2, sw=0.07)
    line(ctx, f, u1, v2, u2, v1, sw=0.07)


def shelves(ctx, f, u1, v1, u2, v2, n=None, fill='#f4f1ea'):
    rect(ctx, f, u1, v1, u2, v2, fill=fill, sw=0.13)
    lu, lv = abs(u2 - u1), abs(v2 - v1)
    if n is None:
        n = max(2, int(max(lu, lv) / 0.45))
    for k in range(1, n):
        if lu >= lv:
            uu = u1 + (u2 - u1) * k / n
            line(ctx, f, uu, v1, uu, v2, sw=0.06)
        else:
            vv = v1 + (v2 - v1) * k / n
            line(ctx, f, u1, vv, u2, vv, sw=0.06)


def rack(ctx, f, u1, v1, u2, v2, fill='#e9ecef', label=None, size=1.6):
    rect(ctx, f, u1, v1, u2, v2, fill=fill, sw=0.15)
    line(ctx, f, u1, v1, u2, v2, sw=0.06)
    if label and ctx.detail and ctx.labels:
        x, y = f.p((u1 + u2) / 2, (v1 + v2) / 2)
        ctx.svg.add(text(x, y + size * 0.35, label, size=size, fill='#333', weight=600))


def tank(ctx, f, u, v, r, label=None, size=1.5):
    circ(ctx, f, u, v, r, fill=WATER, stroke=WATER_D, sw=0.15)
    circ(ctx, f, u, v, r * 0.72, fill='none', stroke=WATER_D, sw=0.06)
    if label and ctx.detail and ctx.labels:
        x, y = f.p(u, v)
        ctx.svg.add(text(x, y + size * 0.35, label, size=size, fill='#1d4f73', weight=600))


def counter(ctx, f, u1, v1, u2, v2, fill='#f3f3f3'):
    rect(ctx, f, u1, v1, u2, v2, fill=fill, sw=0.14)


def sink(ctx, f, u, v, w=0.5, d=0.4):
    rrect(ctx, f, u - w / 2, v - d / 2, u + w / 2, v + d / 2, 0.08, fill='#ffffff', sw=0.1)
    circ(ctx, f, u, v, 0.04, fill='#999', stroke='none')


def cooktop(ctx, f, u, v, w=0.6, d=0.5):
    rect(ctx, f, u - w / 2, v - d / 2, u + w / 2, v + d / 2, fill='#ffffff', sw=0.1)
    for du in (-0.14, 0.14):
        for dv in (-0.11, 0.11):
            circ(ctx, f, u + du, v + dv, 0.08, fill='none', sw=0.07)


def fridge(ctx, f, u1, v1, u2, v2, lab='K'):
    rect(ctx, f, u1, v1, u2, v2, fill='#eef3f6', sw=0.14)
    line(ctx, f, u1, v1, u2, v2, sw=0.05)
    if ctx.detail and ctx.labels:
        x, y = f.p((u1 + u2) / 2, (v1 + v2) / 2)
        ctx.svg.add(text(x, y + 0.45, lab, size=1.3, fill='#555', weight=600))


def wc(ctx, f, u, v, ang='v+'):
    """vacuum toilet: tank against wall at v side"""
    if ang == 'v+':
        rect(ctx, f, u - 0.22, v - 0.18, u + 0.22, v, fill='#ffffff', sw=0.1)
        ellipse(ctx, f, u, v - 0.45, 0.2, 0.27, sw=0.1)
    elif ang == 'v-':
        rect(ctx, f, u - 0.22, v, u + 0.22, v + 0.18, fill='#ffffff', sw=0.1)
        ellipse(ctx, f, u, v + 0.45, 0.2, 0.27, sw=0.1)
    elif ang == 'u+':
        rect(ctx, f, u - 0.18, v - 0.22, u, v + 0.22, fill='#ffffff', sw=0.1)
        ellipse(ctx, f, u - 0.45, v, 0.27, 0.2, sw=0.1)
    else:
        rect(ctx, f, u, v - 0.22, u + 0.18, v + 0.22, fill='#ffffff', sw=0.1)
        ellipse(ctx, f, u + 0.45, v, 0.27, 0.2, sw=0.1)


def shower(ctx, f, u1, v1, u2, v2):
    rect(ctx, f, u1, v1, u2, v2, fill='#f2f8fc', sw=0.13)
    line(ctx, f, u1, v1, u2, v2, sw=0.06)
    line(ctx, f, u1, v2, u2, v1, sw=0.06)
    circ(ctx, f, (u1 + u2) / 2, (v1 + v2) / 2, 0.05, fill='#999', stroke='none')


def washer(ctx, f, u, v, s=0.6):
    rect(ctx, f, u - s / 2, v - s / 2, u + s / 2, v + s / 2, fill='#ffffff', sw=0.12)
    circ(ctx, f, u, v, s * 0.32, fill='none', sw=0.08)


def plant(ctx, f, u, v, r=0.3, dark=False):
    circ(ctx, f, u, v, r, fill=GREEN if not dark else GREEN_D, stroke=GREEN_D, sw=0.1)
    if r > 0.25 and ctx.detail:
        for k in range(5):
            a = 2 * math.pi * k / 5 + 0.3
            circ(ctx, f, u + r * 0.45 * math.cos(a), v + r * 0.45 * math.sin(a), r * 0.28,
                 fill='#a8d08f', stroke=GREEN_D, sw=0.05)


def tree(ctx, f, u, v, r=1.0):
    n = 14
    P = []
    for k in range(n * 2):
        a = math.pi * k / n
        rr = r * (1.0 if k % 2 == 0 else 0.86)
        P.append((u + rr * math.cos(a), v + rr * math.sin(a)))
    poly(ctx, f, P, fill='#b9d9a4', stroke=GREEN_D, sw=0.12)
    circ(ctx, f, u, v, r * 0.55, fill='#9cc983', stroke=GREEN_D, sw=0.06)
    circ(ctx, f, u, v, r * 0.12, fill='#7a5a3c', stroke='none')


def planter(ctx, f, uv_pts, fill='#e5d9c6'):
    poly(ctx, f, uv_pts, fill=fill, stroke='#8a7660', sw=0.13)


def hydro_rack(ctx, f, u1, v1, u2, v2):
    rect(ctx, f, u1, v1, u2, v2, fill=GREEN_L, stroke=GREEN_D, sw=0.14)
    lu, lv = abs(u2 - u1), abs(v2 - v1)
    n = max(3, int(max(lu, lv) / 0.25))
    for k in range(n):
        t = (k + 0.5) / n
        if lu >= lv:
            circ(ctx, f, u1 + (u2 - u1) * t, (v1 + v2) / 2, min(lv, 0.25) * 0.35, fill=GREEN, stroke='none')
        else:
            circ(ctx, f, (u1 + u2) / 2, v1 + (v2 - v1) * t, min(lu, 0.25) * 0.35, fill=GREEN, stroke='none')


def treadmill(ctx, f, u, v, L=2.0, W=0.85, along='v'):
    if along == 'v':
        rect(ctx, f, u, v, u + W, v + L, fill='#f0f0f0', sw=0.13)
        rect(ctx, f, u + 0.12, v + 0.3, u + W - 0.12, v + L - 0.15, fill='#d6d6d6', sw=0.07)
        rect(ctx, f, u, v, u + W, v + 0.25, fill='#bdbdbd', sw=0.07)
    else:
        rect(ctx, f, u, v, u + L, v + W, fill='#f0f0f0', sw=0.13)
        rect(ctx, f, u + 0.3, v + 0.12, u + L - 0.15, v + W - 0.12, fill='#d6d6d6', sw=0.07)
        rect(ctx, f, u, v, u + 0.25, v + W, fill='#bdbdbd', sw=0.07)


def bike(ctx, f, u, v, along='v'):
    if along == 'v':
        rrect(ctx, f, u - 0.25, v, u + 0.25, v + 1.2, 0.12, fill='#f0f0f0', sw=0.12)
        circ(ctx, f, u, v + 0.25, 0.16, fill='#cfcfcf', sw=0.07)
        rect(ctx, f, u - 0.12, v + 0.85, u + 0.12, v + 1.1, fill='#bdbdbd', sw=0.07)
    else:
        rrect(ctx, f, u, v - 0.25, u + 1.2, v + 0.25, 0.12, fill='#f0f0f0', sw=0.12)
        circ(ctx, f, u + 0.25, v, 0.16, fill='#cfcfcf', sw=0.07)
        rect(ctx, f, u + 0.85, v - 0.12, u + 1.1, v + 0.12, fill='#bdbdbd', sw=0.07)


def resistance(ctx, f, u1, v1, u2, v2):
    rect(ctx, f, u1, v1, u2, v2, fill='#f0f0f0', sw=0.14)
    um, vm = (u1 + u2) / 2, (v1 + v2) / 2
    rect(ctx, f, um - 0.08, v1, um + 0.08, v2, fill='#bdbdbd', sw=0.06)
    line(ctx, f, u1 + 0.1, vm, u2 - 0.1, vm, sw=0.12)
    circ(ctx, f, u1 + 0.18, vm, 0.12, fill='#999', sw=0.05)
    circ(ctx, f, u2 - 0.18, vm, 0.12, fill='#999', sw=0.05)


def mat(ctx, f, u1, v1, u2, v2):
    rect(ctx, f, u1, v1, u2, v2, fill='#eef2e8', stroke='#7c8c6a', sw=0.1)


def suit(ctx, f, u, v, s=0.75, fill='#ffffff'):
    """EVA suit (top view, hanging): PLSS backpack, torso + shoulders, arms, helmet with visor; centred at u,v"""
    rect(ctx, f, u - 0.26 * s, v - 0.40 * s, u + 0.26 * s, v - 0.17 * s, fill='#d9dde1', sw=0.09)      # PLSS
    rrect(ctx, f, u - 0.30 * s, v - 0.19 * s, u + 0.30 * s, v + 0.13 * s, 0.09 * s, fill=fill, sw=0.11)  # torso
    for sg in (-1, 1):
        rrect(ctx, f, u + sg * 0.29 * s, v - 0.12 * s, u + sg * 0.44 * s, v + 0.24 * s, 0.06 * s, fill=fill, sw=0.08)  # arms
    circ(ctx, f, u, v - 0.02 * s, 0.135 * s, fill='#e8eef3', sw=0.09)                                # helmet
    poly(ctx, f, [(u - 0.09 * s, v + 0.05 * s), (u, v + 0.10 * s), (u + 0.09 * s, v + 0.05 * s)], fill='none',
         stroke='#b5532e', sw=0.07, close=False)                                                          # visor


def table_round(ctx, f, u, v, r=0.6, chairs=4):
    circ(ctx, f, u, v, r, sw=0.14)
    for k in range(chairs):
        a = 2 * math.pi * k / chairs + math.pi / chairs
        round_chair(ctx, f, u + (r + 0.28) * math.cos(a), v + (r + 0.28) * math.sin(a))


def table_rect(ctx, f, u1, v1, u2, v2, chairs_u=0, chairs_v=0):
    rect(ctx, f, u1, v1, u2, v2, sw=0.14)
    for k in range(chairs_u):
        uu = u1 + (u2 - u1) * (k + 0.5) / chairs_u
        chair(ctx, f, uu, v1 - 0.28, back='v-')
        chair(ctx, f, uu, v2 + 0.28, back='v+')
    for k in range(chairs_v):
        vv = v1 + (v2 - v1) * (k + 0.5) / chairs_v
        chair(ctx, f, u1 - 0.28, vv, back='u-')
        chair(ctx, f, u2 + 0.28, vv, back='u+')


def screen(ctx, f, u1, v1, u2, v2):
    rect(ctx, f, u1, v1, u2, v2, fill='#4a5866', stroke='#2b333b', sw=0.08)


def glovebox(ctx, f, u1, v1, u2, v2, gloves='v-'):
    rect(ctx, f, u1, v1, u2, v2, fill='#eaf1f4', sw=0.15)
    vv = v1 if gloves == 'v-' else v2
    du = (u2 - u1)
    for t in (0.33, 0.67):
        circ(ctx, f, u1 + du * t, vv + (0.12 if gloves == 'v-' else -0.12), 0.08, fill='#ffffff', sw=0.08)


def label(ctx, f, u, v, s, size=1.6, fill='#555', weight=500, rot=0):
    if not ctx.labels:
        return
    x, y = f.p(u, v)
    ctx.svg.add(text(x, y + size * 0.35, s, size=size, fill=fill, weight=weight, rot=rot if rot else None))
