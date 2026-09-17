name: crash_searchcodebase-timeout
system: CRASH
description: Use when: search_codebase зависает/таймаут или возвращает маркер миграции вместо результатов
when: search_codebase, timeout, migration marker, result missing, hang
date: 17.09.2026
executor: Sergio
task: серия спек 57, поиск по репо
ПОВТОРЫ: 1
ОШИБКА (дословно, для grep):
дословная строка исходного экземпляра не сохранилась; маркер серии (из родственных экземпляров):
[migration] Tool result missing in legacy conversation history.
СИМПТОМ: search_codebase зависает или отдаёт маркер миграции/пустоту вместо результатов; read_files и run_commands (Get-ChildItem, Findstr) работают стабильно.
ПРИЧИНА: индекс search_codebase в миграции/нестабилен; повторные вызовы того же хода результата не дают.
ПРОФИЛАКТИКА:
1. В состоянии миграции search_codebase не использовать вовсе (дельта: .clinerules, ПОИСК, «миграция = правки .py дома»).
2. Поиск имён файлов: Get-ChildItem (-Filter / -Recurse); поиск текста: Findstr /c:"строка" файл, read_files по конкретному пути.
3. Один regex = один вызов; маркер миграции в ответе — сменить инструмент, не повторять вызов (М7).
4. Родственные экземпляры с дословными строками и лечения: SKILL_crash_searchcodebase-multipattern-migration-marker.md, SKILL_crash_searchcodebase-any-pattern-migration-marker.md.
