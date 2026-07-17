# Research Report: Agile Spec-Driven Development Skill

## Executive Summary

Spec-Driven Development (SDD) ist 2025/2026 zum De-facto-Standard fuer KI-gestuetzte Softwareentwicklung geworden — jedes grosse KI-Coding-Tool (Claude Code, AWS Kiro, GitHub Spec Kit, Cursor) hat eigene SDD-Implementierungen geliefert. Der Kernprinzip ist stabil: Die Spec ist das primaere Artefakt, Code ist Ausgabe. Fuer einen Business-Owner ohne Entwickler-Hintergrund ist AWS Kiros Drei-Phasen-Modell (Requirements.md → Design.md → Tasks.md) der direktest umsetzbare Ansatz. Luecken bestehen vor allem bei Multi-Kunden-Faehigkeit, Betrieb ohne DevOps-Wissen und automatisierter Stakeholder-Kommunikation — diese muessen wir selbst schliessen. Context Engineering (was bekommt der Agent wann zu lesen?) ist die entscheidende Disziplin fuer 2026 und hat direkten Einfluss auf Skill-Qualitaet.

---

## Recherche-Ergebnisse nach Bereich

### 1. Ticket-Workflow & Spec-Driven Development

**Was gibt es:**
- AWS Kiro setzt einen Drei-Phasen-Workflow durch: `requirements.md` (User Stories + EARS-Akzeptanzkriterien), `design.md` (Architektur, Schemas, Sequenzdiagramme), `tasks.md` (diskrete Implementierungsschritte mit Abhakenlogik). KI transformiert Natural-Language-Anforderungen automatisch in dieses Format.
- BCMS Definitive SDD Guide 2026: Spec-First als Workflow — erst Spec schreiben, dann Code generieren lassen. Spec liegt im Repo, wird versioniert, ist primaerer KI-Kontext.
- GitHub Spec Kit (2026) hat ein aehnliches Format etabliert. Claude Codes `/sdd:specify`, `/sdd:plan` Skills (shipped late 2025) machen SDD terminal-nativ.
- EARS-Notation (Easy Approach to Requirements Syntax) fuer Akzeptanzkriterien: "When [Bedingung], the system shall [Aktion]" — beweisbar und KI-lesbar.

**Was fehlt:**
- Kein etabliertes Pattern fuer Ticket-Referenzierung in Code-Kommentaren (`# TICKET-42: ...`) spezifisch fuer KI-Agenten.
- Kein Standard-Template fuer Business-Owner-freundliche Tickets ohne Entwickler-Jargon.

**Beste Quellen:**
- https://kiro.dev/docs/specs/
- https://thebcms.com/blog/spec-driven-development
- https://alexop.dev/posts/spec-driven-development-claude-code-in-action/
- https://agentfactory.panaversity.org/docs/General-Agents-Foundations/spec-driven-development

---

### 2. Architecture Decision Records (ADR)

**Was gibt es:**
- **Nygard-Format** (2011, Klassiker): Titel, Status, Kontext, Entscheidung, Konsequenzen — 5 Felder, minimal. Schwaeche: Verworfene Alternativen werden nicht explizit erfasst.
- **MADR** (Markdown Any Decision Records): Vollstaendiges und minimales Template, annotiert und pur. Listet Alternativen explizit auf — fuer KI-Agenten besser, weil "warum nicht X" dokumentiert ist.
- ADRs gehoeren ins selbe Repo wie der Code, in `docs/adr/` oder `decisions/`, nummeriert (`0001-entscheide-datenbank.md`).
- Unveraenderlich nach Abschluss — neues ADR statt Aenderung. Status: Proposed / Accepted / Deprecated / Superseded.

**Was fehlt:**
- Kein etabliertes Pattern, wie KI-Agenten ADRs *automatisch* erzeugen und aktualisieren sollen.
- Kein Template das Business-Owner-freundlich (ohne Architekt-Sprache) ist.

