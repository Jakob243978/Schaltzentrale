# creative-studio — self-contained SDD+PO-Skill-Projekt

Dieser Skill erzeugt markenkonforme Social-Ad-Creatives (Bild + Video) für Meta
aus Content + Brand-Tokens. Seit dem Dezentralisierungs-Umbau (2026-07-12) ist er
ein **eigenständiges SDD+PO-Projekt**: Vision, Tickets, ADRs, Governance und
Roadmap leben hier im Skill, nicht mehr zentral in `skill_dev/`.

> [!info] Skill-Code = dieser Ordner (Single Source of Truth)
> `SKILL.md`, `creative_studio/`, `video/`, `templates/`, `tests/` sind der
> ausführbare Skill. Deployment nach `~/.claude/skills/creative-studio/` via
> `setup.ps1` (robocopy /MIR) der Schaltzentrale. Nach jeder Änderung `setup.ps1`
> laufen lassen, sonst ist die Änderung nur auf der Platte.

---

## Bootstrap-Sequenz (Pflicht beim Start jeder Session an diesem Skill)

1. `CLAUDE.md` (diese Datei) — Kontext + Bootstrap
2. `docs/PROJECT_VISION.md` — Vision-Constitution (PO-Skill), direkt nach CLAUDE.md
3. `docs/sdd-config.yaml` — test_command, verify_report_path
4. `docs/adr/` — Architektur-Entscheidungen (neueste zuerst)
5. `docs/tickets/` — Tickets mit Status `in_progress` + `spec` (max. 10)
6. `ROADMAP.md` → `CHANGELOG.md` (letzte Einträge)
7. `docs/governance_log.md` — letzte autonome Entscheidungen + Verifier-Pass-Log
8. Verify-Status: für jedes `review`-Ticket prüfen, ob ein Verify-Report in
   `docs/tickets/verify/` existiert; sonst `/sdd-verify SKILL-NNN` vorschlagen.
9. Quer-Read: `SKILL.md` + betroffene Module unter `creative_studio/` / `video/`.

## Skill: Agile SDD
Aktiv. Tickets: `docs/tickets/SKILL-NNN.md` | ADRs: `docs/adr/ADR-NNN-titel.md`
Verifier: `docs/tickets/verify/SKILL-NNN-verify-YYYY-MM-DD.md` (Pflicht-Pass vor `done`, Aufruf `/sdd-verify SKILL-NNN`).
Präfix `SKILL-` (nicht `TICKET-`) — Nummern bleiben global eindeutig (historisch aus zentralem skill_dev). Neue Tickets zählen aus der höchsten `SKILL-NNN.md` weiter.
SDD-Config: `docs/sdd-config.yaml` (`manual_verify_required: false` — headless Tooling; Backend-EARS via Verifier-Output).
PO-Hook: Beim Übergang `idea` → `spec` prüfen ob Frontmatter `vision_principle: <principle_id>` gesetzt ist (Warning per Default).

## Skill: PO
Aktiv. Vision-Constitution: `docs/PROJECT_VISION.md` (Pflicht-Lese-Datei in jedem Bootstrap).
Backlog-Hygiene: `docs/DEFERRED.md` (48h-Cooldown) | `docs/po-outcomes.md` (Outcome-Reviews).
Commands: `/po-challenge` (vor jedem neuen Ticket) | `/po-prioritize` (RICE) | `/po-verify-outcome SKILL-NNN` (>= 14 Tage nach done).
Config: `docs/po-config.yaml`. Anti-Pattern: PO-Skill generiert KEINE Tickets — challenged, priorisiert, verifiziert. Vision schärft nur Jakob (Append-only-Log).

---

## Kunden-Weiterentwicklung (Upstream-Review-Flow)

Der Skill ist eigenständig an Kunden ausrollbar. Kunden legen im ausgerollten
Skill **eigene SKILL-Tickets** in `docs/tickets/` an und entwickeln mit eigenem
SDD/PO weiter. Der Original-Maintainer **Jakob** reviewt und entscheidet, ob eine
Kunden-Erweiterung ins Upstream-Original übernommen wird. Konvention:
Kunden-Tickets tragen `origin: customer/<name>` im Frontmatter, damit Review +
Merge nachvollziehbar bleiben. Details: `docs/PROJECT_VISION.md`.
