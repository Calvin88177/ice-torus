"""Embed subsetted Inter (WOFF, base64) into SVGs via @font-face so browsers render the exact font.
usage: embed_fonts.py in.svg out.svg"""
import sys, re, io, base64, html
from fontTools import subset
from fontTools.ttLib import TTFont

FONTS = {400: 'Inter-Regular.otf', 500: 'Inter-Medium.otf', 600: 'Inter-SemiBold.otf',
         700: 'Inter-Bold.otf', 800: 'Inter-ExtraBold.otf'}
DIR = '/usr/share/fonts/opentype/inter/'

src, dst = sys.argv[1], sys.argv[2]
svg = open(src, encoding='utf-8').read()
chars = set()
for m in re.finditer(r'<text[^>]*>(.*?)</text>', svg, re.S):
    chars |= set(html.unescape(m.group(1)))
chars |= set(' 0123456789')
weights = sorted({int(w) for w in re.findall(r'font-weight="(\d+)"', svg)})
rules = []
for w in weights:
    fn = FONTS.get(w, FONTS[400])
    font = TTFont(DIR + fn)
    opts = subset.Options()
    opts.flavor = 'woff'
    opts.layout_features = ['kern', 'liga', 'calt', 'tnum', 'case']
    opts.name_IDs = ['*']
    opts.notdef_outline = True
    sub = subset.Subsetter(options=opts)
    sub.populate(text=''.join(chars))
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = 'woff'
    font.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode('ascii')
    rules.append(f'@font-face{{font-family:"Inter";font-style:normal;font-weight:{w};'
                 f'src:url(data:font/woff;base64,{b64}) format("woff");}}')
style_open = '<style>'
i = svg.index(style_open) + len(style_open)
svg = svg[:i] + ''.join(rules) + svg[i:]
open(dst, 'w', encoding='utf-8').write(svg)
print(dst, len(chars), 'chars', weights, f'{len(svg)/1024:.0f} KB')
