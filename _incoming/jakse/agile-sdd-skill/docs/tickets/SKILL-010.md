---
vision_principle: lessons-aus-live-use-zurueckfuehren
outcome_metric: api_schema_lueke_pro_ticket
---

# SKILL-010: agile-sdd-skill Pflicht-EARS "API-Schema bedenken"

**Status:** review
**Erstellt:** 2026-06-01
**MoSCoW:** Should
**Geschaetzter Aufwand:** S

## Trigger-Live-Erfahrung

Jakob 2026-06-01 (nach Live-PO-Klick T097+T101 in Immobewertung):
> "T103a? ja - wir sollten bei jedem Ticket auch API bedenken. Wie 
> kriegen wir das mit in den SDD Skill rein? Als Ticket dort? Weil 
> das wir rudimentaer bei der Arbeit mit KI Agenten."

Konkretes Beispiel: T092 hat neue Property-Spalten + Region-FK + 
JSON-Felder eingefuehrt. T101 hat sie befuellt. ABER:
`GET /api/property/{id}`-Response wurde NIE erweitert. Frontend muss
2 API-Calls machen um Region-Info zu sehen. Folge-Ticket T103a wurde 
spontan nach Jakobs UI-Klick noetig.

Pattern: **Datenmodell-Aenderungen werden konsequent gemacht, aber
API-Schema-Erweiterungen werden vergessen** — weil EARS-Sections
typischerweise Model + Worker + Tests + UI abdecken, aber das
Response-Schema "irgendwie selbstverstaendlich" laeuft.

## Was soll erreicht werden? (Business-Ziel)

Der agile-sdd-skill soll **strukturell verhindern**, dass API-
Aenderungen vergessen werden. Konkret: in jedem Ticket-Template
und im Verifier-Checklist eine Pflicht-EARS-Sektion "API-Schema-
Kontrakt" einbauen, die der Implementer abhaken muss.

## Akzeptanzkriterien (EARS)

### Teil A — Ticket-Template-Erweiterung

- [ ] When `templates/TICKET.md` erweitert wird, the system shall
      eine neue Pflicht-Sektion `### API-Schema-Kontrakt` haben mit:
      - Checkbox "Aendert dieses Ticket ein Datenmodell? Wenn ja:
        welche API-Endpoints geben diese Felder zurueck?"
      - Checkbox "Wurden GET-Response-Schemas erweitert?"
      - Checkbox "Wurde Backwards-Kompat gepruft (keine 
        Feld-Umbenennung)?"
      - Checkbox "Wurde ein OpenAPI-Diff-Test geschrieben falls 
        bestehende Endpoints geaendert wurden?"

### Teil B — Verifier-Checklist erweitern

- [ ] When `verifier/VERIFIER.md` erweitert wird, the system shall
      einen neuen Pflicht-Check haben:
      - "Hat das Ticket neue Modell-Spalten/FKs eingefuehrt?"
      - "Wenn ja: sind diese Felder im OpenAPI-Schema sichtbar 
        (`curl /openapi.json`)?"
      - "Wenn nein: Verify-Status = `partial` mit Folge-Ticket 
        `<TICKET>a` vorschlagen"

### Teil C — Implementer-Briefing-Erweiterung

- [ ] When Implementer-Subagents instruiert werden, the system shall
      einen Standard-Block "API-Schema-Mitdenken" im Briefing haben:
      - "Wenn du Property/Models-Felder hinzufuegst, pruefe alle 
        relevanten Endpoints (GET/POST/PATCH) und erweitere die 
        Response-Schemas mit"
      - "Setze automatisch einen Verify-Check fuer das 
        OpenAPI-Schema in die Tests"

### Teil D — Operator-Templates-Anpassung

- [ ] When `operator-templates` (T035) erweitert werden, the system
      shall in jedem Template einen Hinweis haben:
      - "Wenn dein Skill-Output neue Felder erzeugt: pruefe das 
        zugehoerige Persist-Endpoint-Schema"

### Teil E — Memory-Feedback

- [ ] When dieser Skill done ist, the system shall einen Memory-
      Eintrag haben `feedback_api_schema_pflicht.md`:
      "Bei jedem Ticket mit Datenmodell-Aenderung pruefen + im 
      Frontmatter `api_endpoints_extended: yes|no|n/a` markieren"

### Teil F — Tests

- [ ] When `tests/test_skill_010_api_schema_check.py` laeuft, the 
      system shall mind 3 Cases gruen haben:
      1. Ticket-Template enthaelt API-Schema-Kontrakt-Sektion
      2. Verifier-Output flagt fehlende API-Schema-Erweiterung als 
         `partial`
      3. Implementer-Briefing-Template enthaelt API-Mitdenken-Block

## Code-Referenzen

- `skills_sources/agile-sdd-skill/templates/TICKET.md` (erweitern)
- `skills_sources/agile-sdd-skill/verifier/VERIFIER.md` (Checklist)
- `skills_sources/agile-sdd-skill/SKILL.md` (Bootstrap-Sequenz-Hinweis)
- `~/.claude/projects/.../memory/feedback_api_schema_pflicht.md` (NEU)

