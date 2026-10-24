"""Descarcă texturile PBR gratuite (licență CC0) aprobate pe 06.10.2026, în texturi/:
- Poly Haven: hărțile 4K necesare (culoare, normal GL, rugozitate, deplasare unde contează) + dimensiunile reale;
- ambientCG: pachetul 4K-JPG (arhivă zip, dezarhivată);
- HDRI Poly Haven 8K pentru cer și exteriorul văzut prin geamuri.
Scrie texturi/LICENTE.md (sursă, licență, dimensiuni). Rulează: python descarca_texturi_pbr.py"""
import json, os, sys, urllib.request, zipfile, io, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'texturi'
UA = {'User-Agent': 'Apartament184-render/1.0 (texturi CC0 pentru randare)'}
PH = [('wood_floor', ['Diffuse', 'nor_gl', 'Rough', 'Displacement'], 'Parchet stejar'),
      ('white_oak_veneer', ['Diffuse', 'nor_gl', 'Rough'], 'Riflaje stejar deschis'),
      ('smooth_concrete_floor', ['Diffuse', 'nor_gl', 'Rough'], 'Microciment alb cald'),
      ('painted_concrete', ['Diffuse', 'nor_gl', 'Rough'], 'Rășină epoxidică gri'),
      ('white_plaster_02', ['nor_gl', 'Rough'], 'Pereți și tavan: relief fin'),
      ('wool_boucle', ['Diffuse', 'nor_gl', 'Rough', 'Displacement'], 'Puf bouclé'),
      ('rough_linen', ['Diffuse', 'nor_gl', 'Rough'], 'Draperii, voal, lenjerie'),
      ('poly_wool_herringbone', ['Diffuse', 'nor_gl', 'Rough'], 'Canapea')]
ACG = [('Travertine009', 'Măsuța de travertin'), ('Metal009', 'Inox periat'), ('Carpet016', 'Covor')]
HDRI = ('buikslotermeerplein', '8k', 'Cer și exterior văzut prin geamuri')


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        return r.read()


def save(url, path, size=None):
    if path.exists() and (size is None or path.stat().st_size == size):
        return path.stat().st_size
    data = get(url)
    if size is not None and len(data) != size:
        raise RuntimeError('mărime diferită: %s (%d / %d)' % (path.name, len(data), size))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return len(data)


log, total = [], 0
for aid, maps, use in PH:
    info = json.loads(get('https://api.polyhaven.com/info/' + aid))
    files = json.loads(get('https://api.polyhaven.com/files/' + aid))
    d = OUT / 'polyhaven' / aid
    got = []
    for m in maps:
        fm = files[m]['4k']
        fmt = 'jpg' if 'jpg' in fm else 'png'
        f = fm[fmt]
        n = save(f['url'], d / os.path.basename(f['url']), f['size'])
        total += n
        got.append(os.path.basename(f['url']))
    (d / 'info.json').write_text(json.dumps({'id': aid, 'name': info.get('name'), 'dimensions_mm': info.get('dimensions'),
                                             'authors': info.get('authors'), 'maps': got, 'license': 'CC0'}, ensure_ascii=False, indent=1), encoding='utf-8')
    log.append(('Poly Haven', aid, info.get('name'), use, 'https://polyhaven.com/a/' + aid, info.get('dimensions'), got))
    print('PH', aid, 'ok', flush=True)

for aid, use in ACG:
    meta = json.loads(get('https://ambientcg.com/api/v2/full_json?id=%s&include=downloadData' % aid))['foundAssets'][0]
    dl = [x for x in meta['downloadFolders']['default']['downloadFiletypeCategories']['zip']['downloads'] if x['attribute'] == '4K-JPG'][0]
    d = OUT / 'ambientcg' / aid
    z = d / dl['fileName']
    total += save(dl['downloadLink'], z, dl['size'])
    with zipfile.ZipFile(z) as zf:
        zf.extractall(d)
        got = zf.namelist()
    log.append(('ambientCG', aid, meta.get('displayName'), use, 'https://ambientcg.com/view?id=' + aid, meta.get('dimensionX') and [meta.get('dimensionX'), meta.get('dimensionY')], got))
    print('ACG', aid, 'ok', flush=True)

aid, res, use = HDRI
files = json.loads(get('https://api.polyhaven.com/files/' + aid))
f = files['hdri'][res]['hdr']
total += save(f['url'], OUT / 'hdri' / os.path.basename(f['url']), f['size'])
log.append(('Poly Haven', aid, 'HDRI ' + res, use, 'https://polyhaven.com/a/' + aid, None, [os.path.basename(f['url'])]))
print('HDRI ok', flush=True)

lines = ['# Texturi PBR pentru randări', '',
         'Descărcate pe %s. Toate au licența **CC0** (domeniu public): se pot folosi gratuit, inclusiv comercial, fără atribuire obligatorie.' % datetime.date.today().strftime('%d.%m.%Y'), '',
         '| Sursă | Textură | Folosită la | Dimensiune reală | Fișiere | Link |', '|---|---|---|---|---|---|']
for src, aid, name, use, url, dim, got in log:
    dims = (' × '.join('%g' % (v / 1000) for v in dim[:2]) + ' m') if isinstance(dim, list) and dim and dim[0] else '-'
    lines.append('| %s | %s | %s | %s | %s | [pagină](%s) |' % (src, aid, use, dims, ', '.join(got[:5]) + (' …' if len(got) > 5 else ''), url))
(OUT / 'LICENTE.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('DOWNLOAD_OK %.0f MB' % (total / 1e6))
