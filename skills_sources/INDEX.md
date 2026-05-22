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
**Version:** 0.3 (2026-05-21)
**Zweck:** Agile Spec-Driven Development mit KI-Agenten. Ticket-Workflow, Spec-First-Entwicklung, ADRs, Living Documentation, Governance-Log fuer volle KI-Autonomie.
**Aktivierung:** Wenn Agent eigenstaendig Features implementieren soll. Erfordert Aktivierungs-Block in Projekt-CLAUDE.md.
**Pilot-Projekt:** Immobewertung (CRM-App, Next.js + FastAPI + SQLite)
**Templates:** ticket, adr, project_spec, roadmap, changelog, sprint_summary, runbook

**Changelog:**
- **0.3 (2026-05-21):** PO-Abnahme differenziert nach UI vs Backend-EARS
  (`manual_verify_required: ui_only` neuer Default). Verifier darf UI-EARS
  nie auf `pass` setzen (max. `partial`), `pass` kommt erst via
  `po_acceptance: confirmed`. Lesson Learned aus TICKET-009 (Immobewertung):
  Verifier hat keine Browser-Capability — Substring-Match deckt Hover-Bugs
  nicht ab. Geaendert: SKILL.md F.4, sdd-config.yaml.example, verify-report.md,
  VERIFIER.md, verifier-prompt.md, commands/sdd-verify.md.
- **0.2:** Manuelle PO-Abnahme fuer ALLE Tickets Pflicht.

---

## Setup

```powershell
# Alle Skills deployen
cd C:\Users\Jakob\claude_projects\Schaltzentrale
.\setup.ps1
```
