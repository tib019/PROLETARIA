"""
Gramsci — Kulturelle Hegemoniearbeit auf allen Ebenen

Benannt nach Antonio Gramsci (1891-1937): Theorie der kulturellen Hegemonie —
Dominanz wird nicht nur durch Zwang, sondern durch Konsens in Zivilgesellschaft,
Kultur und Alltagsdiskurs gesichert. Gegenhegemonie bricht diesen Konsens.

Dieses Modul unterstützt Menschen dabei, auf allen öffentlichen Arenen
wirksam zu kommunizieren. Alle Inhalte werden von Menschen freigegeben
bevor sie veröffentlicht werden (Knopfdruck-Prinzip).

Sprachen: DE (primär), EN, FR, NL, ES, IT, PL
Brain: ProletariaLLM via llm-server
"""
from .core.content_engine import ContentEngine, ContentType, GeneratedContent
from .core.campaign_manager import CampaignManager, Campaign
from .core.narrative_radar import NarrativeRadar
from .core.hegemony_analyzer import HegemonieAnalyzer
from .ui.review_cli import ReviewCLI
from .ui.dashboard import Dashboard
from .config import load_env, get_channel_credentials, LLM_SERVER

__version__ = "0.1.0"
__all__ = [
    "ContentEngine", "ContentType", "GeneratedContent",
    "CampaignManager", "Campaign",
    "NarrativeRadar",
    "HegemonieAnalyzer",
    "ReviewCLI", "Dashboard",
    "load_env", "get_channel_credentials", "LLM_SERVER",
]
