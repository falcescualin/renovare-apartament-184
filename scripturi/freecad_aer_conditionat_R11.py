# Aer conditionat R11: UN SINGUR aparat, in dormitor, pe peretele vest in coltul de nord, cu aerul spre masa de machiaj.
# Conductele (frigorifice + condens + tub electric C15) sunt inchise intr-o masca de la podea la tavan, acoperita cu riflaje
# (aceleasi lamele ca la peretele TV din perete_TV_dormitor.FCStd).
#
# build_ac(doc, parent) construieste grupul "Aer_conditionat" in documentul dat.
# Rulat direct:  creeaza documentul aer_conditionat_R11_propuneri (fundal copiat din apartament_184, fara a-l modifica).
# Rulare din sesiunea GUI:  exec(open(r'...\scripturi\freecad_aer_conditionat_R11.py', encoding='utf-8').read())
import FreeCAD as App, Part
V = App.Vector

WHITE = (0.95, 0.95, 0.95); GREEN = (0.20, 0.62, 0.35); OAK = (0.82, 0.70, 0.54); DARK = (0.25, 0.23, 0.21)

# ---------- parametri (mm) ----------
X0 = 150                      # fata peretelui vest
Y_NORD = -250                 # fata interioara a peretelui de fatada
W, D, H = 700, 190, 250       # unitate interioara 9000 BTU, profil subtire
Y_C = -790                    # axa unitatii (capatul nordic la y -440, lipit de masca)
Z0 = 2090                     # baza unitatii (varful la 2340 => 160 mm sub tavan)
SUP, LAM = 9, 21              # suport + lamela, ca la riflajele din dormitor
MASK_D = 80                   # adancimea mastii: perete -> cavitate 50 mm (conducte 28 mm) -> suport 9 -> lamele 21
MASK_Y0, MASK_Y1 = -440, Y_NORD
Z_TOP = 2495                  # ca peretele TV (riflaje pana la 2495)
Z_FLOOR = 10                  # fata pardoselii finite (parchet 10 mm peste placa)
X_PIPE = 184                  # axa conductelor frigorifice (in cavitate, x 170-198)
Z_FRIG, Z_DRAIN = 2085, 2045  # frigorifice mai sus, condens mai jos (panta spre exterior)
X_COND = 160                  # axa tubului electric Ø20 al circuitului C15 (x 150-170)
Y_COND = -340
Z_COND_TOP = 2200


