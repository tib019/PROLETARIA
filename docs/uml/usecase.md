# PROLETARIA — Use-Case-Übersicht

## Akteure und Use Cases

```mermaid
flowchart LR
    subgraph Akteure
        A1[Aktivist:in]
        A2[OPSEC-Verantwortliche:r]
        A3[Jurist:in]
        A4[Forscher:in]
        A5[Kommunikator:in]
    end

    subgraph OPSEC[OPSEC-Module]
        UC1[Selbst-OSINT-Audit\ndurchführen]
        UC2[Kommunikations-\nstruktur auditieren]
        UC3[Überwachungsakteur\nrecherchieren]
        UC4[DSGVO-Anfrage\nerstellen]
        UC5[DSGVO-Anfrage\neskalieren]
        UC6[OPSEC-Bedrohung\nmelden]
    end

    subgraph NARRATIV[Narrativanalyse]
        UC7[Narrativ\nanalysieren]
        UC8[Gegennarrativ\ngenerieren]
        UC9[Koordinations-\nnetzwerk analysieren]
    end

    subgraph VERHOER[Verhör-Training]
        UC10[Verhör-Szenario\ntrainieren]
        UC11[Rechtliche\nGrundlagen lernen]
        UC12[Verhörtaktiken\nerkennen]
    end

    subgraph LLM[ProletariaLLM]
        UC13[Politischen Text\nanalysieren lassen]
        UC14[Rechtliches Schreiben\ngenerieren]
    end

    subgraph GRAMSCI[Gramsci — Hegemoniearbeit]
        UC15[Einzelnen Inhalt\ngenerieren]
        UC16[Kampagne erstellen\nund koordinieren]
        UC17[Inhalte im ReviewCLI\nfreigeben]
        UC18[Inhalt auf Plattform\nveröffentlichen]
        UC19[Narrativ im Diskurs\nüberwachen]
        UC20[Mehrsprachige\nKampagne erstellen]
        UC21[Kampagnen-Dashboard\naufrufen]
    end

    A1 --> UC1
    A1 --> UC2
    A1 --> UC4
    A1 --> UC10
    A1 --> UC11
    A1 --> UC13
    A1 --> UC15
    A1 --> UC17
    A1 --> UC18

    A2 --> UC1
    A2 --> UC2
    A2 --> UC3
    A2 --> UC6
    A2 --> UC7
    A2 --> UC19

    A3 --> UC4
    A3 --> UC5
    A3 --> UC14
    A3 --> UC11

    A4 --> UC7
    A4 --> UC8
    A4 --> UC9
    A4 --> UC3

    A5 --> UC15
    A5 --> UC16
    A5 --> UC17
    A5 --> UC18
    A5 --> UC19
    A5 --> UC20
    A5 --> UC21
```

## Use-Case-Beschreibungen

### UC1: Selbst-OSINT-Audit

| Feld | Inhalt |
|------|--------|
| **Akteur** | Aktivist:in, OPSEC-Verantwortliche:r |
| **Ziel** | Eigene digitale Spuren erkennen bevor staatliche Akteure es tun |
| **Vorbedingung** | Zugang zu PROLETARIA API |
| **Hauptfluss** | Text/Datei einreichen → ExposureScanner analysiert → Findings mit Severity → Risikoprofil |
| **Alternativfluss** | Datei-Metadaten-Scan (EXIF, Office-Metadaten) |
| **Ergebnis** | Risiko-Score + konkrete Handlungsempfehlungen |

### UC4: DSGVO-Anfrage erstellen

| Feld | Inhalt |
|------|--------|
| **Akteur** | Aktivist:in, Jurist:in |
| **Ziel** | Rechtskonforme Auskunftsanfrage gegen Überwachungsakteur generieren |
| **Vorbedingung** | Name + Adresse des Verantwortlichen bekannt |
| **Hauptfluss** | Anfrage-Typ wählen (Art.15/17/21) → Daten eingeben → Brief generieren → Versenden → Frist überwachen |
| **Alternativfluss** | Massenanfragen gegen mehrere Verantwortliche |
| **Ausnahme** | Keine Antwort → Automatische Eskalation an BfDI |
| **Ergebnis** | Rechtsgültiger Brief + Fristen-Tracking |

### UC10: Verhör-Szenario trainieren

| Feld | Inhalt |
|------|--------|
| **Akteur** | Aktivist:in |
| **Ziel** | Psychologische Vorbereitung auf polizeiliche Befragung |
| **Vorbedingung** | keine |
| **Hauptfluss** | Szenario wählen (Einsteiger/Fortgeschritten/Experte) → Fragen beantworten → Echtzeit-Feedback → Auswertung |
| **Alternativfluss** | TacticAnalyzer-Modus: realen Verhörtext eingeben → Taktik erkennen |
| **Ergebnis** | Zertifikat (bestanden/nicht bestanden) + Verbesserungshinweise |

