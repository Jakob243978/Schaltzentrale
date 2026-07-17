# CHANGELOG — agile-sdd-skill

Skill-Aenderungen pro Datum, neueste oben. Pro `done`-Ticket ein Eintrag
(`### Technical` + `### User-Facing`), nicht gesammelt am Ende.

## [2026-07-15] v0.7: Subagent-Default + EARS auf Deutsch + CLAUDE.md-Pflege

### Technical
- [SKILL-075] CLAUDE.md als Living-Documentation-Pflege-Ziel: SKILL.md Sektion E
  neuer erster Unterabschnitt "CLAUDE.md — Pflege-Pflicht" (Was-rein/Was-nicht,
  Wann = Definition of Done, Abgrenzung zu DEF-001); Bootstrap A.1 + Kompakt-
  Referenz als Lese- UND Pflege-Ziel markiert. Schliesst die Luecke, dass eine
  ticket-etablierte Dauer-Regel nirgends verbindlich in die CLAUDE.md wanderte.
- [SKILL-073] SKILL.md Sektion B: neue Untersektion "Implementer-Default:
  Subagent im Hintergrund" (run_in_background als Default, Ausnahmen-Liste,
  Konfliktregel geteilte Dateien); Sektion J um Abgrenzung Worktrees vs.
  Hintergrund-Subagents + Querverweis ergaenzt.
- [SKILL-074] EARS auf Deutsch: SKILL.md (Ticket-Format-Beispiele + neue
  Untersektion "EARS-Schema auf Deutsch" mit den fuenf Varianten +
  Bestandsschutz), templates/TICKET.md, templates/verify-report.md,
  verifier/VERIFIER.md, verifier/verifier-prompt.md (Matching-Hinweis:
  beide Formen akzeptieren, kein Massen-Rewrite alter Tickets).
- [SKILL-074] Spec-Delta: EARS-Definition von englisch ("When ..., the system
  shall ...") auf deutsches Schema ("WENN ..., SOLL <System> <Verhalten>.")
  umgestellt; Bestands-Tickets bleiben unveraendert.

### User-Facing
- Tickets werden jetzt standardmaessig als Hintergrund-Subagent umgesetzt:
  mehrere Tickets laufen parallel, die Durchlaufzeit sinkt, der Hauptagent
  koordiniert und sammelt ein.
- Akzeptanzkriterien liest und schreibt Jakob jetzt in einem konsistenten
  deutschen EARS-Schema statt englisch/deutschem Mischmasch.

## [2026-07-12] — Dezentralisierung zu self-contained SDD+PO-Projekt

### Technical
- Skill "agile-sdd-skill" (Agile Spec-Driven Development mit KI-Agenten) als eigenstaendiges SDD+PO-Projekt initialisiert:
  docs/PROJECT_VISION.md, docs/sdd-config.yaml, docs/po-config.yaml,
  docs/DEFERRED.md, docs/po-outcomes.md, docs/governance_log.md, docs/adr/,
  CHANGELOG.md, ROADMAP.md, CLAUDE.md.
- 14 bestehende SKILL-Tickets aus `skill_dev/docs/tickets/agile-sdd-skill/` per `git mv`
  nach `docs/tickets/` migriert (IDs unveraendert, global eindeutig).

### User-Facing
- Der Skill kann jetzt eigenstaendig an Kunden ausgerollt und von diesen mit
  eigenem SDD/PO weiterentwickelt werden (Upstream-Review-Flow).
