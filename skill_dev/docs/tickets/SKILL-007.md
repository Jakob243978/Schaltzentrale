# SKILL-007: Reveal-Presentation Skill — Visual-Review-Step nach Build (Chromium-Screenshot-Pass)

**Status:** spec
**Erstellt:** 2026-05-27
**MoSCoW:** Should
**Geschaetzter Aufwand:** M
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren` + `dogfood-zwingt-qualitaet`
**outcome_metric:** anti_pattern_im_skill_patterns_ordner (Ziel: neues Pattern `visual-review.md` + Anti-Pattern "fertig-ohne-Screenshot" dokumentiert) + token_saving_pro_skill_nutzung (weniger User-Feedback-Loops = weniger Re-Read-Tokens auf grosse HTML-Files)
**outcome_review_at:** null (wird beim done-Set gesetzt)
**Trigger-Live-Erfahrung:** BeyerImmo-Onboarding-Praesi 2026-05-27 (`KundenAB/BeyerImmo/onboarding/onboarding_office_team.html`) — ~1 Stunde Jakob-Feedback-Loops, weil 3 visuelle Bugs aus dem HTML-Quellcode allein nicht erkennbar waren
**Skill-Vorversion:** reveal-presentation aktueller Stand (siehe `docs/skill-versions.md` — Versions-Eintrag fuer reveal-presentation noch nicht angelegt, ggf. parallel zu SKILL-005-Logik nachziehen)

> [!warning] Live-Erfahrung 2026-05-27 — warum dieses Ticket
> Bei der Buildphase der BeyerImmo-Onboarding-Praesi (16 Slides,
> reveal.js 4.6.1, Editorial-Mode) hat der Skill-Workflow mehrfach
> "fertig" gemeldet, waehrend Jakob im Browser drei gravierende
> visuelle Probleme sah, die aus dem HTML-Quellcode allein nicht
> erkennbar waren:
>
> 1. **CSS-Grid-Bug auf `.reveal .items > li`** — `display: grid;
>    grid-template-columns: 2.2em 1fr` macht direkte Inline-Children
>    zu separaten Grid-Items. `<li><strong>X</strong> · text</li>`
>    zerlegte jedes Wort auf eine eigene Zeile.
> 2. **Slide-Hoehe-Overflow** — `display:flex; justify-content:center;
>    overflow:hidden` schneidet bei zuviel Inhalt OBEN + UNTEN
>    gleichermassen ab (Headlines halb weg, letzte Bullets verschwunden).
> 3. **Sub-Text-Pattern + max-width-Erhoehung** linderten nur das
>    Symptom — die Wurzel war Punkt 1. Iterationen ueber 1 Stunde
>    Jakob-Feedback waeren mit einem Screenshot-Pass nach Build vermeidbar
>    gewesen.

## Pre-Conditions

1. `skills_sources/reveal-presentation/SKILL.md` existiert und ist
   live deployed unter `~/.claude/skills/reveal-presentation/SKILL.md`
   — verifiziere via `ls ~/.claude/skills/reveal-presentation/SKILL.md`.
2. Chromium oder Google Chrome ist lokal installiert und ueber einen
   bekannten Pfad aufrufbar (Windows: `C:/Program Files/Google/Chrome/Application/chrome.exe`,
   macOS/Linux analog) — verifiziere via Existenz-Check des Binary.
3. Mind. 1 Live-Beispiel-Praesi existiert, deren Bugs sich mit dem
   neuen Visual-Review-Pass haetten frueher fangen lassen
   (`KundenAB/BeyerImmo/onboarding/onboarding_office_team.html` —
   2026-05-27).
4. Implementer-Modell kann Bilder lesen (Read-Tool unterstuetzt PNG
   — gegeben in Claude Code).

## Was soll erreicht werden? (Business-Ziel)

Der `reveal-presentation`-Skill bekommt eine **verbindliche Phase 4
Visual-Review-Pass** nach dem Build (Phase 3). Statt im HTML-
Quellcode "fertig" zu melden, macht der Skill **headless-Chromium-
Screenshots pro Slide**, liest sie mit dem Read-Tool ein und bewertet
visuell. Bei Auffaelligkeiten wird **automatisch in den
Anpassungs-Loop** zurueckgesprungen (CSS/HTML-Fix → Re-Screenshot),
bis max. 3 Auto-Iterationen erreicht sind oder ein strukturelles
Problem (z.B. Slide-Aufteilung noetig) eine User-Entscheidung
verlangt.

Ziel-Effekt:
- **Subjektive Iterations-Zeit** in Live-Use sinkt (Jakob muss nicht
  mehr nach jedem Build manuell screenshooten + Feedback geben fuer
  Symptome, die der Skill selbst sehen koennte).
- **Anti-Pattern "fertig-ohne-Screenshot"** wird verbindlich
  dokumentiert + im Workflow erzwungen.
- Skill bleibt im Sinne von `skill-schlanker-als-was-er-ersetzt`:
  ein zusaetzlicher Pass kostet einmal ~10s pro Slide, spart aber
  mehrere 30-Min-Feedback-Schleifen.

> [!info] Komplementaer zu SKILL-006 (KNOWN_FAILURES.md)
> Die 3 heute aufgetretenen Bugs (CSS-Grid, Slide-Overflow, Sub-Text-
> Pattern) sind **prototypische Failure-Modes** fuer reveal-Builds.
> Sobald SKILL-006 live ist, gehoeren sie als FAILURE-NNN-Eintraege in
> ein optionales `reveal-presentation/KNOWN_FAILURES.md` (skill-lokal)
> oder in die projekt-Ebene des konsumierenden Repos. Dieses Ticket
> liefert **Detection**, SKILL-006 liefert **Symptom→Recovery-Doku**.

## Akzeptanzkriterien (EARS-Format mit Pre-Conditions)

### Teil A — Neue Phase 4 in SKILL.md

**Pre-Conditions Teil A:**
1. `skills_sources/reveal-presentation/SKILL.md` enthaelt heute Phase 1-3 + Checkliste (gegeben)
2. Workflow-Sektion ist identifizierbar (Header `## Workflow`)

