import FreeCAD as App, FreeCADGui as Gui, Part, json
from pathlib import Path
R=Path('C:/Users/Falcescu Alin/Desktop/Apartament_184_Bloc_L14')
D=json.loads((R/'output/pdf/Apartament_184_Revizie_electrica_R10.json').read_text(encoding='utf-8'))
A=json.loads((R/'tmp/termic_model.json').read_text(encoding='utf-8'))
F=json.loads((R/'tmp/mobilier_plan_R03.json').read_text(encoding='utf-8'))['items']
name='montaj_electric_R10_revizie'
if name in App.listDocuments():App.closeDocument(name)
doc=App.newDocument(name);doc.Label='Electric R10 | REVIZIE DE COORDONARE'
root=doc.addObject('App::Part','Revizie_R10')
root.addProperty('App::PropertyString','Statut');root.Statut='NU este plan de executie validat. Axele necesita revizie coturi, treceri, latimi culoare si cote pardoseala.'
root.addProperty('App::PropertyString','Documentatie');root.Documentatie='output/pdf/Apartament_184_Ghid_vizual_electric_R10.pdf'
context=doc.addObject('App::DocumentObjectGroup','Context');root.addObject(context)
edges=[Part.makeLine(App.Vector(*e[0],0),App.Vector(*e[1],0)) for e in A['wall_edges'] if len(e)==2]
o=doc.addObject('Part::Feature','Pereti_plan');o.Shape=Part.makeCompound(edges);context.addObject(o);o.ViewObject.LineColor=(.2,.22,.24);o.ViewObject.LineWidth=2.5
o=doc.addObject('Part::Feature','Pereti_3D');o.Shape=Part.makeCompound([e.extrude(App.Vector(0,0,700)) for e in edges]);context.addObject(o);o.ViewObject.ShapeColor=(.8,.81,.8);o.ViewObject.Transparency=82
furn=[]
for f in F:
 for poly in f.get('polys') or [f['poly']]:furn.append(Part.makePolygon([App.Vector(x,y,5) for x,y in poly+poly[:1]]))
o=doc.addObject('Part::Feature','Mobilier_referinta');o.Shape=Part.makeCompound(furn);context.addObject(o);o.ViewObject.LineColor=(.6,.6,.6);o.ViewObject.DrawStyle='Dashed';o.ViewObject.LineWidth=1
groups={};palette=[(.03,.4,.65),(.75,.35,.08),(.02,.48,.37),(.6,.18,.5)]
for t in D['tubes']:
 ci=t['circuit']
 if ci not in groups:
  g=doc.addObject('App::DocumentObjectGroup','Circuit_'+ci);g.Label=ci+' | '+next((x[1] for x in D['circuits'] if x[0]==ci),'curenti slabi / conexiune locala');root.addObject(g);groups[ci]=g
 o=doc.addObject('Part::Feature',t['id']);o.Shape=Part.makePolygon([App.Vector(*p) for p in t['points']]);groups[ci].addObject(o)
 o.Label=t['id']+' | '+t['source']+' > '+t['destination']+' | '+str(t['wire_count'])+' fire/cabluri'
 for key,val in [('DeLa',t['source']),('PanaLa',t['destination']),('Circuit',ci),('Continut',t['wire_roles']),('Sectiune',str(t['section_mm2'])+' mm2'),('Statut','DE REVIZUIT tragerea' if t['pull_review'] else 'Coordonare; montaj nevalidat'),('Coordonate',json.dumps(t['points']))]:
  o.addProperty('App::PropertyString',key,'Montaj');setattr(o,key,val)
 for key,val in [('NumarFireSauCabluri',t['wire_count']),('DiametruExteriorPropus',t['diameter_proposed_mm'])]:o.addProperty('App::PropertyInteger',key,'Montaj');setattr(o,key,val)
 o.ViewObject.LineColor=palette[(int(ci[1:])-1)%4] if ci.startswith('C') else (.5,.22,.7);o.ViewObject.LineWidth=3
nodegroup=doc.addObject('App::DocumentObjectGroup','Puncte');root.addObject(nodegroup)
seen=set()
for t in D['tubes']:
 for node,pt in [(t['source'],t['points'][0]),(t['destination'],t['points'][-1])]:
  if node in seen:continue
  seen.add(node);o=doc.addObject('Part::Feature','Punct_'+node.replace(' / ','_').replace(' ','_'));o.Label=node;o.Shape=Part.makeSphere(28,App.Vector(*pt));nodegroup.addObject(o);o.ViewObject.ShapeColor=(1.0,.65,.1)
for l in D['lights']:
 o=doc.addObject('Part::Feature','Existent_'+l['id']);o.Label=l['id']+' | pozitie model / legatura existenta de verificat';o.Shape=Part.makeSphere(45,App.Vector(*l['model_endpoint']));nodegroup.addObject(o);o.ViewObject.ShapeColor=(1.0,.85,.2)
doc.recompute();Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
doc.saveAs(str(R/(name+'.FCStd')))
Gui.activeDocument().activeView().saveImage(str(R/'output/Electric_R10_3D.png'),1600,1100,'White')
doc.getObject('Pereti_3D').ViewObject.Visibility=False
Gui.activeDocument().activeView().viewTop();Gui.activeDocument().activeView().fitAll()
Gui.activeDocument().activeView().saveImage(str(R/'output/Electric_R10_plan.png'),1600,1100,'White')
doc.save()
print('R10 saved; tubes='+str(len(D['tubes']))+'; circuits='+str(len(groups)))

