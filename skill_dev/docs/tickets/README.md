# Skill-Tickets — Substruktur-Konvention

Tickets liegen seit 2026-05-29 nicht mehr flach in `docs/tickets/`, sondern
pro Skill in einem Unterverzeichnis. Damit koennen mehrere Skills parallel
entwickelt werden, ohne dass die Ticket-Liste in einer Sandkorn-Wueste
ertrinkt.

## Verzeichnisstruktur

```
docs/tickets/
├── README.md                  ← diese Datei
├── agile-sdd-skill/           ← Tickets, die agile-sdd-skill aendern
│   ├── SKILL-NNN.md
│   └── verify/
├── po-skill/                  ← Tickets, die po-skill aendern
│   ├── SKILL-NNN.md
│   └── verify/
├── obsidian-skills/           ← reserved, noch keine Tickets
│   └── verify/
├── operator-templates/        ← reserved, noch keine Tickets
│   └── verify/
├── reveal-presentation/       ← Tickets, die reveal-presentation aendern
│   ├── SKILL-NNN.md
│   └── verify/
├── n8n-human-readable/        ← neuer Skill (Sub-Agent 2 legt hier Ticket ab)
│   └── verify/
└── cross-cutting/             ← Tickets, die mehrere Skills betreffen
    ├── SKILL-NNN.md
    └── verify/
```

## Konvention fuer neue Tickets

### Ticket-Nummerierung
**Global weiterzaehlend, NICHT pro Skill von vorn.** Die Nummern
SKILL-001…SKILL-NNN bleiben einzigartig ueber alle Skill-Verzeichnisse
hinweg. Begruendung:

- Memory-Eintraege (`feedback_skill_*`), `governance_log.md`, Commit-
  History und Cross-Referenzen zwischen Tickets nennen `SKILL-NNN` ohne
  Skill-Pfad → Eindeutigkeit muss erhalten bleiben.
- Pro-Skill-Nummerierung wuerde Konflikte (zwei `SKILL-001.md`) und
  Mehrdeutigkeit in Logs verursachen.

**Naechste freie Nummer ermitteln** (PowerShell):
```powershell
Get-ChildItem docs/tickets -Recurse -Filter "SKILL-*.md" |
  ForEach-Object { ($_.BaseName -replace 'SKILL-','') -as [int] } |
  Measure-Object -Maximum |
  Select-Object -ExpandProperty Maximum
```

### Wohin gehoert ein neues Ticket?

| Faellt das Ticket primaer auf | Pfad |
|---|---|
| genau einen Skill | `docs/tickets/<skill-name>/SKILL-NNN.md` |
| zwei oder mehr Skills | `docs/tickets/cross-cutting/SKILL-NNN.md` |
| einen neuen Skill ohne Code-Pfad | erst Verzeichnis anlegen (`mkdir <skill>/verify`), dann Ticket dort |

**Skill-Verzeichnisname = exakt der Verzeichnisname** in
`<Schaltzentrale>/skills_sources/<skill-name>/`. Sonst greppt niemand
mehr durch.

### Verifier-Reports
`<skill>/verify/SKILL-NNN-verify-YYYY-MM-DD.md` — d.h. ein eigenes
verify/ pro Skill, nicht ein zentrales. Vorteil: Verifier-Subagent kann
sich auf das eine Skill-Verzeichnis konzentrieren.

## Mapping nach der Migration 2026-05-29

| Ticket | Pfad | Begruendung |
|---|---|---|
| SKILL-001 (PO-Skill bauen) | `po-skill/` | aendert `skills_sources/po-skill/` |
| SKILL-002 (Vision↔Features-Bridge) | `po-skill/` | aendert po-skill (Generator) |
| SKILL-003 (Implementer-Hygiene) | `agile-sdd-skill/` | aendert agile-sdd (Implementer-Subagent-Briefing) |
| SKILL-004 (EARS-Pre-Conditions) | `agile-sdd-skill/` | aendert SDD-Ticket-Template + Verifier |
| SKILL-005 (Skill-Versions-Anker) | `cross-cutting/` | betrifft agile-sdd + po-skill |
| SKILL-006 (KNOWN_FAILURES.md) | `agile-sdd-skill/` | aendert agile-sdd (Bootstrap + Pflicht-Datei) |
| SKILL-007 (Reveal-Visual-Review) | `reveal-presentation/` | aendert reveal-presentation |
| SKILL-008 (Reveal-Wrapper-Fixes) | `reveal-presentation/` | aendert reveal-presentation/tools/ |
| SKILL-009 (inbox/-Konvention) | `agile-sdd-skill/` | aendert SDD-Workflow |

## Reserved Skill-Verzeichnisse

Diese Skills existieren in `skills_sources/`, haben aber heute kein
offenes Ticket. Verzeichnisse sind angelegt, sodass das erste Ticket
direkt am richtigen Platz landet:

- `obsidian-skills/`
- `operator-templates/`
- `n8n-human-readable/` (Skill noch nicht in `skills_sources/`,
  Verzeichnis fuer Sub-Agent 2 vorbereitet)
