# Gramsci — Bedienungsanleitung

---

## Was ist Gramsci?

Antonio Gramsci (1891–1937) entwickelte die Theorie der **kulturellen Hegemonie**: Herrschaft wird nicht nur durch Zwang gesichert, sondern durch Konsens — in Zivilgesellschaft, Medien, Alltagsdiskurs. Gegenhegemonie bedeutet, diesen Konsens zu brechen, eigene Frames zu setzen, Narrative zu verschieben.

Das Gramsci-Modul übersetzt diese Theorie in Praxis: Es unterstützt Menschen dabei, **auf allen öffentlichen Arenen wirksam zu kommunizieren** — von Mastodon bis Pressemitteilung, von Petition bis Newsletter. Dabei gilt immer das **Knopfdruck-Prinzip**: Kein generierter Inhalt wird ohne explizite menschliche Freigabe veröffentlicht.

**ProletariaLLM liefert Entwürfe. Menschen entscheiden.**

---

## Voraussetzungen

```bash
# ProletariaLLM muss lokal laufen
# llm-server auf Port 8001:
python llm-server/serve.py
# oder via Docker:
docker compose up -d llm-server ollama

# Python-Abhängigkeiten
pip install -r requirements.txt
```

---

## Schnellstart

```bash
# Einzelnen Post generieren und im Terminal reviewen
python -m gramsci generate "Mietpreisbremse versagt" --platform mastodon --lang de

# Mit Sprache und Typ
python -m gramsci generate "Klimagerechtigkeit jetzt" --platform twitter --lang en --type short_post

# Ohne interaktives Review (direkte Ausgabe)
python -m gramsci generate "Solidarität" --platform mastodon --no-review

# Kampagnen-Dashboard anzeigen
python -m gramsci dashboard

# Kampagne reviewen und freigeben
python -m gramsci review <campaign_id>

# Konfigurierte Kanäle anzeigen
python -m gramsci credentials
```

---

## Unterstützte Plattformen und Zeichenlimits

| Plattform | `--platform` | Zeichenlimit |
|-----------|-------------|--------------|
| Mastodon | `mastodon` | 500 |
| Twitter/X | `twitter` | 280 |
| Telegram | `telegram` | 4096 |
| Facebook | `facebook` | 63206 |
| Instagram | `instagram` | 2200 |
| TikTok | `tiktok` | 2200 |
| Reddit (Body) | `reddit_body` | 40000 |
| Kommentar | `comment` | 1000 |
| Langform | `long_form` | unbegrenzt |
| Pressemitteilung | `press_release` | unbegrenzt |
| Flyer | `flyer` | unbegrenzt |
| Newsletter | `newsletter` | unbegrenzt |

---

## Inhaltstypen

| Typ | `--type` | Beschreibung |
|-----|----------|-------------|
| Kurz-Post | `short_post` | Ein Post für Social Media |
| Thread | `thread` | Mehrteiliger Thread |
| Kommentar-Antwort | `comment_response` | Antwort auf fremden Post |
| Langform | `long_form` | Ausführlicher Artikel |
| Pressemitteilung | `press_release` | Formelle Pressemitteilung |
| Leserbrief | `letter_to_editor` | Brief an Zeitungsredaktion |
| Flyer | `flyer` | Physisches Verteilmaterial |
| Newsletter | `newsletter` | E-Mail-Newsletter |
| Meme-Text | `meme_text` | Kurzer Text für Meme-Grafik |
| Petition | `petition_text` | Petitionstext |
| Öffentliche Erklärung | `public_statement` | Offizielle Stellungnahme |

---

## Kampagne erstellen

Eine Kampagne koordiniert mehrere Inhalte für verschiedene Plattformen und Sprachen als zusammenhängende Einheit.

