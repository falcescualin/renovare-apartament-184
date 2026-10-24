# Construieste in sesiunea FreeCAD (GUI) documentul montaj_electric_R11_copex din tmp/electric_R11/trasee_R11.json.
# Rulare: exec(open(r'...\scripturi\freecad_trasee_R11.py', encoding='utf-8').read()) din consola FreeCAD / MCP.
# Salvarea se face din GUI (nu headless), ca sa ramana culorile si vizibilitatea.
import json, math, os
import FreeCAD as App, Part
ROOT = r'C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14'
D = json.load(open(os.path.join(ROOT, 'tmp', 'electric_R11', 'trasee_R11.json'), encoding='utf-8'))
ARCH = json.load(open(os.path.join(ROOT, 'tmp', 'termic_model.json'), encoding='utf-8'))
NAME = 'montaj_electric_R11_copex'
if NAME in App.listDocuments(): App.closeDocument(NAME)
doc = App.newDocument(NAME)
V = App.Vector
COL = {'C01': (0.90, 0.63, 0.00), 'C02': (0.82, 0.44, 0.00), 'C03': (0.69, 0.31, 0.00), 'C04': (0.12, 0.47, 0.71),
       'C05': (0.17, 0.63, 0.17), 'C06': (0.09, 0.75, 0.81), 'C07': (0.58, 0.40, 0.74), 'C08': (0.55, 0.34, 0.29),
       'C09': (0.84, 0.15, 0.16), 'C10': (0.89, 0.47, 0.76), 'C11': (0.50, 0.50, 0.50), 'C12': (0.74, 0.74, 0.13),
       'C13': (1.00, 0.50, 0.05), 'C14': (0.22, 0.23, 0.47)}
WEAKC = (0.48, 0.17, 0.75)

def grp(name, parent=None):
    g = doc.addObject('App::DocumentObjectGroup', name)
    if parent: parent.addObject(g)
    return g

def tube_shape(pts, d):
    r = d / 2.0; parts = []
    for a, b in zip(pts, pts[1:]):
        pa, pb = V(*a), V(*b); L = (pb - pa).Length
        if L < 0.5: continue
        parts.append(Part.makeCylinder(r, L, pa, (pb - pa).normalize()))
    for p in pts[1:-1]: parts.append(Part.makeSphere(r, V(*p)))
    return Part.makeCompound(parts)

def color(obj, rgb, transp=0):
    try:
        obj.ViewObject.ShapeColor = rgb; obj.ViewObject.LineColor = rgb; obj.ViewObject.Transparency = transp
    except Exception: pass

def props(obj, **kw):
    for k, v in kw.items():
        obj.addProperty('App::PropertyString', k, 'Electric_R11'); setattr(obj, k, str(v))

g_all = grp('Instalatie_R11')
g_p = grp('Forta_230V', g_all); g_w = grp('Curenti_slabi', g_all); g_box = grp('Doze', g_all)
g_te = grp('Tablou_si_coloana', g_all); g_x = grp('Incrucisari', g_all); g_ctx = grp('Context_pereti', g_all)
circ_groups = {}
for t in D['tubes']:
    if t['net'] == 'P':
        c = t['circuit']
        if c not in circ_groups: circ_groups[c] = grp('Circuit_' + c, g_p)
        g = circ_groups[c]; rgb = COL.get(c, (0, 0, 0))
    else:
        g = g_w; rgb = WEAKC
    o = doc.addObject('Part::Feature', (t['id'] + '_' + t['src'] + '_' + t['dst']).replace('.', '_'))
    o.Shape = tube_shape(t['points'], t['d'])
    o.Label = f"{t['id']} {t['src']}->{t['dst']} {t['circuit']} D{t['d']}"
    props(o, Tub=t['id'], De_la=t['src'], Pana_la=t['dst'], Circuit=t['circuit'], Diametru_copex_mm=t['d'],
          Continut=(f"{t['wires']} x {t['section']} mm2 H07V-K: " if t['section'] else '') + t['roles'],
          Lungime_axa_m=t['length_m'], Nota=t['note'])
    g.addObject(o); color(o, rgb)

