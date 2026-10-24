"""Biblioteca de montaj comuna pentru toate corpurile: feronerie pozitionata (S.hw_at) + gaurile ei (part['holes3'], apar pe desenele de gaurire).
Conventie: mm, fata corpului = +y, sus = +z, x mic = dreapta privit din fata. Fiecare functie intoarce numarul de bucati adaugate.
Cote Blum: balamale CLIP top 110° (Product details 71T3550 / 71B3590, MD CLIP top 11.24, TD-151): cupa Ø35 x 13, TB din tabelul FA,
gaurile flansei la 45 / 9,5 (3,5 x 17), placuta 173L6100 la 37 de muchia din fata, gauri la ±16 (3,5 x 15);
TIP-ON usi (MD-019): adaptor 956.1201 cu suruburi la 20 si 37 de muchie, ax la 14,5, placa Ø15 pe usa."""
import math


def box(p):
    x, y, z, dx, dy, dz = p['box']
    return x, x + dx, y, y + dy, z, z + dz


def P(S, pid):
    return next(p for p in S.parts if p['id'] == pid)


def hole(part, kind, pos, n_out, dia, depth, note='', through=False, hw=None):
    part.setdefault('holes3', []).append(dict(kind=kind, pos=[round(float(v), 2) for v in pos], n_out=[float(v) for v in n_out], dia=dia, depth=depth,
                                              through=through, hw=hw, note=note))


def hinge_count(h):
    """Blum: numarul de balamale dupa inaltimea usii (front 18 mm, greutate normala)"""
    return 2 if h <= 900 else 3 if h <= 1600 else 4 if h <= 2000 else 5


def hinge_z(z0, z1, n, edge=100.0):
    if n == 1:
        return [(z0 + z1) / 2]
    return [z0 + edge + i * (z1 - z0 - 2 * edge) / (n - 1) for i in range(n)]


HINGE_MODEL = {'70T3550': 'balama_blum', '70T3650': 'balama_70T3650', '71B3550': 'balama_71B3550', '70T3750': 'balama_70T3650'}


def hinges(S, step, door, side, tip='70T3550', n=None, zs=None, letters=('BA', 'PB', 'D17', 'D15'), explode_plate=60):
    """balamale pe usa 'door' (piesa role 'door') prinse pe 'side' (lateral / despartitor). Partea balamalei se deduce din pozitie.
    Adauga: balama (atasata de usa), placuta + 2 suruburi 3,5 x 15 (pe lateral), 2 suruburi 3,5 x 17 in cupa (pe usa);
    gauri: Ø35 x 13 in usa, 2 x Ø2,5 pentru flansa, 2 x Ø2,5 pentru placuta."""
    d, s = P(S, door), P(S, side)
    dx0, dx1, dy0, dy1, dz0, dz1 = box(d)
    sx0, sx1, sy0, sy1, sz0, sz1 = box(s)
    sgn = 1 if (sx0 + sx1) / 2 < (dx0 + dx1) / 2 else -1        # +1: lateralul e in dreapta usii (x mic), interiorul spre +x
    x_in = sx1 if sgn > 0 else sx0                               # fata laterala dinspre interior
    x_out = sx0 if sgn > 0 else sx1
    edge = dx0 if sgn > 0 else dx1                               # muchia usii dinspre balama
    FA = (sx1 - edge) if sgn > 0 else (edge - sx0)               # cat acopera usa din muchia lateralului
    inset = FA < 0                                               # usa incastrata (in gol)
    half = (tip.endswith('3650') or FA < 12) and not inset
    TB = 5.0 if inset else max(3.0, min(7.0, (FA - 1.5) if half else (FA - 11.0)))
    if inset:
        tip = '70T3750'
    c = edge + sgn * (TB + 17.5)                                 # centrul cupei
    xc_model = 16.0 if half else 6.5
    yb = dy0                                                     # fata din spate a usii
    zl = zs or hinge_z(dz0, dz1, n or hinge_count(dz1 - dz0))
    L1, L2, L3, L4 = letters
    model = HINGE_MODEL['70T3650' if (half and tip == '70T3550') or tip == '70T3750' else tip]
    for z in zl:
        at = (c - sgn * xc_model, yb, z)
        S.hw_at(step, model, at, az=(0, -1, 0), ax=(sgn, 0, 0), attach=door, explode=0, letter=L1, dash=False, tag='balama')
        S.hw_at(step, 'placuta_balama', (x_in, yb, z), az=(0, -1, 0), ax=(sgn, 0, 0), attach=side, explode=0, letter=L2, dash=False, tag='placuta')
        fx = c + sgn * 9.5
        for dz in (-22.5, 22.5):
            S.hw_at(step, 'surub_3_5x17', (fx, yb - 3.2, z + dz), az=(0, -1, 0), attach=door, explode=35, letter=L3, tag='balama')
            hole(d, 'pil25', (fx, yb, z + dz), (0, -1, 0), 2.5, 10, 'flanșă balama')
        for dz in (-16.0, 16.0):
            S.hw_at(step, 'surub_3_5x15', (x_in + sgn * 3.05, sy1 - 37.0, z + dz), az=(sgn, 0, 0), attach=side, explode=35, letter=L4, tag='placuta')
            hole(s, 'plate', (x_in, sy1 - 37.0, z + dz), (sgn, 0, 0), 2.5, 12, 'plăcuță balama')
        hole(d, 'cup35', (c, yb, z), (0, -1, 0), 35.0, 13.0, 'cupă balama')
    d.setdefault('hinge_info', []).append(dict(side=side, n=len(zl), z=[round(v, 1) for v in zl], TB=TB, FA=round(FA, 1), tip=tip, half=half))
    if inset:
        S.inset_hinges = getattr(S, 'inset_hinges', 0) + len(zl)
    return len(zl)


