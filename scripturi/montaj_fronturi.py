"""Pagini detaliate: fixarea fronturilor de sertar (poziționare cu rosturi, bandă dublu adeziv, șuruburi din interior, reglaj).
Se genereaza din fronturile (role='door') din spec; foloseste cotele reale ale pieselor."""
from reportlab.lib.colors import HexColor, white
INK = HexColor('#14323f'); TEAL = HexColor('#2f8f88'); MUT = HexColor('#6b7f87'); GRID = HexColor('#c9d6da')
WARN = HexColor('#fbeee9'); WARN_B = HexColor('#c0562c'); OK = HexColor('#e8f4e8'); OK_B = HexColor('#3c8a45'); PALE = HexColor('#e7f3f1')
CAS = HexColor('#c9c3b8'); WHITEB = HexColor('#ecebe6'); TAPE = HexColor('#e9c46a'); SCREW = HexColor('#555d63')


def doors(S):
    fr = [p for p in S.parts if p.get('role') == 'door' and p['id'].endswith('.fr')]
    return fr or [p for p in S.parts if p.get('role') == 'door']


def carcass_box(S):
    xs = [p['box'][0] for p in S.parts if p['code'] in ('N-01',)]
    return None


def dim_h(P, PH, x0, x1, y, txt, size=8.5):
    c = P.c; c.setStrokeColor(MUT); c.setLineWidth(.6)
    c.line(x0, PH - y, x1, PH - y); c.line(x0, PH - y - 3, x0, PH - y + 3); c.line(x1, PH - y - 3, x1, PH - y + 3)
    P.text(txt, (x0 + x1) / 2, y - 12, 'SegB', size, INK, 'c')


def dim_v(P, PH, x, y0, y1, txt, size=8.5, left=True):
    c = P.c; c.setStrokeColor(MUT); c.setLineWidth(.6)
    c.line(x, PH - y0, x, PH - y1); c.line(x - 3, PH - y0, x + 3, PH - y0); c.line(x - 3, PH - y1, x + 3, PH - y1)
    P.text(txt, x - 6 if left else x + 6, (y0 + y1) / 2 - 4, 'SegB', size, INK, 'r' if left else 'l')


def elevatie(P, PH, S, x, top, w, h):
    """front carcasa cu fronturile, rosturi cotate"""
    c = P.c
    ds = sorted(doors(S), key=lambda p: -p['box'][2])        # sus -> jos
    # carcasa (laterale + baza + blat corp): din lateralele N-01
    lat = [p for p in S.parts if p.get('role') == 'panel' and p['mat'] != 'sertar' and p['code'] not in ('SL', 'PERETE')]
    cx0 = min(p['box'][0] for p in lat); cx1 = max(p['box'][0] + p['box'][3] for p in lat)
    cz0 = min(p['box'][2] for p in lat); cz1 = max(p['box'][2] + p['box'][5] for p in lat)
    cw, ch = cx1 - cx0, cz1 - cz0
    s = min((w - 120) / cw, (h - 90) / ch)
    ox, oy = x + 70, top + 40
    def X(v): return ox + (cx1 - v) * s            # privit din fata: +x = stanga
    def Y(z): return oy + (cz1 - z) * s
    P.rect(x, top, w, h, stroke=GRID, lw=.6, r=4)
    P.text('VEDERE DIN FAȚĂ: ROSTURI', x + 14, top + 10, 'SegB', 10, TEAL)
    P.rect(ox, oy, cw * s, ch * s, fill=WHITEB, stroke=INK, lw=1)
    P.text('corp', ox + 8, oy + 8, 'Seg', 8, MUT)
    for p in ds:
        bx, by, bz, dx, dy, dz = p['box']
        x0, x1_ = X(bx + dx), X(bx); y0, y1 = Y(bz + dz), Y(bz)
        P.rect(x0, y0, x1_ - x0, y1 - y0, fill=CAS, stroke=INK, lw=1)
        P.pill((x0 + x1_) / 2, (y0 + y1) / 2, p['code'], size=9)
    # cote rosturi
    if len(ds) >= 2:
        up, lo = ds[0], ds[1]
        gap = lo['box'][2] + lo['box'][5]
        gap_mid = up['box'][2] - gap
        dim_v(P, PH, ox + cw * s + 26, Y(up['box'][2]), Y(gap), '%g mm' % gap_mid, left=False)
    lo = ds[-1]
    dim_v(P, PH, ox - 22, Y(lo['box'][2]), Y(cz0), '%g mm' % (lo['box'][2] - cz0))
    up = ds[0]
    dim_v(P, PH, ox - 22, Y(cz1), Y(up['box'][2] + up['box'][5]), '%g mm' % (cz1 - up['box'][2] - up['box'][5]))
    d0 = ds[0]['box']
    gl = cx1 - (d0[0] + d0[3]); gr = d0[0] - cx0
    dim_h(P, PH, ox, X(d0[0] + d0[3]), oy + ch * s + 24, '%g mm' % gl)
    dim_h(P, PH, X(d0[0]), ox + cw * s, oy + ch * s + 24, '%g mm' % gr)
    P.text('Rosturile sunt ghidate de distanțiere de carton/plastic de aceeași grosime, nu de ochi.', x + 14, top + h - 22, 'Seg', 8.5, MUT)


