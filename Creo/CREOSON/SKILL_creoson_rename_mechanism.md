---
name: creoson_rename_mechanism
system: Creo
description: Use when: переименование модели и чертежа через CREOSON (rename, onlysession, General Error)
when: rename, onlysession, переименование, General Error, чертёж, save, backup, Давыдовка
priority: critical
---
# CREOSON: переименование модели и чертежа — доказанный механизм (16.09.2026)

Живые пробы в чистой сессии на копии в tmp (объект `zkr_rename_test.prt`), CREOSON
3.0.2 + Creo 12.4.2.0 + Temurin 25 (Java 25 — штатный JRE creoson 3.0.2, см. RELEASE_NOTES).

## Что работает, что нет
| Вызов | Результат |
|---|---|
| `file:rename {file, new_name}` (дисковый) | ❌ `A Pro/TOOLKIT error has occurred: General Error. Check your model/drawing for accuracy.` |
| `file:rename {file, new_name, rename_dependencies:true}` | ❌ тот же General Error — **параметра `rename_dependencies` в CREOSON НЕТ** (спека `file-rename.json`) |
| `file:rename {file, new_name, onlysession:true}` | ✅ сессионный rename: ссылки в сборках-владельцах переключаются В ПАМЯТИ, диск не тронут |
| `file:save {new_name}` после onlysession-rename | ✅ на диске появляется файл **ПОД НОВЫМ ИМЕНЕМ** (`zkr_rename_test2.prt.1`), старая версия остаётся |

Вывод: «rename в async не работает» — верно только для дискового вызова. Схема
Давыдовки (`Rename` + `Save` в сессии) полностью воспроизводится чистым CREOSON,
без синхронного CreoJS.

## Рабочий порядок
1. Проверить сессию (`file:list`); чужие модели не выгружать, свои — выгрузить после.
2. Загрузить ДО переименования: модель, её чертёж, **все сборки-владельцы**
   (`file:open {display:false}`). Владельцы — из базы `usage` дома или обходом `bom:get_paths`.
3. `file:rename {file: old.ext, new_name: new, onlysession:true}` — модель.
   Чертёж: `file:rename {file: old.drw, new_name: new, onlysession:true}` → `drawing:regenerate {drawing: new.drw}`.
4. Сохранять **снизу вверх**: модель → сборки-владельцы → чертёж **последним**
   (ERR 2.8: чертёж не был загружен до Rename — ссылка не переключится).
5. Старые версии (`old.ext.N`) не удалять, а уводить в backup-папку.
6. Выгрузить всё, что загружали (`file:erase` по имени).

## Ловушки (проверено живьём)
- `file:save` с НЕСУЩЕСТВУЮЩИМ именем — не ошибка: сохраняется активная модель
  (в пробе так появились версии совсем других файлов). Перед save сверять владельца.
- `file:save` создаёт НОВУЮ версию `name.ext.N`, а не перезаписывает.
- `erase_not_displayed` сессию полностью не чистит: нужен цикл `file:erase` по именам.
- `file:open` по имени, уже загруженному в сессию, отдаёт модель ИЗ ПАМЯТИ (даже если
  в другой папке лежит одноимённый файл) — копии под тем же именем не защищают.
- `file:get_fileinfo` отдаёт путь с удвоенным диском (`"D:D:\..."`).
- `sessionId` — **верхний уровень** запроса (не в `data`), иначе «No session found».
- `creo:set_creo_version {"version":12}` вызывать до пишущих операций (Creo 7+).
- `file:list_files` без параметра `file` листает папку; с `file:"*"` вернул пусто.

## Реализация в доме
- `agent/rename_tools.py`: `build_plan()` (модель + чертёж + владельцы из `usage`),
  `tool_rename_model(old_name, new_name, drawings, parents, dry_run)`, `rename_preview`.
- `agent/creo_ops_tools.py::tool_rename_model` — делегат в `rename_tools` (прежний код
  с `rename_dependencies` был нерабочим).
- Окно: витрина агента → 🧙 МАСТЕР ОПЕРАЦИЙ → блок «ПЕРЕИМЕНОВАНИЕ»:
  «План переименования» (`POST /wiz_rename_preview`) и «Переименовать»
  (`rename_model …` через щит согласования).
