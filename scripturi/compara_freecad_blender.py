"""Compară exportul nou din FreeCAD (blender_export_2026-10-06) cu scena de randare din Blender (dump JSON din
blender_dump_scena.py) și cu exportul vechi (blender_export, 05.10.2026).
Rulează: python compara_freecad_blender.py  → tmp/diferente_freecad_blender.json + rezumat în consolă."""
import json, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEW = json.loads((ROOT / 'blender_export_2026-10-06/furniture_manifest.json').read_text(encoding='utf-8'))['parts']
OLD = json.loads((ROOT / 'blender_export/furniture_manifest.json').read_text(encoding='utf-8'))['parts']
BL = json.loads((ROOT / 'tmp/scena_randare_dump.json').read_text(encoding='utf-8'))['objects']
TOL = 1.0   # mm

new = {p['part_id'][:63]: p for p in NEW}
old = {p['part_id'][:63]: p for p in OLD}
bl = {o['name']: o for o in BL}


def box(p):
    mn = p['bbox_min_mm']; sz = p['bbox_mm']
    return mn, [mn[i] + sz[i] for i in range(3)]


def moved(p, o):
    mn, mx = box(p)
    d = max(max(abs(mn[i] - o['bbox_min'][i]), abs(mx[i] - o['bbox_max'][i])) for i in range(3))
    return d


res = dict(noi_in_freecad=[], scoase_din_freecad=[], geometrie_diferita=[], ascunse_in_blender=[], culoare_schimbata=[], doar_in_blender=[])
for pid, p in new.items():
    o = bl.get(pid)
    if o is None:
        res['noi_in_freecad'].append(dict(id=pid, label=p['label'], assembly=p['assembly'], bbox_mm=[round(v) for v in p['bbox_mm']],
                                          vechi=pid in old))
        continue
    d = moved(p, o)
    if d > TOL:
        res['geometrie_diferita'].append(dict(id=pid, label=p['label'], diferenta_mm=round(d, 1),
                                              freecad=[[round(v) for v in x] for x in box(p)], blender=[o['bbox_min'], o['bbox_max']]))
    if o['hide_render'] and not p.get('hidden'):
        res['ascunse_in_blender'].append(dict(id=pid, label=p['label']))
    q = old.get(pid)
    if q and (q['color_rgb'] != p['color_rgb'] or q.get('transparency') != p.get('transparency')):
        res['culoare_schimbata'].append(dict(id=pid, label=p['label'], vechi=[q['color_rgb'], q.get('transparency')], nou=[p['color_rgb'], p.get('transparency')]))
for name, o in bl.items():
    if name in new:
        continue
    if o['part_id'] or name in old:
        res['scoase_din_freecad'].append(dict(id=name, hide_render=o['hide_render'], collection=o['collection'], in_export_vechi=name in old))
    else:
        res['doar_in_blender'].append(dict(id=name, collection=o['collection'], hide_render=o['hide_render']))
(ROOT / 'tmp/diferente_freecad_blender.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
print('FreeCAD acum: %d piese | Blender: %d obiecte mesh | export vechi: %d' % (len(new), len(bl), len(old)))
for k, v in res.items():
    print('\n==', k, len(v))
    for r in v[:60]:
        print('  ', json.dumps(r, ensure_ascii=False)[:260])
