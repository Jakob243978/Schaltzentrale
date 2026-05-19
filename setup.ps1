# Schaltzentrale Setup-Skript
# Richtet die Entwicklungsumgebung auf einem neuen Geraet ein.
# Ausfuehren: .\setup.ps1
#   Optional: .\setup.ps1 -EnableMemoryJunction   (Memory-Pfad als Junction in Vault\Memory setzen)
#   Optional: .\setup.ps1 -DryRun                  (zeigt nur was getan wuerde)

param(
    [switch]$EnableMemoryJunction,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$BaseDir = Split-Path $PSScriptRoot -Parent
$ClaudeDir = "C:\Users\$env:USERNAME\.claude"
$DryPrefix = if ($DryRun) { "[DRY] " } else { "" }

Write-Host "=== Schaltzentrale Setup ===" -ForegroundColor Cyan
if ($DryRun) { Write-Host "  DRY-RUN aktiv - keine Aenderungen" -ForegroundColor Yellow }

# ---------------------------------------------------------------
# 1. Globale CLAUDE.md deployen
# ---------------------------------------------------------------
Write-Host "`n[1/5] Globale CLAUDE.md nach $ClaudeDir kopieren..."
if (-not (Test-Path $ClaudeDir)) {
    if (-not $DryRun) { New-Item -ItemType Directory -Path $ClaudeDir | Out-Null }
}
if ($DryRun) {
    Write-Host "  ${DryPrefix}Copy-Item $PSScriptRoot\claude_global.md -> $ClaudeDir\CLAUDE.md" -ForegroundColor Yellow
} else {
    Copy-Item "$PSScriptRoot\claude_global.md" "$ClaudeDir\CLAUDE.md" -Force
    Write-Host "  OK: $ClaudeDir\CLAUDE.md" -ForegroundColor Green
}

# ---------------------------------------------------------------
# 2. Agenten- und Vault-Repos klonen (falls noch nicht vorhanden)
# ---------------------------------------------------------------
Write-Host "`n[2/5] Repos pruefen / klonen..."

$Repos = @(
    @{ Name = "Termindokumentierer"; Url = "https://github.com/Jakob243978/Termindokumentierer.git" },
    @{ Name = "Assistenz";           Url = "https://github.com/Jakob243978/Assistenz.git" },
    @{ Name = "Workflow Builder";    Url = "https://github.com/Jakob243978/Workflow-Builder.git" },
    @{ Name = "SocialMediaBuilder";  Url = "https://github.com/Jakob243978/SocialMediaBuilder.git" },
    @{ Name = "ZeitenAbgleich";      Url = "https://github.com/Jakob243978/ZeitenAbgleich.git" },
    @{ Name = "vault";               Url = "https://github.com/Jakob243978/vault.git" }
)

foreach ($repo in $Repos) {
    $path = Join-Path $BaseDir $repo.Name
    if (Test-Path $path) {
        Write-Host "  OK (bereits vorhanden): $($repo.Name)" -ForegroundColor Yellow
    } else {
        if ($DryRun) {
            Write-Host "  ${DryPrefix}git clone $($repo.Url) $path" -ForegroundColor Yellow
        } else {
            Write-Host "  Klone: $($repo.Name)..."
            git clone $repo.Url $path
            Write-Host "  OK: $($repo.Name)" -ForegroundColor Green
        }
    }
}

# ---------------------------------------------------------------
# 3. Skills nach ~\.claude\skills\ deployen (idempotent via robocopy /MIR)
# ---------------------------------------------------------------
Write-Host "`n[3/5] Skills nach $ClaudeDir\skills\ deployen..."

$SkillsSource = "$PSScriptRoot\skills_sources"
$SkillsTarget = "$ClaudeDir\skills"

if (-not (Test-Path $SkillsSource)) {
    Write-Host "  WARNUNG: $SkillsSource fehlt - kein Skill-Deploy moeglich" -ForegroundColor Red
} else {
    if ($DryRun) {
        Write-Host "  ${DryPrefix}robocopy /MIR $SkillsSource -> $SkillsTarget" -ForegroundColor Yellow
    } else {
        if (-not (Test-Path $SkillsTarget)) { New-Item -ItemType Directory -Path $SkillsTarget | Out-Null }
        $result = robocopy $SkillsSource $SkillsTarget /MIR /NFL /NDL /NJH /NJS /NC /NS
        # Robocopy: exit code <8 = success
        if ($LASTEXITCODE -lt 8) {
            Write-Host "  OK: Skills deployt nach $SkillsTarget" -ForegroundColor Green
        } else {
            Write-Host "  FEHLER: robocopy exit code $LASTEXITCODE" -ForegroundColor Red
        }
    }
}

# ---------------------------------------------------------------
# 4. Memory-Junction setzen (nur bei -EnableMemoryJunction)
# ---------------------------------------------------------------
if ($EnableMemoryJunction) {
    Write-Host "`n[4/5] Memory-Junction setzen..."

    # Claude-Code-Projektname aus $BaseDir ableiten: ':', '\' und '_' -> '-'
    # PC1: C:\Users\LG\claude_projects -> C--Users-LG-claude-projects
    # PC2: C:\claude_projekte           -> C--claude-projekte
    $projectFolderName = ($BaseDir -replace '[:\\_]', '-')
    $MemoryDefaultPath = "$ClaudeDir\projects\$projectFolderName\memory"

    # Fallback: falls abgeleiteter Pfad nicht existiert, im projects-Verzeichnis nach
    # einem Ordner mit memory-Subordner suchen (case-insensitive, deckt PC1-Eigenart c--... ab)
    if (-not (Test-Path $MemoryDefaultPath)) {
        $candidate = Get-ChildItem "$ClaudeDir\projects" -Directory -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -ieq $projectFolderName -and (Test-Path (Join-Path $_.FullName 'memory')) } |
            Select-Object -First 1
        if ($candidate) {
            $MemoryDefaultPath = Join-Path $candidate.FullName 'memory'
            Write-Host "  Hinweis: Pfad case-insensitive aufgeloest -> $MemoryDefaultPath" -ForegroundColor Yellow
        }
    }
    $MemoryVaultPath = Join-Path $BaseDir "vault\Memory"
    $BackupTimestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $BackupPath = "$ClaudeDir\projects\_memory_backup_$BackupTimestamp"

    # Sicherheits-Check
    if (-not (Test-Path $MemoryVaultPath)) {
        Write-Host "  ABBRUCH: $MemoryVaultPath fehlt - Vault muss vorher geklont sein" -ForegroundColor Red
        exit 1
    }

    # Backup existierender Memory (falls vorhanden und kein Junction)
    if (Test-Path $MemoryDefaultPath) {
        $item = Get-Item $MemoryDefaultPath -Force
        if ($item.LinkType -eq "Junction") {
            Write-Host "  Junction bereits aktiv -> $($item.Target | Select-Object -First 1)" -ForegroundColor Yellow
        } else {
            if ($DryRun) {
                Write-Host "  ${DryPrefix}Backup $MemoryDefaultPath -> $BackupPath" -ForegroundColor Yellow
                Write-Host "  ${DryPrefix}Remove $MemoryDefaultPath" -ForegroundColor Yellow
                Write-Host "  ${DryPrefix}mklink /J $MemoryDefaultPath $MemoryVaultPath" -ForegroundColor Yellow
            } else {
                Write-Host "  Backup nach $BackupPath..."
                robocopy $MemoryDefaultPath $BackupPath /E /NFL /NDL /NJH /NJS /NC /NS | Out-Null
                if ($LASTEXITCODE -ge 8) {
                    Write-Host "  ABBRUCH: Backup fehlgeschlagen (exit $LASTEXITCODE) - keine Junction gesetzt" -ForegroundColor Red
                    exit 1
                }
                Write-Host "  Backup OK ($((Get-ChildItem $BackupPath -Recurse -File).Count) Files)" -ForegroundColor Green

                # Default-Memory loeschen
                Remove-Item $MemoryDefaultPath -Recurse -Force
                # Junction setzen
                cmd /c mklink /J "$MemoryDefaultPath" "$MemoryVaultPath" | Out-Null
                $linkItem = Get-Item $MemoryDefaultPath -Force
                if ($linkItem.LinkType -eq "Junction") {
                    Write-Host "  OK: Junction gesetzt $MemoryDefaultPath -> $MemoryVaultPath" -ForegroundColor Green
                } else {
                    Write-Host "  FEHLER: Junction nicht erstellt - Backup unter $BackupPath" -ForegroundColor Red
                    exit 1
                }
            }
        }
    } else {
        # Memory-Default-Pfad existiert nicht (z.B. PC2 Erst-Setup) - direkt Junction setzen
        if ($DryRun) {
            Write-Host "  ${DryPrefix}mklink /J $MemoryDefaultPath $MemoryVaultPath (neu)" -ForegroundColor Yellow
        } else {
            $parent = Split-Path $MemoryDefaultPath -Parent
            if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
            cmd /c mklink /J "$MemoryDefaultPath" "$MemoryVaultPath" | Out-Null
            Write-Host "  OK: Junction (neu) $MemoryDefaultPath -> $MemoryVaultPath" -ForegroundColor Green
        }
    }
} else {
    Write-Host "`n[4/5] Memory-Junction uebersprungen (Flag -EnableMemoryJunction nicht gesetzt)" -ForegroundColor Yellow
}

