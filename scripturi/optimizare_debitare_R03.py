"""Optimizare debitare R03 pe plăci 2800 × 2070 (blat 4100 × 600), din tmp/lista_debitare_R03.json.
- tăieturi ghilotină (cum taie fierăstrăul de panouri), margine 10 mm pe fiecare latură, pânză 4,4 mm;
- piesele uni se pot roti; piesele de stejar NU (fibra pe lungimea plăcii);
- pentru fiecare material se încearcă multe ordini (euristici + aleatoare, cu sămânță fixă) și se păstrează
  soluția cu cele mai puține plăci, apoi cu ultima placă cât mai liberă (rest refolosibil);
- VERIFICARE la final: fiecare piesă e o singură dată, în zona utilă, fără suprapuneri, cu pânza între piese;
  se calculează lungimea exactă a tăieturilor (inclusiv tunderea marginilor).
Iese: tmp/debitare_layout_R03.json"""
import json, random, itertools
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
L = json.loads((ROOT / 'tmp/lista_debitare_R03.json').read_text(encoding='utf-8'))
TRIM, KERF = 15.0, 4.4          # Regency: piesă max 2770 × 2040 → 15 mm pe fiecare margine
SHEET = {'BLAT38': (4100, 600)}
DEFAULT = (2800, 2070)
NOROT = {'STJ18', 'BLAT38'}


def pieces(mat):
    out = []
    for p in L['piese']:
        if p['mat'] != mat:
            continue
        for i in range(p['n']):
            out.append(dict(cod=p['cod'], inst='%s#%d' % (p['cod'], i + 1), den=p['den'], mob=p['mob'], Lp=p['L'], Wp=p['W'], forma=p['forma']))
    return out


def pack(pcs, order_key, rule, UL, UW, rot_ok, rnd=None):
    sheets = []

    def place(sh, pc):
        best = None
        for fi, (fx, fy, fw, fh) in enumerate(sh['free']):
            for rot in ((False, True) if rot_ok else (False,)):
                pw, ph = (pc['Wp'], pc['Lp']) if rot else (pc['Lp'], pc['Wp'])
                if pw <= fw + 1e-6 and ph <= fh + 1e-6:
                    score = (min(fw - pw, fh - ph), max(fw - pw, fh - ph))
                    if best is None or score < best[0]:
                        best = (score, fi, rot, pw, ph)
        if not best:
            return False
        _, fi, rot, pw, ph = best
        fx, fy, fw, fh = sh['free'].pop(fi)
        rw, rh = fw - pw - KERF, fh - ph - KERF
        if rule == 'sas':
            horiz = rw < rh
        elif rule == 'las':
            horiz = rw >= rh
        elif rule == 'area':
            horiz = pw * rh > ph * rw
        else:
            horiz = rnd.random() < 0.5
        cuts = []
        if horiz:      # întâi tăietura pe toată lățimea liberă, sub piesă; apoi cea scurtă, lângă piesă
            if rh > -KERF + 1e-6 and fh - ph > 1e-6:
                cuts.append(fw)
            if rw > -KERF + 1e-6 and fw - pw > 1e-6:
                cuts.append(ph)
            a = (fx + pw + KERF, fy, rw, ph)
            b = (fx, fy + ph + KERF, fw, rh)
        else:
            if rw > -KERF + 1e-6 and fw - pw > 1e-6:
                cuts.append(fh)
            if rh > -KERF + 1e-6 and fh - ph > 1e-6:
                cuts.append(pw)
            a = (fx + pw + KERF, fy, rw, fh)
            b = (fx, fy + ph + KERF, pw, rh)
        sh['placed'].append(dict(pc, x=round(fx, 1), y=round(fy, 1), w=pw, h=ph, rot=rot))
        sh['cut'] += sum(cuts)
        sh['free'] += [r for r in (a, b) if r[2] > 30 and r[3] > 30]
        return True

    for pc in sorted(pcs, key=order_key):
        if not any(place(sh, pc) for sh in sheets):
            sh = dict(free=[(0.0, 0.0, UL, UW)], placed=[], cut=0.0)
            if not place(sh, pc):
                raise ValueError('nu încape: %s %s × %s' % (pc['inst'], pc['Lp'], pc['Wp']))
            sheets.append(sh)
    return sheets


