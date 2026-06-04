"""
ContentEngine — ProletariaLLM-basierte Inhaltsgenerierung

Erzeugt politische Texte in mehreren Sprachen für alle Kanäle.
Nutzt lokale ProletariaLLM-Inferenz — kein externes Logging.
"""
from __future__ import annotations

import json
import requests
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

LLM_SERVER = "http://localhost:8001"

SUPPORTED_LANGUAGES = {
    "de": "Deutsch",
    "en": "English",
    "fr": "Français",
    "nl": "Nederlands",
    "es": "Español",
    "it": "Italiano",
    "pl": "Polski",
}

FORMAT_LIMITS = {
    "twitter":    280,
    "mastodon":   500,
    "instagram":  2200,
    "tiktok":     2200,
    "facebook":   63206,
    "telegram":   4096,
    "reddit_title": 300,
    "reddit_body":  40000,
    "comment":    1000,
    "long_form":  None,
    "press_release": None,
    "flyer":      None,
    "newsletter": None,
}


class ContentType(str, Enum):
    SHORT_POST       = "short_post"
    THREAD           = "thread"
    COMMENT_RESPONSE = "comment_response"
    LONG_FORM        = "long_form"
    PRESS_RELEASE    = "press_release"
    LETTER_TO_EDITOR = "letter_to_editor"
    FLYER            = "flyer"
    NEWSLETTER       = "newsletter"
    MEME_TEXT        = "meme_text"
    PETITION_TEXT    = "petition_text"
    PUBLIC_STATEMENT = "public_statement"


@dataclass
class GeneratedContent:
    text: str
    content_type: ContentType
    language: str
    platform: str
    topic: str
    char_count: int = field(init=False)
    approved: bool = False
    edited_text: Optional[str] = None

    def __post_init__(self):
        self.char_count = len(self.text)

    @property
    def final_text(self) -> str:
        return self.edited_text if self.edited_text else self.text

    def fits_platform(self) -> bool:
        limit = FORMAT_LIMITS.get(self.platform)
        return limit is None or len(self.final_text) <= limit


