"""Rulează în FreeCAD (interfață), cu documentul baie deschis: exec din consola Python sau prin MCP   (07.10.2026)
Nu se salvează fișierele FreeCAD fără interfață: se pierd vizibilitatea și culorile.
Modelează în baie.FCStd două produse Alessandro Design, cu dimensiunile din fișele lor:
- Coloană de duș 9710N (inox SUS304, Gun Grey): baterie 270 × 30 × 30 mm, pălărie pătrată 220 × 220 × 10 mm,
  pară 210 × 30 × 10 mm, înălțime 1100 mm (valoarea mare din „78 cm, 110 cm”), 380 mm de la perete.
  Pe peretele cu scafa de gips (masca cu nișe, fața la y = −5420): axa bateriei la x = 500 și z = 1200, pe banda plină
  dintre nișe (z 1150–1250); suportul parei pe banda 1600–1700, bracketul de țeavă pe banda 2000–2110.
- Baterie lavoar 9707N (alamă sanitară, Gun Grey, 1 orificiu, pipă fixă): lungime 190 mm, înălțime 180 mm, pe marginea lavoarului.
Detaliile care nu sunt în fișă (rozete, forma manetei, traseul furtunului) sunt aproximări după fotografii.
Exportă OBJ-urile (mm, coordonate globale) în tmp/baterii_obj/."""
import os
import FreeCAD as App
import Part
import MeshPart
from FreeCAD import Vector as V

R = r'C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14'
d = App.getDocument('baie')
root = d.getObject('Baie_amenajare')
GRI = (0.27, 0.28, 0.30)


def fuse(shapes):
    s = shapes[0]
    return s.fuse(shapes[1:]).removeSplitter() if len(shapes) > 1 else s


def cyl(r, h, p, dr):
    return Part.makeCylinder(r, h, V(*p), V(*dr))


def seg(a, b, r):
    a, b = V(*a), V(*b)
    return Part.makeCylinder(r, (b - a).Length, a, b - a)


def tubes(pts, r):
    out = [seg(a, b, r) for a, b in zip(pts, pts[1:])]
    out += [Part.makeSphere(r, V(*p)) for p in pts[1:-1]]
    return fuse(out)


# cadru local: u în afara peretelui (+Y), v de-a lungul peretelui (+X), w în sus de la axa bateriei
X0, Y0, Z0 = 500.0, -5420.0, 1200.0
P = lambda u, v, w: (X0 + v, Y0 + u, Z0 + w)
BX = lambda u0, u1, v0, v1, w0, w1: Part.makeBox(v1 - v0, u1 - u0, w1 - w0, V(X0 + v0, Y0 + u0, Z0 + w0))
OUT = (0, 1, 0)
U_T = 50.0
parts = {}

bat = [BX(35, 65, -135, 135, -15, 15)]
for v in (-75, 75):
    bat += [cyl(30, 12, P(0, v, 0), OUT), cyl(11, 40, P(0, v, 0), OUT)]
bat.append(BX(40, 50, -12, 12, -105, -10))
parts['Coloana_dus_baterie'] = fuse(bat)

tub = [seg(P(U_T, 0, 15), P(U_T, 0, 1100), 12.5), seg(P(U_T, 0, 1100), P(270, 0, 1100), 12.5),
       Part.makeSphere(12.5, V(*P(U_T, 0, 1100))), seg(P(270, 0, 1100), P(270, 0, 1088), 9)]
tub += [cyl(22, 10, P(0, 0, 850), OUT), seg(P(10, 0, 850), P(U_T, 0, 850), 8), cyl(17, 25, P(U_T, 0, 838), (0, 0, 1))]
parts['Coloana_dus_teava'] = fuse(tub)

parts['Coloana_dus_palarie'] = BX(160, 380, -110, 110, 1078, 1088)

