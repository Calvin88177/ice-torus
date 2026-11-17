"""Core: SVG writer, view transforms, shell geometry for the Mars Ice-Arch Torus drawings.

World plan coords: metres, X east, Y north, tower at (0,0).
Bearing b (deg) measured clockwise from north. Point (R, b) -> X = R sin b, Y = R cos b.
Radial offset x = R - R0 (positive = outer side of the ring).
Sheet coords: millimetres, y down.
"""
import math
import numpy as np

# ---------------------------------------------------------------- constants
R0 = 28.0            # ring 1 axis radius
SPAN = 16.0          # outer ice span at +-0.00
RISE = 9.0           # outer ice crown height
T_ICE = 0.60
T_GAP = 0.10         # CO2 pocket
T_MEM = 0.025        # double membrane (two skins + interstitial gap), drawn slightly exaggerated in plan
MOD = 5.0            # degrees per module
X_FLOOR = 7.26       # membrane at floor level (14.52 clear)
X_CHASE = 6.60       # utility chase face
X_CORR = 1.80        # corridor clear half width (3.60)
WALL = 0.10          # partition thickness
CUT_G = 1.20         # plan cut height ground floor
CUT_M = 4.20         # plan cut height mezzanine (+3.00 + 1.20)
MEZ_TOP = 3.00
MEZ_BOT = 2.70
MEZ_EDGE = 4.50


def _solve_a():
    lo, hi = 1.0, 50.0
    for _ in range(200):
        m = 0.5 * (lo + hi)
        f = m * (math.cosh(SPAN / 2 / m) - 1) - RISE
        if f > 0:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)


A_CAT = _solve_a()


def z_outer(x):
    return RISE - A_CAT * (np.cosh(np.asarray(x) / A_CAT) - 1)


def offset_curve(d, xmax=8.6, n=4001):
    """Curve offset inward (toward the interior) by normal distance d from the outer ice face.
    Returns x, z arrays (full width, left to right)."""
    x = np.linspace(-xmax, xmax, n)
    z = z_outer(x)
    dz = -np.sinh(x / A_CAT)
    nx, nz = -dz, np.ones_like(dz)
    L = np.hypot(nx, nz)
    nx, nz = nx / L, nz / L          # outward normal
    return x - d * nx, z - d * nz


def half_width(d, z):
    """|x| of the offset-d curve at height z (positive side)."""
    x, zz = offset_curve(d)
    m = x >= 0
    x, zz = x[m], zz[m]
    i = np.argsort(zz)
    return float(np.interp(z, zz[i], x[i]))


def height_at(d, xq):
    x, zz = offset_curve(d)
    m = x >= 0
    x, zz = x[m], zz[m]
    i = np.argsort(x)
    return float(np.interp(abs(xq), x[i], zz[i]))


# plan-cut widths
def cut_widths(h):
    return dict(ice_out=half_width(0.0, h), ice_in=half_width(T_ICE, h),
                mem_out=half_width(T_ICE + T_GAP, h), mem_in=half_width(T_ICE + T_GAP + T_MEM, h))


# ---------------------------------------------------------------- formatting
def fmt(v, nd=2):
    s = f"{v:.{nd}f}"
    return s.replace('.', ',')


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


# ---------------------------------------------------------------- view
class View:
    """World (m) -> sheet (mm). denom = scale denominator, rot = view rotation in deg
    (bearing that points to sheet-up), origin = sheet position of world (0,0)."""

    def __init__(self, denom, ox, oy, up_bearing=0.0):
        self.denom = denom
        self.s = 1000.0 / denom
        self.ox, self.oy = ox, oy
        self.up = up_bearing

    def T(self, X, Y):
        a = math.radians(self.up)
        # rotate world so that bearing `up` points to +Y
        xr = X * math.cos(a) - Y * math.sin(a)
        yr = X * math.sin(a) + Y * math.cos(a)
        return self.ox + xr * self.s, self.oy - yr * self.s

    def P(self, R, b):
        br = math.radians(b)
        return self.T(R * math.sin(br), R * math.cos(br))

    def L(self, m):
        return m * self.s

    def dirs(self, b):
        """sheet unit vectors (tangential +b, radial outward) at bearing b"""
        x0, y0 = self.P(0, b)
        xr, yr = self.P(1, b)
        rx, ry = xr - x0, yr - y0
        n = math.hypot(rx, ry)
        rx, ry = rx / n, ry / n
        # tangential (+b, clockwise on screen) = radial rotated -90 in world -> on screen (y down) rotate +90
        tx, ty = -ry, rx
        return (tx, ty), (rx, ry)

    def local(self, R, b, tu=1, rv=1):
        return Frame(self, R, b, tu, rv)

    def sheet_angle(self, b):
        """screen angle (deg, clockwise from +x) of the radial outward direction at bearing b"""
        (tx, ty), (rx, ry) = self.dirs(b)
        return math.degrees(math.atan2(ry, rx))


