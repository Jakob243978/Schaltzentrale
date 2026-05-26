# SKILL-005: Skill-Versions-Anker (rollbar-zu-v0.4 vor Pre-Condition-Einbau)

**Status:** spec
**Erstellt:** 2026-05-26
**MoSCoW:** Must
**Geschaetzter Aufwand:** XS
**Vision-Prinzip:** `dogfood-zwingt-qualitaet` + `skill-schlanker-als-was-er-ersetzt`
**outcome_metric:** time_to_new_skill_in_neues_projekt (Ziel: Rollback auf eine bekannte Skill-Version <= 5 Min)
**outcome_review_at:** null (wird beim done-Set gesetzt)

> [!info] Warum dieses Ticket
> Bevor SKILL-004 (Pre-Conditions) und SKILL-006 (KNOWN_FAILURES.md) den
> agile-sdd-skill anfassen, brauchen wir einen sauberen Rollback-Punkt
> auf die funktionierende v0.4 (EARS-Verify + Cost-Tracking, validiert
> in Immobewertung). Sonst koennen wir nicht "zurueck zu v0.4" falls die
> Pre-Condition-Pflicht in der Praxis mehr Reibung erzeugt als sie spart
> (Vision-Prinzip `skill-schlanker-als-was-er-ersetzt`).

## Pre-Conditions

1. Schaltzentrale-Repo ist git-versioniert und HEAD entspricht dem
   gewuenschten Stand — verifiziere via `git status` (clean) und
   `git log -1 --format=%H`.
2. agile-sdd-skill v0.4 ist live und funktional validiert in
   Immobewertung (mind. 1 erfolgreicher `/sdd-verify` mit
   Cost-Tracking-Frontmatter laeuft) — verifiziere via `ls
   Immobewertung/docs/tickets/verify/*.md` und Frontmatter-Check
   (`tokens_total`, `cost_usd`).

## Was soll erreicht werden? (Business-Ziel)

Klarer, dokumentierter Rollback-Anker auf agile-sdd-skill v0.4 — die
**letzte funktional validierte Version vor dem Pre-Condition-Umbau** —
ohne Skill-Code anzufassen.

Zwei Optionen, eine zu waehlen:

- **Option A — Git-Tag `agile-sdd-skill-v0.4-pre-pre-conditions`** auf
  Commit `fe9337a` (SDD: Verifier-Skill v0.4 …) oder auf den letzten
  Commit der den Skill VOR SKILL-004 anfasste.
- **Option B — `docs/skill-versions.md`** mit Append-only Log
  (Version, Datum, Commit-Hash, "wofuer validiert", "rollback-Befehl").

**Empfehlung:** Option B (skill-versions.md) als Primaer-Mechanismus +
optional Tag obenauf. Begruendung:
- skill-versions.md ist im Repo selbst auditierbar (Jakob kann es im
  Editor lesen, kein `git tag -l` noetig).
- Funktioniert auch wenn Schaltzentrale-Repo neu geklont wird.
- Konsistent mit Convention im Repo (Append-only Logs in
  SKILLS_VISION.md, governance_log.md, DEFERRED.md).
- Tag ist optionale Ergaenzung — nicht ersetzend.

## Akzeptanzkriterien (EARS-Format mit Pre-Conditions)

### Teil A — skill-versions.md anlegen

**Pre-Conditions Teil A:**
1. `skill_dev/docs/` existiert (gegeben seit TICKET-083)
2. Konventions-Schema fuer Append-only Logs ist klar (SKILLS_VISION.md
   liefert das Vorbild)

- [ ] When dieses Ticket implementiert wird, the system shall die Datei
      `skill_dev/docs/skill-versions.md` haben, mit Header-Sektion +
      Append-only Log pro Skill.
- [ ] When ein Eintrag fuer agile-sdd-skill v0.4 angelegt wird, the
      system shall folgende Felder enthalten:
      - Version: 0.4
      - Datum: 2026-05-25 (Commit-Datum von fe9337a)
      - Commit-Hash: `fe9337a` (kurz) ODER der spaeter relevante Sub-Tree-Commit
      - Status: `funktional validiert`
      - Wofuer validiert: "EARS-Verify (Sektion F.4), Cost-Tracking
        (5 Pflicht-Felder im Verify-Report-Frontmatter), PO-Hooks zu
        SKILL-001"
      - Rollback-Befehl (PowerShell): `git checkout <hash> --
        skills_sources/agile-sdd-skill/; .\setup.ps1`
      - Bekannte Live-Anwendungen: Immobewertung (Verifier-Pass auf
        T078/T079), Schaltzentrale skill_dev (SKILL-001 Review)
