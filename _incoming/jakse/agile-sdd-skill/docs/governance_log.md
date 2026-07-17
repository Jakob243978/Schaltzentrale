# Governance-Log — Skill "agile-sdd-skill"

Alle autonomen Entscheidungen + Verifier-Pass-Log fuer diesen self-contained Skill.
Neueste Eintraege oben.

## 2026-07-12 — Dezentralisierung: Skill wird self-contained SDD+PO-Projekt
**Ticket:** kein Ticket (Struktur-Migration, Architektur-Umbau durch Subagent)
**Entscheidung:** Der Skill "agile-sdd-skill" bekommt eine eigene SDD+PO-Initialisierung
(PROJECT_VISION, sdd-config, po-config, tickets/, adr/, governance_log, CHANGELOG,
ROADMAP, CLAUDE.md). Die bisher zentral in `skill_dev/docs/tickets/agile-sdd-skill/` liegenden
SKILL-Tickets wurden per `git mv` hierher (`docs/tickets/`) migriert; Ticket-IDs
(SKILL-NNN, global eindeutig) unveraendert.
**Begruendung:** Jeder Skill soll eigenstaendig an Kunden ausrollbar sein und von
diesen mit eigenem SDD/PO weiterentwickelt werden koennen (Upstream-Review-Flow).
Zentrale Entwicklung in `skill_dev/` skaliert nicht auf Kunden-Rollout.
**Betroffene Dateien:** docs/PROJECT_VISION.md, docs/sdd-config.yaml,
docs/po-config.yaml, docs/DEFERRED.md, docs/po-outcomes.md, docs/governance_log.md,
docs/adr/, docs/tickets/ (migriert), CHANGELOG.md, ROADMAP.md, CLAUDE.md.
**ADR:** keins (reine Struktur-Migration; inhaltliche Skill-ADRs kommen ins docs/adr/)
**Review:** ausstehend (Jakob)