def sectiune(P, PH, S, x, top, w, h):
    """sectiune orizontala prin partea din fata a sertarului: corp, cutie sertar, banda adeziva, surub, front"""
    c = P.c
    P.rect(x, top, w, h, stroke=GRID, lw=.6, r=4)
    P.text('SECȚIUNE ORIZONTALĂ PRIN FRONTUL SERTARULUI', x + 14, top + 10, 'SegB', 10, TEAL)
    # scara (pt / mm): incape in caseta, cu loc pentru textul de jos
    s = min(3.0, (h - 150) / 90.0)
    ox = x + 70; oy = top + 62
    # lateral corp (18) si lateral sertar (16), fata interioara sertar (18), front (18)
    def R(xx, yy, ww, hh, col, lab=None):
        P.rect(ox + xx * s, oy + yy * s, ww * s, hh * s, fill=col, stroke=INK, lw=.9)
        if lab: P.text(lab, ox + (xx + ww / 2) * s, oy + (yy + hh / 2) * s - 4, 'Seg', 7.5, INK, 'c')
    # orientare: sus = interior sertar, jos = exterior (fata)
    R(0, 0, 18, 70, WHITEB)                        # lateral corp
    P.text('lateral corp 18', ox + 9 * s, oy - 12, 'Seg', 7.5, MUT, 'c')
    R(23, 0, 16, 70, HexColor('#f1efe6'))          # lateral sertar 16
    P.text('lateral sertar 16', ox + 31 * s, oy - 12, 'Seg', 7.5, MUT, 'c')
    R(39, 48, 80, 18, HexColor('#f1efe6'))         # fata interioara a sertarului 18 (orizontal)
    P.text('față interioară sertar 18', ox + 66 * s, oy + 57 * s - 4, 'Seg', 7.5, INK, 'c')
    R(2, 66, 120, 18, CAS)                         # front 18
    P.text('front 18', ox + 40 * s, oy + 75 * s - 4, 'Seg', 7.5, INK, 'c')
    # banda dubla adeziv (intre fata interioara si front)
    P.rect(ox + 44 * s, oy + 65.2 * s, 22 * s, 0.8 * s * 2, fill=TAPE, stroke=None)
    P.text('bandă dublu adeziv (poziționare)', ox + 55 * s, oy + 84 * s + 6, 'Seg', 7.5, INK, 'c')
    # surub 4 x 25 cu cap bombat + saiba M4, din interior: saiba pe fata interioara, tija 25 mm -> ~6 mm in front
    sx = ox + 100 * s
    P.rect(sx - 4.5 * s, oy + 47.2 * s, 9 * s, 0.8 * s, fill=SCREW, stroke=INK, lw=.5)          # saiba
    P.rect(sx - 4.0 * s, oy + 44.2 * s, 8 * s, 3.0 * s, fill=SCREW, stroke=INK, lw=.6)          # cap bombat
    P.rect(sx - 2.0 * s, oy + 48.0 * s, 4.0 * s, 24.2 * s, fill=SCREW, stroke=INK, lw=.6)       # tija
    P.text('șurub 4 × 25 + șaibă', sx + 16, oy + 36 * s, 'SegB', 8, INK)
    P.text('≈ 6 mm în front, ≈ 12 mm rămân intacți', sx + 16, oy + 36 * s + 11, 'Seg', 7.5, MUT)
    dim_v(P, PH, ox + 128 * s, oy + 66 * s, oy + 84 * s, '18')
    # joc de reglaj
    P.para('<b>Joc de reglaj:</b> găurile din fața interioară a sertarului se fac Ø5 (mai mari decât șurubul Ø4) și șurubul se pune cu șaibă. '
           'Astfel frontul se poate deplasa cu ±1 mm după montaj, ca să-i potrivești rosturile.', x + 14, top + h - 46, w - 28, st_(9))


