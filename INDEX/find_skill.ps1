# ============================================================================
# find_skill.ps1 — ПОИСК СКИЛЛА/ИНСТРУМЕНТА ПО СМЫСЛУ (по готовому индексу)
# ============================================================================
# Зачем: «какой скилл нужен для задачи» — за миллисекунды, без чтения 26 КБ карты и grep.
# КАНОН:
#  * префикс запроса — ОБЯЗАТЕЛЬНО "search_query: " (без него качество рушится);
#  * индекс собирается скриптом index_skills.ps1 (полная индексация, один раз);
#  * выдача — кандидаты (путь+оценка), решение принимает вызывающий (правила/модель).
# ЗАПУСК: powershell -NoProfile -ExecutionPolicy Bypass -File find_skill.ps1 -Query "сделать коммит по правилам дома" [-Top 5]
#         -Query @('текст1','текст2')  — можно пачкой (эмбеддим одним запросом)
#         -Full — печатать ПОЛНЫЕ пути (для вызова из инструмента теста find_skill)
# ============================================================================
param(
    [string[]]$Query = @(),
    [int]$Top = 5,
    [string]$Model = 'nomic-embed-text-v2-moe:latest',
    [switch]$NoPrefix,
    [switch]$Full
)
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = 'Stop'
$root = 'D:\AI\repo\INDEX'
# БАЗА СМЕНЯЕМАЯ: берём версию из указателя index\CURRENT.txt (иначе — старый путь для совместимости)
$curPtr = Join-Path $root 'index\CURRENT.txt'
$idx = ''
if (Test-Path $curPtr) {
    $ver = (Get-Content $curPtr -Raw -Encoding utf8).Trim()
    if ($ver) { $idx = Join-Path $root ("index\versions\$ver\skills_index.jsonl") }
}
if (-not $idx -or -not (Test-Path $idx)) { $idx = Join-Path $root 'index\skills_index.jsonl' }
if (-not (Test-Path $idx)) { Write-Host "НЕТ ИНДЕКСА: сначала index_skills_v2.ps1"; exit 1 }
if (-not $Query.Count) { Write-Host 'Укажи -Query "текст задачи"'; exit 1 }

function B64Vec([string]$b64) {
    $bytes = [Convert]::FromBase64String($b64)
    $n = $bytes.Length / 4
    $v = New-Object single[] $n
    for ($i = 0; $i -lt $n; $i++) { $v[$i] = [BitConverter]::ToSingle($bytes, $i * 4) }
    return $v
}
$sw = [Diagnostics.Stopwatch]::StartNew()
$recs = @(Get-Content $idx -Encoding utf8 | Where-Object { $_.Trim() } | ForEach-Object { $_ | ConvertFrom-Json })
# нормы документов (для косинуса)
$dvecs = New-Object 'System.Collections.Generic.List[object]'
foreach ($r in $recs) {
    $v = B64Vec $r.vec
    $nrm = 0.0; foreach ($x in $v) { $nrm += $x * $x }
    [void]$dvecs.Add([pscustomobject]@{ path = $r.path; part = $r.part; head = $r.head; vec = $v; nrm = [math]::Sqrt($nrm) })
}
$loadMs = [math]::Round($sw.Elapsed.TotalMilliseconds, 0)

$pref = if ($NoPrefix) { '' } else { 'search_query: ' }
$inputs = @($Query | ForEach-Object { $pref + $_ })
$body = @{ model = $Model; input = $inputs } | ConvertTo-Json -Depth 4 -Compress
$w = Invoke-WebRequest -Uri 'http://localhost:11434/api/embed' -Method Post -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -ContentType 'application/json; charset=utf-8' -TimeoutSec 120 -UseBasicParsing
$qv = ([System.Text.Encoding]::UTF8.GetString($w.RawContentStream.ToArray()) | ConvertFrom-Json).embeddings
$qMs = [math]::Round($sw.Elapsed.TotalMilliseconds, 0) - $loadMs

for ($qi = 0; $qi -lt $Query.Count; $qi++) {
    $q = $qv[$qi]
    $qn = 0.0; foreach ($x in $q) { $qn += $x * $x }
    $qn = [math]::Sqrt($qn)
    $rank = New-Object System.Collections.ArrayList
    foreach ($d in $dvecs) {
        $s = 0.0
        for ($i = 0; $i -lt $d.vec.Length; $i++) { $s += $q[$i] * $d.vec[$i] }
        [void]$rank.Add([pscustomobject]@{ score = [math]::Round($s / ($qn * $d.nrm), 3); path = $d.path; part = $d.part; head = $d.head })
    }
    Write-Host ''
    Write-Host ('ЗАПРОС: ' + $Query[$qi])
    $rank | Sort-Object score -Descending | Select-Object -First $Top | ForEach-Object {
        $p = if ($Full) { $_.path } else { $_.path -replace [regex]::Escape('D:\AI\'), '' }
        Write-Host ('  {0,6}  {1} (часть {2})' -f $_.score, $p, $_.part)
        Write-Host ('          ' + $_.head)
    }
}
Write-Host ''
Write-Host ('чанков в индексе: ' + $dvecs.Count + ' | загрузка ' + $loadMs + ' мс | поиск ' + $qMs + ' мс (модель ' + $Model + ')')