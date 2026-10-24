"""Run in the FreeCAD GUI Python environment. Isolated Woodworking pilot."""
import FreeCAD as App
import FreeCADGui as Gui
import sys, json, csv
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripturi'))
from montaj_spec_noptiera import noptiera
Gui.activateWorkbench('WoodworkingWorkbench')
sys.path.insert(0, str(Path(App.getUserAppDataDir()) / 'Mod' / 'woodworking' / 'Tools'))
import MagicPanels

OUT = ROOT / 'output' / 'woodworking_pilot'
OUT.mkdir(parents=True, exist_ok=True)
doc = App.newDocument('Noptiera_Woodworking_Pilot')
doc.Label = 'Noptieră — pilot Woodworking, verificare R03'
spec = noptiera()
reference = {p['cod']: p for p in json.loads((ROOT / 'tmp/lista_debitare_R03.json').read_text(encoding='utf-8'))['piese'] if p['cod'].startswith('N-')}
objects, rows = [], []
for p in spec.parts:
    if p['code'] not in reference:
        continue
    ref = reference[p['code']]
    x, y, z, dx, dy, dz = p['box']
    obj = doc.addObject('Part::Box', 'Panel_' + p['id'].replace('.', '_'))
    obj.Label = p['code'] + ' | ' + p['label'] + ' | ' + p['id']
    obj.Length, obj.Width, obj.Height = dx, dy, dz
    obj.Placement.Base = App.Vector(x, y, z)
    for name, value in [('CodPiesa', p['code']), ('MaterialComanda', ref['mat']), ('Label2', ref['mat']), ('CantL1', ref['L1']), ('CantL2', ref['L2']), ('CantW1', ref['W1']), ('CantW2', ref['W2']), ('Fibra', ref['fibra'])]:
        if name not in obj.PropertiesList:
            obj.addProperty('App::PropertyString', name, 'Debitare R03')
        setattr(obj, name, value)
    obj.ViewObject.ShapeColor = (0.72, 0.66, 0.57) if ref['mat'] == 'CAS18' else (0.91, 0.91, 0.89)
    objects.append(obj)
doc.recompute()
for obj in objects:
    thickness, width, length = sorted(MagicPanels.getSizes(obj))
    ref = reference[obj.CodPiesa]
    expected_t = {'CAS18':18, 'ALB18':18, 'ALB16':16, 'HDF3':3}[ref['mat']]
    expected_w, expected_l = sorted([ref['W'], ref['L']])
    rows.append(dict(id=obj.Name, cod=obj.CodPiesa, material=obj.MaterialComanda, L=length, W=width, grosime=thickness, R03_L=expected_l, R03_W=expected_w, R03_grosime=expected_t, conform=(length==expected_l and width==expected_w and thickness==expected_t), L1=obj.CantL1, L2=obj.CantL2, W1=obj.CantW1, W2=obj.CantW2))

# Execute the installed getDimensions implementation with its GUI prompt disabled.
# No changes to the installed extension; use its actual scan/report functions.
tool = Path(MagicPanels.__file__).parent / 'getDimensions.py'
source = tool.read_text(encoding='utf-8')
prefix = source.split('# check if there is active document and init')[0]
ns = {'__name__':'woodworking_pilot_report'}
exec(compile(prefix, str(tool), 'exec'), ns)
ns['checkStatus']()
ns.update(sLTF='n', sAEI=False, sATS=False, sARGD=False, sARME=False, sARM=False, sARP=False, sARD=False, sARVS=False, sAWC=False, sAPC=False, sAMAX=False)
ns['gFakeCube'] = doc.addObject('Part::Box','gFakeCube')
ns['initLang']()
ns['dbColumns']['max'] = ns['getColumnsMax']('main')
ns['scanObjects'](objects, 'main')
ns['selectView']('main')
doc.removeObject('gFakeCube')
doc.recompute()
sheet = doc.getObject('toCut')
assert sheet is not None, 'Woodworking getDimensions did not produce a spreadsheet'
sheet.Label = 'Woodworking getDimensions — verificare panouri'
sheet.exportFile(str(OUT / 'Woodworking_getDimensions.csv'))
counts = Counter(r['cod'] for r in rows)
quantity_errors = {c: {'model':counts[c], 'R03':r['n']} for c,r in reference.items() if counts[c] != r['n']}
overlaps=[]
for i,a in enumerate(objects):
    for b in objects[i+1:]:
        vol=a.Shape.common(b.Shape).Volume
        if vol > 0.001:
            overlaps.append({'a':a.Name,'b':b.Name,'volum_mm3':vol})
result = dict(panouri=len(rows), pozitii=len(counts), diferente=[r for r in rows if not r['conform']], diferente_cantitati=quantity_errors, suprapuneri=overlaps, origine='Geometrie din montaj_spec_noptiera.py; dimensiuni prin MagicPanels.getSizes; raport nativ getDimensions.', limitari=['Canturile sunt metadate R03, nu raport Woodworking validat pe culorile muchiilor.', 'Nu include feronerie, găuri sau parametrizare completă. Pilotul nu este comandă de producție.'])
(OUT / 'comparatie_R03.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
with (OUT / 'comparatie_R03.csv').open('w',newline='',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]))
    writer.writeheader(); writer.writerows(rows)
Gui.activeDocument().activeView().viewAxonometric()
Gui.activeDocument().activeView().fitAll()
doc.saveAs(str(OUT / 'Noptiera_Woodworking_Pilot.FCStd'))
Gui.activeDocument().activeView().saveImage(str(OUT / 'Noptiera_Woodworking_Pilot.png'),1200,1000,'White')
print(json.dumps(result,ensure_ascii=False,indent=2))
