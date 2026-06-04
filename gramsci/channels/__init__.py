from .base import BaseChannelAdapter, PublishResult
from .social import (
    MastodonAdapter, TwitterAdapter, RedditAdapter, TelegramAdapter,
    FacebookAdapter, InstagramAdapter, TikTokAdapter,
)
from .comments import YouTubeCommentAdapter, NewsSiteCommentAdapter
from .civic import PetitionAdapter, PublicConsultationAdapter
from .media import PressReleaseAdapter, LetterToEditorAdapter
from .print import FlyerGeneratorAdapter, NewsletterAdapter

__all__ = [
    "BaseChannelAdapter", "PublishResult",
    "MastodonAdapter", "TwitterAdapter", "RedditAdapter", "TelegramAdapter",
    "FacebookAdapter", "InstagramAdapter", "TikTokAdapter",
    "YouTubeCommentAdapter", "NewsSiteCommentAdapter",
    "PetitionAdapter", "PublicConsultationAdapter",
    "PressReleaseAdapter", "LetterToEditorAdapter",
    "FlyerGeneratorAdapter", "NewsletterAdapter",
]