ORD = {'arie': lambda p: (-p['Lp'] * p['Wp'], p['inst']), 'lung': lambda p: (-max(p['Lp'], p['Wp']), -min(p['Lp'], p['Wp']), p['inst']),
       'lat': lambda p: (-min(p['Lp'], p['Wp']), -max(p['Lp'], p['Wp']), p['inst']), 'perim': lambda p: (-(p['Lp'] + p['Wp']), p['inst']),
       'L': lambda p: (-p['Lp'], -p['Wp'], p['inst']), 'W': lambda p: (-p['Wp'], -p['Lp'], p['inst'])}


def best_pack(pcs, UL, UW, rot_ok, tries=400):
    rnd = random.Random(184)
    best = None

    def consider(sh, how):
        nonlocal best
        used_last = sum(p['w'] * p['h'] for p in sh[-1]['placed'])
        key = (len(sh), used_last, sum(s['cut'] for s in sh))
        if best is None or key < best[0]:
            best = (key, sh, how)

    for (on, o), sr in itertools.product(ORD.items(), ('sas', 'las', 'area')):
        consider(pack(pcs, o, sr, UL, UW, rot_ok), on + '/' + sr)
    for t in range(tries):        # ordini aleatoare în jurul celei mai bune euristici (piesele mari tot primele)
        noise = {p['inst']: rnd.random() for p in pcs}
        o = lambda p, nz=noise: (-(p['Lp'] * p['Wp']) * (0.75 + 0.5 * nz[p['inst']]),)
        consider(pack(pcs, o, rnd.choice(('sas', 'las', 'area', 'rnd')), UL, UW, rot_ok, rnd), 'aleator %d' % t)
    return best[1], best[2]


def verify(sheets, pcs, UL, UW):
    seen = [p['inst'] for s in sheets for p in s['placed']]
    assert sorted(seen) == sorted(p['inst'] for p in pcs), 'piese lipsă / duble'
    for s in sheets:
        P = s['placed']
        for p in P:
            assert p['x'] >= -1e-6 and p['y'] >= -1e-6 and p['x'] + p['w'] <= UL + 1e-6 and p['y'] + p['h'] <= UW + 1e-6, ('iese din placă', p['inst'])
        for a, b in itertools.combinations(P, 2):
            sep = (a['x'] + a['w'] + KERF <= b['x'] + 1e-6 or b['x'] + b['w'] + KERF <= a['x'] + 1e-6 or
                   a['y'] + a['h'] + KERF <= b['y'] + 1e-6 or b['y'] + b['h'] + KERF <= a['y'] + 1e-6)
            assert sep, ('suprapunere / fără pânză', a['inst'], b['inst'])
    return True


res = {}
mats = sorted({p['mat'] for p in L['piese']})
for m in mats:
    SL, SW = SHEET.get(m, DEFAULT)
    trim = 0.0 if m == 'BLAT38' else TRIM
    UL, UW = SL - 2 * trim, SW - 2 * trim
    pcs = pieces(m)
    sheets, how = best_pack(pcs, UL, UW, m not in NOROT, tries=60 if len(pcs) < 16 else (40000 if m == 'HDF3' else 12000))
    verify(sheets, pcs, UL, UW)
    area = sum(p['Lp'] * p['Wp'] for p in pcs) / 1e6
    trim_cut = 0 if m == 'BLAT38' else 2 * SL + 2 * SW
    res[m] = dict(sheet=[SL, SW], trim=trim, kerf=KERF, n=len(sheets), pieces=len(pcs), area=round(area, 3),
                  util=round(area / (len(sheets) * SL * SW / 1e6) * 100, 1), how=how,
                  cut_m=round((sum(s['cut'] for s in sheets) + trim_cut * len(sheets)) / 1000, 1),
                  sheets=[dict(placed=s['placed'], free=[[round(v, 1) for v in r] for r in s['free']], cut_m=round(s['cut'] / 1000, 2),
                               used=round(sum(p['w'] * p['h'] for p in s['placed']) / (SL * SW) * 100, 1)) for s in sheets])
    print('%-7s %2d plăci  %3d piese  %5.2f m2  utilizare %4.1f%%  tăieturi %6.1f m  (%s)' % (m, len(sheets), len(pcs), area, res[m]['util'], res[m]['cut_m'], how))

(ROOT / 'tmp/debitare_layout_R03.json').write_text(json.dumps(dict(revizie='R03', trim=TRIM, kerf=KERF, materiale=res), ensure_ascii=False), encoding='utf-8')
print('VERIFICARE_OK')
