import sys
import os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_pdf.py"), encoding="utf-8-sig").read()
exec(src.split("# ------------------------------------------------------------------ main")[0])

OUT = sys.argv[1] if len(sys.argv) > 1 else "Apartament_184_plan_mobilare.pdf"

C_WOOD = (0.96, 0.93, 0.86)
C_SOFT = (0.90, 0.91, 0.95)
C_APP = (0.88, 0.92, 0.96)
C_SAN = (1.0, 1.0, 1.0)
C_KIT = (0.93, 0.90, 0.84)

# nr, incapere, element, forma, dimensiuni, buc, recomandare, buget (min, max) lei
ITEMS = [
    (1, "Dormitor", "Pat tapițat cu ladă depozitare", "160 × 200", 1, "tăblia pe peretele de vest; 80 cm liber la picior", (1500, 3000)),
    (2, "Dormitor", "Saltea", "160 × 200", 1, "spumă / arcuri împachetate, fermitate medie", (1500, 3000)),
    (3, "Dormitor", "Noptiere", "40 × 40", 2, "cu sertar; prize + USB deasupra", (300, 800)),
    (4, "Dormitor", "Dulap cu uși glisante", "220 × 60 × 236", 1, "uși glisante (nu deschid peste pat), oglindă pe o ușă", (2500, 5000)),
    (5, "Dormitor", "Birou compact + scaun", "110 × 50", 1, "sub fereastră, lumină naturală", (600, 1200)),
    (6, "Cameră de zi", "Canapea extensibilă 3 locuri", "220 × 95", 1, "extensibilă = loc de dormit pt. 2 oaspeți", (2500, 5000)),
    (7, "Cameră de zi", "Comodă TV + TV 55\" pe perete", "160 × 40", 1, "TV pe suport de perete, cabluri prin tub", (2300, 4500)),
    (8, "Cameră de zi", "Măsuță de cafea", "100 × 55", 1, "colțuri rotunjite", (200, 600)),
    (9, "Cameră de zi", "Masă extensibilă + 2 scaune", "120(160) × 75", 1, "lângă fereastră; se extinde pt. 4 persoane", (800, 1800)),
    (10, "Cameră de zi", "Corp depozitare / bibliotecă joasă", "300 × 40 × 90", 1, "pe peretele dinspre hol; trecerea U3–U4 rămâne liberă", (900, 2000)),
    (11, "Bucătărie", "Mobilier bucătărie în L (corpuri jos + sus, blat)", "≈ 2,6 + 1,95 ml", 1, "corpuri sus până la tavan; blat compact HPL", (8000, 15000)),
    (12, "Bucătărie", "Frigider combină", "60 × 65 × 185", 1, "lângă ușă (zona de descărcare)", (2000, 3500)),
    (13, "Bucătărie", "Plită inducție 60 + cuptor + hotă", "60", 1, "verificați puterea aprobată (vezi nota)", (3000, 6000)),
    (14, "Bucătărie", "Chiuvetă + baterie + mașină spălat vase 45", "45 / 80", 1, "chiuveta sub fereastră", (2200, 4000)),
    (15, "Bucătărie", "Blat bar rabatabil + 2 scaune bar", "100 × 40", 1, "mic dejun; se pliază", (400, 900)),
    (16, "Nișă", "Rafturi cămară", "100 × 30", 1, "dacă nișa nu are rol tehnic", (150, 400)),
    (17, "Hol", "Dulap hol (haine + pantofi)", "160 × 60 × 236", 1, "uși glisante sau batante 40 cm", (1500, 3000)),
    (18, "Hol", "Cuier + oglindă pe perete", "≈ 90", 1, "montate pe peretele bucătăriei", (200, 500)),
    (19, "Baie", "Duș walk-in, sifon liniar, perete sticlă", "90 × 100", 1, "în locul căzii; pantă 1,5–2% spre sifon", (3000, 6000)),
    (20, "Baie", "Mașină de spălat rufe", "60 × 60", 1, "slim 45 cm dacă se dorește mai mult spațiu", (1500, 2500)),
    (21, "Baie", "Lavoar cu mobilier + oglindă", "60 × 45", 1, "oglindă cu iluminare LED", (800, 1800)),
    (22, "Baie", "WC suspendat + cadru încastrat", "36 × 53", 1, "poziție lângă coloana existentă*", (1500, 3000)),
    (23, "Baie", "Calorifer port-prosop", "50 × 80", 1, "lângă ușă", (300, 800)),
    (24, "Balcon", "Set bistro (masă + 2 scaune)", "Ø 60", 1, "pliabil, pentru exterior", (300, 700)),
]
BMIN = sum(i[6][0] for i in ITEMS)
BMAX = sum(i[6][1] for i in ITEMS)


