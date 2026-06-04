"""
HegemonieAnalyzer — Strategische Analyse des Diskursraums

Bewertet welche Themen, Frames und Räume für Gegenhegemoniearbeit
am wirksamsten sind. Unterstützt strategische Kampagnenplanung.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import requests

LLM_SERVER = "http://localhost:8001"


class DiscourseArena(str, Enum):
    SOZIALE_MEDIEN      = "soziale_medien"
    KOMMENTARBEREICHE   = "kommentarbereiche"
    PETITIONEN          = "petitionen"
    BUERGERBETEILIGUNG  = "buergerbeteiligung"
    PRESSE              = "presse"
    NEWSLETTER          = "newsletter"
    PRINT               = "print"
    LOKALPOLITIK        = "lokalpolitik"


class StrategicPriority(str, Enum):
    NIEDRIG     = "niedrig"
    MITTEL      = "mittel"
    HOCH        = "hoch"
    DRINGEND    = "dringend"


@dataclass
class ArenaAssessment:
    arena: DiscourseArena
    priority: StrategicPriority
    rationale: str
    recommended_content_types: list[str]
    recommended_languages: list[str]
    estimated_reach: str  # "lokal", "regional", "national", "international"


@dataclass
class HegemonyCampaignStrategy:
    topic: str
    core_message: str
    counter_frames: list[str]
    arena_assessments: list[ArenaAssessment] = field(default_factory=list)
    timeline_weeks: int = 4
    key_audiences: list[str] = field(default_factory=list)
    llm_strategic_advice: str = ""

    def top_arenas(self, n: int = 3) -> list[ArenaAssessment]:
        order = [StrategicPriority.DRINGEND, StrategicPriority.HOCH,
                 StrategicPriority.MITTEL, StrategicPriority.NIEDRIG]
        sorted_arenas = sorted(
            self.arena_assessments,
            key=lambda a: order.index(a.priority),
        )
        return sorted_arenas[:n]


class HegemonieAnalyzer:
    """
    Strategische Analyse für Gegenhegemoniearbeit.

    Beantwortet: Wo sollen wir ansetzen? Mit welchem Frame?
    Für welche Zielgruppe? In welcher Sprache?
    """

    ARENA_DEFAULTS: dict[DiscourseArena, dict] = {
        DiscourseArena.SOZIALE_MEDIEN: {
            "content_types": ["short_post", "thread", "meme_text"],
            "reach": "national",
        },
        DiscourseArena.KOMMENTARBEREICHE: {
            "content_types": ["comment_response"],
            "reach": "regional",
        },
        DiscourseArena.PETITIONEN: {
            "content_types": ["petition_text", "short_post"],
            "reach": "national",
        },
        DiscourseArena.BUERGERBETEILIGUNG: {
            "content_types": ["public_statement", "long_form"],
            "reach": "lokal",
        },
        DiscourseArena.PRESSE: {
            "content_types": ["press_release", "letter_to_editor"],
            "reach": "regional",
        },
        DiscourseArena.NEWSLETTER: {
            "content_types": ["newsletter"],
            "reach": "lokal",
        },
        DiscourseArena.PRINT: {
            "content_types": ["flyer"],
            "reach": "lokal",
        },
        DiscourseArena.LOKALPOLITIK: {
            "content_types": ["public_statement", "press_release"],
            "reach": "lokal",
        },
    }

    def __init__(self, llm_url: str = LLM_SERVER):
        self.llm_url = llm_url

    def analyze(
        self,
        topic: str,
        context: str = "",
        languages: list[str] = None,
        arenas: list[DiscourseArena] = None,
    ) -> HegemonyCampaignStrategy:
        """Erstellt vollständige Kampagnenstrategie für ein Thema."""
        languages = languages or ["de"]
        arenas = arenas or list(DiscourseArena)

        strategy = HegemonyCampaignStrategy(
            topic=topic,
            core_message="",
            counter_frames=[],
            key_audiences=[],
        )

        for arena in arenas:
            defaults = self.ARENA_DEFAULTS.get(arena, {})
            assessment = ArenaAssessment(
                arena=arena,
                priority=self._default_priority(arena, topic),
                rationale=f"Standard-Bewertung für {arena.value}",
                recommended_content_types=defaults.get("content_types", []),
                recommended_languages=languages,
                estimated_reach=defaults.get("reach", "lokal"),
            )
            strategy.arena_assessments.append(assessment)

        if self.llm_url:
            strategy.llm_strategic_advice = self._llm_strategy(topic, context, languages)
            self._enrich_strategy(strategy, topic, context)

        return strategy

    def evaluate_message(
        self,
        message: str,
        target_audience: str = "",
        language: str = "de",
    ) -> dict:
        """Bewertet eine Kernbotschaft auf Wirksamkeit und Framing."""
        lang_names = {"de": "Deutsch", "en": "English", "fr": "Français",
                      "nl": "Nederlands", "es": "Español", "it": "Italiano", "pl": "Polski"}
        lang_name = lang_names.get(language, language)

        prompt = f"""Bewerte folgende politische Botschaft auf:
