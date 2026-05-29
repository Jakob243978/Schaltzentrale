# skill_dev — Skill-Entwicklungs-Repo (Eat-Your-Own-Dogfood)

Dieses Sub-Verzeichnis von Schaltzentrale ist die **Meta-Ebene** fuer die
Claude-Code-Skills, die in `<Schaltzentrale>/skills_sources/` als Code
liegen. Hier leben Vision, Tickets, ADRs, Roadmap und Outcome-Tracking
fuer die Skill-Entwicklung selbst.

> [!warning] Skill-Code lebt NICHT hier
> Der ausfuehrbare Skill-Code (SKILL.md, commands/, templates/,
> generators/) lebt unter
> `<Schaltzentrale>/skills_sources/<skill-name>/` (Single Source of
> Truth). Von dort wird er per `setup.ps1` (robocopy /MIR) nach
> `~/.claude/skills/` deployed, wo der Claude-Code-Harness ihn liest.
>
> Nach JEDER Aenderung an `skills_sources/<skill>/` einmalig ausfuehren:
> ```powershell
> cd C:\Users\Jakob\claude_projects\Schaltzentrale; .\setup.ps1
> ```
> Sonst sind die Aenderungen nur auf der Festplatte, aber nicht im
> laufenden Skill.

---

## Bootstrap-Sequenz (Pflicht beim Start jeder Skill-Dev-Session)

Reihenfolge der Pflicht-Lese-Dateien, bevor an einem SKILL-Ticket
gearbeitet wird (analog Immobewertung):

1. `CLAUDE.md` (diese Datei) — Repo-Kontext + Bootstrap-Sequenz
2. `docs/SKILLS_VISION.md` — die Vision-Constitution fuer Skills
3. `docs/adr/` — relevante Architektur-Entscheidungen (falls vorhanden)
4. `docs/tickets/README.md` — Sub-Struktur-Konvention (welcher Skill an welchem Pfad)
5. `docs/tickets/<skill>/SKILL-NNN.md` — das aktuelle Ticket (im passenden Skill-Unterverzeichnis;
   Cross-Cutting-Tickets unter `docs/tickets/cross-cutting/`)
6. `docs/governance_log.md` — autonome KI-Entscheidungen + Verifier-Pass-Log
7. `docs/tickets/<skill>/verify/` — Verify-Status fuer den betroffenen Skill
   (gibt es `review`-Tickets ohne Report?)
8. **Quer-Read:** `skills_sources/<betroffener-skill>/SKILL.md` — der Skill-Code,
   den das Ticket aendert. Dieser Pfad liegt im Schwester-Verzeichnis
   `<Schaltzentrale>/skills_sources/`.
9. **Sanity:** existiert das `<betroffene-skill>` im Source-Tree? Ist es
   schon nach `~/.claude/skills/` deployed? `setup.ps1`-Run noetig?

---

## Verzeichnisstruktur

```
skill_dev/
├── CLAUDE.md                       ← diese Datei
├── CHANGELOG.md                    ← Skill-Aenderungen pro Datum, neueste oben
├── ROADMAP.md                      ← geplante Skill-Tickets, MoSCoW-sortiert
├── docs/
│   ├── SKILLS_VISION.md            ← Vision-Constitution (eine fuer alle Skills)
│   ├── DEFERRED.md                 ← geparkte Ideen aus /po-challenge
│   ├── governance_log.md           ← autonome Entscheidungen, Verifier-Pass-Log
│   ├── po-config.yaml              ← PO-Skill-Konfig (cooldown, outcome-review-days)
│   ├── po-outcomes.md              ← Outcome-Reviews >=14 Tage nach done
│   ├── adr/                        ← Architektur-Entscheidungen (Skill-spezifisch)
│   └── tickets/                    ← seit 2026-05-29 pro Skill ein Sub-Verzeichnis
│       ├── README.md               ← Sub-Struktur-Konvention (wohin gehoert ein neues Ticket?)
│       ├── agile-sdd-skill/        ← SKILL-003, -004, -006, -009 + verify/
│       ├── po-skill/               ← SKILL-001, -002 + verify/
│       ├── reveal-presentation/    ← SKILL-007, -008 + verify/
│       ├── cross-cutting/          ← SKILL-005 (Skill-Versions-Anker, agile-sdd + po-skill)
│       ├── obsidian-skills/        ← reserved (kein offenes Ticket)
│       ├── operator-templates/     ← reserved (kein offenes Ticket)
│       └── n8n-human-readable/     ← neuer Skill (Sub-Agent 2 legt hier Ticket ab)
└── tests/
    └── test_skill_dev_smoke.py     ← Smoke-Tests (Existenz/Parsebarkeit der Meta-Files)
```

