# Apartament 184 – Bloc L14 (Locuințe Titan), Sector 3, București
Renovare și amenajare modernă pentru închiriere. Ultima actualizare: 05.10.2026.

## Fișiere (ultimele versiuni, după curățenia din 05.10.2026)
| Fișier | Ce este |
|---|---|
| `apartament_184.FCStd` | Modelul 3D FreeCAD al apartamentului: pereți, goluri, mobilier, electric. Componentele de mai jos sunt legate în el, deci rămân în același folder. |
| `dulap_hol`, `bucatarie`, `debara`, `dressing`, `spalatorie_vestibul`, `baie`, `noptiera`, `perete_TV`, `perete_TV_dormitor`, `masuta_cafea`, `conexiuni_TV`, `dulap_dormitor`, `corp_spate_pat` `.FCStd` | Componentele de mobilier și de baie, legate în apartament (ultimele două: dormitorul refăcut de Codex pe 06.10) |
| `instalatie_electrica_R02.FCStd`, `montaj_electric_R04.FCStd` (+ `montaj_electric_R03.FCStd`, legat ascuns în apartament) | Instalația electrică: puncte și trasee |
| `apartament_184_randare.blend`, `plan_3D.blend`, `apartament_184.blend` | Scena de randare, vederea 3D de sus, importul brut din FreeCAD |
| `randari/zi`, `randari/noapte`, `randari/web`, `randari/Plan_3D_apartament_184.png` | Randările finale (zi și seară), variantele JPG, planul 3D adnotat |
| `Deviz_materiale_ap184_R04.xlsx` | Devizul de materiale R04 (06.10): plăci Kronospan din planul de debitare R03, dormitorul nou; cele mai bune oferte, etape, plăți pe săptămâni, calendar. R03 rămâne lângă el cât timp indexul Codex trimite la el |
| `Debitare_R03_comanda.xlsx` | Comanda de debitare R03: toate corpurile, o foaie pe decor (lungime, lățime, bucăți, fibră, cant pe laturi) + costuri Regency / Mambricolaj / Egger |
| `Dulap_hol_ap184_Debimax.xlsx` / `..._Mambricolaj.xlsx` | Liste de debitare, găurire, feronerie pentru atelier |
| `output/pdf/` | Planșele: plan de mobilare **R03**, electric R03 + montaj electric R05, sanitar R02, termic R02, plan de debitare **R03**, montaj dulap hol R03, deviz **R04**, plan de lucrări **R02** (versiunile anterioare rămân lângă ele cât timp `00_DESCHIDE_PROIECTUL.html` trimite la ele) |
| `scripturi/` | Scripturile care generează PDF-urile, Excelurile și randările. `plan_comun.py` = baza comună a planșelor (fundal de mobilier, prețuri din deviz, cabluri) |
| `tmp/` | Date intermediare citite de scripturi (nu se șterg) |
| `_arhiva/2026-10-05_versiuni_vechi/`, `_arhiva/2026-10-05_inlocuite_seara/` | Versiuni vechi și copii intermediare, fiecare cu index în `CITESTE-MA.md`; nimic nu e șters |

## Date de bază
- Înălțime liberă: **2,50 m**
- Suprafață locuibilă 30,22 m² (dormitor 12,22 + cameră de zi 18,00); utilă ≈ 49,0 m²; balcon 4,81 m²
- Pereții de 15 / 25 cm sunt structurali – NU se demolează. Doar pereții de 7,5 cm se pot modifica.
- Peretele holului spre casa scării este oblic (~14,5°).

## Reguli de lucru
- **Nu se generează PDF-uri până la versiunea finală.** Iterăm în modelul 3D și în chat.
- Materialele pentru mobilier se aleg din **Egger** și **Kronospan**, cu codul de decor.
- Debitare, cant și găurire: **Debimax** sau **Mambricolaj**.
- Feroneria se alege de la **Blum**.

## Decizii luate
### Amenajare (propunere aprobată ca bază)
- Cameră de zi: masă extensibilă la fereastră, canapea extensibilă de 220 cm, TV pe perete, bibliotecă joasă spre hol
- Dormitor: pat 160×200 cu ladă, dulap glisant de 220 cm, birou sub fereastră
- Bucătărie în L, cu frigider lângă ușă și chiuvetă sub fereastră
- Baie (revizuit): cadă 150×70 cm (lățime provizorie), WC suspendat cu rezervor încastrat și trapă laterală; lavoar pe același perete cu WC-ul. Mașina de spălat este mutată în vestibul. Poziția exactă a coloanelor și evacuării de verificat.

### Pardoseli și praguri (în FreeCAD și Blender)

| Încăpere | Finisaj |
|---|---|
| Camera de zi | parchet stejar |
| Dormitor | parchet clasic stejar |
| Bucătărie | rășină epoxidică gri, simplă și ieftină |
| Balcon | rășină epoxidică gri (strat peste placa existentă) |
| Vestibul, baie | microciment alb cald, cu pete și urme de gletieră (după poza de referință) |
| Hol | microciment (confirmat) |
| Debara | rășină epoxidică gri, ca în bucătărie (confirmat) |

- **Praguri înguste**, profil de aluminiu periat de 10 mm, la nivelul pardoselii, în dreptul ușii, **doar unde se schimbă materialul**:
  - U1 dormitor / vestibul;
  - U3 camera de zi / vestibul;
  - U4 camera de zi / hol;
  - U5 hol / bucătărie;
  - U8 camera de zi / balcon.
- U2 (baie / vestibul) și U6 (bucătărie / debara) au același material pe ambele părți, deci fără prag. În golurile tuturor ușilor pardoseala e completată cu finisajul fiecărei părți.
- În FreeCAD: grupul `Pardoseli_finisaje` + proprietatea `Finisaj` pe fiecare pardoseală. În Blender: materialele `R_Parchet_stejar`, `R_Microciment_alb_cald`, `R_Rasina_epoxidica_gri`, `R_Prag_aluminiu_periat`, în `apartament_184_randare.blend`.

### Dulap hol (custom) – FINALIZAT pentru debitare
- Pe tot peretele de jos al holului, cu capătul drept oblic. Lungime 2304 mm în spate și 2453 mm în față, adâncime 600 mm.
- Înălțime corp 2460 mm, cu picioare reglabile de 80 mm. Sus are o mască de compensare din U702, ajustată pe tavan la montaj.
- 2 module (~102 cm fiecare):
  - jos: sertar pentru pantofi (front de 366 mm până la 1 cm de podea, interior util ~18 cm);
  - mijloc: haine agățate (~157 cm liber; trenciuri în stânga, jachete în dreapta);
  - sus: compartiment pentru lucruri de sezon.
- Colț oblic: 4 rafturi deschise (W1000) și plintă la nivelul fronturilor.
- Uși: 8 uși cu oglindă de 4 mm cu folie de siguranță, push-to-open, fără mânere.
- LED: doar în cele 2 module. Profil sub polița de sus, bandă 24 V la 4000 K, senzori IR pe uși, sursă în compartimentul de sus.
- Materiale: Egger **W1000 ST9** pentru corp, rafturi și sertare; **U702 ST9** pentru fronturi, plintă și mască.
- Feronerie Blum:
  - CLIP top fără arc: 70T3550 ×6, 70T3650 ×18 (semiaplicat, cod de confirmat);
  - plăcuțe 173L6100 ×24;
  - TIP-ON 956.1004 ×8;
  - glisiere MOVENTO 760H5000S ×2 perechi, cu TIP-ON BLUMOTION și sincronizare.
- Montaj **în picioare, pe loc** (holul are doar 2 m adâncime, dulapul nu se poate monta culcat). Se prinde în perete cu colțare anti-răsturnare.
- Înainte de debitare: înălțimea finită a tavanului din hol trebuie să fie **≥ 2480 mm**.

### Bucătărie (în lucru) – fișier separat `bucatarie.FCStd`, importat ca link în apartament
- **Liniară** pe peretele din stânga ușii (lângă camera de zi), lungime 322 cm. Blatul e la ~91 cm, iar corpurile merg până la tavan, cu mască.
- Module, de la ușă spre geam:
  - chiuvetă 60 (lângă ușă, unde sunt acum țevile);
  - mașină de spălat vase incorporabilă 60;
  - corp 40;
  - plită pe gaz 60 (sertare dedesubt);
  - corp 40;
  - coloană 60, cu cuptor electric și microunde incorporabile, la nivelul ochilor.
- Sus: picurător (scurgător de vase) deasupra chiuvetei, hotă incorporabilă deasupra plitei, corpuri cu înălțime de 100 cm.
- Frigider în dreapta ușii, în colțul de sud-est. Masă de 80×60 cu 2 scaune pe peretele din dreapta, lângă geam.
- **Decis:**
  - frigider liber (nu incorporat): **TCL RP503SSE1 side-by-side**, 92 × 63 × 176,8 cm, 83 kg, dozator de apă cu rezervor (fără racord la apă). L-am rotit cu **spatele la peretele din dreapta** și fața spre blat, în colțul din dreapta ușii: ~12 cm până la colț, ~18 cm până la tocul debaralei, ~124 cm de trecere până la blat. Lângă ușă, cu spatele la perete, nu încăpea: rămâneau doar ~95 cm între toc și perete, iar ușile și aerisirea laterală n-ar fi avut loc;
  - ușa bucătăriei (U5) se întoarce: balama pe dreapta, se deschide spre frigider;
  - fronturi deocamdată la fel ca la dulap: Egger W1000 pentru corp și U702 pentru fronturi.
- **Electrocasnice alese (modelate exact în `bucatarie.FCStd`):**

| Aparat | Model | Dimensiuni | Unde | Putere |
|---|---|---|---|---|
| Cuptor electric 71 l | Arctic ARSE11130XD (inox) | 59,4 × 59,5 × 56,7 cm | în coloană, la 85–144,5 cm | 2,4 kW |
| Plită pe gaz 60 cm, 4 arzătoare (1 wok), aprindere electrică | Arctic (pachet cu cuptorul) | 60 × 51 cm | pe blat, modulul de 60 | – |
| Microunde 28 l, sticlă neagră, ușa cu balama pe stânga | Heinner HMW-MDBI28GDBK | 59,4 × 38,2 × 36,9 cm | în coloană, deasupra cuptorului (145–183 cm) | 900 W + grill 1000 W |

  Nișa minimă a cuptorului: 56 cm lățime. Decupajul exact pentru plită (în blat) și nișa microundelor se iau din fișele de montaj ale producătorilor înainte de debitare. Aranjarea arzătoarelor plitei din model e aproximativă.
- **Hotă:**
  - gura de evacuare existentă e pe **peretele cu geamul**;
  - tub plat de 150×70 mm: urcă vertical prin corpul de deasupra plitei (îmbrăcat într-o cutie în colțul din spate), apoi merge **pe deasupra corpurilor** spre peretele cu geamul, ascuns de masca de tavan (~2,1 m);
  - corpurile de sus și coloana au partea de sus la 241 cm; masca acoperă de la 241 până la tavan;
  - poziția exactă a gurii pe peretele cu geamul e **presupusă** (în colțul de deasupra coloanei); trebuie măsurată;
  - hota trebuie să aibă ≥ 600 m³/h, iar la gura de aerisire se pune clapetă anti-retur;
  - de verificat cu firma de gaze că gura nu e aerisirea obligatorie pentru gaz (dacă este, trebuie să rămână liberă).
- Aranjarea e înghețată deocamdată; nu se mai schimbă.
- Rămâne de ales: blatul (Egger / Kronospan), protecția de perete, feroneria Blum pentru bucătărie.

### Debara (nișa din dreapta bucătăriei) – fișier separat `debara.FCStd`, importat ca link
- Doar rafturi albe W1000, în 3 zone:
  - pe peretele cu geamul (35 cm adâncime);
  - pe peretele spre bucătărie, la stânga intrării (25 cm adâncime), cu **capătul dinspre ușă teșit**: pe ultimii 35 cm raftul se îngustează în diagonală de la 25 cm la 0, ca să ajungi ușor la rafturile din colț și de pe peretele cu geamul. Banda LED urmărește și diagonala;
  - în dreapta intrării, rafturi care umplu tot spațiul îngust până la peretele din spate (55 → 23 cm lățime, ~124 cm adâncime).
- 4 niveluri de rafturi, la 70 / 110 / 150 / 190 cm. Jos (sub 70 cm) e liber pentru lucruri voluminoase (aspirator, mop, baxuri de apă); sus (190–250 cm) la fel, pentru cutii mari.
- Bandă LED 24 V sub muchia din față a fiecărui raft. Sursa e sus, pe peretele cu geamul.
- Lumină LED centrală pe tavan (plafonieră slim, Ø ~24 cm).
- **Întrerupător dublu** în bucătărie, lângă ușa debaralei, **pe partea dinspre masă** (nu spre frigider, unde l-ar bloca ușa frigiderului deschisă). E la ~8 cm de gol, cu centrul la 105 cm: o tastă pentru benzile LED, una pentru lumina centrală.
- Ușa: **normală (batantă), de 70 cm, care se deschide spre bucătărie**, cu **balamaua pe partea frigiderului** și clanța spre masă. Glisanta nu are loc (masa și frigiderul ocupă peretele din ambele părți); spre interior n-ar avea loc din cauza rafturilor.

### Dressing camera de zi – fișier separat `dressing.FCStd`, importat ca link (în lucru, de verificat vizual)
- Pe tot peretele din stânga când intri din hol (peretele dinspre baie și vestibul), în locul bibliotecii joase. Are 338 cm, 60 cm adâncime, corp până la 246 cm, mască până la tavan, picioare reglabile, fronturi până la 1 cm de podea.
- Module (de la vest la est):
  - M1 ~70: 2 bare (cămăși / pantaloni);
  - M2 ~70: 2 sertare interioare + rafturi la 30 cm;
  - M3 ~57: masă de călcat incorporată (la ~85–89 cm), coș de rufe extractibil jos, rafturi sus, **priză pentru fierul de călcat în interior** (115 cm);
  - M4 ~70: 4 sertare interioare + rafturi;
  - M5 ~70: bară lungă + raft jos;
  - sus, peste toate: depozitare cu uși separate.
- Fronturi U702, push-to-open. LED sub polița de sus în fiecare modul, cu senzori de ușă; sursa e în M3; doză de 230 V deasupra dressingului.
- Întrerupătorul bucătăriei din hol e **dublu**: o tastă pentru lumina de pe tavan, una pentru LED-ul de sub corpuri.

## Note electrice (pentru planul electric)
- **Întrerupător hol:** în dreapta ușii de intrare când intri, adică pe partea clanței. E pe peretele oblic, la ~15 cm de toc, cu centrul la **105 cm** de la pardoseală. Rămâne de ales modelul și câte posturi are.
- **Întrerupător bucătărie:** în **hol**, imediat lângă ușa bucătăriei, pe partea clanței (stânga ușii, privind din hol). E la ~8 cm de gol, cu centrul la 105 cm. Pe partea dinspre bucătărie nu încape: între capătul blatului și toc rămân doar ~15 cm.
- **Întrerupător balcon:** în camera de zi, pe peretele cu fereastra, **chiar lângă tocul ușii balconului**, pe partea clanței. Centrul e la x ≈ 618 cm (~8 cm de gol) și la **105 cm**. Comandă plafoniera LED a balconului.
  - Ca să rămână liber: panoul 2 al draperiei din camera de zi se strânge acum la 626–671 cm (după întrerupător), iar șina de draperie e prelungită până la 680 cm (era 660).
- **Tablou electric:** **deasupra ușii de intrare**, montat aparent, de circa 40 × 25 cm (un singur rând, ~18 module). E jos la ~219 cm și sus la ~244 cm.
  - Peretele de deasupra ușii e probabil structural, spre casa scării, deci nu se îngroapă. Se verifică pe teren.
  - Pentru tablou compact se folosesc disjunctoare diferențiale (RCBO) de 1 modul.
  - Poziția trebuie acceptată de electricianul autorizat ANRE (Normativul I7).
- Doză de 230 V deasupra dulapului din hol, la ~240 cm, pentru sursa LED. Cablul se trage înainte de montajul dulapului.
- **Bucătărie – prize (cerute de beneficiar, puse în model):**

