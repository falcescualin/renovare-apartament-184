# R11 - trasee copex prin sapa (Claude), din punctele R10 (Codex), cu retea de culoare corectata.
# Retea = arbore planar: tuburile dintr-un manunchi sunt ordonate dupa ordinea ramificatiilor,
# deci tuburile de forta nu se incruciseaza intre ele. Curentii slabi au arbore separat.
# Iesire: tmp/electric_R11/trasee_R11.json. Nu modifica fisierele R10.
from pathlib import Path
import json, math, collections

R = Path(__file__).resolve().parents[1]
OUT = R / 'tmp' / 'electric_R11'; OUT.mkdir(parents=True, exist_ok=True)
r10 = json.loads((R / 'output/pdf/Apartament_184_Revizie_electrica_R10.json').read_text(encoding='utf-8'))
arch = json.loads((R / 'tmp/termic_model.json').read_text(encoding='utf-8'))

ZF = -40           # axa tuburilor in sapa, mm sub pardoseala finita (conventie; se confirma dupa masurare)
GAP = 10           # spatiu liber intre tuburi alaturate, mm
Z_CORNISA = 2350   # traseul aparent TE -> coloana, in caseta de gips-carton peste tocul usii
TE = [9956, -4330, 2300]

# ---------- puncte (centre aparataj, coordonate model, mm) ----------
P = {t['destination']: list(t['points'][-1]) for t in r10['tubes']}
P.update({
    'NET': [7350, -5540, 2000],   # cutie media ONT/patch (R10: X7900) mutata spre stanga, langa usa camerei
    'P23': [7600, -5540, 2000],   # 4 prize router, langa cutia NET
    'F01': [5300, -5544, 2425],   # sursa LED dressing, decalata 100 mm de P11 (altfel coboara in acelasi loc)
    'J01': [9330, -3590, 2400],
    'J05': [7900, -3470, 2400],   # doza bucatarie pe peretele usii, chiar in spatele lui S03 (R10: X9000)
    'F06': [7250, -3300, 2300],   # sursa LED sub corpuri, la capatul dinspre usa (R10: Y-2200)
    'J03': [2515, -3845, 2400],   # doza dormitor deasupra lui S01, langa usa (R10: pe peretele estic)   # doza hol mutata in caseta coloanei (R10: X7250), acces la capacul casetei
    'AP1': [3700, -1575, 1525],   # aplica liniara TV sufragerie stanga (perete_TV.FCStd, Z 1200-1850)
    'AP2': [3700, -3725, 1525],   # aplica liniara TV sufragerie dreapta
    'M1': [3550, -350, 755],     # baza benzii LED 24 V a oglinzii, partea ferestrei (perete_TV_dormitor.FCStd)
    'AC': [160, -340, 2200],      # unitate interioara AC dormitor (masca de riflaje NV), alimentare C15
    'W1': [3700, -2750, 1350], 'W2': [3700, -2690, 350], 'W3': [3550, -1800, 1410], 'W4': [3700, -790, 600],
})
P['TE'] = TE
DROP = {'S09': [157, -780], 'F07': [900, -5544]}   # coborari decalate fata de centrul aparatului
INFO = {
    'P01': 'Priza noptiera spre dulap', 'P02': 'Priza noptiera spre fereastra', 'P03': 'Priza dulap dormitor / sursa LED (sus)',
    'P04': 'Priza TV dormitor', 'P05': 'Priza dubla masa machiaj', 'P06': 'Priza TV sufragerie sus', 'P07': 'Priza tripla comoda TV',
    'P08': 'Priza dubla langa canapea', 'P09': 'Priza dubla birou (laterala)', 'P10': 'Modul birou 2 Schuko + RJ45',
    'P11': 'Priza fier de calcat (dressing M3)', 'P12': 'Priza masina de spalat rufe', 'P13': 'Prize baie IP44 (uscator/aparat ras)',
    'P14': 'Priza frigider', 'P15': 'Priza dubla masa bucatarie', 'P16': 'Priza hota', 'P17': 'Priza masina de spalat vase',
    'P18': 'Priza aprindere plita gaz', 'P19': 'Priza sub chiuveta', 'P20': 'Priza cuptor', 'P21': 'Priza microunde',
    'P22': 'Priza dubla contrablat', 'P23': 'Prize router/ONT (4x)',
    'S01': 'Intrerupator cap-scara dormitor (usa)', 'S02': 'Intrerupator dublu sufragerie: plafoniera + aplice TV', 'AP1': 'Aplica liniara TV sufragerie (stanga)',
    'AP2': 'Aplica liniara TV sufragerie (dreapta)', 'M1': 'Banda LED 24 V oglinda machiaj (fereastra) - din sursa F03', 'S03': 'Intrerupator dublu bucatarie (in hol)',
    'S04': 'Intrerupator hol (la intrare)', 'S05': 'Intrerupator debara', 'S06': 'Intrerupator balcon', 'S07': 'Intrerupator vestibul',
    'S08': 'Intrerupator dublu baie: lumina + ventilator', 'S09': 'Intrerupator cap-scara langa pat',
    'F01': 'Alimentare sursa LED dressing', 'F02': 'Alimentare sursa LED mobilier TV sufragerie', 'F03': 'Alimentare LED TV + oglinda dormitor',
    'F04': 'Alimentare sursa LED dulap hol', 'F05': 'Alimentare LED debara', 'F06': 'Alimentare LED sub corpuri bucatarie',
    'F07': 'Ventilator baie (L, N, PE, LT)', 'J01': 'Doza derivatie hol', 'J02': 'Doza derivatie sufragerie', 'J03': 'Doza derivatie dormitor',
    'J04': 'Doza derivatie vestibul', 'J05': 'Doza derivatie bucatarie', 'J06': 'Doza derivatie debara',
    'W1': 'Doza date+TV sufragerie sus', 'W2': 'Doza date+TV comoda sufragerie', 'W3': 'Doza date+TV dormitor', 'W4': 'Doza date birou',
    'AC': 'Aer conditionat dormitor, alimentare unitate interioara (C15)', 'NET': 'Cutie media (ONT, patch-panel, splitter TV)', 'TE': 'Tablou electric',
}

