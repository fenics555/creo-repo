# ERR_creoson_write_ops — пишущие операции CREOSON в async-соединении
СТАТУС: ПРАВИЛО (не повторять). Выявлено 01.09.2026 полным тестом.

## backup
file:backup БЕЗ параметра target_dir → «No 'target_dir' parameter given».
ПРАВИЛЬНО: {"file": <имя>, "target_dir": <путь>}. (dirname — НЕ параметр backup.)

## rename
file:rename в async CREOSON → Pro/TOOLKIT General Error. НЕ РАБОТАТ в принципе.
ПРАВИЛЬНО: переименовывать файлы на уровне ОС (os.rename по версиям .prt.N)
либо через синхронную сессию CreoJS (схема Давыдовки: rename в сессии + save).
Для копии: backup(target_dir) → cd → open → правки → save → erase → ОС-rename.

## open после backup
open видит файл только если backup прошёл и сделан cd в ту же папку.
Проверять оба шага, иначе каскад «was not open / could not open».

## вердикты
Тест ПРОЙДЕН только если ВСЕ шаги OK. «Предупреждение» = НЕ ПРОЙДЕН.
