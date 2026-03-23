# Schaltzentrale

Meta-Projekt: Uebersicht, Setup und Dokumentation aller Claude-Agenten.

## Agenten

| Agent | Zweck | Repo |
|---|---|---|
| **Termindokumentierer** | Fireflies-Transkripte -> Google Calendar | [Link](https://github.com/Jakob243978/Termindokumentierer) |
| **Assistenz** | (in Entwicklung) | — |
| **Workflow Builder** | (in Entwicklung) | — |

## Setup auf neuem Geraet

```powershell
# 1. Schaltzentrale klonen
git clone https://github.com/Jakob243978/Schaltzentrale.git C:\Users\<name>\claude_projects\Schaltzentrale

# 2. Setup ausfuehren (klont alle Repos, deployt CLAUDE.md, installiert Abhaengigkeiten)
cd C:\Users\<name>\claude_projects\Schaltzentrale
.\setup.ps1

# 3. .env Dateien anlegen (Vorlage: .env.example in jedem Projekt)

# 4. Claude Code neu starten
```

## Session-Workflow (Git Sync)

### Session starten
Beim Start einer neuen Claude-Code-Session alle Repos aktuell halten:

```powershell
cd C:\Users\<name>\claude_projects\Schaltzentrale
.\pull_all.ps1
```

Oder Claude sagt es direkt: Einfach am Anfang der Session **"Session starten"** sagen —
Claude fuehrt dann `pull_all.ps1` aus.

### Session beenden
Am Ende der Session alle Aenderungen committen und nach GitHub pushen:

```powershell
.\commit_all.ps1
# Optional mit eigener Nachricht:
.\commit_all.ps1 -Message "Termindokumentierer: Webhook entfernt"
```

Das Signal an Claude: Einfach **"Session beenden"** sagen —
Claude fuehrt dann `commit_all.ps1` aus und gibt eine Zusammenfassung der gepushten Aenderungen.

### Warum?
- Alle Geraete bleiben automatisch auf dem gleichen Stand (main branch)
- Kein manuelles git-Management noetig
- Claude weiss beim naechsten Start sofort wo wir stehen

## Struktur

```
Schaltzentrale/
├── README.md           # Diese Datei
├── setup.ps1           # Ersteinrichtung auf neuem Geraet
├── pull_all.ps1        # Session-Start: alle Repos pullen
├── commit_all.ps1      # Session-Ende: alle Repos committen & pushen
└── claude_global.md    # Quelle fuer ~/.claude/CLAUDE.md
```

## CLAUDE.md aktualisieren

Wenn `claude_global.md` geaendert wurde:

```powershell
.\setup.ps1   # deployt die aktuelle Version nach ~/.claude/CLAUDE.md
```
