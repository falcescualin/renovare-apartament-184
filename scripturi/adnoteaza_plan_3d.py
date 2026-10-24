"""Adnoteaza vederea de sus (plan_3D_sus_baza.png): fundal hartie, umbra, axe, cote, incaperi, zone, circulatie.
Ruleaza: python adnoteaza_plan_3d.py"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os

BASE = r"C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14"
SRC = os.path.join(BASE, "randari", "plan_3D_sus_baza.png")
OUT = os.path.join(BASE, "randari", "Plan_3D_apartament_184.png")
W, H, ORTHO, CX, CY = 3200, 2200, 14.0, 5.575, -2.20          # identic cu plan_3d_sus.py
S = W / ORTHO
X0 = CX - ORTHO / 2
YT = CY + (H / W) * ORTHO / 2
PAD_T, PAD_B = 150, 260                                        # spatiu in plus pentru legenda si cartus

FR = r"C:\Windows\Fonts\segoeui.ttf"
FB = r"C:\Windows\Fonts\segoeuib.ttf"
f = lambda size, bold=False: ImageFont.truetype(FB if bold else FR, size)
INK, MUT, AX = (45, 47, 52), (110, 112, 118), (120, 122, 128)
ZONE = {"zi": (217, 115, 78), "noapte": (91, 127, 166), "servicii": (110, 158, 107), "circ": (60, 62, 66)}


def P(x_cm, y_cm):
    """coordonate din plan (cm, y in jos) -> pixeli pe planșa finala"""
    X, Y = x_cm / 100.0, -y_cm / 100.0
    return ((X - X0) * S, (YT - Y) * S + PAD_T)


base = Image.open(SRC).convert("RGBA")
canvas = Image.new("RGBA", (W, H + PAD_T + PAD_B), (243, 241, 237, 255))
# umbra moale sub macheta
alpha = base.split()[3]
sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
sh.putalpha(alpha.point(lambda a: int(a * 0.35)))
sh = sh.filter(ImageFilter.GaussianBlur(28))
canvas.alpha_composite(sh, (22, PAD_T + 30))
canvas.alpha_composite(base, (0, PAD_T))
d = ImageDraw.Draw(canvas)


def dashed(p0, p1, col, width=3, dash=18, gap=12):
    import math
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0)
    if L == 0:
        return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    t = 0.0
    while t < L:
        t2 = min(L, t + dash)
        d.line((x0 + ux * t, y0 + uy * t, x0 + ux * t2, y0 + uy * t2), fill=col, width=width)
        t += dash + gap


def text_c(xy, s, font, col=INK):
    w = d.textlength(s, font=font)
    d.text((xy[0] - w / 2, xy[1]), s, font=font, fill=col)


# ---- axe structurale (linii subtiri prelungite, cu cercuri si litere/cifre)
for lab, x in (("A", 7.5), ("B", 362.5), ("C", 717.5), ("D", 983.75)):
    xa = P(x, 0)[0]
    dashed((xa, P(0, -205)[1]), (xa, P(0, 650)[1]), AX, 2, 14, 10)
    for yy in (P(0, -225)[1], P(0, 670)[1]):
        d.ellipse((xa - 26, yy - 26, xa + 26, yy + 26), outline=AX, width=3, fill=(243, 241, 237))
        text_c((xa, yy - 19), lab, f(30, True), AX)
for lab, y in (("1", 12.5), ("2", 388.25), ("3", 562.5)):
    ya = P(0, y)[1]
    dashed((P(-60, 0)[0], ya), (P(1180, 0)[0], ya), AX, 2, 14, 10)
    for xx in (P(-82, 0)[0], P(1202, 0)[0]):
        d.ellipse((xx - 26, ya - 26, xx + 26, ya + 26), outline=AX, width=3, fill=(243, 241, 237))
        text_c((xx, ya - 19), lab, f(30, True), AX)


# ---- cote generale (cm)
def dim_h(x0, x1, y, label):
    a, b = P(x0, y), P(x1, y)
    d.line((a[0], a[1], b[0], b[1]), fill=INK, width=2)
    for p in (a, b):
        d.line((p[0] - 9, p[1] + 9, p[0] + 9, p[1] - 9), fill=INK, width=3)
        d.line((p[0], p[1] - 16, p[0], p[1] + 16), fill=INK, width=2)
    text_c(((a[0] + b[0]) / 2, a[1] - 40), label, f(28), INK)


def dim_v(y0, y1, x, label):
    a, b = P(x, y0), P(x, y1)
    d.line((a[0], a[1], b[0], b[1]), fill=INK, width=2)
    for p in (a, b):
        d.line((p[0] - 9, p[1] + 9, p[0] + 9, p[1] - 9), fill=INK, width=3)
        d.line((p[0] - 16, p[1], p[0] + 16, p[1]), fill=INK, width=2)
    tw = d.textlength(label, font=f(28))
    lay = Image.new("RGBA", (int(tw) + 8, 40), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((4, 2), label, font=f(28), fill=INK)
    lay = lay.rotate(90, expand=True)
    canvas.alpha_composite(lay, (int(a[0] - 52), int((a[1] + b[1]) / 2 - lay.size[1] / 2)))


dim_h(0, 1115, -175, "11,15 m")
dim_h(15, 355, -150, "3,40");
dim_h(370, 710, -150, "3,40")
dim_h(725, 980, -150, "2,55")
dim_v(0, 570, -40, "5,70 m")
dim_v(25, 384.5, -15, "3,595")

# ---- incaperi (card + punct de zona)
ROOMS = [
    ("CAMERĂ DE ZI", "18,00 m²", "zi", 665, 380), ("DORMITOR", "12,22 m²", "noapte", 230, 300),
    ("BUCĂTĂRIE", "8,21 m²", "zi", 835, 150), ("HOL", "5,16 m²", "servicii", 905, 412),
    ("BAIE", "3,75 m²", "servicii", 120, 410), ("VESTIBUL", "1,67 m²", "servicii", 304, 520),
    ("DEBARA", "2,06 m²", "servicii", 1045, 70), ("BALCON", "4,81 m²", "zi", 470, -65),
]
for name, area, zone, x, y in ROOMS:
    cx, cy = P(x, y)
    t1, t2 = f(30, True), f(26)
    w = max(d.textlength(name, font=t1), d.textlength(area, font=t2)) + 70
    box = (cx - w / 2, cy - 38, cx + w / 2, cy + 44)
    card = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle(box, radius=14, fill=(255, 255, 255, 215))
    canvas.alpha_composite(card)
    d = ImageDraw.Draw(canvas)
    d.ellipse((box[0] + 16, cy - 22, box[0] + 34, cy - 4), fill=ZONE[zone])
    d.text((box[0] + 44, cy - 34), name, font=t1, fill=INK)
    d.text((box[0] + 44, cy + 4), area, font=t2, fill=MUT)

# ---- circulatie de la intrare (linie punctata)
paths = [
    [(990, 455), (900, 458), (740, 450), (600, 445)],      # intrare -> hol -> camera de zi
    [(800, 452), (800, 352), (820, 260)],                  # hol -> bucatarie
    [(600, 440), (362, 450), (304, 450), (305, 388), (305, 330)],   # camera de zi -> vestibul -> dormitor
    [(304, 455), (248, 455), (190, 455)],                  # vestibul -> baie
    [(567, 380), (567, 12), (567, -55)],                   # camera de zi -> balcon
    [(840, 230), (983, 185), (1030, 160)],                 # bucatarie -> debara
]
for pts in paths:
    for a, b in zip(pts, pts[1:]):
        dashed(P(*a), P(*b), ZONE["circ"], 4, 16, 12)
ex, ey = P(1003, 455)
d.polygon([(ex + 30, ey), (ex + 6, ey - 16), (ex + 6, ey + 16)], fill=ZONE["circ"])
d.text((ex + 36, ey - 18), "INTRARE", font=f(26, True), fill=ZONE["circ"])

# ---- legenda zone (sus)
lx, ly = 120, 46
items = [("ZONA DE ZI", ZONE["zi"]), ("ZONA DE NOAPTE", ZONE["noapte"]), ("SERVICII", ZONE["servicii"])]
for lab, col in items:
    d.ellipse((lx, ly + 8, lx + 22, ly + 30), fill=col)
    d.text((lx + 34, ly), lab, font=f(28, True), fill=INK)
    lx += d.textlength(lab, font=f(28, True)) + 110
dashed((lx, ly + 19), (lx + 70, ly + 19), ZONE["circ"], 4, 14, 10)
d.text((lx + 86, ly), "CIRCULAȚIE", font=f(28, True), fill=INK)

# ---- cartus + scara grafica (jos)
yb = H + PAD_T + 40
d.line((120, yb, W - 120, yb), fill=(200, 198, 192), width=2)
d.text((120, yb + 30), "APARTAMENT 184 · BLOC L14", font=f(54, True), fill=INK)
d.text((120, yb + 100), "Plan 3D — vedere de sus, fără tavan, pereți la 2,50 m · suprafață utilă ≈ 49 m² + balcon 4,81 m²", font=f(30), fill=MUT)
sx, sy = W - 1060, yb + 70
for i in range(4):
    x0, x1 = sx + i * S, sx + (i + 1) * S
    d.rectangle((x0, sy, x1, sy + 18), fill=INK if i % 2 == 0 else (243, 241, 237), outline=INK, width=2)
    text_c((x0, sy + 28), str(i), f(24), MUT)
text_c((sx + 4 * S, sy + 28), "4 m", f(24), MUT)
d.text((sx, sy - 52), "SCARĂ GRAFICĂ", font=f(24, True), fill=MUT)

canvas.convert("RGB").save(OUT, quality=95)
print("SALVAT", OUT, canvas.size)
