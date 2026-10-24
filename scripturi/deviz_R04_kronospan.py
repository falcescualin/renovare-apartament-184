"""Deviz R04 (06.10.2026): plăcile de mobilier trec pe Kronospan și debitarea e calculată exact din planul R03.
Pornește din R03 (tmp/deviz.json → copie în tmp/deviz_R03.json) și schimbă doar liniile de mobilier la comandă:
- M062–M066, M068: plăci Kronospan cu cantitățile din optimizare (17 / 5 / 2 / 6 / 1 + blat după dormitorul nou),
  cea mai bună ofertă pe fiecare material și alternativa;
- M067: debitare pe foaie + cant aplicat (metri exacți din lista de piese);
- M104: găurile de balamale, decupajele și dublarea blaturilor (le face atelierul);
- M072 / M074: balamalele corectate după tabelul Blum (dressing 35 în loc de 30, bucătărie 22 în loc de 24);
- dormitorul refăcut de Codex pe 06.10: M105 feroneria dulapului nou și a corpului din spatele patului, M106 tabloul,
  LED-ul dulapului în M036 / M037 / M039, iar M076 pierde sertarele noptierei scoase.
Restul liniilor rămân ca în R03. Scrie tmp/deviz.json (R04) și Deviz_materiale_ap184_R04.xlsx."""
import json, shutil, datetime, collections
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'tmp/deviz.json'
R03 = ROOT / 'tmp/deviz_R03.json'
if not R03.exists():
    shutil.copy(SRC, R03)
D = json.loads(R03.read_text(encoding='utf-8'))
assert D['revision'] == 'R03', D['revision']
C = json.loads((ROOT / 'tmp/cost_debitare_R03.json').read_text(encoding='utf-8'))
Y = json.loads((ROOT / 'tmp/debitare_layout_R03.json').read_text(encoding='utf-8'))['materiale']
ROWS = {r['id']: r for r in D['rows']}
V, E = 'verificat', 'estimat'
DT = '06.10.2026'


def set_row(i, art, q, um, best, store, url, alt, alt_store, note, st=V):
    r = ROWS[i]
    r.update(art=art, q=q, um=um, pmin=round(best, 2), pmax=round(alt, 2), url=url, st=st, magazin=store, magazin_alt=alt_store, note=note,
             price_basis='Cea mai bună ofertă: %s; alternativă: %s (%s)' % (store, alt_store, DT))


N = {m: Y[m]['n'] for m in Y}
set_row('M062', 'PAL Kronospan 8685 BS Snow White 18 mm 2800 × 2070 (corpuri)', N['ALB18'], 'placă', 264.10, 'Regency 264,10 lei',
        'https://regencycompany.ro/pal-melaminat-kronospan-alb-corp-zapada-8685-bs-18mm-2-80-x-2-07', 279.00, 'Mambricolaj K8681 PE 279 lei (în stoc)',
        'Din planul de debitare R03 (%d plăci, %s %% folosite; 4 doar pentru dulapul nou de dormitor). Echivalentul Egger W1000 ST9 în tabelele de cant.' % (
            N['ALB18'], str(Y['ALB18']['util']).replace('.', ',')))
set_row('M063', 'PAL Kronospan 5981 BS Cashmere 18 mm 2800 × 2070 (fronturi, noptiere, comoda TV)', N['CAS18'], 'placă', 279.00, 'Mambricolaj 279 lei (în stoc)',
        'https://www.mam-bricolaj.ro/cumpara/pal-melaminat-casmir-5981bs-2800x2070x18mm-6239', 313.86, 'Regency 313,86 lei',
        'Din planul de debitare R03 (%d plăci). 5981 = Egger U702 în tabelele de cant.' % N['CAS18'])
set_row('M064', 'PAL Kronospan 8685 SM 16 mm (cutii de sertar MOVENTO, spate din baie și nișa de detergenți)', N['ALB16'], 'placă', 257.59, 'Regency 257,59 lei',
        'https://regencycompany.ro/kronospan', 269.38, 'Regency 114 SM 16 mm 269,38 lei', 'Din planul de debitare R03 (%d plăci).' % N['ALB16'])
