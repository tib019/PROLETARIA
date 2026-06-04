# Developer Guide

---

## Projektstruktur

```
PROLETARIA/
├── gramsci/                  # Python: Gramsci-Modul (Hegemoniearbeit)
│   ├── __init__.py
│   ├── __main__.py           # CLI-Einstiegspunkt: python -m gramsci
│   ├── config.py             # load_env(), get_channel_credentials()
│   ├── core/
│   │   ├── content_engine.py     # ContentEngine, ContentType, GeneratedContent
│   │   ├── campaign_manager.py   # CampaignManager, Campaign, CampaignItem
│   │   ├── narrative_radar.py    # NarrativeRadar, NarrativeAnalysis
│   │   └── hegemony_analyzer.py  # HegemonieAnalyzer
│   ├── channels/
│   │   ├── base.py               # BaseChannelAdapter, PublishResult
│   │   ├── social/               # Mastodon, Twitter, Reddit, Telegram, Facebook, Instagram, TikTok
│   │   ├── comments/             # YouTube, NewsSite
│   │   ├── civic/                # Petition, PublicConsultation
│   │   ├── media/                # PressRelease, LetterToEditor
│   │   └── print/                # FlyerGenerator, Newsletter
│   └── ui/
│       ├── review_cli.py         # ReviewCLI (Terminal-Interface)
│       └── dashboard.py          # Dashboard (Kampagnen-Übersicht)
│
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
│   └── guides/               # Diese Datei + OPSEC/Verhör/Deployment/Gramsci
│
├── docker-compose.yml        # Gesamtstack
├── requirements.txt          # Python-Dependencies
├── setup.sh                  # Setup-Skript
└── .gitmodules               # Submodul-Konfiguration
```

---

## Neuen Kanal-Adapter hinzufügen

Gramsci unterstützt beliebige neue Kanäle über das `BaseChannelAdapter`-Protokoll. Das Guard-Prinzip (`approved=True` vor Publish) wird von der Basisklasse erzwungen — der neue Adapter muss sich darum nicht kümmern.

### 1. Adapter-Datei erstellen

Zum Beispiel `gramsci/channels/social/bluesky.py`:

```python
"""
BlueSkyAdapter — Veröffentlichung auf Bluesky (AT Protocol)
"""
from __future__ import annotations

import os
import requests
from ...channels.base import BaseChannelAdapter, PublishResult
from ...core.content_engine import GeneratedContent


class BlueSkyAdapter(BaseChannelAdapter):
    channel_name = "bluesky"

    def __init__(self):
        self.handle = os.environ.get("BLUESKY_HANDLE", "")
        self.app_password = os.environ.get("BLUESKY_APP_PASSWORD", "")
        self.pds_url = os.environ.get("BLUESKY_PDS_URL", "https://bsky.social")

    def validate_credentials(self) -> bool:
        return bool(self.handle and self.app_password)

    def _do_publish(self, content: GeneratedContent) -> PublishResult:
        # Guard wurde bereits in BaseChannelAdapter.publish() geprüft
        if not self.validate_credentials():
            return PublishResult(
                success=False,
                error="BLUESKY_HANDLE oder BLUESKY_APP_PASSWORD fehlt in .env",
                channel=self.channel_name,
            )
        try:
            # 1. Session erstellen
            session = requests.post(
                f"{self.pds_url}/xrpc/com.atproto.server.createSession",
                json={"identifier": self.handle, "password": self.app_password},
                timeout=10,
            ).json()
            token = session["accessJwt"]

            # 2. Post senden
            resp = requests.post(
                f"{self.pds_url}/xrpc/com.atproto.repo.createRecord",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "repo": session["did"],
                    "collection": "app.bsky.feed.post",
                    "record": {
                        "$type": "app.bsky.feed.post",
                        "text": content.final_text,
                        "createdAt": content.platform,
                    },
                },
                timeout=10,
            ).json()
            uri = resp.get("uri", "")
            return PublishResult(success=True, url=uri, channel=self.channel_name)
        except Exception as exc:
            return PublishResult(success=False, error=str(exc), channel=self.channel_name)
```

### 2. In `gramsci/channels/social/__init__.py` exportieren

```python
from .bluesky import BlueSkyAdapter

__all__ = [
    ...,
    "BlueSkyAdapter",
]
```

### 3. In `gramsci/channels/__init__.py` exportieren

```python
from .social import (
    MastodonAdapter, TwitterAdapter, ..., BlueSkyAdapter,
)
__all__ = [..., "BlueSkyAdapter"]
```

### 4. `.env`-Variablen dokumentieren

In `docs/guides/GRAMSCI_GUIDE.md` in der Kanäle-Tabelle ergänzen:

| Variable | Pflicht | Beschreibung |
|----------|---------|--------------|
| `BLUESKY_HANDLE` | ja | Handle z.B. `name.bsky.social` |
| `BLUESKY_APP_PASSWORD` | ja | App-Passwort aus Bluesky-Settings |
| `BLUESKY_PDS_URL` | nein | Standard: `https://bsky.social` |

### 5. FORMAT_LIMITS ergänzen (optional)

In `gramsci/core/content_engine.py` das Zeichenlimit eintragen:

```python
FORMAT_LIMITS = {
    ...,
    "bluesky": 300,
}
```

---

## Gramsci-Kampagne programmieren

Vollständige Kampagne per Python-API ohne CLI:

```python
from gramsci import load_env, CampaignManager, ContentType, ReviewCLI
from gramsci.channels import MastodonAdapter, TelegramAdapter

# 1. Credentials aus .env laden
load_env()

# 2. Kampagne erstellen — ContentEngine generiert automatisch für alle Kombinationen
manager = CampaignManager()
campaign = manager.create(
    name="Mietpreisbremse-Kampagne",
    topic="Die Mietpreisbremse versagt. Wir brauchen echte Vergesellschaftung.",
    platforms=["mastodon", "telegram", "press_release"],
    languages=["de", "en"],
    content_type=ContentType.SHORT_POST,
)
print(f"Kampagne erstellt: {campaign.id} ({campaign.total_items} Items)")

# 3. Im ReviewCLI freigeben (interaktiv)
cli = ReviewCLI(manager)
cli.review_campaign(campaign)

# 4. Freigegebene Items veröffentlichen
adapters = {
    "mastodon": MastodonAdapter(),
    "telegram": TelegramAdapter(),
}

for item in campaign.items:
    if item.content.approved and item.channel_adapter in adapters:
        result = adapters[item.channel_adapter].publish(item.content)
        print(result)
        if result.success:
            item.published_at = __import__("datetime").datetime.now().isoformat()
            item.publish_url = result.url

manager.save(campaign)
```

### NarrativeRadar in Kampagne integrieren

```python
from gramsci import NarrativeRadar, ContentEngine, ContentType

radar = NarrativeRadar()
engine = ContentEngine()

# Aktuellen Diskurs analysieren
analyse = radar.analyze(
    "Die Klimakleber blockieren die Wirtschaft und gefährden Leben."
)
print(f"Narrativ: {analyse.narrative_type.value}")
print(f"Bedrohung: {analyse.threat_level.value}")
print(f"Erkannte Frames: {', '.join(analyse.detected_frames)}")

# Gegennarrativ direkt als Kontext für ContentEngine nutzen
gegennarrativ = radar.generate_counter(analyse)
inhalt = engine.generate(
    topic="Klimagerechtigkeit und Aktionsformen",
    content_type=ContentType.SHORT_POST,
    platform="mastodon",
    language="de",
    context=f"Gegennarrativ zu: {gegennarrativ}",
)
print(inhalt.final_text)
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