def tipon(S, step, door, panel, x, letters=('TO', 'AD', 'PM'), y_front=None):
    """TIP-ON pentru usi (956.1004 in adaptor 956.1201) pe placa 'panel' (blat corp: sub ea; baza: pe ea), la muchia din fata, in dreptul lui x;
    placa metalica Ø15 pe usa. Gauri: 2 x Ø2,5 in panou (la 20 si 37 de muchie), 1 x Ø2,5 in usa."""
    d, p = P(S, door), P(S, panel)
    px0, px1, py0, py1, pz0, pz1 = box(p)
    dx0, dx1, dy0, dy1, dz0, dz1 = box(d)
    above = (pz0 + pz1) / 2 > (dz0 + dz1) / 2                    # panoul e deasupra (montaj sub el)
    zf = pz0 if above else pz1
    ax = (1, 0, 0) if above else (-1, 0, 0)
    up = -1 if above else 1
    L1, L2, L3 = letters
    if y_front is not None:
        py1 = y_front                                            # usa incastrata: TIP-ON in spatele usii
    S.hw_at(step, 'adaptor_tipon', (x, py1 - 1.5, zf), az=(0, 1, 0), ax=ax, attach=panel, explode=0, letter=L2, dash=False, tag='tipon')
    S.hw_at(step, 'tipon_usa', (x, py1 - 1.5, zf + up * 14.5), az=(0, 1, 0), attach=panel, explode=45, letter=L1, tag='tipon')
    S.hw_at(step, 'placa_tipon', (x, dy0 - 1.0, zf + up * 14.5), az=(0, -1, 0), attach=door, explode=0, letter=L3, dash=False, tag='tipon')
    for off in (20.0, 37.0):
        hole(p, 'tipon', (x, py1 - off, zf), (0, 0, up), 2.5, 10, 'adaptor TIP-ON')
    hole(d, 'pil25', (x, dy0, zf + up * 14.5), (0, -1, 0), 2.5, 8, 'placă TIP-ON')
    return 1


def shelf_pins(S, step, shelf, left, right, inset=37.0, letter='PR', rows=(-32, 0, 32)):
    """raft mobil pe 4 pini Ø5 cu talpa; gauri Ø5 x 12 in laterale: 2 randuri (37 de fata / spate), cate 3 gauri la 32 (reglaj)"""
    sh = P(S, shelf)
    x0, x1, y0, y1, z0, z1 = box(sh)
    za = z0 - 4.2
    n = 0
    for pid, xf, az, ax in ((left, x0, (1, 0, 0), (0, -1, 0)), (right, x1, (-1, 0, 0), (0, 1, 0))):
        pp = P(S, pid)
        for yy in (y0 + inset, y1 - inset):
            S.hw_at(step, 'pin_raft', (xf, yy, za), az=az, ax=ax, attach=pid, explode=30, letter=letter, dash=True, tag='pin')
            n += 1
            for r in rows:
                hole(pp, 'pin5', (xf, yy, za + r), [-a for a in az], 5.0, 12.0, 'pin raft')
    return n