# ---------------------------------------------------------------
# 4b. Researcher-Junction sicherstellen (idempotent, immer)
#     vault/Researcher zeigt auf claude_projects/Researcher (Repo-canonical).
# ---------------------------------------------------------------
$ResearcherRepo = Join-Path $BaseDir "Researcher"
$ResearcherVaultPath = Join-Path $BaseDir "vault\Researcher"

if ((Test-Path $ResearcherRepo) -and (Test-Path (Join-Path $BaseDir "vault"))) {
    Write-Host "`n[4b/5] Researcher-Junction sicherstellen..."
    if (Test-Path $ResearcherVaultPath) {
        $item = Get-Item $ResearcherVaultPath -Force
        if ($item.LinkType -eq "Junction") {
            Write-Host "  Junction bereits aktiv -> $($item.Target | Select-Object -First 1)" -ForegroundColor Yellow
        } else {
            if ($DryRun) {
                Write-Host "  ${DryPrefix}Remove vault\Researcher (war kein Junction)" -ForegroundColor Yellow
                Write-Host "  ${DryPrefix}mklink /J vault\Researcher -> $ResearcherRepo" -ForegroundColor Yellow
            } else {
                Remove-Item $ResearcherVaultPath -Recurse -Force
                cmd /c mklink /J "$ResearcherVaultPath" "$ResearcherRepo" | Out-Null
                $linkItem = Get-Item $ResearcherVaultPath -Force
                if ($linkItem.LinkType -eq "Junction") {
                    Write-Host "  OK: Junction gesetzt vault\Researcher -> $ResearcherRepo" -ForegroundColor Green
                } else {
                    Write-Host "  FEHLER: Junction nicht erstellt" -ForegroundColor Red
                }
            }
        }
    } else {
        if ($DryRun) {
            Write-Host "  ${DryPrefix}mklink /J vault\Researcher -> $ResearcherRepo (neu)" -ForegroundColor Yellow
        } else {
            cmd /c mklink /J "$ResearcherVaultPath" "$ResearcherRepo" | Out-Null
            Write-Host "  OK: Junction (neu) vault\Researcher -> $ResearcherRepo" -ForegroundColor Green
        }
    }
}

# ---------------------------------------------------------------
# 5. Python-Abhaengigkeiten installieren
# ---------------------------------------------------------------
Write-Host "`n[5/5] Python-Abhaengigkeiten installieren..."

$PythonProjects = @("Termindokumentierer")
foreach ($proj in $PythonProjects) {
    $req = Join-Path (Join-Path $BaseDir $proj) "requirements.txt"
    if (Test-Path $req) {
        if ($DryRun) {
            Write-Host "  ${DryPrefix}pip install -r $req" -ForegroundColor Yellow
        } else {
            Write-Host "  pip install fuer $proj..."
            pip install -r $req --quiet
            Write-Host "  OK: $proj" -ForegroundColor Green
        }
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
Write-Host "  4. Obsidian-App: Vault unter $BaseDir\vault\ oeffnen"
if (-not $EnableMemoryJunction) {
    Write-Host "  5. Memory-Junction aktivieren: .\setup.ps1 -EnableMemoryJunction"
}
