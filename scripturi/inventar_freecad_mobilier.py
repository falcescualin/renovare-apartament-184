"""Rulează fără interfață: freecadcmd inventar_freecad_mobilier.py
Inventar complet al pieselor de mobilier din fișierele FreeCAD SALVATE (sursa de adevăr pentru debitare):
pentru fiecare obiect cu solid: document, nume, etichetă, grup, dimensiuni (bbox local și global), volum,
cât de „cutie” e (volum / volum bbox), număr de fețe, vizibilitate și proprietățile adăugate.
Iese: tmp/inventar_freecad_mobilier.json. Nu modifică nimic."""
import os, json
import FreeCAD as App

ROOT = r"C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14"
DOCS = ["dulap_hol", "dressing", "spalatorie_vestibul", "debara", "baie", "noptiera", "perete_TV", "dulap_dormitor", "corp_spate_pat",
        "perete_TV_dormitor", "bucatarie", "masuta_cafea", "conexiuni_TV"]
STD = None


def chain(o):
    out, p = [], o
    for _ in range(8):
        ps = [x for x in p.InList if x.TypeId in ("App::Part", "App::DocumentObjectGroup")]
        if not ps:
            break
        p = ps[0]
        out.append(p.Label)
    return " / ".join(reversed(out))


try:
    App.openDocument(os.path.join(ROOT, "masuta_cafea.FCStd"))
except Exception:
    pass
for n in list(App.listDocuments()):
    App.closeDocument(n)

res = []
for dn in DOCS:
    doc = App.openDocument(os.path.join(ROOT, dn + ".FCStd"))
    base = set(App.ActiveDocument.Objects[0].PropertiesList) if False else None
    for o in doc.Objects:
        if o.TypeId in ("App::Part", "App::DocumentObjectGroup", "App::Link", "App::Origin", "App::Line", "App::Plane"):
            continue
        sh = getattr(o, "Shape", None)
        if sh is None or sh.isNull() or not sh.Solids:
            continue
        # piese folosite doar ca bază pentru altele (ex. Cut/Fusion) — marcăm dacă au părinți de tip Part::Feature
        used_by = [x.Name for x in o.InList if x.TypeId not in ("App::Part", "App::DocumentObjectGroup")]
        bb = sh.BoundBox
        try:
            gpl = o.getGlobalPlacement()
            gs = sh.copy(); gs.Placement = gpl.multiply(o.Placement.inverse()).multiply(gs.Placement)
            gbb = gs.BoundBox
        except Exception:
            gbb = bb
        vol = sh.Volume
        bvol = max(bb.XLength * bb.YLength * bb.ZLength, 1e-9)
        extra = {}
        for p in o.PropertiesList:
            if o.getGroupOfProperty(p) not in ("Base", "Part", "Attachment", "Shape", "") and p not in ("Label2",):
                try:
                    v = getattr(o, p)
                    if isinstance(v, (str, int, float, bool)):
                        extra[p] = v
                except Exception:
                    pass
        res.append(dict(doc=dn, name=o.Name, label=o.Label, label2=getattr(o, "Label2", ""), type=o.TypeId, group=chain(o),
                        vis=bool(getattr(o, "Visibility", True)), used_by=used_by,
                        bb=[round(bb.XMin, 1), round(bb.YMin, 1), round(bb.ZMin, 1), round(bb.XMax, 1), round(bb.YMax, 1), round(bb.ZMax, 1)],
                        gbb=[round(gbb.XMin, 1), round(gbb.YMin, 1), round(gbb.ZMin, 1), round(gbb.XMax, 1), round(gbb.YMax, 1), round(gbb.ZMax, 1)],
                        dims=sorted([round(bb.XLength, 1), round(bb.YLength, 1), round(bb.ZLength, 1)]),
                        vol=round(vol / 1e6, 4), boxness=round(vol / bvol, 3), faces=len(sh.Faces), solids=len(sh.Solids), extra=extra))
    App.closeDocument(doc.Name)
out = os.path.join(ROOT, "tmp", "inventar_freecad_mobilier.json")
json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("INVENTAR_OK", len(res))
