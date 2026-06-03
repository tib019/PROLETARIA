# ADR-005: TypeScript für verhoer-trainer

**Status:** Akzeptiert  
**Datum:** 2026-06

---

## Kontext

Der Verhör-Trainer soll langfristig in die Electron-App (Interview Copilot)
integriert werden. Die Wahl der Sprache beeinflusst diese Integration direkt.

## Entscheidung

**TypeScript** für `verhoer-trainer/`, obwohl der Rest von PROLETARIA Python ist.

## Begründung

1. **Electron-Integration**: Interview Copilot ist eine Electron/TypeScript-App.
   Ein Python-Modul wäre als Child-Process oder via HTTP anzubinden — unnötige Komplexität.
   TypeScript kann direkt als npm-Paket importiert werden.

2. **Frontend-Nähe**: Die Verhör-Training-UI (Fragen anzeigen, Feedback geben,
   Zertifikat ausstellen) ist Frontend-Code. TypeScript-Logik im selben Paket
   vermeidet eine Python↔JS-Grenze.

3. **Typsicherheit**: Komplexe Datenstrukturen (Scenario, ScenarioTurn, ResponseEvaluation)
   profitieren von TypeScript's statischem Typsystem — weniger Laufzeitfehler.

4. **Kein LLM erforderlich**: Der Verhör-Trainer braucht für Grundfunktionen
   kein LLM (regelbasierte Bewertung). LLM-Integration via `TacticAnalyzer.analyzeWithLLM()`
   ist optional und erfolgt via HTTP-Call zu `llm-server/`.

## Konsequenzen

- Entwickler:innen brauchen Node.js/TypeScript-Kenntnisse für dieses Modul
- Build-Step erforderlich (tsc) vor Integration in Electron
- Python-Entwickler:innen können `TacticAnalyzer`-Logik nicht direkt nutzen —
  aber HTTP-Endpoint in `llm-server/` kann als Bridge dienen
