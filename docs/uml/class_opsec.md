# UML-Klassendiagramm: OPSEC-Modul

## Vollständiges Klassendiagramm

```mermaid
classDiagram
    direction TB

    %% ─── Enums ───────────────────────────────────────────────
    class ActorType {
        <<enumeration>>
        CORPORATE
        STATE_INTELLIGENCE
        LAW_ENFORCEMENT
        MILITARY
        DATA_BROKER
        NGO
    }

    class ThreatLevel {
        <<enumeration>>
        LOW
        MEDIUM
        HIGH
        CRITICAL
    }

    class RequestType {
        <<enumeration>>
        AUSKUNFT_ART15
        LOESCHUNG_ART17
        WIDERSPRUCH_ART21
        EINSCHRAENKUNG_ART18
        PORTABILITAET_ART20
    }

    class RequestStatus {
        <<enumeration>>
        ENTWURF
        VERSENDET
        BESTAETIGT
        BEANTWORTET
        UEBERFAELLIG
        ESKALIERT
        ABGESCHLOSSEN
    }

    class RiskCategory {
        <<enumeration>>
        UNENCRYPTED_CHANNEL
        METADATA_LEAK
        TIMING_PATTERN
        PLATFORM_COOPERATION
        CONTACT_EXPOSURE
        LOCATION_LEAK
    }

    %% ─── ExposureScanner ─────────────────────────────────────
    class ExposureFinding {
        +String source
        +String finding_type
        +ThreatLevel severity
        +String description
        +String target
        +datetime found_at
        +Dict raw_data
        +String recommendation
    }

    class ExposureScanner {
        -String target
        -OpsecAlgedonicChannel algedonic_channel
        -String llm_server_url
        +scan_exposure(target: str) List~ExposureFinding~
        +check_data_breaches(email: str) List~ExposureFinding~
        +analyze_social_footprint(username: str) ExposureFinding
        +check_public_documents(name: str) List~ExposureFinding~
        +check_domain_exposure(domain: str) List~ExposureFinding~
        +generate_exposure_report(findings: List~ExposureFinding~) str
        -_score_severity(raw_data: Dict) ThreatLevel
        -_persist_findings(findings: List~ExposureFinding~)
        -_notify_algedonic(findings: List~ExposureFinding~)
    }

    ExposureScanner "1" --> "*" ExposureFinding : erstellt
    ExposureScanner --> OpsecAlgedonicChannel : meldet kritische Findings
    ExposureFinding --> ThreatLevel : hat

    %% ─── SurveillanceDB ──────────────────────────────────────
    class SurveillanceActor {
        +String name
        +ActorType actor_type
        +ThreatLevel threat_level
        +List~String~ capabilities
        +List~String~ known_data_categories
        +String dsgvo_contact
        +String dsgvo_jurisdiction
        +String headquarters
        +String description
        +List~String~ known_victims
        +datetime last_updated
    }

    class SurveillanceDB {
        -Dict~str, SurveillanceActor~ actors
        -String db_path
        +get_actor(name: str) SurveillanceActor
        +search_actors(query: str) List~SurveillanceActor~
        +get_by_threat_level(level: ThreatLevel) List~SurveillanceActor~
        +get_by_type(actor_type: ActorType) List~SurveillanceActor~
        +add_actor(actor: SurveillanceActor)
        +update_capabilities(name: str, caps: List~String~)
        +get_dsgvo_contact(actor_name: str) str
        +get_all_critical() List~SurveillanceActor~
        +export_to_json() str
        -_load_default_actors()
        -_persist()
    }

    SurveillanceDB "1" --> "*" SurveillanceActor : verwaltet
    SurveillanceActor --> ActorType : hat
    SurveillanceActor --> ThreatLevel : hat
    SurveillanceDB --> DSGVOAutomation : liefert Kontaktdaten für

    %% ─── DSGVOAutomation ─────────────────────────────────────
    class DSGVORequest {
        +String id
        +String target_organization
        +String target_contact
        +RequestType request_type
        +RequestStatus status
        +String requester_name
        +String requester_address
        +String requester_email
        +datetime created_at
        +datetime sent_at
        +datetime response_due
        +datetime response_received_at
        +String generated_letter
        +String response_text
        +List~String~ attachments
    }

    class DSGVOAutomation {
        -String db_path
        -String template_dir
        +create_request(target: str, request_type: RequestType, requester_data: Dict) DSGVORequest
        +generate_letter(request_id: str) str
        +mark_sent(request_id: str)
        +mark_responded(request_id: str, response_text: str)
        +check_overdue() List~DSGVORequest~
        +escalate_to_aufsicht(request_id: str)
        +get_status(request_id: str) RequestStatus
        +get_all_requests() List~DSGVORequest~
        +get_statistics() Dict
        -_calculate_due_date(sent_at: datetime) datetime
        -_generate_art15_letter(request: DSGVORequest) str
        -_generate_art17_letter(request: DSGVORequest) str
        -_generate_art21_letter(request: DSGVORequest) str
        -_generate_complaint_letter(request: DSGVORequest) str
        -_send_email(to: str, subject: str, body: str)
        -_persist_request(request: DSGVORequest)
    }

    DSGVOAutomation "1" --> "*" DSGVORequest : verwaltet
    DSGVORequest --> RequestType : hat
    DSGVORequest --> RequestStatus : hat

    %% ─── CommPatternAnalyzer ─────────────────────────────────
    class CommEvent {
        +String id
        +String channel
        +String sender
        +String recipient
        +datetime timestamp
        +bool encrypted
        +String metadata
        +int message_length
        +Dict platform_data
    }

    class OpsecRisk {
        +String id
        +RiskCategory category
        +ThreatLevel severity
        +String description
        +List~CommEvent~ related_events
        +String recommendation
        +datetime detected_at
    }

    class CommPatternAnalyzer {
        -List~CommEvent~ event_buffer
        -OpsecAlgedonicChannel algedonic_channel
        +analyze_patterns(events: List~CommEvent~) List~OpsecRisk~
        +detect_metadata_leaks(events: List~CommEvent~) List~OpsecRisk~
        +check_channel_security(channel: str) OpsecRisk
        +detect_timing_patterns(events: List~CommEvent~) OpsecRisk
        +detect_contact_exposure(events: List~CommEvent~) List~OpsecRisk~
        +generate_audit_report() str
        +add_event(event: CommEvent)
        -_score_channel(channel: str) ThreatLevel
        -_analyze_timing(events: List~CommEvent~) bool
        -_check_platform_cooperation(platform: str) bool
    }

    CommPatternAnalyzer "1" --> "*" CommEvent : analysiert
    CommPatternAnalyzer "1" --> "*" OpsecRisk : erstellt
    CommPatternAnalyzer --> OpsecAlgedonicChannel : meldet Risiken
    OpsecRisk --> RiskCategory : hat
    OpsecRisk --> ThreatLevel : hat

    %% ─── OpsecAlgedonicChannel ───────────────────────────────
    class ThreatEvent {
        +String id
        +String source_component
        +ThreatLevel severity
        +String description
        +Dict context_data
        +datetime timestamp
        +bool acknowledged
        +String response_plan
    }

    class OpsecAlgedonicChannel {
        -List~ThreatEvent~ active_threats
        -int threat_score
        -ThreatLevel current_level
        -String llm_server_url
        -int THRESHOLD_MEDIUM
        -int THRESHOLD_HIGH
        -int THRESHOLD_CRITICAL
        +report_threat(event: ThreatEvent)
        +get_current_threat_level() ThreatLevel
        +get_active_threats() List~ThreatEvent~
        +generate_response_plan() str
        +acknowledge_threat(event_id: str)
        +get_threat_history(since: datetime) List~ThreatEvent~
        +reset_channel()
        -_recalculate_score()
        -_check_thresholds()
        -_escalate(level: ThreatLevel)
        -_notify_user(message: str)
        -_request_response_plan() str
    }

    OpsecAlgedonicChannel "1" --> "*" ThreatEvent : verwaltet
    ThreatEvent --> ThreatLevel : hat
    OpsecAlgedonicChannel --> ThreatLevel : aggregiert zu

    %% ─── Modul-übergreifende Beziehungen ─────────────────────
    ExposureScanner --> OpsecAlgedonicChannel : meldet Findings
    CommPatternAnalyzer --> OpsecAlgedonicChannel : meldet Risiken
    SurveillanceDB --> DSGVOAutomation : liefert Zielkontakte
```

