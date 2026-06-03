/**
 * TacticAnalyzer — erkennt Verhörtaktiken in Echtzeit
 *
 * Nutzt Pattern-Matching um die aktuell angewandte Taktik zu identifizieren
 * und gibt sofortige Handlungsempfehlungen.
 *
 * Kann mit ProletariaLLM verbunden werden für LLM-basierte Analyse.
 */

export interface TacticDetection {
  tactic: string;
  confidence: number;   // 0–1
  counter: string;
  urgency: 'sofort' | 'beachten' | 'info';
}

interface TacticPattern {
  name: string;
  patterns: RegExp[];
  counter: string;
  urgency: 'sofort' | 'beachten' | 'info';
}

const TACTIC_PATTERNS: TacticPattern[] = [
  {
    name: 'Good Cop / Empathie-Taktik',
    patterns: [
      /verstehe (dich|Sie)/i,
      /kein feind/i,
      /vertrauen/i,
      /ich war auch (mal|jung)/i,
      /als mensch/i,
    ],
    counter: 'Empathie ist Taktik. Schweige trotz sympathischem Ton.',
    urgency: 'beachten',
  },
  {
    name: 'Drohung / Bad Cop',
    patterns: [
      /konsequenzen/i,
      /schwer (wiegen|nehmen)/i,
      /nicht gut (aus|für)/i,
      /bisher haben sie/i,
      /macht Sie verdächtig/i,
    ],
    counter: 'Drohung ohne Substanz. Ruhig bleiben, schweigen, Anwalt fordern.',
    urgency: 'sofort',
  },
  {
    name: 'Falsche Beweise',
    patterns: [
      /(haben|haben wir|wir haben).*(video|foto|zeuge|beweis|aufnahme)/i,
      /auf video/i,
      /bereits bewiesen/i,
      /(mitangeklagte|freunde) haben.*(gesagt|ausgesagt)/i,
    ],
    counter: 'Polizei darf über Beweislage täuschen. Nicht einschüchtern lassen. Weiter schweigen.',
    urgency: 'sofort',
  },
  {
    name: 'Minimierung',
    patterns: [
      /nicht so schlimm/i,
      /kleine (sache|vergehen)/i,
      /alle machen das/i,
      /kann ich (helfen|regeln)/i,
      /wenn Sie zugeben/i,
    ],
    counter: 'Minimierung ist eine Falle. Kein Kommentar zur Einschätzung der Tat.',
    urgency: 'beachten',
  },
  {
    name: 'Kronzeuge / Kooperationsangebot',
    patterns: [
      /kronzeuge/i,
      /beim staatsanwalt erwähnen/i,
      /strafmilderung/i,
      /kooperation (hilft|lohnt)/i,
      /letzte (chance|möglichkeit)/i,
    ],
    counter: 'Versprechungen der Polizei sind unverbindlich. Nur Gericht kann mildern. Erst Anwalt.',
    urgency: 'sofort',
  },
  {
    name: 'Solidarität brechen',
    patterns: [
      /freunde? (haben|hat|schon)/i,
      /einzig(e|er|es)? der schweigt/i,
      /alle haben ausgesagt/i,
      /(benutzt|verraten) (dich|Sie)/i,
    ],
    counter: 'Kann gelogen sein. Solidarität halten. Keine Aussagen über andere.',
    urgency: 'sofort',
  },
  {
    name: 'Ermüdung / Zeitdruck',
    patterns: [
      /nur noch eine frage/i,
      /letzte frage/i,
      /dann können Sie gehen/i,
      /schon so lange/i,
    ],
    counter: '"Letzte Frage" gibt es nicht. Konsequenz bis zum Ende. Recht auf Pause einfordern.',
    urgency: 'beachten',
  },
  {
    name: 'Normalität simulieren / Small Talk',
    patterns: [
      /wie geht es Ihnen/i,
      /wie war Ihr (wochenende|urlaub)/i,
      /kaffee|wasser|pause/i,
      /ganz entspannt/i,
    ],
    counter: 'Small Talk ist kein Pause-Signal. Alles kann notiert werden. Freundlich aber kein Inhalt.',
    urgency: 'info',
  },
];

export class TacticAnalyzer {
  private proletariaUrl?: string;

  constructor(proletariaLlmUrl?: string) {
    this.proletariaUrl = proletariaLlmUrl;
  }

  analyze(text: string): TacticDetection[] {
    const detections: TacticDetection[] = [];

    for (const tactic of TACTIC_PATTERNS) {
      const matches = tactic.patterns.filter(p => p.test(text));
      if (matches.length > 0) {
        const confidence = Math.min(1, matches.length / tactic.patterns.length + 0.3);
        detections.push({
          tactic: tactic.name,
          confidence,
          counter: tactic.counter,
          urgency: tactic.urgency,
        });
      }
    }

    return detections.sort((a, b) => {
      const urgencyOrder = { sofort: 0, beachten: 1, info: 2 };
      return urgencyOrder[a.urgency] - urgencyOrder[b.urgency];
    });
  }

  async analyzeWithLLM(text: string): Promise<{ local: TacticDetection[]; llm?: string }> {
    const local = this.analyze(text);

    if (!this.proletariaUrl) {
      return { local };
    }

    try {
      const resp = await fetch(`${this.proletariaUrl}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, task: 'opsec' }),
      });
      const data = await resp.json() as { analysis: string };
      return { local, llm: data.analysis };
    } catch {
      return { local };
    }
  }

  getImmediateAdvice(detections: TacticDetection[]): string {
    const critical = detections.filter(d => d.urgency === 'sofort');
    if (critical.length === 0 && detections.length === 0) {
      return 'Keine bekannte Taktik erkannt. Weiterhin schweigen.';
    }
    if (critical.length > 0) {
      return `ACHTUNG [${critical[0].tactic}]: ${critical[0].counter}`;
    }
    return `Beachten [${detections[0].tactic}]: ${detections[0].counter}`;
  }
}
