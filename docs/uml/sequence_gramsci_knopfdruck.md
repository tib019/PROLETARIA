# Gramsci — Sequenzdiagramm: Knopfdruck-Flow

Zeigt den vollständigen Ablauf von der Nutzereingabe bis zur Veröffentlichung auf einer Plattform.

```mermaid
sequenceDiagram
    actor Nutzer
    participant CLI as ReviewCLI
    participant CM as CampaignManager
    participant CE as ContentEngine
    participant LLM as ProletariaLLM<br/>(llm-server :8001)
    participant Ollama as Ollama<br/>(:11434)
    participant Adapter as ChannelAdapter<br/>(z.B. MastodonAdapter)
    participant Plattform as Plattform<br/>(z.B. Mastodon)

    %% ── Schritt 1: Inhalt generieren ────────────────────────────
    Nutzer->>CE: generate(topic, content_type, platform, language)
    CE->>CE: _build_prompt(topic, content_type, platform, language)
    CE->>LLM: POST /generate {prompt, max_tokens}
    LLM->>Ollama: Modell-Inferenz (proletaria-llm)
    Ollama-->>LLM: Generierter Rohtext
    LLM-->>CE: {text: "..."}
    CE->>CE: _trim_to_limit(text, platform)
    CE-->>Nutzer: GeneratedContent(approved=False)
    Note over CE,Nutzer: approved=False — noch nicht freigegeben

    %% ── Schritt 2: Kampagne laden (alternativ direkt) ───────────
    Nutzer->>CLI: python -m gramsci review campaign_id
    CLI->>CM: get(campaign_id)
    CM-->>CLI: Campaign (items mit GeneratedContent)

    %% ── Schritt 3: Review-Schleife ─────────────────────────────
    loop Für jedes CampaignItem
        CLI->>Nutzer: Inhalt anzeigen (Text, Plattform, Sprache, Zeichenanzahl)
        Nutzer->>CLI: Eingabe: [e] Bearbeiten / [ENTER] Freigeben / [n] Ablehnen

        alt Nutzer wählt [e] Bearbeiten
            CLI->>Nutzer: Eingabefeld für Bearbeitung (readline)
            Nutzer->>CLI: Bearbeiteter Text
            CLI->>CLI: content.edited_text = neuer Text
            CLI->>Nutzer: Geänderten Inhalt erneut anzeigen
            Nutzer->>CLI: [ENTER] Freigeben / [n] Ablehnen
        end

        alt Nutzer gibt Freigabe [ENTER]
            CLI->>CLI: content.approved = True
            Note over CLI: GeneratedContent.approved = True
        else Nutzer lehnt ab [n]
            CLI->>CLI: Item überspringen
            Note over CLI: content.approved bleibt False
        end
    end

    %% ── Schritt 4: Veröffentlichen ──────────────────────────────
    Nutzer->>CLI: [p] Freigegebene Items veröffentlichen

    loop Für jedes approved CampaignItem
        CLI->>Adapter: publish(content)
        Adapter->>Adapter: Guard-Check: approved=True?
        Adapter->>Adapter: Guard-Check: fits_platform()?

        alt Guard fehlgeschlagen
            Adapter-->>CLI: PublishResult(success=False, error="...")
            CLI->>Nutzer: Fehlermeldung anzeigen
        else Guard bestanden
            Adapter->>Plattform: API-Call (POST mit final_text)
            Plattform-->>Adapter: post_id / URL
            Adapter-->>CLI: PublishResult(success=True, url="...")
            CLI->>CM: item.published_at = now(), item.publish_url = url
            CM->>CM: Campaign speichern (JSON)
            CLI->>Nutzer: Erfolg + URL anzeigen
        end
    end

    %% ── Schritt 5: Kampagnen-Status aktualisieren ───────────────
    CM->>CM: status = ABGESCHLOSSEN (wenn alle Items published)
    CLI->>Nutzer: Kampagnen-Zusammenfassung anzeigen
```

## Anmerkungen

### Sicherheits-Invarianten

| Punkt | Invariante |
|-------|-----------|
| Nach `generate()` | `content.approved == False` immer |
| `BaseChannelAdapter.publish()` | Lehnt ab wenn `approved == False` |
| `BaseChannelAdapter.publish()` | Lehnt ab wenn `fits_platform() == False` |
| `CampaignItem.is_ready` | `approved AND fits_platform()` |
| Persistenz | `published_at` wird erst nach erfolgreichem API-Call gesetzt |

### Kurzbefehl ohne Kampagne

```mermaid
sequenceDiagram
    actor Nutzer
    participant CE as ContentEngine
    participant LLM as llm-server (:8001)
    participant Ollama as Ollama (:11434)
    participant CLI as ReviewCLI

    Nutzer->>CE: python -m gramsci generate "Thema" --platform mastodon
    CE->>CE: _build_prompt(...)
    CE->>LLM: POST /generate
    LLM->>Ollama: Inferenz
    Ollama-->>LLM: Text
    LLM-->>CE: {text}
    CE-->>CLI: GeneratedContent(approved=False)
    CLI->>Nutzer: Text anzeigen + Review-Prompt
    Nutzer->>CLI: [ENTER] approve / [n] ablehnen
    Note over Nutzer,CLI: Kein Publish ohne approve
```
