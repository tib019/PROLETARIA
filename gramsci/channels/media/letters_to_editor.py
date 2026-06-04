"""
Leserbrief-Adapter — Formatierung und Export für Tageszeitungen.

Erstellt formatierte Leserbriefe und öffnet Einreichungsseiten.
"""
from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from ..base import BaseChannelAdapter, PublishResult
from ...core.content_engine import GeneratedContent


@dataclass
class NewspaperTarget:
    name: str
    submission_url: str = ""
    submission_email: str = ""
    max_chars: int = 2000
    region: str = ""


GERMAN_NEWSPAPERS: list[NewspaperTarget] = [
    NewspaperTarget("taz", "https://www.taz.de/!p4608/", max_chars=1500, region="national"),
    NewspaperTarget("Neues Deutschland", "https://www.nd-aktuell.de/service/leserbrief.html", max_chars=2000, region="national"),
    NewspaperTable := None,
]
GERMAN_NEWSPAPERS = [n for n in GERMAN_NEWSPAPERS if n is not None]


class LetterToEditorAdapter(BaseChannelAdapter):
    """
    Exportiert Leserbriefe als formatierte Textdatei und öffnet Einreichungsseite.
    """

    channel_name = "letter_to_editor"

    def __init__(
        self,
        target: NewspaperTarget = None,
        output_dir: str = "leserbriefe",
    ):
        self.target = target
        self.output_dir = Path(output_dir)

    def _do_publish(self, content: GeneratedContent) -> PublishResult:
        self.output_dir.mkdir(exist_ok=True)
        safe_topic = content.topic[:40].replace("/", "-").replace(" ", "_")
        outlet = self.target.name.replace(" ", "_") if self.target else "leserbrief"
        filepath = self.output_dir / f"{outlet}_{safe_topic}_{content.language}.txt"

        text = content.final_text
        if self.target and len(text) > self.target.max_chars:
            text = text[:self.target.max_chars]

        filepath.write_text(text, encoding="utf-8")
        self._copy_to_clipboard(text)

        url = None
        if self.target:
            url = self.target.submission_url or self.target.submission_email
            if self.target.submission_url:
                self._open_browser(self.target.submission_url)

        return PublishResult(
            success=True,
            url=url,
            channel=self.channel_name,
        )

    def _copy_to_clipboard(self, text: str):
        try:
            if sys.platform == "darwin":
                subprocess.run(["pbcopy"], input=text.encode(), check=True)
            elif sys.platform == "win32":
                subprocess.run(["clip"], input=text.encode(), check=True)
            else:
                subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode(), check=True)
        except Exception:
            pass

    def _open_browser(self, url: str):
        try:
            import webbrowser
            webbrowser.open(url)
        except Exception:
            pass
