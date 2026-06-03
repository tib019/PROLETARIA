# Developer Guide

---

## Projektstruktur

```
PROLETARIA/
├── opsec/                    # Python: OPSEC-Kernmodule
│   ├── __init__.py
│   ├── exposure_scanner.py   # Credential/PII/Infrastruktur-Scanner
│   ├── surveillance_db.py    # Wissensbasis Überwachungsakteure
│   ├── dsgvo_automation.py   # DSGVO-Brief-Generator + Fristenverwaltung
│   ├── comm_pattern_analyzer.py  # Kommunikationsstruktur-Audit
│   └── algedonic.py          # Eskalationsprotokoll (Beer/Cybersyn-Prinzip)
│
├── verhoer-trainer/          # TypeScript: Verhör-Trainingspaket
│   ├── package.json
│   └── src/
│       ├── index.ts          # Exports
│       ├── LegalKnowledgeBase.ts  # §136/55 StPO, Taktiken, Notfallskript
│       ├── scenarios.ts      # Szenario-Definitionen
│       ├── TrainingSession.ts # Sitzungs-Management + Bewertung
│       └── TacticAnalyzer.ts # Pattern-Matching + LLM-Bridge
│
├── llm-server/               # Python: FastAPI LLM-Bridge
│   ├── serve.py              # /generate, /chat, /analyze Endpoints
│   └── Dockerfile
│
├── cybersyn/                 # Referenz-Dokumentation (kein Code)
│   └── README.md
│
├── modules/                  # Git-Submodule (nicht direkt bearbeiten)
│   ├── anti-ki/
│   ├── proletaria-llm/
│   ├── interview-copilot/
│   ├── osint/
│   └── cybersyn/
│
├── docs/                     # Diese Dokumentation
│   ├── architecture/         # C4-Diagramme, Deployment
│   ├── uml/                  # Klassen-, Sequenz-, Use-Case-Diagramme
│   ├── adr/                  # Architecture Decision Records
│   ├── planning/             # Roadmap, Milestones, Backlog
│   └── guides/               # Diese Datei + OPSEC/Verhör/Deployment
│
├── docker-compose.yml        # Gesamtstack
├── requirements.txt          # Python-Dependencies
├── setup.sh                  # Setup-Skript
└── .gitmodules               # Submodul-Konfiguration
```

---

## Neues OPSEC-Modul hinzufügen

1. **Datei erstellen** `opsec/mein_modul.py`:

```python
"""
MeinModul — kurze Beschreibung

Defensiver Einsatz: ...
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class MeinFinding:
    severity: str
    description: str

class MeinModul:
    def analyze(self, input: str) -> list[MeinFinding]:
        ...
```

2. **Export in `opsec/__init__.py`** hinzufügen:

```python
from .mein_modul import MeinModul
__all__ = [..., "MeinModul"]
```

3. **API-Endpoint in `modules/anti-ki/api/main.py`** (nach PROLETARIA-Zustimmung):

```python
@app.post('/api/opsec/mein-endpoint', dependencies=[Depends(verify_token)])
def mein_endpoint(req: MeinRequest):
    from opsec.mein_modul import MeinModul
    ...
```

4. **Dokumentation**: `docs/uml/class_opsec.md` aktualisieren.

---

## Neuen Überwachungsakteur in SurveillanceDB eintragen

```python
from opsec.surveillance_db import SurveillanceDB, SurveillanceActor, ActorType, ThreatLevel

db = SurveillanceDB()
db.add_actor(SurveillanceActor(
    id="eindeutige_id",          # lowercase, keine Leerzeichen
    name="Vollständiger Name",
    actor_type=ActorType.KOMMERZIELL,  # oder BEHOERDE, POLIZEI, NACHRICHTENDIENST
    threat_level=ThreatLevel.HOCH,
    country="Deutschland",
    description="...",
    capabilities=["Was kann der Akteur?"],
    known_targets=["Welche Gruppen sind betroffen?"],
    legal_basis=["§ XY Gesetz"],
    counter_measures=["Konkrete Maßnahme 1", "Maßnahme 2"],
    sources=["Quelle (URL oder Dokument)"]
))
```

Für Aufnahme in die Builtin-Liste: Pull Request mit Quellen-Nachweis.

---

## Neues Verhör-Szenario schreiben

In `verhoer-trainer/src/scenarios.ts`:

```typescript
export const SCENARIOS: Scenario[] = [
  // ... bestehende Szenarien ...
  {
    id: 'eindeutige_id',
    title: 'Titel des Szenarios',
    role: 'beschuldigt',           // 'beschuldigt' | 'zeuge' | 'auskunftsperson'
    difficulty: 'fortgeschritten', // 'einsteiger' | 'fortgeschritten' | 'experte'
    context: 'Beschreibung der Situation...',
    turns: [
      {
        speaker: 'beamter',
        text: 'Was der Beamte sagt...',
        expected_response_type: 'schweigen', // Erwartete Reaktion
        hint: 'Tipp für Trainierenden',
        legal_note: 'Rechtliche Grundlage'
      }
    ],
    learning_objectives: ['Was soll gelernt werden?']
  }
];
```

**Erlaubte `expected_response_type` Werte:**
- `schweigen` — keine Aussage machen
- `personalien` — nur Name/Adresse/Geburtsdatum
- `rechtsverweis` — aktiv auf Rechte hinweisen
- `anwalt_fordern` — explizit Anwalt verlangen
- `frage_zurueckweisen` — unzulässige Methode benennen

---

## Branching-Strategie

```
main          — Stabiler Stand, nur via Merge
dev           — Aktive Entwicklung
feature/xyz   — Einzelne Features
fix/xyz       — Bugfixes
```

Commits folgen Conventional Commits:
```
feat: neue Funktionalität
fix: Bugfix
docs: nur Dokumentation
refactor: kein neues Feature, kein Fix
test: Tests hinzufügen/ändern
```

---

## Submodule — wichtige Regeln

1. **Niemals direkt in `modules/` committen** — nur in den Original-Repos
2. **Submodul-Updates** via `git submodule update --remote` + Commit in PROLETARIA
3. **Cybersyn** (`modules/cybersyn`) — read-only, keine Issues, keine PRs

```bash
# Submodul-Update in PROLETARIA committen
git submodule update --remote modules/anti-ki
git add modules/anti-ki
git commit -m "chore: anti-ki auf neuesten Stand bringen"
```