---

## Attribut- und Methodenbeschreibungen

### ExposureScanner

| Methode | Eingabe | Ausgabe | Beschreibung |
|---------|---------|---------|--------------|
| `scan_exposure` | `target: str` | `List[ExposureFinding]` | Vollständiger Multi-Source-Scan |
| `check_data_breaches` | `email: str` | `List[ExposureFinding]` | Prüft bekannte Datenlecks |
| `analyze_social_footprint` | `username: str` | `ExposureFinding` | Analysiert Social-Media-Spuren |
| `check_public_documents` | `name: str` | `List[ExposureFinding]` | Öffentliche Dokument-Recherche |
| `generate_exposure_report` | `findings: List` | `str` | Markdown-Bericht |

### SurveillanceDB — Vorbefüllte Akteure

Die Datenbank enthält standardmäßig folgende Akteure:

| Name | Typ | Threat Level |
|------|-----|-------------|
| Palantir Technologies | CORPORATE | CRITICAL |
| Clearview AI | CORPORATE | HIGH |
| NSO Group | CORPORATE | CRITICAL |
| Bundesamt für Verfassungsschutz | STATE_INTELLIGENCE | HIGH |
| Meta Platforms | DATA_BROKER | HIGH |
| Google LLC | DATA_BROKER | MEDIUM |
| Axciom | DATA_BROKER | MEDIUM |

### DSGVOAutomation — Fristen

| Aktion | Frist | Rechtsgrundlage |
|--------|-------|----------------|
| Antwort auf Art.15 | 30 Tage | Art. 12 Abs. 3 DSGVO |
| Antwort auf Art.17 | Unverzüglich | Art. 17 Abs. 1 DSGVO |
| Eskalation bei Überschreitung | Nach 30 Tagen | Art. 77 DSGVO |
| Beschwerde DSB | Sofort möglich | Art. 77 Abs. 1 DSGVO |

### OpsecAlgedonicChannel — Schwellenwerte

| Score | Level | Reaktion |
|-------|-------|---------|
| 0–29 | LOW | Logging, kein Alert |
| 30–59 | MEDIUM | Alert an Nutzer:in |
| 60–79 | HIGH | Dringende Handlungsempfehlungen |
| 80–100 | CRITICAL | Response-Plan via LLM, sofortige Eskalation |
