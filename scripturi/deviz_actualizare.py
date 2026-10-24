"""Actualizeaza devizul inceput, pastrand o copie a datelor initiale."""
from pathlib import Path
import json, math, copy, collections
ROOT=Path(__file__).resolve().parents[1]
baseline=ROOT/'tmp/deviz_initial_claude.json'
if not baseline.exists(): baseline.write_bytes((ROOT/'tmp/deviz.json').read_bytes())
D=json.loads(baseline.read_text(encoding='utf-8')); rows=D['rows']
for r in rows:
    r['st']='estimat';r['url']='';r['price_basis']='Interval preluat din devizul inițial; ofertă de confirmat.'
    r['note']=r['note'].replace('verificat','preluat')
def row(prefix):return next(r for r in rows if r['art'].startswith(prefix))
def update(prefix,**fields):row(prefix).update(fields)
def add(cat,art,q,um,pmin,pmax,note,url='',st='estimat',price_basis='Buget provizoriu, produs/ofertă de confirmat.'):
    rows.append(dict(cat=cat,art=art,q=q,um=um,pmin=pmin,pmax=pmax,note=note,url=url,st=st,price_basis=price_basis))
def price(prefix,lo,hi,url,note):
    update(prefix,pmin=lo,pmax=hi,url=url,st='verificat',price_basis=note)

# Aria este calculata din poligoanele CAD; diferentele fata de 49 m2 din notele vechi raman de verificat.
geo=json.loads((ROOT/'tmp/termic_model.json').read_text(encoding='utf-8'))
areas={}
for r in geo['rooms']:
    p=r['polygon'];areas[r['name']]=abs(sum(x*y2-x2*y for (x,y),(x2,y2) in zip(p,p[1:]+p[:1])))/2/1e6
interior=sum(v for k,v in areas.items() if k!='Balcon_placa');wet=areas['Pardoseala_Baie'];dry=interior-wet
update('Amorsă pentru șapă',note=f'Arie CAD interior {interior:.2f} m². Dozaj și suport de verificat; nu dublează amorsa inclusă în kiturile de finisaj.')
update('Șapă autonivelantă',art='Șapă autonivelantă Ceresit CN 68, 25 kg, zone interioare uscate',q=math.ceil(dry*5*1.5*1.05/25),note=f'{dry:.2f} m² × 5 mm × 1,5 kg/m²/mm + 5% pierderi. Grosimea de 5 mm este ipoteză; baie exclusă.')
price('Șapă autonivelantă',64.84,69.90,'https://www.dedeman.ro/ro/sapa-autonivelanta-ceresit-cn-68-interior-25-kg/p/5009284','Pagina de produs 64,84 lei; listă categorie 69,90 lei. Preț/localitate de confirmat; 05.10.2026.')
add(rows[0]['cat'],'Șapă cimentică compatibilă cu baia, 25 kg',2,'sac',65,100,f'{wet:.3f} m²; 5 mm și consum 1,6 kg/m²/mm sunt ipoteze. Sistem final după suport/hidroizolație.')
micro=row('Microciment:');micro.update(art='Kit microciment pardoseală impermeabilă, acoperire 10 m²/kit',q=2,um='kit',note='Hol + vestibul + baie = 10,58 m² CAD. Două kituri întregi; ofertă la suprafață exactă poate reduce surplusul.')
price('Kit microciment pardoseală',1899,2110,'https://www.cementart.ro/cemher/microciment-kit-pentru-10-mp-pardoseala-impermeabila','Cementart: promoție 1.899 / preț afișat anterior 2.110 lei per kit; 05.10.2026.')
add(micro['cat'],'Kit microciment pereți impermeabil, acoperire 10 m²/kit',2,'kit',2106,2340,'Pereți umezi baie: 12 m² ESTIMAȚI. Două kituri întregi; nișe și goluri de măsurat. Hidroizolația suportului se coordonează separat.','https://www.cementart.ro/cemher/microciment-kit-pentru-10-mp-pereti-100-impermeabil','verificat','Cementart: promoție 2.106 / preț afișat anterior 2.340 lei per kit; 05.10.2026.')
update('Rășină / vopsea',q=17,note='Bucătărie + debara + balcon = 15,08 m² CAD; buget 17 m² cu pierderi. Soluție simplă, nu strat autonivelant gros.')
update('Parchet stejar',note='30,24 m² CAD × 1,08 = 32,66 m²; 33 m² de buget, ambalaje finale de confirmat. Prețul vechi nu a fost reconfirmat.')

