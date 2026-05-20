# Skills Index — Claude Code Skills fuer Jakob

Alle Skills in diesem Verzeichnis werden via `setup.ps1` nach `~\.claude\skills\` deployed.

---

## Verfuegbare Skills

### obsidian-skills
**Pfad:** `obsidian-skills/`
**Deployment:** `~\.claude\skills\obsidian-skills\`
**Zweck:** Obsidian Flavored Markdown erstellen und bearbeiten — Wikilinks, Callouts, Frontmatter, Bases, Canvas.
**Aktivierung:** Automatisch bei .md-Dateien im Vault oder wenn User Obsidian-Begriffe erwaehnt.
**Enthaltene Skills:** obsidian-markdown, obsidian-bases, obsidian-cli, json-canvas, defuddle

---

### agile-sdd-skill
**Pfad:** `agile-sdd-skill/`
**Deployment:** `~\.claude\skills\agile-sdd-skill\`
**Zweck:** Agile Spec-Driven Development mit KI-Agenten. Ticket-Workflow, Spec-First-Entwicklung, ADRs, Living Documentation, Governance-Log fuer volle KI-Autonomie.
**Aktivierung:** Wenn Agent eigenstaendig Features implementieren soll. Erfordert Aktivierungs-Block in Projekt-CLAUDE.md.
**Pilot-Projekt:** Immobewertung (CRM-App, Next.js + FastAPI + SQLite)
**Templates:** ticket, adr, project_spec, roadmap, changelog, sprint_summary, runbook

---

## Setup

```powershell
# Alle Skills deployen
cd C:\Users\Jakob\claude_projects\Schaltzentrale
.\setup.ps1
```