class Frame:
    """Local rigid frame at polar point (R, b): u = tu * tangential(+b), v = rv * radial outward (metres)."""

    def __init__(self, view, R, b, tu=1, rv=1):
        self.v = view
        self.c = view.P(R, b)
        (tx, ty), (rx, ry) = view.dirs(b)
        self.tx, self.ty = tu * tx, tu * ty
        self.rx, self.ry = rv * rx, rv * ry
        self.R, self.b = R, b

    def p(self, u, v):
        s = self.v.s
        return (self.c[0] + (u * self.tx + v * self.rx) * s, self.c[1] + (u * self.ty + v * self.ry) * s)

    def uang(self):
        """screen angle of +u"""
        return math.degrees(math.atan2(self.ty, self.tx))

    def vang(self):
        return math.degrees(math.atan2(self.ry, self.rx))


# ---------------------------------------------------------------- svg
class SVG:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.defs = []
        self.body = []

    def add(self, s):
        self.body.append(s)

    def d(self, s):
        self.defs.append(s)

    def save(self, path, title=""):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                f'width="{self.w}mm" height="{self.h}mm" viewBox="0 0 {self.w} {self.h}">\n')
        if title:
            head += f'<title>{esc(title)}</title>\n'
        style = ('<style>text{font-family:Inter,"Helvetica Neue",Arial,sans-serif;}'
                 '.mono{font-family:"DejaVu Sans Mono",monospace;}</style>\n')
        out = head + style + '<defs>\n' + '\n'.join(self.defs) + '\n</defs>\n' + \
            f'<rect x="0" y="0" width="{self.w}" height="{self.h}" fill="#ffffff"/>\n' + '\n'.join(self.body) + '\n</svg>\n'
        with open(path, 'w') as f:
            f.write(out)


def num(v):
    return f"{v:.3f}".rstrip('0').rstrip('.')


def pts(seq):
    return ' '.join(f"{num(x)},{num(y)}" for x, y in seq)


def path_poly(seq, close=True):
    s = 'M' + ' L'.join(f"{num(x)},{num(y)}" for x, y in seq)
    return s + (' Z' if close else '')


def style(fill='none', stroke='#000', sw=0.25, extra=''):
    s = f'fill="{fill}" stroke="{stroke}" stroke-width="{num(sw)}"'
    if extra:
        s += ' ' + extra
    return s


def arc_d(view, R, b1, b2, move=True):
    """SVG path segment for an arc of radius R from bearing b1 to b2 (any direction)."""
    x1, y1 = view.P(R, b1)
    x2, y2 = view.P(R, b2)
    rr = view.L(R)
    large = 1 if abs(b2 - b1) > 180 else 0
    sweep = 1 if b2 > b1 else 0
    s = f"M{num(x1)},{num(y1)} " if move else f"L{num(x1)},{num(y1)} "
    if abs(b2 - b1) >= 359.999:
        bm = b1 + (b2 - b1) / 2
        xm, ym = view.P(R, bm)
        s += f"A{num(rr)},{num(rr)} 0 0 {sweep} {num(xm)},{num(ym)} "
        s += f"A{num(rr)},{num(rr)} 0 0 {sweep} {num(x2)},{num(y2)} "
        return s
    s += f"A{num(rr)},{num(rr)} 0 {large} {sweep} {num(x2)},{num(y2)} "
    return s


def sector_d(view, R1, R2, b1, b2):
    """closed annular sector path"""
    s = arc_d(view, R2, b1, b2, move=True)
    x, y = view.P(R1, b2)
    s += f"L{num(x)},{num(y)} "
    rr = view.L(R1)
    large = 1 if abs(b2 - b1) > 180 else 0
    sweep = 0 if b2 > b1 else 1
    x, y = view.P(R1, b1)
    s += f"A{num(rr)},{num(rr)} 0 {large} {sweep} {num(x)},{num(y)} Z"
    return s


def radial_d(view, b, R1, R2):
    x1, y1 = view.P(R1, b)
    x2, y2 = view.P(R2, b)
    return f"M{num(x1)},{num(y1)} L{num(x2)},{num(y2)}"


def text(x, y, s, size=2.5, anchor='middle', weight=400, fill='#1a1a1a', rot=None, extra='', ls=None, italic=False):
    tr = f' transform="rotate({num(rot)} {num(x)} {num(y)})"' if rot is not None else ''
    st = ' font-style="italic"' if italic else ''
    lsp = f' letter-spacing="{ls}"' if ls is not None else ''
    return (f'<text x="{num(x)}" y="{num(y)}" font-size="{num(size)}" text-anchor="{anchor}" '
            f'font-weight="{weight}" fill="{fill}"{st}{lsp}{tr} {extra}>{esc(s)}</text>')


def upright(angle):
    """make a text rotation readable (between -90 and 90)"""
    a = (angle + 180) % 360 - 180
    if a > 90:
        a -= 180
    if a < -90:
        a += 180
    return a
