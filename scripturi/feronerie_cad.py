"""Modele 3D solide (FreeCAD Part / OpenCASCADE) pentru feroneria din feronerie_catalog.py.
Fiecare constructor intoarce [(Part.Shape, culoare)], in mm. Filetele sunt elice reale (sweep), locasurile PZ2 / hex 4 sunt taiate in cap.
Folosit de feronerie_cad_export.py (freecadcmd: STEP + OBJ) si din FreeCAD GUI (document feronerie_3d.FCStd, cu culori)."""
import math
import FreeCAD as App
import Part
from feronerie_catalog import CATALOG, COL

V = App.Vector


# ---------------------------------------------------------------- primitive
def cyl(r, z0, z1, x=0.0, y=0.0):
    return Part.makeCylinder(r, z1 - z0, V(x, y, z0))


def cone(r0, r1, z0, z1, x=0.0, y=0.0):
    """r0 la z0 (jos), r1 la z1 (sus)"""
    return Part.makeCone(r0, r1, z1 - z0, V(x, y, z0))


def box(x0, x1, y0, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def rev(pts):
    """solid de revolutie in jurul axei Z dintr-un profil (r, z) inchis"""
    w = Part.makePolygon([V(r, 0, z) for r, z in pts] + [V(pts[0][0], 0, pts[0][1])])
    return Part.Face(w).revolve(V(0, 0, 0), V(0, 0, 1), 360)


def prism_xz(pts, y0, y1):
    """poligon in planul XZ extrudat pe Y intre y0 si y1"""
    w = Part.makePolygon([V(x, y0, z) for x, z in pts] + [V(pts[0][0], y0, pts[0][1])])
    return Part.Face(w).extrude(V(0, y1 - y0, 0))


def prism_yz(pts, x0, x1):
    w = Part.makePolygon([V(x0, y, z) for y, z in pts] + [V(x0, pts[0][0], pts[0][1])])
    return Part.Face(w).extrude(V(x1 - x0, 0, 0))


def rbox(x0, x1, y0, y1, z0, z1, r, axis='z'):
    """paralelipiped cu muchiile paralele cu axa data rotunjite"""
    b = box(x0, x1, y0, y1, z0, z1)
    try:
        ed = [e for e in b.Edges if abs(getattr(e.tangentAt(0), axis)) > 0.99]
        return b.makeFillet(r, ed)
    except Exception:
        return b


def fil(s, r, test=None):
    try:
        ed = [e for e in s.Edges if (test is None or test(e))]
        return s.makeFillet(r, ed)
    except Exception:
        return s


def fuse(lst):
    """fuziune pas cu pas (fuziunea multipla din OCC pierde uneori filetul)"""
    s = lst[0]
    for x in lst[1:]:
        s = s.fuse(x)
    return s.Solids[0] if len(s.Solids) == 1 else s


def rot(s, ax, ang, c=(0, 0, 0)):
    s = s.copy()
    s.rotate(V(*c), V(*ax), ang)
    return s


def mv(s, x=0.0, y=0.0, z=0.0):
    s = s.copy()
    s.translate(V(x, y, z))
    return s


def ax_to(s, frm, to):
    """roteste un solid construit pe Z pe axa dorita: 'x' sau 'y'"""
    if to == 'x':
        return rot(s, (0, 1, 0), 90)
    if to == 'y':
        return rot(s, (1, 0, 0), -90)
    return s


# ---------------------------------------------------------------- filet, locasuri
def thread(r0, r1, P, z_top, z_bot, tip=0.0, run=0.0, flank=40.0):
    """filet elicoidal dreapta intre z_bot si z_top; descreste la varf pe 'tip' si la iesire pe 'run'"""
    h = r1 - r0
    base = min(0.8 * P, 2 * h * math.tan(math.radians(flank / 2)) + 0.12)
    L = z_top - z_bot
    hx = Part.makeHelix(P, L + 2 * P, r0 - 0.04)
    tri = Part.makePolygon([V(r0 - 0.04, 0, -base / 2), V(r1, 0, -0.05), V(r1, 0, 0.05), V(r0 - 0.04, 0, base / 2), V(r0 - 0.04, 0, -base / 2)])
    sw = Part.Wire(hx).makePipeShell([tri], True, True)
    sw.translate(V(0, 0, z_bot - P))
    R = r1 + 0.3
    trim = cyl(R, z_bot + tip, z_top - run)
    if tip > 0:
        trim = trim.fuse(cone(r0 - 0.1, R, z_bot, z_bot + tip))
    if run > 0:
        trim = trim.fuse(cone(R, r0, z_top - run, z_top))
    r = sw.common(trim)
    return r.Solids[0] if len(r.Solids) == 1 else r


def _cross(a, w, z):
    pts = [(w, a), (-w, a), (-w, w), (-a, w), (-a, -w), (-w, -w), (-w, -a), (w, -a), (w, -w), (a, -w), (a, w), (w, w)]
    return Part.makePolygon([V(x, y, z) for x, y in pts] + [V(pts[0][0], pts[0][1], z)])


def pz_cut(m, depth, z0=0.0, marks=True):
    """locas Pozidriv: cruce conica + cele 4 crestaturi la 45 grade de pe cap"""
    s = Part.makeLoft([_cross(0.22 * m, 0.10 * m, z0 - depth), _cross(m / 2, 0.17 * m, z0 + 0.3)], True)
    if marks:
        for k in range(4):
            s = s.fuse(rot(box(-0.09, 0.09, 0.2 * m, 0.42 * m, z0 - 0.12, z0 + 0.3), (0, 0, 1), 45 + 90 * k))
    return s


def hex_cut(af, depth, z0=0.0):
    R = af / math.sqrt(3)
    pts = [V(R * math.cos(math.radians(60 * i + 30)), R * math.sin(math.radians(60 * i + 30)), z0 + 0.3) for i in range(6)]
    s = Part.Face(Part.makePolygon(pts + [pts[0]])).extrude(V(0, 0, -(depth + 0.3)))
    return s.fuse(cone(0.05, R, z0 - depth - 0.6 * R, z0 - depth))


# ---------------------------------------------------------------- suruburi
SCR = {3.5: dict(dk=7.0, k=2.25, kp=2.6, d1=2.25, P=1.6, ds=2.55, m=3.9),
       4.0: dict(dk=8.0, k=2.55, kp=3.0, d1=2.55, P=1.8, ds=2.9, m=4.4),
       5.0: dict(dk=10.0, k=3.1, kp=3.6, d1=3.1, P=2.2, ds=3.6, m=5.2)}


def surub_pal(d, L, cap='inecat', b=None, col='zinc_galben'):
    s = SCR[d]
    r1, r0, tip = d / 2, s['d1'] / 2, 0.85 * d
    rs = s['ds'] / 2
    if cap == 'inecat':
        k = s['k']
        rn = rs if b else r0 + 0.12
        head = rev([(0, 0), (s['dk'] / 2, 0), (s['dk'] / 2, -0.25), (rn, -k), (0, -k)])
        rdepth = k + 0.2
    else:                                                   # cap bombat (lenticular)
        k = s['kp']
        R = s['dk'] / 2
        dome = [(R * t, -(k - 0.45) * (1 - math.sqrt(max(0.0, 1 - (t * 0.985) ** 2)))) for t in [i / 10 for i in range(11)]]
        rn = rs if b else r0 + 0.12
        head = rev([(0, 0)] + dome[1:] + [(R, -k), (rn, -k), (0, -k)])
        rdepth = k * 0.8
    zt = -k
    if cap != 'inecat':                                     # la capul bombat lungimea nominala se masoara sub cap (DIN 7505 B)
        L = L + k
    parts = [head]
    if b:                                                   # filet partial: tija neteda
        parts.append(cyl(rs, -(L - b), zt + 0.01))
        z_thr = -(L - b)
    else:
        z_thr = zt - 0.15
    pt = 0.5 * tip                                          # varful neted; filetul se termina deasupra lui, descrescand
    parts.append(cyl(r0, -L + pt, z_thr + 0.01))
    parts.append(rev([(0, -L), (0.12, -L), (r0, -L + pt), (0, -L + pt)]))
    parts.append(thread(r0, r1, s['P'], z_thr, -L + pt - 0.05, tip=tip - pt, run=0.8 if b else 0.4))
    sol = fuse(parts).cut(pz_cut(s['m'], rdepth))
    return [(sol, col)]


def confirmat(L=50.0):
    head = rev([(0, 0), (5.0, 0), (5.0, -1.2), (3.5, -3.0), (0, -3.0)])
    r0, r1 = 2.38, 3.5
    parts = [head, cyl(3.5, -12.0, -2.99), cyl(r0, -L + 2.5, -12.0), rev([(0, -L), (1.5, -L), (r0, -L + 2.5), (0, -L + 2.5)]),
             thread(r0, r1, 3.0, -12.4, -L + 2.45, tip=3.0, run=1.2, flank=50)]
    sol = fuse(parts).cut(hex_cut(4.0, 3.4))
    return [(sol, 'zinc')]


def capac_confirmat():
    R = 7.0
    dome = [(R * t, 0.4 + 1.2 * math.sqrt(max(0.0, 1 - t ** 2))) for t in [1 - i / 12 for i in range(1, 13)]]
    top = rev([(0, 0), (R, 0), (R, 0.4)] + dome)
    Rh = 3.9 / math.sqrt(3)
    hx = [V(Rh * math.cos(math.radians(60 * i + 30)), Rh * math.sin(math.radians(60 * i + 30)), -3.5) for i in range(6)]
    pin = Part.Face(Part.makePolygon(hx + [hx[0]])).extrude(V(0, 0, 3.55))
    return [(fuse([top, pin]), 'cashmere')]


def cep(L=35.0, d=8.0):
    r, c = d / 2, 1.0
    s = rev([(0, 0), (r - c, 0), (r, -c), (r, -L + c), (r - c, -L), (0, -L)])
    for i in range(10):
        s = s.cut(rot(box(-0.3, 0.3, r - 0.5, r + 0.5, -L + 1.2, -1.2), (0, 0, 1), 36 * i))
    return [(s, 'lemn')]


def saiba(d1=4.3, d2=9.0, h=0.8):
    return [(rev([(d1 / 2, 0), (d2 / 2, 0), (d2 / 2, -h), (d1 / 2, -h)]), 'zinc')]


def capsa(c=10.0, L=14.0, a=1.2, t=0.6):
    s = box(-c / 2, c / 2, -t / 2, t / 2, -a, 0)
    for x in (-c / 2, c / 2 - a):
        leg = box(x, x + a, -t / 2, t / 2, -L, -a + 0.01)
        tip = prism_xz([(x, -L), (x + a, -L), (x + a / 2 if x < 0 else x + a / 2, -L - 1.0)], -t / 2, t / 2)
        s = s.fuse([leg, tip])
    return [(s, 'zinc')]


def pin_raft():
    pin = rev([(0, 0), (2.5, 0), (2.5, -7.5), (2.1, -8.0), (0, -8.0)])
    plate = rbox(-4.5, 4.5, -4.2, 4.5, 0, 1.2, 1.5, 'z')
    tongue = box(-4.5, 4.5, -4.2, -2.5, 0.5, 11.0)
    tongue = fil(tongue, 0.6, lambda e: abs(e.tangentAt(0).x) > 0.99 and e.BoundBox.ZMax > 10)
    return [(fuse([pin, plate, tongue]), 'nichel')]


def coltar(a=40.0, w=20.0, t=2.0, holes=(14.0, 30.0), slot=False):
    """aripa 1 pe planul z = 0 (spre +y), aripa 2 pe planul y = 0 (spre +z); fetele interioare la z = t si y = t"""
    leg1 = box(0, w, 0, a, 0, t)
    leg2 = box(0, w, 0, t, 0, a)
    rib = prism_yz([(t - 0.1, t - 0.1), (t + 8, t - 0.1), (t - 0.1, t + 8)], w / 2 - 1.6, w / 2 + 1.6)
    s = fuse([leg1, leg2, rib])
    for p in holes:
        s = s.cut(cyl(2.25, -1, t + 1, w / 2, p).fuse(cone(2.25, 4.2, t - 1.0, t + 0.01, w / 2, p)))
        if slot and p == holes[-1]:
            h2 = fuse([cyl(2.6, -1, t + 1, 0, -3), cyl(2.6, -1, t + 1, 0, 3), box(-2.6, 2.6, -3, 3, -1, t + 1)])
        else:
            h2 = cyl(2.25, -1, t + 1).fuse(cone(2.25, 4.2, t - 1.0, t + 0.01))
        s = s.cut(mv(rot(h2, (1, 0, 0), -90), w / 2, 0, p))
    s = fil(s, 1.2, lambda e: abs(e.tangentAt(0).x) < 0.01 and (e.BoundBox.YMin > a - 0.5 or e.BoundBox.ZMin > a - 0.5))
    return [(s, 'zinc')]


def diblu(d=6.0, L=40.0):
    r = d / 2
    prof = [(1.6, 0), (r + 0.25, 0), (r + 0.25, -1.2), (r, -1.4)]
    z = -6.0
    while z > -L + 7:
        prof += [(r, z + 0.01), (r + 0.55, z - 0.4), (r, z - 2.6)]
        z -= 3.2
    prof += [(r, -L + 3), (r * 0.72, -L), (1.6, -L)]
    s = rev(prof)
    s = s.cut(box(-0.45, 0.45, -r - 1, r + 1, -L + 4, -9.0))
    s = s.cut(box(-r - 1, r + 1, -0.45, 0.45, -L - 1, -L + 9))
    for k in range(4):
        s = s.fuse(rot(prism_xz([(r - 0.2, -2.0), (r + 0.9, -2.6), (r + 0.9, -6.0), (r - 0.2, -6.0)], -0.6, 0.6), (0, 0, 1), 45 + 90 * k))
    return [(s, 'nylon')]


# ---------------------------------------------------------------- Blum: balamale si placuta
def _pz_head(x, y, z, R=3.6, h=1.6, axis='z', col='nichel'):
    s = rev([(0, 0)] + [(R * t, -(h - 0.3) * (1 - math.sqrt(max(0.0, 1 - (t * 0.985) ** 2)))) for t in [i / 8 for i in range(1, 9)]] + [(R, -h), (0, -h)])
    s = s.cut(pz_cut(R * 1.15, h * 0.8, marks=False))
    s = mv(s, 0, 0, h)
    if axis == 'x':
        s = rot(s, (0, 1, 0), 90)
    return mv(s, x, y, z)


def balama_clip_top(tip='aplicat', blumotion=False):
    """Cadru: usa la z<0 (fata din spate a usii la z = 0), lateralul corpului la x<0 (fata interioara la x = 0), y vertical.
    Pozitie inchisa, TB = 5, FA = 16 (aplicat) / cotit 9,5 (semiaplicat)."""
    xc = 6.5 if tip == 'aplicat' else 16.0
    out = []
    # cupa Ø35 (gaura) x 13; cupa propriu-zisa Ø34,8 x 11,3, goala
    cup = rev([(0, 0), (17.4, 0), (17.4, -9.6), (15.8, -11.3), (0, -11.3)])
    cup = cup.cut(cyl(15.9, -10.3, 0.5))
    # flansa 57 x 22 x 3,2 cu gaurile de prindere la 45 / 9,5
    fx = xc + 9.5
    fl = fuse([box(fx - 11, fx + 11, -17.5, 17.5, 0, 3.2), cyl(11, 0, 3.2, fx, -17.5), cyl(11, 0, 3.2, fx, 17.5), cyl(18.2, 0, 1.4, xc, 0)])
    fl = fil(fl, 0.8, lambda e: e.BoundBox.ZMin > 3.1)
    for yy in (-22.5, 22.5):
        fl = fl.cut(cyl(2.3, -1, 5, fx, yy).fuse(cone(2.3, 3.9, 1.6, 3.25, fx, yy)))
    fl = fl.cut(cyl(15.9, -1, 5, xc, 0))
    cup = mv(cup, xc, 0, 0)
    out.append((fuse([cup, fl]), 'nichel'))
    # mecanismul din cupa: bolturi + bratele de legatura
    pins = [mv(rot(cyl(1.6, -8.5, 8.5), (1, 0, 0), 90), px, 0, pz) for (px, pz) in ((xc + 6.0, -4.0), (xc - 2.0, -6.5))]
    out += [(p, 'otel') for p in pins]
    link1 = prism_xz([(xc + 4.6, -5.0), (xc + 7.4, -3.0), (19.5, 9.0), (16.7, 11.0)], -6.8, 6.8)
    link2 = prism_xz([(xc - 3.4, -7.5), (xc - 0.6, -5.5), (13.5, 7.0), (10.7, 9.0)], -5.6, 5.6)
    out += [(link1, 'otel'), (link2, 'otel')]
    # bratul: profil U deschis spre lateral, peste placuta (fata de sus la 21,5 de lateral)
    arm = rbox(8.5, 21.5, -8.5, 8.5, 6.0, 62.0, 1.6, 'z')
    arm = fil(arm, 1.4, lambda e: abs(e.tangentAt(0).z) > 0.99 and e.BoundBox.XMin > 21.4)
    arm = arm.cut(box(7.0, 20.0, -7.2, 7.2, 5.0, 60.6))           # profil U, inchis la capatul din spate
    neck = prism_xz([(12.0, 3.0), (21.5, 6.0), (21.5, 9.0), (12.0, 6.5)], -7.6, 7.6)
    for (zz, ww, ll) in ((25.5, 5.8, 7.0), (43.0, 5.8, 7.0)):
        arm = arm.cut(box(19.0, 23.0, -ww / 2, ww / 2, zz - ll / 2, zz + ll / 2))
    arm = arm.cut(box(19.0, 23.0, -1.4, 1.4, 8.5, 12.0))
    out.append((fuse([arm, neck]), 'nichel'))
    out.append((_pz_head(21.3, 0, 17.0, axis='x'), 'nichel'))
    out.append((_pz_head(21.3, 0, 34.5, axis='x'), 'nichel'))
    lever = fuse([box(19.8, 22.6, -6.2, 6.2, 50.0, 61.0)] + [box(22.5, 23.1, -6.2, 6.2, 51.0 + 2.0 * i, 51.8 + 2.0 * i) for i in range(5)])
    out.append((lever, 'gri_inchis'))
    if tip != 'aplicat':                                    # cotitura de 9,5 a bratului semiaplicat
        out.append((prism_xz([(8.5, 4.0), (12.0, 4.0), (18.0, -1.0), (14.5, -1.0)], -7.0, 7.0), 'nichel'))
    if blumotion:                                           # amortizorul BLUMOTION din cupa
        dmp = cyl(9.0, -10.2, -1.0, xc - 4.0, 0).common(box(xc - 14, xc - 1.5, -10, 10, -11, 0))
        out.append((dmp, 'gri_blum'))
        out.append((box(xc - 15.2, xc - 12.6, -2.0, 2.0, -3.0, 0.6), 'negru'))
    return out


def placuta_173L6100():
    """Placuta CLIP in cruce 0 mm: H 8,5; gauri ovale la ±16 (32), la 37 de muchia din fata (z = 0)."""
    body = rbox(0, 8.5, -7.0, 7.0, 22.0, 60.0, 1.5, 'x')
    body = fil(body, 1.0, lambda e: e.BoundBox.XMin > 8.4)
    body = body.cut(box(6.0, 9.0, -2.2, 2.2, 30.0, 55.0))           # canalul pentru clipsul bratului
    body = body.cut(box(-1, 5.5, -5.6, 5.6, 23.5, 58.5))             # interior gol (de jos)
    wings = fuse([box(0, 3.0, -17.0, 17.0, 30.0, 44.0)] + [mv(rot(cyl(7.0, 0, 3.0), (0, 1, 0), 90), 0, yy, 37.0) for yy in (-17.0, 17.0)])
    s = fuse([body, wings])
    for yy in (-16.0, 16.0):
        slot = fuse([mv(rot(cyl(2.3, -1, 12), (0, 1, 0), 90), 0, yy - 1.6, 37.0), mv(rot(cyl(2.3, -1, 12), (0, 1, 0), 90), 0, yy + 1.6, 37.0),
                     box(-1, 11, yy - 1.6, yy + 1.6, 37.0 - 2.3, 37.0 + 2.3)])
        cs = fuse([mv(rot(cone(2.3, 4.0, 1.6, 3.05), (0, 1, 0), 90), 0, yy + dy, 37.0) for dy in (-1.6, 1.6)])
        s = s.cut(slot).cut(cs)
    return [(s, 'nichel')]


# ---------------------------------------------------------------- Blum TIP-ON (usi)
def tipon_usa():
    """TIP-ON scurt cu magnet 956.1004: corp Ø10 introdus spre -z; inel de reglaj si piston cu magnet spre +z."""
    body = fuse([cyl(5.0, -48.0, 0.0)] + [rot(box(4.6, 5.6, -0.5, 0.5, -46.0, -4.0), (0, 0, 1), 120 * i) for i in range(3)])
    body = body.fuse(rev([(0, -48.6), (4.2, -48.6), (5.0, -47.8), (0, -47.8)]))
    ring = rev([(3.6, 0), (6.4, 0), (6.4, 5.5), (3.6, 5.5)])
    for i in range(18):
        ring = ring.cut(rot(box(6.0, 7.0, -0.35, 0.35, 0.6, 4.9), (0, 0, 1), 20 * i))
    plunger = cyl(3.6, 0.0, 12.0)
    mag = rev([(0, 12.0), (3.9, 12.0), (3.9, 13.4), (3.4, 14.0), (0, 14.0)])
    return [(body, 'gri_blum'), (ring, 'gri_inchis'), (plunger, 'gri_blum'), (mag, 'magnet')]


def adaptor_tipon():
    """adaptor drept 956.1201: lungime 53, ax TIP-ON la 14,5 deasupra bazei (y = 0), suruburi la 20 si 37 de fata (z = 0)"""
    prof = [(-9.0, 0), (9.0, 0)] + [(9.0 * math.cos(math.radians(a)), 16.0 + 6.0 * math.sin(math.radians(a))) for a in range(0, 181, 15)]
    w = Part.makePolygon([V(x, y, 0) for x, y in prof] + [V(prof[0][0], prof[0][1], 0)])
    s2 = Part.Face(w).extrude(V(0, 0, -53.0)).cut(cyl(5.1, -54, 1, 0, 14.5))
    for zz in (-20.0, -37.0):
        s2 = s2.cut(mv(rot(cyl(2.2, -30, 30), (1, 0, 0), -90), 0, 0, zz))
        s2 = s2.cut(mv(rot(cyl(4.2, 0, 30), (1, 0, 0), -90), 0, 3.0, zz))
    s2 = fil(s2, 0.8, lambda e: abs(e.tangentAt(0).z) < 0.01 and e.BoundBox.ZMin > -0.1)
    return [(s2, 'nichel')]


def placa_tipon():
    disc = rev([(0, 0), (7.5, 0), (7.5, -1.0), (0, -1.0)]).cut(cone(1.9, 3.5, -1.05, 0.01))
    scr = surub_pal(3.5, 12, 'inecat', col='nichel')[0][0]
    return [(disc, 'otel'), (mv(scr, 0, 0, 0.0), 'nichel')]


# ---------------------------------------------------------------- Blum MOVENTO + TIP-ON BLUMOTION
def glisiera_movento(NL=350.0):
    """Cadru: lateralul corpului la x = 0 (interior x>0), muchia din fata a corpului la y = 0, glisiera spre -y; baza profilului la z = 0.
    Catalog Blum 2022/23 p. 437 si 2024/25 p. 419 / 428: profil L pe lateral, glisiera sub fundul sertarului (fundul la z = 28,5),
    fata interioara a lateralului de sertar la x = 21; suruburi 609.1500 la z = 38, la 37 / 69 / 261 mm de muchia din fata (NL 300-350);
    carligul din spate intra in gaura Ø6 x 10 din capatul lateralului de sertar (la 7 mm de fata exterioara, 11 mm de jos)."""
    y0, y1 = -2.0, -(NL + 1.0)
    out = []
    Lp = fuse([box(0, 1.5, y1, y0, 0, 46.0), box(0, 26.0, y1, y0, 0, 1.5), box(24.5, 26.0, y1, y0, 0, 5.0)])
    for yy in (-37.0, -69.0, -261.0 if NL >= 300 else -197.0):                      # gaurile de prindere (cu fraiza pentru cap)
        Lp = Lp.cut(mv(rot(cyl(1.9, -1, 3), (0, 1, 0), 90), 0, yy, 38.0)).cut(mv(rot(cone(1.9, 3.6, 0.0, 1.55), (0, 1, 0), 90), 0, yy, 38.0))
    for yy in (-9.0, -101.0, -133.0, -229.0, -293.0):                               # restul gaurilor de sistem
        if yy > y1 + 10:
            Lp = Lp.cut(mv(rot(cyl(1.9, -1, 3), (0, 1, 0), 90), 0, yy, 38.0))
    out.append((Lp, 'zinc'))
    outer = fuse([box(24.5, 47.0, y1 + 4, y0 - 2, 1.5, 3.0), box(24.5, 26.0, y1 + 4, y0 - 2, 1.5, 20.0), box(45.5, 47.0, y1 + 4, y0 - 2, 1.5, 20.0)])
    mid = fuse([box(28.0, 43.5, y1 + 14, y0 - 6, 4.0, 5.2), box(28.0, 29.2, y1 + 14, y0 - 6, 4.0, 22.0), box(42.3, 43.5, y1 + 14, y0 - 6, 4.0, 22.0)])
    inner = fuse([box(25.0, 47.0, y1 + 8, y0 - 4, 26.8, 28.5), box(31.0, 32.4, y1 + 8, y0 - 4, 9.0, 27.0), box(39.0, 40.4, y1 + 8, y0 - 4, 9.0, 27.0)])
    out += [(outer, 'zinc'), (mid, 'otel'), (inner, 'zinc')]
    for yy in (y0 - 14, y1 + 26):                        # role
        out.append((mv(rot(cyl(5.0, -1.6, 1.6), (0, 1, 0), 90), 35.7, yy, 13.0), 'negru'))
    out.append((box(47.0, 59.0, y1 + 30, y1 + 30 + 0.55 * NL, 3.0, 22.0), 'gri_blum'))      # amortizor BLUMOTION
    yr = -(NL - 10.0)                                                                     # capatul din spate al sertarului (SKL = NL - 10)
    hook = fuse([box(10.0, 26.0, yr - 6.0, yr, 20.5, 32.5), box(24.0, 32.0, yr - 6.0, yr + 4.0, 24.0, 28.5),
                 mv(rot(cyl(2.8, 0, 8.0), (1, 0, 0), -90), 12.0, yr, 26.5)])
    out.append((hook, 'zinc'))                                                            # carligul din spate
    out.append((box(25.0, 47.0, y0 - 9, y0 - 4, 21.0, 26.8), 'gri_blum'))                   # opritor fata
    return out


def tip_on_movento(NL=350.0, LW=464.0):
    """unitate TIP-ON BLUMOTION pentru MOVENTO: se clipseaza pe glisiera (cadrul glisierei); spre interior pana la x = 133,5,
    unde intra bara de sincronizare (lungime LW - 267, MD Blum TIP-ON BLUMOTION p. 3)."""
    ya, yb = -(NL - 20.0), -(NL - 190.0)
    hs = rbox(47.0, 128.0, ya, yb, 4.0, 16.0, 3.0, 'z')
    hs = fil(hs, 1.2, lambda e: abs(e.tangentAt(0).z) < 0.01 and e.BoundBox.ZMin > 15.9)
    for i in range(10):
        hs = hs.cut(box(60.0 + 6.0 * i, 62.5 + 6.0 * i, ya + 30, yb - 40, 15.0, 17.0))
    clip = box(40.0, 50.0, ya + 20, ya + 70, 1.5, 9.0)
    lever = fuse([box(70.0, 104.0, yb, yb + 10.0, 6.0, 14.0), box(82.0, 92.0, yb + 10.0, yb + 16.0, 7.0, 13.0)])
    sock = mv(rot(cyl(6.5, 0, 5.5), (0, 1, 0), 90), 128.0, (ya + yb) / 2, 10.0)
    return [(hs, 'gri_blum'), (clip, 'gri_inchis'), (lever, 'gri_inchis'), (sock, 'negru')]


def cleme_movento():
    """clema de cuplare T51.7601 (dreapta): sub fundul sertarului, lipita de lateral si in fata; fata de sus la z = 0 (fundul), corpul spre -z;
    x = 0 la fata interioara a lateralului de sertar (spre interior +x), y = 0 la fata sertarului (spre spate -y). Forma de pana, ca in MD MOVENTO."""
    prof = [(0, 0), (-52.0, 0), (-52.0, -5.0), (-30.0, -12.0), (0, -12.0)]
    b = prism_yz(prof, 2.0, 36.0)
    b = fil(b, 1.5, lambda e: abs(e.tangentAt(0).x) > 0.99)
    b = b.cut(box(6.0, 32.0, -44.0, -16.0, -13, -9.0))
    tab = box(0, 9.0, -30.0, -4.0, -12.0, 0)
    wheel = mv(rot(cyl(6.5, 0, 4.0), (0, 1, 0), 90), 20.0, -8.0, -9.0)
    for i in range(16):
        wheel = wheel.cut(mv(rot(box(-0.5, 0.5, -0.4, 0.4, 5.9, 6.9), (1, 0, 0), 22.5 * i), 22.0, -8.0, -9.0))
    holes = [mv(cyl(1.9, -13, 1), 0, 0, 0)]
    b = fuse([b, tab])
    for (xx, yy) in ((26.0, -36.0), (12.0, -46.0)):                    # gauri cu lamaj: capul surubului la 5 mm sub fund
        b = b.cut(cyl(1.9, -13, 1, xx, yy)).cut(cyl(3.8, -13, -5.0, xx, yy))
    return [(b, 'gri_blum'), (wheel, 'portocaliu' if False else 'gri_inchis')]


def bara_sincronizare(L=197.0):
    """bara de sincronizare (MOVENTO: L = LW - 267), axa pe +x de la 0 la L; capetele intra in unitatile TIP-ON BLUMOTION"""
    rod = mv(rot(cyl(4.0, 0, L), (0, 1, 0), 90), 0, 0, 0)
    ends = [mv(rot(cyl(5.2, 0, 9.0), (0, 1, 0), 90), x, 0, 0) for x in (0.0, L - 9.0)]
    return [(rod, 'zinc'), (ends[0], 'negru'), (ends[1], 'negru')]


# ---------------------------------------------------------------- glisiera cu bile, corp, perete, bara
def glisiera_bile(NL=450.0):
    y0, y1 = -2.0, -(NL + 2.0)
    out = []
    outer = fuse([box(0, 1.2, y1, y0, -22.5, 22.5), box(0, 6.5, y1, y0, 21.3, 22.5), box(0, 6.5, y1, y0, -22.5, -21.3)])
    for yy in [-35.0, -67.0, -163.0, -259.0, -355.0, y1 + 20]:
        outer = outer.cut(fuse([mv(rot(cyl(2.2, -1, 3), (0, 1, 0), 90), 0, yy - 2, 0), mv(rot(cyl(2.2, -1, 3), (0, 1, 0), 90), 0, yy + 2, 0), box(-1, 3, yy - 2, yy + 2, -2.2, 2.2)]))
    mid = fuse([box(4.4, 5.4, y1 + 6, y0 - 3, -18.5, 18.5), box(4.4, 9.4, y1 + 6, y0 - 3, 17.5, 18.5), box(4.4, 9.4, y1 + 6, y0 - 3, -18.5, -17.5)])
    inner = fuse([box(11.5, 12.7, y1 + 12, y0, -14.0, 14.0), box(8.4, 12.7, y1 + 12, y0, 13.0, 14.0), box(8.4, 12.7, y1 + 12, y0, -14.0, -13.0)])
    out += [(outer, 'zinc'), (mid, 'zinc'), (inner, 'zinc')]
    balls = []
    for yy in [y0 - 8 - 6 * i for i in range(6)] + [y1 + 14 + 6 * i for i in range(6)]:
        for zz in (19.9, -19.9):
            balls.append(Part.makeSphere(1.6, V(3.2, yy, zz)))
        for zz in (15.7, -15.7):
            balls.append(Part.makeSphere(1.6, V(7.0, yy, zz)))
    out.append((fuse(balls), 'otel'))
    out.append((box(0.5, 6.0, y1, y1 + 48, -12.0, 12.0), 'negru'))
    out.append((box(8.6, 11.5, y0 - 26, y0 - 6, -9.0, 9.0), 'negru'))
    return out


def picior(h=100.0):
    plate = rev([(0, 0), (30.0, 0), (30.0, -4.0), (0, -4.0)])
    for k in range(4):
        a = math.radians(45 + 90 * k)
        plate = plate.cut(cyl(2.3, -5, 1, 22 * math.cos(a), 22 * math.sin(a)).fuse(cone(2.3, 4.2, -1.6, 0.01, 22 * math.cos(a), 22 * math.sin(a))))
    tube = rev([(0, -3.9), (16.0, -3.9), (16.0, -h + 22.0), (12.0, -h + 18.0), (0, -h + 18.0)])
    for k in range(6):
        tube = tube.fuse(rot(box(15.5, 18.0, -0.9, 0.9, -h + 26, -6.0), (0, 0, 1), 60 * k))
    tube = tube.cut(rev([(15.0, -h + 44), (18.5, -h + 44), (18.5, -h + 49), (15.0, -h + 49)]))
    spindle = cyl(9.0, -h + 6.0, -h + 22.0)
    for i in range(6):
        spindle = spindle.cut(rev([(8.4, -h + 8 + 2.4 * i), (9.5, -h + 8 + 2.4 * i), (9.5, -h + 9 + 2.4 * i), (8.4, -h + 9 + 2.4 * i)]))
    foot = rev([(0, -h), (19.0, -h), (20.0, -h + 1.0), (20.0, -h + 6.0), (0, -h + 6.0)])
    return [(fuse([plate, tube]), 'negru'), (spindle, 'gri_inchis'), (foot, 'negru')]


def clema_soclu():
    ring = rev([(16.2, 0), (19.0, 0), (19.0, 5.0), (16.2, 5.0)]).cut(box(-8.0, 8.0, 10.0, 30.0, -1, 6))
    arm = box(-6.0, 6.0, -42.0, -18.5, 0, 5.0)
    pad = box(-15.0, 15.0, -45.0, -42.0, -15.0, 25.0)
    for zz in (-5.0, 15.0):
        pad = pad.cut(mv(rot(cyl(2.2, -1, 5), (1, 0, 0), 90), 0, -40.0, zz))
    return [(fuse([ring, arm, pad]), 'negru')]


def agatatoare():
    """agatatoare corp suspendat (tip Camar 807): lateralul la x = 0, spatele corpului la y = 0, sus la z = 0"""
    hs = rbox(0, 15.0, -52.0, 0, -66.0, 0, 2.0, 'x')
    hs = fil(hs, 1.0, lambda e: e.BoundBox.XMin > 14.9)
    cover = box(15.0, 16.2, -50.0, -2.0, -64.0, -2.0)
    hook = fuse([box(4.0, 11.0, -2.0, 11.0, -16.0, -10.0), box(4.0, 11.0, 8.0, 11.0, -24.0, -10.0)])
    s1 = _pz_head(16.0, -40.0, -14.0, R=3.5, h=1.5, axis='x')
    s2 = _pz_head(16.0, -40.0, -50.0, R=3.5, h=1.5, axis='x')
    return [(hs, 'alb'), (cover, 'alb'), (hook, 'zinc'), (s1, 'zinc'), (s2, 'zinc')]


def sina_suspendare(L=300.0):
    prof = [(0, 0), (10.0, 0), (10.0, -8.0), (8.5, -8.0), (8.5, -1.5), (1.5, -1.5), (1.5, -50.0), (0, -50.0)]
    w = Part.makePolygon([V(0, y, z) for y, z in prof] + [V(0, 0, 0)])
    s = Part.Face(w).extrude(V(L, 0, 0))
    for x in [20.0 + i * (L - 40.0) / 4 for i in range(5)]:
        s = s.cut(fuse([mv(rot(cyl(2.6, -1, 3), (1, 0, 0), -90), x - 3, 0, -30.0), mv(rot(cyl(2.6, -1, 3), (1, 0, 0), -90), x + 3, 0, -30.0), box(x - 3, x + 3, -1, 3, -32.6, -27.4)]))
    return [(s, 'zinc')]


def bara_ovala(L=300.0):
    e1 = Part.Face(Part.Wire(Part.Ellipse(V(0, 0, 0), 15.0, 7.5).toShape()))
    e2 = Part.Face(Part.Wire(Part.Ellipse(V(0, 0, 0), 14.0, 6.5).toShape()))
    s = e1.cut(e2).extrude(V(0, 0, L))
    s = rot(s, (0, 1, 0), 90)
    return [(s, 'crom')]


def suport_bara():
    fl = rev([(0, 0), (25.0, 0), (25.0, 3.0), (0, 3.0)])
    fl = rot(fl, (0, 1, 0), 90)
    e1 = Part.Face(Part.Wire(Part.Ellipse(V(0, 0, 0), 17.0, 9.5).toShape())).extrude(V(0, 0, 12.0))
    e2 = Part.Face(Part.Wire(Part.Ellipse(V(0, 0, 0), 15.2, 7.7).toShape())).extrude(V(0, 0, 13.0))
    cup = rot(e1.cut(mv(e2, 0, 0, 1.5)), (0, 1, 0), 90)
    s = fl.fuse(cup)
    for k in range(3):
        a = math.radians(90 + 120 * k)
        s = s.cut(mv(rot(cyl(2.1, -1, 5), (0, 1, 0), 90), 0, 21.5 * math.cos(a), 21.5 * math.sin(a)))
    return [(s, 'crom')]


def banda_dublu():
    return [(box(0, 100.0, 0, 25.0, -0.6, -0.05), 'alb'), (box(0, 100.0, 0, 25.0, -0.05, 0), 'rosu')]


BUILD = {
    'confirmat': confirmat, 'capac_confirmat': capac_confirmat, 'cep': cep,
    'surub_3_5x15': lambda: surub_pal(3.5, 15, 'inecat', col='nichel'), 'surub_3_5x17': lambda: surub_pal(3.5, 17, 'inecat', col='nichel'),
    'surub_3_5x16': lambda: surub_pal(3.5, 16, 'inecat'), 'surub_4x16': lambda: surub_pal(4.0, 16, 'bombat'), 'surub_4x25': lambda: surub_pal(4.0, 25, 'bombat'),
    'surub_4x30': lambda: surub_pal(4.0, 30, 'inecat'), 'surub_4x40': lambda: surub_pal(4.0, 40, 'inecat', b=24.0),
    'saiba': saiba, 'capsa': capsa, 'pin_raft': pin_raft, 'coltar_40': coltar,
    'anti_rasturnare': lambda: coltar(35.0, 20.0, 2.0, holes=(13.0, 26.0), slot=True), 'diblu_6x40': diblu,
    'balama_blum': lambda: balama_clip_top('aplicat'), 'balama_70T3650': lambda: balama_clip_top('semi'),
    'balama_71B3550': lambda: balama_clip_top('aplicat', blumotion=True), 'placuta_balama': placuta_173L6100,
    'tipon_usa': tipon_usa, 'adaptor_tipon': adaptor_tipon, 'placa_tipon': placa_tipon,
    'glisiera_movento': glisiera_movento, 'tip_on': tip_on_movento, 'cleme_movento': cleme_movento, 'bara_sincronizare': bara_sincronizare,
    'glisiera_bile_450': glisiera_bile, 'picior': picior, 'clema_soclu': clema_soclu, 'suport_suspendare': agatatoare,
    'sina_suspendare': sina_suspendare, 'bara_ovala': bara_ovala, 'suport_bara': suport_bara, 'banda_dublu': banda_dublu,
}
assert set(BUILD) == {c[0] for c in CATALOG}, set(BUILD) ^ {c[0] for c in CATALOG}


PARAM = {'coltar_40': lambda a: coltar(a, 30.0, 3.0, holes=(30.0, a - 30.0)), 'bara_sincronizare': bara_sincronizare, 'picior': picior, 'glisiera_movento': glisiera_movento, 'tip_on': tip_on_movento,
         'glisiera_bile_450': glisiera_bile, 'sina_suspendare': sina_suspendare, 'bara_ovala': bara_ovala}


def build(mid):
    """'id' din catalog sau 'id@parametru' (ex. bara_sincronizare@197, glisiera_movento@500)"""
    out = []
    if '@' in mid:
        base, arg = mid.split('@', 1)
        parts = PARAM[base](float(arg))
    else:
        parts = BUILD[mid]()
    for s, c in parts:
        if s is None:
            continue
        out.append((s, c))
    return out
