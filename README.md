# PROLETARIA
## Anti-Palantir Konglomerat — Defensive Überwachungsgegeninfrasktur

*Entwickelt von Tobias Buß | 2026*

---

## Was ist PROLETARIA?

PROLETARIA ist das Dach-Repository des Anti-Palantir Konglomerats.
Es verbindet fünf spezialisierte Module zu einer kohärenten defensiven
Gegenkraft gegen staatliche und kommerzielle Überwachungsinfrastruktur.

**PROLETARIA spiegelt Palantir/Clearview/NSO — aber invertiert:**
Statt Bewegungen zu überwachen, schützt es Bewegungen vor Überwachung.

---

## Module

| Modul | Beschreibung | Repo |
|-------|-------------|------|
| **ANTI-KI** | Narrativanalyse + OPSEC-Zentrum | [tib019/anti-ki](https://github.com/tib019/anti-ki) |
| **ProletariaLLM** | Lokales politisches Sprachmodell | [tib019/proletaria-llm](https://github.com/tib019/proletaria-llm) |
| **Interview Copilot** | Verhör-Training + Job-Interview | [tib019/interview-copilot](https://github.com/tib019/interview-copilot) |
| **OSINT Tool** | Öffentliche Quellen-Analyse | [tib019/osinttoolprolatraion](https://github.com/tib019/osinttoolprolatraion) |
| **Cybersyn 2.0** | Dezentrale Energie-Koordination (Steuerelement) | [tib019/cybersyn2-hamburg](https://github.com/tib019/cybersyn2-hamburg) |

---

## Direkt in PROLETARIA enthaltene Module

```
opsec/               # Defensive Überwachungs-Gegenmodule
  exposure_scanner.py      — Eigene digitale Spuren erkennen
  surveillance_db.py       — Wissensbasis: Palantir, Clearview, NSO, BfV...
  dsgvo_automation.py      — Automatisierte Art.15/17/21-Anfragen
  comm_pattern_analyzer.py — OPSEC-Audit eigener Kommunikationsstruktur
  algedonic.py             — Eskalationsprotokoll (nach Cybersyn/Beer)

verhoer-trainer/     # Verhör-Trainingsmodul (TypeScript)
  src/
    LegalKnowledgeBase.ts  — § 136/55 StPO, Art. 6 EMRK, Notfallskript
    scenarios.ts           — 3 Trainingsszenarien
    TrainingSession.ts     — Turn-basierte Übungseinheit mit Bewertung
    TacticAnalyzer.ts      — Echtzeit-Erkennung von 8 Verhörtaktiken

llm-server/          # ProletariaLLM als REST API
  serve.py                 — FastAPI-Server (lokal via Ollama)

cybersyn/            # Cybersyn 2.0 Steuerelement
  README.md                — Verweis + Integrationsanleitung
```

---

## Schnellstart

```bash
# 1. Repository mit Submodulen klonen
git clone --recurse-submodules https://github.com/tib019/PROLETARIA

# 2. Setup
bash setup.sh

# 3. Stack starten
docker compose up -d
```

---

## OPSEC-Grundprinzipien

1. **Lokal first** — Kein Modul erfordert Cloud-API-Keys
2. **Kein Logging** — Sensible Analysen werden nicht extern gespeichert
3. **Selbst-Audit** — PROLETARIA prüft sich mit eigenen OPSEC-Tools
4. **Dezentralisierung** — Kein Single-Point-of-Failure
5. **Rechtliche Absicherung** — Alle Features basieren auf legalen Mitteln

Siehe [KONGLOMERAT.md](./KONGLOMERAT.md) für vollständige Architektur-Dokumentation.
