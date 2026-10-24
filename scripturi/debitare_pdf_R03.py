"""Plan de debitare R03 – COMPLET (toate corpurile, inclusiv bucătăria desfăcută pe plăci), decoruri Kronospan.
Date: tmp/lista_debitare_R03.json (lista_debitare_R03.py), tmp/debitare_layout_R03.json (optimizare_debitare_R03.py),
tmp/cost_debitare_R03.json (cost_debitare_R03.py). Rulează cu Python-ul care are reportlab.
Iese: output/pdf/Apartament_184_Plan_debitare_R03.pdf"""
from pathlib import Path
import json, sys, collections
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripturi'))
from plan_comun import patch_prefix
prefix = (ROOT / 'scripturi/plan_termic_pdf.py').read_text(encoding='utf-8').split('# T00')[0]
prefix = prefix.replace("OUT=ROOT/'output/pdf/Apartament_184_Plan_termic_R01.pdf'", "OUT=ROOT/'output/pdf/Apartament_184_Plan_debitare_R03.pdf'").replace('R01 |', 'R03 |')
prefix = prefix.replace("COORDONARE ȘI OFERTARE - NU PLAN DE EXECUȚIE VALIDAT", "PLAN DE DEBITARE | COTE FINITE ÎN MM, CU CANT")
exec(patch_prefix(prefix))
c.setTitle('Apartament 184 - Plan de debitare - R03')
LST = json.loads((ROOT / 'tmp/lista_debitare_R03.json').read_text(encoding='utf-8'))
LAY = json.loads((ROOT / 'tmp/debitare_layout_R03.json').read_text(encoding='utf-8'))
CST = json.loads((ROOT / 'tmp/cost_debitare_R03.json').read_text(encoding='utf-8'))
P = LST['piese']; MAT = LAY['materiale']; TR, KF = LAY['trim'], LAY['kerf']
DEC = {'ALB18': 'Alb 18 mm – Kronospan 8685 BS Snow White (Regency) / K8681 PE (Mambricolaj)',
       'CAS18': 'Cashmere 18 mm – Kronospan 5981 BS (echivalentul Egger U702)',
       'STJ18': 'Stejar 18 mm – Kronospan 3025 SN Sonoma (echivalentul H1145) / K003 PW',
       'ALB16': 'Alb 16 mm – Kronospan 8685 SM (cutii de sertar)',
       'HDF3': 'HDF lăcuit alb 2,5–3 mm (spate)',
       'BLAT38': 'Blat de lucru stejar 38 mm 4100 × 600 – Kronospan 3025 WO / K003 FP'}
SHORT = {'ALB18': 'Alb 18', 'CAS18': 'Cashmere 18', 'STJ18': 'Stejar 18', 'ALB16': 'Alb 16', 'HDF3': 'HDF', 'BLAT38': 'Blat 38'}
FILL = {'ALB18': HexColor('#f4f5f3'), 'CAS18': HexColor('#d9d3ca'), 'STJ18': HexColor('#dcc7a8'), 'ALB16': HexColor('#f1f3f4'),
        'HDF3': HexColor('#eceae4'), 'BLAT38': HexColor('#dcc7a8')}
MOBC = {'Dulap hol': '#9fd3cc', 'Dressing': '#c6d8ef', 'Spălătorie': '#e7d4ef', 'Dulap WC': '#cfe6c4', 'Noptieră': '#f2c9c0', 'Dulap dormitor': '#d9e7d2', 'Corp spate pat': '#e9d6c9',
        'Comodă TV cameră de zi': '#d6d0f0', 'Comodă TV dormitor': '#efd2b8', 'Machiaj': '#f6e2a8', 'Debara': '#f3e3b5', 'Bucătărie': '#bfe0e9'}
MOBC = {k: HexColor(v) for k, v in MOBC.items()}
REST = HexColor('#fdf1e3'); RESTL = HexColor('#d9a066')
ORDER = ['ALB18', 'CAS18', 'STJ18', 'ALB16', 'HDF3', 'BLAT38']
mobof = {p['cod']: p['mob'] for p in P}


