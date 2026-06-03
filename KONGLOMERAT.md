# ANTI-PALANTIR KONGLOMERAT
## Defensive Überwachungsgegeninfrasktur für linke Organisationen

*Entwickelt von Tobias Buß | 2026*

---

## Politische Einordnung

Der Kontext ist real: Staatliche Repression gegen linke, antirassistische und
klimabewegte Organisationen nimmt zu. Palantir, Clearview, NSO Group und
nationale Datenbehörden bauen Infrastruktur zur Bewegungsüberwachung.

Dieses Konglomerat baut eine defensive Gegenkraft — keine Angriffswerkzeuge,
sondern Infrastruktur für **digitale Selbstverteidigung, kollektive Resilienz
und Systemkritik durch Transparenz**.

Das Erstellen und Betreiben dieser Infrastruktur ist rechtlich zulässig.

---

## Produktportfolio

```
┌─────────────────────────────────────────────────────────────────┐
│                    ANTI-PALANTIR KONGLOMERAT                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [1] ANTI-KI          Narrative & OPSEC-Geheimdienstcenter     │
│      tib019/anti-ki   Kern der Gesamtarchitektur               │
│                                                                 │
│  [2] CYBERSYN 2.0     Dezentrale Energiekoordination           │
│      tib019/cybersyn2-hamburg  VSM-Simulation Nordeuropa       │
│                                                                 │
│  [3] PROLETARIA-LLM   Lokales politisches Sprachmodell         │
│      tib019/proletaria-llm  Privacy-first LLM-Infrastruktur    │
│                                                                 │
│  [4] INTERVIEW COPILOT  Vorbereitung auf Verhöre/Befragungen   │
│      tib019/interview-copilot  Lokale Verhörtrainingssoftware  │
│                                                                 │
│  [5] PHANTOM (OSINT)  Öffentliche Quellen-Analyse              │
│      tib019/osinttoolprolatraion  Defensive OSINT-Basis        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Architektur der Integration

```
                    ANTI-KI (Kern)
                   ┌─────────────┐
                   │  Narrativ-  │
                   │  analyse    │◄──── PHANTOM (OSINT Input)
                   │             │
                   │  OPSEC-     │◄──── ExposureScanner
                   │  Module     │◄──── CommPatternAnalyzer
                   │             │◄──── SurveillanceDB
                   │  Algedonic  │      (Bedrohungswissen)
                   │  Channel    │
                   └──────┬──────┘
                          │
              ┌───────────┴───────────┐
              │                       │
    ┌─────────▼──────┐     ┌──────────▼────────┐
    │ PROLETARIA-LLM │     │ INTERVIEW COPILOT │
    │ Lokale Inferenz│     │ Verhör-Training   │
    │ Mistral-7B+LoRA│     │ Electron-App      │
    └─────────┬──────┘     └──────────┬────────┘
              │                       │
              └───────────┬───────────┘
                          │
                 ┌────────▼───────┐
                 │  CYBERSYN 2.0  │
                 │  Resilienz-    │
                 │  Simulation    │
                 │  (Infrastruktur│
                 │   Planung)     │
                 └────────────────┘
