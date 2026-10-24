"""Rulează fără interfață: freecadcmd export_freecad_headless.py   (sau cu python-ul FreeCAD)
Exportă apartamentul din fișierele SALVATE (nu din sesiunea deschisă în FreeCAD, unde pot fi modificări nesalvate)
ca OBJ per piesă + manifest, cu aceleași reguli ca export_freecad_blender.py, într-un folder nou datat.
- vizibilitatea se ia din proprietatea Visibility salvată în fișier (fără interfață nu există ViewObject);
- documentele de instalație electrică (montaj_electric_*, instalatie_electrica_*) nu intră: sunt trasee din pereți,
  nu se văd în randări și nu erau nici în exportul vechi."""
import os, sys, json
import FreeCAD as App

ROOT = r"C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14"
OUT = os.path.join(ROOT, "blender_export_2026-10-06")
G = {}
exec(open(os.path.join(ROOT, "scripturi", "export_freecad_blender.py"), encoding="utf-8").read(), G)
EXCLUDE = ("montaj_electric", "instalatie_electrica")


def visible(o):
    return bool(getattr(o, "Visibility", True))


G["visible"] = visible
_collect = G["collect"]


def collect(doc):
    keep = []
    for it in _collect(doc):
        pid, obj, pl, asm, hidden = it
        if obj.Document.Name.startswith(EXCLUDE) or obj.Document.FileName and os.path.basename(obj.Document.FileName).startswith(EXCLUDE):
            continue
        keep.append(it)
    return keep


G["collect"] = collect
# În freecadcmd, prima deschidere de fișier din proces eșuează („Invalid project file” / „bad conversion”) și lasă
# un document gol. Se face o deschidere de încălzire, se închide tot, apoi se deschide apartamentul, care își încarcă
# singur componentele legate; la final se verifică faptul că fiecare componentă vizibilă are piese.
try:
    App.openDocument(os.path.join(ROOT, "masuta_cafea.FCStd"))
except Exception:
    pass
for n in list(App.listDocuments()):
    App.closeDocument(n)
doc = App.openDocument(os.path.join(ROOT, "apartament_184.FCStd"))
empty = [o.Name for o in doc.Objects if o.TypeId == "App::Link" and getattr(o, "Visibility", True)
         and (o.LinkedObject is None or not getattr(o.LinkedObject, "Group", [1]))]
assert len(doc.Objects) > 100 and not empty, (len(doc.Objects), empty)
print("componente:", {o.Name: len(o.LinkedObject.Group) for o in doc.Objects if o.TypeId == "App::Link" and o.LinkedObject})
print("documente incarcate:", sorted(App.listDocuments().keys()))
records, n = G["export_bundle"](doc, out_dir=OUT)
G["write_manifest"](doc, records, out_dir=OUT)
print("EXPORT_OK", len(records), "piese", OUT.encode("ascii", "replace").decode())
