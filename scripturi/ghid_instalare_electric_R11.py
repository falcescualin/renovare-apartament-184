# Ghid de instalare electrica R11 (Claude) - PDF + CSV, din tmp/electric_R11/trasee_R11.json
# Rulare cu Python-ul Codex (are reportlab):  ~/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe
from pathlib import Path
import json, math, csv, collections
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, PageBreak,
                                Image, KeepTogether, CondPageBreak)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing, Line, String, Circle, Rect, PolyLine
from PIL import Image as PILImage

R = Path(__file__).resolve().parents[1]; O = R / 'output' / 'pdf'; T11 = R / 'tmp' / 'electric_R11'
D = json.loads((T11 / 'trasee_R11.json').read_text(encoding='utf-8'))
R10 = json.loads((O / 'Apartament_184_Revizie_electrica_R10.json').read_text(encoding='utf-8'))
ARCH = json.loads((R / 'tmp' / 'termic_model.json').read_text(encoding='utf-8'))
FURN = json.loads((R / 'tmp' / 'mobilier_plan_R03.json').read_text(encoding='utf-8'))['items']
for n, f in [('Seg', 'segoeui.ttf'), ('SegB', 'segoeuib.ttf'), ('SegI', 'segoeuii.ttf')]:
    pdfmetrics.registerFont(TTFont(n, 'C:/Windows/Fonts/' + f))
pdfmetrics.registerFontFamily('Seg', normal='Seg', bold='SegB', italic='SegI', boldItalic='SegB')

TUBES = D['tubes']; TB = {t['id']: t for t in TUBES}; P = D['points']; INFO = D['info']; ZF = D['ZF']
DATE = '07.10.2026'

# ---------------- stiluri ----------------
INK = colors.HexColor('#1d2a30'); ACC = colors.HexColor('#0f5c73'); MUTED = colors.HexColor('#5d6f76')
WARN = colors.HexColor('#a23b16'); LIGHTBG = colors.HexColor('#eef4f5'); GRID = colors.HexColor('#c5d3d7')
ST = {
    'h1': ParagraphStyle('h1', fontName='SegB', fontSize=17, leading=21, textColor=ACC, spaceAfter=6),
    'h2': ParagraphStyle('h2', fontName='SegB', fontSize=11.5, leading=15, textColor=INK, spaceBefore=6, spaceAfter=3),
    'b': ParagraphStyle('b', fontName='Seg', fontSize=9, leading=12.4, textColor=INK, spaceAfter=4),
    's': ParagraphStyle('s', fontName='Seg', fontSize=7.6, leading=9.8, textColor=INK),
    'sb': ParagraphStyle('sb', fontName='SegB', fontSize=7.6, leading=9.8, textColor=INK),
    'note': ParagraphStyle('note', fontName='SegI', fontSize=7.8, leading=10.2, textColor=MUTED, spaceAfter=3),
    'warn': ParagraphStyle('warn', fontName='Seg', fontSize=8.8, leading=12, textColor=WARN, spaceAfter=4),
    'cover': ParagraphStyle('cover', fontName='SegB', fontSize=28, leading=33, textColor=ACC),
    'cover2': ParagraphStyle('cover2', fontName='Seg', fontSize=13, leading=18, textColor=INK),
}
story = []
def h1(t): story.append(Paragraph(t, ST['h1']))
def h2(t): story.append(Paragraph(t, ST['h2']))
def p(t, s='b'): story.append(Paragraph(t, ST[s]))
def br(): story.append(PageBreak())
def table(head, rows, widths, fs='s', zebra=True, keep=False):
    data = [[Paragraph(str(h), ST['sb']) for h in head]] + [[Paragraph(str(c), ST[fs]) for c in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    sty = [('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d9e8ec')), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
           ('GRID', (0, 0), (-1, -1), .3, GRID), ('TOPPADDING', (0, 0), (-1, -1), 2.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
           ('LEFTPADDING', (0, 0), (-1, -1), 3.5), ('RIGHTPADDING', (0, 0), (-1, -1), 3.5)]
    if zebra:
        for i in range(2, len(data), 2): sty.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f6f9fa')))
    t.setStyle(TableStyle(sty)); story.append(t); story.append(Spacer(1, 5))
def box(text, color=LIGHTBG, border=ACC):
    t = Table([[Paragraph(text, ST['b'])]], colWidths=[770])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), color), ('BOX', (0, 0), (-1, -1), .8, border),
                           ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                           ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    story.append(t); story.append(Spacer(1, 6))
def img(path, w, hmax=None):
    im = PILImage.open(path); iw, ih = im.size; h = w * ih / iw
    if hmax and h > hmax: w = w * hmax / h; h = hmax
    story.append(Image(str(path), width=w, height=h))

# ---------------- calcule ----------------
RHO = 0.0225
CIRC = {  # cod: (descriere, protectie, sectiune, putere ipoteza kW)
    'C01': ('Iluminat dormitor, sufragerie, balcon + aplice TV sufragerie', 'RCBO B10 30 mA tip A (AFDD recomandat: dormitor)', 1.5, 0.40),
    'C02': ('Iluminat hol, bucătărie (+ LED sub corpuri), debara (+ LED rafturi)', 'RCBO B10 30 mA tip A', 1.5, 0.30),
    'C03': ('Iluminat vestibul, baie + ventilator baie', 'RCBO B10 30 mA tip A', 1.5, 0.15),
    'C04': ('Prize dormitor + sursă LED oglindă/TV dormitor (F03)', 'RCBO B16 30 mA tip A (AFDD recomandat)', 2.5, 1.50),
    'C05': ('Prize sufragerie, birou, TV, fier de călcat + surse LED dressing/TV (F01, F02)', 'RCBO B16 30 mA tip A', 2.5, 2.50),
    'C06': ('Prize baie (IP44)', 'RCBO B16 30 mA tip A', 2.5, 2.00),
    'C07': ('Mașină de spălat rufe Heinner (1,65 kW)', 'RCBO B16 30 mA tip A', 2.5, 1.65),
    'C08': ('Mașină de spălat vase + aprindere plită gaz', 'RCBO B16 30 mA tip A', 2.5, 2.00),
    'C09': ('Cuptor Arctic ARSE11130XD (2,4 kW)', 'RCBO B16 30 mA tip A', 2.5, 2.40),
    'C10': ('Priză masă bucătărie + priză sub chiuvetă', 'RCBO B16 30 mA tip A', 2.5, 2.00),
    'C11': ('Frigider', 'RCBO B16 30 mA tip A', 2.5, 0.30),
    'C12': ('Router / ONT (4 prize) + sursă LED dulap hol (F04)', 'RCBO B16 30 mA tip A', 2.5, 0.20),
    'C13': ('Microunde', 'RCBO B16 30 mA tip A', 2.5, 1.50),
    'C14': ('Contrablat (fierbător etc.) + hotă', 'RCBO B16 30 mA tip A', 2.5, 2.40),
    'C15': ('Aer condiționat dormitor 9.000 BTU (unitatea interioară; exterioara se alimentează prin cablul de legătură)', 'RCBO B16 30 mA tip A', 2.5, 1.20),
}
def bends(t):
    pts = t['points']
    if t['src'] == 'TE':   # tragerea incepe de la baza casetei coloanei (canal cu capac in caseta)
        k = next((i for i, q in enumerate(pts) if q[2] == ZF), 0); pts = pts[k:]
    if t['dst'] == 'TE':
        k = max((i for i, q in enumerate(pts) if q[2] == ZF), default=len(pts) - 1); pts = pts[:k + 1]
    segs = [(b[0] - a[0], b[1] - a[1], b[2] - a[2], math.dist(a, b)) for a, b in zip(pts, pts[1:]) if math.dist(a, b) > .5]
    n = 0; i = 0
    while i < len(segs) - 1:
        a, b = segs[i], segs[i + 1]
        if b[3] < 70 and i + 2 < len(segs):       # decalaj de banda (jog scurt) = curba larga, nu se numara
            i += 2; continue
        cos = (a[0] * b[0] + a[1] * b[1] + a[2] * b[2]) / (a[3] * b[3])
        if cos < .9: n += 1
        i += 1
    return n
for t in TUBES:
    t['b90'] = bends(t)
    t['ceiling'] = t['id'].startswith('TV_')
    t['local'] = 'local' in (t['note'] or '')
    t['floor_m'] = round(sum(math.dist(a, b) for a, b in zip(t['points'], t['points'][1:]) if a[2] == b[2] == ZF) / 1000, 2)
    if t['net'] == 'W': t['pull'] = 'după pozare, fir de nylon + lubrifiant; raza ≥ 8× diam. cablu'
    elif t['b90'] <= 4: t['pull'] = 'după pozare (sârmă de tragere)'
    else: t['pull'] = 'fire introduse în tub ÎNAINTE de pozare'

COLORS = {  # roluri -> culoare izolatie
    'L': 'maro', 'N': 'albastru', 'PE': 'verde-galben', 'R': 'negru', 'A': 'negru (inel A)', 'B': 'gri (inel B)', 'LT': 'gri'}
