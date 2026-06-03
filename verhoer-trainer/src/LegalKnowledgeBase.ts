/**
 * LegalKnowledgeBase — rechtliche Grundlagen für Verhör-Situationen (DE)
 */

export interface LegalRight {
  norm: string;
  title: string;
  content: string;
  when_to_invoke: string;
  exact_wording?: string;
}

export interface LegalTactic {
  tactic_name: string;
  description: string;
  legal_response: string;
  warning: string;
}

export const LEGAL_RIGHTS: LegalRight[] = [
  {
    norm: '§ 136 StPO',
    title: 'Schweigerecht als Beschuldigte/r',
    content:
      'Beschuldigte sind vor ihrer Vernehmung darüber zu belehren, dass es ihnen freisteht, ' +
      'sich zu der Beschuldigung zu äußern oder nicht zur Sache auszusagen.',
    when_to_invoke:
      'Sofort nach Festnahme oder wenn klar ist, dass man als Beschuldigte/r gilt. ' +
      'Vor jeder inhaltlichen Antwort.',
    exact_wording:
      'Ich mache von meinem Recht Gebrauch, die Aussage zu verweigern. ' +
      'Ich möchte zunächst mit meinem Anwalt / meiner Anwältin sprechen.',
  },
  {
    norm: '§ 55 StPO',
    title: 'Auskunftsverweigerungsrecht für Zeugen',
    content:
      'Jeder Zeuge kann die Auskunft auf solche Fragen verweigern, deren Beantwortung ' +
      'ihm selbst oder einem Angehörigen die Gefahr strafgerichtlicher Verfolgung zuziehen würde.',
    when_to_invoke:
      'Wenn man als Zeuge geladen ist, aber eigene Strafverfolgung drohen könnte. ' +
      'Auch bei Fragen zu Angehörigen und Mitstreiterinnen.',
    exact_wording:
      'Ich verweigere die Auskunft gemäß § 55 StPO, da mir die Beantwortung ' +
      'die Gefahr strafgerichtlicher Verfolgung zuziehen würde.',
  },
  {
    norm: '§ 136a StPO',
    title: 'Verbotene Vernehmungsmethoden',
    content:
      'Verboten sind: Täuschung, Drohung, Versprechen, Erschöpfung, körperliche Einwirkung, ' +
      'Hypnose, Verabreichung von Mitteln, Quälerei, grausame oder erniedrigende Behandlung.',
    when_to_invoke:
      'Bei psychologischem Druck, Drohungen, falschen Versprechungen oder Täuschungsversuchen. ' +
      'Erkenne diese Methoden und benenne sie explizit.',
    exact_wording:
      'Ich weise darauf hin, dass diese Befragungsmethode möglicherweise gegen § 136a StPO verstößt. ' +
      'Ich bitte um sofortige Anwesenheit meines Anwalts / meiner Anwältin.',
  },
  {
    norm: 'Art. 6 EMRK',
    title: 'Recht auf Verteidigung',
    content:
      'Jede Person hat das Recht auf angemessene Zeit und Gelegenheit zur Vorbereitung der Verteidigung ' +
      'und auf Verteidigung durch einen Beistand.',
    when_to_invoke: 'Bei Verweigerung des Anwaltsgesprächs oder unzureichender Vorbereitungszeit.',
    exact_wording:
      'Ich bestehe auf meinem Recht auf anwaltlichen Beistand gemäß Art. 6 EMRK ' +
      'und werde keine weiteren Aussagen machen bis ich mit meiner Anwältin / meinem Anwalt gesprochen habe.',
  },
  {
    norm: '§ 163a StPO',
    title: 'Anwesenheitsrecht des Verteidigers',
    content:
      'Der Verteidiger ist berechtigt, bei richterlichen Untersuchungshandlungen und ' +
      'bei Vernehmungen des Beschuldigten anwesend zu sein.',
    when_to_invoke: 'Bei Vernehmungen — Anwalt hat das Recht anwesend zu sein.',
    exact_wording: 'Ich bestehe auf Anwesenheit meiner Anwältin / meines Anwalts bei dieser Vernehmung.',
  },
];