## Out of Scope

- Auto-Code-Generierung von Pydantic-Schemas aus Models
- OpenAPI-Diff-CI (kann Phase-2 sein)
- API-Versioning-Logik

## Verknuepfte Tickets

- Konkretes Beispiel: T103a (Immobewertung) — Property-Response-
  Erweiterung die durch fehlendes API-Mitdenken entstanden ist
- SKILL-006 Implementer-Hygiene-Patterns
- SKILL-009 Inbox-Konvention fuer externe Materialien

## Ergebnis / Notizen

**Implementiert 2026-06-01** (Implementer-Subagent, claude-opus-4-7 1M).

**Aenderungen (alle Pfade absolut):**
- `C:/Users/Jakob/claude_projects/Schaltzentrale/skills_sources/agile-sdd-skill/templates/TICKET.md` — Pflicht-Sektion `## API-Schema-Kontrakt` mit 4 Checkboxen + Frontmatter-Hinweis `api_endpoints_extended: yes|no|n/a` (Teil A).
- `C:/Users/Jakob/claude_projects/Schaltzentrale/skills_sources/agile-sdd-skill/verifier/VERIFIER.md` — Neuer Pflicht-Check-Schritt 6 "API-Schema-Coverage-Check" mit Diff-Pruefung, `curl /openapi.json`-Verifikation, `partial`-Regel + Folge-Ticket-Empfehlung. Token-Aggregation wurde auf Schritt 7 verschoben (Teil B).
- `C:/Users/Jakob/claude_projects/Schaltzentrale/skills_sources/agile-sdd-skill/templates/IMPLEMENTER_BRIEFING_STANDARDS.md` — NEU. Standard-Bloecke "API-Schema-Mitdenken" + "Implementer-Hygiene" + "Skill-Code-Pfad" zur Wiederverwendung im Subagent-Briefing (Teil C).
- `C:/Users/Jakob/claude_projects/Schaltzentrale/skills_sources/agile-sdd-skill/SKILL.md` — Templates-Tabelle erweitert + neue Sektion "Implementer-Briefing-Standards" in B die auf das neue File verweist.
- `C:/Users/Jakob/claude_projects/Schaltzentrale/skills_sources/operator-templates/SKILL.md` — Block "MCP/API-Schema-Hinweis" eingefuegt, der bei Persist-Endpoints die GET-Symmetrie prueft (Teil D).
- `C:/Users/Jakob/.claude/projects/C--Users-Jakob-claude-projects/memory/feedback_api_schema_pflicht.md` — NEU. Memory-Eintrag mit Rule/Why/How-to-apply, Live-Trigger T103a (Teil E).
- `C:/Users/Jakob/.claude/projects/C--Users-Jakob-claude-projects/memory/MEMORY.md` — 1-Zeile-Index-Eintrag fuer das neue Memory-File (Teil E).
- `C:/Users/Jakob/claude_projects/Schaltzentrale/skill_dev/tests/test_skill_010_api_schema_check.py` — NEU. 6 Tests (3 Pflicht-Cases + 3 Bonus). Alle gruen (Teil F).

**Deploy (Teil G):** `setup.ps1` ausgefuehrt — Skills-Deploy-Schritt 3/5 erfolgreich (Pip-Install-Schritt 5/5 hatte unrelated Fehler, blockt Skill-Deploy nicht). `~/.claude/skills/agile-sdd-skill/templates/IMPLEMENTER_BRIEFING_STANDARDS.md` ist vorhanden, alle Pflicht-Stichworte ("API-Schema-Kontrakt", "API-Schema-Coverage", "API-Schema-Hinweis") sind in den deployten Files praesent (`grep -c == 1`).

**Tests:** `python -m pytest skill_dev/tests/test_skill_010_api_schema_check.py -v` → 6 passed (3 EARS + 3 Bonus).

**Anti-Pattern bewusst nicht behoben:** Vorbestehender Duplicate-Fall `SKILL-010.md` in `n8n-human-readable/`-Sub-Verzeichnis (pre-existing, vom Sub-Agent 2 angelegt). Lass den smoke-test im `test_skill_dev_smoke.py::test_ears_g2_skill_tickets_listed` aktuell rot — sollte separat geloest werden (n8n-human-readable-Ticket umnummerieren).

**PO-Klick-Anleitung fuer Jakob (Sektion C des Tickets):**
1. Lies `skill_dev/docs/tickets/agile-sdd-skill/SKILL-010.md` (dieses File) durch.
2. Bei nicht-trivialen Aenderungen: `git diff skills_sources/agile-sdd-skill/templates/TICKET.md` ansehen.
3. Falls passt: Status auf `done` setzen, `outcome_review_at: 2026-06-15` im Frontmatter setzen, CHANGELOG.md + governance_log.md sind bereits gefuellt.