def wire_colors(t):
    r = t['roles']
    if t['section'] is None: return r
    if t['kind'] == 'V': return '2 × 1 mm² (cablu SELV roșu/negru)'
    if r.startswith('L, N, PE'): return 'L maro · N albastru · PE verde-galben'
    if r.startswith('naveta'): return 'naveta A negru · naveta B gri · retur L01 maro cu inel R · N albastru · PE verde-galben'
    if r.startswith('L permanent'): return 'L maro · N albastru · PE verde-galben · LT (retur ventilator) gri'
    if r.startswith('retur'): return 'retur negru · N albastru · PE verde-galben'
    return r
def ends_reserve(t):
    a = 0.7 if t['src'] == 'TE' else 0.3; b = 0.7 if t['dst'] == 'TE' else 0.3
    return a + b
# circuit graphs -> distanta de la TE
def circuit_dist(c):
    adj = collections.defaultdict(list)
    for t in TUBES:
        if t['circuit'] == c: adj[t['src']].append((t['dst'], t['length_m'])); adj[t['dst']].append((t['src'], t['length_m']))
    dist = {'TE': 0}; todo = ['TE']
    while todo:
        u = todo.pop()
        for v, L in adj[u]:
            if v not in dist: dist[v] = dist[u] + L; todo.append(v)
    return dist
CROWS = []; CSTAT = {}
for c, (desc, prot, sec, kw) in CIRC.items():
    dist = circuit_dist(c); far = max((k for k in dist if k != 'TE'), key=lambda k: dist[k])
    I = 16 if sec == 2.5 else 10; du = 2 * RHO * dist[far] * I / sec; pct = 100 * du / 230
    legs = sum(1 for t in TUBES if t['circuit'] == c and t['src'] == 'TE')
    tubes = [t for t in TUBES if t['circuit'] == c]
    wm = sum(t['wires'] * (t['length_m'] + ends_reserve(t)) for t in tubes)
    lim = 3 if sec == 1.5 else 5
    CSTAT[c] = dict(far=far, L=dist[far], du=du, pct=pct, legs=legs, n=len(tubes), wm=wm)
    CROWS.append([c, desc, prot, f'3 × {sec:.1f} mm² Cu'.replace('.', ','), legs, len(tubes), f'{far} · {dist[far]:.1f} m',
                  f"{pct:.1f} % — {'OK' if pct <= lim else 'DEPĂȘIT'} (lim. {lim} %)", f'{kw:.2f}'.replace('.', ',')])

# zone de incrucisare (cluster 400 mm)
cr = D['crossings']; zones = []
for c in cr:
    for z in zones:
        if any(math.dist(c['xy'], q['xy']) < 400 for q in z): z.append(c); break
    else: zones.append([c])
def room_of(x, y):
    for r in ARCH['rooms']:
        poly = r['polygon']; inside = False
        for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
            if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: inside = not inside
        if inside: return r['name'].replace('Pardoseala_', '').replace('CameraDeZi', 'Sufragerie').replace('Nisa', 'Debara')
    return '—'
ZROWS = []
for i, z in enumerate(zones):
    xs = [c['xy'][0] for c in z]; ys = [c['xy'][1] for c in z]
    ids = sorted({c['a'] for c in z} | {c['b'] for c in z})
    mixed = any(c['mixed'] for c in z)
    ZROWS.append([f'X{i+1}', room_of(sum(xs) / len(xs), sum(ys) / len(ys)), f'X {min(xs):.0f}–{max(xs):.0f} / Y {min(ys):.0f}–{max(ys):.0f}',
                  len(z), 'forță × date' if mixed else 'forță × forță', ', '.join(ids)])
    for c in z: c['zone'] = f'X{i+1}'

# tronsoane
NAMES = {
 'R0-A1': 'Hol: baza casetei coloanei → culoarul holului', 'A1-H_K': 'Hol: culoar principal până în dreptul ușii bucătăriei',
 'H_K-Z_D': 'Hol: culoar → ușa sufrageriei (sub prag) → sufragerie', 'H_K-K_D': 'Hol → bucătărie (sub pragul ușii)',
 'H_K-H_KS': 'Hol: ramura spre dulapul de hol', 'H_KS-H_KW': 'Hol: sub dulapul de hol (router, LED dulap)',
 'K_D-K_W': 'Bucătărie: de la ușă spre peretele cu corpuri', 'K_W-K_WN': 'Bucătărie: sub corpurile de jos, de-a lungul peretelui vest',
 'K_D-K_E': 'Bucătărie: de la ușă spre frigider', 'K_E-K_EN': 'Bucătărie: perete est, frigider', 'K_EN-K_EN2': 'Bucătărie: perete est, masă',
 'Z_D-Z_W': 'Sufragerie: culoar de-a lungul dressingului', 'Z_D-Z_EN': 'Sufragerie: perete est (canapea)',
 'Z_EN-Z_NW': 'Sufragerie: perete fereastră → întrerupător balcon', 'Z_W-Z_N': 'Sufragerie: perete TV / birou',
 'Z_W-V_E': 'Ușa sufragerie → vestibul (sub prag)', 'V_E-V_S': 'Vestibul → mașina de spălat', 'V_E-V_W': 'Vestibul: spre ușa băii',
 'V_W-V_N': 'Vestibul: întrerupător baie', 'V_W-V_B': 'Vestibul: în fața ușii băii', 'V_B-B_D': 'Ușa băii (sub prag)',
 'B_D-B_S': 'Baie: spre prize lavoar', 'B_S-B_W': 'Baie: spre ventilator (lângă cadă)', 'V_E-DM_E': 'Vestibul → dormitor (sub prag)',
 'DM_E-DM_C': 'Dormitor: intrare → nod central', 'DM_C-DM_W': 'Dormitor: în fața dulapului, spre peretele patului',
 'DM_W-DM_WN': 'Dormitor: perete pat (noptieră, cap-scară)', 'DM_C-DM_N': 'Dormitor: perete TV / masă machiaj',
 'NET0-NU': 'Date: cutia NET → hol', 'NU-NE': 'Date: hol, spre coloana slabă de lângă ușă', 'NE-WR': 'Date: coloana slabă (lângă ușă)',
 'NU-ND2': 'Date: hol → ușa sufrageriei', 'ND2-ZD': 'Date: sub pragul ușii sufrageriei', 'ZD-ZDW': 'Date: sufragerie, spre peretele TV',
 'ZDW-ZDN': 'Date: perete TV / birou', 'ZDW-VD': 'Date: sufragerie → vestibul (sub prag)', 'VD-DMD': 'Date: vestibul → dormitor → TV dormitor',
}
NX = D['corridor_nodes']
TROWS = []
for k, ids in D['corridors'].items():
    if k not in NAMES: continue
    a, b = k.split('-'); L = math.dist(NX[a], NX[b]) / 1000
    pw = [i for i in ids if TB[i]['net'] == 'P']; wk = [i for i in ids if TB[i]['net'] == 'W']
    width = sum(TB[i]['d'] + 10 for i in ids) - 10
    TROWS.append([NAMES[k], f'{L:.2f}', len(pw), len(wk), len(ids), f'{width} mm',
                  ', '.join(pw) + (' | date: ' + ', '.join(wk) if wk else '')])

# ---------------- desen plan ----------------
CCOL = {'C01': '#e6a100', 'C02': '#d07000', 'C03': '#b05000', 'C04': '#1f77b4', 'C05': '#2ca02c', 'C06': '#17becf', 'C07': '#9467bd',
        'C08': '#8c564b', 'C09': '#d62728', 'C10': '#e377c2', 'C11': '#7f7f7f', 'C12': '#bcbd22', 'C13': '#ff7f0e', 'C14': '#393b79'}
def tcol(t): return colors.HexColor('#7b2cbf' if t['net'] == 'W' else CCOL.get(t['circuit'], '#000000'))
def clip(a, b, box):
    # Liang-Barsky in plan; intoarce segmentul decupat sau None
    x0, y0, x1, y1 = box; ax, ay = a[0], a[1]; dx, dy = b[0] - ax, b[1] - ay; t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, ax - x0), (dx, x1 - ax), (-dy, ay - y0), (dy, y1 - ay)):
        if pp == 0:
            if qq < 0: return None
        else:
            r = qq / pp
            if pp < 0: t0 = max(t0, r)
            else: t1 = min(t1, r)
    if t0 > t1: return None
    return (ax + t0 * dx, ay + t0 * dy), (ax + t1 * dx, ay + t1 * dy)