```python
from gramsci import load_env, CampaignManager, ContentType

load_env()

manager = CampaignManager()

# Kampagne erstellen — generiert automatisch für alle Kombinationen
campaign = manager.create(
    name="Wohnungsnot-Kampagne Juni",
    topic="Mieten steigen während Wohnraum leer steht. Vergesellschaftung jetzt.",
    platforms=["mastodon", "twitter", "telegram", "press_release"],
    languages=["de", "en"],
    content_type=ContentType.SHORT_POST,
)

print(f"Kampagne {campaign.id}: {campaign.total_items} Items generiert")
# Ausgabe: Kampagne a3f1b2c4: 8 Items generiert (4 Plattformen × 2 Sprachen)
```

### Kampagne reviewen

```bash
python -m gramsci review a3f1b2c4
```

Oder per Python:

```python
from gramsci import ReviewCLI, CampaignManager

manager = CampaignManager()
cli = ReviewCLI(manager)

campaign = manager.get("a3f1b2c4")
cli.review_campaign(campaign)
```

---

## Kanäle konfigurieren

Alle Credentials werden aus einer `.env`-Datei im Projektroot gelesen. Nur konfigurierte Kanäle können tatsächlich veröffentlichen.

```bash
# .env anlegen
cp .env.example .env
# Credentials eintragen
```

### Umgebungsvariablen pro Kanal

#### Mastodon
| Variable | Pflicht | Beschreibung |
|----------|---------|--------------|
| `MASTODON_ACCESS_TOKEN` | ja | Access Token aus Mastodon-Einstellungen → Entwicklung |
| `MASTODON_API_BASE_URL` | ja | Instanz-URL z.B. `https://social.coop` |

#### Twitter / X
| Variable | Pflicht | Beschreibung |
|----------|---------|--------------|
| `TWITTER_API_KEY` | ja | Consumer Key |
| `TWITTER_API_SECRET` | ja | Consumer Secret |
| `TWITTER_ACCESS_TOKEN` | ja | Access Token |
| `TWITTER_ACCESS_SECRET` | ja | Access Token Secret |

#### Telegram
| Variable | Pflicht | Beschreibung |
|----------|---------|--------------|
| `TELEGRAM_BOT_TOKEN` | ja | Token vom BotFather |
| `TELEGRAM_CHAT_ID` | ja | Kanal- oder Gruppen-ID |

#### Reddit
| Variable | Pflicht | Beschreibung |
|----------|---------|--------------|
| `REDDIT_CLIENT_ID` | ja | App-ID aus reddit.com/prefs/apps |
| `REDDIT_CLIENT_SECRET` | ja | App-Secret |
| `REDDIT_USERNAME` | ja | Reddit-Username |
| `REDDIT_PASSWORD` | ja | Reddit-Passwort |
| `REDDIT_USER_AGENT` | nein | Standard: `gramsci/0.1` |

#### Facebook
| Variable | Pflicht | Beschreibung |
|----------|---------|--------------|
| `FACEBOOK_PAGE_ACCESS_TOKEN` | ja | Page Access Token aus Meta Developer |
| `FACEBOOK_PAGE_ID` | ja | Seiten-ID |

#### Instagram
| Variable | Pflicht | Beschreibung |
|----------|---------|--------------|
| `INSTAGRAM_ACCESS_TOKEN` | ja | Access Token (Instagram Business) |
| `INSTAGRAM_ACCOUNT_ID` | ja | Instagram Account ID |

#### TikTok
| Variable | Pflicht | Beschreibung |
|----------|---------|--------------|
| `TIKTOK_ACCESS_TOKEN` | ja | Access Token aus TikTok Developer |
| `TIKTOK_OPEN_ID` | ja | Open ID des Accounts |

#### YouTube (Kommentare)
| Variable | Pflicht | Beschreibung |
|----------|---------|--------------|
| `YOUTUBE_API_KEY` | ja | API Key aus Google Cloud Console |
| `YOUTUBE_CHANNEL_ID` | nein | Standard-Kanal für Kommentare |

#### Gramsci-Konfiguration
| Variable | Pflicht | Beschreibung |
|----------|---------|--------------|
| `LLM_SERVER` | nein | Standard: `http://localhost:8001` |
| `GRAMSCI_CAMPAIGN_DIR` | nein | Standard: `.gramsci_campaigns/` |

