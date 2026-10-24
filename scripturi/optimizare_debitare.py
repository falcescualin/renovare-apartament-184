"""Optimizare debitare (nesting ghilotina) pe placi 2800 x 2070.
Scenariul A: doar dulapul din hol (lista exacta din excel_debitare.py).
Scenariul B: comanda comuna - dulap hol + panourile 18 mm masurate din modelul 3D (dressing, spalatorie, debara, baie,
noptiere, comode TV, fronturi bucatarie). Corpurile bucatariei nu sunt inca desfacute pe placi si lipsesc din B.
Iese: tmp/debitare_layout.json (folosit de debitare_pdf.py)."""
import json, itertools
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHEET_L, SHEET_W, TRIM, KERF = 2800, 2070, 10, 4.4
UL, UW = SHEET_L - 2 * TRIM, SHEET_W - 2 * TRIM

src = (ROOT / 'scripturi/excel_debitare.py').read_text(encoding='utf-8').split('# ---------------------------------------------------------------- gaurire')[0]
D = {}
exec(src, D)

MAT = {'Egger W1000 ST9 Premium White': 'W1000', 'Egger U702 ST9 Cashmere Grey': 'U702', 'HDF alb': 'HDF'}


def mat_key(p):
    return '%s %d mm' % (MAT[p[2]], p[3])


def hol_pieces():
    out = []
    for p in D['P']:
        cod, den, L, l, n = p[0], p[1], p[4], p[5], p[6]
        if cod == 'C09':      # rafturile trapez se pereche: doua piese intr-un dreptunghi 577 x 525, taiere oblica la final
            out += [dict(id='C09×2', inst=t, label='Raft colț ×2 (pereche)', L=577, W=525, mat=mat_key(p), rot=True, src='Dulap hol')
                    for t in ('C09.1+2', 'C09.3+4')]
            continue
        out += [dict(id=cod, inst=('%s.%d' % (cod, i + 1)) if n > 1 else cod, label=den, L=L, W=l, mat=mat_key(p), rot=True, src='Dulap hol')
                for i in range(n)]
    return out


def model_pieces():
    inv = json.loads((ROOT / 'tmp/inventar_panouri.json').read_text(encoding='utf-8'))
    out, split = [], []
    names = {'Dressing_custom': 'Dressing', 'Spalatorie_vestibul_custom': 'Spălătorie', 'Debara_custom': 'Debara', 'Baie_custom': 'Baie',
             'Noptiera_nord': 'Noptiere', 'Noptiera_sud': 'Noptiere', 'Perete_TV_custom': 'Comodă TV', 'Perete_TV_dormitor_custom': 'Comodă TV dormitor',
             'Bucatarie_custom': 'Bucătărie (fronturi)'}
    for x in inv:
        if x['col'] not in names or x['t'] not in (3.0, 16.0, 18.0):
            continue
        m = 'HDF' if x['t'] == 3.0 else 'W1000' if 'W1000' in x['mat'] else 'U702' if 'U702' in x['mat'] else 'H1145' if 'H1145' in x['mat'] else None
        if not m:
            continue
        L, W = x['L'], x['W']
        if L > UL:            # piese mai lungi decat placa: se imbina din doua bucati
            split.append('%s %s %d' % (names[x['col']], x['name'], L))
            half = round((L + 30) / 2)
            pcs = [half, half]
        else:
            pcs = [L]
        for LL in pcs:
            out.append(dict(id=x['name'][:22], inst=x['name'][:22], label=x['name'], L=LL, W=W, mat='%s %d mm' % (m, x['t']),
                            rot=(m != 'H1145'), src=names[x['col']]))
    return out, split


