"""Twitter/X-Adapter — 280 Zeichen, API v2."""
from __future__ import annotations

import os
import requests
from requests_oauthlib import OAuth1

from ..base import BaseChannelAdapter, PublishResult
from ...core.content_engine import GeneratedContent


class TwitterAdapter(BaseChannelAdapter):
    """
    Veröffentlicht Tweets via Twitter API v2.

    Env-Variablen: TWITTER_API_KEY, TWITTER_API_SECRET,
                   TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    """

    channel_name = "twitter"
    API_URL = "https://api.twitter.com/2/tweets"

    def __init__(
        self,
        api_key: str = "",
        api_secret: str = "",
        access_token: str = "",
        access_token_secret: str = "",
    ):
        self.api_key = api_key or os.getenv("TWITTER_API_KEY", "")
        self.api_secret = api_secret or os.getenv("TWITTER_API_SECRET", "")
        self.access_token = access_token or os.getenv("TWITTER_ACCESS_TOKEN", "")
        self.access_token_secret = access_token_secret or os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")

    def validate_credentials(self) -> bool:
        return all([self.api_key, self.api_secret, self.access_token, self.access_token_secret])

    def _do_publish(self, content: GeneratedContent) -> PublishResult:
        if not self.validate_credentials():
            return PublishResult(
                success=False,
                error="Twitter-Credentials fehlen (TWITTER_API_KEY, _SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET).",
                channel=self.channel_name,
            )

        auth = OAuth1(self.api_key, self.api_secret, self.access_token, self.access_token_secret)

        try:
            resp = requests.post(
                self.API_URL,
                auth=auth,
                json={"text": content.final_text},
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            tweet_id = data.get("data", {}).get("id", "")
            return PublishResult(
                success=True,
                post_id=tweet_id,
                url=f"https://twitter.com/i/web/status/{tweet_id}" if tweet_id else None,
                channel=self.channel_name,
            )
        except Exception as e:
            return PublishResult(success=False, error=str(e), channel=self.channel_name)
