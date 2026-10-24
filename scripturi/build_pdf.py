import fitz, math, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "Apartament_184_documentatie.pdf"
W, HH = 1190.55, 841.89          # A3 landscape (pt)
FR = r"C:\Windows\Fonts\segoeui.ttf"
FB = r"C:\Windows\Fonts\segoeuib.ttf"
fr = fitz.Font(fontfile=FR)
fb = fitz.Font(fontfile=FB)

INK = (0.11, 0.12, 0.14)
MUT = (0.45, 0.47, 0.50)
ACC = (0.0, 0.37, 0.60)
RED = (0.78, 0.15, 0.15)
WALL = (0.15, 0.16, 0.18)
HEIGHT = 250.0                    # cm, inaltime libera
SLAB = 15.0                       # cm, grosime planseu (ipoteza)
S = 72 / 2.54 / 50.0              # pt per cm la 1:50

TINT = {
    "dorm": (0.90, 0.94, 0.98), "cz": (0.99, 0.96, 0.88), "kit": (0.99, 0.91, 0.86),
    "bath": (0.88, 0.96, 0.96), "vest": (0.95, 0.95, 0.88), "hol": (0.94, 0.91, 0.97),
    "nisa": (0.90, 0.90, 0.90),
}


def fmt(v):
    if abs(v - round(v)) < 0.05:
        return str(int(round(v)))
    return ("%.1f" % v).replace(".", ",")


def fmt2(v):
    return ("%.2f" % v).replace(".", ",")


def xo(y):
    return 968 + 0.2579 * (570 - y)


def xi(y):
    return xo(y) - 15.5


def poly_area(pts):
    a = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        a += x1 * y2 - x2 * y1
    return abs(a) / 2.0


def poly_perim(pts):
    return sum(math.dist(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts)))


# ------------------------------------------------------------------ geometrie (cm, y in jos)
ROOMS = [
    # id, nume, tinta, poligon, dimensiuni text, observatii
    ("dorm", "Dormitor", [(15, 25), (355, 25), (355, 384.5), (15, 384.5)], "340 × 359,5", ""),
    ("cz", "Cameră de zi", [(370, 25), (710, 25), (710, 555), (370, 555)], "340 × 529,5", ""),
    ("kit", "Bucătărie", [(725, 25), (980, 25), (980, 347), (725, 347)], "255 × 322", ""),
    ("hol", "Hol", [(725, 354.5), (xi(354.5), 354.5), (xi(555), 555), (725, 555)], "≈ 283 / 231 × 200", "trapez (perete oblic)"),
    ("bath", "Baie", [(15, 392), (245, 392), (245, 555), (15, 555)], "230 × 163", ""),
    ("vest", "Vestibul", [(252.5, 392), (355, 392), (355, 555), (252.5, 555)], "102,5 × 163", ""),
    ("nisa", "Nișă tehnică*", [(987.5, 25), (xi(25), 25), (xi(347), 347), (987.5, 347)], "≈ 107 / 24 × 322", "destinație de confirmat"),
]
AREA = {r[0]: poly_area(r[2]) / 1e4 for r in ROOMS}
PERIM = {r[0]: poly_perim(r[2]) / 100 for r in ROOMS}
AREA["dorm"] = 340 * 359.5 / 1e4        # exact din cote
AREA["cz"] = 340 * 529.5 / 1e4
AREA["kit"] = 255 * 322 / 1e4
AREA["bath"] = 230 * 163 / 1e4
AREA["vest"] = 102.5 * 163 / 1e4
FOOTPRINT = poly_area([(0, 0), (1115, 0), (968, 570), (0, 570)]) / 1e4
LOCUIBILA = round(AREA["dorm"], 2) + round(AREA["cz"], 2)
UTILA = sum(AREA[r[0]] for r in ROOMS if r[0] != "nisa")
BALCON = 370 * 130 / 1e4

FEREASTRE = [  # id, loc, x0, x1, parapet, inaltime
    ("F1", "Dormitor", 168, 328, 90, 150),
    ("F2", "Cameră de zi", 375, 520, 90, 150),
    ("F3", "Bucătărie", 823, 963, 90, 150),
]
USI = [  # id, loc, latime, inaltime
    ("U1", "Dormitor – vestibul", 90, 210),
    ("U2", "Vestibul – baie", 70, 210),
    ("U3", "Cameră de zi – vestibul", 90, 210),
    ("U4", "Cameră de zi – hol", 90, 210),
    ("U5", "Hol – bucătărie", 80, 210),
    ("U6", "Bucătărie – nișă tehnică*", 70, 210),
    ("U7", "Intrare apartament (hol)", 90, 210),
    ("U8", "Cameră de zi – balcon", 85, 220),
]


