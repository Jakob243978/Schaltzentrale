param([string]$Dir = "C:\claude_projekte\vault\Memory")

$dash = [char]0x2014

$files = Get-ChildItem "$Dir\*.md" | Where-Object { $_.Name -ne 'MEMORY.md' } | Sort-Object Name
$entries = foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw -Encoding UTF8
    if ($content -match '(?s)^---\s*\r?\n(.*?)\r?\n---') {
        $fm = $matches[1]
        $title = if ($fm -match '(?m)^title:\s*(.+?)\s*$') { $matches[1].Trim() } else { $f.BaseName }
        $desc  = if ($fm -match '(?m)^description:\s*(.+?)\s*$') { $matches[1].Trim().Trim('"') } else { '' }
        $type  = if ($fm -match '(?m)^type:\s*(\w+)') { $matches[1] } else { 'other' }
        [PSCustomObject]@{ File=$f.Name; Type=$type; Title=$title; Desc=$desc }
    }
}

$lines = @()
foreach ($t in @('user','project','feedback','reference')) {
    $group = $entries | Where-Object Type -eq $t
    if (-not $group) { continue }
    foreach ($e in $group) {
        $lines += "- [$($e.Title)]($($e.File)) $dash $($e.Desc)"
    }
}

$out = ($lines -join "`n") + "`n"
[System.IO.File]::WriteAllText("$Dir\MEMORY.md", $out, [System.Text.UTF8Encoding]::new($false))

Write-Host "Zeilen: $($lines.Count)"
Write-Host "Bytes:  $((Get-Item "$Dir\MEMORY.md").Length)"
