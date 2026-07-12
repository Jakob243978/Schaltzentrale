# SDD-Doku State of the Art — Abgleich mit agile-sdd-skill & po-skill

**Datum:** 2026-06-19
**Autor:** Research-Analyst (Agent)
**Scope:** State of the Art der Dokumentation in Spec-Driven Development / Ticket-basiertem Engineering, abgeglichen mit den Remote-Versionen `agile-sdd v0.6` und `po-skill v0.2`. Ergebnis: priorisierte skill_dev-Ticket-Kandidaten.

---

## Executive Summary

Unser SDD-Setup ist gemessen am Stand 2026 **überraschend nah am State of the Art** — in mehreren Punkten sogar voraus. Die Kernidee "Spec ist Quelle der Wahrheit, Code ist Ausgabe" (Tessl, spec-kit, Kiro), EARS-Akzeptanzkriterien, MADR-ADRs, ein bias-freier Verifier in frischer Session, Governance-Log und Empfehlungs-First-Antwortmuster sind alle vorhanden und teils strenger umgesetzt als bei den Referenz-Frameworks. Was uns von der Spitze trennt, sind **vier konkrete, mechanisch fehlende Bausteine**:

1. **Traceability-Matrix (Requirement → Test → Code → Verify)** als ein abfragbares Artefakt fehlt. Wir haben alle Bestandteile (EARS-IDs, `test_ears_N`, `# TICKET-NNN`-Kommentare, Verify-Report), aber keine zusammengeführte Matrix — der industrielle Kern-Hebel für messbare Doku-Qualität (RTM als Phase-Gate).
2. **Spec-Delta / Brownfield-Workflow** (OpenSpec `propose → apply → archive`): Unser `PROJECT_SPEC.md` wird "während der Implementierung aktualisiert", aber es gibt kein Delta-Konzept, das Spec-Änderungen pro Ticket als nachvollziehbares Artefakt führt. ThoughtWorks Radar v34 setzt genau hier den Akzent ("brownfield > greenfield" für reale Projekte).
3. **Cognitive-Debt-Gegenmaßnahmen** — ThoughtWorks Radar v34 (Hauptthema April 2026) warnt explizit, dass KI-generierter Code schneller wächst als das menschliche Verständnis. Unser Setup hat Verifier + Governance-Log, aber kein bewusstes "Mensch-versteht-noch"-Gate (z.B. PROJECT_SPEC-Frischetest, Rationale-Pflicht in Design-Schritt).
4. **Design-Schritt zwischen Spec und Code fehlt formal.** Kiro und spec-kit haben drei Phasen (Requirements → **Design** → Tasks). Wir springen von Ticket-Akzeptanzkriterien direkt zu Code; ADRs decken nur Architektur-Weichen ab, nicht das ticket-lokale "wie genau".

**Top-3-Vorschläge (Priorität Must/Should):**
- **MUST — Traceability-Matrix-Generator** (`agile-sdd`): aus EARS-IDs + Test-Namen + Code-Kommentaren + Verify-Status eine `docs/TRACEABILITY.md` generieren. Größter realer Doku-Qualitäts-Hebel, baut nur auf Vorhandenem auf.
- **SHOULD — Spec-Delta pro Ticket** (`agile-sdd`): jedes Ticket mit Spec-Touch schreibt einen `## Spec-Delta`-Block (was an PROJECT_SPEC additiv geändert wurde), archiviert nach `done`. Schließt OpenSpec-Lücke.
- **SHOULD — Leichtgewichtiger Design-/Approach-Block im Ticket** (`agile-sdd`): optionaler `## Lösungs-Skizze (Approach)`-Abschnitt für M/L/XL-Tickets, der das "wie" festhält, bevor Code entsteht — gegen Cognitive Debt, ohne Kiro-Schwergewicht.

**Über-Engineering-Warnung:** Wir sollten **nicht** arc42-12-Sektionen, RAD-AI-EU-AI-Act-Annex-IV, PRFAQ-Vollprozess oder Multi-Stakeholder-Review-Boards übernehmen. Das ist für ein 1-Personen-KI-Setup Ballast. Der po-skill verbietet PR-Gatekeeper bereits bewusst — richtig so.

