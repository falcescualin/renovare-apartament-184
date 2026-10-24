"""Rulează în FreeCAD (document apartament_184 deschis)   (07.10.2026)
Canapea extensibilă 3 locuri Puma, Dedeman 8119379, crem, stofă: 215 × 76 × 87 cm (lungime × adâncime × înălțime), 1.599 lei.
Înlocuiește canapeaua veche (JYSK ILDVED 220, ascunsă, nu ștearsă). Spatele la peretele din est (x = 7100), același centru (y = −2800).
Forma după fotografia produsului: ladă de depozitare joasă, trei perne de șezut, spătar ușor înclinat cu caneluri verticale,
brațe late rotunjite, picioare de lemn la capete și patru picioare negre rotunde. Detaliile care nu sunt în fișă sunt aproximări.
Salvează documentul și exportă OBJ-urile (mm) în tmp/canapea_obj/."""
import os
import FreeCAD as App
import Part
import MeshPart
from FreeCAD import Vector as V

R = r'C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14'
d = App.getDocument('apartament_184')
grp = d.getObject('Mobilier')
XB, YC = 7100.0, -2800.0          # fața spatelui (perete) și centrul canapelei
L, D, H = 2150.0, 760.0, 870.0    # fișa produsului
HL = L / 2
ARM = 200.0                       # lățimea brațului (aprox.)
FOOT = 120.0                      # înălțimea picioarelor


def bx(v0, v1, d0, d1, w0, w1):
    """cutie în coordonate locale: v pe lungime (față de centru), d adâncime de la perete, w înălțime"""
    return Part.makeBox(d1 - d0, v1 - v0, w1 - w0, V(XB - d1, YC + v0, w0))


def rounded(shp, r):
    try:
        return shp.makeFillet(r, shp.Edges)
    except Exception:
        return shp


def fuse(lst):
    return lst[0].fuse(lst[1:]).removeSplitter() if len(lst) > 1 else lst[0]


P = lambda dd, v, w: V(XB - dd, YC + v, w)
parts = {}

# lada de sub șezut; mai scurtă cu 4 mm decât brațele, ca fețele să nu fie coplanare (z-fighting în randare)
parts['Canapea_lada'] = rounded(bx(-HL + 4, HL - 4, 0, D - 4, FOOT, 400), 6)

# brațe
arms = [rounded(bx(-HL, -HL + ARM, 0, D, FOOT, 680), 35), rounded(bx(HL - ARM, HL, 0, D, FOOT, 680), 35)]
parts['Canapea_brate'] = fuse(arms)

# spătar înclinat: profil (d, w) extrudat pe lungimea dintre brațe, cu 17 caneluri verticale
vin = HL - ARM
prof = [P(0, -vin, 400), P(190, -vin, 400), P(100, -vin, 870), P(0, -vin, 870), P(0, -vin, 400)]
back = Part.Face(Part.makePolygon(prof)).extrude(V(0, 2 * vin, 0))
for k in range(-8, 9):
    v = k * 100.0
    c = [P(184.3 - 8, v - 6, 430), P(105.7 - 8, v - 6, 840), P(105.7 + 12, v - 6, 840), P(184.3 + 12, v - 6, 430), P(184.3 - 8, v - 6, 430)]
    back = back.cut(Part.Face(Part.makePolygon(c)).extrude(V(0, 12, 0)))
parts['Canapea_spatar'] = back

# trei perne de șezut (580 × 530 × 110)
w3 = 2 * vin / 3
seat = []
for i in range(3):
    seat.append(rounded(bx(-vin + i * w3 + 3, -vin + (i + 1) * w3 - 3, 190, 740, 400, 510), 22))
parts['Canapea_perne_sezut'] = fuse(seat)

# picioare de lemn la capete (2 × 2), picioare negre rotunde (4)
wood = [bx(s * (HL - 55) - 30, s * (HL - 55) + 30, dd - 35, dd + 35, 0, FOOT) for s in (-1, 1) for dd in (70, 690)]
parts['Canapea_picioare_lemn'] = fuse(wood)
blk = [Part.makeCylinder(22, FOOT, P(dd, v, 0)) for v in (-420, 420) for dd in (110, 650)]
parts['Canapea_picioare_negre'] = fuse(blk)

LAB = {'Canapea_lada': 'Canapea Puma – ladă de depozitare', 'Canapea_brate': 'Canapea Puma – brațe',
       'Canapea_spatar': 'Canapea Puma – spătar cu caneluri', 'Canapea_perne_sezut': 'Canapea Puma – perne de șezut',
       'Canapea_picioare_lemn': 'Canapea Puma – picioare lemn', 'Canapea_picioare_negre': 'Canapea Puma – picioare negre'}
COL = {'Canapea_picioare_lemn': (0.62, 0.40, 0.22), 'Canapea_picioare_negre': (0.07, 0.07, 0.07)}
out = os.path.join(R, 'tmp', 'canapea_obj')
os.makedirs(out, exist_ok=True)
for n, s in parts.items():
    o = d.getObject(n) or d.addObject('Part::Feature', n)
    if o not in grp.Group:
        grp.addObject(o)
    o.Shape = s
    o.Label = LAB[n]
    o.ViewObject.ShapeColor = COL.get(n, (0.86, 0.80, 0.70))
    m = MeshPart.meshFromShape(Shape=s, LinearDeflection=0.2, AngularDeflection=0.3)
    m.write(os.path.join(out, n + '.obj'))
old = d.getObject('Canapea')
old.ViewObject.Visibility = False
old.Label = 'Canapea veche JYSK ILDVED 220 (înlocuită, ascunsă)'
d.recompute()
bad = [n for n in parts if not d.getObject(n).Shape.isValid()]
allb = parts['Canapea_lada'].BoundBox
for s in parts.values():
    allb.add(s.BoundBox)
d.save()
print('CANAPEA', 'invalide:', bad, 'bbox:', allb)
