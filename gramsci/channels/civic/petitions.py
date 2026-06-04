"""
Petitions-Adapter — Campact, Change.org, OpenPetition.

Erstellt Petitionstexte und öffnet Plattformen im Browser.
Automatisches Einreichen ist plattformabhängig (APIs oft nicht vorhanden).
"""
from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum

from ..base import BaseChannelAdapter, PublishResult
from ...core.content_engine import GeneratedContent


class PetitionPlatform(str, Enum):
    CAMPACT         = "campact"
    CHANGE_ORG      = "change_org"
    OPEN_PETITION   = "open_petition"
    WEACT           = "weact"


PLATFORM_URLS = {
    PetitionPlatform.CAMPACT:       "https://www.campact.de",
    PetitionPlatform.CHANGE_ORG:    "https://www.change.org",
    PetitionPlatform.OPEN_PETITION: "https://www.openpetition.de",
    PetitionPlatform.WEACT:         "https://weact.campact.de",
}


class PetitionAdapter(BaseChannelAdapter):
    """
    Bereitet Petitionstexte vor und leitet zur Plattform weiter.

    Kein automatisches Einreichen — Nutzer:in kontrolliert das Abschicken.
    """

    channel_name = "petition"

    def __init__(self, platform: PetitionPlatform = PetitionPlatform.CAMPACT):
        self.platform = platform

    def _do_publish(self, content: GeneratedContent) -> PublishResult:
        url = PLATFORM_URLS.get(self.platform, "")
        self._copy_to_clipboard(content.final_text)
        self._open_browser(url)

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