def r(sh, x0, y0, x1, y1, fill=C_WOOD, w=0.6, radius=None, dash=None):
    a, b = P(x0, y0), P(x1, y1)
    sh.rect(a[0], a[1], b[0], b[1], fill=fill, color=INK, width=w, radius=radius, dash=dash)


def c(sh, cx, cy, rr, fill=C_WOOD, w=0.6):
    sh.circle(P(cx, cy), rr * S, fill=fill, color=INK, width=w)


def num(sh, cx, cy, n):
    p = P(cx, cy)
    sh.circle(p, 6.0, fill=(1, 1, 1), color=(0.80, 0.33, 0.10), width=0.8)
    sh.text(p[0], p[1] + 2.0, str(n), 6.0, True, (0.80, 0.33, 0.10), "c")


def furniture(sh):
    # ---- dormitor
    r(sh, 15, 125, 215, 285, C_SOFT)
    r(sh, 20, 135, 52, 200, (1, 1, 1), 0.4, 0.3)
    r(sh, 20, 210, 52, 275, (1, 1, 1), 0.4, 0.3)
    sh.line(P(90, 125), P(90, 285), MUT, 0.4)
    r(sh, 15, 80, 55, 120)
    r(sh, 15, 290, 55, 330)
    r(sh, 295, 30, 355, 250)
    sh.line(P(322, 30), P(322, 140), MUT, 0.5)
    sh.line(P(328, 140), P(328, 250), MUT, 0.5)
    r(sh, 180, 25, 290, 75)
    c(sh, 235, 100, 20, C_SOFT)
    num(sh, 150, 205, 1); num(sh, 35, 100, 3); num(sh, 325, 195, 4); num(sh, 235, 50, 5)
    # ---- camera de zi
    r(sh, 615, 170, 710, 390, C_SOFT, 0.7, 0.08)
    r(sh, 630, 170, 710, 190, C_SOFT, 0.4)
    r(sh, 630, 370, 710, 390, C_SOFT, 0.4)
    sh.line(P(630, 190), P(630, 370), MUT, 0.4)
    r(sh, 370, 200, 410, 360)
    r(sh, 372, 215, 377, 345, INK, 0.3)  # TV
    r(sh, 480, 230, 535, 330, C_WOOD, 0.6, 0.15)
    r(sh, 390, 35, 510, 110)
    r(sh, 510, 35, 530, 110, None, 0.4, None, "[2 2] 0")  # extensie
    c(sh, 420, 135, 20, C_SOFT); c(sh, 480, 135, 20, C_SOFT)
    r(sh, 390, 515, 690, 555)
    for xx in (465, 540, 615):
        sh.line(P(xx, 515), P(xx, 555), MUT, 0.4)
    num(sh, 665, 280, 6); num(sh, 393, 280, 7); num(sh, 507, 280, 8); num(sh, 450, 72, 9); num(sh, 540, 535, 10)
    # zona de trecere U3-U4
    sh.rect(*P(372, 400), *P(708, 492), fill=None, color=(0.80, 0.33, 0.10), width=0.5, dash="[3 3] 0")
    x, y = P(540, 450)
    sh.text(x, y, "trecere liberă ≥ 90 cm", 6.0, False, (0.80, 0.33, 0.10), "c")
    # ---- bucatarie
    r(sh, 725, 25, 785, 285, C_KIT)
    r(sh, 785, 25, 980, 85, C_KIT)
    sh.line(P(725, 85), P(785, 85), MUT, 0.4)
    sh.line(P(725, 145), P(785, 145), MUT, 0.4)
    sh.line(P(725, 205), P(785, 205), MUT, 0.4)
    for cy in (160, 190):
        for cx in (742, 768):
            c(sh, cx, cy, 9, None, 0.4)
    r(sh, 727, 145, 783, 205, None, 0.4, None, "[2 2] 0")  # hota (proiectie)
    sh.line(P(830, 25), P(830, 85), MUT, 0.4)
    r(sh, 852, 32, 922, 78, (1, 1, 1), 0.5, 0.2)
    c(sh, 887, 55, 4, None, 0.4)
    r(sh, 725, 285, 790, 347, C_APP)
    sh.line(P(725, 285), P(790, 347), MUT, 0.3); sh.line(P(790, 285), P(725, 347), MUT, 0.3)
    r(sh, 940, 230, 980, 330)
    c(sh, 915, 255, 15, C_SOFT); c(sh, 915, 305, 15, C_SOFT)
    r(sh, 990, 28, 1085, 58, C_WOOD, 0.5)
    num(sh, 755, 110, 11); num(sh, 757, 316, 12); num(sh, 755, 240, 13); num(sh, 805, 55, 14); num(sh, 960, 280, 15); num(sh, 1035, 43, 16)
    # ---- hol
    r(sh, 735, 495, 895, 555)
    sh.line(P(815, 495), P(815, 555), MUT, 0.4)
    sh.line(P(895, 357), P(985, 357), (0.80, 0.33, 0.10), 1.6)
    num(sh, 815, 525, 17); num(sh, 940, 372, 18)
    # ---- baie
    r(sh, 15, 455, 105, 555, (0.92, 0.97, 0.98))
    sh.line(P(105, 455), P(105, 530), ACC, 1.2)
    sh.line(P(25, 545), P(95, 545), INK, 1.0)
    r(sh, 15, 392, 75, 452, C_APP)
    c(sh, 45, 422, 20, None, 0.4)
    r(sh, 120, 392, 180, 437, C_SAN)
    r(sh, 130, 398, 170, 430, None, 0.4, 0.4)
    r(sh, 145, 545, 195, 555, (0.85, 0.85, 0.85), 0.4)
    r(sh, 152, 492, 188, 545, C_SAN, 0.6, 0.45)
    r(sh, 238, 500, 245, 550, (0.85, 0.85, 0.85), 0.4)
    num(sh, 60, 505, 19); num(sh, 45, 422, 20); num(sh, 150, 455, 21); num(sh, 170, 515, 22); num(sh, 225, 525, 23)
    # ---- balcon
    c(sh, 640, -65, 30); c(sh, 595, -65, 18, C_SOFT); c(sh, 685, -65, 18, C_SOFT)
    num(sh, 640, -65, 24)


