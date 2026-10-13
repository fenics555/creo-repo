# ============================================================================
# demo_embed_skill.ps1 — ДЕМО: семантический поиск по скиллам/инструментам дома
# (что даёт nomic-embed-text: 768-мерные векторы -> поиск ПО СМЫСЛУ, а не по словам)
# Запуск: powershell -NoProfile -ExecutionPolicy Bypass -File demo_embed_skill.ps1 [-Top 3]
# ============================================================================
param([int]$Top = 3)
$ErrorActionPreference = 'Stop'
$uri = 'http://localhost:11434/api/embed'

function Emb([string[]]$texts) {
    $body = @{ model = 'nomic-embed-text:latest'; input = $texts } | ConvertTo-Json -Depth 4
    $wr = Invoke-WebRequest -Uri $uri -Method Post -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) `
          -ContentType 'application/json; charset=utf-8' -TimeoutSec 120 -UseBasicParsing
    $r = [System.Text.Encoding]::UTF8.GetString($wr.RawContentStream.ToArray()) | ConvertFrom-Json
    return $r.embeddings
}
function Cos($a, $b) {
    $s = 0.0; $na = 0.0; $nb = 0.0
    for ($i = 0; $i -lt $a.Count; $i++) { $s += $a[$i]*$b[$i]; $na += $a[$i]*$a[$i]; $nb += $b[$i]*$b[$i] }
    return $s / ([math]::Sqrt($na) * [math]::Sqrt($nb))
}

# кандидаты: скиллы дома (суть шапки) + инструменты дома
$cand = @(
    @{ name = 'SKILL_parallel_legs.md';                          text = 'правила git-коммитов, совместная работа ног, чужой staged не трогать' }
    @{ name = 'AUDIT\SKILL_audit_program.md';                    text = 'аудит программы: лишние файлы и настройки, проверка чистоты' }
    @{ name = 'Prog\SKILL_settings_audit.md';                    text = 'аудит настроек дома: config, куда пишет и откуда читает программа' }
    @{ name = 'Creo\CREOSON\SKILL_creoson_rename_mechanism.md';   text = 'механизм переименования модели в Creo через CREOSON file:rename, onlysession' }
    @{ name = 'Creo\SKILL_creo_index.md';                        text = 'карта скиллов направления Creo: вход темы' }
    @{ name = 'SKILL_anti_hallucination.md';                     text = 'запрет выдумок: источник факта, презумпция существования' }
    @{ name = 'SKILL_index.md';                                  text = 'карта всех скиллов репо: где что лежит и куда смотреть' }
    @{ name = 'tools\agent\log_clean.py';                        text = 'инструмент дома: очистка старых логов' }
    @{ name = 'tools\agent\orphan_scan.py';                      text = 'инструмент дома: поиск осиротевших файлов' }
    @{ name = 'Prog\SKILL_python_standard.md';                   text = 'стандарт python-кода дома' }
    @{ name = 'PDF\SKILL_pdf_control.md';                        text = 'работа с PDF: заполненные формы, контроль версий' }
    @{ name = 'OLAMA\SKILL_ollama_index.md';                     text = 'Ollama: раннер, num_predict, локальные модели' }
)
$tasks = @(
    'Рабочая директория: D:\AI\PROBA. Переименуй модель PROBA\models\00080-03.prt в 00080-04.prt ТАК, КАК ЭТО ПРИНЯТО В ДОМЕ: сначала выясни ПРАВИЛА дома и найди ИНСТРУМЕНТ/механизм дома, которым это делается, и только потом выполняй.'
    'Рабочая директория: D:\AI\PROBA. Сделай коммит своих изменений в репозитории D:\AI\repo ТАК, КАК ЭТО ПРИНЯТО В ДОМЕ: сначала выясни ПРАВИЛА коммитов и совместной работы ног, и ИНСТРУМЕНТ дома для работы с репозиторием, потом выполняй.'
    'Рабочая директория: D:\AI\PROBA. Проверь папку PROBA\trash ПО ПРАВИЛАМ ДОМА: сначала выясни ПРАВИЛА аудита и чистки и найди ИНСТРУМЕНТ дома, который этим занимается (реестр D:\AI\tools\agent), затем проверь.'
)

# ВАЖНЫЙ ЗАМЕР (13.10.2026): без префиксов `search_document:`/`search_query:` качество рушится —
# все cosine 0.74–0.77 и топ случайный (Creo-задача НЕ выводила CREOSON-скилл). С префиксами — 3/3 в топ-1.
$qShort = @(
    'search_query: переименовать модель в Creo по правилам дома'
    'search_query: сделать коммит в репозиторий, правила работы ног'
    'search_query: аудит: лишние файлы и настройки в папке'
)
$sw = [Diagnostics.Stopwatch]::StartNew()
$candVec = Emb ($cand | ForEach-Object { 'search_document: ' + $_.text })
$sw.Stop(); Write-Host ('кандидатов: ' + $cand.Count + ' | время ' + [math]::Round($sw.Elapsed.TotalSeconds,1) + ' с (первый вызов = загрузка модели)')
$sw.Restart()
$taskVec = Emb $qShort
$sw.Stop(); Write-Host ('запросов (сокращённая суть задачи): ' + $qShort.Count + ' | время ' + [math]::Round($sw.Elapsed.TotalSeconds,1) + ' с')

for ($i = 0; $i -lt $qShort.Count; $i++) {
    $rank = @()
    for ($j = 0; $j -lt $cand.Count; $j++) { $rank += [pscustomobject]@{ name = $cand[$j].name; score = [math]::Round((Cos $taskVec[$i] $candVec[$j]), 3) } }
    Write-Host ''
    Write-Host ('ЗАПРОС ' + ($i+1) + ': ' + ($qShort[$i] -replace 'search_query: ', ''))
    $rank | Sort-Object score -Descending | Select-Object -First $Top | ForEach-Object { Write-Host ('   ' + $_.score + '  ' + $_.name) }
}
