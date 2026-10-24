"""Pagini PDF: feroneria in imagini 3D (card pe articol) si fiecare placa in vedere izometrica cu gaurile si feroneria explodata (stil IKEA)."""
from pathlib import Path
import json
from reportlab.lib.colors import HexColor, white
import montaj_panouri
from feronerie_catalog import INFO

ROOT = Path(__file__).resolve().parents[1]
FER = ROOT / 'tmp' / 'feronerie_R2' / 'png'
INK = HexColor('#14323f'); TEAL = HexColor('#2f8f88'); MUT = HexColor('#6b7f87'); GRID = HexColor('#c9d6da'); PALE = HexColor('#e7f3f1')
KIND_TXT = {
    'conf7': ('Ø7 de trecere', 'confirmat'), 'cep8': ('Ø8 × %g (oarbă)', 'cep'), 'rail': ('Ø3 × 13 pilot', 'surub_3_5x15'), 'pilot5': ('Ø5 × 55 pilot în muchie', None)}
KIND_NAME = {'conf7': 'confirmat Ø7 × 50', 'cep8': 'cep Ø8 × 35', 'rail': 'șurub Blum 3,5 × 15 (609.1500)', 'pilot5': 'gaură pilot pentru confirmat',
             'hook6': 'pentru cârligul din spate al glisierei MOVENTO', 'cup35': 'cupa balamalei Blum', 'pin5': 'pin de raft',
             'plate': 'plăcuța balamalei (2 șuruburi 3,5 × 15)', 'tipon': 'adaptorul TIP-ON', 'hang': 'agățătoarea corpului',
             'pil25': 'șurub 3,5 × 17 / placă TIP-ON'}


def hardware_cards(P, st, PH, S):
    items = [h for h in S.hw if h.get('model')]
    if not items: return
    per = 6
    pages = [items[i:i + per] for i in range(0, len(items), per)]
    for pi, grp in enumerate(pages, 1):
        P.page('Feroneria în imagini 3D (%d/%d)' % (pi, len(pages)), S.title)
        for i, h in enumerate(grp):
            cx = 40 + (i % 3) * 375; cy = 84 + (i // 3) * 350
            P.rect(cx, cy, 360, 338, stroke=GRID, lw=.6, r=5)
            P.dot(cx + 22, cy + 22, h['letter'], size=12)
            P.para('<b>%s</b>' % h['name'], cx + 48, cy + 10, 300, st(11))
            P.img(FER / (h['model'] + '.png'), cx + 14, cy + 52, 332, 200)
            inf = INFO.get(h['model'])
            if inf: P.para('<font color="#6b7f87">%s · model %s</font>' % (inf[3], inf[6]), cx + 14, cy + 258, 332, st(9))
            P.para('<b>Cantitate:</b> %s · <b>Pași:</b> %s<br/>%s' % (h['qty'], h['steps'], h['note']), cx + 14, cy + 290, 332, st(9.5))
        P.para('Imaginile sunt modele 3D la scară proprie (fiecare articol încadrat separat). Modele CAD: <b>feronerie_3d.FCStd</b>; STEP / OBJ în <b>tmp/feronerie_R2/</b>. „exact” = după standard / fișa oficială; „gabarit” = cote de montaj Blum, mecanism simplificat.', 40, 792, 1110, st(9, MUT))


def kind_line(kind, hs):
    n = len(hs); h0 = hs[0]
    if kind == 'conf7': return n, 'Ø7 mm, de trecere (grosimea plăcii)', 'confirmat'
    if kind == 'cep8': return n, 'Ø8 mm, adâncime %g mm' % h0['depth'], 'cep'
    if kind == 'rail': return n, 'Ø3 mm, adâncime 13 mm', 'surub_3_5x15'
    if kind == 'hook6': return n, 'Ø6 mm, adâncime 10 mm, în capătul din spate', None
    if kind == 'cup35': return n, 'Ø35 mm, adâncime 13 mm (Forstner)', 'balama_blum'
    if kind == 'pin5': return n, 'Ø5 mm, adâncime 12 mm', 'pin_raft'
    if kind == 'plate': return n, 'Ø2,5 mm, adâncime 12 mm', 'placuta_balama'
    if kind == 'tipon': return n, 'Ø2,5 mm, adâncime 10 mm', 'adaptor_tipon'
    if kind == 'hang': return n, 'Ø2,5 mm, adâncime 12 mm', 'suport_suspendare'
    if kind == 'pil25': return n, 'Ø2,5 mm, adâncime 8–10 mm', 'surub_3_5x17'
    return n, 'Ø5 mm, adâncime 55 mm, în muchie, la mijlocul grosimii', None


def panel_pages(P, st, PH, S, folder, uniq):
    folder = Path(folder)
    imgs = json.loads((folder / 'panouri' / 'panouri_imagini.json').read_text(encoding='utf-8'))
    for u in uniq:
        files = imgs.get(u['id'], [])
        views = u['views']
        P.page('Placa %s: %s' % (u['code'], u['label']), S.title)
        P.pill(70, 92, u['code'], size=13)
        L, W, T = u['size']
        P.para('<b>%g × %g × %g mm</b> · %d buc. %s' % (L, W, T, u['count'],
               '(piesele stânga/dreapta sunt în oglindă)' if u['code'] in ('N-01', 'N-S.L', 'N-07') else ''), 110, 84, 640, st(12))
        n = len(views)
        cols = 2 if n > 1 else 1
        rows = (n + cols - 1) // cols
        cw = 560 if cols == 2 else 1110; ch = 330 if rows == 2 else 680 if rows == 1 else 330
        if rows == 1 and cols == 2: ch = 560
        for k, v in enumerate(views):
            cx = 40 + (k % cols) * (cw + 10); cy = 118 + (k // cols) * (ch + 10)
            if cy + ch > 810: break
            P.rect(cx, cy, cw, ch, stroke=GRID, lw=.6, r=5)
            P.text(v['name'].upper(), cx + 14, cy + 10, 'SegB', 10, TEAL)
            ih = ch - 110
            P.img(folder / 'panouri' / files[k], cx + 6, cy + 28, cw - 12, ih)
            ly = cy + 28 + ih + 8
            by_kind = {}
            for h in v['holes']: by_kind.setdefault(h['kind'], []).append(h)
            lx = cx + 14
            for kind, hs in by_kind.items():
                n_, desc, model = kind_line(kind, hs)
                if model and (FER / (model + '.png')).exists():
                    P.img(FER / (model + '.png'), lx, ly - 2, 54, 40)
                    P.para('<b>%d ×</b> gaură %s<br/><font color="#6b7f87">%s</font>' % (n_, desc, KIND_NAME[kind]), lx + 60, ly, 190, st(8.5))
                else:
                    P.rect(lx + 18, ly + 6, 16, 16, fill=HexColor('#10161a'), r=8)
                    P.para('<b>%d ×</b> gaură %s<br/><font color="#6b7f87">%s</font>' % (n_, desc, KIND_NAME[kind]), lx + 60, ly, 190, st(8.5))
                lx += 262
                if lx + 250 > cx + cw:
                    lx = cx + 14; ly += 44
        P.para('Pozițiile exacte (cote de la colțuri) sunt pe paginile „Desene de găurire”. Hardware-ul 3D este mărit de 1,7× față de gaură, ca să se vadă clar, și trasat explodat deasupra găurii.',
               40, 800, 1110, st(8.5, MUT))
