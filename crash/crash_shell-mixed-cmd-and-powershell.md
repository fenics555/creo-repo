---
name: crash_shell-mixed-cmd-and-powershell
system: CRASH
description: Use when: PowerShell-командлет (Select-Object и др.) попал внутрь cmd /c — cmd.exe его не знает, код возврата 1 врёт о провале операции
when: cmd /c, Select-Object, PowerShell, cmd.exe, конвейер, ложный exit 1, push
date: 01.10.2026
executor: Cline
task: AGENT_SETTINGS, ~22:48
---

# crash_shell-mixed-cmd-and-powershell — конвейер PowerShell внутри `cmd /c`

ОШИБКА (дословно, для grep):
crash_shell-mixed-cmd-and-powershell: 'Select-Object' is not recognized as an internal or external command, operable program or batch file.

**Подпись:** `'Select-Object' is not recognized as an internal or external command,
operable program or batch file.`

**Симптом (01.10.2026, ~22:48, задача AGENT_SETTINGS):**
```
cmd /c 'cd /d D:\AI\AGENT_SETTINGS && git push origin master 2>&1 | Select-Object -Last 2'
[Command exited with code 1]
[stderr] 'Select-Object' is not recognized as an internal or external command
```
Причина: `cmd /c` — это оболочка **cmd.exe**. Всё, что после `&&` в этой строке, исполняет
**cmd.exe**, а не PowerShell. `Select-Object`, `ForEach-Object`, `Where-Object`, `Get-*`,
`Measure-Object` — командлеты PowerShell, в cmd.exe их нет. Труба `|` в cmd означает
перенаправление в файл, а не конвейер PowerShell.

**Чем опасно:** пуш **не выполнился**, а код возврата 1 выглядит как «пуш упал» — можно
зря искать проблему в git или в сети, или (хуже) повторить пуш вслепую.

**Лечение (смена метода, не повтор):**
1. Внутри `cmd /c` использовать только команды cmd: без конвейеров PowerShell, без `2>&1 |`.
2. Нужен вывод целиком — просто убери `| Select-Object …` (git push и так короткий).
3. Нужна фильтрация в PowerShell — выполняй команду **без** обёртки `cmd /c`, прямо в
   PowerShell (там `cd` = `Set-Location`, а пуши лучше делать через `Set-Location D:\AI\repo; git ...`).
4. Для `cd /d` внутри cmd — `cmd /c 'cd /d D:\AI\... && git ...'` рабочая форма, менять её не надо.

**Профилактика:** одна команда — одна оболочка. Перед вызовом смотри, начинается ли строка
с `cmd /c` — тогда внутри допустимы ТОЛЬКО команды cmd.exe. Проверка на граблях фазы:
push повторён без конвейера и прошёл (`0 0` с обеих сторон).

**Смежные подписи:** `SKILL_crash_sleep-poll-loop-after-timeout` (ожидание детача),
`crash_quoted-escape-parse-failure` (кавычки в PowerShell), `crash_ollama-ansi-stderr-falseexit`
(ложный ненулевой код выхода — сюда же попадает любой «exit 1», который на деле означает лишь
ошибку запуска, а не провал операции).
