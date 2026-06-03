"""
OpsecAlgedonicChannel — algedonischer Kanal für OPSEC-Bedrohungseskalation

Analog zum Cybersyn-Algedonischen Kanal (Beer 1972):
Bypass der normalen Berichtskette wenn OPSEC-Bedrohung kritische Schwelle überschreitet.

Stufen:
  GRÜN   (0-3)  — Normalbetrieb
  GELB   (4-6)  — Erhöhte Aufmerksamkeit
  ORANGE (7-8)  — Aktive Bedrohung, Gegenmaßnahmen einleiten
  ROT    (9-10) — Kritische Kompromittierung, Notfallprotokoll

Bei ROT: sofortige Benachrichtigung aller Mitglieder, Kommunikationsstopp,
Wechsel zu Backup-Kanälen, rechtliche Unterstützung aktivieren.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class ThreatLevel(str, Enum):
    GREEN  = "GRÜN"
    YELLOW = "GELB"
    ORANGE = "ORANGE"
    RED    = "ROT"


@dataclass
class ThreatEvent:
    score: int                 # 0–10
    source: str                # z.B. "exposure_scanner", "comm_analyzer", "manual"
    description: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    auto_actions_taken: list[str] = field(default_factory=list)


class OpsecAlgedonicChannel:
    """
    Zentraler Alarmkanal der ANTI-KI OPSEC-Infrastruktur.

    Wird von ExposureScanner, CommPatternAnalyzer und manuellen
    Meldungen gespeist. Eskaliert automatisch bei Schwellenwertüberschreitung.

    Einsatz:
    - Zentrales Monitoring-Dashboard für OPSEC-Verantwortliche
    - Automatische Auslösung von Gegenmaßnahmen
    - Protokollierung für Nachbesprechung (After-Action Review)
    """

    THRESHOLDS = {
        ThreatLevel.YELLOW: 4,
        ThreatLevel.ORANGE: 7,
        ThreatLevel.RED:    9,
    }

    def __init__(
        self,
        on_escalation: Optional[Callable[[ThreatLevel, ThreatEvent], None]] = None,
        history_path: str = "data/opsec_algedonic.json",
    ):
        self._current_level = ThreatLevel.GREEN
        self._current_score = 0
        self._history: list[ThreatEvent] = []
        self._on_escalation = on_escalation
        self._history_path = history_path
        self._response_plans: dict[ThreatLevel, list[str]] = self._default_plans()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def report(self, score: int, source: str, description: str) -> ThreatLevel:
        """
        Meldet ein Bedrohungsereignis.

        score: 1–10 (Schwere des Ereignisses)
        Returns: neue Bedrohungsstufe
        """
        score = max(0, min(10, score))
        event = ThreatEvent(score=score, source=source, description=description)

        self._update_score(score)
        new_level = self._compute_level()

        if new_level != self._current_level:
            old_level = self._current_level
            self._current_level = new_level
            event.auto_actions_taken = self._auto_respond(new_level)
            logger.warning(
                "OPSEC ESKALATION: %s → %s (Score: %d) | %s",
                old_level, new_level, self._current_score, description
            )
            if self._on_escalation:
                self._on_escalation(new_level, event)

        self._history.append(event)
        self._persist()
        return new_level

    def report_from_findings(self, findings: list, source: str = "scanner") -> ThreatLevel:
        """Aggregiert ExposureFinding-Liste zu einem Score."""
        severity_scores = {"critical": 10, "high": 7, "medium": 4, "low": 2, "info": 0}
        if not findings:
            return self._current_level

        max_score = max(severity_scores.get(getattr(f, 'severity', 'info'), 0) for f in findings)
        count_weight = min(3, len(findings) // 3)
        effective_score = min(10, max_score + count_weight)

        descriptions = "; ".join(
            getattr(f, 'description', str(f))[:60] for f in findings[:3]
        )
        return self.report(effective_score, source, f"{len(findings)} Findings: {descriptions}")

    @property
    def status(self) -> dict:
        return {
            "level": self._current_level,
            "score": self._current_score,
            "response_plan": self._response_plans.get(self._current_level, []),
            "event_count": len(self._history),
            "last_event": self._history[-1].timestamp.isoformat() if self._history else None,
        }

    def reset(self, reason: str = "Manueller Reset"):
        """Setzt Kanal zurück (nach Behebung der Bedrohung)."""
        event = ThreatEvent(score=0, source="manual", description=f"Reset: {reason}")
        self._history.append(event)
        self._current_score = 0
        self._current_level = ThreatLevel.GREEN
        self._persist()

    def get_history(self, last_n: int = 50) -> list[dict]:
        return [
            {
                "score": e.score,
                "source": e.source,
                "description": e.description,
                "timestamp": e.timestamp.isoformat(),
                "actions": e.auto_actions_taken,
            }
            for e in self._history[-last_n:]
        ]

    def set_response_plan(self, level: ThreatLevel, actions: list[str]):
        """Überschreibt Standardmaßnahmen für eine Stufe."""
        self._response_plans[level] = actions

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _update_score(self, new_score: int):
        # Exponentiell gewichteter Durchschnitt (α=0.4) — reagiert schnell auf Spitzen
        alpha = 0.4
        self._current_score = int(alpha * new_score + (1 - alpha) * self._current_score)

    def _compute_level(self) -> ThreatLevel:
        if self._current_score >= self.THRESHOLDS[ThreatLevel.RED]:
            return ThreatLevel.RED
        if self._current_score >= self.THRESHOLDS[ThreatLevel.ORANGE]:
            return ThreatLevel.ORANGE
        if self._current_score >= self.THRESHOLDS[ThreatLevel.YELLOW]:
            return ThreatLevel.YELLOW
        return ThreatLevel.GREEN

    def _auto_respond(self, level: ThreatLevel) -> list[str]:
        """Automatische Gegenmaßnahmen bei Eskalation."""
        actions = self._response_plans.get(level, [])
        for action in actions:
            logger.info("AUTO-RESPONSE [%s]: %s", level, action)
        return actions

    @staticmethod
    def _default_plans() -> dict[ThreatLevel, list[str]]:
        return {
            ThreatLevel.GREEN: [],
            ThreatLevel.YELLOW: [
                "OPSEC-Verantwortliche benachrichtigen",
                "Exposition-Scan wiederholen",
                "Kommunikationskanäle prüfen",
            ],
            ThreatLevel.ORANGE: [
                "Alle aktiven Mitglieder über erhöhte Bedrohung informieren",
                "Wechsel zu sekundären Kommunikationskanälen",
                "Sensitive Aktionen pausieren",
                "Juridische Unterstützung kontaktieren (Rote Hilfe / GFF)",
                "Backup-Infrastruktur aktivieren",
            ],
            ThreatLevel.RED: [
                "SOFORTIGER Kommunikationsstopp auf primären Kanälen",
                "Alle Mitglieder über Notfallkanal (Analog/in-Person) informieren",
                "Kompromittierte Geräte isolieren",
                "Anwalt kontaktieren",
                "Betroffene Infrastruktur offline nehmen",
                "After-Action Review einleiten",
                "DSGVO Auskunftsanfragen bei relevanten Behörden stellen",
            ],
        }

    def _persist(self):
        try:
            import os
            os.makedirs(os.path.dirname(self._history_path) or ".", exist_ok=True)
            data = {
                "current_level": self._current_level,
                "current_score": self._current_score,
                "history": self.get_history(100),
            }
            with open(self._history_path, "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.debug("Persistenz-Fehler: %s", e)
