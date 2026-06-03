# C4-Modell Level 1 — Systemkontext: PROLETARIA

## Übersicht

Das Systemkontext-Diagramm zeigt PROLETARIA in seiner Umgebung: Wer nutzt das System, welche externen Systeme interagieren damit, und welche Bedrohungsakteure das System abwehren soll. PROLETARIA ist eine defensive Gegeninfrastruktur — ein Anti-Palantir-Konglomerat für linke Organisationen, Aktivist:innen und politische Strukturen, die Überwachung ausgesetzt sind oder ihr entgegenwirken wollen.

---

## Mermaid-Diagramm

```mermaid
C4Context
    title Systemkontext — PROLETARIA (Anti-Palantir Gegeninfrastruktur)

    Person(aktivist, "Aktivist:in", "Einzelperson, die sich gegen Überwachung schützt, Verhöre trainiert und die eigene digitale Exposition analysiert.")
    Person(opsec_verantwortliche, "OPSEC-Verantwortliche:r", "Sicherheitsbeauftragte:r einer linken Organisation.")
    Person(juristin, "Jurist:in / Rechtsschutz", "Unterstützt bei DSGVO-Eskalationen und rechtlichen Verteidigungsstrategien.")
    Person(forscher, "Forscher:in", "Analysiert Narrative, Desinformation und Überwachungsnetzwerke.")

    System(proletaria, "PROLETARIA", "Anti-Palantir Gegeninfrastruktur. Lokal betriebenes KI-Stack für OPSEC-Analyse, Narrativanalyse, DSGVO-Automatisierung, Verhör-Training und OSINT-Gegenrecherche.")

    System_Ext(palantir, "Palantir / Gotham / Metropolis", "Kommerzielle Überwachungsplattform. Analysiert soziale Netzwerke, politische Aktivitäten, Bewegungsprofile. Primärer Bedrohungsakteur.")
    System_Ext(clearview, "Clearview AI", "Gesichtserkennung. Scrapt öffentliche Bilder. Bedrohungsakteur für physische Exposition.")
    System_Ext(nso, "NSO Group / Pegasus", "Staatliche Spyware. Zielt auf Aktivist:innen und Journalist:innen.")
    System_Ext(bfv, "BfV / Verfassungsschutz", "Inlandsgeheimdienst. Beobachtet politische Organisationen.")
    System_Ext(meta, "Meta / Facebook", "Datenbroker. Profiling, Werbetargeting, Kooperation mit Strafverfolgung.")
    System_Ext(google, "Google / Alphabet", "Datenbroker. E-Mail, Standort, Suche.")

    System_Ext(entso_e, "ENTSO-E / Energiedaten", "Europäische Stromnetzdaten. Wird von Cybersyn 2.0 als read-only Messgröße genutzt (akademisch).")
    System_Ext(dsgvo_behoerde, "Datenschutzbehörde (DSB)", "Aufsichtsbehörde. Empfängt eskalierte DSGVO-Beschwerden.")
    System_Ext(auskunftei, "Auskunftsstelle / Behörde", "Empfängt DSGVO-Anfragen nach Art. 15/17/21 DSGVO.")

    Rel(aktivist, proletaria, "OPSEC-Audit, Verhör-Training, Selbst-OSINT")
    Rel(opsec_verantwortliche, proletaria, "Org-OPSEC, Kommunikationsaudit, DSGVO-Workflow")
    Rel(juristin, proletaria, "DSGVO-Automatisierung, Rechtsvorlagen, Eskalation")
    Rel(forscher, proletaria, "Narrativanalyse, OSINT, Graphdatenbank")

    Rel(proletaria, palantir, "Analysiert als Bedrohungsakteur, erstellt Gegenmaßnahmen", "OSINT read-only")
    Rel(proletaria, clearview, "Dokumentiert in SurveillanceDB, DSGVO-Anfragen", "Analyse / Anfragen")
    Rel(proletaria, nso, "Dokumentiert Angriffsmuster, Schutzempfehlungen", "Analyse read-only")
    Rel(proletaria, bfv, "Dokumentiert, DSGVO-Gegenanfragen", "OSINT / DSGVO")
    Rel(proletaria, meta, "Exposition analysieren, DSGVO Art.15/17", "Analyse / Anfragen")
    Rel(proletaria, google, "Exposition analysieren, DSGVO Art.15/17", "Analyse / Anfragen")

    Rel(proletaria, entso_e, "Liest Energiedaten für Cybersyn-Steuermodell", "HTTP read-only")
    Rel(proletaria, dsgvo_behoerde, "Eskaliert Beschwerden automatisch", "HTTPS / E-Mail")
    Rel(proletaria, auskunftei, "Sendet DSGVO-Anfragen nach Art.15/17/21", "HTTPS / E-Mail")
```