set_row('M065', 'HDF lăcuit alb 2,5 mm 2800 × 2070 (spate corpuri)', N['HDF3'], 'placă', 83.79, 'Regency HDF alb 110 PE 83,79 lei',
        'https://regencycompany.ro/kronospan', 126.65, 'Mathaus HDF Kronospan alb 3 mm 126,65 lei', 'Din planul de debitare R03 (%d plăci; spatele dulapului nou din 4 bucăți).' % N['HDF3'])
set_row('M066', 'PAL Kronospan 3025 SN stejar Sonoma 18 mm (comoda TV dormitor, machiaj, blatul comodei TV)', N['STJ18'], 'placă', 285.00, 'Hornbach 285 lei',
        'https://www.hornbach.ro/c/lemn-ferestre-usi/constructie-mobilier/placi-pal/S14781/?f.brand=Kronospan', 307.07, 'Regency 307,07 lei',
        '3025 = Egger H1145 în tabelele de cant; alternativa mai ieftină K003 Gold Craft Oak 279 lei la Mambricolaj (alt ton).')
set_row('M068', 'Blat bucătărie Kronospan 3025 WO stejar Sonoma 4100 × 600 × 38 mm', 1, 'buc', 557.48, 'Regency 557,48 lei',
        'https://regencycompany.ro/kronospan', 597.95, 'Mambricolaj K003 FP 597,95 lei', 'Se folosesc 2620 mm; din rest ies pervazuri / poliță.')
R = C['variante']['Regency']['pe_categorii']; M = C['variante']['Mambricolaj']['pe_categorii']
cq = C['cantitati']
set_row('M067', 'Debitare pe foaie + cant ABS aplicat (%d foi PAL, %d HDF; %.0f m cant 2 mm, %.0f m 0,4–0,8 mm, %.0f m 42 × 2)' % (
            N['ALB18'] + N['CAS18'] + N['STJ18'] + N['ALB16'], N['HDF3'], sum(v for k, v in cq['cant'].items() if '22x2' in k),
            sum(v for k, v in cq['cant'].items() if '22x0.4' in k), sum(v for k, v in cq['cant'].items() if '42x2' in k)),
        1, 'lot', R['Debitare'] + R['Cant'], 'tarife Mambricolaj + cant Regency', 'https://www.mam-bricolaj.ro/catalog/servicii-oferite-717',
        M['Debitare'] + M['Cant'], 'Mambricolaj (debitare 45,95 lei/foaie, cantuire 3,95 lei/m + cant)',
        'Cantități exacte din lista de piese R03 (cu 4 cm pierdere pe muchie). La Regency, prețul serviciilor se confirmă din fișierul lor de optimizare.')
set_row('M104', 'Prelucrări la atelier: %d găuri balama Ø35, decupaj chiuvetă + plită, dublare blaturi (%s m²)' % (cq['balamale'], str(cq['dublare_m2']).replace('.', ',')), 1, 'lot',
        R['Prelucrări'], 'Mambricolaj: 5,95 lei/gaură, 74,95 lei/decupaj, 19,95 lei/m²', 'https://www.mam-bricolaj.ro/catalog/servicii-oferite-717',
        R['Prelucrări'], 'idem', 'Găurile de confirmat și pini le face montatorul cu șablon (manoperă).')
# balamale corectate după tabelul Blum (5 pe ușile de 2068 mm la dressing; 22 la bucătărie)
r = ROWS['M072']; r['pmin'] = round(r['pmin'] + 5 * 7.50 + 5 * 0.85, 2); r['pmax'] = round(r['pmax'] + 5 * 7.50 + 5 * 0.85, 2)
r['art'] = r['art'].replace('30 balamale', '35 balamale'); r['note'] = r['note'] + ' R04: +5 × 70T3650 + 5 plăcuțe (5 balamale pe ușile de 2068 mm).'
r = ROWS['M074']; r['pmin'] = round(r['pmin'] - 2 * 7.50 - 2 * 0.85, 2); r['pmax'] = round(r['pmax'] - 2 * 7.50 - 2 * 0.85, 2)
r['art'] = r['art'].replace('24 balamale', '22 balamale'); r['note'] = r['note'] + ' R04: 22 balamale (2 + 2 + 2 + 2 + 4 × 3 + 2).'