# ---------- arbori de culoare ----------
# nod: (x, y); muchii parinte -> copil
POWER = dict(
    nodes=dict(R0=(9300, -3600), A1=(9300, -4250), H_K=(8450, -4250),
               H_KS=(8450, -5300), H_KW=(7600, -5300),
               Z_D=(6900, -4250), Z_EN=(6900, -450), Z_NW=(6180, -450), Z_W=(3900, -4250), Z_N=(3900, -370),
               V_E=(3250, -4250), V_S=(3250, -5450), V_W=(2700, -4250), V_N=(2700, -4050), V_B=(2700, -4550),
               B_D=(2250, -4550), B_S=(1650, -4550), B_W=(900, -4550),
               DM_E=(3250, -3600), DM_C=(3250, -3100), DM_N=(3250, -256), DM_W=(400, -3100), DM_WN=(400, -330),
               K_D=(8450, -3300), K_W=(7450, -3300), K_WN=(7450, -450), K_E=(9600, -3300), K_EN=(9600, -1850),
               K_EN2=(9600, -700), DB_D=(10050, -1850), DB_N=(10050, -400), DB_S=(10050, -2350)),
    edges=[('R0', 'A1'), ('A1', 'H_K'), ('H_K', 'H_KS'), ('H_KS', 'H_KW'),
           ('H_K', 'Z_D'), ('Z_D', 'Z_EN'), ('Z_EN', 'Z_NW'), ('Z_D', 'Z_W'), ('Z_W', 'Z_N'), ('Z_W', 'V_E'),
           ('V_E', 'V_S'), ('V_E', 'V_W'), ('V_W', 'V_N'), ('V_W', 'V_B'), ('V_B', 'B_D'), ('B_D', 'B_S'), ('B_S', 'B_W'),
           ('V_E', 'DM_E'), ('DM_E', 'DM_C'), ('DM_C', 'DM_N'), ('DM_C', 'DM_W'), ('DM_W', 'DM_WN'),
           ('H_K', 'K_D'), ('K_D', 'K_W'), ('K_W', 'K_WN'), ('K_D', 'K_E'), ('K_E', 'K_EN'), ('K_EN', 'K_EN2'),
           ('K_EN', 'DB_D'), ('DB_D', 'DB_N'), ('DB_D', 'DB_S')],
    root='R0',
    # aparat -> muchia pe care se racordeaza (derivatie perpendiculara) sau nodul de capat
    leaves={'P23': ('H_KS', 'H_KW'), 'F04': ('H_KS', 'H_KW'),
            'S02': ('Z_D', 'Z_EN'), 'P08': ('Z_D', 'Z_EN'), 'S06': ('Z_EN', 'Z_NW'),
            'P11': ('Z_D', 'Z_W'), 'F01': ('Z_D', 'Z_W'),
            'S07': ('Z_W', 'Z_N'), 'AP2': ('Z_W', 'Z_N'), 'AP1': ('Z_W', 'Z_N'), 'P07': ('Z_W', 'Z_N'), 'F02': ('Z_W', 'Z_N'), 'P10': ('Z_W', 'Z_N'), 'P09': ('Z_W', 'Z_N'),
            'P12': 'V_S', 'S08': ('V_W', 'V_N'), 'P13': 'B_S', 'F07': 'B_W',
            'S01': 'DM_E', 'P04': ('DM_C', 'DM_N'), 'F03': ('DM_C', 'DM_N'), 'M1': ('DM_C', 'DM_N'), 'P05': 'DM_N',
            'P03': ('DM_C', 'DM_W'), 'P01': ('DM_W', 'DM_WN'), 'P02': ('DM_W', 'DM_WN'), 'S09': ('DM_W', 'DM_WN'), 'AC': 'DM_WN',
            'S03': ('H_K', 'Z_D'), 'P19': ('K_W', 'K_WN'), 'P17': ('K_W', 'K_WN'), 'P18': ('K_W', 'K_WN'), 'P22': ('K_W', 'K_WN'),
            'P16': ('K_W', 'K_WN'), 'P20': ('K_W', 'K_WN'), 'P21': ('K_W', 'K_WN'),
            'P14': ('K_E', 'K_EN'), 'S05': ('K_EN', 'K_EN2'), 'P15': ('K_EN', 'K_EN2'),
            },
)
WEAK = dict(
    nodes=dict(NET0=(7350, -5540), NU=(7350, -5000), NE=(9640, -5000), WR=(9640, -4930), ND2=(7350, -4780),
               ZD=(6900, -4780), ZDW=(4100, -4780), ZDN=(4100, -790), VD=(3420, -4780), DMD=(3420, -1800)),
    edges=[('NET0', 'NU'), ('NU', 'NE'), ('NE', 'WR'), ('NU', 'ND2'), ('ND2', 'ZD'), ('ZD', 'ZDW'), ('ZDW', 'ZDN'),
           ('ZDW', 'VD'), ('VD', 'DMD')],
    root='NET0',
    leaves={'W1': ('ZDW', 'ZDN'), 'W2': ('ZDW', 'ZDN'), 'W4': ('ZDW', 'ZDN'), 'W3': 'DMD'},
)

