# SKILL-041: creative-studio — Carousel-/Multi-Slide-Rendering in render_image.py + batch.py

**Status:** spec
**Erstellt:** 2026-06-24
**MoSCoW:** Should
**Geschaetzter Aufwand:** L
**Vision-Prinzip:** `skill-muss-multi-projekt-tauglich-sein`
**outcome_metric:** null (wird bei in_progress gesetzt)
**outcome_review_at:** null
**Wissensgrundlage:** `AgentischesArbeiten/docs/marketing/research/2026-06-24_social-content-types.md` (§2.2/§2.3 Carousel, §3.3 „Carousel-Slide-Rendering selbst", §5 MoSCoW Should)

> [!info] Herkunft (Recherche 2026-06-24)
> Carousels sind 2026 der **Engagement-Motor** (IG-Carousel 6,90 % ER, +109 % vs. Reels; LinkedIn-Doc-Post
> 21,77 % Median-ER). Der Skill rendert heute aber **1 Vorlage → 1 PNG pro Format** (Single-Image). Ein
> mehrseitiges Slide-Set (Karte 1 = Hook, letzte = CTA) ist ein **eigenes Render-Feature**, nicht nur ein
> Spec-Eintrag (§3.3). Dieses Ticket baut das Multi-Slide-Rendering fuer die `multi_image`-ContentTypes
> (`carousel`, `educational_carousel`, `listicle`).

## Was soll erreicht werden? (Business-Ziel)
Ein Carousel-Job rendert **n PNG-Slides als ein benanntes Set** mit konsistentem Brand-Grid + Safe-Zone je
Karte; pro Set ein Manifest-Eintrag mit Slide-Index. So entstehen Step-/Listicle-/Beweis-Carousels in einem
Lauf, anschlussfaehig an die bestehende Batch-Engine (SKILL-023) und Naming-Systematik (SKILL-024).

## Akzeptanzkriterien (EARS-Format)
- [ ] **EARS-1:** When ein `carousel`/`educational_carousel`/`listicle`-Job mit N Slide-Definitionen
      uebergeben wird, the system shall **N safe-zone-korrekte PNGs** (eines pro Slide) je Format rendern.
      → Test `test_carousel_renders_n_slides`.
- [ ] **EARS-2:** When ein Slide-Set gerendert wird, the system shall den Slide-Index in Dateiname **und**
      Manifest pro Slide ablegen (Karte 1 = Hook-Slide, letzte = CTA-Slide), erweitert das SKILL-024-Naming
      additiv um einen Slide-Index (z.B. `<variant_id>__s00`). → Tests `test_carousel_slide_index_in_filename`,
      `test_carousel_manifest_has_slide_entries`.
- [ ] **EARS-3:** When ein Carousel-Job laeuft, the system shall die `min_slides`/`max_slides`-Warnung aus
      `content_type_warnings()` (SKILL-040) auslosen, wenn die Slide-Anzahl ausserhalb der Range liegt —
      Warnung, kein Abbruch. → Test `test_carousel_warns_slidecount_out_of_range`.
- [ ] **EARS-4:** When ein einzelner Slide-Render fehlschlaegt, the system shall den Lauf **nicht** abbrechen,
      sondern den Fehler je Slide markieren (analog SKILL-023 EARS-5). → Test `test_carousel_slide_error_isolated`.
- [ ] **EARS-5 [multi-projekt]:** When der Skill in verschiedenen Projekten laeuft, the system shall Brand +
      Slide-Inhalte ausschliesslich aus Job/CLI beziehen — kein hartkodierter Projektwert.
      → Test `test_carousel_project_neutral`.

## Loesungs-Skizze (Approach)
- **Gewaehlter Ansatz:** Die bestehende `render()`-Mechanik (HTML/CSS → Playwright → PNG) je Slide
  wiederverwenden; Slide-Schleife in `batch.py` (oder neue `render_carousel()`), die pro Slide ein
  `AdContent` baut und das Naming um einen Slide-Index erweitert. Manifest-Schema additiv um
  `slide_index`/`slide_role` (hook/body/cta) ergaenzen.
- **Verworfene Alternative:** Eigenes Carousel-Template mit allen Slides in einem HTML — verworfen, weil
  Meta n getrennte Bild-Dateien je Karte erwartet und das bestehende Single-Slide-Template wiederverwendbar ist.
- **Betroffene Module:** `render_image.py` (ggf. `render_carousel`-Helper), `batch.py` (Slide-Schleife +
  Manifest), `specs.py` (Slide-Index-Naming, nur additiv), neue Testdatei. → Architektur-Weiche: keine (ADR n/a).

## Technische Hinweise
- Job-Schema additiv erweitern: eine Variante darf statt `headline/...` eine `slides: [...]`-Liste tragen
  (je Slide eigene `headline/subline/cta/eyebrow/bg_image`). `content_type` am Job/Variante kennzeichnet
  `multi_image`.
- Naming bleibt Single Source (SKILL-024): Slide-Index als zusaetzlicher Block, **kein** Parallel-Schema.
- Safe-Zone je Karte aus `FORMATS` (1:1 oben ~10 % / unten ~16 %) — bereits in `specs.py`.
- Voraussetzung: SKILL-039 + SKILL-040 (ContentType + Validator).

## Code-Referenzen
- `skills_sources/creative-studio/creative_studio/render_image.py` — Multi-Slide-Render (Block `# SKILL-041`).
- `skills_sources/creative-studio/creative_studio/batch.py` — Slide-Schleife + Manifest-Eintraege pro Slide.
- `skills_sources/creative-studio/creative_studio/specs.py` — Slide-Index-Naming (additiv).
- `skills_sources/creative-studio/tests/test_skill_041_carousel.py` (neu).
- Wissensgrundlage: `2026-06-24_social-content-types.md` (§2.2, §2.3, §3.3, §5 Should).

## Ergebnis / Notizen
_(wird beim Implementieren befuellt)_
