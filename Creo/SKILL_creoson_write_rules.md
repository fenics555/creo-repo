---
name: creoson_write_rules
system: Creo
description: Use when: пишущие операции через CREOSON (backup, rename, копия моделей)
when: creoson, backup, rename, копия, async
priority: critical
---
# CREOSON: пишущие операции (async-мост)
1. backup: только с "target_dir" (без него — ошибка параметра) И файл обязан быть ОТКРЫТ
   в сессии, иначе `File '<name>' was not open.` (проба полигона 22.09.2026). Порядок:
   `file:open {display:false}` → `file:backup {file, target_dir}`.
2. rename: дисковый вызов file:rename {file,new_name} в async ПАДАЕТ (Pro/TOOLKIT
   General Error), а параметра rename_dependencies в CREOSON НЕТ вовсе. Рабочий путь —
   сессионный: file:rename {file,new_name,onlysession:true} (ссылки сборок-владельцев
   переключаются в памяти, диск не тронут) → file:save пишет файл ПОД НОВЫМ ИМЕНЕМ;
   старые версии уводить в backup, не удалять. Чертёж и владельцев грузить ДО rename,
   сохранять снизу вверх, чертёж последним. См. Creo/SKILL_creoson_rename_mechanism.md.
3. Копия модели: backup(target_dir=temp) → creo:cd temp → file:open →
   parameter/set, relations_set, regenerate → file:save → file:erase →
   ОС-rename/перенос файлов → creo:cd обратно.
4. Полный тест (creoson_full_test) считается ПРОЙДЕН только при всех OK;
   «предупреждений» в вердикте не бывает.
См. также: Ошибки/ERR_creoson_write_ops.md
Справка CREOSON (истина о функциях и параметрах): D:\PTC\CREO-LOCAL-SETUP\creoson\web\
functions.html + web\assets\creoson_stuff\jsonSpecs\*.json (по файлу на функцию) +
start.html (запуск; порт рекомендован 9056, а 22/80/8080/443 просят избегать) +
playground.html (тестер из браузера). Эндпоинты: POST /creoson и /server.
Механика rename и ловушки: Creo/SKILL_creoson_rename_mechanism.md;
методика безопасных проб: Creo/SKILL_creoson_probe_method.md;
сессии, старт Creo/CREOSON и рабочие директории: Creo/SKILL_creoson_sessions_workdirs.md.


export_pdf — пишущая операция: только через инструмент с approval (pdf_refresh);
после экспорта mtime pdf обновляется и это единственный источник вердикта свежести;
«предупреждений» у перепечати не бывает: либо OK, либо ошибка с причиной.

rename: дисковый file:rename мёртв (General Error в async); сессионный file:rename {file, new_name, onlysession:true} жив; боевой путь = сессионный rename, file:save, ОС-перенос старых версий в backup
Без onlysession — General Error, файлы только ОС-rename.