---

## SOTA-Befunde (mit Quellen)

### 1. Spec-Driven Development heute — Spec als Quelle der Wahrheit

**Konvergenz 2026:** Alle großen KI-Coding-Stacks sind sich einig, dass chat-first ohne strukturierte Spec in Produktion bei Skalierung versagt. Die drei dominanten Ansätze:

- **GitHub spec-kit** (v0.8.7, Mai 2026, 93k+ Stars, 30+ Agents inkl. Claude Code): 5-Phasen-Pipeline `constitution → specify → plan → tasks → implement`. Kernaussagen aus der `spec-driven.md`:
  - *"The specification becomes the primary artifact. Code becomes its expression."*
  - **`constitution.md`** = "architektonische DNA", unveränderliche Prinzipien (9 Artikel), auf die alle anderen Phasen zurückverweisen. **Das ist exakt unsere po-skill Vision-Constitution** mit `principle_id`-Referenzpflicht.
  - **Test-first erzwungen:** Contract-Tests müssen vor Implementierungscode existieren.
  - **Task-Traceability:** Jeder Task verweist zurück auf Akzeptanzkriterien der Spec; `[P]`-Marker kennzeichnen parallelisierbare Tasks nach Dependency-Analyse.
  - **Living loop:** "Production incidents feed back into specifications for regeneration" — Spec wird re-generiert, nicht der Code gepatcht.
  Quelle: https://github.com/github/spec-kit · https://github.com/github/spec-kit/blob/main/spec-driven.md

- **AWS Kiro** (agentic IDE, Code-OSS): erzwingt drei Phasen **Requirements → Design → Tasks** vor jeder Code-Generierung. `requirements.md` (User Stories + EARS), `design.md` (Architektur, Schemas, Sequenzdiagramme), `tasks.md` (diskrete Schritte mit Abhaken). Der **Design-Zwischenschritt** ist der wesentliche Unterschied zu unserem Setup.
  Quelle: https://kiro.dev/docs/specs/ · https://www.devoteam.com/expert-view/aws-kiro-beyond-vibe-coding/

- **OpenSpec** (ThoughtWorks Radar v34, "worth assessing"): leichtgewichtige Alternative, Workflow `propose → apply → archive`. Kernidee **"spec deltas"** — inkrementelle Spec-Änderungen statt Vollspezifikation, ausdrücklich für **Brownfield** (Bestandssysteme) gedacht. Tool-agnostisch, kein IDE-Lock-in. ThoughtWorks rät, "native Modell-Fähigkeiten weiter zu beobachten, um zu prüfen, ob dediziertes SDD-Tooling überhaupt noch nötig ist".
  Quelle: https://www.thoughtworks.com/en-us/radar/tools/openspec

- **Tessl** "spec-as-source": Spec ist das einzig gepflegte Artefakt, Code ist generiert.
  Quelle: https://www.marktechpost.com/2026/05/08/9-best-ai-tools-for-spec-driven-development-in-2026-kiro-bmad-gsd-and-more-compare/

**ThoughtWorks Technology Radar v34 (April 2026) — Leitmotiv "Cognitive Debt":**
- KI-Coding-Agenten gehören "an die Leine" (harnesses). Zwei Kontroll-Klassen:
  - **Feedforward-Controls** (proaktiv): Agent Skills + Spec-Driven Development.
  - **Feedback-Controls** (reaktiv): Mutation Testing zur Selbstkorrektur *vor* dem menschlichen Review.
- **Cognitive Debt:** "accumulating cognitive debt as AI generates increasingly larger amounts of code" — die Lücke zwischen Entwickler und System wächst. Gegenmittel: Rückbesinnung auf Engineering-Fundamentals (Testbarkeit, DORA-Metriken, Zero-Trust).
- **Mensch nicht aus dem Loop:** "preventing humans from stepping out of the loop despite temptation".
  Quelle: https://www.thoughtworks.com/about-us/news/2026/combat-ai-cognitive-debt-radar-v34 · https://tanatloke.medium.com/thoughtworks-tech-radar-recap-the-ai-refresher-7c90f5bb5827

