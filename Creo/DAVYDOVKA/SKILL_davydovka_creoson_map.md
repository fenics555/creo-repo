---
name: davydovka_creoson_map
system: Creo
description: Use when: перенос операций Давыдовки (переименование, копия сборки, семейства, граф) на CREOSON
when: Давыдовка, копия сборки, семейства, граф, перенос, bom, familytable, drawing, manufacturing
priority: high
---
# Давыдовка (CreoJS) → CREOSON: карта операций с живыми вердиктами (16.09.2026)

Давыдовка — веб-приложение в встроенном браузере Creo (Creo.JS + свой python-сервер на 8000).
Дом работает через CREOSON (JSON поверх JLINK, 127.0.0.1:8080/creoson). Проверено живьём:

| Операция Давыдовки (CreoJS) | Аналог в CREOSON | Вердикт |
|---|---|---|
| `assembly.ListItems(ITEM_FEATURE)` + `feature.Id` + `pfcCreateComponentPath` | **`bom:get_paths {file, skeletons, paths}`** → BomChild `{file, seq_path, path[], children[]}` | ✅ полный эквивалент: `path` = feature-id компонента |
| `GetParam` / чтение параметров | `parameter:list {file}` → `paramlist[name,type,value,designate]` | ✅ |
| `ListRows()` / вложенные семейства / `GetImmediateGenericInfo` | `file:has_instances`, **`file:list_instances`** (отдаёт `generic`, `files`, `dirname`), **`familytable:list_tree`** (иерархия с `total`), `familytable:get_parents` | ✅; у не найденного в путях поиска файла `list_instances` вернул `null` |
| Связь «чертёж → модель» | **`drawing:list_models {drawing}`** → `{files:[...]}` | ✅ (чертёж должен быть открыт в сессии) |
| `Rename()` в сессии + `Save()` | **`file:rename {onlysession:true}` → `file:save`** | ✅ (см. Creo/CREOSON/SKILL_creoson_rename_mechanism.md) |
| `Backup(descriptor)` по каждому файлу | `file:backup {file, target_dir}` (оба обязательны) | ✅ проба 22.09.2026 (полигон): `error:false`, в `target_dir` лёг `23-1017gri-01r.prt.1` |
| `Copy()` модели/семейства с новым именем | ОС-копия версий + `file:open/regenerate/save/erase`; дерево — `familytable:list_tree` | ✅ реализовано: Creo/COPY/SKILL_copy_assembly_project.md (умная копия проекта) + `agent/copy_tools.py` |
| Экспорт JPEG для отчётов (`ExportRasterImage`) | `interface:export_image` | ✅ проба 22.09.2026: `{file,type:"JPEG",filename,height,width}` → `{filename,dirname}`; `filename` БЕЗ пути с `:` (иначе «invalid character: :»); модель должна быть показана (`file:display`) |
| **Мануфактуринг** (`creoRenameManufacturingInfo`, fixture-компоненты) | в каталоге CREOSON **нет ни одной `mfg-*` функции** | ❌ отсутствует: отдельная задача или ручная работа |
| Граф использования файлов, «не используется» | своя база `usage(child,parent,parent_path)` + `bom:get_paths` | ✅ (в доме `usage_tools.py`, `graph_tools.py`) |

## Что уже перенесено в дом
- `agent/rename_tools.py` — переименование (план + исполнение, толькоsession-механизм).
- `agent/copy_tools.py` — копия детали/семейства (ОС-копия + валидация в Creo, `dry_run`).
- `agent/copy/copy_server.py` — сервер страницы «Копия сборки» на 8000 (каркас, эндпоинты как у Давыдовки).
- `agent/excel/excel_export.py`, `excel_import.py` — из Давыдовки.
- Окно: витрина агента → 🧙 МАСТЕР ОПЕРАЦИЙ (копия + переименование).

## Правило переноса
Сначала гейт-проба механики в CREOSON (Creo/CREOSON/SKILL_creoson_probe_method.md), затем код.
Не тащить в дом целые модули Давыдовки: она опирается на CreoJS-вызовы, которых в
агенте нет; переносится МЕХАНИКА (последовательность CREOSON-вызовов), UI собирается заново.

## ИНВЕНТАРЬ КОДА ДАВЫДОВКИ + ЖИВЫЕ ФАКТЫ (22.09.2026)
Источник: `D:\AI\ИЗУЧИТЬ\ДАВЫДОВКА\creoJS\creo_bom_js\`; полный конспект —
`D:\AI\ИЗУЧИТЬ\ДАВЫДОВКА\STUDY_NOTES.md`. Приложение = CreoJS во ВСТРОЕННОМ браузере Creo
плюс локальный python-сервер на порту **8000** (в доме 8000 занят `copy-server`).

| Файл | Байт | Роль |
|---|---|---|
| `creojs.js` = `_creojs.js` | 46 714 | браузерный мост CreoJS (Promise-полифилл + `connector`, сокет-RPC; текст `Connection to Creo session lost`) |
| `index.creojs` | 50 270 | CreoJS-скрипт СПЕЦИФИКАЦИИ (компоненты, параметры, основная надпись, изображения) |
| `index_rename.creojs` | 134 111 | CreoJS-скрипт ПЕРЕИМЕНОВАНИЯ (семейства, mfg, `Rename`→`Save`, backup) |
| `index_report.creojs` | 53 181 | CreoJS-скрипт ОТЧЁТОВ (batch-съёмка окон, фон, конфиг, восстановление сессии) |
| `rename.js` | 312 813 | UI графа ссылок страницы «Переименование» |
| `server.py` | 79 461 | HTTP-сервер 8000, эндпоинты `/api/*` (graph, family-table, copy-workspace, excel, pdf) |
| `excel_export.py` / `excel_import.py` | 26 248 / 5 398 | XLSX-спецификация без внешних зависимостей (zip+xml) |
| `family_table_file.py` | 9 741 | дерево семейств ПРЯМО ИЗ ФАЙЛА модели (секция `FamilyInf`, теги `e3`/`1f`) |
| `python\` / `vendor\` | — | портативный CPython 3.13; Pillow, pypdf, reportlab |

Новое (в скиллах не было):
1. `family_table_file.py` — строки семейств читаются из файла generic БЕЗ сессии Creo и без
   загрузки исполнений (проверено на Pro/E-, Creo 8, Creo 13); дешёвая альтернатива
   `familytable:list_tree`/`file:list_instances`.
2. Паттерн гигиены сессии (`index_report.creojs`): сохранить `originalDirectory` → сменить
   папку/фон/конфиг → снять → ВОССТАНОВИТЬ фон/конфиг → вернуть папку → активировать окно
   (не оставлять сессию инженера в чужом состоянии; ср. правило 16.5, `SKILL_creo_cards.md`).
3. Давыдовка ОДНОсессионная: всё через `pfcGetCurrentSession()`; выбора инстанса Creo и работы
   с несколькими сессиями НЕТ; «batch» = съёмка окон в ТОЙ ЖЕ сессии.
4. Записи о нескольких сессиях, переключении и закрытии Creo — `SKILL_creoson_sessions_workdirs.md`
   (один creoson = один Creo; sessionId — ручка сервера, а не выбор инстанса; `stop_creo` — только
   прицепленный; `kill_creo` запрещён; адресно — `Stop-Process -Id <pid>`).