# ---------- tuburi ----------
L3 = 'L, N, PE'
TUBES = []
def tub(i, a, b, c, kind, sec, n, roles, d=20, net='P', note=''):
    TUBES.append(dict(id=i, src=a, dst=b, circuit=c, kind=kind, section=sec, wires=n, roles=roles, d=d, net=net, note=note))
# Circuite de prize / receptoare: membrii se inlantuie automat in ordinea ramificatiilor (fara incrucisari intre ei)
# fiecare lista interioara = o plecare din TE (un circuit poate avea doua plecari, prin borna de distributie din tablou)
SOCKETS = {
    'C04': [['P01', 'P02', 'P03'], ['P04', 'P05', 'F03']],              # F03: LED TV + oglinda dormitor, permanent
    'C05': [['P11', 'F01'], ['P06', 'P07', 'P08', 'P09', 'P10', 'F02']], # F01/F02: surse LED mobilier, comanda proprie
    'C06': [['P13']], 'C07': [['P12']], 'C08': [['P17', 'P18']], 'C09': [['P20']],
    'C10': [['P19'], ['P15']], 'C11': [['P14']], 'C12': [['P23', 'F04']], 'C13': [['P21']], 'C14': [['P22', 'P16']], 'C15': [['AC']],
}
LOCAL = {('P06', 'P07'): 'local, vertical in perete / mobilier TV'}
# Iluminat: fiecare doza J are tub propriu din TE; J01 sta in caseta coloanei, langa TE
LIGHT = [   # decizie beneficiar 07.10: din intrerupator se urca prin perete pe tavan pana la lampa; fara doze J
    ('T01', 'TE', 'S02', 'C01', 'S', 3, L3),
    ('T01e', 'S02', 'AP2', 'C01', 'A', 3, 'retur aplice (tasta 2 S02), N, PE'),
    ('T01f', 'AP2', 'AP1', 'C01', 'A', 3, 'retur aplice, N, PE'), ('T01b', 'TE', 'S06', 'C01', 'S', 3, L3), ('T01c', 'TE', 'S01', 'C01', 'S', 3, L3),
    ('T01d', 'S01', 'S09', 'C01', 'S', 5, 'naveta A, naveta B, retur L01 (inapoi spre S01), N, PE'),
    ('T02', 'TE', 'S04', 'C02', 'S', 3, L3, 'local, in caseta coloanei'),
    ('T02b', 'TE', 'S03', 'C02', 'S', 3, L3), ('T02c', 'TE', 'S05', 'C02', 'S', 3, L3),
    ('T03', 'TE', 'S07', 'C03', 'S', 3, L3), ('T03b', 'TE', 'S08', 'C03', 'S', 3, L3),
    ('T03c', 'S08', 'F07', 'C03', 'F', 4, 'L permanent, N, PE, retur F07 (LT)'),
]
SELV = [('V01', 'F03', 'M1', 'C04', 'V', 2, '+24 V, 0 V (SELV, din sursa F03); 2 x 1 mm2', 16)]
for it in LIGHT:
    tub(it[0], it[1], it[2], it[3], it[4], 1.5, it[5], it[6], note=it[7] if len(it) > 7 else '')
for it in SELV:
    tub(it[0], it[1], it[2], it[3], it[4], 1.0, it[5], it[6], d=it[7], note='SELV 24 V - tub separat de 230 V')