# ------------------------------------------------------------------ desen
class Sheet:
    def __init__(self, doc):
        self.pg = doc.new_page(width=W, height=HH)
        self.pg.insert_font(fontname="sg", fontfile=FR)
        self.pg.insert_font(fontname="sgb", fontfile=FB)

    def text(self, x, y, t, size=8, bold=False, color=INK, align="l", rot=0):
        f = fb if bold else fr
        w = f.text_length(t, fontsize=size)
        if rot == 0:
            if align == "c":
                x -= w / 2
            elif align == "r":
                x -= w
        else:
            if align == "c":
                y += w / 2
        self.pg.insert_text(fitz.Point(x, y), t, fontsize=size,
                            fontname="sgb" if bold else "sg", color=color, rotate=rot)

    def line(self, a, b, color=INK, width=0.5, dash=None):
        self.pg.draw_line(fitz.Point(*a), fitz.Point(*b), color=color, width=width, dashes=dash)

    def rect(self, x0, y0, x1, y1, fill=None, color=INK, width=0.5, dash=None, radius=None):
        r = fitz.Rect(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
        if radius:
            self.pg.draw_rect(r, color=color, fill=fill, width=width, dashes=dash, radius=radius)
        else:
            self.pg.draw_rect(r, color=color, fill=fill, width=width, dashes=dash)

    def poly(self, pts, fill=None, color=INK, width=0.5, close=True, dash=None):
        self.pg.draw_polyline([fitz.Point(*p) for p in pts], color=color, fill=fill,
                              width=width, closePath=close, dashes=dash)

    def circle(self, c, r, fill=None, color=INK, width=0.5):
        self.pg.draw_circle(fitz.Point(*c), r, color=color, fill=fill, width=width)


def frame(sh, title, sub, scale, n, N):
    sh.rect(24, 24, W - 24, HH - 24, color=INK, width=0.8)
    # titlu sus
    sh.text(40, 52, title, 17, True, INK)
    sh.text(40, 68, sub, 8.5, False, MUT)
    sh.line((40, 76), (W - 40, 76), MUT, 0.4)
    # cartus
    y0 = HH - 82
    sh.line((24, y0), (W - 24, y0), INK, 0.8)
    cols = [24, 400, 700, 900, 1010, W - 24]
    for c in cols[1:-1]:
        sh.line((c, y0), (c, HH - 24), INK, 0.4)
    sh.text(34, y0 + 12, "OBIECT", 6, False, MUT)
    sh.text(34, y0 + 28, "Apartament nr. 184 – Bloc L14", 11, True)
    sh.text(34, y0 + 42, "Locuințe Titan", 8.5)
    sh.text(34, y0 + 53, "Releveu redesenat și modelat 3D (FreeCAD)", 7.5, False, MUT)
    sh.text(410, y0 + 12, "PLANȘĂ", 6, False, MUT)
    sh.text(410, y0 + 30, sub if len(sub) < 70 else title, 10, True)
    sh.text(410, y0 + 44, title, 8.5)
    sh.text(710, y0 + 12, "NOTĂ", 6, False, MUT)
    sh.text(710, y0 + 26, "Document informativ, întocmit după releveul original.", 7)
    sh.text(710, y0 + 37, "Nu înlocuiește releveul / documentația cadastrală.", 7)
    sh.text(710, y0 + 48, "Cotele marcate cu * sunt deduse sau de confirmat.", 7)
    sh.text(910, y0 + 12, "SCARĂ", 6, False, MUT)
    sh.text(910, y0 + 32, scale, 13, True, ACC)
    sh.text(1020, y0 + 12, "PLANȘA", 6, False, MUT)
    sh.text(1020, y0 + 32, "%d / %d" % (n, N), 13, True)
    sh.text(1020, y0 + 46, "05.10.2026", 7.5, False, MUT)


def chain(sh, cms, tf, axis, pos, ext_to=None, labels=None, size=6.0, color=ACC, extra_ext=0):
    pts = [tf(c) for c in cms]
    if axis == "h":
        sh.line((min(pts), pos), (max(pts), pos), color, 0.4)
    else:
        sh.line((pos, min(pts)), (pos, max(pts)), color, 0.4)
    for i, c in enumerate(cms):
        p = pts[i]
        et = None
        if ext_to is not None:
            et = ext_to(c) if callable(ext_to) else ext_to
        if axis == "h":
            if et is not None:
                sgn = 1 if et > pos else -1
                sh.line((p, pos - sgn * 2.5), (p, et - sgn * 2.0), color, 0.3)
            sh.line((p - 2.4, pos + 2.4), (p + 2.4, pos - 2.4), color, 0.7)
        else:
            if et is not None:
                sgn = 1 if et > pos else -1
                sh.line((pos - sgn * 2.5, p), (et - sgn * 2.0, p), color, 0.3)
            sh.line((pos - 2.4, p + 2.4), (pos + 2.4, p - 2.4), color, 0.7)
    for i in range(len(cms) - 1):
        d = abs(cms[i + 1] - cms[i])
        if labels is not None:
            lab = labels[i]
        else:
            lab = None if d < 6 else fmt(d)
        if lab in (None, ""):
            continue
        mid = (pts[i] + pts[i + 1]) / 2
        if axis == "h":
            sh.text(mid, pos - 2.2, lab, size, False, color, "c")
        else:
            sh.text(pos - 2.2, mid, lab, size, False, color, "c", rot=90)


def tag(sh, c, label, r=6.3):
    sh.circle(c, r, fill=(1, 1, 1), color=ACC, width=0.7)
    sh.text(c[0], c[1] + 1.9, label, 5.4, True, ACC, "c")


def arc_pts(h, c, o, n=22):
    r = math.dist(h, c)
    a0 = math.atan2(c[1] - h[1], c[0] - h[0])
    a1 = math.atan2(o[1] - h[1], o[0] - h[0])
    d = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    return [(h[0] + r * math.cos(a0 + d * k / n), h[1] + r * math.sin(a0 + d * k / n)) for k in range(n + 1)]


# ------------------------------------------------------------------ PLAN
PX, PY = 150.0, 205.0


def P(x, y):
    return (PX + x * S, PY + y * S)


def fill_poly_cm(sh, pts, fill, color=None, width=0.2):
    sh.poly([P(*p) for p in pts], fill=fill, color=color if color else fill, width=width)


def seg_gaps(a0, a1, gaps):
    segs, cur = [], a0
    for a, b in sorted(gaps):
        if a > cur:
            segs.append((cur, a))
        cur = b
    if cur < a1:
        segs.append((cur, a1))
    return segs


def draw_plan(sh, base_only=False):
    # tente camere
    for rid, name, pts, dims, obs in ROOMS:
        fill_poly_cm(sh, pts, TINT[rid])
    # balcon
    for r in [(355, -130, 365, 0), (715, -130, 725, 0), (355, -130, 725, -120)]:
        fill_poly_cm(sh, [(r[0], r[1]), (r[2], r[1]), (r[2], r[3]), (r[0], r[3])], (0.72, 0.74, 0.76), INK, 0.4)
    fill_poly_cm(sh, [(365, -120), (715, -120), (715, 0), (365, 0)], (0.95, 0.95, 0.96))
    # pereti
    def wall_rect(x0, y0, x1, y1):
        fill_poly_cm(sh, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], WALL, WALL, 0.3)

    wall_rect(0, 0, 15, 570)
    for a, b in seg_gaps(0, 1108, [(168, 328), (375, 520), (525, 610), (823, 963)]):
        wall_rect(a, 0, b, 25)
    wall_rect(0, 555, 968, 570)
    for a, b in seg_gaps(25, 555, [(405, 495)]):
        wall_rect(355, a, 370, b)
    for a, b in seg_gaps(25, 555, [(395, 485)]):
        wall_rect(710, a, 725, b)
    for a, b in seg_gaps(15, 355, [(260, 350)]):
        wall_rect(a, 384.5, b, 392)
    for a, b in seg_gaps(392, 555, [(420, 490)]):
        wall_rect(245, a, 252.5, b)
    for a, b in seg_gaps(725, 1015, [(800, 880)]):
        wall_rect(a, 347, b, 354.5)
    for a, b in seg_gaps(25, 347, [(150, 220)]):
        wall_rect(980, a, 987.5, b)
    for y0, y1 in [(0, 388), (478, 570)]:
        fill_poly_cm(sh, [(xo(y0), y0), (xo(y1), y1), (xi(y1), y1), (xi(y0), y0)], WALL, WALL, 0.3)
    # ferestre (simbol)
    for fid, loc, x0, x1, par, h in FEREASTRE:
        for yy in (7, 12.5, 18):
            sh.line(P(x0, yy), P(x1, yy), INK, 0.4)
        sh.line(P(x0, 0), P(x0, 25), INK, 0.5)
        sh.line(P(x1, 0), P(x1, 25), INK, 0.5)
    sh.line(P(525, 0), P(525, 25), INK, 0.5)
    sh.line(P(610, 0), P(610, 25), INK, 0.5)
    # usi: (hinge, closed, open)
    H7 = (xi(478), 478)
    C7 = (xi(388), 388)
    dx, dy = C7[0] - H7[0], C7[1] - H7[1]
    O7 = (H7[0] + dy, H7[1] - dx)
    doors = [
        ((350, 388.25), (260, 388.25), (350, 298.25)),
        ((248.75, 490), (248.75, 420), (318.75, 490)),
        ((362.5, 405), (362.5, 495), (452.5, 405)),
        ((717.5, 485), (717.5, 395), (627.5, 485)),
        ((880, 350.75), (800, 350.75), (880, 270.75)),  # U5: balama dreapta, se deschide spre frigider
        ((983.75, 220), (983.75, 150), (913.75, 220)),  # U6 debara: balama spre frigider, clanța spre masă
        (H7, C7, O7),
        ((525, 12.5), (610, 12.5), (525, 97.5)),
    ]
    for h, c, o in doors:
        sh.line(P(*h), P(*o), INK, 0.9)
        sh.poly([P(*p) for p in arc_pts(h, c, o)], color=MUT, width=0.4, close=False)
    if base_only:
        return
    # dotari
    sh.rect(*P(15, 392), *P(85, 555), fill=(1, 1, 1), color=INK, width=0.5)
    sh.rect(*P(22, 399), *P(78, 548), fill=None, color=MUT, width=0.35, radius=0.2)
    sh.circle(P(50, 540), 2.0, fill=None, color=MUT, width=0.4)
    sh.rect(*P(175, 440), *P(215, 462), fill=(1, 1, 1), color=INK, width=0.5)
    sh.rect(*P(178, 462), *P(212, 510), fill=(1, 1, 1), color=INK, width=0.5, radius=0.45)
    sh.rect(*P(110, 515), *P(160, 555), fill=(1, 1, 1), color=INK, width=0.5)
    sh.circle(P(135, 535), 7, fill=None, color=MUT, width=0.4)
    sh.rect(*P(725, 25), *P(785, 347), fill=None, color=INK, width=0.5)
    sh.rect(*P(727, 60), *P(783, 110), fill=None, color=MUT, width=0.35)  # chiuveta (orientativ)
    for cy in (230, 260):
        sh.circle(P(755, cy), 7, fill=None, color=MUT, width=0.4)
    # etichete camere
    labs = [
        ("DORMITOR", "dorm", 185, 255, 8), ("CAMERĂ DE ZI", "cz", 645, 300, 8),
        ("BUCĂTĂRIE", "kit", 840, 235, 7), ("HOL", "hol", 820, 505, 7),
        ("BAIE", "bath", 130, 458, 6.5), ("VESTIBUL", "vest", 304, 530, 5.6),
    ]
    for name, rid, cx, cy, sz in labs:
        x, y = P(cx, cy)
        sh.text(x, y, name, sz, True, INK, "c")
        sh.text(x, y + sz + 1.5, fmt2(AREA[rid]) + " m²", sz - 0.5, False, MUT, "c")
    x, y = P(1040, 150)
    sh.text(x, y, "NIȘĂ*", 5.2, True, MUT, "c", rot=90)
    x, y = P(460, -80)
    sh.text(x, y, "BALCON", 7, True, INK, "c")
    sh.text(x, y + 9, "370 × 130 cm", 6, False, MUT, "c")
    # etichete goluri
    for lab, (cx, cy) in {
        "F1": (248, -22), "F2": (447, -22), "U8": (567, -22), "F3": (893, -22),
        "U1": (320, 345), "U2": (282, 462), "U3": (402, 440), "U4": (682, 450),
        "U5": (838, 312), "U6": (950, 190), "U7": (935, 452),
    }.items():
        tag(sh, P(cx, cy), lab)
    # cote exterioare
    top0 = lambda c: P(0, -130)[1] if 355 <= c <= 725 else P(0, 0)[1]
    chain(sh, [0, 15, 168, 328, 355, 370, 375, 520, 525, 610, 710, 725, 823, 963, 1115],
          lambda c: P(c, 0)[0], "h", P(0, -150)[1], top0)
    chain(sh, [0, 15, 355, 370, 710, 725, 980, 987.5, 1115], lambda c: P(c, 0)[0], "h", P(0, -175)[1], top0,
          labels=["15", "340", "15", "340", "15", "255", "7,5", "127,5"])
    chain(sh, [0, 1115], lambda c: P(c, 0)[0], "h", P(0, -200)[1], top0, labels=["1115"])
    chain(sh, [-130, 0], lambda c: P(0, c)[1], "v", P(745, 0)[0], P(725, 0)[0], labels=["130"])
    bot = P(0, 570)[1]
    chain(sh, [0, 15, 245, 252.5, 355, 370, 710, 725, 956.4, 968], lambda c: P(c, 0)[0], "h", P(0, 628)[1], bot,
          labels=["15", "230", "7,5", "102,5", "15", "340", "15", "231", "11,5"])
    chain(sh, [0, 968], lambda c: P(c, 0)[0], "h", P(0, 650)[1], bot, labels=["968"])
    lx = P(0, 0)[0]
    chain(sh, [0, 25, 384.5, 392, 555, 570], lambda c: P(0, c)[1], "v", P(-35, 0)[0], lx,
          labels=["25", "359,5", "7,5", "163", "15"])
    chain(sh, [0, 570], lambda c: P(0, c)[1], "v", P(-60, 0)[0], lx, labels=["570"])
    # cote interioare
    chain(sh, [15, 355], lambda c: P(c, 0)[0], "h", P(0, 120)[1], None, labels=["340"])
    chain(sh, [25, 384.5], lambda c: P(0, c)[1], "v", P(40, 0)[0], None, labels=["359,5"])
    chain(sh, [370, 710], lambda c: P(c, 0)[0], "h", P(0, 520)[1], None, labels=["340"])
    chain(sh, [25, 555], lambda c: P(0, c)[1], "v", P(490, 0)[0], None, labels=["529,5"])
    chain(sh, [725, 980], lambda c: P(c, 0)[0], "h", P(0, 60)[1], None, labels=["255"])
    chain(sh, [25, 347], lambda c: P(0, c)[1], "v", P(895, 0)[0], None, labels=["322"])
    chain(sh, [354.5, 555], lambda c: P(0, c)[1], "v", P(745, 0)[0], None, labels=["200"])
    chain(sh, [15, 245], lambda c: P(c, 0)[0], "h", P(0, 410)[1], None, labels=["230"])
    chain(sh, [392, 555], lambda c: P(0, c)[1], "v", P(97, 0)[0], None, labels=["163"])
    chain(sh, [252.5, 355], lambda c: P(c, 0)[0], "h", P(0, 405)[1], None, labels=["102,5"])
    # trasee sectiuni
    dd = "[7 2 1.5 2] 0"
    xa0, xa1 = P(-14, 200)[0], P(xo(200) + 16, 200)[0]
    ya = P(0, 200)[1]
    sh.line((xa0, ya), (xa1, ya), RED, 0.7, dd)
    for xx in (xa0, xa1):
        sh.line((xx, ya), (xx, ya - 22), RED, 0.9)
        sh.poly([(xx, ya - 26), (xx - 2.6, ya - 19), (xx + 2.6, ya - 19)], fill=RED, color=RED, width=0.2)
    sh.circle((xa0 - 9, ya), 6.2, fill=(1, 1, 1), color=RED, width=0.8)
    sh.text(xa0 - 9, ya + 2.5, "A", 7.5, True, RED, "c")
    sh.circle((xa1 + 9, ya), 6.2, fill=(1, 1, 1), color=RED, width=0.8)
    sh.text(xa1 + 9, ya + 2.5, "A", 7.5, True, RED, "c")
    xb = P(560, 0)[0]
    yb0, yb1 = P(0, -118)[1], P(0, 586)[1]
    sh.line((xb, yb0), (xb, yb1), RED, 0.7, dd)
    for yy in (yb0, yb1):
        sh.line((xb, yy), (xb - 22, yy), RED, 0.9)
        sh.poly([(xb - 26, yy), (xb - 19, yy - 2.6), (xb - 19, yy + 2.6)], fill=RED, color=RED, width=0.2)
    sh.circle((xb, yb0 - 9), 6.2, fill=(1, 1, 1), color=RED, width=0.8)
    sh.text(xb, yb0 - 6.5, "B", 7.5, True, RED, "c")
    sh.circle((xb, yb1 + 9), 6.2, fill=(1, 1, 1), color=RED, width=0.8)
    sh.text(xb, yb1 + 11.5, "B", 7.5, True, RED, "c")