VH = 280.0
sup = [cyl(20, 10, P(0, VH, 450), OUT), seg(P(10, VH, 450), P(60, VH, 450), 9), cyl(17, 30, P(60, VH, 435), (0, 0, 1))]
parts['Coloana_dus_suport_para'] = fuse(sup)
parts['Coloana_dus_para'] = BX(55, 65, VH - 15, VH + 15, 380, 590)
parts['Coloana_dus_furtun'] = tubes([P(60, VH, 380), P(60, VH, 250), P(60, VH - 20, 120), P(55, VH - 80, 40),
                                     P(50, 120, 20), P(50, 100, -15)], 5)

# baterie lavoar 9707N, axa la (1250, −5500), baza pe marginea lavoarului (z = 890)
AX, AY, AZ = 1250.0, -5500.0, 890.0
Q = lambda dx, dy, dz: V(AX + dx, AY + dy, AZ + dz)
B = lambda x0, x1, y0, y1, z0, z1: Part.makeBox(x1 - x0, y1 - y0, z1 - z0, Q(x0, y0, z0))
lav = [B(-23, 23, -20, 20, 0, 7), B(-15, 15, -15, 15, 7, 142), B(-13, 13, -15, 165, 128, 142),
       Part.makeCylinder(11, 32, Q(0, 0, 142))]
lever = B(-13, 13, -25, 140, 174, 180)
lever = lever.cut(B(-5, 5, 20, 62, 170, 184)).cut(B(-5, 5, 72, 118, 170, 184))
lav.append(lever)
parts['Baterie_lavoar'] = fuse(lav)

for name, shp in parts.items():
    o = d.getObject(name)
    if o is None:
        o = d.addObject('Part::Feature', name)
        root.addObject(o)
    o.Shape = shp
    o.Label = {'Baterie_lavoar': 'Baterie lavoar 9707N (Alessandro Design) 190 × 180 mm, Gun Grey'}.get(
        name, name.replace('_', ' ') + ' – coloană duș 9710N (Alessandro Design)')
    o.ViewObject.ShapeColor = GRI
    o.ViewObject.Visibility = True

# culori pe familii de materiale (în fișier nu fuseseră păstrate)
FAM = [
    (('Cada_', 'Lavoar_60', 'WC_suspendat', 'Colac_WC'), (0.96, 0.96, 0.94)),
    (('Masca_', 'Panou_cada', 'Trapa_'), (0.52, 0.52, 0.43)),
    (('Dulap_WC_usa', 'Corp_lavoar'), (0.72, 0.71, 0.67)),
    (('Dulap_WC_',), (0.93, 0.93, 0.91)),
    (('Cadru_WC', 'Sifon_cada', 'Calorifer', 'Profil_paravan', 'Balama_'), (0.62, 0.64, 0.66)),
    (('Rezervor_incastrat',), (0.78, 0.84, 0.87)), (('Clapeta_WC',), (0.70, 0.71, 0.70)),
    (('Recipient_nisa',), (0.64, 0.75, 0.76)), (('Oglinda_lavoar',), (0.65, 0.76, 0.78)),
    (('Garnitura_paravan',), (0.93, 0.93, 0.91)),
]
for o in d.Objects:
    if o.TypeId != 'Part::Feature':
        continue
    for pre, c in FAM:
        if o.Name.startswith(pre):
            o.ViewObject.ShapeColor = c
            break
    if o.Name == 'Paravan_sticla_cada':
        o.ViewObject.ShapeColor = (0.70, 0.85, 0.90)
        o.ViewObject.Transparency = 60
d.recompute()
for name in parts:
    assert d.getObject(name).Shape.isValid(), name
d.save()

out = os.path.join(R, 'tmp', 'baterii_obj')
os.makedirs(out, exist_ok=True)
for name in parts:
    sh = d.getObject(name).Shape
    m = MeshPart.meshFromShape(Shape=sh, LinearDeflection=0.05, AngularDeflection=0.25)
    m.write(os.path.join(out, name + '.obj'))
    bb = sh.BoundBox
    print('PIESA|%s|%.0f %.0f %.0f|%.0f %.0f %.0f' % (name, bb.XMin, bb.YMin, bb.ZMin, bb.XMax, bb.YMax, bb.ZMax))
