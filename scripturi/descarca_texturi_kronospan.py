"""Descarcă texturile oficiale Kronospan pentru randări (Biblioteca digitală kronospan.com, publică, fără cont).
Nu sunt CC0: sunt imaginile Kronospan oferite pentru vizualizări; le folosim doar în randările apartamentului.
- culorile uni: imaginea decorului 1200 × 1800 px (cererea „download” de pe pagina decorului);
- stejarul: scanarea plăcii întregi 2070 × 2800 mm, scoasă SINGURĂ din arhiva mare (cereri HTTP Range:
  directorul central al arhivei + doar octeții fișierului dorit), fără să se descarce toată arhiva de 2 GB;
- structurile de suprafață (PE, BS, SU, PW, FP), din arhiva „Textures”, tot cu cereri parțiale.
Rulează: python descarca_texturi_kronospan.py   →  texturi/kronospan/ + rânduri noi în texturi/LICENTE.md"""
import struct, urllib.request, zlib, json, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'texturi' / 'kronospan'
UA = {'User-Agent': 'Mozilla/5.0 (Apartament184-render)'}
DECOR = 'https://kronospan.com/ro_RO/ajax/express_services/download?args%%5B0%%5D=decors&args%%5B1%%5D=kronodesign&args%%5B2%%5D=%s&args%%5B3%%5D=%s.jpg&name=%s'
FULL = 'https://kronospan.com/public/files/bdl/kd2023-standard-2070x2800mm.zip'
TEXZ = 'https://kronospan.com/public/files/express-services/downloads/for-all-countries/decors-and-textures-for-visualisation/kd2023-textures.zip'
COLORS = {'K8681': 'Brilliant White', 'K8685': 'Snow White', 'K8100': 'Pearl White', 'K101': 'Front White',
          'K5981': 'Cashmere', 'K7045': 'Satin', 'K003': 'Gold Craft Oak', 'K076': 'Sand Expressive Oak',
          '3025': 'Light Vintage Oak (Sonoma)'}
FULL_FILES = {'kd2023-standard-2070x2800mm/K003.jpg': 'K003_2070x2800mm.jpg',
              'kd2023-standard-2070x2800mm/3025.jpg': '3025_2070x2800mm.jpg'}
STRUCT = ['PE', 'BS', 'SU', 'PW', 'FP', 'SM', 'SN']


def req(url, rng=None, method='GET'):
    h = dict(UA)
    if rng:
        h['Range'] = 'bytes=%d-%d' % rng
    with urllib.request.urlopen(urllib.request.Request(url, headers=h, method=method), timeout=300) as r:
        return r.read() if method == 'GET' else int(r.headers['Content-Length'])


def zip_dir(url):
    n = req(url, method='HEAD')
    tail = req(url, (max(0, n - 70000), n - 1))
    i = tail.rfind(b'PK\x05\x06')
    _, _, _, _, ent, cd_size, cd_off, _ = struct.unpack('<IHHHHIIH', tail[i:i + 22])
    cd = req(url, (cd_off, cd_off + cd_size - 1))
    out, p = {}, 0
    while cd[p:p + 4] == b'PK\x01\x02':
        f = struct.unpack('<IHHHHHHIIIHHHHHII', cd[p:p + 46])
        meth, crc, csz, usz, nl, el, cl, lho = f[4], f[7], f[8], f[9], f[10], f[11], f[12], f[16]
        name = cd[p + 46:p + 46 + nl].decode('utf-8', 'replace')
        out[name] = dict(meth=meth, crc=crc, csz=csz, usz=usz, lho=lho)
        p += 46 + nl + el + cl
    return out


def zip_get(url, e):
    h = req(url, (e['lho'], e['lho'] + 29))
    nl, el = struct.unpack('<HH', h[26:30])
    start = e['lho'] + 30 + nl + el
    raw = req(url, (start, start + e['csz'] - 1))
    data = raw if e['meth'] == 0 else zlib.decompress(raw, -15)
    assert len(data) == e['usz'] and (zlib.crc32(data) & 0xffffffff) == e['crc'], 'CRC greșit'
    return data


OUT.mkdir(parents=True, exist_ok=True)
log, total = [], 0
for code, name in COLORS.items():
    f = OUT / (code + '.jpg')
    if not f.exists():
        f.write_bytes(req(DECOR % (code[0], code, code)))
    total += f.stat().st_size
    log.append((code + ' ' + name, 'imaginea decorului 1200 × 1800 px', f.name, f.stat().st_size))
for url, files in ((FULL, FULL_FILES), (TEXZ, {'kd2023-textures/%s.jpg' % s: 'structura_%s.jpg' % s for s in STRUCT})):
    d = zip_dir(url)
    for src, dst in files.items():
        f = OUT / dst
        if not f.exists():
            f.write_bytes(zip_get(url, d[src]))
        total += f.stat().st_size
        log.append((dst.replace('.jpg', ''), 'din ' + url.rsplit('/', 1)[1] + ' (doar acest fișier)', f.name, f.stat().st_size))
        print('OK', dst, f.stat().st_size, flush=True)

lic = ROOT / 'texturi' / 'LICENTE.md'
txt = lic.read_text(encoding='utf-8') if lic.exists() else ''
if '## Kronospan' not in txt or '3025' not in txt:
    txt = txt.split('\n## Kronospan')[0]
    lines = ['', '## Kronospan (imagini oficiale pentru vizualizare, nu CC0)', '',
             'Descărcate pe %s din Biblioteca digitală kronospan.com (publică, fără cont). Drepturile aparțin Kronospan; '
             'le folosim doar în randările apartamentului, nu le redistribuim separat.' % datetime.date.today().strftime('%d.%m.%Y'), '',
             '| Decor / structură | Sursă | Fișier | Mărime |', '|---|---|---|---|']
    lines += ['| %s | %s | `kronospan/%s` | %.1f MB |' % (a, b, c, s / 1e6) for a, b, c, s in log]
    lic.write_text(txt.rstrip('\n') + '\n' + '\n'.join(lines) + '\n', encoding='utf-8')
print('KRONOSPAN_OK %.1f MB' % (total / 1e6))
