"""
DSGVOAutomation — automatisierte Datenschutzrechte-Durchsetzung (Art. 15-22 DSGVO)

Generiert rechtskonforme Auskunfts-, Löschungs- und Widerspruchsschreiben.
Verfolgt Fristen und eskaliert bei Nichtbeantwortung.

Rechtliche Grundlage: DSGVO Art. 15 (Auskunft), Art. 17 (Löschung),
Art. 21 (Widerspruch), Art. 77 (Beschwerde bei Aufsichtsbehörde).
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional


class RequestType(str, Enum):
    AUSKUNFT   = "auskunft"       # Art. 15 — was habt ihr über mich
    LOESCHUNG  = "loeschung"      # Art. 17 — löscht es
    BERICHTIGUNG = "berichtigung" # Art. 16 — korrigiert es
    EINSCHRAENKUNG = "einschraenkung"  # Art. 18 — sperrt die Verarbeitung
    WIDERSPRUCH = "widerspruch"   # Art. 21 — hört auf mit Profiling
    BESCHWERDE = "beschwerde"     # Art. 77 — Aufsichtsbehörde


class RequestStatus(str, Enum):
    DRAFT     = "draft"
    SENT      = "sent"
    CONFIRMED = "confirmed"   # Eingangsbestätigung erhalten
    ANSWERED  = "answered"
    OVERDUE   = "overdue"
    ESCALATED = "escalated"   # Aufsichtsbehörde eingeschaltet


@dataclass
class DSGVORequest:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    controller: str = ""           # Verantwortlicher (Unternehmen/Behörde)
    controller_address: str = ""
    controller_email: str = ""
    request_type: RequestType = RequestType.AUSKUNFT
    requester_name: str = ""
    requester_address: str = ""
    subject_description: str = ""  # Was genau wird beantragt
    created_at: datetime = field(default_factory=datetime.utcnow)
    sent_at: Optional[datetime] = None
    deadline: Optional[datetime] = None    # Gesetzlich: 1 Monat
    status: RequestStatus = RequestStatus.DRAFT
    notes: str = ""

    def is_overdue(self) -> bool:
        if self.deadline and self.status in (RequestStatus.SENT, RequestStatus.CONFIRMED):
            return datetime.utcnow() > self.deadline
        return False


class DSGVOAutomation:
    """
    Einsatz:
    - Massenhaft Auskunftsersuchen gegen kommerzielle Überwachungsfirmen
    - Löschungsanträge bei Clearview-ähnlichen Gesichts-DB-Betreibern
    - Widerspruch gegen Profiling-basierte Polizeisysteme (PredPol etc.)
    - Eskalation zu Datenschutzaufsichtsbehörden (BfDI, LDA Bayern etc.)
    """

    AUFSICHTSBEHOERDEN = {
        "bundesweit": {
            "name": "Bundesbeauftragter für den Datenschutz und die Informationsfreiheit (BfDI)",
            "address": "Husarenstraße 30, 53117 Bonn",
            "email": "poststelle@bfdi.bund.de",
            "fax": "+49 228 997799-5550",
        },
        "hamburg": {
            "name": "Hamburgischer Beauftragter für Datenschutz und Informationsfreiheit",
            "address": "Ludwig-Erhard-Str. 22, 20459 Hamburg",
            "email": "mailbox@datenschutz.hamburg.de",
        },
        "nrw": {
            "name": "Landesbeauftragter für Datenschutz und Informationsfreiheit NRW",
            "address": "Kavalleriestraße 2-4, 40213 Düsseldorf",
            "email": "poststelle@ldi.nrw.de",
        },
    }

    def __init__(self, storage_path: str = "data/dsgvo_requests"):
        self.storage = Path(storage_path)
        self.storage.mkdir(parents=True, exist_ok=True)
        self._requests: dict[str, DSGVORequest] = {}
        self._load_existing()

    # ------------------------------------------------------------------
    # Request lifecycle
    # ------------------------------------------------------------------

    def create_request(
        self,
        request_type: RequestType,
        controller: str,
        controller_address: str,
        requester_name: str,
        requester_address: str,
        subject_description: str = "",
        controller_email: str = "",
    ) -> DSGVORequest:
        req = DSGVORequest(
            controller=controller,
            controller_address=controller_address,
            controller_email=controller_email,
            request_type=request_type,
            requester_name=requester_name,
            requester_address=requester_address,
            subject_description=subject_description,
        )
        self._requests[req.id] = req
        self._save(req)
        return req

    def generate_letter(self, request_id: str) -> str:
        """Gibt fertigen Brieftext zurück (DE, formell)."""
        req = self._requests[request_id]

        generators = {
            RequestType.AUSKUNFT:      self._letter_auskunft,
            RequestType.LOESCHUNG:     self._letter_loeschung,
            RequestType.WIDERSPRUCH:   self._letter_widerspruch,
            RequestType.BERICHTIGUNG:  self._letter_berichtigung,
            RequestType.EINSCHRAENKUNG: self._letter_einschraenkung,
            RequestType.BESCHWERDE:    self._letter_beschwerde,
        }

        return generators[req.request_type](req)

    def mark_sent(self, request_id: str) -> DSGVORequest:
        req = self._requests[request_id]
        req.sent_at = datetime.utcnow()
        req.deadline = req.sent_at + timedelta(days=30)
        req.status = RequestStatus.SENT
        self._save(req)
        return req

    def check_overdue(self) -> list[DSGVORequest]:
        overdue = []
        for req in self._requests.values():
            if req.is_overdue():
                req.status = RequestStatus.OVERDUE
                self._save(req)
                overdue.append(req)
        return overdue

    def escalate_to_aufsicht(self, request_id: str, bundesland: str = "bundesweit") -> str:
        """Generiert Beschwerdeschreiben an Aufsichtsbehörde."""
        req = self._requests[request_id]
        behoerde = self.AUFSICHTSBEHOERDEN.get(bundesland, self.AUFSICHTSBEHOERDEN["bundesweit"])

        req.status = RequestStatus.ESCALATED
        self._save(req)

        return self._letter_eskalation(req, behoerde)

    def get_dashboard(self) -> dict:
        by_status: dict[str, int] = {}
        by_type: dict[str, int] = {}
        overdue = []

        for req in self._requests.values():
            by_status[req.status] = by_status.get(req.status, 0) + 1
            by_type[req.request_type] = by_type.get(req.request_type, 0) + 1
            if req.is_overdue():
                overdue.append(req.id)

        return {
            "total": len(self._requests),
            "by_status": by_status,
            "by_type": by_type,
            "overdue_ids": overdue,
            "timestamp": datetime.utcnow().isoformat(),
        }

    # ------------------------------------------------------------------
    # Letter templates
    # ------------------------------------------------------------------

    def _header(self, req: DSGVORequest) -> str:
        return f"""{req.requester_name}
{req.requester_address}