def back_screws(S, step, back, spacing=150.0, letter='D', model='surub_3_5x16', explode=45):
    """suruburi in spatele HDF: in muchiile din spate ale panourilor care il ating, la ~spacing, la 50 de capete"""
    b = P(S, back)
    bx0, bx1, by0, by1, bz0, bz1 = box(b)
    n = 0
    for p in S.parts:
        if p['role'] not in ('panel',) or p['id'] == back:
            continue
        x0, x1, y0, y1, z0, z1 = box(p)
        if abs(y0 - by1) > 1.0:
            continue
        # muchia din spate: linia de-a lungul celei mai lungi dimensiuni din planul y = y0
        ox0, ox1 = max(x0, bx0), min(x1, bx1); oz0, oz1 = max(z0, bz0), min(z1, bz1)
        if ox1 - ox0 < 10 or oz1 - oz0 < 10:
            continue
        along_x = (ox1 - ox0) >= (oz1 - oz0)
        a0, a1 = (ox0, ox1) if along_x else (oz0, oz1)
        L = a1 - a0
        k = max(2, int(math.ceil((L - 100) / spacing)) + 1) if L > 160 else 1
        pos = [a0 + L / 2] if k == 1 else [a0 + 50 + i * (L - 100) / (k - 1) for i in range(k)]
        for a in pos:
            at = (a, by0, (oz0 + oz1) / 2) if along_x else ((ox0 + ox1) / 2, by0, a)
            S.hw_at(step, model, at, az=(0, -1, 0), attach=back, explode=explode, letter=letter)
            n += 1
    return n


def legs(S, step, base, positions, h=100.0, letter='PI'):
    b = P(S, base)
    x0, x1, y0, y1, z0, z1 = box(b)
    m = 'picior' if h == 100 else 'picior@%d' % h
    for (x, y) in positions:
        S.hw_at(step, m, (x, y, z0), az=(0, 0, 1), attach=base, explode=-60, letter=letter, dash=False, tag='picior')
        for k in range(4):
            a = math.radians(45 + 90 * k)
            S.hw_at(step, 'surub_4x16', (x + 22 * math.cos(a), y + 22 * math.sin(a), z0 - 4.0), az=(0, 0, -1), attach=base, explode=-100, letter='I', tag='picior')
    return len(positions)


def hangers(S, step, side_r, side_l, top, wall_y, rail_len=None, letters=('AG', 'SI', 'T', 'U')):
    """agatatori in colturile de sus-spate (dreapta + stanga) + sina pe perete; suruburi 4 x 16 in laterale, dibluri + 4 x 40 in perete"""
    r, l, t = P(S, side_r), P(S, side_l), P(S, top)
    rx0, rx1 = box(r)[0:2]
    lx0, lx1 = box(l)[0:2]
    tz0 = box(t)[4]
    yb = max(box(r)[2], box(l)[2])
    L1, L2, L3, L4 = letters
    S.hw_at(step, 'suport_suspendare', (rx1, yb, tz0), az=(0, 0, 1), ax=(-1, 0, 0), mirror=True, attach=side_r, explode=0, letter=L1, dash=False, tag='agat')
    S.hw_at(step, 'suport_suspendare', (lx0, yb, tz0), az=(0, 0, 1), ax=(-1, 0, 0), attach=side_l, explode=0, letter=L1, dash=False, tag='agat')
    for x, sx, pid in ((rx1, 1, side_r), (lx0, -1, side_l)):
        for dz in (-18.0, -48.0):
            S.hw_at(step, 'surub_4x16', (x + sx * 15.5, yb + 26.0, tz0 + dz), az=(sx, 0, 0), attach=pid, explode=40, letter='I', tag='agat')
            hole(P(S, pid), 'hang', (x, yb + 26.0, tz0 + dz), (sx, 0, 0), 2.5, 12, 'agățătoare')
    L = rail_len or (lx0 - rx1 - 20)
    S.hw_at(step, 'sina_suspendare@%d' % round(L), (rx1 + 10, wall_y, tz0 - 4.0), az=(0, 0, 1), ax=(1, 0, 0), attach=None, explode=0, letter=L2, dash=False, tag='sina')
    k = max(3, int(math.ceil(L / 300.0)) + 1)
    for i in range(k):
        x = rx1 + 10 + 20 + i * (L - 40) / (k - 1)
        S.hw_at(step, 'diblu_6x40', (x, wall_y, tz0 - 34.0), az=(0, 1, 0), explode=70, letter=L3, tag='sina')
        S.hw_at(step, 'surub_4x40', (x, wall_y + 1.5, tz0 - 34.0), az=(0, 1, 0), explode=125, letter=L4, tag='sina')
    return 2


