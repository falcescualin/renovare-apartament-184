"""Document PDF de montaj pas cu pas pentru un corp (A3 landscape, stilul planselor proiectului).
build(spec, folder) -> cale PDF. Citeste: lista de debitare R03 (piese, canturi), planul de debitare R03 (placa fiecarei piese),
modelul pereților (harta de amplasare) si imaginile din folder (montaj_blender.py)."""
from pathlib import Path
import json, math, collections
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle

ROOT = Path(__file__).resolve().parents[1]
for n, f in [('Seg', 'segoeui.ttf'), ('SegB', 'segoeuib.ttf'), ('SegI', 'segoeuii.ttf')]:
    pdfmetrics.registerFont(TTFont(n, 'C:/Windows/Fonts/' + f))
pdfmetrics.registerFontFamily('Seg', normal='Seg', bold='SegB', italic='SegI', boldItalic='SegB')

PW, PH = landscape(A3)           # 1190.55 x 841.89
INK = HexColor('#14323f'); TEAL = HexColor('#2f8f88'); MUT = HexColor('#6b7f87'); GRID = HexColor('#c9d6da')
PALE = HexColor('#e7f3f1'); WARN = HexColor('#fbeee9'); WARN_B = HexColor('#c0562c'); OK = HexColor('#e8f4e8'); OK_B = HexColor('#3c8a45')
HWC = HexColor('#c27a2c')
DATE = '07.10.2026'

LISTA = json.loads((ROOT / 'tmp/lista_debitare_R03.json').read_text(encoding='utf-8'))['piese']
LAY = json.loads((ROOT / 'tmp/debitare_layout_R03.json').read_text(encoding='utf-8'))['materiale']
ARCH = json.loads((ROOT / 'tmp/termic_model.json').read_text(encoding='utf-8'))
FURN = json.loads((ROOT / 'tmp/mobilier_plan_R03.json').read_text(encoding='utf-8'))['items']
MATN = {'ALB18': 'PAL alb 18 mm', 'CAS18': 'PAL cashmere 18 mm', 'STJ18': 'PAL stejar 18 mm', 'ALB16': 'PAL alb 16 mm',
        'HDF3': 'HDF alb 3 mm', 'BLAT38': 'Blat stejar 38 mm'}
SHEET = collections.defaultdict(set)
for m, r in LAY.items():
    for i, sh in enumerate(r['sheets'], 1):
        for p in sh['placed']:
            SHEET[p['cod']].add('%s-%d' % (m, i))
R03 = {p['cod']: p for p in LISTA}


def st(size=9.5, color=INK, bold=False, leading=None, align=0, italic=False):
    return ParagraphStyle('s', fontName='SegB' if bold else ('SegI' if italic else 'Seg'), fontSize=size, leading=leading or size * 1.32, textColor=color, alignment=align)


