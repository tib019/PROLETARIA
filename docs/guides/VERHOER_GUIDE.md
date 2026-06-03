# Verhör-Training Guide

---

## Warum dieses Training?

Polizeiliche Vernehmungen folgen erlernten psychologischen Techniken.
Wer diese Techniken nicht kennt, ist ihnen schutzlos ausgeliefert —
auch wenn man nichts getan hat.

Das Training vermittelt:
1. **Rechtliche Grundlagen** — Was darf die Polizei, was nicht?
2. **Taktiken erkennen** — Good Cop/Bad Cop, falsche Beweise, Minimierung
3. **Konsequent schweigen** — Unter Druck, erschöpft, über Stunden

---

## Rechtliche Grundlagen (Kurzfassung)

| Recht | Norm | Gilt für |
|-------|------|----------|
| Schweigerecht | § 136 StPO | Beschuldigte |
| Auskunftsverweigerung | § 55 StPO | Zeugen (bei Selbstbelastungsgefahr) |
| Anwaltsgespräch | Art. 6 EMRK | Alle |
| Anwalt bei Vernehmung | § 163a StPO | Beschuldigte |
| Verbotene Methoden | § 136a StPO | Alle (Täuschung, Drohung, Erschöpfung) |

**Goldene Regel:** Personalien angeben (Name, Adresse, Geburtsdatum) — alles andere schweigen, bis Anwalt da ist.

**Notfallkontakt:** Rote Hilfe e.V. — 030 44 66 66 70

---

## Szenarien

### Szenario 1: Festnahme auf Demonstration (Einsteiger)

Trainiert: Grundlegendes Schweigerecht, Personalien vs. Sachaussage, Drucktaktiken aushalten.

```typescript
import { TrainingSession, getScenario } from './src';

const session = new TrainingSession('festnahme_demo');

// Aktuelles Scenario abrufen
const question = session.currentQuestion;
console.log(`[${question?.speaker}]: ${question?.text}`);

// Antwort eingeben
const result = session.respond("schweigen");
console.log(`Korrekt: ${result.correct}`);
console.log(`Feedback: ${result.feedback}`);
console.log(`Rechtlicher Hinweis: ${result.legal_explanation}`);

// Tipp wenn unsicher
console.log(`Tipp: ${session.getHint()}`);
```

### Szenario 2: Zeugenbefragung (Fortgeschritten)

Trainiert: § 55 StPO (Zeuge mit Selbstbelastungsrisiko), keine Aussagen über andere.

### Szenario 3: Psychologischer Druck (Experte)

Trainiert: Good Cop/Bad Cop, Ermüdung nach Stunden, "letzte Frage"-Falle.

---

## TacticAnalyzer — Echtzeit-Erkennung

```typescript
import { TacticAnalyzer } from './src';

const analyzer = new TacticAnalyzer(
  'http://localhost:8001'  // Optional: ProletariaLLM für tiefere Analyse
);

// Verhörtext analysieren
const detections = analyzer.analyze(
  "Ich verstehe dich. Ich war auch mal jung und idealistisch. Du kannst mir vertrauen."
);

for (const d of detections) {
  console.log(`[${d.urgency.toUpperCase()}] ${d.tactic}`);
  console.log(`Gegenmaßnahme: ${d.counter}`);
}
// → [BEACHTEN] Good Cop / Empathie-Taktik
// → Gegenmaßnahme: Empathie ist Taktik. Schweige trotz sympathischem Ton.

// Sofortige Handlungsempfehlung
const advice = analyzer.getImmediateAdvice(detections);
console.log(advice);
```

### Mit ProletariaLLM (tiefere Analyse)

```typescript
const result = await analyzer.analyzeWithLLM(verhörtext);
console.log('Pattern-Matching:', result.local);
console.log('LLM-Analyse:', result.llm);
```

---

## Vollständige Trainingseinheit

```typescript
import { TrainingSession, LegalKnowledgeBase } from './src';

async function runTraining() {
  const kb = new LegalKnowledgeBase();

  // Notfallskript ausgeben
  console.log(kb.getEmergencyScript());

  // Training starten
  const session = new TrainingSession('psychologischer_druck');

  while (!session.isFinished) {
    const q = session.currentQuestion!;
    console.log(`\n[${q.speaker.toUpperCase()}]: ${q.text}`);
    console.log(`Progress: ${session.progress.percentage}%`);

    // Eingabe von Nutzer:in
    const userInput = await getUserInput();
    const eval_ = session.respond(userInput);

    console.log(eval_.correct ? '✓ Richtig' : '✗ Falsch');
    console.log(eval_.feedback);
    if (eval_.improvement) console.log(`Verbesserung: ${eval_.improvement}`);
  }

  // Auswertung
  const result = session.getResult();
  console.log(`\n=== Ergebnis ===`);
  console.log(`Score: ${result.score}/100`);
  console.log(`Status: ${result.certificate_level}`);
  console.log(result.summary);
}
```

---

## Neue Szenarien schreiben

```typescript
// In scenarios.ts hinzufügen:
const meinSzenario: Scenario = {
  id: 'razzia_buero',
  title: 'Razzia im Büro',
  role: 'zeuge',
  difficulty: 'fortgeschritten',
  context: 'Das Büro eurer Gruppe wird durchsucht...',
  turns: [
    {
      speaker: 'beamter',
      text: 'Was machen Sie hier?',
      expected_response_type: 'schweigen',
      hint: '§ 55 StPO: Als Zeuge keine Pflicht zur Sachaussage bei Selbstbelastungsrisiko',
      legal_note: 'Auskunftsverweigerungsrecht gilt auch bei Durchsuchungen'
    }
  ],
  learning_objectives: ['§ 55 StPO in Stresssituation anwenden']
};
```
