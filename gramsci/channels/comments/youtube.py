"""YouTube-Adapter — Kommentare via Data API v3."""
from __future__ import annotations

import os
import requests

from ..base import BaseChannelAdapter, PublishResult
from ...core.content_engine import GeneratedContent


class YouTubeCommentAdapter(BaseChannelAdapter):
    """
    Postet Kommentare auf YouTube-Videos via Data API v3.

    Env-Variablen: YOUTUBE_API_KEY, YOUTUBE_OAUTH_TOKEN
    Hinweis: Kommentare erfordern OAuth 2.0 (kein API-Key allein).
    """

    channel_name = "youtube_comment"
    API_BASE = "https://www.googleapis.com/youtube/v3"

    def __init__(self, oauth_token: str = "", video_id: str = ""):
        self.oauth_token = oauth_token or os.getenv("YOUTUBE_OAUTH_TOKEN", "")
        self.default_video_id = video_id or os.getenv("YOUTUBE_DEFAULT_VIDEO_ID", "")

    def validate_credentials(self) -> bool:
        return bool(self.oauth_token)

    def _do_publish(self, content: GeneratedContent) -> PublishResult:
        if not self.validate_credentials():
            return PublishResult(
                success=False,
                error="YOUTUBE_OAUTH_TOKEN fehlt.",
                channel=self.channel_name,
            )

        video_id = self.default_video_id
        if not video_id:
            return PublishResult(
                success=False,
                error="Kein Video-ID angegeben (YOUTUBE_DEFAULT_VIDEO_ID).",
                channel=self.channel_name,
            )

        try:
            resp = requests.post(
                f"{self.API_BASE}/commentThreads?part=snippet",
                headers={"Authorization": f"Bearer {self.oauth_token}"},
                json={
                    "snippet": {
                        "videoId": video_id,
                        "topLevelComment": {
                            "snippet": {"textOriginal": content.final_text}
                        },
                    }
                },
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            comment_id = data.get("id", "")
            return PublishResult(
                success=True,
                post_id=comment_id,
                url=f"https://youtube.com/watch?v={video_id}&lc={comment_id}",
                channel=self.channel_name,
            )
        except Exception as e:
            return PublishResult(success=False, error=str(e), channel=self.channel_name)
