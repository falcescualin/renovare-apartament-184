"""Cost exact pentru plăcile mobilierului la comandă (R03), pe furnizori, din:
- tmp/lista_debitare_R03.json (piese, canturi) și tmp/debitare_layout_R03.json (plăci, tăieturi);
- prețurile găsite online pe 06.10.2026 (TVA inclus), cu sursa fiecărui preț.
Mambricolaj are lista de servicii publică (debitare pe foaie, căntuire pe ml, găuri balama, decupaje).
Regency are prețuri publice pentru plăci și canturi, dar serviciile se ofertează din fișierul lor de optimizare:
pentru ele se folosesc tarifele Mambricolaj ca ESTIMARE (marcat ca atare).
Iese: tmp/cost_debitare_R03.json"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
L = json.loads((ROOT / 'tmp/lista_debitare_R03.json').read_text(encoding='utf-8'))
Y = json.loads((ROOT / 'tmp/debitare_layout_R03.json').read_text(encoding='utf-8'))['materiale']
NS = {m: r['n'] for m, r in Y.items()}

# ---------------------------------------------------------------- cantităţi
E = {}
for p in L['piese']:
    for k, ln in (('L1', p['L']), ('L2', p['L']), ('W1', p['W']), ('W2', p['W'])):
        if p[k] != '-':
            dec = {'ALB16': 'ALB', 'ALB18': 'ALB', 'CAS18': 'CAS', 'STJ18': 'STJ', 'BLAT38': 'STJ'}[p['mat']]
            t = {'2': '22x2', '0.8': '22x0.4', '42': '42x2'}[p[k]]
            E[(dec, t)] = E.get((dec, t), 0) + (ln + 40) * p['n'] / 1000          # + 4 cm pierdere la fiecare muchie
E = {k: round(v, 1) for k, v in E.items()}


def hinges(h):
    """număr de balamale după înălțimea laturii cu balamale (recomandarea Blum pentru uși de 18 mm)"""
    return 2 if h <= 900 else 3 if h <= 1600 else 4 if h <= 2000 else 5


DOORS = {'DH-F01': 1699, 'DH-F02': 377, 'SP-07': 647, 'SP-13': 660, 'SP-14': 1657, 'DW-04': 796, 'CTV-06': 376, 'DD-07': 2276,
         'BJ-F01': 716, 'BJ-F03': 716, 'BJ-F04': 716, 'BJ-F08': 573, 'BJ-F09': 956, 'BJ-F10': 956, 'BJ-F11': 756}
NB = 0
for p in L['piese']:
    if p['cod'] in DOORS:
        NB += hinges(DOORS[p['cod']]) * p['n']
    elif re.match(r'DR-U\d', p['cod']):
        NB += hinges(2068) * p['n']
    elif re.match(r'DR-S\d', p['cod']):
        NB += hinges(377) * p['n']
OBLIC = 14            # tăieturi oblice: debara 4 + 4 + 2 perechi, dulap hol C03/C04 + 2 perechi C09
NOPT = sum(p['n'] for p in L['piese'] if p['cod'] == 'N-04')
DUBLARE = round(NOPT * 0.5 * 0.42 + 2.4 * 0.4, 2)  # blaturi lipite: noptiere + comoda TV (m², o dată pe blat)
Q = dict(placi=NS, cant=E, balamale=NB, oblic=OBLIC, dublare_m2=DUBLARE, decupaje=2, taiere_blat=2)

# ---------------------------------------------------------------- tarife (lei cu TVA, 06.10.2026)
MAM = dict(nume='Mambricolaj (București: Morarilor, Luica)', srv='public',
           placi={'ALB18': (279.00, 'Kronospan K8681 PE Brilliant White, în stoc'),
                  'CAS18': (279.00, 'Kronospan K5981 BS Cashmere, în stoc'),
                  'STJ18': (279.00, 'Kronospan K003 PW Gold Craft Oak, în stoc'),
                  'ALB16': (257.59, 'nu apare online → prețul Regency 8685 SM 16 mm'),
                  'HDF3': (83.79, 'nu apare online → prețul Regency HDF alb 110 PE'),
                  'BLAT38': (597.95, 'Blat Kronospan K003 FP 4100 × 600 × 38')},
           cant={('ALB', '22x2'): 2.95, ('ALB', '22x0.4'): 0.95, ('CAS', '22x2'): 3.95, ('CAS', '22x0.4'): 1.95, ('CAS', '42x2'): 8.95,
                 ('STJ', '22x2'): 5.95, ('STJ', '42x2'): 10.95},
           debitare_pal=45.95, debitare_hdf=27.95, debitare_blat=34.95, oblic=15.95, cantuire_22=3.95, cantuire_42=6.95,
           balama=5.95, decupaj=74.95, dublare=19.95)
REG = dict(nume='Regency (București: Morarilor, Metalurgiei)', srv='estimat (ofertă din fișierul lor de optimizare)',
           placi={'ALB18': (264.10, 'Kronospan 8685 BS Snow White'), 'CAS18': (313.86, 'Kronospan 5981 BS Cashmere'),
                  'STJ18': (307.07, 'Kronospan 3025 SN Sonoma (echivalentul H1145) – sau K003 PW 313,87'),
                  'ALB16': (257.59, 'Kronospan 8685 SM 16 mm'), 'HDF3': (83.79, 'HDF lăcuit alb 110 PE 2,5 mm'),
                  'BLAT38': (557.48, 'Blat Kronospan 3025 WO / K003 FP 4100 × 600 × 38')},
           cant={('ALB', '22x2'): 2.49, ('ALB', '22x0.4'): 0.71, ('CAS', '22x2'): 3.43, ('CAS', '22x0.4'): 1.03, ('CAS', '42x2'): 8.64,
                 ('STJ', '22x2'): 4.25, ('STJ', '42x2'): 10.73},
           debitare_pal=45.95, debitare_hdf=27.95, debitare_blat=34.95, oblic=15.95, cantuire_22=3.95, cantuire_42=6.95,
           balama=5.95, decupaj=74.95, dublare=19.95)
EGG = dict(nume='Egger – varianta din devizul R03 (pentru comparație)', srv='tarife Mambricolaj',
           placi={'ALB18': (366.42, 'Egger W1000 ST9, Regency'), 'CAS18': (366.42, 'Egger U702 ST9, Regency'),
                  'STJ18': (295.05, 'Egger H1145 ST10, Metalcom'), 'ALB16': (340.00, 'Egger W1000 16 mm, estimat'),
                  'HDF3': (126.65, 'HDF Kronospan alb, Mathaus'), 'BLAT38': (595.29, 'Blat Egger H1145, Regency')},
           cant={('ALB', '22x2'): 3.95, ('ALB', '22x0.4'): 1.95, ('CAS', '22x2'): 3.95, ('CAS', '22x0.4'): 1.95, ('CAS', '42x2'): 8.95,
                 ('STJ', '22x2'): 5.95, ('STJ', '42x2'): 10.95},
           debitare_pal=45.95, debitare_hdf=27.95, debitare_blat=34.95, oblic=15.95, cantuire_22=3.95, cantuire_42=6.95,
           balama=5.95, decupaj=74.95, dublare=19.95)


def calc(R):
    rows = []
    for m in ('ALB18', 'CAS18', 'STJ18', 'ALB16', 'HDF3', 'BLAT38'):
        pr, src = R['placi'][m]
        rows.append(('Plăci', '%s × %d' % (m, NS[m]), NS[m] * pr, '%d × %.2f – %s' % (NS[m], pr, src)))
    npal = sum(NS[m] for m in ('ALB18', 'CAS18', 'STJ18', 'ALB16'))
    rows.append(('Debitare', 'PAL %d foi' % npal, npal * R['debitare_pal'], '%d × %.2f / foaie' % (npal, R['debitare_pal'])))
    rows.append(('Debitare', 'HDF %d foi' % NS['HDF3'], NS['HDF3'] * R['debitare_hdf'], '%d × %.2f / foaie' % (NS['HDF3'], R['debitare_hdf'])))
    rows.append(('Debitare', 'blat: 2 tăieturi', 2 * R['debitare_blat'], ''))
    rows.append(('Debitare', 'tăieturi oblice (debara, dulap hol)', OBLIC * R['oblic'], '%d × %.2f' % (OBLIC, R['oblic'])))
    for (dec, t), ml in sorted(E.items()):
        cm = R['cant'][(dec, t)]
        ap = R['cantuire_42'] if t == '42x2' else R['cantuire_22']
        rows.append(('Cant', '%s %s: %.1f m' % (dec, t, ml), ml * (cm + ap), '%.1f m × (cant %.2f + aplicare %.2f)' % (ml, cm, ap)))
    rows.append(('Prelucrări', 'găuri balama Ø35: %d' % NB, NB * R['balama'], '%d × %.2f' % (NB, R['balama'])))
    rows.append(('Prelucrări', 'decupaj chiuvetă + plită', 2 * R['decupaj'], ''))
    rows.append(('Prelucrări', 'dublare blaturi: %.2f m²' % DUBLARE, DUBLARE * R['dublare'], ''))
    tot = sum(r[2] for r in rows)
    by = {}
    for r in rows:
        by[r[0]] = by.get(r[0], 0) + r[2]
    return dict(nume=R['nume'], servicii=R['srv'], randuri=[dict(cat=a, art=b, lei=round(c, 2), calcul=d) for a, b, c, d in rows],
                pe_categorii={k: round(v, 2) for k, v in by.items()}, total=round(tot, 2))


res = dict(cantitati=dict(placi=NS, cant={'%s %s' % k: v for k, v in E.items()}, balamale=NB, oblic=OBLIC, dublare_m2=DUBLARE),
           variante={'Mambricolaj': calc(MAM), 'Regency': calc(REG), 'Egger_R03': calc(EGG)})
# varianta mixtă: fiecare material de unde e mai ieftin (plăci + cant), serviciile la fiecare furnizor
mix = calc(MAM)
for i, r in enumerate(mix['randuri']):
    pass
best = {}
for m in ('ALB18', 'CAS18', 'STJ18', 'ALB16', 'HDF3', 'BLAT38'):
    a, b = MAM['placi'][m][0], REG['placi'][m][0]
    best[m] = ('Mambricolaj', a) if a <= b else ('Regency', b)
res['cel_mai_ieftin_pe_material'] = {m: dict(furnizor=f, pret=p) for m, (f, p) in best.items()}
(ROOT / 'tmp/cost_debitare_R03.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
print('Cantități:', json.dumps(res['cantitati'], ensure_ascii=False))
for k, v in res['variante'].items():
    print('\n==', v['nume'], '| servicii:', v['servicii'])
    for r in v['randuri']:
        print('   %-11s %-40s %9.2f  %s' % (r['cat'], r['art'], r['lei'], r['calcul']))
    print('   ', v['pe_categorii'], 'TOTAL', v['total'])
print('\nCel mai ieftin pe material:', best)
