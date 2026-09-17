name: crash_searchcodebase-any-pattern-migration-marker
system: CRASH
description: Use when: search_codebase возвращает маркер миграции
[missing in legacy conversation history] при любом количестве паттернов (1+),
включая точечные запросы
when: search_codebase, migration marker, result missing, any pattern,
index corrupted, tool unstable
date: 17.09.2026
executor: Cline (solar-pro4)
task: спека 57, фаза 1 — добор параметров liteika_hts_mm
СЧЁТЧИК ПОВТОРОВ: 1
ОШИБКА (дословно, для grep):
[migration] Tool result missing in legacy conversation history.
СИМПТОМ: search_codebase с любым количеством паттернов (1, 2, 4) возвращает
маркер миграции вместо результатов поиска; read_files и run_commands (Get-ChildItem,
Findstr) работают стабильно.
ПРИЧИНА:
1. search_codebase на этой машине в текущем состоянии нестабилен: возвращает
маркер миграции вместо результатов при любом запросе.
2. Исполнитель пытался использовать search_codebase какprimary инструмент поиска,
что привело к потере результатов.
ЛЕЧЕНИЕ (проверено):
- Не использовать search_codebase в текущем состоянии.
- Вместо поиска: Get-ChildItem (по конкретным путям/паттернам имён файлов),
read_files (по конкретным путям), Findstr (по конкретным файлам с текстом).
- Если нужен текстовый поиск по содержимому — Findstr /C:"строка" файл,
или чтение конкретного файла через read_files.
ПРОФИЛАКТИКА:
1. В состоянии, когда search_codebase мигрирует — не использовать его.
2. Для поиска имён файлов: Get-ChildItem -Filter, Get-ChildItem -Recurse -Filter.
3. Для поиска текста в файлах: Findstr, или read_files конкретного файла.
4. Если search_codebase внезапно заработал — проверить результат одним паттерном,
прежде чем массово.