class Pdf:
    def __init__(self, path, title, footer):
        self.c = canvas.Canvas(str(path), pagesize=(PW, PH)); self.c.setTitle(title); self.c.setAuthor('Claude')
        self.footer, self.n = footer, 0

    # ---- primitive
    def y(self, top):           # coordonata de sus in coordonate de pagina
        return PH - top

    def para(self, text, x, top, w, style, h=None):
        p = Paragraph(text, style); pw, ph = p.wrap(w, 2000)
        p.drawOn(self.c, x, PH - top - ph); return ph

    def text(self, s, x, top, font='Seg', size=10, color=INK, align='l'):
        c = self.c; c.setFont(font, size); c.setFillColor(color)
        {'l': c.drawString, 'r': c.drawRightString, 'c': c.drawCentredString}[align](x, PH - top - size * .8, s)

    def rect(self, x, top, w, h, fill=None, stroke=None, lw=.8, r=0):
        c = self.c
        if fill: c.setFillColor(fill)
        if stroke: c.setStrokeColor(stroke); c.setLineWidth(lw)
        (c.roundRect(x, PH - top - h, w, h, r, stroke=1 if stroke else 0, fill=1 if fill else 0) if r else
         c.rect(x, PH - top - h, w, h, stroke=1 if stroke else 0, fill=1 if fill else 0))

    def pill(self, x, top, s, col=TEAL, size=10):
        c = self.c; w = pdfmetrics.stringWidth(s, 'SegB', size) + 12
        c.setFillColor(col); c.setStrokeColor(white); c.setLineWidth(1.2)
        c.roundRect(x - w / 2, PH - top - size * .75, w, size * 1.6, size * .8, stroke=1, fill=1)
        c.setFillColor(white); c.setFont('SegB', size); c.drawCentredString(x, PH - top - size * .33 + 1, s)

    def dot(self, x, top, s, size=10, col=HWC):
        c = self.c; c.setFillColor(col); c.setStrokeColor(white); c.setLineWidth(1.2); c.circle(x, PH - top, size * .95, stroke=1, fill=1)
        c.setFillColor(white); c.setFont('SegB', size); c.drawCentredString(x, PH - top - size * .35, s)

    def page(self, title, sub=''):
        if self.n: self.c.showPage()
        self.n += 1; c = self.c
        self.rect(0, 0, PW, 62, fill=INK)
        self.text(title, 40, 17, 'SegB', 22, white)
        if sub: self.text(sub, PW - 40, 24, 'Seg', 12, HexColor('#bcd3d8'), 'r')
        c.setFillColor(MUT); c.setFont('Seg', 8.5)
        c.drawString(40, 18, self.footer); c.drawRightString(PW - 40, 18, 'pagina %d' % self.n)
        c.setStrokeColor(GRID); c.setLineWidth(.6); c.line(40, 30, PW - 40, 30)

    def img(self, path, x, top, w, h):
        path = Path(path)
        if not path.exists():
            return
        if path.suffix.lower() == '.png':                       # PNG cu transparenta -> JPEG pe fond alb (PDF de cateva ori mai mic)
            from PIL import Image
            jd = path.parent / '_jpg'; jd.mkdir(exist_ok=True)
            jp = jd / (path.stem + '.jpg')
            if not jp.exists() or jp.stat().st_mtime < path.stat().st_mtime:
                im = Image.open(path)
                if im.mode in ('RGBA', 'LA', 'P'):
                    im = im.convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); im = bg
                im.convert('RGB').save(jp, 'JPEG', quality=86, optimize=True)
            path = jp
        self.c.drawImage(str(path), x, PH - top - h, w, h, preserveAspectRatio=True, anchor='c')

    def save(self):
        self.c.showPage(); self.c.save()

    def table(self, head, rows, x, top, widths, size=9, head_fill=HexColor('#d9e8ec'), pad=4):
        data = [[Paragraph('<b>%s</b>' % h, st(size)) for h in head]] + [[(v if not isinstance(v, str) else Paragraph(v, st(size))) for v in r] for r in rows]
        t = Table(data, colWidths=widths, repeatRows=1)
        sty = [('BACKGROUND', (0, 0), (-1, 0), head_fill), ('GRID', (0, 0), (-1, -1), .4, GRID), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
               ('TOPPADDING', (0, 0), (-1, -1), pad), ('BOTTOMPADDING', (0, 0), (-1, -1), pad), ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5)]
        for i in range(2, len(data), 2): sty.append(('BACKGROUND', (0, i), (-1, i), HexColor('#f6f9fa')))
        t.setStyle(TableStyle(sty)); w, h = t.wrap(0, 0); t.drawOn(self.c, x, PH - top - h); return h


def codes_of(S):
    seen, out = set(), []
    for p in S.parts:
        if p['code'] in R03 and p['code'] not in seen:
            seen.add(p['code']); out.append(p['code'])
    return out


def edges(p):
    e = []
    for k in ('L1', 'L2', 'W1', 'W2'):
        v = p[k]
        if v not in ('-', '', None): e.append('%s %s' % (k, v))
    return ' · '.join(e) or '—'