class ContentEngine:
    """
    Erzeugt politische Inhalte via ProletariaLLM.

    Alle Inhalte werden generiert aber NICHT automatisch veröffentlicht.
    Der Mensch entscheidet via ReviewCLI.
    """

    SYSTEM_PROMPT = """Du bist Gramsci — ein politischer Kommunikationsassistent
für linke, antirassistische und klimabewegliche Organisationen.

Du schreibst wirksame, authentische politische Texte die:
- Faktenbasiert und überprüfbar sind
- Klar und verständlich formuliert sind
- Emotionen ansprechen ohne zu manipulieren
- Zur Handlung auffordern
- Die Perspektive marginalisierter Gruppen einbeziehen

Du schreibst NICHT in der Sprache des Feindes (keine Übernahme rechter Frames).
Du verwendest konkrete Beispiele statt Abstraktionen.
Du schreibst in der angegebenen Sprache."""

    def __init__(self, llm_url: str = LLM_SERVER):
        self.llm_url = llm_url

    def generate(
        self,
        topic: str,
        content_type: ContentType,
        platform: str,
        language: str = "de",
        context: str = "",
        target_audience: str = "",
        campaign_tone: str = "sachlich-engagiert",
        counter_narrative: str = "",
    ) -> GeneratedContent:
        """Generiert einen einzelnen Inhalt."""

        lang_name = SUPPORTED_LANGUAGES.get(language, language)
        limit = FORMAT_LIMITS.get(platform)
        limit_hint = f"Maximal {limit} Zeichen." if limit else "Keine Zeichenbegrenzung."

        prompt = self._build_prompt(
            topic=topic,
            content_type=content_type,
            platform=platform,
            lang_name=lang_name,
            limit_hint=limit_hint,
            context=context,
            target_audience=target_audience,
            campaign_tone=campaign_tone,
            counter_narrative=counter_narrative,
        )

        text = self._call_llm(prompt, language)

        return GeneratedContent(
            text=text,
            content_type=content_type,
            language=language,
            platform=platform,
            topic=topic,
        )

    def generate_thread(
        self,
        topic: str,
        platform: str,
        num_posts: int = 5,
        language: str = "de",
        context: str = "",
    ) -> list[GeneratedContent]:
        """Generiert einen mehrteiligen Thread."""
        lang_name = SUPPORTED_LANGUAGES.get(language, language)
        limit = FORMAT_LIMITS.get(platform, 500)

        prompt = f"""Schreibe einen {num_posts}-teiligen Thread auf {platform} über:
Thema: {topic}
Sprache: {lang_name}
Zeichenlimit pro Post: {limit}
{f"Kontext: {context}" if context else ""}

Format: Nummeriere jeden Post mit [1/], [2/] etc.
Der erste Post muss sofort aufmerksamkeitsstark sein.
Der letzte Post enthält einen konkreten Handlungsaufruf.
Trenne Posts mit einer Leerzeile."""

        full_text = self._call_llm(prompt, language)
        posts = self._split_thread(full_text, num_posts)

        return [
            GeneratedContent(
                text=post,
                content_type=ContentType.THREAD,
                language=language,
                platform=platform,
                topic=f"{topic} [{i+1}/{len(posts)}]",
            )
            for i, post in enumerate(posts)
        ]

    def generate_comment_response(
        self,
        original_post: str,
        our_position: str,
        language: str = "de",
        platform: str = "comment",
        tone: str = "sachlich",
    ) -> GeneratedContent:
        """Generiert eine Antwort auf einen konkreten Beitrag."""
        lang_name = SUPPORTED_LANGUAGES.get(language, language)
        limit = FORMAT_LIMITS.get(platform, 1000)

        prompt = f"""Schreibe eine wirksame Antwort auf folgenden Beitrag.

Originalbeitrag:
---
{original_post}
---

Unsere Position: {our_position}
Ton: {tone}
Sprache: {lang_name}
Max. Zeichen: {limit}

Die Antwort soll:
- Direkt auf den Originalbeitrag eingehen
- Falsche Behauptungen sachlich korrigieren
- Unsere Position klar machen
- Keine Beleidigungen enthalten
- Andere Lesende ansprechen, nicht nur den Autor"""

        text = self._call_llm(prompt, language)
        return GeneratedContent(
            text=text,
            content_type=ContentType.COMMENT_RESPONSE,
            language=language,
            platform=platform,
            topic=original_post[:80],
        )

    def translate(self, content: GeneratedContent, target_language: str) -> GeneratedContent:
        """Übersetzt bestehenden Inhalt in eine andere Sprache."""
        lang_name = SUPPORTED_LANGUAGES.get(target_language, target_language)
        limit = FORMAT_LIMITS.get(content.platform)
        limit_hint = f"Maximal {limit} Zeichen." if limit else ""

        prompt = f"""Übersetze folgenden Text ins {lang_name}.
Behalte Ton, politische Aussage und Struktur bei.
{limit_hint}
Passe kulturelle Referenzen an falls nötig.

Text:
{content.text}"""

        translated = self._call_llm(prompt, target_language)
        return GeneratedContent(
            text=translated,
            content_type=content.content_type,
            language=target_language,
            platform=content.platform,
            topic=content.topic,
        )

    def multilingual_campaign(
        self,
        topic: str,
        content_type: ContentType,
        platform: str,
        languages: list[str],
        **kwargs,
    ) -> dict[str, GeneratedContent]:
        """Generiert denselben Inhalt in mehreren Sprachen."""
        results = {}
        base = self.generate(topic, content_type, platform, language=languages[0], **kwargs)
        results[languages[0]] = base

        for lang in languages[1:]:
            results[lang] = self.translate(base, lang)

        return results

    # ------------------------------------------------------------------

    def _build_prompt(self, topic, content_type, platform, lang_name,
                      limit_hint, context, target_audience, campaign_tone,
                      counter_narrative) -> str:

        type_instructions = {
            ContentType.SHORT_POST: "Kurzer, wirkungsvoller Social-Media-Post.",
            ContentType.LONG_FORM: "Ausführlicher Artikel oder Essay.",
            ContentType.PRESS_RELEASE: "Professionelle Pressemitteilung im journalistischen Stil.",
            ContentType.LETTER_TO_EDITOR: "Leserbrief für eine Tageszeitung.",
            ContentType.FLYER: "Flyer-Text mit Titel, Kernbotschaft und Handlungsaufruf.",
            ContentType.NEWSLETTER: "Newsletter-Abschnitt für politische Organisation.",
            ContentType.MEME_TEXT: "Kurzer, einprägsamer Meme-Text (max. 2 Zeilen).",
            ContentType.PETITION_TEXT: "Petitionstext mit Begründung und Forderung.",
            ContentType.PUBLIC_STATEMENT: "Öffentliche Stellungnahme.",
        }

        return f"""Format: {type_instructions.get(content_type, content_type.value)}
Plattform: {platform}
Sprache: {lang_name}
{limit_hint}
Ton: {campaign_tone}

Thema: {topic}
{f"Kontext: {context}" if context else ""}
{f"Zielgruppe: {target_audience}" if target_audience else ""}
{f"Zu widersprechendes Narrativ: {counter_narrative}" if counter_narrative else ""}

Schreibe direkt den fertigen Text, ohne Metakommentare."""

    def _call_llm(self, prompt: str, language: str) -> str:
        try:
            resp = requests.post(
                f"{self.llm_url}/generate",
                json={
                    "prompt": prompt,
                    "system": self.SYSTEM_PROMPT,
                    "temperature": 0.8,
                    "max_tokens": 2048,
                },
                timeout=120,
            )
            resp.raise_for_status()
            return resp.json().get("response", "").strip()
        except requests.exceptions.ConnectionError:
            return f"[FEHLER: ProletariaLLM nicht erreichbar — http://localhost:8001]"
        except Exception as e:
            return f"[FEHLER: {e}]"

    @staticmethod
    def _split_thread(text: str, num_posts: int) -> list[str]:
        """Trennt Thread-Text in einzelne Posts."""
        import re
        parts = re.split(r'\n(?=\[\d+/)', text)
        if len(parts) >= num_posts:
            return [p.strip() for p in parts[:num_posts]]
        # Fallback: gleichmäßig aufteilen
        lines = [l for l in text.split('\n') if l.strip()]
        chunk = max(1, len(lines) // num_posts)
        return ['\n'.join(lines[i:i+chunk]) for i in range(0, len(lines), chunk)][:num_posts]
