"""Montaj electric R05: aceleași trasee ca R04 (electric_r04_complet.py, nemodificat), refăcut cu ultimele decizii:
- fundalul are mobilierul actual din modelul 3D (tmp/mobilier_plan.json), nu dreptunghiurile vechi;
- planșa nouă K1: cablul de tăiat pe fiecare circuit, calculat exact pe trasee (traseul comun numărat o singură dată),
  plus cablurile Cat6 / coaxial, fiecare separat până la distribuitor.
Rulează cu Python-ul care are reportlab.
Iese: output/pdf/Apartament_184_Montaj_electric_R05.pdf, Apartament_184_Trasee_complete_R05.json, Verificare_trasee_R05.csv"""
import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from plan_comun import *

SRC = (ROOT / 'scripturi/electric_r04_complet.py').read_text(encoding='utf-8')


def rep(a, b, n=1):
    global SRC
    assert SRC.count(a) == n, (SRC.count(a), a[:90])
    SRC = SRC.replace(a, b)


rep('Apartament_184_Trasee_complete_R04.json', 'Apartament_184_Trasee_complete_R05.json')
rep("{'revision':'R04'", "{'revision':'R05'")
rep('Apartament_184_Verificare_trasee_R04.csv', 'Apartament_184_Verificare_trasee_R05.csv')
rep('Apartament_184_Montaj_electric_R04.pdf', 'Apartament_184_Montaj_electric_R05.pdf')
rep(".replace('R01 |','R04 |')", ".replace('R01 |','R05 |')")
rep('exec(src)\n', 'exec(patch_prefix(src))\n')
rep("c.setTitle('Apartament 184 - Montaj electric R04 - traseu pana la fiecare punct')",
    "c.setTitle('Apartament 184 - Montaj electric R05 - traseu pana la fiecare punct')")
# corecția veche a fundalului (noptierele) nu mai e necesară: noptierele sunt în mobilier_plan.json
SRC = '\n'.join(l for l in SRC.split('\n') if not l.startswith("DATA['furniture']=") and not l.startswith('# Correct old grouped furniture'))

# ---- planșa 00
rep("startp('00','Fiecare punct are acum traseul complet','R04 | plan de citire simplă + verificare de continuitate + detalii de montaj')",
    "startp('00','Montaj electric / traseul complet al fiecărui punct','R05 | trasee R04 neschimbate + mobilierul actual pe fundal + cablul pe circuite (K1)')")
SRC = re.sub(r"para\(42,310,525,'<b>Corecția importantă</b>.*?',12\)",
             lambda m: "para(42,310,525,'<b>Ce e nou în R05</b><br/>Traseele sunt cele din R04, verificate punct cu punct. "
                       "Fundalul are acum mobilierul actual din modelul 3D: dulapul din hol, dressingul, bucătăria, comodele TV și noptierele. "
                       "Planșa K1 arată cât cablu tai pentru fiecare circuit. P02 (priza de lângă geamul dormitorului) și P05 (machiaj) au trasee separate.',12)",
             SRC, count=1)
rep("['4 / Verificare','Registrul final + CSV','Fiecare ID, sursa, circuitul și capătul traseului'] ],11)",
    "['4 / Verificare','Registrul final + CSV','Fiecare ID, sursa, circuitul și capătul traseului'],['5 / Cablu','K1 - cablu pe circuite','Metri de 3×1,5 / 3×2,5 pe circuit, Cat6 și coaxial pe priză'] ],11)")

# ---- planșa K1, imediat după 00
K1 = r'''
CC=cable_circuits(list(routes.values()));T15,T25=cable_totals(CC);DL=data_lines(list(routes.values()))
startp('K1','Cablu pe circuite / cât tai pentru fiecare','Pe traseele din acest dosar: aparatele de pe același circuit se leagă unul după altul, deci traseul comun se pune o singură dată')
rows=[['Circuit','Ce alimentează / aparate','Buc.','Cablu','Traseu comun m','Urcări între prize m','Tablou 1 m + 0,3 m / aparat','Total m']]
for r in CC:
 rows.append(['<b>'+r['id']+'</b><br/>'+r['prot'],r['dest']+'<br/><font color="#536473">'+r['ids']+'</font>',str(r['n']),r['sec']+' mm²',('%.1f'%r['union']).replace('.',','),('%.1f'%r['urcari']).replace('.',',') if r['urcari'] else '-',('%.1f'%(r['te']+r['capete'])).replace('.',','),'<b>'+('%.1f'%r['total']).replace('.',',')+'</b>'])
rows.append(['','<b>Total de cumpărat</b>','','','','','','<b>3×1,5: %d m<br/>3×2,5: %d m</b>'%(T15,T25)])
y=tbl(42,150,[78,372,46,82,110,130,160,128],rows,9,4,total=True)
cat=[d for d in DL if d['kind']=='D'];cox=[d for d in DL if d['kind']=='T']
f=lambda v:('%.1f'%v).replace('.',',')
para(42,y+14,525,'<b>Cum se citește</b><br/>Traseul comun e lungimea reuniunii segmentelor circuitului: tabloul, culoarul de la Z2400, ramurile și coborârile. La prize, cablul coboară la priză și urcă înapoi la tavan spre următoarea (coloana „Urcări”), mai puțin la ultima. Se adaugă 1 m la tablou și 0,3 m la fiecare aparat. Întrerupătoarele au deja coborârea lor în traseu. LED-ul de 24 V de la noptiere (F08A/B) nu intră aici.',10)
para(620,y+14,528,'<b>Ce cumperi</b> (deviz R03, cele mai bune oferte)<br/>3×1,5 mm²: %d m, adică o rolă de 100 m (%s).<br/>3×2,5 mm²: %d m, adică o rolă de 100 m + 37 m la metru (%s).<br/><b>Cat6, câte un cablu separat până la NET:</b> %s = %s m.<br/><b>Coaxial RG6, separat pe fiecare priză:</b> %s = %s m.<br/>La date se adaugă 2 m pe legătură: 1 m ordonat la distribuitor, 0,3 m în doză și restul la tăiere.'%(T15,esc(where(DVR['M018'])),T25,esc(where(DVR['M019'])),' + '.join(d['id']+' '+f(d['buy']) for d in cat),f(sum(d['buy'] for d in cat)),' + '.join(d['id']+' '+f(d['buy']) for d in cox),f(sum(d['buy'] for d in cox))),10)
end()
'''
rep("startp('01','Priza de lângă geam / P02'", K1 + "startp('01','Priza de lângă geam / P02'")

# ---- planșa finală
rep("startp('FIN','Ce s-a verificat / ce se confirmă la montaj','R04 înlocuiește reprezentarea traseelor din R03')",
    "startp('FIN','Ce s-a verificat / ce se confirmă la montaj','R05 = traseele R04 + mobilierul actual pe fundal + cablul pe circuite (K1)')")
rep("R04: poziționare și trasee complete. R02: aparataj și preselecție circuite, de validat. Lungimile vechi R02/R03 nu se folosesc ca listă finală de comandă după aceste corecții. CSV-ul R04",
    "R05: poziționare, trasee complete și cablul pe circuite (K1). Plan electric R03: aparataj, protecții și produsele alese, cu preț. Lungimile vechi din R02/R03 nu se mai folosesc. CSV-ul R05")

exec(compile(SRC, 'electric_r04_complet+R05', 'exec'))
