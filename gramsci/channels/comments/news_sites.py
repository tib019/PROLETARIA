"""
NewsSite-Adapter — Clipboard-basiert für manuelle Kommentareingabe.

Die meisten Nachrichtenseiten haben keine öffentliche Kommentar-API.
Dieser Adapter stellt den Text bereit und öffnet die Ziel-URL im Browser.
"""
from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from typing import Optional

from ..base import BaseChannelAdapter, PublishResult
from ...core.content_engine import GeneratedContent


@dataclass
class NewsSiteTarget:
    name: str
    url: str
    comment_section_hint: str = ""


KNOWN_SITES: list[NewsSiteTarget] = [
    NewsSiteTarget("Spiegel Online", "https://www.spiegel.de", "Kommentare am Ende des Artikels"),
    NewsSiteTarget("taz", "https://www.taz.de", "Kommentarfeld unter dem Artikel"),
    NewsSiteTarget("Zeit Online", "https://www.zeit.de", "Kommentar-Button 'Diskutieren'"),
    NewsSiteTarget("Heise Online", "https://www.heise.de", "Forum-Tab unter dem Artikel"),
]


class NewsSiteCommentAdapter(BaseChannelAdapter):
    """
    Clipboard-basierter Adapter für Kommentare auf Nachrichtenseiten.

    Kopiert Text in Zwischenablage und kann Artikel-URL im Browser öffnen.
    Kein automatisches Posting (kein API) — Knopfdruck bleibt beim Menschen.
    """

    channel_name = "news_comment"

    def __init__(self, article_url: str = "", site_name: str = ""):
        self.article_url = article_url
        self.site_name = site_name

    def _do_publish(self, content: GeneratedContent) -> PublishResult:
        text = content.final_text
        copied = self._copy_to_clipboard(text)
        opened = self._open_browser(self.article_url) if self.article_url else False

        msg = "Text in Zwischenablage"
        if opened:
            msg += f" + Browser geöffnet: {self.article_url}"
        if not copied:
            msg = f"Manuell kopieren:\n\n{text}"

        return PublishResult(
            success=True,
            url=self.article_url or None,
            error=None if copied else "Zwischenablage nicht verfügbar",
            channel=self.channel_name,
        )

    def _copy_to_clipboard(self, text: str) -> bool:
        try:
            if sys.platform == "darwin":
                subprocess.run(["pbcopy"], input=text.encode(), check=True)
            elif sys.platform == "win32":
                subprocess.run(["clip"], input=text.encode(), check=True)
            else:
                subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode(), check=True)
            return True
        except Exception:
            try:
                subprocess.run(["xsel", "--clipboard", "--input"], input=text.encode(), check=True)
                return True
            except Exception:
                return False

    def _open_browser(self, url: str) -> bool:
        try:
            import webbrowser
            webbrowser.open(url)
            return True
        except Exception:
            return False