| Priză | Unde | Înălțime | Observații |
|---|---|---|---|
| Frigider (simplă) | perete dreapta, în spatele frigiderului, decalată spre colț | 55 cm | circuit separat recomandat |
| **Contrablat (dublă)** – una singură, pentru restul aparatelor | între chiuvetă și plită | 110 cm (~20 cm peste blat) | la ≥ 60 cm de chiuvetă, ≥ 30 cm de plită |
| Masă (dublă) | perete dreapta, deasupra mesei | 90 cm | |
| **Mașină de spălat vase + aprindere plită gaz (dublă)** | în spatele mașinii de spălat vase | 25 cm | circuit dedicat (MSV ~2 kW) |
| **Sub chiuvetă** | în spatele coșului de gunoi | 30 cm | |
| **Cuptor + microunde (dublă)** | în coloană, imediat sub cuptor (acces prin sertarul de jos) | 75 cm | circuit dedicat 16 A, 3×2,5 mm² (cuptor 2,4 kW + microunde ~1 kW) |
| **Hotă** | sus, în spatele hotei (în corpul de deasupra, lângă tub) | 180 cm | |

  (Revizie 05.10.2026, la cererea beneficiarului: a doua priză de contrablat și prizele separate pentru plită, microunde și cuptor au fost comasate ca mai sus.)

## De făcut / întrebări deschise
1. Plan electric complet: prize, iluminat, circuite, schema tabloului
2. Încălzire: termoficare sau centrală? Există gaz în bucătărie?
3. Aer condiționat: da/nu, în ce camere
4. Profilul chiriașilor și bugetul de renovare
5. Detaliu baie: hidroizolație, pante, poziția coloanelor
6. Ghid pas cu pas: ordinea lucrărilor, hidroizolație, șapă autonivelantă
7. Bucătărie custom (Egger, Blum) – combinată la debitare cu resturile de la dulap
8. La final: toate PDF-urile, manual de montaj în stil IKEA, desene de găurire, STEP refăcut

### Cameră de zi – continuare Codex, 05.10.2026
- Beneficiar: chirie pe termen lung pentru o persoană sau un cuplu; dressingul mare se păstrează.
- `sufragerie_variante.FCStd`: două studii separate, cu masă dreptunghiulară 120×75 orientată de-a lungul peretelui sau masă rotundă Ø90. Nu sunt variante aprobate. Modelul principal păstrează mobilierul anterior.
- Adăugat în modelul principal: `Intrerupator_camera_de_zi`, în interior lângă intrarea din hol U4, pe partea clanței conform planului, centru la 105 cm și la 8,5 cm de marginea golului. Poziție model: x≈7090, y=-3865, z=1050 mm. Sensul real al ușii și cota pardoselii finite trebuie confirmate. Funcția tastei: lumina generală a camerei de zi; circuitul se stabilește în planul electric.

### Spălătorie vestibul – concept, 05.10.2026
- Beneficiarul a corectat linkul: numai mașină de spălat **Heinner HWM-HME1014IVA10+++**, 10 kg, 1400 rpm; fără uscător în acest corp.
- Fișier separat `spalatorie_vestibul.FCStd`, cu link în apartament. Mașina schematică veche din baie este ascunsă, păstrată pentru referință.
- Corp propus: **1000 × 650 × 2460 mm**, mască până la tavan, în capătul vestibulului. Egger W1000 ST9 corp / U702 ST9 fronturi.
- Vestibul: 1025 × 1630 mm; cu corpul închis rămân 980 mm în față. Corpul ocupă ultimii 50 mm ai golului U3: acces nominal rămas ~850 mm; se confirmă cu tocurile și finisajele reale.
- Mașina ridicată pe platformă portantă independentă la 500 mm de pardoseala modelată. Structură metalică schematică, NU dimensionată pentru execuție. Manualul Heinner permite platformă înaltă numai cu asigurare împotriva răsturnării. Suportul, prinderile și întreaga sarcină dinamică se dimensionează separat.
- Sub mașină: sertar cu două coșuri detașabile pentru sortare; separat, poliță extractibilă cu cursă propusă de 450 mm pentru coșul folosit la încărcare/descărcare. Feronerie Blum MOVENTO, lungime/sarcină de ales; blocare la deschidere pentru poliță. Glisierele nu susțin mașina.
- Deasupra mașinii: nișă pentru detergenți și balsam la ~1420–1800 mm, cu tavă detașabilă; dulap superior până la ~2470 mm. Coloană laterală pentru accesorii și acces la racorduri.
- **Conflict verificat:** ușa băii U2 deschisă spre vestibul intersectează corpul de 650 mm. Deschiderea spre baie este propunere necesară acestei variante; nu este decizie de execuție. Spațiul față de WC real, mânerul și arcul complet trebuie verificate.
- Date manual: 595 × 590 × 845 mm, 61 kg. Schema dimensională arată și 580 mm adâncime închisă, 1040 mm cu ușa deschisă; pentru concept rezervăm conservator 590 mm închis și 50 mm spate. Exteriorul/hubloul/panoul sunt schematice, nu model detaliat de producător.
- Manual: minimum 25 mm lateral/deasupra și 50 mm spate în schema de montaj. Modelul rezervă ~34,5 / 52,5 mm lateral și 65 mm deasupra. Racordurile reale și demontarea pentru service se verifică înainte de debitare.
- Sursa: https://heinner.ro/electrocasnice/wp-content/uploads/sites/5/2026/09/manual_de_utilizare_HWM-HME1014IVA10____68aed84fbbb54.pdf
- Robinet, scurgere și priză în compartiment accesibil lateral: poziții conceptuale, de proiectat cu instalator/electrician. Înălțimea scurgerii la aparat ridicat se confirmă cu instrucțiunile producătorului; nu se execută după simbolurile din model.
- **Status: concept de discutat, nu listă de debitare / proiect tehnic.**

### Prize și LED – completare la cererea beneficiarului, 05.10.2026
- Adăugate în grupul `Electric` din apartament:
  - `Priza_masina_spalat_vestibul`: simplă, centru 650 mm, în compartimentul tehnic lateral accesibil; înlocuiește simbolul provizoriu din fișierul spălătoriei (ascuns).
  - `Priza_TV`: simplă la 1350 mm, în spatele ecranului, pe peretele spre dormitor; poziția conectorilor și distanța suportului se confirmă cu aparatul real.
  - `Priza_soundbar`: separată, simplă la 900 mm, sub televizor și deasupra comodei.
  - `Prize_birou_4`: patru prize la 650 mm, sub blatul biroului din dormitor și sub parapetul ferestrei.
  - `Priza_canapea_dubla`: două prize la 300 mm, pe peretele dinspre bucătărie, lângă capătul canapelei dinspre balcon; ~150 mm dincolo de canapeaua actuală.
- Dressingul din sufragerie avea deja cinci benzi LED și sursă 24 V. Au fost adăugați în `dressing.FCStd` cinci senzori de ușă, câte unul pentru fiecare modul; LED 4000 K. Alimentarea `Doza_LED_dressing` existentă este păstrată și etichetată explicit pentru această funcție.
- Cotele reprezintă pozițiile centrului în model, de coordonat cu pardoseala finită. Prizele, circuitele, cablurile și montajul în raport cu pereții structurali rămân de stabilit în planul electric; acestea sunt simboluri de poziționare, nu proiect de instalații.