def plan(box, W, H, labels=True, tube_ids=False, furniture=True, ceiling=True, only=None):
    x0, y0, x1, y1 = box; s = min(W / (x1 - x0), H / (y1 - y0))
    dr = Drawing(W, H); ox = (W - (x1 - x0) * s) / 2; oy = (H - (y1 - y0) * s) / 2
    def xy(q): return ox + (q[0] - x0) * s, oy + (q[1] - y0) * s
    def inbox(q, m=0): return x0 - m <= q[0] <= x1 + m and y0 - m <= q[1] <= y1 + m
    if furniture:
        for f in FURN:
            for poly in f.get('polys') or [f['poly']]:
                for a, b in zip(poly, poly[1:] + poly[:1]):
                    cl = clip(a, b, box)
                    if cl: dr.add(Line(*xy(cl[0]), *xy(cl[1]), strokeColor=colors.HexColor('#c9cfd1'), strokeWidth=.4, strokeDashArray=[2, 2]))
    for e in ARCH['wall_edges']:
        cl = clip(e[0], e[1], box) if len(e) == 2 else None
        if cl: dr.add(Line(*xy(cl[0]), *xy(cl[1]), strokeColor=INK, strokeWidth=1.1))
    sel = [t for t in TUBES if (only is None or t['id'] in only)]
    for t in sel:
        c = tcol(t); pts = t['points']
        for a, b in zip(pts, pts[1:]):
            cl = clip(a, b, box)
            if not cl: continue
            if a[2] == b[2] == ZF:
                dr.add(Line(*xy(cl[0]), *xy(cl[1]), strokeColor=c, strokeWidth=max(.6, t['d'] * s * .9)))
            elif ceiling and a[2] > 2450 and b[2] > 2450:
                dr.add(Line(*xy(cl[0]), *xy(cl[1]), strokeColor=c, strokeWidth=1.1, strokeDashArray=[4, 2.5]))
    for c in cr:
        if inbox(c['xy']) and (only is None or c['a'] in only or c['b'] in only):
            x, y = xy(c['xy']); dr.add(Circle(x, y, 3.2, fillColor=None, strokeColor=colors.red, strokeWidth=.8))
    if labels:
        taken = []
        for k, q in sorted(P.items()):
            if k in ('TE',) or not inbox(q): continue
            if not any(t['src'] == k or t['dst'] == k for t in TUBES): continue
            x, y = xy(q); col = colors.HexColor('#7b2cbf') if k.startswith('W') or k == 'NET' else INK
            dr.add(Rect(x - 2, y - 2, 4, 4, fillColor=colors.white, strokeColor=col, strokeWidth=.6))
            lx, ly = x + 3.5, y + 2.5; wdt = pdfmetrics.stringWidth(k, 'SegB', 6.4) + 2
            while any(not (lx + wdt < a or lx > b_ or ly + 7 < c_ or ly > d_) for a, b_, c_, d_ in taken): ly += 7.2
            taken.append((lx, lx + wdt, ly - 1, ly + 7))
            dr.add(Rect(lx - 1, ly - 1.2, wdt, 7.6, fillColor=colors.Color(1, 1, 1, .85), strokeColor=None))
            dr.add(String(lx, ly, k, fontName='SegB', fontSize=6.4, fillColor=col))
    if tube_ids:
        for t in sel:
            fl = [q for q in t['points'] if q[2] == ZF]
            if len(fl) < 2: continue
            segs = sorted(zip(fl, fl[1:]), key=lambda ab: -math.dist(ab[0], ab[1]))
            a, b = segs[0]; m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            if not inbox(m): continue
            x, y = xy(m); dr.add(String(x + 2, y + 1.5, t['id'], fontName='Seg', fontSize=5.2, fillColor=tcol(t)))
    if inbox(D['TE']):
        te = xy(D['TE']); dr.add(Rect(te[0] - 4, te[1] - 6, 8, 12, fillColor=colors.HexColor('#333a3d'), strokeColor=None))
        dr.add(String(te[0] + 6, te[1] - 3, 'TE', fontName='SegB', fontSize=7))
    dr.add(Rect(ox, oy, (x1 - x0) * s, (y1 - y0) * s, fillColor=None, strokeColor=GRID, strokeWidth=.5))
    # scara grafica 1 m
    dr.add(Line(8, 8, 8 + 1000 * s, 8, strokeColor=INK, strokeWidth=1.2)); dr.add(String(8, 11, '1 m', fontName='Seg', fontSize=6.5))
    return dr
def legend():
    cells = []
    for c, col in CCOL.items():
        cells.append(Paragraph(f'<font color="{col}">■■■</font> {c}', ST['s']))
    cells.append(Paragraph('<font color="#7b2cbf">■■■</font> date/TV', ST['s']))
    cells.append(Paragraph('<font color="#d07000">– – –</font> tavan (șanț)', ST['s']))
    cells.append(Paragraph('<font color="#ff0000">○</font> încrucișare', ST['s']))
    rows = [cells[i:i + 9] for i in range(0, len(cells), 9)]
    for r in rows: r += [''] * (9 - len(r))
    t = Table(rows, colWidths=[85] * 9, hAlign='LEFT'); t.setStyle(TableStyle([('TOPPADDING', (0, 0), (-1, -1), 1), ('BOTTOMPADDING', (0, 0), (-1, -1), 1)]))
    story.append(t)

# ---------------- continut ----------------
n_te = sum(1 for t in TUBES if t['src'] == 'TE' and t['net'] == 'P')
cop = collections.defaultdict(float)
for t in TUBES: cop[t['d']] += t['length_m']
wire = collections.defaultdict(float)   # (sectiune, culoare) -> m
for t in TUBES:
    if t['section'] is None or t['kind'] == 'V': continue
    L = t['length_m'] + ends_reserve(t); r = t['roles']
    roles = [x.strip() for x in r.split(',')]
    for ro in roles:
        if ro.startswith('L'): col = 'maro' if not ro.startswith('LT') else 'gri'
        elif ro.startswith('N'): col = 'albastru'
        elif ro.startswith('PE'): col = 'verde-galben'
        elif ro.startswith('naveta B'): col = 'gri'
        elif ro.startswith('retur L01'): col = 'maro'
        else: col = 'negru'
        if ro.startswith('retur LT') or 'LT' in ro: col = 'gri'
        wire[(t['section'], col)] += L
cat6 = sum((t['length_m'] + 2.0) * (1 if t['id'] != 'W0' else 0) for t in TUBES if t['id'] in ('W1', 'W2', 'W3', 'W4'))
coax = sum(t['length_m'] + 2.0 for t in TUBES if t['id'] in ('W1', 'W2', 'W3'))

# 1. coperta
story.append(Spacer(1, 40))
story.append(Paragraph('Instalația electrică prin pardoseală — ghid de execuție pas cu pas', ST['cover']))
story.append(Spacer(1, 10))
story.append(Paragraph(f'Apartament 184, Bloc L14 · revizia <b>R11</b> · {DATE}', ST['cover2']))
story.append(Paragraph('Copex prin șapă, coborâri prin pereți, iluminat din întrerupător pe tavan · curenți tari și slabi', ST['cover2']))
story.append(Spacer(1, 18))
kp = [['Plecări 230 V din tablou', n_te], ['Tuburi copex (total)', len(TUBES)],
      ['Copex Ø16 / Ø20 / Ø25 (axă, fără pierderi)', f"{cop[16]:.0f} m / {cop[20]:.0f} m / {cop[25]:.0f} m"],
      ['Circuite', '15 (C01–C15, inclusiv aer condiționat dormitor), fiecare cu RCBO 30 mA'], ['Încrucișări în șapă', f'{len(cr)} perechi de tuburi în {len(zones)} zone; 0 în mănunchiurile principale'],
      ['Model 3D', 'montaj_electric_R11_copex.FCStd (FreeCAD)']]
t = Table([[Paragraph(a, ST['b']), Paragraph(f'<b>{b}</b>', ST['b'])] for a, b in kp], colWidths=[300, 400], hAlign='LEFT')
t.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, -1), .3, GRID), ('TOPPADDING', (0, 0), (-1, -1), 4)])); story.append(t)
story.append(Spacer(1, 18))
box('<b>Statut:</b> proiect de coordonare pentru execuție. Instalația se execută, se verifică și se pune sub tensiune numai de un '
    '<b>electrician autorizat ANRE</b>, care confirmă dimensionarea, cotele măsurate pe șantier și buletinele de verificare (PRAM). '
    'Cotele X/Y/Z sunt ale modelului CAD (mm); înainte de trasare se verifică pe șantier. Ce trebuie măsurat întâi este în capitolul 3.',
    colors.HexColor('#fff4ec'), WARN)
br()

# 2. verificare R10
h1('1. Ce am verificat în planul ChatGPT (R10) și ce am corectat')
p('R10 avea logica de circuite bună: circuite separate pentru receptoarele mari, protecție diferențială pe fiecare circuit, tub separat pentru date, '
  'doze accesibile, fără înnădiri în șapă. Le-am păstrat. Geometria traseelor însă nu se putea executa așa cum era desenată:')
