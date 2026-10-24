"""Plan electric R03: aceleași planșe ca R02 (plan_electric_pdf.py, nemodificat), refăcute cu deciziile de după:
- fundalul are mobilierul actual din modelul 3D;
- LED-ul dulapului din hol pornește din 4 senzori de ușă IR, lângă balamaua de sus (E02, E13);
- tabloul: 10 RCBO + 2 AFDD cu RCBO, tablou Noark 54 module (E09);
- E14 / E15: produsele alese în devizul R03, cu preț și link;
- E15 / E17: cablurile calculate exact pe traseele din montajul electric R05 (Cat6 și coaxial câte unul pe priză,
  230 V cu traseul comun al circuitului numărat o singură dată);
- E12: poziția routerului față de ușile cu oglindă ale dulapului din hol (decizie deschisă).
Rulează cu Python-ul care are reportlab, după montaj_electric_R05.py.
Iese: output/pdf/Apartament_184_Plan_electric_R03.pdf, Apartament_184_Registru_electric_R03.csv, tmp/electric_plan.json"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from plan_comun import *

R5 = json.loads(routes_file().read_text(encoding='utf-8'))['routes']
R5LEN = {r['id']: r['length_m'] for r in R5}
SRC = (ROOT / 'scripturi/plan_electric_pdf.py').read_text(encoding='utf-8')


def rep(a, b, n=1):
    global SRC
    assert SRC.count(a) == n, (SRC.count(a), a[:90])
    SRC = SRC.replace(a, b)


def block(start, stop, new):
    """înlocuiește planșa dintre sheet(start...) și sheet(stop...)"""
    global SRC
    i, j = SRC.index("sheet('%s'," % start), SRC.index("sheet('%s'," % stop)
    SRC = SRC[:i] + new.lstrip('\n') + SRC[j:]


rep('Apartament_184_Plan_electric_R02.pdf', 'Apartament_184_Plan_electric_R03.pdf')
rep("prefix=prefix.replace('R01 |','R02 |')", "prefix=prefix.replace('R01 |','R03 |')")
rep('exec(prefix)\n', 'exec(patch_prefix(prefix))\n')
rep("c.setTitle('Apartament 184 - Instalatii electrice curenti tari si slabi - R02')",
    "c.setTitle('Apartament 184 - Instalatii electrice curenti tari si slabi - R03')")
# lungimile Cat6 / coax de pe traseele complete R05, +2 m rezervă pe legătură
rep("BOXES=[('J01'", "for p in points:\n if p['id'] in R5LEN and p['kind'] in ('D','T'):p['route_m']=round(R5LEN[p['id']]+2,1)\nBOXES=[('J01'")

# ---- E00
rep("table(42,450,[70,440,596],", "_y=table(42,450,[70,440,596],")
rep("['E14-E17','Cantități, cabluri, verificări și surse','Ofertare, rezervă, recepție']",
    "['E14-E17','Produsele alese cu preț, cabluri calculate exact, verificări și surse','Cumpărare și recepție']")
rep("'Montaj și coordonare cu pereții / mobilierul'] ],10)\nend()",
    "'Montaj și coordonare cu pereții / mobilierul'] ],10)\n"
    "para(42,_y+16,1106,'<b>Ce e nou în R03:</b> fundalul are mobilierul actual din modelul 3D; LED-ul dulapului din hol pornește din 4 senzori de ușă; "
    "tabloul are 10 RCBO + 2 AFDD cu RCBO (C01, C04); produsele alese au preț și magazin (E14, E15); cablurile sunt calculate exact pe traseele "
    "din montajul electric R05 (E15, E17). Poziția routerului față de dulapul din hol e decizie deschisă (E12).',10)\nend()")

# ---- E02 / E13: LED dulap hol pe senzori de ușă IR
rep('Dressing: 5 senzori de uși, alimentare permanentă a sursei 24V.',
    'Dressing: 5 întrerupătoare de ușă 24 V. Dulap hol: 4 senzori de ușă IR 24 V, lângă balamaua de sus a celor 4 uși mari, '
    'câte 2 în paralel pe modul; LED-ul se aprinde când se deschide ușa. Sursele 24 V au alimentare permanentă.')
rep('Dressing: 5 benzi ≈3,17 m total și 5 senzori;',
    'Dressing: 5 benzi ≈3,17 m total și 5 întrerupătoare de ușă; dulap hol: LED în ambele module, 4 senzori de ușă IR 24 V '
    '(câte 2 în paralel pe modul), sursa F04;')

# ---- E09: tablou ales
rep("(778,'DISTRIBUȚIE / 12 RCBO','Plecări 1P+N cu 30mA; neutrul propriu fiecărui circuit și bară PE continuă. Tip/curbă după receptor.')",
    "(778,'DISTRIBUȚIE / 10 RCBO + 2 AFDD','10 RCBO 1P+N 30 mA tip A și 2 AFDD cu RCBO pe C01 și C04. Neutrul propriu fiecărui circuit, bară PE continuă.')")
rep('<b>Carcasă orientativă:</b> 54 module, de verificat după RCBO/SPD și cele 2 AFDD prevăzute pentru C01 și C04 (circuite dormitor). Se păstrează ≈20% rezervă.',
    '<b>Tablou ales:</b> Noark 54 module aparent (3 rânduri × 18), cu separator 2P 40 A, SPD T2, 10 RCBO ETI KZS-1M și 2 AFDD+RCBO Schneider A9TDE3616 '
    'pe C01 și C04 (dormitor). Se verifică locul după aparatele cumpărate; se păstrează ≈20% rezervă.')

# ---- E12: routerul și ușile cu oglindă
rep("'<b>Wi-Fi</b><br/>Holul este o propunere accesibilă, dar acoperirea prin pereții dintre camere se verifică după instalare.",
    "'<b>Wi-Fi / decizie deschisă</b><br/>Punctul NET (X7900, Z2000) cade în spatele dulapului din hol, care are uși cu oglindă; oglinda "
    "atenuează semnalul. ONT-ul și patch-panelul pot sta într-un compartiment al dulapului, cu acces din față, dar routerul Wi-Fi rămâne în afara "
    "lui. Se decide până la electricul brut (13–21.10). Acoperirea prin pereții dintre camere se verifică după instalare.")

# ---- E14: aparataj, protecții, iluminat
block('E14', 'E15', r'''
sheet('E14','Lista de cantități / aparataj, protecții și iluminat','Produsele alese în devizul R03, la cea mai bună ofertă găsită pe 05.10.2026, prețuri cu TVA; magazinele sunt linkuri')
ns=sum(p['n'] for p in points if p['kind']=='P')
EX={'M018':'C01–C03, calcul exact în E17','M019':'C04–C12, calcul exact în E17','M020':'copex pe toate traseele; doze de aparat și J01–J06',
 'M021':str(ns)+' mecanisme Schuko în 23 de grupuri (P01–P23)','M022':'S01–S08; S03 și S08 sunt duble','M023':'tabloul TE de deasupra ușii',
 'M024':'C02, C03 pe B10; C05–C12 pe B16','M025':'C01 și C04 (dormitor): AFDD și RCBO într-un singur aparat','M026':'îmbinări numai în doze accesibile',
 'M027':'baie: aparataj IP44, alimentarea ventilatorului F07','M034':'L01–L08; baie și balcon în variantă IP44','M036':'dulap hol, dressing, debara, bucătărie, comode TV, riflaje, oglindă, noptiere',
 'M038':'F01–F06 și noptierele F08A/F08B','M039':'dulap hol 4 (lângă balamaua de sus a ușilor mari) + dressing 5'}
IDS=['M018','M019','M020','M021','M022','M023','M024','M025','M026','M027','M034','M035','M036','M037','M038','M039']
rows=[['Cod','Articol ales','Cant.','Total lei','Unde (cea mai bună ofertă)']]+[dvrow(i,extra=EX.get(i)) for i in IDS]
rows.append(['','<b>Total aparataj, protecții, cablu și iluminat</b>','','<b>'+lei(sum(DVR[i]['tmin'] for i in IDS))+'</b>','prețuri observate pe 05.10.2026; pot varia'])
tbl(42,148,[48,392,62,62,542],rows,9,3,total=True)
end()
''')

# ---- E15: date și TV, câte un cablu pe priză
block('E15', 'E16', r'''
sheet('E15','Curenți slabi / cabluri și necesar','Fiecare priză are cablul ei până la distribuitorul NET (legare în stea); lungimi pe traseele din montajul electric R05')
lan=[p for p in points if p['kind']=='D'];coax=[p for p in points if p['kind']=='T']
DL=data_lines(R5);f=lambda v:('%.1f'%v).replace('.',',')
rows=[['ID','Legătură individuală','Traseu m','De cumpărat m','Cablu']]
for d in DL:rows.append([d['id'],esc(d['desc']),f(d['geo']),f(d['buy']),'Cat6 cupru integral, fără îmbinare' if d['kind']=='D' else 'Coaxial RG6 75 Ω, fără îmbinare'])
rows.append(['','<b>Total</b>','','<b>Cat6 '+f(sum(d['buy'] for d in DL if d['kind']=='D'))+' m<br/>coax '+f(sum(d['buy'] for d in DL if d['kind']=='T'))+' m</b>','+2 m pe legătură: 1 m la distribuitor, 0,3 m în doză, restul la tăiere'])
y=tbl(42,148,[60,420,100,170,356],rows,10,4,total=True)
IDS=['M028','M029','M030','M031','M032','M033']
rows=[['Cod','Articol ales','Cant.','Total lei','Unde (cea mai bună ofertă)']]+[dvrow(i) for i in IDS]
rows.append(['','<b>Total curenți slabi</b>','','<b>'+lei(sum(DVR[i]['tmin'] for i in IDS))+'</b>','Cat6 se poate lua și la metru (~50 m), dacă găsești cupru integral'])
y=tbl(42,y+18,[48,392,62,62,542],rows,9,3,total=True)
para(42,y+12,1106,'Nu se trece cablul de date dintr-o priză în alta. Cat6 se testează pe fiecare legătură (permanent-link), coaxialul cu nivelul de semnal la fiecare priză; porturile libere ale distribuitorului se închid cu terminator 75 Ω. HDMI H01/H02 rămâne local, între TV și comodă, în tub propriu.',10)
end()
''')

# ---- E17: cabluri 230 V exacte
block('E17', 'E18', r'''
sheet('E17','Cabluri 230 V / calcul exact pe circuite','Pe traseele complete din montajul electric R05; aparatele de pe același circuit se leagă unul după altul, traseul comun se numără o singură dată')
CC=cable_circuits(R5);T15,T25=cable_totals(CC)
rows=[['Circuit','Ce alimentează / aparate','Buc.','Cablu','Traseu comun m','Urcări între prize m','Tablou 1 m + 0,3 m / aparat','Total m']]
for r in CC:
 rows.append(['<b>'+r['id']+'</b><br/>'+r['prot'],r['dest']+'<br/><font color="#536473">'+r['ids']+'</font>',str(r['n']),r['sec']+' mm²',('%.1f'%r['union']).replace('.',','),('%.1f'%r['urcari']).replace('.',',') if r['urcari'] else '-',('%.1f'%(r['te']+r['capete'])).replace('.',','),'<b>'+('%.1f'%r['total']).replace('.',',')+'</b>'])
rows.append(['','<b>Total de cumpărat</b>','','','','','','<b>3×1,5: %d m<br/>3×2,5: %d m</b>'%(T15,T25)])
y=tbl(42,148,[78,372,46,82,110,130,160,128],rows,9,4,total=True)
para(42,y+14,525,'<b>Metoda</b><br/>Traseul comun e lungimea reuniunii segmentelor circuitului: tabloul, culoarul de la Z2400, ramurile și coborârile. La prize, cablul coboară la priză și urcă înapoi la tavan spre următoarea, mai puțin la ultima. Se adaugă 1 m la tablou și 0,3 m la fiecare aparat; întrerupătoarele au coborârea lor în traseu. LED-ul de 24 V de la noptiere (F08A/B) nu intră aici.',10)
para(620,y+14,528,'<b>Față de R02</b><br/>Bugetul vechi (110 m de 3×1,5 și 170 m de 3×2,5) aduna separat traseul fiecărui punct până la tablou. Pe traseele exacte ies %d m și %d m.<br/><b>Cumpărare:</b> 3×1,5 o rolă de 100 m; 3×2,5 o rolă de 100 m + 37 m la metru (deviz M018, M019). Conductorii din tub se listează pe culori după schema finală.'%(T15,T25),10)
end()
''')

# ---- registru și date
rep("'revision':'R02'", "'revision':'R03'")
rep("(ROOT/'tmp/electric_plan.json').write_text(", "model['cable_exact']={'circuits':CC,'3x1.5_m':T15,'3x2.5_m':T25,'data':DL};(ROOT/'tmp/electric_plan.json').write_text(")
rep('Apartament_184_Registru_electric_R02.csv', 'Apartament_184_Registru_electric_R03.csv')

exec(compile(SRC, 'plan_electric_pdf+R03', 'exec'))
