# Desen de control (PIL) pentru tmp/electric_R11/trasee_R11.json
from pathlib import Path
import json, sys
from PIL import Image, ImageDraw, ImageFont
R = Path(__file__).resolve().parents[1]
d = json.loads((R / 'tmp/electric_R11/trasee_R11.json').read_text(encoding='utf-8'))
arch = json.loads((R / 'tmp/termic_model.json').read_text(encoding='utf-8'))
box = [float(v) for v in sys.argv[1:5]] if len(sys.argv) > 4 else [-100, -5800, 11200, 1400]
S = float(sys.argv[5]) if len(sys.argv) > 5 else 0.18
W = int((box[2] - box[0]) * S); H = int((box[3] - box[1]) * S)
im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
f = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', max(9, int(S * 60)))
def xy(p): return ((p[0] - box[0]) * S, (box[3] - p[1]) * S)
for e in arch['wall_edges']:
    if len(e) == 2: dr.line([xy(e[0]), xy(e[1])], fill='black', width=2)
col = {'C01': '#e6a100', 'C02': '#d07000', 'C03': '#b05000', 'C04': '#1f77b4', 'C05': '#2ca02c', 'C06': '#17becf', 'C07': '#9467bd',
       'C08': '#8c564b', 'C09': '#d62728', 'C10': '#e377c2', 'C11': '#7f7f7f', 'C12': '#bcbd22', 'C13': '#ff7f0e', 'C14': '#393b79'}
for t in d['tubes']:
    pts = [p for p in t['points']]
    c = '#7b2cbf' if t['net'] == 'W' else col.get(t['circuit'], 'black')
    for a, b in zip(pts, pts[1:]):
        if a[2] < 0 and b[2] < 0: dr.line([xy(a), xy(b)], fill=c, width=max(1, int(t['d'] * S)))
    for p in pts:
        if p[2] < 0: pass
for c in d['crossings']:
    x, y = xy(c['xy']); dr.ellipse([x - 4, y - 4, x + 4, y + 4], outline='red', width=2)
for k, v in d['points'].items():
    if k in ('TE',): continue
    x, y = xy(v); dr.rectangle([x - 3, y - 3, x + 3, y + 3], outline='black'); dr.text((x + 4, y - 12), k, fill='black', font=f)
out = R / 'tmp/electric_R11' / (sys.argv[6] if len(sys.argv) > 6 else 'plan_check.png')
im.save(out); print(out)
