"""Reddit-Adapter — Subreddit-Posts und Kommentare via PRAW."""
from __future__ import annotations

import os
from typing import Optional

from ..base import BaseChannelAdapter, PublishResult
from ...core.content_engine import GeneratedContent


class RedditAdapter(BaseChannelAdapter):
    """
    Veröffentlicht auf Reddit via PRAW.

    Env-Variablen: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET,
                   REDDIT_USERNAME, REDDIT_PASSWORD, REDDIT_USER_AGENT
    """

    channel_name = "reddit"

    def __init__(
        self,
        client_id: str = "",
        client_secret: str = "",
        username: str = "",
        password: str = "",
        user_agent: str = "",
        default_subreddit: str = "",
    ):
        self.client_id = client_id or os.getenv("REDDIT_CLIENT_ID", "")
        self.client_secret = client_secret or os.getenv("REDDIT_CLIENT_SECRET", "")
        self.username = username or os.getenv("REDDIT_USERNAME", "")
        self.password = password or os.getenv("REDDIT_PASSWORD", "")
        self.user_agent = user_agent or os.getenv("REDDIT_USER_AGENT", "gramsci/1.0")
        self.default_subreddit = default_subreddit or os.getenv("REDDIT_DEFAULT_SUBREDDIT", "")
        self._reddit = None

    def validate_credentials(self) -> bool:
        return all([self.client_id, self.client_secret, self.username, self.password])

    def _get_reddit(self):
        if self._reddit is None:
            try:
                import praw
                self._reddit = praw.Reddit(
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    username=self.username,
                    password=self.password,
                    user_agent=self.user_agent,
                )
            except ImportError:
                raise RuntimeError("praw nicht installiert: pip install praw")
        return self._reddit

    def _do_publish(self, content: GeneratedContent) -> PublishResult:
        if not self.validate_credentials():
            return PublishResult(
                success=False,
                error="Reddit-Credentials fehlen.",
                channel=self.channel_name,
            )

        subreddit_name = self.default_subreddit
        if not subreddit_name:
            return PublishResult(
                success=False,
                error="Kein Subreddit angegeben (REDDIT_DEFAULT_SUBREDDIT).",
                channel=self.channel_name,
            )

        try:
            reddit = self._get_reddit()
            subreddit = reddit.subreddit(subreddit_name)

            if content.platform == "reddit_title":
                submission = subreddit.submit(title=content.final_text, selftext="")
            else:
                lines = content.final_text.split("\n", 1)
                title = lines[0][:300]
                body = lines[1].strip() if len(lines) > 1 else ""
                submission = subreddit.submit(title=title, selftext=body)

            return PublishResult(
                success=True,
                post_id=submission.id,
                url=f"https://reddit.com{submission.permalink}",
                channel=self.channel_name,
            )
        except Exception as e:
            return PublishResult(success=False, error=str(e), channel=self.channel_name)

    def post_comment(self, submission_url: str, comment_text: str) -> PublishResult:
        """Antwortet auf einen bestehenden Reddit-Post."""
        if not self.validate_credentials():
            return PublishResult(success=False, error="Credentials fehlen.", channel=self.channel_name)
        try:
            reddit = self._get_reddit()
            submission = reddit.submission(url=submission_url)
            comment = submission.reply(comment_text)
            return PublishResult(
                success=True,
                post_id=comment.id,
                url=f"https://reddit.com{comment.permalink}",
                channel=self.channel_name,
            )
        except Exception as e:
            return PublishResult(success=False, error=str(e), channel=self.channel_name)
