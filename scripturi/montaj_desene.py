"""Desene de gaurire pe panou (fata si muchii), desenate cu reportlab din montaj_holes.compute().
Foloseste obiectul Pdf si stilurile din montaj_pdf (trimise ca argumente)."""
from reportlab.lib.colors import HexColor, white
import montaj_holes

INK = HexColor('#14323f'); MUT = HexColor('#6b7f87'); GRID = HexColor('#c9d6da'); WARN_B = HexColor('#c0562c')
SYM_COL = {'conf7': HexColor('#c0392b'), 'cep8': HexColor('#2a6fb8'), 'rail': HexColor('#2f8f88'), 'pilot5': HexColor('#2a6fb8'),
           'cup35': HexColor('#8e44ad'), 'pil25': HexColor('#8e44ad'), 'plate': HexColor('#d35400'), 'pin5': HexColor('#16a085'),
           'tipon': HexColor('#7f8c8d'), 'hang': HexColor('#d35400')}
FACE_HINT = {'stânga': 'fața dinspre stânga', 'dreapta': 'fața dinspre dreapta', 'sus': 'fața de sus', 'jos': 'fața de jos',
             'față': 'fața din față', 'spate': 'fața din spate'}


def flip_u(d, sign):
    """True daca, privit din exteriorul fetei (normala sign pe axa t), sistemul (u, v) nu e orientat direct => oglindim u."""
    a, b, t = d['u'], d['v'], d['t']
    c = [k for k in range(3) if k not in (a, b)][0]
    cyc = ((a, b, c) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)))
    cross_sign = 1 if cyc else -1                       # e_a x e_b = cross_sign * e_c
    n_dot = cross_sign * sign if c == t else 0
    return n_dot < 0


