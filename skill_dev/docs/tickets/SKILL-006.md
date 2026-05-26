# SKILL-006: KNOWN_FAILURES.md als Pflicht-Datei + Bootstrap-Eintrag (Living Runbook)

**Status:** spec
**Erstellt:** 2026-05-26
**MoSCoW:** Should
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren` + `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** anti_pattern_im_skill_patterns_ordner + projekte_die_einen_skill_nutzen (Ziel: KNOWN_FAILURES.md in >=2 Projekten gewachsen nach 30 Tagen)
**outcome_review_at:** null (wird beim done-Set gesetzt)
**Trigger-Recherche:** `Researcher/jakob/spec-driven-development/recherche/2026-05-26_Knowledge_Persistence_Flaky_Processes.md` Empfehlung 1 + 1.6 (Living Runbooks)
**Skill-Vorversion:** agile-sdd-skill v0.4 (siehe `docs/skill-versions.md`)

> [!info] Status `spec` (hochgestuft 2026-05-26)
> Parallel zu SKILL-004 bearbeitbar, da unabhaengig in der Wirkung —
> KNOWN_FAILURES.md kann eigenstaendig Wert liefern. Jakobs Entscheidung
> (2026-05-26): nicht erst auf SKILL-004-Outcome warten, sondern beide
> Tickets parallel laufen lassen. Falls SKILL-004 in der Praxis das
> Wiederholungsproblem alleine loest, kann SKILL-006 spaeter immer noch
> schlanker werden (`skill-schlanker-als-was-er-ersetzt`).

## Pre-Conditions

1. SKILL-005 ist `done` (Versions-Anker existiert, Rollback moeglich)
   — verifiziere via `grep status:.*done docs/tickets/SKILL-005.md`.
2. Mindestens 1 Projekt (z.B. DropboxCheck) hat manuell ein
   KNOWN_FAILURES.md-Aequivalent angefangen, damit Live-Material
   existiert (sonst Skill-fuer-Skills-Sake-Risiko).
3. Parallel-Lauf zu SKILL-004 ist akzeptiert (Jakobs Entscheidung
   2026-05-26): KNOWN_FAILURES.md wirkt unabhaengig, kein Warten auf
   SKILL-004-Outcome.

## Was soll erreicht werden? (Business-Ziel)

Recherche (2026-05-26): Industrie-Konsens 2026 — Living Runbooks
(Symptom→Detection→Recovery→Prevention) schlagen freitextliche
CLAUDE.md-Fallstricke. Anthropic Auto-Memory + "Dreaming" zeigen:
explizit gemanagte Memory-Systeme schlagen Implicit Model Memory.
**KNOWN_FAILURES.md** ist die strukturierte Form dieser Erkenntnis im
agile-sdd-Skill.

Ziel: Im `agile-sdd-skill` neue **Pflicht-Datei**
`docs/KNOWN_FAILURES.md` (pro Projekt) einfuehren mit standardisiertem
FAILURE-NNN-Schema. Bootstrap-Sequenz wird erweitert (Punkt 10), der
Verifier-Pass prueft ob neu entdeckte Failures dort eingetragen
wurden.

**Anti-Pattern bewusst vermeiden:** Dies ist KEIN Ersatz fuer ADRs
(Architektur-Entscheidungen) oder Governance-Log (autonome
Entscheidungen). Es ist eine **dritte Kategorie**: bekannte
Failure-Modes mit Recovery-Procedure.

| Datei | Inhalt | Zeitlich |
|---|---|---|
| ADRs | Architektur-Entscheidungen | einmalig pro Entscheidung |
| Governance-Log | autonome KI-Entscheidungen | append-only pro Session |
| KNOWN_FAILURES.md | Symptom → Recovery pro Failure-Mode | append-only, aber jeder Eintrag wird **aktualisiert** wenn der Failure wieder auftritt |

## Akzeptanzkriterien (EARS-Format mit Pre-Conditions)

### Teil A — Template + Doku

**Pre-Conditions Teil A:**
1. SKILL-004 done, Skill auf v0.5
2. `skills_sources/agile-sdd-skill/templates/` existiert (heute schon der Fall)