R10T = R10['tubes']
c04 = sum(t['length_m'] for t in R10T if t['circuit'] == 'C04' and t['kind'] == 'P')
c05 = sum(t['length_m'] for t in R10T if t['circuit'] == 'C05' and t['kind'] == 'P')
table(['#', 'Constatare în R10', 'Gravitate', 'Ce face R11'], [
    [1, '17 tuburi coboară vertical din tablou <b>prin mijlocul golului ușii de intrare</b> (X 9956, Y −4330), de la 2,25 m la pardoseală — prin foaia ușii.', 'blocant',
     'Tuburile ies din tablou într-o cornișă de gips-carton peste toc și coboară într-o <b>casetă de gips-carton</b> pe peretele nordic al holului, lângă colț. Niciun tub în golul ușii.'],
    [2, '<b>18 tuburi trec sub pragul ușii de intrare</b>.', 'blocant', 'Niciun tub sub prag; distanța minimă față de prag este de peste 150 mm (verificat automat).'],
    [3, 'Până la <b>21 de tuburi desenate pe aceeași axă</b> (unul peste altul), cu încrucișări nerezolvate în hol.', 'mare',
     'Fiecare tub are banda lui, la 30 mm interax (10 mm între tuburi). Ordinea benzilor urmează ramificațiile, deci mănunchiurile din hol și din uși nu au încrucișări.'],
    [4, 'Tubul spre S03 trece prin peretele plin bucătărie–hol la nivelul pardoselii.', 'mediu', 'S03 se alimentează din culoarul holului, de partea holului.'],
    [5, 'Copex Ø25 pentru 3 × 2,5 mm². Regula de umplere (aria interioară ≥ 3 × aria conductoarelor cu izolație) e îndeplinită deja de Ø20.', 'mediu',
     'Ø20 pentru toate tuburile de forță (cu 5 × 1,5 mm² încă în regulă), Ø16 numai pe tavan (3 fire), Ø25 pentru date. Pardoseala e cu 5 mm mai subțire, iar benzile cu 20 % mai înguste.'],
    [6, f'Lanțurile de prize C04 ({c04:.1f} m) și C05 ({c05:.1f} m): la 16 A în priza cea mai îndepărtată, căderea de tensiune iese ~5,2–5,3 %, peste limita de 5 %.', 'mare',
     'C04, C05 și C10 au câte două plecări din tablou; toate circuitele de prize rămân sub 5 % la 16 A (tabelul din capitolul 4).'],
    [7, 'Aplicele liniare de pe peretele TV din sufragerie și benzile LED din dormitor nu aveau tub propriu și nici comandă.', 'mare',
     'S02 devine întrerupător dublu: tasta 2 comandă aplicele AP1/AP2, cu tub până în spatele fiecărei aplice. Banda LED a oglinzii are tub SELV 24 V separat (V01).'],
    [8, 'Cutia NET și priza routerului P23 aveau aceeași coordonată; P11/F01 și P02/S09 coborau în același punct.', 'mic', 'Coborările au fost decalate (P23 X 7600, NET X 7350, F01 X 5300, S09 Y −780).'],
    [9, 'Tabloul: 15 circuite + general + SPD (+ AFDD) nu încap în „1 rând, 18 module” din nota inițială.', 'mare', 'Necesar ≥ 24 de module + rezervă → recomandat 2 × 18. Vezi decizia D1.'],
    [11, 'Aerul condiționat din dormitor nu era în plan (nici circuit, nici tub, nici trecere prin fațadă).', 'mare', 'C15 are tub Ø20 propriu din tablou (T15), care urcă în masca de riflaje până la unitate. Conductele ies prin fațadă la 2,05 m, în aceeași mască. Capitolul 10b.'],
    [10, 'Încrucișările dintre forță și date nu erau tratate, iar grosimea șapei nu era cunoscută.', 'mare', 'Zonele de încrucișare sunt numerotate (X1…); se cer o măsurătoare și o regulă de execuție (capitolele 3 și 7).'],
], [22, 300, 50, 398])
p('Iluminatul a fost refăcut după decizia din 07.10: pe jos se aduc faza, nulul și PE la întrerupător; din întrerupător se urcă prin perete și, prin șanț în tavan, se ajunge la lampă. '
  'Dozele de derivație J01–J06 din R10 nu mai sunt necesare. Nulul ajunge în fiecare doză de întrerupător, util pentru întrerupătoare smart.', 'note')
br()

# 3. decizii si masuratori
h1('2. Răspunsul scurt: ce trece prin fiecare tub și ce punem împreună')
table(['Întrebare', 'Răspuns în acest proiect'], [
    ['Fazele, nulul și PE ale aceluiași circuit?', '<b>Mereu împreună, în același tub.</b> Niciodată faza într-un tub și nulul în altul (se induc curenți în tub și apar câmpuri).'],
    ['Două circuite de 230 V în același tub?', '<b>Nu.</b> Un tub = un circuit (sau o legătură dintre două aparate ale aceluiași circuit). I7 ar permite în anumite condiții, dar se încălzesc împreună, un defect afectează două circuite, iar depanarea și protecția diferențială devin mai complicate.'],
    ['Curenți tari și slabi (230 V cu internet/TV)?', '<b>Niciodată în același tub și nici în aceeași doză.</b> Pe porțiunile paralele din șapă: minimum 100 mm între ele (în R11 sunt 150 mm sau mai mult). Încrucișare numai la 90°, cu tubul de date trecut peste sau sub, nu pe lângă. Dozele de date sunt separate de cele de prize, chiar dacă stau în aceeași ramă.'],
    ['24 V LED (SELV) cu 230 V?', 'Tub separat (V01). Firele de 24 V nu intră în doza de 230 V. Sursa LED stă într-un loc accesibil.'],
    ['Cablu de date înnădit?', '<b>Nu.</b> Cat6 și coaxialul sunt continue de la cutia NET până la priză. În tubul de Ø25 merg 1 Cat6 + 1 coaxial (ambele curenți slabi).'],
    ['Doze sau înnădiri îngropate în șapă?', '<b>Nu.</b> Toate legăturile sunt în doze accesibile: doze de aparat (prize, întrerupătoare), tablou, cutia NET.'],
    ['Câte fire în fiecare tub?', '3 (L, N, PE) la prize și receptoare; 3 pe jos până la întrerupător (L, N, PE); 3 pe tavan, de la întrerupător la lampă (retur, N, PE); 4 la ventilator; 5 între capetele de cap-scară. Detaliile, tub cu tub, sunt în registrul din capitolul 8.'],
], [190, 580])
h1('3. Înainte de primul șanț: decizii și măsurători obligatorii')
table(['Cod', 'Ce', 'De ce contează', 'Cine / când'], [
    ['M1', '<b>Înălțimea disponibilă de la placa de beton la pardoseala finită</b>, în 5–6 puncte (hol, sufragerie, dormitor, bucătărie, vestibul, baie). Cota pardoselii finite e fixată de pragul ușii de intrare și palier, de tocurile ușilor și de baie. Se verifică și planeitatea plăcii.',
     'Tuburile stau direct pe placă și se toarnă șapa peste ele. Pe benzile cu un singur strat (Ø20): <b>șapă ≥ 50 mm</b> (20 mm tub + ≥ 30 mm deasupra). În zonele de încrucișare (2 straturi): <b>≥ 65–70 mm</b>. Din înălțimea disponibilă se scade finisajul (parchet + suport, gresie + adeziv, microciment). Dacă nu ajunge, se elimină încrucișările (D2). <b>Autonivelanta de 5 mm din deviz nu ajunge:</b> e nevoie de șapă cimentoasă, armată cu fibre sau plasă.', 'Beneficiar + electrician + cine toarnă șapa, ziua 1'],
    ['M2', '<b>Ce pereți sunt structurali</b> (beton armat): în special peretele dormitor/sufragerie (150 mm), sufragerie/hol, peretele de la intrare.',
     'În pereții de beton armat nu se taie șlițuri. Pe ei, aparatul se montează în mobilier, în placare de gips-carton sau aparent.', 'Planul blocului / asociație / inginer'],
    ['M3', '<b>Placa de tavan:</b> tip (monolită / prefabricată / cu goluri), grosimea stratului de acoperire a armăturii, detector de armătură pe traseele de tavan.',
     'Șanțurile în tavan sunt în placă de beton armat. Fără acord, nu se taie. Vezi capitolul 9.', 'Inginer structurist'],
    ['M4', '<b>Tuburile existente din placă</b> spre fiecare plafonieră (L01–L08): unde ies, se pot folosi?', 'Un tub existent bun scutește un șanț în tavan.', 'Electrician, ziua 1'],
    ['M5', '<b>Alimentarea apartamentului:</b> puterea aprobată, mono/trifazat, secțiunea coloanei, existența PE, siguranța din firidă.',
     'Scenariul de vârf R10 (cuptor + rufe + vase + fierbător) ≈ 8,9 kW / 38,5 A. Nu se mărește generalul fără verificarea coloanei.', 'Electrician + furnizor'],
    ['D1', '<b>Locul tabloului.</b> Deasupra ușii (decizia actuală) sunt ~400 mm între toc și tavan (de măsurat), iar tabloul cerut are 2 rânduri (≥ 24 module).',
     '<b>Recomandare:</b> tabloul pe peretele nordic al holului, în capul casetei coloanei (aparatele între ~1,5 și 2,0 m). Dispar cornișa peste ușă și ~1 m de tub pe fiecare plecare, iar tabloul e la îndemână.', 'Beneficiar'],
    ['D2', '<b>Cutia NET</b> rămâne în dulapul de hol (R10) sau se mută în zona TV a sufrageriei?', 'Cu NET în sufragerie ar dispărea aproape toate încrucișările forță × date (zonele X) și Wi-Fi-ul ar fi central.', 'Beneficiar, până la trasare'],
    ['D4', '<b>Aer condiționat:</b> unitatea exterioară pe fațadă (x 150–950, consolă) și gaura Ø65 în fațadă la 3–4 cm de colțul camerei.', 'Cere acordul asociației/proprietarilor și verificarea peretelui de fațadă (M2). Fără acord, alternativa e unitatea exterioară pe balcon, cu conducte mai lungi.', 'Beneficiar + administrator'],
    ['D3', '<b>Aplicele AP1/AP2:</b> modelul ales (230 V sau 24 V cu sursă proprie) și ce comandă tasta 2 a lui S02.', 'Dacă sunt pe 24 V, sursa intră în spatele comodei TV și tubul T01e/T01f rămâne pe 230 V doar până la sursă.', 'Beneficiar'],
], [30, 255, 335, 150])
box('<b>Cât pierzi în înălțime?</b> Șapa se toarnă oricum (acum e doar placa), deci tuburile nu adaugă un strat separat. Ele cer doar ca șapa să aibă minimum 50 mm, '
    'iar 65–70 mm în cele câteva zone de încrucișare. Dacă înălțimea disponibilă (M1) e mai mică, reducem încrucișările (D2: NET în sufragerie), ca să nu fie nevoie de o șapă mai groasă peste tot. '
    'Tavanul fals ar fi luat încă 5–8 cm din înălțimea camerei. Cu varianta aleasă (tuburi pe placă + șanț în tavan doar spre lampă), tavanul rămâne la cota actuală.')