def draw_face(P, st, PH, x, top, w, h, code, d, fkey, fdata, label):
    c = P.c
    L, W, T = d['L'], d['W'], d['T']
    mx, my = 46, 46
    sc = min((w - mx - 20) / L, (h - my - 44) / W)
    pw_, ph_ = L * sc, W * sc
    ox, oy = x + mx, top + my
    flip = flip_u(d, fdata['sign'])

    def X(u): return ox + ((L - u) if flip else u) * sc

    def Y(v): return oy + (W - v) * sc
    P.rect(x, top, w, h, stroke=GRID, lw=.6, r=4)
    P.pill(x + 34, top + 12, code, size=9)
    P.para('<b>%s</b> · %s' % (label, FACE_HINT.get(fkey, fkey)), x + 66, top + 4, w - 72, st(9))
    c.setFillColor(HexColor('#f3f7f8')); c.setStrokeColor(INK); c.setLineWidth(1.1)
    c.rect(ox, PH - oy - ph_, pw_, ph_, stroke=1, fill=1)
    # marcajul muchiei din fata (+y)
    for axis, is_u in ((d['u'], True), (d['v'], False)):
        if axis == 1:
            c.setStrokeColor(WARN_B); c.setLineWidth(2.4)
            if is_u:
                xx = X(L); c.line(xx, PH - oy, xx, PH - oy - ph_)
                P.text('FAȚĂ', xx - 26 if xx > ox + pw_ / 2 else xx + 4, oy - 13, 'SegB', 7, WARN_B)
            else:
                yy = Y(W); c.line(ox, PH - yy, ox + pw_, PH - yy)
                P.text('FAȚĂ', ox + 4, yy - 12, 'SegB', 7, WARN_B)
    # contur glisiere
    for r in d.get('rails', []):
        if r['face'] == fkey and d['v'] == 2:
            yv = Y(r['z']); c.setStrokeColor(SYM_COL['rail']); c.setLineWidth(.9); c.setDash(3, 2)
            c.rect(ox, PH - yv - 5, pw_, 10, stroke=1, fill=0); c.setDash()
            P.text('glisieră MOVENTO', ox + pw_ / 2, yv + 7, 'Seg', 6.5, SYM_COL['rail'], 'c')
    us, vs = set(), set()
    for (u, v, kind, note) in fdata['holes']:
        col = SYM_COL.get(kind, INK); X0, Y0 = X(u), Y(v)
        if kind == 'conf7':
            c.setFillColor(white); c.setStrokeColor(col); c.setLineWidth(1.3); c.circle(X0, PH - Y0, 4.2, stroke=1, fill=1)
            c.line(X0 - 3, PH - Y0, X0 + 3, PH - Y0); c.line(X0, PH - Y0 - 3, X0, PH - Y0 + 3)
        elif kind == 'cep8':
            c.setStrokeColor(col); c.setLineWidth(1.1); c.setDash(2, 1.5)
            pth = c.beginPath(); pth.moveTo(X0, PH - Y0 + 4.5); pth.lineTo(X0 + 4.5, PH - Y0); pth.lineTo(X0, PH - Y0 - 4.5); pth.lineTo(X0 - 4.5, PH - Y0); pth.close()
            c.drawPath(pth, stroke=1, fill=0); c.setDash()
        elif kind == 'rail':
            c.setFillColor(col); c.setStrokeColor(white); c.setLineWidth(.8); c.circle(X0, PH - Y0, 3.4, stroke=1, fill=1)
        elif kind == 'cup35':
            r_ = max(5.0, 17.5 * sc)
            c.setStrokeColor(col); c.setFillColor(HexColor('#efe3f5')); c.setLineWidth(1.2); c.circle(X0, PH - Y0, r_, stroke=1, fill=1)
            c.line(X0 - 3, PH - Y0, X0 + 3, PH - Y0); c.line(X0, PH - Y0 - 3, X0, PH - Y0 + 3)
        elif kind in ('pil25', 'plate', 'tipon', 'hang'):
            c.setFillColor(col); c.setStrokeColor(col); c.setLineWidth(.6); c.circle(X0, PH - Y0, 1.8, stroke=1, fill=1)
        elif kind == 'pin5':
            c.setStrokeColor(col); c.setFillColor(white); c.setLineWidth(.9); c.circle(X0, PH - Y0, 2.4, stroke=1, fill=1)
        us.add(round(u)); vs.add(round(v))

    def ticks(vals, horiz):
        last = -99
        for val in sorted(vals):
            if horiz:
                xx = X(val)
                if abs(xx - last) < 20: continue
                last = xx; c.setStrokeColor(MUT); c.setLineWidth(.4); c.line(xx, PH - oy + 2, xx, PH - oy + 7)
                P.text(str(val), xx, oy - 22, 'Seg', 6.8, MUT, 'c')
            else:
                yy = Y(val)
                if abs(yy - last) < 10: continue
                last = yy; c.setStrokeColor(MUT); c.setLineWidth(.4); c.line(ox - 7, PH - yy, ox - 2, PH - yy)
                P.text(str(val), ox - 10, yy - 4, 'Seg', 6.8, MUT, 'r')
    ticks(us, True); ticks(vs, False)
    P.text('%g' % L, ox + pw_ / 2, oy + ph_ + 6, 'SegB', 8, INK, 'c')
    P.text('%g × %g' % (W, T), ox + pw_ + 4, oy + ph_ / 2 - 5, 'SegB', 8, INK)
    kinds = {}
    for (u, v, kind, note) in fdata['holes']: kinds[kind] = kinds.get(kind, 0) + 1
    names = {'conf7': 'confirmat Ø7 (trecere)', 'cep8': 'cep Ø8 × 12 (față opusă)', 'rail': 'prindere glisieră (Ø3 × 13)',
             'cup35': 'cupă balama Ø35 × 13', 'pil25': 'pilot Ø2,5 (flanșă / placă TIP-ON)', 'plate': 'plăcuță balama Ø2,5 × 12',
             'pin5': 'pin raft Ø5 × 12', 'tipon': 'adaptor TIP-ON Ø2,5', 'hang': 'agățătoare Ø2,5 × 12'}
    ly = oy + ph_ + 22
    for k, n in kinds.items():
        c.setStrokeColor(SYM_COL.get(k, INK)); c.setFillColor(SYM_COL.get(k, INK)); c.circle(ox + 4, PH - ly - 3, 2.6, stroke=1, fill=(k == 'rail'))
        P.text('%d × %s' % (n, names.get(k, k)), ox + 12, ly - 2, 'Seg', 7.5, INK); ly += 11


