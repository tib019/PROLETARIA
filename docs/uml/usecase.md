# PROLETARIA — Use-Case-Übersicht

## Akteure und Use Cases

```mermaid
flowchart LR
    subgraph Akteure
        A1[👤 Aktivist:in]
        A2[🔒 OPSEC-Verantwortliche:r]
        A3[⚖️ Jurist:in]
        A4[🔬 Forscher:in]
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

    A1 --> UC1
    A1 --> UC2
    A1 --> UC4
    A1 --> UC10
    A1 --> UC11
    A1 --> UC13

    A2 --> UC1
    A2 --> UC2
    A2 --> UC3
    A2 --> UC6
    A2 --> UC7

    A3 --> UC4
    A3 --> UC5
    A3 --> UC14
    A3 --> UC11

    A4 --> UC7
    A4 --> UC8
    A4 --> UC9
    A4 --> UC3
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
