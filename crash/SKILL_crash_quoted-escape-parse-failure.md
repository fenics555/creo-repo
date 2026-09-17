name: crash_quoted-escape-parse-failure
system: CRASH
description: ParseException «Отсутствует имя типа после знака "["» на \" внутри массива run_commands
when: run_commands, quoted, escape, parse-failure
date: 17.09.2026
executor: Cline
task: спека 60, нога 2
ОШИБКА (дословно, для grep):
ParseException «Отсутствует имя типа после знака "["»
СИМПТОМ: падение при использовании кавычек в run_commands
ПРИЧИНА: неверное экранирование JSON
ПРОФИЛАКТИКА:
1. кавычки без обратных слэшей либо вынос команды в .py или .ps1 файл.
ПОВТОРЫ: 1
