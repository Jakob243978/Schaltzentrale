# SKILL-057: creative-studio — Reel-Theme-/Design-Token-System (`BRAND_HIGHLIGHT` & Co.)

**Status:** review
**Erstellt:** 2026-06-25
**MoSCoW:** Should
**Geschaetzter Aufwand:** S
**surface:** backend
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-25_reel-design-critique-content-types.md` (§1.7 Brand-Konsistenz, §2 Reel-Theme-Soll) + `AgentischesArbeiten/CLAUDE.md` (Konvention „Brand-Tokens", ADR-010)

> [!info] Herkunft (Frame-Critique 2026-06-25)
> Die Critique deckte einen Brand-Token-Bruch auf: das Caption-Highlight-Gelb `#ffd400` ist in
> `Root.tsx` (Z.99) **hartkodiert** und steht NICHT in `branding.env` (dort nur `BRAND_WARN="#ffc857"`,
> `BRAND_ACCENT="#f25d3e"`). Hook-Title-Card und Captions nutzen damit teils unterschiedliche visuelle
> Sprachen ohne gemeinsame Quelle. Die projektweite Konvention (CLAUDE.md/ADR-010) verlangt **EINE**
> Quelle für Marken-Werte — `branding.env`. Dieses Ticket schließt die Lücke für den Reel-Look.

> [!note] Abgrenzung
> SKILL-055 baut die Caption-Lesbarkeit (Pill/Stroke/Highlight) — es **konsumiert** die hier definierten
> Tokens. SKILL-057 liefert die **Token-Quelle** (additiv in `branding.env`, Mapping in den Skill). Kein
> Doppel: SKILL-055 referenziert Brand-Props, SKILL-057 stellt sicher, dass deren Defaults aus EINER
> Quelle kommen (kein `#ffd400`-Streuung mehr).

## Was soll erreicht werden? (Business-Ziel)
Der gesamte Reel-Look (Caption-Highlight, Caption-Hintergrund-Alpha, Caption-Font) zieht aus **einer**
Brand-Quelle statt aus verstreuten Literalen — analog zur projektweiten `branding.env`-Konvention. So ist
der Reel-Look beim finalen Brandbook in **Stunden statt Tagen** über Title-Card + Captions + Lower-Third
hinweg austauschbar. Multi-Projekt bleibt: Defaults im Token, Override per Spec-Brand-Block.

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When der Reel-Look gerendert wird, the system shall die Caption-/Reel-Design-Werte
      (`highlight`, `caption_bg_alpha`, `caption_font`) aus dem **Brand-Block** der Reel-Spec beziehen, mit
      Defaults aus benannten Konstanten — **kein** `#ffd400`-/Stil-Literal mehr in `Root.tsx`/`Captions.tsx`.
      → Test `test_reel_theme_tokens_no_hardcode`.
- [ ] **EARS-2:** When `branding.env` die neuen Variablen (`BRAND_HIGHLIGHT`, `BRAND_CAPTION_FONT`,
      `BRAND_CAPTION_BG_ALPHA`) enthält, the system shall sie als Reel-Brand-Defaults für AgentischesArbeiten
      bereitstellen (additiv, bestehende Variablen unverändert). → Test/Check `test_branding_env_has_reel_tokens`.
- [ ] **EARS-3:** When eine Reel-Spec einen eigenen Brand-Block mitbringt, the system shall dessen Werte
      **vorrangig** vor den Defaults nutzen (Override). → Test `test_reel_theme_spec_override`.
- [ ] **EARS-4 [multi-projekt]:** When der Skill in einem anderen Projekt läuft, the system shall **keine**
      AgentischesArbeiten-spezifischen Hex/Fonts im Skill-Code halten — Defaults sind generische,
      überschreibbare Konstanten; projektspezifische Werte leben in dessen `branding.env`/Spec.
      → Test `test_reel_theme_project_neutral`.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** (1) `terraform/base-dev/build/customization/branding.env` (AgentischesArbeiten)
  additiv um `BRAND_HIGHLIGHT="#ffd400"`, `BRAND_CAPTION_FONT="Montserrat, …"`, `BRAND_CAPTION_BG_ALPHA="0.62"`
  ergänzen (bestehende Werte unangetastet). (2) Im Skill die Reel-Brand-Defaults als **benannte Konstanten**
  zentralisieren (`reel_spec.py`-Brand-Defaults bzw. ein kleines `reel_theme`-Mapping), die `Root.tsx`-
  Default-Props daraus speisen. (3) Spec-Brand-Block (SKILL-045) um `highlight`/`captionFont`/`captionBgAlpha`
  additiv erweitern (Override).