### 2. Requirements-/Akzeptanz-Notation: EARS vs. Gherkin/BDD

- **EARS** (Easy Approach to Requirements Syntax, Mavin et al., IEEE 2009): "When [Bedingung], the system shall [Aktion]." Constrained Natural Language, **von Mensch UND LLM parsebar** — explizit als KI-tauglich hervorgehoben. Erfasst Preconditions, Trigger, erwartete Systemantwort, deckt Edge-Cases ab, die sonst erst bei der Implementierung auffallen.
- **Gherkin / Given-When-Then (BDD):** Fokus auf *Testbarkeit* — "How to test this feature?". Verhaltensorientiert, nicht implementierungsorientiert.
- **2026-Konsens (komplementär, nicht konkurrierend):** "EARS ist die beste Wahl, wenn die Anforderung lautet 'Das System soll Y unter Bedingung X tun', Gherkin ist ideal für 'Wie teste ich dieses Feature?'". Empfohlene Kette: **User Story (grob) → EARS (Regel) → Gherkin/Given-When-Then (Testszenario)**. Tools konvertieren inzwischen EARS↔Gherkin automatisch.
  Quelle: https://makerneo.com/en/articles/what-is-ears-requirements-syntax-how-to-write-better-ai-prompts.html · https://testquality.com/gherkin-user-stories-acceptance-criteria-guide/ · https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax

- **Definition of Done vs. Definition of Ready vs. Acceptance Criteria** (drei verschiedene Dinge):
  - **DoR** (Definition of Ready, basiert auf INVEST: Independent, Negotiable, Valuable, Estimable, Small, Testable) = Tor *vor* Start: ist das Ticket reif genug, um begonnen zu werden?
  - **AC** (Acceptance Criteria) = "baut das *richtige* Produkt" — pro Ticket.
  - **DoD** (Definition of Done) = "baut das Produkt *richtig*" — projektweiter, releasebarer Standard.
  - Merksatz: AC ist ticket-lokal, DoD ist projektweit, DoR ist das Eintritts-Tor.
  Quelle: https://www.altexsoft.com/blog/acceptance-criteria-definition-of-done/ · https://www.atlassian.com/agile/project-management/definition-of-done

### 3. Design-/Decision-Doku: ADR, RFC, Design Docs, Working Backwards

- **ADR — Nygard (2011) vs. MADR:** Nygard = Context/Decision/Consequences (5 Felder, minimal, **listet verworfene Alternativen nicht** auf). **MADR fixt genau das** — explizite Alternativen-Liste, voll/minimal × annotiert/bar. Best Practices 2026: ein ADR = eine Kern-Entscheidung; ADRs ins Repo nahe am Code/CI; **"the truth of the architecture is the full chain of ADRs, not the latest one"**; ADRs an Code + Tickets + Diagramme verlinken (= Traceability).
  Quelle: https://adr.github.io/ · https://adr.github.io/adr-templates/ · https://www.techtarget.com/searchapparchitecture/tip/4-best-practices-for-creating-architecture-decision-records

- **RFC / Design Docs (Pragmatic Engineer):** Google, Airbnb, Amazon u.a. nutzen RFCs/Design Docs, um Annahmen früh zu klären und Pläne früh zirkulieren zu lassen — *vor* dem Code.
  Quelle: https://blog.pragmaticengineer.com/rfcs-and-design-docs/

- **Stripe (Benchmark für Doku-Kultur):**
  - **"A feature isn't shipped until its documentation is written, reviewed, and published."** Doku-Beiträge zählen in Performance-Reviews und Beförderungen.
  - Design-Docs (~20 Seiten) mit **Stakeholder-Checkboxen am Anfang** (Review-Status sichtbar), asynchrone Debatte im Dokument.
  Quelle: https://newsletter.pragmaticengineer.com/p/stripe-part-2 · https://www.mintlify.com/blog/stripe-docs · https://blog.postman.com/how-stripe-builds-apis/

- **Amazon Working Backwards / PRFAQ:** Pressemitteilung + FAQ aus der Zukunft, *vom Kunden-Outcome rückwärts*. Alignment auf Outcome/Vision statt Features. Schwergewicht — für uns nur als Geist im po-skill (Outcome-Metriken) relevant, nicht als Vollprozess.
  Quelle: https://workingbackwards.com/concepts/working-backwards-pr-faq-process/