### Televizoare (modelate exact)
- **Camera de zi:** **TCL 55C6K Pro** (122,9 × 71,3 × 5,6 cm, 12,2 kg, VESA 300×300, Onkyo 2.1 + Dolby Atmos), pe peretele dinspre dormitor, centrat pe modulul multimedia (y ≈ 275 cm), centru ecran la 140 cm.
- **Dormitor:** **TCL 55P8L** (122,4 × 70,8 × 7,0 cm, 11 kg, VESA 300×300), pe peretele dinspre camera de zi, centrat pe pat și pe modulul multimedia (y ≈ 180 cm), centru ecran la 141 cm.
- **Suporturi:** câte un **Nexio NX-LPA52-446** full-motion (32–55", max 40 kg, 5,3–46,4 cm de la perete, rotire ±60°, înclinare +5°/−15°), modelat strâns la perete. Placa de perete și brațul sunt **deasupra prizelor** (150–174 cm), ca prizele să rămână accesibile. Fără intersecții.
- Vechile volume generice `TV` și `TV_dormitor` au fost înlocuite.

### Perete TV camera de zi – fișier separat `perete_TV.FCStd`, importat ca link (după poza de referință)
- Pe peretele dinspre dormitor, între birou și ușa U3: **260 cm** (y 135–395).
- **Baghete decorative** (poliuretan, de vopsit în culoarea peretelui), între 66 și 236 cm înălțime:
  - panou central de 160 cm, cu televizorul;
  - două panouri laterale de 45 cm.
- **Aplice liniare verticale negre** (~65 cm) în mijlocul panourilor laterale.
- **Comodă suspendată** 240 × 40 × ~40 cm, la 20 cm de podea:
  - 3 fronturi greige (U702), blat stejar (propunere Egger H1145);
  - **LED sub comodă**, spre podea, și **LED pe perete** deasupra blatului.
- **Cornișă cu LED indirect** la tavan, pe toată lățimea compoziției (15 cm adâncime, 10 cm înălțime).
- Televizorul TCL 55C6K Pro a fost **mutat cu 10 cm** (centrat la y ≈ 265 cm); prizele multimedia rămân în spatele ecranului.
- Vechea comodă TV a fost scoasă. Scaunul de birou e mutat cu 15 cm spre cameră.
- Prizele multimedia de jos ajung în interiorul comodei; la montaj se face un **decupaj în spatele comodei**.
- **Spoturile încastrate** din poză **nu** sunt modelate: în planșeul de beton nu se pot încastra, ar cere tavan fals din rigips.
- De stabilit: comanda iluminatului (LED-uri și aplice pe circuite / întrerupătoare separate), modelul aplicelor, profilul exact al baghetelor.

### Perete TV dormitor + riflaje + machiaj – fișier separat `perete_TV_dormitor.FCStd`, importat ca link
- Pe peretele dinspre camera de zi, între fereastră și zona în care se sprijină ușa U1 deschisă (de la y 298): **~263 cm** disponibili.
- **Riflaje** de la podea la tavan, y 118–268 (150 cm):
  - 37 de lamele de stejar deschis (2,7 × 2,1 cm, pas 4 cm), pe suport de pâslă de 0,9 cm;
  - **decupaj** în dreptul modulului TV (priză, RJ45, coax, HDMI), ca să rămână accesibil în spatele televizorului.
- **LED vertical** pe muchia riflajelor dinspre fereastră și draperie, de la podea la tavan.
- **Comodă TV suspendată** 170 × 35 cm, din stejar, cu 2 sertare, la 30–58 cm, cu LED dedesubt. Se oprește la y 290, ca ușa dormitorului să se deschidă complet.
- Televizorul TCL 55P8L rămâne centrat pe pat; e mutat cu 3 cm în fața riflajelor.
- **Zonă de machiaj** lângă fereastră:
  - birou suspendat 80 × 40 cm, cu 2 sertare, blat la 75 cm;
  - **oglindă pe toată lățimea mesei (80 cm), de la blat (75 cm) până la tavan**, la fel de sus ca riflajele (~80 × 174 cm), **fără decupaj**; LED-ul e pe laterale, nu în spatele oglinzii (revizie 06.10.2026, vezi mai jos);
  - puf rotund bouclé Ø40;
  - **priză dublă pe peretele cu fereastra**, în colțul dintre fereastră și oglindă (x ≈ 340 cm), la 90 cm, **ascunsă de draperia strânsă** (x 328–350). A fost mutată de pe peretele oglinzii, ca oglinda să nu mai aibă decupaj.
- Culoarul dintre pat și comodă e de ~1 m. Fără intersecții.

### Măsuțe de cafea – fișier separat `masuta_cafea.FCStd`, importat ca link (după poza de referință)
- Pereche de măsuțe suprapuse, între canapea și peretele TV, în locul vechii măsuțe:
  - **mare:** blat oval de travertin 110 × 65 × 3,5 cm, sus la 35 cm, pe un picior cilindric de stejar Ø36;
  - **mică:** blat rotund de stejar Ø60, sus la 25 cm, pe un picior cilindric Ø40; intră parțial sub blatul mare.
- Fără intersecții; ~67 cm până la canapea, ~72 cm până la comoda TV.

### Transfer în Blender (05.10.2026)
- Export din FreeCAD cu `scripturi/export_freecad_blender.py`: **473 de piese**, câte un OBJ per piesă (coordonate globale, mm), plus `blender_export/furniture_manifest.json` cu ID, sursă, plasare, dimensiuni și culoare. Componentele legate sunt parcurse recursiv. Obiectele vechi, ascunse și înlocuite **nu** sunt exportate; tavanul balconului e exportat, dar ascuns.
- Import în Blender 5.2 (în fundal) cu `scripturi/import_blender.py` → **`apartament_184.blend`**:
  - 473/473 de piese importate, **0 erori de dimensiuni** (toleranță 0,5 mm);
  - scară aplicată (mm → m), 108 materiale de bază din culorile FreeCAD, 23 de colecții, câte una pe componentă;
  - fiecare obiect păstrează `part_id`, documentul și obiectul sursă.
- Verificare: randări Workbench în `blender_export/verificare/` (de sus și în perspectivă). Orientarea și pozițiile corespund cu FreeCAD; gabarit 11,15 × 7,00 × 2,65 m.
- Urmează pentru randări fotorealiste: materiale reale (decoruri Egger, travertin, stejar, textile, sticlă), tavane, iluminat (fereastră + lumini interioare), camere pe încăperi, Cycles.
- **Sursa dimensiunilor rămâne FreeCAD.** La modificări se reexportă bundle-ul și se reface importul.

### Noptiere – fișier separat `noptiera.FCStd`, două link-uri în dormitor
- După poza de referință: corp greige mat (U702), 2 sertare fără mânere, nișă deschisă cu **bandă LED** sub blat, **blat „plutitor”** de 4 cm sprijinit pe un bloc lateral retras.
- Dimensiuni ~**50 × 40 × 52 cm**; blatul iese 2 cm în față.
- Două variante în oglindă (A la nord, B la sud), cu suportul blatului spre pat. Stau la 5 cm de pat, iar prizele de 65 cm rămân imediat deasupra blatului. Fără intersecții.
- De stabilit: materialul exact (propunere U702, ca restul fronturilor), feroneria (sertare push-to-open Blum) și alimentarea LED-ului (din priza de lângă noptieră).

### Balcon existent închis – corecție model, 05.10.2026
- Beneficiarul confirmă că balconul este deja **închis cu termopan și are tavan normal deasupra**. Nu se tratează ca lucrare nouă de închidere.
- Adăugat în apartament grupul `Balcon_inchis`: tâmplărie și vitraj pe fața frontală și cele două laturi, deasupra parapetului existent de 1000 mm; tavan cu intrados presupus la 2500 mm.
- Patru panouri pe fața frontală și două pe fiecare latură, profil alb și sticlă transparentă. Împărțirea panourilor, tipul deschiderilor, natura exactă a lateralelor, grosimea/profilele și cota tavanului sunt **orientative**, până la verificarea situației reale.
- Tavanul este modelat ca placă de 150 mm grosime, numai pentru reprezentare. Nu reprezintă dimensionare structurală.
- Parapetul și placa de pardoseală sunt păstrate. Eticheta devine `BALCON INCHIS`.
- **Revizie: balconul e doar zonă de uscat rufe.**
  - Setul bistro a fost **scos**.
  - În locul lui: un **uscător de rufe pliabil, liber pe picioare** (~180 × 56 × 105 cm deschis, ~20 m de sârmă), de-a lungul ferestrelor din față. Rămân ~60 cm de trecere spre ușa balconului.
  - **Nimic prins de tavan sau de pereți.**
  - Când nu e folosit, se pliază (~8–10 cm grosime) și se sprijină de peretele lateral.

### Module multimedia TV – revizie la cererea beneficiarului, 05.10.2026
- Două grupuri identice, fiecare cu **1 priză normală 230 V + 1 RJ45 + 1 coaxial TV**:
  - `Priza_TV`, în spatele televizorului, centru la 1350 mm;
  - `Modul_multimedia_comoda_TV`, la comoda TV, centru la 350 mm, poziționare finală după compartimentul tehnic/spatele mobilierului.
- `Priza_soundbar` separată la 900 mm este păstrată.
- Simbolurile sunt pe peretele spre dormitor. RJ45 și coaxialul fiecărui grup se prevăd cablate individual către distribuția de internet/TV, fără a presupune legare în serie. Compatibilitatea dozelor, separarea alimentării de cablurile de date și traseele se stabilesc în planul electric. Pozițiile se coordonează cu suportul TV și accesul prin mobilier.

### Componentă multimedia TV separată – revizie vizuală, 05.10.2026
- Creat `conexiuni_TV.FCStd`, componenta `Conexiuni_TV`, legată în apartament prin `Conexiuni_TV_custom`.
- Sus, complet în spatele ecranului: **1 priză 230 V + 1 RJ45 + 1 coaxial + 1 trecere cu perie pentru cabluri HDMI**.
- Jos, în compartimentul tehnic al comodei: **3 prize 230 V (aparat, rezervă, soundbar) + 1 RJ45 + 1 coaxial + 1 trecere cu perie HDMI**.
- Porturile sunt obiecte distincte și au simboluri diferențiate (contacte 230 V, port rectangular RJ45, mufă coaxială și trecere cabluri). Verificate numărul porturilor și validitatea formelor.
- Ascunse simbolurile vechi `Priza_TV`, `Priza_soundbar` și `Modul_multimedia_comoda_TV`. Alimentarea soundbarului este acum în comodă, fără priză separată expusă sub TV.
- Modelul schematic TV a fost depărtat 60 mm de perete pentru suport și conexiuni. Distanța finală se confirmă cu televizorul/suportul real.
- În comoda schematică a fost decupată o rezervă de service în spate: ~440 × 260 mm, adâncime 120 mm. Acces prin interior/capac demontabil de detaliat la proiectarea mobilei.
- Trecerea HDMI reprezintă acces pentru cablu direct, nu adaptor HDMI. Traseul ascuns, separarea alimentării de date și carcasa modulară compatibilă se stabilesc în planul electric; fără a presupune șanț în peretele structural.

### Iluminat vestibul – completare, 05.10.2026
- `Intrerupator_LED_vestibul`: simplu pentru lumina generală LED, în interior lângă intrarea din sufragerie U3, centru 1050 mm. Pe peretele spre sufragerie, porțiunea liberă dintre dormitor și golul ușii, pe partea balamalei conform planului: x≈3540, y=-4000 mm. Partea clanței este ocupată de corpul spălătoriei. Se confirmă spațiul față de tocul real.
- `Plafoniera_LED_vestibul`: simbol plafonieră LED slim Ø240 mm pe tavan, în fața corpului mașinii de spălat, x=3037,5, y=-4480, z=2480–2500 mm. Se comandă de la întrerupătorul de mai sus. Modelul comercial, puterea, temperatura culorii și circuitul se aleg în planul electric.

### Întrerupătoare baie și dormitor – completare, 05.10.2026
- `Intrerupator_baie`: în vestibul, pe peretele băii, partea clanței U2; centru la 1050 mm, y=-4120 mm, ~80 mm de marginea golului. Controlează lumina generală a băii. Accesul rămâne liber de corpul spălătoriei.
- `Intrerupator_dormitor`: în interiorul dormitorului, pe peretele spre vestibul, partea clanței U1; centru la 1050 mm, x=2515 mm, ~85 mm de marginea golului. Controlează lumina generală a dormitorului.
- Confirmate geometric porțiunile de perete: simbolurile nu sunt în golurile ușilor. Cotele finale se coordonează cu tocurile și pardoseala finită. Salvate în grupul `Electric` din modelul apartamentului.

### Întrerupător vestibul – poziție revizuită, 05.10.2026
- La cererea beneficiarului, `Intrerupator_LED_vestibul` este mutat **în sufragerie, lângă intrarea în vestibul**, pe fața din sufragerie a peretelui, nu în interiorul vestibulului.
- Centru x≈3700, y=-4000, z=1050 mm. Pe porțiunea liberă spre dormitor, în afara golului U3. Controlează aceeași plafonieră LED a vestibulului. Spațiul față de toc și foaia reală a ușii se confirmă la montaj.
- Această poziție înlocuiește poziția anterioară din interiorul vestibulului.

### Baie – cadă și WC încastrat, revizie 05.10.2026
- Beneficiarul dorește **cadă de 150 cm**, lavoar pe aceeași parte cu WC-ul deoarece acolo se află coloana de apă, WC cu rezervor încastrat și acces dinspre lavoar.
- Creat fișier separat `baie.FCStd`, legat în apartament prin `Baie_custom`. Dușul, sticla dușului, WC-ul și lavoarul vechi sunt ascunse, păstrate pentru referință.
- Cadă conceptuală **1500 × 700 mm**, pe peretele din stânga în plan; lățimea de 700 mm este presupusă, de confirmat cu produsul ales. Panou pentru acces la sifon, schematic.
- WC suspendat pe cadrul portant propriu, rezervor încastrat într-o mască **650 × 300 × 1200 mm**, cu capac/poliță de 25 mm deasupra. Poziția măștii x=950–1600 mm, y=-5550–-5250 mm.
- Lavoar 600 × 450 mm, pe același perete de jos în plan, x=1800–2400, y=-5550–-5100 mm. Rămân **200 mm** între lavoar și mască.
- Trapă demontabilă pe lateralul măștii spre lavoar: ~250 × 500 mm, pentru acces suplimentar la robineți/racorduri. Este panou demontabil, nu ușă cu balamale în golul îngust. Accesul la rezervor prin clapeta frontală este păstrat. Poziția și dimensiunea accesului real se stabilesc după măsurarea coloanei; pentru intervenții ample poate fi necesară demontarea mobilierului lavoarului.
- Cadru WC dimensionat și fixat conform sistemului ales; placarea decorativă nu susține vasul. Sistem pentru umiditate, hidroizolație și faianță, conform producătorului; detaliile/grosimile sunt schematice în model.
- Ușa băii spre interior a fost modelată transparent ca propunere necesară spălătoriei din vestibul. Noul WC și lavoar nu se intersectează cu poziția foii la 90°; mânerul, arcul complet și obiectele reale se verifică.
- Poziția exactă a coloanei de apă și a evacuării WC NU este măsurată: folosim peretele WC-ului din model ca bază. Se confirmă înainte de execuție.
- Surse: Geberit, accesul la rezervor prin clapetă: https://www.geberit.ro/sisteme-sanitare-tevi/sisteme-de-instalare-spalare/ ; Knauf, plăci rezistente la umiditate și hidroizolație: https://knauf.com/ro-RO/p/produs/knauf-h-15-gkb-i-15-0mm-13138_0123
- Status: **concept**, nu proiect de instalații / dimensionare structurală. Această variantă înlocuiește propunerea veche cu duș.


### Baie – lavoar central, revizie la cererea beneficiarului, 05.10.2026
- Schimbate pozițiile: în plan, **cadă x=150–850; lavoar central x=950–1550; mască WC x=1750–2400 mm**. WC-ul și lavoarul rămân pe același perete spre coloana de apă.
- Trapă laterală demontabilă mutată pe partea stângă a măștii WC, spre lavoarul central. Gol între lavoar și mască ~200 mm.
- **Conflict nou:** WC-ul mutat spre intrare intersectează poziția foii U2 propuse la 90° spre interior. Această configurație necesită revizuirea sensului/sistemului ușii înainte de execuție; nu este variantă finală. Orice soluție de ușă se verifică și cu spălătoria din vestibul.
- Salvate `baie.FCStd` și modelul apartamentului. Această poziționare înlocuiește pozițiile din revizia anterioară. Scriptul inițial `baie_cada.py` este istoric; fișierul FreeCAD salvat reprezintă poziția curentă.

### Ușa băii spre vestibul – revizie, 05.10.2026
- La cererea beneficiarului, U2 se deschide **spre vestibul**, cu balamaua mutată la capătul golului **dinspre dormitor**, y=-4200 mm. Poziția la 90° este reprezentată prin `Usa_baie_sens_propus`.
- Foaie schematică 700 mm: x=2487,5–3187,5, y=-4217,5–-4182,5 mm. Nu intersectează corpul spălătoriei cu frontul y=-4900; distanță în plan ~682,5 mm.
- La deschiderea completă rămâne doar ~362,5 mm trecere laterală nominală spre dormitor. Pentru circulație confortabilă și folosirea sertarelor/poliței spălătoriei, ușa băii trebuie închisă. Nu se consideră trecere liberă de 90 cm cu ușa deschisă.
- WC-ul din dreapta și lavoarul central sunt păstrate. Sensul anterior spre interior este înlocuit. Tocul, grosimea foii, mânerul și limitarea cursei se confirmă în situația reală.

### Depozitare și electric baie – revizie, 05.10.2026
- Beneficiarul cere deplasarea căzii spre dreapta privit din intrare, mască cu nișe pentru igienă, depozitare deasupra WC-ului, racord pentru ventilator și prize pentru uscător/aparat de ras.
- Cada deplasată **100 mm spre peretele dormitorului (+Y)**: y=-5450–-3950. Rămân ~30 mm nominal până la peretele dormitorului. Dimensiunile finite și produsul real se confirmă înainte de montaj.
- La capătul căzii, pe peretele WC/lavoar: mască 700×100×2100 mm, 3 nișe, adâncime geometrică ~80 mm, mai mică după finisaje; potrivită pentru recipiente mici, nu bidoane mari. Sistem pentru umiditate și hidroizolație. Nu se decupează peretele structural.
- Deasupra WC-ului: dulap 650×250×800 mm, de la z=1350 la 2150; corp W1000/fronturi U702, rafturi și 2 uși. Clapeta și trapa laterală WC rămân accesibile.
- `Prize_baie_uscator_ras`: 2 prize normale cu capac, contact de protecție, IP44 sau superior conform produsului și montajului, centru la x=1650, y=-5550, z=1100 mm, în dreapta oglinzii. Marginea cea mai apropiată de cadă x=1572,5 mm, distanță nominală orizontală de gabaritul căzii ~722,5 mm. Poziția în zonele electrice, jeturile, gradul IP în utilizare, protecția diferențială 30mA și circuitele se confirmă de electrician. Nu sunt prize impermeabile.
- Beneficiarul confirmă: **ventilatorul existent este pe peretele WC/lavoar, deasupra căzii, aproape de tavan**. `Ventilator_baie` și `Alimentare_ventilator_baie` mutate acolo: centru simbol x≈500, z≈2350 mm; cota exactă de măsurat. Masca cu nișe se termină la 2110 mm, sub ventilator; gura rămâne liberă.
- Întrerupătorul băii este acum dublu, în aceeași poziție din vestibul: tastă lumină + tastă ventilator. Temporizare/senzor umiditate, alimentare permanentă dacă modelul o cere și gradul IP deasupra căzii se stabilesc după aparatul real; simbolurile nu reprezintă un circuit executabil.
- Salvate `baie.FCStd` și `apartament_184.FCStd`. Pozițiile fanului din reviziile anterioare sunt înlocuite de poziția confirmată de beneficiar.

### Calorifer baie – poziție revizuită, 05.10.2026
- La cererea beneficiarului, caloriferul portprosop este **pe peretele opus lavoarului**, peretele dinspre dormitor, centrat la x=1250 mm în dreptul lavoarului central.
- Adăugat în `baie.FCStd` ca `Calorifer_prosop` și afișat prin link în apartament; în documentele curente nu mai exista un calorifer de mutat.
- Gabarit schematic ~500×800 mm, partea de jos la 500 mm; proiecție ~70 mm în cameră. Nu intersectează cada. Ușa băii se deschide spre vestibul, astfel încât nu intersectează caloriferul.
- Model comercial, putere și racorduri de confirmat după instalația de încălzire. Nu se presupune calorifer electric. Salvat în baie și în apartament.
### Cada, paravan si plafoniere LED – 05.10.2026
- Cada deplasata suplimentar 30 mm spre nord: y=-5420..-3920. Masca cu nise extinsa la 130 mm: y=-5550..-5420, latime 700 mm. Ansamblu cada 1500 + masca 130 = 1630 mm intre pereti, fara gol nominal; cote finite si racord etans de confirmat.
- Nise cu adancime geometrica 110 mm (mai putin dupa finisaje); masca hidrofuga/hidroizolata. Ventilatorul deasupra ramane liber.
- Paravan rabatabil schematic 800x1400x8 mm, sticla securizata, pe marginea libera a cazii, la capatul cu nise. Profil prins in ranforsarea mastii, garnitura inferioara. Rabatare spre cada, acces nise prin rabatare. Model comercial si prinderi de definit.
- Adaugate plafoniere LED la tavan in dormitor, camera de zi, bucatarie, baie, hol, nisa si balcon inchis. Plafoniera existenta in vestibul pastrata. Diametre orientative 240–500 mm, lumina 3000K; flux si modele finale de ales. Baie: pozitie peste zona libera, propunere IP44 sau superior de verificat la montaj; balcon: protectie pentru eventual condens.
- Salvate baie.FCStd si apartament_184.FCStd. Nu sunt planuri de executie electrica.
### Dormitor – repozitionare si prize, 05.10.2026
- Dulapul existent 2200x600 mm rotit pe peretele din stanga intrarii din vestibul: x150..2350, y-3845..-3245, front spre camera. Ramane 250 mm pana la golul usii x2600.
- Patul si ambele noptiere deplasate 250 mm spre fereastra. Axa patului y=-1800; televizor nou pe peretele estic, centrat exact pe aceeasi axa. Nu exista intersectii pat/noptiere cu dulapul; distanta dulap–noptiera apropiata 195 mm. Biroul pastrat.
- TV dormitor schematic 1000x580 mm, suport cu rezerva de 60 mm fata de perete. Modul in proiectia ecranului: 1 Schuko, 1 RJ45 cablat Cat6, 1 coaxial, 1 trecere HDMI cu perie. RJ45 este conectorul, Cat6 categoria cablului; nu doua mufe diferite. Separare 230V/date la executie.
- Cate o priza Schuko laterala fiecarei noptiere, la z650 mm: y=-3150 si -450 pe peretele vestic. O priza Schuko la dulap, x2150, z2250, in compartiment tehnic accesibil; decupaj interior de definit cu mobilierul.
- Salvat apartament_184.FCStd. Cotele sunt de concept, produsele si detaliile de montaj se confirma la masuratori.
### Usi si dormitor fara birou – 05.10.2026
- Eliminate din model Birou si Scaun_birou. Grupul celor 4 prize sub fereastra pastrat ca prize generale, eticheta actualizata.
- Adaugate U1–U8: foi schematice de 35 mm la 90 grade, arcuri de deschidere si linii intrerupte pentru pozitia inchisa. Foaia foloseste latimea golului nominal; tocurile si dimensiunile efective se stabilesc la masuratori.
- U1 spre dormitor, U2 spre vestibul cu balamaua spre dormitor (decizia curenta), U3 si U4 spre sufragerie, U5 spre bucatarie/frigider, U6 spre bucatarie cu balamaua spre frigider, U7 spre hol, U8 **spre camera de zi** (revizie la cererea beneficiarului; balama la x 5250, foaia deschisă ocupă ~85 cm în cameră, fără coliziuni cu masa, scaunele sau draperiile). U2 vechi ascuns, inlocuit de Usa_U2.
- Foile la 90 grade nu intersecteaza patul, noptierele, dulapul dormitorului, canapeaua, masa, comoda sau setul balconului. Verificarea nu include manerele si tocurile comerciale.
- Limitarea anterioara a circulatiei in vestibul cu usa baii complet deschisa ramane valabila (~36 cm trecere laterala).
- Modelul apartamentului salvat.
### Corectie prize dormitor – 05.10.2026
- La cererea beneficiarului, eliminat grupul Prize_birou_4 de sub geam. Pastrarea lui ca prize generale din revizia anterioara este anulata.
- Raman prizele solicitate la cele doua noptiere, dulap si modulul ascuns al televizorului.
### Draperii blackout si rulouri – 05.10.2026
- Dormitor: doua panouri blackout pe sina de tavan x1450..3500, reprezentate stranse la lateralele ferestrei. Taupe cald orientativ, tiv z60, sus z2450.
- **Corecție radiator / birou / draperii în camera de zi:**
  - radiatorul (32–42,3 cm de la perete) intersecta biroul, iar draperia era între perete și radiator;
  - acum șina și draperiile sunt la **46–49,7 cm de la perete**, în fața radiatorului, care rămâne în spatele draperiilor;
  - biroul e **IKEA TROTTEN cu înălțime reglabilă electric, alb, 120 × 70 cm** (71–118 cm, max. 50 kg), la 52–122 cm de la perete, modelat la 75 cm. IDÅSEN 160×80 nu încăpea (sunt ~155 cm până la zona în care se deschide ușa balconului) și nu apare cu blat alb. Biroul e **lipit de peretele din stânga** (x 370–490). Cele 2 scaune de masă sunt înlocuite cu **un scaun de birou** ergonomic pe rotile;
  - **priză dublă pentru birou**, verticală, pe peretele din stânga, între colțul ferestrei și birou, **în spatele draperiei strânse**, cu centrul la 85 cm (deasupra blatului la 75 cm). Pe peretele cu fereastra nu se poate (radiatorul e dedesubt, fereastra deasupra);
  - verificat: fără intersecții între radiator, birou, draperii, scaune, ușa balconului și canapea.
- Sufragerie: sina comuna x3700..6800 (prelungita de la 6600) pentru fereastra si usa balconului, doua panouri blackout parcate lateral (panoul 2 la x6260..6710, dupa intrerupatorul balconului). Gol usa x5250..6100 ramane liber; draperiile stranse nu intersecteaza masa din model.
- Bucatarie: doua rulouri textile lavabile, filtrante, propuse pe canaturile geamului x8230..9630, reprezentate partial coborate. Impartire 2x700 orientativa; canaturile, montajul si deschiderea se confirma pe tamplaria reala. Blackout cerut numai la dormitor si sufragerie.
- Tesaturile, latimea desfasurata cu incretire, suprapunerile si intoarcerile laterale se stabilesc la masuratori. Model salvat in apartament_184.FCStd.
### Radiatoare noi, pozitii pastrate – 05.10.2026
- Beneficiarul confirma termoficare si cere doar reprezentarea radiatoarelor noi, fara mutarea pozitiilor.
- Adaugate radiator panou schematic tip22 dormitor 1000x600x100, centru x2480 sub geam; sufragerie 1200x600x100, centru x4475 sub geam in zona indicata a biroului. Baza z150, y=-420..-320, fara modificari de mobilier sau trasee.
- In model nu existau radiatoare in aceste camere. Centrele ferestrelor sunt repere provizorii pentru pozitiile existente; decalajele fata de racordurile reale nu sunt masurate. Puterea, produsul, dimensiunile si compatibilitatea cu termoficarea se confirma ulterior. Draperiile actuale pastrate; conflictul functional la inchiderea peste radiator ramane de rezolvat.
- Salvat apartament_184.FCStd.
### Incalzire – bucatarie fara radiator, 05.10.2026
- Beneficiarul cere sa nu fie radiator in bucatarie. Modelul nu are radiator in bucatarie; ramane asa.
- Solicitat necesar termic si numar orientativ de elementi. Etajul, izolatia, ferestrele si temperaturile reale tur/retur sunt inca neconfirmate. Estimarea volumetrica nu este calcul de pierderi termice pentru executie si nu dimensioneaza incalzirea indirecta a bucatariei/holului.
### Salvare generala si date incalzire confirmate – 05.10.2026
- Beneficiarul confirma: etaj 1, bloc izolat exterior, ferestre termopan, locuinta incalzita sub apartament, alimentare prin termoficare. Bucataria ramane fara radiator.
- Estimarea preliminara discutata: dormitor ~1100 W, sufragerie ~1600 W, fara sarcina suplimentara pentru incalzirea indirecta a bucatariei/holului. Nu este calcul final de pierderi termice. Conversie exemplu Global VOX500: 9/13 elementi la 75/65/20 si 14/21 la 60/50/20. Model comercial, temperaturi reale si puterea portprosopului de confirmat.
- Salvare generala a tuturor documentelor FreeCAD deschise care au fisier asociat, inclusiv apartament si componentele legate. Nu s-au generat PDF-uri noi.
### Plan termic PDF R01 – 05.10.2026
- La cererea finala a beneficiarului, generat DOAR dosarul termic; planurile electrice si lista generala de renovare sunt excluse din aceasta livrare.
- Coloana C1 confirmata in coltul sufragerie–dormitor dinspre ferestre; trecere existenta prin perete spre dormitor. Axe, diametre, regim mono/bifilar, temperatura si presiune inca nemasurate. Racordul baii nu este presupus legat la C1.
- Fisier output/pdf/Apartament_184_Plan_termic_R01.pdf, 9 planse A3: plan1:50, detaliu coloana1:25, elevatii1:20, baie1:10, sectiune1:5, traversare perete, necesar preliminar, scheme principiu, cantitati si verificari.
- Geometrie extrasa din modelul curent apartament_184.FCStd si baie.FCStd. Radiatoarele si mobilierul nu sunt modificate.
- Cantitati ferme: 3 corpuri noi (R1, R2, R3), 2 demontari fonta; accesoriile sunt conditionate de produsele alese. Tevi si fitinguri de masurat, fara lungimi sau DN inventate.
- Estimarea termica este pentru buget, nu calcul complet EN12831: R1~1100 W, R2~1600 W, R3~450 W; sarcina suplimentara nealocata ~1500 W a bucatariei/holului/vestibulului/debaralei la 20C este explicitata. Bucataria ramane fara radiator. Compatibilitatea draperiilor si mobilierului cu convectia este punct deschis.
- PDF randat si verificat vizual, 9 pagini, texte incadrate, cote si tabele lizibile. Dosar de coordonare/ofertare, nu proiect de executie semnat/verificat.

## 05.10.2026 — Plan sanitar baie și linkuri materiale
- Confirmat: coloana de canalizare și racordurile de apă sunt în zona WC-ului, spre vestibul; poziția exactă și cotele racordurilor necesită măsurare.
- Generat output/pdf/Apartament_184_Plan_sanitar_baie_R01.pdf: 10 planșe A3, amplasare, alimentare apă, canalizare, elevație, detalii WC/cadă/nișe, cantități, montaj și verificări; 31 linkuri clicabile.
- Actualizat output/pdf/Apartament_184_Plan_termic_R01.pdf: 9 planșe, linkuri în lista de cantități; 14 linkuri clicabile în document.
- Verificat vizual PDF-urile randate. Produsele sunt propuneri de coordonat cu gabaritele CAD; lungimile conductelor și racordurile finale nu sunt inventate. Documentele sunt pentru coordonare și ofertare, nu proiect de execuție validat.
- Modelul CAD nu a fost modificat în această etapă.


## Randări finale + plan 3D (2026-10-05)
- 15 unghiuri × zi/noapte, 1920×1200, 384 eșantioane: `randari/zi`, `randari/noapte` (JPG pentru document în `randari/web`).
- Plan 3D vedere de sus cu adnotări: `randari/Plan_3D_apartament_184.png` (scripturi `plan_3d_sus.py` + `adnoteaza_plan_3d.py`, scena în `plan_3D.blend`).
- Documentul de design are toate secțiunile pe încăperi completate, cu zi + seară.
- De reglat: LED-ul vertical de la riflaje (dormitor) e prea puternic, iar debaraua e cam fadă ziua.
- Planșe pe încăperi (stil prezentare): în așteptare, întâi o mostră pentru camera de zi.

## 05.10.2026 — Plan electric curenti tari / slabi, R02
- Beneficiarul confirma tabloul electric si intrarea internetului deasupra usii de intrare in apartament. Axele si dimensiunile reale raman de masurat.
- Generat output/pdf/Apartament_184_Plan_electric_R02.pdf: 19 planse A3, E00-E18; planuri 1:50, registre, 12 circuite propuse, tablou de principiu, doze J01-J06, detalii multimedia, router/NET, baie, LED, sectiune verticala, cote locale, cantitati si estimari cabluri. 23 linkuri clicabile. PDF randat si verificat vizual, fara iesiri de text din margini.
- Varianta include 23 grupuri de prize / 35 mecanisme Schuko, 8 pozitii de intrerupatoare, 8 plafoniere, 4 legaturi Cat6 si 3 coaxiale. P09 lateral birou pastrat; P10 + D04 adaugate sub birou, Z600. Priza eliminata de sub geamul dormitorului nu reapare.
- Router/ONT/distributie NET propuse in hol, perete sudic in plan, X7900/Y-5540/Z2000; acces si ventilatie de coordonat cu dulapul. Pozitia nu este prezentata ca masurata. 4 prize C12; patch-panel 8 porturi cu 4 populate; switch optional dupa router/operator.
- Circuite separate pentru MSV, masina rufe, cuptor, frigider, prize baie, retea. Plita CAD este pe GAZ: circuit pentru aprindere, nu dimensionare pentru inductie. Preselectie Cu 1,5/2,5 mm2 si RCBO B10/B16, 30mA; se valideaza dupa receptori, pozare si masuratori. AFDD prevazut pentru C01/C04 dormitor, conform Ordin 959/2023 pct.4.2.2.10-12.
- Estimari cabluri de date si 230V calculate din coridoarele propuse, cu coborari si rezerva explicita; nu reprezinta releveu sau comanda definitiva. PE, puterea aprobata, fazele, Ik, DeltaU si echipamentele reale necunoscute.
- Componenta separata instalatie_electrica_R02.FCStd, cu 54 puncte identificate, doze, trasee si gabarite TE/NET; link ascuns implicit in apartament pentru a nu aglomera amenajarea, traseele pot fi afisate pe grupe. Formele verificate valide.
- Adaugat concret in apartament Modul_birou_Cat6: 2 Schuko + 1 RJ45, carcasa separata date, Z600; coordonare cu cadrul si cursa biroului la montaj. Apartamentul salvat.
- Registru editabil: output/pdf/Apartament_184_Registru_electric_R02.csv. R01 electric este o versiune intermediara, se foloseste R02.

## 05.10.2026 — Corecții randări + instrucțiuni montaj dulap hol R01
- Corecții la randare: oglinda de machiaj avea material emisiv și acum e oglindă (R_Oglinda). LED-ul din spatele oglinzii și cel vertical de la riflaje au material propriu, R_LED_oglinda, cu intensitate 2,5. Debara: lumina 40 W, expunere zi 0,5 și noapte −0,4. Scriptul e `fix_randare_oglinda_debara.py`. Pe planul 3D, corpurile de sus ale bucătăriei sunt ascunse.
- Unghiul DB_01 din debara arată mai mult pereți: de refăcut camera dacă e nevoie.
- PDF cerut explicit de beneficiar: `output/pdf/Apartament_184_Dulap_hol_montaj_R01.pdf`, 21 de planșe A3 în stilul dosarelor existente:
  - copertă, verificări, unelte;
  - lista pieselor (2 pagini), feronerie A–X;
  - 14 pași cu imagini Workbench (piesele noi în turcoaz), necesar, unelte și atenționări;
  - detaliu cutie sertar 1:5, detaliu balamale uși 1:10.
- Scripturi: `dulap_hol_pasi_blender.py` (imagini în `tmp/dulap_hol_pasi`) și `dulap_hol_montaj_pdf.py`. Rulează cu Python-ul care are reportlab: `~/.cache/codex-runtimes/.../python.exe`.
- Montaj propus: în picioare, cu spatele la ~60 cm de perete ca să se poată prinde spatele HDF, apoi dulapul se împinge la perete. Blatul se introduce din față, orizontal.
- DE COORDONAT: în planul electric R02, routerul/ONT e la X7900 Z2000, adică în spatele dulapului de hol.

## 05.10.2026 — Montaj electric detaliat R03
- Creat output/pdf/Apartament_184_Montaj_electric_R03.pdf: 35 planse A3, detalii marite pe incaperi, registre globale si cote locale, elevatii, 19 coridoare TR01-TR19, 27 coborari B01-B27, doze J, comenzi si ramuri plafoniere.
- Axa superioara propusa Z2400 inlocuieste Z2300 pentru geometria R03; spatiul pentru masca/tuburi se verifica fata de mobilier, tavan si structura. Cotele sunt ale propunerii CAD, nu releveu validat pentru executie.
- Grupare trasee cu tuburi distincte pe circuite; cabluri date separate de 230V. TV/birou/dulapuri folosesc compartimente demontabile pentru reducerea santurilor. Nicio economie procentuala sau permisiune de taiere a structurii nu este presupusa.
- H01 HDMI living Z350-1350, H02 rezerva dormitor Z400-1410: tub separat orientativ 32-40 mm, de verificat dupa mufa/raza, acces la capete, cablu inlocuibil si proba inainte de inchidere.
- Registru editabil output/pdf/Apartament_184_Trasare_R03.csv si date geometrice JSON. Toate cele 54 puncte acoperite: 45 in coborari, 8 plafoniere, F08 local la noptiere.
- Salvat montaj_electric_R03.FCStd, 19 trasee principale, 27 coborari si 2 HDMI, toate formele valide. Link ascuns in apartament; documentul separat afisat pentru verificare. Apartamentul salvat.
- PDF randat si verificat vizual; 35 pagini, fara depasiri ale marginilor textului. R02 ramane baza de aparataj/protectii preliminare; geometria traseelor de montaj este R03. Lungimile preliminare de cablu R02 trebuie recalculate la executie dupa traseele R03 aprobate pe teren.

## 05.10.2026 — Plan de debitare R01 (optimizare plăci)
- `scripturi/optimizare_debitare.py`: așezare ghilotină pe plăci 2800×2070, margine 10 mm, pânză 4,4 mm. Rotire permisă la W1000/U702/HDF, interzisă la H1145. C09 se taie în perechi de 577×525. Rezultatul e în `tmp/debitare_layout.json`.
- Inventarul pieselor celorlalte corpuri e luat din modelul Blender, în `tmp/inventar_panouri.json`. Sunt estimări; corpurile bucătăriei nu sunt desfăcute pe plăci și lipsesc.
- PDF: `output/pdf/Apartament_184_Plan_debitare_R01.pdf`, 12 planșe. Script: `scripturi/debitare_pdf.py`, rulat cu Python-ul codex care are reportlab.
- Dulapul de hol singur: 8 plăci (W1000 18 ×3, U702 ×2, W1000 16 ×1, HDF ×2). A doua placă U702 e folosită ~7%, pentru că ușile de 519 nu încap câte 4 pe lățime.
- Toate corpurile, comandate separat: 30 de plăci. Comandă comună: 22 de plăci (U702 9→5, W1000 18 13→11, HDF 6→4).
- Pe dressing, piesele de 3344 mm (bază, blat, soclu, mască, spate) depășesc placa și trebuie împărțite cu îmbinare.

## 05.10.2026 - Montaj electric R04, audit punct cu punct
- PDF R04: 45 planse A3, randate integral si inspectate; fara depasiri de margini detectate. Planse pe camere cu maximum 5 puncte, detalii P02/P05, fise individuale si registru de verificare.
- Corectie: rutele R03 pana la axele comune nu reprezentau explicit toate segmentele finale. R04 conecteaza fiecare centru real de aparat; P02 verificat in CAD la [158,-450,650], P05 la [3400,-256,900].
- 63 trasee verificate geometric: 55 terminale, 6 alimentari de doze si 2 HDMI; 23 grupe P. F08 separat in F08A/F08B, iesiri locale pentru noptiere. Niciun capat de ruta deconectat; nu reprezinta proba electrica sau proiect de executie validat.
- JSON si CSV R04 contin poliliniile complete XYZ folosite de PDF si CAD. Lungimile vechi nu sunt cantitati finale dupa aceste corectii.
- montaj_electric_R04.FCStd salvat cu FreeCADCmd, toate formele valide. Integrarea GUI a expirat dupa 90 s; legatura in apartamentul principal si afisarea in sesiunea GUI NU sunt confirmate. Modelul separat este salvat si disponibil.
- De coordonat la executie: router/ONT fata de dulapul de hol, acces la doze, structura, trasee in masti, volume baie, PE si protectii. Cotele raman propuneri din model, de confirmat prin releveu.

## 05.10.2026 — Montaj dulap hol R02 + balamale push + întrerupătoare de balama
- Beneficiarul vrea deschidere prin apăsare (TIP-ON). Rămân balamalele CLIP top fără arc (70T3550 / 70T3650), FĂRĂ soft-close; la dealer se poate întreba de o variantă TIP-ON cu închidere lentă pentru uși.
- LED interior: senzorii IR sunt înlocuiți cu 4 întrerupătoare de balama 24 V, pe balamaua de sus a celor 4 uși mari, câte 2 în paralel pe modul. Excelurile Debimax și Mambricolaj sunt regenerate (feronerie: întrerupătoare și 250 de șuruburi 4×16).
- Fiecare piesă are etichetă unică (C07.1, F01.3…) legată de placa din planul de debitare (W18-1…3, U18-1…2, W16-1, HDF-1…2). Etichetele apar și pe hărțile din Plan_debitare_R01.
- `output/pdf/Apartament_184_Dulap_hol_montaj_R02.pdf`, 36 de planșe:
  - folii de etichetare de printat pe autocolant;
  - etichete pe imaginile 3D (ancore din `ancore.json`);
  - la fiecare pas, o pagină de îmbinări: fețele panourilor cu găurile din foaia „Găurire” și un tabel cu elementul, codul Blum, bucățile și locul de montaj.
- R01 rămâne doar ca istoric.

## 05.10.2026 — Deviz materiale R02, prețuri verificate cu link
- Am pornit de la R01 făcut de ChatGPT/Codex (`scripturi/deviz_actualizare.py`, 103 linii, 6 verificate; backup în `tmp/deviz_R01_codex.json`).
- `scripturi/deviz_verificare_preturi.py`: 67 de linii au preț observat online pe 05.10.2026 la produsul ales, cu link. Alte 14 au link de reper, dar includ părți estimate. 22 rămân provizioane (loturi de instalații, consumabile, transport, mobilier la comandă).
- Total materiale cu 7% rezervă: 100.526 – 140.422 lei, mediu 120.474 lei (R01: 95.512 – 153.438 lei).
- Fișiere:
  - `Deviz_materiale_ap184_R02.xlsx` (cel vechi era deschis în Excel), cu coloanele „Sursa prețului” și „Link”;
  - `output/pdf/Apartament_184_Deviz_materiale_R02.pdf`, 26 de pagini, cu lista prețurilor observate și linkurile clicabile.
- Alegeri de produs făcute pentru verificare: IKEA FRIHETEN, GLADSTAD/IDANÄS, VALEVÅG, FLINTAN, NÄSINGE, MAJGULL+VIDGA; Schneider Asfora; Gewiss 54 module; Purmo C22; Roca Gap New 60; Geberit Duofix 111.300.00.5; Häfele Ironfix. Se pot schimba.

## 05.10.2026 — Cabluri calculate exact pe traseele R04
- Bugetul vechi (110 m 3×1,5 + 170 m 3×2,5) socotea separat traseul fiecărui punct până la tablou: 522 m adunați, din care s-a făcut o estimare.
- Calcul exact pe circuite, cu traseul comun numărat o singură dată (prizele de pe un circuit legate una după alta):
  - 3×1,5 (C01–C03): 77,8 m net, 86 m cu rezerve;
  - 3×2,5 (C04–C12): 115,6 m + 4,6 m urcări, 137 m cu rezerve.
- Cele mai lungi circuite: dormitor C04 26 m, cameră de zi C05 24 m, bucătărie C10 19 m. Tabloul e la intrare, iar apartamentul are 11 m lungime.
- Coaxial: 14,7 m de traseu, buget 20 m. Cat6: 20,4 m de traseu.
- LED-ul de la noptiere (F08A/B) e pe 24 V și nu intră în cablul de 230 V.
- Devizul R02 e actualizat: 100.123 – 139.975 lei cu rezervă.

## 05.10.2026 — Deviz R03 (cele mai bune oferte), etape de cheltuieli, plan de lucrări
- `scripturi/deviz_R03_oferte_etape.py`, pornind de la R02 (`tmp/deviz_R02.json`): pentru fiecare articol, prețul de bază e cel mai mic găsit online, cu magazin și link; alternativa e un magazin comod. Sunt 104 linii, 82 verificate.
- Total materiale cu 7% rezervă: **96.923 lei** la cele mai bune oferte, 128.718 lei la alternative (R02: 100.080 – 138.930).
- Oferte principale:
  - cablu Hornbach / Leroy Merlin;
  - siguranțe diferențiale (RCBO) ETI tip A 140 lei;
  - tablou Noark;
  - AFDD Celon;
  - PAL W1000 / U702 Regency 366 lei;
  - feronerie Blum la cel mai mic preț pe bucată, seturi calculate pe bucăți;
  - debitare și cant calculate pe metri (Mambricolaj): 437 m tăiere, 298 m cant 2 mm;
  - instalații sanitare cu țevi PPR și canalizare PP calculate din modelul băii;
  - canapea JYSK ILDVED, pat JYSK HALD.
- Etape E1–E8 și săptămâna de cumpărare pe fiecare articol. Plăți (oferte): S1 8,3k, S2 1,3k, S3 24,6k, S4 10,9k, S5 33,4k, S6 12,1k lei.
- Fișiere:
  - `Deviz_materiale_ap184_R03.xlsx` (Rezumat, Deviz detaliat cu filtre, Etape și plăți, Calendar lucrări, Opționale);
  - `output/pdf/Apartament_184_Deviz_materiale_R03.pdf` (30 de planșe);
  - `output/pdf/Apartament_184_Plan_lucrari_R01.pdf` (7 planșe: Gantt, drum critic, cumpărături pe săptămâni). Script: `scripturi/plan_lucrari_pdf.py`; date în `tmp/timeline.json`.
- Calendar: start 12.10.2026, termic înainte de pornirea căldurii, șapă 26.10, comanda la atelier 26.10, Black Friday 13.11, mobilier 16–21.11, final ~27.11, rezervă până la 04.12.

## 05.10.2026 — Toate planurile și montajele refăcute cu ultimele decizii
- Bază comună nouă: `scripturi/plan_comun.py`. Scripturile Codex (`plan_electric_pdf.py`, `plan_sanitar_baie_pdf.py`, `plan_termic_pdf.py`, `electric_r04_complet.py`) NU sunt modificate; fiecare revizie nouă e un script separat care le citește și schimbă doar ce s-a decis între timp.
- Fundalul de mobilier al tuturor planurilor vine acum din scena 3D: `scripturi/extrage_mobilier_plan.py` → `tmp/mobilier_plan.json` (37 de piese, cu cod).
  - Dressingul are conturul lui real de 60 cm; masa de călcat deschisă e piesă separată (MC, cu linie întreruptă).
  - Rafturile debaralei au forma reală: L cu capăt teșit + trapez, nu toată nișa.
- Fișiere noi în `output/pdf`:
  - **Plan_mobilare_R02** (12 planșe, `plan_mobilare_pdf.py`): plan cotat, plan de mobilare cu toate piesele și legendă, câte o planșă pe încăperi (dimensiuni, produs ales, preț, link), pardoseli și praguri, plan 3D, 15 randări. Buget mobilier 31.207 lei (plăci și atelier, feronerie, gata făcut).
  - **Plan_electric_R03** (19, `plan_electric_R03.py`): produsele alese cu preț (E14: 10.211 lei; E15: 1.364 lei); 10 RCBO + 2 AFDD, tablou Noark 54 module; cabluri exacte pe circuite (E17).
  - **Montaj_electric_R05** (46, `montaj_electric_R05.py`): trasee R04 neschimbate; planșa nouă K1 cu cablul de tăiat pe fiecare circuit.
  - **Plan_sanitar_baie_R02** (10, `plan_sanitar_R02.py`): obiecte alese cu preț (7.456 lei); listă exactă de țevi PPR / PP, fitinguri, robineți, R777, Nivello 50, CL 51, CL 152 (1.593 lei); racordul mașinii de spălat inclus; ordinea șapă → hidroizolație → microciment.
  - **Plan_termic_R02** (9, `plan_termic_R02.py`): Purmo C22 600 × 1000 / 600 × 1200, Santorini 500 × 714, kit Danfoss, multistrat (1.777 lei). Radiatoarele se montează pe 13–15.10, înainte de pornirea căldurii.
  - **Plan_debitare_R02** (13): planșa nouă de costuri. Plăci + debitare + cant + găurire + oglinzi + feronerie Blum = 21.794 lei la cele mai bune oferte (28.286 la alternative).
  - **Dulap_hol_montaj_R03** (37): pagina nouă M04b de cumpărături. Feronerie A–U 949,69 lei, oglinzi, LED; total 2.260 lei.
- Cabluri pe traseele exacte: 3×1,5 = 86 m, 3×2,5 = 137 m. Cat6 și coaxialul sunt legate în stea, deci se adună traseele, plus 2 m rezervă pe legătură: Cat6 48,7 m (4 legături), coaxial 35,1 m (3 legături). Devizul M030 e corectat de la 20 m la 35 m coaxial.
- **Corecție LED dulap hol / dressing:**
  - Produsul din deviz (24led, 45,50 lei) e un senzor de ușă IR care se lipește pe corp, nu un întrerupător pe balama. Blum nu are întrerupător de balama în gamă, iar în magazinele din România am găsit doar senzori de ușă.
  - Senzorul se lipește lângă balamaua de sus și nu apasă pe ușă, deci merge cu TIP-ON. Funcția e aceeași: LED-ul se aprinde când se deschide ușa.
  - Montajul R03, Excelurile de atelier, planul electric R03 și devizul (M039) folosesc acum această descriere.
  - Alternativă: un senzor pentru uși duble (~52 lei, LED Solution) pe fiecare modul.
- **Decizie deschisă (până la 21.10):** punctul NET (router / ONT) cade în spatele dulapului din hol, care are uși cu oglindă, iar oglinda atenuează Wi-Fi. Propunere: ONT și patch-panel în dulap, cu acces din față; routerul în afara dulapului.
- Deviz R03 regenerat: 96.940 lei cu 7 % rezervă, la cele mai bune oferte (alternative: 128.768 lei).
- Versiunile înlocuite sunt în `_arhiva/2026-10-05_inlocuite_seara/`, cu index. `Trasee_complete_R04.json` rămâne în `output/pdf`, pentru că e citit de alte scripturi.

## 06.10.2026 — Oglinda de machiaj din dormitor (FreeCAD)
- În FreeCAD oglinda părea panou luminos. Era transparentă 20 %, iar în spatele ei o placă LED caldă acoperea aproape toată suprafața.
- Modificări în `perete_TV_dormitor.FCStd`:
  - `Machiaj_oglinda_LED` e acum opacă, argintie și lucioasă.
  - Placa `Machiaj_LED_spate_oglinda` e ascunsă, păstrată pentru istoric.
- Bandă LED pe ambele laterale ale oglinzii:
  - dinspre fereastră: nou `Machiaj_LED_lateral_fereastra`, profil aplicat cu difuzor opal, 16 mm lățime, de la blat (755) la tavan (2495), la 3 mm de oglindă;
  - dinspre riflaje: banda verticală existentă a riflajelor, tot la 3 mm de oglindă.
- Fără intersecții cu alte piese. Copia de dinainte: `_arhiva/2026-10-06_oglinda_machiaj/perete_TV_dormitor_inainte.FCStd`.
- Blender (`apartament_184_randare.blend`, script `scripturi/oglinda_led_laterale_blender.py`): placa din spate e scoasă din randare, iar banda dinspre fereastră e adăugată cu materialul benzii riflajelor (`R_LED_oglinda`). Copia de dinainte e în aceeași arhivă.
- Refăcute randările D_02 (perete TV cu riflaje) și D_03 (zona de machiaj), zi și seară, la 384 de eșantioane: sunt singurele unghiuri în care se vede oglinda (verificat prin ray-cast). Imaginile sunt actualizate în documentul de design și în planul de mobilare R02.

## 06.10.2026 — Reimport din FreeCAD și comparație cu Blender
- Export nou din fișierele FreeCAD salvate: `scripturi/export_freecad_headless.py` → `blender_export_2026-10-06/`, 494 de piese.
  - Exportul nu folosește sesiunea deschisă în FreeCAD, unde Codex are lucru nesalvat la instalația electrică (R07, R08_3D).
  - Documentele electrice nu intră în export.
- Comparația cu scena de randare (`blender_dump_scena.py` + `compara_freecad_blender.py` → `tmp/diferente_freecad_blender.json`):
  - geometrie identică la toate piesele comune (nicio diferență peste 1 mm);
  - lipsea din Blender modulul de prize de sub birou (2 Schuko + RJ45, 6 piese): adăugat cu `sincronizare_freecad_blender.py`, cu materialele aparatajului;
  - banda LED nouă de la oglinda de machiaj nu era în grupul componentei, deci nu apărea în apartament: mutată în grup și salvată în FreeCAD.
- Diferențe păstrate intenționat:
  - 3 uși ascunse la randare (U7 și U8 deschise, propunerea de ușă de la baie);
  - 33 de obiecte doar pentru randare (perne, covor, voaluri, pled, blocuri din depărtare, sol, tavan, ușa de intrare închisă);
  - 2 piese ascunse în ambele programe (placa LED din spatele oglinzii, masa de călcat deschisă).
- Copia scenei de dinainte: `_arhiva/2026-10-06_sincronizare_freecad/`.

## 06.10.2026 — R09: distribuție electrică predominant prin pardoseală
- Decizie utilizator: trasee noi cât mai mult pe jos, peste placa de beton, apoi șapă; fără șlițuri în tavan.
- Se păstrează pozițiile existente ale plafonierelor. Tuburile și conductoarele existente trebuie verificate; pozițiile modelului nu țin loc de releveu.
- Înălțimea disponibilă de la placă la pardoseala finită: DE MĂSURAT.
- `montaj_electric_R09_3D.FCStd`: propunere de coordonare, 55 legături noi/preluate din model și 8 puncte de iluminat de verificat. Traseele existente spre plafoniere nu sunt inventate și nu intră în lungimile noi.
- Cota axei tuburilor -30 mm este numai convenție grafică preluată din R08; NU reprezintă o cotă de execuție sau grosimea șapei. Axele suprapuse încă necesită separare fizică și verificarea încrucișărilor.
- Dozele de derivație rămân accesibile pe pereți, conform pozițiilor existente în model; nu se îngroapă conexiuni în șapă. Numărul final de tuburi, secțiunile, prinderile și trecerile se validează cu electricianul după măsurători.
- R08 rămâne comparație istorică. PDF-ul R08 și devizul nu sunt încă recalculate pentru R09.

## 06.10.2026 — Organizarea versiunilor
- Punct unic de acces: 00_DESCHIDE_PROIECTUL.html, cu versiuni curente și starea documentelor electrice.
- 26 de fișiere înlocuite / copii automate mutate în _arhiva/2026-10-06_organizare, cu manifest și verificare SHA-256 după fiecare mutare. Nu au fost șterse fișiere.
- 17 documente din sesiunea FreeCAD conectată salvate suplimentar ca instantanee; R09 salvat în fișierul curent. Instantaneele nu suprascriu componentele actualizate separat pe disc.
- Păstrate la locația inițială componentele referite de modelul principal, inclusiv cele două referințe electrice istorice R02/R03. Păstrate și sursele JSON necesare scripturilor.
- PDF-ul de montaj R08 este arhivat ca variantă comparativă. Planul de aparataj R05 rămâne cel mai recent PDF electric disponibil, marcat explicit drept anterior deciziei R09. Devizul R03 nu este încă recalculat pentru R09.

## 06.10.2026 — Biblioteci Egger / Kronospan și texturi PBR
- **Egger:** imaginile oficiale ale decorurilor („Date despre decoruri”) se descarcă din portalul myEGGER, cu cont gratuit.
  - Se pot lua decoruri individuale sau pachete pentru programe CAD.
  - Fără cont se văd pe site doar placa scanată (2.311 × 1.300 mm) și vederea 3D.
  - Paginile decorurilor: `egger.com/ro/mobilier-si-design-interior/decoruri/W1000_9`, `U702_9`, `H1145_10`.
  - Contul îl face beneficiarul (pagina de înregistrare e deschisă în browserul din aplicație). După autentificare se descarcă W1000 ST9, U702 ST9 și H1145 ST10.
- **Kronospan:** Digital Library publică, fără cont (`kronospan.com/en_US/express-services/downloads/`).
  - Secțiunea Images are decoruri la rezoluție mare, pe colecții, cu „Download all”; fiecare pagină de decor are și „Download”.
  - Sunt doar scanări de culoare, fără hărți PBR.
- **Texturi PBR CC0** în `texturi/`, 620 MB, cu `LICENTE.md`:
  - Poly Haven: wood_floor, white_oak_veneer, smooth_concrete_floor, painted_concrete, white_plaster_02, wool_boucle, rough_linen, poly_wool_herringbone + HDRI buikslotermeerplein 8K;
  - ambientCG: Travertine009, Metal009, Carpet016.
- **`scripturi/materiale_pbr_blender.py`** (aplicat pe `apartament_184_randare.blend`; copia de dinainte în `_arhiva/2026-10-06_texturi_pbr/`):
  - Culoarea rămâne cea din proiect, iar textura dă variația (fibră, pete, țesătură), relieful (hartă normal) și luciul (rugozitate).
  - La travertin, inox și covor, culoarea vine direct din textură.
  - Coordonatele sunt UV pe cub, în metri, ca texturile să aibă mărimea reală.
  - Bouclé-ul (în carouri), betonul vopsit (verde) și inul (albastru) dau doar relief și luciu.
  - H1145: provizoriu fibra de stejar descărcată, recolorată în tonul Bardolino, până vin scanările Egger. W1000 / U702: relief foarte fin, ca structura ST9.
  - Microcimentul e pus și pe pereții băii și pe măști (ca în proiect), iar expunerea pentru baie e 0,7.
  - Cerul: HDRI în loc de cerul Nishita; soarele rămâne.
- **Randări refăcute:**
  - 15 unghiuri × zi/seară, 384 eșantioane, plus planul 3D de sus;
  - imaginile sunt actualizate în documentul de design (31) și în planul de mobilare R02.

## 06.10.2026 — Kronospan în loc de Egger: echivalente, texturi, prețuri (propunere, nedecisă)
- **Texturi Kronospan** (publice, fără cont; imagini oficiale pentru vizualizare, nu CC0):
  - imaginea fiecărui decor, 1200 × 1800 px: `kronospan.com/ro_RO/ajax/express_services/download?args[0]=decors&args[1]=kronodesign&args[2]=K&args[3]=<COD>.jpg` (culori ~50 KB, lemn 0,4–0,8 MB);
  - scanări pe toată placa 2070 × 2800 mm în arhivele `kronospan.com/public/files/bdl/kd2023-<colecție>-2070x2800mm.zip` (0,2–2 GB). Serverul acceptă cereri parțiale, deci se poate lua o singură imagine (ex. K003 35,7 MB, K076 57,7 MB);
  - structurile de suprafață (PE, BS, SU, PW, FP etc., 0,5–1,8 MB fiecare) sunt în `.../decors-and-textures-for-visualisation/kd2023-textures.zip`;
  - nu există hărți PBR. Relieful și luciul se fac din fotografia structurii.
- **Echivalente**, cu diferența de culoare ΔE măsurată pe imaginile oficiale (sub 2 nu se vede, 2–5 se vede doar alăturat):

  | Egger | Kronospan | ΔE |
  |---|---|---|
  | W1000 | K8681 Brilliant White | 5,2 (puțin mai rece) |
  | W1000 | K8685 Snow White | 4,3 |
  | W1000 | K8100 Pearl White | 1,5 |
  | U702 | K5981 Cashmere | 3,9 (puțin mai gri) |
  | U702 | K7045 Satin / Champagne | 1,7 |
  | H1145 | K003 Gold Craft Oak | 7,8 (mai auriu, cu crăpături) |
  | H1145 | K076 Sand Expressive Oak | 1,5 (nu există ca blat) |
  | H1145 | K527 Biscotti Hudson Oak | 1,3 |

- **Prețuri** (18 mm, 2800 × 2070, 06.10.2026):

  | Furnizor | Kronospan | Egger, același furnizor |
  |---|---|---|
  | Mambricolaj (în stoc) | K8681 PE, K5981 BS, K003 PW: 279; blat K003 FP 38 mm: 597,95; cant alb 22 × 2: 2,95 lei/m | W1000: 389,95; U702: 409,95; cant W1000: 3,95 lei/m |
  | Regency (preț special) | 8685 BS 264,10; 5981 BS și 7045 SU 313,86; K003 PW 313,87; K076 PW 389,15; alb 114 SM 16 mm 269,38; blat K003 FP 557,48 | 366,42 |

- **Calcul pe cantitățile din devizul R03** (16 + 6 + 2 × 16 mm + 1 + blat):
  - Egger: 9.631,58 lei;
  - varianta A, Mambricolaj: 7.553,71 lei (K8681 / K5981 / K003 + blat K003; 16 mm de la Regency), cu ~2.078 lei mai puțin;
  - varianta B, Regency: 7.518,87 lei (8685 / 7045 / K003 + blat K003; fronturile 7045 sunt practic U702), cu ~2.113 lei mai puțin;
  - cu rezerva de 7%: ~2.220–2.260 lei mai puțin.
- De confirmat:
  - stocul pentru 16 plăci K8681 la Mambricolaj;
  - cantul asortat pentru K8681 și K5981;
  - mostrele fizice ale decorurilor, în magazin.
- Mambricolaj mai are „Pal melaminat Bardolino Krono” la 279 lei, fără cod Kronospan. De întrebat în magazin ce decor e.


## 06.10.2026 — Dulap dormitor separat și organizat
- Nou dulap_dormitor.FCStd, legat în apartament prin Dulap_dormitor_custom. Piesa veche este ascunsă; copii înainte de modificare în _arhiva/2026-10-06_dulap_dormitor.
- Gabarit carcasă 2200 × 600 × 2360 mm; mânerele ies încă 22 mm. Poziția păstrată.
- Două jumătăți egale, fiecare cu 4 sertare (ceasuri cu 8 compartimente, lenjerie, șosete, pijamale), 5 rafturi în modulul lateral, bară de umerașe și suport extractibil cu 8 brațe pentru pantaloni în modulul central; depozitare sus.
- 4 uși, LED lateral, acces prin spate la priza existentă. Interiorul se vede ascunzând grupul Fronturi.
- Vederi în output/Dulap_dormitor_interior.png și output/Dulap_dormitor_detaliu.png; a doua este o prezentare temporară cu extrageri, fișierul CAD salvat are sertarele retrase și ușile vizibile.
- Concept, nu debitare validată: feronerie, jocuri, balamale, fixare anti-răsturnare de dimensionat. Devizul anterior considera dulapul păstrat, deci nu include încă această reorganizare. Randările Blender și PDF-ul de mobilare nu au fost regenerate în această intervenție.


## 06.10.2026 — Dulap dormitor: LED și feronerie
- Confirmat de utilizator: două bare de cămăși în TOTAL, cele deasupra pantalonilor, la 1940 mm.
- Patru benzi LED cu profile și senzori independenți, lungime utilă totală 5,90 m. Ipoteză 24 V / 7,2 W/m, sursă propusă 60 W; specificațiile produselor de confirmat.
- Modelate gabarite de feronerie: 20 balamale și plăcuțe (alocare provizorie), 8 perechi glisiere sertare, suporturi bare, suporturi rafturi, amortizoare pantaloni, 4 colțare anti-răsturnare. Nu sunt cote de găurire și nici produse validate pentru comandă.
- Necesar orientativ: output/Dulap_dormitor_feronerie_LED.csv; vedere actuală: output/Dulap_dormitor_LED_feronerie.png. Componenta și apartamentul salvate; copii înainte în arhivă.

## 06.10.2026 — Analiză deschidere dulap dormitor
- Verificare geometrică a ușilor între 0–155 grade, pas 1 grad, pe axe de balamale propuse; sertare între 0–450 mm, pas 5 mm. Nu reprezintă cinematica exactă a unui produs ales.
- Ușa 1, lângă noptiera sud: prima intersecție la circa 14 grade. Celelalte trei uși nu intersectează patul/noptierele în această simulare individuală; nu s-a validat deschiderea simultană sau feroneria reală.
- Sertarele inferioare din modulul 0: pijamale circa 130 mm, șosete și lenjerie circa 140 mm până la coliziune cu noptiera. Sertarul de ceasuri, fiind mai sus, nu lovește noptiera.
- Soluție preferată pentru studiu: fronturi glisante plus schimbarea modulelor interioare de pe jumătatea de lângă noptieră: umerașe/pantaloni în colț, sertare în modulul alăturat. Șinele și lățimea de acces trebuie dimensionate înainte de implementare.
- Alternativă simplă: modulul din colț deschis, cu aceeași mutare a sertarelor. Schimbarea sensului ușii nu este presupusă suficientă; nu a fost validată.
- Fișiere de analiză în output/Analiza_usi_dormitor.FCStd, PNG și Analiza_deschidere_dulap_dormitor.json. Mobilierul nu a fost mutat în această analiză.

## 06.10.2026 — Plan de debitare R03 complet, prețuri Kronospan, deviz R04, randări refăcute
- **Lista de piese completă**, din fișierele FreeCAD salvate (`scripturi/inventar_freecad_mobilier.py` → `tmp/inventar_freecad_mobilier.json`).
  - În model, corpurile bucătăriei, noptierele, comodele, machiajul și sertarele erau blocuri pline. Planul R02 le estima.
  - Acum sunt desfăcute pe plăci după reguli fixe (`scripturi/lista_debitare_R03.py`): 360 de piese, 175 de rânduri.
  - Regulile:
    - cote finite cu cant;
    - fronturi cu cant 2 mm pe toate laturile;
    - sertare Blum MOVENTO cu lățimea interioară = lumina corpului − 42 mm, lateralul = lungimea glisierei − 10 mm, fund de 16 mm retras 13 mm;
    - spate HDF;
    - piesele de peste 2770 mm îmbinate pe despărțitori.
  - Dulapul din hol folosește lista exactă existentă, verificată cu modelul.
- **Optimizare verificată** (`scripturi/optimizare_debitare_R03.py`): margine de 15 mm (Regency primește piese de cel mult 2770 × 2040), pânză 4,4 mm, tăieturi ghilotină, stejarul fără rotire, peste 12.000 de așezări încercate.
  - Verificarea automată confirmă: fiecare piesă apare o dată, în zona utilă, fără suprapuneri.
  - **Rezultat:** 12 plăci albe de 18 mm, 6 cashmere, 1 stejar, 2 albe de 16 mm, 4 HDF și 1 blat 4100 × 600. Devizul R03 avea 16 / 6 / 2 / 6 / 1.
  - Cant: 306 m de 2 mm, 61 m de 0,4–0,8 mm, 13 m de 42 × 2. Găuri de balama: 101 (tabelul Blum).
- **Decoruri Kronospan alese.** Echivalențele Egger → Kronospan vin din tabelele furnizorilor de cant (Regency):

  | Egger | Kronospan |
  |---|---|
  | W1000 | 8685 BS Snow White (sau 101 PE / 114 PE) |
  | U702 | 5981 BS Cashmere |
  | H1145 | 3025 SN Sonoma (Light Vintage Oak) |

  Alternativa ieftină la stejar e K003 Gold Craft Oak (279 lei la Mambricolaj, ton mai auriu).
- **Prețuri** (06.10.2026, cu TVA):
  - Regency: 8685 BS 264,10; 8685 SM 16 mm 257,59; 5981 BS 313,86; 3025 SN 307,07; K003 PW 313,87; HDF alb 2,5 mm 83,79; blat 3025 WO / K003 FP 557,48.
  - Mambricolaj, în stoc: K8681 PE, K5981 BS, K003 PW la 279; blat K003 FP 597,95.
  - Hornbach: 3025 285; 5981 287; alb 0110 259.
  - Mathaus: alb 114 SM / PE / BS 272,76.
  - **Servicii Mambricolaj** (listă publică):
    - debitare PAL 45,95 lei / foaie, HDF 27,95, blat 34,95;
    - căntuire 3,95 lei/m (22 mm), 6,95 lei/m (42 mm);
    - gaură de balama 5,95 lei; decupaj 74,95 lei; dublare 19,95 lei/m².
    - Tarifele vechi din R03 (1,79 lei/m debitare, 2,54 lei/m cant) nu mai sunt valabile.
  - Regency: serviciile se ofertează din fișierul lor `tabel_optimizare.xlsx` (de descărcat după acord).
- **Cost exact pe aceleași cantități** (`scripturi/cost_debitare_R03.py`):
  - Regency 11.577 lei (serviciile estimate cu tarifele Mambricolaj);
  - Mambricolaj 11.751 lei;
  - cu plăci Egger: 13.858 lei.
- **Fișiere noi:**
  - `output/pdf/Apartament_184_Plan_debitare_R03.pdf` (24 de planșe: sumar, reguli, costuri, toate hărțile, lista de piese, cant, balamale);
  - `Debitare_R03_comanda.xlsx`;
  - `Deviz_materiale_ap184_R04.xlsx` + `output/pdf/Apartament_184_Deviz_materiale_R04.pdf`;
  - `output/pdf/Apartament_184_Plan_lucrari_R02.pdf`.
- **Deviz R04** (`scripturi/deviz_R04_kronospan.py`): 88.313 lei la cele mai bune oferte (94.495 cu rezerva de 7%). R03 avea 90.598 / 96.940.
  - Balamalele sunt corectate după tabelul Blum: dressing 35, bucătărie 22.
- **De confirmat** înainte de comandă:
  - spălătoria are nevoie de două separatoare (golurile 664 + 264), nu de unul;
  - mașina de vase e incorporabilă, deci primește front cashmere;
  - blaturile noptierelor și al comodei TV sunt din două plăci lipite (36 mm);
  - spatele dulapului din baie și al nișei de detergenți e din PAL de 16 mm;
  - stocul de 12 plăci albe.
- **Texturi** (`texturi/LICENTE.md`):
  - Kronospan, oficiale, nu CC0: 8685, 5981, 7045, K8681, K8100, K101, K076, K003, 3025 + scanările plăcii întregi 3025 (43 MB) și K003 (36 MB), scoase singure din arhivele de 2 GB; structurile PE, BS, SU, PW, FP, SM, SN, transformate în hărți de relief (`scripturi/structuri_kronospan_relief.py`);
  - CC0 pentru baie: ambientCG Concrete046 și Poly Haven plastered_wall_04.
- **Blender** (copia de dinainte în `_arhiva/2026-10-06_kronospan_baie_dormitor/`). Materialele, aplicate de `scripturi/materiale_kronospan_blender.py`:
  - R_Egger_W1000 = Kronospan 8685 BS;
  - R_Egger_U702 = 5981 BS;
  - R_Stejar_natural_H1145 = 3025 SN.

  Stejarul folosește scanarea plăcii la mărime reală, cu fibra pe lungimea fiecărei piese. Mașina de vase are front cashmere. Numele materialelor au rămas cele vechi; decorul real e în proprietatea „decor”.
- **Corecturi în scenă** (`scripturi/baie_dormitor_fix_blender.py`):
  - baia: microciment olive grey #7F7D6C, lumină de 4000 K, obiectiv de 16 mm;
  - patul: cadru și tăblie din stejar Sonoma, saltea, pilotă căzută pe margini, perne sprijinite, pled (vechile obiecte sunt doar ascunse);
  - voalul: avea material cu refracție, ca sticla, care dădea „lamelele” albe de deasupra caloriferului; acum e țesătură translucidă cu pliuri netede;
  - draperiile: pliuri sinusoidale netede;
  - camera D_01 e mutată;
  - plăcile de mobilier au muchii rotunjite de 1 mm (doar la randare).
- **Randări** (`scripturi/randeaza_R04.py`, cu expunere automată pe fiecare unghi, țintă: mediana 0,58 ziua și 0,42 seara): toate cele 15 unghiuri, zi și seară, plus planul 3D. Cele vechi sunt în `_arhiva/2026-10-06_kronospan_baie_dormitor/randari_inainte/`.


## 06.10.2026 — Corp îngust spate pat și tablou
- Pat avansat 150 mm spre televizor, fără deplasare laterală. Ambele noptiere ascunse, păstrate reversibil.
- Corp separat corp_spate_pat.FCStd: 130 mm adâncime, 1600 mm lățime, blat la 1120 mm deasupra tăbliei existente; legat în apartament. Tablou geometric 1100 × 700 mm, centrat, la 1450–2150 mm.
- Distanță CAD minimă pat–mobilier TV: 492,9 mm; spațiul lateral față de dulap rămâne 623 mm. Ușile dulapului verificate individual 0–90 grade față de pat și noul corp, fără coliziuni.
- Prizele vechilor noptiere rămân pe pozițiile existente; relocarea lor nu este inclusă. Randările Blender, PDF-urile și devizul necesită sincronizare ulterioară.
- Previzualizare output/Dormitor_corp_pat_tablou.png: mobilierul TV ascuns doar în vederea de prezentare pentru a se vedea patul.

## 06.10.2026 — Noptieră păstrată și comandă lângă pat
- Noptiera dinspre fereastră (Noptiera_nord) reafișată și avansată 150 mm spre TV, aliniată cu patul. Noptiera dinspre dulap rămâne ascunsă.
- Prizele apropiate de marginea patului: centre Y=-2700 și Y=-850 mm, Z=750 mm, perete X=150 mm. Se păstrează corpul îngust din spatele tăbliei.
- Comandă cap-scară nouă lângă noptiera păstrată: centru Y=-850, Z=900 mm. Întrerupătorul de la intrare este prevăzut ca celălalt cap-scară pentru aceeași plafonieră.
- Geometria și apartamentul salvate; schema de cablare, traseele R09, cantitățile și PDF-urile încă necesită sincronizare. Comanda se leagă pe circuitul de iluminat, nu la circuitul prizelor. Datele schimbărilor sunt în output/Modificari_prize_cap_scara_dormitor.json.

## 06.10.2026 — Salvare FreeCAD și sincronizare Blender
- Salvate 19 documente FreeCAD cu fișiere existente și copii suplimentare ale tuturor documentelor din sesiunea conectată în _arhiva/2026-10-06_salvare_finala/FreeCAD. Documentele istorice deja arhivate nu au fost recreate în rădăcină.
- Sesiunea Blender deschisă a fost salvată înainte de modificări; copii ale fișierului anterior și ale sesiunii salvate în aceeași arhivă.
- Sincronizate 273 de piese pentru dormitor: dulap și interior, LED, feronerie, corp spate pat, tablou, pat, noptiera păstrată, prize și comanda cap-scară. Dulapul simplificat vechi și noptiera sud ascunse. Textilele patului avansate cu 150 mm.
- Verificare gabarite globale Blender față de exportul FreeCAD: toate cele 273 de piese în toleranță de 1 mm. Scena actuală salvată în apartament_184_randare.blend. Camerele, luminile și materialele pieselor existente păstrate.
- PNG-urile de randare și PDF-urile anterioare nu au fost regenerate prin această operație de salvare.

## 06.10.2026 — Corecție material oglindă dormitor
- Cauză verificată în Blender: Machiaj_oglinda_LED avea material R_LED_alb_cald (emisie 7), iar panoul LED din spate era vizibil la randare.
- Aplicat același material R_Oglinda ca pe ușa de oglindă din hol, fără emisie; panoul din spate ascuns. Restabilită banda laterală dinspre fereastră cu scriptul existent.
- Regula materialelor corectată: Machiaj_oglinda_LED este identificată înaintea regulii generale LED.
- Scena salvată și reîncărcată în Blender; verificare vizuală prin randarea output/Oglinda_dormitor_corectata.png. Copie de siguranță în _arhiva/2026-10-06_corectie_material_oglinda.

## 06.10.2026 — Re-randări R04 (zi și seară) și dormitorul Codex în debitare, deviz și planuri
- **Randări** din scena refăcută (`scripturi/randeaza_R04.py`, expunere automată): 16 unghiuri × zi / seară + planul 3D. Unghi nou `D_04_dulap_tablou`. Medianele ies 0,58–0,60 ziua și 0,40–0,44 seara (baia: 0,50 / 0,40).
  - Texturi Kronospan 8685 / 5981 / 3025, baia în microciment olive grey, dormitorul Codex (dulap nou, corp în spatele patului, tablou, o singură noptieră).
  - Copii JPG în `randari/web/{zi,noapte}` (`scripturi/randari_web.py`); `Plan_3D_apartament_184.png` adnotat din nou.
- **Incident 13:13–13:14:** `apartament_184_randare.blend` a fost suprascris de o sesiune Codex pornită dintr-o bază fără PBR.
  - Scena s-a refăcut din scripturi; corecția oglinzii a lui Codex e păstrată (R_Oglinda, panoul LED din spate ascuns).
  - Copii în `_arhiva/2026-10-06_kronospan_baie_dormitor/`: `..._salvat_de_Codex_13-14.blend` și `..._final_R04.blend` (identic cu scena actuală).
- **Lista de debitare R03**: + dulapul de dormitor (DD, 79 de piese), + corpul din spatele patului (CP, 5 piese), noptiera de sud scoasă. Total 420 de piese pe 199 de poziții.
  - Plăci: 17 albe 18, 5 cashmere, 1 stejar, 2 albe 16, 6 HDF (spatele dulapului din 4 bucăți), 1 blat; verificarea automată e OK.
  - Balamale: 121 (+20 la dulap, câte 5 pe ușile de 2276 mm).
- **Cost debitare** (plăci + debitare + cant + găuri):
  - Regency 13.494 lei;
  - Mambricolaj 13.808 lei;
  - cu plăci Egger 16.427 lei.

  Varianta mixtă (cashmere și stejar de la Mambricolaj) economisește doar ~80 lei, pentru că acolo cantul e mai scump.
- **Problemă în modelul Codex (de rezolvat înainte de comandă):** 4 din cele 8 fronturi de sertar interior ating balamalele de jos (cotele 182–218 și 632–668 mm).
  - Fronturile stau la 20 mm de muchie. Cutia de 495,5 mm lasă 16 mm pe parte, iar glisierele cu bile cer 12,7.
  - Piesele DD-F* / DD-S* sunt marcate PROVIZORIU.
  - Numărul de plăci rămâne 17 albe în toate cele 4 variante testate (cotele modelului, glisiere 12,7 mm, distanțiere de 18 sau de 25 mm).
- **Distanța dintre dulap și pat:** 62,5 cm până la cadru și 51 cm până la pilotă. Ușa de 546 mm deschisă la 90° trece de cadru (ca în verificarea Codex), dar împinge pilota cu ~3 cm.
- **Deviz R04:** 92.024 lei la cele mai bune oferte, 121.293 lei alternativa; cu rezerva de 7%, 98.465 – 129.783 lei (R03: 90.598 – 120.344).
  - M105 (nou): feroneria dulapului și a corpului din spatele patului, 1.500 – 2.245 lei.
    - 20 de balamale Blum 71B3550 la 14,54 lei (Feromob) / 16,77 (Regency);
    - 8 perechi de glisiere GTV Versalite Plus+ de 450 mm la 35,75 lei;
    - 2 suporturi de pantaloni la 145–196 lei;
    - mânerele, soclul și organizatoarele sunt estimate.
  - M106 (nou): tabloul de 110 × 70, 250–450 lei, estimat.
  - M076: −2 sertare MOVENTO pentru noptiera scoasă.
  - LED: +1 rolă de bandă, +4 profile, +4 senzori de ușă.
- **Fișiere refăcute:**
  - `Plan_debitare_R03.pdf` (28 de planșe) și `Debitare_R03_comanda.xlsx`;
  - `Deviz_materiale_ap184_R04.xlsx` + PDF (30 de pagini);
  - `Plan_lucrari_R02.pdf`;
  - `Plan_mobilare_R03.pdf` (14 planșe, cu randări de seară și D_04).

  Extragerea planului de mobilare R03 e în `tmp/mobilier_plan_R03.json` (`scripturi/extrage_mobilier_plan_R03.py`). `tmp/mobilier_plan.json` a rămas neatins, pentru planurile electrice ale lui Codex.
- **Documentul de design** (claude.ai, rev 41):
  - 33 de imagini noi;
  - secțiunea „Dulapul nou și tabloul”;
  - decorurile Kronospan, baia olive grey, o singură noptieră;
  - rânduri noi pentru dulap și pentru corpul din spatele patului.
- **Nearhivat intenționat:** Deviz R03 (xlsx + pdf), Plan_debitare_R02, Plan_lucrari_R01 și Plan_mobilare_R02.
  - Rămân în folder pentru că `00_DESCHIDE_PROIECTUL.html` (indexul lui Codex) trimite încă la ele.
  - Se mută în arhivă după ce indexul trece pe versiunile noi.


## 06.10.2026 — Plafonieră debară, draperii și masă de machiaj, coloane termice, scurgere izolată fonic
- **Plafoniera din debară** (`Plafoniera_LED_Nisa` și punctul L05) mutată la mijlocul coridorului liber dintre rafturi: X 10400 → 10199, Y −1860 → −1835.
  - Montajul electric (`montaj_electric_R03`, TR17, B18) nu a fost atins: traseele spre L05 se reverifică pe noua poziție.
- **Draperii dormitor:** șina și cele două panouri, cu 175 mm în cameră (Y ≈ −497…−460), ca în sufragerie, ca să acopere radiatorul R1 (Y −423…−320).
  - Blatul mesei de machiaj scurtat de la 800 la 630 mm, începând la Y −530 (`perete_TV_dormitor.FCStd`: Machiaj_corp, fronturile cu 311 mm). Oglinda a rămas de 80 × 174.
  - Lista de debitare: MJ-01 630, MJ-04 594, fronturi 311, cutii de sertar pe lumina de 287. Plăcile rămân aceleași (17 / 5 / 1 / 2 / 6).
- **Două coloane de agent termic** în colțul dormitor–sufragerie, pe partea radiatorului: țevi Ø26,9 de la pardoseală la tavan, la X 3465 și 3525, Y −280, în spatele draperiei.
  - Poziție, diametru, material, sens tur/retur și legătura cu C1 din planul R01 (simbol în sufragerie, X ≈ 3755) sunt de măsurat.
- **Racordurile radiatoarelor** R1 (dormitor) și R2 (sufragerie) la coloane: multistrat 16 × 2, Z 70 și 110 mm, sub radiatoare (`Racord_R1_A/B`, `Racord_R2_A/B`).
  - Ramurile spre sufragerie trec prin peretele despărțitor de 150 mm (X 3550–3705) pe la traversarea existentă, de verificat. Nu se fac șanțuri noi.
  - Traseele sunt indicative; regimul mono/bifilar nu e cunoscut.
- **Radiatorul din baie (R3):** nu se știe de unde vine agentul termic. Planul termic R02 și planul sanitar R02 au o planșă nouă de note (T10 / S10) cu:
  - ce se verifică (țevi tur/retur în zona băii, ACM sau încălzire, termoficarea, posibilitatea de racord la cele două coloane);
  - decizia „schimbăm totul pe PPR în baie?”. PPR PN20 simplu nu e pentru agent termic la temperatura turului din termoficare; pentru încălzire PPR armat sau multistrat, confirmat cu instalatorul.
- **Scurgerea mașinii de spălat:** coloana de canalizare PP Ø110 trece prin colțul vestibul–sufragerie (model: X 3450, Y −5450, de măsurat).
  - Izolată fonic: vată minerală 40 mm + membrană fonică (Ø190), într-o mască de gips-carton 2 × 12,5 mm de ~22 × 22 cm, cu trapă de acces.
  - Mobilierul ocolește masca: rafturile coloanei laterale de la 624 la 382 mm adâncime (SP-11 / SP-12), panoul lateral drept 405 mm (SP-01b), capacul de sus cu decupaj în colț (SP-03), robinetul de rezervă cu 250 mm spre ușă.
  - Deviz R04: M107 (izolație fonică + mască), 350–700 lei, estimat. Total R04: 92.356 lei la cele mai bune oferte, 98.821 – 130.512 cu rezerva.
- **Blender:** coloanele, racordurile, scurgerea și mobilierul modificat sunt aplicate (`scripturi/coloane_termice_scurgere_blender.py`). Exportul din FreeCAD (758 de piese) față de scenă: zero piese noi; singura diferență de geometrie e netezirea draperiilor, lăsată ca atare.
- **Texturi PBR descărcate:** toate seturile sunt legate de materiale (`scripturi/texturi_complete_blender.py`).
  - S-au adăugat hărțile care nu erau folosite: AO (Carpet016, Travertine009), displacement (Travertine009, Metal009), Metalness (Metal009), normala Concrete046 și rugozitatea / difuzia plastered_wall_04 la microcimentul olive, difuzia painted_concrete (rășină), wool_boucle (bucle).
  - Profilele și cadrele metalice plate din FreeCAD au trecut pe metalul periat.
- Copii de dinainte: `_arhiva/2026-10-06_plafoniera_debara/`, `_arhiva/2026-10-06_coloane_termice_scurgere/`.
- **Nerefăcut:** planurile electric, sanitar și termic au încă fundalul de mobilier din `tmp/mobilier_plan.json` (fără coloanele noi). Planul de mobilare R03 trebuie regenerat după randări.
- **Randări R04 refăcute la 21:00–21:40** (zi + seară, toate unghiurile, plus planul 3D și JPG-urile web), după coloane, racorduri, texturile complete și noua poziție a plafonierei din debară.
  - Voalul transparent din dormitor (`D_Voal_dormitor`) a fost mutat cu 190 mm în cameră, în fața radiatorului; fără el radiatorul se vedea în fața voalului.
  - Plan de mobilare R03 regenerat (14 planșe) din `tmp/mobilier_plan_R03.json` nou.
  - Documentul de design (rev 45): toate cele 33 de imagini înlocuite, plus propoziții noi despre coloana de scurgere și cele două coloane termice.

## 07.10.2026 — Coloană de duș, baterie lavoar, canapea Puma
- **Coloana de duș Alessandro Design 9710N** (https://www.alessandrodesign.ro/products/coloana-de-dus-inox-sus304-satinat-9710n), Gun Grey: baterie 270 × 30 × 30 mm, pălărie pătrată 220 × 220 × 10 mm, pară 210 × 30 × 10 mm, 380 mm de la perete.
  - Fișa dă „înălțime 78 cm, 110 cm”: am luat 1100 mm pentru țeava verticală (de la axa bateriei) și 780 mm pentru suportul parei. De confirmat cu produsul.
  - Montaj pe peretele cu scafa de gips (masca cu nișe, fața la y = −5420): axa bateriei la x = 500, z = 1200 mm, pe banda plină dintre nișe; pălăria la z ≈ 2280 mm; suportul parei la x = 780, z = 1650. Corectat la cererea beneficiarului (prima variantă era pe peretele lung). Poziția e propusă, nu măsurată.
  - Rozetele, maneta și traseul furtunului sunt aproximări după fotografii. Piese: `Coloana_dus_*` în `baie.FCStd`.
- **Baterie lavoar 9707N** (https://www.alessandrodesign.ro/products/baterie-lavoar-monocomanda-cartus-ceramic-alama-sanitara-gri-satin-racorduri-si-kit-fixare-incluse-9707n): lungime 190 mm, înălțime 180 mm, pipă fixă, 1 orificiu, Gun Grey. A înlocuit simbolul cilindric `Baterie_lavoar`, la (1250, −5500), cu baza pe marginea lavoarului; maneta stă la 8 mm de oglindă.
- **Canapea Puma, Dedeman 8119379** (1.599 lei): 215 × 76 × 87 cm, crem, stofă, extensibilă. Spatele la peretele din est, același centru (y = −2800), față la x = 6340; înainte era JYSK ILDVED 220 (950 mm adâncime).
  - Piese `Canapea_*` în `apartament_184.FCStd`; canapeaua veche e ascunsă, nu ștearsă. Fișa nu dă adâncimea șezutului, înălțimea picioarelor sau lățimea brațelor; sunt luate după poză.
  - **Neactualizat:** rândul canapelei din deviz (JYSK ILDVED) și planul de mobilare, care încă folosesc canapeaua veche.
- Scena de randare: `baterii_baie_blender.py`, `canapea_puma_blender.py`, cameră nouă `CZ_05_canapea` (`camera_canapea_blender.py`). Copii în `_arhiva/2026-10-07_baterii_baie/`.
- **Incident 07.10.2026:** salvarea headless a `baie.FCStd` a șters `GuiDocument.xml`, deci în FreeCAD toată baia apărea ascunsă. Remediat din copia din `_arhiva/2026-10-07_baterii_baie/` și salvat din interfață; geometria nu s-a pierdut. Randările de după 01:55 sunt incomplete (zi oprită la `D_01`) și se refac.

## 07.10.2026 — Electric R11 (Claude): verificarea R10 + trasee copex + ghid de instalare
- **Verificare R10 (ChatGPT/Codex), probleme blocante:**
  - 17 tuburi coborau din tablou prin mijlocul golului ușii de intrare;
  - 18 tuburi treceau sub pragul ușii de intrare;
  - până la 21 de tuburi erau pe aceeași axă, cu încrucișări nerezolvate;
  - S03 trecea prin peretele plin bucătărie–hol;
  - lanțurile C04/C05 depășeau 5 % cădere de tensiune la 16 A;
  - aplicele liniare de pe peretele TV din sufragerie și banda LED a oglinzii nu aveau tub;
  - copex Ø25 la 3×2,5 era supradimensionat.
- **Decizii beneficiar 07.10:**
  - **iluminatul din întrerupător pe tavan**: pe jos L, N, PE până la întrerupător, apoi retur, N, PE prin perete și șanț în tavan până la lampă, cu tub Ø16. Dozele J01–J06 din R10 nu mai există;
  - **fără tavan fals**.
  - Șanțul în placă se face numai cu aviz structural și detector de armătură; tubul vechi din placă e preferat.
- **R11:**
  - 56 de tuburi: 22 de plecări 230 V din TE, care coboară într-o casetă de gips-carton pe peretele nordic al holului (TE rămâne deasupra ușii, legat printr-o cornișă);
  - copex Ø20 la forță, Ø25 la date, Ø16 pe tavan și la SELV;
  - un tub = un circuit; date în tuburi separate, la ≥ 150 mm de forță;
  - 0 încrucișări în mănunchiurile principale; 64 de perechi în 10 zone X, numai locale;
  - C04, C05, C10 au câte 2 plecări; toate circuitele sunt sub 3 % (iluminat) și 5 % (prize);
  - S02 devine dublu (tasta 2 = aplice AP1/AP2); V01 = 24 V spre oglinda din dormitor;
  - F01/F02 trec pe C05, F03 pe C04, F04 pe C12, hota pe C14, aprinderea plitei pe C08;
  - NET mutat la X 7350, P23 la X 7600.
- **Fișiere:**
  - `scripturi/trasee_copex_R11.py` → `tmp/electric_R11/trasee_R11.json`;
  - `scripturi/freecad_trasee_R11.py` → `montaj_electric_R11_copex.FCStd`, salvat din GUI;
  - `scripturi/ghid_instalare_electric_R11.py` (cu Python-ul Codex) → `output/pdf/Apartament_184_Ghid_instalare_electrica_R11.pdf` (24 de pagini) + `Apartament_184_Tuburi_fire_R11.csv`.
  - Fișierele R10 Codex și documentul FreeCAD `montaj_electric_R10_revizie` nu au fost atinse.
- **Deschis:**
  - M1 înălțimea de la placă la pardoseala finită. **Corecție 07.10:** acum nu există șapă; tuburile se pun pe placă și se toarnă șapă nouă peste ele. Grosime minimă ≥ 50 mm pe benzile simple și 65–70 mm la încrucișări. Autonivelanta de 5 mm din deviz nu ajunge, trebuie șapă cimentoasă armată;
  - ghidul corectat este `Apartament_184_Ghid_instalare_electrica_R11a.pdf` (R11 era blocat, deschis la beneficiar);
  - M2 pereții structurali; M3 aviz pentru placă; M4 tuburile existente din placă; M5 bransamentul;
  - D1 tabloul deasupra ușii nu încape în 2 rânduri (recomandat pe peretele nordic al holului, în capul casetei);
  - D2 NET în hol sau în sufragerie (în sufragerie ar dispărea majoritatea încrucișărilor forță × date);
  - D3 modelul aplicelor (230 V sau 24 V).
  - Devizul nu e încă recalculat pentru R11.

## 07.10.2026 — Aer condiționat dormitor (un singur aparat), C15, import în Blender
- **Decizie beneficiar:** un singur AC, în dormitor, foarte aproape de perete, cu aerul spre masa de machiaj. Fără AC în sufragerie. Conductele se maschează cu riflaje, **bandă de la podea la tavan, subțire** (190 × 80 mm).
- **Model în `apartament_184.FCStd`** (grup `AC_Aer_conditionat`, obiecte `AC_*`):
  - unitate interioară 9.000 BTU, profil 190 mm, pe peretele vest în colțul de nord, baza la 2090 / vârful la 2340 mm, aerul pe axa x spre masă (x 3340 / y −845);
  - mască de riflaje în colț (x 150–230, y −440…−250, de la parchet la 2495), aceleași lamele ca la peretele TV (27 × 21 mm, pas 40, suport închis la culoare); lamelele dintre 1,96 și 2,20 m se demontează pentru acces;
  - conducte frigorifice + condens prin fațadă la x 184 / z 2085 și 2045 (pantă spre exterior), toate în cavitatea măștii; unitate exterioară pe consolă de fațadă, x 150–950, y 80–380, z 1250–1800;
  - tub electric C15 în mască, de la podea la 2200 mm.
- **Plan electric R11 actualizat:** circuit **C15** (RCBO B16 30 mA, 3 × 2,5 mm²), tub T15 Ø20 din tablou la unitate, ~20 m, ΔU 2,5 %. Acum 57 de tuburi, 15 circuite. `montaj_electric_R11_copex.FCStd` regenerat din GUI, Ghid PDF `Apartament_184_Ghid_instalare_electrica_R11b.pdf` (capitol 10b nou, decizia D4: unitate exterioară pe fațadă cere acordul asociației), CSV și `Lista_achizitii_electric_R11.xlsx` actualizate (cablu 4 × 1,5 spre exterior, kit AC la montator).
- **Blender (`apartament_184_randare.blend`):** adăugat AC (colecția `Aer_conditionat_dormitor`, materiale din scenă: riflaje `R_Stejar_deschis_riflaje`, suport `R_Pasla_antracit`). Aplicate și diferențele rămase din 07.10, care lipseau din .blend: `baterii_baie_blender.py` (coloana de duș 9710N, bateria 9707N), `canapea_puma_blender.py` (Puma, canapeaua veche ascunsă) și `camera_canapea_blender.py` (CZ_05). Randare de verificare: `output/Randare_AC_dormitor_D01.png` (D_01, 48 de eșantioane, nu randare finală). Randările R04 din `randari/` NU sunt refăcute.
- **Copii înainte:** `_arhiva/2026-10-07_ac_in_apartament/` (apartament_184, apartament_184_randare.blend, montaj_electric_R11_copex, CSV); `_arhiva/2026-10-07_aer_conditionat/` (propunerile vechi cu 2 aparate / v1 cu bandă).
- **Salvat:** `apartament_184.FCStd` și `montaj_electric_R11_copex.FCStd` din interfață. Celelalte documente deschise erau nemodificate. `plan_3D.blend` nu a fost atins.
- **Deschis:** acordul asociației pentru unitatea exterioară pe fațadă, verificarea peretelui de fațadă la gaura Ø65 (la ~3 cm de colț), poziția tabloului (D1) și cutia NET (D2), tabloul de 15 circuite în 2 × 18 module; devizul R04 nu include AC, C15 și noile cantități; Plan_mobilare, planurile electric/sanitar/termic și randările R04 nu arată AC.

## 2026-10-07 – Biblioteca de feronerie 3D R2 (acuratețe maximă, pentru toată casa)
- Căutare online: modelele STEP oficiale Blum există doar în portalul Blum E-SERVICES (cont gratuit, se face de proprietar). Häfele / PARTcommunity / TraceParts cer și ele cont. Până atunci, modelele sunt construite din fișele oficiale.
- Surse folosite:
  - Blum Product details 71T3550 / 71B3590: flanșă 57 × 22 × 3,2; cupă Ø35 × 13; găuri 45 / 9,5; braț 21,5;
  - MD „CLIP top BLUMOTION, CLIP top, CLIP” (11.24): plăcuța 173L6100 are H 8,5 la D 0, găuri la 32 / 37; șuruburi 3,5 × 17 în ușă;
  - MD-019 TIP-ON uși: Ø10 × 50, adaptor 53 mm, ax la 14,5, placă Ø15;
  - catalog Blum 2024/25 p. 419 (secțiune MOVENTO 28,5 / 21, SKW = LW − 42, SKL = NL − 10) și p. 426 (șuruburi 609.1500 / 609.1700);
  - McFeely's pentru confirmat 7 × 50 (cap Ø10, umăr Ø7 × 9, filet 38, miez Ø4,76);
  - DIN 7505 / EN 14592 (șuruburi PAL), DIN 68150 (cep), ISO 7089 (șaibă).
- 35 de modele, solide reale în FreeCAD (filet elicoidal, locaș PZ2 / hex 4):
  - 12 „exact” (standard / fișă oficială);
  - 11 „gabarit” (Blum: cote de montaj exacte, mecanism simplificat);
  - 12 „generic” (produsul nu e ales încă).
- Fișiere:
  - `feronerie_3d.FCStd` (salvat din GUI, cu culori și proprietăți);
  - `tmp/feronerie_R2/step/*.step` (+ `feronerie_toate.step`), `obj/`, `png/`, `feronerie_3d.blend`;
  - planșa `catalog_feronerie_R2.png`.
- Scripturi: `feronerie_catalog.py` → `feronerie_cad.py` → `feronerie_cad_export.py` (freecadcmd) → `feronerie_blender_R2.py`. Versiunea v1 e în `_arhiva/2026-10-07_feronerie_v1/`.
- Corecturi în montajul noptierei:
  - glisierele MOVENTO se prind cu șuruburi Blum 3,5 × 15 (609.1500), nu 4 × 16;
  - s-au adăugat clemele de cuplare T51.7601 (P), cu pasul 4;
  - randările plăcilor folosesc biblioteca R2.
- De făcut:
  - glisierele din modelul de montaj al noptierei (casete 5 × 22) trebuie aliniate la secțiunea MOVENTO reală;
  - PDF-ul noptierei R04 se regenerează după aprobare;
  - dacă proprietarul își face cont Blum E-SERVICES, piesele Blum se înlocuiesc cu STEP-urile oficiale.

## 2026-10-07 – Montaj noptieră R04 (cu feroneria 3D)
- `output/pdf/Apartament_184_Montaj_noptiera_R04.pdf` (41 de pagini). Pipeline: `python montaj_rulare.py noptiera spec|blender|panouri`, apoi `pdf` cu Python-ul Codex.
- Fiecare pas are:
  - banda de feronerie (iconiță 3D, literă, număr de bucăți numărate din model);
  - imagine explodată stil IKEA: piese noi turcoaz, feronerie nouă portocalie, linii punctate până la gaură;
  - „Rezultat” (pasul montat) și „Detaliu”.
- Corecturi față de R03, după catalogul Blum (2022/23 p. 437, 2024/25 p. 419 / 428) și MD TIP-ON BLUMOTION:
  - glisierele MOVENTO se prind cu 3 șuruburi 609.1500, la 37 / 69 / 261 mm de muchia din față;
  - axa șuruburilor e la 57 mm (sertarul de jos) și 223 mm (sertarul de sus) de muchia de jos a lateralului; sunt incluse +1 mm cerute la montajul înainte de asamblare;
  - cutia sertarului:
    - fundul e retras 13 mm (în R03 era 10, iar fața interioară se suprapunea cu fundul);
    - cutia stă la muchia din față a corpului (în R03 era cu 32 mm mai în spate);
    - fiecare lateral are în capătul din spate o gaură Ø6 × 10 pentru cârlig (la 7 mm de fața exterioară și 11 mm de jos);
  - TIP-ON BLUMOTION se clipsează pe glisieră, nu pe bază; bara de sincronizare se taie la LW − 267 = 197 mm;
  - clemele de cuplare T51.7601 sunt adăugate.
- Ordinea pașilor:
  1. blatul dublu se lipește primul;
  2. glisierele pe laterale;
  3. corpul;
  4. spatele;
  5. cutia de susținere, fixată din interiorul corpului cu 4 × 4×30;
  6. TIP-ON BLUMOTION și bara;
  7. cutiile de sertar și clemele;
  8. fronturile;
  9. blatul (4 × 4×30 din cutie), capacul N-08 și LED-ul;
  10. capacele;
  11. peretele.
- Cantități din model: 54 de confirmate (+6 rezervă), 26 de cepuri, 20 de șuruburi 609.1500, 14 șuruburi 3,5×16, 8 șuruburi 4×30, 8 șuruburi 4×25 cu 8 șaibe și 12 capace.
- Planul de debitare R03 nu se schimbă: dimensiunile pieselor sertarelor erau deja corecte.

## 2026-10-07 – Planuri de montaj R04 pentru toate cele 12 corpuri
- `output/pdf/Apartament_184_Montaj_<corp>_R04.pdf`:
  - noptiera, dulap_wc, comoda_tv_dormitor, machiaj, comoda_tv_zi, corp_spate_pat, debara;
  - dulap_hol, dressing, spalatorie, bucatarie, dulap_dormitor.
- Pipeline:
  - `python montaj_rulare.py <corp> all` (spec, Blender, panouri), apoi `pdf` cu Python-ul Codex;
  - lot: `tmp/run_batch.sh <corpuri...>`;
  - specificațiile sunt în `montaj_spec_*.py`; biblioteca comună e în `montaj_lib.py` (balamale, TIP-ON, pini, agățători, picioare, spate, îmbinări ascunse) și `montaj_comun.py` (lista de feronerie generată din model, literele comune).
- Probleme găsite și rezolvate în planuri (de confirmat la comandă):
  - **Ridicarea corpurilor înalte:**
    - dulapul de pe hol: cu picioare, diagonala e 2527 mm, peste tavanul de ~2500 → se ridică fără picioare (2450);
    - spălătoria (2460 × 650): diagonala e 2544 → se asamblează în picioare, pe loc.
  - **Balamale diferite de deviz:**
    - spălătoria are uși încastrate → 10 × 70T3750 (în deviz 70T3550/70T3650);
    - dulapul din dormitor are ușile 2 și 3 semiaplicate pe despărțitorul din mijloc → 10 × 71B3650 + 10 × 71B3550 (în deviz 20 × 71B3550); balamalele ușii 3 sunt decalate cu 40 mm;
    - dressing: 14 × 70T3550 + 21 × 70T3650 (deviz 6 + 29);
    - bucătăria: 22 × 70T3550 (deviz 10 + 14).
  - **Plăcuțe pe ambele fețe ale despărțitorilor:** fiecare despărțitor are plăcuțe pe o singură față; unde au rămas pe ambele fețe, balamalele sunt decalate.
  - **Glisiere MOVENTO pe ambele fețe ale despărțitorului:** șuruburi decalate, 37/101/261 pe o față și 69/133/229 pe cealaltă.
  - **Sertarele interioare din dulapul din dormitor** (provizorii) sunt retrase la 515 mm, ca să nu atingă brațele balamalelor.
  - **Dimensiuni de verificat în R03:**
    - machiaj: despărțitorul MJ-03 are 397, trebuie 384;
    - corp spate pat: spatele CP-03 are 1564 încastrat, recomand 1600 aplicat;
    - spălătorie: polița extractibilă SP-09 are 530 și cere distanțiere de 46 mm (sau poliță de 622).
  - **Machiaj:** bara de sincronizare TIP-ON BLUMOTION se calculează cu LW − 241 = 47 mm (LW ≤ 293).
  - **Comode TV dormitor și machiaj:** blatul și baza de stejar nu au confirmate vizibile (cepuri + colțare pe interior).