# ---------------------------------------------------------------- dormitorul refăcut de Codex (06.10.2026)
# noptiera de sud e scoasă: M076 pierde 2 × MOVENTO 760H3500S + 2 × TIP-ON BLUMOTION S1 + 2 × cleme (prețurile din rând)
r = ROWS['M076']; k = r['pmax'] / r['pmin']; d = 2 * 118.99 + 2 * 85.83 + 2 * 6.00
r['pmin'] = round(r['pmin'] - d, 2); r['pmax'] = round(r['pmax'] - d * k, 2)
r['art'] = r['art'].replace('Noptiere, comode TV', 'Noptieră, comode TV').replace('8 sertare MOVENTO', '6 sertare MOVENTO')
r['note'] = r['note'] + ' R04: noptiera de sud e scoasă din model (−2 MOVENTO, −2 TIP-ON BLUMOTION, −2 cleme).'
HW = [(20, 'balama Blum CLIP top BLUMOTION 71B3550 (uși cu mâner)', 14.54, 16.77), (20, 'plăcuță 173L6100', 0.85, 0.85),
      (8, 'pereche glisiere cu bile 450 mm, extragere totală, soft-close (GTV Versalite Plus+)', 35.75, 56.80),
      (2, 'suport pantaloni extractibil, montaj lateral, pentru lumina de 527,5 mm', 145.00, 196.00),
      (2, 'bară ovală 1 m', 6.11, 6.11), (4, 'suport bară', 0.76, 0.76), (40, 'pin raft Ø5', 0.10, 0.10),
      (4, 'anti-răsturnare', 5.00, 5.00), (8, 'picior H100', 1.25, 1.25), (4, 'clemă soclu', 2.00, 2.00),
      (1, 'soclu negru 80 mm × 2,2 m (profil PVC / aluminiu)', 120.00, 200.00), (4, 'mâner negru 240 mm (uși)', 20.00, 40.00),
      (8, 'mâner negru 120 mm (sertare interioare)', 10.00, 20.00), (6, 'organizator / separatoare sertar', 25.00, 45.00),
      (1, 'distribuitor LED 24 V cu 4 ieșiri', 25.00, 45.00),
      (1, 'corp spate pat: bordură aluminiu negru 20 mm × 1,6 m + 4 prinderi de perete', 60.00, 110.00),
      (90, 'confirmat', 0.10, 0.10), (60, 'capac', 0.05, 0.05), (8, 'colțar', 1.00, 1.00), (3, 'șuruburi ×100', 8.00, 8.00)]
new = dict(cat=ROWS['M076']['cat'],
           art='Dulap dormitor nou (Codex) + corp spate pat: 20 balamale BLUMOTION, 8 perechi glisiere, 2 suporturi pantaloni, mânere, soclu, accesorii',
           q=1, um='set', pmin=round(sum(n * a for n, _, a, _ in HW), 2), pmax=round(sum(n * b for n, _, _, b in HW), 2), st=E,
           note='Cantități și prețuri: ' + '; '.join('%d × %s %s' % (n, t, ('%.2f' % a).replace('.', ',')) for n, t, a, _ in HW) + '. '
                'Balama 14,54 lei Feromob / 16,77 Regency; glisiere 35,75 lei perechea (Concris) / 56,80 (Maxdeco); suport pantaloni 145–196 lei. '
                'Mânerele, soclul și organizatoarele sunt estimate. Sertarele interioare sunt provizorii: feroneria finală se alege după '
                'rezolvarea atingerii cu balamalele.',
           url='https://www.feromob.ro/product/balama-blum-clip-aplicata-110-grade-cu-blumotion-incorporat/', id='M105', etapa='E4', sapt=3,
           magazin='Feromob, Concris, Amoshop (06.10.2026)', magazin_alt='Regency, Maxdeco',
           price_basis='Cea mai bună ofertă: Feromob 71B3550 14,54 lei, GTV Versalite Plus+ 450 mm 35,75 lei/pereche; '
                       'alternativă: Regency 16,77 lei, Maxdeco 56,80 lei/pereche (%s)' % DT)
