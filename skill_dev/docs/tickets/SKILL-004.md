# SKILL-004: EARS-Pre-Conditions als Pflicht im SDD-Ticket-Template + Verifier-Check

**Status:** spec
**Erstellt:** 2026-05-26
**MoSCoW:** Must
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren` + `dogfood-zwingt-qualitaet`
**outcome_metric:** anti_pattern_im_skill_patterns_ordner (Ziel: dokumentiertes Pre-Condition-Pattern + mind. 1 Live-Anwendung in DropboxCheck-Ticket sichtbar)
**outcome_review_at:** null (wird beim done-Set gesetzt)
**Trigger-Recherche:** `Researcher/jakob/spec-driven-development/recherche/2026-05-26_Knowledge_Persistence_Flaky_Processes.md` Empfehlung 2 ("die EINE Maßnahme, die das Problem am meisten löst")
**Skill-Vorversion:** agile-sdd-skill v0.4 (siehe `docs/skill-versions.md`)

> [!info] Pre-Conditions dieses Tickets (Dogfood-Beispiel)
> Dieses Ticket nutzt selbst das vorgeschlagene Pre-Condition-Format —
> bewusst als Meta-Beispiel. Wenn die Pre-Conditions hier nicht erfuellt
> sind, kann der Implementer nicht starten:
>
> 1. SKILL-001 ist im Status `review` oder `done` (PO-Skill existiert) — verifiziere via `ls skills_sources/po-skill/SKILL.md`
> 2. `docs/skill-versions.md` existiert und haelt einen Eintrag fuer agile-sdd v0.4 mit konkretem Commit-Hash (siehe SKILL-005-parallel oder vorab manuell) — verifiziere via `grep "v0.4" docs/skill-versions.md`
> 3. agile-sdd v0.4 ist live deployed und funktional validiert (Verifier-Pass + Cost-Tracking laufen in Immobewertung) — verifiziere via `ls ~/.claude/skills/agile-sdd-skill/SKILL.md` + Frontmatter-Version

## Was soll erreicht werden? (Business-Ziel)

Jakob beobachtet aus DropboxCheck: Pre-Conditions fuer UI-Schritte
(z.B. "LR ist offen", "kein modaler Dialog", "Lock-Files weg") leben heute
**implizit** — in CLAUDE.md-Fliesstext, Code-Kommentaren, im Kopf des
Entwicklers. Folge: bei jeder Re-Implementierung oder neuem Subagent gehen
sie verloren, der gleiche Fehler tritt wieder auf, Datei-Vermehrung
(e2e_v3..v12) ohne Konsolidierung.

Recherche-Kern (2026-05-26): EARS-Standard erlaubt explizit 0-N
Pre-Conditions ("`While [pre-conds], when [trigger], the system shall
[response]`"). Wenn Pre-Conditions als feste Sektion im Ticket-Template
vorgesehen sind und der Verifier-Pass prueft ob sie im Code aktiv
verifiziert werden, wird das Wissen ueber Pre-Conditions **strukturell
sichtbar** — es bleibt nicht mehr nur im Kopf des Entwicklers.

> [!info] Warning, kein Hard-Block (Design-Entscheidung Jakob 2026-05-26)
> Pre-Conditions werden als **Warning** geliefert, nicht als Hard-Block.
> Begruendung: Pre-Conditions werden nicht in jedem Ticket passen — die
> Regel ist „pruefe + dokumentiere wenn relevant", nicht „blockiere ohne".
> **Kein Strict-Mode geplant** (kein `SDD_STRICT_PRE_CONDITIONS=1`, kein
> Folge-Ticket). Das ist eine bewusste Design-Entscheidung, nicht ein
> „spaeter vielleicht".

Ziel: Das Ticket-Template + die Verifier-Pass-Logik im `agile-sdd-skill`
um eine **Sektion Pre-Conditions** erweitern (im Template fest vorgesehen,
in der Anwendung pro Ticket optional). Bestandsschutz fuer v0.4-Tickets:
legacy-Tickets ohne Pre-Conditions bleiben gueltig, neue Tickets (ab
Skill-Version >= 0.5) sollten das neue Format nutzen, fehlen Pre-
Conditions wird gewarnt, nicht blockiert.

## Akzeptanzkriterien (EARS-Format mit Pre-Conditions)

### Teil A — Ticket-Template erweitert

**Pre-Conditions Teil A:**
1. `templates/TICKET.md` im agile-sdd-skill existiert (heutige Pflicht-Sektion B)
2. Aktuelle Version v0.4 ist als Tag/Eintrag in `docs/skill-versions.md` festgehalten (Rollback moeglich)

- [ ] When ein neues SDD-Ticket-Template ausgerollt wird (Skill-Version
      >= 0.5), the system shall im `templates/TICKET.md` eine
      **Pflicht-Sektion "Pre-Conditions"** vor den EARS-Akzeptanzkriterien
      enthalten, mit folgendem Format:
      ```
      ## Pre-Conditions
      <!-- Welche Anfangszustaende muessen erfuellt sein? -->
      1. <Pre-Condition> — verifiziere via <konkrete Pruefung>
      2. ...
      ```
- [ ] When ein EARS-Satz im Ticket steht, the system shall folgendes
      Format unterstuetzen (Empfehlung, nicht Hard-Block):
      ```
      - [ ] While [Pre-Conditions PC-1, PC-2, ...], when [Trigger],
            the system shall [Response].
      ```
      (EARS-Standard erlaubt 0-3 inline-Pre-Conditions; > 3 → Tabelle.)
- [ ] When eine Pre-Condition gelistet wird, the system shall ein
      `Detection bei Verletzung`-Feld optional anbieten (Hinweis: was
      passiert wenn die Pre-Condition zur Laufzeit kaputt geht?).

### Teil B — Verifier-Pass erweitert (F.4)

**Pre-Conditions Teil B:**
1. agile-sdd-skill Verifier-Pass v0.4 existiert in `SKILL.md` Sektion F.4 — verifiziere via Read auf den entsprechenden Abschnitt
2. Verifier-Reports liegen in `<verify_report_path>/TICKET-NNN-verify-*.md`

- [ ] When der Verifier-Pass (Sektion F.4) einen `review`-Status pruefen
      soll und das Ticket Pre-Conditions auflistet, the system shall pro
      Pre-Condition pruefen ob im Code (oder Test-Suite) eine aktive
      Verifikation existiert.
- [ ] When eine Pre-Condition gelistet ist, aber im Code **nicht** aktiv
      verifiziert wird, the system shall den Verify-Status auf `partial`
      setzen (nicht `pass`) und im Report Klartext-Hinweis liefern:
      "PC-N wird gelistet, aber keine Verifikation gefunden — Hard-Fail
      moeglich zur Laufzeit, kein Test schlaegt an."
- [ ] When ein Ticket aus Skill-Version < 0.5 stammt (legacy, vor diesem
      Ticket), the system shall die Pre-Condition-Pflicht **nicht**
      erzwingen (Bestandsschutz).

### Teil C — Migrationspfad & Doku

**Pre-Conditions Teil C:**
1. Teil A+B sind implementiert
2. `docs/skill-versions.md` haelt die neue Version v0.5 bereit als Eintrag

- [ ] When Teil A+B implementiert sind, the system shall in
      `skills_sources/agile-sdd-skill/SKILL.md`-Frontmatter die Version
      auf `0.5` setzen.
- [ ] When die neue Version live geht, the system shall eine Doku-Datei
      `skills_sources/agile-sdd-skill/patterns/pre-conditions.md` haben
      mit:
      - Erlaeuterung des Patterns am DropboxCheck-Live-Beispiel
      - 2 Minimal-Templates (1 mit Pre-Conditions, 1 ohne — fuer
        einfache Backend-Tickets bleibt Pre-Conditions optional)
      - Verweis auf [Alistair Mavin EARS Official Guide](https://alistairmavin.com/ears/)
      - "Wann Pre-Conditions Pflicht sind" — Heuristik:
        - UI-Automation: immer
        - State-modifizierende Worker mit externen Locks: immer
        - Backend-Logik ohne externen State: optional
- [ ] When ein neues Ticket nach v0.5 angelegt wird und keine
      Pre-Conditions hat, the system shall im Bootstrap-Hint warnen
      (nicht blockieren): "Dieses Ticket hat keine Pre-Conditions.
      Bewusste Entscheidung? Falls UI/State involved → bitte ergaenzen."

### Teil D — Tests (Smoke)

**Pre-Conditions Teil D:**
1. `skill_dev/tests/test_skill_dev_smoke.py` existiert und ist lauffaehig

- [ ] When `tests/test_skill_dev_smoke.py` ausgefuehrt wird, the system
      shall einen Test enthalten, der prueft:
      - `skills_sources/agile-sdd-skill/templates/TICKET.md` enthaelt die
        Zeichenkette `## Pre-Conditions`
      - `skills_sources/agile-sdd-skill/SKILL.md` Frontmatter-Version
        ist >= 0.5
      - `skills_sources/agile-sdd-skill/patterns/pre-conditions.md`
        existiert

