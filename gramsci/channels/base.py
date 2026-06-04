"""
Abstrakte Basis für alle Kanal-Adapter.

Jeder Kanal implementiert publish() und validate().
Kein Adapter veröffentlicht ohne approved=True.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from ..core.content_engine import GeneratedContent


@dataclass
class PublishResult:
    success: bool
    url: Optional[str] = None
    post_id: Optional[str] = None
    error: Optional[str] = None
    channel: str = ""

    def __str__(self) -> str:
        if self.success:
            return f"[{self.channel}] Veröffentlicht: {self.url or self.post_id}"
        return f"[{self.channel}] FEHLER: {self.error}"


class BaseChannelAdapter(ABC):
    """
    Abstrakte Basis für alle Kanal-Adapter.

    Unterklassen implementieren _do_publish().
    publish() prüft approved-Flag bevor es delegiert.
    """

    channel_name: str = "unknown"

    def publish(self, content: GeneratedContent) -> PublishResult:
        if not content.approved:
            return PublishResult(
                success=False,
                error="Inhalt nicht freigegeben (approved=False). Bitte erst im ReviewCLI freigeben.",
                channel=self.channel_name,
            )
        if not content.fits_platform():
            return PublishResult(
                success=False,
                error=f"Text überschreitet Zeichenlimit für {content.platform}.",
                channel=self.channel_name,
            )
        return self._do_publish(content)

    @abstractmethod
    def _do_publish(self, content: GeneratedContent) -> PublishResult:
        """Implementiert die eigentliche Veröffentlichung."""

    def validate_credentials(self) -> bool:
        """Prüft ob alle benötigten Credentials vorhanden sind."""
        return True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(channel={self.channel_name})"
