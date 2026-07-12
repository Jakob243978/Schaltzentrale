# SKILL-008: Reveal-Presentation Visual-Review-Wrapper — Windows-Pfad-Bug (sh) + PS-NativeCommandError (ps1)

**Status:** spec
**Erstellt:** 2026-05-28
**MoSCoW:** Must
**Geschaetzter Aufwand:** S
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren` + `dogfood-zwingt-qualitaet`
**outcome_metric:** zero false-positive Phase-4-Failures auf Windows in den naechsten 3 reveal-presentation-Builds (Default-Shell PowerShell, Sekundaer-Shell Git-Bash). Messung: Implementer-Bericht pro Build (Phase 4 lief / Phase 4 musste umgangen werden).
**outcome_review_at:** null (wird beim done-Set gesetzt)
**Trigger-Live-Erfahrung:** 2026-05-28, BeyerImmo-Onboarding-Praesi (`KundenAB/BeyerImmo/onboarding/onboarding_office_team.html`) — Erst-Anwendung von SKILL-007 (16 Slides). Beide Wrapper-Scripts scheiterten Windows-spezifisch (Bug 1: bash-Wrapper produziert 16 Chromium-404-Screenshots; Bug 2: ps1-Wrapper bricht nach Slide 00 mit NativeCommandError ab). Recovery in der Session: bash-Inline-Call mit Temp-HTML auf `C:/tmp/onboarding_visible.html` (Windows-Pfad) statt `mktemp` — Chromium oeffnet sauber, Phase 4 lieferte korrekt 1 Slide-Overflow-Treffer auf Slide 11.
**Skill-Vorversion:** reveal-presentation v0.x nach SKILL-007 (Phase 4 eingefuehrt am 2026-05-28, Wrapper-Scripts neu unter `tools/screenshot_slides.{sh,ps1}`)

> [!warning] Live-Erfahrung 2026-05-28 — warum dieses Ticket
> Phase 4 aus SKILL-007 wurde heute zum ersten Mal echt verwendet. Der
> Mechanismus selbst hat sich bewiesen (er hat den Slide-Hoehe-Overflow
> auf Slide 11 zuverlaessig gefangen, sobald die Screenshots da waren).
> Beide automatisierten Wrapper-Scripts sind aber auf Windows praktisch
> nicht benutzbar:
>
> 1. **bash-Wrapper (`screenshot_slides.sh`)** legt seine Temp-HTML
>    via `mktemp --suffix=.html` unter Git-Bash/MSYS nach `/tmp/xxx.html`
>    ab. Die `case "$TMP_HTML" in /c/*) ... ;; *) URL="file://$TMP_HTML"
>    ;; esac`-Logik faellt fuer `/tmp/...` auf den Default zurueck →
>    URL = `file:///tmp/xxx.html`. Chromium auf Windows kann diesen
>    MSYS-Pfad nicht aufloesen → **alle 16 Screenshots zeigten die
>    Chromium-Fehlermeldung "Zugriff auf die Datei nicht moeglich ·
>    ERR_FILE_NOT_FOUND"**. Recovery: Temp-HTML direkt auf
>    `C:/tmp/onboarding_visible.html` (Windows-Pfad) geschrieben.
> 2. **PowerShell-Wrapper (`screenshot_slides.ps1`)** trifft mit
>    `& $chrome ... 2>$null | Out-Null` den bekannten PS-5.1-
>    NativeCommandError-Quirk: chrome.exe schreibt seine Erfolgs-
>    meldung ("N bytes written to file ...") auf stderr, PS wrapt das
>    als ErrorRecord, setzt `$?=$false`, mit `$ErrorActionPreference =
>    "Stop"` bricht der Loop nach Slide 00 ab — obwohl der Screenshot
>    tatsaechlich geschrieben wurde. Beleg aus heutiger Session:
>    `chrome.exe : 59169 bytes written to file C:\tmp\shots_2026-05-28\slide_00.png`
>    + NativeCommandError + Exit 1. Exakt dieser Quirk ist in der
>    globalen `~/.claude/CLAUDE.md` unter PowerShell-Hinweisen
>    explizit gewarnt ("Avoid `2>&1` on native executables …").
>
> Konsequenz: SKILL-007 Phase 4 funktioniert auf Windows aktuell nur
> via bash-Inline-Workaround. Der Auto-Modus aus dem SKILL.md ist
> Fiktion bis dieses Ticket done ist.

## Pre-Conditions

1. SKILL-007 ist `review` (Wrapper-Scripts + Phase-4-Sektion in
   `skills_sources/reveal-presentation/SKILL.md` existieren) — heute
   gegeben.
2. Chromium oder Google Chrome ist lokal installiert (Windows-Pfad
   `C:/Program Files/Google/Chrome/Application/chrome.exe` — heute
   gegeben, gleiche Annahme wie SKILL-007).
3. Mind. 1 Live-Beispiel-Praesi existiert, an der die Wrapper sich
   smoke-test-en lassen — `KundenAB/BeyerImmo/onboarding/onboarding_office_team.html`
   (16 Slides) ist verfuegbar und reproduziert beide Bugs deterministisch.
4. Beide Default-Shells sind verfuegbar (PowerShell als Default, Git-Bash
   parallel installiert) — heute gegeben.

## Was soll erreicht werden? (Business-Ziel)

Die zwei Visual-Review-Wrapper aus SKILL-007 sollen auf Windows in der
**Default-Shell (PowerShell)** UND in der **Sekundaer-Shell (Git-Bash)**
zuverlaessig durchlaufen — ohne Inline-Workaround durch den Implementer.
Phase 4 aus SKILL-007 soll genau das tun, was sie verspricht: pro Slide
ein PNG, sauberer Loop bis Slide N-1, klare Fehlermeldung wenn Chromium
fehlt oder Pfad nicht aufloesbar ist.

Ziel-Effekt:
- Implementer-Subagenten kommen bei einer neuen reveal-presentation-
  Build-Session nicht in die Falle „Wrapper meldet 16 Erfolge, alle PNGs
  sind 404-Seiten" oder „Loop bricht nach Slide 00 ab".
- SKILL-007 wird auf Windows produktiv. Vorher war es bewiesen-im-
  Prinzip aber praktisch-unbenutzbar (Live-Beleg 2026-05-28).
- Anti-Pattern aus SKILL-003 (Implementer-Hygiene) wird gehaertet:
  Wrapper haben jetzt einen echten Smoke-Test, nicht nur Existenz-
  Check.

> [!info] Komplementaer zu SKILL-007
> Dieses Ticket korrigiert NICHT die Phase-4-Logik selbst — die hat
> funktioniert (sobald die Screenshots da waren, hat das Read-Tool den
> Slide-11-Overflow gefangen). Es korrigiert nur die zwei Wrapper-
> Scripts, die zwischen „Build fertig" und „Screenshots da" sitzen.
> Phase-4-Verfahren bleibt unveraendert.

## Akzeptanzkriterien (EARS-Format mit Pre-Conditions)

### Teil A — Bug 1 Fix: `tools/screenshot_slides.sh` Windows-Pfad

**Pre-Conditions Teil A:**
1. Script existiert heute mit `mktemp --suffix=.html`-Pfadlogik
   (gegeben, siehe `skills_sources/reveal-presentation/tools/screenshot_slides.sh`).
2. Recovery-Beleg vom 2026-05-28: Temp-HTML im selben Output-Ordner
   (Windows-Pfad) macht den Chromium-Call funktionieren.

- [ ] When dieses Ticket implementiert ist, the system shall die
      Temp-HTML NICHT mehr unter `/tmp/...` (MSYS-Pfad) anlegen, sondern
      so, dass Chromium auf Windows den Pfad aufloesen kann.
- [ ] When der Wrapper unter Git-Bash auf Windows laeuft, the system
      shall die Temp-HTML in einem Pfad anlegen, der entweder schon
      Windows-Form hat (z.B. `${OUTPUT_DIR}/_visible.html`) oder via
      `cygpath -w` zuverlaessig konvertierbar ist.
- [ ] When der Wrapper unter Linux/macOS laeuft, the system shall sich
      verhalten wie bisher (keine Regression — `/tmp/xxx.html` mit
      `file://...` ist dort korrekt).
- [ ] When ein Chromium-Aufruf fehlschlaegt (Exit-Code != 0 oder PNG
      < 10 KB), the system shall **abbrechen statt still weiterzumachen**
      — heute laeuft der Loop durch obwohl alle 16 PNGs 404-Seiten sind.
      Stop-on-first-failure ist akzeptabel; ein 404-PNG ist `>0` Bytes
      und kann nur per Mindest-Groesse oder Header-Sniffing erkannt
      werden (Recommendation: `>= 50 KB` als Untergrenze fuer ein
      gerendertes 1920x1080-PNG; eine ERR_FILE_NOT_FOUND-Seite ist
      typisch < 30 KB).

### Teil B — Bug 2 Fix: `tools/screenshot_slides.ps1` NativeCommandError

**Pre-Conditions Teil B:**
1. Script existiert heute mit `& $chrome ... 2>$null | Out-Null` und
   `$ErrorActionPreference = "Stop"` (gegeben).
2. Live-Beleg vom 2026-05-28: Loop bricht nach Slide 00 ab mit
   NativeCommandError, obwohl `slide_00.png` (59 KB) erfolgreich
   geschrieben wurde.

- [ ] When dieses Ticket implementiert ist, the system shall den
      Chromium-Aufruf **nicht mehr ueber `& $chrome ... 2>$null`** machen
      — diese Form triggert in PS 5.1 das NativeCommandError-Wrapping
      bei jeder stderr-Zeile.
- [ ] When der Wrapper unter Windows-PowerShell 5.1 laeuft, the system
      shall den Loop bis Slide N-1 durchlaufen, ohne dass eine stderr-
      Zeile von chrome.exe den Loop abbricht.
- [ ] When ein Chromium-Aufruf wirklich fehlschlaegt (Exit-Code != 0
      oder PNG < 50 KB nach dem Call), the system shall mit klarer
      Meldung abbrechen (analog Teil A — kein stilles Weiterlaufen).
- [ ] When der Wrapper sauber durchlaeuft, the system shall die gleiche
      Sammel-Bestaetigung ausgeben wie heute (`OK $NSlides Screenshots
      in $OutputDir/`).

### Teil C — Smoke-Test in `skill_dev/tests/test_skill_dev_smoke.py`

**Pre-Conditions Teil C:**
1. Smoke-Test-File existiert (gegeben).
2. Eine Mini-Reveal-HTML mit >= 2 Slides ist als Test-Fixture erzeugbar
   (kann in den Test inline geschrieben werden, Reveal-CDN reicht).

- [ ] When der Smoke-Test laeuft und Chromium nicht installiert ist,
      the system shall den Test als `skipped` markieren — nicht als
      `failed` (CI-Tauglichkeit, andere Rechner ohne Chrome).
- [ ] When der Smoke-Test laeuft und Chromium installiert ist, the
      system shall:
      1. Eine Mini-Reveal-HTML mit 2 Slides in `tmp_path` schreiben.
      2. Den passenden Wrapper aufrufen (`screenshot_slides.ps1` auf
         Windows, `screenshot_slides.sh` sonst — oder beide, wenn beide
         Shells verfuegbar sind).
      3. Pruefen, dass beide erwarteten PNGs (`slide_00.png`,
         `slide_01.png`) existieren UND jeweils **>= 50 KB** sind
         (Schutz gegen die 404-PNG-Regression aus Bug 1).
      4. Bei Fehlschlag eine Meldung ausgeben, die klar macht, welcher
         Wrapper / welche Shell fehlgeschlagen ist.

### Teil D — Live-Erfahrung im SKILL.md verewigen

**Pre-Conditions Teil D:**
1. `skills_sources/reveal-presentation/SKILL.md` Phase-4-Sektion ist
   identifizierbar (gegeben aus SKILL-007).
2. Teil A + Teil B done — sonst beschreibt der Block einen Zustand der
   noch nicht hergestellt ist.

- [ ] When dieses Ticket implementiert ist, the system shall in der
      Phase-4-Sektion von `skills_sources/reveal-presentation/SKILL.md`
      einen kurzen **"Live-Erfahrung / KNOWN_FIXES"**-Block enthalten,
      der die beiden Bugs aus 2026-05-28 zusammenfasst (1-2 Saetze pro
      Bug + Verweis auf SKILL-008 als Quelle des Fixes). Begruendung:
      analog zu SKILL-006-Pattern (KNOWN_FAILURES), aber hier als
      KNOWN_FIXES weil das Ticket den Bug behebt — der Block dient als
      Anker fuer den naechsten Implementer, der einen aehnlichen Quirk
      sieht.

## Technische Hinweise

### Bug 1 — Fix-Optionen (sh-Wrapper)

(a) `mktemp` unter `$LOCALAPPDATA/Temp` oder `${TEMP:-/tmp}` setzen + Pfad
    korrekt nach `C:/...` konvertieren via `cygpath -w` falls verfuegbar.
    **Risiko:** Cygpath ist nicht ueberall vorhanden, Fallback-Logik
    blaeht das Script auf.

(b) Explizit `TMP_HTML="${OUTPUT_DIR}/_visible.html"` im selben Output-
    Ordner. **Vorteil:** vermeidet die ganze Pfad-Mapping-Frage — wenn
    der User `OutputDir=C:/tmp/shots` uebergibt, ist die Temp-HTML
    automatisch unter `C:/tmp/shots/_visible.html` und Chromium liest sie
    sauber. **Nachteil:** Temp-File liegt zwischenzeitlich neben den
    Output-PNGs (Cleanup im `trap` muss diesen Pfad treffen, nicht den
    `mktemp`-Pfad).

(c) Auf Windows zwingend `screenshot_slides.ps1` empfehlen und im
    sh-Wrapper frueh `exit` mit Hinweis. **Nachteil:** verschiebt das
    Problem, loest es nicht — und der ps1-Wrapper hat Bug 2.

**Empfehlung: (b)** — robustester Fix mit kleinstem Diff. Cleanup im
`trap` mit angepasstem Pfad ist trivial. Die `case`-URL-Logik kann
gleich bleiben (greift weiter fuer Linux/macOS-`/tmp/`-Pfade).

### Bug 2 — Fix-Optionen (ps1-Wrapper)

(a) `2>$null`-Pipe entfernen, stattdessen Output mit
    `Start-Process -Wait -NoNewWindow -RedirectStandardError $null`
    abfangen. **Nachteil:** Start-Process gibt Exit-Code nur ueber das
    Process-Objekt, Loop-Logik wird etwas haesslicher.

(b) `cmd.exe /c "chrome ... 2>nul"` aufrufen. **Vorteil:** cmd.exe
    schluckt stderr direkt — PowerShell sieht weder die stderr-Zeile
    noch die NativeCommandError-Wrapping-Falle. Umgeht den Quirk
    vollstaendig.

(c) `$ErrorActionPreference="Continue"` lokal in der Loop setzen +
    Exit-Code separat pruefen. **Nachteil:** macht den ganzen Script-
    Block schwacher gegen echte Fehler.

**Empfehlung: (b)** — `cmd.exe /c` Variante. Am robustesten, umgeht die
ganze NativeCommandError-Falle, ist 1-Zeilen-Diff. Exit-Code von
`cmd.exe /c "..."` wird durchgereicht, kann mit `$LASTEXITCODE`
gepruefte werden. Mindest-PNG-Groessen-Check (>= 50 KB) als zusaetzliche
Schutzschicht analog zu Bug 1.

### Allgemein

- **Recovery-Methode aus heutiger Session:** bash-Inline-Call mit
  Temp-HTML direkt auf `C:/tmp/onboarding_visible.html` (Windows-Pfad)
  → Chromium oeffnet sauber → Loop laeuft durch → Read-Tool inspiziert
  Slide 11 → Overflow-Treffer. Das ist exakt der Verfahrens-Pfad, den
  beide Wrapper nach dem Fix gehen sollen.
- **404-PNG-Erkennung:** ERR_FILE_NOT_FOUND-Screenshots sind typisch
  klein (Chromium rendert die Fehlermeldungs-Seite im Viewport). Heute
  waren die 16 fehlgeschlagenen PNGs alle in derselben kleinen
  Groesse — Mindest-50-KB-Schwelle ist eine robuste Heuristik fuer
  ein 1920x1080-PNG mit echtem Slide-Inhalt.
- **Smoke-Test-Tauglichkeit auf CI:** Chromium-Praesenz NICHT als
  hartes Requirement. Pytest-Skip-Marker ist die richtige Wahl —
  Tests laufen lokal bei Jakob durch, im CI auf einem Build-Slave
  ohne Chrome werden sie geskippt. Konsistent mit
  `skill-schlanker-als-was-er-ersetzt`.

## Code-Referenzen

- `skills_sources/reveal-presentation/tools/screenshot_slides.sh` (FIX
  Bug 1 — Empfehlung: Variante b)
- `skills_sources/reveal-presentation/tools/screenshot_slides.ps1` (FIX
  Bug 2 — Empfehlung: Variante b, `cmd.exe /c "... 2>nul"`)
- `skills_sources/reveal-presentation/SKILL.md` (Phase-4-Sektion —
  KNOWN_FIXES-Block ergaenzen)
- `skill_dev/tests/test_skill_dev_smoke.py` (Roundtrip-Test ergaenzen)
- Live-Beleg-Pfad:
  `KundenAB/BeyerImmo/onboarding/onboarding_office_team.html` (2026-05-28)

## Out of Scope

- **Refactor der Phase-4-Logik selbst.** Nur die Wrapper werden
  angefasst. Der Auto-Iterations-Mechanismus (max 3 Loops, Eskalation
  an User) bleibt unveraendert — er hat heute funktioniert, sobald die
  Screenshots da waren.
- **Multi-Shell-Probing** (Auto-Detection welche Shell verfuegbar ist
  und automatische Wahl des Wrappers). Wer den Wrapper aufruft, weiss
  in welcher Shell er ist. Skill bleibt schlank
  (`skill-schlanker-als-was-er-ersetzt`).
- **Visual-Diff-Tools / Baseline-Vergleich** (siehe SKILL-007 Out-of-
  Scope, bleibt gleich).
- **PowerShell-7-Support garantieren.** Fix wird auf PS 5.1 (Windows-
  Default) verifiziert. Wenn er auf PS 7 auch laeuft: bonus. Wenn
  nicht: separates Ticket.
- **Update der SKILL-007-Akzeptanzkriterien.** SKILL-007 bleibt
  `review`-Status — die Phase-4-Mechanik hat sich bewiesen
  (Slide-11-Overflow gefangen). Dieses Ticket korrigiert die zwei
  Liefer-Vehikel, nicht den Mechanismus.

## Voraussetzung

- Chromium/Chrome lokal installiert (siehe Pre-Conditions, identisch
  zu SKILL-007).
- SKILL-007-Wrapper sind heute in `skills_sources/reveal-presentation/tools/`
  vorhanden — direkter Edit-Pfad.
- Live-Beispiel `KundenAB/BeyerImmo/onboarding/onboarding_office_team.html`
  bleibt als Regressions-Anker fuer den manuellen Re-Test nach Fix
  verfuegbar.

## Verknuepfte Tickets

- **Trigger:** SKILL-007 Live-Anwendung 2026-05-28 (BeyerImmo-Onboarding-
  Praesi, beide Wrapper scheiterten Windows-spezifisch).
- **Eltern:** SKILL-007 (Visual-Review-Pass) — bleibt `review`, dieses
  Ticket repariert die zwei Wrapper-Scripts, NICHT die Phase-4-Logik.
- **Verbunden:** SKILL-003 (Implementer-Hygiene) — Smoke-Test-
  Verschaerfung in Teil C ist konkrete Operationalisierung von
  "Live-Smoke != Existenz-Check".
- **Methodisch verwandt:** SKILL-006 (KNOWN_FAILURES.md) — Teil D
  (KNOWN_FIXES-Block im SKILL.md) ist die Schwester-Konvention zu
  KNOWN_FAILURES: wenn ein Bug gefixt ist, bleibt der Hinweis als
  Anker fuer den naechsten Implementer stehen.

## Ergebnis / Notizen

_(wird vom Implementer befuellt)_