---

## Erläuterung der Akteure

### Primäre Nutzer:innen

| Akteur | Beschreibung | Primäre Module |
|--------|-------------|----------------|
| **Aktivist:in** | Einzelperson, die sich selbst schützen will. Führt Selbst-OSINT durch, trainiert Verhörsituationen, analysiert die eigene digitale Spur. | `opsec/`, `verhoer-trainer/` |
| **OPSEC-Verantwortliche:r** | Sicherheitsbeauftragte:r einer Gruppe oder Organisation. Auditiert Kommunikationsmuster, verwaltet DSGVO-Anfragen, konfiguriert Alarmierungen. | `opsec/`, `modules/osint` |
| **Jurist:in** | Rechtsschutz-Akteur. Nutzt DSGVO-Automatisierung, generiert Anfragebriefe, koordiniert Eskalationen an Aufsichtsbehörden. | `opsec/` (DSGVOAutomation) |
| **Forscher:in** | Analysiert Desinformationskampagnen, Narrative, Überwachungsnetzwerke. Nutzt ANTI-KI und OSINT-Module. | `modules/anti-ki`, `modules/osint` |

### Bedrohungsakteure (externe Systeme — keine Kooperation, nur Analyse)

| System | Typ | Relevanz |
|--------|-----|----------|
| **Palantir / Gotham** | Kommerzielle Massenüberwachungsplattform | Primärer Bedrohungsakteur. PROLETARIA ist explizit als Gegenantwort konzipiert. |
| **Clearview AI** | Biometrische Datenbank | Gefährdet physische Anonymität durch Gesichtserkennung aus öffentlichen Quellen. |
| **NSO Group / Pegasus** | Staatliche Spyware-Infrastruktur | Zielt auf Endgeräte. PROLETARIA dokumentiert bekannte Angriffsvektoren. |
| **BfV / Verfassungsschutz** | Inlandsgeheimdienst Deutschland | Beobachtet legale politische Aktivitäten. DSGVO-Anfragen möglich. |
| **Meta / Google** | Datenbrokernetzwerke | Kooperieren mit Strafverfolgungsbehörden, Massenprofilierung. |

### Externe Systeme (kooperativ / neutral)

| System | Funktion | Nutzungsart |
|--------|----------|-------------|
| **ENTSO-E** | Europäisches Energieverbundnetz | Read-only für Cybersyn 2.0 akademisches Steuermodell |
| **Datenschutzbehörde** | DSGVO-Aufsicht | Empfängt eskalierte Beschwerden nach Art. 77 DSGVO |
| **Auskunftsstellen** | Datenverarbeitende Stellen | Empfangen DSGVO Art.15/17/21-Anfragen |

---

## Designprinzipien im Systemkontext

1. **Lokal-First**: PROLETARIA sendet keine Nutzungsdaten an externe Server. Alle KI-Inferenz läuft lokal via Ollama. Kein Cloud-Logging, kein Telemetrie.
2. **Defensive Offensive**: DSGVO-Anfragen, OSINT-Gegenrecherche und Narrativgegenangriffe sind legale Mittel gegen Überwachungsinfrastruktur.
3. **Kein Vertrauen in Dritte**: Keine API-Keys für OpenAI, Anthropic, Google. Alle Modelle sind lokal und auditierbar.
4. **Algedonisches Prinzip**: Bedrohungen werden automatisch eskaliert — nach dem Vorbild von Stafford Beers Cybersyn-Regelkreis (vgl. ADR-003).
5. **Rechtliche Einbettung**: Jede DSGVO-Aktion ist durch explizite Rechtsgrundlagen (Art. 6, 15, 17, 21 DSGVO; Art. 77 DSGVO) abgesichert.
