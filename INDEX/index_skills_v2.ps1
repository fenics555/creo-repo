# ============================================================================
# index_skills.ps1 v2 — ИНКРЕМЕНТАЛЬНАЯ ИНДЕКСАЦИЯ СКИЛЛОВ/ИНСТРУМЕНТОВ (сменяемые версии)
# ============================================================================
# ПРАВИЛА (владелец, 13.10.2026):
#  1) ПОВТОРНОЕ СКАНИРОВАНИЕ читает только ИЗМЕНЁННЫЕ файлы (сверка size+mtime по манифесту;
#     неизменённые чанки ПЕРЕИСПОЛЬЗУЮТСЯ вместе с их векторами — не читаем и не считаем заново);
#  2) ПИШЕМ НЕ В ЖИВУЮ БАЗУ: сборка идёт в index\staging_<дата>\, живой индекс не трогается до успеха;
#  3) БАЗЫ СМЕНЯЕМЫЕ: версии в index\versions\ver_<дата>\ + указатель index\CURRENT.txt;
#     переключение = запись указателя (откат = указать прежнюю версию); старые версии чистятся (-KeepVersions);
#  4) остальное по канону: префиксы search_document/search_query, контекст в чанке (файл+шапка),
#     ограничение гигантов (-MaxParts), лог с датой, прогресс с оценкой времени.
# ЗАПУСК: powershell -NoProfile -ExecutionPolicy Bypass -File index_skills.ps1 [-Full] [-KeepVersions 3]
# ВЫХОД: index\versions\ver_<дата>\{skills_index.jsonl, manifest.jsonl, meta.txt}, index\CURRENT.txt
# ============================================================================
param(
    [string]$Model = 'nomic-embed-text-v2-moe:latest',
    [int]$MaxChars = 800, [int]$Overlap = 150, [int]$Batch = 32, [int]$MaxParts = 30,
    [int]$KeepVersions = 3,
    [switch]$Full
)
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = 'Stop'
$root   = 'D:\AI\repo\INDEX'
$idxDir = Join-Path $root 'index'
$versDir = Join-Path $idxDir 'versions'
$stamp  = Get-Date -Format 'yyyy-MM-dd_HHmmss'
$stage  = Join-Path $idxDir ("staging_" + $stamp)
$curPtr = Join-Path $idxDir 'CURRENT.txt'
$log    = Join-Path $root ("log\index_" + $stamp + ".log")
foreach ($d in @($idxDir, $versDir, (Join-Path $root 'log'), $stage)) { if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d -Force | Out-Null } }
function L($m) { $line = '[' + (Get-Date -Format 'HH:mm:ss') + '] ' + $m; $line | Out-File $log -Append -Encoding utf8; Write-Host $line }
L ('СТАРТ: stage=' + (Split-Path $stage -Leaf) + ' | модель=' + $Model + ' | Full=' + [bool]$Full)
# --- 1) корпус: скиллы/законы/карты репо + инструменты дома + md настроек ---
$files = New-Object System.Collections.ArrayList
foreach ($f in (Get-ChildItem 'D:\AI\repo' -Recurse -File -ErrorAction SilentlyContinue)) {
    if ($f.Extension -ne '.md' -and $f.Name -notlike '.clinerules*') { continue }
    if ($f.Name -like 'SKILL_*' -or $f.Name -like '.clinerules*' -or $f.Name -match '^(MANIFEST|README|_INDEX)\b' -or $f.Name -match 'index\.md$') { [void]$files.Add($f) }
}
foreach ($f in (Get-ChildItem 'D:\AI\tools\agent' -Recurse -File -ErrorAction SilentlyContinue)) {
    if ($f.Extension -in @('.py', '.md') -and $f.FullName -notmatch '\\data\\|\\__pycache__\\') { [void]$files.Add($f) }
}
foreach ($f in (Get-ChildItem 'D:\AI\AGENT_SETTINGS' -File -ErrorAction SilentlyContinue)) {
    if ($f.Extension -eq '.md' -or $f.Name -like '.clinerules*') { [void]$files.Add($f) }
}
# живой закон дома лежит в корне D:\AI (напр. D:\AI\.clinerules) — тоже индексируем
foreach ($f in (Get-ChildItem 'D:\AI' -File -ErrorAction SilentlyContinue)) {
    if ($f.Name -like '.clinerules*' -or $f.Extension -eq '.md') { [void]$files.Add($f) }
}
# ИСКЛЮЧЕНИЕ шума: архивные копии repo\data\backup\ (старые .clinerules/SKILL = ~118 чанков)
$files = @($files | Where-Object { $_.FullName -notmatch '\\data\\backup\\' })
L ('файлов в корпусе: ' + $files.Count + ' | MaxChars=' + $MaxChars + ' Overlap=' + $Overlap + ' MaxParts=' + $MaxParts)

