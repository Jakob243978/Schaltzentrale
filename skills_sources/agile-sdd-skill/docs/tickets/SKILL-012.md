---
vision_principle: lessons-aus-live-use-zurueckfuehren
outcome_metric: anti_pattern_im_skill_patterns_ordner
outcome_review_at: null
ui_verify_urls: []
api_endpoints_extended: n/a
---

# SKILL-012: Verifier um Visual-UI-Check (Playwright-Screenshots) erweitern

**Status:** spec
**Erstellt:** 2026-06-02
**MoSCoW:** Should
**Geschaetzter Aufwand:** M (zweigeteilt: Phase 1 Skeleton + Phase 2 Full Implementation)
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren` + `dogfood-zwingt-qualitaet`

## Trigger-Live-Erfahrung

Jakob 2026-06-02 (nach mehreren UI-EARS-Tickets in Immobewertung, die `partial`
blieben weil der Verifier nur Code/Tests prueft und Jakob jedes mal manuell
klicken musste):

> "Sollten wir eigentlich auch in die Verievier packen in den
> urspruenglichen skill oder? Also quasi wenn wir Webapps entwickeln,
> dann sollte auch Screenshots der UI gemacht werden, und falls
> noetig direkt fixes eingebaut werden oder zumindest im Veryfier
> gefeedbackt werden als nicht bestandenen Test. So spare ich mir
> nochmal Arbeit und werde eher die Arbeit machen, die es braucht,
> um den Mehrwert des Produktes sicher zu stellen. Das macht mehr
> Sinn als PO, sonst bin ich ja nur ein Tester."

Pattern: Heute prueft der Verifier (siehe `verifier/VERIFIER.md`) nur Tests +
Health-Check + Diff. UI-EARS-Saetze bleiben per Konvention max. `partial`
(siehe Lesson Learned T009: Source-Code-Substring-Match ist kein Hover-Test)
— die Abnahme verlagert sich auf Jakobs manuellen Browser-Klick. Konsequenz:
Jakob faellt in eine Tester-Rolle, statt PO zu sein.

**Komplementaer-Verhaeltnis zu SKILL-007 (Reveal-Visual-Review):**
SKILL-007 hat Chromium-Screenshot-Pass im **reveal-presentation-Build**
operationalisiert. SKILL-012 verallgemeinert das Muster auf den **SDD-Verifier
fuer Webapps**. Tech-Stack hier ist `Playwright Python` statt Bash-Chromium-
Wrapper (robuster, MIT-Lizenz, headless out-of-the-box, lest Console-Errors).

## Pre-Conditions

1. `skills_sources/agile-sdd-skill/verifier/VERIFIER.md` existiert und ist
   live deployed unter `~/.claude/skills/agile-sdd-skill/verifier/VERIFIER.md`.
2. `skills_sources/agile-sdd-skill/templates/verify-report.md` existiert
   (heute v0.4 mit Cost-Tracking-Frontmatter).
3. `skills_sources/agile-sdd-skill/templates/TICKET.md` existiert.
4. Playwright Python (`playwright`) ist **nicht** Pflicht-Installiert — Verifier
   pruefty Verfuegbarkeit und faellt graceful auf `partial` + Hinweis zurueck
   (analog zu ccusage-Fallback in VERIFIER.md Schritt 7c). NIEMALS automatisch
   `pip install` aus dem Verifier.
5. Mind. 1 Live-Beispiel-Ticket existiert, das den neuen Pass durchlaufen kann
   (Immobewertung T097 oder T103 — UI-EARS mit konkreten Routen wie
   `/property/2`).

## Was soll erreicht werden? (Business-Ziel)

Der SDD-Verifier-Subagent fuehrt fuer Tickets mit UI-EARS-Saetzen
**automatisch einen Visual-UI-Check** durch (Phase nach Test-Run, vor Token-
Aggregation), produziert Screenshots + Console-Error-Report, und embedded
das Ergebnis im Verify-Report. So entscheidet Jakob nicht mehr "klick ich
oder klick ich nicht", sondern nur "passt das Bild oder nicht".

Ziel-Effekt:
- **Jakob bleibt PO**, nicht Klick-Tester. Verifier liefert visuellen Beleg.
- **UI-EARS kann auf `partial+visual_pass`** angehoben werden (neuer Sub-Status),
  der die `po_acceptance: confirmed`-Huerde aufweicht (Jakob reviewed das
  Screenshot-Embed im Report statt im Browser).
- **Anti-Pattern "Verifier sagt grun, UI ist kaputt"** wird verbindlich
  geschlossen (Live-Beispiel: T097 Marktanalyse-Card war im Code da, im
  Browser unsichtbar wegen CSS-Conflict — Verifier hat das nie gesehen).

> [!info] Komplementaer zu SKILL-007 (Reveal-Visual-Review)
> SKILL-007 macht Screenshots im Reveal-Build-Workflow. SKILL-012 macht sie
> im SDD-Verifier-Workflow fuer Webapps. Beide nutzen den gleichen
> Konzept-Backbone ("Bild ist die Wahrheit, Code ist die Hoffnung"), aber
> unterschiedliche Skills und Tech-Stacks.

## Akzeptanzkriterien (EARS-Format mit Pre-Conditions)

### Teil A — Trigger-Erkennung im Verifier

**Pre-Conditions Teil A:**
1. `verifier/VERIFIER.md` heute Schritt 0-7 (siehe SKILL-010-Layout)

- [ ] When der Verifier ein Ticket prueft, the system shall **automatisch
      erkennen ob ein Visual-Check noetig ist** anhand:
      1. Ticket-Frontmatter enthaelt `ui_verify_urls: [<liste>]` mit mind. 1 URL
      2. ODER: Diff enthaelt Files unter `frontend/` (`frontend/app/`,
         `frontend/components/`, `frontend/pages/`)
      3. ODER: Mind. 1 EARS-Satz wurde in Schritt 0 als `ui` klassifiziert
- [ ] When kein Trigger zutrifft, the system shall die Visual-Check-Sektion im
      Report mit "n/a — kein UI-Touch im Diff" markieren und ohne weitere
      Arbeit zu Schritt 7 (Token-Aggregation) springen.

### Teil B — Visual-Check-Sub-Step (Schritt 6.5 zwischen API-Schema-Check und Token-Aggregation)

**Pre-Conditions Teil B:**
1. Teil A done (Trigger-Logik im Verifier-Algorithmus dokumentiert)
2. Playwright Python verfuegbar ODER Fallback-Pfad definiert

- [ ] When Visual-Check getriggert ist UND `ui_verify_urls` befuellt ist,
      the system shall fuer jede URL:
      1. Headless-Browser starten (Playwright Chromium)
      2. Navigieren, auf Network-Idle warten (timeout 5s)
      3. Screenshot speichern unter
         `<verify_report_path>/screenshots/TICKET-NNN-<slug>.png`
      4. Console-Errors (Severity: error) einsammeln
      5. Failed-Network-Requests einsammeln (Status >= 400)
- [ ] When Visual-Check getriggert ist ABER `ui_verify_urls` leer ist,
      the system shall Fallback nutzen:
      1. Frontend-Diff scannen nach Routen-Pattern (`page.tsx`, `app/*/page.tsx`,
         `routes/*.tsx`)
      2. Bei Fund: erste 3 erkannte Routen automatisch screenshooten
      3. Bei keinem Fund: Status `partial` + Notiz "ui_verify_urls fehlt im
         Ticket-Frontmatter — bitte Implementer/PO nachtragen"
- [ ] When Playwright nicht verfuegbar ist (Import-Error oder Browser-Binary
      fehlt), the system shall **nicht** `pip install` machen, sondern:
      - Visual-Check-Status auf `skipped_tool_missing`
      - Verify-Report bekommt Notiz mit Setup-Befehl
        (`pip install playwright && playwright install chromium`)
      - EARS-Status der UI-Saetze bleibt unveraendert auf `partial`

### Teil C — Verify-Report Sektion "Visual UI Verification"

**Pre-Conditions Teil C:**
1. `templates/verify-report.md` enthaelt heute Sektionen Zusammenfassung,
   EARS-Pruefung, Test-Output, Health-Check, Manuelle PO-Abnahme, Empfehlungen,
   Verifier-Metadaten (siehe File)
2. Teil B done (Visual-Check produziert Output)

- [ ] When das Verify-Report-Template erweitert wird, the system shall eine
      neue Sektion `## Visual UI Verification` direkt nach "Health-Check"
      und vor "Manuelle PO-Abnahme" enthalten, mit:
      - **Status-Zeile:** `not_required | pass | partial | fail | skipped_tool_missing`
      - **Pro URL:** Pfad, Screenshot-Embed (`![alt](screenshots/...png)`),
        Console-Error-Count, Failed-Network-Request-Count
      - **Pass-Kriterien (Default):** 0 Console-Errors, 0 Failed-Requests,
        Screenshot existiert und ist >0 Bytes
      - **Fail-Kriterien:** Mind. 1 Console-Error ODER mind. 1 Failed-Request
        ODER Screenshot fehlt
- [ ] When Visual-Check `fail` zurueckliefert, the system shall den Overall-
      Verify-Status auf `partial` (nicht hoeher) setzen — analog zur API-Schema-
      Coverage-Regel in Schritt 6.

### Teil D — Ticket-Template-Feld `ui_verify_urls`

**Pre-Conditions Teil D:**
1. `templates/TICKET.md` enthaelt heute die Sektionen: Status, Erstellt,
   MoSCoW, Aufwand, Business-Ziel, EARS-Kriterien, API-Schema-Kontrakt,
   Technische Hinweise, Code-Referenzen, Ergebnis (siehe File)

- [ ] When `templates/TICKET.md` erweitert wird, the system shall im
      Frontmatter-Block eine optionale Liste `ui_verify_urls:` dokumentieren,
      mit Hinweis im Body-Bereich:
      ```yaml
      ui_verify_urls:
        - path: /property/2
          expect: Marktanalyse-Card sichtbar
        - path: /property/287
          expect: DDR-Empfehlung sichtbar
      ```
      Erlaubte Formate: nur `path` (string) ODER `path + expect` (object).
- [ ] When ein Ticket Frontmatter ohne `ui_verify_urls` hat, the system shall
      kein Hard-Block ausloesen (Feld ist optional) — nur die Fallback-Logik
      in Teil B greift.

### Teil E — Skeleton-Code `verifier/visual_check.py`

**Pre-Conditions Teil E:**
1. `skills_sources/agile-sdd-skill/verifier/` ist heute nur Markdown
   (`VERIFIER.md` + `verifier-prompt.md`) — Python-Module dort sind Neuland

- [ ] When dieses Ticket Phase 1 (Skeleton) done ist, the system shall die
      Datei `skills_sources/agile-sdd-skill/verifier/visual_check.py`
      enthalten mit:
      - Modul-Docstring mit Phasen-Plan-Verweis
      - Dataclass `VisualCheckResult` (status, urls, screenshots, console_errors,
        network_errors, notes)
      - Funktion `def run_visual_check(ticket_urls: list[dict], output_dir: Path) -> VisualCheckResult:`
        mit TODO-Skeleton (Playwright-Import-Guard, Screenshot-Loop-Stub,
        Result-Aggregation-Stub)
      - Funktion `def render_report_section(result: VisualCheckResult) -> str:`
        die Markdown-Embed-Block fuer den Verify-Report zurueckliefert
      - Kein lauffaehiger Code, nur Architektur-Stubs mit klaren TODO-Markern
      - Header-Kommentar: "Phase 1: Skeleton — keine Runtime-Logik. Phase 2:
        Volle Playwright-Impl. Siehe SKILL-012."

### Teil F — VERIFIER.md Algorithmus-Update

**Pre-Conditions Teil F:**
1. `verifier/VERIFIER.md` heute mit Schritten 0-7 (siehe File)

- [ ] When `verifier/VERIFIER.md` erweitert wird, the system shall einen neuen
      **Schritt 6.5 "Visual UI Verification"** zwischen heutigem Schritt 6
      (API-Schema-Coverage) und Schritt 7 (Token-Aggregation) enthalten,
      mit:
      - Verweis auf `verifier/visual_check.py`
      - Trigger-Logik (Frontmatter ODER Frontend-Diff ODER UI-EARS)
      - Status-Aggregation (skipped/pass/partial/fail)
      - Hinweis: "Verifier installiert NIEMALS Playwright selbst"
- [ ] When der Verifier die Sektion "Output A) Verify-Report" referenziert,
      the system shall die neue Sektion "Visual UI Verification" in der
      Pflicht-Befuellung-Liste erwaehnen.

### Teil G — Tests (Smoke, Phase 1)

**Pre-Conditions Teil G:**
1. `skill_dev/tests/test_skill_dev_smoke.py` existiert

- [ ] When der Smoke-Test laeuft, the system shall pruefen:
      - `skills_sources/agile-sdd-skill/verifier/visual_check.py` existiert
        und enthaelt Substring "VisualCheckResult" + "run_visual_check"
      - `templates/verify-report.md` enthaelt Substring "Visual UI Verification"
      - `templates/TICKET.md` enthaelt Substring "ui_verify_urls"
      - `verifier/VERIFIER.md` enthaelt Substring "Schritt 6.5" + "visual_check.py"

## Phasen-Plan

| Phase | Scope | Status | Output |
|---|---|---|---|
| **1 — Spec + Skeleton + Template-Erweiterung** | dieser Ticket-Anlauf | **spec** (heute) | Ticket SKILL-012, `visual_check.py` (Stubs), Diff-Vorschlaege fuer 3 Templates, Tests-Stub |
| **2 — Full Implementation + Smoke-Run** | Folge-Ticket SKILL-012b | tbd | Lauffaehiger Visual-Check, Run gegen Immobewertung T097 oder T103, erste 3 Verify-Reports mit eingebetteten Screenshots |
| **3 — Visual-Regression (Baseline-Comparison)** | optionales Folge-Ticket SKILL-012c | tbd (entscheiden ueber Tool: pixelmatch / Percy / Chromatic / pure-Python-pixel-diff) | Baseline-Verzeichnis pro Ticket-Branch, Diff-Report bei Re-Run |

## Architektur

```
Verifier-Subagent (frische Session)
  │
  ├─ Schritt 0   EARS-Typ-Klassifizierung (ui|backend)
  ├─ Schritt 1-5 EARS-Pruefung pro Satz
  ├─ Schritt 6   API-Schema-Coverage-Check (SKILL-010)
  ├─ Schritt 6.5 ★ NEU: Visual UI Verification (SKILL-012)
  │     │
  │     ├─ Trigger? (ui_verify_urls | frontend-Diff | ui-EARS)
  │     ├─ Playwright verfuegbar? (Import-Guard, kein pip-install)
  │     ├─ visual_check.run_visual_check(urls, output_dir)
  │     │     ├─ launch chromium headless
  │     │     ├─ navigate + wait_for_load
  │     │     ├─ screenshot → screenshots/TICKET-NNN-<slug>.png
  │     │     ├─ collect console_errors + failed_requests
  │     │     └─ return VisualCheckResult
  │     └─ visual_check.render_report_section(result)
  │           → Markdown-Block fuer Verify-Report
  └─ Schritt 7   Token-Aggregation + Report-Erstellung
```

## Tool-Stack

- **Playwright Python** (`pip install playwright && playwright install chromium`)
  - Standard 2026, breite Adoption, headless out-of-the-box
  - Liefert Console-Errors + Network-Status nativ
  - MIT-Lizenz
- **Screenshot-Format:** PNG, 1280x800 Default (overridable via
  `ui_verify_viewport` in sdd-config.yaml — Phase 2)
- **Ablage:** `<verify_report_path>/screenshots/TICKET-NNN-<slug>.png`
  (z.B. `docs/tickets/verify/screenshots/TICKET-097-property-2.png`)
- **Visual-Regression (Phase 3):** offene Entscheidung (siehe "Was Jakob
  entscheiden muss")

## Code-Referenzen

- `skills_sources/agile-sdd-skill/verifier/visual_check.py` (NEU, Phase 1 Skeleton)
- `skills_sources/agile-sdd-skill/verifier/VERIFIER.md` (Schritt 6.5 ergaenzen, Phase 1)
- `skills_sources/agile-sdd-skill/templates/verify-report.md` (Sektion "Visual UI Verification" ergaenzen, Phase 1)
- `skills_sources/agile-sdd-skill/templates/TICKET.md` (Frontmatter-Feld `ui_verify_urls` dokumentieren, Phase 1)
- `skills_sources/agile-sdd-skill/SKILL.md` (Sektion F.4 / Verify-Pass-Beschreibung referenziert neuen Schritt — Phase 2)
- `skill_dev/tests/test_skill_dev_smoke.py` (4 neue Test-Cases — Phase 1)
- `skills_sources/agile-sdd-skill/templates/sdd-config.yaml.example`
  (Defaults `visual_check_enabled: auto`, `visual_check_viewport: 1280x800`,
  Phase 2)

## API-Schema-Kontrakt

- [x] Aendert dieses Ticket ein Datenmodell? **Nein** (kein DB-Touch — nur
      Skill-Source-Files und Templates).
- [x] Frontmatter `api_endpoints_extended: n/a` gesetzt.

## Out of Scope

- **Automatischer Fix von visuellen Bugs** — Verifier flagt nur, fixt nicht
  (analog zur Code-Aenderungs-Sperre in VERIFIER.md "Was du NICHT tust").
  Auto-Iteration ist Sache von SKILL-007 im Reveal-Kontext, nicht hier.
- **Multi-Browser-Testing** (Firefox, WebKit) — Chromium reicht als Baseline.
  Cross-Browser-Tests sind eigener Skill-Use-Case (deferred).
- **Visual-Regression mit Baseline-Comparison** — Phase 3, entkoppelt.
- **Authentication-Flows** (Login, Cookies, Session) — Phase 2 muss Default-
  Annahme "Public Route" treffen. Auth-Required-Routen sind Phase 3+.
- **Interaktion (Klicks, Form-Submissions)** — Phase 1+2 nur Navigate +
  Screenshot. Interaction-Tests waeren ein eigenes Konzept (Test-User
  Story-Recording).
- **Mobile-Viewport-Tests** — wenn jemals relevant, Frontmatter-Feld
  `ui_verify_viewport_mobile: yes` als Phase-3-Erweiterung.

## Verknuepfte Tickets

- **Trigger:** Jakob 2026-06-02 (Zitat oben) — Live-Erfahrung aus
  Immobewertung-UI-EARS-Wellen T097/T101/T103
- **Komplementaer:** SKILL-007 (Reveal-Visual-Review) — gleicher Konzept-
  Backbone, anderer Skill / anderer Tech-Stack
- **Erweitert:** SKILL-010 (API-Schema-Coverage) — neue Verifier-Schritt
  reiht sich ein
- **Live-Pattern:** Lesson Learned T009 in SKILL.md F.4 — "Substring-Match
  ist kein Hover-Test" wird durch Visual-Check entkraeftet

## Voraussetzung

- Playwright Python ist als optionale Abhaengigkeit dokumentiert
  (`pip install playwright && playwright install chromium`).
- Skeleton-Code in Phase 1 ist **nicht** lauffaehig — bewusster Cut, damit
  Architektur fix ist bevor Tooling-Wahl in Phase 2 final wird.

## Ergebnis / Notizen

_(wird vom Implementer in Phase 2 befuellt)_

**Phase 1 (Spec + Skeleton, 2026-06-02):**

Phase 1 ist mit dem Anlegen dieses Tickets, der `visual_check.py`-Skelett-Datei
sowie den Diff-Vorschlaegen unter `### Diff-Vorschlaege fuer Phase 1` (unten in
diesem Ticket-Body als Hinweis-Block) abgeschlossen. **Kein `setup.ps1`-Lauf** —
Jakob entscheidet manuell wann deployed wird (Anti-Pattern: stilles Re-Deploy
bricht Skill-Versionierung).

### Diff-Vorschlaege fuer Phase 1 (nicht-applied, Hinweise fuer den Phase-2-Implementer)

**1) `templates/verify-report.md` — neue Sektion vor "Manuelle PO-Abnahme":**

```markdown
## Visual UI Verification

**Status:** not_required | pass | partial | fail | skipped_tool_missing

> Wenn `not_required`: kein UI-Touch im Diff, keine `ui_verify_urls` im
> Ticket-Frontmatter, keine UI-EARS-Saetze — Sektion mit "n/a" markieren.
>
> Wenn `skipped_tool_missing`: Playwright nicht verfuegbar — Setup-Befehl
> notieren, Verifier-Status der UI-EARS bleibt `partial`.

### Pro URL

#### URL 1: <path>

- **Screenshot:** ![<path>](screenshots/TICKET-NNN-<slug>.png)
- **Console-Errors:** <count> (Details: [error1, error2, ...])
- **Failed-Network-Requests:** <count> (Details: [url1 (4xx), url2 (5xx), ...])
- **Erwartung (aus Ticket-Frontmatter):** "<expect>"
- **Pass/Fail:** pass | fail

### Aggregat

- **URLs gepruft:** <n>
- **URLs pass:** <n_pass>
- **URLs fail:** <n_fail>
- **Empfehlung:** [konkret, z.B. "EARS-3 Marktanalyse-Card war auf /property/2 nicht sichtbar — Folge-Ticket noetig"]
```

**2) `templates/TICKET.md` — Frontmatter-Erweiterung im Body-Hinweisblock:**

```yaml
# Optional. Liste der URLs die nach Implementierung visuell gescreenshotted werden.
# Wird vom Verifier (SKILL-012, Schritt 6.5) konsumiert.
ui_verify_urls:
  - path: /property/2
    expect: Marktanalyse-Card sichtbar
  - path: /property/287
    expect: DDR-Empfehlung sichtbar
```

**3) `verifier/VERIFIER.md` — neuer Schritt 6.5 (direkt nach Schritt 6, vor heutigem Schritt 7):**

```markdown
6.5. **Visual-UI-Check** (SKILL-012, 2026-06-02) — VOR Token-Aggregation.

   Pflicht-Check fuer Tickets mit Web-UI-Touch. Trigger:
   - Ticket-Frontmatter `ui_verify_urls: [...]` befuellt, ODER
   - Diff enthaelt Files unter `frontend/`, ODER
   - Mind. 1 EARS-Satz in Schritt 0 als `ui` klassifiziert

   Wenn kein Trigger: Sektion mit `not_required` markieren, kein Status-Einfluss.

   Wenn Trigger:
   1. Pruefe Playwright-Verfuegbarkeit:
      ```python
      try:
          from playwright.sync_api import sync_playwright
      except ImportError:
          status = "skipped_tool_missing"
      ```
      Bei `skipped_tool_missing`: Setup-Befehl im Report notieren
      (`pip install playwright && playwright install chromium`), KEIN
      automatisches `pip install` (analog ccusage-Fallback).
   2. Rufe `verifier/visual_check.py::run_visual_check(urls, output_dir)` auf:
      - URLs aus Frontmatter `ui_verify_urls` ODER aus Frontend-Diff-Scan
      - `output_dir = <verify_report_path>/screenshots/`
   3. Aggregiere Result:
      - 0 console_errors + 0 network_errors pro URL → URL = pass
      - Mind. 1 Fehler → URL = fail
   4. Setze Sektion "Visual UI Verification" im Report (Template).
   5. Status-Aggregation: mind. 1 URL = fail → Overall Verify-Status MUSS
      auf `partial` (nicht hoeher), auch wenn EARS-Saetze alle gruen sind.
      Analog zur API-Schema-Coverage-Regel in Schritt 6.

   **Wichtig:** Der Verifier installiert NIEMALS Playwright selbst. Bei
   fehlendem Tool immer `skipped_tool_missing`-Fallback.
```