- [ ] When dieses Ticket implementiert ist, the system shall in
      `skills_sources/reveal-presentation/SKILL.md` eine neue Sektion
      **`### Phase 4 — Visual-Review-Pass (Chromium-Screenshots)`**
      direkt nach Phase 3 enthalten, mit:
      - Begruendung (kurz: warum HTML-Quellcode-Check nicht reicht)
      - Schritt-fuer-Schritt-Verfahren (Temp-HTML mit Fragments-
        sichtbar, Chromium headless pro Slide, Read-Tool-Inspektion)
      - Check-Liste was visuell zu pruefen ist
      - Anti-Pattern-Block ("Niemals 'fertig' melden ohne
        Screenshot-Pass durchgelaufen")
- [ ] When ein Build-Workflow im SKILL.md beschrieben wird, the system
      shall die Reihenfolge `Phase 1 → 2 → 3 → 4 → (Loop falls noetig)`
      explizit machen — Phase 4 ist nicht optional.

### Teil B — Wrapper-Script `tools/screenshot_slides.sh`

**Pre-Conditions Teil B:**
1. Teil A done (SKILL.md referenziert Script-Pfad)
2. Skill-Source unterstuetzt `tools/`-Unterverzeichnis (heute leer/nicht vorhanden — neu anlegen ok)

- [ ] When dieses Ticket implementiert ist, the system shall ein
      Wrapper-Script
      `skills_sources/reveal-presentation/tools/screenshot_slides.sh`
      bereitstellen, das:
      - 3 Argumente nimmt: `<presi.html>` `<n_slides>` `<output_dir>`
      - Eine Temp-Kopie mit Fragments-Visible-Override erzeugt
        (`sed 's|</style>|.reveal .fragment{opacity:1!important;visibility:visible!important;}\n</style>|'`)
      - Pro Slide einen Chromium-headless-Aufruf macht (1920x1080,
        `--virtual-time-budget=8000`, separates `--user-data-dir` pro
        Slide um Lock-Konflikte zu vermeiden)
      - Den Chromium-Pfad ueber Env-Variable `$CHROME` ueberschreibbar
        haelt (Default: `/c/Program Files/Google/Chrome/Application/chrome.exe`
        auf Windows-Git-Bash; fallback `chromium`/`google-chrome` auf
        Linux/macOS)
      - Bei fehlendem Chromium mit klarem Fehler abbricht, nicht still
        weitermacht
- [ ] When das Script erfolgreich laeuft, the system shall PNG-Dateien
      mit Pattern `slide_NN.png` in `<output_dir>` erzeugen.
- [ ] When Windows-PowerShell statt Git-Bash der Default-Shell ist,
      the system shall **zusaetzlich** ein
      `tools/screenshot_slides.ps1`-Aequivalent enthalten (gleiche
      Semantik, PowerShell-Syntax). Begruendung: globaler CLAUDE.md-
      Kontext gibt PowerShell als Default-Shell.

### Teil C — Visual-Check-Liste als Pattern-Datei

**Pre-Conditions Teil C:**
1. Teil A+B done
2. `skills_sources/reveal-presentation/patterns/` ist anlegbar (heute nicht vorhanden — neu ok)

- [ ] When das Ticket done ist, the system shall die Datei
      `skills_sources/reveal-presentation/patterns/visual-review.md`
      enthalten mit:
      - **Was wird visuell geprueft (Check-Liste):**
        1. Headline vollstaendig sichtbar (nicht oben oder unten
           abgeschnitten)
        2. Items/Bullets brechen sinnvoll (kein Wort-pro-Zeile-
           Layout, kein einzelner Buchstabe hinter `<br>`)
        3. Slide-Hoehe-Overflow (letzte Bullet noch sichtbar? Footer
           noch da?)
        4. Umlaute korrekt gerendert (kein `Ã¼` statt `ü`, kein
           Tofu-Block fuer fehlende Glyphen)
        5. Fragment-Override greift (alle Inhalte sichtbar im
           Screenshot, nicht nur erstes Fragment)
        6. Farben/Akzente erkennbar (kein versehentlich-weiss-auf-
           weiss durch CSS-Konflikt)
      - **3 Live-Beispiele aus BeyerImmo-Onboarding 2026-05-27**
        (CSS-Grid-Bug, Slide-Overflow, Sub-Text-Pattern) — mit
        Symptom-Screenshot-Beschreibung und Recovery-Skizze.
      - **Anti-Pattern-Block:** "Niemals 'fertig' melden ohne
        Screenshot-Pass durchgelaufen. Wenn Screenshot zeigt Problem
        → erst fixen, dann erneut screenshotten. Erst dann an User
        uebergeben."

### Teil D — Auto-Iterations-Logik

**Pre-Conditions Teil D:**
1. Teil A done (Phase 4 in SKILL.md beschrieben)

- [ ] When ein Slide-Screenshot ein visuelles Problem zeigt
      (Headline abgeschnitten, Items unschoen umbrechen, Inhalt
      Overflow), the system shall **direkt in den Anpassungs-Loop**
      gehen (CSS/HTML-Fix → Re-Screenshot fuer betroffene Slide),
      OHNE User-Feedback abzuwarten.
- [ ] When 3 Auto-Iterationen erreicht sind ohne dass das Problem
      geloest ist, the system shall an den User uebergeben mit:
      - Kurzbeschreibung des Problems
      - Pfad zum letzten Screenshot
      - Hypothese ueber strukturelle Ursache (z.B. "Slide hat zuviel
        Inhalt fuer 1080p — Aufteilung in 2 Slides noetig?")
- [ ] When alle Slides clean sind, the system shall den User mit
      kurzer Sammel-Bestaetigung + Output-Pfad der Screenshots
      informieren (z.B. "16/16 Slides visuell ok — Screenshots in
      `/tmp/shots/`. Bereit fuer inhaltlichen Review?").

### Teil E — Checkliste in SKILL.md erweitert

**Pre-Conditions Teil E:**
1. Teil A done (Phase 4 beschrieben)
2. Existierende "Nach dem Bauen — Checkliste"-Sektion in SKILL.md ist auffindbar

- [ ] When die "Nach dem Bauen — Checkliste"-Sektion erweitert wird,
      the system shall folgende Punkte ergaenzen:
      ```
      - [ ] Phase 4 Visual-Review-Pass durchgelaufen — alle Slides per
            Chromium-Screenshot inspiziert, keine offenen visuellen
            Bugs
      - [ ] Screenshots liegen in `<output_dir>/` zur User-Review
      ```

### Teil F — Tests (Smoke)

**Pre-Conditions Teil F:**
1. `skill_dev/tests/test_skill_dev_smoke.py` existiert

- [ ] When der Smoke-Test laeuft, the system shall pruefen:
      - `skills_sources/reveal-presentation/tools/screenshot_slides.sh`
        existiert + ist nicht leer
      - `skills_sources/reveal-presentation/tools/screenshot_slides.ps1`
        existiert + ist nicht leer
      - `skills_sources/reveal-presentation/patterns/visual-review.md`
        existiert + enthaelt Substring "Anti-Pattern"
      - `skills_sources/reveal-presentation/SKILL.md` enthaelt
        Substring "Phase 4" und "Visual-Review-Pass"

## Technische Hinweise

- **Method-Validierung:** Das Verfahren wurde am 2026-05-27 ad-hoc
  auf der BeyerImmo-Praesi angewandt und hat **funktioniert**
  (Screenshots haben die 3 Bugs aufgedeckt, die vorher nur Jakob
  manuell sah). Lift-and-Shift-Kandidat ins Skill, klassisch.
- **Fragments-Override-Trick:** Reveal.js versteckt Fragments per
  Default. Ohne Override sieht der Screenshot nur das erste Fragment.
  Inline-CSS-Injection (`opacity:1!important; visibility:visible!important`)
  in einer Temp-HTML-Kopie umgeht das ohne den Original-File zu
  veraendern.
- **Chromium-User-Data-Lock:** Mehrere parallele Chromium-Instanzen
  auf demselben Profil locken sich gegenseitig. Loesung: pro Slide
  ein eigenes `--user-data-dir=/tmp/chrome_userdata_NN` (separater
  Profil-Slot).
- **Virtual-Time-Budget:** 8000ms reicht fuer reveal.js + Fonts +
  Mermaid-Render. Bei langsamen CDN-Loads ggf. auf 12000ms erhoehen.
- **Token-Kosten der Bild-Inspektion:** PNGs mit Read-Tool kosten
  Tokens (geschaetzt ~1.5k pro 1920x1080-Slide). Bei 16 Slides
  ~24k Tokens zusaetzlich pro Build. Trade-Off: deutlich weniger
  als die User-Feedback-Schleifen + Re-Reads grosser HTML-Files
  vorher (geschaetzt 50-100k pro Iteration).
- **Skill-Schlankheit:** Wenn Phase 4 in der Praxis ueberraschend
  haeufig "alles ok" liefert (>= 95% der Builds clean beim ersten
  Pass), ist die Phase trotzdem wertvoll — sie eliminiert die
  Unsicherheit, nicht nur die Fehler.

## Code-Referenzen

- `skills_sources/reveal-presentation/SKILL.md` (Sektion "Workflow" +
  "Nach dem Bauen — Checkliste" erweitern, Frontmatter ggf.
  Versions-Bump)
- `skills_sources/reveal-presentation/tools/screenshot_slides.sh` (NEU)
- `skills_sources/reveal-presentation/tools/screenshot_slides.ps1` (NEU)
- `skills_sources/reveal-presentation/patterns/visual-review.md` (NEU)
- `skill_dev/tests/test_skill_dev_smoke.py` (4 neue Test-Cases)
- Live-Beispiel-Verweis:
  `KundenAB/BeyerImmo/onboarding/onboarding_office_team.html` (2026-05-27)

## Out of Scope

- **Inhaltliche Review** (Faktentreue, Story-Bogen, Tonalitaet,
  Brand-Voice) — bleibt manuell beim User. Evtl. separates Folge-
  Ticket, wenn ein nuechternes Pattern fuer "halluzinationsfreier
  Praesentations-Inhalt" entstehen sollte. Jakob explizit am
  2026-05-27.
- **Multi-Browser-Rendering** (Firefox + Safari + Chrome
  Screenshot-Vergleich) — Chromium reicht als Baseline, reveal.js
  ist gut Cross-Browser-getestet.
- **Mobile-Viewport-Screenshots** — Praesis werden auf Laptop/Beamer
  gezeigt, nicht auf Mobile. Wenn das mal anders ist: separates
  Ticket.
- **Visual-Diff-Tool gegen Baseline** (z.B. Percy, Chromatic) —
  Overkill fuer 1-Personen-Setup. Auto-Iteration mit Read-Tool
  reicht.
- **Auto-OCR der Slides** zur Inhalts-Verifikation — Nutzen unklar,
  Aufwand hoch. Manuelle Inhalts-Review bleibt User-Job (siehe oben).

## Voraussetzung

- Chromium/Chrome lokal installiert (siehe Pre-Conditions).
- **SKILL-005 (Versions-Anker) nicht zwingend** — der reveal-
  presentation-Skill ist noch nicht in `skill-versions.md` getaggt;
  Rollback waere via Git-Sub-Tree-Checkout moeglich, aber kein
  formales Tag noetig. Optional als Folge-Aufgabe in
  `docs/skill-versions.md` einen Eintrag fuer reveal-presentation
  v0.1 (Pre-Visual-Review) anlegen.
- Live-Beispiel-File bleibt im BeyerImmo-Repo verfuegbar als
  Regressions-Anker.

## Verknuepfte Tickets

- **Trigger:** Live-Erfahrung 2026-05-27 (BeyerImmo-Onboarding-
  Praesi, ~1h Jakob-Feedback-Loops wegen visueller Bugs)
- **Komplementaer:** SKILL-006 (KNOWN_FAILURES.md) — die 3 heute
  identifizierten Failure-Modes (CSS-Grid, Slide-Overflow, Sub-Text)
  sind Erstkandidaten fuer ein `reveal-presentation/KNOWN_FAILURES.md`
  sobald SKILL-006 live ist
- **Verbunden:** SKILL-003 (Implementer-Hygiene) — Anti-Pattern
  "Live-Smoke = 1x am Ende" wird hier konkret operationalisiert
  (Live-Smoke = Screenshot-Pass, nicht "Browser-Open im User-Kopf")
- **Optional Folge:** Inhaltliche Review-Phase (Faktentreue,
  Story-Bogen) — wenn jemals empirisch sinnvoll formalisierbar

## Ergebnis / Notizen

_(wird vom Implementer befuellt)_
