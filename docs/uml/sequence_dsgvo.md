# DSGVO-Automatisierung — Sequenzdiagramm

## Vollständiger Workflow: Anfrage → Eskalation

```mermaid
sequenceDiagram
    actor N as Nutzer:in
    participant API as PROLETARIA API
    participant DA as DSGVOAutomation
    participant FS as Filesystem<br/>(data/dsgvo_requests/)
    participant AB as Aufsichtsbehörde

    N->>API: POST /api/opsec/dsgvo/create<br/>{controller, request_type, ...}
    API->>DA: create_request(RequestType.AUSKUNFT, ...)
    DA->>DA: DSGVORequest erstellen (UUID, Status=DRAFT)
    DA->>FS: _save(request) → {id}.json
    DA-->>API: DSGVORequest
    API->>DA: generate_letter(request_id)
    DA->>DA: _letter_auskunft(req) → Brieftext
    DA-->>API: {request_id, letter, status: "draft"}
    API-->>N: Brieftext zum Versenden

    Note over N,FS: Nutzer versendet Brief (Post/E-Mail)

    N->>API: POST /api/opsec/dsgvo/sent/{id}
    API->>DA: mark_sent(request_id)
    DA->>DA: sent_at = now(), deadline = now() + 30 Tage
    DA->>DA: status = SENT
    DA->>FS: _save(request)
    DA-->>API: DSGVORequest (Status=SENT)
    API-->>N: Frist gesetzt: {deadline}

    Note over N,DA: Nach 30 Tagen automatische Prüfung

    N->>API: GET /api/opsec/dsgvo/dashboard
    API->>DA: check_overdue()
    DA->>FS: Alle Requests laden
    DA->>DA: is_overdue() für jeden Request prüfen
    DA->>FS: Überfällige als OVERDUE speichern
    DA-->>API: {overdue_ids: ["abc123"], ...}
    API-->>N: Dashboard mit überfälligen Anfragen

    alt Anfrage beantwortet
        N->>DA: status = ANSWERED (manuell)
    else Keine Antwort nach Fristablauf
        N->>API: POST /api/opsec/dsgvo/escalate/{id}
        API->>DA: escalate_to_aufsicht(id, "bundesweit")
        DA->>DA: _letter_eskalation(req, behoerde)
        DA->>DA: status = ESCALATED
        DA->>FS: _save(request)
        DA-->>API: Beschwerdeschreiben an BfDI
        API-->>N: Eskalationsbrief (Art. 77 DSGVO)
        Note over N,AB: Nutzer sendet Beschwerde an BfDI
    end
```

## Rechtliche Fristen

| Schritt | Frist | Rechtsgrundlage |
|---------|-------|-----------------|
| Erste Antwort | 30 Tage | Art. 12 Abs. 3 DSGVO |
| Verlängerung (komplex) | +60 Tage mit Begründung | Art. 12 Abs. 3 DSGVO |
| Beschwerde bei Aufsicht | Jederzeit | Art. 77 DSGVO |
| Aufsicht antwortet | 3 Monate | Art. 78 DSGVO |

## Request-Status-Maschine

```mermaid
stateDiagram-v2
    [*] --> DRAFT: create_request()
    DRAFT --> SENT: mark_sent()
    SENT --> CONFIRMED: Eingangsbestätigung
    SENT --> OVERDUE: 30 Tage überschritten
    CONFIRMED --> ANSWERED: Antwort erhalten
    CONFIRMED --> OVERDUE: 30 Tage überschritten
    OVERDUE --> ESCALATED: escalate_to_aufsicht()
    ANSWERED --> [*]
    ESCALATED --> [*]
```
