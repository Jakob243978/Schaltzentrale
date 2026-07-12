# n8n-human-readable — self-contained SDD+PO-Skill-Projekt (GEPLANT)

Geplanter Skill (noch kein Code). Seit dem Dezentralisierungs-Umbau (2026-07-12)
ein eigenständiges SDD+PO-Projekt: Vision, Tickets, Research, Governance leben
hier. Der Skill-Code wird beim Umsetzen von `docs/tickets/SKILL-010.md` angelegt.

> [!info] Skill-Code = dieser Ordner (Single Source of Truth, sobald gebaut)
> Deployment nach `~/.claude/skills/n8n-human-readable/` via `setup.ps1`.

## Bootstrap-Sequenz
1. `CLAUDE.md` (diese Datei)
2. `docs/PROJECT_VISION.md`
3. `docs/sdd-config.yaml`
4. `docs/adr/`
5. `docs/tickets/` (SKILL-010 = idea)
6. `docs/research/2026-05-29_n8n-readability-analyse.md` (Live-Trigger + Best-Practice)
7. `docs/governance_log.md`

## Skill: Agile SDD
Aktiv. Tickets: `docs/tickets/SKILL-NNN.md` | Verifier: `docs/tickets/verify/`.
Präfix `SKILL-` (global eindeutig). SDD-Config: `docs/sdd-config.yaml`.

## Skill: PO
Aktiv. Vision: `docs/PROJECT_VISION.md`. Config: `docs/po-config.yaml`.
Nächster Schritt: `/po-challenge` auf SKILL-010, offene Klärungen auflösen.

## Kunden-Weiterentwicklung (Upstream-Review-Flow)
Kunden legen eigene SKILL-Tickets in `docs/tickets/` an (`origin: customer/<name>`);
Jakob reviewt + entscheidet über Upstream-Merge. Details: `docs/PROJECT_VISION.md`.
