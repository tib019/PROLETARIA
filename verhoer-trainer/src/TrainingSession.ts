/**
 * TrainingSession — verwaltet eine aktive Übungseinheit
 */
import { Scenario, ScenarioTurn, getScenario } from './scenarios';
import { LegalKnowledgeBase } from './LegalKnowledgeBase';

export type ResponseEvaluation = {
  correct: boolean;
  score: number;      // 0–100
  feedback: string;
  legal_explanation: string;
  improvement?: string;
};

export interface SessionResult {
  scenario_id: string;
  total_turns: number;
  correct_turns: number;
  score: number;        // 0–100
  duration_seconds: number;
  turn_results: ResponseEvaluation[];
  summary: string;
  certificate_level?: 'bestanden' | 'nicht_bestanden';
}

export class TrainingSession {
  private scenario: Scenario;
  private currentTurn = 0;
  private turnResults: ResponseEvaluation[] = [];
  private startTime = Date.now();
  private kb = new LegalKnowledgeBase();

  constructor(scenarioId: string) {
    const scenario = getScenario(scenarioId);
    if (!scenario) throw new Error(`Szenario '${scenarioId}' nicht gefunden`);
    this.scenario = scenario;
  }

  get isFinished(): boolean {
    return this.currentTurn >= this.scenario.turns.length;
  }

  get currentQuestion(): ScenarioTurn | null {
    return this.scenario.turns[this.currentTurn] ?? null;
  }

  get progress(): { current: number; total: number; percentage: number } {
    return {
      current: this.currentTurn,
      total: this.scenario.turns.length,
      percentage: Math.round((this.currentTurn / this.scenario.turns.length) * 100),
    };
  }

  /**
   * Bewertet eine Antwort und gibt Feedback zurück.
   * userResponse: was der Nutzende gesagt hat (leer = Schweigen)
   */
  respond(userResponse: string): ResponseEvaluation {
    if (this.isFinished) throw new Error('Sitzung bereits beendet');

    const turn = this.scenario.turns[this.currentTurn];
    const evaluation = this._evaluate(userResponse, turn);

    this.turnResults.push(evaluation);
    this.currentTurn++;

    return evaluation;
  }

  getResult(): SessionResult {
    const correct = this.turnResults.filter(r => r.correct).length;
    const score = Math.round((correct / this.scenario.turns.length) * 100);
    const duration = Math.round((Date.now() - this.startTime) / 1000);

    return {
      scenario_id: this.scenario.id,
      total_turns: this.scenario.turns.length,
      correct_turns: correct,
      score,
      duration_seconds: duration,
      turn_results: this.turnResults,
      summary: this._buildSummary(correct, score),
      certificate_level: score >= 70 ? 'bestanden' : 'nicht_bestanden',
    };
  }

  getHint(): string {
    const turn = this.currentQuestion;
    if (!turn) return '';
    return turn.hint ?? 'Denke an deine Rechte nach § 136 StPO.';
  }

  getLegalNote(): string {
    const turn = this.currentQuestion;
    if (!turn) return '';
    return turn.legal_note ?? '';
  }

  // ------------------------------------------------------------------

