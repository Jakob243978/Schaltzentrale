# SKILL-107: LP-Layout-Fehler verhindern (Spacing-Pflicht, Spalten-Balance, equal-height Kacheln, mobiler Boden, Testimonial-Slider) + Playwright-Layout-Linter

**Status:** review
**Erstellt:** 2026-07-13
**MoSCoW:** Must
**Geschaetzter Aufwand:** M (SKILL.md-Regeln schaerfen + Template haerten + wiederverwendbarer Playwright-Linter + Doku)
**surface:** web
**related:** SKILL-105, SKILL-106
**vision_principle:** lessons-aus-live-use-zurueckfuehren
**outcome_metric:** die drei realen warteliste-02-Layout-Fehler entstehen aus dem Template nicht mehr ODER werden vom Linter (Exit-Gate) gefangen, bevor eine LP „fertig" gemeldet wird

## Kontext / Root-Cause
Anlass: drei wiederkehrende Layout-Fehler an der Referenz-LP `AgentischesArbeiten/landing/warteliste-02/`,
die visuell als „gequetscht / tote Leere" auffielen. SKILL-106 hatte das Spacing-System (§16i) schon
eingefuehrt, aber (a) die Skala war im Template teils nur BENANNT, nicht konsequent ANGEWENDET, und
(b) zwei Layout-Fehlerklassen (Spalten-Balance, Equal-Height-Karten) waren noch nicht als Regel +
automatischer Check abgesichert.

Die drei Fehler:
1. **Feste px-margins statt Spacing-Skala.** Bloecke mit `margin-top:16px/18px/30px` fest verdrahtet,
   waehrend die Sektion aussen grosszuegig war (`.band` bis 120px) → innen geklebt, aussen leer.
2. **Spalten-Balance.** 2-Spalter (Text | Formular) mit kurzer Spalte oben geklebt (`align-items:start`,
   330px) neben langer Spalte (916px) → grosse tote Leere unten unter der kurzen Spalte.
3. **Equal-Height-Karten mit ungleichem Text.** Gleich hohe Karten, sehr unterschiedliche Textmenge →
   textarme Karte hat unten tote Flaeche („Space ohne Anker").

## Was soll erreicht werden?
Diese Fehlerklasse entsteht kuenftig entweder gar nicht (Template + geschaerfte Regeln) ODER wird
spaetestens von einem automatischen, wiederverwendbaren Playwright-Check gefangen. Arbeit NUR im Skill,
keine Aenderung an der konkreten warteliste-02-LP.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, Skala ist Pflicht in der Ausgabe]:** SKILL.md §16i formuliert explizit, dass die
      `--space-*`-Skala in der AUSGELIEFERTEN LP angewendet sein muss (nicht nur benannt); feste
      px-Abstaende zwischen Inhaltsbloecken sind ein Fehler (Ausnahme: eyebrow → Heading, tokenbasiert).
      Die bewaehrten Werte `--space-sm/-md/-lg/-xl` (clamp) sind in SKILL.md + Template hinterlegt.
- [x] **EARS-2 [Must, Spalten-Balance]:** SKILL.md §16b + §16i.5 verbieten `align-items:start` an der
      kurzen Spalte ungleich langer 2-Spalter (→ `align-items:center`/balanciert). Template: `.form-layout`
      auf `align-items:center`.
- [x] **EARS-3 [Must, Kacheln equal-height]:** SKILL.md §16i.6: Kacheln in einem Grid MUESSEN gleich
      gross sein (`align-items:stretch`); ungleiche Hoehen = Fehler, `align-items:start` verboten; Loesung
      bei ungleichem Inhalt = **Text angleichen**. Template: `.card`/`.step` equal-height (flex-column zur
      sauberen Verteilung, ersetzt nicht das Angleichen).
- [x] **EARS-4 [Must, Template gehaertet]:** `--space-*`-Skala im `:root` real definiert, Block-Abstaende
      auf Skala umgestellt (keine festen px zwischen Bloecken; inline `margin-top:*px` entfernt),
      2-Spalter balanciert (`.form-layout align-items:center`), Kacheln equal-height.