def st_(size, color=INK):
    from reportlab.lib.styles import ParagraphStyle
    return ParagraphStyle('s', fontName='Seg', fontSize=size, leading=size * 1.35, textColor=color)


def spate_front(P, PH, S, x, top, w, h):
    """vedere dinspre interior: pozitia surubelor pe fata interioara a sertarului (prima cutie)"""
    c = P.c
    ds = sorted(doors(S), key=lambda p: -p['box'][2])
    p = ds[-1]
    fx, fy, fz, fdx, fdy, fdz = p['box']
    boards = [q for q in S.parts if q['id'].endswith('.fa')]
    # fata interioara a sertarului care se afla in dreptul frontului p
    q = min(boards, key=lambda b: abs((b['box'][2] + b['box'][5] / 2) - (fz + fdz / 2)))
    bx, by, bz, bdx, bdy, bdz = q['box']
    P.rect(x, top, w, h, stroke=GRID, lw=.6, r=4)
    P.text('SPATELE FRONTULUI (vedere din interiorul sertarului): ȘURUBURI', x + 14, top + 10, 'SegB', 10, TEAL)
    s = min((w - 100) / fdx, (h - 120) / fdz)
    ox, oy = x + 50, top + 50
    def X(v): return ox + (fx + fdx - v) * s          # privit din spate: oglindit
    def Y(z): return oy + (fz + fdz - z) * s
    P.rect(ox, oy, fdx * s, fdz * s, fill=CAS, stroke=INK, lw=1)
    # fata interioara
    P.rect(X(bx + bdx), Y(bz + bdz), bdx * s, bdz * s, fill=HexColor('#f1efe6'), stroke=INK, lw=.9)
    P.text('față interioară sertar', ox + fdx * s / 2, Y(bz + bdz / 2) - 4, 'Seg', 8, MUT, 'c')
    pts = [(bx + 40, bz + 20), (bx + bdx - 40, bz + 20), (bx + 40, bz + bdz - 20), (bx + bdx - 40, bz + bdz - 20)]
    for (u, z) in pts:
        c.setFillColor(white); c.setStrokeColor(HexColor('#c0392b')); c.setLineWidth(1.3); c.circle(X(u), PH - Y(z), 4.2, stroke=1, fill=1)
        c.line(X(u) - 3, PH - Y(z), X(u) + 3, PH - Y(z)); c.line(X(u), PH - Y(z) - 3, X(u), PH - Y(z) + 3)
    dim_h(P, PH, X(bx + 40), X(bx + bdx - 40), oy + fdz * s + 22, '%g mm între șuruburi' % (bdx - 80))
    dim_v(P, PH, ox - 14, Y(bz + bdz - 20), Y(bz + 20), '%g' % (bdz - 40))
    P.text('40 mm de capete, 20 mm de muchii', ox + fdx * s / 2, oy + fdz * s + 44, 'Seg', 8, MUT, 'c')