  private _evaluate(response: string, turn: ScenarioTurn): ResponseEvaluation {
    const normalized = response.trim().toLowerCase();
    const isSilent = normalized === '' || normalized === 'schweigen' || normalized === 'keine aussage';

    switch (turn.expected_response_type) {
      case 'schweigen':
        return isSilent
          ? {
              correct: true,
              score: 100,
              feedback: 'Richtig! Schweigen ist hier die beste Strategie.',
              legal_explanation: turn.legal_note ?? '',
            }
          : {
              correct: false,
              score: 0,
              feedback: 'Fehler: Du hättest hier schweigen sollen.',
              legal_explanation: turn.legal_note ?? '',
              improvement: 'Übe, in Drucksituationen konsequent zu schweigen.',
            };

      case 'personalien':
        const hasPersonalien =
          (normalized.includes('name') || normalized.includes('adresse') || normalized.includes('geburtsdatum')) &&
          !normalized.includes('beruf') && !normalized.includes('arbeitgeber');
        return hasPersonalien || normalized.includes('personalien')
          ? {
              correct: true,
              score: 100,
              feedback: 'Richtig! Personalien angeben, zur Sache schweigen.',
              legal_explanation: turn.legal_note ?? '',
            }
          : isSilent
          ? {
              correct: false,
              score: 30,
              feedback: 'Zu restriktiv: Personalien müssen angegeben werden (§ 111 OWiG).',
              legal_explanation: turn.legal_note ?? '',
              improvement: 'Gib Name, Adresse, Geburtsdatum an — aber keine weiteren Angaben.',
            }
          : {
              correct: false,
              score: 10,
              feedback: 'Zu viel gesagt. Nur Pflichtangaben (Name, Adresse, Geburtsdatum).',
              legal_explanation: turn.legal_note ?? '',
            };

      case 'rechtsverweis':
        const hasRef = normalized.includes('§') || normalized.includes('stpo') ||
                       normalized.includes('emrk') || normalized.includes('recht') ||
                       normalized.includes('anwalt') || normalized.includes('schweige');
        return hasRef
          ? {
              correct: true,
              score: 100,
              feedback: 'Sehr gut! Klarer Rechtsverweis ist hier korrekt.',
              legal_explanation: turn.legal_note ?? '',
            }
          : isSilent
          ? {
              correct: true,
              score: 70,
              feedback: 'Schweigen ist akzeptabel, ein aktiver Rechtsverweis wäre besser.',
              legal_explanation: turn.legal_note ?? '',
              improvement: 'Formuliere den Rechtsverweis explizit — das schützt besser.',
            }
          : {
              correct: false,
              score: 0,
              feedback: 'Keine sachliche Aussage machen. Auf dein Recht verweisen.',
              legal_explanation: turn.legal_note ?? '',
            };

      case 'anwalt_fordern':
        const demandsLawyer = normalized.includes('anwalt') || normalized.includes('anwältin') ||
                              normalized.includes('verteidiger') || normalized.includes('rechtsbeistand');
        return demandsLawyer
          ? {
              correct: true,
              score: 100,
              feedback: 'Richtig! Anwalt fordern ist hier zwingend notwendig.',
              legal_explanation: turn.legal_note ?? '',
            }
          : {
              correct: false,
              score: 20,
              feedback: 'Du hättest explizit deinen Anwalt / deine Anwältin fordern sollen.',
              legal_explanation: turn.legal_note ?? '',
              improvement: '"Ich bestehe auf sofortigem Anwaltsgespräch." — Diesen Satz üben.',
            };

      case 'frage_zurueckweisen':
        const rejects = normalized.includes('frage') || normalized.includes('unzulässig') ||
                        normalized.includes('136a') || normalized.includes('verboten');
        return rejects
          ? {
              correct: true,
              score: 100,
              feedback: 'Richtig! Diese Frage/Methode zurückweisen und protokollieren.',
              legal_explanation: turn.legal_note ?? '',
            }
          : {
              correct: false,
              score: 0,
              feedback: 'Diese Vernehmungsmethode hätte zurückgewiesen werden sollen.',
              legal_explanation: turn.legal_note ?? '',
            };

      default:
        return { correct: false, score: 0, feedback: 'Unbekannter Typ', legal_explanation: '' };
    }
  }

  private _buildSummary(correct: number, score: number): string {
    const total = this.scenario.turns.length;
    if (score >= 90) {
      return `Ausgezeichnet! ${correct}/${total} Situationen korrekt gemeistert. Du bist gut vorbereitet.`;
    } else if (score >= 70) {
      return `Bestanden. ${correct}/${total} korrekt. Weiterüben — besonders die kritischen Momente.`;
    } else {
      return `Noch nicht bereit. ${correct}/${total} korrekt. Lerne die Rechtsgrundlagen und trainiere konsequentes Schweigen.`;
    }
  }
}
