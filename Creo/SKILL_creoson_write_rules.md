---
name: creoson_write_rules
system: Creo
description: Use when: пишущие операции через CREOSON (backup, rename, копия моделей)
when: creoson, backup, rename, копия, async
priority: critical
---
# CREOSON: пишущие операции (async-мост)
1. backup: только с "target_dir". Без него ошибка параметра.
2. rename: file:rename в async НЕ работает (General Error). Файлы — ОС-rename;
   сессионное переименование — только через синхронный CreoJS (J-link в Creo).
3. Копия модели: backup(target_dir=temp) → creo:cd temp → file:open →
   parameter/set, relations_set, regenerate → file:save → file:erase →
   ОС-rename/перенос файлов → creo:cd обратно.
4. Полный тест (creoson_full_test) считается ПРОЙДЕН только при всех OK;
   «предупреждений» в вердикте не бывает.
См. также: Ошибки/ERR_creoson_write_ops.md