# Curenti slabi - stea din cutia NET, cablu continuu, tub separat de forta
tub('W0', 'TE', 'NET', 'NET', 'W', None, 1, 'fibra / cablu operator + sarma de tragere', d=25, net='W')
tub('W5', 'TE', 'NET', 'REZ', 'W', None, 0, 'rezerva goala, cu sarma de tragere', d=25, net='W')
tub('W1', 'NET', 'W1', 'LAN+TV', 'D', None, 2, '1 Cat6 U/UTP + 1 coaxial RG6', d=25, net='W')
tub('W2', 'NET', 'W2', 'LAN+TV', 'D', None, 2, '1 Cat6 U/UTP + 1 coaxial RG6', d=25, net='W')
tub('W3', 'NET', 'W3', 'LAN+TV', 'D', None, 2, '1 Cat6 U/UTP + 1 coaxial RG6', d=25, net='W')
tub('W4', 'NET', 'W4', 'LAN', 'D', None, 1, '1 Cat6 U/UTP', d=20, net='W')

# ---------- orientarea peretelui fiecarui aparat ----------
edges_w = [e for e in arch['wall_edges'] if len(e) == 2]
def wall_side(p):
    best = None
    for (a, b) in edges_w:
        if abs(a[0] - b[0]) < 1:
            lo, hi = sorted([a[1], b[1]])
            if lo - 5 <= p[1] <= hi + 5:
                dd = abs(p[0] - a[0]); best = min(best or (1e9, ''), (dd, 'x'))
        elif abs(a[1] - b[1]) < 1:
            lo, hi = sorted([a[0], b[0]])
            if lo - 5 <= p[0] <= hi + 5:
                dd = abs(p[1] - a[1]); best = min(best or (1e9, ''), (dd, 'y'))
    return best[1]
def foot(name): return tuple(DROP.get(name, P[name][:2]))

# ---------- construire arbore cu frunze ----------
def build(spec):
    nodes = dict(spec['nodes']); parent = {}; children = collections.defaultdict(list); orig = {}
    for a, b in spec['edges']: parent[b] = a; children[a].append(b); orig[b] = (a, b)
    # derivatii pe muchii: sparg muchia in punctul proiectiei
    taps = collections.defaultdict(list)
    for leaf, att in spec['leaves'].items():
        if isinstance(att, tuple):
            a, b = att; pa, pb = nodes[a], nodes[b]; f = foot(leaf)
            tp = (pa[0], f[1]) if pa[0] == pb[0] else (f[0], pa[1])
            taps[att].append((leaf, tp))
    for (a, b), lst in taps.items():
        pa, pb = nodes[a], nodes[b]; ax = 1 if pa[0] == pb[0] else 0
        lo, hi = sorted([pa[ax], pb[ax]])
        for leaf, tp in lst: assert lo - .5 <= tp[ax] <= hi + .5, f'derivatia {leaf} cade in afara muchiei {a}-{b}'
        lst.sort(key=lambda it: abs(it[1][ax] - pa[ax]))
        chain = [a]
        for leaf, tp in lst:
            if abs(tp[ax] - pa[ax]) < .5: tn = a
            elif abs(tp[ax] - pb[ax]) < .5: tn = b
            elif abs(tp[ax] - nodes[chain[-1]][ax]) < .5: tn = chain[-1]      # doua aparate la aceeasi cota
            else: tn = f'{a}~{leaf}'; nodes[tn] = tp
            if tn != chain[-1] and tn != b: chain.append(tn)
            spec['leaves'][leaf] = tn
        chain.append(b)
        children[a].remove(b)
        for u, v in zip(chain, chain[1:]): parent[v] = u; children[u].append(v); orig[v] = (a, b)
    # frunze: picior + cot intermediar daca e nevoie
    for leaf, att in spec['leaves'].items():
        an = att; pa = nodes[an]; f = foot(leaf); ws = wall_side(P[leaf])
        if pa[0] == f[0] or pa[1] == f[1]:
            nodes[leaf] = f; parent[leaf] = an; children[an].append(leaf); orig[leaf] = ('*', leaf)
        else:
            bend = (pa[0], f[1]) if ws == 'x' else (f[0], pa[1])
            bn = f'{leaf}^'; nodes[bn] = bend; parent[bn] = an; children[an].append(bn)
            nodes[leaf] = f; parent[leaf] = bn; children[bn].append(leaf); orig[bn] = orig[leaf] = ('*', leaf)
    spec['_orig'] = orig
    return nodes, parent, children

def dfs_order(nodes, parent, children, root):
    order = {}; cnt = [0]
    def ang(v): return math.atan2(v[1], v[0])
    def rec(n, came):
        order[n] = cnt[0]; cnt[0] += 1
        ch = children.get(n, [])
        back = came if came else (0, 1)
        def cw(c):
            v = (nodes[c][0] - nodes[n][0], nodes[c][1] - nodes[n][1])
            d = (ang(back) - ang(v)) % (2 * math.pi)       # unghi masurat in sens orar de la directia spre parinte
            return d if d > 1e-9 else 2 * math.pi
        for c in sorted(ch, key=cw):
            rec(c, (nodes[n][0] - nodes[c][0], nodes[n][1] - nodes[c][1]))
    rec(root, None)
    return order

