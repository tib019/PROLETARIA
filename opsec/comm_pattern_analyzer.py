"""
CommPatternAnalyzer — erkennt Kommunikationsmuster die OPSEC gefährden

Analysiert Metadaten (nicht Inhalte) der Kommunikationsstruktur einer
Organisation auf gefährliche Muster: Zentralisierung, regelmäßige
Taktzeiten, erkennbare Rollen.

Defensiver Einsatz: Selbstaudit von Kommunikationsstrukturen.
"""
from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class CommEvent:
    sender_id: str    # anonymisiert/gehashed
    receiver_id: str  # anonymisiert/gehashed
    timestamp: datetime
    channel: str      # "signal", "matrix", "email", "phone"
    size_bytes: int = 0


@dataclass
class OpsecRisk:
    severity: str
    pattern: str
    description: str
    recommendation: str
    affected_nodes: list[str] = field(default_factory=list)


class CommPatternAnalyzer:
    """
    Analysiert Kommunikationsmetadaten auf OPSEC-Risiken.

    Input: Liste von CommEvents (anonymisiert — keine Inhalte)
    Output: Liste von OpsecRisk-Befunden

    Erkannte Risikotypen:
    - Zentralknoten (Single Point of Failure + Identifikationsziel)
    - Regelmäßige Taktzeiten (erkennbare Meetingzeiten)
    - Unverschlüsselte Kanäle in sensitiven Verbindungen
    - Starke Clusterbildung (Gruppenidentifikation)
    - Burst-Kommunikation vor Aktionen (Timing-Fingerprint)
    """

    SAFE_CHANNELS = {"signal", "matrix", "briar", "session"}
    UNSAFE_CHANNELS = {"email", "sms", "telegram", "whatsapp", "phone"}

    def __init__(self, events: Optional[list[CommEvent]] = None):
        self.events: list[CommEvent] = events or []

    def add_events(self, events: list[CommEvent]):
        self.events.extend(events)

    def analyze(self) -> list[OpsecRisk]:
        if not self.events:
            return []

        risks: list[OpsecRisk] = []
        risks += self._check_centralization()
        risks += self._check_regular_timing()
        risks += self._check_unsafe_channels()
        risks += self._check_burst_patterns()
        risks += self._check_asymmetric_communication()

        return sorted(risks, key=lambda r: ["critical","high","medium","low"].index(r.severity)
                      if r.severity in ["critical","high","medium","low"] else 4)

    def network_stats(self) -> dict:
        """Grundlegende Netzwerkstatistiken."""
        nodes = set()
        edges: dict[tuple, int] = defaultdict(int)
        for ev in self.events:
            nodes.add(ev.sender_id)
            nodes.add(ev.receiver_id)
            edges[(ev.sender_id, ev.receiver_id)] += 1

        degree: dict[str, int] = defaultdict(int)
        for s, r in edges:
            degree[s] += 1
            degree[r] += 1

        return {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "event_count": len(self.events),
            "avg_degree": sum(degree.values()) / len(degree) if degree else 0,
            "max_degree_node": max(degree, key=degree.get) if degree else None,
            "channel_distribution": dict(Counter(e.channel for e in self.events)),
        }

    # ------------------------------------------------------------------
    # Risk checks
    # ------------------------------------------------------------------

    def _check_centralization(self) -> list[OpsecRisk]:
        """Erkennt Knoten mit unverhältnismäßig hoher Kommunikation."""
        degree: dict[str, int] = defaultdict(int)
        for ev in self.events:
            degree[ev.sender_id] += 1
            degree[ev.receiver_id] += 1

        if not degree:
            return []

        total = sum(degree.values())
        avg = total / len(degree)
        risks = []

        for node, deg in degree.items():
            ratio = deg / avg
            if ratio > 5.0:
                risks.append(OpsecRisk(
                    severity="critical",
                    pattern="Hochgradig zentraler Knoten",
                    description=(
                        f"Knoten {node} hat {deg} Verbindungen ({ratio:.1f}× Durchschnitt). "
                        "Solche Knoten sind primäre Zielpunkte für Überwachung und "
                        "Organisationsstruktur-Rekonstruktion."
                    ),
                    recommendation=(
                        "Dezentralisierung: Rollen auf mehrere Personen verteilen. "
                        "Horizontale Netzwerkstruktur anstreben."
                    ),
                    affected_nodes=[node],
                ))
            elif ratio > 3.0:
                risks.append(OpsecRisk(
                    severity="high",
                    pattern="Erhöhte Zentralisierung",
                    description=f"Knoten {node} hat {ratio:.1f}× durchschnittliche Konnektivität.",
                    recommendation="Aufgaben und Kommunikation breiter verteilen.",
                    affected_nodes=[node],
                ))

        return risks

    def _check_regular_timing(self) -> list[OpsecRisk]:
        """Erkennt regelmäßige Kommunikationsmuster (z.B. wöchentliche Plenum-Zeiten)."""
        if len(self.events) < 10:
            return []

        hour_counts: dict[int, int] = defaultdict(int)
        weekday_counts: dict[int, int] = defaultdict(int)

        for ev in self.events:
            hour_counts[ev.timestamp.hour] += 1
            weekday_counts[ev.timestamp.weekday()] += 1

        risks = []
        total = len(self.events)

        # Stunden-Konzentration
        for hour, count in hour_counts.items():
            if count / total > 0.25:
                risks.append(OpsecRisk(
                    severity="medium",
                    pattern="Regelmäßige Kommunikationszeit",
                    description=(
                        f"{count/total*100:.0f}% aller Nachrichten werden um {hour}:00 Uhr gesendet. "
                        "Regelmäßige Muster erlauben Rückschlüsse auf Treffen und Aktionsplanung."
                    ),
                    recommendation=(
                        "Kommunikationszeiten variieren. Asynchrone Kommunikation bevorzugen. "
                        "Wichtige Meetings auf wechselnde Zeiten legen."
                    ),
                ))

        # Wochentag-Konzentration
        days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
        for day, count in weekday_counts.items():
            if count / total > 0.30:
                risks.append(OpsecRisk(
                    severity="low",
                    pattern="Wochentag-Konzentration",
                    description=f"Erhöhte Aktivität am {days[day]} ({count/total*100:.0f}% aller Events).",
                    recommendation="Aktivitäten auf verschiedene Wochentage verteilen.",
                ))

        return risks

    def _check_unsafe_channels(self) -> list[OpsecRisk]:
        """Warnt bei Nutzung unsicherer Kommunikationskanäle."""
        unsafe_events = [e for e in self.events if e.channel.lower() in self.UNSAFE_CHANNELS]
        if not unsafe_events:
            return []

        channel_counts = Counter(e.channel for e in unsafe_events)
        ratio = len(unsafe_events) / len(self.events)

        severity = "critical" if ratio > 0.3 else "high" if ratio > 0.1 else "medium"

        return [OpsecRisk(
            severity=severity,
            pattern="Unsichere Kommunikationskanäle",
            description=(
                f"{len(unsafe_events)} von {len(self.events)} Nachrichten ({ratio*100:.0f}%) "
                f"über unsichere Kanäle: {dict(channel_counts)}. "
                "Metadaten sind für Behörden ohne richterlichen Beschluss abrufbar."
            ),
            recommendation=(
                "Migration auf sichere Kanäle: Signal für Mobile, Matrix/Element für Gruppen. "
                "E-Mail nur verschlüsselt (PGP). Kein Telegram für Sensitive."
            ),
        )]

    def _check_burst_patterns(self) -> list[OpsecRisk]:
        """Erkennt Burst-Kommunikation (kurz vor Aktionen typisch)."""
        if len(self.events) < 20:
            return []

        # Nachrichten pro Stunde
        hourly: dict[str, int] = defaultdict(int)
        for ev in self.events:
            key = ev.timestamp.strftime("%Y-%m-%d-%H")
            hourly[key] += 1

        counts = list(hourly.values())
        avg = sum(counts) / len(counts)
        std = math.sqrt(sum((c - avg) ** 2 for c in counts) / len(counts))

        bursts = [(k, v) for k, v in hourly.items() if v > avg + 3 * std]

        if not bursts:
            return []

        return [OpsecRisk(
            severity="medium",
            pattern="Burst-Kommunikation erkannt",
            description=(
                f"{len(bursts)} Stunden mit Kommunikationsvolumen >3σ über Durchschnitt. "
                "Burst-Muster vor Aktionen sind ein erkennbarer Fingerabdruck."
            ),
            recommendation=(
                "Vorab-Kommunikation über taktische Details auf Präsenz-Treffen verlagern. "
                "Kein erhöhtes digitales Kommunikationsvolumen kurz vor Aktionen."
            ),
        )]

    def _check_asymmetric_communication(self) -> list[OpsecRisk]:
        """Erkennt Broadcaster (senden viel, empfangen wenig) — Führungsstrukturen."""
        sent: dict[str, int] = defaultdict(int)
        received: dict[str, int] = defaultdict(int)

        for ev in self.events:
            sent[ev.sender_id] += 1
            received[ev.receiver_id] += 1

        risks = []
        all_nodes = set(sent) | set(received)
        for node in all_nodes:
            s = sent.get(node, 0)
            r = received.get(node, 0)
            if s + r < 5:
                continue
            ratio = s / (r + 1)
            if ratio > 8:
                risks.append(OpsecRisk(
                    severity="medium",
                    pattern="Asymmetrischer Broadcaster",
                    description=(
                        f"Knoten {node} sendet {s}× aber empfängt nur {r}×. "
                        "Broadcaster-Muster identifiziert Führungspersonen."
                    ),
                    recommendation=(
                        "Bidirektionale Kommunikation stärken. "
                        "Dezentrale Informationsverteilung ohne Führungsperson als Hub."
                    ),
                    affected_nodes=[node],
                ))

        return risks
