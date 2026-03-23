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

## Session-Workflow

### Session starten
Wenn Jakob "Session starten" sagt oder eine neue Session beginnt:
```powershell
cd C:\Users\Jakob\claude_projects\Schaltzentrale && .\pull_all.ps1
```
Alle Repos werden auf den neuesten Stand gebracht.

### Session beenden
Wenn Jakob **"Session beenden"** sagt:
1. `commit_all.ps1` ausfuehren — committet und pusht alle Repos mit Aenderungen
2. Kurze Zusammenfassung ausgeben: welche Repos wurden gepusht, was hat sich geaendert
```powershell
cd C:\Users\Jakob\claude_projects\Schaltzentrale && .\commit_all.ps1
```

## Wichtige Pfade

- Globale Claude-Einstellungen: `C:\Users\Jakob\.claude\settings.json`
- Diese Datei (Quelle): `C:\Users\Jakob\claude_projects\Schaltzentrale\claude_global.md`
- Deployed nach: `C:\Users\Jakob\.claude\CLAUDE.md`