def table(sh, x, y, cols, header, rows, size=7.5, rowh=16.0, aligns=None, bold_last=False):
    aligns = aligns or ["l"] * len(cols)
    tw = sum(cols)
    sh.rect(x, y, x + tw, y + rowh, fill=ACC, color=ACC, width=0.3)
    cx = x
    for i, h in enumerate(header):
        tx = cx + 5 if aligns[i] == "l" else (cx + cols[i] / 2 if aligns[i] == "c" else cx + cols[i] - 5)
        sh.text(tx, y + rowh - 5, h, size, True, (1, 1, 1), aligns[i])
        cx += cols[i]
    for r, row in enumerate(rows):
        yy = y + rowh * (r + 1)
        if r % 2 == 1:
            sh.rect(x, yy, x + tw, yy + rowh, fill=(0.95, 0.96, 0.97), color=None, width=0)
        sh.line((x, yy + rowh), (x + tw, yy + rowh), (0.8, 0.82, 0.84), 0.3)
        cx = x
        last = bold_last and r == len(rows) - 1
        for i, cell in enumerate(row):
            s = size
            f = fb if last else fr
            while f.text_length(cell, fontsize=s) > cols[i] - 8 and s > 5:
                s -= 0.3
            tx = cx + 5 if aligns[i] == "l" else (cx + cols[i] / 2 if aligns[i] == "c" else cx + cols[i] - 5)
            sh.text(tx, yy + rowh - 5, cell, s, last, INK, aligns[i])
            cx += cols[i]
    sh.line((x, y + rowh * (len(rows) + 1)), (x + tw, y + rowh * (len(rows) + 1)), INK, 0.6)
    return y + rowh * (len(rows) + 1)


