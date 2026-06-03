# PROLETARIA — Meilensteine

---

## M1: Stack läuft lokal ✅

**Status:** Abgeschlossen (Juni 2026)

### Akzeptanzkriterien
- [x] `git clone --recurse-submodules` funktioniert
- [x] `docker compose up -d` startet alle Services ohne Fehler
- [x] ANTI-KI API erreichbar unter `localhost:8000/docs`
- [x] LLM-Server erreichbar unter `localhost:8001/docs`
- [x] OSINT-Backend erreichbar unter `localhost:8002/docs`
- [x] Neo4j Browser erreichbar unter `localhost:7474`
- [x] `POST /api/opsec/exposure-scan` gibt valides JSON zurück
- [x] `POST /api/opsec/dsgvo/create` generiert lesbaren Brieftext
- [x] Verhör-Trainer: `TrainingSession` durchläuft alle Turns ohne Fehler

---

## M2: ProletariaLLM fine-tuned

**Status:** Offen

### Akzeptanzkriterien
- [ ] QLoRA-Training auf Corpus abgeschlossen (Verlust < 1.5)
- [ ] `Modelfile` für Ollama erstellt und dokumentiert
- [ ] `ollama create proletaria-llm -f Modelfile` funktioniert
- [ ] LLM-Server antwortet mit ProletariaLLM statt Basis-Mistral
- [ ] Evaluation: 80% korrekte Antworten auf politischen Testfragen
- [ ] Politische Bias-Analyse dokumentiert

---

## M3: Verhör-UI in Electron

**Status:** Offen

### Akzeptanzkriterien
- [ ] Verhör-Trainer als Tab in Interview-Copilot-App integriert
- [ ] Alle 3 Szenarien spielbar mit UI (Fragen anzeigen, Antwort eingeben)
- [ ] Echtzeit-Feedback nach jeder Antwort sichtbar
- [ ] TacticAnalyzer: Erkannte Taktik wird farblich hervorgehoben
- [ ] Zertifikat (bestanden/nicht bestanden) als PDF exportierbar
- [ ] Offline-Betrieb: App funktioniert ohne Internetverbindung
- [ ] Neues Szenario hinzufügen ohne Code-Änderung (JSON-Konfiguration)

---

## M4: OSINT → ANTI-KI Pipeline

**Status:** Offen

### Akzeptanzkriterien
- [ ] `phantom_client.py` in PROLETARIA: OSINT-API-Wrapper
- [ ] OSINT-Findings werden automatisch in Neo4j-Graph geschrieben
- [ ] Narrative aus OSINT-Texten werden automatisch mit ANTI-KI analysiert
- [ ] Dashboard zeigt verbundene OSINT-Entitäten + Narrative in einem View
- [ ] SurveillanceDB-Einträge werden mit OSINT-Findings verknüpft

---

## M5: Multi-Org OPSEC

**Status:** Offen

### Akzeptanzkriterien
- [ ] Zwei PROLETARIA-Instanzen tauschen SurveillanceDB-Updates aus
- [ ] Föderationsprotokoll dokumentiert (Datenschutz: nur opt-in Sharing)
- [ ] OpsecAlgedonicChannel: Alerts können an Vertrauensnetz weitergeleitet werden
- [ ] Instanz-Isolation: Keine ungewollten Datenlecks zwischen Instanzen
- [ ] Penetrationstest durchgeführt (extern oder intern)

---

## M6: Cybersyn Steuerelement live

**Status:** Offen (abhängig von Cybersyn-Weiterentwicklung)

### Akzeptanzkriterien
- [ ] Cybersyn-Algedonischer-Kanal-Events werden in PROLETARIA empfangen
- [ ] Energiekrise-Simulation löst OPSEC-Empfehlung aus (Demo)
- [ ] Cybersyn Stufe 6 (Westeuropa) als Submodul-Update verfügbar
- [ ] Dokumentation: Wie Cybersyn-VSM-Prinzipien auf Org-Sicherheit übertragen
