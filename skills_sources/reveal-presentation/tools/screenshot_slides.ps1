# screenshot_slides.ps1 - Visual-Review-Pass für reveal.js Decks (PowerShell)
#
# Macht headless-Chromium-Screenshots pro Slide, mit allen Fragments
# sichtbar (Override via Temp-HTML-Kopie). Output ist eine PNG pro Slide
# unter <OutputDir>/slide_NN.png.
#
# Usage:
#   .\tools\screenshot_slides.ps1 -Presi <presi.html> -NSlides <n> -OutputDir <dir>
#
# Beispiel:
#   .\tools\screenshot_slides.ps1 -Presi onboarding\team.html -NSlides 16 -OutputDir C:\temp\shots
#
# Env-Override:
#   $env:CHROME = "<pfad>"   Chromium-Binary (Default: Windows Chrome)

param(
    [Parameter(Mandatory=$true)][string]$Presi,
    [Parameter(Mandatory=$true)][int]$NSlides,
    [Parameter(Mandatory=$true)][string]$OutputDir
)

$ErrorActionPreference = "Stop"

# Chromium auflösen: $env:CHROME zuerst, dann Standard-Pfade
$chrome = $env:CHROME
if (-not $chrome) {
    $candidates = @(
        "C:\Program Files\Google\Chrome\Application\chrome.exe",
        "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "${env:LOCALAPPDATA}\Google\Chrome\Application\chrome.exe"
    )
    foreach ($c in $candidates) {
        if (Test-Path $c) { $chrome = $c; break }
    }
}
if (-not $chrome -or -not (Test-Path $chrome)) {
    Write-Error "Chromium-Binary nicht gefunden. Setze `$env:CHROME oder installiere Chrome."
    exit 3
}

if (-not (Test-Path $Presi)) {
    Write-Error "Presi-File '$Presi' nicht gefunden."
    exit 4
}

$presiAbs = (Resolve-Path $Presi).Path
New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null

# CSS-Override injizieren: Fragments sofort sichtbar
$tmpHtml = [System.IO.Path]::GetTempFileName() + ".html"
$override = '.reveal .fragment{opacity:1!important;visibility:visible!important;}'
$content = Get-Content $presiAbs -Raw -Encoding utf8
$content = $content -replace '</style>', ($override + "`n</style>")
Set-Content -Path $tmpHtml -Value $content -Encoding utf8

# URL für Chromium
$tmpAbs = (Resolve-Path $tmpHtml).Path
$url = "file:///" + ($tmpAbs -replace '\\', '/')

Write-Host "Chromium: $chrome"
Write-Host "Source:   $presiAbs"
Write-Host "Slides:   $NSlides"
Write-Host "Output:   $OutputDir"
Write-Host ""

try {
    for ($n = 0; $n -lt $NSlides; $n++) {
        $nn = "{0:D2}" -f $n
        $out = Join-Path $OutputDir "slide_$nn.png"
        $userDir = Join-Path $env:TEMP "chrome_userdata_$(Get-Random)"
        Write-Host "  Slide $nn -> $out"
        & $chrome `
            --headless=new `
            --disable-gpu `
            --no-sandbox `
            --hide-scrollbars `
            --user-data-dir=$userDir `
            --window-size=1920,1080 `
            --screenshot=$out `
            --virtual-time-budget=8000 `
            "$url#/$n" 2>$null | Out-Null
        if (Test-Path $userDir) { Remove-Item -Recurse -Force $userDir -ErrorAction SilentlyContinue }
    }
}
finally {
    if (Test-Path $tmpHtml) { Remove-Item $tmpHtml -Force }
}

Write-Host ""
Write-Host "OK $NSlides Screenshots in $OutputDir/"
Write-Host "  Naechster Schritt: mit Read-Tool pro Datei visuell pruefen."
