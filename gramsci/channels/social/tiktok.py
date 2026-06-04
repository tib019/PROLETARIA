"""TikTok-Adapter — Text-Posts via Content Posting API."""
from __future__ import annotations

import os
import requests

from ..base import BaseChannelAdapter, PublishResult
from ...core.content_engine import GeneratedContent


class TikTokAdapter(BaseChannelAdapter):
    """
    Veröffentlicht Text-Posts auf TikTok via Content Posting API.

    Hinweis: TikTok unterstützt seit 2024 reine Textposts.
    Video-Posts erfordern separate Video-Upload-Pipeline.

    Env-Variablen: TIKTOK_ACCESS_TOKEN, TIKTOK_OPEN_ID
    """

    channel_name = "tiktok"
    API_BASE = "https://open.tiktokapis.com/v2"

    def __init__(
        self,
        access_token: str = "",
        open_id: str = "",
    ):
        self.access_token = access_token or os.getenv("TIKTOK_ACCESS_TOKEN", "")
        self.open_id = open_id or os.getenv("TIKTOK_OPEN_ID", "")

    def validate_credentials(self) -> bool:
        return bool(self.access_token)

    def _do_publish(self, content: GeneratedContent) -> PublishResult:
        if not self.validate_credentials():
            return PublishResult(
                success=False,
                error="TIKTOK_ACCESS_TOKEN fehlt.",
                channel=self.channel_name,
            )

        try:
            resp = requests.post(
                f"{self.API_BASE}/post/publish/text/",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json; charset=UTF-8",
                },
                json={
                    "post_info": {
                        "title": content.final_text[:150],
                        "privacy_level": "PUBLIC_TO_EVERYONE",
                        "disable_comment": False,
                    },
                    "source_info": {
                        "source": "PULL_FROM_URL",
                    },
                },
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            post_id = data.get("data", {}).get("publish_id", "")
            return PublishResult(
                success=True,
                post_id=post_id,
                channel=self.channel_name,
            )
        except Exception as e:
            return PublishResult(success=False, error=str(e), channel=self.channel_name)
