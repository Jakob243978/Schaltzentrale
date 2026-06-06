---
vision_principle: lessons-aus-live-use-zurueckfuehren
outcome_metric: aenderungen_mit_ticket_und_commit
outcome_review_at: null
ui_verify_urls: []
api_endpoints_extended: n/a
---

# SKILL-013: Governance-Prinzip "Kein Fix ohne Ticket und Code"

**Status:** spec
**Erstellt:** 2026-06-05
**MoSCoW:** Must
**Geschaetzter Aufwand:** S
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren`

## Trigger-Live-Erfahrung

Jakob 2026-06-05:

> "Wir fixen nichts ohne Ticket und Code dazu."

Hintergrund: In einer Session wurden Daten direkt in der DB bereinigt
(`UPDATE`/`cancel`/Status-Aenderungen) **ohne** dediziertes Ticket und ohne
nachvollziehbaren Code-Pfad. Folge: Verwirrung darueber, was, wann und warum
geaendert wurde — die Aenderung war nicht reproduzierbar und nicht im
Audit-Trail. Lehre: Auch "schnelle" Korrekturen und manuelle DB-Eingriffe
muessen durch den normalen Spec-First-Workflow (Ticket + Code/Commit) laufen,
bevor sie angewandt werden.

## Was soll erreicht werden? (Business-Ziel)

Der agile-sdd-Skill verankert als **verbindliches Kern-Governance-Prinzip**:
Jede Aenderung an Code, Daten oder Konfiguration MUSS ein Ticket (Spec) haben
UND ueber zugehoerigen Code/Commit laufen — bevor sie angewandt wird. Das gilt
ausdruecklich auch fuer Hotfixes, Daten-Bereinigungen/Backfills/manuelle
DB-Eingriffe und Konfig-/Infra-Eingriffe. Einzige Ausnahme: reine
Lese-/Diagnose-Operationen (read-only). So bleibt jede Mutation nachvollziehbar
und vertrauenswuerdig (Audit-Trail + Reproduzierbarkeit).

## Akzeptanzkriterien (EARS-Format)

- [ ] When der agile-sdd-Skill (SKILL.md) gelesen wird, the system shall ein
      prominent platziertes, verbindliches Governance-Prinzip enthalten, das
      besagt: keine Mutation an Code/Daten/Konfiguration ohne Ticket + Code/Commit.
- [ ] When das Prinzip beschrieben wird, the system shall ausdruecklich Hotfixes,
      Daten-Bereinigungen/Backfills/manuelle DB-Eingriffe (`UPDATE`/`cancel`/
      Status-Aenderungen) und Konfig-/Infra-Eingriffe als eingeschlossen nennen.
- [ ] When das Prinzip eine Ausnahme definiert, the system shall ausschliesslich
      reine Lese-/Diagnose-Operationen (read-only SELECT, Status-Checks) als
      ticket-frei zulassen.
- [ ] When eine Mutation ohne Ticket+Code noetig erscheint ("mal eben direkt in
      der DB"), the system shall verlangen, zuerst ein Ticket anzulegen und die
      Aenderung als nachvollziehbaren Code/Commit zu fahren.

## Technische Hinweise

- Skill-Code-Aenderung: `skills_sources/agile-sdd-skill/SKILL.md` — neuer,
  prominenter Governance-Abschnitt nahe dem Kopf des Dokuments (vor "A) Agent
  Bootstrap-Sequenz"), damit jeder Agent das Prinzip zuerst sieht. Append-only/
  additiv — nichts Bestehendes verfaelschen.
- Kein neues Datenmodell, keine API-Aenderung (`api_endpoints_extended: n/a`).
- Deployment via `setup.ps1` (robocopy /MIR) nach `~/.claude/skills/`.

## Code-Referenzen

- `skills_sources/agile-sdd-skill/SKILL.md` (neuer Abschnitt "Governance-Grundregel")
- `skill_dev/CHANGELOG.md` (Eintrag)
- `skill_dev/docs/governance_log.md` (Eintrag)

## Ergebnis / Notizen

**Umgesetzt 2026-06-05:**

- Neuer Abschnitt **"Governance-Grundregel: Kein Fix ohne Ticket und Code"**
  in `SKILL.md` direkt nach der Einleitung, vor Abschnitt A. Verbindliches
  Prinzip + explizite Einschluss-Liste (Hotfixes, Daten-Bereinigungen/Backfills/
  manuelle DB-Eingriffe, Konfig/Infra) + einzige Ausnahme (read-only).
- CHANGELOG + governance_log ergaenzt.
- `setup.ps1` ausgefuehrt (Deploy nach `~/.claude/skills/agile-sdd-skill/`).