def fmt(v):
    return ('%.0f' % v) if abs(v - round(v)) < .05 else ('%.1f' % v).replace('.', ',')


def ce(v):
    return {'2': '2', '0.8': '0,8', '42': '42/2', '-': '–'}[v]


def draw_sheet(x0, y0, k, m, sh):
    SL, SW = MAT[m]['sheet']
    tr = MAT[m]['trim']
    rect(x0, y0, SL * k, SW * k, fill=HexColor('#fbfbfa'), stroke=INK, lw=.8)
    if tr:
        rect(x0 + tr * k, y0 + tr * k, (SL - 2 * tr) * k, (SW - 2 * tr) * k, stroke=GRAY, lw=.3)
    for fx, fy, fw, fh in sh['free']:
        if fw >= 150 and fh >= 150:
            rect(x0 + (tr + fx) * k, y0 + (tr + fy) * k, fw * k, fh * k, fill=REST, stroke=RESTL, lw=.4)
    for p in sh['placed']:
        col = MOBC.get(p['mob'], LIGHT)
        rect(x0 + (tr + p['x']) * k, y0 + (tr + p['y']) * k, p['w'] * k, p['h'] * k, fill=col, stroke=INK, lw=.45)
        cx, cy = x0 + (tr + p['x'] + p['w'] / 2) * k, y0 + (tr + p['y'] + p['h'] / 2) * k
        if p['w'] * k > 34 and p['h'] * k > 14:
            c.setFillColor(INK); c.setFont('SegoeB', 6.8)
            c.drawCentredString(cx, H - cy + 1.5, p['cod'])
            if p['h'] * k > 24:
                c.setFont('Segoe', 6.3)
                c.drawCentredString(cx, H - cy - 6.5, '%s × %s%s' % (fmt(p['Lp']), fmt(p['Wp']), ' R' if p['rot'] else ''))


# ---------------------------------------------------------------- D00 sumar
V = CST['variante']
tot_pl = sum(MAT[m]['n'] for m in ORDER if m != 'BLAT38')
start('D00', 'Plan de debitare R03 – toate corpurile, decoruri Kronospan',
      'Piesă cu piesă din modelele FreeCAD (bucătăria, dulapul nou de dormitor, noptiera, comodele și sertarele desfăcute pe plăci) | verificat automat | prețuri 06.10.2026, cu TVA')
cards = [('PLĂCI DE CUMPĂRAT', '%d + 1 blat' % tot_pl, '%d alb, %d cashmere, %d stejar, %d alb 16, %d HDF' % tuple(MAT[m]['n'] for m in ('ALB18', 'CAS18', 'STJ18', 'ALB16', 'HDF3'))),
         ('PIESE', '%d' % sum(p['n'] for p in P), '%d poziții în listă, %d corpuri de mobilier' % (len(P), len({p['mob'] for p in P}))),
         ('COST REGENCY', lei(V['Regency']['total']) + ' lei', 'plăci + debitare + cant + găuri (servicii estimate)'),
         ('COST MAMBRICOLAJ', lei(V['Mambricolaj']['total']) + ' lei', 'tot cu tarifele lor publice')]
for i, (t, v, s) in enumerate(cards):
    x = 42 + i * 279
    rect(x, 145, 266, 92, fill=LIGHT if i < 2 else HexColor('#e7f3f1'), stroke=GRAY, lw=.6)
    txt(x + 12, 168, t, 9.5, TEAL, True); txt(x + 12, 202, v, 21, INK, True); txt(x + 12, 224, s, 8.5, MUT)
rows = [['Material', 'Decor propus', 'Plăci', 'Utilizare', 'Tăieturi', 'Piese']]
for m in ORDER:
    r = MAT[m]
    rows.append([SHORT[m], DEC[m], '<b>%d</b>' % r['n'], '%s %%' % fmt(r['util']), '%s m' % fmt(r['cut_m']), str(r['pieces'])])
