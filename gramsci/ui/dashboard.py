"""
Dashboard — Übersicht über alle Kampagnen und Aktivitäten.

Einfache Terminal-Übersicht, keine externen Dependencies.
"""
from __future__ import annotations

import sys
from datetime import datetime

from ..core.campaign_manager import CampaignManager, CampaignStatus


RESET   = "\033[0m"
BOLD    = "\033[1m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
CYAN    = "\033[36m"
GREY    = "\033[90m"
RED     = "\033[31m"


def _c(text: str, color: str) -> str:
    if not sys.stdout.isatty():
        return text
    return f"{color}{text}{RESET}"


class Dashboard:
    """Terminal-Dashboard für Gramsci-Aktivitäten."""

    def __init__(self, manager: CampaignManager = None):
        self.manager = manager or CampaignManager()

    def show(self):
        """Zeigt vollständiges Dashboard."""
        campaigns = self.manager.list_campaigns()
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        print(f"\n{_c('═' * 64, CYAN)}")
        print(f"{_c('  GRAMSCI — KULTURELLE HEGEMONIEARBEIT', BOLD)}")
        print(f"{_c(f'  Stand: {now}', GREY)}")
        print(f"{_c('═' * 64, CYAN)}\n")

        # Statistiken
        total = len(campaigns)
        active = sum(1 for c in campaigns if c.status in (
            CampaignStatus.BEREIT, CampaignStatus.TEILWEISE
        ))
        done = sum(1 for c in campaigns if c.status == CampaignStatus.ABGESCHLOSSEN)
        total_items = sum(c.total_items for c in campaigns)
        approved = sum(c.approved_items for c in campaigns)
        published = sum(c.published_items for c in campaigns)

        print(f"  Kampagnen:   {_c(str(total), BOLD)} gesamt | "
              f"{_c(str(active), YELLOW)} aktiv | "
              f"{_c(str(done), GREEN)} abgeschlossen")
        print(f"  Inhalte:     {total_items} gesamt | "
              f"{_c(str(approved), GREEN)} freigegeben | "
              f"{_c(str(published), CYAN)} veröffentlicht\n")

        if not campaigns:
            print(f"  {_c('Keine Kampagnen vorhanden.', GREY)}\n")
            return

        # Aktive Kampagnen
        active_campaigns = [c for c in campaigns if c.status in (
            CampaignStatus.BEREIT, CampaignStatus.TEILWEISE, CampaignStatus.ENTWURF
        )]
        if active_campaigns:
            print(f"  {_c('AKTIVE KAMPAGNEN', BOLD)}")
            print(f"  {_c('─' * 60, GREY)}")
            for c in active_campaigns[:10]:
                bar = self._progress_bar(c.approved_items, c.total_items)
                print(f"  {_c(c.id, GREY)} {c.name[:30]:<30} {bar}")
                print(f"  {' ' * 8} {_c(c.topic[:50], GREY)}")
            print()

        # Ausstehende Freigaben
        pending = [(c, i, item)
                   for c in campaigns
                   for i, item in enumerate(c.items)
                   if not item.content.approved and not item.published_at]
        if pending:
            print(f"  {_c(f'AUSSTEHEND: {len(pending)} Freigaben', YELLOW)}")
            for c, i, item in pending[:5]:
                print(f"  · [{c.id}] {c.name}: {item.channel_adapter} / {item.content.language}")
            if len(pending) > 5:
                print(f"  · ... und {len(pending) - 5} weitere")
            print()

        print(f"{_c('═' * 64, CYAN)}\n")

    def _progress_bar(self, done: int, total: int, width: int = 20) -> str:
        if total == 0:
            return _c("[" + "─" * width + "]", GREY)
        filled = int(width * done / total)
        bar = "█" * filled + "░" * (width - filled)
        pct = int(100 * done / total)
        color = GREEN if pct == 100 else YELLOW if pct > 0 else GREY
        return _c(f"[{bar}]", color) + f" {done}/{total}"
