# UML-Klassendiagramm: Verhör-Trainer

## Vollständiges Klassendiagramm

```mermaid
classDiagram
    direction TB

    %% ─── Enums ───────────────────────────────────────────────
    class Role {
        <<enumeration>>
        USER
        INTERROGATOR
        LAWYER
        ASSISTANT
        SYSTEM
    }

    class Difficulty {
        <<enumeration>>
        BEGINNER
        INTERMEDIATE
        ADVANCED
        EXPERT
    }

    class ScenarioType {
        <<enumeration>>
        POLICE_INTERROGATION
        CUSTOMS_BORDER
        EMPLOYER_QUESTIONING
        CIVIL_INTERROGATION
    }

    class TacticType {
        <<enumeration>>
        GOOD_COP_BAD_COP
        FALSE_EVIDENCE
        MINIMIZATION
        MAXIMIZATION
        ISOLATION
        FATIGUE
        RAPPORT_BUILDING
        REID_TECHNIQUE
        REPETITIVE_QUESTIONING
        BLUFF
        CONFRONTATION
        THEME_DEVELOPMENT
    }

    class EvaluationScore {
        <<enumeration>>
        EXCELLENT
        GOOD
        ACCEPTABLE
        POOR
        DANGEROUS
    }

    class LegalRightType {
        <<enumeration>>
        SCHWEIGERECHT
        ANWALTRECHT
        BELEHRUNGSPFLICHT
        ZEUGENRECHT
        AKTENEINSICHT
        AUSSAGEVERWEIGERUNG_ZEUGE
    }

    %% ─── LegalKnowledgeBase ──────────────────────────────────
    class LegalRight {
        +String id
        +LegalRightType right_type
        +String title
        +String description
        +String legal_basis
        +List~String~ key_phrases
        +String when_to_invoke
        +List~String~ common_mistakes
        +String example_statement
    }

    class LegalTactic {
        +String id
        +String name
        +TacticType tactic_type
        +String description
        +List~String~ indicators
        +String counter_strategy
        +String legal_basis
        +bool is_legal
    }

    class LegalKnowledgeBase {
        -Map~String, LegalRight~ rights
        -Map~String, LegalTactic~ tactics
        +getRightById(id: string) LegalRight
        +getTacticById(id: string) LegalTactic
        +getApplicableRights(scenario_type: ScenarioType) LegalRight[]
        +getRightByType(type: LegalRightType) LegalRight
        +getAllTactics() LegalTactic[]
        +searchRights(query: string) LegalRight[]
        +getCounterStrategy(tactic: TacticType) string
        +getSchweigerecht() LegalRight
        +getAnwaltrecht() LegalRight
        -_loadDefaultRights()
        -_loadDefaultTactics()
    }

    LegalKnowledgeBase "1" --> "*" LegalRight : enthält
    LegalKnowledgeBase "1" --> "*" LegalTactic : enthält
    LegalRight --> LegalRightType : hat
    LegalTactic --> TacticType : hat

    %% ─── Scenario ────────────────────────────────────────────
    class ScenarioTurn {
        +string id
        +Role role
        +string content
        +TacticType detected_tactic
        +string timestamp
        +Map~string, any~ metadata
    }

    class Scenario {
        +string id
        +string title
        +ScenarioType scenario_type
        +Difficulty difficulty
        +string description
        +string context
        +string objective
        +List~ScenarioTurn~ initial_turns
        +List~string~ applicable_rights
        +List~TacticType~ expected_tactics
        +string evaluationCriteria
        +Map~string, string~ hints
    }

    Scenario "1" --> "*" ScenarioTurn : hat initiale
    Scenario --> ScenarioType : ist vom Typ
    Scenario --> Difficulty : hat
    ScenarioTurn --> Role : hat
    ScenarioTurn --> TacticType : erkennt

    %% ─── TrainingSession ─────────────────────────────────────
    class ResponseEvaluation {
        +string response_id
        +EvaluationScore score
        +List~string~ positive_aspects
        +List~string~ negative_aspects
        +List~string~ missed_rights
        +string recommendation
        +bool invoked_schweigepflicht
        +bool invoked_anwaltrecht
        +TacticType detected_tactic_used_against
    }

    class SessionResult {
        +string session_id
        +string scenario_id
        +Difficulty difficulty
        +int total_turns
        +float overall_score
        +List~ResponseEvaluation~ evaluations
        +List~string~ rights_successfully_invoked
        +List~string~ rights_missed
        +List~TacticType~ tactics_recognized
        +List~TacticType~ tactics_missed
        +string final_assessment
        +string improvement_suggestions
        +datetime completed_at
    }

    class TrainingSession {
        -string session_id
        -Scenario scenario
        -List~ScenarioTurn~ history
        -LegalKnowledgeBase legal_kb
        -TacticAnalyzer tactic_analyzer
        -string llm_server_url
        -bool is_active
        -datetime started_at
        +startSession(scenario: Scenario) void
        +submitResponse(response: string) ScenarioTurn
        +evaluateResponse(response: string) ResponseEvaluation
        +getNextInterrogatorTurn() ScenarioTurn
        +getHint() string
        +endSession() SessionResult
        +getHistory() ScenarioTurn[]
        +getCurrentTurn() number
        -_buildPrompt(history: ScenarioTurn[]) string
        -_callLLM(prompt: string) Promise~string~
        -_evaluateWithLLM(response: string, context: string) ResponseEvaluation
        -_detectTactics(turn: ScenarioTurn) TacticType[]
        -_generateInterrogatorResponse() Promise~string~
    }

    TrainingSession --> Scenario : lädt
    TrainingSession --> LegalKnowledgeBase : nutzt
    TrainingSession --> TacticAnalyzer : nutzt
    TrainingSession "1" --> "*" ScenarioTurn : verwaltet
    TrainingSession --> SessionResult : erstellt
    SessionResult "1" --> "*" ResponseEvaluation : enthält
    ResponseEvaluation --> EvaluationScore : hat

    %% ─── TacticAnalyzer ──────────────────────────────────────
    class TacticPattern {
        +string id
        +TacticType tactic_type
        +List~string~ keyword_indicators
        +List~string~ phrase_patterns
        +string description
        +float confidence_threshold
        +string counter_strategy
    }

    class TacticDetection {
        +string id
        +TacticType detected_tactic
        +float confidence
        +List~string~ matched_indicators
        +string explanation
        +string recommended_response
        +string legal_basis
        +datetime detected_at
    }

    class TacticAnalyzer {
        -List~TacticPattern~ patterns
        -LegalKnowledgeBase legal_kb
        -string llm_server_url
        +analyzeTurn(turn: ScenarioTurn) TacticDetection[]
        +detectTactics(text: string) TacticDetection[]
        +getRealTimeAlert(text: string) TacticDetection
        +explainTactic(tactic_type: TacticType) string
        +getCounterStrategy(detection: TacticDetection) string
        +analyzeSession(history: ScenarioTurn[]) TacticDetection[]
        -_matchPatterns(text: string) TacticDetection[]
        -_llmEnhancedAnalysis(text: string) Promise~TacticDetection[]~
        -_calculateConfidence(matches: string[]) float
        -_loadPatterns()
    }

    TacticAnalyzer "1" --> "*" TacticPattern : nutzt
    TacticAnalyzer "1" --> "*" TacticDetection : erstellt
    TacticAnalyzer --> LegalKnowledgeBase : nutzt
    TacticDetection --> TacticType : identifiziert
    TacticPattern --> TacticType : beschreibt

    %% ─── Moduldefinierte Szenarien ───────────────────────────
    class SzenarienKatalog {
        <<static>>
        +SZENARIO_POLIZEIVERHOER: Scenario
        +SZENARIO_ZOLLKONTROLLE: Scenario
        +SZENARIO_ARBEITGEBER: Scenario
        +getAllScenarios() Scenario[]
        +getByDifficulty(d: Difficulty) Scenario[]
        +getByType(t: ScenarioType) Scenario[]
    }

    SzenarienKatalog "1" --> "3" Scenario : definiert
```