y = tbl(42, 262, [80, 470, 50, 62, 70, 50], rows, 9) + 14
cq = CST['cantitati']
y = panel(42, y, 782, 'Cum s-a calculat și verificat',
          'Plăci 2800 × 2070 mm, <b>15 mm tăiați pe fiecare margine</b> (Regency primește piese de maximum 2770 × 2040), pânză 4,4 mm, tăieturi '
          'de la un capăt la altul (ghilotină), ca la mașina de debitat. Piesele uni se pot roti (R); stejarul nu, fibra merge pe lungimea plăcii. '
          'Pentru fiecare material s-au încercat peste 12.000 de așezări și s-a păstrat cea cu cele mai puține plăci. <b>Verificarea automată</b> confirmă că '
          'fiecare piesă apare o singură dată, stă în zona utilă și are pânza de 4,4 mm față de vecine, fără suprapuneri. '
          'Cant: %s m de 2 mm, %s m de 0,4–0,8 mm și %s m de 42 × 2 mm, cu 4 cm pierdere la fiecare muchie. %d găuri de balama Ø35 '
          '(după tabelul Blum: 2 balamale până la 900 mm, 3 până la 1600, 4 până la 2000, 5 peste).' % (
              fmt(sum(v for k, v in cq['cant'].items() if '22x2' in k)), fmt(sum(v for k, v in cq['cant'].items() if '22x0.4' in k)),
              fmt(sum(v for k, v in cq['cant'].items() if '42x2' in k)), cq['balamale'])) + 12
panel(842, 262, 306, 'Față de R02',
      '• bucătăria era estimată „la media plăcilor”; acum e desfăcută piesă cu piesă;<br/>'
      '• noptierele, comodele, machiajul și sertarele dressingului erau blocuri în model;<br/>'
      '• intră și dulapul nou de dormitor și corpul din spatele patului (modelate de Codex pe 06.10); noptiera de sud e scoasă;<br/>'
      '• debitarea se plătește pe foaie (45,95 lei la Mambricolaj), nu pe metru;<br/>'
      '• cantul are un preț de aplicare actual: 3,95 lei/m, plus cantul ales.')
end()

# ---------------------------------------------------------------- D01 reguli de construcție + note pentru atelier
start('D01', 'Reguli de construcție și note pentru atelier', 'Aceleași reguli la toate corpurile; ce trebuie confirmat înainte de comandă')
y = panel(42, 145, 540, 'Reguli (le respectă lista de piese)',
          '1. <b>Cote finite, cu cantul inclus</b>: atelierul scade grosimea cantului la debitare. Se scrie pe comandă.<br/>'
          '2. Cant: fronturi 2 mm pe toate laturile; muchia din față a pieselor de corp 2 mm; cutii de sertar 0,8 mm sus; muchiile ascunse fără cant. '
          'L1, L2 = laturile lungi, W1, W2 = laturile scurte (L1 = muchia vizibilă, scrisă în coloana Observații când contează).<br/>'
          '3. Stejarul: fibra pe L (prima cotă). La comanda Regency se pune „ține cont de fibră = 1”.<br/>'
          '4. Sertare Blum MOVENTO din PAL 16 mm: lățimea interioară = lumina corpului − 42 mm; laterala = lungimea glisierei − 10 mm; '
          'fundul de 16 mm stă între laterale, retras 13 mm; fața interioară și spatele = înălțimea laterală − 29 mm (se taie din resturile de 18 mm).<br/>'
          '5. Spate HDF bătut pe spate, cu 6 mm mai mic pe fiecare latură la bucătărie; la dressing, încastrat între laterale și îmbinat pe despărțitori.<br/>'
          '6. Piesele peste 2770 mm se împart: baza, blatul și spatele dressingului se îmbină pe despărțitori; soclul și masca bucătăriei la rostul M3/M4.<br/>'
          '7. Trapeze: rafturile de colț din hol (C09) și rafturile debaralei din dreapta intrării se taie câte două dintr-un dreptunghi, cu o tăietură oblică.') + 12