# ------------------------------------------------------------------ main
doc = fitz.open()
N = 4

# ============ 1: plan
sh = Sheet(doc)
frame(sh, "Plan apartament – cotat", "Apartament nr. 184, Bloc L14 – plan etaj curent, cote în cm", "1 : 50", 1, N)
draw_plan(sh)

# legenda + date generale (dreapta)
lx0 = 830
sh.text(lx0, 110, "DATE GENERALE", 8, True, ACC)
sh.line((lx0, 114), (1150, 114), ACC, 0.5)
rows = [
    ("Înălțime liberă", "2,50 m"),
    ("Suprafață locuibilă (dormitor + cameră de zi)", fmt2(LOCUIBILA) + " m²"),
    ("Suprafață utilă interioară (fără nișă și balcon)", fmt2(UTILA) + " m²"),
    ("Nișă tehnică*", fmt2(AREA["nisa"]) + " m²"),
    ("Balcon", fmt2(BALCON) + " m²"),
    ("Arie construită aprox. (cu pereți, fără balcon)", fmt2(FOOTPRINT) + " m²"),
    ("Ferestre / uși", "%d / %d" % (len(FEREASTRE), len(USI))),
]
yy = 130
for k, v in rows:
    sh.text(lx0, yy, k, 7.2, False, INK)
    w = fb.text_length(v, fontsize=7.6)
    sh.text(1150 - w, yy, v, 7.6, True, INK)
    sh.line((lx0, yy + 3.5), (1150, yy + 3.5), (0.85, 0.86, 0.88), 0.3)
    yy += 15.5

