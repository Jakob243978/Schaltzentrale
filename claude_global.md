# Globaler Kontext fuer Claude Code

## Ueber den Nutzer

- Name: Jakob
- Arbeitet mit mehreren Claude-Agenten fuer Automatisierung und Produktivitaet
- Projekte liegen unter dem Schaltzentrale-Eltern-Verzeichnis (z.B. `C:\Users\Jakob\claude_projects\` oder `C:\claude_projekte\`). Die Skripte ermitteln den Pfad via `$PSScriptRoot` automatisch.
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
cd <pfad-zu-Schaltzentrale>; .\pull_all.ps1
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
cd <pfad-zu-Schaltzentrale>; .\commit_all.ps1
```
Skripte ermitteln das Repo-Eltern-Verzeichnis selbst (`$PSScriptRoot`-Parent), funktionieren also rechner-unabhaengig.

**Schritt 3 — Zusammenfassung:** kurz ausgeben, welche Repos gepusht wurden und was sich geaendert hat.

## Obsidian-Vault & Skill-Bootstrap

Das Vault unter `<BaseDir>\vault\` ist die zentrale querybare KI-Wissensbasis (Memory + Researcher + Bases + Synthese-Notes). Alle .md-Dateien dort folgen Obsidian-Konvention (Frontmatter, Wikilinks `[[...]]`, Callouts `> [!type]`, Bases).

**Skill-Bootstrap-Regel (deterministisch, nicht auf Auto-Discovery verlassen):**

Bei JEDEM Task, der eine .md-Datei in `<BaseDir>\vault\` betrifft, ODER wenn der User Memory / Wikilinks / Callouts / Frontmatter / Bases / Obsidian erwähnt:

1. **Lade VORHER explizit** `~\.claude\skills\obsidian-skills\skills\obsidian-markdown\SKILL.md` per Read-Tool.
2. Bei `.base`-Files zusätzlich `~\.claude\skills\obsidian-skills\skills\obsidian-bases\SKILL.md`.
3. Bei `.canvas`-Files zusätzlich `~\.claude\skills\obsidian-skills\skills\json-canvas\SKILL.md`.

Hintergrund: Auto-Discovery hat bei Immobewertung wiederholt nicht zuverlässig getriggert — explizite Bootstrap-Anweisung loest das Problem deterministisch.

**Skill-Quelle (Single Source of Truth):** `<Schaltzentrale>\skills_sources\obsidian-skills\`. Deployment nach `~\.claude\skills\` via `setup.ps1` (robocopy /MIR). Manuelle Skill-Installation im `~\.claude\skills\` NICHT mehr nötig — wenn Skill fehlt: `pull_all.ps1` zeigt Warnung, dann `setup.ps1` ausführen.

**Memory-Standort:**
- **Default (heute):** `~\.claude\projects\c--Users-<USER>-claude-projects\memory\` (Claude-Code-Default-Pfad)
- **Geplant (Stufe 3):** Junction auf `<BaseDir>\vault\Memory\` — dann ist Vault canonical, Git-synct über Vault-Repo
- Pull_all.ps1 zeigt am Ende ob Junction aktiv ist

## Wichtige Pfade

- Globale Claude-Einstellungen: `~\.claude\settings.json` (z.B. `C:\Users\Jakob\.claude\settings.json` oder `C:\Users\LG\.claude\settings.json`)
- Diese Datei (Quelle): `<Schaltzentrale>\claude_global.md`
- Deployed nach: `~\.claude\CLAUDE.md`
- Vault: `<BaseDir>\vault\` (Obsidian-Vault, Git-Repo: `github.com/Jakob243978/vault`)
- Skill-Sources: `<Schaltzentrale>\skills_sources\` → `~\.claude\skills\` via setup.ps1
