# Governance-Log — Skill "agile-sdd-skill"

Alle autonomen Entscheidungen + Verifier-Pass-Log fuer diesen self-contained Skill.
Neueste Eintraege oben.

## 2026-07-15: SKILL-073 + SKILL-074, Subagent-Default + EARS auf Deutsch

**Ticket:** SKILL-073, SKILL-074
**Entscheidung:** (1) Neuer verbindlicher Implementer-Default: Ticket-Umsetzung
laeuft grundsaetzlich als Subagent im Hintergrund (run_in_background),
Hauptagent koordiniert; Ausnahmen: Hello-/op-/ssh-Gates, Prod-Deploys,
ueberlappende Datei-Sets, XS-Edits, Mensch-Interaktion. Konfliktregel:
Subagents schreiben nicht parallel in geteilte Dateien, Eintraege als
Textblock an den Hauptagenten. (2) EARS-Schema auf Deutsch umgestellt
("WENN <Ausloeser/Bedingung>, SOLL <System> <Verhalten>." + fuenf Varianten);
Verifier akzeptiert englische Bestands-Saetze weiter, kein Massen-Rewrite.
**Begruendung:** (1) Parallelisierung senkt Durchlaufzeit, 4x praktisch erprobt
am 2026-07-15; verworfen: Vordergrund-Default (blockiert den Hauptkontext).
(2) Reale Tickets sind laengst deutsch, Mischmasch shall/SOLL/When/Wenn;
verworfen: Massen-Rewrite alter Tickets (append-only-Historie).
**Betroffene Dateien:** SKILL.md (Sektion B, J, Frontmatter v0.7),
templates/TICKET.md, templates/verify-report.md, verifier/VERIFIER.md,
verifier/verifier-prompt.md, docs/tickets/SKILL-073.md,
docs/tickets/SKILL-074.md, CHANGELOG.md
**ADR:** keins (Workflow-Konvention bzw. Doku-Schema, keine Architektur-Weiche)
**Review:** ausstehend

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

---

## 2026-07-15 — CLAUDE.md als Living-Doc-Pflege-Ziel (SKILL-075)

**Ticket:** SKILL-075 (`done`, origin: jakob).
**Entscheidung:** `CLAUDE.md` explizit als Living-Documentation-Pflege-Ziel in SKILL.md
Sektion E aufgenommen (bisher nur Bootstrap-Lese-Datei; Sektion E kannte sie nicht). Regel:
etabliert ein Ticket eine dauerhafte, sessionuebergreifend geltende Regel (Konvention, Pfad/
Gate, Gotcha-Kurzform, ADR-Pointer), gehoert ein praegnanter Block im selben Ticket in die
CLAUDE.md — Teil der Definition of Done, wie die CHANGELOG-Zeile.
**Begruendung:** Jakob-Beobachtung 2026-07-15 — der Skill fasst die CLAUDE.md oft nicht an
("traut sich nicht"/nicht bewusst) → Kontextverlust zwischen Sessions, User muss sich
wiederholen. Root-Cause: CLAUDE.md fehlte in Sektion E; Parallel-Konfliktregel rahmte sie als
"heikle geteilte Datei".
**Abgrenzung DEF-001 (bleibt geparkt):** kein autonomes Auto-Memory/Black-Box, sondern
deterministisch ticket-gekoppelt. Kein Doppel-Mechanismus.
**Deployment:** `setup.ps1` (robocopy /MIR) nach `~/.claude/skills/`. Doc-Skill
(`manual_verify_required: false`): Abnahme via Review + Dogfood.