br()

# 4. tablou si circuite
h1('4. Tabloul și circuitele')
table(['Circ.', 'Ce alimentează', 'Protecție (preselecție)', 'Conductoare', 'Plecări din TE', 'Tuburi', 'Punct cel mai îndepărtat',
       'ΔU la I nominal', 'kW ipoteză'], CROWS, [30, 210, 120, 70, 45, 38, 95, 92, 45])
p('ΔU = 2·ρ·L·I/S, cu ρ = 0,0225 Ω·mm²/m, I = 16 A la prize și 10 A la iluminat, toată sarcina pusă în punctul cel mai îndepărtat (caz acoperitor). '
  'Nu include coloana din amonte. Limitele I7 pentru consumatori alimentați din rețeaua publică de joasă tensiune: 3 % la iluminat, 5 % la alte receptoare. '
  'Puterile marcate sunt ipoteze de sarcină (cuptor și mașina de rufe, din fișele producătorilor).', 'note')
h2('Componența tabloului (preselecție, de confirmat de electrician)')
table(['Aparat', 'Buc.', 'Module', 'Observații'], [
    ['Separator / întreruptor general 2P (sau 4P la trifazat), dimensionat după bransament', 1, 2, 'Calibrul se alege după puterea aprobată și coloană (M5).'],
    ['Descărcător de supratensiune SPD tip 2', 1, '2–4', 'Recomandat.'],
    ['RCBO 1P+N, 30 mA, tip A — B10 pentru C01–C03, B16 pentru C04–C15', 15, '15–30', 'RCBO compact de 1 modul sau standard de 2 module.'],
    ['AFDD (detector de arc) pentru dormitor (C01, C04)', '0–2', '0–4', 'Recomandat; aparat combinat AFDD + RCBO.'],
    ['Borne de distribuție N / PE, bară PE, piepteni', '—', '—', 'Două plecări pe același circuit (C04, C05, C10) prin bornă de distribuție, nu două fire sub același șurub.'],
    ['<b>Total, cu ~20 % rezervă</b>', '', '<b>≥ 24 → 2 × 18 = 36</b>', 'Tablou aparent cu 2 rânduri, ~450–500 mm lățime. Verificați gabaritul (D1).'],
], [330, 40, 90, 310])
br()

# 5. plan general
h1('5. Plan general al traseelor (pardoseală + tavan)')
story.append(plan((-150, -5800, 11250, 1350), 790, 410, labels=True)); legend()
p('Linie plină = tub în pardoseală, cu lățimea la scară. Linie întreruptă = tub în tavan (șanț), de la întrerupător la lampă. Pătrat = coborâre în perete la un aparat. '
  'Cercurile roșii sunt încrucișări (capitolul 7). Mobilierul apare punctat. Nordul planului este în sus.', 'note')
br()
h1('5b. Model 3D FreeCAD')
img(T11 / 'fc_iso_c.png', 780, 380)
p('montaj_electric_R11_copex.FCStd: fiecare tub e un obiect cu proprietățile Tub, De_la, Pana_la, Circuit, Diametru_copex_mm, Continut, Lungime_axa_m. '
  'Sunt grupate pe circuite (Forta_230V), Curenti_slabi, Doze, Tablou_si_coloana, Incrucisari. Modelul are aceleași coordonate ca apartament_184.FCStd și se poate deschide alături de el.', 'note')
br()

# 6. planuri pe zone
ZONES = [
    ('Hol, coloana tabloului și cutia NET', (7000, -5650, 10250, -3100), ['Hol']),
    ('Bucătărie și debara', (7100, -3650, 10950, -150), ['Bucatarie', 'Debara']),
    ('Sufragerie', (3500, -5650, 7300, 1100), ['Sufragerie', 'Balcon_placa']),
    ('Vestibul și baie', (100, -5650, 3800, -3700), ['Vestibul', 'Baie']),
    ('Dormitor', (100, -3950, 3700, -150), ['Dormitor']),
]
def dev_room(t):
    if t['dst'] in ('TE',): return None
    if t['ceiling'] or t['local']: q = P[t['dst']]
    else:
        fl = [q for q in t['points'] if q[2] == ZF]
        q = fl[-2] if len(fl) >= 2 else P[t['dst']]
    return room_of(q[0], q[1])
def tubes_in(box):
    x0, y0, x1, y1 = box; out = []
    for t in TUBES:
        for q in t['points']:
            if x0 <= q[0] <= x1 and y0 <= q[1] <= y1 and q[2] in (ZF,) or (t['dst'] in P and x0 <= P[t['dst']][0] <= x1 and y0 <= P[t['dst']][1] <= y1):
                out.append(t); break
    return out
for title, bx, rooms in ZONES:
    h1('6. ' + title)
    loc = [t for t in TUBES if dev_room(t) in rooms]
    def fire(t):
        if t['section'] is None: return 'gol (rezervă)' if t['wires'] == 0 else ('1 Cat6 + 1 coax' if t['wires'] == 2 else '1 cablu')
        return f"{t['wires']}×{str(t['section']).replace('.', ',')}"
    rows = [[Paragraph(x, ST['s']) for x in (t['id'], f"{t['src']} → {t['dst']}", t['circuit'], f"Ø{t['d']}", fire(t))] for t in loc]
    tt = Table([[Paragraph(h, ST['sb']) for h in ['Tub', 'De la → la', 'Circ.', 'Ø', 'Fire']]] + rows, colWidths=[44, 74, 32, 28, 62], repeatRows=1)
    tt.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d9e8ec')), ('GRID', (0, 0), (-1, -1), .3, GRID),
                            ('TOPPADDING', (0, 0), (-1, -1), 1.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5), ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    side = Table([[plan(bx, 515, 470, labels=True, tube_ids=True), [Paragraph('Tuburile care ajung la aparatele din această zonă', ST['sb']), Spacer(1, 3), tt]]],
                 colWidths=[525, 245])
    side.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0)]))
    story.append(side)
    br()

# 7. tronsoane, usi, incrucisari
h1('7. Câte tuburi trec pe fiecare traseu')
p('„Traseu” = un culoar din șapă între două ramificații. Lățimea benzii = Σ(Ø + 10 mm) − 10 mm, cu tuburile alăturate în același strat. '
  'Pe benzile mai late de ~200 mm, peste tuburi se pune plasă de armare (sau șapă cu fibre), ca șapa să nu fisureze deasupra lor.', 'note')
TROWS.sort(key=lambda r: -r[4])
table(['Traseu', 'm', 'Forță', 'Date', 'Total', 'Lățime bandă', 'Tuburi'], TROWS, [215, 32, 35, 32, 32, 60, 364])
br()
h1('7b. Treceri prin uși și zone de încrucișare')
table(['Ușă (sub prag)', 'Tuburi', 'Care'], [[k, len(v), ', '.join(v)] for k, v in D['door_use'].items()], [170, 45, 555])
p('Sub prag tuburile stau strict paralele și perpendiculare pe linia ușii, fără curbe. Pragul de aluminiu se fixează cu adeziv sau cu dibluri scurte (≤ 25 mm), '
  'în afara benzii de tuburi. Marcați banda pe perete înainte de montarea tocului.', 'note')