def draw_edge(P, st, PH, x, top, w, h, code, d, ed, label):
    c = P.c
    L, W, T = d['L'], d['W'], d['T']
    mx, my = 34, 46
    sc = min((w - mx - 34) / L, (h - my - 92) / W)
    pw_, ph_ = L * sc, W * sc
    ox, oy = x + mx, top + my
    P.rect(x, top, w, h, stroke=GRID, lw=.6, r=4)
    P.pill(x + 34, top + 12, code, size=9)
    P.para('<b>%s</b> · %s (pe care vine %s)' % (label, ed['edge'], ed['with_']), x + 66, top + 4, w - 72, st(9))
    c.setFillColor(HexColor('#f3f7f8')); c.setStrokeColor(INK); c.setLineWidth(1.1); c.rect(ox, PH - oy - ph_, pw_, ph_, stroke=1, fill=1)
    sign = ed['sign']
    hook = ed.get('tip') == 'hook6'
    col_e = HexColor('#8e44ad') if hook else SYM_COL['pilot5']
    c.setStrokeColor(col_e); c.setLineWidth(3.2)
    if ed['axis'] == 'u':
        xx = ox if sign < 0 else ox + pw_
        c.line(xx, PH - oy, xx, PH - oy - ph_)
    else:
        yy = oy + ph_ if sign < 0 else oy
        c.line(ox, PH - yy, ox + pw_, PH - yy)
    for pv in ed['pos']:
        c.setStrokeColor(col_e); c.setFillColor(white); c.setLineWidth(1.2)
        if ed['axis'] == 'u':
            xx = ox if sign < 0 else ox + pw_; yy = oy + (W - pv) * sc
            c.circle(xx, PH - yy, 3.8, stroke=1, fill=1)
            P.text('%g' % pv, (ox - 8) if sign < 0 else (ox + pw_ + 8), yy - 4, 'Seg', 7, MUT, 'r' if sign < 0 else 'l')
        else:
            yy = oy + ph_ if sign < 0 else oy; xx = ox + pv * sc
            c.circle(xx, PH - yy, 3.8, stroke=1, fill=1)
            P.text('%g' % pv, xx, (yy + 8) if sign < 0 else (yy - 17), 'Seg', 7, MUT, 'c')
    P.text('%g' % L, ox + pw_ / 2, oy + ph_ + 16, 'SegB', 8, INK, 'c')
    P.text('%g × %g' % (W, T), ox + pw_ + 6, oy + ph_ / 2 - 5, 'SegB', 8, INK)
    if hook:
        P.para('<b>1</b> gaură <b>Ø6 × 10</b> în capătul din spate, la <b>%g mm de fața exterioară</b> (cea dinspre corp) și <b>%g mm de muchia de jos</b>: '
               'aici intră cârligul glisierei MOVENTO. Fă-o pe ambele laterale ale sertarului, oglindit.' % (ed.get('off', 7), ed['pos'][0]), x + 12, top + h - 50, w - 24, st(8, MUT))
    else:
        P.para('<b>%d</b> găuri pilot Ø5 × 55 în muchia îngroșată, la mijlocul grosimii (%g mm de fețe), pentru confirmate; cepuri Ø8 între ele.' % (len(ed['pos']), T / 2),
               x + 12, top + h - 44, w - 24, st(8, MUT))


def drilling_pages(P, st, PH, S, R03):
    info = montaj_holes.compute(S)
    cells, seen = [], set()
    for pid, d in info.items():
        p = d['p']; code = p['code']
        if code not in R03: continue
        sig = (code, tuple(sorted((k, tuple(sorted((round(u), round(v), t) for u, v, t, n in fd['holes']))) for k, fd in d['faces'].items())),
               tuple(sorted((e['edge'], tuple(e['pos'])) for e in d['edges'])))
        if sig in seen: continue
        seen.add(sig)
        for fk, fd in sorted(d['faces'].items()):
            if fd['holes']: cells.append(('face', code, d, fk, fd, p['label']))
        for e in d['edges']:
            cells.append(('edge', code, d, e, None, p['label']))
    cells.sort(key=lambda c: (c[1], c[0]))
    CW, CH = 360, 320
    pages = [cells[i:i + 6] for i in range(0, len(cells), 6)] or [[]]
    for pi, grp in enumerate(pages, 1):
        P.page('Desene de găurire (%d/%d)' % (pi, len(pages)), S.title)
        for i, cell in enumerate(grp):
            cx = 40 + (i % 3) * (CW + 15); cy = 80 + (i // 3) * (CH + 12)
            if cell[0] == 'face': draw_face(P, st, PH, cx, cy, CW, CH, cell[1], cell[2], cell[3], cell[4], cell[5])
            else: draw_edge(P, st, PH, cx, cy, CW, CH, cell[1], cell[2], cell[3], cell[5])
        P.para('<b>Cum se citește:</b> panoul e desenat cum îl vezi cu fața spre tine; <font color="#c0562c"><b>FAȚĂ</b></font> marchează muchia din față a corpului. '
               'Cotele de sus și din stânga sunt distanțele de la colțul panoului la centrul găurilor (mm). '
               '<font color="#c0392b">Cercul cu cruce</font> = confirmat Ø7 (trecere); <font color="#2a6fb8">rombul punctat</font> = cep Ø8 pe fața opusă; '
               '<font color="#2f8f88">punctul turcoaz</font> = prindere glisieră. Găurile din muchii sunt pe desenele „muchie”, cu muchia îngroșată.',
               40, 80 + 2 * (CH + 12) + 4, 1110, st(9, MUT))
