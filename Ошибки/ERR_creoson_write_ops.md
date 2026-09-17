---
name: err-creoson-write-ops
system: CRASH
description: Use when: пишущая операция CREOSON упала — backup без target_dir, rename General Error
when: backup, target_dir, rename, General Error, CREOSON, запись, async
priority: high
---
# ERR_creoson_write_ops — пишущие операции CREOSON в async-соединении
СТАТУС: ПРАВИЛО (не повторять). Выявлено 01.09.2026 полным тестом.

## backup
file:backup БЕЗ параметра target_dir → «No 'target_dir' parameter given».
ПРАВИЛЬНО: {"file": <имя>, "target_dir": <путь>}. (dirname — НЕ параметр backup.)

## rename
УТОЧНЕНО 16.09.2026 живой пробой в чистой сессии: падает ДИСКОВЫЙ вызов
file:rename {file,new_name} → «A Pro/TOOLKIT error has occurred: General Error»,
и вызов с параметром rename_dependencies (такого параметра в CREOSON НЕТ).
РАБОТАЕТ сессионный: file:rename {file, new_name, onlysession:true} — ссылки в
сборках-владельцах переключаются в памяти, диск не тронут; затем file:save пишет
файл ПОД НОВЫМ ИМЕНЕМ (старая версия остаётся — уводить в backup, не удалять).
Это и есть схема Давыдовки, воспроизведённая чистым CREOSON (без CreoJS).
Для копии: backup(target_dir) → cd → open → правки → regenerate → save → erase → ОС-перенос.
Подробности и ловушки: Creo/SKILL_creoson_rename_mechanism.md.

## open после backup
open видит файл только если backup прошёл и сделан cd в ту же папку.
Проверять оба шага, иначе каскад «was not open / could not open».

## вердикты
Тест ПРОЙДЕН только если ВСЕ шаги OK. «Предупреждение» = НЕ ПРОЙДЕН.
