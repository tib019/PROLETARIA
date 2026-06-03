# ADR-004: DSGVO-Automatisierung als offensives Defensivinstrument

**Status:** Akzeptiert  
**Datum:** 2026-06

---

## Kontext

Überwachungsunternehmen (Clearview, Palantir) und Behörden (BKA, BfV) speichern
massenhaft personenbezogene Daten. Betroffene haben Rechte nach DSGVO —
aber die Durchsetzung ist aufwändig und wird selten systematisch genutzt.

## Entscheidung

**DSGVOAutomation**: Automatisierte Generierung und Verwaltung von DSGVO-Anfragen
als systematisches Gegeninstrument gegen Überwachungsinfrastruktur.

## Begründung

### Rechtliche Stärke

DSGVO-Rechte sind in der EU durchsetzbar mit echten Konsequenzen:
- Bußgelder bis 4% des weltweiten Jahresumsatzes (Art. 83)
- Aufsichtsbehörden haben Prüf- und Sanktionsbefugnisse
- EuGH hat mehrfach pro Betroffenenrechte entschieden (Schrems I+II)

### Strategischer Wert

**Massenhafte Auskunftsanfragen** binden Ressourcen bei Überwachungsakteuren:
- Clearview muss auf jeden Art.-15-Antrag antworten
- BKA/BfV müssen INPOL-Daten offenlegen oder Verweigerung begründen
- Nichtbeantwortung → BfDI-Beschwerde → öffentlicher Druck

**Löschungsanträge** entziehen Daten aus Profiling-Systemen.

**Widerspruch gegen Profiling** (Art. 21) deaktiviert automatisierte Entscheidungen.

### Vergleich mit manueller Durchsetzung

| | Manuell | DSGVOAutomation |
|--|---------|-----------------|
| Zeit pro Anfrage | 1-2h | < 2 Min |
| Fristenverfolgung | Manuell (fehleranfällig) | Automatisch |
| Eskalation | Oft vergessen | Automatisch nach 30 Tagen |
| Skalierbarkeit | Einzeln | Massenhaft |

## Konsequenzen

- Alle generierten Briefe sind rechtlich nicht verbindlich überprüft —
  bei komplexen Fällen Anwalt hinzuziehen
- Massenhafe Anfragen können als Schikane gewertet werden — im Zweifelsfall
  auf echte Betroffenheit beschränken
- Daten werden lokal gespeichert (`data/dsgvo_requests/`) — kein Cloud-Upload