sh.text(lx0, 270, "LEGENDĂ", 8, True, ACC)
sh.line((lx0, 274), (1150, 274), ACC, 0.5)
sh.rect(lx0, 284, lx0 + 22, 293, fill=WALL, color=WALL, width=0.3)
sh.text(lx0 + 30, 292, "Pereți (25 / 15 / 7,5 cm) – conform releveu", 7.2)
tag(sh, (lx0 + 11, 310), "F1")
sh.text(lx0 + 30, 313, "Ferestre F1–F3, uși U1–U8 (vezi tabelul de goluri, pl. 3)", 7.2)
sh.line((lx0, 328), (lx0 + 22, 328), ACC, 0.4)
sh.line((lx0 + 3, 331), (lx0 + 8, 325), ACC, 0.7)
sh.line((lx0 + 14, 331), (lx0 + 19, 325), ACC, 0.7)
sh.text(lx0 + 30, 331, "Cote în centimetri", 7.2)
sh.line((lx0, 346), (lx0 + 22, 346), RED, 0.7, "[7 2 1.5 2] 0")
sh.text(lx0 + 30, 349, "Trasee secțiuni A-A și B-B (pl. 2 și 3)", 7.2)
sh.line((lx0, 364), (lx0 + 22, 364), INK, 0.9)
sh.text(lx0 + 30, 367, "Canat ușă deschis la 90° și arc de rotire", 7.2)
sh.text(lx0, 392, "* Cote și elemente deduse / de confirmat: nișa tehnică din dreapta", 6.6, False, MUT)
sh.text(lx0, 402, "bucătăriei, poziția sanitarelor și a blatului de bucătărie, grosimea", 6.6, False, MUT)
sh.text(lx0, 412, "planșeului (15 cm). Peretele oblic al holului este preluat din releveu.", 6.6, False, MUT)

# tabel incaperi (sub plan)
ty = P(0, 650)[1] + 16
tr = []
for i, (rid, name, pts, dims, obs) in enumerate(ROOMS):
    tr.append([str(i + 1), name, dims, fmt2(AREA[rid]), fmt2(PERIM[rid]),
               fmt2(AREA[rid] * 2.5)])