**Beste Quellen:**
- https://adr.github.io/adr-templates/
- https://github.com/joelparkerhenderson/architecture-decision-record
- https://hidekazu-konishi.com/entry/architecture_decision_records_templates_and_operations.html

---

### 3. Context Engineering & Agent Onboarding

**Was gibt es:**
- **Anthropic selbst** (Artikel: "Effective context engineering for AI agents"): CLAUDE.md soll concise und human-readable sein. Gestaffelte Ladung: Root-File lean + universell, Unterordner-Files tief und spezifisch.
- **AGENTS.md** ist 2026 De-facto-Standard fuer Engineering-Teams; CLAUDE.md fuer Claude-spezifisch. Beide folgen Why/What/How/Progressive-Disclosure-Format.
- **Agentic Context Engineering (ACE)** von Stanford/SambaNova/UC Berkeley: Context als evolving playbook das der Agent selbst aktualisieren kann — Fehlerbericht, Erfolgs-Pattern, Merkliste.
- **Bootstrap-Sequenz Best Practice** (2026): Stateless Session → CLAUDE.md → SPEC → ADRs → aktuelle Tickets → offene Tasks. Jede Schicht erbt Kontext der vorigen.
- **Staged Loading** (Claude Agent SDK Skills): Drei Tiers — sofort geladen, on-demand geladen, nie in Context. Minimiert Token-Verbrauch.
- Anthropic Skills-Repo auf GitHub hat Onboarding-Patterns fuer Managed Agents dokumentiert.

**Was fehlt:**
- Kein standardisiertes "Session-State-Summary"-Format (komprimierter Projektstand fuer neue Session).
- Kein Pattern fuer "Warm Handoff" zwischen KI-Sessions bei laufenden Projekten.

**Beste Quellen:**
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://blog.buildbetter.ai/agents-md-complete-guide-for-engineering-teams-in-2026/
- https://www.humanlayer.dev/blog/writing-a-good-claude-md
- https://claudefa.st/blog/guide/mechanics/claude-md-mastery
- https://github.com/anthropics/skills

---

### 4. Living Documentation

**Was gibt es:**
- **Living Architecture** (ceaksan.com): `architecture.md` Template mit 10 Kernsektionen + 11 optionale Module + 3 Tiefenstufen (L1/L2/L3). Projekt-agnostisch, KI-spezifisch designed.
- AI-powered CHANGELOG-Generatoren (trigger.dev, Lindy.ai, entro314-labs/ai-changelog-generator): Commit-Messages → strukturierter CHANGELOG via KI. MCP-faehig.
- Unterscheidung `CHANGELOG.md` (technisch, Git-basiert) vs. `RELEASE_NOTES.md` (User-Sprache, was wurde besser) ist Best Practice, aber nicht ueberall durchgehalten.
- "Developer Notes" vs. "Change Notes" als separate Artefakte: Developer Notes fuer technische Stakeholder, Change Notes fuer End-Nutzer — kaum etablierte Templates.

**Was fehlt:**
- Kein Workflow der Living Docs automatisch waehrend der KI-Coding-Session aktualisiert (nicht nachtraeglich).
- Kein Business-Owner-Template fuer "Was hat sich fuer den Nutzer geaendert?" in nicht-technischer Sprache.

**Beste Quellen:**
- https://ceaksan.com/en/living-architecture-ai-architectural-documentation
- https://github.com/entro314-labs/AI-Changelog-Generator
- https://trigger.dev/showcase/projects/auto-changelog

---

### 5. AI-First Entwicklung fuer Business-Owner (Non-Developer)

**Was gibt es:**
- Plattform-Boom 2025/2026: Lovable ($300M ARR Jan 2026, 8M User), Bubble, Softr, WeWeb — aber alle erfordern Plattform-Lock-In.
- IBM Bob (April 2026): Enterprise-Tool "From AI-Assisted Coding to Production-Ready Software" — aber Enterprise-Fokus, nicht SMB.
- Kiro ist der naechste Schritt: kein Plattform-Lock-In, aber erfordert VS-Code-Oekosystem. Business-Owner muss trotzdem Terminal-affin sein.
- **Luecke**: Es gibt keinen Workflow der Business-Owners *vollstaendig* ohne Terminal-Arbeit ermaechtigt. Claude Code + strukturierte Specs + MCP-Tools ist aktuell der praktikabelste Hybrid.