## Technische Hinweise

- **v0.4-Kompatibilitaet:** legacy-Tickets bleiben gueltig, Verifier
  **warnt** (nicht: blockiert) bei fehlenden Pre-Conditions nur fuer
  Tickets mit `created >= 2026-XX-XX` (Datum = Tag des Mergens dieses
  Tickets) ODER via Skill-Version-Check im Verifier-Bootstrap.
- **Breaking?** Nein — auch fuer NEUE Tickets ab v0.5 ist die Pre-
  Condition-Sektion **Warning-only**, nicht erzwungen. Bestehende
  `in_progress`/`review`-Tickets in Immobewertung/DropboxCheck etc.
  bleiben uneingeschraenkt. Migrationspfad: Bei naechstem Anfassen eines
  legacy-Tickets soll der Implementer einladen die Pre-Conditions
  nachzutragen (Sanft-Hinweis im Briefing).
- **Skill-Vorversion-Tag:** Bevor SKILL.md angefasst wird, muss
  `docs/skill-versions.md` einen klaren Eintrag fuer v0.4 haben (siehe
  SKILL-005). Das ermoeglicht Rollback per `git checkout <tag>` falls
  die Pre-Condition-Warnings in der Praxis Reibung erzeugen.
- **Anti-Pattern aus Recherche:** Pre-Conditions sind KEIN Ersatz fuer
  KNOWN_FAILURES.md (SKILL-006). Sie ergaenzen sich:
  - Pre-Conditions = strukturelle Bedingungen IM Ticket (vorher)
  - KNOWN_FAILURES.md = Symptom-Index BEKANNTER Failures (nachher,
    iterativ gewachsen aus Live-Use)