# Acoperirea aparatajului R04; lungimile de cablu raman buget preliminar, nu suma rutelor de alimentare repetate.
elect=json.loads((ROOT/'output/pdf/Apartament_184_Trasee_complete_R04.json').read_text(encoding='utf-8'))
update('Prize Schuko',q=sum(r['quantity'] for r in elect['routes'] if r['kind']=='P'),note='R04: 23 grupuri P, 35 mecanisme. Rame după grupare; baia și aparatajul cu protecție umiditate în lotul separat.')
update('Cablu 3 × 1,5',note='110 m buget preliminar R02. R04 verifică geometria, nu conductoarele. Retururi multiple, comenzi și alimentare ventilator cer schemă finală.')
update('Cablu 3 × 2,5',note='170 m buget preliminar R02. Nu se însumează toate rutele TE-aparat din R04: porțiunile comune sunt repetate în fișe. Lungimea finală după schema circuitelor.')
update('RCBO 1P+N',art='RCBO 1P+N 30 mA tip A, 2 × B10 + 8 × B16',q=10,note='10 circuite; C01 și C04 sunt bugetate separat cu protecție completă AFDD+RCBO. Selectivitate și capacitate de rupere de validat.')
update('AFDD pentru',art='Protecție completă AFDD + RCBO tip A pentru C01 / C04',pmin=450,pmax=900,note='2 ansambluri: B10 / B16 după circuite. Nu se dublează RCBO-ul inclus; preț de buget, produs final de ales.',url='https://www.voltashop.ro/tablouri-si-distributie-electrica/intrerupatoare-automate-si-fuzibile/sigurante-automate-si-accesorii/diferential-afdd-noark-ex9nla-el-b16-2p-tip-a-30ma-cu-detectie-arc-113632.html',price_basis='Exemplu B16 integrat la 455 lei; interval de buget pentru două modele, nu ofertă pentru B10.')
add(row('Prize Schuko')['cat'],'Supliment aparataj baie/IP, ieșiri de cablu și alimentare ventilator',1,'lot',150,300,'Buget diferență față de cele 35 Schuko de bază, nu alte prize. Ventilatorul existent se păstrează; racord/borne/temporizare după model.')
update('Cablu Cat6',q=52,note='R04: 4 linii individuale, 40,675 m geometric. Buget 52 m include capete, rezerve și pierderi; rutare finală după accesul la NET.')
update('Prize RJ45',note='4 porturi RJ45 D01–D04, patch-panel 8 porturi și patch-corduri. Componente compatibile Cat6 cupru integral.')
update('Cablu coaxial',note='R04: 3 linii T01–T03, 29,113 m geometric; buget circa 35 m + 3 prize + distribuitor. Set, preț orientativ.')
add(row('Cablu Cat6')['cat'],'Cabluri HDMI certificate, 3 m, legătură TV–comodă',2,'buc',70,160,'H01 living și H02 rezervă dormitor. Necesitate 1,062 / 1,010 m geometric; cablu 3 m pentru capete și buclă, probă înainte de închidere.')
add(row('Cablu Cat6')['cat'],'Tuburi HDMI Ø32–40 și ieșiri cu perie',2,'set',50,100,'Două trasee independente. Diametrul după mufă/curbură; nu dublăm tuburile de putere din lotul electric.')
update('Surse 24 V',q=8,note='6 grupuri F01–F06 + 2 noptiere F08A/F08B. Alimentarea TV/oglindă poate necesita surse suplimentare după lungime și putere reală.')

