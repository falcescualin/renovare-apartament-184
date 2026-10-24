"""Calcul automat al gaurilor din geometria pieselor (cutii 3D din spec).
Pentru fiecare pereche de panouri care se ating (fata unuia pe muchia celuilalt) se genereaza:
- pe panoul A (fata): gauri de trecere Ø7 pentru confirmate, pe fata opusa lui B, in lungul liniei de imbinare;
- pe panoul B (muchie): gauri pilot Ø5 x 55 in muchia lui, la mijlocul grosimii;
- cepuri Ø8 intre confirmate (gauri oarbe pe ambele).
Sertarele: glisierele (SL) au gauri de prindere pe fata interioara a lateralului: la 37 mm de muchia din fata, apoi pe grila de 32 mm.
Iese: dict cod -> {dims:(u,v,t), faces:{nume:{normal, holes:[(u,v,tip,nota)]}}, edges:[{edge,pos,tip}]}"""
import math
from montaj_specs import joint_positions

AX = 'xyz'
PANEL_ROLES = ('panel',)


def bbox(p):
    x, y, z, dx, dy, dz = p['box']
    return [x, y, z], [x + dx, y + dy, z + dz]


def frame(p):
    """axa grosimii, axa lunga (u), axa scurta (v) pentru un panou"""
    mn, mx = bbox(p); sz = [mx[i] - mn[i] for i in range(3)]
    t = min(range(3), key=lambda i: sz[i])
    rest = [i for i in range(3) if i != t]
    u = max(rest, key=lambda i: sz[i]); v = [i for i in rest if i != u][0]
    return t, u, v, sz


def side_name(axis, sign, front_axis=1):
    # vazut din fata (fata = +y): +x = stanga, -x = dreapta, +z = sus, -z = jos, +y = fata, -y = spate
    return {(0, 1): 'stânga', (0, -1): 'dreapta', (1, 1): 'față', (1, -1): 'spate', (2, 1): 'sus', (2, -1): 'jos'}[(axis, sign)]


def contacts(parts, tol=0.7, skip=()):
    out = []
    for i, A in enumerate(parts):
        a0, a1 = bbox(A)
        for B in parts[i + 1:]:
            if frozenset((A['id'], B['id'])) in skip:
                continue
            b0, b1 = bbox(B)
            for t in range(3):
                gap1 = b0[t] - a1[t]; gap2 = a0[t] - b1[t]
                if abs(gap1) <= tol or abs(gap2) <= tol:
                    ov = [min(a1[k], b1[k]) - max(a0[k], b0[k]) for k in range(3)]
                    others = [k for k in range(3) if k != t]
                    if all(ov[k] > 1.0 for k in others):
                        # B este la +t fata de A daca gap1 ~ 0
                        sgn = 1 if abs(gap1) <= tol else -1
                        out.append((A, B, t, sgn, ov))
    return out


