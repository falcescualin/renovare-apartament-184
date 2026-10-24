"""Construieste toate modelele din feronerie_cad.py si le exporta (fara GUI, doar fisiere de schimb - .FCStd se salveaza din GUI).
Rulare:  freecadcmd feronerie_cad_export.py   (iesire in tmp/feronerie_R2/)
  step/<id>.step, step/feronerie_toate.step, obj/<id>.obj + .mtl (o culoare = un material), manifest.json (gabarit, volum, timp)"""
import sys, os, json, time, traceback
HERE = r'C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14\scripturi'
sys.path.insert(0, HERE)
import FreeCAD as App, Part
import importlib, feronerie_catalog, feronerie_cad
importlib.reload(feronerie_catalog); importlib.reload(feronerie_cad)
from feronerie_catalog import CATALOG, COL, METAL
import feronerie_cad as C

OUT = os.path.join(os.path.dirname(HERE), 'tmp', 'feronerie_R2')
only = [a for a in sys.argv[1:] if not a.endswith('.py')]
for d in ('step', 'obj'):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)


def write_obj(mid, parts):
    bb = None
    for s, c in parts:
        bb = s.BoundBox if bb is None else bb.united(s.BoundBox)
    diag = bb.DiagonalLength
    tol = min(0.03, max(0.006, diag * 0.00035))
    lines = ['# %s - feronerie R2 (mm)' % mid, 'mtllib %s.mtl' % mid]
    mats = []
    off = 1
    for k, (s, c) in enumerate(parts):
        v, f = s.tessellate(tol)
        lines.append('o %s_%d' % (mid, k))
        lines.append('usemtl %s' % c)
        if c not in mats:
            mats.append(c)
        lines += ['v %.4f %.4f %.4f' % (p.x, p.y, p.z) for p in v]
        lines += ['f %d %d %d' % (a + off, b + off, cc + off) for a, b, cc in f]
        off += len(v)
    open(os.path.join(OUT, 'obj', mid + '.obj'), 'w').write('\n'.join(lines) + '\n')
    m = []
    for c in mats:
        r, g, b = COL[c]
        m += ['newmtl %s' % c, 'Kd %.4f %.4f %.4f' % (r, g, b), 'Ks %.2f %.2f %.2f' % ((0.6,) * 3 if c in METAL else (0.15,) * 3),
              'Ns %d' % (300 if c in METAL else 60), 'd 1.0', 'illum 2', '']
    open(os.path.join(OUT, 'obj', mid + '.mtl'), 'w').write('\n'.join(m))
    return tol


man, allshapes, x = {}, [], 0.0
ROWS = list(CATALOG) + [(m, '', m, '', '', 'variantă parametrică', 'gabarit', '') for m in only if '@' in m]
for (mid, cod, name, dims, use, src, prec, frame) in ROWS:
    if only and mid not in only:
        continue
    t0 = time.time()
    try:
        parts = C.build(mid)
        bad = [k for k, (s, c) in enumerate(parts) if not s.isValid() or s.Volume <= 0]
        comp = Part.makeCompound([s for s, c in parts])
        comp.exportStep(os.path.join(OUT, 'step', mid + '.step'))
        tol = write_obj(mid, parts)
        bb = comp.BoundBox
        man[mid] = dict(name=name, cod=cod, precizie=prec, sursa=src, cadru=frame, n_solide=len(parts), invalide=bad,
                        gabarit=[round(bb.XMin, 2), round(bb.YMin, 2), round(bb.ZMin, 2), round(bb.XMax, 2), round(bb.YMax, 2), round(bb.ZMax, 2)],
                        volum_mm3=round(sum(s.Volume for s, c in parts), 1), tol=tol, sec=round(time.time() - t0, 2))
        c2 = comp.copy(); c2.translate(App.Vector(x - bb.XMin, 0, 0)); allshapes.append(c2); x += bb.XLength + 30
        print('OK %-20s %5.2fs  solide %d  invalide %s  gabarit %.1f x %.1f x %.1f' % (mid, time.time() - t0, len(parts), bad, bb.XLength, bb.YLength, bb.ZLength))
    except Exception as e:
        man[mid] = dict(name=name, eroare=str(e))
        print('EROARE', mid, e)
        traceback.print_exc()
if not only:
    Part.makeCompound(allshapes).exportStep(os.path.join(OUT, 'step', 'feronerie_toate.step'))
mf = os.path.join(OUT, 'manifest.json')
old = json.load(open(mf, encoding='utf-8')) if (only and os.path.exists(mf)) else {}
old.update(man)
json.dump(old, open(mf, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('GATA', len(man))