# ---------------------------------------------------------------- ghilotina cu dreptunghiuri libere
def pack(pieces, order, split_rule):
    sheets = []                                   # fiecare: dict(free=[...], placed=[...])

    def place(sh, pc):
        best = None
        for fi, (fx, fy, fw, fh) in enumerate(sh['free']):
            for rot in ((False, True) if pc['rot'] else (False,)):
                pw, ph = (pc['W'], pc['L']) if rot else (pc['L'], pc['W'])
                if pw <= fw + 1e-6 and ph <= fh + 1e-6:
                    score = (min(fw - pw, fh - ph), max(fw - pw, fh - ph))
                    if best is None or score < best[0]:
                        best = (score, fi, rot, pw, ph)
        if not best:
            return False
        _, fi, rot, pw, ph = best
        fx, fy, fw, fh = sh['free'].pop(fi)
        sh['placed'].append(dict(pc, x=fx, y=fy, w=pw, h=ph, rotated=rot))
        rw, rh = fw - pw - KERF, fh - ph - KERF   # resturi dupa taietura (cu latimea panzei)
        horiz = (rw < rh) if split_rule == 'sas' else (rw >= rh) if split_rule == 'las' else (pw * rh > ph * rw)
        if horiz:     # taietura pe toata lungimea dreptunghiului liber, sub piesa
            a = (fx + pw + KERF, fy, rw, ph); b = (fx, fy + ph + KERF, fw, rh)
        else:
            a = (fx + pw + KERF, fy, rw, fh); b = (fx, fy + ph + KERF, pw, rh)
        sh['free'] += [r for r in (a, b) if r[2] > 30 and r[3] > 30]
        return True

    for pc in sorted(pieces, key=lambda p: (order(p), p['inst'])):
        if not any(place(sh, pc) for sh in sheets):
            sh = dict(free=[(0, 0, UL, UW)], placed=[])
            if not place(sh, pc):
                raise ValueError('Piesa nu incape pe placa: %s %s' % (pc['id'], pc['L']))
            sheets.append(sh)
    return sheets


ORDERS = {'arie': lambda p: -p['L'] * p['W'], 'lung': lambda p: (-max(p['L'], p['W']), -min(p['L'], p['W'])),
          'lat': lambda p: (-min(p['L'], p['W']), -max(p['L'], p['W'])), 'perim': lambda p: -(p['L'] + p['W'])}


def best_pack(pieces):
    best = None
    for (on, o), sr in itertools.product(ORDERS.items(), ('sas', 'las', 'area')):
        sh = pack(pieces, o, sr)
        used_last = sum(p['w'] * p['h'] for p in sh[-1]['placed'])
        key = (len(sh), used_last)           # cat mai putine placi, apoi ultima placa cat mai goala (rest refolosibil)
        if best is None or key < best[0]:
            best = (key, sh, on + '/' + sr)
    return best[1], best[2]


def run(pieces):
    res = {}
    for m in sorted({p['mat'] for p in pieces}):
        pcs = [p for p in pieces if p['mat'] == m]
        sheets, how = best_pack(pcs)
        area = sum(p['L'] * p['W'] for p in pcs) / 1e6
        res[m] = dict(sheets=[s['placed'] for s in sheets], free=[[list(r) for r in s['free']] for s in sheets], n=len(sheets),
                      area=round(area, 2), util=round(area / (len(sheets) * SHEET_L * SHEET_W / 1e6) * 100, 1), how=how, pieces=len(pcs))
    return res


hol = hol_pieces()
model, split = model_pieces()
A = run(hol)
by_src = {}
for p in model:
    by_src.setdefault(p['src'], []).append(p)
separat = {s: run(v) for s, v in by_src.items()}
B = run(hol + model)
out = dict(sheet=[SHEET_L, SHEET_W], trim=TRIM, kerf=KERF, A=A, separat=separat, B=B, split=split)
(ROOT / 'tmp/debitare_layout.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
for m, r in A.items():
    print('A', m, r['n'], 'placi', r['util'], '%', r['how'])
tot_sep = {}
for s, rr in separat.items():
    for m, r in rr.items():
        tot_sep[m] = tot_sep.get(m, 0) + r['n']
for m, r in A.items():
    tot_sep[m] = tot_sep.get(m, 0) + r['n']
for m, r in B.items():
    print('B', m, r['n'], 'placi', r['util'], '% | separat:', tot_sep.get(m))
print('impartite:', split)
