# ROADMAP — Skill-Entwicklung

Geplante SKILL-Tickets, sortiert nach MoSCoW + Vision-Prinzip-Match.
Diese Datei ist **nicht** Ground-Truth — die `docs/tickets/SKILL-NNN.md`
sind es. Hier nur Uebersicht fuer Sprint-Planung + Status-Check.

---

## Must

| Ticket | Titel | Status | Vision-Prinzip |
|---|---|---|---|
| SKILL-001 | PO-Skill bauen (Schaltzentrale) + Init in Immobewertung | review (Implementierung in T080 erfolgt, Verifier-Pass + Outcome offen) | `skill-muss-multi-projekt-tauglich-sein` + `dogfood-zwingt-qualitaet` |
| SKILL-005 | Skill-Versions-Anker (rollbar-zu-v0.4 vor Pre-Condition-Einbau) | spec — Voraussetzung fuer SKILL-004/006 | `dogfood-zwingt-qualitaet` + `skill-schlanker-als-was-er-ersetzt` |
| SKILL-004 | EARS-Pre-Conditions als Pflicht im SDD-Ticket-Template + Verifier-Check | spec — wartet auf SKILL-005 done | `lessons-aus-live-use-zurueckfuehren` + `dogfood-zwingt-qualitaet` |

## Should

| Ticket | Titel | Status | Vision-Prinzip |
|---|---|---|---|
| SKILL-002 | Refactor T078/T079 in PO-Skill (Vision↔Features-Bridge generalisieren) | spec — wartet auf T078+T079 done in Immobewertung | `skill-muss-multi-projekt-tauglich-sein` + `lessons-aus-live-use-zurueckfuehren` |
| SKILL-003 | Anti-Pattern "Iterative Artefakt-Generierung" + Implementer-Hygiene | spec | `lessons-aus-live-use-zurueckfuehren` + `skill-schlanker-als-was-er-ersetzt` |
| SKILL-006 | KNOWN_FAILURES.md als Pflicht-Datei + Bootstrap-Eintrag (Living Runbook) | spec — parallel zu SKILL-004 bearbeitbar (Jakob-Entscheidung 2026-05-26) | `lessons-aus-live-use-zurueckfuehren` + `skill-muss-multi-projekt-tauglich-sein` |

## Could (offene Ideen, noch keine SKILL-Tickets)

- **operator-templates-Skill formal aufsetzen** — heute teils unter
  `~/.claude/skills/operator-templates/` aktiv, aber kein eigenes
  `skills_sources/operator-templates/`-Repo. Nach Bedarf SKILL-Ticket
  anlegen sobald mehrere Templates dort landen.
- **SDD-Skill: Verifier-Subagent-Caching** — wenn Verifier in jeder
  Session frisch SKILLS_VISION + Ticket-Spec liest, kommt redundanter
  Read-Overhead. Nur sinnvoll wenn Subagent-Calls > 5 Min werden.
- **PO-Skill: Outcome-Auto-Tracking** — heute manuell via
  `/po-verify-outcome`. Anti-Pattern: Auto-Tracking kann den User
  abstumpfen lassen. Bleibt bewusst manuell.

## Wont (explizit nicht)

- **Eigener Skill-Marketplace / Public-Sharing** — siehe SKILLS_VISION.md
  "Was NICHT im Scope ist".
- **Auto-Discovery via LLM-Klassifizierung** — Skills bleiben
  deterministisch aktiviert. Siehe globale CLAUDE.md
  "Skill-Bootstrap-Regel".

---

## Naechster Sprint-Vorschlag

1. Jakob: SKILLS_VISION.md review + schaerfen wo noetig.
2. Jakob: setup.ps1 ausfuehren (deployt nach `~/.claude/skills/`)
   — falls noch nicht passiert.
3. SKILL-001 Verifier-Pass ausstehend (falls Status `review`):
   `/sdd-verify SKILL-001`.
4. **NEU 2026-05-26 (Knowledge-Persistence-Recherche + Jakob-Update):**
   - SKILL-005 (Versions-Anker) zuerst — XS, blockt nichts ausser SKILL-004/006.
     `docs/skill-versions.md` ist bereits initial befuellt (v0.4-Anker
     `fe9337a`); offen: Smoke-Test-Erweiterung + optional Git-Tag durch Jakob.
   - **SKILL-004 (Pre-Conditions als Sektion, Warning-only)** — M,
     strukturell wichtige Aenderung. Bumpt agile-sdd v0.4 → v0.5.
     **Kein Strict-Mode geplant** (Jakob-Entscheidung 2026-05-26):
     Pre-Conditions bleiben dauerhaft Warning, kein Hard-Block.
   - **SKILL-006 (KNOWN_FAILURES.md)** — jetzt `spec`, **parallel zu
     SKILL-004 bearbeitbar** (Jakob-Entscheidung 2026-05-26). Wirkt
     unabhaengig, kein Warten auf SKILL-004-Outcome noetig.
5. SKILL-002 abwarten, bis T078/T079 in Immobewertung done sind.
6. SKILL-003 (Implementer-Hygiene) kann sofort angegangen werden —
   Pattern-Datei + Memory-Save sind kleine Stueck-Arbeit.