# --- 2) предыдущая версия (для инкремента): манифест + чанки по файлам ---
$curVer = ''; $curDir = ''
if (Test-Path $curPtr) { $curVer = (Get-Content $curPtr -Raw -Encoding utf8).Trim() }
if ($curVer) { $curDir = Join-Path $versDir $curVer }
$oldManifest = @{}
$oldByPath   = @{}     # path -> List[record]
if ((-not $Full) -and $curDir -and (Test-Path (Join-Path $curDir 'manifest.jsonl'))) {
    foreach ($ln in (Get-Content (Join-Path $curDir 'manifest.jsonl') -Encoding utf8)) {
        if (-not $ln.Trim()) { continue }
        $m = $ln | ConvertFrom-Json
        $oldManifest[$m.path] = $m
    }
    foreach ($ln in (Get-Content (Join-Path $curDir 'skills_index.jsonl') -Encoding utf8)) {
        if (-not $ln.Trim()) { continue }
        $r = $ln | ConvertFrom-Json
        if (-not $oldByPath.ContainsKey($r.path)) { $oldByPath[$r.path] = New-Object System.Collections.ArrayList }
        [void]$oldByPath[$r.path].Add($r)
    }
    L ('инкремент от версии ' + $curVer + ': файлов=' + $oldManifest.Count + ', чанков=' + ($oldByPath.Values | ForEach-Object { $_.Count } | Measure-Object -Sum).Sum)
} else { L 'инкремент выключен (нет прошлой версии или -Full) — полная сборка' }

# --- 3) обходим файлы: неизменённые — переиспользуем, изменённые — режем заново ---
function Get-Emb([string[]]$texts) {
    $body = @{ model = $Model; input = $texts } | ConvertTo-Json -Depth 4 -Compress
    $wr = Invoke-WebRequest -Uri 'http://localhost:11434/api/embed' -Method Post -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) `
          -ContentType 'application/json; charset=utf-8' -TimeoutSec 600 -UseBasicParsing
    return ([System.Text.Encoding]::UTF8.GetString($wr.RawContentStream.ToArray()) | ConvertFrom-Json).embeddings
}
function VecB64($v) {
    $b = New-Object byte[] ($v.Count * 4)
    for ($i = 0; $i -lt $v.Count; $i++) { [BitConverter]::GetBytes([single]$v[$i]).CopyTo($b, $i * 4) }
    return [Convert]::ToBase64String($b)
}
$recs     = New-Object System.Collections.ArrayList   # готовые записи (повторы + новые)
$manifest = New-Object System.Collections.ArrayList
$todo     = New-Object System.Collections.ArrayList   # тексты на эмбеддинг (только изменённое)
$todoInfo = New-Object System.Collections.ArrayList
$reusedFiles = 0; $changedFiles = 0; $reusedChunks = 0
$sw = [Diagnostics.Stopwatch]::StartNew()
foreach ($f in $files) {
    $len = $f.Length; $mt = $f.LastWriteTimeUtc.Ticks
    $old = $oldManifest[$f.FullName]
    if ($old -and $old.len -eq $len -and $old.mtime -eq $mt -and $oldByPath.ContainsKey($f.FullName)) {
        $reusedFiles++
        foreach ($r in $oldByPath[$f.FullName]) { [void]$recs.Add($r); $reusedChunks++ }
        [void]$manifest.Add([pscustomobject]@{ path = $f.FullName; len = $len; mtime = $mt; chunks = $oldByPath[$f.FullName].Count })
        continue
    }
    # изменённый/новый файл: читаем и режем (контекст: файл + шапка)
    $changedFiles++
    $txt = Get-Content $f.FullName -Raw -Encoding utf8 -ErrorAction SilentlyContinue
    if (-not $txt -or $txt.Trim().Length -lt 40) { continue }
    $txt = $txt -replace "`r", ''
    $fm = ''
    foreach ($ln in ($txt -split "`n" | Select-Object -First 40)) {
        if ($ln -match '^\s*(name|description|when)\s*:\s*(.+)$') { $fm += ' ' + $matches[1] + '=' + $matches[2].Trim() }
    }
    $rel = $f.FullName -replace [regex]::Escape('D:\AI\'), ''
    $ctx = '[файл ' + $rel + ']' + $(if ($fm.Trim()) { ' [' + $fm.Trim() + ']' } else { '' }) + ' :: '
    $pos = 0; $part = 0; $cnt = 0
    while ($pos -lt $txt.Length -and $part -lt $MaxParts) {
        $l = [Math]::Min($MaxChars, $txt.Length - $pos)
        $piece = $txt.Substring($pos, $l)
        if ($piece.Trim().Length -ge 40) {
            [void]$todo.Add('search_document: ' + $ctx + $piece)
            [void]$todoInfo.Add([pscustomobject]@{ path = $f.FullName; part = $part; head = ($piece -replace '\s+', ' ').Trim() })
            $cnt++
        }
        $part++
        if ($pos + $l -ge $txt.Length) { break }
        $pos = $pos + $l - $Overlap
    }
    [void]$manifest.Add([pscustomobject]@{ path = $f.FullName; len = $len; mtime = $mt; chunks = $cnt })
}
L ('разбор: переиспользовано файлов ' + $reusedFiles + ' (чанков ' + $reusedChunks + '), изменённых ' + $changedFiles + ' -> на эмбеддинг ' + $todo.Count)
# --- 4) эмбеддинги только для изменённого (пачками) ---
$embSec = 0
if ($todo.Count) {
    $sw2 = [Diagnostics.Stopwatch]::StartNew()
    for ($i = 0; $i -lt $todo.Count; $i += $Batch) {
        $grp = @($todo[$i..([Math]::Min($i + $Batch - 1, $todo.Count - 1))])
        try { $vecs = Get-Emb $grp } catch { L ('ошибка пачки ' + $i + ': ' + $_.Exception.Message); continue }
        for ($k = 0; $k -lt $grp.Count; $k++) {
            [void]$recs.Add([pscustomobject]@{ path = $todoInfo[$i + $k].path; part = $todoInfo[$i + $k].part; head = $todoInfo[$i + $k].head; vec = (VecB64 $vecs[$k]) })
        }
        if ((($i + $grp.Count) % 320) -lt $Batch) {
            $el = $sw2.Elapsed.TotalSeconds
            $avg = $el / ($i + $grp.Count)
            L ('эмбеддинг: ' + ($i + $grp.Count) + ' из ' + $todo.Count + ' | прошло ' + [math]::Round($el, 0) + ' с | ОСТАЛОСЬ ~' + [math]::Round(($avg * ($todo.Count - $i - $grp.Count)), 0) + ' с')
        }
    }
    $sw2.Stop(); $embSec = [math]::Round($sw2.Elapsed.TotalSeconds, 1)
} else { L 'изменённых файлов нет — эмбеддинг не нужен (переиспользован прошлый индекс)' }

