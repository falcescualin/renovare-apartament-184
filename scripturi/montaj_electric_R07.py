"""R07: montaj R05 plus plansa explicita pentru iluminatul balconului."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripturi'))
wrapper=(ROOT/'scripturi/montaj_electric_R05.py').read_text(encoding='utf-8')
wrapper=wrapper[:wrapper.rfind("exec(compile(SRC,")]
wrapper=wrapper.replace('R05','R07')
exec(compile(wrapper,'montaj_R07_base','exec'))
SRC=SRC.replace('05.10.2026','06.10.2026')
SRC=SRC.replace('exec(patch_prefix(src))',"exec(patch_prefix(src).replace('05.10.2026','06.10.2026'))")
POS={'J01': [7250, -3750, 2400], 'J02': [7100, -3750, 2400], 'J03': [3550, -3600, 2400], 'J04': [2525, -4050, 2400], 'J05': [9000, -3470, 2400], 'J06': [9875, -2350, 2400]}
SRC=SRC.replace('routes={}\n', 'for jid,xyz_wall in '+repr(POS)+'.items():\n J[jid].update(dict(zip((\"x\",\"y\",\"z\"),xyz_wall)))\nroutes={}\n')

SRC=SRC.replace('Dormitor, deasupra intrării','Dormitor, perete spre sufragerie').replace('Bucătărie, deasupra intrării','Bucătărie, perete spre hol')
SRC=SRC.replace('lx=max(55,min(650,x+10));ly=y-9+dy','lx=max(55,min(650,x+10));ly=y-9+dy\n if r[\"id\"]==\"J01\":ly=y+25\n if r[\"id\"]==\"J02\":lx=x-35;ly=y-18')

detail=r'''
end()
startp('BAL','Balcon inchis / iluminat si comanda','R07 | doze pe fetele peretilor; balcon L06 / S06 pe C02')
scale=.064
project=lambda p:(65+p[0]*scale,260-p[1]*scale)
for edge in DATA['wall_edges']:
 if len(edge)==2:
  a,b=map(project,edge);line(*a,*b,GRAY,.7)
for rid,col in [('L06',TEAL),('S06',ORANGE)]:
 r=routes[rid]
 for a,b in zip(r['points'],r['points'][1:]):
  aa,bb=project(a),project(b)
  if aa!=bb:line(*aa,*bb,col,2.2)
 x,y=project(r['endpoint']);circle(x,y,6,col,col);txt(x+10,y-8,rid,12,col,True)
for rid in ['J05']:
 x,y=project(routes[rid]['endpoint']);circle(x,y,5,INK,white);txt(x+10,y-9,rid,11,INK,True)
x,y=project(TE);circle(x,y,6,RED,RED);txt(x+10,y-10,'TE',12,RED,True)
txt(340,155,'BALCON INCHIS',14,TEAL,True)
table(780,158,[85,270],[['Reper','Pozitie fata de model, mm'],['L06 / plafoniera','X 5400 / Y 650 / Z 2490'],['S06 / comanda','X 6180 / Y -255 / Z 1050'],['J05 / derivatie','X 9000 / Y -3470 / Z 2400'],['Circuit','C02, conform planului electric'],['Distributie','Z 2400; coborare la comanda'] ],10)
para(780,405,355,'<b>Citirea traseului</b><br/>Verde: TE - J05 - L06. Portocaliu: TE - J05 - S06. Portiunile comune sunt suprapuse; nu se numara de doua ori ca santuri.<br/><br/><b>Comanda</b><br/>S06 comanda L06. N si PE merg la corp; faza comandata este distincta. Numarul conductoarelor se stabileste dupa cablarea comenzii, fara folosirea PE ca retur.<br/><br/><b>Corpul propus</b><br/>Plafoniera LED, preferabil IP54 pentru condens. Cota Z2490 se confirma dupa grosimea corpului si tavanul real. Intrerupatorul ramane in sufragerie, langa usa balconului.',11)
para(65,650,675,'<b>Model FreeCAD:</b> montaj_electric_R07.FCStd. Grupul BALCON afiseaza traseele L06 / S06 si derivatia J05. Grupele pe circuite contin toate cele 63 de rute originale, cu coordonate si lungime geometrica. Afisati cate un circuit pentru o vedere clara.',11)
para(65,715,675,'<b>Montaj:</b> trecerea prin golul usii se coordoneaza cu structura si tamplaria existenta; nu se gaureste rama termopanului. Traseele sunt propuse, nu autorizatie pentru strapungeri in beton. Plafoniera balconului este una dintre cele 8 deja bugetate.',10)
end();c.save()
'''
assert SRC.count('end();c.save()')==1
SRC=SRC.replace('end();c.save()',detail)
exec(compile(SRC,'electric_complet_R07','exec'))
