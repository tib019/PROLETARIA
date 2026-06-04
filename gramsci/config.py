"""
Gramsci-Konfiguration — Credentials und Einstellungen.

Lädt aus .env oder Umgebungsvariablen.
Niemals Credentials in Code committen.
"""
from __future__ import annotations

import os
from pathlib import Path


def load_env(env_file: str = ".env"):
    """Lädt .env-Datei falls vorhanden."""
    path = Path(env_file)
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def get_channel_credentials() -> dict:
    """Gibt alle konfigurierten Kanal-Credentials zurück (ohne Secrets zu loggen)."""
    configured = []
    checks = {
        "mastodon":  ["MASTODON_INSTANCE_URL", "MASTODON_ACCESS_TOKEN"],
        "twitter":   ["TWITTER_API_KEY", "TWITTER_ACCESS_TOKEN"],
        "reddit":    ["REDDIT_CLIENT_ID", "REDDIT_USERNAME"],
        "telegram":  ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"],
        "facebook":  ["FACEBOOK_PAGE_ID", "FACEBOOK_PAGE_ACCESS_TOKEN"],
        "instagram": ["INSTAGRAM_ACCOUNT_ID", "INSTAGRAM_ACCESS_TOKEN"],
        "tiktok":    ["TIKTOK_ACCESS_TOKEN"],
        "youtube":   ["YOUTUBE_OAUTH_TOKEN"],
        "smtp":      ["SMTP_HOST", "SMTP_USER"],
    }
    for channel, keys in checks.items():
        if all(os.getenv(k) for k in keys):
            configured.append(channel)
    return {"configured_channels": configured}


LLM_SERVER      = os.getenv("LLM_SERVER_URL", "http://localhost:8001")
ORG_NAME        = os.getenv("GRAMSCI_ORG_NAME", "")
DEFAULT_LANGUAGE = os.getenv("GRAMSCI_DEFAULT_LANGUAGE", "de")
CAMPAIGN_DIR    = os.getenv("GRAMSCI_CAMPAIGN_DIR", ".gramsci_campaigns")
OUTPUT_DIR      = os.getenv("GRAMSCI_OUTPUT_DIR", "gramsci_output")