- **arc42 / C4 / RAD-AI:** arc42 = 12-Sektionen-Architektur-Template (inkl. Sektion 9 "Architecture Decisions"). **RAD-AI** (ANGE/IEEE ICSA 2026) erweitert arc42 um 8 KI-Sektionen + EU-AI-Act-Annex-IV-Mapping (Enforcement ab 02.08.2026 für High-Risk). → **Für unser Setup Over-Engineering**, aber als Signal relevant: Architektur-Doku für KI-Systeme wird regulatorisch.
  Quelle: https://arxiv.org/abs/2603.28735

### 4. Lean/Agile-Doku: Shape Up, INVEST, "just enough"

- **Shape Up (Basecamp):** "Pitch" = Problem, Appetite (Zeitbudget), Solution, Rabbit Holes, No-Gos. **Appetite** (fixe Zeit, variabler Scope) ist das interessante Konzept — entspricht grob unserem `Geschaetzter Aufwand: XS-XL`, aber Shape Up dreht die Logik um (Zeit fix, Scope flex). "Rabbit Holes / No-Gos" als expliziter Spec-Block fehlt uns.
  Quelle: https://basecamp.com/shapeup/1.5-chapter-06 · https://www.prodify.group/blog/book-report-5-key-takeaways-from-shape-up-by-basecamps-ryan-singer

### 5. Was Doku-Qualität messbar verbessert: Traceability-Matrix

- **Requirements Traceability Matrix (RTM)** ist der industrielle Kern-Hebel:
  - Verknüpft Requirement → Design → Test → Ergebnis, upstream + downstream.
  - **Lebendes Dokument**, das pro Sprint mitwächst (nicht Big-Upfront).
  - Dient als **Phase-Gate-Artefakt** ("nothing slips through the cracks during handoffs"), schafft Audit-Trail für Compliance, ermöglicht datengetriebene Freigabe-Entscheidungen.
  - In regulierten Branchen (Medizintechnik) Pflicht; jedes Requirement muss mit messbaren Daten belegt sein.
  Quelle: https://www.6sigma.us/six-sigma-in-focus/requirements-traceability-matrix-rtm/ · https://www.ketryx.com/blog/the-ultimate-guide-to-requirements-traceability-matrix-rtm · https://testomat.io/blog/the-ultimate-guide-to-rtm-requirements-traceability-matrix/

---

## Gap-Analyse

Legende Bewertung: ✅ SOTA-konform/voraus · 🟡 vorhanden, aber lückenhaft · 🔴 fehlt · ⚪ bewusst out-of-scope (kein Gap)

