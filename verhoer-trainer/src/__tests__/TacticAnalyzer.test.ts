import { describe, expect, it } from "vitest";
import { TacticAnalyzer, type TacticDetection } from "../TacticAnalyzer";

const analyzer = new TacticAnalyzer();

describe("TacticAnalyzer.analyze", () => {
  describe("Erkennung einzelner Taktiken", () => {
    const faelle: Array<[string, string]> = [
      ["Ich verstehe Sie, ich bin kein Feind.", "Good Cop / Empathie-Taktik"],
      ["Das wird Konsequenzen haben.", "Drohung / Bad Cop"],
      ["Wir haben Sie auf Video.", "Falsche Beweise"],
      ["Das ist doch nicht so schlimm, alle machen das.", "Minimierung"],
      ["Kooperation hilft, das ist Ihre letzte Chance.", "Kronzeuge / Kooperationsangebot"],
      ["Alle haben ausgesagt, Sie sind der Einzige der schweigt.", "Solidarität brechen"],
      ["Nur noch eine Frage, dann können Sie gehen.", "Ermüdung / Zeitdruck"],
      ["Wie geht es Ihnen? Möchten Sie einen Kaffee?", "Normalität simulieren / Small Talk"],
    ];

    it.each(faelle)("erkennt in %j die Taktik %s", (text, erwartet) => {
      const namen = analyzer.analyze(text).map(d => d.tactic);
      expect(namen).toContain(erwartet);
    });
  });

  describe("Abgrenzung", () => {
    it("meldet bei neutralem Text keine Taktik", () => {
      expect(analyzer.analyze("Die Vernehmung beginnt um 14 Uhr in Raum 3.")).toEqual([]);
    });

    it("meldet bei leerem Text keine Taktik", () => {
      expect(analyzer.analyze("")).toEqual([]);
    });

    it("erkennt mehrere Taktiken in einem Text getrennt", () => {
      const treffer = analyzer.analyze(
        "Ich verstehe Sie. Aber wir haben Sie auf Video, das hat Konsequenzen."
      );
      const namen = treffer.map(d => d.tactic);

      expect(namen).toContain("Good Cop / Empathie-Taktik");
      expect(namen).toContain("Falsche Beweise");
      expect(namen).toContain("Drohung / Bad Cop");
    });
  });

  describe("Sortierung nach Dringlichkeit", () => {
    it("stellt 'sofort' vor 'beachten' vor 'info'", () => {
      const treffer = analyzer.analyze(
        "Möchten Sie einen Kaffee? Ich verstehe Sie. Wir haben Sie auf Video."
      );
      const rang = { sofort: 0, beachten: 1, info: 2 } as const;
      const folge = treffer.map(d => rang[d.urgency]);

      expect(folge).toEqual([...folge].sort((a, b) => a - b));
    });
  });

  describe("Konfidenzwert", () => {
    const alleTexte = [
      "Ich verstehe Sie, ich bin kein Feind, Sie können mir vertrauen.",
      "Wir haben Sie auf Video.",
      "Wie geht es Ihnen?",
    ];

    it("liegt immer im Intervall [0, 1]", () => {
      const werte = alleTexte.flatMap(t => analyzer.analyze(t)).map(d => d.confidence);

      expect(werte.length).toBeGreaterThan(0);
      for (const w of werte) {
        expect(w).toBeGreaterThan(0);
        expect(w).toBeLessThanOrEqual(1);
      }
    });

    it("steigt, wenn mehr Muster derselben Taktik zutreffen", () => {
      const einTreffer = analyzer.analyze("Ich verstehe Sie.")[0];
      const dreiTreffer = analyzer.analyze(
        "Ich verstehe Sie, ich bin kein Feind, Sie können mir vertrauen."
      )[0];

      expect(dreiTreffer.confidence).toBeGreaterThan(einTreffer.confidence);
    });
  });
});

describe("TacticAnalyzer.getImmediateAdvice", () => {
  it("weist ohne Treffer auf konsequentes Schweigen hin", () => {
    expect(analyzer.getImmediateAdvice([])).toBe(
      "Keine bekannte Taktik erkannt. Weiterhin schweigen."
    );
  });

  it("hebt eine 'sofort'-Taktik hervor, auch wenn sie nicht zuerst uebergeben wird", () => {
    const detections: TacticDetection[] = [
      { tactic: "Small Talk", confidence: 0.5, counter: "Kein Inhalt.", urgency: "info" },
      { tactic: "Falsche Beweise", confidence: 0.8, counter: "Weiter schweigen.", urgency: "sofort" },
    ];

    expect(analyzer.getImmediateAdvice(detections)).toBe(
      "ACHTUNG [Falsche Beweise]: Weiter schweigen."
    );
  });

  it("nennt ohne 'sofort'-Taktik die erste gemeldete Taktik", () => {
    const detections: TacticDetection[] = [
      { tactic: "Minimierung", confidence: 0.5, counter: "Kein Kommentar.", urgency: "beachten" },
    ];

    expect(analyzer.getImmediateAdvice(detections)).toBe(
      "Beachten [Minimierung]: Kein Kommentar."
    );
  });
});

describe("TacticAnalyzer.analyzeWithLLM", () => {
  it("liefert ohne konfigurierte LLM-URL nur die lokale Analyse", async () => {
    const ergebnis = await analyzer.analyzeWithLLM("Wir haben Sie auf Video.");

    expect(ergebnis.llm).toBeUndefined();
    expect(ergebnis.local.map(d => d.tactic)).toContain("Falsche Beweise");
  });

  it("faellt bei nicht erreichbarem LLM auf die lokale Analyse zurueck", async () => {
    // Adresse im reservierten TEST-NET-1-Bereich: garantiert kein Dienst.
    const mitLlm = new TacticAnalyzer("http://192.0.2.1:9");
    const ergebnis = await mitLlm.analyzeWithLLM("Wir haben Sie auf Video.");

    expect(ergebnis.llm).toBeUndefined();
    expect(ergebnis.local.length).toBeGreaterThan(0);
  });
});
