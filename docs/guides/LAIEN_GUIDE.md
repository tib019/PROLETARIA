# PROLETARIA — Bedienungsanleitung für Einsteiger:innen

**Kein Programmier-Vorwissen nötig.**

---

## Was ist PROLETARIA?

PROLETARIA ist eine Werkzeugkiste für Organisationen und Aktivist:innen
die digital sicherer arbeiten wollen.

Konkret hilft PROLETARIA dabei:

- **Zu wissen ob man überwacht wird** — und von wem
- **Seine Rechte durchzusetzen** — automatisch generierte Briefe an Behörden
- **Auf Verhöre vorbereitet zu sein** — durch Training
- **Desinformation zu erkennen** — politische Texte analysieren lassen

Alles läuft auf deinem eigenen Computer. Nichts geht raus.

---

## Voraussetzungen installieren

### Schritt 1: Docker installieren

Docker ist das Programm das alle Teile von PROLETARIA startet.

→ Gehe auf **https://www.docker.com/products/docker-desktop**  
→ Lade "Docker Desktop" herunter (Windows/Mac/Linux)  
→ Installiere es und starte es  
→ Du siehst ein Wal-Symbol in der Taskleiste — Docker läuft

### Schritt 2: Ollama installieren

Ollama ist das Programm das die KI lokal auf deinem Computer laufen lässt.

→ Gehe auf **https://ollama.ai**  
→ Lade Ollama herunter und installiere es  
→ Öffne das Terminal (Windows: Suche "cmd", Mac: Suche "Terminal")  
→ Tippe: `ollama pull mistral` und drücke Enter  
→ Warte bis der Download fertig ist (ca. 4 GB)

### Schritt 3: Git installieren

Git lädt PROLETARIA von GitHub herunter.

→ Gehe auf **https://git-scm.com**  
→ Lade Git herunter und installiere es

---

## PROLETARIA herunterladen und starten

Öffne das Terminal und tippe folgende Befehle (einen nach dem anderen):

```bash
git clone --recurse-submodules https://github.com/tib019/PROLETARIA
cd PROLETARIA
docker compose up -d
```

Das dauert beim ersten Mal 5-10 Minuten. Danach läuft PROLETARIA.

**Prüfen ob alles läuft:**  
Öffne deinen Browser und gehe auf: **http://localhost:8000/docs**  
Du siehst eine blaue Seite mit "ANTI-KI API" — PROLETARIA läuft.

---

## Die drei wichtigsten Werkzeuge

### Werkzeug 1: OPSEC-Scanner — "Was weiß das Internet über mich?"

**Was macht es?** Prüft Texte und Dateien auf gefährliche Informationen
(Passwörter, GPS-Koordinaten, IP-Adressen, E-Mail-Adressen).

**So benutzt du es:**

1. Öffne **http://localhost:8000/docs** in deinem Browser
2. Klicke auf **POST /api/opsec/exposure-scan**
3. Klicke auf **"Try it out"**
4. Im Feld `text` schreibe den Text den du prüfen möchtest
5. Klicke auf **Execute**
6. Scrolle runter zu **Response** — du siehst das Ergebnis

**Was bedeutet das Ergebnis?**

| Farbe | Bedeutung |
|-------|-----------|
| `"risk_level": "SAUBER"` | Keine Probleme gefunden |
| `"risk_level": "NIEDRIG"` | Kleine Auffälligkeiten, prüfen |
| `"risk_level": "MITTEL"` | Aufpassen, etwas korrigieren |
| `"risk_level": "HOCH"` | Dringend handeln |
| `"risk_level": "KRITISCH"` | Sofort handeln — Passwort/Key gefunden |

---

### Werkzeug 2: DSGVO-Briefe — "Ich will wissen was BKA/Clearview über mich hat"

**Was macht es?** Schreibt automatisch rechtskonforme Briefe an Behörden
und Unternehmen die deine Daten speichern.

**So benutzt du es:**

1. Öffne **http://localhost:8000/docs**
2. Klicke auf **POST /api/opsec/dsgvo/create**
3. Klicke auf **"Try it out"**
4. Fülle das Formular aus:

