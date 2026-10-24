"""Plan de debitare (hărți de tăiere pe plăci) - dulap hol + comandă comună. Date din optimizare_debitare.py.
Ruleaza cu Python-ul care are reportlab. Iese: output/pdf/Apartament_184_Plan_debitare_R02.pdf (R02: + planșa de costuri și ateliere, prețuri din deviz R03)"""
from pathlib import Path
import json, sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripturi'))
from plan_comun import patch_prefix, DVR, where
prefix = (ROOT / 'scripturi/plan_termic_pdf.py').read_text(encoding='utf-8').split('# T00')[0]
prefix = prefix.replace("OUT=ROOT/'output/pdf/Apartament_184_Plan_termic_R01.pdf'", "OUT=ROOT/'output/pdf/Apartament_184_Plan_debitare_R02.pdf'").replace('R01 |', 'R02 |')
prefix = prefix.replace("COORDONARE ȘI OFERTARE - NU PLAN DE EXECUȚIE VALIDAT", "PLAN DE DEBITARE | COTE FINITE ÎN MM, CU CANT")
exec(patch_prefix(prefix))
c.setTitle('Apartament 184 - Plan de debitare - R02')
L = json.loads((ROOT / 'tmp/debitare_layout.json').read_text(encoding='utf-8'))
SL, SW = L['sheet']; TR = L['trim']; KF = L['kerf']
A, B, SEP = L['A'], L['B'], L['separat']
REST = HexColor('#fdf1e3'); RESTL = HexColor('#d9a066')
FILL = {'W1000': HexColor('#f4f5f3'), 'U702': HexColor('#d9d1c6'), 'HDF': HexColor('#eceae4'), 'H1145': HexColor('#d8b48a')}
SRC_COL = {'Dulap hol': HexColor('#9fd3cc'), 'Dressing': HexColor('#c6d8ef'), 'Spălătorie': HexColor('#e7d4ef'), 'Debara': HexColor('#f3e3b5'),
           'Baie': HexColor('#cfe6c4'), 'Noptiere': HexColor('#f2c9c0'), 'Comodă TV': HexColor('#d6d0f0'), 'Comodă TV dormitor': HexColor('#efd2b8'),
           'Bucătărie (fronturi)': HexColor('#bfe0e9')}
SC = {'W1000 18 mm': 'W18', 'U702 18 mm': 'U18', 'W1000 16 mm': 'W16', 'HDF 3 mm': 'HDF', 'H1145 18 mm': 'H18'}
DEC = {'W1000': 'Egger W1000 ST9 Premium White', 'U702': 'Egger U702 ST9 Cashmere Grey', 'HDF': 'HDF alb', 'H1145': 'Egger H1145 ST10 Stejar Bardolino natur'}


def fmt(v):
    return ('%.0f' % v) if abs(v - round(v)) < .05 else ('%.1f' % v).replace('.', ',')


def draw_sheet(x0, y0, k, placed, free, by_src=False, labels=True, mat='W1000'):
    rect(x0, y0, SL * k, SW * k, fill=HexColor('#fbfbfa'), stroke=INK, lw=.8)
    rect(x0 + TR * k, y0 + TR * k, (SL - 2 * TR) * k, (SW - 2 * TR) * k, stroke=GRAY, lw=.3)
    rests = []
    for fx, fy, fw, fh in free:
        if fw >= 150 and fh >= 150:
            rect(x0 + (TR + fx) * k, y0 + (TR + fy) * k, fw * k, fh * k, fill=REST, stroke=RESTL, lw=.4)
            rests.append((fw, fh))
            if labels and fw * k > 40 and fh * k > 14:
                s = '%s × %s' % (fmt(fw), fmt(fh))
                c.setFillColor(RESTL); c.setFont('Segoe', 7.5); c.drawCentredString(x0 + (TR + fx + fw / 2) * k, H - (y0 + (TR + fy + fh / 2) * k) - 3, s)
    for p in placed:
        col = SRC_COL.get(p['src'], LIGHT) if by_src else FILL[mat.split()[0]]
        rect(x0 + (TR + p['x']) * k, y0 + (TR + p['y']) * k, p['w'] * k, p['h'] * k, fill=col, stroke=INK, lw=.5)
        if labels:
            cx, cy = x0 + (TR + p['x'] + p['w'] / 2) * k, y0 + (TR + p['y'] + p['h'] / 2) * k
            big = p['w'] * k > 60 and p['h'] * k > 26
            c.setFillColor(INK); c.setFont('SegoeB', 10 if big else 7.5)
            c.drawCentredString(cx, H - cy + (2 if big else 1), p.get('inst', p['id']))
            c.setFont('Segoe', 8 if big else 6.5)
            if p['h'] * k > 18:
                c.drawCentredString(cx, H - cy - (10 if big else 7), '%s × %s%s' % (fmt(p['L']), fmt(p['W']), ' (R)' if p['rotated'] else ''))
    return rests


