"""Pregateste panouri.json pentru randarea izometrica a fiecarui panou (montaj_panouri_blender.py) si metadatele pentru PDF.
build(S, folder) -> (lista panouri unice cu vederi, cale json)"""
import json, subprocess
from pathlib import Path
import montaj_holes

BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
ROOT = Path(__file__).resolve().parents[1]
AXN = {0: 'X', 1: 'Y', 2: 'Z'}


def view_dir(n):
    a = max(range(3), key=lambda i: abs(n[i])); s = 1 if n[a] > 0 else -1
    d = [0.0, 0.0, 0.0]; d[a] = 1.0 * s
    if a == 2:
        d[1] += 0.55; d[0] += -0.5
    elif a == 0:
        d[1] += 0.6; d[2] += 0.5
    else:
        d[0] += 0.6; d[2] += 0.5
    return d


def groups(d):
    g = {}
    for h in d['h3']:
        key = tuple(round(v) for v in h['n_out'])
        g.setdefault(key, []).append(h)
    return g


FACE_NAME = {(1, 0, 0): 'fața dinspre stânga', (-1, 0, 0): 'fața dinspre dreapta', (0, 1, 0): 'fața din față', (0, -1, 0): 'fața din spate',
             (0, 0, 1): 'fața de sus', (0, 0, -1): 'fața de jos'}


def build(S, folder, run=True):
    info = montaj_holes.compute(S)
    uniq, seen = [], {}
    for pid, d in info.items():
        if not d['h3']:
            continue
        sig = (d['p']['code'], tuple(sorted((tuple(round(v) for v in h['pos']), h['kind']) for h in d['h3'])))
        # panoul e acelasi doar daca pozitiile relative sunt identice; deosebim lateralele stanga/dreapta (oglindite)
        key = (d['p']['code'], tuple(sorted((round(h['pos'][0] - d['p']['box'][0], 1), round(h['pos'][1] - d['p']['box'][1], 1), round(h['pos'][2] - d['p']['box'][2], 1), h['kind'])
                                            for h in d['h3'])))
        if key in seen:
            seen[key]['count'] += 1
            continue
        views = []
        for n, hs in sorted(groups(d).items(), key=lambda kv: -len(kv[1])):
            kinds = {}
            for h in hs: kinds[h['kind']] = kinds.get(h['kind'], 0) + 1
            fname = FACE_NAME.get(n, str(n))
            if all(h['kind'] in ('pilot5', 'cep8', 'hook6') and h.get('face') == 'muchie' for h in hs):
                fname = 'muchia ' + FACE_NAME.get(n, str(n)).replace('fața ', '')
            views.append(dict(name=fname, n=list(n), dir=view_dir(n), holes=hs, kinds=kinds))
        e = dict(id=pid, code=d['p']['code'], label=d['p']['label'], box=d['p']['box'], mat=d['p']['mat'], views=views, count=1,
                 size=(d['L'], d['W'], d['T']))
        seen[key] = e; uniq.append(e)
    folder = Path(folder).resolve()
    js = folder / 'panouri.json'
    js.write_text(json.dumps(dict(panels=[dict(id=u['id'], box=u['box'], mat=u['mat'], views=[dict(name=v['name'], dir=v['dir'], holes=v['holes']) for v in u['views']]) for u in uniq]),
                             ensure_ascii=False), encoding='utf-8')
    if run:
        lib = ROOT / 'tmp' / 'feronerie_R2' / 'feronerie_3d.blend'
        r = subprocess.run([BLENDER, '--background', '--python', str(ROOT / 'scripturi' / 'montaj_panouri_blender.py'), '--', str(js), str(folder / 'panouri'), str(lib)],
                           capture_output=True, text=True)
        print(r.stdout[-300:], r.stderr[-400:])
    return uniq
