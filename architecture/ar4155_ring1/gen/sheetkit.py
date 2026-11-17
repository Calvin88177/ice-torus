"""Sheet furniture: frame, header, title block, legend swatches, dimension helpers, markers."""
import math
from core import num, text, esc, arc_d, radial_d, sector_d, fmt, upright, R0, path_poly
from plan import ICE_EDGE, MEM, HATCH_C, NODE_C

W, H = 841, 594
M = 10
ACC = '#8c2f14'      # accent (titles)
DIM = '#7a2a12'      # dimension colour
PROJECT = 'MARS ICE-ARCH TORUS HABITAT'
SITE = 'Utopia Planitia, Mars · 39,95° LU – 80,30° BT'
COURSE = 'AR4155 Topik Khusus E: Arsitektur Antariksa — “Membuat Hunian di Mars” · ITB'
GROUP = 'Kelompok 7'
DATE = '17 November 2026'


def frame(svg):
    svg.add(f'<rect x="{M}" y="{M}" width="{W-2*M}" height="{H-2*M}" fill="none" stroke="#1a1a1a" stroke-width="0.5"/>')
    svg.add(f'<rect x="{M+1.5}" y="{M+1.5}" width="{W-2*M-3}" height="{H-2*M-3}" fill="none" stroke="#1a1a1a" stroke-width="0.15"/>')


TOTAL = 6


def header(svg, sheet_no, title, subtitle, scale_txt):
    x0, y0 = M + 8, M + 14
    svg.add(text(x0, y0, title, size=9.5, anchor='start', weight=800, fill='#151515', ls='0.4'))
    svg.add(text(x0, y0 + 8, subtitle, size=5.0, anchor='start', weight=600, fill=ACC, ls='0.2'))
    svg.add(text(x0, y0 + 14.5, f'{PROJECT} · {SITE}', size=3.0, anchor='start', weight=500, fill='#444'))
    # sheet number badge top right
    bx, by = W - M - 34, M + 5
    svg.add(f'<rect x="{bx}" y="{by}" width="28" height="20" fill="#151515"/>')
    svg.add(text(bx + 14, by + 8.2, 'LEMBAR', size=2.6, weight=600, fill='#ffffff', ls='0.6'))
    svg.add(text(bx + 14, by + 17.2, f'{sheet_no}/{TOTAL}', size=7.5, weight=800, fill='#ffffff'))
    svg.add(text(bx - 4, by + 8.5, scale_txt, size=3.4, anchor='end', weight=700, fill='#151515'))
    svg.add(text(bx - 4, by + 14, 'kertas A1 (841 × 594 mm)', size=2.4, anchor='end', fill='#555'))


def title_block(svg, x, y, w, h, sheet_no, sheet_title, scale_txt, notes=None):
    svg.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#ffffff" stroke="#151515" stroke-width="0.35"/>')
    svg.add(f'<rect x="{x}" y="{y}" width="{w}" height="11" fill="#151515"/>')
    svg.add(text(x + 3, y + 7.4, PROJECT, size=4.4, anchor='start', weight=800, fill='#ffffff', ls='0.35'))
    rows = [
        ('Lokasi', SITE),
        ('Mata kuliah', COURSE),
        ('Tim', GROUP),
        ('Gambar', sheet_title),
        ('Skala', scale_txt),
        ('Tanggal / revisi', f'{DATE} · revisi total (modul 5,0° · separator 2 modul)'),
        ('Status', 'Desain konsep — bukan untuk konstruksi'),
    ]
    yy = y + 16
    for k, val in rows:
        svg.add(text(x + 3, yy, k.upper(), size=1.9, anchor='start', weight=700, fill='#777', ls='0.25'))
        svg.add(text(x + 27, yy, val, size=2.45, anchor='start', weight=500 if k != 'Gambar' else 700, fill='#1a1a1a'))
        yy += 4.6
    svg.add(f'<rect x="{x + w - 26}" y="{y + h - 19}" width="23" height="16" fill="#f2efe9" stroke="#151515" stroke-width="0.25"/>')
    svg.add(text(x + w - 14.5, y + h - 13.6, 'LEMBAR', size=2.0, weight=700, fill='#555', ls='0.4'))
    svg.add(text(x + w - 14.5, y + h - 6.0, f'{sheet_no}/{TOTAL}', size=6.2, weight=800))