| Bereich | SOTA-Erwartung | Unser Stand (v0.6 / v0.2) | Bewertung | Lücke / Anmerkung |
|---|---|---|---|---|
| Spec als Quelle der Wahrheit | Spec primär, Code Ausgabe | PROJECT_SPEC + Spec-First-Workflow (C) | ✅ | Konzept da; aber Spec wird "aktualisiert", nicht delta-getrackt (s.u.) |
| Constitution / Vision-Prinzipien | spec-kit `constitution.md`, unveränderlich, referenzpflichtig | po-skill PROJECT_VISION + `vision_principle`-Pflicht + Strict-Mode | ✅ **voraus** | Wir haben zusätzlich 3x-Why, Cooldown, Outcome-Review — über spec-kit hinaus |
| EARS-Akzeptanzkriterien | EARS als KI-parsebare Notation | Pflichtfeld im Ticket, 1 EARS = ≥1 Test | ✅ **voraus** | Strenger als Referenz (Test-Pflicht-Kopplung) |
| Gherkin/Given-When-Then für Tests | komplementär zu EARS für Testszenarien | nicht vorhanden | 🟡 | EARS→Test direkt; Given-When-Then-Zwischenschicht fehlt (geringe Priorität, Could) |
| **Traceability-Matrix (Req→Test→Code→Verify)** | RTM als lebendes Phase-Gate-Artefakt | Bestandteile da (EARS-IDs, `test_ears_N`, `# TICKET-NNN`, Verify-Report), **keine zusammengeführte Matrix** | 🔴 | **Größte Lücke.** Alle Daten vorhanden, nur nie aggregiert |
| **Design-/Approach-Phase** | Kiro/spec-kit: Requirements→**Design**→Tasks | Ticket-AC → direkt Code; ADR nur für Architektur-Weichen | 🔴 | Ticket-lokales "wie" wird nirgends festgehalten → Cognitive-Debt-Risiko |
| **Spec-Delta / Brownfield** | OpenSpec `propose→apply→archive`, spec deltas | PROJECT_SPEC wird inline aktualisiert, kein Delta-Artefakt | 🔴 | Spec-Änderung pro Ticket nicht nachvollziehbar isoliert |
| ADR (MADR, Alternativen explizit) | MADR, immutable, verlinkt | MADR-Format (D), immutable, Governance-Log-Kopplung | ✅ | Konform |
| Test-first / TDD | Tests vor Code (spec-kit erzwingt) | "idealerweise vor Code", zwingend vor Verify | ✅ | Etwas weicher, aber pragmatisch ok |
| Mutation Testing (Feedback-Control) | ThoughtWorks v34: Selbstkorrektur vor Review | nicht vorhanden | 🟡 | Property-Based Testing (F.5) deckt Teil ab; Mutation-Testing fehlt (Could) |
| **Cognitive-Debt-Gate** | Mensch versteht System noch (ThoughtWorks v34) | Verifier + Governance-Log, aber kein "Verständnis"-Check | 🟡 | Kein bewusstes Frische-/Verständnis-Gate auf PROJECT_SPEC |
| Verifier in frischer Session | Bias-Vermeidung | F.4 Verifier-Subagent, frische Session | ✅ **voraus** | Sehr stark; explizite UI-vs-Backend-Klassifikation ist exzellent |
| Living Documentation | CHANGELOG/Release-Notes-Trennung, kontinuierlich | CHANGELOG (tech/user getrennt), ROADMAP, FEATURE_MAP-Generator | ✅ | Auto-Generatoren (TICKET-078/079) sind SOTA |
| "Feature not shipped until docs" (Stripe) | Doku als Ship-Gate | done-Hook regeneriert FEATURE_MAP + Overview | ✅ | Geist erfüllt |
| Decision Log / Governance | Entscheidungen auffindbar | Governance-Log (I) + L.3 Doku-Pflicht | ✅ **voraus** | Sehr ausgereift |
| Priorisierung (RICE/MoSCoW) | datenbasiert + Scope | po-skill RICE + MoSCoW-Fallback | ✅ | Konform |
| Outcome-Verifikation | seltener Standard | po-skill 14-Tage-Outcome-Check | ✅ **voraus** | Über die meisten Frameworks hinaus |
| Parallelisierung | spec-kit `[P]`-Marker, Worktrees | J) Worktrees, disjunkte File-Sets, max 2-3 | ✅ | Konform; `[P]`-Marker im Ticket fehlen (Could) |
| Multi-Stakeholder-Review-Board (Stripe) | Review-Board, Checkboxen | bewusst nicht (1-Personen-Setup) | ⚪ | Richtig weggelassen |
| PRFAQ / Working Backwards Vollprozess | Amazon | nur Outcome-Geist im po-skill | ⚪ | Vollprozess wäre Over-Engineering |
| arc42 12 Sektionen / RAD-AI / EU-AI-Act | Enterprise/reguliert | nicht vorhanden | ⚪ | Over-Engineering für dieses Setup |
| Cost-Tracking pro Ticket | selten | F.6 (5 Pflichtfelder, ccusage, Modell-Gruppierung) | ✅ **weit voraus** | Praktisch einzigartig |

**Zusammenfassung der echten Lücken (priorisiert):**
1. 🔴 Keine zusammengeführte Traceability-Matrix (Daten da, Aggregation fehlt).
2. 🔴 Kein Design-/Approach-Schritt zwischen AC und Code.
3. 🔴 Kein Spec-Delta-Artefakt pro Ticket (Brownfield-Nachvollziehbarkeit).
4. 🟡 Kein bewusstes Cognitive-Debt-/Verständnis-Gate.
5. 🟡 Given-When-Then-Testszenarien und Mutation Testing fehlen (niedrige Priorität).