def front_pages(P, st, PH, S):
    ds = doors(S)
    if not ds: return
    P.page('Fronturile de sertar în detaliu (1/2): poziționare', S.title)
    elevatie(P, PH, S, 40, 80, 520, 440)
    sectiune(P, PH, S, 580, 80, 570, 440)
    P.text('METODA', 40, 545, 'SegB', 12, TEAL)
    steps = [
        'Montează cutiile de sertar pe glisiere și verifică-le: ies și intră fără frecare, sunt paralele cu corpul.',
        'Deschide sertarul complet. Șterge fața exterioară a feței interioare a sertarului (și spatele frontului) de praf.',
        'Lipește 2 fâșii de bandă dublu adeziv de 25 × 100 mm pe fața interioară a sertarului, la 40 mm de fiecare capăt. Nu scoate încă folia.',
        'Pune distanțierele pe corp: 3 mm sub fiecare front (între front și baza corpului sau fronturile vecine) și 2 mm pe fiecare parte (vezi cotele din desen).',
        'Începe cu frontul de jos: scoate folia, apasă-l în poziție pe distanțiere, cu fața decorată spre exterior și muchia cu cant în față.',
        'Deschide sertarul cu grijă (frontul rămâne lipit) și fixează-l din interior cu 4 șuruburi 4 × 25 (desenul din pagina următoare), după ce ai găurit pilot Ø3 × 20 prin fața interioară.',
    ]
    top = 570
    for i, t in enumerate(steps, 1):
        h = P.para('<b>%d.</b> %s' % (i, t), 40 if i <= 3 else 620, top if i <= 3 else (570 + (i - 4) * 74), 540, st(10));
        if i <= 3: top += h + 8
    P.rect(620, 540, 530, 22, fill=PALE)
    P.text('Pașii 4–6 (continuare)', 630, 545, 'SegB', 10, TEAL)
    P.rect(40, 770, 1110, 40, fill=WARN, stroke=WARN_B, r=5)
    P.para('<b>Atenție:</b> banda dublu adeziv și adezivul nu țin singure frontul: greutatea sertarului încărcat și tracțiunea la deschidere îl smulg. Frontul se fixează întotdeauna și cu șuruburi.',
           52, 778, 1086, st(10))

    P.page('Fronturile de sertar în detaliu (2/2): fixare și reglaj', S.title)
    spate_front(P, PH, S, 40, 80, 560, 440)
    P.text('FIXARE', 640, 86, 'SegB', 12, TEAL)
    steps2 = [
        'Găurește pilot Ø3 × 20 mm prin fața interioară a sertarului, în punctele din desen, cu opritor de adâncime (burghiul NU trebuie să iasă prin fața frontului). Pentru reglaj, găurește fața interioară Ø5 și folosește șaibe.',
        'Pune șuruburile 4 × 25 cu șaibă și strânge-le ușor, cu mâna sau cu șurubelnița reglată pe cuplu mic. Nu strânge la maxim.',
        'Închide sertarul și verifică rosturile: 2 mm pe laterale, 3 mm între fronturi și sub front. Dacă un rost e prea mare, slăbește șuruburile, mută frontul cu ±1 mm și strânge din nou.',
        'Montează al doilea front (sertarul de sus) folosind primul front ca reper: 3 mm între ele, cu distanțier. Același proces: bandă, poziționare, găurire pilot, șuruburi.',
        'Dacă ai TIP-ON BLUMOTION: deschide și închide de câteva ori apăsând pe front, ca să verifici că mecanismul trage corect (poziția lui se reglează după fișa Blum).',
        'Scoate distanțierele. Verifică cu nivela că ambele fronturi sunt orizontale și aliniate cu laterala corpului. Șterge urmele de adeziv cu alcool izopropilic.',
    ]
    top = 112
    for i, t in enumerate(steps2, 1):
        h = P.para('<b>%d.</b> %s' % (i, t), 640, top, 510, st(10.5)); top += h + 8
    P.rect(40, 540, 560, 120, fill=OK, stroke=OK_B, r=5)
    P.text('VARIANTĂ CU CLEME BLUM (în loc de banda adezivă)', 54, 548, 'SegB', 10, OK_B)
    P.para('Dacă folosești cleme de fixare Blum pentru front (reglaj în 3 axe fără scule), montează-le pe cutia sertarului înainte de front, după șablonul Blum pentru tipul tău de sertar, '
           'și agață frontul pe ele. Găurile din front sunt cele din șablonul Blum (nu cele din acest desen). Verifică articolul exact (MOVENTO 760H cu cutie din lemn) în fișa tehnică Blum înainte să comanzi.',
           54, 566, 532, st(9.5))
    P.rect(640, 540, 510, 120, fill=WARN, stroke=WARN_B, r=5)
    P.text('GREȘELI FRECVENTE', 654, 548, 'SegB', 10, WARN_B)
    P.para('• Șuruburi prea lungi (4 × 30 sau mai mult): ies prin fața frontului. Folosește 4 × 25.<br/>• Front lipit cu bandă și lăsat așa: se desprinde după câteva zile.<br/>• Rosturi trase din ochi: folosește distanțiere.<br/>• Burghiu fără opritor: poți străpunge frontul.',
           654, 566, 484, st(9.5))
