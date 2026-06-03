# ADR-003: Algedonischer Kanal als OPSEC-Eskalationsmodell

**Status:** Akzeptiert  
**Datum:** 2026-06

---

## Kontext

PROLETARIA braucht ein Eskalationsprotokoll das bei erkannten OPSEC-Bedrohungen
automatisch reagiert — ohne dass jede Kleinigkeit menschliche Aufmerksamkeit erfordert,
aber kritische Bedrohungen sofort eskaliert werden.

## Entscheidung

**Stafford Beer's Algedonischer Kanal** (aus Cybersyn, 1972) als konzeptuelles Vorbild
für `OpsecAlgedonicChannel`.

## Hintergrund: Beer's Algedonischer Kanal

Im Cybersyn-Projekt (Chile 1971–73) beschrieb Beer den Algedonischen Kanal als
direkten Bypass-Kanal der normalen Hierarchie: Wenn ein System-Parameter einen
kritischen Schwellenwert überschreitet, wird sofort die höchste Ebene alarmiert —
ohne Filterung durch mittlere Managementebenen.

Der Name kommt vom Griechischen: *algos* (Schmerz) + *hedone* (Freude) —
das System meldet Schmerz (Krise) oder Freude (Normalzustand) direkt.

## Übertragung auf OPSEC

| Cybersyn | PROLETARIA OPSEC |
|----------|------------------|
| Produktionsdaten unter Schwellenwert | OPSEC-Score unter Schwellenwert |
| Algedonischer Alarm → Operationsraum | OPSEC Score ≥ 9 → Notfallprotokoll |
| Bypass der Managementhierarchie | Bypass normaler Kommunikationskanäle |
| Automatische Eskalation | Automatische Gegenmaßnahmen |
| Vier Farb-Stufen (Original) | GRÜN/GELB/ORANGE/ROT |

## Verbindung zu Cybersyn 2.0

Cybersyn 2.0 (tib019/cybersyn2-hamburg) implementiert denselben Algedonischen
Kanal für Energieverteilungsnetze. PROLETARIA übernimmt das Prinzip für
Organisationssicherheit — das ist der konzeptuelle Kern der "Steuerelement"-Rolle
von Cybersyn im Konglomerat.

## Konsequenzen

- Einheitliches Eskalationskonzept über beide Systeme (Energie + OPSEC)
- Schwellenwerte (4/7/9) sind konfigurierbar via `set_response_plan()`
- Exponentiell gewichteter Durchschnitt (α=0.4) verhindert False Positives
- Automatische Maßnahmen bei ROT: Kommunikationsstopp, Anwalt kontaktieren