def path(parent, a, b):
    def anc(x):
        out = [x]
        while x in parent: x = parent[x]; out.append(x)
        return out
    A, B = anc(a), anc(b); sb = set(B)
    lca = next(x for x in A if x in sb)
    return A[:A.index(lca) + 1] + list(reversed(B[:B.index(lca)]))

def layout(spec, tubes, src_map):
    nodes, parent, children = build(spec)
    order = dfs_order(nodes, parent, children, spec['root'])
    sub_last = {}
    def last(n):
        if n not in sub_last: sub_last[n] = max([order[n]] + [last(c) for c in children.get(n, [])])
        return sub_last[n]
    use = collections.defaultdict(list)
    for t in tubes:
        a, b = src_map(t['src']), src_map(t['dst'])
        t['_path'] = path(parent, a, b)
        for u, v in zip(t['_path'], t['_path'][1:]):
            c = v if parent.get(v) == u else u
            use[c].append(t)
    off = {}
    def direc(c):
        p = parent[c]; dx = nodes[c][0] - nodes[p][0]; dy = nodes[c][1] - nodes[p][1]; L = math.hypot(dx, dy) or 1
        return (round(dx / L, 6), round(dy / L, 6))
    bfs = [spec['root']]; i = 0
    while i < len(bfs): bfs += children.get(bfs[i], []); i += 1
    for c in bfs[1:]:
        if c not in use: continue
        ts = use[c]; p = parent[c]
        def key(t):
            ends = [src_map(t['src']), src_map(t['dst'])]
            inside = [e for e in ends if order[c] <= order[e] <= last(c)]
            other = [e for e in ends if e not in inside]
            return (order[inside[0]] if inside else -1, -(order[other[0]]) if other else 0)
        ts = sorted(ts, key=key)       # stanga -> dreapta fata de sensul parinte -> copil; offset pozitiv = stanga
        w = {t['id']: t['d'] + GAP for t in ts}
        inh = {}
        if p in parent and direc(p) == direc(c):            # continuare in linie dreapta: fiecare tub isi pastreaza banda
            inh = {t['id']: off[(t['id'], p)] for t in ts if (t['id'], p) in off}
        idx = [k for k, t in enumerate(ts) if t['id'] in inh]
        new_mid = idx and any(t['id'] not in inh for t in ts[idx[0]:idx[-1] + 1])
        if not inh or new_mid:
            if new_mid: print('atentie: banda recentrata pe', p, '->', c)
            tot = sum(w.values()); acc = tot / 2
            for t in ts: off[(t['id'], c)] = acc - w[t['id']] / 2; acc -= w[t['id']]
        else:
            for t in ts:
                if t['id'] in inh: off[(t['id'], c)] = inh[t['id']]
            left = ts[:idx[0]]; right = ts[idx[-1] + 1:]
            edge = inh[ts[idx[0]]['id']] + w[ts[idx[0]]['id']] / 2
            for t in reversed(left): off[(t['id'], c)] = edge + w[t['id']] / 2; edge += w[t['id']]
            edge = inh[ts[idx[-1]]['id']] - w[ts[idx[-1]]['id']] / 2
            for t in right: off[(t['id'], c)] = edge - w[t['id']] / 2; edge -= w[t['id']]
    for t in tubes:
        pts = []; pl = t['_path']; segs = []
        for u, v in zip(pl, pl[1:]):
            c = v if parent.get(v) == u else u; p = parent[c]
            dx = nodes[c][0] - nodes[p][0]; dy = nodes[c][1] - nodes[p][1]; L = math.hypot(dx, dy) or 1
            nl = (-dy / L, dx / L); o = off[(t['id'], c)]
            segs.append(((nodes[u][0] + nl[0] * o, nodes[u][1] + nl[1] * o), (nodes[v][0] + nl[0] * o, nodes[v][1] + nl[1] * o)))
        pts.append(segs[0][0])
        for s1, s2 in zip(segs, segs[1:]):
            # intersectia celor doua drepte (perpendiculare) sau jog daca sunt coliniare
            (a1, b1), (a2, b2) = s1, s2
            if abs(a1[0] - b1[0]) < 1e-6 and abs(a2[1] - b2[1]) < 1e-6: pts.append((a1[0], a2[1]))
            elif abs(a1[1] - b1[1]) < 1e-6 and abs(a2[0] - b2[0]) < 1e-6: pts.append((a2[0], a1[1]))
            else: pts += [b1, a2]
        pts.append(segs[-1][1])
        t['floor'] = [[round(x, 1), round(y, 1)] for x, y in pts]
    corr = collections.defaultdict(set)
    for c, ts in use.items():
        o = spec['_orig'][c]
        if o[0] != '*': corr[o[0] + '-' + o[1]] |= {t['id'] for t in ts}
    spec['_corr'] = {k: sorted(v) for k, v in corr.items()}
    spec['_nodes_xy'] = {k: nodes[k] for k in spec['nodes']}
    return nodes, parent

