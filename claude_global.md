# Globaler Kontext fuer Claude Code

## Ueber den Nutzer

- Name: Jakob
- Arbeitet mit mehreren Claude-Agenten fuer Automatisierung und Produktivitaet
- Projekte liegen unter `C:\Users\Jakob\claude_projects\` (Windows)
- Sprache: Deutsch (Antworten immer auf Deutsch)

## Agenten-Uebersicht

| Agent | Pfad | Zweck |
|---|---|---|
| **Termindokumentierer** | `claude_projects/Termindokumentierer` | Fireflies-Transkripte -> Google Calendar Zusammenfassungen + Action Items |
| **Assistenz** | `claude_projects/Assistenz` | (in Entwicklung) |
| **Workflow Builder** | `claude_projects/Workflow Builder` | (in Entwicklung) |
| **Schaltzentrale** | `claude_projects/Schaltzentrale` | Meta-Projekt: Uebersicht, Setup, Dokumentation aller Agenten |

## MCP-Verbindungen (via Composio)

Folgende MCP-Verbindungen sind eingerichtet und aktiv:
- **Google Calendar** (Composio) — jakobsebov@gmx.de (primaer), hello@jakobsebov.de, sofia.lieblingsshooting@gmail.com
- **Fireflies** (Composio) — Meeting-Transkripte und Ask-Fred
- **Gmail** (Composio)
- **Canva** (Composio)

Direkte MCP-Server (nicht Composio):
- **Google Calendar** (claude.ai native)

## Arbeitsweise

- Immer die `CLAUDE.md` des jeweiligen Projekts lesen, bevor Aenderungen gemacht werden
- Secrets niemals committen (.env ist immer in .gitignore)
- Jedes Projekt hat `requirements.txt`, `.env.example` und `CLAUDE.md`
- Antworten kurz und direkt halten

## Wichtige Pfade

- Globale Claude-Einstellungen: `C:\Users\Jakob\.claude\settings.json`
- Diese Datei (Quelle): `C:\Users\Jakob\claude_projects\Schaltzentrale\claude_global.md`
- Deployed nach: `C:\Users\Jakob\.claude\CLAUDE.md`