# doze de aparataj / derivatie
P = D['points']; INFO = D['info']
used = {t['src'] for t in D['tubes']} | {t['dst'] for t in D['tubes']}
def wall_x(p):
    best = None
    for e in ARCH['wall_edges']:
        if len(e) != 2: continue
        (a, b) = e
        if abs(a[0] - b[0]) < 1 and min(a[1], b[1]) - 5 <= p[1] <= max(a[1], b[1]) + 5:
            d_ = abs(p[0] - a[0]); best = min(best or (1e9, ''), (d_, 'x'))
        elif abs(a[1] - b[1]) < 1 and min(a[0], b[0]) - 5 <= p[0] <= max(a[0], b[0]) + 5:
            d_ = abs(p[1] - a[1]); best = min(best or (1e9, ''), (d_, 'y'))
    return best[1] == 'x'
for k in sorted(used):
    if k in ('TE', 'NET'): continue
    p = P[k]; big = k.startswith('J') or k.startswith('W')
    s = 100 if big else 70; dp = 50 if big else 45
    dx, dy = (dp, s) if wall_x(p) else (s, dp)
    b = doc.addObject('Part::Box', 'Doza_' + k)
    b.Length, b.Width, b.Height = dx, dy, s
    b.Placement.Base = V(p[0] - dx / 2, p[1] - dy / 2, p[2] - s / 2)
    b.Label = f"{k} - {INFO.get(k, '')}"
    props(b, Punct=k, Descriere=INFO.get(k, ''), Centru_mm=p)
    g_box.addObject(b)
    color(b, (0.95, 0.95, 0.95) if k[0] in 'PS' else ((1.0, 0.85, 0.3) if k.startswith('J') else (0.85, 0.75, 1.0)))

# tablou, cutie NET, caseta coloanei, cornisa peste usa
TE = D['TE']
te = doc.addObject('Part::Box', 'Tablou_TE'); te.Length, te.Width, te.Height = 120, 450, 300
te.Placement.Base = V(TE[0] - 60, TE[1] - 225, 2150); te.Label = 'TE - tablou electric (deasupra usii de intrare)'
g_te.addObject(te); color(te, (0.30, 0.30, 0.32))
net = doc.addObject('Part::Box', 'Cutie_NET'); net.Length, net.Width, net.Height = 300, 100, 400
net.Placement.Base = V(P['NET'][0] - 150, -5550, 1800); net.Label = 'NET - cutie media (ONT / patch / splitter)'
g_te.addObject(net); color(net, WEAKC, 30)
drops = [t['points'][3] for t in D['tubes'] if t['src'] == 'TE' and t['net'] == 'P' and 'local' not in t['note']]
xs = [p[0] for p in drops]
mask = doc.addObject('Part::Box', 'Caseta_coloana_GC')
mask.Length, mask.Width, mask.Height = max(xs) - min(xs) + 120, 120, 2450
mask.Placement.Base = V(min(xs) - 60, -3545 - 120, 0)
mask.Label = 'Caseta gips-carton coloana (cu capac demontabil)'; g_te.addObject(mask); color(mask, (0.85, 0.85, 0.8), 70)
corn = doc.addObject('Part::Feature', 'Cornisa_GC_peste_usa')
corn.Shape = Part.makePolygon([V(TE[0], TE[1] - 230, 2350), V(10040, -3650, 2350), V(min(xs) - 60, -3605, 2350)])
corn.Label = 'Traseu aparent in cornisa GC: TE -> caseta'; g_te.addObject(corn)
try: corn.ViewObject.LineWidth = 6; corn.ViewObject.LineColor = (0.4, 0.4, 0.4)
except Exception: pass

# incrucisari
for i, c in enumerate(D['crossings']):
    s_ = doc.addObject('Part::Feature', f'X{i+1:02d}')
    s_.Shape = Part.makeSphere(28, V(c['xy'][0], c['xy'][1], D['ZF']))
    s_.Label = f"X{i+1:02d} {c['a']} x {c['b']}" + (' (forta/slabi)' if c['mixed'] else '')
    g_x.addObject(s_); color(s_, (1, 0, 0), 40)

# context: muchiile peretilor la pardoseala
edges = [Part.makeLine(V(e[0][0], e[0][1], 0), V(e[1][0], e[1][1], 0)) for e in ARCH['wall_edges'] if len(e) == 2]
w = doc.addObject('Part::Feature', 'Pereti_contur'); w.Shape = Part.makeCompound(edges); g_ctx.addObject(w)
try: w.ViewObject.LineColor = (0.2, 0.2, 0.2); w.ViewObject.LineWidth = 2
except Exception: pass
doc.recompute()
print('obiecte', len(doc.Objects), 'tuburi', len(D['tubes']))