def area(pl):
    return sum(p['L'] * p['W'] for p in pl) / 1e6


# ---------------------------------------------------------------- D00 sumar
start('D00', 'Plan de debitare – dulap hol și comandă comună', 'Plăci 2800 × 2070 | margine 10 mm | pânză 4,4 mm | tăieturi drepte (ghilotină), ca la mașina de debitat')
tot_A = sum(r['n'] for r in A.values())
sep_tot = {}
for rr in list(SEP.values()) + [A]:
    for m, r in rr.items():
        sep_tot[m] = sep_tot.get(m, 0) + r['n']
tot_B, tot_S = sum(r['n'] for r in B.values()), sum(sep_tot.values())
for i, (t, v, s) in enumerate([('DULAP HOL', '%d plăci' % tot_A, 'listă exactă, gata de trimis la atelier'),
                               ('COMANDĂ SEPARATĂ', '%d plăci' % tot_S, 'fiecare corp comandat separat'),
                               ('COMANDĂ COMUNĂ', '%d plăci' % tot_B, '%d plăci mai puțin, aceleași piese' % (tot_S - tot_B))]):
    x = 42 + i * 372
    rect(x, 145, 352, 96, fill=LIGHT if i < 2 else HexColor('#e7f3f1'), stroke=GRAY, lw=.6)
    txt(x + 14, 170, t, 10, TEAL, True); txt(x + 14, 205, v, 22, INK, True); txt(x + 14, 228, s, 9, MUT)
rows = [['Material', 'Decor', 'Dulap hol', 'Utilizare', 'Toate corpurile, separat', 'Comandă comună', 'Utilizare comună']]
for m in sorted(B):
    a = A.get(m)
    rows.append([m, DEC[m.split()[0]], str(a['n']) if a else '–', ('%s %%' % fmt(a['util'])) if a else '–', str(sep_tot.get(m, 0)), '<b>%d</b>' % B[m]['n'], '%s %%' % fmt(B[m]['util'])])
y = table(42, 270, [110, 260, 90, 90, 160, 130, 120], rows, 10) + 22
ys = y
y = panel(42, y, 540, 'Cum s-a calculat',
          'Piesele sunt așezate automat pe plăci de 2800 × 2070 mm, cu 10 mm tăiați pe contur și 4,4 mm pierduți la fiecare tăietură. '
          'Toate tăieturile merg de la un capăt la altul al bucății, cum lucrează mașina de debitat. Decorurile W1000 și U702 sunt unicolore, deci piesele se pot roti (R); '
          'stejarul H1145 are fibră și nu se rotește. Rafturile trapez din colț (C09) se așază câte două, cap la cap, și se taie oblic la final.') + 14
panel(610, ys, 538, 'Ce înseamnă pentru atelier',
           'Debimax și Mambricolaj optimizează și ei, cu programul lor. Planul nostru arată câte plăci trebuie să plătești și <b>ce resturi mari rămân</b> '
           '(portocaliu în hărți), ca să le ceri înapoi sau să le folosești la alte corpuri. Pentru comanda comună, piesele celorlalte corpuri sunt măsurate din '
           'modelul 3D și se confirmă la listele lor de debitare. Corpurile bucătăriei nu sunt încă desfăcute pe plăci și lipsesc din calcul.')
end()