- [ ] When dieses Ticket done ist, the system shall in
      `skills_sources/agile-sdd-skill/templates/KNOWN_FAILURES.md.tpl`
      ein Template enthalten mit Schema:
      ```
      ## FAILURE-NNN — <Kurzbeschreibung>

      - **Symptom (Detection-Pattern):** <Konkrete Fehlermeldung / Verhalten>
      - **Wahrscheinlichste Ursache:** <Hypothese, dokumentiert>
      - **Recovery (idempotent):**
        1. <Schritt>
        2. <Schritt>
      - **Prevention (Pre-Condition oder Code-Aenderung):** <wie wir
        das strukturell verhindern — Verweis auf Pre-Condition-Ticket
        oder Pre-Flight-Check>
      - **Erstmals gesehen:** YYYY-MM-DD (`<log-quelle>`)
      - **Wieder gesehen:** YYYY-MM-DD, YYYY-MM-DD, ... (Append-only)
      - **EARS-Bezug:** TICKET-NNN, EARS-N (Pre-Condition-Verletzung)
      ```
- [ ] When `patterns/known-failures.md` im Skill angelegt wird, the
      system shall am DropboxCheck-Live-Beispiel demonstrieren:
      mind. 2 Failures aus realen 2026-05-Logs migriert + Verweis auf
      die Pre-Conditions in den jeweiligen Tickets.

### Teil B — Bootstrap-Sequenz erweitert

**Pre-Conditions Teil B:**
1. Teil A done
2. `SKILL.md` Sektion A (Bootstrap) ist aktuell

- [ ] When der agile-sdd-skill SKILL.md Sektion A erweitert wird, the
      system shall einen neuen Punkt 10 enthalten:
      ```
      10. docs/KNOWN_FAILURES.md (falls vorhanden) — Symptom-Index
          bekannter Failures. Beim Start jeder Session mit-lesen,
          damit wiederkehrende Probleme nicht erneut ad-hoc geloest
          werden.
      ```
- [ ] When im Projekt `docs/KNOWN_FAILURES.md` NICHT existiert, the
      system shall keinen Stop ausloesen — Datei ist optional pro
      Projekt-Reifegrad (jung = leer ok, reif = Pflicht).

### Teil C — Verifier-Pass erweitert

**Pre-Conditions Teil C:**
1. Teil A+B done
2. Verifier-Pass F.4 ist live (v0.4-Funktionalitaet bleibt erhalten)

- [ ] When im Implementer-Bericht / Verifier-Pass ein Fehler
      diagnostiziert wurde, der zur Recovery fuehrte, the system shall
      pruefen: gibt es einen FAILURE-NNN-Eintrag in
      `docs/KNOWN_FAILURES.md`? Wenn nein → Warning im Verify-Report
      ("Failure-Mode war neu, bitte FAILURE-NNN-Eintrag anlegen").
- [ ] When ein Verifier-Pass-Report den Failure-Mode dokumentiert, the
      system shall den Vorschlag in einem Block "Vorschlag fuer
      KNOWN_FAILURES.md-Eintrag" rendern (copy-paste-faehig).

### Teil D — Hook fuer Auto-Update (leicht)

**Pre-Conditions Teil D:**
1. Teil C done
2. KNOWN_FAILURES.md ist nicht-leer in mind. 1 Projekt

- [ ] When der Verifier-Pass laeuft, the system shall pruefen ob es
      `_retry`/`_v2`-Indikatoren in Log-Files oder Workflow-Outputs
      gab, fuer die KEIN FAILURE-NNN-Eintrag existiert. Wenn ja:
      Warning + Eintragsvorschlag im Verify-Report (nicht
      Hard-Block).

### Teil E — Anti-Rot-Regel

**Pre-Conditions Teil E:**
1. Teil A-D done

- [ ] When ein FAILURE-NNN-Eintrag aelter als 90 Tage ist UND keine
      "Wieder gesehen"-Eintraege in den letzten 30 Tagen hat, the
      system shall den Eintrag im Verify-Report als "Kandidat fuer
      Archiv" markieren (Hinweis: vielleicht durch Code-Fix obsolet
      geworden? bitte verifizieren).
- [ ] When ein Eintrag archiviert wird, the system shall ihn nicht
      loeschen, sondern in `docs/KNOWN_FAILURES_archive.md`
      verschieben (Lern-Material bleibt).

### Teil F — Tests