An:
{req.controller}
{req.controller_address}

{datetime.utcnow().strftime("%d.%m.%Y")}

Betreff: Datenschutzrechtliche Anfrage gemäß DSGVO — Referenz {req.id}
"""

    def _footer(self, req: DSGVORequest) -> str:
        return f"""
Mit freundlichen Grüßen,
{req.requester_name}

---
Diese Anfrage wurde automatisch generiert durch das ANTI-KI OPSEC-System.
Bitte antworten Sie innerhalb von 30 Tagen (Art. 12 Abs. 3 DSGVO).
"""

    def _letter_auskunft(self, req: DSGVORequest) -> str:
        return self._header(req) + f"""
Sehr geehrte Damen und Herren,

gemäß Art. 15 der Datenschutz-Grundverordnung (DSGVO) beantrage ich hiermit
unentgeltlich Auskunft über alle personenbezogenen Daten, die Ihre Organisation
über mich gespeichert hat.

Ich bitte um Auskunft zu:
1. Welche personenbezogenen Daten werden verarbeitet?
2. Zu welchen Zwecken erfolgt die Verarbeitung?
3. Aus welchen Quellen stammen die Daten?
4. An welche Empfänger wurden Daten weitergegeben?
5. Wie lange werden die Daten gespeichert?
6. Wurden automatisierte Entscheidungen oder Profiling durchgeführt?

{f"Ergänzender Sachverhalt: {req.subject_description}" if req.subject_description else ""}

Bitte beachten Sie, dass Sie gesetzlich verpflichtet sind, innerhalb von
einem Monat zu antworten (Art. 12 Abs. 3 DSGVO).
""" + self._footer(req)

    def _letter_loeschung(self, req: DSGVORequest) -> str:
        return self._header(req) + f"""
Sehr geehrte Damen und Herren,

gemäß Art. 17 DSGVO fordere ich die unverzügliche Löschung aller mich
betreffenden personenbezogenen Daten.

{f"Konkret handelt es sich um: {req.subject_description}" if req.subject_description else ""}

Löschgründe (Art. 17 Abs. 1 DSGVO):
- Die Daten sind für die ursprünglichen Zwecke nicht mehr erforderlich
- Ich widerrufe hiermit jede erteilte Einwilligung
- Die Verarbeitung erfolgt ohne Rechtsgrundlage