### UC7: Narrativ analysieren

| Feld | Inhalt |
|------|--------|
| **Akteur** | OPSEC-Verantwortliche:r, Forscher:in |
| **Ziel** | Rechte/staatliche Narrative in Texten erkennen und verstehen |
| **Vorbedingung** | ProletariaLLM / Ollama läuft |
| **Hauptfluss** | Text einreichen → Narrative erkannt → Frames analysiert → Gegennarrativ generiert |
| **Ergebnis** | Vollständige Analyse + handlungsfähige Gegenstrategien |

### UC15: Einzelnen Inhalt generieren

| Feld | Inhalt |
|------|--------|
| **Akteur** | Aktivist:in, Kommunikator:in |
| **Ziel** | Einen politischen Text für eine bestimmte Plattform generieren |
| **Vorbedingung** | ProletariaLLM läuft (`llm-server` auf `:8001`) |
| **Hauptfluss** | `python -m gramsci generate "Thema" --platform mastodon --lang de` → ContentEngine generiert → ReviewCLI zeigt an → Freigabe → optional Veröffentlichen |
| **Alternativfluss** | `--no-review` für direkte Ausgabe ohne interaktives Review |
| **Ergebnis** | Freigegebener oder abgelehnter GeneratedContent |

### UC16: Kampagne erstellen und koordinieren

| Feld | Inhalt |
|------|--------|
| **Akteur** | Kommunikator:in |
| **Ziel** | Mehrere Inhalte für verschiedene Plattformen und Sprachen als zusammenhängende Kampagne koordinieren |
| **Vorbedingung** | ProletariaLLM läuft |
| **Hauptfluss** | `CampaignManager.create(name, topic, platforms, languages)` → Für jede Plattform+Sprache-Kombination ContentEngine generiert → Kampagne persistiert als JSON |
| **Ergebnis** | Kampagne im Status ENTWURF mit allen Items |

### UC17: Inhalte im ReviewCLI freigeben

| Feld | Inhalt |
|------|--------|
| **Akteur** | Aktivist:in, Kommunikator:in |
| **Ziel** | Jeden generierten Inhalt vor Veröffentlichung sichten, ggf. bearbeiten und freigeben |
| **Vorbedingung** | Kampagne mit generierten Items existiert |
| **Hauptfluss** | `python -m gramsci review <id>` → ReviewCLI zeigt Item → [e] bearbeiten / [ENTER] freigeben / [n] ablehnen → Alle Items durchlaufen |
| **Invariante** | Kein Inhalt erhält `approved=True` ohne explizite Nutzereingabe |
| **Ergebnis** | Items mit `approved=True` bereit für Veröffentlichung |

### UC18: Inhalt auf Plattform veröffentlichen

| Feld | Inhalt |
|------|--------|
| **Akteur** | Kommunikator:in |
| **Ziel** | Freigegebenen Inhalt über den konfigurierten Kanal-Adapter senden |
| **Vorbedingung** | `content.approved=True`, API-Credentials in `.env` konfiguriert |
| **Hauptfluss** | ReviewCLI → `[p]` → ChannelAdapter.publish(content) → Guard-Check → API-Call → PublishResult → URL persistiert |
| **Ausnahme** | Guard schlägt fehl (nicht freigegeben oder Zeichenlimit) → Fehlermeldung, kein Publish |
| **Ergebnis** | `CampaignItem.published_at` gesetzt, URL gespeichert |

### UC19: Narrativ im Diskurs überwachen

| Feld | Inhalt |
|------|--------|
| **Akteur** | Kommunikator:in, OPSEC-Verantwortliche:r |
| **Ziel** | Reaktionäre Frames und Desinformation in Texten erkennen, um gezielte Gegeninhalte zu generieren |
| **Vorbedingung** | ProletariaLLM läuft |
| **Hauptfluss** | `NarrativeRadar.analyze(text)` → Frames erkannt → ThreatLevel bewertet → `generate_counter()` → Gegennarrativ als ContentEngine-Kontext |
| **Ergebnis** | NarrativeAnalysis mit counter_narrative + ThreatLevel |

### UC20: Mehrsprachige Kampagne erstellen

| Feld | Inhalt |
|------|--------|
| **Akteur** | Kommunikator:in |
| **Ziel** | Dasselbe Thema in mehreren Sprachen für internationale Vernetzung aufbereiten |
| **Vorbedingung** | ProletariaLLM mit mehrsprachiger Kompetenz (DE/EN/FR/NL/ES/IT/PL) |
| **Hauptfluss** | CampaignManager.create(..., languages=["de","en","fr"]) → ContentEngine für jede Sprache → separate GeneratedContent-Objekte → ReviewCLI je Sprache |
| **Ergebnis** | Kampagne mit Items für alle gewählten Sprachen |