# Separare corp de cada de kitul neincluse, preturi si exemple comerciale.
update('Cadă Roca',art='Cadă Roca Contesa A236060000, 150 × 70, oțel emailat',note='IS01; suportul și masca nu sunt incluse în pagina comerciantului.')
price('Cadă Roca',855.93,855.93,'https://www.dedeman.ro/ro/cada-baie-dreptunghiulara-roca-contesa-a236060000-150-x-70-cm/p/3036495','Dedeman: 855,93 lei/cadă, localitate și stoc de confirmat; 05.10.2026.')
add(row('Cadă Roca')['cat'],'Kit susținere/fixare compatibil cadă Roca 150 × 70',1,'set',100,200,'IS02; separat de cadă. Kit final confirmat de producător/comerciant.')
add(row('Cadă Roca')['cat'],'Racorduri mașină de spălat în vestibul: apă, izolare, evacuare',1,'lot',250,600,'Provizion omis din planul sanitar al băii. Traseu, pantă și lungime după releveu; fără pompă presupusă.')
update('Radiator Purmo Compact 22, 600 × 1000',url='https://mathaus.ro/p/calorifer-otel-purmo-c22-1709-w-alb-600-x-1000-mm-accesorii-incluse/000000000010800589',note='IT01; exemplu de produs, interval vechi de buget. Puterea la termoficare și tipul racordului se validează; poziție păstrată.')
update('Radiator Purmo Compact 22, 600 × 1200',url='https://mathaus.ro/p/calorifer-otel-purmo-c22-2051-w-alb-600-x-1200-mm-accesorii-incluse/000000000010800592',note='IT02; 579 lei observat în lista MatHaus. Interval de buget păstrat; selecție condiționată de regimul termic.')
update('PAL Egger W1000 ST9 18',note='16 plăci de buget: 11 din debitare + 5 pentru bucătărie. Bucătăria rămâne estimativă; preț Regency folosit ca reper, atelierul final Debimax/Mambricolaj.')
price('PAL Egger W1000 ST9 18',366.42,566.85,'https://regencycompany.ro/pal-egger-alb-premium-w1000-st9-18mm-2-80-x-2-07','Regency: 366,42 promoție / 566,85 standard, TVA inclus, 05.10.2026. Nu este ofertă de atelier Debimax/Mambricolaj.')
update('Dulap hol: balamale',url='https://regencycompany.ro/balama-blum-clip-top-aplicata-110-grade-70t3550tl',note='Lotul complet rămâne estimat. Exemplu balama 70T3550.TL: 9,48 lei, plăcuță separată; glisiere/TIP-ON de ofertat. Se folosește BOM dulap hol pentru comandă.')
update('Birou IKEA',note='Model ales 120 × 70 cm. Preț fără livrare; stoc de confirmat.')
price('Birou IKEA',999,999,'https://www.ikea.com/ro/ro/p/trotten-birou-cu-inaltime-reglabila-electric-alb-s49621871/','IKEA: 999 lei, pagina consultată 05.10.2026.')
update('Mașină de spălat rufe Heinner',url='https://www.vexio.ro/masini-spalat-rufe/heinner/3270142-hwm-hme1014iva10-plus-plus-plus-10-kg-1400-rpm-clasa-a-alb/',note='Produs ales. Comparatorul și pagina comerciantului afișează prețuri diferite; interval de buget, de reconfirmat la comandă.')
update('Microunde incorporabil',url='https://www.domo.ro/cuptor-cu-microunde-incorporabil-heinner-hmw-mdbi28gdbk-28l-control-digital-900w-putere-grill-1000w-afisaj-led-sticla-neagra-pMCI1NzEvPiA-l/',note='Model ales; ofertă observată Domo 789 lei. Interval de buget, nu preț eMAG reconfirmat.')
update('Frigider side-by-side',url='https://www.emag.ro/side-by-side/brand/tcl/c',note='Model ales RP503SSE1. Interval preluat 2.500–2.900 lei; preț direct nereconfirmat. Link categorie, nu ofertă fermă.')
update('Televizor TCL 55C6K',url='https://www.emag.ro/televizoare/c',note='Model ales; 3.000 lei este buget preluat, nu preț direct reconfirmat. Link categorie.')
update('Televizor TCL 55P8L',url='https://www.compari.ro/televizor-c3164/tcl/55p8l-p1337224405/',note='Model ales; 2.500 lei este buget preluat. Ofertele promoționale pot fi mai mici; verificare la comandă.')
update('Suport TV Nexio',url='https://www.tehnotool.ro/suport-tv-de-perete-cu-brat-reglabil-nexio-nx-lpa52-446',note='2 suporturi. 185 lei/buc este buget preluat; VESA, fixări și preț final de confirmat.')
update('Pachet cuptor Arctic',note='Model ales în proiect; valoare preluată din cercetarea inițială, linkul ofertei nu a fost păstrat. Se cere ofertă pentru pachet complet.')
add(row('Chiuvetă compozit')['cat'],'Racord gaz plită, robinet și accesorii compatibile',1,'lot',150,350,'Buget provizoriu; traseu și soluție după instalația existentă și executant autorizat. Manoperă/avize excluse.')