def build_ac(doc, parent=None, prefix=''):
    def grp(n, par=None):
        g = doc.addObject('App::DocumentObjectGroup', prefix + n)
        if par: par.addObject(g)
        return g
    def color(o, rgb, tr=0):
        try:
            o.ViewObject.ShapeColor = rgb; o.ViewObject.LineColor = rgb; o.ViewObject.Transparency = tr
        except Exception: pass
    def box(name, x, y, z, dx, dy, dz, rgb, par, label, tr=0):
        b = doc.addObject('Part::Box', prefix + name); b.Length, b.Width, b.Height = dx, dy, dz
        b.Placement.Base = V(x, y, z); b.Label = label; par.addObject(b); color(b, rgb, tr); return b
    def tube(name, pts, d, rgb, label, par):
        parts = []
        for a, b2 in zip(pts, pts[1:]):
            pa, pb = V(*a), V(*b2); L = (pb - pa).Length
            if L > 0.5: parts.append(Part.makeCylinder(d / 2, L, pa, (pb - pa).normalize()))
        for p in pts[1:-1]: parts.append(Part.makeSphere(d / 2, V(*p)))
        o = doc.addObject('Part::Feature', prefix + name); o.Shape = Part.makeCompound(parts); o.Label = label; par.addObject(o); color(o, rgb); return o

    G = grp('Aer_conditionat')
    if parent: parent.addObject(G)
    gM = grp('Masca_riflaje', G); gU = grp('Unitati', G); gP = grp('Conducte', G); gX = grp('Flux_aer', G)

    # ----- masca de la podea la tavan, acoperita cu riflaje -----
    x_front = X0 + MASK_D                       # fata lamelelor
    x_sup = x_front - LAM - SUP                 # fata suportului
    ymid = (MASK_Y0 + MASK_Y1) / 2
    box('Masca_suport', x_sup, MASK_Y0, Z_FLOOR, SUP, MASK_Y1 - MASK_Y0, Z_TOP - Z_FLOOR, DARK, gM,
        'Masca - panou frontal inchis la culoare (suport riflaje), podea-tavan, 190 x 80 mm')
    box('Masca_flanc_sud', X0, MASK_Y0, Z_FLOOR, x_sup + SUP - X0, SUP, Z_TOP - Z_FLOOR, DARK, gM, 'Masca - flanc lateral (spre camera)')
    n = 0
    y = MASK_Y0 + 6
    while y + 27 <= MASK_Y1 + 1:
        box(f'Lamela_{n:02d}', x_front - LAM, y, Z_FLOOR, LAM, 27, Z_TOP - Z_FLOOR, OAK, gM, 'Lamela stejar 27x21 mm, pas 40 mm (ca la peretele TV)')
        n += 1; y += 40
    box('Masca_capac_vizita', x_sup - 2, MASK_Y0 + 10, 1960, 2, 170, 240, (0.6, 0.45, 0.2), gM,
        'Zona de acces: lamelele dintre z 1960 si 2200 se demonteaza (prindere magnetica / suruburi ascunse)', tr=60)

    # ----- unitati -----
    box('INT_AC', X0, Y_C - W / 2, Z0, D, W, H, WHITE, gU,
        'Unitate interioara 9000 BTU, profil subtire 190 mm, lipita de perete, baza 2090 / varf 2340')
    box('FANTA_AC', X0 + D - 12, Y_C - W / 2 + 25, Z0 + 22, 14, W - 50, 38, (0.25, 0.25, 0.28), gU, 'Gura de aer (jos, pe fata)')
    xo, yo, zo = 150, 80, 1250
    box('EXT_AC', xo, yo, zo, 800, 300, 550, GREEN, gU, 'Unitate exterioara 9000 BTU pe consola de fatada')
    f = doc.addObject('Part::Feature', prefix + 'VENT_AC'); f.Shape = Part.makeCylinder(187, 12, V(xo + 280, yo + 300, zo + 275), V(0, 1, 0))
    f.Label = 'Ventilator unitate exterioara'; gU.addObject(f); color(f, (0.15, 0.15, 0.15))
    for dx_ in (120, 640): box(f'CONS_{dx_}', xo + dx_, yo - 70, zo - 50, 40, 370, 40, (0.4, 0.4, 0.4), gU, 'Consola unitate exterioara')

    # ----- conducte (in cavitatea mastii) -----
    tube('Conducte_frigorifice', [(X_PIPE, Y_C + W / 2, Z_FRIG), (X_PIPE, Y_NORD, Z_FRIG), (X_PIPE, 0, Z_FRIG), (X_PIPE, 150, Z_FRIG), (X_PIPE, 150, 1560)],
         28, (0.85, 0.35, 0.05), 'Conducte frigorifice 1/4" + 3/8" in izolatie (+ cablu 4x1,5 spre exterior), prin fatada la x 184 / z 2085', gP)
    tube('Condens', [(X_PIPE, Y_C + W / 2, Z_DRAIN), (X_PIPE, 0, Z_DRAIN - 25), (X_PIPE, 150, Z_DRAIN - 45), (X_PIPE, 150, 800)],
         16, (0.3, 0.5, 0.95), 'Scurgere condens Ø16, panta spre exterior', gP)
    tube('Tub_electric_C15', [(X_COND, Y_COND, -40), (X_COND, Y_COND, Z_COND_TOP), (X_COND, MASK_Y0 + 20, Z_COND_TOP)],
         20, (1, 0.9, 0.1), 'Tub copex Ø20 C15 (3x2,5 mm2): din podea, urca in masca pana la unitate', gP)

    # ----- flux de aer spre masa de machiaj -----
    ax = V(1, 0, -0.30).normalize()
    cone = doc.addObject('Part::Feature', prefix + 'Flux_aer'); cone.Shape = Part.makeCone(60, 700, 3250, V(X0 + D, Y_C, Z0 + 40), ax)
    cone.Label = 'Flux aer spre masa de machiaj'; gX.addObject(cone); color(cone, (0.2, 0.6, 1.0), 82)
    t = doc.addObject('Part::Feature', prefix + 'Tinta_masa_machiaj'); t.Shape = Part.makeSphere(60, V(3340, -845, 1000))
    t.Label = 'Masa de machiaj (x 3340 / y -845) - tinta fluxului'; gX.addObject(t); color(t, (1, 0.3, 0.5))
    return G


if __name__ == '__main__' or 'NAME' not in globals():
    NAME = 'aer_conditionat_R11_propuneri'
    src = App.getDocument('apartament_184')
    if NAME in App.listDocuments(): App.closeDocument(NAME)
    doc = App.newDocument(NAME)
    g_ctx = doc.addObject('App::DocumentObjectGroup', 'Fundal_apartament'); n_ctx = 0
    for o in src.Objects:
        if o.Name.startswith('AC_'): continue                   # nu copia AC-ul deja adus in apartament
        if not hasattr(o, 'Shape') or o.Shape.isNull() or not o.Visibility: continue
        if any(s in o.Label.lower() for s in ('axis', 'plane', 'origin', 'aer conditionat')) or o.Shape.BoundBox.XLength > 1e6: continue
        c = doc.addObject('Part::Feature', 'F_' + o.Name); c.Shape = o.Shape; c.Label = o.Label; g_ctx.addObject(c); n_ctx += 1
        try:
            vo = o.ViewObject; c.ViewObject.ShapeColor = vo.ShapeColor; c.ViewObject.DiffuseColor = vo.DiffuseColor
            c.ViewObject.Transparency = 88 if o.Label == 'Pereti' else vo.Transparency
        except Exception: pass
    build_ac(doc)
    doc.recompute()
    print('context', n_ctx, 'obiecte', len(doc.Objects))
