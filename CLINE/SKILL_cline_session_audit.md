---
name: cline-session-audit
system: CLINE
description: Внешний подсмотр/аудит хода другой ноги Cline — как читать пошаговую историю сессии (`messages.json`), находить нужную сессию, разбирать шаги и ловить петли/угадывания/несоблюдение правил.
when: подсмотр, аудит хода, другая нога, история сессии, messages.json, сессия Cline, что делает модель, петля, угадал, тест модели, промпт на тест, gemma
priority: high
date: 19.11.2026
executor: Cline
---

# ВНЕШНИЙ ПОДСМОТР/АУДИТ ХОДА НОГИ CLINE

**Зачем:** дать модели промпт-тест и наблюдать со стороны, что она делает/думает/гадает/петляет — читая её пошаговую историю. Плюс — аудит уже идущей ноги на соблюдение правил.

## 1. ГДЕ ЛЕЖИТ ИСТОРИЯ (ФАКТ)
- Папки сессий: `%USERPROFILE%\.cline\data\sessions\<session_id>\`
- **Метаданные:** `<session_id>.json` — `provider`, `model`, `started_at`, `status`, `cwd`, `prompt`, `enable_spawn`, `messages_path`.
- **История шагов:** `<session_id>.messages.json` — `messages[]`; каждый шаг: `role`, `content` (список блоков `text` / `tool_use` / `tool_result` / `thinking`), `ts`, `modelInfo`, `metrics`.
- Файлы субагентов лежат рядом: `agent_<uuid>.messages.json` — не путать с сессией.

## 2. НАЙТИ НУЖНУЮ СЕССИЮ (по модели/времени)
```powershell
$root="$env:USERPROFILE\.cline\data\sessions"
Get-ChildItem -LiteralPath $root -Directory | Sort LastWriteTime -Descending | Select -First 6 | ForEach-Object {
  $j = Join-Path $_.FullName ($_.Name + '.json')
  if (Test-Path $j) { $m = Get-Content $j -Raw | ConvertFrom-Json; "$($_.Name) | $($m.model) | $($m.started_at) | $($m.status)" }
}
```

## 3. ПРОЧИТАТЬ ШАГИ
Разобрать `<id>.messages.json` через `ConvertFrom-Json`; печатать `role`, типы блоков (`tool_use` с именем инструмента) и короткий текст. Для компактности — только имена инструментов и превью текста.

## 4. ГРАБЛЯ: КОНСОЛЬ ИСКАЖАЕТ КИРИЛЛИЦУ
В PowerShell русский текст выводится кракозябрами — это **артефакт вывода, а не данных**. **Выгрузить разбор в файл UTF-8 и прочитать его через `read_files`.**

## 5. ЧТО ЛОВИМ (чек-лист аудита хода)
- **Угадывания** (напр. `T_START` «по системной дате» вместо `Get-Date -Format HH:mm:ss`).
- **Петли** — повтор того же запроса/команды (напр. gemma4: «Let's go. Thinking about the Group … files.» по кругу без действий — см. `crash\SKILL_crash_plan-loop-replan-no-exec.md`).
- **Несоблюдение правил**: чтение `Z:` без разрешения; запрос разрешения через `run_commands` вместо обычного текста.
- **Неиспользование субагентов** в режиме `ДИСПЕТЧЕР`.
- Стоимость/темп: `metrics.inputTokens` / `outputTokens`.

## 6. БЕЗОПАСНОСТЬ
Это данные самого Cline (не диск `Z:`), чтение разрешения владельца **не требует**. Секреты из истории не выводить.

## 7. СВЯЗАННЫЕ
- `SKILL_local_agent_cline.md` — выживание, режимы §2, замер окна §8.
- `SKILL_cline_context_mechanism.md` — как Cline грузит правила/скиллы.