---

## Priorisierte Vorschläge (skill_dev-Ticket-Kandidaten)

> Verortung: alle als Tickets in `Schaltzentrale\skill_dev\docs\tickets\` (nicht in Projekt-Repos — Memory `feedback_skill_tickets_verortung`). Skill-Quelle: `Schaltzentrale\skills_sources\…`, Deployment via `setup.ps1`.

### MUST

#### SKILL-T-A: Traceability-Matrix-Generator (`docs/TRACEABILITY.md`)
- **Betroffener Skill:** agile-sdd
- **Lernziel / Warum:** Die RTM ist der industrielle Kern-Hebel für *messbare* Doku-Qualität (Six Sigma, Ketryx, Medizintechnik-Compliance) und schließt den ThoughtWorks-v34-"Mensch-im-Loop"-Anspruch ab. Wir besitzen bereits **jeden Bestandteil** verstreut (EARS-IDs im Ticket, `test_ears_N`-Tests, `# TICKET-NNN`-Code-Kommentare, Verify-Report mit `pass/partial/fail`), führen sie aber nie zusammen. Eine generierte Matrix macht auf einen Blick sichtbar: Welcher EARS-Satz hat keinen Test? Welcher Test ist nicht grün? Welcher Code-Pfad ist verwaist? Maximaler Nutzen bei minimalem Neubau.
- **Grobe Akzeptanzkriterien (EARS):**
  - When ein Ticket auf `done` gesetzt wird, the system shall `docs/TRACEABILITY.md` regenerieren (analog FEATURE_MAP-Hook, TICKET-078/079).
  - When ein EARS-Satz keinen zugeordneten `test_ears_N`-Test hat, the system shall die Zeile in der Matrix als `⚠ kein Test` markieren.
  - When ein Verify-Report `fail`/`partial` enthält, the system shall den Status in der Matrix-Zeile spiegeln.
  - When die Matrix generiert wird, the system shall pro Zeile EARS-ID, Ticket, Test-Name, Code-Referenz und Verify-Status führen.
- **Hinweis:** Best-effort (nicht `done` blocken), wie die bestehenden Generatoren. Reine Worker-Logik, kein UI.

### SHOULD

#### SKILL-T-B: Spec-Delta-Block pro Ticket (Brownfield-Nachvollziehbarkeit)
- **Betroffener Skill:** agile-sdd
- **Lernziel / Warum:** OpenSpec (ThoughtWorks v34) zeigt: in Bestandssystemen ist die *Änderung* der Spec das wertvolle Artefakt, nicht die Voll-Spec. Heute aktualisieren wir `PROJECT_SPEC.md` inline — die Änderung verschwindet in der Git-History und ist nicht ticket-lokal nachvollziehbar. Ein `## Spec-Delta`-Block im Ticket (was wurde an PROJECT_SPEC additiv geändert/ergänzt) macht jede Spec-Mutation auffindbar und an das auslösende Ticket gekoppelt — passt exakt zur Governance-Grundregel "kein Fix ohne Ticket".
- **Grobe Akzeptanzkriterien (EARS):**
  - When ein Ticket `PROJECT_SPEC.md` verändert, the system shall im Ticket einen `## Spec-Delta`-Block mit Vorher/Nachher-Kurzfassung führen.
  - When das Ticket auf `done` geht, the system shall den Spec-Delta-Verweis im CHANGELOG `### Technical` referenzieren.
  - When kein Spec-Touch stattfand, the system shall den Block weglassen (optional, kein Zwang).
- **Hinweis:** Bewusst leichtgewichtig (Delta-Notiz, **kein** separates Delta-File pro Ticket wie OpenSpec — das wäre für unser Setup Over-Engineering).

