# Lista de achizitii instalatie electrica R11 -> output/Lista_achizitii_electric_R11.xlsx
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

R = Path(__file__).resolve().parents[1]
H, D, M, A = 'Hornbach', 'Dedeman', 'Micul Electrician', 'A2T'
# (categorie, material, necesar, cumperi, um, pret_unitar, magazin, link, status, observatii)
ROWS = [
 ('Copex', 'Copex Ø20 Gewiss 750 N, cu fir de tragere (forță)', '376 m', 4, 'colac 100 m', 108, H, 'https://www.hornbach.ro/p/copex-tub-flexibil-din-pvc-gewiss-o20mm-diam-ext-750n-lungime-100m-cu-fir-de-tragere/10254790/', 'verificat', 'Art. 10254790; interior 14,1 mm; în stoc la Domnești'),
 ('Copex', 'Copex Ø25 Gewiss 750 N, cu fir de tragere (date)', '50 m', 1, 'colac 75 m', 149, H, 'https://www.hornbach.ro/p/copex-tub-flexibil-din-pvc-gewiss-o25mm-diam-ext-750n-lungime-75m-cu-fir-de-tragere/10254791/', 'verificat', 'Art. 10254791; interior 18,3 mm'),
 ('Copex', 'Copex Ø16 Gewiss 750 N, cu fir de tragere (tavan, SELV)', '37 m', 1, 'colac 100 m', 96, H, 'https://www.hornbach.ro/p/copex-tub-flexibil-din-pvc-gewiss-o16mm-diam-ext-750n-lungime-100m-cu-fir-de-tragere/5624010/', 'verificat', 'Art. 5624010; interior 10,7 mm'),
 ('Conductoare 230 V', 'Conductor MYF H07V-K 2,5 mm² maro', '247 m', 260, 'm', 2.27, M, 'https://miculelectrician.ro/conductor-myf-flexibil-25-maro-h05v-k-h07v-k', 'verificat', 'Minim 100 m. Alternativ Hornbach colac 100 m, 191 lei (art. 8584094)'),
 ('Conductoare 230 V', 'Conductor MYF H07V-K 2,5 mm² albastru', '247 m', 260, 'm', 2.27, M, 'https://miculelectrician.ro/conductor-myf-flexibil-25-albastru-h05v-k-h07v-k', 'verificat', 'Minim 100 m. Alternativ Hornbach colac 100 m, 191 lei (art. 8584093)'),
 ('Conductoare 230 V', 'Conductor MYF H07V-K 2,5 mm² verde-galben', '247 m', 260, 'm', 2.27, M, 'https://miculelectrician.ro/conductor-myf-flexibil-25-verde-galben-h05v-k-h07v-k', 'verificat', 'Minim 100 m. La Hornbach indisponibil online'),
 ('Conductoare 230 V', 'Conductor MYF H07V-K 1,5 mm² maro', '108 m', 120, 'm', 1.41, M, 'https://miculelectrician.ro/conductor-myf-flexibil-15-maro-h05v-k-h07v-k', 'verificat', 'Minim 100 m'),
 ('Conductoare 230 V', 'Conductor MYF H07V-K 1,5 mm² albastru', '155 m', 170, 'm', 1.45, H, 'https://www.hornbach.ro/p/conductor-myf-h07v-k-1-5mm-albastru/7769467/', 'verificat', 'La metru, fără minim'),
 ('Conductoare 230 V', 'Conductor MYF H07V-K 1,5 mm² verde-galben', '155 m', 170, 'm', 1.45, H, 'https://www.hornbach.ro/p/conductor-myf-h07v-k-1-5mm-verde-galben/5122078/', 'verificat', 'La metru, fără minim'),
 ('Conductoare 230 V', 'Conductor MYF H07V-K 1,5 mm² negru', '56 m', 1, 'colac 100 m', 96.9, H, 'https://www.hornbach.ro/p/conductor-myf-h07v-k-1-5mm-negru-inel-100m/8584090/', 'verificat', 'Retururi comandă'),
 ('Conductoare 230 V', 'Conductor MYF H07V-K 1,5 mm² roșu (în loc de gri: naveta B, retur ventilator)', '17 m', 20, 'm', 1.26, D, 'https://www.dedeman.ro/ro/conductor-electric-myf/-h07v-k-1-5-mmp-rosu-cupru/p/1014038', 'de verificat', 'Gri nu se găsește la 1,5 mm²; preț ~1,26 lei/m'),
 ('Aer condiționat', 'Cablu MYYM (H05VV-F) 4×1,5 mm², legătură unitate interioară–exterioară (după fișa producătorului)', '4 m', 5, 'm', 4.90, H, 'https://www.hornbach.ro/p/cablu-myym-h05vv-f-4x1-5-mm-alb/7473995/', 'verificat', 'Vândut la metru; verifică tipul cerut de producătorul AC'),
 ('Aer condiționat', 'Kit instalare AC: conducte Cu izolate 1/4"+3/8", consolă exterioară, țeavă condens Ø16', '—', 1, 'set', None, 'montator AC', '', 'de verificat', 'De obicei în oferta montatorului; montajul, vidul și testul cu azot tot la el'),
 ('Curenți slabi', 'Cablu UTP Cat6, 100 % cupru, 24 AWG, rolă 100 m (Safer)', '49 m', 1, 'rolă 100 m', 299.99, A, 'https://www.a2t.ro/cabluri-de-retea/cablu-utp-cat6-din-cupru-23awg-izolatie-pvc-rola-100m-safer-adm-utp6-4x2x0-51-100m.html', 'verificat', 'Pe comandă. Nu CCA. Înlocuiește rola de 305 m din deviz'),
 ('Curenți slabi', 'Cablu coaxial TV RG6/U, ecranare triplă', '36 m', 40, 'm', 1.49, H, 'https://www.hornbach.ro/p/cablu-tv-coaxial-rg6-u-1-02mm-85db-alb-ecranare-tripla/5605892/', 'verificat', 'Art. 5605892; vândut la metru'),
 ('Curenți slabi', 'Cablu MYYM 2×1 mm² (LED 24 V, V01)', '4 m', 5, 'm', 2.30, H, 'https://www.hornbach.ro/p/cablu-myym-h05vv-f-2x1-mm-alb/8586043/', 'verificat', 'Vândut la metru'),
 ('Doze', 'Doză aparat îngropată TEM Ø68×60 mm', '47 poziții', 50, 'buc', 1.70, H, 'https://www.hornbach.ro/p/doza-simpla-ingropata-pentru-aparataje-tem-o68x60-mm-combinare-in-serie/7197614/', 'verificat', 'Art. 7197614; la ramele duble, doze legate în serie'),
 ('Doze', 'Doză simplă gips-carton Ø65×60 mm', '—', 10, 'buc', None, H, 'https://www.hornbach.ro/p/doza-simpla-gipscarton-pentru-aparataje-o65x60-mm/5534532/', 'de verificat', 'Pentru casetă / pereți de gips-carton'),
 ('Doze', 'Doză aplicată de tavan Electroplast Ø70 (rozete lămpi)', '8 lămpi', 8, 'buc', 8.90, H, 'https://www.hornbach.ro/p/doza-aplicata-de-tavan-pentru-legaturi-electroplast-o70-mm-culoare-neagra/4066065/', 'verificat', ''),
 ('Conectori', 'Wago 221-413 (3 conductoare), set 50 buc', '~100 buc', 2, 'set 50', 157.49, 'Mathaus', 'https://mathaus.ro/p/conector-imbinare-cu-parghii-wago-221-413-30-a-3-x-4-mmp-50-bucati-set/000000000010514667', 'de verificat', 'Preț din deviz R04 (157–231 lei/set). La Hornbach: 12 buc = 33,40 lei'),
 ('Conectori', 'Wago 221-412 (2 cond.) și 221-415 (5 cond.), ~20 buc fiecare', '~40 buc', None, 'buc', None, 'Hornbach / Mathaus', 'https://www.hornbach.ro/s/wago', 'de verificat', 'Caută după cod'),
 ('Fixare și montaj', 'Bride copex Ø20 eBULL, pachet 50 buc', '~200 buc', 4, 'pachet 50', 32.90, H, 'https://www.hornbach.ro/p/bride-plastic-pentru-tub-rigid-copex-ebull-o20-mm-pachet-50-bucati/5963544/', 'verificat', 'Fixarea principală pe placă se face cu ipsos; bridele la curbe și capete'),
 ('Fixare și montaj', 'Ipsos Adeplast IC90, sac 20 kg', '—', 3, 'sac 20 kg', None, H, 'https://www.hornbach.ro/p/ipsos-pentru-constructii-adeplast-ic90-de-interior-20-kg/8671002/', 'de verificat', 'Puncte de fixare tuburi pe placă la 50–60 cm'),
 ('Fixare și montaj', 'Fir de tragere nylon 20 m', '—', 1, 'buc', None, H, 'https://www.hornbach.ro/p/fir-de-tragere-cabluri-electrice-commel-20-m-material-nailon/10669998/', 'de verificat', 'Copexul are deja fir de tragere inclus'),
 ('Fixare și montaj', 'Lubrifiant (gel) pentru tragerea firelor', '—', 1, 'buc', None, 'magazin electric', '', 'de verificat', 'Nu l-am găsit la Hornbach'),
 ('Marcare', 'Marcaj cablu 0,9–1,5 mm², pachet 150 buc', '112 capete de tub', 1, 'pachet', 38.90, H, 'https://www.hornbach.ro/p/marcaj-cablu-electric-0-9-1-5mm-pachet-150-bucati/12555639/', 'verificat', 'Etichetează tuburile și firele la ambele capete'),
 ('Casetă coloană', 'Placă gips-carton Knauf 2000×1200×12,5 mm', '—', 2, 'buc', None, H, 'https://www.hornbach.ro/p/placa-gips-carton-knauf-2000x1200x12-5-mm/7356471/', 'de verificat', 'Caseta coloanei, cu capac demontabil'),
 ('Casetă coloană', 'Profil UW 50 (4 m) Knauf', '—', 2, 'buc', None, H, 'https://www.hornbach.ro/c/materiale-de-constructii/constructii-gips-carton/profile-gipscarton/S14881/', 'de verificat', ''),
 ('Casetă coloană', 'Profil CW 50 (3 m) Knauf', '—', 4, 'buc', None, H, 'https://www.hornbach.ro/c/materiale-de-constructii/constructii-gips-carton/profile-gipscarton/S14881/', 'de verificat', 'Cere CW 50 (la Hornbach am văzut doar CW 100)'),
]

