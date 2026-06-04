"""Mastodon-Adapter — Fediversum, dezentral, kein Algorithmus."""
from __future__ import annotations

import os
import requests

from ..base import BaseChannelAdapter, PublishResult
from ...core.content_engine import GeneratedContent


class MastodonAdapter(BaseChannelAdapter):
    """
    Veröffentlicht auf Mastodon-Instanz via API.

    Env-Variablen: MASTODON_INSTANCE_URL, MASTODON_ACCESS_TOKEN
    """

    channel_name = "mastodon"

    def __init__(
        self,
        instance_url: str = "",
        access_token: str = "",
        visibility: str = "public",
    ):
        self.instance_url = instance_url or os.getenv("MASTODON_INSTANCE_URL", "")
        self.access_token = access_token or os.getenv("MASTODON_ACCESS_TOKEN", "")
        self.visibility = visibility

    def validate_credentials(self) -> bool:
        return bool(self.instance_url and self.access_token)

    def _do_publish(self, content: GeneratedContent) -> PublishResult:
        if not self.validate_credentials():
            return PublishResult(
                success=False,
                error="MASTODON_INSTANCE_URL und MASTODON_ACCESS_TOKEN fehlen.",
                channel=self.channel_name,
            )

        try:
            resp = requests.post(
                f"{self.instance_url}/api/v1/statuses",
                headers={"Authorization": f"Bearer {self.access_token}"},
                json={
                    "status": content.final_text,
                    "visibility": self.visibility,
                    "language": content.language,
                },
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            return PublishResult(
                success=True,
                url=data.get("url"),
                post_id=data.get("id"),
                channel=self.channel_name,
            )
        except requests.exceptions.HTTPError as e:
            return PublishResult(success=False, error=str(e), channel=self.channel_name)
        except Exception as e:
            return PublishResult(success=False, error=str(e), channel=self.channel_name)
