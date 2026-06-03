# OPSEC-Guide — Anleitung zur Nutzung der defensiven Module

---

## Schnellübersicht

```
ExposureScanner      → Was leakt meine Organisation nach außen?
SurveillanceDB       → Wer überwacht uns und wie?
DSGVOAutomation      → Unsere Rechte gegen Überwachung durchsetzen
CommPatternAnalyzer  → Wie sieht unsere Kommunikationsstruktur aus?
OpsecAlgedonicChannel → Automatische Eskalation bei Bedrohung
```

---

## 1. ExposureScanner — Selbst-OSINT-Audit

### Wann nutzen?
- Vor Veröffentlichung von Dokumenten oder Texten
- Nach einer Sicherheitspanne zur Schadensanalyse
- Regelmäßiger Selbst-Audit (monatlich empfohlen)

### Grundnutzung (Python)

```python
from opsec.exposure_scanner import ExposureScanner

scanner = ExposureScanner()

# Text scannen
findings = scanner.scan_text(
    "Unser Server läuft auf 192.168.1.50, Passwort: geheim123",
    source="internes_dokument"
)

# Risikoprofil ausgeben
risk = scanner.assess_risk()
print(f"Risikostufe: {risk['risk_level']}")  # KRITISCH
print(f"Findings: {risk['total_findings']}")

for f in risk['findings']:
    print(f"  [{f['severity'].upper()}] {f['description']}")
```

### Datei-Metadaten prüfen

```python
# EXIF-Daten aus Foto entfernen bevor Veröffentlichung
findings = scanner.scan_file_metadata("demo_foto.jpg")
for f in findings:
    if f.category == "pii":
        print(f"WARNUNG: {f.description}")
        # → GPS-Koordinaten in Bilddatei — vor Veröffentlichung entfernen!
```

### Via API

```bash
curl -X POST http://localhost:8000/api/opsec/exposure-scan \
  -H "Content-Type: application/json" \
  -d '{"text": "Euer Text hier", "source": "manual"}'
```

---

## 2. SurveillanceDB — Überwachungsakteure recherchieren

### Alle kritischen Akteure auflisten

```python
from opsec.surveillance_db import SurveillanceDB, ThreatLevel

db = SurveillanceDB()

# Alle kritischen Akteure
critical = db.search(min_threat=ThreatLevel.KRITISCH)
for actor in critical:
    print(f"{actor.name} ({actor.country}): {actor.description[:80]}")

# Gegenmaßnahmen für Palantir
measures = db.get_countermeasures("palantir_gotham")
for m in measures:
    print(f"  → {m}")
```

### Neuen Akteur hinzufügen

```python
from opsec.surveillance_db import SurveillanceActor, ActorType, ThreatLevel

db.add_actor(SurveillanceActor(
    id="predictive_policing_nrw",
    name="Predictive Policing NRW (Skala)",
    actor_type=ActorType.POLIZEI,
    threat_level=ThreatLevel.HOCH,
    country="Deutschland",
    description="Prädiktives Polizei-System in NRW zur Einbruchsprognose...",
    capabilities=["Standortprognose", "Personenrisikobewertung"],
    counter_measures=["Auskunftsrecht §19 BDSG", "Verfassungsbeschwerde"],
    sources=["netzpolitik.org/2023/skala"]
))
```

### Via API

```bash
# Alle deutschen Akteure
curl "http://localhost:8000/api/opsec/surveillance-db?country=Deutschland"

# Details zu Clearview
curl "http://localhost:8000/api/opsec/surveillance-db/clearview_ai"
```

---

## 3. DSGVOAutomation — Datenschutzrechte durchsetzen

### Auskunftsanfrage gegen BKA

