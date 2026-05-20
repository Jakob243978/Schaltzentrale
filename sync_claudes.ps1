# Spiegelt alle Projekt-CLAUDE.md-Files nach vault/Docs/<projekt>_CLAUDE.md
# Read-only Snapshot — Source of Truth bleibt das jeweilige Repo.
# Haengt automatisch eine "Verwandte Memorys"-Sektion an, basierend auf
# vault/Memory/*.md-Files mit passendem project:-Frontmatter.
# Wird von pull_all.ps1 am Ende aufgerufen.

$BaseDir = Split-Path $PSScriptRoot -Parent
$VaultRoot = Join-Path $BaseDir "vault"
$VaultDocs = Join-Path $VaultRoot "Docs"
$VaultMemory = Join-Path $VaultRoot "Memory"

Write-Host "=== Sync CLAUDE.mds nach vault\Docs\ ===" -ForegroundColor Cyan

if (-not (Test-Path $VaultRoot)) {
    Write-Host "  ABBRUCH: vault\ fehlt - sync nicht moeglich" -ForegroundColor Red
    return
}
if (-not (Test-Path $VaultDocs)) {
    New-Item -ItemType Directory -Path $VaultDocs | Out-Null
}

# ---------------------------------------------------------------
# Project-Key-Aliases: ein Repo kann mehrere Memory-project:-Werte anziehen
# Beispiel: KundenAB-Repo enthaelt BeyerImmo-Workflows -> Memorys haben project: beyerimmo
# Format: 'repo-key' = @('mem-key1', 'mem-key2', ...)
# Defaults: jeder Repo-Key matched auch sich selbst (lowercase).
# ---------------------------------------------------------------
$ProjectAliases = @{
    'kundenab'         = @('beyerimmo', 'kundenab')
    'homeassistant'    = @('homeassistant', 'heizung-restore', 'heizung_restore', 'ha')
    'immobewertung'    = @('immobewertung', 'ankaufsprofil', 'ankaufsprofil-idee', 'ankaufsprofil_idee')
    'dropboxcheck'     = @('dropboxcheck', 'lr-import', 'lr_import')
    'workflow_builder' = @('workflow-builder', 'workflowbuilder', 'workflow_builder')
}

# ---------------------------------------------------------------
# Memory-Index aufbauen (einmal scannen, dann je Projekt filtern)
# ---------------------------------------------------------------
$memoryIndex = @()
if (Test-Path $VaultMemory) {
    foreach ($memFile in Get-ChildItem $VaultMemory -File -Filter *.md) {
        if ($memFile.Name -eq 'MEMORY.md') { continue }
        $content = Get-Content $memFile.FullName -Raw -Encoding UTF8
        if ($content -match '(?s)^---\r?\n(.*?)\r?\n---') {
            $fm = $matches[1]
            $proj  = if ($fm -match '(?m)^project:\s*(.+?)\s*$') { $matches[1].Trim('"').Trim("'").Trim().ToLower() } else { $null }
            $type  = if ($fm -match '(?m)^type:\s*(.+?)\s*$')    { $matches[1].Trim().ToLower() } else { 'other' }
            $desc  = if ($fm -match '(?m)^description:\s*(.+?)\s*$') { $matches[1].Trim('"').Trim("'").Trim() } else { '' }

            $memoryIndex += [PSCustomObject]@{
                FileName  = $memFile.BaseName
                Project   = $proj
                Type      = $type
                Desc      = $desc
            }
        }
    }
}
Write-Host "  Memory-Index: $($memoryIndex.Count) Files indexiert" -ForegroundColor DarkGray

# ---------------------------------------------------------------
# Repos scannen und CLAUDE.mds spiegeln
# ---------------------------------------------------------------
$ExcludeDirs = @("vault", "obsidian", "lightroom-mcp")
$projects = Get-ChildItem $BaseDir -Directory | Where-Object {
    $_.Name -notin $ExcludeDirs -and
    $_.Name -notlike "_*" -and
    $_.Name -notlike "*_BACKUP_*" -and
    $_.Name -notlike "*_backup_*" -and
    $_.Name -notlike ".*"
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
    $safeName = $repoName -replace ' ', '_'
    $targetPath = Join-Path $VaultDocs "${safeName}_CLAUDE.md"

    # Original lesen + ggf. Frontmatter strippen
    $originalContent = Get-Content $sourcePath -Raw -Encoding UTF8
    if ($originalContent -match '(?s)^---\r?\n.*?\r?\n---\r?\n') {
        $bodyContent = $originalContent -replace '(?s)^---\r?\n.*?\r?\n---\r?\n', ''
    } else {
        $bodyContent = $originalContent
    }

    # Mirror-Header
    $timestamp = Get-Date -Format 'yyyy-MM-ddTHH:mm:ss'
    $projKeyForTag = $safeName.ToLower()
    $tagsLine = "tags: [typ/claude-md-mirror, project/$projKeyForTag]"
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

    # ---- Cross-Ref Sektion: Memorys mit passendem project: ----
    $repoKey = $safeName.ToLower()
    $memProjectKeys = if ($ProjectAliases.ContainsKey($repoKey)) {
        $ProjectAliases[$repoKey]
    } else {
        @($repoKey)
    }

    $relatedByType = [ordered]@{
        project   = @()
        feedback  = @()
        reference = @()
        user      = @()
    }
    foreach ($mem in $memoryIndex) {
        if ($null -eq $mem.Project) { continue }
        if ($memProjectKeys -contains $mem.Project) {
            $entry = "- [[../Memory/$($mem.FileName)|$($mem.FileName)]]"
            if ($mem.Desc) { $entry += " - $($mem.Desc)" }
            $bucket = if ($relatedByType.Contains($mem.Type)) { $mem.Type } else { 'project' }
            $relatedByType[$bucket] += $entry
        }
    }

    $totalRelated = ($relatedByType.Values | ForEach-Object { $_.Count } | Measure-Object -Sum).Sum
    $crossRefSection = ""
    if ($totalRelated -gt 0) {
        $crossRefSection = "`n`n---`n`n## Verwandte Memorys (auto-generiert)`n`n"
        $crossRefSection += "> [!info] Quelle`n> Auto-injected von ``sync_claudes.ps1`` aus ``vault/Memory/*.md`` mit ``project: $($memProjectKeys -join ', ')`` im Frontmatter.`n`n"
        foreach ($t in @('project', 'feedback', 'reference', 'user')) {
            if ($relatedByType[$t].Count -gt 0) {
                $crossRefSection += "### $($t.Substring(0,1).ToUpper() + $t.Substring(1))`n"
                $crossRefSection += ($relatedByType[$t] -join "`n") + "`n`n"
            }
        }
    }

    $finalContent = $mirrorHeader + $bodyContent + $crossRefSection
    [System.IO.File]::WriteAllText($targetPath, $finalContent, [System.Text.UTF8Encoding]::new($false))

    $relMsg = if ($totalRelated -gt 0) { " (+$totalRelated verwandte Memorys)" } else { "" }
    Write-Host "  OK: $repoName -> Docs\${safeName}_CLAUDE.md$relMsg" -ForegroundColor Green
    $syncedCount++
}

Write-Host ""
Write-Host "  Synced: $syncedCount  /  Skipped (keine CLAUDE.md): $skippedCount" -ForegroundColor Cyan