# ---------------------------------------------------------------- hărți dulap hol, 1:10
K = 72 / 25.4 / 10
sheet_no = 0
for m in ('W1000 18 mm', 'U702 18 mm', 'W1000 16 mm', 'HDF 3 mm'):
    r = A[m]
    for i, (pl, fr) in enumerate(zip(r['sheets'], r['free']), 1):
        sheet_no += 1
        start('D%02d' % sheet_no, 'Dulap hol – placa %s-%d (%s, %d din %d)' % (SC[m], i, m, i, r['n']),
              DEC[m.split()[0]] + ' | piesele cu cota finită L × l (cu cant) | (R) = piesă rotită | portocaliu = rest refolosibil', '1:10 la imprimare A3, 100%')
        rests = draw_sheet(42, 150, K, pl, fr, mat=m)
        dim(42, 150 + SW * K, 42 + SL * K, 150 + SW * K, '2800', 16)
        dim(42 + SL * K, 150, 42 + SL * K, 150 + SW * K, '2070', 14)
        x = 870
        used = area(pl)
        rows = [['Etichetă', 'L × l', 'Buc.']]
        cnt = {}
        for p in pl:
            key = (p['inst'], p['L'], p['W'])
            cnt[key] = cnt.get(key, 0) + 1
        for (cid, l1, w1), n in cnt.items():
            rows.append([cid, '%s × %s' % (fmt(l1), fmt(w1)), str(n)])
        y = table(x, 150, [80, 130, 68], rows, 10) + 16
        y += para(x, y, 278, '<b>Folosit:</b> %s m² din 5,80 m² (%d %%)' % (fmt(round(used, 2)), round(used / 5.796 * 100)), 10) + 8
        big = sorted([rr for rr in rests if rr[0] >= 300 and rr[1] >= 200], key=lambda t: -t[0] * t[1])[:5]
        if big:
            y += para(x, y, 278, '<b>Resturi mari de păstrat:</b><br/>' + '<br/>'.join('%s × %s mm' % (fmt(a), fmt(b)) for a, b in big), 10)
        end()

