"""
Newsletter-Adapter — E-Mail-Versand und Markdown-Export.

Unterstützt direkten SMTP-Versand oder Export als .md/.html
für Integration in bestehende Newsletter-Tools (Listmonk, Mailchimp-Import).
"""
from __future__ import annotations

import os
import smtplib
from dataclasses import dataclass, field
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from ..base import BaseChannelAdapter, PublishResult
from ...core.content_engine import GeneratedContent


@dataclass
class NewsletterConfig:
    subject_prefix: str = "[Newsletter]"
    sender_name: str = ""
    sender_email: str = ""
    reply_to: str = ""
    subscribers: list[str] = field(default_factory=list)
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""


class NewsletterAdapter(BaseChannelAdapter):
    """
    Versendet Newsletter via SMTP oder exportiert als Markdown/HTML.

    Env-Variablen: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD,
                   NEWSLETTER_SENDER_NAME, NEWSLETTER_SENDER_EMAIL
    """

    channel_name = "newsletter"

    def __init__(
        self,
        config: NewsletterConfig = None,
        output_dir: str = "newsletter",
    ):
        self.config = config or NewsletterConfig(
            smtp_host=os.getenv("SMTP_HOST", ""),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            smtp_user=os.getenv("SMTP_USER", ""),
            smtp_password=os.getenv("SMTP_PASSWORD", ""),
            sender_name=os.getenv("NEWSLETTER_SENDER_NAME", ""),
            sender_email=os.getenv("NEWSLETTER_SENDER_EMAIL", ""),
        )
        self.output_dir = Path(output_dir)

    def _do_publish(self, content: GeneratedContent) -> PublishResult:
        self.output_dir.mkdir(exist_ok=True)
        safe_topic = content.topic[:40].replace("/", "-").replace(" ", "_")
        md_path = self.output_dir / f"newsletter_{safe_topic}_{content.language}.md"
        md_path.write_text(f"# {content.topic}\n\n{content.final_text}", encoding="utf-8")

        if self.config.subscribers and self.config.smtp_host and self.config.sender_email:
            errors = self._send_bulk(content)
            if errors:
                return PublishResult(
                    success=False,
                    error=f"{len(errors)} Fehler beim Versand",
                    channel=self.channel_name,
                )
            return PublishResult(
                success=True,
                url=str(md_path),
                channel=self.channel_name,
            )

        return PublishResult(
            success=True,
            url=str(md_path),
            channel=self.channel_name,
        )

    def _send_bulk(self, content: GeneratedContent) -> list[str]:
        errors = []
        subject = f"{self.config.subject_prefix} {content.topic}"
        try:
            with smtplib.SMTP(self.config.smtp_host, self.config.smtp_port) as server:
                server.starttls()
                server.login(self.config.smtp_user, self.config.smtp_password)
                for email in self.config.subscribers:
                    msg = MIMEMultipart("alternative")
                    msg["From"] = f"{self.config.sender_name} <{self.config.sender_email}>"
                    msg["To"] = email
                    msg["Subject"] = subject
                    if self.config.reply_to:
                        msg["Reply-To"] = self.config.reply_to
                    msg.attach(MIMEText(content.final_text, "plain", "utf-8"))
                    try:
                        server.send_message(msg)
                    except Exception as e:
                        errors.append(str(e))
        except Exception as e:
            errors.append(str(e))
        return errors