- [x] **EARS-5 [Must, Playwright-Layout-Linter]:** `tests/lp_layout_lint.py` (Python + playwright.sync_api),
      `--url` (file:// oder http), rendert auf ≥ 3 Breiten (1900/1440/390), breitenabhaengige Checks
      overflow/tote-spalte/kacheln-ungleich (FAIL) + karten-leere/mobil-bottom-space/testimonial-slider/
      enge-abstaende (WARN), Schwellen als Konstanten, Exit-Code = Gate (0/1), Findings als Klartext,
      robust (kein Crash bei fehlenden Elementen).
- [x] **EARS-6 [Must, mobiler Sektions-Boden]:** SKILL.md §16i.7 + Linter-Check `mobil-bottom-space`:
      auf ≤ 480px darf das letzte Element einer `.band` nicht (< 24px) an der Sektions-Unterkante kleben.
- [x] **EARS-7 [Must, Testimonial-Slider ab > 3]:** SKILL.md §16j + wiederverwendbare Slider-Komponente
      im Template (S8): CSS scroll-snap + defensives JS (Pfeile/Dots, kein Framework), mobil 1 / Desktop
      2-3 pro View, `data-testimonials`/`data-testimonial`-Marker. Linter-Check `testimonial-slider`
      warnt bei > 3 Testimonials ohne Slider-Markup.
- [x] **EARS-8 [Must, projektneutral + nicht-brechend]:** Kein Projektwert im Template/Skill.
      `python -m pytest tests/ -q` bleibt gruen (429 passed); der Linter ist NICHT als pytest-Blocker
      eingehaengt.

## Loesungs-Skizze
- **SKILL.md** §16i: PFLICHT-Absatz (Skala anwenden, nicht nur benennen) + bewaehrte
  `--space-sm/-md/-lg/-xl`-Werte; Regeln 5) Spalten-Balance, 6) Kacheln equal-height (Text angleichen,
  NICHT `align-items:start`), 7) mobiler Sektions-Boden; Do/Don't erweitert; Linter-Aufruf dokumentiert.
  §16b: 2-Spalten-Balance-Bullet. Neues §16j: Testimonial-Slider (ab > 3).
- **Template** `templates/landingpage/index.template.html`: `--space-sm/-md/-lg/-xl` im `:root`; inline
  `margin-top:*px` entfernt/auf Tokens umgestellt; `.eyebrow + h1/h2/h3` tight tokenbasiert; Block-Margins
  auf Skala; `.form-layout align-items:center`; `.card`/`.step` equal-height (flex-column); neue
  Testimonial-Slider-Komponente (S8: CSS scroll-snap + defensives JS, Marker-Attribute).
- **Linter** `tests/lp_layout_lint.py`: siehe EARS-5/6/7.

## Test-Ergebnis / Beleg
- **Linter gegen Live-LP** `https://warteliste-02.jakobsebov.de/`: Exit 1 (rot). Erster Lauf fing den
  realen `div.form-layout`-Fehler (330px vs 916px, `align-items:start`); nach Jakobs Parallel-Fix zeigt
  der aktuelle Lauf `kacheln-ungleich` an `.cards` (Kacheln 180px vs 206/232px, nicht equal-height):
  genau die neue Regel. Keine False-Positives (Icon+Text-Reihen wie `.consent-row`/`li` per
  Absolut-Diff-Schwelle gefiltert); Mobile 390px gruen.
- **Linter gegen gehaertetes Template** (file://, `--strict`): 0 FAIL, 0 WARN → Exit 0 (gruen), inkl.
  aktivem Testimonial-Slider (kein testimonial-slider-Warn, da Slider-Markup vorhanden).
- **Synthetischer Bad-Case** (ungleiche Kacheln, 4 Testimonials im Grid, mobil klebendes Element):
  triggert `kacheln-ungleich` (FAIL), `testimonial-slider` (WARN) und `mobil-bottom-space` (WARN @390):
  die neuen Checks feuern nachweislich.
- **Regression:** `python -m pytest tests/ -q` → 429 passed, 3 warnings. Linter wird von pytest nicht
  eingesammelt (kein `test_`-Praefix), blockiert die Suite also nicht.

### Verify-Vermerk
Kein `/sdd-verify`-Report noetig fuer den gruenen `done`-Uebergang, solange Jakob zentral reviewt:
Beleg ist der doppelte Linter-Lauf (rot auf Live-Bug, gruen auf gehaertetem Template) + gruene pytest.
Linter-Aufruf (Windows: `python`, nicht `python3`):
```
python tests/lp_layout_lint.py --url https://warteliste-02.jakobsebov.de/   # Live: rot (Bug sichtbar)
python tests/lp_layout_lint.py --url landing/<site>/index.html --strict      # neue LP: sollte gruen sein
```
Der Linter ist bewusst NICHT als Blocker in `docs/sdd-config.yaml` (`test_command`) eingehaengt, weil er
eine gerenderte LP-URL braucht; er ist ein LP-QA-Schritt vor „fertig" (ergaenzt Vision-QA §16g).

## Code-Referenzen
- `SKILL.md` §16b (2-Spalten-Balance-Bullet) + §16i (PFLICHT-Absatz, bewaehrte Tokens, Regeln 5/6, Linter-Doku)
- `templates/landingpage/index.template.html` (`:root`-Tokens, Block-Abstaende, `.form-layout`, `.card`/`.step`)
- `templates/landingpage/README.md` (Spacing/Linter-Hinweis)
- `tests/lp_layout_lint.py` (Playwright-Layout-Linter)
- Anlass/Belegquelle: `AgentischesArbeiten/landing/warteliste-02/` (wird separat von Jakob gefixt)
- Vorgaenger: SKILL-105 (Content-Type), SKILL-106 (Spacing-System §16i)
