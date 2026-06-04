# PROLETARIA

**Defensives Konglomerat gegen staatliche und kommerzielle Überwachungsinfrastruktur — und kulturelle Hegemoniearbeit für soziale Bewegungen.**

![Build](https://img.shields.io/github/actions/workflow/status/tib019/PROLETARIA/ci.yml?branch=main&label=build)
![License](https://img.shields.io/github/license/tib019/PROLETARIA)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)

---

## Module

| Modul | Typ | Beschreibung | Pfad / Repo |
|-------|-----|-------------|-------------|
| **OPSEC** | Python (lokal) | ExposureScanner, SurveillanceDB, DSGVO-Automatisierung, Kommunikations-Audit, Algedonischer Kanal | `opsec/` |
| **Verhör-Trainer** | TypeScript / Electron | Interaktives Verhörtraining, TacticAnalyzer, LegalKnowledgeBase (§136/55 StPO) | `verhoer-trainer/` |
| **LLM Server** | Python / FastAPI | Bridge zu ProletariaLLM (Ollama). Alle LLM-Anfragen im Stack laufen hier durch | `llm-server/` |
| **ANTI-KI** | Python / FastAPI | Narrativanalyse, Desinformationserkennung, Gegennarrativ-Generierung, Neo4j-Graph | `modules/anti-ki/` |
| **ProletariaLLM** | Python / Modell | Fine-tuned Mistral-7B auf politischem Corpus (Marx, Gramsci, Netzpolitik, Jungle World) | `modules/proletaria-llm/` |
| **Interview Copilot** | TypeScript / Electron | Echtzeit-Transkription und KI-Unterstützung bei Job-Interviews | `modules/interview-copilot/` |
| **OSINT Tool** | Python / FastAPI | Öffentliche Quellen-Analyse, Akteur-Recherche, Netzwerk-Graph | `modules/osint/` |
| **Cybersyn 2.0** | Python | Dezentrale Energie-Koordination, VSM-Modell Norddeutschland + Benelux | `modules/cybersyn/` |
| **Gramsci** | Python (lokal) | Kulturelle Hegemoniearbeit: KI-gestützte Inhaltsgenerierung für alle Kanäle, Review-Pflicht, Kampagnen-Management | `gramsci/` |

---

## Schnellstart

```bash
# 1. Repository mit Submodulen klonen
git clone --recurse-submodules https://github.com/tib019/PROLETARIA
cd PROLETARIA

# 2. Setup
bash setup.sh

# 3. Gesamtstack starten (Docker)
docker compose up -d

# 4. Gramsci direkt nutzen (kein Docker nötig)
pip install -r requirements.txt
python -m gramsci generate "Mietpreisbremse" --platform mastodon --lang de
```

---

## Was PROLETARIA ist

- Eine Sammlung von Werkzeugen für soziale Bewegungen, Aktivist:innen und Organisationen
- **Defensiv:** schützt vor Überwachung, stärkt Kommunikations-OPSEC
- **Offensiv:** unterstützt politische Kommunikation auf allen Plattformen (Gramsci-Modul)
- Vollständig lokal betreibbar — kein Cloud-Zwang, kein externes Logging
- Rechtlich abgesichert: alle Features basieren auf legalen Mitteln
- Kein Inhalt verlässt das System ohne explizite menschliche Freigabe (Knopfdruck-Prinzip)

## Was PROLETARIA nicht ist

- Kein Überwachungswerkzeug — keine Funktion zur Überwachung Dritter
- Kein Spam-Tool — Gramsci veröffentlicht nichts ohne manuelles Approve
- Kein Ersatz für politisches Urteilsvermögen — KI liefert Entwürfe, Menschen entscheiden
- Keine SaaS-Plattform — kein zentraler Server, keine Cloud-Abhängigkeit
- Kein Anonymisierungs-Allheilmittel — OPSEC-Tools ergänzen, ersetzen nicht Disziplin

---

## Guides

- [Developer Guide](docs/guides/DEVELOPER_GUIDE.md) — Architektur, neue Module hinzufügen
- [Gramsci Guide](docs/guides/GRAMSCI_GUIDE.md) — Kampagnen, Kanäle, ReviewCLI, NarrativeRadar
- [C4 Container-Diagramm](docs/architecture/C4_container.md) — Systemarchitektur
- [Roadmap](docs/planning/ROADMAP.md) — Milestones und geplante Features
- [Backlog](docs/planning/BACKLOG.md) — Priorisierte User Stories

---

## OPSEC-Grundprinzipien

1. **Lokal first** — Kein Modul erfordert Cloud-API-Keys
2. **Kein Logging** — Sensible Analysen werden nicht extern gespeichert
3. **Knopfdruck-Prinzip** — Kein generierter Inhalt wird ohne Freigabe veröffentlicht
4. **Dezentralisierung** — Kein Single-Point-of-Failure
5. **Rechtliche Absicherung** — Features vor Release mit Rote Hilfe / GFF abgestimmt

---

*Benannt nach Antonio Gramsci (1891–1937), Vordenker der kulturellen Hegemonie-Theorie.*
*Entwickelt von Tobias Buß | 2026*