1. Framing (progressiv/reaktionär/neutral)
2. Emotionale Wirkung (0-10)
3. Verständlichkeit (0-10)
4. Handlungsaufforderung vorhanden (ja/nein)
5. Verbesserungsvorschlag (1 Satz)

Botschaft: "{message}"
{f"Zielgruppe: {target_audience}" if target_audience else ""}
Sprache: {lang_name}

Antworte strukturiert."""

        try:
            resp = requests.post(
                f"{self.llm_url}/generate",
                json={"prompt": prompt, "temperature": 0.5, "max_tokens": 400},
                timeout=60,
            )
            resp.raise_for_status()
            return {"evaluation": resp.json().get("response", "").strip()}
        except Exception as e:
            return {"evaluation": f"[FEHLER: {e}]"}

    def _default_priority(self, arena: DiscourseArena, topic: str) -> StrategicPriority:
        high_priority = {
            DiscourseArena.SOZIALE_MEDIEN,
            DiscourseArena.KOMMENTARBEREICHE,
            DiscourseArena.PETITIONEN,
        }
        if arena in high_priority:
            return StrategicPriority.HOCH
        if arena == DiscourseArena.PRESSE:
            return StrategicPriority.MITTEL
        return StrategicPriority.NIEDRIG

    def _llm_strategy(self, topic: str, context: str, languages: list[str]) -> str:
        lang_str = ", ".join(languages)
        try:
            resp = requests.post(
                f"{self.llm_url}/generate",
                json={
                    "prompt": f"""Entwickle eine kurze Gegenhegemoniesstrategie für:
Thema: {topic}
{f"Kontext: {context}" if context else ""}
Sprachen: {lang_str}

Beantworte: Welcher Frame soll gesetzt werden? Welche Zielgruppe priorisieren?
Welche drei Kernbotschaften? (Max. 200 Wörter)""",
                    "temperature": 0.7,
                    "max_tokens": 500,
                },
                timeout=90,
            )
            resp.raise_for_status()
            return resp.json().get("response", "").strip()
        except Exception:
            return ""

    def _enrich_strategy(self, strategy: HegemonyCampaignStrategy, topic: str, context: str):
        try:
            resp = requests.post(
                f"{self.llm_url}/generate",
                json={
                    "prompt": f"Welche 3-5 Zielgruppen sind für '{topic}' am wichtigsten? Nur Liste, keine Erklärungen.",
                    "temperature": 0.5,
                    "max_tokens": 150,
                },
                timeout=30,
            )
            resp.raise_for_status()
            lines = resp.json().get("response", "").strip().split("\n")
            strategy.key_audiences = [l.strip("- •123.") for l in lines if l.strip()][:5]
        except Exception:
            pass
