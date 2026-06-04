"""Instagram-Adapter — Business Accounts via Meta Graph API."""
from __future__ import annotations

import os
import requests

from ..base import BaseChannelAdapter, PublishResult
from ...core.content_engine import GeneratedContent


class InstagramAdapter(BaseChannelAdapter):
    """
    Veröffentlicht auf Instagram Business via Graph API.

    Hinweis: Instagram erlaubt nur Posts mit Medien (Bild/Video).
    Reels/Carousels erfordern separate Media-Upload-Pipeline.
    Für reine Textposts wird ein Platzhalter-Bild benötigt.

    Env-Variablen: INSTAGRAM_ACCOUNT_ID, INSTAGRAM_ACCESS_TOKEN
    """

    channel_name = "instagram"
    GRAPH_API = "https://graph.facebook.com/v19.0"

    def __init__(
        self,
        account_id: str = "",
        access_token: str = "",
        default_image_url: str = "",
    ):
        self.account_id = account_id or os.getenv("INSTAGRAM_ACCOUNT_ID", "")
        self.access_token = access_token or os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
        self.default_image_url = default_image_url or os.getenv("INSTAGRAM_DEFAULT_IMAGE_URL", "")

    def validate_credentials(self) -> bool:
        return bool(self.account_id and self.access_token)

    def _do_publish(self, content: GeneratedContent) -> PublishResult:
        if not self.validate_credentials():
            return PublishResult(
                success=False,
                error="INSTAGRAM_ACCOUNT_ID und INSTAGRAM_ACCESS_TOKEN fehlen.",
                channel=self.channel_name,
            )
        if not self.default_image_url:
            return PublishResult(
                success=False,
                error="Instagram benötigt ein Bild (INSTAGRAM_DEFAULT_IMAGE_URL). Reine Textposts nicht möglich.",
                channel=self.channel_name,
            )

        try:
            # Schritt 1: Media-Container erstellen
            container_resp = requests.post(
                f"{self.GRAPH_API}/{self.account_id}/media",
                data={
                    "image_url": self.default_image_url,
                    "caption": content.final_text,
                    "access_token": self.access_token,
                },
                timeout=30,
            )
            container_resp.raise_for_status()
            container_id = container_resp.json().get("id")

            # Schritt 2: Container veröffentlichen
            publish_resp = requests.post(
                f"{self.GRAPH_API}/{self.account_id}/media_publish",
                data={
                    "creation_id": container_id,
                    "access_token": self.access_token,
                },
                timeout=30,
            )
            publish_resp.raise_for_status()
            post_id = publish_resp.json().get("id", "")
            return PublishResult(
                success=True,
                post_id=post_id,
                channel=self.channel_name,
            )
        except Exception as e:
            return PublishResult(success=False, error=str(e), channel=self.channel_name)
