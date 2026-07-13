# SKILL-108: Mobiler Block-Abstand in kollabierten Layouts (Linter-Check) + Sticky-CTA am Anker ausblenden

**Status:** review
**Erstellt:** 2026-07-13
**MoSCoW:** Must
**Geschaetzter Aufwand:** S (neuer Linter-Check + Slider/CTA-Pattern im Template + Doku)
**surface:** web
**related:** SKILL-105, SKILL-106, SKILL-107
**vision_principle:** lessons-aus-live-use-zurueckfuehren
**outcome_metric:** die zwei an warteliste-02 aufgetretenen Mobil-Fehler (gestapelte Bloecke zu eng vor einer Karte; Sticky-CTA bleibt am Anker sichtbar) entstehen aus dem Template nicht mehr ODER werden vom Linter gefangen

## Kontext / Root-Cause
Zwei neue, an `AgentischesArbeiten/landing/warteliste-02/` aufgetretene Mobil-Fehler, die SKILL-107
(Linter/Template) noch nicht abdeckte:

1. **Gestapelte Bloecke auf Mobil zu eng.** In einem Layout, das auf 390px auf **eine Spalte**
   kollabiert (`.form-layout`: grid 1-col), war der vertikale Gap zwischen den gestapelten direkten
   Kindern zu klein (29px), sodass ein kurzer Text-Block am darunter gestapelten **Formular** klebte.
   Der bestehende Check `mobil-bottom-space` fing das NICHT (der prueft nur den Abstand des letzten
   Elements zur Sektions-Unterkante, nicht Block-zu-Block innerhalb gestapelter Layouts). Realer Fix:
   `@media (max-width:959px){ .form-layout{ gap: var(--space-xl); } }` (29px -> 54px).
2. **Sticky-CTA am Anker sichtbar.** Der mobile Sticky-CTA (`.mobile-cta`, `position:fixed`) fuehrt
   per Anchor auf `#warteliste`. Er blieb sichtbar, auch wenn man schon an der Ziel-Sektion war
   (redundant/stoerend). Er soll verschwinden, sobald die Sektion im Viewport ist, und beim
   Hochscrollen zurueckkommen. IntersectionObserver war im Verify unzuverlaessig -> throttled
   Scroll-Handler.

## Akzeptanzkriterien (EARS)
- [x] **EARS-1 [Must, Linter-Check mobil-block-abstand]:** `tests/lp_layout_lint.py` prueft @ ≤ 480px
      fuer auf 1 Spalte kollabierte Layouts (grid 1-col ODER flex-column) den vertikalen Gap zwischen
      gestapelten **substanziellen** Bloecken: Gap < 32px vor einer Karte/Form (oberer Block schlicht) →
      **FAIL**; zwei enge Content-Bloecke < 24px → **WARN**. Robust/defensiv: Form-Feld-Gruppen
      (label/input), Listen (ul/ol/li) und Pills/Chips (inline, schmal) sind ausgenommen (keine
      False-Positives). Schwellen als Konstanten.
- [x] **EARS-2 [Must, Template-Fix Block-Gap]:** Template `.form-layout` bekommt
      `@media (max-width:959px){ gap: var(--space-xl); }` (der reale Fix), damit gestapelte Bloecke mobil
      Luft haben. SKILL.md §16i.8 dokumentiert die Regel + Fix-Muster.
- [x] **EARS-3 [Must, Sticky-CTA-Pattern]:** Wiederverwendbares Pattern im Template: CSS
      `.mobile-cta.is-hidden{ display:none !important; }` + **throttled Scroll-Handler** (rAF, kein
      IntersectionObserver), der `is-hidden` togglet, sobald `#warteliste` im Viewport ist. SKILL.md §16b
      nennt die Regel.
- [x] **EARS-4 [Must, projektneutral + nicht-brechend]:** Kein Projektwert. `python -m pytest tests/ -q`
      bleibt gruen; Linter kein pytest-Blocker.

## Loesungs-Skizze
- **Linter** `tests/lp_layout_lint.py`: neuer Check `mobil-block-abstand` (3d), breitenabhaengig (WIDTH
  in cfg), mit Karten-/Substanz-/Listen-Heuristik; Schwellen `BLOCK_GAP_FAIL_PX=32`, `BLOCK_GAP_WARN_PX=24`,
  `BLOCK_MIN_HEIGHT_PX=48`, `BLOCK_MIN_WIDTH_RATIO=0.55`, `CARD_PAD_MIN_PX=16`.
- **Template** `index.template.html`: `@media (max-width:959px){ .form-layout{ gap: var(--space-xl); } }`;
  `.mobile-cta.is-hidden`-CSS + defensiver, throttled Sticky-CTA-Script-Block.
- **SKILL.md** §16i.8 (Block-Abstand) + §16b (Sticky-CTA am Anker ausblenden); Linter-Check-Liste + Do/Don't.

## Test-Ergebnis / Beleg
- **Linter gegen Live-LP** `https://warteliste-02.jakobsebov.de/` (nach Jakobs Fix): **grün auf allen
  Breiten inkl. 390px** (0 FAIL, 0 WARN). Die zuvor false-positiven `span.cost`-Pills und `ul`-Listen
  werden durch die Substanz-/Listen-Heuristik korrekt ignoriert.
- **Synthetischer Bad-Case** (kollabiertes `.form-layout`, 8px Gap zwischen Text-Block und `.form-card`):
  @390 **FAIL mobil-block-abstand** (8px vor einer Karte/Form). Wie erwartet.
- **Gehaertetes Template** (file://, `--strict`): 0 FAIL, 0 WARN → grün (inkl. Sticky-CTA-Script + form-layout-Fix).
- **Regression:** `python -m pytest tests/ -q` → 429 passed. Linter nicht von pytest eingesammelt.

### Verify-Vermerk
Aufruf (Windows: `python`, nicht `python3`):
```
python tests/lp_layout_lint.py --url https://warteliste-02.jakobsebov.de/    # Live: gruen inkl. @390
python tests/lp_layout_lint.py --url landing/<site>/index.html --strict       # neue LP
```
Kein `/sdd-verify`-Report noetig fuer den `done`-Uebergang bei zentralem Review: Beleg ist Live-LP grün +
Bad-Case FAIL + gruene pytest.

## Code-Referenzen
- `tests/lp_layout_lint.py` (Check `mobil-block-abstand`, Konstanten)
- `templates/landingpage/index.template.html` (`.form-layout` mobile-gap, `.mobile-cta.is-hidden` + Script)
- `SKILL.md` §16i.8 + §16b + Linter-Check-Liste
- Anlass/Belegquelle: `AgentischesArbeiten/landing/warteliste-02/`
- Vorgaenger: SKILL-107 (Layout-Linter + Spacing-Haertung)