```

---

## Modul 1: ANTI-KI

**Zweck:** Zentrales Analyse- und Geheimdienstzentrum

**Komponenten:**
- `agents/analyst.py` — Narrativdetection, Koordinationsanalyse, Gegennarrative
- `graph_db/` — Neo4j Netzwerkanalyse (Verbreitungsinfrastruktur)
- `rag/` — ChromaDB Vektorstore (Kontextgedächtnis)
- `llm_core/` — Ollama-Interface (lokale Inferenz, keine Cloud-Abhängigkeit)
- `opsec/` — **Defensives Überwachungs-Gegenzentrum** (neu):
  - `exposure_scanner.py` — Eigene digitale Spuren erkennen
  - `surveillance_db.py` — Wissensbasis: Palantir, Clearview, NSO etc.
  - `dsgvo_automation.py` — Automatisierte Datenschutzrechte-Durchsetzung
  - `comm_pattern_analyzer.py` — OPSEC-Audit der eigenen Kommunikation
  - `algedonic.py` — Algedonischer Kanal: Eskalationsprotokoll bei Kompromittierung
- `api/main.py` — FastAPI REST Gateway (inkl. `/api/opsec/*` Endpoints)

**Analogie:** Wie Palantir Gotham für Behörden — aber invertiert:
statt Bewegungen zu überwachen, schützt es Bewegungen vor Überwachung.

---

## Modul 2: Cybersyn 2.0

**Zweck:** Simulation und Planung dezentraler Energieresilienz

**Aktueller Stand:**
- Stufe 1–4: Hamburg + Schleswig-Holstein + Niedersachsen (validiert)
- Stufe 5: + Benelux (NL/BE/LU) — 6-Knoten fraktales VSM (abgeschlossen)
- Stufe 6: Westeuropa 15+ Knoten (geplant)

**Kernresultat Stufe 5:**
Cybersyn-Koordination transportiert bei Atomausfall Belgien 4,1× mehr
Solidaritätsstrom (1322 GWh) als Marktmechanismus (321 GWh) — bei gleicher
physischer Infrastruktur.

**Politische Relevanz:** Zeigt empirisch dass dezentrale Solidarkoordination
(Beer's VSM) bei Krisen effektiver ist als Marktmechanismen.

---

## Modul 3: ProletariaLLM

**Zweck:** Lokales, privatsphäre-wahrendes Sprachmodell für linke Organisationen

**Geplante Architektur:**
- Basis: Mistral-7B-Instruct
- Fine-Tuning: LoRA auf politischem Textkorpus (Netzpolitik, Jungle World,
  linker Bewegungsliteratur, Parlamentsprotokollen)
- Inferenz: Ollama (kein API-Key, kein Cloud-Provider)
- Integration: Dient als LLM-Backend für ANTI-KI

**Datenschutz:** Alle Daten bleiben lokal. Kein Logging an externe Server.

---

## Modul 4: Interview Copilot

**Zweck:** Vorbereitung auf polizeiliche Befragungen und Verhöre

**Geplante Features:**
- Simuliertes Verhör-Training mit lokaler KI
- Rechtliche Grundlagen DE (Aussageverweigerungsrecht, §55 StPO)
- Rollen-Szenarios (Beschuldigter, Zeuge, V-Mann-Gefährdung)
- Electron-App — läuft lokal, kein Internet erforderlich
- Vernetzung mit ANTI-KI SurveillanceDB (Taktikwissen)

**Zielgruppe:** Aktivistinnen, die mit polizeilichen Maßnahmen konfrontiert
werden können.

---

## Modul 5: PHANTOM (OSINT)

**Zweck:** Öffentliche Quellen-Analyse als defensives OSINT-Fundament

**Funktion im Konglomerat:**
- Sammelt öffentlich verfügbare Informationen über bekannte Überwachungsakteure
- Speist SurveillanceDB in ANTI-KI
- Versorgt Narrativanalyse mit externem Kontext

---

## OPSEC-Grundprinzipien des Konglomerats

1. **Lokal first** — Kein Modul erfordert Cloud-API-Keys für Kernfunktionen
2. **Kein Logging** — Sensible Analysen werden nicht persistent gespeichert
3. **Selbst-Audit** — ANTI-KI nutzt seine eigenen OPSEC-Tools für sich selbst
4. **Dezentralisierung** — Kein Single-Point-of-Failure in der Infrastruktur
5. **Rechtliche Absicherung** — Jedes Feature basiert auf legalen Mitteln

---

## Roadmap

| Priorität | Modul | Aufgabe | Status |
|-----------|-------|---------|--------|
| 1 | ANTI-KI | OPSEC-Module (5 Dateien) | ✅ Abgeschlossen |
| 2 | ANTI-KI | API OPSEC-Endpoints | ✅ Abgeschlossen |
| 3 | Cybersyn | Stufe 5 Simulation + Bericht | ✅ Abgeschlossen |
| 4 | ProletariaLLM | corpus_loader.py | 🔲 Offen |
| 5 | ProletariaLLM | fine_tune.py (LoRA) | 🔲 Offen |
| 6 | ProletariaLLM | serve.py (Ollama-Integration) | 🔲 Offen |
| 7 | Interview Copilot | Electron-App Grundstruktur | 🔲 Offen |
| 8 | Cybersyn | Stufe 6 (Westeuropa 15 Knoten) | 🔲 Offen |
| 9 | PHANTOM→ANTI-KI | integration/phantom_client.py | 🔲 Offen |

---

## Rechtliche Einordnung

Alle Module operieren ausschließlich mit:
- Öffentlich zugänglichen Daten (OSINT)
- Eigenen Daten der Nutzenden (DSGVO-Anfragen)
- Simulierten Szenarien (Cybersyn, Interview Copilot)
- Defensiver Sicherheitsforschung (OPSEC-Audit)

Keine Komponente greift auf fremde Systeme zu, exfiltriert Daten,
führt Angriffe durch oder unterstützt illegale Aktivitäten.

Die Infrastruktur ist mit Datenschutzbüros, Rote Hilfe e.V.,
GFF (Gesellschaft für Freiheitsrechte) und ähnlichen Organisationen
rechtlich koordinierbar.