def plan_map(P, x, top, w, h, gbox):
    x0, y0, x1, y1 = -100, -5800, 11200, 1400
    s = min(w / (x1 - x0), h / (y1 - y0)); ox = x + (w - (x1 - x0) * s) / 2; oy = top + (h - (y1 - y0) * s) / 2
    def X(v): return ox + (v - x0) * s
    def Y(v): return oy + (y1 - v) * s
    c = P.c; c.setStrokeColor(INK); c.setLineWidth(.9)
    for e in ARCH['wall_edges']:
        if len(e) == 2: c.line(X(e[0][0]), PH - Y(e[0][1]), X(e[1][0]), PH - Y(e[1][1]))
    c.setStrokeColor(HexColor('#c9cfd1')); c.setLineWidth(.4)
    for f in FURN:
        for poly in f.get('polys') or [f['poly']]:
            pts = poly + poly[:1]
            for a, b in zip(pts, pts[1:]): c.line(X(a[0]), PH - Y(a[1]), X(b[0]), PH - Y(b[1]))
    if gbox:
        gx0, gy0, gx1, gy1 = gbox
        c.setFillColor(HexColor('#2f8f88')); c.setFillAlpha(.55); c.setStrokeColor(TEAL); c.setLineWidth(1.4)
        c.rect(X(gx0), PH - Y(gy0), (gx1 - gx0) * s, (gy1 - gy0) * s * -1 * -1 if False else (Y(gy1) - Y(gy0)) * -1 * -1, stroke=1, fill=1) if False else None
        rx, ry, rw, rh = X(gx0), PH - Y(gy0), (gx1 - gx0) * s, (Y(gy0) - Y(gy1))
        c.rect(rx, ry, rw, rh, stroke=1, fill=1); c.setFillAlpha(1)
        # cerc de reperare
        cx, cy = X((gx0 + gx1) / 2), PH - Y((gy0 + gy1) / 2)
        c.setStrokeColor(WARN_B); c.setLineWidth(1.6); c.circle(cx, cy, 20, stroke=1, fill=0)


