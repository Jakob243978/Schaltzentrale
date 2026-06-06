# Session Ende: Alle Repos committen und nach GitHub pushen
# Ausfuehren: .\commit_all.ps1
# Optional mit eigenem Commit-Message: .\commit_all.ps1 -Message "Meine Nachricht"

param(
    [string]$Message = "Session sync $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
)

$BaseDir = Split-Path $PSScriptRoot -Parent
$Repos = @("Schaltzentrale", "Termindokumentierer", "Assistenz", "Workflow Builder", "SocialMediaBuilder", "GuestAI", "HomeAssistant", "Researcher", "Immobewertung", "KundenAB", "PropertyDesk", "DropboxCheck", "ZeitenAbgleich", "AgentischesArbeiten", "vault", "personal_branding")

Write-Host "=== Session Ende: Commit & Push alle Repos ===" -ForegroundColor Cyan
Write-Host "  Commit-Message: $Message`n"

foreach ($repo in $Repos) {
    $path = Join-Path $BaseDir $repo
    if (-not (Test-Path "$path\.git")) {
        Write-Host "  Uebersprungen (nicht vorhanden): $repo" -ForegroundColor Yellow
        continue
    }

    # Size-Check fuer vault: warne bei untracked/modified Files >5 MB
    if ($repo -eq "vault") {
        $bigFiles = git -C $path status --porcelain | ForEach-Object {
            $file = $_.Substring(3).Trim('"')
            $fullPath = Join-Path $path $file
            if ((Test-Path $fullPath -PathType Leaf) -and ((Get-Item $fullPath).Length -gt 5MB)) {
                "{0} ({1:N1} MB)" -f $file, ((Get-Item $fullPath).Length / 1MB)
            }
        }
        if ($bigFiles) {
            Write-Host "  WARNUNG: vault enthaelt Files >5 MB:" -ForegroundColor Red
            $bigFiles | ForEach-Object { Write-Host "    - $_" -ForegroundColor Red }
            Write-Host "  Pruefe .gitignore (PDF/XLSX/MP4 sollten ignoriert sein)." -ForegroundColor Yellow
        }
    }

    $status = git -C $path status --porcelain 2>&1
    if ($status) {
        Write-Host "  $repo - $($status.Count) Aenderung(en)..."
        git -C $path add -A
        git -C $path commit -m $Message
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  FEHLER: Commit fehlgeschlagen ($repo, Exit $LASTEXITCODE)" -ForegroundColor Red
            continue
        }
        git -C $path push
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  OK: $repo gepusht" -ForegroundColor Green
        } else {
            Write-Host "  FEHLER: Push fehlgeschlagen ($repo, Exit $LASTEXITCODE) - Commit liegt lokal vor" -ForegroundColor Red
        }
    } else {
        Write-Host "  Keine Aenderungen: $repo" -ForegroundColor Yellow
    }
}

Write-Host "`n=== Sync abgeschlossen ===" -ForegroundColor Cyan