---

## Szenarienbeschreibungen

### Szenario 1: Polizeiverhör (POLICE_INTERROGATION)

**Schwierigkeit**: ADVANCED  
**Kontext**: Aktivist:in wird nach einer Demonstration zur Polizeiwache vorgeladen. Beschuldigtenstatus unklar.  
**Ziel**: §136 StPO-Rechte wahrnehmen. Schweigerecht korrekt ausüben. Anwalt anfordern.  
**Erwartete Taktiken**: REID_TECHNIQUE, RAPPORT_BUILDING, FALSE_EVIDENCE, MINIMIZATION  
**Rechtliche Grundlagen**:
- § 136 StPO: Belehrung Beschuldigter
- § 163a StPO: Vernehmung Beschuldigter
- Art. 6 EMRK: Recht auf faires Verfahren

### Szenario 2: Zollkontrolle (CUSTOMS_BORDER)

**Schwierigkeit**: INTERMEDIATE  
**Kontext**: Grenzübergang. Laptop und Handy werden gefordert. Keine klare Rechtsgrundlage genannt.  
**Ziel**: Rechte kennen, kooperieren ohne selbst zu belasten, Grenzen erkennen.  
**Erwartete Taktiken**: ISOLATION, MAXIMIZATION, FATIGUE  
**Rechtliche Grundlagen**:
- § 12 ZollVG
- Grundgesetz Art. 13 (Unverletzlichkeit der Wohnung/Eigentum)

### Szenario 3: Arbeitgeberbefragung (EMPLOYER_QUESTIONING)

**Schwierigkeit**: BEGINNER  
**Kontext**: Arbeitgeber befragt Mitarbeiter:in zu politischen Aktivitäten außerhalb der Arbeitszeit.  
**Ziel**: Grenzen der Auskunftspflicht erkennen. Persönlichkeitsrecht wahren.  
**Erwartete Taktiken**: RAPPORT_BUILDING, THEME_DEVELOPMENT, GOOD_COP_BAD_COP  
**Rechtliche Grundlagen**:
- BDSG § 26: Datenschutz im Beschäftigungsverhältnis
- GG Art. 1/2: Persönlichkeitsrecht

---

## LegalKnowledgeBase — Schlüsselrechte

| Recht | § / Norm | Wann anwenden |
|-------|----------|---------------|
| **Schweigerecht** | § 136 StPO | Sofort bei jeder Vernehmung als Beschuldigte:r |
| **Recht auf Anwalt** | § 137 StPO, Art. 6 EMRK | Unmittelbar nach Feststellung Beschuldigtenstatus |
| **Belehrungspflicht** | § 136 Abs. 1 StPO | Muss vor Vernehmung erfolgen — wenn nicht: Widerspruch |
| **Zeugen-Verweigerung** | § 55 StPO | Wenn Aussage zur Selbstbelastung führen kann |
| **Akteneinsicht** | § 147 StPO | Über Verteidiger:in jederzeit möglich |