import copy
_n, _p, _c = build(copy.deepcopy(POWER)); DFS = dfs_order(_n, _p, _c, POWER['root'])
SOCKET_TUBES = []
for circ, legs in SOCKETS.items():
  for li, members in enumerate(legs):
    loc = {a: b for (a, b) in LOCAL if a not in DFS}            # aparat legat local de altul (fara coborare proprie in sapa)
    ms = sorted([m for m in members if m not in loc], key=lambda m: DFS[m])
    r0 = POWER['nodes']['R0']
    if abs(P[ms[-1]][0] - r0[0]) + abs(P[ms[-1]][1] - r0[1]) < abs(P[ms[0]][0] - r0[0]) + abs(P[ms[0]][1] - r0[1]): ms.reverse()
    chain = ['TE'] + ms
    base = 'T' + circ[1:] + ('' if li == 0 else '.' + str(li + 1))
    for k, (a, b) in enumerate(zip(chain, chain[1:])):
        tid = base + ('' if k == 0 else chr(ord('a') + k))
        SOCKET_TUBES.append(dict(id=tid, src=a, dst=b, circuit=circ, kind='A' if b == 'AC' else ('P' if b.startswith('P') else 'F'), section=2.5, wires=3,
                                 roles=L3, d=20, net='P', note=''))
    for m in members:
        if m in loc:
            SOCKET_TUBES.append(dict(id=base + 'L', src=loc[m], dst=m, circuit=circ, kind='P', section=2.5, wires=3,
                                     roles=L3, d=20, net='P', note=LOCAL[(m, loc[m])]))
TUBES[:0] = SOCKET_TUBES
power = [t for t in TUBES if t['net'] == 'P' and 'local' not in t['note']]
weak = [t for t in TUBES if t['net'] == 'W']
pn, pp = layout(POWER, power, lambda n: 'R0' if n == 'TE' else n)
wn, wp = layout(WEAK, weak, lambda n: 'WR' if n == 'TE' else ('NET0' if n == 'NET' else n))

# ---------- 3D ----------
def z_of(n): return P[n][2]
for t in TUBES:
    if 'local' in t['note']:
        a, b = P[t['src']], P[t['dst']]
        if t['src'] == 'TE': t['points'] = [a[:2] + [Z_CORNISA], [10040, -3650, Z_CORNISA], [b[0], b[1], Z_CORNISA], b]
        elif t['src'] == 'J01': t['points'] = [a, [a[0], a[1], Z_CORNISA], [10000, -3600, Z_CORNISA], [10000, -3600, b[2]], b]
        elif t['src'] == 'J05': t['points'] = [a, [a[0], a[1], b[2]], [b[0], a[1], b[2]], b]
        else: t['points'] = [a, [a[0], a[1], b[2]], b] if a[:2] != b[:2] else [a, b]
    else:
        fl = t['floor']; pts = []
        s, e = t['src'], t['dst']
        def end3(name, xy, first):
            if name == 'TE':
                if t['net'] == 'P': seq = [TE[:2] + [Z_CORNISA], [10040, -3650, Z_CORNISA], [xy[0], xy[1], Z_CORNISA], [xy[0], xy[1], ZF]]
                else: seq = [[TE[0], TE[1] - 200, Z_CORNISA], [9700, -4860, Z_CORNISA], [xy[0], xy[1], Z_CORNISA], [xy[0], xy[1], ZF]]
            elif name == 'NET': seq = [[xy[0], xy[1], P['NET'][2]], [xy[0], xy[1], ZF]]
            else:
                seq = [[xy[0], xy[1], z_of(name)], [xy[0], xy[1], ZF]]
                if name in DROP and name == 'F07': seq = [P[name], [xy[0], xy[1], z_of(name)], [xy[0], xy[1], ZF]]
            return seq if first else list(reversed(seq))
        pts = end3(s, fl[0], True) + [[x, y, ZF] for x, y in fl[1:-1]] + end3(e, fl[-1], False)
        c = []
        for p in pts:
            p = [round(v, 1) for v in p]
            if not c or p != c[-1]: c.append(p)
        t['points'] = c
    t['length_m'] = round(sum(math.dist(a, b) for a, b in zip(t['points'], t['points'][1:])) / 1000, 2)
    t['bends'] = max(0, len(t['points']) - 2)
    t.pop('_path', None)