tr.append(["", "Total încăperi (fără nișă)", "", fmt2(UTILA), "", fmt2(UTILA * 2.5)])
table(sh, 150, ty, [26, 150, 140, 80, 80, 80], ["Nr.", "Încăpere", "Dimensiuni interioare (cm)", "S (m²)", "P (m)", "V (m³)"],
      tr, size=7.2, rowh=14.5, aligns=["c", "l", "l", "r", "r", "r"], bold_last=True)

# ============ 2: fatada + sectiune A-A
sh = Sheet(doc)
frame(sh, "Fațadă principală și secțiune A-A", "Apartament nr. 184, Bloc L14 – fațada dinspre balcon (vedere din exterior) și secțiune longitudinală", "1 : 50", 2, N)

# --- fatada
EXm = 130.0
EB = 255.0


def tx_f(x):
    return EXm + (1115 - x) * S


def tz_f(z):
    return EB - z * S


sh.text(EXm, 100, "FAȚADĂ PRINCIPALĂ (vedere din exterior, dinspre balcon)", 8.5, True, ACC)
sh.rect(tx_f(1115), tz_f(0), tx_f(0), tz_f(HEIGHT), fill=(0.93, 0.93, 0.92), color=INK, width=0.8)
sh.rect(tx_f(1115), tz_f(0), tx_f(0), tz_f(-SLAB), fill=(0.55, 0.56, 0.58), color=INK, width=0.6)
for fid, loc, x0, x1, par, h in FEREASTRE:
    sh.rect(tx_f(x1), tz_f(par + h), tx_f(x0), tz_f(par), fill=(0.80, 0.90, 0.96), color=INK, width=0.8)
    sh.line((tx_f((x0 + x1) / 2), tz_f(par + h)), (tx_f((x0 + x1) / 2), tz_f(par)), INK, 0.5)
    sh.text((tx_f(x0) + tx_f(x1)) / 2, tz_f(par + h / 2) + 2, fid, 7, True, ACC, "c")
sh.rect(tx_f(610), tz_f(220), tx_f(525), tz_f(0), fill=(0.80, 0.90, 0.96), color=INK, width=0.8)
sh.line((tx_f(567.5), tz_f(220)), (tx_f(567.5), tz_f(0)), INK, 0.5)
sh.text(tx_f(567.5), tz_f(150), "U8", 7, True, ACC, "c")
# balcon in fata
sh.rect(tx_f(725), tz_f(0), tx_f(355), tz_f(-SLAB), fill=(0.62, 0.63, 0.65), color=INK, width=0.7)
sh.rect(tx_f(725), tz_f(100), tx_f(355), tz_f(0), fill=(0.84, 0.85, 0.86), color=INK, width=0.8)
sh.text((tx_f(725) + tx_f(355)) / 2, tz_f(50) + 2, "parapet balcon h = 100", 6.5, False, MUT, "c")
# niveluri
for z, lab in [(0, "±0,00"), (HEIGHT, "+2,50")]:
    sh.line((tx_f(1115) - 18, tz_f(z)), (tx_f(0) + 12, tz_f(z)), MUT, 0.4, "[4 2] 0")
    sh.poly([(tx_f(1115) - 14, tz_f(z)), (tx_f(1115) - 9, tz_f(z) - 4), (tx_f(1115) - 4, tz_f(z))], fill=INK, color=INK, width=0.3)
    sh.text(tx_f(1115) - 20, tz_f(z) - 2, lab, 6.5, True, INK, "r")
sh.text(tx_f(1115) - 20, tz_f(-SLAB) + 7, "-0,15 (planșeu*)", 6.2, False, MUT, "r")
chain(sh, [0, 15, 168, 328, 355, 370, 375, 520, 525, 610, 710, 725, 823, 963, 1115], tx_f, "h", tz_f(-SLAB) + 22, tz_f(-SLAB))
chain(sh, [0, 1115], tx_f, "h", tz_f(-SLAB) + 38, tz_f(-SLAB), labels=["1115"])
chain(sh, [0, 90, 240, 250], lambda z: tz_f(z), "v", tx_f(0) + 18, tx_f(0), labels=["90", "150", "10"])
chain(sh, [0, 250], lambda z: tz_f(z), "v", tx_f(0) + 34, tx_f(0), labels=["250"])
chain(sh, [0, 100], lambda z: tz_f(z), "v", tx_f(355) - 12, tx_f(355), labels=["100"])

# --- sectiune A-A
AX = 90.0
AB = 500.0


def tx_a(x):
    return AX + x * S


def tz_a(z):
    return AB - z * S


sh.text(AX, 330, "SECȚIUNE A-A (la y = 200 cm, privind spre fațadă)", 8.5, True, ACC)
XW = xo(200)
sh.rect(tx_a(0), tz_a(0), tx_a(XW), tz_a(-SLAB), fill=WALL, color=WALL, width=0.3)
sh.rect(tx_a(0), tz_a(HEIGHT + SLAB), tx_a(XW), tz_a(HEIGHT), fill=WALL, color=WALL, width=0.3)
# fata interioara a fatadei (dincolo de plan)
for a, b in [(15, 355), (370, 710), (725, 980), (987.5, xi(200))]:
    sh.rect(tx_a(a), tz_a(HEIGHT), tx_a(b), tz_a(0), fill=(0.94, 0.94, 0.93), color=None, width=0)
for fid, loc, x0, x1, par, h in FEREASTRE:
    sh.rect(tx_a(x0), tz_a(par + h), tx_a(x1), tz_a(par), fill=(0.80, 0.90, 0.96), color=INK, width=0.7)
    sh.text((tx_a(x0) + tx_a(x1)) / 2, tz_a(par + h / 2) + 2, fid, 7, True, ACC, "c")