- **Verworfene Alternative:** Tokens nur im Skill-Code halten ohne `branding.env`-Andockung — verworfen,
  weil es die projektweite Single-Source-Konvention (ADR-010) bricht und das Brandbook-Ausrollen wieder
  über verstreute Stellen liefe.
- **Betroffene Module:** `terraform/base-dev/build/customization/branding.env` (additiv, AgentischesArbeiten-
  Repo), `creative_studio/reel_spec.py` (Reel-Brand-Defaults), `video/src/Root.tsx` (Default-Props aus
  Konstanten). → Architektur-Weiche: bestätigt ADR-010 (keine neue ADR).

## Technische Hinweise
- `surface: backend`. Der Skill bleibt **projektneutral** — die `branding.env`-Ergänzung ist die
  AgentischesArbeiten-**Instanz** der Tokens; der Skill liefert nur generische Default-Konstanten.
- Konsumiert von SKILL-055 (Captions) und SKILL-058 (Hook-Title-Card). Reihenfolge: 057 kann parallel
  zu 055 laufen; bis 057 fertig ist, nutzt 055 die benannte Default-Konstante.
- Keine Secrets in `branding.env` (sind nur Brand-Design-Werte).

## Code-Referenzen
- `AgentischesArbeiten/terraform/base-dev/build/customization/branding.env` — additiv `BRAND_HIGHLIGHT` etc.
- `skills_sources/creative-studio/creative_studio/reel_spec.py` — Reel-Brand-Default-Konstanten + Spec-Override.
- `skills_sources/creative-studio/video/src/Root.tsx` — Default-Props aus Konstanten (kein `#ffd400`-Literal).
- `skills_sources/creative-studio/tests/test_skill_057_reel_theme.py` (neu).
- Wissensgrundlage: `2026-06-25_reel-design-critique-content-types.md` (§2), `AgentischesArbeiten/CLAUDE.md` (Brand-Tokens), `ADR-010`.

## Ergebnis / Notizen
**Umgesetzt 2026-06-25** (Brand-Highlight-Kopplung gebaut → `review`).

- `branding.env` (AgentischesArbeiten) additiv um `BRAND_HIGHLIGHT="#f25d3e"` (Brand-Akzent
  statt Gelb — Jakob-Vorgabe), `BRAND_CAPTION_FONT="Montserrat, …"`, `BRAND_CAPTION_BG_ALPHA="0.62"`
  erweitert (bestehende Variablen unangetastet).
- `creative_studio/reel_spec.py`: benannte Reel-Theme-Default-Konstanten (`DEFAULT_ACCENT`,
  `DEFAULT_CAPTION_FONT`, `DEFAULT_CAPTION_BG`, `DEFAULT_CAPTION_BG_ALPHA`). Mapping zieht
  `highlight`/`captionFont`/`captionBg`/`captionBgAlpha` aus dem Spec-Brand-Block (Override),
  Highlight-Default = **Brand-Akzent** (kein festes `#ffd400`).
- `video/src/Root.tsx`: Default-Props aus Konstanten (`CAPTION_HIGHLIGHT_DEFAULT = BRAND_ACCENT_DEFAULT`,
  `CAPTION_FONT_DEFAULT` = Montserrat) — **kein `#ffd400`-Literal mehr** in Root.tsx/Captions.tsx.

**Tests:** `tests/test_skill_057_reel_theme.py` (6 Tests, EARS-1..4 + Override + Accent-Fallback).
EARS-2 prueft die `branding.env`-Andockung (skip wenn Projekt-Repo fehlt → Skill bleibt projektneutral).

**Multi-Projekt gewahrt:** Skill-Code haelt nur generische, ueberschreibbare Defaults; die
`branding.env`-Werte sind die AgentischesArbeiten-Instanz. Spec-Brand-Block ueberschreibt alles.