# ---------- tavan: doza J (sau intrerupator) -> plafoniera, in sant in placa, la decizia beneficiarului 07.10 ----------
# Tub D16, numai 3 conductoare (retur comutat, N, PE) -> sant minim. Trasee paralele cu peretii.
Z_TAV = 2500; Z_SANT = 2512          # axa tubului in sant, ~12 mm peste fata tavanului (sant ~25 mm) - CONDITIONAT de aviz structural
LAMPS = {l['id']: list(l['model_endpoint']) for l in r10['lights']}
P.update({k: v for k, v in LAMPS.items()})
CEIL = [('L01', 'S01', 'C01'), ('L02', 'S02', 'C01'), ('L06', 'S06', 'C01'), ('L04', 'S04', 'C02'), ('L03', 'S03', 'C02'),
        ('F06', 'S03', 'C02'), ('L05', 'S05', 'C02'), ('F05', 'L05', 'C02'), ('L07', 'S07', 'C03'), ('L08', 'S08', 'C03')]
for lid, src, circ in CEIL:
    a = P[src]; b = P[lid]
    ws = wall_side(a) if not src.startswith('L') else 'x'
    corner = [b[0], a[1]] if ws == 'x' else [a[0], b[1]]       # intai perpendicular pe perete, apoi spre lampa
    pts = [a, [a[0], a[1], Z_SANT], [corner[0], corner[1], Z_SANT], [b[0], b[1], Z_SANT], b]
    if src.startswith('L'): pts = [a, [a[0], a[1], Z_SANT]] + pts[2:]
    c = []
    for q in pts:
        q = [round(v, 1) for v in q]
        if not c or q != c[-1]: c.append(q)
    roles = {'L05': 'retur L05+F05', 'F05': 'retur L05+F05 (continuare)', 'F06': 'retur F06'}.get(lid, 'retur ' + lid) + ', N, PE'
    note = 'tavan: sant in placa de beton armat - numai cu aviz structural; se prefera tubul existent'
    extra = {'L06': 'urca din S06, gaura prin peretele fatadei sub tavan, apoi tavanul balconului',
             'L08': 'urca din S08, gaura prin peretele vestibul-baie sub tavan',
             'L03': 'urca din S03 (hol), gaura prin peretele hol-bucatarie sub tavan', 'F06': 'urca din S03, gaura prin perete, coboara la sursa LED de deasupra corpurilor',
             'L07': 'urca din S07, gaura prin peretele sufragerie-vestibul sub tavan', 'F05': 'continua din rozeta L05 pana deasupra sursei LED',
             'L04': 'urca din S04 in caseta coloanei, apoi tavanul holului'}.get(lid)
    if extra: note = extra + '; ' + note
    TUBES.append(dict(id='TV_' + lid, src=src, dst=lid, circuit=circ, kind='L', section=1.5, wires=3, roles=roles, d=16, net='P',
                      note=note, points=c, floor=[],
                      length_m=round(sum(math.dist(u, v) for u, v in zip(c, c[1:])) / 1000, 2), bends=max(0, len(c) - 2)))
INFO.update({'F05': 'Sursa LED debara (comandata cu L05)', 'F06': 'Sursa LED sub corpuri bucatarie (tasta 2 S03)', 'L01': 'Plafoniera dormitor', 'L02': 'Plafoniera sufragerie', 'L03': 'Plafoniera bucatarie', 'L04': 'Plafoniera hol',
             'L05': 'Plafoniera debara', 'L06': 'Plafoniera balcon', 'L07': 'Plafoniera vestibul', 'L08': 'Plafoniera baie'})

# ---------- verificari ----------
walls = {
 'dormitor|sufragerie': [(3550, 3700, -4050, -250), (3550, 3700, -5550, -4950)],
 'dormitor|vestibul': [(150, 2600, -3920, -3845), (3500, 3550, -3920, -3845)],
 'baie|vestibul': [(2450, 2525, -4200, -3920), (2450, 2525, -5550, -4900)],
 'sufragerie|hol-bucatarie': [(7100, 7250, -3950, -250), (7100, 7250, -5550, -4850)],
 'bucatarie|hol': [(7250, 8000, -3545, -3470), (8800, 10080, -3545, -3470)],
 'bucatarie|debara': [(9800, 9875, -1500, -250), (9800, 9875, -3470, -2200)],
}
DOORS = {'Usa hol-sufragerie': (7100, 7250, -4850, -3950), 'Usa bucatarie': (8000, 8800, -3545, -3470), 'Usa debara': (9800, 9875, -2200, -1500),
         'Usa sufragerie-vestibul': (3550, 3700, -4950, -4050), 'Usa dormitor': (2600, 3500, -3920, -3845), 'Usa baie': (2450, 2525, -4900, -4200),
         }
PRAG = ((9762, -4780), (9994, -3880))   # fata interioara a golului usii de intrare (oblic)
def dist_seg(p, a, b):
    ax, ay = a; bx, by = b; px, py = p; vx, vy = bx - ax, by - ay
    t = max(0, min(1, ((px - ax) * vx + (py - ay) * vy) / (vx * vx + vy * vy)))
    return math.hypot(px - ax - t * vx, py - ay - t * vy)
