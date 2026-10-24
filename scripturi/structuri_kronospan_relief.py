"""Transformă fotografiile structurilor Kronospan (lumină razantă, cu gradient de iluminare) în hărți de relief:
gri → scădere estompare mare (filtru trece-sus, sigma 25 px) → normalizare robustă (p1–p99) → PNG 16 biți.
Pentru stejar (3025, K003): relieful porilor din scanarea plăcii, la rezoluție redusă 1:2.
Iese în texturi/kronospan/relief/. Rulează: python structuri_kronospan_relief.py"""
import numpy as np
from PIL import Image, ImageFilter
from pathlib import Path
Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'texturi' / 'kronospan'
OUT = D / 'relief'
OUT.mkdir(exist_ok=True)


def relief(src, dst, sigma, scale=1.0):
    im = Image.open(src).convert('L')
    if scale != 1.0:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    a = np.asarray(im, dtype=np.float32)
    blur = np.asarray(im.filter(ImageFilter.GaussianBlur(sigma)), dtype=np.float32)
    hp = a - blur
    lo, hi = np.percentile(hp, 1), np.percentile(hp, 99)
    h = np.clip((hp - lo) / max(hi - lo, 1e-6), 0, 1)
    Image.fromarray((h * 65535).astype(np.uint16)).save(dst)
    print(dst.name, im.size, 'p1/p99 %.1f/%.1f' % (lo, hi))


for s in ('PE', 'BS', 'SU', 'PW', 'FP', 'SM', 'SN'):
    f = D / ('structura_%s.jpg' % s)
    if f.exists():
        relief(f, OUT / ('relief_%s.png' % s), 25)
for k in ('3025', 'K003'):
    f = D / ('%s_2070x2800mm.jpg' % k)
    if f.exists():
        relief(f, OUT / ('relief_%s_pori.png' % k), 6, 0.5)
print('RELIEF_OK')
