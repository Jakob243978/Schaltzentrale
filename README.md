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

## Struktur

```
Schaltzentrale/
├── README.md           # Diese Datei
├── setup.ps1           # Einrichtungsskript fuer neues Geraet
└── claude_global.md    # Quelle fuer ~/.claude/CLAUDE.md (globaler Claude-Kontext)
```

## CLAUDE.md aktualisieren

Wenn `claude_global.md` geaendert wurde:

```powershell
.\setup.ps1   # deployt die aktuelle Version nach ~/.claude/CLAUDE.md
```