Ich fordere Sie auf, mir die erfolgte Löschung schriftlich zu bestätigen
sowie alle Drittparteien zu informieren, an die Daten weitergegeben wurden.
""" + self._footer(req)

    def _letter_widerspruch(self, req: DSGVORequest) -> str:
        return self._header(req) + f"""
Sehr geehrte Damen und Herren,

gemäß Art. 21 DSGVO lege ich hiermit Widerspruch gegen die Verarbeitung
meiner personenbezogenen Daten — insbesondere zum Zweck der Profilbildung,
Verhaltensanalyse, Risikoeinschätzung und automatisierten Entscheidungsfindung — ein.

{f"Kontext: {req.subject_description}" if req.subject_description else ""}

Sie haben ab Eingang dieses Widerspruchs die Verarbeitung unverzüglich
einzustellen (Art. 21 Abs. 1 DSGVO), sofern Sie keine zwingenden
schutzwürdigen Gründe nachweisen können.
""" + self._footer(req)

    def _letter_berichtigung(self, req: DSGVORequest) -> str:
        return self._header(req) + f"""
Sehr geehrte Damen und Herren,

gemäß Art. 16 DSGVO fordere ich die Berichtigung unrichtiger
personenbezogener Daten sowie die Vervollständigung unvollständiger Daten.

Konkrete Berichtigung: {req.subject_description}
""" + self._footer(req)

    def _letter_einschraenkung(self, req: DSGVORequest) -> str:
        return self._header(req) + f"""
Sehr geehrte Damen und Herren,

gemäß Art. 18 DSGVO beantrage ich die Einschränkung der Verarbeitung
meiner personenbezogenen Daten.

Begründung: {req.subject_description}

Die Daten dürfen während der Einschränkung nur mit meiner Einwilligung
oder zur Geltendmachung von Rechtsansprüchen verarbeitet werden.
""" + self._footer(req)

    def _letter_beschwerde(self, req: DSGVORequest) -> str:
        return self._header(req) + f"""
Sehr geehrte Damen und Herren,

ich reiche hiermit Beschwerde gemäß Art. 77 DSGVO ein gegen:

Verantwortlicher: {req.controller}
Adresse: {req.controller_address}

Beschwerdegegenstand: {req.subject_description}

Ich bitte um Einleitung eines Prüfverfahrens und Unterrichtung über
den Ausgang gemäß Art. 77 Abs. 2 DSGVO.
""" + self._footer(req)

    def _letter_eskalation(self, req: DSGVORequest, behoerde: dict) -> str:
        sent_info = f"Meine ursprüngliche Anfrage vom {req.sent_at.strftime('%d.%m.%Y') if req.sent_at else 'unbekannt'} (Ref: {req.id}) blieb unbeantwortet."
        return f"""{req.requester_name}
{req.requester_address}

An:
{behoerde['name']}
{behoerde['address']}

{datetime.utcnow().strftime("%d.%m.%Y")}

Betreff: Beschwerde gemäß Art. 77 DSGVO gegen {req.controller}

Sehr geehrte Damen und Herren,

{sent_info}

Die gesetzliche Frist von 30 Tagen (Art. 12 Abs. 3 DSGVO) wurde
durch {req.controller} nicht eingehalten. Ich bitte um Einleitung
aufsichtsbehördlicher Maßnahmen gemäß Art. 58 DSGVO.

Anlage: Kopie der ursprünglichen Anfrage (Ref. {req.id})

Mit freundlichen Grüßen,
{req.requester_name}
"""

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _save(self, req: DSGVORequest):
        path = self.storage / f"{req.id}.json"
        data = {
            "id": req.id,
            "controller": req.controller,
            "controller_address": req.controller_address,
            "controller_email": req.controller_email,
            "request_type": req.request_type,
            "requester_name": req.requester_name,
            "requester_address": req.requester_address,
            "subject_description": req.subject_description,
            "created_at": req.created_at.isoformat(),
            "sent_at": req.sent_at.isoformat() if req.sent_at else None,
            "deadline": req.deadline.isoformat() if req.deadline else None,
            "status": req.status,
            "notes": req.notes,
        }
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def _load_existing(self):
        for path in self.storage.glob("*.json"):
            try:
                data = json.loads(path.read_text())
                req = DSGVORequest(**{
                    k: v for k, v in data.items()
                    if k not in ("created_at", "sent_at", "deadline", "request_type", "status")
                })
                req.created_at = datetime.fromisoformat(data["created_at"])
                req.sent_at = datetime.fromisoformat(data["sent_at"]) if data.get("sent_at") else None
                req.deadline = datetime.fromisoformat(data["deadline"]) if data.get("deadline") else None
                req.request_type = RequestType(data["request_type"])
                req.status = RequestStatus(data["status"])
                self._requests[req.id] = req
            except Exception:
                pass
