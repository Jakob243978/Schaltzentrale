# Session Start: Alle Repos auf den neuesten Stand bringen
# Ausfuehren: .\pull_all.ps1

$BaseDir = Split-Path $PSScriptRoot -Parent
$Repos = @("Schaltzentrale", "Termindokumentierer", "Assistenz", "Workflow Builder", "SocialMediaBuilder", "GuestAI", "HomeAssistant", "Researcher", "Immobewertung", "KundenAB")

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

Write-Host "`n=== Alle Repos aktuell ===" -ForegroundColor Cyan
