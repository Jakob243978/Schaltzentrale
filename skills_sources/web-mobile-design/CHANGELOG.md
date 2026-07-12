# CHANGELOG — web-mobile-design

Skill-Aenderungen pro Datum, neueste oben. Pro `done`-Ticket ein Eintrag
(`### Technical` + `### User-Facing`), nicht gesammelt am Ende.

## [2026-07-12] — Dezentralisierung zu self-contained SDD+PO-Projekt

### Technical
- Skill "web-mobile-design" (Checkliste + Heuristik fuer mobil-taugliches, responsives Web-Design) als eigenstaendiges SDD+PO-Projekt initialisiert:
  docs/PROJECT_VISION.md, docs/sdd-config.yaml, docs/po-config.yaml,
  docs/DEFERRED.md, docs/po-outcomes.md, docs/governance_log.md, docs/adr/,
  CHANGELOG.md, ROADMAP.md, CLAUDE.md.
- 1 bestehende SKILL-Tickets aus `skill_dev/docs/tickets/web-mobile-design/` per `git mv`
  nach `docs/tickets/` migriert (IDs unveraendert, global eindeutig).

### User-Facing
- Der Skill kann jetzt eigenstaendig an Kunden ausgerollt und von diesen mit
  eigenem SDD/PO weiterentwickelt werden (Upstream-Review-Flow).