# --- 5) пишем в STAGING (живая база не тронута) ---
$ixStage  = Join-Path $stage 'skills_index.jsonl'
$manStage = Join-Path $stage 'manifest.jsonl'
foreach ($r in $recs) { ($r | ConvertTo-Json -Compress) | Out-File $ixStage -Append -Encoding utf8 }
foreach ($m in $manifest) { ($m | ConvertTo-Json -Compress) | Out-File $manStage -Append -Encoding utf8 }
$meta = @(
    'ИНДЕКС СКИЛЛОВ И ИНСТРУМЕНТОВ ДОМА (v2, сменяемые версии)'
    ('дата: ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))
    ('модель: ' + $Model)
    ('файлов: ' + $files.Count + ' (переиспользовано ' + $reusedFiles + ', изменённых ' + $changedFiles + ')')
    ('чанков: ' + $recs.Count + ' (переиспользовано ' + $reusedChunks + ', новых ' + $todo.Count + ')')
    ('параметры: MaxChars=' + $MaxChars + ' Overlap=' + $Overlap + ' Batch=' + $Batch + ' MaxParts=' + $MaxParts)
    'префиксы: "search_document: " индексация / "search_query: " поиск (обязательно)'
    ('предыдущая версия: ' + $(if ($curVer) { $curVer } else { 'нет' }) + $(if ($Full) { ' (ключач -Full)' } else { '' }))
    ('время: разбор+сборка ' + [math]::Round($sw.Elapsed.TotalSeconds, 1) + ' с, эмбеддинг ' + $embSec + ' с')
) -join "`r`n"
$meta | Out-File (Join-Path $stage 'meta.txt') -Encoding utf8

# --- 6) публикация: staging -> versions\ver_<дата>, затем УКАЗАТЕЛЬ (смена базы) ---
$verName = 'ver_' + $stamp
Move-Item $stage (Join-Path $versDir $verName) -Force
$verName | Out-File $curPtr -Encoding utf8
L ('ОПУБЛИКОВАНО: ' + $verName + ' | CURRENT.txt -> ' + $verName + ' (живой индекс сменён)')

# --- 7) чистка старых версий (без мусора) ---
$old = @(Get-ChildItem $versDir -Directory | Sort-Object LastWriteTime -Descending | Select-Object -Skip $KeepVersions)
foreach ($v in $old) { Remove-Item $v.FullName -Recurse -Force -ErrorAction SilentlyContinue; L ('удалена старая версия: ' + $v.Name) }
$allV = @(Get-ChildItem $versDir -Directory | ForEach-Object { $_.Name })
L ('ИТОГО: чанков=' + $recs.Count + ' | файл ' + [math]::Round((Get-Item (Join-Path $versDir "$verName\skills_index.jsonl")).Length / 1MB, 2) + ' МБ | версий на диске: ' + $allV.Count + ' (' + ($allV -join ', ') + ')')