def _xf(at, ax, ay, az, lp):
    return [at[i] + ax[i] * lp[0] + ay[i] * lp[1] + az[i] * lp[2] for i in range(3)]


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def hidden_joint(S, step, face, edge, inside, dowels=None, brackets=None, letters=('C', 'L', 'I'), skip=True):
    """imbinare fara confirmate vizibile (blaturi / baze la vedere): cepuri Ø8 cu adeziv in muchia lui 'edge' + colțare 40 x 40 pe interior,
    prinse cu 4 x 16. 'face' = placa orizontala (deasupra sau dedesubt), 'edge' = placa verticala, 'inside' = directia spre interiorul compartimentului
    (±x sau ±y) din fata lui 'edge'. Daca skip, imbinarea e scoasa din confirmatele automate."""
    F, E = P(S, face), P(S, edge)
    fx0, fx1, fy0, fy1, fz0, fz1 = box(F)
    ex0, ex1, ey0, ey1, ez0, ez1 = box(E)
    above = (fz0 + fz1) / 2 > (ez0 + ez1) / 2
    zc = fz0 if above else fz1                                  # planul de contact
    up = 1 if above else -1
    ind = tuple(float(v) for v in inside)
    along_y = abs(ind[0]) > 0.5                                 # E are grosimea pe x -> imbinarea merge pe y
    if along_y:
        a0, a1 = max(ey0, fy0), min(ey1, fy1); xc = (ex0 + ex1) / 2
        face_in = ex1 if ind[0] > 0 else ex0
    else:
        a0, a1 = max(ex0, fx0), min(ex1, fx1); yc = (ey0 + ey1) / 2
        face_in = ey1 if ind[1] > 0 else ey0
    L = a1 - a0
    dp = dowels or ([a0 + L * k for k in (0.2, 0.5, 0.8)] if L > 250 else [a0 + L * 0.3, a0 + L * 0.7])
    lc, lb, li = letters
    for a in dp:
        pt = (xc, a, zc) if along_y else (a, yc, zc)
        S.hw_at(step, 'cep', (pt[0], pt[1], zc + up * 12.0), az=(0, 0, up), attach=edge, explode=0, letter=lc, dash=False, tag='cep')
        hole(F, 'cep8', pt, (0, 0, -up), 8.0, 12.0, 'cep (fără confirmat)')
        hole(E, 'cep8', pt, (0, 0, up), 8.0, 22.0, 'cep (fără confirmat)')
    bp = brackets or ([a0 + 60.0, a1 - 80.0] if L > 200 else [a0 + (L - 20) / 2])
    az = (0, 0, -up)
    for a in bp:
        at = (face_in, a, zc) if along_y else (a, face_in, zc)
        ay = ind
        ax = _cross(ay, az)
        S.hw_at(step, 'coltar_40', at, az=az, ax=ax, attach=edge, explode=40, letter=lb, dash=False, tag='coltar')
        for lp in ((10.0, 14.0, 2.0), (10.0, 30.0, 2.0)):        # 2 suruburi in placa orizontala
            S.hw_at(step, 'surub_4x16', _xf(at, ax, ay, az, lp), az=az, attach=edge, explode=70, letter=li, tag='coltar')
        for lp in ((10.0, 2.0, 14.0), (10.0, 2.0, 30.0)):        # 2 in placa verticala
            S.hw_at(step, 'surub_4x16', _xf(at, ax, ay, az, lp), az=ay, attach=edge, explode=70, letter=li, tag='coltar')
    if skip:
        S.skip_joints.append((face, edge))
    return len(dp)
