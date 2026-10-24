# Renovare Apartament 184

Proiect complet de renovare și design interior pentru Apartamentul 184, inclusiv modele 3D, planuri tehnice, deviz materiale, randări și plan de lucrări.

## 📋 Cuprins

- [Rezumat Proiect](#rezumat-proiect)
- [Structura Proiectului](#structura-proiectului)
- [Documentație Tehnică](#documentație-tehnică)
- [Scripturi și Automatizări](#scripturi-și-automatizări)
- [Decizii și Istoric](#decizii-și-istoric)
- [Linkuri Utile](#linkuri-utile)

## Rezumat Proiect

| Element | Detaliu |
|---------|---------|
| **Suprafață** | Apartament 184 |
| **Start lucrări** | 12.10.2026 |
| **Term preconizat** | ~27.11.2026 (cu rezervă până la 04.12) |
| **Deviz Total (Materiale)** | ~98.465 lei (cu rezervă 7%) |
| **Deviz Mobilier** | 31.207 lei (plăci + atelier + feronerie) |
| **Circuite Electrice** | 15 circuite, 57 tuburi |
| **Modele 3D** | FreeCAD (.FCStd) + Blender (.blend) |

## Structura Proiectului

```
├── 00_DESCHIDE_PROIECTUL.html       ← Punct de intrare principal
├── PROGRES_si_DECIZII.md            ← Istoric decizii și evoluție
├── apartament_184.FCStd             ← Model principal FreeCAD
├── apartament_184_randare.blend     ← Scena Blender (randări)
├── plan_3D.blend                     ← Model Blender 3D
├── feronerie_3d.FCStd               ← Bibliotecă feronerie 3D
├── output/                           ← Randări, PDF-uri, analize
│   ├── pdf/                          ← Documentație PDF
│   ├── prezentari/                   ← Prezenteri beneficiar
│   └── woodworking_pilot/            ← Planșe atelier
├── randari/                          ← Randări Blender (zi/seară)
├── scripturi/                        ← Python scripts
├── texturi/                          ← Texturi PBR (CC0)
├── tmp/                              ← Fișiere temporare
└── _arhiva/                          ← Versiuni istorice
```

## Documentație Tehnică

### Planuri PDF generate (`output/pdf/`)

| Document | Versiune | Pagini | Descriere |
|----------|----------|--------|-----------|
| Plan Mobilare | R03 | 14 | Plan cotat, plan de mobilare, planșe pe încperi, 3D, randări |
| Plan Electric | R03 | 19 | Circuite, aparataj, cabluri pe trasee |
| Montaj Electric | R05 | 46 | Trasee, schemă aparataj, cablu de tăiat pe circuit |
| Plan Sanitar Baie | R02 | 10 | Obiecte sanitare, țevi PPR/PP, fitinguri |
| Plan Termic | R02 | 9 | Radiatoare, racorduri, multistrat |
| Plan Debitare | R03 | 24 | Lista piese, hărți optimizare, costuri |
| Montaje Corpi | R04 | 12× | Instrucțiuni montaj pentru fiecare corp de mobilă |
| Ghid Instalare Electrică | R11b | 24 | Ghid detaliat de instalare electrică |
| Deviz Materiale | R04 | 30 | Deviz complet cu Oferte și Alternative |
| Plan Lucrări | R02 | 7 | Gantt, drum critic, cumpărături pe săptămâni |

### Devizuri

| Versiune | Materiale (cele mai bune oferte) | Cu rezervă 7% | Descriere |
|----------|-----------------------------------|---------------|-----------|
| R04 | 88.313 lei | 94.495 lei | Kronospan, oferte actualizate |
| R03 | 90.598 lei | 96.940 lei | Oferte inițiale |

### Plan de Lucrări

| Etapă | Descriere | Săptămâna |
|-------|-----------|-----------|
| E1 | Demolări, pregătire | S1 (12-13.10) |
| E2 | Electric (tuburi din placă) | S2 (14-15.10) |
| E3 | Șapă, uscător | S3 (16-21.10) |
| E4 | Instalare radiatoare | 13-15.10 |
| E5 | Comandă atelier | 26.10 |
| E6 | Mobileare, montaj | 16-21.11 |
| E7 | Finisaje, instalații sanitare | Black Friday 13.11 |
| E8 | Finalizare, curățenie | ~27.11 |

## Scripturi și Automatizări

Toate scripturile sunt în `scripturi/`:

| Categorii | Scripturi |
|-----------|-----------|
| **PDF Generation** | `plan_electric_R03.py`, `plan_sanitar_R02.py`, `plan_termic_R02.py`, `plan_mobilare_R03.py`, `plan_lucrari_R02.py`, `debitare_pdf_R03.py`, `montaj_electric_R05.py`, `deviz_R04_kronospan.py` |
| **FreeCAD Export** | `export_freecad_headless.py`, `inventar_freecad_mobilier.py`, `lista_debitare_R03.py` |
| **Blender** | `materiale_kronospan_blender.py`, `materiale_pbr_blender.py`, `randeaza_R04.py`, `randari_web.py` |
| **Feromerie 3D** | `feronerie_catalog.py`, `feronerie_cad.py`, `feronerie_cad_export.py`, `feronerie_blender_R2.py` |
| **Montaj** | `montaj_rulare.py`, `montaj_lib.py`, `montaj_pdf.py`, `montaj_spec_*.py` |
| **Analiză** | `cost_debitare_R03.py`, `optimizare_debitare_R03.py`, `compara_freecad_blender.py`, `verifica_usi_dormitor.py` |

## Decizii și Istoric

Vezi `PROGRES_si_DECIZII.md` pentru istoricul detaliat al tuturor deciziilor (de la 05.10.2026).

### Decizii Deschise

| ID | Descriere | Status |
|----|-----------|--------|
| D1 | Poziția tabloului electric | Deschis |
| D2 | Poziția cutiei NET / router | Deschis |
| M1 | Înălțimea placă → pardoseală finită | De măsurat |
| M2 | Pereți structurali | De confirmat |
| M3 | Aviz structural pentru șanț în placă | De făcut |
| M4 | Tuburile existente în placă | De verificare |

## Linkuri Utile

### Furnizori și Produse

- **Egger:** myEGGER portal (cont necesar)
- **Kronospan:** [Digital Library](https://kronospan.com/en_US/express-services/downloads/)
- **Blum:** [E-SERVICES](https://www.blum.com) (cont necesar pentru STEP)
- **Baterii baie:** [Alessandro Design](https://www.alessandrodesign.ro)

### Prețuri Referință (06.10.2026)

| Articol | Preț minim | Furnizor |
|---------|-----------|----------|
| Placă Kronospan 18mm | 264,10 lei | Regency |
| Glisiere MOVENTO Blum | ~35 lei/buc | Feromob |
| Balamă Blum 71B3550 | 14,54 lei | Feromob |
| RCBO ETI tip A | 140 lei | ETI |

## Licențe

- **Texturi PBR:** CC0 (Creative Commons Zero) - Poly Haven, ambientCG
- **Cod Python:** propriu
- **Modele 3D:** date tehnice din fișele producătorilor

---

*Acest document se actualizează automat cu fiecare revizie a proiectului.*
