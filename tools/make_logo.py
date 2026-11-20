"""Export the toned-down Mirrored M logo as SVG and PNG files."""
import cairosvg, os
OUT=os.path.join(os.path.dirname(__file__), '..', 'images', 'brand')
NAVY='#0b1a2c'; INK='#0F1E2E'
m_rows=["X.....X","XX...XX","X.X.X.X","X..X..X","X.....X"]
rowpal=[["#365f89","#3f6f9e"],["#3f6f9e","#2f6b4f"],["#2f6b4f","#285c45"],["#3a7d5c","#5d8a49"],["#5d8a49","#b8912a"]]
base={}
for r,row in enumerate(m_rows):
    for c,ch in enumerate(row):
        if ch=='X': base[(c,r)]=rowpal[r][(c+r)%2]
withdot=dict(base); withdot[(3,3)]='#eb6834'
CELL, GAP = 22, 3
STEP=CELL+GAP; COLS, ROWS = 7, 5
W=COLS*STEP-GAP; H=ROWS*STEP-GAP

def rects(cells, ox=0, oy=0, reflect=True, op=0.5):
    p=[f'<rect x="{ox+c*STEP}" y="{oy+r*STEP}" width="{CELL}" height="{CELL}" fill="{col}"/>' for (c,r),col in cells.items()]
    h=H
    if reflect:
        top=oy+H+GAP*2; rh=CELL*0.6
        for (c,r),col in cells.items():
            rr=ROWS-1-r; dx=round(CELL*0.12*(1 if rr%2 else -1),1)
            p.append(f'<rect x="{ox+c*STEP+dx}" y="{top+rr*(rh+GAP):.1f}" width="{CELL}" height="{rh:.1f}" fill="{col}" opacity="{op}"/>')
        h=H+GAP*2+ROWS*(rh+GAP)-GAP
    return "".join(p), h

def mark(cells, reflect=True, label="Mirrormere Labs"):
    body,h=rects(cells, ox=4, reflect=reflect)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W+8}" height="{h:.0f}" viewBox="0 0 {W+8} {h:.0f}" role="img" aria-label="{label}"><title>{label}</title>{body}</svg>'

def icon(cells, bg=NAVY, size=256, radius=48):
    # M without reflection, centred on a rounded navy square
    pad=(size-W)/2; padv=(size-H)/2
    body,_=rects(cells, ox=pad, oy=padv, reflect=False)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" role="img" aria-label="Mirrormere Labs"><title>Mirrormere Labs</title><rect width="{size}" height="{size}" rx="{radius}" fill="{bg}"/>{body}</svg>'

def lockup(cells, text_col, bg=None):
    body,h=rects(cells, ox=0, oy=0, reflect=True)
    tw=620; Wt=W+24+tw; Ht=max(h,H)
    bgr=f'<rect width="{Wt+48}" height="{Ht+48}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wt+48} {Ht+48:.0f}" role="img" aria-label="Mirrormere Labs">'
            f'<title>Mirrormere Labs</title>{bgr}<g transform="translate(24 24)">{body}'
            f'<text x="{W+24}" y="{H*0.78:.0f}" font-family="Public Sans, Helvetica Neue, Arial, sans-serif" font-size="{H*0.62:.0f}" font-weight="700" letter-spacing="-2" fill="{text_col}">Mirrormere Labs</text></g></svg>')

files={
 'logo-mark.svg': mark(withdot),                 # main mark, with the orange pixel
 'logo-mark-small.svg': mark(base),              # for small uses (menu bar), no orange pixel
 'favicon.svg': icon(base, radius=56),
 'logo-lockup-light.svg': lockup(withdot, INK),
 'logo-lockup-dark.svg': lockup(withdot, '#ffffff', bg=NAVY),
}
for n,s in files.items(): open(os.path.join(OUT,n),'w').write(s)
cairosvg.svg2png(bytestring=files['logo-mark.svg'].encode(), write_to=f'{OUT}/logo-mark-1024.png', output_width=1024)
cairosvg.svg2png(bytestring=files['favicon.svg'].encode(), write_to=f'{OUT}/apple-touch-icon.png', output_width=180, output_height=180)
cairosvg.svg2png(bytestring=files['favicon.svg'].encode(), write_to=f'{OUT}/favicon-32.png', output_width=32, output_height=32)
cairosvg.svg2png(bytestring=files['favicon.svg'].encode(), write_to=f'{OUT}/icon-512.png', output_width=512, output_height=512)
cairosvg.svg2png(bytestring=files['logo-lockup-light.svg'].encode(), write_to=f'{OUT}/logo-lockup-light.png', output_width=1600)
cairosvg.svg2png(bytestring=files['logo-lockup-dark.svg'].encode(), write_to=f'{OUT}/logo-lockup-dark.png', output_width=1600)
print(sorted(os.listdir(OUT)))
