# CHANGELOG — creative-studio

Skill-Aenderungen pro Datum, neueste oben. Pro `done`-Ticket ein Eintrag
(`### Technical` + `### User-Facing`), nicht gesammelt am Ende.

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