**Was fehlt:**
- Template fuer "Business-Owner schreibt Anforderung in Plaintext → KI macht daraus Ticket + Spec + Tasks" vollautomatisch.
- Governance-Muster: Wer genehmigt was, wer entscheidet bei Konflikten zwischen KI-Vorschlag und Business-Intuition?

**Beste Quellen:**
- https://kiro.dev/
- https://apidots.com/guides/ai-software-development-guide-2026/
- https://medium.com/predict/spec-driven-development-with-ai-coding-agents-the-definitive-guide-453fba1baf39

---

### 6. Priorisierungs-Frameworks

**Was gibt es:**
- **RICE**: Reach × Impact × Confidence ÷ Effort = Score. Datenbasiert, gut fuer Roadmap-Entscheidungen. Erweiterung RICE-A: +AI Complexity als 5. Faktor.
- **MoSCoW**: Must / Should / Could / Won't. Scope-Management, gut fuer Sprint-Planung und Stakeholder-Kommunikation. Keine Zahlen noetig.
- **Kano-Model**: Delight vs. Basic vs. Performance Features — hilft bei "Was begeistert Nutzer wirklich".
- Fuer Business-Owner ohne PM-Hintergrund: MoSCoW ist zugaenglicher (kein Scoring), RICE besser fuer datengetriebene Entscheidungen.
- KI kann RICE-Scores vorschlagen wenn Kontext gut dokumentiert ist.

**Was fehlt:**
- Kein etabliertes Format fuer "KI schlaegt Priorisierung vor, Business-Owner bestaetigt/korrigiert".
- Kein leichtgewichtiges Roadmap-File-Format das KI-lesbar und Business-Owner-freundlich ist.

**Beste Quellen:**
- https://marily.substack.com/p/rice-a-a-prioritization-framework
- https://plane.so/blog/feature-prioritization-frameworks-rice-moscow-and-kano-explained
- https://www.productlift.dev/blog/product-prioritization-framework-comparison/

---

### 7. Monitoring & Betrieb

**Was gibt es:**
- Generelle Empfehlungen: strukturierte Logs (JSON), Alert-Schwellenwerte dokumentiert in `ops/monitoring.md`, Fehler-Patterns als KI-lesbare Runbooks.
- Anthropic MCP-Protokoll (97M Installs, Maerz 2026) als Standard fuer KI-Tooling im Betrieb.
- Agentic AI Trends 2026 (MachineLearningMastery): Self-healing Workflows, automatische Fehlerdiagnose wenn Runbooks vorhanden.

**Was fehlt:**
- Kein Standard-Template fuer "Operations Manual" das KI-Agenten fuer Fehlerdiagnose nutzen.
- Kein einfacher Ansatz fuer Business-Owner-freundliches Alerting (keine PagerDuty-Kenntnisse noetig).

**Beste Quellen:**
- https://machinelearningmastery.com/7-agentic-ai-trends-to-watch-in-2026/
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

---

### 8. Test- und Qualitaetsstrategie

**Was gibt es:**
- EARS-Akzeptanzkriterien als direkte Testbasis: "When X, system shall Y" ist direkt in Test-Code uebersetzbar.
- Kiro: Acceptance Criteria sind Teil der Requirements.md — KI generiert Tests aus diesen Kriterien automatisch.
- SDD-Prinzip: KI schreibt Tests *gleichzeitig* mit Code, nicht nachtraeglich.
- "Getestet wird was spezifiziert ist" — was nicht in der Spec steht, ist kein Testfall.

**Was fehlt:**
- Kein einfaches Framework fuer "Was testet die KI automatisch, was entscheidet der Business-Owner zu testen".
- Kein Template fuer Test-Protokoll das nicht-technische Stakeholder lesen koennen.

