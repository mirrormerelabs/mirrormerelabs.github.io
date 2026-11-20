"""Pixel fells reflected in a mere. Adapted from Peter's assets/make_banner.py.
Usage: python3 fells.py OUT.svg THEME(dark|light) WIDTH HEIGHT HORIZON X0"""
import math, random, sys
out, theme = sys.argv[1], sys.argv[2]
W, H, HZ, x0 = (int(v) for v in sys.argv[3:7])
HS = float(sys.argv[7]) if len(sys.argv) > 7 else 1.0   # hill height scale
C = int(sys.argv[8]) if len(sys.argv) > 8 else 10
random.seed(7)
sx = (W - x0) / (1280 - 600)          # stretch the original peak layout across the art area
def X(x): return x0 + (x - 600) * sx
NEAR = [(X(c), w * sx, a) for c, w, a in [(700,70,52),(820,60,88),(930,85,70),(1060,55,104),(1170,70,66),(1265,60,48)]]
FAR  = [(X(c), w * sx, a) for c, w, a in [(760,90,96),(900,70,140),(1010,80,118),(1120,60,150),(1230,90,110)]]
def bumps(x, peaks): return sum(a * math.exp(-((x - c) / w) ** 2) for c, w, a in peaks)
def ease(x): return min(1, max(0, (x - x0) / (120 * sx)))
def ridge(x): return HS * (bumps(x, NEAR) + 8 * math.sin(x / 23.0)) * ease(x)
def ridge_far(x): return HS * (bumps(x, FAR) + 6 * math.sin(x / 31.0 + 1)) * ease(x)
WOOD=["#2f6b4f","#3a7d5c","#285c45"]; GRASS=["#6f9a54","#7fa860","#5d8a49"]; CROP=["#c9a227","#d9b44a","#b8912a"]; ACCENT=["#eb6834"]
def cover(row, top_rows):
    depth = row / max(1, top_rows); r = random.random()
    if r < 0.012: return random.choice(ACCENT)
    if depth < 0.45: pool = WOOD if r < 0.8 else GRASS
    elif depth < 0.8: pool = GRASS if r < 0.55 else (WOOD if r < 0.75 else CROP)
    else: pool = CROP if r < 0.5 else GRASS
    return random.choice(pool)
if theme == "dark":
    HAZE=["#3f6f9e","#4a7bab","#365f89","#5588b8"]; sky=("#0b1a2c","#1b3f63"); mere=("#14304d","#0a1726")
    refl_op, rip_col, rip_op, grat_col, grat_op, line_op = 0.33, "#cfe0f2", 0.22, "#9ec5f4", 0.0, 0.18
else:
    HAZE=["#9db8d3","#aac3dc","#8eabc8","#b5cde3"]; sky=("#ffffff","#ffffff"); mere=("#eef3f7","#f7fafc")
    refl_op, rip_col, rip_op, grat_col, grat_op, line_op = 0.22, "#7f9bb5", 0.25, "#2F5D6E", 0.0, 0.25
land, refl, far = [], [], []
for cx in range(x0, W, C):
    rows = int(ridge_far(cx + C/2) // C)
    for r in range(rows):
        far.append(f'<rect x="{cx}" y="{HZ-(r+1)*C}" width="{C-1}" height="{C-1}" fill="{random.choice(HAZE)}" opacity="{0.35+0.35*r/max(1,rows):.2f}"/>')
for cx in range(x0, W, C):
    rows = int(ridge(cx + C/2) // C)
    for r in range(rows):
        col = cover(rows-1-r, rows)
        land.append(f'<rect x="{cx}" y="{HZ-(r+1)*C}" width="{C-1}" height="{C-1}" fill="{col}"/>')
        ry = HZ + r*C*0.62 + 2
        if ry < H - 4:
            dx = round(3*math.sin(r*1.7 + cx/40), 1)
            refl.append(f'<rect x="{cx+dx}" y="{ry:.1f}" width="{C-1}" height="{C*0.62-1:.1f}" fill="{col}"/>')
rips = []
for i in range(9):
    y = HZ + 10 + i*11
    if y > H - 6: break
    x = random.randint(x0-40, W-260); w = random.randint(80, 220)
    rips.append(f'<rect class="rip r{i%3}" x="{x}" y="{y}" width="{w}" height="1.2" rx="0.6" fill="{rip_col}" opacity="{rip_op}"/>')
grat = "".join(f'<path d="M0 {y} H{W}" stroke="{grat_col}" stroke-opacity="{grat_op}"/>' for y in range(40, HZ, 43)) + \
       "".join(f'<path d="M{x} 0 V{HZ}" stroke="{grat_col}" stroke-opacity="{grat_op}"/>' for x in range(80, W, 80)) if grat_op else ""
sat = f'<g class="sat"><circle cx="0" cy="34" r="2.2" fill="#ffffff" opacity="0.85"/><path d="M-46 34 H-4" stroke="#ffffff" stroke-opacity="0.25" stroke-width="1"/></g>' if theme=="dark" else ""
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMaxYMax meet" role="img" aria-label="Hills drawn as land-cover pixels, woodland, grassland and cropland, reflected in a lake">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky[0]}"/><stop offset="1" stop-color="{sky[1]}"/></linearGradient>
<linearGradient id="mere" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{mere[0]}"/><stop offset="1" stop-color="{mere[1]}"/></linearGradient>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{mere[1]}" stop-opacity="0"/><stop offset="1" stop-color="{mere[1]}" stop-opacity="0.85"/></linearGradient>
<style>
.rip {{ animation: drift 14s ease-in-out infinite alternate; }} .r1 {{ animation-duration: 19s; }} .r2 {{ animation-duration: 23s; }}
@keyframes drift {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-60px); }} }}
.sat {{ animation: orbit 38s linear infinite; }}
@keyframes orbit {{ from {{ transform: translateX(-60px); }} to {{ transform: translateX({W+60}px); }} }}
@media (prefers-reduced-motion: reduce) {{ .rip, .sat {{ animation: none; }} }}
</style></defs>
{grat}{sat}
<g opacity="{refl_op}">{"".join(refl)}</g>
{"".join(rips)}<g>{"".join(far)}</g><g>{"".join(land)}</g>
<path d="M0 {HZ} H{W}" stroke="{rip_col}" stroke-opacity="{line_op}"/>
</svg>'''
open(out, "w").write(svg)
print(out, len(svg)//1024, "KB")
