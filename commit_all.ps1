# Session Ende: Alle Repos committen und nach GitHub pushen
# Ausfuehren: .\commit_all.ps1
# Optional mit eigenem Commit-Message: .\commit_all.ps1 -Message "Meine Nachricht"

param(
    [string]$Message = "Session sync $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
)

$BaseDir = "C:\Users\$env:USERNAME\claude_projects"
$Repos = @("Schaltzentrale", "Termindokumentierer", "Assistenz", "Workflow Builder")

Write-Host "=== Session Ende: Commit & Push alle Repos ===" -ForegroundColor Cyan
Write-Host "  Commit-Message: $Message`n"

foreach ($repo in $Repos) {
    $path = Join-Path $BaseDir $repo
    if (-not (Test-Path "$path\.git")) {
        Write-Host "  Uebersprungen (nicht vorhanden): $repo" -ForegroundColor Yellow
        continue
    }

    $status = git -C $path status --porcelain 2>&1
    if ($status) {
        Write-Host "  $repo - $($status.Count) Aenderung(en)..."
        git -C $path add -A
        git -C $path commit -m $Message
        git -C $path push
        Write-Host "  OK: $repo gepusht" -ForegroundColor Green
    } else {
        Write-Host "  Keine Aenderungen: $repo" -ForegroundColor Yellow
    }
}

Write-Host "`n=== Sync abgeschlossen ===" -ForegroundColor Cyan
