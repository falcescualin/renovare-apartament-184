"""Copii JPG pentru documente și web: randari/{zi,noapte}/*.png → randari/web/{zi,noapte}/*.jpg (1600 × 1000, calitate 88).
Rulează: python randari_web.py"""
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
n = 0
for mode in ('zi', 'noapte'):
    out = ROOT / 'randari' / 'web' / mode
    out.mkdir(parents=True, exist_ok=True)
    for f in sorted((ROOT / 'randari' / mode).glob('*.png')):
        im = Image.open(f).convert('RGB')
        im.thumbnail((1600, 1000), Image.LANCZOS)
        im.save(out / (f.stem + '.jpg'), quality=88, optimize=True)
        n += 1
print('WEB_OK', n)
