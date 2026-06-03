# ADR-002: Lokale LLM-Inferenz via Ollama

**Status:** Akzeptiert  
**Datum:** 2026-06

---

## Kontext

PROLETARIA benötigt LLM-Inferenz für Narrativanalyse, Gegennarrativ-Generierung
und politische Textanalyse. Mögliche Ansätze:

1. **Cloud-API** — OpenAI, Anthropic, Google
2. **Ollama lokal** — Mistral-7B, ProletariaLLM
3. **Selbst-gehostetes Open-Source-Modell** — vLLM, HuggingFace Inference Server

## Entscheidung

**Ollama mit lokalem Mistral-7B / ProletariaLLM** (Option 2).

## Begründung

### OPSEC-Argument (entscheidend)

Cloud-APIs bedeuten: Jeder analysierte Text, jede OPSEC-Anfrage, jedes
Gegennarrativ wird an externe Server gesendet und dort geloggt.

Für Organisationen unter staatlicher Beobachtung ist das inakzeptabel:
- OpenAI/Anthropic unterliegen US-Rechtsprechung (NSL, FISA)
- API-Anfragen sind Metadaten die IP-Adressen, Zeitstempel, Muster preisgeben
- Terms of Service erlauben Datenweitergabe an Behörden in bestimmten Fällen

### Praktisches Argument

Ollama ist einfach zu installieren, unterstützt GPU-Beschleunigung,
und erlaubt Custom Models (ProletariaLLM als fine-getuntes Modell laden).

### Gegenargument (bekannt)

Lokale Inferenz ist langsamer und erfordert Hardware (min. 8GB VRAM für Mistral-7B-Q4).
Für Organisationen ohne GPU: Mistral-7B läuft auch auf CPU, nur langsamer.

## Konsequenzen

- Keine externen API-Keys erforderlich
- Hardware-Anforderungen: min. 16GB RAM, GPU empfohlen
- ProletariaLLM-Modell muss in Ollama importiert werden
- Keine Abhängigkeit von externen Diensten bei Aktionen