**KEIN Code in diesem Subtree.** Wenn ein Ticket Skill-Code schreibt,
liegt der Output unter `<Schaltzentrale>/skills_sources/<skill>/`.
Hier nur Meta (Tickets, Vision, Reviews, Tests fuer Meta-Files).

---

## Aktive Skills (Stand 2026-05-25)

| Skill | Code-Pfad (Source) | Deploy-Target | Status |
|---|---|---|---|
| agile-sdd-skill | `skills_sources/agile-sdd-skill/` | `~/.claude/skills/agile-sdd-skill/` | live |
| po-skill | `skills_sources/po-skill/` | `~/.claude/skills/po-skill/` | live (seit T080) |
| obsidian-skills/* | `skills_sources/obsidian-skills/` | `~/.claude/skills/obsidian-skills/` | live |
| operator-templates | (noch im Skill-Source `skills_sources/operator-templates/` falls existent) | `~/.claude/skills/operator-templates/` | partial |

---

## Skill: Agile SDD
Aktiv. Bootstrap-Sequenz: CLAUDE.md (diese Datei) → docs/SKILLS_VISION.md
(Vision-Constitution, PO-Skill) → docs/adr/ → docs/tickets/SKILL-NNN.md →
docs/governance_log.md → Verify-Status (review-Tickets ohne Report?).
Tickets: docs/tickets/SKILL-NNN.md | ADRs: docs/adr/ADR-NNN-titel.md
Verifier: docs/tickets/verify/SKILL-NNN-verify-YYYY-MM-DD.md
Praefix `SKILL-` statt `TICKET-` — markiert Skill-Tickets eindeutig.
PO-Hook: Beim Status-Uebergang `idea` -> `spec` pruefen ob Ticket-Frontmatter
`vision_principle: <principle_id>` enthaelt (Warning per Default, Hard-Block
bei `PO_SKILL_STRICT=1` oder `po-config.yaml: strict_vision_principle: true`).
Beim Status `done` automatisch `outcome_review_at: <heute+14d>` setzen.

## Skill: PO
Aktiv (initialisiert 2026-05-25 manuell im Rahmen von TICKET-083 — `/po-init`
wurde wegen Sonderfall "neues Repo mit Vision-Material aus Briefing" inline
ausgefuehrt). Vision-Constitution: docs/SKILLS_VISION.md (Pflicht-Lese-Datei
in jedem Skill-Implementer-Bootstrap, direkt nach CLAUDE.md).
Backlog-Hygiene: docs/DEFERRED.md (geparkte Ideen mit 48h-Cooldown) |
docs/po-outcomes.md (Outcome-Reviews >= 14 Tage nach done).
Commands: `/po-init` (bereits manuell ausgefuehrt — KEIN Re-Run noetig) |
`/po-challenge` (vor jedem neuen SKILL-Ticket — 3x-Why + Vision-Prinzip-Match
+ 48h-Cooldown) | `/po-prioritize` (RICE-Score auf idea-SKILL-Tickets) |
`/po-verify-outcome SKILL-NNN` (>= 14 Tage nach done, oder `--all-due`).
SDD-Integration: SKILL-Tickets brauchen `vision_principle: <principle_id>` im
Frontmatter bevor Status auf `spec` geht (Warning per Default).
Config: docs/po-config.yaml.
Anti-Pattern: PO-Skill generiert NICHT selbst Tickets — er challenged,
priorisiert, verifiziert. Vision wird ausschliesslich von Jakob geschaerft
(Append-only Log in SKILLS_VISION.md). Kein PR-Gatekeeper, kein
Multi-Stakeholder-Voting.

---

## Wichtige Pfade & Konventionen

- **Ticket-Praefix:** `SKILL-NNN` (nicht `TICKET-NNN`) — markiert Skill-Tickets
  eindeutig von Projekt-Tickets. Beim Erstellen weiterzaehlen aus dem
  bisher hoechsten `SKILL-NNN.md` **ueber alle Skill-Unterverzeichnisse hinweg**
  (globale Nummerierung, nicht pro Skill — sonst Konflikte mit Memory +
  governance_log + Commit-Referenzen). Siehe `docs/tickets/README.md`.
- **Ticket-Ablage:** seit 2026-05-29 pro Skill ein Sub-Verzeichnis unter
  `docs/tickets/<skill-name>/`. Skill-Verzeichnisname = exakt der Name aus
  `skills_sources/`. Cross-Cutting-Tickets (mehrere Skills betroffen) landen
  in `docs/tickets/cross-cutting/`. Konvention + Mapping in
  `docs/tickets/README.md`.
- **Lift-and-Shift-Pattern:** Wenn ein Ticket einen Worker / Generator von
  einem Projekt-Repo ins Skill-Source verschiebt — sofortige Verzeichnis-
  Verschiebung machen, Projekt-Repo bekommt nur einen Plug-in-Hook
  (siehe SKILL-002). Niemals beide Stellen lange parallel laufen lassen.
- **Verifier-Praxis:** Verifier-Subagent laeuft in frischer Session, liest
  nur SKILLS_VISION.md + Ticket-Spec + tatsaechliche Skill-Source-Files —
  greift NICHT auf Implementer-Session-Kontext zurueck (Bias-Vermeidung).
- **Memory-Eintraege:** Skill-bezogene Feedback-Patterns (z.B.
  Implementer-Hygiene, Token-Budget-Regeln) gehoeren in den globalen
  `memory/`-Pfad mit Praefix `feedback_skill_*` — sodass sie ueber alle
  Projekte hinweg gelten.

---

## Wann ist ein Ticket ein SKILL-Ticket vs. Projekt-Ticket?

| Frage | SKILL-Ticket | Projekt-Ticket |
|---|---|---|
| Aendert es ein File in `skills_sources/`? | ja | nein |
| Ist die Loesung **multi-projekt-relevant**? | ja | nein |
| Loest es ein generelles Methodik-/Workflow-Problem? | ja | nein |
| Betrifft es eine konkrete Projekt-Datenbank, API, Workflow? | nein | ja |
| Im Zweifel: | Skill-Repo (kostet wenig, vermeidet spaeteren Lift-and-Shift) | — |

Siehe Memory-Regel `feedback_skill_tickets_verortung.md` (gespeichert
unter `~/.claude/projects/.../memory/`).

---

## Out of Scope dieses Repos

- Kein Git-Remote separat — Sub-Tree in Schaltzentrale-Repo.
- Kein eigenes Deploy-Skript — `setup.ps1` der Schaltzentrale erledigt
  Skill-Deploys ueber `skills_sources/`.
- Keine Tests fuer Skill-Logik (die laufen pro Skill ggf. in einem
  konsumierenden Projekt — z.B. `tests/test_po_skill_smoke.py` in
  Immobewertung pruefen die Init-Output-Files). Hier nur Smoke-Tests
  fuer die Meta-Struktur.
