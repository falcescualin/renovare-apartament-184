"""Descarcă texturile CC0 pentru microcimentul olive grey din baie (cerut 06.10.2026):
- ambientCG Concrete046 (perete neted, fără rosturi, 2,4 × 2,4 m), pachetul 4K-JPG;
- Poly Haven plastered_wall_04 (tencuială/ciment de interior, urme de gletieră, 3,2 × 3,2 m), hărțile 4K.
Adaugă rândurile în texturi/LICENTE.md. Rulează: python descarca_texturi_baie.py"""
import json, os, urllib.request, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'texturi'
UA = {'User-Agent': 'Apartament184-render/1.0 (texturi CC0 pentru randare)'}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=600) as r:
        return r.read()


def save(url, path, size=None):
    if path.exists() and (size is None or path.stat().st_size == size):
        return path.stat().st_size
    data = get(url)
    if size is not None and len(data) != size:
        raise RuntimeError('mărime diferită: %s' % path.name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return len(data)


rows, total = [], 0
aid = 'Concrete046'
meta = json.loads(get('https://ambientcg.com/api/v2/full_json?id=%s&include=downloadData' % aid))['foundAssets'][0]
dl = [x for x in meta['downloadFolders']['default']['downloadFiletypeCategories']['zip']['downloads'] if x['attribute'] == '4K-JPG'][0]
d = OUT / 'ambientcg' / aid
z = d / dl['fileName']
total += save(dl['downloadLink'], z, dl['size'])
with zipfile.ZipFile(z) as zf:
    zf.extractall(d)
    got = zf.namelist()
rows.append(('ambientCG', aid, 'Microciment olive grey din baie: variație și relief', '2,4 × 2,4 m', ', '.join(got[:4]) + ' …', 'https://ambientcg.com/view?id=' + aid))
print('ACG ok', flush=True)

aid = 'plastered_wall_04'
info = json.loads(get('https://api.polyhaven.com/info/' + aid))
files = json.loads(get('https://api.polyhaven.com/files/' + aid))
d = OUT / 'polyhaven' / aid
got = []
for m in ('Diffuse', 'nor_gl', 'Rough'):
    f = files[m]['4k']['jpg']
    total += save(f['url'], d / os.path.basename(f['url']), f['size'])
    got.append(os.path.basename(f['url']))
(d / 'info.json').write_text(json.dumps({'id': aid, 'name': info.get('name'), 'dimensions_mm': info.get('dimensions'), 'authors': info.get('authors'),
                                         'maps': got, 'license': 'CC0'}, ensure_ascii=False, indent=1), encoding='utf-8')
rows.append(('Poly Haven', aid, 'Microciment olive grey din baie: urme de gletieră', '3,2 × 3,2 m', ', '.join(got), 'https://polyhaven.com/a/' + aid))
print('PH ok', flush=True)

lic = OUT / 'LICENTE.md'
txt = lic.read_text(encoding='utf-8')
add = [r for r in rows if r[1] not in txt]
if add:
    head = txt.split('\n## Kronospan')[0].rstrip('\n')
    tail = txt[len(head):]
    head += '\n' + '\n'.join('| %s | %s | %s | %s | %s | [pagină](%s) |' % r for r in add)
    lic.write_text(head + tail, encoding='utf-8')
print('BAIE_OK %.0f MB' % (total / 1e6))
