"""Excel de comandă R03 pentru debitare + căntuire (toate corpurile, decoruri Kronospan).
Foi: Sumar | câte o foaie pe decor (lungime, lățime, bucăți, fibră 0/1, cant pe laturi – formatul cerut de ateliere,
inclusiv fișierul de optimizare Regency) | Costuri (aceleași cantități la Regency, Mambricolaj și Egger).
Date: tmp/lista_debitare_R03.json, tmp/debitare_layout_R03.json, tmp/cost_debitare_R03.json.
Iese: Debitare_R03_comanda.xlsx în folderul proiectului."""
import json
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
L = json.loads((ROOT / 'tmp/lista_debitare_R03.json').read_text(encoding='utf-8'))
Y = json.loads((ROOT / 'tmp/debitare_layout_R03.json').read_text(encoding='utf-8'))['materiale']
C = json.loads((ROOT / 'tmp/cost_debitare_R03.json').read_text(encoding='utf-8'))
DEC = {'ALB18': ('Alb 18', 'Kronospan 8685 BS Snow White (Regency) / K8681 PE Brilliant White (Mambricolaj)', 'cant alb perlat 8685 / 101 PE'),
       'CAS18': ('Cashmere 18', 'Kronospan 5981 BS Cashmere', 'cant 5981 = Egger U702'),
       'STJ18': ('Stejar 18', 'Kronospan 3025 SN Sonoma (Regency) / K003 PW Gold Craft Oak (Mambricolaj)', 'cant 3025 = Egger H1145 / K003'),
       'ALB16': ('Alb 16', 'Kronospan 8685 SM 16 mm', 'cant alb 0,8 mm'),
       'HDF3': ('HDF', 'HDF lăcuit alb 110 PE 2,5 mm (sau HDF alb 3 mm)', '-'),
       'BLAT38': ('Blat 38', 'Blat Kronospan 3025 WO / K003 FP 4100 × 600 × 38', 'cant 42 × 2 la capăt')}
HDR = Font(bold=True, color='FFFFFF'); HFILL = PatternFill('solid', fgColor='137A6E')
THIN = Side(style='thin', color='BFC7CC'); B = Border(bottom=THIN)
ED = {'2': '2 mm', '0.8': '0,8 mm', '42': '42×2 mm', '-': ''}
wb = Workbook()
ws = wb.active; ws.title = 'Sumar'
ws.append(['Apartament 184 – comandă debitare și căntuire R03 (06.10.2026)'])
ws['A1'].font = Font(bold=True, size=14)
ws.append(['Cote FINITE în mm, cu cantul inclus. Stejarul are fibra pe lungime (fibră = 1). L1/L2 = laturile lungi, W1/W2 = laturile scurte.'])
ws.append([])
ws.append(['Material', 'Decor', 'Cant asortat', 'Plăci 2800×2070', 'Piese', 'm² piese', 'Utilizare %'])
for c in ws[4]:
    c.font = HDR; c.fill = HFILL
for m in ('ALB18', 'CAS18', 'STJ18', 'ALB16', 'HDF3', 'BLAT38'):
    r = Y[m]
    ws.append([DEC[m][0], DEC[m][1], DEC[m][2], r['n'], r['pieces'], r['area'], r['util']])
ws.append([])
ws.append(['Cant (m, cu 4 cm pierdere/muchie)'])
ws.cell(ws.max_row, 1).font = Font(bold=True)
for k, v in C['cantitati']['cant'].items():
    ws.append([k, v])
ws.append(['Găuri balama Ø35', C['cantitati']['balamale']])
ws.append(['Tăieturi oblice', C['cantitati']['oblic']])
ws.append(['Blaturi dublate (m²)', C['cantitati']['dublare_m2']])
for col, w in zip('ABCDEFG', (34, 70, 32, 16, 8, 10, 12)):
    ws.column_dimensions[col].width = w

n = 0
for m in ('ALB18', 'CAS18', 'STJ18', 'ALB16', 'HDF3', 'BLAT38'):
    sh = wb.create_sheet(DEC[m][0])
    sh.append([DEC[m][1]]); sh['A1'].font = Font(bold=True, size=12)
    sh.append(['Nr', 'Cod', 'Mobilier', 'Denumire', 'Lungime L (mm)', 'Lățime W (mm)', 'Bucăți', 'Fibră (0/1)', 'Cant L1', 'Cant L2', 'Cant W1', 'Cant W2', 'Formă', 'Observații'])
    for c in sh[2]:
        c.font = HDR; c.fill = HFILL; c.alignment = Alignment(wrap_text=True, vertical='center')
    i = 0
    for p in L['piese']:
        if p['mat'] != m:
            continue
        i += 1; n += p['n']
        sh.append([i, p['cod'], p['mob'], p['den'], p['L'], p['W'], p['n'], 1 if p['fibra'] else 0,
                   ED[p['L1']], ED[p['L2']], ED[p['W1']], ED[p['W2']], p['forma'], p['note']])
        for c in sh[sh.max_row]:
            c.border = B
    sh.append([]); sh.append(['', '', '', 'Total bucăți', '', '', '=SUM(G3:G%d)' % (sh.max_row - 1)])
    for col, w in zip('ABCDEFGHIJKLMN', (5, 11, 22, 46, 13, 13, 8, 9, 9, 9, 9, 9, 9, 70)):
        sh.column_dimensions[col].width = w
    sh.freeze_panes = 'A3'
    sh.auto_filter.ref = 'A2:N%d' % (sh.max_row - 2)

cs = wb.create_sheet('Costuri')
cs.append(['Cost cu aceleași cantități (lei cu TVA, 06.10.2026)'])
cs['A1'].font = Font(bold=True, size=12)
for v in ('Regency', 'Mambricolaj', 'Egger_R03'):
    V = C['variante'][v]
    cs.append([]); cs.append([V['nume'], 'servicii: ' + V['servicii']]); cs.cell(cs.max_row, 1).font = Font(bold=True)
    cs.append(['Categorie', 'Articol', 'Calcul', 'Lei'])
    for c in cs[cs.max_row]:
        c.font = HDR; c.fill = HFILL
    for r in V['randuri']:
        cs.append([r['cat'], r['art'], r['calcul'], r['lei']])
    cs.append(['', 'TOTAL', '', V['total']]); cs.cell(cs.max_row, 2).font = Font(bold=True); cs.cell(cs.max_row, 4).font = Font(bold=True)
for col, w in zip('ABCD', (14, 48, 80, 12)):
    cs.column_dimensions[col].width = w
out = ROOT / 'Debitare_R03_comanda.xlsx'
wb.save(out)
print('XLSX', out, n, 'piese')
