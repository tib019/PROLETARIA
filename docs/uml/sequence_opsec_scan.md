# Sequenzdiagramm: OPSEC-Scan-Flow

## Vollständiger Ablauf eines OPSEC-Scans

```mermaid
sequenceDiagram
    actor Nutzer as Aktivist:in / Nutzer:in
    participant API as OPSEC API<br/>:8003
    participant Scanner as ExposureScanner
    participant SurvDB as SurveillanceDB
    participant CommAn as CommPatternAnalyzer
    participant Alg as OpsecAlgedonicChannel
    participant LLM as LLM Server<br/>:8001
    participant DB as SQLite OPSEC-DB

    Note over Nutzer,DB: ── Phase 1: Scan-Anfrage ──────────────────────────────

    Nutzer->>API: POST /opsec/scan<br/>{ target: "alice@org.de", include_comm: true }
    API->>API: Eingabe validieren<br/>Rate-Limit prüfen

    Note over API,Scanner: ── Phase 2: Exposition scannen ────────────────────────

    API->>Scanner: scan_exposure("alice@org.de")
    Scanner->>Scanner: Datenleck-Datenbanken prüfen
    Scanner->>Scanner: Social-Media-Footprint analysieren
    Scanner->>Scanner: Öffentliche Dokumente suchen
    Scanner->>Scanner: Domain-Exposition prüfen

    alt Findings gefunden
        Scanner->>LLM: POST /generate<br/>{ prompt: "Bewerte Findings: [...]\nSeverity-Analyse" }
        LLM-->>Scanner: KI-Schweregradbewertung
        Scanner->>Scanner: Findings mit KI-Scores anreichern
    end

    Scanner->>DB: findings speichern (INSERT)
    Scanner-->>API: List[ExposureFinding] (n Findings)

    Note over API,CommAn: ── Phase 3: Kommunikationsmuster analysieren (optional) ──

    opt include_comm == true
        API->>CommAn: analyze_patterns(recent_comm_events)
        CommAn->>CommAn: Metadaten-Lecks erkennen
        CommAn->>CommAn: Kanalverschlüsselung prüfen
        CommAn->>CommAn: Timing-Patterns analysieren
        CommAn->>CommAn: Plattform-Kooperation prüfen
        CommAn->>DB: CommEvents + OpsecRisks speichern
        CommAn-->>API: List[OpsecRisk]
    end

    Note over API,SurvDB: ── Phase 4: Bedrohungsakteure abgleichen ──────────────

    API->>SurvDB: search_actors(relevant_platforms)
    SurvDB->>DB: Akteure laden
    SurvDB-->>API: List[SurveillanceActor] (relevante Akteure)

    Note over API,Alg: ── Phase 5: Algedonische Kanalbewertung ──────────────────

    API->>Alg: report_threat(ThreatEvent{ source: "ExposureScanner", severity: HIGH, ... })

    loop für jedes kritische Finding
        API->>Alg: report_threat(ThreatEvent{ severity: finding.severity })
    end

    Alg->>Alg: _recalculate_score()
    Alg->>Alg: _check_thresholds()

    alt Threat Score >= CRITICAL (>= 80)
        Alg->>LLM: POST /generate<br/>{ prompt: "Erstelle KRITISCHEN Response-Plan für:<br/>Findings: [...]\nAkteure: [...]" }
        LLM-->>Alg: Strukturierter Response-Plan (Markdown)
        Alg->>DB: ThreatEvents + Response-Plan speichern
        Alg->>API: KRITISCH-Alert + Response-Plan
        API->>Nutzer: 🚨 HTTP 200 { threat_level: CRITICAL,<br/>  response_plan: "...",<br/>  immediate_actions: [...] }

    else Threat Score >= HIGH (>= 60)
        Alg->>LLM: POST /generate<br/>{ prompt: "Erstelle dringenden Response-Plan..." }
        LLM-->>Alg: Response-Plan
        Alg->>DB: ThreatEvents speichern
        API->>Nutzer: ⚠️ HTTP 200 { threat_level: HIGH,<br/>  response_plan: "...",<br/>  priority_actions: [...] }

    else Threat Score >= MEDIUM (>= 30)
        Alg->>DB: ThreatEvents speichern
        API->>Nutzer: HTTP 200 { threat_level: MEDIUM,<br/>  findings: [...],<br/>  recommendations: [...] }

    else Threat Score < 30 (LOW)
        Alg->>DB: ThreatEvents speichern
        API->>Nutzer: HTTP 200 { threat_level: LOW,<br/>  findings: [...],<br/>  status: "keine akuten Risiken" }
    end

    Note over Nutzer,DB: ── Phase 6: Optionale DSGVO-Anschlussaktion ─────────────

    opt Nutzer:in möchte DSGVO-Anfrage stellen
        Nutzer->>API: POST /dsgvo/create<br/>{ target: "Meta Platforms",<br/>  type: "AUSKUNFT_ART15" }
        Note over API,DB: → Weiterleitung an DSGVOAutomation<br/>(siehe sequence_dsgvo.md)
    end
```

