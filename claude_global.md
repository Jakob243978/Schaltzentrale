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
| **SocialMediaBuilder** | `claude_projects/SocialMediaBuilder` | Taegliche Content-Pipeline IG/TikTok aus Markdown + Memory -> Trello |
| **Schaltzentrale** | `claude_projects/Schaltzentrale` | Meta-Projekt: Uebersicht, Setup, Dokumentation aller Agenten |

## MCP-Verbindungen (via Composio)

Folgende MCP-Verbindungen sind eingerichtet und aktiv:
- **Google Calendar** (Composio) — jakobsebov@gmx.de (primaer), hello@jakobsebov.de, sofia.lieblingsshooting@gmail.com
- **Fireflies** (Composio) — Meeting-Transkripte und Ask-Fred
- **Gmail** (Composio)
- **Canva** (Composio)
- **Trello** (Composio) — Content-Karten fuer SocialMediaBuilder (TODO: Verbindung in claude.ai/Composio einrichten)

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
Wenn Jakob **"Session beenden"** sagt, in dieser Reihenfolge:

**Schritt 1 — SocialMediaBuilder Impact-Q&A** (vor dem Commit, damit das Ergebnis mit gepusht wird):

**1a. Vor dem Q&A: Substanz holen.** Schau dir kurz an, was in dieser Session veraendert wurde — Git-Diff, neue/aktualisierte Files. Bei Tech-Sessions: lies CLAUDE.md, SETUP.md, TESTS.md des betroffenen Projekts an. Du sollst **konkret** wissen, was gebaut wurde, bevor du Jakob fragst.

**1b. Das Q&A nicht oberflaechlich abfragen.** Stelle die acht Fragen aus `SocialMediaBuilder/CLAUDE.md` ("End-of-Session Q&A Workflow"), aber wenn eine Antwort oberflaechlich bleibt, hak nach:
- "Was war das eigentliche Aha-Erlebnis?"
- "Welcher Aspekt war neu gegenueber vorher?"
- "Was haettest du frueher anders gemacht?"
- Frag konkret nach Zahlen, Tools, Geraeten, Kosten — nicht im Allgemeinen bleiben.

**1c. Skip-Regel:** Wenn Jakob sagt **"nichts dazu" / "nichts heute" / "skip"** o.Ae., direkt zu Schritt 2 springen — keine Datei anlegen, nicht weiter nachfragen.

**1d. Ablegen** unter `claude_projects/SocialMediaBuilder/sessions/Session_YYYY-MM-DD_Impact.md` (Datum = heute). Die Antworten muessen so detailliert sein, dass der SocialMediaBuilder daraus spaeter substanzielle Content-Karten ziehen kann — nicht nur Stichworte.

**Schritt 2 — Commit & Push:**
```powershell
cd C:\Users\Jakob\claude_projects\Schaltzentrale && .\commit_all.ps1
```

**Schritt 3 — Zusammenfassung:** kurz ausgeben, welche Repos gepusht wurden und was sich geaendert hat.

## Wichtige Pfade

- Globale Claude-Einstellungen: `C:\Users\Jakob\.claude\settings.json`
- Diese Datei (Quelle): `C:\Users\Jakob\claude_projects\Schaltzentrale\claude_global.md`
- Deployed nach: `C:\Users\Jakob\.claude\CLAUDE.md`