table(['Zonă', 'Încăpere', 'Unde (mm)', 'Perechi', 'Tip', 'Tuburi implicate'], ZROWS, [32, 70, 165, 40, 75, 388])
box('<b>Cum se execută o încrucișare:</b> tubul care continuă drept rămâne în stratul de jos. Tubul care traversează trece peste el la 90°, cu ~30 mm de fixare de o parte și de alta, fără să fie strivit. '
    'Pentru forță × date, tubul de date trece peste (sau pe sub) toate tuburile de forță într-un singur punct. În zona de încrucișare acoperirea totală e de ≥ 65 mm (M1). '
    'Dacă înălțimea M1 nu permite 65–70 mm, zona de încrucișare se elimină prin rerutare sau prin D2. Placa de beton nu se taie.')
br()

# 8. registru tuburi
h1('8. Registrul tuburilor: conținut, culori, lungimi, metoda de tragere')
p('m axă = lungimea tubului din model. Copexul se cumpără cu +10 %. Firele se taie la lungimea tubului + 0,3 m la fiecare doză și + 0,7 m la tablou. '
  'Cota axei din model (−40 mm) e convențională: pe șantier tuburile stau direct pe placă. „Curbe” = curbe de 90° între punctele de tragere: pentru plecările din TE se numără de la baza casetei, unde tuburile se termină într-un canal cu capac.', 'note')
rows = []
for t in TUBES:
    cont = (f"{t['wires']} × {str(t['section']).replace('.', ',')} mm² — " if t['section'] and t['kind'] != 'V' else '') + wire_colors(t)
    where = 'tavan' if t['ceiling'] else ('local' if t['local'] else 'pardoseală')
    rows.append([t['id'], f"{t['src']} → {t['dst']}", t['circuit'], f"Ø{t['d']}", cont, where,
                 f"{t['length_m']:.2f}".replace('.', ','), f"{t['length_m'] * 1.1:.1f}".replace('.', ','), t['b90'], t['pull']])
table(['Tub', 'De la → la', 'Circ.', 'Ø', 'Conținut / culori', 'Unde', 'm axă', 'm de cumpărat', 'Curbe', 'Tragere'], rows,
      [40, 70, 38, 26, 250, 50, 34, 42, 30, 190])
br()

# 9. tavan
h1('9. Tavan: de la întrerupător la lampă')
box('<b>Atenție, structură:</b> tavanul este placa de beton armat a blocului. Un șanț în placă poate fi considerat intervenție asupra structurii de rezistență. '
    'Se execută <b>numai după avizul scris al unui inginer structurist</b> (M3), cu detector de armătură înainte de fiecare tăiere. Șanț de maximum ~25 mm, tăiat cu freză cu două discuri și aspirator (fără picamer). '
    '<b>Nu se taie armătura.</b> Se ocolesc grinzile și rosturile dintre plăcile prefabricate. Unde există tub vechi utilizabil în placă (M4), se folosește acela.',
    colors.HexColor('#fff4ec'), WARN)
rows = []
for t in TUBES:
    if not t['ceiling']: continue
    rows.append([t['id'], f"{t['src']} → {t['dst']}", t['circuit'], 'Ø16', wire_colors(t), f"{t['length_m']:.2f}".replace('.', ','), t['note'].split(';')[0]])
table(['Tub', 'De la → la', 'Circ.', 'Ø', 'Fire', 'm', 'Traseu'], rows, [50, 75, 38, 30, 190, 35, 352])
p('Traseul pe tavan e drept și paralel cu pereții: întâi perpendicular pe peretele întrerupătorului, apoi o singură curbă spre rozetă. Fără diagonale. '
  'Copex Ø16 intră doar cu 3 conductoare de 1,5 mm² (aria interioară ≥ 3 × aria firelor). Urcarea din întrerupător în perete se face într-un șlițuri vertical, în același tub. '
  'La rozetă, tubul se termină într-o doză de tavan sau sub baza lămpii, cu 15 cm de fir liber.', 'note')
br()

# 10. legaturi in doze
h1('10. Legăturile în dozele întrerupătoarelor (fără doze J)')
p('Doză de aparat adâncă (60–65 mm) la fiecare întrerupător: aici se fac legăturile de N și PE spre lampă, cu cleme cu pârghie (tip Wago 221) potrivite pentru 1,5 mm².', 'b')
table(['Întrerupător', 'Intră pe jos (din TE)', 'Iese spre tavan / alt aparat', 'Ce se leagă în doză'], [
    ['S02 dublu (sufragerie)', 'T01: L, N, PE', 'TV_L02: retur L02, N, PE · T01e (pe jos) spre AP2 → AP1: retur aplice, N, PE',
     'L → borna comună a ambelor taste; tasta 1 → retur L02; tasta 2 → retur aplice; N: intrare + tavan + aplice (clemă 3); PE la fel.'],
    ['S06 (balcon)', 'T01b: L, N, PE', 'TV_L06: retur L06, N, PE (prin peretele fațadei)', 'L → comun; ieșire → retur L06; N și PE: clemă 2 sau 3.'],
    ['S01 cap-scară (ușa dormitorului)', 'T01c: L, N, PE', 'T01d spre S09: navete A, B, retur L01, N, PE · TV_L01: retur L01, N, PE',
     'L → comunul S01; A și B → navetele S01; returul L01 care vine de la comunul S09 → clemă cu retur TV_L01; N și PE: clemă 3.'],
    ['S09 cap-scară (pat)', 'T01d: A, B, retur L01, N, PE', '—', 'A, B → navete; comunul S09 → retur L01; N izolat (rezervă smart); PE la carcasă/rezervă.'],
    ['S04 (hol, în casetă)', 'T02: L, N, PE (local)', 'TV_L04: retur L04, N, PE', 'L → comun; ieșire → retur L04.'],
    ['S03 dublu (bucătărie, în hol)', 'T02b: L, N, PE', 'TV_L03: retur L03, N, PE · TV_F06: retur F06, N, PE', 'tasta 1 → L03; tasta 2 → sursa LED sub corpuri F06; N, PE: clemă 3.'],
    ['S05 (debara)', 'T02c: L, N, PE', 'TV_L05: retur, N, PE → continuă în TV_F05 la sursa LED', 'Plafoniera și LED-ul rafturilor pe aceeași tastă (ca în R10).'],
    ['S07 (vestibul, din sufragerie)', 'T03: L, N, PE', 'TV_L07: retur L07, N, PE', 'L → comun; ieșire → L07.'],
    ['S08 dublu (baie)', 'T03b: L, N, PE', 'TV_L08: retur L08, N, PE · T03c (pe jos) spre ventilator F07: L, N, PE, LT', 'tasta 1 → L08; tasta 2 → LT ventilator; L permanent la ventilator (temporizare).'],
], [120, 120, 230, 300])
p('PE se leagă la fiecare lampă și aparat de clasa I. La lămpile de clasa II, PE se izolează și se lasă disponibil. '
  'Firele N nefolosite (de exemplu la S09) se izolează cu clemă, nu cu bandă.', 'note')
br()

# 10b. aer conditionat
h1('10b. Aer condiționat în dormitor (9.000 BTU, un singur aparat)')
img(T11 / 'ac_apt_iso_c.png', 520, 330) if (T11 / 'ac_apt_iso_c.png').exists() else None
table(['Element', 'Specificație', 'Observații'], [
    ['Unitate interioară', '9.000 BTU, profil subțire 190 mm, pe peretele vest în colțul de nord, baza la 2,09 m / vârful la 2,34 m', 'Lipită de perete; 16 cm liberi sub tavan. Aerul pleacă spre est, ușor în jos, spre masa de machiaj (~3 m).'],
    ['Mască cu riflaje', 'Bandă de la podea la tavan, 190 × 80 mm, în colț, lipită de fațadă. Interior: conductele + tubul electric. Față: lamele stejar 27×21 mm, pas 40 mm, pe suport închis la culoare, ca la peretele TV.', 'Zona dintre 1,96 și 2,20 m are lamelele demontabile (acces la fitinguri). Unitatea interioară NU se acoperă: gura de aer și grila de aspirație rămân libere.'],
    ['Conducte frigorifice', 'Cupru izolat 1/4" + 3/8" (kit montator), cablu de legătură 4 × 1,5 mm² după fișa producătorului', 'Prin fațadă, într-o gaură Ø65 la x 184 mm / z 2,085 m. Lungime vizibilă: 0.'],
    ['Scurgere condens', 'Țeavă Ø16, în aceeași gaură, cu panta spre exterior (gaura la z 2,045 m, sub baza unității)', 'Panta minimă ~1 cm la metru. Nu se ridică spre tavan.'],
    ['Unitate exterioară', '9.000 BTU, pe consolă de fațadă, la x 150–950, y 80–380, z 1,25–1,80 m', 'Necesită acordul asociației. Gura de evacuare spre exterior, 30 cm liberi în spate.'],
    ['Alimentare 230 V (C15)', 'RCBO B16 30 mA, tub Ø20 T15 din tablou, 3 × 2,5 mm² (L, N, PE), urcă în mască până la 2,20 m', 'Se leagă la unitatea interioară (borne sub capac), nu la o priză comună. Deconectare locală lângă unitatea exterioară, dacă o cere fișa.'],
], [120, 380, 270])
p('<b>Ordinea lucrărilor:</b> tubul electric T15 se montează cu restul copexului din pardoseală; masca se construiește înainte de zugrăveală, iar gaura prin fațadă se face după verificarea peretelui (M2). '
  'Montatorul de AC vine după mască și după aparataj: face vidul, testează cu azot și pune în funcțiune. '
  'Tubul T15 (Ø20) și firele sale sunt în registrul din capitolul 8 și în listele de materiale.', 'note')