export const INTERROGATION_TACTICS: LegalTactic[] = [
  {
    tactic_name: 'Reid-Technik / Falsche Freundlichkeit',
    description:
      'Beamte geben sich verständnisvoll, suggerieren dass ein Geständnis hilfreich sei ' +
      'oder bagatellisieren die Tat.',
    legal_response:
      'Freundlichkeit erwidern aber schweigen. Keine emotionale Resonanz auf Sympathieangebote. ' +
      'Merke: Freundlichkeit ist eine Taktik, keine persönliche Beziehung.',
    warning:
      'Jede Äußerung — auch scheinbar harmlose — kann verwendet werden. ' +
      '"Off the record" gibt es nicht.',
  },
  {
    tactic_name: 'Konfrontation mit falschen Beweisen',
    description:
      'Beamte behaupten Beweise zu haben, die sie nicht haben, oder übertreiben deren Bedeutung. ' +
      'In Deutschland legal (§ 136a StPO gilt nur für physische Mittel, nicht für Täuschung über Beweise).',
    legal_response:
      'Nicht einschüchtern lassen. Weiterhin schweigen. ' +
      'Beweise erst gemeinsam mit Anwalt prüfen.',
    warning:
      '"Wir haben alles auf Video" — muss nicht stimmen. Niemals Annahmen über Beweise bestätigen.',
  },
  {
    tactic_name: 'Ermüdungsbefragung',
    description: 'Sehr lange Befragungen ohne Pause, um die Widerstandsfähigkeit zu brechen.',
    legal_response:
      'Pausen verlangen (§ 136 StPO). Nach mehr als X Stunden Unterbrechung fordern. ' +
      'Anwalt verlangen. Bei Erschöpfung explizit auf § 136a StPO hinweisen.',
    warning: 'Erschöpfung ist ein Risikofaktor für unbeabsichtigte Aussagen.',
  },
  {
    tactic_name: 'Minimierung und Normalisierung',
    description:
      '"Das war doch nicht so schlimm", "Alle machen das", ' +
      '"Wenn Sie zugeben, kommen Sie schneller raus."',
    legal_response:
      'Nicht auf Bewertungen eingehen. Schweigen ist keine Schuldanerkenntnis.',
    warning:
      'Aussagen im Affekt ("das war keine große Sache") können rechtlich relevant sein.',
  },
  {
    tactic_name: 'Keil zwischen Mitangeklagte treiben',
    description:
      '"Ihre Freundin hat schon ausgesagt", "Sie werden der einzige sein der schweigt", ' +
      '"Wir bieten Kronzeugenregelung an."',
    legal_response:
      'Keine Aussagen über andere Personen. Solidarität aushalten. ' +
      'Kronzeugenprogramm nur mit Anwalt prüfen.',
    warning: 'Aussagen über andere sind oft schwerwiegender als eigene Aussagen.',
  },
];

export class LegalKnowledgeBase {
  getRights(): LegalRight[] {
    return LEGAL_RIGHTS;
  }

  getTactics(): LegalTactic[] {
    return INTERROGATION_TACTICS;
  }

  getRightByNorm(norm: string): LegalRight | undefined {
    return LEGAL_RIGHTS.find(r => r.norm === norm);
  }

  getEmergencyScript(): string {
    return [
      '═══ NOTFALLSKRIPT — FESTNAHME / VERNEHMUNG ═══',
      '',
      '1. SOFORT SAGEN (ruhig, klar):',
      '   "Ich mache von meinem Schweigerecht Gebrauch.',
      '    Ich möchte meinen Anwalt / meine Anwältin kontaktieren."',
      '',
      '2. PERSONALIEN (nur wenn verpflichtet):',
      '   Name, Adresse, Geburtsdatum — mehr nicht.',
      '',
      '3. AUF KEINE FRAGE ZUR SACHE ANTWORTEN',
      '   Auch nicht "harmlose" Fragen. Auch nicht über andere Personen.',
      '',
      '4. ANWALT VERLANGEN:',
      '   "Ich bestehe auf sofortigem Anwaltsgespräch."',
      '   Rote Hilfe: 030 44 66 66 70',
      '   GFF Notfall: info@freiheitsrechte.org',
      '',
      '5. ALLES BEOBACHTEN:',
      '   Zeit, Ort, Beamtennamen (Dienstnummer), Zeugen.',
      '   Nach Freilassung sofort aufschreiben.',
      '',
      '═══════════════════════════════════════════════',
    ].join('\n');
  }
}
