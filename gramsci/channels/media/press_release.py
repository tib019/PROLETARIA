"""
Pressemitteilung-Adapter — E-Mail an Redaktionen + Datei-Export.

Versendet Pressemitteilungen an konfigurierte Redaktionsverteiler
oder exportiert als formatierte .txt/.md-Datei.
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
class PressContact:
    name: str
    email: str
    outlet: str = ""
    beat: str = ""  # Ressort


class PressReleaseAdapter(BaseChannelAdapter):
    """
    Versendet Pressemitteilungen per E-Mail an Redaktionen.

    Env-Variablen: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD,
                   PRESS_SENDER_NAME, PRESS_SENDER_EMAIL
    """

    channel_name = "press_release"

    def __init__(
        self,
        contacts: list[PressContact] = None,
        output_dir: str = "pressemitteilungen",
        smtp_host: str = "",
        smtp_port: int = 587,
        smtp_user: str = "",
        smtp_password: str = "",
        sender_name: str = "",
        sender_email: str = "",
    ):
        self.contacts = contacts or []
        self.output_dir = Path(output_dir)
        self.smtp_host = smtp_host or os.getenv("SMTP_HOST", "")
        self.smtp_port = smtp_port or int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = smtp_user or os.getenv("SMTP_USER", "")
        self.smtp_password = smtp_password or os.getenv("SMTP_PASSWORD", "")
        self.sender_name = sender_name or os.getenv("PRESS_SENDER_NAME", "")
        self.sender_email = sender_email or os.getenv("PRESS_SENDER_EMAIL", "")

    def _do_publish(self, content: GeneratedContent) -> PublishResult:
        self.output_dir.mkdir(exist_ok=True)
        safe_topic = content.topic[:40].replace("/", "-").replace(" ", "_")
        filepath = self.output_dir / f"pm_{safe_topic}_{content.language}.txt"
        filepath.write_text(content.final_text, encoding="utf-8")

        if self.contacts and self.smtp_host and self.sender_email:
            errors = self._send_emails(content)
            if errors:
                return PublishResult(
                    success=False,
                    error=f"E-Mail-Fehler: {'; '.join(errors)}",
                    channel=self.channel_name,
                )
            return PublishResult(
                success=True,
                url=str(filepath),
                channel=self.channel_name,
            )

        return PublishResult(
            success=True,
            url=str(filepath),
            channel=self.channel_name,
        )

    def _send_emails(self, content: GeneratedContent) -> list[str]:
        errors = []
        subject = content.topic[:100]
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                for contact in self.contacts:
                    msg = MIMEMultipart()
                    msg["From"] = f"{self.sender_name} <{self.sender_email}>"
                    msg["To"] = contact.email
                    msg["Subject"] = f"Pressemitteilung: {subject}"
                    msg.attach(MIMEText(content.final_text, "plain", "utf-8"))
                    try:
                        server.send_message(msg)
                    except Exception as e:
                        errors.append(f"{contact.email}: {e}")
        except Exception as e:
            errors.append(str(e))
        return errors
