# SKILL-002: Refactor T078/T079 in PO-Skill (Vision↔Features-Bridge generalisieren)

**Status:** spec
**Erstellt:** 2026-05-25 (Original) | **Migriert:** 2026-05-25 (aus TICKET-081, Immobewertung)
**MoSCoW:** Should
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein` + `lessons-aus-live-use-zurueckfuehren`
**outcome_metric:** projekte_die_einen_skill_nutzen (Generator soll spaeter im 2. Projekt 1:1 laufen)
**outcome_review_at:** null (wird beim done-Set gesetzt)

> [!info] Migrations-Hinweis
> Dieses Ticket wurde am 2026-05-25 aus `Immobewertung/docs/tickets/TICKET-081.md`
> nach `Schaltzentrale/skill_dev/docs/tickets/SKILL-002.md` migriert (TICKET-083).
> Original-Ticket bleibt mit Status `done` + Migrations-Note in Immobewertung
> bestehen.

## Was soll erreicht werden? (Business-Ziel)

Jakob 2026-05-25:
> "Aha ok, und im PO-Skill haben wir das nicht eingebaut oder? Also so eine
> HTML + Feature Map als Schnittstelle zwischen PO-Skill und den SDD-Skill
> oder man koennte auch sagen zwischen Vision und den Tickets."

Volltreffer. T078 (PROJECT_OVERVIEW.html) + T079 (FEATURE_MAP) wurden in
Immobewertung als Worker gebaut. Das ist **funktional richtig** (Pattern
erstmal in einem Projekt validieren), aber **architektonisch falsch
verortet**: HTML + FEATURE_MAP sind die natuerliche **Schnittstelle
zwischen Vision (PO-Skill) und Tickets (SDD-Skill)** — sie gehoeren als
generisches Tooling in den PO-Skill, sodass jedes Projekt mit PO-Skill sie
automatisch hat.

Ziel: **Lift-and-Shift in den PO-Skill** sobald T078/T079 in Immobewertung
funktional validiert sind. Pattern: erst projekt-spezifisch bauen +
nutzen, dann ins Skill-Source heben.

## Akzeptanzkriterien (EARS-Format)

### Teil A — Generator-Code in PO-Skill

- [ ] When der Lift-and-Shift fertig ist, the system shall folgende neuen
      Artefakte unter `<Schaltzentrale>/skills_sources/po-skill/` haben:
      ```
      po-skill/
      ├── generators/
      │   ├── feature_map_generator.py
      │   ├── project_overview_generator.py
      │   └── overview_template.html
      ├── commands/
      │   ├── po-generate-feature-map.md
      │   └── po-generate-overview.md
      ```
- [ ] When der Generator-Code im PO-Skill liegt, the system shall die
      Konsumenten-Logik so refactoren dass **per-Projekt-Konfig** in
      `<projekt>/docs/po-config.yaml` die Generator-Parameter setzt:
      - `feature_map.output_path`
      - `overview.output_path`
      - `overview.banned_tokens`
      - `overview.live_db_stats_hook`
      - `feature_map.job_categories`
      - `vision_principle_mapping.mode` (`heuristic|frontmatter|manual`)

### Teil B — Live-DB-Stats als Plug-in

- [ ] When `overview.live_db_stats_hook` in po-config.yaml gesetzt ist,
      the system shall das Python-Modul importieren + `get_stats()` aufrufen.
- [ ] When der Hook nicht definiert ist, the system shall den
      Status-Banner im Overview einfach weglassen (kein Crash).

### Teil C — Slash-Commands im PO-Skill

- [ ] When `/po-generate-feature-map` ausgefuehrt wird, the system shall
      den Generator aufrufen + Output-Pfad ausgeben.
- [ ] When `/po-generate-overview` ausgefuehrt wird, the system shall
      beide Generatoren in der richtigen Reihenfolge ausfuehren.

### Teil D — Auto-Refresh-Hook verschoben

- [ ] When der SDD-Skill-Hook bei Ticket-`done` greift, the system shall
      PO-Skill-Command `/po-generate-overview` aufrufen (statt direkten
      Worker-Aufruf in Immobewertung).

### Teil E — Immobewertung-Bereinigung

- [ ] When der Lift-and-Shift abgeschlossen ist, the system shall:
      - `workers/feature_map_generator.py` aus Immobewertung **loeschen**
      - `workers/project_overview_generator.py` aus Immobewertung **loeschen**
      - **belassen**: `docs/FEATURE_MAP.md`, `docs/PROJECT_OVERVIEW.html`,
        `frontend/app/about/page.tsx`, `docs/po-config.yaml`
      - `workers/po_overview_stats_immobewertung.py` (NEU,
        Plug-in-Hook fuer Live-DB-Stats)

### Teil F — Tests bleiben

- [ ] When `tests/test_ticket_078_*.py` + `tests/test_ticket_079_*.py`
      laufen, the system shall sie unveraendert gruen halten.

### Teil G — Smoke fuer leeres Projekt

- [ ] When ein hypothetisches zweites Projekt ohne `live_db_stats_hook`
      `/po-generate-overview` aufruft, the system shall trotzdem ein
      valides HTML produzieren.

## Technische Hinweise

- **Pattern:** Code wandert ins Skill, Konfig + Konsument-Hooks bleiben
  im Projekt. Klassisches "Framework vs Application"-Pattern.
- **Anti-Pattern aus SKILL-003 anwenden:** Generator-Pattern bei
  Outputs > 10 KB ist Pflicht. HTML/MD via Template + 1 Generator-Aufruf,
  KEIN iteratives Schreiben.
- **Sub-Skill-Pattern:** wie wird Code aus einem Skill in einem Projekt
  ausgefuehrt? Vermutlich via `python -m`-Import von
  `~/.claude/skills/po-skill/generators/feature_map_generator.py` mit
  `cwd=<projekt>`.

## Code-Referenzen

- `<Schaltzentrale>/skills_sources/po-skill/generators/` (NEU)
- `<Schaltzentrale>/skills_sources/po-skill/commands/po-generate-*.md` (NEU)
- `<Schaltzentrale>/skills_sources/agile-sdd-skill/SKILL.md` (Hook-Aufruf umstellen)
- `Immobewertung/workers/feature_map_generator.py` (loeschen)
- `Immobewertung/workers/project_overview_generator.py` (loeschen)
- `Immobewertung/workers/po_overview_stats_immobewertung.py` (NEU)
- `Immobewertung/docs/po-config.yaml` (Felder erweitern)

## Out of Scope

- Multi-Projekt-Validierung — wird erst beim 2. Projekt (z.B. BeyerImmo)
  real geprueft. Hier nur fuer Immobewertung verifizieren dass nichts
  bricht.

## Voraussetzung

T078 + T079 in Immobewertung muessen `done` sein (HTML + FEATURE_MAP
funktionieren live), bevor SKILL-002 angefasst wird. Sonst refactored
man auf schwankendem Boden.

## Verknuepfte Tickets

- **Original:** `Immobewertung/docs/tickets/TICKET-081.md` (Migrations-
  Note hinzugefuegt)
- **Voraussetzung:** Immobewertung T078 + T079 done
- **Trigger:** TICKET-083 (Skill-Dev-Repo aufsetzen)
- **Verbunden:** SKILL-001 (PO-Skill bauen) | SKILL-003 (Hygiene-Regeln,
  die hier beim Generator-Pattern angewendet werden)

## Ergebnis / Notizen

_(wird vom Implementer nach T078/T079-done befuellt)_