#### SKILL-T-C: Optionaler Lösungs-Skizze-/Approach-Block (Design-Phase light)
- **Betroffener Skill:** agile-sdd
- **Lernziel / Warum:** Kiro und spec-kit haben bewusst eine **Design-Phase** zwischen Requirements und Tasks. Wir springen von Akzeptanzkriterium direkt zu Code — das funktioniert bei XS/S, erzeugt aber bei M/L/XL genau die **Cognitive Debt**, vor der ThoughtWorks v34 warnt (KI baut, Mensch versteht das "wie" nicht mehr). Ein knapper, **nur für M/L/XL verpflichtender** `## Lösungs-Skizze (Approach)`-Block (3-6 Zeilen: gewählter Weg, verworfene Alternative, betroffene Module) hält das "wie" fest, ohne Kiro-Schwergewicht. Bei trivialen Tickets bleibt er weg — kein Overhead.
- **Grobe Akzeptanzkriterien (EARS):**
  - When ein Ticket den Aufwand `M`, `L` oder `XL` hat, the system shall vor Status `in_progress` einen `## Lösungs-Skizze`-Block mit gewähltem Ansatz und mind. einer verworfenen Alternative verlangen.
  - When der gewählte Ansatz eine Architektur-Weiche berührt, the system shall stattdessen auf ein ADR verweisen (kein Doppel-Dokument).
  - When der Aufwand `XS`/`S` ist, the system shall den Block als optional behandeln.
- **Abgrenzung zu ADR:** Approach-Block = ticket-lokales "wie" (vergänglich, im Ticket). ADR = projektweite Architektur-Weiche (immutable, eigenes File). Klare Grenze nötig, damit kein Wildwuchs entsteht.

### COULD

#### SKILL-T-D: Cognitive-Debt-/Spec-Frische-Gate im Bootstrap
- **Betroffener Skill:** agile-sdd
- **Lernziel / Warum:** ThoughtWorks v34 macht "cognitive debt" zum Leitthema. Wir haben bereits einen Frische-Check für FEATURE_MAP/Overview (A.8). Analog ein passiver Hinweis, wenn `PROJECT_SPEC.md` deutlich älter ist als die letzten N done-Tickets ("Spec evtl. hinter der Realität — kurz prüfen?"). Kostet fast nichts, hält Mensch im Loop.
- **Grobe Akzeptanzkriterien (EARS):**
  - When beim Bootstrap die letzte PROJECT_SPEC-Aktualisierung älter als die letzten 5 done-Tickets ist, the system shall einen passiven Hinweis ausgeben (nicht blocken).
- **Begründung Could:** Nutzen real, aber Spec-Delta (T-B) adressiert die Ursache direkter; T-D ist Ergänzung.

#### SKILL-T-E: Given-When-Then als optionale Testszenario-Schicht
- **Betroffener Skill:** agile-sdd
- **Lernziel / Warum:** 2026-Konsens ist EARS (Regel) + Gherkin/Given-When-Then (Testszenario) komplementär. Für Daten-Worker mit kniffligen Edge-Cases könnte ein optionaler Given-When-Then-Block die Test-Ableitung schärfen. **Niedrige Priorität**, weil unsere `1 EARS = 1 Test`-Regel bereits gut funktioniert und Doppel-Notation Overhead erzeugt.
- **Grobe Akzeptanzkriterien (EARS):**
  - When ein Ticket komplexe Edge-Cases hat (Frontmatter-Flag), the system shall pro kritischem EARS-Satz ein Given-When-Then-Szenario zur Testableitung zulassen.
- **Begründung Could / ehrlich:** Gefahr von Notations-Redundanz. Nur einbauen, wenn ein realer Schmerz auftritt — sonst Skill-Bloat.

### Bewusst NICHT vorgeschlagen (Over-Engineering, ehrlich)
- **arc42 / C4 / RAD-AI / EU-AI-Act-Annex-IV:** 12+ Sektionen für ein 1-Personen-KI-Setup = reiner Ballast. PROJECT_SPEC + ADRs reichen.
- **Stripe-Style Multi-Reviewer-Board mit Checkboxen:** widerspricht dem bewusst gewählten 1-Personen-Modell (po-skill verbietet PR-Gatekeeper korrekt).
- **PRFAQ-Vollprozess:** Outcome-Geist ist über po-skill bereits abgedeckt; der Vollprozess ist für interne Tooling-Projekte Theater.
- **Spec-Regeneration ("Code aus Spec neu generieren", Tessl):** zu radikal für laufende Produktions-Workflows; unser inkrementeller Ticket-Ansatz ist sicherer.