---

## ReviewCLI bedienen

Der ReviewCLI ist das Kerninterface von Gramsci. Kein Inhalt verlässt das System ohne explizite Eingabe.

### Tastenbelegung

| Taste | Aktion |
|-------|--------|
| `ENTER` | Inhalt freigeben (`approved=True`) |
| `e` | Inhalt bearbeiten (Inline-Editor) |
| `n` | Inhalt ablehnen (überspringen) |
| `p` | Alle freigegebenen Items veröffentlichen |
| `q` | ReviewCLI beenden ohne Veröffentlichen |

### Ablauf im Detail

```
╔═══════════════════════════════════════════════╗
║  GRAMSCI — Review                             ║
║  Kampagne: Wohnungsnot-Kampagne Juni          ║
║  Item 1/8 · mastodon · DE                     ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  Mieten steigen während tausende Wohnungen    ║
║  leer stehen. Das ist kein Marktversagen —   ║
║  das ist Politik. Vergesellschaftung jetzt!  ║
║  #Wohnungsnot #Vergesellschaftung            ║
║                                               ║
║  487/500 Zeichen · passt ✓                   ║
╠═══════════════════════════════════════════════╣
║  [ENTER] Freigeben  [e] Bearbeiten  [n] Nein ║
╚═══════════════════════════════════════════════╝
```

### Bearbeiten

Nach `e` erscheint ein Eingabefeld. Der aktuelle Text wird angezeigt. Nach Bestätigung wird der bearbeitete Text als `edited_text` gespeichert — das Original bleibt erhalten. `final_text` gibt dann den bearbeiteten Text zurück.

---

## NarrativeRadar nutzen

Der NarrativeRadar analysiert Texte auf reaktionäre Frames und gibt strukturierte Gegennarrative zurück.

```python
from gramsci import NarrativeRadar, load_env

load_env()
radar = NarrativeRadar()

# Text analysieren
analyse = radar.analyze(
    "Die Klimakleber terrorisieren die Bevölkerung und gefährden Menschenleben."
)

print(f"Narrativ-Typ:   {analyse.narrative_type.value}")
print(f"Bedrohungslevel: {analyse.threat_level.value}")
print(f"Erkannte Frames: {', '.join(analyse.detected_frames)}")
print(f"Vertrauen:       {analyse.confidence:.0%}")
print()
print("Gegennarrativ:")
print(analyse.counter_narrative)
```

Ausgabe (Beispiel):
```
Narrativ-Typ:    klimaleugnung
Bedrohungslevel: hoch
Erkannte Frames: klimakleber terroristen, lügenpresse
Vertrauen:       87%

Gegennarrativ:
Der Begriff "Klimaterrorismus" diffamiert Menschen, die für ihre Zukunft eintreten.
Wissenschaftliche Einigkeit: ohne sofortige Maßnahmen sind Millionen Leben bedroht.
Wer die Botschaft angreift, hat der Sache nichts entgegenzusetzen.
```

### Erkannte Narrativ-Typen

| Typ | Erkennt |
|-----|---------|
| `rechtsextrem` | Überfremdung, Remigration, Volksverrat, Bevölkerungsaustausch |
| `islamfeindlich` | Islamisierung, Abendland-Rhetorik |
| `antifeministisch` | Genderideologie-Narrative |
| `klimaleugnung` | Klimahysterie, Klimaschwindel, Klimaalarmismus |
| `verschwörung` | Globalisten, Great Reset, Chemtrails |
| `rassistisch` | Ausländerkriminalität-Frames |
| `antikommunismus` | Kommunismus=Totalitarismus-Gleichsetzungen |
| `polizeipropaganda` | "Unsere Polizei"-Apologetik |
| `neoliberal` | Alternativlosigkeits-Rhetoric, Sachzwang-Framing |

### NarrativeRadar als ContentEngine-Kontext