---

### 9. Stakeholder-Kommunikation

**Was gibt es:**
- Auto-CHANGELOG via KI aus Git-Commits (mehrere Tools verfuegbar, s.o.).
- Trennung Developer Notes / Release Notes / User Change Notes als Konzept vorhanden, aber kaum Template-standardisiert.
- Sprint-Summary-Pattern: Kiro liefert "was wurde diese Iteration gebaut" als strukturiertes Output.

**Was fehlt:**
- Kein Template fuer "Auftraggeber-Update" in nicht-technischer Sprache aus Specs generiert.
- Kein Workflow fuer "User-Feedback → neues Ticket" automatisiert.

---

### 10. Multi-Kunden-Faehigkeit

**Was gibt es:**
- Template-Repos als Starting Point (Taskade, diverse GitHub-Templates).
- Mastra.ai Best Practices: Shared `_shared/` Verzeichnis + Kunden-spezifische Instanz-Verzeichnisse.
- Living Architecture Template: L1/L2/L3 Tiefenstufen koennen als Shared/Customer-spezifisch interpretiert werden.

**Was fehlt:**
- Kein etabliertes Pattern fuer "Skill deployen auf N Kunden-Projekte" in Claude Code Skill-Oekosystem.
- Kein "Inheritance"-Modell fuer CLAUDE.md: globale Regeln + Kunden-Ueberschreibungen.

**Beste Quellen:**
- https://mastra.ai/blog/how-to-structure-projects-for-ai-agents-and-llms
- https://ceaksan.com/en/living-architecture-ai-architectural-documentation

---

## Empfohlenes Vorgehen fuer den Skill

### Was wir direkt uebernehmen

| Konzept | Quelle | Uebernehmen als |
|---|---|---|
| Drei-Phasen-Spec (Requirements / Design / Tasks) | AWS Kiro | Kern-Template: `spec/requirements.md`, `spec/design.md`, `spec/tasks.md` |
| EARS-Akzeptanzkriterien | Kiro / SDD Literatur | Pflichtfeld in Ticket-Template |
| MADR-ADR-Format | adr.github.io | `decisions/NNNN-titel.md` Template |
| Bootstrap-Sequenz | Context Engineering 2026 | CLAUDE.md Section "Agent Bootstrap Order" |
| Staged Loading (3 Tiers) | Anthropic Skills SDK | Skill-interene Dokumenten-Hierarchie |
| MoSCoW fuer Business-Owner | PM Frameworks | `roadmap/backlog.md` Format |
| RICE-A fuer Roadmap-Scoring | RICE-A Erweiterung | Optional — wenn Projekt skaliert |
| Living Architecture Template | ceaksan.com | `architecture.md` als Pflicht-Datei |

### Was wir neu bauen muessen

1. **Business-Owner Ticket-Template**: Plaintext-Anforderung → strukturiertes Ticket mit Akzeptanzkriterien (kein Entwickler-Jargon, kein JIRA-Overhead).
2. **Session-State-Summary-Format**: Komprimierter Projektstand fuer neue KI-Session (`STATUS.md` — letzte 3 Entscheidungen, offene Blocker, naechste Tasks).
3. **Dual-CHANGELOG-System**: `CHANGELOG.md` (technisch, KI-generiert aus Commits) + `CHANGES_FOR_USERS.md` (Business-Sprache, KI-generiert aus Spec-Delta).
4. **Operations Runbook Template**: Fuer KI-Fehlerdiagnose ohne DevOps-Kenntnisse des Business-Owners.
5. **Governance-Schema**: Wer entscheidet was — Business-Owner vs. KI-Autonomie-Bereich klar abgrenzen.
6. **Multi-Kunden-Inheritance**: `_shared/CLAUDE_BASE.md` + `projects/<kunde>/CLAUDE.md` Override-Pattern.

---

## Skill-Struktur (Vorschlag)

