---
vision_principle: lessons-aus-live-use-zurueckfuehren
outcome_metric: workflow_readability_score
outcome_review_at: null
---

# SKILL-010: n8n-human-readable — Prettify-Skill fuer lesbare Workflows

**Status:** idea
**Erstellt:** 2026-05-29
**MoSCoW:** Should
**Geschaetzter Aufwand:** L

> [!info] Trigger-Live-Erfahrung
> Bewerbung-Bot wurde am 2026-05-28 von 10 Nodes (v0.5.5) auf 33 Nodes
> (v0.7.2) erweitert — Reader-Pfad, Classifier, Switch-Verzweigung,
> Standort-Lookup, Top-Score-Loop. **Null Sticky Notes, keine Sektions-
> Headlines, keine Lane-Trennung, mehrere parallele Tracks ueberlappen
> visuell** (Reader-Sub-Agent-Block bei `y=250` kollidiert visuell mit
> Filter-Pfad). Workflow erfuellt das Vision-Prinzip
> `visuelle-nachvollziehbarkeit` nur noch theoretisch — ohne Doku
> lesen ist die Switch-Pfad-Bedeutung (qualified vs. unqualified vs.
> incomplete) nicht erkennbar.

## Was soll erreicht werden? (Business-Ziel)

Workflows in `workflows/prod/` und `workflows/experiment/` sollen so
layoutet, kommentiert und gruppiert sein, dass Jakob (oder ein
Implementer-Subagent) sie in 6 Monaten **ohne Doku-Lesen** verstehen
kann. Der Skill verwandelt das heutige "Vision-Prinzip"
`visuelle-nachvollziehbarkeit` von einer Mahnung in ein automatisch
herstellbares Werkzeug — vergleichbar mit `black`/`prettier` fuer Code.

## Akzeptanzkriterien (EARS-Format)

- [ ] When ein Workflow > 15 Nodes hat, the system shall beim
      `/n8n-readability-audit <workflow-id>`-Aufruf mindestens 1 Sticky
      Note pro logischer Sektion (Input / Routing / Processing / Output)
      vorschlagen oder als Verstoss melden.
- [ ] When eine IF- oder Switch-Verzweigung mit >= 2 Output-Pfaden im
      Workflow existiert, the system shall pruefen ob jeder Pfad per
      Naming-Konvention (`[true] Branch-Name`, `[false] Branch-Name`)
      ODER per benachbarter Sticky Note semantisch beschriftet ist;
      sonst Verstoss melden.
- [ ] When `/n8n-prettify <workflow-id>` ausgefuehrt wird, the system
      shall (a) eine Reorganisations-Vorschau erzeugen (Lane-Layout
      Top-to-Bottom, ein Track pro Switch-Output), (b) Sticky-Note-
      Drafts pro Sektion erzeugen, (c) Diff zur aktuellen Position
      anzeigen — **niemals direkt in die Live-Instanz schreiben ohne
      Jakobs Bestaetigung**.
- [ ] When der Prettify-Lauf endet, the system shall einen
      `readability_score` (0-100) ausgeben, der mindestens diese
      Faktoren wiegt: Sticky-Note-Coverage, Branch-Label-Coverage,
      Knoten-Pro-Sektion, Lane-Konsistenz, Naming-Konvention-
      Compliance. Score-Definition versionert in `patterns/scoring.md`.
- [ ] When ein Workflow als `template: true` markiert ist (verkaufbar),
      the system shall bei `readability_score < 70` einen Hard-Block
      gegen `versions/`-Snapshot werfen — Templates muessen die
      Readability-Schwelle reissen, bevor sie an Kunden gehen.