def section_heading(svg, x, y, s, size=3.4, color='#151515', underline=None):
    svg.add(text(x, y, s, size=size, anchor='start', weight=800, fill=color, ls='0.3'))
    if underline:
        svg.add(f'<line x1="{x}" y1="{y+1.4}" x2="{x+underline}" y2="{y+1.4}" stroke="{color}" stroke-width="0.35"/>')


def para(svg, x, y, lines, size=2.35, lh=1.42, color='#2a2a2a', weight=400, bullet=False):
    for i, ln in enumerate(lines):
        s = ('• ' + ln) if bullet else ln
        svg.add(text(x, y + i * size * lh, s, size=size, anchor='start', weight=weight, fill=color))
    return y + len(lines) * size * lh


# ------------------------------------------------------------ dimension helpers (plan, polar)
def arc_dim(ctx, R, b1, b2, label_top=None, label_bot=None, ext_from=None, size=2.3, color=DIM, tick=1.6, bold=False):
    v, svg = ctx.view, ctx.svg
    svg.add(f'<path d="{arc_d(v, R, b1, b2)}" fill="none" stroke="{color}" stroke-width="0.18"/>')
    for b in (b1, b2):
        x, y = v.P(R, b)
        (tx, ty), (rx, ry) = v.dirs(b)
        # 45-degree tick
        dx, dy = (rx + tx) * 0.7071, (ry + ty) * 0.7071
        svg.add(f'<line x1="{num(x - dx*tick)}" y1="{num(y - dy*tick)}" x2="{num(x + dx*tick)}" y2="{num(y + dy*tick)}" stroke="{color}" stroke-width="0.32"/>')
        if ext_from is not None:
            svg.add(f'<path d="{radial_d(v, b, ext_from, R + 0.25)}" stroke="{color}" stroke-width="0.12" fill="none"/>')
    bm = 0.5 * (b1 + b2)
    (tx, ty), (rx, ry) = v.dirs(bm)
    ang = upright(math.degrees(math.atan2(ty, tx)))
    if label_top:
        x, y = v.P(R + 0.55, bm)
        svg.add(text(x, y, label_top, size=size, fill=color, weight=700 if bold else 600, rot=ang))
    if label_bot:
        x, y = v.P(R - 0.55 - size / 10 * 1.4, bm)
        x2, y2 = v.P(R - 0.55, bm)
        svg.add(text(x, y + 0.0, label_bot, size=size * 0.88, fill=color, weight=500, rot=ang))


def lin_dim(svg, p1, p2, off, label, size=2.3, color=DIM, ext=True, tick=1.4, text_side=1, ext_from=None):
    """linear dimension between sheet points p1, p2 offset by `off` mm along the left normal"""
    x1, y1 = p1
    x2, y2 = p2
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    nx, ny = -uy, ux
    a1 = (x1 + nx * off, y1 + ny * off)
    a2 = (x2 + nx * off, y2 + ny * off)
    svg.add(f'<line x1="{num(a1[0])}" y1="{num(a1[1])}" x2="{num(a2[0])}" y2="{num(a2[1])}" stroke="{color}" stroke-width="0.18"/>')
    for (px, py), (ax, ay) in ((p1, a1), (p2, a2)):
        if ext:
            s0 = 0.8 if off > 0 else -0.8
            svg.add(f'<line x1="{num(px + nx*s0)}" y1="{num(py + ny*s0)}" x2="{num(ax + nx*(1.0 if off>0 else -1.0))}" y2="{num(ay + ny*(1.0 if off>0 else -1.0))}" stroke="{color}" stroke-width="0.12"/>')
        dx, dy = (ux + nx) * 0.7071, (uy + ny) * 0.7071
        svg.add(f'<line x1="{num(ax - dx*tick)}" y1="{num(ay - dy*tick)}" x2="{num(ax + dx*tick)}" y2="{num(ay + dy*tick)}" stroke="{color}" stroke-width="0.32"/>')
    mx, my = (a1[0] + a2[0]) / 2, (a1[1] + a2[1]) / 2
    ang = upright(math.degrees(math.atan2(uy, ux)))
    # place text on the outer side
    ox, oy = nx * (1.1 if text_side > 0 else -2.9), ny * (1.1 if text_side > 0 else -2.9)
    if ang != math.degrees(math.atan2(uy, ux)):
        ox, oy = -ox, -oy
    svg.add(text(mx + ox * (1 if text_side > 0 else 1), my + oy, label, size=size, fill=color, weight=600, rot=ang))