# ---------------------------------------------------------------- comanda comuna: miniaturi
KM = 72 / 25.4 / 42
items = [(m, i, pl, fr) for m in sorted(B) for i, (pl, fr) in enumerate(zip(B[m]['sheets'], B[m]['free']), 1)]
per_page = 15
for pg in range(0, len(items), per_page):
    start('D%02d' % (sheet_no + 1 + pg // per_page), 'Comandă comună – toate plăcile (%d / %d)' % (pg // per_page + 1, -(-len(items) // per_page)),
          'Culoarea arată corpul de mobilier; portocaliu = rest refolosibil | estimare din modelul 3D pentru corpurile fără listă de debitare', '1:42')
    for j, (m, i, pl, fr) in enumerate(items[pg:pg + per_page]):
        x0, y0 = 42 + (j % 5) * 222, 150 + (j // 5) * 185
        txt(x0, y0 - 6, '%s · placa %d / %d · %d %%' % (m, i, B[m]['n'], round(area(pl) / 5.796 * 100)), 8.5, INK, True)
        draw_sheet(x0, y0, KM, pl, fr, by_src=True, labels=False, mat=m)
    # legenda
    lx = 42
    for s, col in SRC_COL.items():
        rect(lx, H - 92, 10, 10, fill=col, stroke=INK, lw=.4); txt(lx + 14, H - 83, s, 8.5, MUT)
        lx += 24 + pdfmetrics.stringWidth(s, 'Segoe', 8.5) + 6
    end()
last = sheet_no + 1 + (len(items) - 1) // per_page

# ---------------------------------------------------------------- recomandari
start('D%02d' % (last + 1), 'Alinierea materialelor – recomandări', 'Ce schimbăm în comandă ca să plătim mai puține plăci')
rows = [['Material', 'Problema la dulapul de hol singur', 'Ce facem']]
rows.append(['U702 18 mm', 'ușile de 519 mm nu încap câte 4 pe lățimea plăcii, așa că a doua placă e folosită doar ~%d %%' % round(area(A['U702 18 mm']['sheets'][-1]) / 5.796 * 100),
             'Comandăm toate fronturile U702 odată (dressing, spălătorie, noptiere, comoda TV, baie, bucătărie): %d plăci în loc de %d.' % (B['U702 18 mm']['n'], sep_tot['U702 18 mm'])])
rows.append(['W1000 18 mm', 'placa a treia e folosită ~%d %%' % round(area(A['W1000 18 mm']['sheets'][-1]) / 5.796 * 100),
             'Restul merge la rafturile debaralei și ale spălătoriei: %d plăci în loc de %d (fără corpurile bucătăriei).' % (B['W1000 18 mm']['n'], sep_tot['W1000 18 mm'])])
rows.append(['W1000 16 mm', 'o placă întreagă pentru 2 cutii de sertar (~35 %)',
             'Toate cutiile de sertar din lemn (noptiere, spălătorie, eventual bucătărie) din aceeași placă de 16 mm; altfel cerem atelierului un rest de 16 mm.'])
rows.append(['HDF 3 mm', 'două plăci la ~47 %: spatele de 2376 mm nu încap două pe o placă',
             'Al doilea HDF se împarte cu spatele dressingului: %d plăci în loc de %d.' % (B['HDF 3 mm']['n'], sep_tot['HDF 3 mm'])])
if 'H1145 18 mm' in B:
    rows.append(['H1145 18 mm', 'fronturile de stejar din dormitor folosesc ~%d %% dintr-o placă' % round(B['H1145 18 mm']['util']),
                 'Cerem atelierului rest de H1145 sau tăiere din placa lor (plată pe m²); altfel restul de stejar rămâne pentru alte piese.'])
y = table(42, 145, [110, 430, 566], rows, 10) + 20
y = panel(42, y, 1106, 'Reguli pentru comandă',
          '1. Aceeași grosime și același decor în toate corpurile: carcase W1000 18 mm, fronturi U702 18 mm, sertare W1000 16 mm, spate HDF alb 3 mm, accente H1145.<br/>'
          '2. O singură comandă la un singur atelier pentru toate corpurile, ca resturile unuia să fie piese pentru altul.<br/>'
          '3. Piesele de peste 2780 mm (dressing: bază, blat, soclu, mască, spate) se împart în două, cu îmbinarea pe un despărțitor.<br/>'
          '4. Cerem în scris resturile peste 300 × 200 mm: sunt ale noastre, le-am plătit.<br/>'
          '5. Corpurile bucătăriei se adaugă după ce le desfacem pe plăci; abia atunci numărul final de plăci e sigur.') + 14
end()

# ---------------------------------------------------------------- costuri si ateliere (deviz R03)
start('D%02d' % (last + 2), 'Costuri: plăci, debitare, cant și găurire', 'Comanda comună pentru toate corpurile, la cele mai bune oferte găsite pe 05.10.2026 (deviz R03); prețuri cu TVA')
IDS = ['M062', 'M063', 'M064', 'M065', 'M066', 'M068', 'M067', 'M104', 'M069']
rows = [['Cod', 'Articol', 'Cant.', 'Preț unitar', 'Cea mai bună ofertă', 'Alternativă', 'Unde']]
for i in IDS:
    r = DVR[i]
    pu = lei2(r['pmin']) if r['q'] != 1 else '-'
    rows.append([i, '<b>' + esc(r['art']) + '</b>' + ('<br/><font color="#536473">' + esc(r['note']) + '</font>' if r.get('note') else ''),
                 qty(r), pu, lei(r['tmin']), lei(r['tmax']), dvlink(r)])
fer = ['M071', 'M072', 'M074', 'M075', 'M076']
rows.append(['M071–M076', '<b>Feronerie Blum pentru toate corpurile</b> (balamale, TIP-ON, MOVENTO, picioare, confirmat), calculată pe bucăți', '5 seturi', '-',
             lei(sum(DVR[i]['tmin'] for i in fer)), lei(sum(DVR[i]['tmax'] for i in fer)), 'Feromob, Triton, Darel, Regency (cel mai mic preț pe bucată)'])
tb = sum(DVR[i]['tmin'] for i in IDS + fer); ta = sum(DVR[i]['tmax'] for i in IDS + fer)
rows.append(['', '<b>Total mobilier la comandă (fără LED și electrocasnice)</b>', '', '', '<b>' + lei(tb) + '</b>', '<b>' + lei(ta) + '</b>', ''])
y = tbl(42, 145, [62, 470, 62, 66, 92, 76, 278], rows, 8, 3, total=True) + 16
para(42, y, 540, '<b>Cum comanzi</b><br/>1. Ceri ofertă la Mambricolaj și la Debimax cu fișierele Excel ale dulapului din hol, extinse cu celelalte corpuri, pentru toată comanda odată.<br/>'
     '2. Plăcile: cel mai mic preț găsit e la Regency (366,42 lei W1000 / U702). Dacă atelierul nu primește plăci aduse, le iei de la atelier (Mambricolaj 389,95 / 409,95 lei).<br/>'
     '3. Cant de 2 mm pe fronturi și muchiile vizibile, 0,8 mm pe socluri și cutii de sertar; găurirea (locașuri Ø35, confirmat) se cere odată cu debitarea.', 10)
para(620, y, 528, '<b>Calendar</b><br/>Comanda pleacă pe 26.10, cu cotele remăsurate după tencuieli și glet; piesele vin în jur de 09–10.11, montajul începe pe 16.11 (planul de lucrări R01).<br/><br/>'
     '<b>Ce nu e în preț</b><br/>Transportul, manopera de montaj și corpurile bucătăriei desfăcute pe plăci (sunt estimate la media celorlalte plăci până la desenul lor).', 10)
end()
c.save()
print('PDF', OUT, PAGE, 'pagini')
