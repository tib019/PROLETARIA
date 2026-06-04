# PROLETARIA

> Defensive Gegeninfrastruktur gegen staatliche und kommerzielle Überwachung —
> und kulturelle Hegemoniearbeit für soziale Bewegungen.

[![License: AGPL-3.0](https://img.shields.io/badge/license-AGPL--3.0-red.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-compose-2496ED.svg)](docker-compose.yml)
[![Local-first](https://img.shields.io/badge/runs-100%25%20lokal-green.svg)](#opsec-prinzipien)

---

## Warum PROLETARIA?

Palantir analysiert Bewegungen. Clearview identifiziert Gesichter. Pimeyes findet Profile.
PROLETARIA kehrt diese Logik um:

| Palantir / Clearview | PROLETARIA |
|----------------------|-----------|
| Überwacht Aktivist:innen | Schützt Aktivist:innen vor Überwachung |
| Aggregiert Daten über Bewegungen | Löscht eigene Datenspuren |
| Analysiert Kommunikationsmuster | Auditiert eigene OPSEC |
| Generiert Profile | Generiert DSGVO-Löschanfragen |
| Beeinflusst öffentliche Narrative | Baut Gegennarrative auf |

Alles läuft lokal. Kein Cloud-Zwang. Kein externes Logging.

---

## Module

| Modul | Sprache | Funktion |
|-------|---------|---------|
| [**OPSEC**](opsec/) | Python | Eigene Spuren scannen, Überwachungsakteure identifizieren, DSGVO-Anfragen automatisieren, Kommunikationsstruktur auditieren |
| [**Gramsci**](gramsci/) | Python | Politische Inhalte generieren (7 Sprachen, 15+ Kanäle), Narrative analysieren, Kampagnen verwalten — mit Knopfdruck-Freigabe |
| [**Verhör-Trainer**](verhoer-trainer/) | TypeScript | Interaktives Training für Polizeibefragungen: §136 StPO, Schweigerecht, Taktik-Erkennung |
| [**LLM-Server**](llm-server/) | Python / FastAPI | Lokale Inferenz-Bridge zu ProletariaLLM via Ollama |
| [**ANTI-KI**](modules/anti-ki/) | Python / FastAPI | Narrativanalyse, Desinformationserkennung, Gegennarrativ-Engine, Neo4j-Wissensgraph |
| [**ProletariaLLM**](modules/proletaria-llm/) | Python | Fine-tuned Mistral-7B auf politischem Corpus (Marx, Gramsci, Netzpolitik) |
| [**Interview Copilot**](modules/interview-copilot/) | TypeScript | Echtzeit-Transkription und Gesprächsunterstützung |
| [**OSINT Tool**](modules/osint/) | Python | Öffentliche Quellen-Analyse, Akteur-Recherche, Netzwerk-Visualisierung |
| [**Cybersyn 2.0**](modules/cybersyn/) | Python | Dezentrale Energie-Koordination (VSM-Modell, read-only Steuerelement) |

---

## Schnellstart

### Vollständiger Stack (Docker)

```bash
# Repository mit allen Submodulen klonen
git clone --recurse-submodules https://github.com/tib019/PROLETARIA
cd PROLETARIA

# Umgebungsvariablen konfigurieren
cp modules/anti-ki/config/.env.example modules/anti-ki/config/.env

# Stack starten (Ollama + Neo4j + API-Services)
docker compose up -d

# Status prüfen
curl http://localhost:8000/health   # ANTI-KI API
curl http://localhost:8001/health   # LLM-Server
```

### Nur Gramsci (ohne Docker)

```bash
pip install -r requirements.txt
ollama pull mistral  # oder eigenes ProletariaLLM-Modell

# Inhalt generieren und interaktiv freigeben
python -m gramsci generate "Mietpreisbremse verlängern" --platform mastodon --lang de

# Kampagnen-Übersicht
python -m gramsci dashboard
```

---

## Gramsci — Kulturelle Hegemoniearbeit

Das Gramsci-Modul unterstützt politische Kommunikation auf allen öffentlichen Arenen.
Benannt nach Antonio Gramsci (1891–1937): Hegemonie wird nicht nur durch Zwang,
sondern durch Diskursmacht gesichert. Gegenhegemonie bricht diesen Konsens.

**Unterstützte Kanäle:**

| Bereich | Kanäle |
|---------|--------|
| Social Media | Mastodon, Twitter/X, Telegram, Facebook Pages, Instagram Business, TikTok |
| Langform | Reddit, Blogs, Newsletters |
| Kommentare | YouTube, Nachrichtenseiten |
| Zivilgesellschaft | Campact, Change.org, OpenPetition, Bürgerbeteiligung |
| Medien | Pressemitteilungen, Leserbriefe |
| Print | Flyer (HTML/TXT-Export), Newsletter (SMTP) |

**Sprachen:** DE · EN · FR · NL · ES · IT · PL

**Knopfdruck-Prinzip:** Kein Inhalt wird ohne explizite menschliche Freigabe veröffentlicht.
Das `ReviewCLI` zeigt jeden Entwurf an — Freigabe, Ablehnung oder Bearbeitung liegt beim Menschen.

```
═══════════════════════════════════════════════════════════
  GRAMSCI — INHALTSPRÜFUNG
═══════════════════════════════════════════════════════════

  Typ: short_post | Plattform: mastodon | Sprache: de | Zeichen: 312
  ✓ passt

  ┌─ INHALT ────────────────────────────────────────────────
  │ Während Mieter:innen in Hamburg im Durchschnitt 42% ihres
  │ Einkommens für Wohnen aufwenden, verbuchen die zehn größten
  │ Immobilienkonzerne Rekordgewinne. Die Mietpreisbremse muss
  │ nicht nur verlängert, sondern verschärft werden. #Wohnen
  └─────────────────────────────────────────────────────────

  [ENTER] Freigeben  [e] Bearbeiten  [n] Ablehnen  [q] Abbrechen
  >
```

---

## OPSEC — Selbstschutz vor Überwachung

```python
from opsec import ExposureScanner, DSGVOAutomation, SurveillanceDB

# Eigenen Text auf PII / Credentials scannen
scanner = ExposureScanner()
result = scanner.scan("Mein Passwort ist abc123, ich wohne in der Musterstr. 1")
# → risk_level: KRITISCH | findings: [PASSWORD, ADDRESS]

# DSGVO-Auskunftsanfrage an BKA generieren
dsgvo = DSGVOAutomation()
letter = dsgvo.create_request(
    request_type="auskunft",
    controller="Bundeskriminalamt",
    requester_name="Max Muster"
)

# Überwachungsakteure prüfen
db = SurveillanceDB()
actors = db.query_by_threat_level("KRITISCH")
```

---

## Architektur

```
PROLETARIA/
├── opsec/              # Defensive OPSEC-Module
├── gramsci/            # Politische Kommunikation
│   ├── core/           #   ContentEngine, NarrativeRadar, CampaignManager
│   ├── channels/       #   15+ Kanal-Adapter
│   └── ui/             #   ReviewCLI (Knopfdruck), Dashboard
├── verhoer-trainer/    # Verhör-Training (TypeScript)
├── llm-server/         # ProletariaLLM-Bridge (FastAPI)
├── modules/            # Git-Submodule
│   ├── anti-ki/        #   Narrativanalyse-API
│   ├── proletaria-llm/ #   Finetuned Sprachmodell
│   ├── interview-copilot/
│   ├── osint/
│   └── cybersyn/       #   Read-only Steuerelement
└── docs/               # Vollständige Dokumentation
    ├── architecture/   #   C4-Diagramme
    ├── uml/            #   Klassen-, Sequenz-, Use-Case-Diagramme
    ├── adr/            #   Architecture Decision Records
    ├── guides/         #   Developer, Gramsci, OPSEC, Verhör, Deployment
    └── planning/       #   Roadmap, Milestones, Backlog
```

→ Vollständige Architektur: [C4 Container-Diagramm](docs/architecture/C4_container.md)

---

## OPSEC-Prinzipien

1. **Lokal first** — Kein Modul erfordert Cloud-API-Keys oder externe Dienste
2. **Kein Logging** — Sensible Analysen verlassen das System nicht
3. **Knopfdruck-Prinzip** — Kein KI-generierter Inhalt wird ohne Freigabe veröffentlicht
4. **Dezentralisierung** — Kein Single-Point-of-Failure, keine zentrale Infrastruktur
5. **Rechtliche Absicherung** — Alle Features basieren auf Grundrechten (DSGVO, Art. 10 GG)

---

## Dokumentation

| Guide | Inhalt |
|-------|--------|
| [Laien-Guide](docs/guides/LAIEN_GUIDE.md) | Einstieg ohne Programmierkenntnisse |
| [Gramsci-Guide](docs/guides/GRAMSCI_GUIDE.md) | Kampagnen, Kanäle, ReviewCLI, NarrativeRadar |
| [OPSEC-Guide](docs/guides/OPSEC_GUIDE.md) | ExposureScanner, SurveillanceDB, DSGVO |
| [Verhör-Guide](docs/guides/VERHOER_GUIDE.md) | Trainingsszenarien, Rechte, Notfallskript |
| [Developer Guide](docs/guides/DEVELOPER_GUIDE.md) | Neue Module, Adapter, Architektur-Entscheidungen |
| [Deployment Guide](docs/guides/DEPLOYMENT_GUIDE.md) | Docker, Ollama, Umgebungsvariablen |

---

## Systemanforderungen

| Komponente | Minimum | Empfohlen |
|-----------|---------|-----------|
| RAM | 16 GB | 32 GB |
| GPU | — | NVIDIA ≥ 8 GB VRAM |
| Speicher | 50 GB | 100 GB SSD |
| Docker | ≥ 24.0 | aktuell |
| Python | ≥ 3.11 | 3.12 |

---

## Rechtliches

PROLETARIA ist freie Software (AGPL-3.0). Alle implementierten Funktionen
basieren auf legalen Mitteln: DSGVO-Auskunftsrechte (Art. 15), Schweigerecht
(§136 StPO), öffentliche Kommunikation, Open-Source-Entwicklung.

Die Nutzung für Überwachung Dritter, Spam oder nicht autorisierte Eingriffe
widerspricht dem Projektzweck und ist nicht erlaubt.

---

*Entwickelt von Tobias Buß · 2026*
*Benannt nach Antonio Gramsci (1891–1937) — Vordenker der Theorie kultureller Hegemonie*