def sec_marker(ctx, R, b, letter, look_dir, sheet_ref='3', color='#c0391b'):
    """end marker of a section line at polar point (R,b); arrow toward bearing direction look_dir (+1/-1)"""
    v, svg = ctx.view, ctx.svg
    x, y = v.P(R, b)
    (tx, ty), (rx, ry) = v.dirs(b)
    ax, ay = tx * look_dir, ty * look_dir
    svg.add(f'<line x1="{num(x)}" y1="{num(y)}" x2="{num(x + ax*6)}" y2="{num(y + ay*6)}" stroke="{color}" stroke-width="0.6" marker-end="url(#arrR)"/>')
    cx, cy = x + (rx if R > R0 else -rx) * 4.0, y + (ry if R > R0 else -ry) * 4.0
    svg.add(f'<circle cx="{num(cx)}" cy="{num(cy)}" r="3.4" fill="#ffffff" stroke="{color}" stroke-width="0.45"/>')
    svg.add(f'<line x1="{num(cx-3.4)}" y1="{num(cy)}" x2="{num(cx+3.4)}" y2="{num(cy)}" stroke="{color}" stroke-width="0.25"/>')
    svg.add(text(cx, cy - 0.6, letter, size=2.9, weight=800, fill=color))
    svg.add(text(cx, cy + 2.6, sheet_ref, size=2.0, weight=600, fill=color))


def north_arrow(svg, cx, cy, ang_screen, size=9, label='U'):
    """ang_screen: screen direction (deg, clockwise from +x... we pass angle of north vector) """
    a = math.radians(ang_screen)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    tip = (cx + ux * size, cy + uy * size)
    tail = (cx - ux * size * 0.55, cy - uy * size * 0.55)
    l = (cx + nx * size * 0.38 - ux * size * 0.15, cy + ny * size * 0.38 - uy * size * 0.15)
    r = (cx - nx * size * 0.38 - ux * size * 0.15, cy - ny * size * 0.38 - uy * size * 0.15)
    svg.add(f'<circle cx="{num(cx)}" cy="{num(cy)}" r="{num(size*0.72)}" fill="none" stroke="#222" stroke-width="0.25"/>')
    svg.add(f'<path d="M{num(tip[0])},{num(tip[1])} L{num(l[0])},{num(l[1])} L{num(tail[0])},{num(tail[1])} Z" fill="#222"/>')
    svg.add(f'<path d="M{num(tip[0])},{num(tip[1])} L{num(r[0])},{num(r[1])} L{num(tail[0])},{num(tail[1])} Z" fill="#ffffff" stroke="#222" stroke-width="0.25"/>')
    svg.add(text(cx + ux * (size + 3.2), cy + uy * (size + 3.2) + 1.2, label, size=3.4, weight=800))


