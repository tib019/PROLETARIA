"""Telegram-Adapter — Kanal- und Gruppen-Posts via Bot API."""
from __future__ import annotations

import os
import requests

from ..base import BaseChannelAdapter, PublishResult
from ...core.content_engine import GeneratedContent


class TelegramAdapter(BaseChannelAdapter):
    """
    Sendet Nachrichten in Telegram-Kanäle oder -Gruppen via Bot API.

    Env-Variablen: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
    """

    channel_name = "telegram"
    API_BASE = "https://api.telegram.org/bot{token}"

    def __init__(
        self,
        bot_token: str = "",
        chat_id: str = "",
        parse_mode: str = "HTML",
    ):
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID", "")
        self.parse_mode = parse_mode

    def validate_credentials(self) -> bool:
        return bool(self.bot_token and self.chat_id)

    def _do_publish(self, content: GeneratedContent) -> PublishResult:
        if not self.validate_credentials():
            return PublishResult(
                success=False,
                error="TELEGRAM_BOT_TOKEN und TELEGRAM_CHAT_ID fehlen.",
                channel=self.channel_name,
            )

        try:
            api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            resp = requests.post(
                api_url,
                json={
                    "chat_id": self.chat_id,
                    "text": content.final_text,
                    "parse_mode": self.parse_mode,
                },
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            msg_id = str(data.get("result", {}).get("message_id", ""))
            return PublishResult(
                success=True,
                post_id=msg_id,
                channel=self.channel_name,
            )
        except Exception as e:
            return PublishResult(success=False, error=str(e), channel=self.channel_name)