# Exemple deja documentate in planul sanitar; linkul de selectie nu probeaza pretul.
links={'Rezervor încastrat':'https://catalog.geberit.ro/ro-RO/product/PRO_3933392','Vas WC suspendat':'https://www.roca.ro/produse/vas-wc-compact-suspendat-rimless-evacuare-orizontala-346244..0','Lavoar + mobilier':'https://www.roca.ro/produse/lavoar-suspendat-60cm-3270M1..0?sku=A3270M1000','Sifon cadă':'https://www.alcadrain.ro/produse/sifoane-pentru-cada/ovladane/a55km-detail','Paravan cadă':'https://configurator.radaway.ro/paravane-de-cada/serie','Țevi și fitinguri apă':'https://www.geberit.ro/sisteme-sanitare-tevi/sisteme-de-alimentare-cu-apa/geberit-flowfit/','Canalizare PP':'https://www.geberit.ro/sisteme-sanitare-tevi/sisteme-de-drenaj/geberit-silent-pp/','Hidroizolație Ceresit':'https://www.ceresit.ro/servicii/aplicatii/placari/solutii-de-hidroizolare-pentru-camere-umede.html','Portprosop Purmo':'https://www.purmo.com/ro-ro/produse/14407/santorini/','Robinet termostatic':'https://assets.danfoss.com/documents/latest/208753/AB370141588735ro-RO0101.pdf'}
for prefix,url in links.items(): update(prefix,url=url)
order={s['cat']:i for i,s in enumerate(D['summary'])};rows.sort(key=lambda r:order[r['cat']])
for i,r in enumerate(rows,1):
    r['id']=f'M{i:03}';r['tmin']=round(r['q']*r['pmin'],2);r['tmax']=round(r['q']*r['pmax'],2)
cats=list(order)
S=[dict(cat=c,tmin=round(sum(r['tmin'] for r in rows if r['cat']==c),2),tmax=round(sum(r['tmax'] for r in rows if r['cat']==c),2),n=sum(r['cat']==c for r in rows),ver=sum(r['cat']==c and r['st']=='verificat' for r in rows)) for c in cats]
D.update(rows=rows,summary=S,tot_min=round(sum(s['tmin'] for s in S),2),tot_max=round(sum(s['tmax'] for s in S),2),ver_sum=sum(r['tmin'] for r in rows if r['st']=='verificat'),areas=areas,interior_area=interior,revision='R01',date='05.10.2026')
D['old_total']=[json.loads(baseline.read_text(encoding='utf-8'))[k] for k in ('tot_min','tot_max')]
D['notes']=['Materiale, echipamente, livrări și taxe de atelier. Manopera de șantier este exclusă.','Minim/maxim sunt scenarii de buget pe articole. Media este media aritmetică, nu ofertă sau cost garantat.','7% rezervă financiară se adaugă după subtotal. Pierderile fizice/ambalajele sunt deja incluse numai unde sunt explicate.','Preț verificat înseamnă observație pe pagina indicată, nu toate produsele dintr-un lot. Estimat: interval de buget preluat ori adăugat.','Dulapul existent din dormitor și închiderea termopan a balconului se păstrează. Nu sunt bugetate ca achiziții noi.','Plăcile bucătăriei (~9) sunt estimative: nu există încă debitare completă. Totalul de 31 plăci nu este comandă validată.','Cablurile de putere 110/170 m rămân provizioane R02; cantitățile finale cer schema circuitelor pe rutele R04. R04 confirmă 35 Schuko, 4 RJ45, 3 coaxiale, 8 plafoniere și 8 comenzi.','Aria CAD interior este 51,09 m², diferită de circa 49 m² în notele vechi; suprafețele se confirmă în releveu.','Feroneria și uneltele speciale se confirmă după BOM; cantitățile de țevi/fitinguri rămân loturi de buget.','Nu sunt incluse demolări, evacuare moloz, montaj, proiecte/avize, golire/umplere termoficare, probe și punere în funcțiune, reparații ascunse sau decor suplimentar.']
(ROOT/'tmp/deviz.json').write_text(json.dumps(D,ensure_ascii=False,indent=2),encoding='utf-8')
assert sum(s['n'] for s in S)==len(rows)
assert all(r['pmin']<=r['pmax'] for r in rows)
print(json.dumps({'rows':len(rows),'subtotal':[D['tot_min'],D['tot_max']],'total_7pct':[round(D['tot_min']*1.07,2),round(D['tot_max']*1.07,2)],'price_rows_verified':sum(r['st']=='verificat' for r in rows)},ensure_ascii=False))