def scale_bar(svg, x, y, s_mm_per_m, ticks=(0, 1, 2, 5, 10), label='skala grafis (m)'):
    L = ticks[-1] * s_mm_per_m
    h = 1.6
    for i in range(len(ticks) - 1):
        a, b = ticks[i] * s_mm_per_m, ticks[i + 1] * s_mm_per_m
        svg.add(f'<rect x="{num(x + a)}" y="{num(y)}" width="{num(b - a)}" height="{h}" fill="{"#151515" if i % 2 == 0 else "#ffffff"}" stroke="#151515" stroke-width="0.2"/>')
    for t in ticks:
        svg.add(text(x + t * s_mm_per_m, y + h + 3.2, f'{t}', size=2.3, weight=600))
    svg.add(text(x + L + 3, y + h, 'm', size=2.3, anchor='start', weight=600))
    svg.add(text(x, y - 1.6, label, size=2.1, anchor='start', fill='#555'))


# ------------------------------------------------------------ legend swatches
def sw_rect(svg, x, y, w, h, fill, stroke='#333', sw=0.2, extra=''):
    svg.add(f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')


def legend_row(svg, x, y, kind, label, w=9, h=3.6, size=2.25):
    yc = y - h * 0.75
    if kind == 'ice':
        sw_rect(svg, x, yc, w, h, 'url(#iceH)', ICE_EDGE, 0.25)
    elif kind == 'icebelow':
        sw_rect(svg, x, yc, w, h, '#eaf3fa', ICE_EDGE, 0.15, 'stroke-dasharray="1,0.5"')
    elif kind == 'gap':
        sw_rect(svg, x, yc, w, h, 'url(#gapH)', '#7a9cb8', 0.15)
    elif kind == 'mem':
        svg.add(f'<line x1="{x}" y1="{num(yc+h*0.35)}" x2="{x+w}" y2="{num(yc+h*0.35)}" stroke="{MEM}" stroke-width="0.4"/>')
        svg.add(f'<line x1="{x}" y1="{num(yc+h*0.65)}" x2="{x+w}" y2="{num(yc+h*0.65)}" stroke="{MEM}" stroke-width="0.22"/>')
    elif kind == 'chase':
        sw_rect(svg, x, yc, w, h, 'url(#chaseH)', '#8d8d8d', 0.15)
    elif kind == 'reg':
        sw_rect(svg, x, yc, w, h, 'url(#regH)', '#9c8463', 0.15)
    elif kind == 'node':
        sw_rect(svg, x, yc + h * 0.25, w, h * 0.5, NODE_C, 'none', 0)
    elif kind == 'wall':
        sw_rect(svg, x, yc + h * 0.35, w, h * 0.3, '#262626', 'none', 0)
    elif kind == 'acou':
        sw_rect(svg, x, yc + h * 0.2, w, h * 0.6, '#262626', 'none', 0)
        svg.add(f'<line x1="{x}" y1="{num(yc+h*0.5)}" x2="{x+w}" y2="{num(yc+h*0.5)}" stroke="#fff" stroke-width="0.6" stroke-dasharray="1.2,0.8"/>')
    elif kind == 'water':
        sw_rect(svg, x, yc, w, h, 'url(#waterH)', '#4a86b5', 0.15)
    elif kind == 'glass':
        svg.add(f'<line x1="{x}" y1="{num(yc+h*0.5)}" x2="{x+w}" y2="{num(yc+h*0.5)}" stroke="#5f8fb0" stroke-width="0.6"/>')
        svg.add(f'<line x1="{x}" y1="{num(yc+h*0.5)}" x2="{x+w}" y2="{num(yc+h*0.5)}" stroke="#fff" stroke-width="0.2"/>')
    elif kind == 'door':
        svg.add(f'<line x1="{x}" y1="{num(yc+h)}" x2="{x+w}" y2="{num(yc+h)}" stroke="#262626" stroke-width="0.4"/>')
        svg.add(f'<line x1="{x+1}" y1="{num(yc+h)}" x2="{x+1}" y2="{num(yc+h-3.4)}" stroke="#222" stroke-width="0.3"/>')
        svg.add(f'<path d="M{x+1},{num(yc+h-3.4)} A3.4,3.4 0 0 1 {x+4.4},{num(yc+h)}" fill="none" stroke="#555" stroke-width="0.12" stroke-dasharray="0.6,0.4"/>')
    elif kind == 'slide':
        svg.add(f'<line x1="{x}" y1="{num(yc+h*0.6)}" x2="{x+w}" y2="{num(yc+h*0.6)}" stroke="#262626" stroke-width="0.4"/>')
        sw_rect(svg, x + 2, yc + h * 0.6 - 0.6, 4.5, 0.6, '#fff', '#222', 0.15)
    elif kind == 'hatch':
        svg.add(f'<line x1="{x}" y1="{num(yc+h)}" x2="{x+w}" y2="{num(yc+h)}" stroke="{NODE_C}" stroke-width="0.8"/>')
        sw_rect(svg, x + 0.6, yc + h - 3.6, 0.7, 3.6, HATCH_C, 'none', 0)
        svg.add(f'<path d="M{x+1},{num(yc+h-3.6)} A3.6,3.6 0 0 1 {x+4.6},{num(yc+h)}" fill="none" stroke="{HATCH_C}" stroke-width="0.15" stroke-dasharray="0.7,0.4"/>')
    elif kind == 'h240':
        svg.add(f'<line x1="{x}" y1="{num(yc+h*0.5)}" x2="{x+w}" y2="{num(yc+h*0.5)}" stroke="#9a7b5a" stroke-width="0.2" stroke-dasharray="2.5,0.8,0.5,0.8"/>')
    elif kind == 'floor':
        svg.add(f'<line x1="{x}" y1="{num(yc+h*0.5)}" x2="{x+w}" y2="{num(yc+h*0.5)}" stroke="#7a8a99" stroke-width="0.2" stroke-dasharray="0.8,0.6"/>')
    elif kind == 'mezz':
        svg.add(f'<line x1="{x}" y1="{num(yc+h*0.5)}" x2="{x+w}" y2="{num(yc+h*0.5)}" stroke="#5a5a5a" stroke-width="0.25" stroke-dasharray="2.2,1.0"/>')
    elif kind == 'axis':
        svg.add(f'<line x1="{x}" y1="{num(yc+h*0.5)}" x2="{x+w}" y2="{num(yc+h*0.5)}" stroke="#b08a50" stroke-width="0.2" stroke-dasharray="4,0.8,0.6,0.8"/>')
    elif kind == 'grid':
        svg.add(f'<line x1="{x+w/2}" y1="{yc}" x2="{x+w/2}" y2="{yc+h}" stroke="#c9c6bd" stroke-width="0.2" stroke-dasharray="0.6,0.5"/>')
        sw_rect(svg, x, yc, w, h, '#efeeea', 'none', 0, 'opacity="0.6"')
    elif kind == 'corr':
        sw_rect(svg, x, yc, w, h, '#efeeea', '#8a8478', 0.2, 'stroke-dasharray="1.2,0.7"')
    elif kind == 'cut':
        svg.add(f'<line x1="{x}" y1="{num(yc+h*0.5)}" x2="{x+w}" y2="{num(yc+h*0.5)}" stroke="#c0391b" stroke-width="0.35" stroke-dasharray="3,0.8,0.6,0.8"/>')
    elif kind == 'void':
        sw_rect(svg, x, yc, w, h, 'url(#voidH)', '#9aa3ad', 0.2)
    elif kind == 'roof':
        sw_rect(svg, x, yc, w, h, 'url(#roofH)', '#9e9e9e', 0.15)
    elif kind == 'slab':
        sw_rect(svg, x, yc, w, h, 'url(#slabH)', '#666', 0.2)
    elif kind.startswith('#'):
        sw_rect(svg, x, yc, w, h, kind, '#999', 0.15)
    svg.add(text(x + w + 2.2, y, label, size=size, anchor='start', fill='#222'))