## Code-Referenzen

- `skills_sources/agile-sdd-skill/templates/TICKET.md` (neue Sektion)
- `skills_sources/agile-sdd-skill/SKILL.md` (Sektion B + F.4 + Frontmatter version=0.5)
- `skills_sources/agile-sdd-skill/patterns/pre-conditions.md` (NEU)
- `skill_dev/tests/test_skill_dev_smoke.py` (3 neue Test-Cases)
- `skill_dev/docs/skill-versions.md` (Rollback-Anker, siehe SKILL-005)

## Out of Scope

- **Automatische Pre-Condition-Generierung aus Code** (z.B. AST-Analyse
  von `pre_flight.py`) — manuell-deklarativ reicht.
- **State-Machine-Framework** (UiPath REFramework, python-statemachine).
  Bleibt projekt-spezifisch (siehe DropboxCheck-Folge-Tickets).
- **Hard-Block bei fehlenden Pre-Conditions / Strict-Mode** — Pre-
  Conditions werden als **Warning** geliefert, nicht als Hard-Block.
  Begruendung (Jakob 2026-05-26): Pre-Conditions werden nicht in jedem
  Ticket passen — die Regel ist „pruefe + dokumentiere wenn relevant",
  nicht „blockiere ohne". **Kein Strict-Mode geplant** — kein Future-
  Promise auf `SDD_STRICT_PRE_CONDITIONS=1` oder ein Folge-Ticket
  dafuer. Das ist eine bewusste Design-Entscheidung, nicht ein „spaeter
  vielleicht".
- **Migration aller alten Tickets in Immobewertung/DropboxCheck** — nicht
  Pflicht; passive Migration (beim naechsten Touch) reicht.

## Voraussetzung

- SKILL-005 (Skill-Versions-Anker fuer v0.4) muss `done` sein, bevor
  dieses Ticket auf `in_progress` geht. Sonst gibt es keinen sauberen
  Rollback-Punkt.
- Recherche-Note `2026-05-26_Knowledge_Persistence_Flaky_Processes.md`
  als Pflicht-Lesung im Implementer-Briefing.

## Verknuepfte Tickets

- **Trigger:** Recherche 2026-05-26 (Empfehlung 2)
- **Voraussetzung:** SKILL-005 (Skill-Versions-Anker)
- **Verbunden:** SKILL-006 (KNOWN_FAILURES.md — komplementaer)
- **Indirekt:** SKILL-003 (Implementer-Hygiene) — gleicher Geist
  ("Wissen strukturell verankern statt im Subagent-Kontext lassen")

## Ergebnis / Notizen

_(wird vom Implementer befuellt)_