**Pre-Conditions Teil F:**
1. `tests/test_skill_dev_smoke.py` existiert

- [ ] When der Smoke-Test laeuft, the system shall pruefen:
      - `skills_sources/agile-sdd-skill/templates/KNOWN_FAILURES.md.tpl`
        existiert
      - `skills_sources/agile-sdd-skill/patterns/known-failures.md`
        existiert mit mind. 2 Beispielen
      - `SKILL.md` Sektion A enthaelt Bootstrap-Punkt 10 mit
        Erwaehnung von KNOWN_FAILURES.md

## Technische Hinweise

- **v0.4-Kompatibilitaet:** Wie bei SKILL-004 — neue Datei optional
  pro Projekt, kein Hard-Block bei Fehlen. Backward-compatible.
- **Skill-Version-Bump:** Geht zu v0.6 (oder v0.5 wenn parallel zu
  SKILL-004 gebaut). Empfehlung: erst SKILL-004 live, dann SKILL-006
  separat — saubere Trennung der Risiken.
- **Komplementaritaet zu SKILL-004:** Pre-Conditions verhindern
  Failures **strukturell**. KNOWN_FAILURES.md dokumentiert die
  Failures, die **trotzdem** auftraten (z.B. weil eine Pre-Condition
  uebersehen wurde). Zusammen: closed loop.
- **Anti-Pattern:** Wenn KNOWN_FAILURES.md > 50 Eintraege bekommt
  OHNE dass die Pre-Conditions wachsen, ist das ein Signal dass
  SKILL-004 nicht voll greift. Outcome-Review beachten.

## Code-Referenzen

- `skills_sources/agile-sdd-skill/templates/KNOWN_FAILURES.md.tpl` (NEU)
- `skills_sources/agile-sdd-skill/patterns/known-failures.md` (NEU)
- `skills_sources/agile-sdd-skill/SKILL.md` Sektion A Punkt 10 (NEU)
- `skills_sources/agile-sdd-skill/SKILL.md` Sektion F.4 (Verifier-Pass-Erweiterung)
- `skill_dev/tests/test_skill_dev_smoke.py` (3 neue Test-Cases)

## Out of Scope

- **Auto-Memory ueber CLAUDE.md-Edits durch den Subagent** — siehe
  DEFERRED.md "Auto-Memory-Pattern". Wird erst nach Empirie aus
  Live-Use von KNOWN_FAILURES.md angefasst.
- **Multi-Project-Sync** (KNOWN_FAILURES.md cross-projekt) — bleibt
  projekt-lokal. Cross-Projekt-Patterns wandern in
  `~/.claude/.../memory/feedback_*.md` (separater Mechanismus).
- **Web-UI / Dashboard fuer Failure-Browsing** — Markdown reicht.
- **Strict-Mode Hard-Block** — Warning per Default reicht (siehe
  Vision-Prinzip `skill-schlanker-als-was-er-ersetzt`).

## Voraussetzung

- **SKILL-005 done** (skill-versions.md mit v0.4-Anker fuer Rollback).
- **SKILL-004 NICHT mehr Pflicht-Voraussetzung** (Jakob-Entscheidung
  2026-05-26): KNOWN_FAILURES.md wirkt unabhaengig — die strukturelle
  Wurzel-Loesung (Pre-Conditions) und die Symptom-Dokumentation
  duerfen parallel reifen. Outcome-Zuordnung erfolgt ueber die
  jeweiligen `outcome_review_at`-Hooks.
- Recherche-Note `2026-05-26_Knowledge_Persistence_Flaky_Processes.md`
  als Pflicht-Lesung im Implementer-Briefing.

## Verknuepfte Tickets

- **Trigger:** Recherche 2026-05-26 (Empfehlung 1)
- **Voraussetzung:** SKILL-005 done (Versions-Anker)
- **Parallel bearbeitbar mit:** SKILL-004 (Pre-Conditions) — Jakob-
  Entscheidung 2026-05-26, beide Tickets wirken unabhaengig
- **Komplementaer:** SKILL-004 (Pre-Conditions verhindern strukturell,
  KNOWN_FAILURES dokumentiert Symptome — closed loop)
- **Verbunden:** SKILL-003 (Implementer-Hygiene) — gleicher Geist

## Ergebnis / Notizen

_(wird vom Implementer befuellt)_
