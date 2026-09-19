name: crash_readfiles_outdated_loop
system: CRASH
description: Use when `read_files` returns `[outdated - see the latest file content]` repeatedly in a loop.
when: readfiles, outdated, loop, tool-loop
date: 19.09.2026
executor: Cline
task: Spec 95 (Frontend Pattern Discovery)
ОШИБКА (дословно, для grep):
[outdated - see the latest file content]
СИМПТОМ: Три одинаковых вызова `read_files` с одним и тем же путем возвращают один и тот же статус "outdated" без содержимого.
ПРИЧИНА: Рассинхрон состояния инструмента `read_files` с файловой системой или кэширование "устаревшего" статуса в рамках сессии.
ПРОФИЛАКТИКА:
1. Не повторять один и тот же вызов `read_files` более одного раза, если получен статус "outdated".
2. При получении "outdated" сменить метод: использовать `run_commands` (например, `type` или `Get-Content`) для проверки или `search_codebase` для поиска фрагментов.
3. Если файл критически важен и `read_files` не работает, использовать `editor` с коротким якорем (если удастся прочитать хотя бы часть).
4. При обнаружении петли (3+ вызова) — немедленно остановить и сообщить пользователю.
ПОВТОРЫ: 1