panel(610, 145, 538, 'De confirmat înainte de comandă',
      '• <b>Cotele pe șantier</b>, după tencuieli și glet (tavanul din hol ≥ 2480 mm, nișa bucătăriei 3220 mm, golul dressingului 3380 mm).<br/>'
      '• <b>Spălătoria</b> e în stadiu de concept: golurile din model (664 + 264 mm) cer <b>două</b> separatoare, nu unul; am pus două.<br/>'
      '• <b>Mașina de vase</b> e incorporabilă, deci primește front cashmere 597 × 716 (BJ-F02); înălțimea exactă se ia din fișa aparatului.<br/>'
      '• Decupajele pentru chiuvetă și plită: după fișele producătorilor.<br/>'
      '• <b>Blatul comodei TV</b> din camera de zi are 2 straturi de 18 mm lipite (36 mm, în model 25), cu cant de 42 mm; la fel blatul noptierei (36 mm, în model 40).<br/>'
      '• <b>Dormitorul</b> (Codex, 06.10): dulapul nou e în listă după modelul FreeCAD (4 uși albe, spatele HDF din 4 bucăți); '
      'corpul îngust din spatele patului are blat de stejar 3025; noptiera de sud e scoasă. Soclul negru și bordura de 20 mm sunt profile cumpărate.<br/>'
      '• <b>Cele 8 sertare interioare ale dulapului nou sunt PROVIZORII</b>: în model, fronturile stau la 20 mm de muchie și 4 dintre ele ating balamalele de jos '
      '(cotele 182–218 și 632–668 mm); cutia de 495,5 mm lasă 16 mm pe parte, iar glisierele cu bile cer 12,7. Se fixează după alegerea feroneriei '
      '(distanțiere pe partea balamalelor sau balamale fără intruziune). Am verificat: în toate variantele ies tot 17 plăci albe.<br/>'
      '• <b>Spatele dulapului din baie și al nișei de detergenți</b> e din PAL alb de 16 mm, nu din HDF: rezistă mai bine la umezeală.<br/>'
      '• Mambricolaj: plăcile Kronospan de 279 lei sunt „în stoc”; trebuie confirmat stocul pentru %d plăci albe. Regency: serviciile se ofertează din fișierul lor de optimizare.' % MAT['ALB18']['n'])
end()

# ---------------------------------------------------------------- D02 costuri
start('D02', 'Cost exact: plăci, debitare, cant, găuri', 'Aceleași cantități la toți furnizorii; prețuri cu TVA găsite online pe 06.10.2026')
rows = [['Categorie', 'Regency', 'Mambricolaj', 'Egger (prețurile devizului R03)']]
cats = ['Plăci', 'Debitare', 'Cant', 'Prelucrări']
for k in cats:
    rows.append([k] + [lei2(V[v]['pe_categorii'].get(k, 0)) + ' lei' for v in ('Regency', 'Mambricolaj', 'Egger_R03')])
rows.append(['<b>Total</b>'] + ['<b>%s lei</b>' % lei2(V[v]['total']) for v in ('Regency', 'Mambricolaj', 'Egger_R03')])
y = tbl(42, 145, [150, 200, 200, 230], rows, 10, total=True) + 14
rows = [['Rând', 'Calcul (Regency)', 'Lei']]
for r in V['Regency']['randuri']:
    rows.append([esc(r['art']), esc(r['calcul']), lei2(r['lei'])])