---

## Erläuterung der Phasen

### Phase 1: Scan-Anfrage
Die Nutzer:in sendet einen POST-Request mit einem Ziel (E-Mail, Name, Username, Domain). Die API validiert die Eingabe und prüft ein Rate-Limit (max. 10 Scans/Stunde), um Missbrauch zu verhindern.

### Phase 2: Expositions-Scan
`ExposureScanner` führt parallel mehrere OSINT-Checks durch:
- **Datenlecks**: Abgleich mit bekannten Breach-Datenbanken
- **Social-Media-Footprint**: Öffentliche Profile, Posts, Verknüpfungen
- **Öffentliche Dokumente**: Presseartikel, Gerichtsdokumente, Vereinsregister
- **Domain**: WHOIS, DNS-History, verbundene Infrastruktur

Nach dem Scan bewertet das LLM die Findings und vergibt Schweregrade.

### Phase 3: Kommunikationsmuster (optional)
Bei `include_comm: true` analysiert der `CommPatternAnalyzer` vorliegende Kommunikationsereignisse auf OPSEC-Risiken.

### Phase 4: Bedrohungsakteure
`SurveillanceDB` liefert Informationen zu Akteuren, die mit den gefundenen Plattformen und Daten in Verbindung stehen.

### Phase 5: Algedonische Kanalbewertung (Kernstück)
Der `OpsecAlgedonicChannel` aggregiert alle Bedrohungssignale zu einem Gesamt-Score. Bei Überschreitung von Schwellenwerten:
- **LOW (< 30)**: Nur Logging
- **MEDIUM (30–59)**: Alert + Empfehlungen
- **HIGH (60–79)**: Dringender Response-Plan via LLM
- **CRITICAL (≥ 80)**: Sofort-Aktionsplan, priorisierte Gegenmaßnahmen

### Phase 6: DSGVO-Anschluss
Falls eine Plattform identifiziert wurde, die personenbezogene Daten verarbeitet, kann die Nutzer:in direkt eine DSGVO-Anfrage auslösen.

---

## Fehlerfälle

```mermaid
sequenceDiagram
    actor Nutzer
    participant API as OPSEC API

    Note over Nutzer,API: Fehlerfall: LLM-Server nicht erreichbar

    Nutzer->>API: POST /opsec/scan { target: "..." }
    API->>API: LLM nicht erreichbar (Timeout)
    API->>API: Fallback: regelbasierte Bewertung
    API-->>Nutzer: HTTP 200 { warning: "LLM nicht verfügbar,<br/>regelbasierte Bewertung aktiv",<br/>findings: [...] }

    Note over Nutzer,API: Fehlerfall: Ungültiges Target

    Nutzer->>API: POST /opsec/scan { target: "" }
    API-->>Nutzer: HTTP 422 { error: "Ungültiges Target" }
```