def compute(S, uniq_by_code=True):
    panels = [p for p in S.parts if p.get('role', 'panel') in PANEL_ROLES]
    res = {}                    # id piesa -> date
    info = {}
    for p in panels:
        t, u, v, sz = frame(p)
        info[p['id']] = dict(p=p, t=t, u=u, v=v, L=sz[u], W=sz[v], T=sz[t], faces={}, edges=[], hole_n=0, h3=[])
    mn_all = [min(bbox(p)[0][i] for p in S.parts) for i in range(3)]
    mx_all = [max(bbox(p)[1][i] for p in S.parts) for i in range(3)]
    cen = [(mn_all[i] + mx_all[i]) / 2 for i in range(3)]

    def face(pid, sign):
        d = info[pid]
        key = side_name(d['t'], sign)
        return d['faces'].setdefault(key, dict(sign=sign, holes=[]))

    for A, B, t, sgn, ov in contacts(panels, skip={frozenset(p) for p in getattr(S, 'skip_joints', [])}):
        ia, ib = info[A['id']], info[B['id']]
        jstep = max(A.get('step', 0), B.get('step', 0))
        # A fata (axa grosimii = t), B muchie (axa grosimii != t)
        if ia['t'] == t and ib['t'] != t:
            fa, eb, a_side = ia, ib, sgn
        elif ib['t'] == t and ia['t'] != t:
            fa, eb, a_side = ib, ia, -sgn
        else:
            continue
        # linia de imbinare: axa din planul de contact cu suprapunerea cea mai mare
        others = [k for k in range(3) if k != t]
        line = max(others, key=lambda k: ov[k]); across = [k for k in others if k != line][0]
        a0, a1 = bbox(fa['p']); b0, b1 = bbox(eb['p'])
        s0 = max(a0[line], b0[line]); L = ov[line]
        pos = joint_positions(L)
        c_across = (max(a0[across], b0[across]) + min(a1[across], b1[across])) / 2
        # gauri pe fata lui A: pe partea opusa lui B (exterior), in coordonatele panoului A
        ext_sign = -a_side
        fc = face(fa['p']['id'], ext_sign)
        ic = face(fa['p']['id'], a_side)
        def vec(axis, val):
            v3 = [0.0, 0.0, 0.0]; v3[axis] = float(val); return v3
        def p3(plane_t, along, acr):
            q = [0.0, 0.0, 0.0]; q[t] = plane_t; q[line] = along; q[across] = acr; return [round(v, 2) for v in q]
        a_plane_ext = a1[t] if ext_sign > 0 else a0[t]
        a_plane_int = a1[t] if a_side > 0 else a0[t]
        for x in pos:
            gu = (s0 + x - a0[fa['u']]) if line == fa['u'] else (c_across - a0[fa['u']])
            gv = (s0 + x - a0[fa['v']]) if line == fa['v'] else (c_across - a0[fa['v']])
            fc['holes'].append((round(gu, 1), round(gv, 1), 'conf7', 'Ø7 trecere'))
            fa['h3'].append(dict(kind='conf7', pos=p3(a_plane_ext, s0 + x, c_across), n_out=vec(t, ext_sign), dia=7.0, depth=fa['T'], through=True, hw='confirmat', face=side_name(t, ext_sign),
                                 with_=eb['p']['id'], step=jstep))
        # cepuri intre confirmate (gauri oarbe pe fata dinspre imbinare)
        mids = [(pos[i] + pos[i + 1]) / 2 for i in range(len(pos) - 1)]
        for x in mids:
            gu = (s0 + x - a0[fa['u']]) if line == fa['u'] else (c_across - a0[fa['u']])
            gv = (s0 + x - a0[fa['v']]) if line == fa['v'] else (c_across - a0[fa['v']])
            ic['holes'].append((round(gu, 1), round(gv, 1), 'cep8', 'Ø8 × 12 oarbă'))
            fa['h3'].append(dict(kind='cep8', pos=p3(a_plane_int, s0 + x, c_across), n_out=vec(t, a_side), dia=8.0, depth=12.0, through=False, hw='cep', face=side_name(t, a_side),
                                 with_=eb['p']['id'], step=jstep))
            eb['h3'].append(dict(kind='cep8', pos=p3(a_plane_int, s0 + x, c_across), n_out=vec(t, -a_side), dia=8.0, depth=22.0, through=False, hw='cep', face='muchie',
                                 with_=fa['p']['id'], step=jstep))
        # muchia lui B: gaura pilot, la mijlocul grosimii; muchia = capatul de pe axa t
        b_edge_sign = -a_side            # muchia lui B atinge A, deci e orientata spre A
        edge_axis_in_B = 'u' if eb['u'] == t else 'v'
        ed_name = ('capăt ' if edge_axis_in_B == 'u' else 'muchie ') + (side_name(t, b_edge_sign))
        # pozitiile pe lungimea muchiei, in coordonate B
        along = eb['u'] if (eb['u'] != t and line == eb['u']) else (eb['v'] if line == eb['v'] else eb['u'])
        for x in pos:
            eb['h3'].append(dict(kind='pilot5', pos=p3(a_plane_int, s0 + x, c_across), n_out=vec(t, -a_side), dia=5.0, depth=55.0, through=False, hw=None, face='muchie',
                                 with_=fa['p']['id'], step=jstep))
        bp = [round(s0 + x - b0[line], 1) for x in pos]
        cp = [round(s0 + x - b0[line], 1) for x in mids]
        eb['edges'].append(dict(edge=ed_name, axis=edge_axis_in_B, sign=b_edge_sign, pos=bp, tip='pilot5', cepi=cp, T=eb['T'], with_=fa['p']['code']))
        # cepuri si pe muchia lui B
    # glisiere: gauri pe fata interioara a lateralelor
    rails = [p for p in S.parts if p['code'] == 'SL']
    for r in rails:
        r0, r1 = bbox(r)
        best = None
        for pid, d in info.items():
            if d['t'] != 0 or d['p']['mat'] == 'sertar':
                continue
            a0, a1 = bbox(d['p'])
            # glisiera lipita de lateral (contact pe x)
            if abs(r0[0] - a1[0]) < 1.0 or abs(r1[0] - a0[0]) < 1.0:
                if min(a1[1], r1[1]) - max(a0[1], r0[1]) > 5 and min(a1[2], r1[2]) - max(a0[2], r0[2]) > 1:
                    best = (pid, d, a0, a1)
        if not best: continue
        pid, d, a0, a1 = best
        side = 1 if abs(r0[0] - a1[0]) < 1.0 else -1       # glisiera e pe fata +x (side=1) sau -x
        fc = d['faces'].setdefault(side_name(0, side), dict(sign=side, holes=[]))
        # u,v ale lateralului: lateral are dy (adancime) si dz; capatul din fata = y max
        zc = r.get('zs', (r0[2] + r1[2]) / 2)
        for off in r.get('offs', (37, 133, 261)):
            yy = a1[1] - off
            if yy < r0[1]: continue
            hu = (yy - a0[d['u']]) if d['u'] == 1 else (zc - a0[d['u']])
            hv = (zc - a0[d['v']]) if d['v'] == 2 else (yy - a0[d['v']])
            fc['holes'].append((round(hu, 1), round(hv, 1), 'rail', 'glisieră, Ø3 × 13 pilot'))
            q = [0.0, 0.0, 0.0]; q[0] = a1[0] if side > 0 else a0[0]; q[1] = yy; q[2] = zc
            d['h3'].append(dict(kind='rail', pos=[round(v, 2) for v in q], n_out=[float(side), 0.0, 0.0], dia=3.0, depth=13.0, through=False, hw='surub_3_5x15', face=side_name(0, side),
                                with_=r['id'], step=r.get('step', 0)))
        d.setdefault('rails', []).append(dict(z=round(zc - a0[2], 1), face=side_name(0, side), y_front=a1[1], offs=list(r.get('offs', (37, 133, 261)))))
    # gaurile de feronerie adaugate explicit (montaj_lib): cupe de balama, placute, pini, TIP-ON, agatatori - si pe usi
    for p in S.parts:
        hl = p.get('holes3')
        if not hl:
            continue
        if p['id'] not in info:
            t, u, v, sz = frame(p)
            info[p['id']] = dict(p=p, t=t, u=u, v=v, L=sz[u], W=sz[v], T=sz[t], faces={}, edges=[], hole_n=0, h3=[])
        d = info[p['id']]
        a0, a1 = bbox(p)
        for h in hl:
            n = h['n_out']; ax = max(range(3), key=lambda i: abs(n[i])); sgn = 1 if n[ax] > 0 else -1
            d['h3'].append(dict(h, face=side_name(ax, sgn) if ax == d['t'] else 'muchie', with_=None, step=p.get('step', 0)))
            if ax == d['t']:
                fc = d['faces'].setdefault(side_name(ax, sgn), dict(sign=sgn, holes=[]))
                q = h['pos']
                fc['holes'].append((round(q[d['u']] - a0[d['u']], 1), round(q[d['v']] - a0[d['v']], 1), h['kind'], h.get('note', '')))
    # carligul din spate MOVENTO: gaura Ø6 x 10 in capatul din spate al lateralului de sertar (7 mm de fata exterioara, 11 mm de jos)
    for pid, d in info.items():
        hk = d['p'].get('hook')
        if not hk:
            continue
        a0, a1 = bbox(d['p'])
        d['h3'].append(dict(kind='hook6', pos=[hk[0], a0[1], hk[1]], n_out=[0.0, -1.0, 0.0], dia=6.0, depth=10.0, through=False, hw=None, face='muchie',
                            with_=None, step=d['p'].get('step', 0)))
        d['edges'].append(dict(edge='capăt spate', axis='u', sign=-1, pos=[round(hk[1] - a0[2], 1)], tip='hook6', cepi=[], T=d['T'], with_='cârligul MOVENTO',
                               off=round(min(abs(hk[0] - a0[0]), abs(a1[0] - hk[0])), 1)))
    return info