```python
from opsec.dsgvo_automation import DSGVOAutomation, RequestType

automation = DSGVOAutomation()

req = automation.create_request(
    request_type=RequestType.AUSKUNFT,
    controller="Bundeskriminalamt (BKA)",
    controller_address="Thaerstraße 11, 65193 Wiesbaden",
    controller_email="poststelle@bka.bund.de",
    requester_name="Max Mustermann",
    requester_address="Musterstraße 1, 10115 Berlin",
    subject_description="Alle über mich gespeicherten Daten in INPOL und verwandten Systemen"
)

# Brief generieren
letter = automation.generate_letter(req.id)
print(letter)

# Als versendet markieren (startet 30-Tage-Frist)
automation.mark_sent(req.id)
```

### Löschungsantrag gegen Clearview

```python
req = automation.create_request(
    request_type=RequestType.LOESCHUNG,
    controller="Clearview AI LLC",
    controller_address="28 Liberty Street, New York, NY 10005",
    controller_email="privacy@clearview.ai",
    requester_name="...",
    requester_address="...",
    subject_description="Alle Gesichtserkennungsdaten und biometrischen Profile"
)
```

### Überfällige Anfragen prüfen und eskalieren

```python
# Täglich/wöchentlich ausführen
overdue = automation.check_overdue()
for req in overdue:
    print(f"ÜBERFÄLLIG: {req.controller} — Anfrage {req.id}")
    # Eskalationsbrief generieren
    letter = automation.escalate_to_aufsicht(req.id, "bundesweit")
    print(letter)
```

---

## 4. CommPatternAnalyzer — Kommunikationsaudit

```python
from opsec.comm_pattern_analyzer import CommPatternAnalyzer, CommEvent
from datetime import datetime

analyzer = CommPatternAnalyzer()

# Kommunikationsereignisse hinzufügen (anonymisiert!)
events = [
    CommEvent("person_a", "person_b", datetime(2026,1,15,14,0), "signal"),
    CommEvent("person_a", "person_c", datetime(2026,1,15,14,5), "signal"),
    CommEvent("person_b", "person_d", datetime(2026,1,15,19,0), "telegram"),
    # ... mehr Events
]
analyzer.add_events(events)

# Analyse durchführen
risks = analyzer.analyze()
for risk in risks:
    print(f"[{risk.severity.upper()}] {risk.pattern}")
    print(f"  {risk.description}")
    print(f"  → {risk.recommendation}")
```

**Wichtig:** Nur Metadaten (wer mit wem wann) — niemals Inhalte eingeben.

---

## 5. OpsecAlgedonicChannel — Eskalationsprotokoll

```python
from opsec.algedonic import OpsecAlgedonicChannel, ThreatLevel

def on_escalation(level, event):
    if level == ThreatLevel.RED:
        # Hier: Push-Notification, Signal-Nachricht etc.
        print(f"🚨 NOTFALL: {event.description}")

channel = OpsecAlgedonicChannel(on_escalation=on_escalation)

# Bedrohung melden
new_level = channel.report(
    score=9,
    source="exposure_scanner",
    description="Kritische Credentials in öffentlichem Dokument gefunden"
)
print(f"Neue Stufe: {new_level}")  # ThreatLevel.RED

# Status prüfen
status = channel.status
print(f"Stufe: {status['level']}, Score: {status['score']}")
print("Maßnahmen:", status['response_plan'])

# Nach Behebung zurücksetzen
channel.reset("Credentials rotiert, Dokument gelöscht")
```

---

## Empfohlener Workflow für Organisationen

```
Wöchentlich:
  → ExposureScanner auf neue Dokumente/Posts
  → CommPatternAnalyzer auf Kommunikationsdaten der Woche

Monatlich:
  → SurveillanceDB auf neue Akteure prüfen (Netzpolitik.org lesen)
  → DSGVOAutomation: check_overdue() ausführen
  → OpsecAlgedonicChannel: History-Review

Vor jeder öffentlichen Aktion:
  → ExposureScanner auf alle zu veröffentlichenden Materialien
  → SurveillanceDB: Welche Akteure sind bei diesem Thema aktiv?
```
