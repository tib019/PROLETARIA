/**
 * Verhör-Szenarien für das Training
 */

export type Role = 'beschuldigt' | 'zeuge' | 'auskunftsperson';
export type Difficulty = 'einsteiger' | 'fortgeschritten' | 'experte';

export interface ScenarioTurn {
  speaker: 'beamter' | 'anwalt' | 'system';
  text: string;
  expected_response_type: 'schweigen' | 'personalien' | 'rechtsverweis' | 'anwalt_fordern' | 'frage_zurueckweisen';
  hint?: string;
  legal_note?: string;
}

export interface Scenario {
  id: string;
  title: string;
  role: Role;
  difficulty: Difficulty;
  context: string;
  turns: ScenarioTurn[];
  learning_objectives: string[];
}

export const SCENARIOS: Scenario[] = [
  {
    id: 'festnahme_demo',
    title: 'Festnahme auf Demonstration',
    role: 'beschuldigt',
    difficulty: 'einsteiger',
    context:
      'Du wirst nach einer Demonstration festgehalten. Die Beamten behaupten, ' +
      'du hast Widerstand gegen Vollstreckungsbeamte geleistet. Du weißt, dass du nichts getan hast.',
    turns: [
      {
        speaker: 'beamter',
        text: 'Was haben Sie bei der Demo gemacht? Wir brauchen das nur für unsere Unterlagen.',
        expected_response_type: 'schweigen',
        hint: 'Klingt harmlos — ist es nicht. "Nur für die Unterlagen" bedeutet nicht, dass es nicht verwendet wird.',
        legal_note: '§ 136 StPO: Du musst keine Angaben zur Sache machen.',
      },
      {
        speaker: 'beamter',
        text: 'Warum schweigen Sie? Das macht Sie verdächtig. Wenn Sie nichts zu verbergen haben, können Sie doch reden.',
        expected_response_type: 'rechtsverweis',
        hint: 'Schweigen ist ein Recht, keine Schuldanerkenntnis. Dieser Einwand ist eine klassische Drucktaktik.',
        legal_note: 'Schweigen darf nicht zu Lasten der angeklagten Person gewertet werden (BGH-Rechtsprechung).',
      },
      {
        speaker: 'beamter',
        text: 'Ich brauche Ihren Namen und Ihre Adresse.',
        expected_response_type: 'personalien',
        hint: 'Personalien musst du angeben. Mehr nicht.',
        legal_note: '§ 111 OWiG / Polizeigesetze: Identitätsfeststellung ist rechtlich verpflichtend.',
      },
      {
        speaker: 'beamter',
        text: 'Wir haben Sie auf Video. Ihre Freunde haben schon ausgesagt. Sie sind der Letzte.',
        expected_response_type: 'schweigen',
        hint: 'Klassische Reid-Technik. Ob das Video existiert und was die Freunde gesagt haben — unklar. Weiterhin schweigen.',
        legal_note: 'Polizei darf über Beweislage täuschen (im Gegensatz zu anderen verbotenen Methoden in § 136a StPO).',
      },
      {
        speaker: 'beamter',
        text: 'Wenn Sie jetzt kooperieren, kann ich das beim Staatsanwalt erwähnen. Das hilft Ihnen.',
        expected_response_type: 'anwalt_fordern',
        hint: 'Versprechen von Strafmilderung — können Beamte nicht einhalten. Nur ein Gericht kann das.',
        legal_note: 'Versprechungen über Strafmilderung durch Polizeibeamte sind wertlos und eine Drucktaktik.',
      },
    ],
    learning_objectives: [
      'Schweigerecht konsequent anwenden',
      'Drucktaktiken erkennen und nicht reagieren',
      'Unterschied Personalien vs. Sachaussagen kennen',
      'Anwalt-Forderung klar formulieren',
    ],
  },

  {
    id: 'zeuge_hausdurchsuchung',
    title: 'Zeugenbefragung nach Hausdurchsuchung',
    role: 'zeuge',
    difficulty: 'fortgeschritten',
    context:
      'Deine Wohnung wurde durchsucht, du wirst als Zeuge befragt. ' +
      'Es geht um Aktivitäten einer Gruppe, der du angehörst. ' +
      'Strafverfolgung gegen dich ist möglich aber noch nicht eingeleitet.',
    turns: [
      {
        speaker: 'beamter',
        text: 'Sie sind nur Zeuge, nicht Beschuldigte. Als Zeuge müssen Sie aussagen.',
        expected_response_type: 'rechtsverweis',
        hint: '§ 55 StPO: Auch Zeugen dürfen schweigen wenn Selbstbelastung droht. "Nur Zeuge" bedeutet keine Aussagepflicht.',
        legal_note: '§ 55 StPO: Auskunftsverweigerungsrecht für Zeugen bei Selbstbelastungsgefahr.',
      },
      {
        speaker: 'beamter',
        text: 'Kennen Sie Tobias M.? Wann haben Sie ihn zuletzt getroffen?',
        expected_response_type: 'schweigen',
        hint: 'Selbst "Ja ich kenne ihn" kann Weitergehenderes implizieren. Mit § 55 StPO verweigern.',
        legal_note: 'Auch scheinbar harmlose Aussagen über andere Personen können diese belasten.',
      },
      {
        speaker: 'beamter',
        text: 'Was hat Ihre Gruppe bei dem Treffen am 15. März besprochen?',
        expected_response_type: 'rechtsverweis',
        hint: 'Direkte Frage nach Vereinsaktivitäten — klarer Fall für § 55 StPO.',
        legal_note: '§ 55 StPO greift bei jeder Frage, die eigene oder Angehörigen-Strafverfolgung riskiert.',
      },
    ],
    learning_objectives: [
      '§ 55 StPO vs. § 136 StPO unterscheiden',
      'Auch als Zeuge Schweigen durchhalten',
      'Keine Aussagen über andere Personen',
    ],
  },

  {
    id: 'psychologischer_druck',
    title: 'Psychologischer Druck und Ermüdung',
    role: 'beschuldigt',
    difficulty: 'experte',
    context:
      'Du wirst seit 4 Stunden befragt. Die Beamten wechseln ab, ' +
      'einer ist freundlich, einer aggressiv (Good Cop / Bad Cop). ' +
      'Du bist erschöpft.',
    turns: [
      {
        speaker: 'beamter',
        text: 'Hör mal, ich verstehe dich. Ich war auch mal jung und idealistisch. ' +
              'Deine Kumpels haben dich benutzt. Du kannst mir vertrauen.',
        expected_response_type: 'schweigen',
        hint: 'Good Cop — sympathisch aber gefährlich. Vertrauen aufzubauen ist Taktik, nicht Fürsorge.',
        legal_note: 'Emotionale Manipulation ist eine Vernehmungstechnik. § 136a schützt nicht davor.',
      },
      {
        speaker: 'beamter',
        text: '(anderer Beamter) Genug geredet! Sie kooperieren nicht — das wird Konsequenzen haben.',
        expected_response_type: 'rechtsverweis',
        hint: 'Drohung ohne Substanz. Was für Konsequenzen? Schweigen ist legal.',
        legal_note: 'Drohungen ohne rechtliche Grundlage sind unzulässig. Ruhig bleiben und dokumentieren.',
      },
      {
        speaker: 'system',
        text: '[Du bist sehr erschöpft. Die Beamten bieten dir Kaffee an und machen Small Talk.]',
        expected_response_type: 'schweigen',
        hint: 'Small Talk ist keine Pause vom Verhör. Jede Äußerung kann notiert werden.',
        legal_note: 'Du hast das Recht auf Unterbrechung. "Ich bin erschöpft und bestehe auf Pause und Anwalt."',
      },
      {
        speaker: 'beamter',
        text: 'Noch eine Frage — nur eine — dann können Sie gehen: Wo waren Sie am Abend des 8. Mai?',
        expected_response_type: 'schweigen',
        hint: '"Nur eine Frage" ist nie nur eine Frage. Konsequentes Schweigen bis zum Schluss.',
        legal_note: 'Verhörrecht hat keine "letzte Frage"-Ausnahme.',
      },
    ],
    learning_objectives: [
      'Good Cop / Bad Cop erkennen',
      'Auch nach Stunden Schweigen aufrechterhalten',
      'Ermüdung als taktisches Werkzeug erkennen',
      'Recht auf Pause kennen und einfordern',
    ],
  },
];

export function getScenario(id: string): Scenario | undefined {
  return SCENARIOS.find(s => s.id === id);
}

export function getScenariosByDifficulty(difficulty: Difficulty): Scenario[] {
  return SCENARIOS.filter(s => s.difficulty === difficulty);
}
