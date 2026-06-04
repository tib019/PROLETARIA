"""
Flyer-Generator — Exportiert Flyer-Texte als .txt und optional als HTML.

Für Druckprodukte: DIN A5/A4 einseitig, zweiseitig, Trifold.
Kein PDF-Export ohne reportlab/weasyprint (optionale Dependencies).
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from ..base import BaseChannelAdapter, PublishResult
from ...core.content_engine import GeneratedContent


class FlyerFormat(str, Enum):
    A5_EINSEITIG    = "a5_einseitig"
    A4_EINSEITIG    = "a4_einseitig"
    A4_ZWEISEITIG   = "a4_zweiseitig"
    TRIFOLD         = "trifold"
    DL_KARTE        = "dl_karte"


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<title>{topic}</title>
<style>
  body {{ font-family: 'Liberation Sans', Arial, sans-serif; margin: 2cm; font-size: 11pt; line-height: 1.5; }}
  h1 {{ font-size: 18pt; margin-bottom: 0.5cm; }}
  .content {{ white-space: pre-wrap; }}
  .footer {{ margin-top: 1cm; font-size: 9pt; color: #555; border-top: 1px solid #ccc; padding-top: 0.3cm; }}
</style>
</head>
<body>
<h1>{topic}</h1>
<div class="content">{text}</div>
<div class="footer">{footer}</div>
</body>
</html>"""


class FlyerGeneratorAdapter(BaseChannelAdapter):
    """
    Exportiert Flyer-Inhalte als .txt und optionales HTML für Druckvorbereitung.
    """

    channel_name = "flyer"

    def __init__(
        self,
        output_dir: str = "flyer",
        flyer_format: FlyerFormat = FlyerFormat.A5_EINSEITIG,
        organization_name: str = "",
        footer_text: str = "",
        generate_html: bool = True,
    ):
        self.output_dir = Path(output_dir)
        self.flyer_format = flyer_format
        self.organization_name = organization_name or os.getenv("GRAMSCI_ORG_NAME", "")
        self.footer_text = footer_text
        self.generate_html = generate_html

    def _do_publish(self, content: GeneratedContent) -> PublishResult:
        self.output_dir.mkdir(exist_ok=True)
        safe_topic = content.topic[:40].replace("/", "-").replace(" ", "_")
        base_name = f"flyer_{safe_topic}_{content.language}"

        txt_path = self.output_dir / f"{base_name}.txt"
        txt_path.write_text(content.final_text, encoding="utf-8")

        html_path = None
        if self.generate_html:
            footer = self.footer_text or self.organization_name or ""
            html = HTML_TEMPLATE.format(
                lang=content.language,
                topic=content.topic,
                text=content.final_text.replace("<", "&lt;").replace(">", "&gt;"),
                footer=footer,
            )
            html_path = self.output_dir / f"{base_name}.html"
            html_path.write_text(html, encoding="utf-8")

        return PublishResult(
            success=True,
            url=str(html_path or txt_path),
            channel=self.channel_name,
        )