art = dict(cat=ROWS['M093']['cat'], art='Tablou canvas 110 × 70 cu ramă neagră (dormitor, deasupra patului – modelul Codex)', q=1, um='buc',
           pmin=250.00, pmax=450.00, st=E, note='Compoziție abstractă cu ocru, verde, bej și teracota, ca în model. Preț estimat pentru print pe pânză cu ramă.',
           url='', id='M106', etapa='E7', sapt=6, magazin='print canvas cu ramă (estimat)', magazin_alt='', price_basis='Estimat 250–450 lei (%s)' % DT)
D['rows'].insert(D['rows'].index(ROWS['M076']) + 1, new); ROWS['M105'] = new
D['rows'].insert(D['rows'].index(ROWS['M093']) + 1, art); ROWS['M106'] = art
# coloana de scurgere Ø110 a mașinii de spălat (existentă) izolată fonic, în colțul vestibul–sufragerie
iz = dict(cat=ROWS['M076']['cat'], art='Izolație fonică coloană de scurgere Ø110 (vestibul): vată minerală 40 mm + membrană fonică + mască gips-carton 2 × 12,5 mm, ~245 × 245 × 2500',
          q=1, um='set', pmin=350.00, pmax=700.00, st=E,
          note='Estimat: ~3 m țeavă acoperită cu manșon fonic (vată 40 mm + folie fonică), 2 plăci GKB 12,5 × 2 straturi pe profile CW/UW, șuruburi, bandă, glet; trapă de acces la mufă. '
               'Poziția coloanei (model: axa X 3450, Y −5450) se măsoară; izolația fonică nu înlocuiește etanșarea trecerii prin planșeu.',
          url='', id='M107', etapa='E4', sapt=3, magazin='materiale de construcții (estimat)', magazin_alt='', price_basis='Estimat 350–700 lei (%s)' % DT)
D['rows'].insert(D['rows'].index(ROWS['M105']) + 1, iz); ROWS['M107'] = iz
# LED-ul dulapului nou: 4 profile verticale de 1,2 m cu senzor de ușă și o sursă de 60 W (sursa noptierei scoase trece la dulap)
r = ROWS['M036']; r['q'] += 1; r['art'] = r['art'].replace('(45 m)', '(50 m)'); r['note'] += ', dulap dormitor (4 × 1,2 m)'
r = ROWS['M037']; r['q'] += 4; r['art'] = r['art'].replace('(40 m)', '(48 m)')
r['note'] = (r['note'] + ' ' if r['note'] else '') + '+4 bare pentru profilele de 1,2 m din dulapul de dormitor.'
r = ROWS['M039']; r['q'] += 4; r['art'] = r['art'].replace('dressing 5)', 'dressing 5, dulap dormitor 4)')
r = ROWS['M038']; r['note'] = r['note'].replace('+ 2 noptiere F08A/F08B', '+ noptiera F08A + dulapul nou de dormitor (noptiera F08B e scoasă)')

# ---------------------------------------------------------------- totaluri, etape, plăți (aceleași reguli ca R03)
STAGES = [(s['cod'], s['nume'], s['sapt']) for s in D['etape']]
for r in D['rows']:
    r['tmin'] = round(r['q'] * r['pmin'], 2)
    r['tmax'] = round(r['q'] * r['pmax'], 2)
cats = list(dict.fromkeys(r['cat'] for r in D['rows']))
D['summary'] = [dict(cat=c, tmin=round(sum(r['tmin'] for r in D['rows'] if r['cat'] == c), 2), tmax=round(sum(r['tmax'] for r in D['rows'] if r['cat'] == c), 2),
                     n=sum(r['cat'] == c for r in D['rows']), ver=sum(r['cat'] == c and r['st'] == V for r in D['rows'])) for c in cats]