sh.rect(tx_a(525), tz_a(220), tx_a(610), tz_a(0), fill=(0.80, 0.90, 0.96), color=INK, width=0.7)
sh.text(tx_a(567.5), tz_a(110) + 2, "U8", 7, True, ACC, "c")
# pereti taiati
for a, b, z0, z1 in [(0, 15, 0, HEIGHT), (355, 370, 0, HEIGHT), (710, 725, 0, HEIGHT),
                     (980, 987.5, 210, HEIGHT), (xi(200), xo(200), 0, HEIGHT)]:
    sh.rect(tx_a(a), tz_a(z1), tx_a(b), tz_a(z0), fill=WALL, color=WALL, width=0.3)
sh.text(tx_a(983.75) - 4, tz_a(100), "U6", 6.5, True, ACC, "c", rot=90)
sh.rect(tx_a(725), tz_a(85), tx_a(785), tz_a(0), fill=(0.78, 0.62, 0.45), color=INK, width=0.5)
sh.text(tx_a(755), tz_a(40) + 2, "blat", 6, False, INK, "c")
# nume incaperi
for nm, cx in [("DORMITOR", 185), ("CAMERĂ DE ZI", 540), ("BUCĂTĂRIE", 852), ("NIȘĂ*", 1018)]:
    sh.text(tx_a(cx), tz_a(HEIGHT + SLAB) - 5, nm, 7.2, True, MUT, "c")
for z, lab in [(0, "±0,00"), (HEIGHT, "+2,50"), (HEIGHT + SLAB, "+2,65*")]:
    sh.line((tx_a(0) - 22, tz_a(z)), (tx_a(0), tz_a(z)), MUT, 0.4, "[4 2] 0")
    sh.text(tx_a(0) - 24, tz_a(z) - 2, lab, 6.5, True, INK, "r")
chain(sh, [0, 15, 355, 370, 710, 725, 980, 987.5, xi(200), XW], tx_a, "h", tz_a(-SLAB) + 22, tz_a(-SLAB),
      labels=["15", "340", "15", "340", "15", "255", "7,5", "60,4*", "15,5*"])
chain(sh, [0, XW], tx_a, "h", tz_a(-SLAB) + 38, tz_a(-SLAB), labels=[fmt(round(XW, 1)) + "*"])
chain(sh, [-SLAB, 0, HEIGHT, HEIGHT + SLAB], lambda z: tz_a(z), "v", tx_a(XW) + 20, tx_a(XW),
      labels=["15*", "250", "15*"])
chain(sh, [0, 90, 240, 250], lambda z: tz_a(z), "v", tx_a(XW) + 36, tx_a(XW), labels=["90", "150", "10"])

# ============ 3: sectiune B-B + goluri
sh = Sheet(doc)
frame(sh, "Secțiune B-B, tabel goluri și note", "Apartament nr. 184, Bloc L14 – secțiune transversală prin camera de zi și balcon, situația golurilor", "1 : 50", 3, N)
BX = 90.0
BB = 330.0


def ty_b(y):
    return BX + (570 - y) * S


def tz_b(z):
    return BB - z * S


sh.text(BX, 100, "SECȚIUNE B-B (la x = 560 cm, privind spre dormitor)", 8.5, True, ACC)
sh.rect(ty_b(570), tz_b(0), ty_b(-130), tz_b(-SLAB), fill=WALL, color=WALL, width=0.3)
sh.rect(ty_b(570), tz_b(HEIGHT + SLAB), ty_b(0), tz_b(HEIGHT), fill=WALL, color=WALL, width=0.3)
sh.rect(ty_b(555), tz_b(HEIGHT), ty_b(25), tz_b(0), fill=(0.94, 0.94, 0.93), color=None, width=0)
sh.rect(ty_b(495), tz_b(210), ty_b(405), tz_b(0), fill=(1, 1, 1), color=INK, width=0.6, dash="[3 2] 0")
sh.text((ty_b(495) + ty_b(405)) / 2, tz_b(105) + 2, "U3 90/210", 6.2, True, ACC, "c")
sh.text(ty_b(290), tz_b(HEIGHT + SLAB) - 5, "CAMERĂ DE ZI (față interioară a peretelui dormitor | cameră de zi)", 6.8, True, MUT, "c")
for a, b, z0, z1 in [(555, 570, 0, HEIGHT), (0, 25, 220, HEIGHT), (-130, -120, 0, 100)]:
    sh.rect(ty_b(a), tz_b(z1), ty_b(b), tz_b(z0), fill=WALL, color=WALL, width=0.3)
sh.text(ty_b(12.5) - 4, tz_b(110), "U8 85/220", 6.2, True, ACC, "c", rot=90)
sh.text(ty_b(-60), tz_b(50), "balcon", 6.5, False, MUT, "c")
for z, lab in [(0, "±0,00"), (HEIGHT, "+2,50")]:
    sh.line((ty_b(570) - 4, tz_b(z)), (ty_b(570) - 24, tz_b(z)), MUT, 0.4, "[4 2] 0")
    sh.text(ty_b(570) - 26, tz_b(z) - 2, lab, 6.5, True, INK, "r")
chain(sh, [570, 555, 25, 0, -120, -130], lambda y: ty_b(y), "h", tz_b(-SLAB) + 22, tz_b(-SLAB),
      labels=["15", "529,5", "25", "120", "10"])