def inside(x, y, r, m=1): return r[0] + m < x < r[1] - m and r[2] + m < y < r[3] - m
def seg_hits(a, b, r, m=1):
    n = int(math.dist(a[:2], b[:2]) // 10) + 2
    return any(inside(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n, r, m) for i in range(n + 1))
problems = []; door_use = collections.defaultdict(list)
for t in TUBES:
    for a, b in zip(t['points'], t['points'][1:]):
        if a[2] == b[2] == ZF:
            for wn_, rs in walls.items():
                if any(seg_hits(a, b, r) for r in rs): problems.append(f"{t['id']}: trece prin peretele plin {wn_}")
            for dn, r in DOORS.items():
                if seg_hits(a, b, r): door_use[dn].append(t['id'])
        if a[:2] == b[:2]:
            for dn, r in DOORS.items():
                if inside(a[0], a[1], r, 0): problems.append(f"{t['id']}: coborare in golul {dn}")
for t in TUBES:
    for a, b in zip(t['points'], t['points'][1:]):
        if a[2] == b[2] == ZF:
            n = int(math.dist(a[:2], b[:2]) // 10) + 2
            dmin = min(dist_seg((a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n), *PRAG) for i in range(n + 1))
            if dmin < 150: problems.append(f"{t['id']}: la {dmin:.0f} mm de pragul usii de intrare")
door_use = {k: sorted(set(v)) for k, v in door_use.items()}
fsegs = [(t, a, b) for t in TUBES for a, b in zip(t['points'], t['points'][1:]) if a[2] == b[2] == ZF and a[:2] != b[:2]]
def inter(s1, s2):
    (t1, a, b), (t2, c, d) = s1, s2
    h1 = abs(a[1] - b[1]) < .01; h2 = abs(c[1] - d[1]) < .01
    if h1 == h2: return None
    if not h1: (t1, a, b), (t2, c, d) = s2, s1
    y = a[1]; x = c[0]
    if min(a[0], b[0]) + .5 < x < max(a[0], b[0]) - .5 and min(c[1], d[1]) + .5 < y < max(c[1], d[1]) - .5: return (x, y)
cross = []
for i in range(len(fsegs)):
    for j in range(i + 1, len(fsegs)):
        if fsegs[i][0]['id'] == fsegs[j][0]['id']: continue
        p = inter(fsegs[i], fsegs[j])
        if p: cross.append(dict(a=fsegs[i][0]['id'], b=fsegs[j][0]['id'], xy=[round(p[0]), round(p[1])],
                                mixed=fsegs[i][0]['net'] != fsegs[j][0]['net']))
# distanta minima intre axe paralele (suprapuneri)
clash = []
for i in range(len(fsegs)):
    for j in range(i + 1, len(fsegs)):
        (t1, a, b), (t2, c, d) = fsegs[i], fsegs[j]
        if t1['id'] == t2['id']: continue
        need = (t1['d'] + t2['d']) / 2 + (0 if t1['net'] == t2['net'] else 100)
        for ax in (0, 1):
            if abs(a[1 - ax] - b[1 - ax]) < .01 and abs(c[1 - ax] - d[1 - ax]) < .01:   # ambele paralele cu axa ax
                ov = min(max(a[ax], b[ax]), max(c[ax], d[ax])) - max(min(a[ax], b[ax]), min(c[ax], d[ax]))
                dist = abs(a[1 - ax] - c[1 - ax])
                if ov > 5 and dist < need - .5: clash.append((t1['id'], t2['id'], round(dist), round(ov)))

res = dict(revision='R11', date='2026-10-07', ZF=ZF, Z_cornisa=Z_CORNISA, GAP=GAP, TE=TE,
           points=P, info=INFO, drops=DROP, tubes=TUBES, door_use=door_use, problems=problems,
           crossings=cross, clashes=clash,
           corridors=dict(POWER['_corr'], **WEAK['_corr']), corridor_nodes=dict(POWER['_nodes_xy'], **WEAK['_nodes_xy']),
           power_edges=POWER['edges'], weak_edges=WEAK['edges'])
(OUT / 'trasee_R11.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
if __name__ == '__main__':
    print('tuburi', len(TUBES), '| din TE (forta):', sum(t['src'] == 'TE' and t['net'] == 'P' for t in TUBES))
    print('probleme:', problems)
    print('usi:', {k: len(v) for k, v in door_use.items()})
    print('incrucisari forta/forta:', [c for c in cross if not c['mixed']])
    print('incrucisari forta/slabi:', len([c for c in cross if c['mixed']]), [ (c['a'], c['b'], c['xy']) for c in cross if c['mixed']])
    print('apropieri sub minim:', clash)
    print('lungime totala tuburi m:', round(sum(t['length_m'] for t in TUBES), 1))
