# PROLETARIA — Roadmap

---

## Phase 1: Kern-Infrastruktur ✅ (Juni 2026)

**Ziel:** Alle Module existieren, PROLETARIA-Dach steht, Stack startet lokal.

### Deliverables
- [x] PROLETARIA Monorepo mit 5 Submodulen
- [x] `opsec/` — 5 defensive Module (ExposureScanner, SurveillanceDB, DSGVOAutomation, CommPatternAnalyzer, OpsecAlgedonicChannel)
- [x] `verhoer-trainer/` — 3 Szenarien, TacticAnalyzer, LegalKnowledgeBase
- [x] `llm-server/serve.py` — FastAPI Bridge für ProletariaLLM
- [x] `docker-compose.yml` — Gesamtstack-Orchestrierung
- [x] Vollständige Dokumentation (UML, ADRs, Guides)
- [x] ANTI-KI: Narrativanalyse + Neo4j + ChromaDB
- [x] Cybersyn 2.0 Stufe 5: 6-Knoten VSM Norddeutschland + Benelux

---

## Phase 2: LLM + UI (Q3 2026)

**Ziel:** ProletariaLLM fine-tuned und nutzbar, Verhör-UI in Electron.

### Deliverables
- [ ] ProletariaLLM QLoRA Fine-Tuning auf politischem Corpus abgeschlossen
  - Marx/Engels, Lenin, Gramsci, Netzpolitik.org, Jungle World
  - Evaluation: Benchmark auf politischen Fragen
- [ ] ProletariaLLM-Modell in Ollama importierbar (`Modelfile` + Anleitung)
- [ ] Verhör-Trainer UI in Interview Copilot Electron-App integriert
  - Fragen anzeigen, Antwort eingeben, Echtzeit-Feedback
  - Zertifikat als PDF exportierbar
- [ ] `llm-server/` um `/analyze/verhör`-Endpoint erweitert
  - Echtzeit-Taktikanalyse via ProletariaLLM statt nur Pattern-Matching

### Abhängigkeiten
- Hardware: GPU mit min. 24GB VRAM für QLoRA-Training (oder Cloud-Training einmalig)
- Corpus: Rechtliche Freigabe der Trainingstexte prüfen

---

## Phase 3: Integration (Q4 2026)

**Ziel:** Alle Module kommunizieren miteinander, OSINT speist ANTI-KI.

### Deliverables
- [ ] `modules/osint` → ANTI-KI Integration (`phantom_client.py`)
  - OSINT-Findings automatisch in Neo4j-Graph schreiben
  - Narrative aus OSINT-Quellen automatisch analysieren
- [ ] OPSEC-Module in ANTI-KI API voll integriert
  - `/api/opsec/*` Endpoints nutzen gemeinsamen OpsecAlgedonicChannel
  - Dashboard: Echtzeit-OPSEC-Status aller aktiven Instanzen
- [ ] SurveillanceDB: Community-Beiträge via Pull Request
  - Neue Überwachungsakteure dokumentieren
  - Quellen-Verifizierungsprozess
- [ ] Cybersyn-Algedonischer-Kanal ↔ OpsecAlgedonicChannel verbinden
  - Konzeptuelle Demo: Energiekrise löst OPSEC-Eskalation aus

### Abhängigkeiten
- Phase 2 abgeschlossen (ProletariaLLM fine-tuned)

---

## Phase 4: Multi-Org-Deployment (2027)

**Ziel:** Mehrere Organisationen können eigene PROLETARIA-Instanzen betreiben und föderieren.

### Deliverables
- [ ] Föderationsprotokoll: Instanzen tauschen SurveillanceDB-Updates aus
  - Dezentral: kein zentraler Server, P2P-Synchronisation
  - Opt-in: Organisationen entscheiden was sie teilen
- [ ] Hardened Deployment: Tor-Hidden-Service Option
  - PROLETARIA API erreichbar via .onion-Adresse
  - Kein IP-Logging
- [ ] Mobile Companion App
  - OpsecAlgedonicChannel Push-Notifications
  - Verhör-Trainer offline nutzbar
- [ ] Cybersyn Stufe 6: Westeuropa (15+ Knoten)
  - Frankreich, Deutschland, Benelux, Skandinavien
  - Live ENTSO-E Daten-Integration

---

## Leitprinzipien für alle Phasen

1. **Kein Feature ohne OPSEC-Review** — Jede neue Funktion wird auf Datenschutzrisiken geprüft
2. **Lokal first** — Cloud-Abhängigkeiten nur wenn unvermeidbar und explizit dokumentiert
3. **Alte Repos bleiben unverändert** — PROLETARIA erweitert, überschreibt nicht
4. **Rechtliche Absicherung** — Features vor Release mit Rote Hilfe / GFF abstimmen
