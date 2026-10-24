"""Plan de lucrări cu calendar (Gantt), drum critic și cumpărături pe săptămâni, în stilul planșelor A3.
Date: tmp/timeline.json și tmp/deviz.json (din deviz_R03_oferte_etape.py). Rulează cu Python-ul care are reportlab.
Iese: output/pdf/Apartament_184_Plan_lucrari_R01.pdf"""
from pathlib import Path
import json, datetime, html
ROOT = Path(__file__).resolve().parents[1]
prefix = (ROOT / 'scripturi/plan_termic_pdf.py').read_text(encoding='utf-8').split('# T00')[0]
prefix = prefix.replace("OUT=ROOT/'output/pdf/Apartament_184_Plan_termic_R01.pdf'", "OUT=ROOT/'output/pdf/Apartament_184_Plan_lucrari_R01.pdf'")
prefix = prefix.replace("COORDONARE ȘI OFERTARE - NU PLAN DE EXECUȚIE VALIDAT", "PLAN DE LUCRĂRI ȘI CUMPĂRĂTURI | DATE ORIENTATIVE")
exec(prefix)
c.setTitle('Apartament 184 - Plan de lucrari si calendar - R01')
TLD = json.loads((ROOT / 'tmp/timeline.json').read_text(encoding='utf-8'))
DV = json.loads((ROOT / 'tmp/deviz.json').read_text(encoding='utf-8'))
T0 = datetime.date(2026, 10, 5); T1 = datetime.date(2026, 12, 6)
NDAYS = (T1 - T0).days
FAZ = {'Pregătire': HexColor('#9aa7b0'), 'Instalații': HexColor('#277dba'), 'Pereți': HexColor('#c27a2c'), 'Pardoseli': HexColor('#7a3fa0'),
       'Mobilier': TEAL, 'Finisare': HexColor('#3d8b37')}
esc = lambda s: html.escape(str(s))


def lei(v):
    return '{:,.0f}'.format(v).replace(',', '.')


# ---------------------------------------------------------------- P01 calendar
start('L01', 'Calendarul lucrărilor', 'Start luni 12.10.2026 · final ~27.11.2026 · o săptămână de rezervă până la 04.12.2026 · zile lucrătoare, fără manoperă detaliată')
X0, XW, Y0, RH = 470, 680, 160, 20.5
k = XW / NDAYS
X = lambda dte: X0 + (dte - T0).days * k
for w, ws in TLD['weeks']:
    d0 = datetime.date.fromisoformat(ws)
    x = X(d0)
    rect(x, Y0 - 22, 7 * k, len(TLD['tasks']) * RH + 22, fill=HexColor('#f4f6f7') if int(w[1:]) % 2 == 0 else white, stroke=white, lw=.1)
    txt(x + 3, Y0 - 10, '%s · %s' % (w, d0.strftime('%d.%m')), 8.5, INK, True)
for dd in range(NDAYS):                                                   # weekend
    dte = T0 + datetime.timedelta(days=dd)
    if dte.weekday() >= 5:
        rect(X(dte), Y0, k, len(TLD['tasks']) * RH, fill=HexColor('#e9edef'), stroke=HexColor('#e9edef'), lw=.1)
for i, t in enumerate(TLD['tasks']):
    y = Y0 + i * RH
    s0, e0 = datetime.date.fromisoformat(t['start']), datetime.date.fromisoformat(t['end'])
    col = FAZ.get(t['faza'], MUT)
    txt(42, y + 13, t['faza'], 8, col, True)
    act = t['act'] if pdfmetrics.stringWidth(t['act'], 'Segoe', 8.5) < 360 else t['act'][:86] + '…'
    txt(102, y + 13, act, 8.5, INK)
    line(42, y + RH, X0 + XW, y + RH, GRAY, .3)
    rect(X(s0), y + 4, max((e0 - s0).days + 1, 1) * k, RH - 8, fill=col, stroke=col, lw=.1)
    lab = s0.strftime('%d.%m') + ('–' + e0.strftime('%d.%m') if e0 != s0 else '')
    lx = X(e0) + k + 3
    if lx + pdfmetrics.stringWidth(lab, 'Segoe', 7.5) > W - 42:            # la marginea din dreapta: eticheta trece în stânga barei
        lx = X(s0) - 3 - pdfmetrics.stringWidth(lab, 'Segoe', 7.5)
    txt(lx, y + 13, lab, 7.5, MUT)
for lab, dte, col in (('start lucrări', datetime.date(2026, 10, 12), RED), ('șapă + comandă mobilier', datetime.date(2026, 10, 26), RED),
                      ('Black Friday', datetime.date(2026, 11, 13), RED), ('final', datetime.date(2026, 11, 27), RED)):
    x = X(dte) + k / 2
    line(x, Y0 - 2, x, Y0 + len(TLD['tasks']) * RH, col, .8, [3, 2])
yl = Y0 + len(TLD['tasks']) * RH + 22
lx = 42
for f, col in FAZ.items():
    rect(lx, yl - 9, 12, 10, fill=col, stroke=col); txt(lx + 16, yl, f, 9, MUT); lx += 30 + pdfmetrics.stringWidth(f, 'Segoe', 9) + 10
txt(lx + 10, yl, 'Linii roșii: start 12.10 · șapă și comanda mobilierului 26.10 · Black Friday 13.11 · final 27.11 · gri = weekend', 9, RED)
end()