```
skills_sources/
  agile-sdd-skill/
    RESEARCH.md                      ← diese Datei
    SKILL.md                         ← Haupt-Skill-Datei (noch zu erstellen)
    templates/
      ticket.md                      ← Ticket-Template (Business-Owner-freundlich)
      spec_requirements.md           ← EARS-basiertes Requirements-Template
      spec_design.md                 ← Design/Architektur-Template
      spec_tasks.md                  ← Tasks-Checkliste-Template
      adr.md                         ← MADR-basiertes ADR-Template
      status.md                      ← Session-State-Summary-Template
      changelog_technical.md         ← Technisches CHANGELOG-Template
      changelog_users.md             ← User-facing Change Notes Template
      roadmap_backlog.md             ← MoSCoW-Backlog-Template
      ops_runbook.md                 ← Operations Runbook Template
      release_notes.md               ← Release Notes fuer Stakeholder
    examples/
      example_ticket.md              ← Ausgefuelltes Beispiel-Ticket
      example_adr.md                 ← Ausgefuelltes Beispiel-ADR
      example_status.md              ← Ausgefuelltes Beispiel-Status-Summary
    SETUP.md                         ← Wie wird der Skill in einem neuen Projekt aktiviert?
```

**Deployment-Pfad:** `~\.claude\skills\agile-sdd-skill\` via `setup.ps1`

**Aktivierung in Projekt-CLAUDE.md:**
```markdown
## Skill: Agile SDD
Dieser Skill ist aktiv. Bootstrap-Sequenz: CLAUDE.md → spec/ → decisions/ → STATUS.md → tickets/open/
```

---

## SKILL.md Inhalts-Outline

Der Skill selbst (`SKILL.md`) soll folgende Sektionen haben:

```
# Agile Spec-Driven Development Skill

