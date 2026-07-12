# web-mobile-design — self-contained SDD+PO-Skill-Projekt

Dieser Skill ist eine ladbare Checkliste + Heuristik fuer mobil-taugliches, responsives Web-Design. Seit dem Dezentralisierungs-Umbau (2026-07-12) ist er
ein **eigenständiges SDD+PO-Projekt**: Vision, Tickets, ADRs, Governance und
Roadmap leben hier im Skill, nicht mehr zentral in `skill_dev/`.

> [!info] Skill-Code = dieser Ordner (Single Source of Truth)
> `SKILL.md` (+ zugehörige Assets) ist der ausführbare Skill. Deployment nach
> `~/.claude/skills/web-mobile-design/` via `setup.ps1` (robocopy /MIR) der Schaltzentrale.
> Nach jeder Änderung `setup.ps1` laufen lassen.

---

## Bootstrap-Sequenz (Pflicht beim Start jeder Session an diesem Skill)

1. `CLAUDE.md` (diese Datei) — Kontext + Bootstrap
2. `docs/PROJECT_VISION.md` — Vision-Constitution (PO-Skill), direkt nach CLAUDE.md
3. `docs/sdd-config.yaml` — test_command, verify_report_path
4. `docs/adr/` — Architektur-Entscheidungen (neueste zuerst)
5. `docs/tickets/` — Tickets mit Status `in_progress` + `spec`
6. `ROADMAP.md` → `CHANGELOG.md` (letzte Einträge)
7. `docs/governance_log.md` — letzte autonome Entscheidungen + Verifier-Pass-Log
8. Verify-Status: `review`-Tickets ohne Report in `docs/tickets/verify/`? → `/sdd-verify SKILL-NNN` vorschlagen.
9. Quer-Read: `SKILL.md` — der Skill-Code, den das Ticket ändert.

## Skill: Agile SDD
Aktiv. Tickets: `docs/tickets/SKILL-NNN.md` | ADRs: `docs/adr/ADR-NNN-titel.md`
Verifier: `docs/tickets/verify/SKILL-NNN-verify-YYYY-MM-DD.md` (Pflicht-Pass vor `done`, Aufruf `/sdd-verify SKILL-NNN`).
Präfix `SKILL-` (nicht `TICKET-`) — Nummern bleiben global eindeutig (historisch aus zentralem skill_dev).
SDD-Config: `docs/sdd-config.yaml` (`manual_verify_required: false` — headless Methodik-/Tooling-Skill). Hinweis: Doc-/Checklisten-Skill — Verifikation via Review + Live-Check.
PO-Hook: Beim Übergang `idea` → `spec` prüfen ob Frontmatter `vision_principle: <principle_id>` gesetzt ist (Warning per Default).

## Skill: PO
Aktiv. Vision-Constitution: `docs/PROJECT_VISION.md` (Pflicht-Lese-Datei in jedem Bootstrap).
Backlog-Hygiene: `docs/DEFERRED.md` (48h-Cooldown) | `docs/po-outcomes.md` (Outcome-Reviews).
Commands: `/po-challenge` | `/po-prioritize` | `/po-verify-outcome SKILL-NNN` (>= 14 Tage nach done).
Config: `docs/po-config.yaml`. Anti-Pattern: PO-Skill generiert KEINE Tickets — challenged, priorisiert, verifiziert. Vision schärft nur Jakob (Append-only-Log).

---

## Kunden-Weiterentwicklung (Upstream-Review-Flow)

Der Skill ist eigenständig an Kunden ausrollbar. Kunden legen im ausgerollten
Skill **eigene SKILL-Tickets** in `docs/tickets/` an und entwickeln mit eigenem
SDD/PO weiter. Der Original-Maintainer **Jakob** reviewt und entscheidet, ob eine
Kunden-Erweiterung ins Upstream-Original übernommen wird. Konvention:
Kunden-Tickets tragen `origin: customer/<name>` im Frontmatter. Details:
`docs/PROJECT_VISION.md`.
