# Session Start: Alle Repos auf den neuesten Stand bringen
# Ausfuehren: .\pull_all.ps1

$BaseDir = Split-Path $PSScriptRoot -Parent
$Repos = @("Schaltzentrale", "Termindokumentierer", "Assistenz", "Workflow Builder", "SocialMediaBuilder", "GuestAI", "HomeAssistant", "Researcher", "Immobewertung", "KundenAB", "PropertyDesk", "DropboxCheck", "ZeitenAbgleich", "vault")

Write-Host "=== Session Start: Pull alle Repos ===" -ForegroundColor Cyan

foreach ($repo in $Repos) {
    $path = Join-Path $BaseDir $repo
    if (Test-Path "$path\.git") {
        Write-Host "  Pull: $repo..." -NoNewline
        $result = git -C $path pull --ff-only 2>&1
        Write-Host " OK" -ForegroundColor Green
    } else {
        Write-Host "  Uebersprungen (nicht vorhanden): $repo" -ForegroundColor Yellow
    }
}

Write-Host "`n=== Verifikation Setup-Integritaet ===" -ForegroundColor Cyan

# Skill-Verzeichnis vorhanden?
$SkillPath = "C:\Users\$env:USERNAME\.claude\skills\obsidian-skills\skills\obsidian-markdown\SKILL.md"
if (Test-Path $SkillPath) {
    Write-Host "  Skills installiert (obsidian-markdown gefunden)" -ForegroundColor Green
} else {
    Write-Host "  WARNUNG: Skills fehlen unter ~\.claude\skills\obsidian-skills\" -ForegroundColor Red
    Write-Host "           -> .\setup.ps1 ausfuehren" -ForegroundColor Yellow
}

# Memory-Junction aktiv? (falls eingerichtet)
$MemoryPath = "C:\Users\$env:USERNAME\.claude\projects\c--Users-$env:USERNAME-claude-projects\memory"
if (Test-Path $MemoryPath) {
    $item = Get-Item $MemoryPath -Force
    if ($item.LinkType -eq "Junction") {
        $target = $item.Target | Select-Object -First 1
        Write-Host "  Memory-Junction aktiv -> $target" -ForegroundColor Green
    } else {
        Write-Host "  Memory ist KEIN Junction (Default-Modus, Vault\Memory nicht canonical)" -ForegroundColor Yellow
    }
}

# Projekt-CLAUDE.mds ins Vault spiegeln (read-only Snapshots)
Write-Host ""
& "$PSScriptRoot\sync_claudes.ps1"

Write-Host "`n=== Alle Repos aktuell ===" -ForegroundColor Cyan
