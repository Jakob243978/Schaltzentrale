# SKILL-072: creative-studio — Layout-Archetypen + Stil-Parameter (Scroll-Stop statt EIN Template-Skelett)

**Status:** review
**Erstellt:** 2026-07-08
**MoSCoW:** Should
**Geschaetzter Aufwand:** M
**surface:** backend
**Vision-Prinzip:** `lessons-aus-live-use-zurueckfuehren`
**outcome_metric:** scroll_stop_archetypen_waehlbar_ohne_bestandsbruch (stat-hero/theme/chrome live) + stil_gap_1_bis_7_als_parameter_verfuegbar
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/marketing/2026-07-08_creative-studio_stil-gap-analyse.md`
(„Sofia-Stil" catchy vs. creative-studio generisch — 7 Stil-Hebel, gemessen: Sofia konzentriert
Text auf 36 % der Bildhoehe/ein Held, der Skill verteilt ihn auf 80 %). Prototyp-Beleg:
`AgentischesArbeiten/marketing/ad-creatives/_prototype-stat-hero/` (93 %-Stat).

> [!info] Herkunft (Live-Use-Feedback Sofia + Jakob-Auftrag „Skill ausbauen")
> Der Skill produziert eine templatisierte SaaS-Anzeige (ein Layout-Skelett, sichere
> Hierarchie, markenkonform) — Sofias Ads sind Editorial-/Poster-Design (bespoke
> Komposition, Typo-Drama, Motiv IST die Aussage, Farbe als Flaeche). Ziel: die
> **Staerken behalten** (Multi-Format, Safe-Zones, Tokens, Compliance) und die 7 Stil-Hebel
> als **waehlbare Layout-Archetypen + Parameter obendrauf** setzen — nicht das Skelett ersetzen.

## Was soll erreicht werden? (Business-Ziel)
creative-studio kann Scroll-Stop-Creatives rendern (Riesenzahl-Held, Cream-Theme, minimal
Chrome, Foto-Poster) statt nur ein Skelett — bei **unveraendertem Default-Verhalten**. Jeder
Archetyp laeuft durch dieselben `FORMATS`-Safe-Zones + Brand-Tokens.

## Akzeptanzkriterien (EARS-Format)
- [x] **EARS-1:** When kein `--layout` gesetzt ist (Default `template`), the system shall exakt
      das Bestands-Creative rendern (nicht-brechend). *Belegt: `build_html(style=None) == build_html(DEFAULT_STYLE)`; Default-Render visuell identisch; 234 Bestands-Tests gruen.*
- [x] **EARS-2:** When `--layout stat-hero` gewaehlt ist, the system shall EIN Hero-Token
      (`--hero-token`, sonst Headline) als Riesen-Element rendern (Scale-Kontrast).
- [x] **EARS-3:** When `--theme light-cream` gewaehlt ist, the system shall Flaeche/Ink
      ueberschreiben, den **Akzent aber markeneigen** lassen.
- [x] **EARS-4:** When `--chrome minimal` gewaehlt ist, the system shall Brand-Name, Top-Balken
      und CTA-Pill abschalten (CTA → Text-Link) — organischer Look.
- [x] **EARS-5:** When Hero-Scale ausserhalb des Sweetspots (0.25–0.40) bzw. ein foto-getriebenes
      Layout ohne Bild vorliegt, the system shall **warnen (keine Sperre)** — konsistent mit dem
      Warn-statt-Block-Muster.
- [x] **EARS-6 [multi-projekt]:** the system shall Layout-/Theme-Katalog projektneutral in
      `specs.py` (`LAYOUTS`/`THEMES`) halten (kein Brand-/Projektwert).

## Loesungs-Skizze (Approach)
- **`specs.py`:** `Layout`/`Theme`-Dataclasses + Kataloge `LAYOUTS` (template/stat-hero/
  photo-poster/object-hero/split-compare) + `THEMES` (dark/light-cream), `apply_theme()`,
  `layout_warnings()`, `HERO_SCALE_SWEETSPOT/-DEFAULT`. Analog zu `FORMATS`/`CONTENT_TYPES`.
- **`render_image.py`:** `DEFAULT_STYLE` + `_style_ctx()` (loest Weight/Case/Tracking/Chrome auf),
  `style`-kwarg durch `build_html()`/`render()` (Default None → Bestandsverhalten; `batch.py`
  unveraendert). CLI-Args `--layout --hero-token --hero-scale --headline-weight --headline-case
  --tracking --kicker-font --theme --accent-as-block --chrome`. Theme via `apply_theme()` auf die
  Brand-Tokens.
- **Template `ad_image.html.j2`:** alle neuen Variablen mit `| default(...)` (robust ggü.
  Alt-Aufrufern/Tests), Chrome-Elemente in `{% if … | default(true) %}`, Layout-Branch
  (stat-hero/poster/split/default). Stat-Hero: `white-space: nowrap` haelt die Riesenzahl auf
  EINER Zeile (sonst Umbruch → CTA rutscht in die untere Safe-Zone).
- **Verworfen:** eigenes zweites Template pro Archetyp (Duplizierung der Safe-Zone-/Brand-Logik);
  stattdessen EIN Template mit Layout-Branch.

## Test-Ergebnis
- `tests/test_skill_072_layouts.py` — **16 passed** (build_html real via Jinja): Default==DEFAULT_STYLE,
  stat-hero-Hero, theme light-cream (Akzent bleibt), chrome minimal (kein Brand/Bar/Pill → Text-Link),
  layout_warnings, Projektneutralitaet.
- Gesamt-Suite **264 passed** (234 Bestand + 16 SKILL-072 + 14 SKILL-073), keine Regression.
- **Render-Beleg:** Default-Render (feed_4x5) visuell identisch zum Bestand; `--layout stat-hero
  --theme light-cream --chrome minimal --headline-weight black --headline-case upper` (feed_4x5 +
  story_9x16) rendert den Sofia-Stil-Stat-Hero (Riesen-„93 %" einzeilig, Pfeil-Icon, Cream-BG,
  CTA als Text-Link), safe-zone-korrekt.

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/specs.py` — `Layout`/`Theme`, `LAYOUTS`/`THEMES`,
  `apply_theme`, `layout_warnings`, `HERO_SCALE_*` (`# SKILL-072:`).
- `skills_sources/creative-studio/creative_studio/render_image.py` — `DEFAULT_STYLE`, `_style_ctx`,
  `build_html(..., style=)`, `render(..., style=)`, CLI-Args (`# SKILL-072:`).
- `skills_sources/creative-studio/templates/ad_image.html.j2` — Layout-Branch + Chrome-Schalter + Stat-Hero.
- `skills_sources/creative-studio/tests/test_skill_072_layouts.py` — 16 Tests.
- `skills_sources/creative-studio/SKILL.md` — Abschnitt 12.

## Ergebnis / Notizen
**Status review (2026-07-08).** Priorisierung eingehalten: stat-hero + theme light-cream +
chrome minimal voll gebaut; photo-poster/object-hero/split-compare als Layout-Geruest angelegt
(werden von SKILL-073 mit Bildern gefuellt — belegt am photo-poster-Render). `setup.ps1` gelaufen.

**Offen:** Verify-Pass (frische Session) + Outcome-Review.
