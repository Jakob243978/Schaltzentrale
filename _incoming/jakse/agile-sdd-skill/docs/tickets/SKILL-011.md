---
vision_principle: lessons-aus-live-use-zurueckfuehren
outcome_metric: mcp_anleitungen_klar_pro_skill
---

# SKILL-011: MCP-Server-Anbindungs-Anleitung (Cross-Cutting)

> [!note] Cross-Cutting (2026-07-12 migriert)
> War ein Cross-Cutting-Ticket (`skill_dev/docs/tickets/cross-cutting/`). Bei der
> skill_dev-Aufloesung dem **agile-sdd-skill** zugeordnet (MCP-Nutzung ist primaer
> Implementer-/Operator-Methodik). **Tangiert auch** po-skill, operator-templates
> und obsidian-skills (deren SKILL.md je einen "MCP-Dependencies"-Block bekommen sollen).

**Status:** idea
**Erstellt:** 2026-06-01
**MoSCoW:** Could
**Geschaetzter Aufwand:** M

## Trigger-Live-Erfahrung

Jakob 2026-06-01:
> "Sowie auch sauberere Wege und Anleitungen fuer MCP Server. Wobei
> MCP zweitrangig erstmal."

Beobachtung: In den aktuellen Skills (agile-sdd, po, operator-templates,
obsidian-skills) ist nirgends standardisiert dokumentiert, **wie ein
Implementer MCP-Server-Tools nutzen soll** (Composio, native MCP,
Fireflies, Gmail etc.).

Heute: ad-hoc. Mal wird per `mcp__claude_ai_Gmail__create_draft` 
direkt aufgerufen, mal wird ein Worker im Projekt geschrieben, mal 
wird ueber AgentTask gerouted. Pattern ist nicht definiert.

## Was soll erreicht werden? (Business-Ziel)

Eine zentrale MCP-Anleitung als Cross-Cutting-Skill-Patch — wann
nutzt ein Subagent direkt MCP-Tools, wann geht es ueber Operator-
Pattern, wann ueber Worker?

## Akzeptanzkriterien (EARS) — Skizze

### Teil A — MCP-Verwendungs-Matrix

- [ ] When ein Implementer/Operator MCP-Tools nutzen will, the system
      shall eine Matrix bereitstellen:
      | Use-Case | Pattern | Beispiel |
      |---|---|---|
      | Einmalige User-Aktion (Mail/Calendar) | Direkt-MCP-Call | Termindokumentierer mit Fireflies |
      | Wiederholt aus Projekt-Logik | Worker mit MCP-Wrapper | Immobewertung Outbound-Mailer |
      | Skill-getrieben | Operator-Template mit MCP-Hint | (noch nicht gebaut) |

### Teil B — Bootstrap-Hinweis

- [ ] When ein neuer Skill spec'd wird mit MCP-Bezug, the system shall
      in der Bootstrap-Sequenz Pflicht-Lese-Datei
      `~/.claude/skills/cross-cutting/mcp-patterns.md` haben.

### Teil C — Skill-Doku-Erweiterung

- [ ] When ein bestehender Skill (z.B. operator-templates) MCP-Tools
      nutzt, the system shall in seinem `SKILL.md` einen Block
      "MCP-Dependencies" haben mit:
      - Liste der genutzten MCP-Tools
      - Composio vs. Native-MCP-Unterscheidung
      - Fallback-Verhalten wenn MCP offline ist

### Teil D — Tests / Verifikation

- [ ] When ein Verifier-Pass laeuft fuer einen Skill mit MCP-Dependencies,
      the system shall checken ob die MCP-Tools im Test gemockt werden
      koennen (nicht reale API-Calls in Tests).

## Out of Scope (vorerst)

- Auto-Config-Generierung fuer Composio
- MCP-Server-Bau (nur Konsum/Nutzung)
- Bezahl-MCP-Server-Auswahl

## Verknuepfte Tickets

- SKILL-010 API-Schema-Pflicht (analoge Methodik)
- Real-Beispiel: Termindokumentierer (Fireflies+Calendar via Composio)

## Status: idea (zweitrangig — siehe Jakobs Notiz)

Wartet auf Trigger durch konkreten Skill mit MCP-Bezug.

## Ergebnis / Notizen

_(wartet auf Trigger)_
