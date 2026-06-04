"""
NarrativeRadar — Erkennung und Analyse politischer Narrative

Überwacht öffentliche Diskurse auf reaktionäre Frames und Desinformation.
Gibt Gramsci-Modul Kontext für gezielte Gegennarrative.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import requests

LLM_SERVER = "http://localhost:8001"


class NarrativeType(str, Enum):
    RECHTSEXTREM        = "rechtsextrem"
    ISLAMFEINDLICH      = "islamfeindlich"
    ANTIFEMINISTISCH    = "antifeministisch"
    KLIMALEUGNUNG       = "klimaleugnung"
    VERSCHWÖRUNG        = "verschwörung"
    RASSISTISCH         = "rassistisch"
    KLASSISMUS          = "klassismus"
    ANTIKOMMUNISMUS     = "antikommunismus"
    POLIZEIPROPAGANDA   = "polizeipropaganda"
    NEOLIBERAL          = "neoliberal"
    NEUTRAL             = "neutral"
    UNBEKANNT           = "unbekannt"


class ThreatLevel(str, Enum):
    GERING      = "gering"
    MITTEL      = "mittel"
    HOCH        = "hoch"
    KRITISCH    = "kritisch"


KNOWN_FRAMES: dict[NarrativeType, list[str]] = {
    NarrativeType.RECHTSEXTREM: [
        "ausländerkriminalität", "überfremdung", "remigration", "volksverrat",
        "great replacement", "bevölkerungsaustausch", "lügenpresse",
        "umvolkung", "abendland", "islamisierung",
    ],
    NarrativeType.KLIMALEUGNUNG: [
        "klimahysterie", "klimasekte", "klimaschwindel", "co2 ist pflanzendünger",
        "klimawandel natürlich", "klimaalarmismus", "klimakleber terroristen",
    ],
    NarrativeType.VERSCHWÖRUNG: [
        "weltwirtschaftsforum steuert", "bill gates chip", "tiefenstaat",
        "great reset", "neue weltordnung", "agenda 2030 kontrolliert",
        "5g corona", "depopulation agenda",
    ],
    NarrativeType.ANTIFEMINISTISCH: [
        "genderideologie", "frühsexualisierung", "männerfeinde",
        "feminismus zerstört", "traditionelle werte", "natürliche rollen",
    ],
    NarrativeType.ANTIKOMMUNISMUS: [
        "kommunismus hat überall versagt", "sozialismus führt zu diktatur",
        "venezuela sozialismus", "linksextremisten", "marxistische infiltration",
    ],
    NarrativeType.POLIZEIPROPAGANDA: [
        "einzelfall", "cops sind helden", "antifa ist terrororganisation",
        "linke gewalt", "klimakleber blockieren",
    ],
}


@dataclass
class NarrativeHit:
    narrative_type: NarrativeType
    threat_level: ThreatLevel
    detected_frames: list[str]
    source_text: str
    counter_narrative_suggestion: str = ""
    confidence: float = 0.0


@dataclass
class RadarReport:
    text: str
    hits: list[NarrativeHit] = field(default_factory=list)
    dominant_narrative: NarrativeType = NarrativeType.NEUTRAL
    overall_threat: ThreatLevel = ThreatLevel.GERING
    recommended_response_tone: str = "sachlich"
    llm_analysis: str = ""

    @property
    def requires_response(self) -> bool:
        return self.overall_threat in (ThreatLevel.HOCH, ThreatLevel.KRITISCH)

    @property
    def frame_summary(self) -> str:
        all_frames = [f for hit in self.hits for f in hit.detected_frames]
        return ", ".join(all_frames[:10])


class NarrativeRadar:
    """
    Scannt Texte auf reaktionäre Frames und schlägt Gegennarrative vor.

    Kombiniert regelbasiertes Keyword-Matching mit ProletariaLLM-Analyse.
    """

    def __init__(self, llm_url: str = LLM_SERVER):
        self.llm_url = llm_url

    def scan(self, text: str, use_llm: bool = True) -> RadarReport:
        """Vollständige Analyse eines Textes."""
        report = RadarReport(text=text)
        text_lower = text.lower()

        for narrative_type, keywords in KNOWN_FRAMES.items():
            found = [kw for kw in keywords if kw in text_lower]
            if found:
                threat = self._assess_threat(found, narrative_type)
                hit = NarrativeHit(
                    narrative_type=narrative_type,
                    threat_level=threat,
                    detected_frames=found,
                    source_text=text[:200],
                )
                report.hits.append(hit)

        if report.hits:
            report.dominant_narrative = max(
                report.hits, key=lambda h: len(h.detected_frames)
            ).narrative_type
            threat_order = [ThreatLevel.GERING, ThreatLevel.MITTEL, ThreatLevel.HOCH, ThreatLevel.KRITISCH]
            report.overall_threat = max(
                (h.threat_level for h in report.hits),
                key=lambda t: threat_order.index(t),
            )

        if use_llm and self.llm_url:
            report.llm_analysis = self._llm_analyze(text, report)
            report.recommended_response_tone = self._suggest_tone(report)

        return report

    def scan_batch(self, texts: list[str]) -> list[RadarReport]:
        return [self.scan(t, use_llm=False) for t in texts]

    def suggest_counter_narrative(self, report: RadarReport, language: str = "de") -> str:
        """Lässt ProletariaLLM ein konkretes Gegennarrativ generieren."""
        if not report.hits:
            return ""

        lang_names = {"de": "Deutsch", "en": "English", "fr": "Français",
                      "nl": "Nederlands", "es": "Español", "it": "Italiano", "pl": "Polski"}
        lang_name = lang_names.get(language, language)

        prompt = f"""Analysiere folgenden reaktionären Text und formuliere ein wirksames Gegennarrativ.

