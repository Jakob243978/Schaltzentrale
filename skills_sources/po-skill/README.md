# po-skill

Product-Owner-Counterpart zum `agile-sdd-skill`. Stellt die **Warum**-Frage
(Vision, Outcome) gegen die **Wie**-Frage des SDD-Skills.

## Was er macht

- Vision-Constitution pflegen (`docs/PROJECT_VISION.md`)
- Neue Ideen challengen bevor sie zu Tickets werden (`/po-challenge`,
  3x-Why + 48h-Cooldown)
- Backlog nach RICE priorisieren (`/po-prioritize`)
- Done-Tickets 14 Tage spaeter auf Outcome pruefen (`/po-verify-outcome`)

## Was er NICHT macht

- Selbst Tickets generieren (Anti-Pattern aus BMad-Erfahrung 2026)
- Code aendern
- PR-Gatekeeper sein (Jakob = 1-Personen-Setup)

## Installation

Source liegt in `Schaltzentrale/skills_sources/po-skill/`. Deployment in
`~/.claude/skills/po-skill/` erfolgt via:

```powershell
cd C:\Users\Jakob\claude_projects\Schaltzentrale; .\setup.ps1
```

Setup.ps1 spiegelt `skills_sources/` per `robocopy /MIR` nach
`~/.claude/skills/` — neue Skills werden automatisch mit-deployed.

## Aktivierung in einem neuen Projekt

```
/po-init
```

Im jeweiligen Projekt-Root. Legt `docs/PROJECT_VISION.md`,
`docs/DEFERRED.md`, `docs/po-config.yaml` an + ergaenzt `CLAUDE.md`.

Details siehe `SKILL.md`.
