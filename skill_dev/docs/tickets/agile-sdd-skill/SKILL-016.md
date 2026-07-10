---
vision_principle: lessons-aus-live-use-zurueckfuehren
outcome_metric: done_tickets_mit_vollstaendigem_verify_report
outcome_review_at: null
ui_verify_urls: []
api_endpoints_extended: n/a
surface: backend
---

# SKILL-016: Hartes Verify-Gate vor `done` + aktiver Bootstrap-Listen-Check

**Status:** spec
**Erstellt:** 2026-06-14
**MoSCoW:** Must
**Geschaetzter Aufwand:** S (Skill-Doku-Aenderung: Status-Gate-Regel verschaerfen +
Bootstrap-Schritt-8 von passiv auf aktiv-listend; keine neue Runtime-Logik)
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren`

## Trigger-Live-Erfahrung

Jakob 2026-06-14 (AgentischesArbeiten, nach einer Wellen-Session mit vielen
parallel abgearbeiteten Tickets):

> „Heute standen viele Tickets auf `review`/`done` OHNE Verify-Report, obwohl der
> Verify-Pass die Pflicht-Stufe vor `done` ist — es brauchte meinen expliziten
> Hinweis. Fehlt uns im Verifier im SDD-Skill noch etwas, damit das zuverlaessig
> passiert?"

**Quantifizierter Befund (AgentischesArbeiten, Stand 2026-06-14):** Mehrere
Tickets standen auf `done` OHNE Verify-Report in `docs/tickets/verify/`
(z.B. TICKET-005, -014, -015, -016, -023, -032, -056) und mehrere auf `review`
ohne Report (z.B. TICKET-035, -039, -041, -066). Erst eine manuell ausgeloeste
Verifier-Nachhol-Welle hat die Reports erzeugt. Das System hat den Verstoss
nicht selbst sichtbar gemacht.

## Diagnose — warum greift es nicht zuverlaessig?

Drei strukturelle Luecken im aktuellen Skill (v0.5):

1. **Bootstrap-Schritt 8 („Verify-Status pruefen") ist rein passiv.** Er sagt
   „dem User aktiv vorschlagen, `/sdd-verify` auszufuehren" — aber nur fuer
   `review`-Tickets, ohne **Liste**, ohne `done`-Tickets zu pruefen, und ohne
   Schwelle. In einer langen Welle geht dieser eine Satz unter; niemand zaehlt
   die ungeprueften Tickets aktiv auf.
2. **Es gibt kein hartes Status-Gate.** Sektion B sagt zwar „Erst wenn
   `verify_status: pass` UND `po_acceptance` ... darf das Ticket auf `done`",
   aber das ist als **Workflow-Beschreibung** formuliert, nicht als
   ueberpruefbare **Vorbedingung** mit klarem „STOPP, wenn Report fehlt".
   Der Implementer kann `done` setzen, ohne dass irgendwo geprueft wird, ob
   `docs/tickets/verify/TICKET-NNN-verify-*.md` ueberhaupt existiert.
3. **Bei paralleler Subagenten-/Wellen-Arbeit setzt jeder Strang seinen Status
   selbst** — ohne dass „auf done setzen" zwingend „Verify-Report schreiben"
   einschliesst. Der Verify-Schritt ist gedanklich vom Status-Wechsel
   entkoppelt, also faellt er unter Zeitdruck als erstes weg.

Kern: Der Verify-Pass ist als **Empfehlung** verankert, nicht als **Gate**.

## Was soll erreicht werden? (Business-Ziel)

Der agile-sdd-Skill macht den Verify-Pass projekt-uebergreifend zu einer
**erzwungenen Vorbedingung** fuer `done` und macht ungepruefte `review`/`done`-
Tickets beim Bootstrap **als sichtbare Liste** sofort kenntlich — sodass kein
Ticket mehr unbemerkt ohne Verify-Report auf `done` landet, auch nicht in
Wellen mit vielen parallelen Subagenten.

## Akzeptanzkriterien (EARS-Format)

- [ ] **EARS-1 (Hartes Status-Gate):** When ein Agent ein Ticket auf `done`
  setzen will, the system shall (in `SKILL.md` B, Status-Flow) verlangen, dass
  `<verify_report_path>/TICKET-NNN-verify-*.md` existiert UND darin alle
  EARS-Saetze `pass` sind (UI-EARS via `po_acceptance: confirmed|not_required`).
  Ist kein Report vorhanden oder ein EARS-Satz nicht `pass`, bleibt das Ticket
  `review` — `done` ist nicht erlaubt. Die Regel ist als ueberpruefbare
  Vorbedingung formuliert („STOPP, wenn Report fehlt"), nicht als Empfehlung.
- [ ] **EARS-2 (Aktiver Bootstrap-Listen-Check):** When der Agent die
  Bootstrap-Sequenz (`SKILL.md` A, Schritt „Verify-Status pruefen") durchlaeuft,
  the system shall **alle** Tickets mit Status `review` ODER `done` auf einen
  vollstaendigen Verify-Report pruefen und jedes Ticket ohne (vollstaendigen)
  Report als **Liste** ausgeben — Format pro Zeile: `TICKET-NNN (<status>) —
  Verify-Report fehlt → /sdd-verify TICKET-NNN faellig`.
- [ ] **EARS-3 (done ohne Report ist Eskalation):** When beim Bootstrap ein
  Ticket mit Status `done` OHNE vollstaendigen Verify-Report gefunden wird, the
  system shall dieses Ticket in der Liste explizit als **Gate-Verletzung**
  markieren (nicht nur „faellig"), weil `done` ohne Report gegen EARS-1
  verstoesst.
- [ ] **EARS-4 (Verify-Pass gehoert zum Status-Wechsel, auch bei Subagenten):**
  When ein Status-Wechsel auf `done` ausgefuehrt wird — auch durch einen
  Subagent in Multi-Subagent-/Wellen-Arbeit — the system shall (in `SKILL.md`
  F.4 + Parallelisierungs-Sektion J) festhalten, dass „auf `done` setzen" den
  Verify-Report-Schritt zwingend einschliesst: wer ein Ticket auf `done` setzt,
  schreibt zwingend den Report bzw. stellt sicher, dass er existiert und alle
  EARS `pass` sind.
- [ ] **EARS-5 (Konfigurierbar pro Projekt, abwaertskompatibel):** When ein
  Projekt `docs/sdd-config.yaml` mit einem Block
  `verify_gate: { require_report_for_done: true, bootstrap_list_unverified: true }`
  traegt, the system shall das harte Gate + die Bootstrap-Liste anwenden;
  fehlt der Block, gilt `require_report_for_done: true` als sicherer Default
  (Gate an), aber kein Bruch bestehender Projekte (additiv, nur Doku-Regel).
- [ ] **EARS-6 (Sammel-Modus fuer Nachhol-Wellen):** When ein Projekt viele
  ungepruefte `review`-Tickets hat, the system shall einen Sammel-Aufruf
  `/sdd-verify --all` (bzw. `/sdd-verify --all-review`) dokumentieren, der pro
  ungeprueftem Ticket nacheinander einen Verifier-Pass faehrt — damit eine
  Nachhol-Welle (wie 2026-06-14) ein definierter Befehl ist, kein Ad-hoc-Lauf.

## Konkreter Patch-Vorschlag (welche SKILL.md-Zeilen)

> [!important] NICHT blind applien — Source-of-Truth = `skills_sources/agile-sdd-skill/`
> Deploy NUR via `setup.ps1`. Zeilennummern Stand v0.5 (2026-06-14) — vor Apply
> gegen die aktuelle Datei verifizieren. Aenderungen additiv/verschaerfend,
> nichts Bestehendes loeschen.

1. **`SKILL.md` A) Bootstrap, Schritt 8 „Verify-Status pruefen" (~Z. 64–68):**
   Von passiv auf **aktiv-listend** umschreiben. Neuer Wortlaut-Kern:
   > „Pruefe **alle** Tickets mit Status `review` ODER `done`, ob ein
   > vollstaendiger Verify-Report (`<verify_report_path>/TICKET-NNN-verify-*.md`,
   > alle EARS `pass`) existiert. Gib jedes Ticket ohne (vollstaendigen) Report
   > als **Liste** aus:
   > `TICKET-NNN (<status>) — Verify-Report fehlt → /sdd-verify TICKET-NNN`.
   > `done`-Tickets ohne Report zusaetzlich als **Gate-Verletzung** markieren
   > (Verstoss gegen das Verify-Gate, Sektion B). Bei vielen ungeprueften
   > `review`-Tickets `/sdd-verify --all` vorschlagen. Kein Auto-Run, aber die
   > Liste ist Pflicht-Output — kein einzelner Hinweissatz."

2. **`SKILL.md` B) Status-Flow, Block `review`→`done` (~Z. 171–181):** Die
   bestehende „Erst wenn ... darf das Ticket auf done"-Passage zu einem
   benannten **Verify-Gate** mit STOPP-Klausel aufwerten. Neuer Zusatz:
   > **„Verify-Gate (hart):** `done` ist nur erlaubt, wenn
   > `<verify_report_path>/TICKET-NNN-verify-*.md` existiert UND alle EARS dort
   > `pass` sind (UI-EARS via `po_acceptance: confirmed|not_required`). Fehlt der
   > Report oder ist ein EARS-Satz nicht `pass`: **STOPP — Ticket bleibt
   > `review`**, kein `done`. Konfigurierbar via `sdd-config.yaml:
   > verify_gate.require_report_for_done` (Default `true`)."

3. **`SKILL.md` F.4 „Verifier-Pass" (Ende der Sektion, ~Z. 398):** Absatz
   **„Status-Wechsel schliesst den Verify-Report ein"** ergaenzen:
   > „Wer ein Ticket auf `done` setzt, schreibt zwingend den Verify-Report (oder
   > stellt sicher, dass er existiert und alle EARS `pass` sind) — auch in
   > Multi-Subagent-/Wellen-Arbeit. Der Verify-Pass ist kein separater,
   > nachgelagerter Schritt, sondern Teil des Status-Wechsels nach `done`. Ein
   > Subagent, der seinen Strang abschliesst, faehrt entweder selbst
   > `/sdd-verify TICKET-NNN` oder laesst das Ticket bewusst auf `review` fuer
   > den Sammel-Pass."

4. **`SKILL.md` J) Parallelisierung (~„Konventionen bei parallelen Branches"):**
   Einen Stichpunkt ergaenzen: „Jeder parallele Strang, der ein Ticket auf `done`
   bringen will, durchlaeuft das Verify-Gate (Sektion B) im eigenen Worktree —
   kein `done`-Merge ohne Verify-Report."

5. **`SKILL.md` „Aktivierung in Projekt-CLAUDE.md" (~Z. 689–700):** SDD-Config-
   Zeile um `verify_gate: { require_report_for_done, bootstrap_list_unverified }`
   ergaenzen; Bootstrap-Beschreibung von „(review-Tickets ohne Report?)" auf
   „(review/done-Tickets ohne Report **listen + Gate**)" schaerfen.

6. **`templates/sdd-config.yaml.example`:** Beispiel-Block ergaenzen:
   ```yaml
   verify_gate:
     require_report_for_done: true   # done nur mit vollstaendigem Verify-Report
     bootstrap_list_unverified: true # Bootstrap listet review/done ohne Report
   ```

7. **`commands/sdd-verify.md`:** Sammel-Modus dokumentieren — wenn `$1` `--all`
   oder `--all-review` ist, iteriert der Command ueber alle `review`-Tickets
   (und optional `done` ohne Report) und faehrt pro Ticket einen Verifier-Pass.
   Anti-Pattern wahren: der Verifier prueft jedes Ticket weiterhin ehrlich und
   setzt NICHT blind `done` — er produziert nur Reports, der Status-Uebergang
   bleibt Implementer-/PO-Entscheidung.

8. **`templates/verify-report.md` (optional):** falls eine `verify_status`-
   Sammelzeile fehlt, einen Frontmatter-/Status-Hinweis ergaenzen, der das
   Gate-Lesen (alle EARS `pass`?) maschinell einfach macht.

## Anti-Pattern wahren (wichtig)

Das Gate erzwingt **die Existenz eines ehrlichen Reports**, NICHT das blinde
Setzen von `done`. Der Verifier bleibt objektiv: er darf UI-EARS hoechstens auf
`partial` setzen, schreibt nur Reports, aendert keinen Code/keine Tests, setzt
keinen Status. Das Gate verhindert nur, dass `done` OHNE Report/ohne `pass`
gesetzt wird — es macht aus `partial`/`fail` niemals automatisch `pass`.

## Verhaeltnis zu SKILL-014 (keine Doppelarbeit)

- **SKILL-014** = *welcher* Verifier fuer *welche Oberflaeche* (surface-Gate:
  web ⇒ UI-Verifier-Pflicht). Es definiert die **Art** der Pruefung pro Surface.
- **SKILL-016** = *dass ueberhaupt ein Report existieren muss*, bevor `done`
  erlaubt ist, plus die **aktive Sichtbarmachung** ungepruefter Tickets beim
  Bootstrap. Es ist die generelle **Existenz-/Vollstaendigkeits-Schranke** ueber
  alle Surfaces.
- Beide greifen sauber ineinander: SKILL-016 verlangt „Report + alle EARS
  `pass`"; bei `surface: web` definiert SKILL-014, dass ein web-EARS nur via
  gruenem UI-Verifier-Pass `pass` werden darf. Reihenfolge egal; SKILL-016 ist
  unabhaengig umsetzbar.

## Code-Referenzen (skills_sources/agile-sdd-skill/)

- `SKILL.md` (A Bootstrap-Schritt 8, B Status-Flow review→done, F.4 Verify-Pass,
  J Parallelisierung, Aktivierungs-Block)
- `commands/sdd-verify.md` (Sammel-Modus `--all`)
- `templates/sdd-config.yaml.example` (`verify_gate`-Block)
- `templates/verify-report.md` (optional: Gate-Lese-Hilfe)
- Verweis: SKILL-014 (surface-Gate) als komplementaere Regel

## Out of Scope

- Maschinelle Erzwingung via Hook/Skript — das hier ist eine Skill-Doku-/
  Verhaltens-Regel, kein Pre-Commit-Hook. (Ein optionaler Hook waere ein
  eigenes Folge-Ticket.)
- Aenderung der Verifier-Pruef-Logik selbst (EARS-Klassifizierung, UI-vs-Backend)
  — bleibt wie in VERIFIER.md.

## Live-Beispiel (Projekt-lokal bereits vorgezogen)

AgentischesArbeiten hat die Gate-Konfig projekt-lokal vorgezogen:
`docs/sdd-config.yaml: verify_gate { require_report_for_done: true,
bootstrap_list_unverified: true }` + CLAUDE.md-Bootstrap-Schritt 10 von
„pruefen" auf „listen + Gate" geschaerft. SKILL-016 hebt das auf die generische
Skill-Ebene fuer ALLE Projekte.

## [J] — was Jakob noch tun muss (Deploy)

1. SKILL-016 reviewen (`/po-challenge` optional) → Patch (Punkte 1–8) umsetzen in
   `Schaltzentrale/skills_sources/agile-sdd-skill/` (SKILL.md, commands/,
   templates/).
2. `Schaltzentrale/setup.ps1` ausfuehren (Deploy nach `~/.claude/skills/`).
   **Hinweis:** Der deployte Skill ist aktuell v0.4, die Source ist bereits v0.5
   (SKILL-012/013/014-Patches liegen in Source, sind aber noch nicht deployed) —
   `setup.ps1` zieht alles in einem Rutsch nach.
3. Entscheiden, ob `require_report_for_done` global Hard-Block oder zunaechst
   Warning ist (Default-Empfehlung: Hard, analog zur Live-Erfahrung 2026-06-14).

## Quelle

Jakob 2026-06-14 (Zitat oben). Komplementaer zu SKILL-014 (surface-Gate) und
SKILL-012 (Visual-Check-Capability).