wb = Workbook(); ws = wb.active; ws.title = 'Lista achiziții'
HDR = ['Nr.', 'Categorie', 'Material', 'Necesar (model)', 'Cumperi', 'U.M.', 'Preț unitar (lei)', 'Total (lei)', 'Magazin', 'Link', 'Status preț', 'Observații']
ws['A1'] = 'Ap. 184 Bloc L14 — Lista de achiziții instalație electrică R11 (cu aer condiționat C15)'
ws['A1'].font = Font(bold=True, size=14, color='0F5C73')
ws['A2'] = ('Prețuri citite la 07.10.2026; se pot schimba. Fără tablou, aparataj și lămpi (sunt în devizul R04). '
            'Cantități cu 10 % pierderi la copex și 5 % la fire. Celulele galbene = preț de verificat.')
ws['A2'].font = Font(italic=True, color='5D6F76')
R0 = 4
thin = Side(style='thin', color='C5D3D7'); BD = Border(left=thin, right=thin, top=thin, bottom=thin)
for c, h in enumerate(HDR, 1):
    cell = ws.cell(R0, c, h); cell.font = Font(bold=True, color='FFFFFF'); cell.fill = PatternFill('solid', fgColor='0F5C73')
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True); cell.border = BD
for i, (cat, mat, nec, qty, um, pret, shop, link, st, nota) in enumerate(ROWS):
    r = R0 + 1 + i
    for c, v in enumerate([i + 1, cat, mat, nec, qty, um, pret, None, shop, '', st, nota], 1):
        cell = ws.cell(r, c, v); cell.border = BD; cell.alignment = Alignment(vertical='top', wrap_text=True)
    ws.cell(r, 8, f'=IF(OR(E{r}="",G{r}=""),"",E{r}*G{r})')
    for c in (7, 8): ws.cell(r, c).number_format = '#,##0.00'
    if link:
        ws.cell(r, 10).value = 'deschide'; ws.cell(r, 10).hyperlink = link; ws.cell(r, 10).font = Font(color='0563C1', underline='single')
    if st == 'de verificat':
        for c in (7, 11): ws.cell(r, c).fill = PatternFill('solid', fgColor='FFF2CC')