Text:
---
{report.text[:500]}
---

Erkannte Frames: {report.frame_summary}
Dominantes Narrativ: {report.dominant_narrative.value}

Schreibe in {lang_name} ein kurzes, schlagkräftiges Gegennarrativ (max. 3 Sätze) das:
- Den reaktionären Frame benennt und dekonstruiert
- Eine progressive Alternative setzt
- Verständlich für breite Öffentlichkeit ist"""

        try:
            resp = requests.post(
                f"{self.llm_url}/generate",
                json={"prompt": prompt, "temperature": 0.7, "max_tokens": 300},
                timeout=60,
            )
            resp.raise_for_status()
            return resp.json().get("response", "").strip()
        except Exception:
            return ""

    def _assess_threat(self, found_keywords: list[str], narrative_type: NarrativeType) -> ThreatLevel:
        n = len(found_keywords)
        if narrative_type in (NarrativeType.RECHTSEXTREM, NarrativeType.RASSISTISCH):
            if n >= 3:
                return ThreatLevel.KRITISCH
            if n >= 2:
                return ThreatLevel.HOCH
            return ThreatLevel.MITTEL
        if n >= 4:
            return ThreatLevel.HOCH
        if n >= 2:
            return ThreatLevel.MITTEL
        return ThreatLevel.GERING

    def _llm_analyze(self, text: str, report: RadarReport) -> str:
        try:
            frames_hint = f"Erkannte Frames: {report.frame_summary}" if report.hits else ""
            resp = requests.post(
                f"{self.llm_url}/analyze",
                json={
                    "text": text[:1000],
                    "task": "narrative_analysis",
                    "hint": frames_hint,
                },
                timeout=60,
            )
            resp.raise_for_status()
            return resp.json().get("analysis", "").strip()
        except Exception:
            return ""

    def _suggest_tone(self, report: RadarReport) -> str:
        tone_map = {
            ThreatLevel.GERING:   "sachlich-informativ",
            ThreatLevel.MITTEL:   "sachlich-engagiert",
            ThreatLevel.HOCH:     "konfrontativ-sachlich",
            ThreatLevel.KRITISCH: "klar-ablehnend",
        }
        return tone_map.get(report.overall_threat, "sachlich")
