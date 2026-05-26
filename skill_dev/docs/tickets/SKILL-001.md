# SKILL-001: PO-Skill bauen (Schaltzentrale) + Init in Immobewertung

**Status:** review
**Erstellt:** 2026-05-25 (Original) | **Migriert:** 2026-05-25 (aus TICKET-080, Immobewertung)
**MoSCoW:** Must
**Geschaetzter Aufwand:** L (neuer Skill + Init-Pattern + Vision-Definition + SDD-Integration)
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein` + `dogfood-zwingt-qualitaet`
**outcome_metric:** projekte_die_einen_skill_nutzen (Ziel: PO-Skill in >=2 Projekten aktiv)
**outcome_review_at:** 2026-06-08 (= done + 14d, wenn Verifier-Pass durch)

> [!info] Migrations-Hinweis
> Dieses Ticket wurde am 2026-05-25 aus `Immobewertung/docs/tickets/TICKET-080.md`
> nach `Schaltzentrale/skill_dev/docs/tickets/SKILL-001.md` migriert (TICKET-083).
> Original-Ticket bleibt mit Status `done` + Migrations-Note in Immobewertung
> bestehen. Hier ist die kanonische Skill-Sicht; Verifier-Reports, Outcomes etc.
> wandern ab jetzt in `skill_dev/docs/tickets/verify/SKILL-001-verify-*.md`.

## Was soll erreicht werden? (Business-Ziel)

Aus der Retrospektive 2026-05-25 + Recherche zu AI-PO-Patterns (BMad-
Method, GitHub spec-kit, Dean Peters PM-Skills, avoid-feature-creep,
Teresa Torres Continuous Discovery) wurde klar:

**Heute fehlt ein expliziter PO-Skill als Counterpart zum SDD-Skill.**
Jakob macht PO-Arbeit implizit (Vision halten, Scope schuetzen,
Prioritaeten setzen), aber:
- Keine schriftliche Vision/Constitution
- Kein Challenge-Workflow vor Ticket-Erstellung (3x-Why, 48h-Cooldown)
- Kein Outcome-Tracking (nur Output-Tracking)
- Keine Definition of Ready
- Keine WIP-Limits explizit
- Ticket-Erstellung passiert "im Flow" — was zu mehr Tickets fuehrt als
  noetig, "warum-haben-wir-das-gebaut"-Frage am Ende offen

Jakob 2026-05-25 (Sprachnachricht-Synthese):
> "Vision: hoechst autonomer Immobilien-Einkauf. Mensch macht Entscheidung,
> KI bereitet vor. Hebel gegenueber Konkurrenz durch Geschwindigkeit. Mehr
> Deals, schneller, ohne Mitarbeiter. Daten sammeln fuer spaetere
> Bank/Verhandlung. Geld findet sich — das Problem ist gute Objekte
> finden, bewerten, verhandeln. Wer hat die Zeit?"

Ziel: **PO-Skill als eigenstaendiger Skill in `<Schaltzentrale>/skills_sources/po-skill/`** —
deploy-bar via `setup.ps1` analog zu `agile-sdd-skill`. Plus **Init-Pattern
fuer ein Projekt**, einmalig im Immobewertung-Repo ausgefuehrt mit Jakobs
initialer Vision.

## Akzeptanzkriterien (EARS-Format)

### Teil A — Skill bauen in Schaltzentrale

- [x] When der Implementer fertig ist, the system shall folgende
      Verzeichnisstruktur unter
      `C:\Users\Jakob\claude_projects\Schaltzentrale\skills_sources\po-skill\` haben:
      ```
      po-skill/
      ├── SKILL.md
      ├── README.md
      ├── templates/
      │   ├── vision.md
      │   ├── DEFERRED.md
      │   └── po-config.yaml.example
      ├── commands/
      │   ├── po-init.md
      │   ├── po-challenge.md
      │   ├── po-prioritize.md
      │   └── po-verify-outcome.md
      └── po-verifier/
          ├── PO_VERIFIER.md
          └── po-verifier-prompt.md
      ```

### Teil B — vision.md Template

- [x] When `templates/vision.md` angelegt ist, the system shall folgende
      Sektionen enthalten: Vision-Statement, Kern-Prinzipien,
      Outcome-Metriken, Was NICHT im Scope ist, Aktualisiert.

### Teil C — Challenge-Workflow

- [x] When der `/po-challenge`-Slash-Command auf einer Ticket-Idee
      aufgerufen wird, the system shall:
      1. Idee gegen `vision.md`-Prinzipien matchen
      2. **3x Why** stellen
      3. **48h-Cooldown-Empfehlung** wenn nicht-akut
      4. Erst wenn Cooldown abgelaufen UND Vision-Prinzip referenziert:
         in den SDD-Skill `idea` → `spec` -Flow uebergeben

### Teil D — Prioritization

- [x] When `/po-prioritize` aufgerufen wird, the system shall alle
      `idea`-Status-Tickets nach **RICE-Score** sortieren.

### Teil E — Outcome-Verifier

- [x] When 14 Tage nach einem `done`-Ticket der `/po-verify-outcome`
      aufgerufen wird, the system shall pruefen ob das Outcome-Metric
      beruehrt wurde.

### Teil F — Init in Immobewertung

- [x] When `/po-init` im Immobewertung-Repo aufgerufen wird, the system
      shall PROJECT_VISION.md, DEFERRED.md, po-config.yaml,
      po-outcomes.md anlegen + CLAUDE.md erweitern.

### Teil G — SDD-Integration

- [x] When ein Ticket im SDD-Skill auf `spec` gesetzt werden soll, the
      system shall pruefen ob `vision.md` existiert + ein Vision-Prinzip
      referenziert ist (Warning per Default, Hard-Block per ENV
      `PO_SKILL_STRICT=1`).

### Teil H — Initial-Vision-Material

Siehe Original TICKET-080 Teil H — Material wurde 1:1 in
`Immobewertung/docs/PROJECT_VISION.md` uebernommen.

### Teil I — Tests

- [x] When `tests/test_po_skill_smoke.py` im Immobewertung-Repo laeuft,
      the system shall mind 3 Cases gruen haben.

## Technische Hinweise

- **Skill-Source-of-Truth:** `<Schaltzentrale>/skills_sources/po-skill/`
- **Deployment:** via `setup.ps1` (Robocopy `/MIR` Pattern)
- **Anti-Pattern (aus Recherche):** PO-Skill darf **NICHT selbst Tickets
  generieren** — er challenged + priorisiert + verifiziert nur.

## Code-Referenzen

- `C:\Users\Jakob\claude_projects\Schaltzentrale\skills_sources\po-skill\` (Skill-Source)
- `C:\Users\Jakob\claude_projects\Schaltzentrale\setup.ps1` (deploy)
- `C:\Users\Jakob\claude_projects\Immobewertung\docs\PROJECT_VISION.md`
- `C:\Users\Jakob\claude_projects\Immobewertung\docs\DEFERRED.md`
- `C:\Users\Jakob\claude_projects\Immobewertung\docs\po-config.yaml`
- `C:\Users\Jakob\claude_projects\Immobewertung\CLAUDE.md` (Skill: PO-Block)
- `C:\Users\Jakob\claude_projects\Immobewertung\tests\test_po_skill_smoke.py`

## Out of Scope

- **Automatisches Outcome-Tracking** mit DB-Metriken — kommt als
  Folge-Ticket SKILL-002 (war T081).
- **PO-Skill fuer andere Projekte** (BeyerImmo, ZeitenAbgleich) —
  diese Session nur Immobewertung. Andere Projekte fuehren ihren
  eigenen `po-init` aus, wenn sie soweit sind.
- **Multi-Stakeholder-Voting** (BMad-Style).

## Ergebnis / Notizen

Implementiert: 2026-05-25 — Subagent (Opus 4.7 1M) im Rahmen von
TICKET-080. Vollstaendige Doku siehe Original-Ticket-Body in
`Immobewertung/docs/tickets/TICKET-080.md` Sektion "Ergebnis / Notizen".

**Status nach Migration (2026-05-25):** `review` — Verifier-Pass
ausstehend. Vorgehen:
1. `/sdd-verify SKILL-001` (Backend-only Ticket).
2. Wenn `pass` → Status `done`, `outcome_review_at: 2026-06-08`.
3. Am 2026-06-08: `/po-verify-outcome SKILL-001` (Outcome-Metric
   `projekte_die_einen_skill_nutzen` — Ziel: PO-Skill in
   Immobewertung aktiv + mind. 1 weiteres Projekt initialisiert).

**Verifier-Hinweis:** Verifier-Subagent muss diesen Pfad lesen
(`skill_dev/docs/tickets/SKILL-001.md`), nicht den Immobewertung-
Original-Pfad — Single Source of Truth ist ab jetzt das Skill-Repo.

## Verknuepfte Tickets

- **Original:** `Immobewertung/docs/tickets/TICKET-080.md` (Migrations-
  Note hinzugefuegt)
- **Folge:** SKILL-002 (Lift-and-Shift T078/T079) | SKILL-003
  (Implementer-Hygiene)
- **Trigger:** TICKET-083 (Skill-Dev-Repo aufsetzen)