# ---------------------------------------------------------------- P02 drum critic si conditii
start('L02', 'Drumul critic și condițiile de care depinde calendarul', 'Ce poate întârzia lucrarea și ce trebuie rezolvat înainte')
rows = [['', 'Condiție', 'Ce faci și când'],
        ['1', 'Încălzirea pornește de obicei la jumătatea lui octombrie', 'Radiatoarele noi și racordurile se fac în prima săptămână (13–15.10). Golirea coloanei se programează din timp cu asociația.'],
        ['2', 'Șapa autonivelantă trebuie să se usuce', 'Șapa se toarnă pe 26.10. Microcimentul și epoxidul încep după cel puțin 5–7 zile, parchetul după ~14 zile (09.11), cu umiditatea măsurată.'],
        ['3', 'Atelierul de debitare are nevoie de ~10 zile lucrătoare', 'Comanda pleacă pe 26.10, cu cotele remăsurate după tencuieli. Piesele vin în jur de 09–10.11, montajul începe pe 16.11.'],
        ['4', 'Dulapul din hol are nevoie de tavan ≥ 2480 mm', 'Se măsoară în prima săptămână. Dacă e mai jos, se ajustează lista de debitare înainte de 26.10.'],
        ['5', 'Routerul / ONT propus în spatele dulapului din hol', 'Se decide până la electricul brut (13–21.10): mutat sau cu acces în spatele dulapului.'],
        ['6', 'Plita pe gaz se racordează doar de o firmă autorizată', 'Programare pentru 18–21.11, odată cu montajul bucătăriei; se păstrează aerisirea obligatorie.'],
        ['7', 'Instalația electrică se recepționează', 'Electrician ANRE: protecții în tablou și măsurători PRAM pe 12–14.11, înainte de mobilier.'],
        ['8', 'Black Friday (de regulă 6 sau 13.11 la eMAG)', 'Electrocasnicele și televizoarele se cumpără atunci; se montează abia pe 18–25.11, deci nu grăbesc lucrarea.'],
        ['9', 'Microcimentul din baie cere hidroizolație uscată', 'CL 51 pe 28–29.10, microcimentul de pe 02.11.'],
        ['10', 'Rezervă', 'Săptămâna 30.11–04.12 rămâne liberă pentru întârzieri de livrare sau uscare.']]
y = table(42, 150, [34, 380, 692], rows, 10) + 18
para(42, y, 1106, '<b>Ordinea nu se schimbă:</b> instalații → rigips și glet → șapă → hidroizolație → microciment / epoxid → vopsea → parchet → aparataj și obiecte sanitare → mobilier. '
     'Mobilierul vine pe pardoseala finită, iar dulapurile se măsoară din nou după glet.', 11)
end()

# ---------------------------------------------------------------- P03.. cumparaturi pe saptamani
ROWS = [r for r in DV['rows']]
WK = [w for w, _ in TLD['weeks']]
WD = dict(TLD['weeks'])
bysw = {}
for r in ROWS:
    bysw.setdefault('S%d' % r['sapt'] if r.get('sapt') else 'S1–S7', []).append(r)
order = [w for w in WK if w in bysw] + (['S1–S7'] if 'S1–S7' in bysw else [])
hdr = [['Săpt.', 'Etapă', 'Ce cumperi', 'Cant.', 'Unde (cea mai bună ofertă)', 'Total ofertă', 'Total alt.']]
W_ = [52, 40, 380, 70, 384, 90, 90]
page_rows, part = list(hdr), 0


def newpage():
    global part
    part += 1
    start('L%02d' % (2 + part), 'Ce cumperi în fiecare săptămână' + (' (%d)' % part if part > 1 else ''),
          'Cumpărături pe etape, la cele mai bune oferte găsite pe 05.10.2026 | totalurile fără rezervă | link-urile sunt în Excelul R03')


def flush(final=False):
    global page_rows
    t = Table([[Paragraph(str(v), styles[9]) for v in row] for row in page_rows], colWidths=W_, repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), LIGHT), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                           ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4), ('LINEBELOW', (0, 0), (-1, 0), 1, TEAL), ('LINEBELOW', (0, 1), (-1, -1), .3, GRAY)]))
    _, h = t.wrapOn(c, sum(W_), 2000)
    t.drawOn(c, 42, H - 150 - h)
    end()
    page_rows = list(hdr)


newpage()
for w in order:
    rs = bysw[w]
    tot = sum(r['tmin'] for r in rs), sum(r['tmax'] for r in rs)
    label = '%s<br/>%s' % (w, datetime.date.fromisoformat(WD[w]).strftime('%d.%m') if w in WD else 'pe parcurs')
    block = [[label, '', '<b>Total săptămână: %s – %s lei</b>' % (lei(tot[0]), lei(tot[1])), '', '', '', '']]
    for r in sorted(rs, key=lambda r: (r['etapa'], r['id'])):
        q = ('%g' % r['q']).replace('.', ',') + ' ' + r['um']
        where = r.get('magazin') or r.get('price_basis', '')
        where = where.replace(' (05.10.2026)', '')
        block.append(['', r['etapa'], esc(r['art']), q, esc(where[:150]), lei(r['tmin']), lei(r['tmax'])])
    for row in block:
        trial = page_rows + [row]
        t = Table([[Paragraph(str(v), styles[9]) for v in rr] for rr in trial], colWidths=W_)
        _, h = t.wrapOn(c, sum(W_), 3000)
        if h > 545:
            flush(); newpage()
        page_rows.append(row)
flush(final=True)

c.save()
print('PDF', OUT, PAGE, 'pagini')
