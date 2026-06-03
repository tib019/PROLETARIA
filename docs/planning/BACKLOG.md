# PROLETARIA — Product Backlog

Priorisiert nach: Sicherheitsrelevanz → Nutzbarkeit → Vollständigkeit

---

## Epic 1: OPSEC-Module

| ID | User Story | Punkte | Prio |
|----|-----------|--------|------|
| O-01 | Als Aktivist:in möchte ich einen Text auf Credentials prüfen, damit ich keine Passwörter versehentlich veröffentliche | 3 | 🔴 |
| O-02 | Als OPSEC-Verantwortliche:r möchte ich eine Datei auf EXIF-Daten prüfen, damit GPS-Koordinaten nicht in Fotos eingebettet sind | 5 | 🔴 |
| O-03 | Als Aktivist:in möchte ich die SurveillanceDB nach Land filtern, damit ich weiß welche Akteure in meinem Land aktiv sind | 2 | 🟡 |
| O-04 | Als Jurist:in möchte ich einen Art.-15-Auskunftsbrief gegen Palantir generieren, damit ich schnell eine rechtskonforme Anfrage habe | 3 | 🔴 |
| O-05 | Als OPSEC-Verantwortliche:r möchte ich mein Kommunikationsnetzwerk auditieren, damit ich Zentralisierungsrisiken erkenne | 8 | 🟡 |
| O-06 | Als Aktivist:in möchte ich beim Überschreiten des ROT-Schwellenwerts sofort informiert werden, damit ich Gegenmaßnahmen einleite | 5 | 🔴 |
| O-07 | Als Jurist:in möchte ich überfällige DSGVO-Anfragen automatisch eskalieren, damit keine Frist versäumt wird | 3 | 🟡 |
| O-08 | Als Forscher:in möchte ich neue Überwachungsakteure in die SurveillanceDB eintragen, damit die Wissensbasis aktuell bleibt | 3 | 🟢 |
| O-09 | Als OPSEC-Verantwortliche:r möchte ich Burst-Kommunikationsmuster erkennen, damit Aktions-Timing nicht digital sichtbar ist | 5 | 🟡 |
| O-10 | Als Nutzer:in möchte ich den OpsecAlgedonicChannel nach einem Vorfall zurücksetzen, damit ich den Normalbetrieb bestätigen kann | 2 | 🟡 |

---

## Epic 2: Verhör-Training

| ID | User Story | Punkte | Prio |
|----|-----------|--------|------|
| V-01 | Als Aktivist:in möchte ich das Einsteiger-Szenario "Festnahme auf Demo" spielen, damit ich meine Rechte in einer Stress-Situation abrufe | 5 | 🔴 |
| V-02 | Als Aktivist:in möchte ich nach jedem Turn sofort wissen ob meine Antwort richtig war, damit ich aus Fehlern lerne | 3 | 🔴 |
| V-03 | Als Aktivist:in möchte ich den TacticAnalyzer auf reale Verhörprotokolle anwenden, damit ich Taktiken in echten Situationen erkenne | 8 | 🟡 |
| V-04 | Als Trainer:in möchte ich ein neues Szenario ohne Programmierkenntnisse erstellen, damit die Bibliothek wächst | 8 | 🟢 |
| V-05 | Als Aktivist:in möchte ich mein Zertifikat als PDF exportieren, damit ich meinen Ausbildungsstand dokumentieren kann | 3 | 🟢 |
| V-06 | Als Aktivist:in möchte ich den Notruf-Kontakt (Rote Hilfe) direkt in der App sehen, damit ich im Ernstfall schnell Hilfe finde | 2 | 🔴 |

---

## Epic 3: ProletariaLLM

| ID | User Story | Punkte | Prio |
|----|-----------|--------|------|
| L-01 | Als Nutzer:in möchte ich ProletariaLLM lokal via Ollama starten, damit keine Daten die Organisation verlassen | 5 | 🔴 |
| L-02 | Als Forscher:in möchte ich ProletariaLLM auf neuen Texten fine-tunen, damit das Modell aktuell bleibt | 13 | 🟡 |
| L-03 | Als Aktivist:in möchte ich einen politischen Text auf Narrative analysieren lassen, damit ich Framing erkennen kann | 3 | 🟡 |
| L-04 | Als Jurist:in möchte ich einen Rohtext für einen DSGVO-Brief eingeben und einen verbesserten Entwurf bekommen | 5 | 🟡 |
| L-05 | Als OPSEC-Verantwortliche:r möchte ich eine OPSEC-Einschätzung eines Textes per LLM erhalten | 5 | 🟡 |

---

## Epic 4: Narrativanalyse (ANTI-KI)

| ID | User Story | Punkte | Prio |
|----|-----------|--------|------|
| N-01 | Als Forscher:in möchte ich einen Tweet auf rechte Narrative prüfen, damit ich Desinformation erkenne | 3 | 🟡 |
| N-02 | Als Aktivist:in möchte ich ein wirksames Gegennarrativ zu einer AFD-Aussage generieren, damit ich argumentativ vorbereitet bin | 5 | 🟡 |
| N-03 | Als Forscher:in möchte ich Koordinationsnetzwerke in Neo4j visualisieren, damit ich Verbreitungswege verstehe | 8 | 🟢 |
| N-04 | Als Nutzer:in möchte ich neue Dokumente in den RAG-Vektorstore laden, damit der Kontext aktuell bleibt | 3 | 🟡 |

---

## Epic 5: Integration & DevOps

| ID | User Story | Punkte | Prio |
|----|-----------|--------|------|
| I-01 | Als Entwickler:in möchte ich `docker compose up -d` starten und alle Services laufen, damit der Setup minimal ist | 5 | 🔴 |
| I-02 | Als Entwickler:in möchte ich OSINT-Findings automatisch in ANTI-KI importieren, damit keine manuelle Übergabe nötig ist | 13 | 🟡 |
| I-03 | Als Admin möchte ich PROLETARIA als Tor-Hidden-Service betreiben, damit die IP der Organisation geschützt ist | 13 | 🟢 |
| I-04 | Als Admin möchte ich eine zweite PROLETARIA-Instanz deployen die sich mit der ersten synchronisiert | 21 | 🟢 |

---

## Legende

| Symbol | Priorität |
|--------|-----------|
| 🔴 | Kritisch — sicherheitsrelevant |
| 🟡 | Hoch — Kernfunktionalität |
| 🟢 | Mittel — Erweiterung |

**Story Points:** Fibonacci (1, 2, 3, 5, 8, 13, 21)