- [ ] When ein Eintrag fuer po-skill v0.1 angelegt wird, the system
      shall die gleichen Felder fuer den po-skill-Initial-Stand (Commit
      aus TICKET-080 / SKILL-001) enthalten.

### Teil B — Optionaler Git-Tag

**Pre-Conditions Teil B:**
1. Teil A ist done
2. Jakob hat explizit das Tag-Setzen freigegeben (NICHT autonom durch
   Implementer setzen)

- [ ] When Jakob das Tag-Setzen freigibt, the system shall vorschlagen:
      `git tag -a agile-sdd-skill-v0.4-pre-pre-conditions <hash> -m
      "v0.4 Snapshot vor Pre-Condition-Einbau (SKILL-004)"`
- [ ] When der Tag gesetzt ist, the system shall den Tag-Namen in
      `skill-versions.md` referenzieren.

### Teil C — Verlinkung von SKILL-004 / SKILL-006

**Pre-Conditions Teil C:**
1. Teil A ist done
2. SKILL-004 und SKILL-006 existieren mit Hinweis auf skill-versions.md

- [ ] When dieses Ticket done ist, the system shall in SKILL-004 und
      SKILL-006 unter "Voraussetzung" einen Verweis auf SKILL-005 +
      `skill-versions.md` haben (bereits beim Ticket-Anlegen aufgenommen).

### Teil D — Smoke-Test

**Pre-Conditions Teil D:**
1. `tests/test_skill_dev_smoke.py` existiert

- [ ] When der Smoke-Test laeuft, the system shall pruefen:
      - `skill_dev/docs/skill-versions.md` existiert
      - Datei enthaelt Zeichenkette `agile-sdd-skill` UND `v0.4`
      - Datei enthaelt mind. einen Eintrag mit `Commit-Hash:` und
        `Rollback-Befehl:`

## Technische Hinweise

- **Aktueller HEAD:** Commit-Hash beim Ticket-Anlegen war
  `7fb0036` (Session sync 2026-05-25). Der eigentliche Skill-Code-
  Commit fuer v0.4 ist `fe9337a` (SDD: Verifier-Skill v0.4) — das ist
  der korrekte Rollback-Punkt vor jedem v0.5-Aenderung.
- **Sub-Tree-Granularitaet:** `git checkout <hash> --
  skills_sources/agile-sdd-skill/` rollt **nur** den Skill-Code zurueck,
  nicht Tickets/skill_dev/. Das ist gewuenscht (Tickets bleiben gueltig,
  nur der Skill-Code geht zurueck).
- **Append-only-Log-Pattern:** Identisch zu SKILLS_VISION.md
  "Aktualisiert"-Sektion — neue Eintraege unten anhaengen, nie
  ueberschreiben.

## Code-Referenzen

- `skill_dev/docs/skill-versions.md` (NEU)
- `skill_dev/tests/test_skill_dev_smoke.py` (1 neuer Test-Case)
- Commit `fe9337a` als v0.4-Anker
- `skills_sources/agile-sdd-skill/SKILL.md` Frontmatter version=0.4
  (heute) — wird durch SKILL-004 auf 0.5 bewegt

## Out of Scope

- **Automatisches Tag-Setzen** — Tag-Erstellung bleibt manueller
  Schritt durch Jakob. Implementer schlaegt vor, fuehrt nicht aus.
- **Multi-Branch-Workflow / Worktrees fuer Skill-Versionen** — wenn
  v0.5 Reibung erzeugt, ist Rollback auf einzelnen Sub-Tree-Commit
  ausreichend. Branches sind Overkill fuer 1-Personen-Setup.
- **CHANGELOG.md ersetzen** — skill-versions.md ist enger gefasst (nur
  validierte Versionen + Rollback-Befehle), CHANGELOG.md bleibt
  feinkoerniger.

## Verknuepfte Tickets

- **Trigger:** Vor SKILL-004 / SKILL-006 noetig (Rollback-Anker)
- **Blockiert:** SKILL-004 (kann nicht auf in_progress ohne v0.4-Anker)
- **Blockiert:** SKILL-006 (analog)

## Ergebnis / Notizen

_(wird vom Implementer befuellt)_
