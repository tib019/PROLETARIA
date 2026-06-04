"""
python -m gramsci — Gramsci CLI

Schnellzugriff auf häufige Aktionen ohne Python-Kenntnisse.
"""
from __future__ import annotations

import sys
import argparse

from . import load_env, ContentEngine, ContentType, CampaignManager, ReviewCLI, Dashboard, get_channel_credentials


def main():
    load_env()

    parser = argparse.ArgumentParser(
        prog="python -m gramsci",
        description="Gramsci — Kulturelle Hegemoniearbeit via ProletariaLLM",
    )
    subparsers = parser.add_subparsers(dest="command")

    # generate
    gen = subparsers.add_parser("generate", help="Einzelnen Inhalt generieren")
    gen.add_argument("topic", help="Thema des Inhalts")
    gen.add_argument("--platform", "-p", default="mastodon",
                     choices=["mastodon", "twitter", "telegram", "facebook", "instagram",
                              "tiktok", "reddit_body", "comment", "long_form",
                              "press_release", "flyer", "newsletter"],
                     help="Zielplattform")
    gen.add_argument("--type", "-t", default="short_post",
                     choices=[ct.value for ct in ContentType],
                     help="Inhaltstyp")
    gen.add_argument("--lang", "-l", default="de",
                     choices=["de", "en", "fr", "nl", "es", "it", "pl"],
                     help="Sprache")
    gen.add_argument("--context", "-c", default="", help="Zusätzlicher Kontext")
    gen.add_argument("--no-review", action="store_true", help="Kein interaktives Review")

    # dashboard
    subparsers.add_parser("dashboard", help="Kampagnen-Übersicht anzeigen")

    # review
    rev = subparsers.add_parser("review", help="Kampagne prüfen und freigeben")
    rev.add_argument("campaign_id", nargs="?", help="Kampagnen-ID (leer: Menü)")

    # credentials
    subparsers.add_parser("credentials", help="Konfigurierte Kanäle anzeigen")

    args = parser.parse_args()

    if args.command == "generate":
        engine = ContentEngine()
        content = engine.generate(
            topic=args.topic,
            content_type=ContentType(args.type),
            platform=args.platform,
            language=args.lang,
            context=args.context,
        )
        if args.no_review:
            print(content.final_text)
        else:
            cli = ReviewCLI()
            cli.review_content(content)

    elif args.command == "dashboard":
        Dashboard().show()

    elif args.command == "review":
        manager = CampaignManager()
        cli = ReviewCLI(manager)
        if args.campaign_id:
            campaign = manager.get(args.campaign_id)
            if not campaign:
                print(f"Kampagne '{args.campaign_id}' nicht gefunden.")
                sys.exit(1)
            cli.review_campaign(campaign)
        else:
            cli.campaign_menu()

    elif args.command == "credentials":
        creds = get_channel_credentials()
        configured = creds["configured_channels"]
        if configured:
            print(f"Konfigurierte Kanäle: {', '.join(configured)}")
        else:
            print("Keine Kanäle konfiguriert. .env-Datei mit API-Keys anlegen.")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
