"""
Bürgerbeteiligung-Adapter — Öffentliche Konsultationen und Anhörungen.

Generiert strukturierte Stellungnahmen für:
- Stadtentwicklungsportale
- Planfeststellungsverfahren
- Bürgeranhörungen
- Online-Konsultationen (EU, Bund, Länder)
"""
from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from ..base import BaseChannelAdapter, PublishResult
from ...core.content_engine import GeneratedContent


@dataclass
class ConsultationTarget:
    name: str
    url: str
    deadline: str = ""
    format_hint: str = ""


class PublicConsultationAdapter(BaseChannelAdapter):
    """
    Bereitet Stellungnahmen für öffentliche Konsultationen vor.

    Speichert formatierte Stellungnahmen als .txt und .md,
    öffnet Konsultationsportal im Browser.
    """

    channel_name = "public_consultation"

    def __init__(
        self,
        target: ConsultationTarget = None,
        output_dir: str = "stellungnahmen",
    ):
        self.target = target
        self.output_dir = Path(output_dir)

    def _do_publish(self, content: GeneratedContent) -> PublishResult:
        self.output_dir.mkdir(exist_ok=True)

        safe_topic = content.topic[:40].replace("/", "-").replace(" ", "_")
        filename = self.output_dir / f"stellungnahme_{safe_topic}_{content.language}.txt"
        filename.write_text(content.final_text, encoding="utf-8")

        if self.target:
            self._copy_to_clipboard(content.final_text)
            self._open_browser(self.target.url)

        return PublishResult(
            success=True,
            url=self.target.url if self.target else None,
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
