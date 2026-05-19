# Spiegelt alle Projekt-CLAUDE.md-Files nach vault/Docs/<projekt>_CLAUDE.md
# Read-only Snapshot — Source of Truth bleibt das jeweilige Repo.
# Wird von pull_all.ps1 am Ende aufgerufen.
# Standalone aufrufbar: .\sync_claudes.ps1

$BaseDir = Split-Path $PSScriptRoot -Parent
$VaultDocs = Join-Path $BaseDir "vault\Docs"

Write-Host "=== Sync CLAUDE.mds nach vault\Docs\ ===" -ForegroundColor Cyan

# Vault muss vorhanden sein
if (-not (Test-Path (Join-Path $BaseDir "vault"))) {
    Write-Host "  ABBRUCH: vault\ fehlt - sync nicht moeglich" -ForegroundColor Red
    return
}

# Docs-Folder anlegen falls fehlt
if (-not (Test-Path $VaultDocs)) {
    New-Item -ItemType Directory -Path $VaultDocs | Out-Null
}

# Alle Top-Level-Projekte unter BaseDir scannen (exclude vault selbst, .obsidian, Backup-Ordner)
$ExcludeDirs = @("vault", "obsidian", "lightroom-mcp")
$projects = Get-ChildItem $BaseDir -Directory | Where-Object {
    $_.Name -notin $ExcludeDirs -and
    $_.Name -notlike "_*" -and
    $_.Name -notlike "obsidian_BACKUP_*"
}

$syncedCount = 0
$skippedCount = 0

foreach ($proj in $projects) {
    $sourcePath = Join-Path $proj.FullName "CLAUDE.md"
    if (-not (Test-Path $sourcePath)) {
        Write-Host "  - $($proj.Name): keine CLAUDE.md" -ForegroundColor DarkGray
        $skippedCount++
        continue
    }

    $repoName = $proj.Name
    # Dateiname-safe: Leerzeichen durch Unterstriche ersetzen
    $safeName = $repoName -replace ' ', '_'
    $targetPath = Join-Path $VaultDocs "${safeName}_CLAUDE.md"

    # Original lesen
    $originalContent = Get-Content $sourcePath -Raw -Encoding UTF8

    # Wenn Original schon Frontmatter hat, strippen (sonst doppelter Frontmatter im Spiegel)
    if ($originalContent -match '(?s)^---\r?\n.*?\r?\n---\r?\n') {
        $bodyContent = $originalContent -replace '(?s)^---\r?\n.*?\r?\n---\r?\n', ''
    } else {
        $bodyContent = $originalContent
    }

    # Mirror-Header mit Frontmatter + Warnung
    $timestamp = Get-Date -Format 'yyyy-MM-ddTHH:mm:ss'
    $tagsLine = "tags: [typ/claude-md-mirror, project/$($safeName.ToLower())]"
    $mirrorHeader = @"
---
title: $repoName - CLAUDE.md (gespiegelt)
type: claude-md-mirror
project: $safeName
source: claude_projects/$repoName/CLAUDE.md
synced_at: $timestamp
$tagsLine
aliases:
  - $repoName CLAUDE
---

> [!warning] Read-only Spiegel
> Auto-Kopie von ``claude_projects/$repoName/CLAUDE.md`` - **NICHT hier editieren**. Wird beim naechsten ``pull_all.ps1`` ueberschrieben. Source of Truth ist das Projekt-Repo.

---

"@

    $finalContent = $mirrorHeader + $bodyContent
    # UTF8 ohne BOM
    [System.IO.File]::WriteAllText($targetPath, $finalContent, [System.Text.UTF8Encoding]::new($false))
    Write-Host "  OK: $repoName -> Docs\${safeName}_CLAUDE.md" -ForegroundColor Green
    $syncedCount++
}

Write-Host ""
Write-Host "  Synced: $syncedCount  /  Skipped (keine CLAUDE.md): $skippedCount" -ForegroundColor Cyan
