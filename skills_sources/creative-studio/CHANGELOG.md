# CHANGELOG — creative-studio

Skill-Aenderungen pro Datum, neueste oben. Pro `done`-Ticket ein Eintrag
(`### Technical` + `### User-Facing`), nicht gesammelt am Ende.

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