def build(S, folder):
    folder = Path(folder)
    out = ROOT / 'output' / 'pdf' / ('Apartament_184_Montaj_%s_R04.pdf' % S.slug)
    P = Pdf(out, 'Apartament 184 – Montaj %s' % S.title, 'Apartament 184, Bloc L14 · %s · instrucțiuni de montaj · R04 · %s · cote în mm' % (S.title, DATE))
    c = P.c
    codes = codes_of(S)
    n_buc = sum(R03[k]['n'] for k in codes)
    sheets = sorted({s for k in codes for s in SHEET.get(k, [])})
    ANC = json.loads((folder / 'ancore.json').read_text(encoding='utf-8'))

    # ---------------------------------------------------------------- 1. coperta
    P.page(S.title, 'INSTRUCȚIUNI DE MONTAJ PAS CU PAS')
    P.para(S.desc, 40, 90, 520, st(13, INK, leading=18))
    facts = [('Dimensiuni (L × A × Î)', '%d × %d × %d mm' % S.dims), ('Piese de tăiat', '%d poziții · %d bucăți' % (len(codes), n_buc)),
             ('Plăci din planul de debitare', ', '.join(sheets) or '—'), ('Pași de montaj', str(len(S.steps))), ('Timp estimat', S.time or '—'),
             ('Persoane', S.people), ('Amplasare', S.where)]
    top = 190
    for k, v in facts:
        P.text(k, 40, top, 'SegB', 10.5, MUT); P.para(v, 230, top - 2, 340, st(11)); top += 36
    P.para('<b>Înainte de montaj:</b> citește paginile „Ce îți trebuie”, „Lista pieselor” și „Găurire”. Piesele sunt etichetate cu codul din planul de debitare (ex. <b>N-01</b>); '
           'codul apare pe imagini într-un ovală turcoaz, iar piesele noi din fiecare pas sunt colorate turcoaz.', 40, 490, 520, st(10.5, INK), )
    P.rect(40, 560, 520, 120, fill=WARN, stroke=WARN_B, r=6)
    P.para('<b>Dimensiunile din documente sunt cote finite</b> din planul de debitare R03 (cantul inclus). Dacă atelierul a livrat piese cu alte cote sau fără canturi, oprește-te și măsoară înainte să găurești. '
           'Cotele de pe șantier pot diferi de model cu câțiva milimetri.', 52, 570, 496, st(10.5, INK))
    P.img(folder / 'final_fata.png', 590, 90, 560, 380)
    P.img(folder / 'final_sus.png', 590, 470, 300, 220) if (folder / 'final_sus.png').exists() else None
    P.text('AMPLASARE ÎN APARTAMENT', 910, 480, 'SegB', 10, MUT)
    plan_map(P, 900, 495, 250, 200, S.gbox)

    # ---------------------------------------------------------------- 2. ce iti trebuie
    from montaj_specs import TOOLS, SAFETY
    P.page('Ce îți trebuie', S.title)
    P.text('UNELTE', 40, 90, 'SegB', 12, TEAL)
    top = 118
    for t, d in TOOLS:
        P.rect(40, top - 2, 14, 14, stroke=TEAL, lw=1.2, r=3)
        h = P.para('<b>%s</b><br/><font color="#6b7f87">%s</font>' % (t, d), 64, top - 3, 330, st(10)); top += max(h, 18) + 8
    P.text('SIGURANȚĂ', 430, 90, 'SegB', 12, TEAL)
    top = 118
    for t in SAFETY:
        h = P.para('• ' + t, 430, top, 330, st(10)); top += h + 8
    P.text('CONDIȚII ÎNAINTE DE MONTAJ', 810, 90, 'SegB', 12, TEAL)
    top = 118
    for t in S.pre or ['Podeaua e finită și uscată, peretele e vopsit.']:
        h = P.para('• ' + t, 810, top, 340, st(10)); top += h + 8
    P.text('LEGENDA', 40, 500, 'SegB', 12, TEAL)
    P.pill(70, 540, 'N-01'); P.para('Codul piesei din planul de debitare R03. Eticheta de pe piesă (folie sau creion) are același cod.', 120, 530, 320, st(10))
    P.dot(480, 540, 'A'); P.para('Litera feroneriei din lista „Feronerie”. Cantitatea e în lista de feronerie.', 505, 530, 320, st(10))
    P.rect(40, 590, 24, 24, fill=HexColor('#54b8ab')); P.para('Piesele turcoaz sunt cele noi din pasul curent; cele gri au fost montate înainte.', 76, 592, 400, st(10))
    P.rect(480, 590, 24, 24, fill=HexColor('#f2801f')); P.para('Feroneria portocalie e cea nouă din pas; pe imaginea explodată e trasă pe direcția de montaj, cu linie punctată până la gaură.', 516, 588, 420, st(10))
    P.rect(40, 640, 1110, 70, fill=PALE, stroke=TEAL, r=6)
    P.para('<b>Regula de aur:</b> montează corpul pe podea (pe covor), nu pe perete. Verifică diagonalele înainte să strângi confirmatele la maxim. Nu fixa spatele HDF până nu ai verificat unghiurile. '
           'Dacă o piesă nu se potrivește, nu forța: verifică codul și orientarea cantului.', 54, 652, 1080, st(11))

    # ---------------------------------------------------------------- 3. lista pieselor
    P.page('Lista pieselor', '%d poziții · %d bucăți' % (len(codes), n_buc))
    rows = []
    for k in codes:
        p = R03[k]
        rows.append(['<b>%s</b>' % k, p['den'], MATN.get(p['mat'], p['mat']), '%g × %g' % (p['L'], p['W']), str(p['n']), edges(p), ', '.join(sorted(SHEET.get(k, []))) or '—', (p['note'] or '')[:70]])
    h = P.table(['Cod', 'Denumire', 'Material', 'L × l (mm)', 'Buc.', 'Cant', 'Placă', 'Observații'], rows, 40, 90, [64, 230, 140, 100, 40, 130, 100, 306], 9.5)
    P.para('<b>Canturi:</b> L1, L2 = muchiile lungi; W1, W2 = muchiile scurte; „2” = ABS 2 mm; „0.8” = ABS 0,8 mm; „42” = ABS 42 × 2 mm (blaturi dublate). '
           '<b>Placă:</b> eticheta plăcii din planul de debitare R03 (ex. CAS18-2 = a 2-a placă de PAL cashmere).', 40, 90 + h + 14, 1100, st(9.5, MUT))

    # ---------------------------------------------------------------- 4. feronerie
    P.page('Feronerie și consumabile', S.title)
    rows = [[('<b>%s</b>' % hw['letter']), hw['name'], str(hw['qty']), hw['note'], hw['steps']] for hw in S.hw]
    h = P.table(['', 'Articol', 'Cantitate', 'Observații', 'Pasul'], rows, 40, 90, [40, 480, 100, 380, 90], 10, pad=5)
    P.para('Cantitățile includ o mică rezervă la șuruburi și confirmate. Articolele cu * sunt de confirmat la comandă (după fișele Blum). '
           'Comanda de feronerie e în devizul R04, lotul M076.', 40, 90 + h + 14, 1100, st(9.5, MUT))

    # ---------------------------------------------------------------- 5. gaurire
    from montaj_specs import CONF_RULES
    P.page('Găurire și îmbinări', 'confirmate Ø7 × 50 și cepuri Ø8')
    P.text('REGULI', 40, 90, 'SegB', 12, TEAL)
    top = 116
    for t in CONF_RULES:
        h = P.para('• ' + t, 40, top, 520, st(10.5)); top += h + 7
    P.text('ÎMBINĂRILE CORPULUI', 600, 90, 'SegB', 12, TEAL)
    rows = []
    for j in S.joints:
        rows.append([str(j['step']), j['name'], '%s / %s' % (j['a'], j['b']), '%d mm' % j['L'], str(len(j['pos'])), ', '.join(str(v) for v in j['pos'])])
    P.table(['Pas', 'Îmbinare', 'Piese', 'Lungime', 'Confirmate', 'Poziții de la un capăt (mm)'], rows, 600, 116, [34, 170, 90, 62, 62, 132], 9)
    P.rect(40, 520, 520, 160, fill=PALE, stroke=TEAL, r=6)
    P.para(('<b>Cote Blum:</b> ' + ' '.join(S.notes) + '<br/><br/>' if S.notes else '') +
           '<b>Confirmatele, cepurile și găurile pentru glisiere se fac la montaj, cu șablonul</b> (găurile de balamale Ø35, unde există, se fac la atelier, lotul M104). '
           'Dacă atelierul le-a făcut deja, verifică pozițiile din desene înainte să asamblezi.', 54, 532, 496, st(10.5))

    import montaj_desene
    montaj_desene.drilling_pages(P, st, PH, S, R03)
    import montaj_izo, montaj_panouri
    montaj_izo.hardware_cards(P, st, PH, S)
    _uniq = montaj_panouri.build(S, folder, run=False)
    montaj_izo.panel_pages(P, st, PH, S, folder, _uniq)

    # ---------------------------------------------------------------- 6. pasi
    total = len(S.steps)
    import montaj_hw
    FERP = ROOT / 'tmp' / 'feronerie_R2' / 'png'
    for step in S.steps:
        n = step['n']
        P.page('Pasul %d din %d: %s' % (n, total, step['title']), S.title)
        det = step.get('detail')
        # banda de feronerie a pasului (ca la IKEA): iconita 3D, litera, cate bucati
        cnt = montaj_hw.count(S, n)
        cards = []
        for L in step['hw'].split():
            hwd = next((h for h in S.hw if h['letter'] == L), None)
            if not hwd:
                continue
            mods = [(m, v) for (l, m), v in cnt.items() if l == L]
            if mods:
                for m, v in mods:
                    cards.append((L, m, '%d ×' % v, hwd['name']))
            else:
                cards.append((L, hwd.get('model'), str(hwd['qty']) if not isinstance(hwd['qty'], int) else '%d ×' % hwd['qty'], hwd['name']))
        top0 = 74
        if cards:
            cw = min(150, 770 / len(cards))
            P.rect(40, top0, 770, 96, fill=HexColor('#f6f9fa'), stroke=GRID, lw=.6, r=5)
            for i, (L, m, q, nm) in enumerate(cards):
                cx = 40 + i * cw
                if m and (FERP / (m + '.png')).exists():
                    P.img(FERP / (m + '.png'), cx + 6, top0 + 6, 62, 62)
                P.dot(cx + 12, top0 + 14, L, size=9)
                P.text(q, cx + 72, top0 + 22, 'SegB', 17, INK)
                P.para('<font color="#6b7f87">%s</font>' % nm, cx + 6, top0 + 70, cw - 10, st(7, leading=8.2))
            top0 += 104
        main_h = 594 - top0
        bx, by, bw, bh = 40, top0, 770, main_h
        P.img(folder / ('pas_%d.png' % n), bx, by, bw, bh)
        # randul de jos: rezultatul pasului (montat) si detaliul
        ry = by + bh + 8
        rh = PH - 40 - ry
        if det:
            P.rect(40, ry, 300, rh, fill=HexColor('#fbfdfd'), stroke=GRID, lw=.8, r=5)
            P.text('REZULTAT', 52, ry + 8, 'SegB', 9, TEAL)
            P.img(folder / ('pas_%d_ok.png' % n), 46, ry + 22, 288, rh - 28)
            P.rect(350, ry, 460, rh, fill=HexColor('#fbfdfd'), stroke=GRID, lw=.8, r=5)
            P.text('DETALIU', 362, ry + 8, 'SegB', 9, TEAL)
            P.img(folder / ('pas_%dd.png' % n), 356, ry + 22, 280, rh - 28)
            P.para(det.get('text', ''), 646, ry + 26, 156, st(9))
        else:
            P.rect(40, ry, 300, rh, fill=HexColor('#fbfdfd'), stroke=GRID, lw=.8, r=5)
            P.text('REZULTAT', 52, ry + 8, 'SegB', 9, TEAL)
            P.img(folder / ('pas_%d_ok.png' % n), 46, ry + 22, 288, rh - 28)
            P.para('<b>Imaginea mare</b> e explodată: piesele noi (turcoaz) și feroneria nouă (portocaliu) sunt trase din poziție, '
                   'pe direcția în care se montează; liniile punctate arată unde intră fiecare șurub. <b>Rezultatul</b> arată pasul terminat.',
                   356, ry + 22, 440, st(9, MUT))
        # callouturi: codurile pieselor noi si literele feroneriei
        iw, ih = 1800, 1300
        sc = min(bw / iw, bh / ih); dw, dh = iw * sc, ih * sc; ox, oy = bx + (bw - dw) / 2, by + (bh - dh) / 2
        done = set(); taken = []
        for pid, (u, v) in ANC.get(str(n), {}).items():
            if pid.startswith('hw:'):
                X, Y = ox + u * dw + 16, oy + (1 - v) * dh - 14
                while any(abs(X - a) < 22 and abs(Y - b) < 18 for a, b in taken): Y -= 20
                taken.append((X, Y)); P.dot(X, Y, pid[3:], size=10)
                continue
            part = next(p for p in S.parts if p['id'] == pid)
            code = part['code']
            if code == 'SL' and 'SL' not in done:                 # glisierele: litera din lista de feronerie
                done.add('SL'); L = next((h['letter'] for h in S.hw if h.get('model') == 'glisiera_movento'), 'F')
                X, Y = ox + u * dw, oy + (1 - v) * dh
                taken.append((X, Y)); P.dot(X, Y, L, size=10)
                continue
            if code in done or code in ('SL', 'LED', 'PERETE') or part.get('role') == 'context' or code not in R03: continue
            done.add(code)
            X, Y = ox + u * dw, oy + (1 - v) * dh
            while any(abs(X - a) < 40 and abs(Y - b) < 18 for a, b in taken): Y += 20
            taken.append((X, Y)); P.pill(X, Y, code)
        # coloana dreapta
        rx = 840
        P.rect(rx, 78, 310, 52, fill=TEAL, r=6); P.text('PASUL %d' % n, rx + 14, 88, 'SegB', 24, white)
        top = 148
        for i, t in enumerate(step['text'], 1):
            h = P.para('<b>%d.</b> %s' % (i, t), rx, top, 310, st(10.5)); top += h + 6
        top += 6
        # piese in pas
        pcodes = []
        for pid in step['parts']:
            part = next(p for p in S.parts if p['id'] == pid)
            if part['code'] in R03 and part['code'] not in pcodes: pcodes.append(part['code'])
        if pcodes:
            P.text('PIESE ÎN ACEST PAS', rx, top, 'SegB', 10, MUT); top += 18
            for k in pcodes:
                p = R03[k]; P.pill(rx + 24, top + 7, k, size=8.5)
                P.para('%s · %g × %g · %s buc.' % (p['den'], p['L'], p['W'], sum(1 for q in S.parts if q['code'] == k and q['step'] == n) or p['n']), rx + 62, top - 2, 250, st(9))
                top += 22
        if step['hw']:
            top += 6; P.text('FERONERIE', rx, top, 'SegB', 10, MUT); top += 18
            for L in step['hw'].split():
                nm = next((h['name'] for h in S.hw if h['letter'] == L), '')
                P.dot(rx + 10, top + 7, L, size=9)
                hh = P.para(nm, rx + 28, top - 1, 280, st(9.5))
                top += max(hh, 16) + 5
            top += 4
        if step['warn']:
            hh = sum(Paragraph('<b>Atenție:</b> ' + t, st(10)).wrap(286, 900)[1] + 6 for t in step['warn']) + 14
            P.rect(rx, top, 310, hh, fill=WARN, stroke=WARN_B, r=5); yy = top + 8
            for t in step['warn']: yy += P.para('<b>Atenție:</b> ' + t, rx + 12, yy, 286, st(10)) + 6
            top += hh + 10
        if step['check']:
            hh = sum(Paragraph('✓ ' + t, st(10)).wrap(286, 900)[1] + 4 for t in step['check']) + 26
            P.rect(rx, top, 310, hh, fill=OK, stroke=OK_B, r=5); P.text('VERIFICĂ', rx + 12, top + 6, 'SegB', 9, OK_B); yy = top + 24
            for t in step['check']: yy += P.para('• ' + t, rx + 12, yy, 286, st(10)) + 4
        if getattr(S, 'front_detail', False) and n == getattr(S, 'front_step', 5):
            import montaj_fronturi
            montaj_fronturi.front_pages(P, st, PH, S)

    import montaj_perete
    montaj_perete.wall_page(P, st, PH, S)

    # ---------------------------------------------------------------- 7. verificare finala
    P.page('Verificare finală', S.title)
    P.img(folder / 'final_fata.png', 40, 80, 560, 400)
    items = ['Toate piesele din lista pieselor sunt montate (bifează codurile).', 'Diagonalele corpului sunt egale ±2 mm și corpul stă drept.',
             'Fronturile sunt aliniate, cu rost de 2–3 mm egal.', 'Sertarele se deschid prin apăsare și se închid amortizat.', 'Capacele de confirmat sunt puse pe fețele vizibile.',
             'Niciun șurub nu iese prin fețele vizibile.', 'Corpul este nivelat și, dacă e înalt, fixat de perete.', 'Rămân suprafețe fără praf, urme de adeziv sau zgârieturi.'] + S.extra_final
    P.text('LISTA DE VERIFICARE', 640, 90, 'SegB', 12, TEAL)
    top = 118
    for t in items:
        P.rect(640, top - 1, 15, 15, stroke=OK_B, lw=1.3, r=3); h = P.para(t, 666, top - 2, 480, st(11)); top += max(h, 18) + 10
    P.rect(640, top + 14, 510, 90, fill=PALE, stroke=TEAL, r=6)
    P.para('<b>Întreținere:</b> șterge cu o cârpă umedă și apoi uscată; fără produse abrazive. Reglează fronturile după primele 2–3 săptămâni (se așază). '
           'Strânge ușor șuruburile balamalelor și picioarelor după o lună.', 654, top + 24, 484, st(10.5))
    P.save()
    return out