- [ ] When ein Code-Node im Workflow vorhanden ist, the system shall im
      Audit eine optionale **Demote-Empfehlung** generieren ("kann
      dieser Code-Block durch IF/Set/HTTP-Nodes ersetzt werden?") —
      orientiert am Vision-Prinzip `visuelle-nachvollziehbarkeit`.

## Technische Hinweise

### Patterns aus der Recherche (5 Kern-Patterns)

1. **Sticky-Note-Sektionen** — pro logischer Phase (Input, Validation,
   Routing, Action, Logging) eine `## Header`-Sticky in Markdown,
   eingefaerbt nach Kategorie (blau=Info, gelb=Warning,
   gruen=Config/Credential, rot=Known-Issue). Quelle:
   ryanandmattdatascience.com + n8n Docs.
2. **Naming-Konvention `[STATUS]/[VERB] Object`** — Nodes wie
   "HTTP Request" sind verboten, stattdessen "Fetch Stripe Invoice"
   oder "POST Pool-Insert". Workflow-Namen tragen `[PROD]/[EXP]`-
   Prefix. Quelle: evalics.com, n8npro.in.
3. **Lane-Layout Top-to-Bottom mit Switch-Tracks** — jeder Switch-
   Output bekommt eine eigene horizontale Lane mit definiertem
   Y-Offset (z.B. 200px Abstand). Quelle: Camunda BPMN-Best-Practice
   adaptiert + n8npro.in.
4. **Sub-Workflow-Threshold** — > 15-20 Nodes ODER > 3 Branches sind
   ein Refactor-Kandidat in einen Execute-Workflow-Trigger. Quelle:
   hatchworks.com, n8nautomation.cloud, dev.to/iloven8n
   (Analyse 6000+ Workflows).
5. **Why-not-What in Sticky Notes** — "HTTP-Request fetcht Stripe" ist
   nutzlos; "Holt alle unbezahlten Rechnungen der letzten 30 Tage,
   weil Klausel X im Mahn-Prozess das verlangt" ist die Pflicht.
   Quelle: ryanandmattdatascience.com.

### Slash-Commands die der Skill anbietet

- `/n8n-readability-audit <workflow-id|json-pfad>` — read-only Audit,
  liefert Score + Issue-Liste, schreibt nichts in n8n.
- `/n8n-prettify <workflow-id|json-pfad>` — generiert Prettify-Vorschlag
  (Sticky-Note-Drafts, Lane-Reorg, Naming-Diff) als JSON-Diff +
  Markdown-Review, Jakob bestaetigt explizit vor Push in n8n.
- `/n8n-rename-nodes <workflow-id>` — schlaegt konsistente Node-Namen
  nach dem `[VERB] Object`-Pattern vor (LLM-gestuetzt aus Node-Konfig).

### Beziehung zu existierenden Skills

- **`po-skill`** liefert das Vision-Prinzip
  [[visuelle-nachvollziehbarkeit]] als Acceptance-Gate — der Prettify-
  Skill ist die operationale Umsetzung dieses Prinzips. PO-Skill
  challenged das Ticket (3x-Why, RICE), Prettify-Skill produziert das
  Outcome.
- **`agile-sdd-skill`** liefert das Ticket-/ADR-Framework — der
  Prettify-Skill selbst wird per SDD-Methodik gebaut (`dogfood-
  zwingt-qualitaet`). Auch: nach erfolgreichem Prettify-Lauf soll ein
  ADR auf Wunsch automatisch dokumentiert werden ("Layout-Entscheidung
  fuer Workflow X").
- **Komplementaer zu (kein Konflikt)** [[SKILL-009]] (inbox/-Konvention)
  und [[SKILL-008]] (Reveal-Wrapper-Fix) — andere Domaene.

### Implementierungs-Skizze

- Skill-Code in `skills_sources/n8n-human-readable/` mit `SKILL.md`,
  `commands/`, `patterns/` (scoring.md, sticky-note-templates.md,
  naming-conventions.md), `tools/` (workflow_json_parser.py,
  readability_scorer.py).
- Input: n8n-API GET `/api/v1/workflows/<id>` ODER lokales
  `versions/vX.Y/workflow.json`.
- Output Phase 1 (audit): Markdown-Report mit Score-Breakdown.
  Output Phase 2 (prettify): n8n-kompatibles Diff-JSON, das Jakob via
  `/n8n-apply` (separater Schritt) auf die Live-Instanz pushen kann.
- **Anti-Pattern (NICHT machen):** Direkter Push in Live-Instanz ohne
  Bestaetigung. `mensch-final-im-loop` aus Workflow-Builder-Vision
  gilt auch hier.

### Bekannte Risiken

- Sticky-Note-Spam: LLM-generierte Notes koennen oberflaechlich sein
  ("AI Agent — der AI Agent verarbeitet die Eingabe"). Why-not-What-
  Regel muss als Prompt-Pflicht im Generator stehen.
- Lane-Reorg kann Connections-IDs durcheinanderbringen — Skill muss
  unbedingt die `connections`-Struktur referenz-stabil halten, nur
  `position`-Felder anpassen.
- Score-Inflation: Wenn Workflow auf 100/100 optimiert wird ohne dass
  Lesbarkeit real besser wird (Goodhart). Outcome-Review nach 14
  Tagen muss qualitative Frage stellen ("hat ein Subagent den Workflow
  6 Wochen spaeter ohne Doku verstanden?").

## Code-Referenzen

- Live-Trigger: [[research_2026-05-29]] — Diff-Analyse Bewerbung-Bot
  v0.5.5 → v0.7.2 + Web-Best-Practice-Sammlung
- Vision-Prinzip: [[PROJECT_VISION]] Punkt 2
  (`visuelle-nachvollziehbarkeit`)
- Live-Beispiele:
  - `workflows/prod/bewerbung-bot/versions/v0.7.2/workflow.json`
    (33 Nodes, kein Sticky, ueberlappende Lanes — Hauptreferenz)
  - `workflows/prod/bewerbung-bot/versions/v0.5.5/workflow.json`
    (10 Nodes, war noch grenzwertig lesbar — Baseline)
- Vergleichs-Skills (Methodik):
  - [[SKILL-007]] (reveal-presentation Visual-Review) — analoges
    Pattern "Skill audited visuelles Output", uebertragen auf n8n
  - [[SKILL-003]] (Implementer-Hygiene) — Smoke-Test-Verschaerfung
    als Vorbild fuer "echtes Outcome statt Existenz-Check"

## Out of Scope

- **Direktes Schreiben in Prod-Instanz ohne User-Confirm.** Hard-No
  (`mensch-final-im-loop`).
- **Auto-Refactor in Sub-Workflows.** Skill kann VORSCHLAGEN ("dieser
  Workflow hat 33 Nodes, splitten in 3 Sub-Workflows?"), aber nicht
  selbst splitten — das ist eine inhaltliche Entscheidung mit
  Webhook-/Datatable-Konsequenzen.
- **Visual-Linting via Screenshot-Diff.** Wir parsen das Workflow-JSON,
  nicht Pixel — Approach ist deterministisch, nicht ML-basiert.
- **Multi-Tenant-Templates ueberschreiben.** Wenn ein Workflow
  `template: true` und bereits versioniert, prettify produziert
  Snapshot-Diff fuer NEUE Version, niemals in eingefrorenen
  `versions/vX.Y/` schreiben.

## Offene Klaerungen (vor `spec`)

- Wo lebt der `readability_score`-Verlauf? (DEFERRED-Idee: Supabase-
  Tabelle `workflow_quality_log`, analog zu `workflow_log`.)
- Soll der Skill auch existierende `versions/`-Snapshots scoren
  (Trend-Analyse "wird der Workflow lesbarer ueber Zeit?") oder nur
  Live-State?
- Welche Lane-Y-Offsets passen zu n8ns Canvas-Raster? (220px in
  v0.7.2-Beobachtung — Standardisierung pruefen.)

## Ergebnis / Notizen

_Wird beim Implementieren befuellt._