chain(sh, [570, 0, -130], lambda y: ty_b(y), "h", tz_b(-SLAB) + 38, tz_b(-SLAB), labels=["570", "130"])
chain(sh, [0, 100], lambda z: tz_b(z), "v", ty_b(-130) + 16, ty_b(-130), labels=["100"])
chain(sh, [0, 220, 250], lambda z: tz_b(z), "v", ty_b(0) + 18, ty_b(0), labels=["220", "30"])
chain(sh, [0, 250], lambda z: tz_b(z), "v", ty_b(0) + 34, ty_b(0), labels=["250"])

# tabel goluri
tx0 = 600
sh.text(tx0, 100, "SITUAȚIA GOLURILOR", 8.5, True, ACC)
gr = []
for fid, loc, x0, x1, par, h in FEREASTRE:
    gr.append([fid, "Fereastră", loc, "%d × %d" % (x1 - x0, h), str(par) + "*", "%d" % (par + h) + "*"])
for uid, loc, wd, h in USI:
    gr.append([uid, "Ușă balcon" if uid == "U8" else "Ușă", loc, "%d × %d" % (wd, h), "0", "%d" % h])
table(sh, tx0, 108, [34, 86, 190, 80, 76, 74], ["ID", "Tip", "Amplasare", "Lățime × H (cm)", "Parapet (cm)", "Nivel sus (cm)"],
      gr, size=7.4, rowh=16, aligns=["c", "l", "l", "c", "c", "c"])

sh.text(tx0, 318, "ELEMENTE DE ÎNCHIDERE ȘI COMPARTIMENTARE", 8.5, True, ACC)
er = [
    ["Perete de fațadă (cu ferestre)", "25 cm", "plan releveu"],
    ["Pereți exteriori laterali și spate", "15 cm", "plan releveu"],
    ["Pereți între camere (dormitor | zi | bucătărie)", "15 cm", "plan releveu"],
    ["Pereți ușori (baie, vestibul, hol, nișă)", "7,5 cm", "plan releveu"],
    ["Montanți / piloni de fațadă", "30 cm", "indicat pe plan"],
    ["Perete oblic spre casa scării", "≈ 15,5 cm", "dedus din cote*"],
    ["Planșeu", "15 cm", "ipoteză*"],
]
table(sh, tx0, 326, [280, 90, 170], ["Element", "Grosime", "Sursă"], er, size=7.4, rowh=16, aligns=["l", "c", "l"])

sh.text(tx0, 480, "NOTE ȘI IPOTEZE", 8.5, True, ACC)
notes = [
    "1. Înălțimea liberă a încăperilor este 2,50 m (confirmată de beneficiar).",
    "2. Cotele sunt cele de pe releveul original (cm). Cotele marcate cu * sunt deduse, calculate",
    "    sau ipoteze și trebuie verificate pe teren înainte de orice lucrare.",
    "3. Suprafața locuibilă de 30,22 m² din releveu = dormitor 12,22 + cameră de zi 18,00 m².",
    "4. Parapetul ferestrelor (90 cm) și grosimea planșeului (15 cm) nu sunt cotate în releveu.",
    "5. La parter nu există balcon, ci o fereastră de 230/150 doar pentru ap. 178 (mențiune din",
    "    releveu); aici este reprezentat apartamentul de etaj, cu balcon.",
    "6. Nișa tehnică din dreapta bucătăriei, sanitarele, blatul de bucătărie și golul de 102,5/210",
    "    de lângă baie sunt reprezentate orientativ sau nu sunt modelate.",
    "7. Modelul 3D (FreeCAD) este în fișierele apartament_184.FCStd și apartament_184.step.",
]
yy = 496
for ln in notes:
    sh.text(tx0, yy, ln, 7.3, False, INK)
    yy += 12.5

# ============ 4: vederi 3D
sh = Sheet(doc)
frame(sh, "Vederi 3D ale modelului", "Apartament nr. 184, Bloc L14 – model FreeCAD, înălțime liberă 2,50 m (planșeu superior neafișat)", "fără scară", 4, N)
sh.rect(40, 96, 600, 700, fill=(0.12, 0.12, 0.12), color=None, width=0, radius=0.02)
sh.rect(620, 96, 1150, 700, fill=(0.12, 0.12, 0.12), color=None, width=0, radius=0.02)
try:
    sh.pg.insert_image(fitz.Rect(52, 150, 588, 670), filename=r"C:\Users\Public\apt184\iso_hi_c.png", keep_proportion=True)
    sh.pg.insert_image(fitz.Rect(632, 150, 1138, 670), filename=r"C:\Users\Public\apt184\top_hi_c.png", keep_proportion=True)
except Exception as e:
    print("imagini:", e)
sh.text(56, 118, "VEDERE IZOMETRICĂ", 8.5, True, (1, 1, 1))
sh.text(56, 132, "Pereți, goluri de uși și ferestre, pardoseli pe camere, balcon, dotări", 7, False, (0.75, 0.75, 0.75))
sh.text(636, 118, "VEDERE DE SUS, CU ETICHETE PE CAMERE", 8.5, True, (1, 1, 1))
sh.text(636, 132, "Etichetele (nume cameră și suprafață) sunt obiecte text în modelul FreeCAD", 7, False, (0.75, 0.75, 0.75))
sh.text(56, 690, "Culori pardoseli: dormitor – albastru, cameră de zi – crem, bucătărie – somon, hol – mov, baie – turcoaz, vestibul – verzui, nișă – gri.",
        7, False, (0.75, 0.75, 0.75))

doc.save(OUT, garbage=3, deflate=True)
print("salvat", OUT, "pagini:", len(doc))
print("Arii (m2):", {k: round(v, 2) for k, v in AREA.items()}, "locuibila", round(LOCUIBILA, 2),
      "utila", round(UTILA, 2), "constr", round(FOOTPRINT, 2), "balcon", round(BALCON, 2))