D['old_total'] = [json.loads(R03.read_text(encoding='utf-8'))[k] for k in ('tot_min', 'tot_max')]
D['tot_min'] = round(sum(s['tmin'] for s in D['summary']), 2)
D['tot_max'] = round(sum(s['tmax'] for s in D['summary']), 2)
D['ver_sum'] = round(sum(r['tmin'] for r in D['rows'] if r['st'] == V), 2)
D['revision'] = 'R04'
D['date'] = DT
WEEKS = [('S0', datetime.date(2026, 10, 5))] + [('S%d' % k, datetime.date(2026, 10, 5) + datetime.timedelta(weeks=k)) for k in range(1, 9)]
st_rows = []
for code, name, wk in STAGES:
    rs = [r for r in D['rows'] if r['etapa'] == code]
    old = next(s for s in D['etape'] if s['cod'] == code)
    st_rows.append(dict(cod=code, nume=name, sapt=wk, n=len(rs), tmin=round(sum(r['tmin'] for r in rs), 2), tmax=round(sum(r['tmax'] for r in rs), 2), sapt_txt=old['sapt_txt']))
cash = collections.OrderedDict((w, [0.0, 0.0]) for w, _ in WEEKS)
what = collections.defaultdict(set)
for r in D['rows']:
    if r['sapt'] is None:
        for k in range(1, 8):
            cash['S%d' % k][0] += r['tmin'] / 7; cash['S%d' % k][1] += r['tmax'] / 7; what['S%d' % k].add('transport')
    else:
        cash['S%d' % r['sapt']][0] += r['tmin']; cash['S%d' % r['sapt']][1] += r['tmax']; what['S%d' % r['sapt']].add(r['etapa'])
D['etape'] = st_rows
D['cashflow'] = [dict(sapt=w, data=d.strftime('%d.%m.%Y'), tmin=round(cash[w][0], 2), tmax=round(cash[w][1], 2), ce=', '.join(sorted(what[w]))) for w, d in WEEKS]
D['notes'] = [n for n in D['notes'] if not n.startswith('R04:')] + [
    'R04: plăcile de mobilier trec pe Kronospan (8685 BS, 5981 BS, 3025 SN, 8685 SM 16 mm, HDF alb), cu cantitățile din planul de debitare R03 '
    '(lista completă de piese, inclusiv bucătăria și dormitorul refăcut de Codex: dulap nou, corp în spatele patului, o singură noptieră) '
    'și tarifele actuale de debitare pe foaie și căntuire pe metru.']
SRC.write_text(json.dumps(D, ensure_ascii=False, indent=2), encoding='utf-8')

# ---------------------------------------------------------------- Excel R04: aceeași structură ca R03
src = (ROOT / 'scripturi/deviz_R03_oferte_etape.py').read_text(encoding='utf-8')
xl = src.split('# ================================================================ Excel R03')[1].split("print('R03'")[0]
xl = xl.replace('Deviz materiale R03', 'Deviz materiale R04').replace('Deviz_materiale_ap184_R03.xlsx', 'Deviz_materiale_ap184_R04.xlsx')
xl = xl.replace('verificat online pe 05.10.2026', 'verificat online pe 05–06.10.2026')
TL = json.loads((ROOT / 'tmp/timeline.json').read_text(encoding='utf-8'))
G = dict(D=D, st_rows=st_rows, WEEKS=WEEKS, TLJ=TL['tasks'], V=V, ROOT=ROOT, datetime=datetime, collections=collections)
exec('from openpyxl import Workbook\nfrom openpyxl.styles import Font, PatternFill, Alignment, Border, Side\n' + xl, G)
print('R04 | oferte %.0f | alternativă %.0f | cu rezervă %.0f – %.0f | R03 %.0f – %.0f' % (
    D['tot_min'], D['tot_max'], D['tot_min'] * (1 + D['rez']), D['tot_max'] * (1 + D['rez']), *D['old_total']))
for i in ('M062', 'M063', 'M064', 'M065', 'M066', 'M067', 'M068', 'M104', 'M072', 'M074', 'M076', 'M105', 'M106', 'M107', 'M036', 'M037', 'M039'):
    r = ROWS[i]
    print(' ', i, r['q'], r['pmin'], r['tmin'], '|', r['tmax'], '|', r['art'][:70])