tbl(42, y, [230, 430, 120], rows, 8, 1.5)
_mix = sum(m['lei'] - r['lei'] for r, m in zip(V['Regency']['randuri'], V['Mambricolaj']['randuri']) if r['art'].startswith(('CAS', 'STJ')))
_dif = sorted(V['Egger_R03']['total'] - V[v]['total'] for v in ('Regency', 'Mambricolaj'))
panel(842, 145, 306, 'Ce înseamnă',
      '<b>Kronospan e cu %s–%s lei mai ieftin</b> decât Egger, la aceleași piese.<br/><br/>' % (lei(round(_dif[0], -1)), lei(round(_dif[1], -1)))
      + 
      '<b>Regency</b> are cele mai mici prețuri la plăci (8685 BS 264,10; 16 mm 257,59; HDF 83,79; blat 557,48) și la cant. '
      'Serviciile lor nu sunt publice: în tabel am pus tarifele Mambricolaj; costul exact îl dă fișierul lor de optimizare completat cu lista noastră.<br/><br/>'
      '<b>Mambricolaj</b> are toate tarifele publice: 45,95 lei / foaie PAL, 27,95 / foaie HDF, 3,95 lei/m aplicare cant 22 mm, 6,95 lei/m pentru 42 mm, '
      '5,95 lei / gaură de balama, 74,95 lei / decupaj. Plăcile Kronospan de 279 lei sunt în stoc.<br/><br/>'
      '<b>Mixt</b> (alb, 16 mm, HDF și blat de la Regency; cashmere și stejar de la Mambricolaj): plăcile ar fi mai ieftine, dar cantul de la Mambricolaj e mai scump; '
      'per total doar ~%s lei mai puțin, cu două comenzi și două debitări. Nu merită.' % lei(round(-_mix, -1)))
end()

# ---------------------------------------------------------------- hărți: 2 plăci pe pagină
items = [(m, i, sh) for m in ORDER for i, sh in enumerate(MAT[m]['sheets'], 1)]
pg = 3
for j in range(0, len(items), 2):
    pair = items[j:j + 2]
    start('D%02d' % pg, 'Hărți de tăiere – %s' % ' și '.join('%s %d/%d' % (SHORT[m], i, MAT[m]['n']) for m, i, _ in pair),
          'Cotele sunt finite (cu cant), L × W; R = piesă rotită; culoarea = corpul de mobilier; portocaliu = rest peste 150 × 150 mm', '≈1:15')
    for q, (m, i, sh) in enumerate(pair):
        SL, SW = MAT[m]['sheet']
        k = 535 / SL
        x0, y0 = 42 + q * 568, 160
        txt(x0, y0 - 8, '%s · placa %d din %d · folosit %s %% · tăieturi %s m' % (DEC[m].split(' – ')[0], i, MAT[m]['n'], fmt(sh['used']), fmt(sh['cut_m'])), 9, INK, True)
        draw_sheet(x0, y0, k, m, sh)
        cnt = collections.Counter((p['cod'], p['Lp'], p['Wp']) for p in sh['placed'])
        s = '; '.join('<b>%s</b> %s×%s%s' % (cod, fmt(a), fmt(b), (' ×%d' % n) if n > 1 else '') for (cod, a, b), n in sorted(cnt.items()))
        para(x0, y0 + SW * k + 12, 535, s, 8)
    lx = 42
    for s_, col in MOBC.items():
        rect(lx, H - 92, 9, 9, fill=col, stroke=INK, lw=.4); txt(lx + 12, H - 84, s_, 8, MUT)
        lx += 20 + pdfmetrics.stringWidth(s_, 'Segoe', 8) + 4
    end()
    pg += 1

# ---------------------------------------------------------------- lista de piese, pe corpuri
by = collections.OrderedDict()
for p in P:
    by.setdefault(p['mob'], []).append(p)
rows_all = []
for mob, ps in by.items():
    rows_all.append(('H', mob, sum(p['n'] for p in ps)))
    for p in ps:
        rows_all.append(('R', p))
PER = 30
chunk, chunks = [], []
for r in rows_all:
    chunk.append(r)
    if len(chunk) >= PER:
        chunks.append(chunk); chunk = []
if chunk:
    chunks.append(chunk)
