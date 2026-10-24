"""Deviz materiale R04 (PDF): rulează deviz_pdf.py nemodificat, cu rânduri noi în tabelul de corecții pentru R04.
Cifrele din rânduri se citesc din tmp/deviz.json, lista de piese, optimizare și costul debitării (nu sunt scrise de mână).
Rulează cu Python-ul care are reportlab, după deviz_R04_kronospan.py."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
J = lambda f: json.loads((ROOT / f).read_text(encoding='utf-8'))
D, L, Y, C = J('tmp/deviz.json'), J('tmp/lista_debitare_R03.json'), J('tmp/debitare_layout_R03.json')['materiale'], J('tmp/cost_debitare_R03.json')
N = {m: Y[m]['n'] for m in Y}
cq = C['cantitati']
lei = lambda v: '{:,.0f}'.format(v).replace(',', '.')
dif = D['tot_min'] - D['old_total'][0]
KRONO = -2285                       # trecerea pe Kronospan (R04 înainte de dormitorul nou, 06.10.2026)
src = (ROOT / 'scripturi/deviz_pdf.py').read_text(encoding='utf-8')
old = "changes=[['Corecție','Bază / efect'],"
assert old in src
rows = [
    ['Plăci Kronospan și debitare exactă (R04)',
     'Lista completă de piese din modelele FreeCAD (%d de piese, inclusiv bucătăria) și optimizarea pe plăci dau %d plăci albe 8685 BS, '
     '%d cashmere 5981 BS, %d stejar 3025 SN, %d albe de 16 mm, %d HDF și blatul 3025. Debitarea se plătește pe foaie, căntuirea pe metru '
     '(%s m de 2 mm); balamalele sunt după tabelul Blum (%d). Trecerea de la Egger la Kronospan: %s lei.' % (
         sum(p['n'] for p in L['piese']), N['ALB18'], N['CAS18'], N['STJ18'], N['ALB16'], N['HDF3'],
         lei(sum(v for k, v in cq['cant'].items() if '22x2' in k)), cq['balamale'], lei(KRONO).replace('-', '−'))],
    ['Dormitorul refăcut de Codex (R04)',
     'Dulap nou 2200 × 600 × 2360 cu 4 uși, 20 balamale BLUMOTION, 8 sertare interioare și LED la uși; corp îngust în spatele patului cu blat '
     'de stejar; tablou 110 × 70; noptiera de sud scoasă. Adaugă %s lei. Față de R03, per total: %s%s lei la cele mai bune oferte.' % (
         lei(dif - KRONO), '+' if dif >= 0 else '−', lei(abs(dif)))],
]
new = old + ''.join('[%r,%r],' % tuple(r) for r in rows)
src = src.replace(old, new, 1)
exec(compile(src, 'deviz_pdf.py', 'exec'), {'__name__': '__main__', '__file__': str(ROOT / 'scripturi/deviz_pdf.py')})