br()

# 11. pasi
h1('11. Pașii de execuție')
STEPS = [
    ('E0', 'Pregătire', 'Întrerupeți alimentarea apartamentului de la firidă și verificați lipsa tensiunii. Faceți poze cu instalația veche. Demontați aparatajul vechi. Tablou provizoriu de șantier cu RCD 30 mA.', 'detector de tensiune, multimetru CAT III', 'lipsa tensiunii verificată'),
    ('E1', 'Măsurători', 'M1–M5 din capitolul 3. Notați pe plan înălțimea de la placă la pardoseala finită. Marcați pe pereți zonele structurale.', 'ruletă, nivelă laser, detector armătură', 'grosimea șapei stabilită (≥ 50 / 65–70 mm)'),
    ('E2', 'Trasare', 'Trasați pe pardoseală axa fiecărui culoar (capitolul 7), cu sfoară cu cretă, după cotele X/Y din planuri, măsurate de la colțuri fixe. Marcați pe pereți axa fiecărei coborâri și centrul fiecărei doze (coordonatele din Anexa A). Fotografiați trasarea.', 'sfoară cu cretă, laser cu linii', 'beneficiarul aprobă trasarea'),
    ('E3', 'Șlițuri în pereți', 'Doar în pereții nestructurali: șlițuri verticale de la pardoseală la doză (lățime ~30 mm, adâncime ~30 mm pentru Ø20). Fără șlițuri orizontale lungi, fără șlițuri pe ambele fețe ale aceluiași perete în dreptul aceluiași punct.', 'freză de pereți cu aspirator', 'adâncimea minimă la pereții subțiri'),
    ('E4', 'Pregătirea plăcii', 'Placa se curăță și se aspiră; denivelările mari se corectează. Cota pardoselii finite se marchează pe toți pereții (laser, linie la +1,00 m), iar din ea se scot grosimea finisajului și a șapei. Se coordonează cu instalatorul: țevile de apă, scurgerile din baie și bucătărie și racordurile caloriferelor au culoarele lor. Tuburile electrice le încrucișează numai la 90°, niciodată pe lungime una peste alta. Placa nu se taie.', 'laser cu linii, aspirator', 'cota +1,00 m marcată în toate camerele'),
    ('E5', 'Doze', 'Montați dozele de aparat (Ø68, adâncime 60–65 mm, la întrerupătoare obligatoriu adânci), dozele de date (separate) și doza de tavan sau rozeta. În gips-carton se folosesc doze pentru gips-carton.', 'carotă Ø68, ipsos rapid', 'fața dozei în planul tencuielii finale'),
    ('E6', 'Caseta coloanei + cornișa', 'Structură de profile CW/UW 50 pe peretele nordic al holului, lângă colț (lățime ≈ banda coloanei + 120 mm). Canal PVC cu capac și cu compartiment separat pentru date (W0, W5). Tuburile de copex se termină în canal, la baza casetei: acolo e punctul de tragere. Capac demontabil.', 'profile GC, canal PVC 2 compartimente', 'acces la baza casetei după finisaje'),
    ('E6b', 'Aer condiționat (dormitor)', 'Tubul T15 (Ø20) pe pardoseală, apoi urcarea în mască. Masca: suport + lamele, cavitate 50 mm; gaura Ø65 prin fațadă după verificarea peretelui; conductele și condensul trase prin gaură, cu panta spre exterior. Montatorul AC face vidul, testul cu azot și punerea în funcțiune după aparataj.', 'carotieră Ø65, kit conducte Cu izolate, consolă', 'pantă condens, etanșare gaură, acces la fitinguri'),
    ('E7', 'Pozarea copexului în pardoseală', 'Întâi mănunchiul holului, în ordinea benzilor din model (tubul cel mai apropiat de perete rămâne apropiat de perete), apoi ramurile. Câte un tub pe bandă, la 10 mm unul de altul, prinse de placă la 50–60 cm și la fiecare curbă, cu puncte de mortar rapid sau ipsos (de preferat) sau cu cleme pe dibluri scurte (gaură ≤ 30 mm, fără să atingeți armătura). Curbe largi, fără strivire (rază ≥ ~100 mm la Ø20). Forță și date pe benzi separate, la ≥ 100 mm. Fiecare capăt de tub etichetat (ex. „T05.2 → P08”) și astupat cu dop.', 'copex greu 750 N (EN 61386-22), bride, dibluri', 'nicio încrucișare în afara zonelor X'),
    ('E8', 'Tragerea conductoarelor', 'Pe tuburile marcate „înainte de pozare”, firele se introduc în copex pe pardoseală, înainte de fixare. Pe restul, după pozare, cu sârmă de tragere și lubrifiant. Lungimi: tub + 0,3 m la doze, + 0,7 m la tablou. Culorile din registru. Fiecare fir se etichetează la ambele capete. Cat6: tensiune de tragere ≤ 100 N, rază ≥ 8 × diametru, fără răsucire. Cablurile de date se trag ultimele.', 'sârmă de tragere, lubrifiant, inele de marcare', 'niciun fir zgâriat'),
    ('E9', 'Verificare înainte de șapă (STOP)', 'Continuitatea fiecărui conductor și rezistența de izolație la 500 V c.c. (≥ 1 MΩ) între toate firele, pe fiecare tub. Test Cat6 (wiremap) și coaxial. Fotografii cu ruleta pe fiecare culoar (planul „as-built”). Tuburile se ancorează ca să nu se ridice la turnare.', 'megohmmetru 500 V, tester Cat6', 'proces-verbal semnat, poze'),
    ('E10', 'Turnarea șapei peste tuburi', 'Amorsă sau punte de aderență pe placă (sau folie + bandă perimetrală, dacă șapa e flotantă, cu izolație fonică). Mortar în puncte peste încrucișări și de-a lungul benzilor, ca tuburile să nu se ridice. Plasă de armare peste benzile mai late de ~200 mm (sau fibre în toată șapa). Șapa se toarnă la cota M1, cu ≥ 30 mm peste tuburi. Nu se calcă direct pe tuburi; se pun scânduri. Se respectă timpul de uscare înainte de finisaje.', 'șapă cimentoasă, fibre / plasă sudată, riglă, laser', 'grosimea peste tuburi verificată în mai multe puncte'),
    ('E11', 'Reverificare după șapă', 'Se repetă izolația și continuitatea: tuburile pot fi strivite la turnare. Orice defect se rezolvă acum, nu după gresie sau parchet.', 'megohmmetru', 'proces-verbal'),
    ('E12', 'Tavan (după aviz)', 'Detector de armătură pe traseu, apoi șanț ≤ 25 mm, copex Ø16, ipsos sau tencuială. Retur, N, PE trase din întrerupător.', 'freză cu 2 discuri, detector', 'aviz structural în dosar'),
    ('E13', 'Tablou', 'Montaj aparent la locul ales (D1). Bare N/PE, borne de distribuție pentru plecările duble, etichetarea fiecărui RCBO cu circuitul și încăperile, strângere la cuplul din fișa aparatului. Schema monofilară se lipește pe ușă.', 'șurubelniță dinamometrică', 'etichete și schemă pe ușa tabloului'),
    ('E14', 'Aparataj și punere în funcțiune', 'Prize, întrerupătoare, aplice, lămpi. Măsurătorile din capitolul 12, apoi punerea sub tensiune pe circuite, una câte una.', 'tester instalații', 'buletine PRAM'),
]
table(['Pas', 'Etapă', 'Ce și cum', 'Unelte / materiale', 'Verificare'], [[a, b, c, d, e] for a, b, c, d, e in STEPS], [28, 85, 420, 120, 117])
br()

# 12. masuratori
h1('12. Verificări și recepție')
table(['Verificare', 'Cum', 'Criteriu (orientativ)'], [
    ['Continuitatea conductoarelor de protecție PE', 'Între bara PE din tablou și fiecare priză sau lampă de clasa I', 'valoare mică și stabilă; fără întreruperi'],
    ['Rezistența de izolație', '500 V c.c., L–N, L–PE, N–PE, pe fiecare circuit, cu receptoarele deconectate', '≥ 1 MΩ (HD 60364-6)'],
    ['Polaritatea', 'Faza pe borna corectă la priză; întrerupătorul întrerupe faza', 'corect pe toate punctele'],
    ['Impedanța buclei de defect / Ik', 'La priza cea mai îndepărtată din fiecare circuit', 'deconectare în timpul cerut pentru B10/B16'],
    ['RCBO 30 mA', 'Test cu aparatul: curent și timp de declanșare; apoi butonul T', 'IΔn = 30 mA, timp conform fișei'],
    ['Căderea de tensiune', 'La sarcină, în punctele cele mai îndepărtate (capitolul 4)', '≤ 3 % iluminat / ≤ 5 % prize'],
    ['Funcțional', 'Fiecare tastă, cap-scara, ventilator (LT), aplicele, sursele LED', 'conform capitolului 10'],
    ['Date / TV', 'Wiremap Cat6 pe fiecare priză, test coaxial', 'toate perechile corecte; fără înnădiri'],
    ['Dosar', 'Schema tabloului, planul as-built cu poze, buletine PRAM, avizul structural pentru tavan', 'predat beneficiarului'],
], [210, 330, 230])
br()