```json
{
  "request_type": "auskunft",
  "controller": "Bundeskriminalamt (BKA)",
  "controller_address": "Thaerstraße 11, 65193 Wiesbaden",
  "requester_name": "Dein Name",
  "requester_address": "Deine Adresse",
  "subject_description": "Alle über mich gespeicherten Daten"
}
```

5. Klicke auf **Execute**
6. Im **Response** siehst du deinen fertigen Brief unter `"letter"`
7. Kopiere den Brief, drucke ihn aus, unterschreibe ihn und schicke ihn ab

**Wichtige `request_type` Werte:**
- `"auskunft"` — Was habt ihr über mich? (Art. 15 DSGVO)
- `"loeschung"` — Löscht meine Daten! (Art. 17 DSGVO)  
- `"widerspruch"` — Hört auf mich zu analysieren! (Art. 21 DSGVO)

**Bekannte Adressen:**

| Organisation | Adresse |
|-------------|---------|
| BKA | Thaerstraße 11, 65193 Wiesbaden |
| Verfassungsschutz (BfV) | Merianstraße 100, 50765 Köln |
| Clearview AI | privacy@clearview.ai |

---

### Werkzeug 3: Verhör-Training — "Ich will auf eine Polizeibefragung vorbereitet sein"

**Was macht es?** Simuliert ein Polizeiverhör und gibt dir nach jeder
Antwort Feedback ob du deine Rechte richtig genutzt hast.

**So benutzt du es** (Terminal):

```bash
cd PROLETARIA
python3 -c "
from verhoer_trainer.src import TrainingSession
session = TrainingSession('festnahme_demo')
while not session.isFinished:
    q = session.currentQuestion
    print(f'\n[BEAMTER]: {q.text}')
    print(f'Tipp: {session.getHint()}')
    antwort = input('Deine Antwort (oder leer für Schweigen): ')
    result = session.respond(antwort)
    print('✓ RICHTIG' if result.correct else '✗ FALSCH')
    print(result.feedback)
result = session.getResult()
print(f'\nErgebnis: {result.score}/100 — {result.certificate_level}')
"
```

**Die wichtigste Antwort die du lernen sollst:**

> *"Ich mache von meinem Schweigerecht Gebrauch.  
> Ich möchte zunächst mit meinem Anwalt / meiner Anwältin sprechen."*

Das ist immer richtig. Immer.

**Notfallnummer Rote Hilfe:** 030 44 66 66 70

---

## PROLETARIA stoppen und neu starten

**Stoppen:**
```bash
docker compose down
```

**Neu starten:**
```bash
docker compose up -d
```

**Updates holen:**
```bash
git pull
git submodule update --remote
docker compose up -d --build
```

---

## Häufige Fragen

**F: Werden meine Daten irgendwo hochgeladen?**  
A: Nein. Alles läuft lokal auf deinem Computer. Die KI (Ollama) arbeitet offline.

**F: Kann die Polizei sehen dass ich PROLETARIA nutze?**  
A: PROLETARIA selbst sendet nichts nach außen. Wie jede Software auf deinem
Computer ist sie sichtbar wenn jemand physischen Zugang zu deinem Gerät hat.
Für höchste Sicherheit: auf einem verschlüsselten Gerät nutzen.

**F: Ist es legal PROLETARIA zu nutzen?**  
A: Ja. DSGVO-Anfragen sind ein gesetzliches Recht. Sich auf Verhöre vorzubereiten
ist legal. Eigene Sicherheit zu erhöhen ist legal.

**F: Was ist wenn ein DSGVO-Brief nicht beantwortet wird?**  
A: Gehe auf http://localhost:8000/docs → GET /api/opsec/dsgvo/dashboard —
PROLETARIA erinnert dich an überfällige Anfragen und generiert automatisch
einen Eskalationsbrief an die Datenschutzaufsichtsbehörde.

**F: Ich habe einen Fehler — was tun?**  
A: Terminal öffnen, `docker compose logs` eingeben — die Ausgabe zeigt was nicht stimmt.
