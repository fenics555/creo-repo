---
name: crash_ollama-ansi-stderr-falseexit
system: CRASH
description: Use when: команда ollama (stop/rm/create/ps) печатает ANSI-спиннер в stderr — PowerShell даёт ложный NativeCommandError/exit1 и рвёт цепочку команд через «;», хотя команда выполнена
when: ollama, ANSI, stderr, NativeCommandError, exit1, semicolon, обёртка, spinner
date: 01.10.2026
executor: Cline
task: правки П1-П6 по итогам прогона loop_revive (01.10.2026)
---

ОШИБКА (дословно, для grep):
NativeCommandError / «command exited with code 1» при `ollama stop|rm|create`, хотя вывод содержит
ожидаемый результат (например `deleted 'gpt-oss:20b'`), а последующие команды цепочки `;` не выполняются.
СИМПТОМ: PowerShell прерывает цепочку `cmd1; cmd2; cmd3` после «ошибочной» команды ollama; сам ollama
отработал успешно (проверяется отдельным вызовом или `ollama list`). Ошибка повторяется только в
PowerShell/VS Code терминале, в `cmd`-скриптах и через HTTP API (/api/generate) её нет.
ПРИЧИНА: интерактивные команды ollama печатают ANSI-управляющие последовательности (спиннер) в stderr;
PowerShell 5+ переводит любой вывод native-команды в stderr в поток ошибок и при включённом
`$ErrorActionPreference`/логировании поднимает NativeCommandError, что даёт ложный exit1.
ПРОФИЛАКТИКА:
1. Не судить об успехе `ollama stop|rm|create|ps` по exit-коду PowerShell — проверять фактический результат:
   `ollama list`, наличие тега, `ollama show <model> --modelfile`.
2. Вызывать такие команды одной строкой без цепочки `;` либо оборачивать: `cmd /c "ollama stop <m> >nul 2>&1"`.
3. Для выгрузки модели в стендах использовать HTTP `POST /api/generate {"model": m, "keep_alive": 0}` —
   stderr не участвует, ложного exit1 нет (так уже сделано в checks\loop_revive_test.py: unload()).
4. Не повторять ту же команду «добить exit0» — это вторая попытка того же хода; сменить метод.
5. Обёртка, если нужна системно: `ollama_quiet.bat` с `>nul 2>&1` и `exit /b %errorlevel%` (долг, файла нет).
ПОВТОРЫ: 1

СВЯЗЬ: rules_enforce П6 (REPORT_loop_revive_cline_2026-10-01.md, строки 165-166).