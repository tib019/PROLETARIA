"""
CampaignManager — Koordiniert mehrkanalige Kampagnen

Verwaltet Kampagnen über mehrere Plattformen und Sprachen hinweg.
Alle Inhalte warten auf menschliche Freigabe vor Veröffentlichung.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional

from .content_engine import ContentEngine, ContentType, GeneratedContent


class CampaignStatus(str, Enum):
    ENTWURF     = "entwurf"
    BEREIT      = "bereit"
    TEILWEISE   = "teilweise_freigegeben"
    ABGESCHLOSSEN = "abgeschlossen"
    ARCHIVIERT  = "archiviert"


@dataclass
class CampaignItem:
    content: GeneratedContent
    channel_adapter: str  # z.B. "mastodon", "twitter", "reddit"
    scheduled_at: Optional[str] = None
    published_at: Optional[str] = None
    publish_url: Optional[str] = None

    @property
    def is_ready(self) -> bool:
        return self.content.approved and self.content.fits_platform()


@dataclass
class Campaign:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    topic: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    status: CampaignStatus = CampaignStatus.ENTWURF
    items: list[CampaignItem] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    notes: str = ""

    @property
    def total_items(self) -> int:
        return len(self.items)

    @property
    def approved_items(self) -> int:
        return sum(1 for i in self.items if i.content.approved)

    @property
    def published_items(self) -> int:
        return sum(1 for i in self.items if i.published_at)

    def update_status(self):
        if not self.items:
            self.status = CampaignStatus.ENTWURF
        elif self.published_items == self.total_items:
            self.status = CampaignStatus.ABGESCHLOSSEN
        elif self.published_items > 0:
            self.status = CampaignStatus.TEILWEISE
        elif self.approved_items > 0:
            self.status = CampaignStatus.BEREIT
        else:
            self.status = CampaignStatus.ENTWURF

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "topic": self.topic,
            "created_at": self.created_at,
            "status": self.status.value,
            "total": self.total_items,
            "approved": self.approved_items,
            "published": self.published_items,
            "tags": self.tags,
            "notes": self.notes,
        }


class CampaignManager:
    """
    Erstellt und verwaltet mehrkanalige Kampagnen.

    Koordiniert ContentEngine, Kanalauswahl und Freigabe-Workflow.
    Persistiert Kampagnen lokal als JSON.
    """

    def __init__(
        self,
        engine: Optional[ContentEngine] = None,
        storage_dir: str = ".gramsci_campaigns",
    ):
        self.engine = engine or ContentEngine()
        self.storage = Path(storage_dir)
        self.storage.mkdir(exist_ok=True)
        self._campaigns: dict[str, Campaign] = {}
        self._load_all()

    # ------------------------------------------------------------------
    # Kampagnen-Erstellung

    def create_campaign(
        self,
        name: str,
        topic: str,
        platforms: list[str],
        languages: list[str] = None,
        content_type: ContentType = ContentType.SHORT_POST,
        tags: list[str] = None,
        **engine_kwargs,
    ) -> Campaign:
        """Erstellt eine neue Kampagne mit Inhalten für alle Plattformen/Sprachen."""
        languages = languages or ["de"]
        campaign = Campaign(name=name, topic=topic, tags=tags or [])

        for platform in platforms:
            for lang in languages:
                content = self.engine.generate(
                    topic=topic,
                    content_type=content_type,
                    platform=platform,
                    language=lang,
                    **engine_kwargs,
                )
                campaign.items.append(CampaignItem(
                    content=content,
                    channel_adapter=platform,
                ))

        self._campaigns[campaign.id] = campaign
        self._save(campaign)
        return campaign

    def create_thread_campaign(
        self,
        name: str,
        topic: str,
        platform: str,
        num_posts: int = 5,
        languages: list[str] = None,
        **kwargs,
    ) -> Campaign:
        """Erstellt Thread-Kampagne für eine oder mehrere Sprachen."""
        languages = languages or ["de"]
        campaign = Campaign(name=name, topic=topic)

        for lang in languages:
            posts = self.engine.generate_thread(
                topic=topic,
                platform=platform,
                num_posts=num_posts,
                language=lang,
                **kwargs,
            )
            for post in posts:
                campaign.items.append(CampaignItem(content=post, channel_adapter=platform))

        self._campaigns[campaign.id] = campaign
        self._save(campaign)
        return campaign

    def create_response_campaign(
        self,
        name: str,
        original_posts: list[str],
        our_position: str,
        platforms: list[str] = None,
        languages: list[str] = None,
    ) -> Campaign:
        """Erstellt Antwort-Kampagne auf eine Liste von Beiträgen."""
        platforms = platforms or ["comment"]
        languages = languages or ["de"]
        campaign = Campaign(name=name, topic=our_position[:80])

        for post in original_posts:
            for lang in languages:
                content = self.engine.generate_comment_response(
                    original_post=post,
                    our_position=our_position,
                    language=lang,
                    platform=platforms[0],
                )
                campaign.items.append(CampaignItem(
                    content=content,
                    channel_adapter=platforms[0],
                ))

        self._campaigns[campaign.id] = campaign
        self._save(campaign)
        return campaign

    # ------------------------------------------------------------------
    # Verwaltung

    def get(self, campaign_id: str) -> Optional[Campaign]:
        return self._campaigns.get(campaign_id)

    def list_campaigns(self, status: Optional[CampaignStatus] = None) -> list[Campaign]:
        campaigns = list(self._campaigns.values())
        if status:
            campaigns = [c for c in campaigns if c.status == status]
        return sorted(campaigns, key=lambda c: c.created_at, reverse=True)

    def approve_item(self, campaign_id: str, item_index: int, edited_text: str = "") -> bool:
        campaign = self._campaigns.get(campaign_id)
        if not campaign or item_index >= len(campaign.items):
            return False
        item = campaign.items[item_index]
        item.content.approved = True
        if edited_text:
            item.content.edited_text = edited_text
        campaign.update_status()
        self._save(campaign)
        return True

    def approve_all(self, campaign_id: str) -> int:
        campaign = self._campaigns.get(campaign_id)
        if not campaign:
            return 0
        count = 0
        for item in campaign.items:
            if not item.content.approved:
                item.content.approved = True
                count += 1
        campaign.update_status()
        self._save(campaign)
        return count

    def mark_published(self, campaign_id: str, item_index: int, url: str = "") -> bool:
        campaign = self._campaigns.get(campaign_id)
        if not campaign or item_index >= len(campaign.items):
            return False
        item = campaign.items[item_index]
        item.published_at = datetime.now().isoformat()
        item.publish_url = url
        campaign.update_status()
        self._save(campaign)
        return True

    def get_ready_items(self, campaign_id: str) -> list[tuple[int, CampaignItem]]:
        """Gibt alle freigegebenen, noch nicht veröffentlichten Items zurück."""
        campaign = self._campaigns.get(campaign_id)
        if not campaign:
            return []
        return [
            (i, item)
            for i, item in enumerate(campaign.items)
            if item.is_ready and not item.published_at
        ]

    def delete_campaign(self, campaign_id: str) -> bool:
        if campaign_id not in self._campaigns:
            return False
        path = self.storage / f"{campaign_id}.json"
        path.unlink(missing_ok=True)
        del self._campaigns[campaign_id]
        return True

    # ------------------------------------------------------------------

    def _save(self, campaign: Campaign):
        path = self.storage / f"{campaign.id}.json"
        data = campaign.to_dict()
        data["_items"] = [
            {
                "text": item.content.final_text,
                "content_type": item.content.content_type.value,
                "language": item.content.language,
                "platform": item.content.platform,
                "topic": item.content.topic,
                "approved": item.content.approved,
                "channel_adapter": item.channel_adapter,
                "published_at": item.published_at,
                "publish_url": item.publish_url,
            }
            for item in campaign.items
        ]
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    def _load_all(self):
        for path in self.storage.glob("*.json"):
            try:
                data = json.loads(path.read_text())
                campaign = Campaign(
                    id=data["id"],
                    name=data["name"],
                    topic=data["topic"],
                    created_at=data["created_at"],
                    status=CampaignStatus(data["status"]),
                    tags=data.get("tags", []),
                    notes=data.get("notes", ""),
                )
                from .content_engine import GeneratedContent, ContentType
                for item_data in data.get("_items", []):
                    content = GeneratedContent(
                        text=item_data["text"],
                        content_type=ContentType(item_data["content_type"]),
                        language=item_data["language"],
                        platform=item_data["platform"],
                        topic=item_data["topic"],
                    )
                    content.approved = item_data.get("approved", False)
                    campaign.items.append(CampaignItem(
                        content=content,
                        channel_adapter=item_data["channel_adapter"],
                        published_at=item_data.get("published_at"),
                        publish_url=item_data.get("publish_url"),
                    ))
                self._campaigns[campaign.id] = campaign
            except Exception:
                pass
