import { describe, expect, it } from "vitest";
import { LegalKnowledgeBase, LEGAL_RIGHTS, INTERROGATION_TACTICS } from "../LegalKnowledgeBase";
import { SCENARIOS, getScenario, getScenariosByDifficulty } from "../scenarios";

const kb = new LegalKnowledgeBase();

describe("LegalKnowledgeBase", () => {
  it("gibt die hinterlegten Rechte zurueck", () => {
    expect(kb.getRights()).toEqual(LEGAL_RIGHTS);
    expect(kb.getRights().length).toBeGreaterThan(0);
  });

  it("gibt die hinterlegten Taktiken zurueck", () => {
    expect(kb.getTactics()).toEqual(INTERROGATION_TACTICS);
  });

  it("findet ein Recht ueber seine Norm", () => {
    const norm = LEGAL_RIGHTS[0].norm;
    expect(kb.getRightByNorm(norm)?.norm).toBe(norm);
  });

  it("liefert fuer eine unbekannte Norm undefined statt zu werfen", () => {
    expect(kb.getRightByNorm("§ 999 Phantasiegesetz")).toBeUndefined();
  });

  it("liefert ein nicht leeres Notfallskript", () => {
    const skript = kb.getEmergencyScript();
    expect(typeof skript).toBe("string");
    expect(skript.trim().length).toBeGreaterThan(0);
  });

  describe("Datenintegritaet", () => {
    it("jedes Recht hat eine eindeutige Norm", () => {
      const normen = LEGAL_RIGHTS.map(r => r.norm);
      expect(new Set(normen).size).toBe(normen.length);
    });

    it("kein Recht hat leere Pflichtfelder", () => {
      for (const r of LEGAL_RIGHTS) {
        expect(r.norm.trim()).not.toBe("");
      }
    });
  });
});

describe("Szenarien", () => {
  it("jede Szenario-ID ist eindeutig", () => {
    const ids = SCENARIOS.map(s => s.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it("getScenario findet jedes hinterlegte Szenario", () => {
    for (const s of SCENARIOS) {
      expect(getScenario(s.id)?.id).toBe(s.id);
    }
  });

  it("getScenario liefert fuer eine unbekannte ID undefined", () => {
    expect(getScenario("gibt-es-nicht")).toBeUndefined();
  });

  it("getScenariosByDifficulty filtert trennscharf", () => {
    for (const stufe of ["einsteiger", "fortgeschritten", "experte"] as const) {
      const treffer = getScenariosByDifficulty(stufe);
      expect(treffer.every(s => s.difficulty === stufe)).toBe(true);
    }
  });

  it("die Summe der Schwierigkeitsstufen ergibt alle Szenarien", () => {
    const summe = (["einsteiger", "fortgeschritten", "experte"] as const)
      .flatMap(stufe => getScenariosByDifficulty(stufe));
    expect(summe.length).toBe(SCENARIOS.length);
  });
});