def room_labels(sh):
    labs = [("DORMITOR", "dorm", 120, 360), ("CAMERĂ DE ZI", "cz", 540, 395 - 210), ("BUCĂTĂRIE", "kit", 850, 140),
            ("HOL", "hol", 900, 470), ("BAIE", "bath", 200, 475), ("VESTIBUL", "vest", 304, 530)]
    for name, rid, cx, cy in labs:
        x, y = P(cx, cy)
        sz = 5.6 if rid in ("vest", "bath") else 7
        sh.text(x, y, name, sz, True, INK, "c")
        sh.text(x, y + sz + 1, fmt2(AREA[rid]) + " m²", sz - 0.6, False, MUT, "c")


doc = fitz.open()
N = 2
sh = Sheet(doc)
frame(sh, "Plan de mobilare – propunere", "Apartament nr. 184, Bloc L14 – amenajare modernă pentru închiriere (1–2 persoane), cote în cm", "1 : 50", 1, N)
draw_plan(sh, base_only=True)
furniture(sh)
room_labels(sh)
# cote principale (exterioare) pentru orientare
chain(sh, [0, 15, 355, 370, 710, 725, 980, 987.5, 1115], lambda v: P(v, 0)[0], "h", P(0, -160)[1],
      lambda v: P(0, -130)[1] if 355 <= v <= 725 else P(0, 0)[1],
      labels=["15", "340", "15", "340", "15", "255", "7,5", "127,5"])
chain(sh, [0, 25, 384.5, 392, 555, 570], lambda v: P(0, v)[1], "v", P(-35, 0)[0], P(0, 0)[0],
      labels=["25", "359,5", "7,5", "163", "15"])
# cote de amplasare mobilier (selecție)
OR = (0.80, 0.33, 0.10)
chain(sh, [215, 295], lambda v: P(v, 0)[0], "h", P(0, 300)[1], None, labels=["80"], color=OR)
chain(sh, [410, 480], lambda v: P(v, 0)[0], "h", P(0, 345)[1], None, labels=["70"], color=OR)
chain(sh, [535, 615], lambda v: P(v, 0)[0], "h", P(0, 345)[1], None, labels=["80"], color=OR)
chain(sh, [785, 940], lambda v: P(v, 0)[0], "h", P(0, 220)[1], None, labels=["155"], color=OR)
chain(sh, [437, 492], lambda v: P(0, v)[1], "v", P(140, 0)[0], None, labels=["55"], color=OR)
chain(sh, [354.5, 495], lambda v: P(0, v)[1], "v", P(760, 0)[0], None, labels=["140"], color=OR)