```python
from gramsci import NarrativeRadar, ContentEngine, ContentType, load_env

load_env()
radar = NarrativeRadar()
engine = ContentEngine()

# Diskurs analysieren
analyse = radar.analyze("Klimakleber blockieren Wirtschaft...")
gegenkontext = radar.generate_counter(analyse)

# Kontext in Generierung einfließen lassen
inhalt = engine.generate(
    topic="Klimagerechtigkeit und Aktionsformen",
    content_type=ContentType.SHORT_POST,
    platform="mastodon",
    language="de",
    context=gegenkontext,  # Radar-Erkenntnisse als Kontext
)
```

---

## Mehrsprachige Kampagnen

Gramsci unterstützt 7 Sprachen: Deutsch (primär), Englisch, Französisch, Niederländisch, Spanisch, Italienisch, Polnisch.

```python
from gramsci import CampaignManager, ContentType, load_env

load_env()
manager = CampaignManager()

# Alle unterstützten Sprachen
kampagne = manager.create(
    name="Internationale Solidaritäts-Kampagne",
    topic="Workers' rights are human rights. Solidarity across borders.",
    platforms=["mastodon", "twitter"],
    languages=["de", "en", "fr", "nl", "es"],
    content_type=ContentType.SHORT_POST,
)

# Ergibt 10 Items (2 Plattformen × 5 Sprachen)
print(f"{kampagne.total_items} Items generiert")
```

### Sprach-Codes

| Code | Sprache |
|------|---------|
| `de` | Deutsch |
| `en` | English |
| `fr` | Français |
| `nl` | Nederlands |
| `es` | Español |
| `it` | Italiano |
| `pl` | Polski |

---

## Veröffentlichen

Nach dem Review werden alle Items mit `approved=True` über den jeweiligen Kanal-Adapter veröffentlicht.

```python
from gramsci import CampaignManager, ReviewCLI, load_env
from gramsci.channels import MastodonAdapter, TelegramAdapter, TwitterAdapter

load_env()
manager = CampaignManager()
campaign = manager.get("a3f1b2c4")

adapters = {
    "mastodon": MastodonAdapter(),
    "twitter":  TwitterAdapter(),
    "telegram": TelegramAdapter(),
}

for item in campaign.items:
    if item.is_ready and item.channel_adapter in adapters:
        result = adapters[item.channel_adapter].publish(item.content)
        print(result)
```

### Guard-Prinzip

Jeder Adapter prüft vor dem Publish:

1. `content.approved == True` — muss im ReviewCLI gesetzt worden sein
2. `content.fits_platform() == True` — Text darf Zeichenlimit nicht überschreiten

Schlägt einer dieser Checks fehl, gibt `publish()` ein `PublishResult(success=False)` zurück, ohne die Plattform-API aufzurufen.

---

## Kampagnen-Persistenz

Kampagnen werden als JSON-Dateien gespeichert:

```
.gramsci_campaigns/
├── a3f1b2c4.json
├── b7e9d1a2.json
└── ...
```

```python
# Alle Kampagnen auflisten
manager = CampaignManager()
for c in manager.list_all():
    print(f"{c.id}  {c.name}  {c.approved_items}/{c.total_items} freigegeben  [{c.status.value}]")

# Kampagne löschen
manager.delete("a3f1b2c4")
```

Der Speicherort ist konfigurierbar:
```bash
GRAMSCI_CAMPAIGN_DIR=/pfad/zu/kampagnen python -m gramsci dashboard
```

---

## Sicherheitshinweise

- **Credentials in `.env` nicht committen.** `.env` ist in `.gitignore` eingetragen.
- **API-Keys für Social-Media-Konten mit begrenzten Rechten** ausstellen (nur Publish, kein Read/Delete wenn möglich).
- **Inhalt vor Freigabe sorgfältig prüfen.** ProletariaLLM kann Fehler machen. Das ReviewCLI ist kein optionaler Schritt.
- **Gramsci nutzt nur Kanäle für die Credentials vorhanden sind.** Nicht konfigurierte Adapter publizieren nicht, sie geben einen Fehler zurück.
- **Kein externer Logging-Dienst.** Alle Daten bleiben lokal.