# 13. materiale
h1('13. Listă de materiale (cantități din model)')
roll = lambda m: math.ceil(m * 1.1 / 50)
bom = [
    ['Tub copex gofrat greu 750 N, Ø16 (tavan, SELV)', f"{cop[16]:.0f} m", f"{cop[16] * 1.1:.0f} m ≈ {roll(cop[16])} colaci de 50 m"],
    ['Tub copex gofrat greu 750 N, Ø20 (forță)', f"{cop[20]:.0f} m", f"{cop[20] * 1.1:.0f} m ≈ {roll(cop[20])} colaci de 50 m"],
    ['Tub copex gofrat greu 750 N, Ø25 (date, rezervă, operator)', f"{cop[25]:.0f} m", f"{cop[25] * 1.1:.0f} m ≈ {roll(cop[25])} colaci de 50 m"],
]
for (sec, col), m in sorted(wire.items()):
    bom.append([f'Conductor H07V-K {str(sec).replace(".", ",")} mm², {col}', f'{m:.0f} m', f'{math.ceil(m * 1.05 / 10) * 10:.0f} m'])
bom += [
    ['Cablu SELV 2 × 1 mm² (V01, LED 24 V)', f"{TB['V01']['length_m'] + 0.6:.1f} m", '5 m'],
    ['Cablu MYYM 4 × 1,5 mm² (legătură AC interior–exterior, după fișa producătorului)', '4 m', '5 m'],
    ['Kit instalare AC: conducte Cu izolate 1/4"+3/8", consolă exterioară, țeavă condens Ø16 (de la montator)', '1 set', 'în oferta montatorului'],
    ['Cablu Cat6 U/UTP (cupru, nu CCA)', f'{cat6:.0f} m', f'{math.ceil(cat6 * 1.05 / 5) * 5:.0f} m'],
    ['Cablu coaxial RG6, 75 Ω', f'{coax:.0f} m', f'{math.ceil(coax * 1.05 / 5) * 5:.0f} m'],
    ['Doze de aparat Ø68, adâncime 60–65 mm (prize, întrerupătoare, aplice, LED, date)', f"{sum(1 for k in P if k[0] in 'PSFAW' or k == 'M1')} poziții", 'plus casete multiple după rame'],
    ['Doze de tavan / rozete pentru plafoniere', '8', ''],
    ['Cleme cu pârghie 221 (2/3/5 conductoare)', '~150', 'estimat: 2–3 / doză'],
    ['Bride / cleme de fixare copex pe pardoseală, dibluri', f"~{int(sum(t['floor_m'] for t in TUBES) / 0.5)}", 'la 50 cm + la curbe'],
    ['Sârmă sau fir de tragere, lubrifiant pentru tragere', f"{sum(t['length_m'] for t in TUBES):.0f} m", ''],
    ['Inele și etichete de marcare pentru fire și tuburi', f"{len(TUBES) * 2} capete de tub", ''],
    ['Canal PVC cu 2 compartimente + profile CW/UW 50 + placă GC 12,5 + capac de vizitare (caseta coloanei)', '1 set', '~2,5 m înălțime'],
    ['Plasă de armare pentru benzile late (sau șapă cu fibre)', '~4 m²', 'hol, uși, sufragerie'],
    ['Mortar rapid / ipsos pentru fixarea tuburilor pe placă (puncte la 50–60 cm)', '~3–4 saci', ''],
]
table(['Material', 'Din model', 'De cumpărat (cu pierderi)'], bom, [430, 120, 220])
p('Aparatura tabloului, aparatajul (prize, întrerupătoare), lămpile și aplicele nu sunt în această listă; sunt în devizul general. '
  'Pentru firele din tuburile „trase înainte de pozare”, tăiați după măsurarea reală pe șantier, nu după tabel.', 'note')
br()

# Anexa A coordonate
h1('Anexa A. Coordonatele aparatelor (model CAD, mm)')
rows = []
for k in sorted(P):
    if not any(t['src'] == k or t['dst'] == k for t in TUBES): continue
    q = P[k]; dp = D['drops'].get(k)
    rows.append([k, INFO.get(k, ''), q[0], q[1], q[2], room_of(q[0], q[1]), f'coborâre la {dp}' if dp else ''])
half = (len(rows) + 1) // 2
table(['Punct', 'Descriere', 'X', 'Y', 'Z', 'Încăpere', 'Notă'], rows[:half], [38, 300, 50, 50, 40, 70, 222])
br(); h1('Anexa A (continuare)')
table(['Punct', 'Descriere', 'X', 'Y', 'Z', 'Încăpere', 'Notă'], rows[half:], [38, 300, 50, 50, 40, 70, 222])
p('Z = centrul dozei față de pardoseala finită. X/Y = coordonatele modelului: pe șantier se transformă în cote față de colțuri fixe. '
  'Plafonierele (L01–L08) păstrează pozițiile existente; L05 e mutată la mijlocul debaralei (06.10).', 'note')
br()
h1('Anexa B. Surse și note')
p('<link href="https://legislatie.just.ro/Public/DetaliiDocument/286763"><u>Normativ I7/2011</u></link> — instalații electrice cu tensiuni ≤ 1000 V c.a.: pozare în tuburi, umplerea tuburilor, doze, căderi de tensiune.')
p('SR HD 60364-6 — verificări la punerea în funcțiune (izolație 500 V ≥ 1 MΩ, continuitate, RCD). SR EN 61386-22 — tuburi flexibile (clasă de compresiune). '
  'SR EN 50174-2 — separarea cablurilor de date de cele de energie (principiul aplicat: tub separat, ≥ 100 mm pe paralel, încrucișare la 90°).')
p('Puteri: Heinner HWM-HME1014IVA10+++ 1,65 kW (manual), Arctic ARSE11130XD 2,4 kW (fișă), preluate din R10. Celelalte sunt ipoteze de sarcină.')
p('Fișiere: <b>montaj_electric_R11_copex.FCStd</b> (model 3D), <b>output/pdf/Apartament_184_Tuburi_fire_R11.csv</b> (registru), '
  'scripturi/trasee_copex_R11.py (generatorul traseelor), scripturi/freecad_trasee_R11.py, scripturi/ghid_instalare_electric_R11.py. '
  'Fișierele R10 ale lui ChatGPT au rămas neatinse.', 'note')

def deco(c, doc):
    c.saveState(); c.setFont('Seg', 7.5); c.setFillColor(MUTED)
    c.drawString(36, 18, f'Ap. 184 Bloc L14 · Ghid instalație electrică R11 · {DATE} · de validat de electrician autorizat ANRE')
    c.drawRightString(806, 18, str(doc.page)); c.setStrokeColor(GRID); c.line(36, 28, 806, 28); c.restoreState()
import sys
out = O / (sys.argv[1] if len(sys.argv) > 1 else 'Apartament_184_Ghid_instalare_electrica_R11.pdf')
doc = BaseDocTemplate(str(out), pagesize=(842, 595), leftMargin=36, rightMargin=36, topMargin=30, bottomMargin=36,
                      title='Ghid instalație electrică R11 - Ap. 184', author='Claude')
doc.addPageTemplates([PageTemplate(id='p', frames=[Frame(36, 36, 770, 529, id='f')], onPage=deco)])
doc.build(story)
# CSV registru
with (O / 'Apartament_184_Tuburi_fire_R11.csv').open('w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['Tub', 'De la', 'Pana la', 'Circuit', 'Diametru copex mm', 'Nr fire/cabluri', 'Sectiune mm2', 'Continut / culori', 'Unde',
                'Lungime axa m', 'Lungime de cumparat m', 'Curbe 90', 'Tragere', 'Nota', 'Coordonate XYZ mm'])
    for t in TUBES:
        w.writerow([t['id'], t['src'], t['dst'], t['circuit'], t['d'], t['wires'], t['section'], wire_colors(t),
                    'tavan' if t['ceiling'] else ('local' if t['local'] else 'pardoseala'), t['length_m'], round(t['length_m'] * 1.1, 2),
                    t['b90'], t['pull'], t['note'], json.dumps(t['points'])])
print(out, 'pagini', doc.page)
print({k: round(v, 1) for k, v in cop.items()}, {f'{k[0]} {k[1]}': round(v) for k, v in wire.items()}, round(cat6), round(coax))
for c, s in CSTAT.items(): print(c, s['far'], round(s['L'], 1), round(s['pct'], 2), s['legs'])