for n, ch in enumerate(chunks, 1):
    start('D%02d' % pg, 'Lista de piese (%d / %d)' % (n, len(chunks)), 'Cote finite cu cant, mm | fibră L la stejar | canturi: 2 / 0,8 / 42 × 2 mm, – = fără')
    rows = [['Cod', 'Denumire', 'Material', 'L', 'W', 'Buc', 'L1', 'L2', 'W1', 'W2', 'Observații']]
    for r in ch:
        if r[0] == 'H':
            rows.append(['<b>%s</b>' % esc(r[1]), '<b>%d piese</b>' % r[2], '', '', '', '', '', '', '', '', ''])
        else:
            p = r[1]
            rows.append([p['cod'], esc(p['den']), SHORT[p['mat']], fmt(p['L']), fmt(p['W']), str(p['n']), ce(p['L1']), ce(p['L2']), ce(p['W1']), ce(p['W2']),
                         esc(p['note'])[:115]])
    tbl(42, 140, [74, 250, 70, 46, 46, 34, 34, 34, 34, 34, 444], rows, 8, 1.4)
    end()
    pg += 1

# ---------------------------------------------------------------- cant și balamale
start('D%02d' % pg, 'Cant și găuri de balama', 'Metri de cant pe decor și grosime (cu 4 cm pierdere la fiecare muchie) | balamale după înălțimea ușii')
rows = [['Decor', 'Cant', 'Metri', 'Unde']]
WH = {'ALB': 'corpuri albe (muchia din față), rafturi', 'CAS': 'fronturi, noptiere, comoda TV, soclu, măști', 'STJ': 'comoda TV dormitor, machiaj, blatul comodei TV, capătul blatului de lucru'}
for k, v in sorted(cq['cant'].items()):
    d, t = k.split()
    rows.append([{'ALB': 'alb (8685 / K8681)', 'CAS': 'cashmere 5981 (= U702)', 'STJ': 'stejar 3025 / K003'}[d], t.replace('x', ' × ') + ' mm', fmt(v) + ' m', WH[d]])
y = tbl(42, 145, [200, 100, 80, 400], rows, 10) + 16
DOORS = [('Dulap hol – uși jos (oglindă)', 4, 1699, 4), ('Dulap hol – uși sus', 4, 377, 2), ('Dressing – uși jos', 5, 2068, 5), ('Dressing – uși sus', 5, 377, 2),
         ('Spălătorie – uși sus', 2, 647, 2), ('Spălătorie – ușa tehnică', 1, 660, 2), ('Spălătorie – ușa de accesorii', 1, 1657, 4),
         ('Dulap WC', 2, 796, 2), ('Comodă TV cameră de zi', 3, 376, 2), ('Dulap dormitor', 4, 2276, 5), ('Bucătărie – M1, M3, M5 (716), M6 sus (573), S4 (756)', 5, 716, 2),
         ('Bucătărie – S1, S2, S3, S5 (956)', 4, 956, 3)]
rows = [['Uși', 'Buc', 'Latura cu balamale', 'Balamale / ușă', 'Total']]
for nm, n, hh, b in DOORS:
    rows.append([nm, str(n), '%d mm' % hh, str(b), str(n * b)])
rows.append(['<b>Total găuri Ø35 (CNC la atelier)</b>', '', '', '', '<b>%d</b>' % sum(n * b for _, n, _, b in DOORS)])
tbl(42, y, [420, 50, 130, 100, 80], rows, 10, total=True)
panel(842, 145, 306, 'Pentru comandă',
      'Fișierul Excel <b>Debitare_R03_comanda.xlsx</b> (în folderul proiectului) are aceeași listă, cu o foaie pe decor, gata de trimis la atelier '
      'sau de copiat în fișierul de optimizare Regency (lungime, lățime, bucăți, fibră 0/1, canturi pe laturi).<br/><br/>'
      'Găurile pentru confirmat, pini și plăcuțe de balama le face montatorul cu șablon, la montaj; la dulapul din hol există planul complet de găurire.')
end()
c.save()
print('PDF', OUT, PAGE, 'pagini')