last = R0 + len(ROWS); t = last + 2
ws.cell(t, 7, 'TOTAL cu prețuri cunoscute').font = Font(bold=True)
ws.cell(t, 8, f'=SUM(H{R0+1}:H{last})').font = Font(bold=True); ws.cell(t, 8).number_format = '#,##0.00'
ws.cell(t + 1, 7, 'Articole fără preț').font = Font(italic=True); ws.cell(t + 1, 8, f'=COUNTBLANK(G{R0+1}:G{last})')
ws.cell(t + 2, 7, 'Articole cu preț de verificat').font = Font(italic=True); ws.cell(t + 2, 8, f'=COUNTIF(K{R0+1}:K{last},"de verificat")')
for col, w in zip('ABCDEFGHIJKL', [5, 17, 52, 16, 10, 12, 12, 13, 17, 10, 13, 55]): ws.column_dimensions[col].width = w
ws.freeze_panes = f'D{R0+1}'; ws.row_dimensions[R0].height = 30; ws.auto_filter.ref = f'A{R0}:L{last}'

w2 = wb.create_sheet('Cum am calculat')
INFO = [
 ('Sursa cantităților', 'montaj_electric_R11_copex.FCStd / tmp/electric_R11/trasee_R11.json (57 tuburi, cu C15 aer condiționat)'),
 ('Copex Ø20 / Ø16 / Ø25 (axă)', '342 m / 34 m / 45,5 m; cu 10 % pierderi: 376 / 37 / 50 m'),
 ('Fire 2,5 mm² (maro / albastru / verde-galben)', '247 m fiecare, +5 % = 260 m (include 0,7 m la tablou, 0,3 m la doze și C15 aer condiționat)'),
 ('Fire 1,5 mm²', 'maro 108, albastru 155, verde-galben 155, negru 56, roșu (în loc de gri) 17 m'),
 ('Cat6 / coaxial', '49 m / 36 m (include 2 m rezervă la fiecare capăt)'),
 ('Doze de aparat', '47 poziții (Anexa A din ghid) + rezervă'),
 ('Nu sunt incluse', 'Tablou, RCBO/AFDD, prize, întrerupătoare, lămpi, aplice, surse LED: sunt în devizul R04'),
 ('Registru complet', 'Ghidul R11 (PDF) și output/pdf/Apartament_184_Tuburi_fire_R11.csv: tub cu tub'),
]
for i, (a, b) in enumerate(INFO, 1):
    w2.cell(i, 1, a).font = Font(bold=True); w2.cell(i, 2, b)
w2.column_dimensions['A'].width = 48; w2.column_dimensions['B'].width = 110
out = R / 'output' / 'Lista_achizitii_electric_R11.xlsx'; wb.save(out); print(out)
tot = sum(q * p for (_, _, _, q, _, p, *_) in ROWS if q is not None and p is not None)
print('total', round(tot, 2), 'fara pret', sum(1 for r in ROWS if r[3] is None or r[5] is None))