---

## Quellenliste

**Spec-Driven Development / Tools**
- GitHub spec-kit — https://github.com/github/spec-kit
- spec-kit `spec-driven.md` — https://github.com/github/spec-kit/blob/main/spec-driven.md
- 9 Best AI Tools for SDD 2026 (MarkTechPost) — https://www.marktechpost.com/2026/05/08/9-best-ai-tools-for-spec-driven-development-in-2026-kiro-bmad-gsd-and-more-compare/
- AWS Kiro Docs — https://kiro.dev/docs/specs/
- AWS Kiro Beyond Vibe Coding (Devoteam) — https://www.devoteam.com/expert-view/aws-kiro-beyond-vibe-coding/
- OpenSpec (ThoughtWorks Radar) — https://www.thoughtworks.com/en-us/radar/tools/openspec
- ThoughtWorks: What is spec-driven development — https://www.thoughtworks.com/insights/podcasts/technology-podcasts/what-is-spec-driven-development

**ThoughtWorks Radar v34 / Cognitive Debt**
- Radar v34 Pressemitteilung — https://www.thoughtworks.com/about-us/news/2026/combat-ai-cognitive-debt-radar-v34
- Radar v34 Recap (Medium) — https://tanatloke.medium.com/thoughtworks-tech-radar-recap-the-ai-refresher-7c90f5bb5827

**EARS / Gherkin / Akzeptanzkriterien**
- EARS für KI-Prompts (MakerNeo) — https://makerneo.com/en/articles/what-is-ears-requirements-syntax-how-to-write-better-ai-prompts.html
- EARS (Wikipedia) — https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax
- Gherkin Acceptance Criteria Guide 2026 (TestQuality) — https://testquality.com/gherkin-user-stories-acceptance-criteria-guide/
- DoD vs DoR vs AC (AltexSoft) — https://www.altexsoft.com/blog/acceptance-criteria-definition-of-done/
- Definition of Done (Atlassian) — https://www.atlassian.com/agile/project-management/definition-of-done

**ADR / RFC / Design Docs**
- ADR GitHub Org — https://adr.github.io/
- ADR Templates (MADR/Nygard) — https://adr.github.io/adr-templates/
- 8 Best Practices for ADRs (TechTarget) — https://www.techtarget.com/searchapparchitecture/tip/4-best-practices-for-creating-architecture-decision-records
- RFCs and Design Docs (Pragmatic Engineer) — https://blog.pragmaticengineer.com/rfcs-and-design-docs/

**Stripe / Working Backwards**
- Inside Stripe's Engineering Culture Part 2 (Pragmatic Engineer) — https://newsletter.pragmaticengineer.com/p/stripe-part-2
- How Stripe creates the best documentation (Mintlify) — https://www.mintlify.com/blog/stripe-docs
- How Stripe Builds APIs (Postman) — https://blog.postman.com/how-stripe-builds-apis/
- Working Backwards PR/FAQ — https://workingbackwards.com/concepts/working-backwards-pr-faq-process/

**arc42 / C4 / RAD-AI**
- RAD-AI: Rethinking Architecture Documentation for AI (arXiv) — https://arxiv.org/abs/2603.28735

**Lean/Agile-Doku**
- Shape Up: Write the Pitch (Basecamp) — https://basecamp.com/shapeup/1.5-chapter-06
- Shape Up Key Takeaways (Prodify) — https://www.prodify.group/blog/book-report-5-key-takeaways-from-shape-up-by-basecamps-ryan-singer

**Traceability-Matrix**
- RTM in Six Sigma — https://www.6sigma.us/six-sigma-in-focus/requirements-traceability-matrix-rtm/
- Ultimate Guide to RTM (Ketryx) — https://www.ketryx.com/blog/the-ultimate-guide-to-requirements-traceability-matrix-rtm
- RTM Guide (Testomat) — https://testomat.io/blog/the-ultimate-guide-to-rtm-requirements-traceability-matrix/
