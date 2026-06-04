"""Facebook-Adapter — Pages via Graph API. Nur Organisationsseiten, keine Profile."""
from __future__ import annotations

import os
import requests

from ..base import BaseChannelAdapter, PublishResult
from ...core.content_engine import GeneratedContent


class FacebookAdapter(BaseChannelAdapter):
    """
    Veröffentlicht auf Facebook Pages via Graph API.

    Env-Variablen: FACEBOOK_PAGE_ID, FACEBOOK_PAGE_ACCESS_TOKEN
    Hinweis: Erfordert Page Access Token (nicht User Token).
    """

    channel_name = "facebook"
    GRAPH_API = "https://graph.facebook.com/v19.0"

    def __init__(
        self,
        page_id: str = "",
        page_access_token: str = "",
    ):
        self.page_id = page_id or os.getenv("FACEBOOK_PAGE_ID", "")
        self.page_access_token = page_access_token or os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "")

    def validate_credentials(self) -> bool:
        return bool(self.page_id and self.page_access_token)

    def _do_publish(self, content: GeneratedContent) -> PublishResult:
        if not self.validate_credentials():
            return PublishResult(
                success=False,
                error="FACEBOOK_PAGE_ID und FACEBOOK_PAGE_ACCESS_TOKEN fehlen.",
                channel=self.channel_name,
            )

        try:
            resp = requests.post(
                f"{self.GRAPH_API}/{self.page_id}/feed",
                data={
                    "message": content.final_text,
                    "access_token": self.page_access_token,
                },
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            post_id = data.get("id", "")
            return PublishResult(
                success=True,
                post_id=post_id,
                url=f"https://facebook.com/{post_id}" if post_id else None,
                channel=self.channel_name,
            )
        except Exception as e:
            return PublishResult(success=False, error=str(e), channel=self.channel_name)
