# Schaltzentrale Setup-Skript
# Richtet die Entwicklungsumgebung auf einem neuen Geraet ein.
# Ausfuehren: .\setup.ps1

$ErrorActionPreference = "Stop"
$BaseDir = Split-Path $PSScriptRoot -Parent
$ClaudeDir = "C:\Users\$env:USERNAME\.claude"

Write-Host "=== Schaltzentrale Setup ===" -ForegroundColor Cyan

# 1. Globale CLAUDE.md deployen
Write-Host "`n[1/3] Globale CLAUDE.md nach $ClaudeDir kopieren..."
if (-not (Test-Path $ClaudeDir)) { New-Item -ItemType Directory -Path $ClaudeDir | Out-Null }
Copy-Item "$PSScriptRoot\claude_global.md" "$ClaudeDir\CLAUDE.md" -Force
Write-Host "  OK: $ClaudeDir\CLAUDE.md" -ForegroundColor Green

# 2. Agenten-Repos klonen (falls noch nicht vorhanden)
Write-Host "`n[2/3] Agenten-Repos pruefen / klonen..."

$Repos = @(
    @{ Name = "Termindokumentierer"; Url = "https://github.com/Jakob243978/Termindokumentierer.git" },
    @{ Name = "Assistenz";           Url = "https://github.com/Jakob243978/Assistenz.git" },
    @{ Name = "Workflow Builder";    Url = "https://github.com/Jakob243978/Workflow-Builder.git" },
    @{ Name = "SocialMediaBuilder";  Url = "https://github.com/Jakob243978/SocialMediaBuilder.git" }
)

foreach ($repo in $Repos) {
    $path = Join-Path $BaseDir $repo.Name
    if (Test-Path $path) {
        Write-Host "  OK (bereits vorhanden): $($repo.Name)" -ForegroundColor Yellow
    } else {
        Write-Host "  Klone: $($repo.Name)..."
        git clone $repo.Url $path
        Write-Host "  OK: $($repo.Name)" -ForegroundColor Green
    }
}

# 3. Python-Abhaengigkeiten installieren
Write-Host "`n[3/3] Python-Abhaengigkeiten installieren..."

$PythonProjects = @("Termindokumentierer")
foreach ($proj in $PythonProjects) {
    $req = Join-Path (Join-Path $BaseDir $proj) "requirements.txt"
    if (Test-Path $req) {
        Write-Host "  pip install fuer $proj..."
        pip install -r $req --quiet
        Write-Host "  OK: $proj" -ForegroundColor Green
    }
}

# Abschluss
Write-Host "`n=== Setup abgeschlossen ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Naechste Schritte (manuell):" -ForegroundColor Yellow
Write-Host "  1. .env Dateien anlegen (Vorlage: .env.example in jedem Projekt)"
Write-Host "  2. MCP-Verbindungen in Claude Code einrichten (Composio)"
Write-Host "     -> /mcp composio"
Write-Host "  3. Claude Code neu starten damit CLAUDE.md geladen wird"
