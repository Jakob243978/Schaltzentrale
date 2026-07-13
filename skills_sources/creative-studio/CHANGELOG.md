# CHANGELOG — creative-studio

Skill-Aenderungen pro Datum, neueste oben. Pro `done`-Ticket ein Eintrag
(`### Technical` + `### User-Facing`), nicht gesammelt am Ende.

## [2026-07-13]: LP-Layout-Fehler verhindern + Playwright-Layout-Linter (SKILL-107)

### Technical
- SKILL.md §16i geschaerft: `--space-*`-Skala ist PFLICHT in der ausgelieferten LP (nicht nur
  benannt), feste px zwischen Bloecken = Fehler (Ausnahme eyebrow → Heading, tokenbasiert); bewaehrte
  `--space-sm/-md/-lg/-xl`-Werte hinterlegt; neue Regeln 5) Spalten-Balance (`align-items:center` statt
  `start`), 6) Kacheln MUESSEN gleich gross sein (equal-height Pflicht, bei ungleichem Inhalt Text
  angleichen, NICHT `align-items:start`) und 7) mobiler Sektions-Boden; §16b um 2-Spalten-Balance-Bullet,
  neues §16j Testimonial-Slider (ab > 3).
- Template `templates/landingpage/index.template.html` gehaertet: `--space-sm/-md/-lg/-xl` im `:root`,
  inline `margin-top:*px` entfernt/auf Skala umgestellt, `.eyebrow + h1/h2/h3` tight tokenbasiert,
  `.form-layout` auf `align-items:center`, `.card`/`.step` equal-height (flex-column). Neue
  wiederverwendbare **Testimonial-Slider-Komponente** (S8): CSS scroll-snap + defensives JS fuer
  Pfeile/Dots, mobil 1 / Desktop 2-3 pro View, `data-testimonials`/`data-testimonial`-Marker, kein Framework.
- Neuer wiederverwendbarer Playwright-Layout-Linter `tests/lp_layout_lint.py` (`--url` file://|http,
  Breiten 1900/1440/390, breitenabhaengige Checks). Checks: overflow / tote-spalte / kacheln-ungleich
  (FAIL), karten-leere / mobil-bottom-space / testimonial-slider / enge-abstaende (WARN). Schwellen als
  Konstanten, Exit-Code = Gate, robust (kein Crash bei fehlenden Elementen). Live-LP warteliste-02 → rot
  (faengt reale Layout-Fehler), gehaertetes Template → gruen; synthetischer Bad-Case triggert alle neuen
  Checks. `pytest tests/ -q` → 429 passed (Linter kein pytest-Blocker). Ticket SKILL-107 (review).

### User-Facing
- Neue Landingpages aus dem Template haben von Anfang an konsistente Abstaende, balancierte Spalten und
  gleich grosse Kacheln; ab 4 Testimonials steht eine fertige Slider-Komponente bereit. Die
  „gequetscht / tote Leere"-Fehler werden entweder gar nicht mehr gebaut oder vom Layout-Linter vor
  „fertig" gefangen.

## [2026-07-12] — Cold-Audience-Ad-Messaging testbar encodiert (SKILL-089..098)

### Technical
- 6 Cold-Audience-Hook-Formeln (F1-F6) als projektneutrale CopyFrameworks
  (`scene`/`kunden_oton`/`vorher_nachher`/`einwand_oton`/`anti_hype`/`umbruch`) +
  `COLD_AUDIENCE_FORMULAS`; `match_frameworks(traffic="cold")` rankt Szenen-Formeln zuerst.
- 8 Human-Messaging-Regeln abrufbar (`human_messaging_rules()`); neue Warn-Funktionen
  `human_rule_warnings` (Statistik-Opener/Consultant-Abstrakta/Begriff-zuerst),
  `brand_voice_warnings` (Tool-Namen/Preis/FOMO/Wortwahl), `hype_warnings`,
  `visual_cliche_warnings` — in Bild- + Reel-Copy-Flow eingehaengt.
- `CTA_LIBRARY`, `TONE_PROFILES`, `apply_value_translations`; `content.load_messaging_doc` +
  `build_analysis_prompt(messaging_doc=...)`; neue `AdContent`-Felder `category_term`/`forbidden_tools`.
- 7 neue Test-Dateien; `pytest tests/ -q` -> 426 passed, 3 skipped (Bestand 363, +63).
- Tickets SKILL-091..099 angelegt (091-096/098 review, 097/099 spec); SKILL-089/090 -> review.

### User-Facing
- Der Skill textet Ads fuer kalte Zielgruppen automatisch menschlicher/markenkonformer
  (Szene statt Statistik, keine Tool-Namen/Hype, Kundensprache als optionale Datenquelle) —
  alles projektneutral, Projektwerte kommen als Parameter/Datei.

## [2026-07-12] — Dezentralisierung zu self-contained SDD+PO-Projekt

### Technical
- Skill "creative-studio" (markenkonforme Social-Ad-Creatives (Bild + Video) fuer Meta) als eigenstaendiges SDD+PO-Projekt initialisiert:
  docs/PROJECT_VISION.md, docs/sdd-config.yaml, docs/po-config.yaml,
  docs/DEFERRED.md, docs/po-outcomes.md, docs/governance_log.md, docs/adr/,
  CHANGELOG.md, ROADMAP.md, CLAUDE.md.
- 62 bestehende SKILL-Tickets aus `skill_dev/docs/tickets/creative-studio/` per `git mv`
  nach `docs/tickets/` migriert (IDs unveraendert, global eindeutig).

### User-Facing
- Der Skill kann jetzt eigenstaendig an Kunden ausgerollt und von diesen mit
  eigenem SDD/PO weiterentwickelt werden (Upstream-Review-Flow).