# coloana dreapta
lx0 = 830
sh.text(lx0, 110, "PRINCIPII DE AMENAJARE", 8, True, ACC)
sh.line((lx0, 114), (1150, 114), ACC, 0.5)
lines = [
    ("Structură", "Pereții de 15 și 25 cm sunt structurali (bloc din panouri) –"),
    ("", "nu se demolează și nu se lărgesc goluri. Doar pereții de 7,5 cm"),
    ("", "(baie, vestibul, nișă) pot fi modificați."),
    ("Cameră de zi", "Trei zone: masă lângă fereastră și balcon, zonă TV la mijloc,"),
    ("", "depozitare pe peretele dinspre hol. Trecerea dintre ușile"),
    ("", "U3 și U4 rămâne liberă."),
    ("Dormitor", "Pat 160×200 cu ladă, dulap glisant de 220 cm pe peretele"),
    ("", "interior, birou sub fereastră. 80 cm liber la piciorul patului."),
    ("Bucătărie", "În L, cu triunghiul frigider – chiuvetă – plită sub 5 m."),
    ("", "Corpurile de sus merg până la tavan (2,50 m)."),
    ("Baie", "Cada se înlocuiește cu duș walk-in 90×100 + loc pentru"),
    ("", "mașina de spălat. WC suspendat. Poziția coloanei de"),
    ("", "scurgere trebuie verificată pe teren*."),
    ("Hol", "Dulap 160×60 pentru haine și pantofi, cuier și oglindă."),
    ("Închiriere", "Culori neutre, mobilier rezistent la uzură, multă depozitare,"),
    ("", "canapea extensibilă pentru 2 persoane în plus."),
]
yy = 130
for k, v in lines:
    if k:
        sh.text(lx0, yy, k, 7.2, True, INK)
    sh.text(lx0 + 68, yy, v, 7.0, False, INK)
    yy += 12.5
yy += 8
sh.text(lx0, yy, "LEGENDĂ", 8, True, ACC)
sh.line((lx0, yy + 4), (1150, yy + 4), ACC, 0.5)
yy += 18
for fill, txt in [(C_WOOD, "Mobilier (lemn / PAL)"), (C_SOFT, "Tapițerie, pat, scaune"), (C_KIT, "Mobilier bucătărie"),
                  (C_APP, "Electrocasnice")]:
    sh.rect(lx0, yy - 7, lx0 + 20, yy + 1, fill=fill, color=INK, width=0.5)
    sh.text(lx0 + 28, yy, txt, 7.0)
    yy += 13
sh.circle((lx0 + 10, yy - 3), 6.0, fill=(1, 1, 1), color=OR, width=0.8)
sh.text(lx0 + 10, yy - 1, "1", 6, True, OR, "c")
sh.text(lx0 + 28, yy, "Număr element – vezi lista de mobilier (planșa 2)", 7.0)
yy += 14
sh.line((lx0, yy - 3), (lx0 + 20, yy - 3), OR, 0.5)
sh.text(lx0 + 28, yy, "Cote de amplasare / spații libere (cm)", 7.0)
yy += 22
sh.text(lx0, yy, "BUGET ORIENTATIV MOBILIER + ELECTROCASNICE", 8, True, ACC)
sh.line((lx0, yy + 4), (1150, yy + 4), ACC, 0.5)
yy += 22
sh.text(lx0, yy, "%s – %s lei" % (format(BMIN, ",").replace(",", "."), format(BMAX, ",").replace(",", ".")), 15, True, INK)
yy += 14
sh.text(lx0, yy, "Prețuri estimative 2026, gamă medie (IKEA / Dedeman / Jysk / eMAG).", 6.8, False, MUT)
yy += 10
sh.text(lx0, yy, "Nu include renovarea, instalațiile, corpurile de iluminat și textilele.", 6.8, False, MUT)

# ---- planșa 2: lista
sh = Sheet(doc)
frame(sh, "Listă mobilier și electrocasnice", "Apartament nr. 184, Bloc L14 – elementele numerotate din planul de mobilare, cu recomandări și buget orientativ", "–", 2, N)
rows = []
for n, room, name, dims, q, rec, (a, b) in ITEMS:
    rows.append([str(n), room, name, dims, str(q), rec, "%s – %s" % (format(a, ",").replace(",", "."), format(b, ",").replace(",", "."))])
rows.append(["", "", "TOTAL ORIENTATIV", "", "", "", "%s – %s" % (format(BMIN, ",").replace(",", "."), format(BMAX, ",").replace(",", "."))])
end = table(sh, 40, 96, [28, 80, 250, 96, 34, 400, 222],
            ["Nr.", "Încăpere", "Element", "Dimensiuni (cm)", "Buc.", "Recomandare / observații", "Buget orientativ (lei)"],
            rows, size=7.3, rowh=21.5, aligns=["c", "l", "l", "c", "c", "l", "r"], bold_last=True)
sh.text(40, end + 18, "* Poziția coloanelor de apă și canalizare din baie nu apare în releveu. Se verifică pe teren înainte de a fixa poziția WC-ului și a dușului.", 7.2, False, MUT)
sh.text(40, end + 30, "Plita cu inducție (7,4 kW) cere de obicei o putere aprobată mai mare decât branșamentul vechi de bloc. Verificați avizul de racordare sau alegeți o plită cu limitare de putere (3,5–4,6 kW).", 7.2, False, MUT)
sh.text(40, end + 42, "Prețurile sunt estimări orientative și trebuie verificate la momentul achiziției.", 7.2, False, MUT)

doc.save(OUT, garbage=3, deflate=True)
print("salvat", OUT, "buget", BMIN, BMAX)
