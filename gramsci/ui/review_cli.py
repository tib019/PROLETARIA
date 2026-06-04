"""
ReviewCLI — Knopfdruck-Interface für menschliche Freigabe

Zeigt generierten Inhalt an, ermöglicht Bearbeitung und Freigabe.
Kein Inhalt wird ohne explizite Bestätigung veröffentlicht.
"""
from __future__ import annotations

import sys
from typing import Optional

from ..core.content_engine import GeneratedContent, ContentType
from ..core.campaign_manager import CampaignManager, Campaign, CampaignItem


RESET   = "\033[0m"
BOLD    = "\033[1m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
CYAN    = "\033[36m"
GREY    = "\033[90m"


def _c(text: str, color: str) -> str:
    if not sys.stdout.isatty():
        return text
    return f"{color}{text}{RESET}"


class ReviewCLI:
    """
    Terminal-Interface für menschliche Kontrolle aller generierten Inhalte.

    Workflow:
        1. Inhalt anzeigen
        2. Bearbeiten (optional)
        3. Freigeben (ENTER) oder Ablehnen (n)
        4. Veröffentlichen (p) oder zurückstellen

    Kein Inhalt verlässt das System ohne approved=True.
    """

    def __init__(self, manager: Optional[CampaignManager] = None):
        self.manager = manager or CampaignManager()

    # ------------------------------------------------------------------
    # Einzelner Inhalt

    def review_content(self, content: GeneratedContent) -> bool:
        """
        Zeigt einen einzelnen Inhalt zur Freigabe an.
        Gibt True zurück wenn freigegeben.
        """
        self._print_header("GRAMSCI — INHALTSPRÜFUNG")
        self._print_content_card(content)

        while True:
            print(f"\n  {_c('[ENTER]', GREEN)} Freigeben  "
                  f"{_c('[e]', CYAN)} Bearbeiten  "
                  f"{_c('[n]', RED)} Ablehnen  "
                  f"{_c('[q]', GREY)} Abbrechen")
            choice = input("  > ").strip().lower()

            if choice in ("", "j", "y", "freigeben"):
                content.approved = True
                print(_c("  ✓ Freigegeben.", GREEN))
                return True
            elif choice == "e":
                edited = self._edit_text(content.text)
                if edited:
                    content.edited_text = edited
                    self._print_content_card(content)
            elif choice in ("n", "nein", "no"):
                print(_c("  ✗ Abgelehnt.", RED))
                return False
            elif choice in ("q", "quit"):
                return False

    def review_list(self, contents: list[GeneratedContent]) -> list[GeneratedContent]:
        """Zeigt eine Liste von Inhalten nacheinander zur Freigabe an."""
        approved = []
        total = len(contents)
        for i, content in enumerate(contents):
            self._print_header(f"INHALT {i+1}/{total}")
            if self.review_content(content):
                approved.append(content)
        print(f"\n  {_c(f'{len(approved)}/{total} Inhalte freigegeben.', GREEN)}\n")
        return approved

    # ------------------------------------------------------------------
    # Kampagnen-Review

    def review_campaign(self, campaign: Campaign) -> int:
        """Interaktives Review einer ganzen Kampagne. Gibt Anzahl freigegebener Items zurück."""
        self._print_header(f"KAMPAGNE: {campaign.name}")
        self._print_campaign_summary(campaign)

        print(f"\n  {_c('[a]', GREEN)} Alle freigeben  "
              f"{_c('[r]', CYAN)} Einzeln prüfen  "
              f"{_c('[q]', GREY)} Abbrechen")
        choice = input("  > ").strip().lower()

        if choice == "a":
            count = self.manager.approve_all(campaign.id)
            print(_c(f"\n  ✓ {count} Inhalte freigegeben.", GREEN))
            return count
        elif choice == "r":
            return self._review_campaign_items(campaign)
        return 0

    def campaign_menu(self):
        """Hauptmenü für Kampagnenverwaltung."""
        while True:
            self._print_header("GRAMSCI — KAMPAGNEN")
            campaigns = self.manager.list_campaigns()

            if not campaigns:
                print("  Keine Kampagnen vorhanden.\n")
            else:
                for i, c in enumerate(campaigns):
                    status_color = GREEN if c.approved_items == c.total_items else YELLOW
                    print(f"  [{i+1}] {_c(c.name, BOLD)} — {c.topic[:50]}")
                    print(f"       Status: {_c(c.status.value, status_color)} | "
                          f"{c.approved_items}/{c.total_items} freigegeben | "
                          f"{c.published_items} veröffentlicht")

            print(f"\n  {_c('[Nr]', CYAN)} Kampagne öffnen  "
                  f"{_c('[q]', GREY)} Beenden")
            choice = input("  > ").strip().lower()

            if choice in ("q", "quit", "exit"):
                break
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(campaigns):
                    self.review_campaign(campaigns[idx])
            except ValueError:
                pass

    # ------------------------------------------------------------------

    def _review_campaign_items(self, campaign: Campaign) -> int:
        approved = 0
        for i, item in enumerate(campaign.items):
            if item.content.approved:
                continue
            self._print_header(f"ITEM {i+1}/{campaign.total_items}: {item.channel_adapter}")
            if self.review_content(item.content):
                self.manager.approve_item(campaign.id, i)
                approved += 1
        return approved

    def _edit_text(self, original: str) -> str:
        print(_c("\n  Bearbeite Text (leere Zeile zum Beenden, 'ABBRUCH' zum Abbrechen):", CYAN))
        print(_c("  Originaltext wird angezeigt — tippe neuen Text ein:\n", GREY))
        lines = []
        try:
            while True:
                line = input("  > ")
                if line.strip().upper() == "ABBRUCH":
                    return ""
                if line == "" and lines:
                    break
                lines.append(line)
        except (EOFError, KeyboardInterrupt):
            return ""
        return "\n".join(lines)

    def _print_header(self, title: str):
        width = 60
        print(f"\n{_c('═' * width, CYAN)}")
        print(f"{_c('  ' + title, BOLD)}")
        print(f"{_c('═' * width, CYAN)}\n")

    def _print_content_card(self, content: GeneratedContent):
        meta = (f"  Typ: {content.content_type.value} | "
                f"Plattform: {content.platform} | "
                f"Sprache: {content.language} | "
                f"Zeichen: {content.char_count}")
        print(_c(meta, GREY))

        fits = content.fits_platform()
        fits_str = _c("✓ passt", GREEN) if fits else _c("✗ ZU LANG", RED)
        print(f"  {fits_str}\n")

        print(_c("  ┌─ INHALT " + "─" * 48, CYAN))
        for line in content.final_text.split("\n"):
            print(f"  │ {line}")
        print(_c("  └" + "─" * 57, CYAN))

        if content.edited_text:
            print(_c("  [Bearbeitet]", YELLOW))

    def _print_campaign_summary(self, campaign: Campaign):
        print(f"  Thema: {_c(campaign.topic, BOLD)}")
        print(f"  Erstellt: {campaign.created_at[:10]}")
        print(f"  Status: {_c(campaign.status.value, YELLOW)}")
        print(f"  Items: {campaign.total_items} gesamt, "
              f"{_c(str(campaign.approved_items), GREEN)} freigegeben, "
              f"{campaign.published_items} veröffentlicht")
        print()
        for i, item in enumerate(campaign.items):
            approved_str = _c("✓", GREEN) if item.content.approved else _c("○", GREY)
            published_str = _c("⬆", CYAN) if item.published_at else ""
            print(f"  {approved_str} [{i+1}] {item.channel_adapter} | "
                  f"{item.content.language} | {item.content.char_count}Z  {published_str}")