## Purpose & Activation
## Agent Bootstrap Sequence (Pflicht-Lesereihenfolge)
## Ticket Workflow (Idee → Spec → Tasks → Done)
## Spec-Driven Development Protocol
## ADR Protocol
## Living Documentation Protocol
## Priorisierung & Roadmap
## Test & Acceptance Protocol
## Stakeholder-Kommunikation
## Operations & Monitoring
## Multi-Kunden-Setup
## Templates Referenz
```

---

## Offene Fragen / Entscheidungen fuer Jakob

### Entscheidung 1: Ticket-System (Kritisch)
**Frage:** Wo leben Tickets — in Markdown-Dateien im Repo, in Trello, oder beides?

- **Option A (Repo-only):** `tickets/open/`, `tickets/done/` — vollstaendig KI-lesbar, kein externes Tool noetig. Nachteil: kein visuelles Board.
- **Option B (Trello+Repo):** Trello als visuelles Board, Ticket-Inhalt im Repo gespiegelt. Nachteil: Synchronisations-Overhead.
- **Option C (Hybrid leichtgewichtig):** Tickets als Markdown im Repo, KI generiert auf Anfrage Trello-Export. Bester Kompromiss?

**Empfehlung:** Option A fuer den Start — weniger Reibung, volle KI-Kontrolle. Spaeter Trello-Sync optional nachrueesten.

---

### Entscheidung 2: Governance — KI-Autonomie-Bereich (Kritisch)
**Frage:** Was darf die KI selbstaendig entscheiden, was braucht deine Bestaetigung?

Beispiel-Abgrenzung:
- KI entscheidet autonom: Implementierungsdetails, Test-Schreiben, CHANGELOG aktualisieren, ADR fuer technische Details
- Jakob bestaetigt: Neue ADRs fuer Architektur-Entscheidungen, Aenderungen an Spec nach Fertigstellung, Release/Deployment, Roadmap-Priorisierung

**Ohne diese Entscheidung** kann der Skill keinen klaren Governance-Abschnitt schreiben.

---

### Entscheidung 3: Scope des ersten Pilot-Projekts (Wichtig)
**Frage:** Auf welchem Projekt soll der Skill zuerst eingesetzt werden?

Der Skill braucht ein Pilot-Projekt um:
- Templates in der Praxis zu validieren
- Den Bootstrap-Flow zu testen
- Feedback fuer SKILL.md-Verfeinerung zu sammeln

Kandidaten aus bekannten Projekten: Termindokumentierer, GuestAI, Immo CRM App, ZeitenAbgleich. Empfehlung: **Immo CRM App** — bereits aktiv, hat STAND.md, bekannte Architektur.

---

### Entscheidung 4: Monitoring-Tiefe (Optional, spaeter entscheidbar)
**Frage:** Wie viel Betrieb-Doku ist Pflicht vs. Optional?

- **Minimal:** Ops Runbook nur fuer Fehler die schon mal aufgetreten sind
- **Standard:** Alle bekannten Failure-Modes vorab dokumentiert
- **Vollstaendig:** Alert-Regeln + Log-Schema + Recovery-Playbooks

Empfehlung: Minimal fuer V1 des Skills, ausbaubar.

---

## Bewertung: Etabliert vs. Experimentell

| Bereich | Status | Direkt umsetzbar ohne Entwickler? |
|---|---|---|
| Spec-First mit Requirements/Design/Tasks | Etabliert (Kiro, SDD 2026) | Ja, mit Templates |
| ADRs (MADR) | Etabliert | Ja, Markdown-Dateien |
| CLAUDE.md Bootstrap-Sequenz | Etabliert | Ja |
| EARS Akzeptanzkriterien | Etabliert | Mit Anleitung ja |
| Auto-CHANGELOG aus Git | Etabliert | Benoetigt minimales Git-Wissen |
| Living Architecture.md | Etabliert (2025) | Ja |
| MoSCoW Backlog | Etabliert | Ja, intuitiv |
| Session-State-Summary | Experimentell / Luecke | Ja, wenn Template gut |
| KI-Governance-Schema | Experimentell / Luecke | Benoetigt Entscheidung von Jakob |
| Multi-Kunden-Inheritance CLAUDE.md | Experimentell / Luecke | Benoetigt Design |
| Dual-CHANGELOG (tech + user) | Teilweise etabliert | Mit Template ja |
| Ops Runbook fuer KI | Experimentell | Mit Template ja |

---

## Quellen

### Spec-Driven Development
- [Chapter 16: Spec-Driven Development with Claude Code | AI Agent Factory](https://agentfactory.panaversity.org/docs/General-Agents-Foundations/spec-driven-development)
- [Spec-Driven Development (SDD): The Definitive 2026 Guide | BCMS](https://thebcms.com/blog/spec-driven-development)
- [From Vibe Coding to Spec-Driven Development | Towards Data Science](https://towardsdatascience.com/from-vibe-coding-to-spec-driven-development/)
- [Spec-Driven Development with AI Coding Agents: The Definitive Guide | Medium](https://medium.com/predict/spec-driven-development-with-ai-coding-agents-the-definitive-guide-453fba1baf39)
- [Using spec-driven development with Claude Code | Heeki Park](https://heeki.medium.com/using-spec-driven-development-with-claude-code-4a1ebe5d9f29)
- [Spec-Driven Development with Claude Code in Action | alexop.dev](https://alexop.dev/posts/spec-driven-development-claude-code-in-action/)
- [Claude Code for Spec-Driven Development | Augment Code](https://www.augmentcode.com/guides/claude-code-spec-driven-development)
- [Spec-Driven Development with Spec Kit and Claude Code | Medium](https://medium.com/vibecodingpub/spec-driven-development-with-spec-kit-and-claude-code-7e2957fd2c9b)
- [Spec-Driven Development: How Kiro and AI Agents Build From Specs | MorphLLM](https://www.morphllm.com/spec-driven-development)
- [Specs - IDE - Docs - Kiro](https://kiro.dev/docs/specs/)
- [AWS Kiro: Why Amazon's Agentic IDE Goes Beyond Vibe Coding | Devoteam](https://www.devoteam.com/expert-view/aws-kiro-beyond-vibe-coding/)
- [From spec to production: drug discovery agent using Kiro | AWS](https://aws.amazon.com/blogs/industries/from-spec-to-production-a-three-week-drug-discovery-agent-using-kiro/)

### Architecture Decision Records
- [ADR Templates | adr.github.io](https://adr.github.io/adr-templates/)
- [Architecture Decision Record Examples | GitHub](https://github.com/joelparkerhenderson/architecture-decision-record)
- [ADR Templates and Operations | hidekazu-konishi.com](https://hidekazu-konishi.com/entry/architecture_decision_records_templates_and_operations.html)
- [Architectural Decision Records | Open Practice Library](https://openpracticelibrary.com/practice/architectural-decision-records-adr/)
- [Nygard Template | GitHub](https://github.com/joelparkerhenderson/architecture-decision-record/blob/main/locales/en/templates/decision-record-template-by-michael-nygard/index.md)

### Context Engineering & Agent Onboarding
- [Effective context engineering for AI agents | Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Context Engineering Best Practices 2026 | Packmind](https://packmind.com/context-engineering-ai-coding/context-engineering-best-practices/)
- [Context Engineering: Complete 2026 Field Guide | Taskade](https://www.taskade.com/blog/context-engineering)
- [AGENTS.md Complete Guide for Engineering Teams 2026 | BuildBetter](https://blog.buildbetter.ai/agents-md-complete-guide-for-engineering-teams-in-2026/)
- [Writing a good CLAUDE.md | HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [CLAUDE.md Mastery | claudefa.st](https://claudefa.st/blog/guide/mechanics/claude-md-mastery)
- [The Complete Guide to AI Agent Memory Files | Medium](https://medium.com/data-science-collective/the-complete-guide-to-ai-agent-memory-files-claude-md-agents-md-and-beyond-49ea0df5c5a9)
- [Implementing CLAUDE.md and Agent Skills | Matthew Groff](https://www.groff.dev/blog/implementing-claude-md-agent-skills)

### Living Documentation & CHANGELOG
- [Living Architecture: Structured Architecture Documentation for AI | ceaksan.com](https://ceaksan.com/en/living-architecture-ai-architectural-documentation)
- [AI Changelog Generator | GitHub entro314-labs](https://github.com/entro314-labs/AI-Changelog-Generator)
- [Generate a changelog from GitHub commits using AI | trigger.dev](https://trigger.dev/showcase/projects/auto-changelog)
- [Automated Changelog Generator Template | Lindy.ai](https://www.lindy.ai/templates/automated-changelog-generator)

### Priorisierungs-Frameworks
- [RICE-A: A Prioritization Framework for AI-Driven Features | Marily Substack](https://marily.substack.com/p/rice-a-a-prioritization-framework)
- [Feature prioritization frameworks: RICE, MoSCoW, and Kano | Plane Blog](https://plane.so/blog/feature-prioritization-frameworks-rice-moscow-and-kano-explained)
- [RICE vs ICE vs MoSCoW Comparison | ProductLift](https://www.productlift.dev/blog/product-prioritization-framework-comparison/)
- [9 Prioritization Frameworks 2025 | Product School](https://productschool.com/blog/product-fundamentals/ultimate-guide-product-prioritization)

### Projektstruktur & Multi-Kunden
- [How to Structure Projects for AI Agents and LLMs | Mastra.ai](https://mastra.ai/blog/how-to-structure-projects-for-ai-agents-and-llms)
- [Agentic AI Frameworks Enterprise Guide 2026 | SpaceO](https://www.spaceo.ai/blog/agentic-ai-frameworks/)

### AI-First fuer Non-Developers
- [AI Software Development 2026: The Complete Business Guide | APIdots](https://apidots.com/guides/ai-software-development-guide-2026/)
- [Introducing IBM Bob: AI Development Partner | IBM Newsroom](https://newsroom.ibm.com/2026-04-28-introducing-ibm-bob-ai-development-partner-that-takes-enterprises-from-ai-assisted-coding-to-production-ready-software)
