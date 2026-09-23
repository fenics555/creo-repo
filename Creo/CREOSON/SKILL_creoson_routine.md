---
name: creoson-routine
system: Creo
description: Use when: автоматизация рутины в Creo через CREOSON — практический разбор (зачем, стек, жизненный цикл, группы команд, типовые сценарии, грабли)
when: creoson, рутина, автоматизация, без программирования, сценарий, стек, функции, группы команд, 199
priority: critical
date: 22.09.2026
---
# CREOSON ДЛЯ РУТИНЫ — ПОЛНЫЙ ПРАКТИЧЕСКИЙ РАЗБОР
Спутники: `SKILL_creoson_complete.md` (карта API), `SKILL_creoson_workflow.md` (цикл и переключение).

## 1. Зачем CREOSON (позиционирование)
- **Просто и дёшево**: JSON по HTTP к локальному серверу — **без программирования** (скрипт/агент на любом языке, чаще Python).
- Полный доступ к модели через JLINK, но **без сборки Java/C++** (в отличие от прямого JLINK/OTK).
- Идеален для **рутины**: аудит папок, копия/переименование проектов, PDF чертежей, параметры/отношения, семейства, массовые характеристики.
- Не для: сложных сборок с нуля, правки 3D-геометрии, Simulate, записи в Windchill (см. `SKILL_creoson_complete.md`).

## 2. Архитектура и стек дома
`HTTP POST JSON` → **CREOSON** (JVM) → **JLINK** → **Creo Parametric**.
- Порт дома **8080** (эндпоинты `/creoson` и `/server`); версия **3.0.2**, JRE **Java 25**
  (`D:\AI\Java`, Temurin) — штатный для Creo 13 (см. RELEASE_NOTES creoson).
- Каталог: `D:\PTC\CREO-LOCAL-SETUP\creoson` (`creoson_run.bat`, `setvars.bat`, jars); подъём —
  `python D:\AI\tools\agent\ctl.py up` (только недостающее).
- `creoson_run.bat`: читает `setvars.bat` (`PROE_COMMON`, `PROE_ENV=x86e_win64`, `JAVA_HOME`, `JSON_PORT`),
  ставит `PRO_COMM_MSG_EXE`, добавляет `%PROE_COMMON%\%PROE_ENV%\{lib,obj}` в `PATH`, собирает
  classpath из локальных jar + `%PROE_COMMON%\text\java\pfcasync.jar`, стартует
  `com.simplifiedlogic.nitro.jshell.MainServer` на `JSON_PORT`.

## 3. Полный каталог команд (18 групп, 199 функций — из `jsonSpecs`)
| Группа | Функций | Назначение |
|---|---|---|
| `bom` | 1 | дерево сборки (`get_paths`) |
| `connection` | 6 | `connect`/`disconnect`, `is_creo_running`, `start_creo`/`stop_creo`/`kill_creo` |
| `creo` | 12 | `pwd`/`cd`, `list_files`/`list_dirs`, `get_config`/`set_config`, `mkdir`/`rmdir`/`delete_files`, `set_creo_version` |
| `dimension` | 7 | размеры: чтение/правка |
| `drawing` | 36 | чертежи: создание, модели, виды, листы, таблицы, регенерация |
| `familytable` | 13 | семейства: `list`/`list_tree`/`exists`/`get_parents`, `add_inst`/`replace`/`set_cell`/`delete_inst` |
| `feature` | 13 | элементы: `list`/`suppress`/`resume` |
| `file` | 42 | главная: `open`/`save`/`rename`/`backup`/`erase`, `relations_get/set`, `massprops`, точность/единицы, упрощённые представления, материалы |
| `geometry` | 3 | геометрия |
| `interface` | 9 | экспорт/импорт: `export_pdf`, `export_image`, `export_file`, `mapkey` |
| `layer` | 4 | слои |
| `note` | 6 | заметки |
| `object` | 23 | объектные/структурные операции |
| `parameter` | 6 | параметры: `list`/`set`/`get` |
| `server` | 1 | `pwd` самого сервера (эндпоинт `/server`) |
| `view` | 4 | виды |
| `windchill` | 12 | Windchill (только чтение) |
| `creosonFunctions` | 1 | служебный список функций |

## 4. Жизненный цикл сессии
1. `connection:connect {}` → `sessionId` (верхний уровень ответа).
2. Каждый запрос: `{sessionId, command, function, data}`.
3. Работа: `creo:pwd` / `creo:cd` / `creo:list_files` → `file:open` → чтение/запись → `file:save`/`file:erase`.
4. `connection:disconnect {}` — закрыть ручку (Creo продолжает работать).

## 5. Типовые рутинные сценарии (готовые последовательности)
- **Аудит папки**: `creo:pwd` → `creo:list_files {"filename":"*"}` → для каждого `.prt/.asm`:
  `file:open {display:false}` → `parameter:list` / `file:massprops` / `file:relations_get` → `file:erase`.
- **Копия проекта**: `bom:get_paths` → `file:backup` в temp → `creo:cd temp` → `file:rename {onlysession:true}`
  → `file:save` снизу вверх → `creo:cd` назад (полностью — `..\COPY\SKILL_copy_assembly_project.md`).
- **Переименование**: `file:rename {file, new_name, onlysession:true}` → `file:save`
  (`SKILL_creoson_rename_mechanism.md`).
- **PDF чертежа**: `interface:export_pdf {file, dirname, use_drawing_settings:true, sheet_range:"all"}`
  (dirname = папка чертежа).
- **Параметры**: `parameter:list {file}` → `parameter:set {file, name, value, type}`.
- **Семейства**: `file:has_instances` / `file:list_instances` / `familytable:list_tree`;
  правка — `familytable:add_inst` / `replace` / `set_cell` / `delete_inst`.
- **Сборка/чертёж**: `bom:get_paths` (дерево), `drawing:list_models` (связь чертёж→модель).

## 6. Грабли (свод; подробно — `SKILL_creoson_workflow.md` §7)
- `file:backup` требует ОТКРЫТУЮ модель; `file:rename` `new_name` — С расширением.
- `file:open` по имени резолвится через остаток сессии/пути поиска → чистая сессия + `dirname`.
- Дисковый `file:rename` (без `onlysession`) — мёртв (`General Error`).
- `interface:export_image`: `filename` без пути с `:`; модель показать.
- Кириллица — только из Python (UTF-8); логи читать `-Encoding UTF8`.
- **Русские имена параметров/папок**: данные ДОЕЗЖАЮТ корректно — проба `ru_params_probe.py`:
  `parameter:list` на `pin_splitk.prt` вернул 47 параметров, **23 с кириллицей**, JSON корректен
  (`НАИМЕНОВАНИЕ="Штифт разрезной"`, `ТИП="Стандарт"`). Боль — только ОТОБРАЖЕНИЕ (консоль cp866 → `???`)
  и PowerShell (`Invoke-RestMethod` искажает пути). Лечение: Python/UTF-8; при нужде — временные
  параметры/файлы-заместители (не подтверждено).
- `familytable:list_tree` на больших семействах висит; 2 Creo = отказ + краш JVM; `kill_creo` запрещён.

## 7. Проверка/приёмка
- Базовые проверки: `connection:is_creo_running`, `creo:pwd`, `file:list`.
- **Спек-истина**: `D:\PTC\CREO-LOCAL-SETUP\creoson\web\functions.html` + `…\jsonSpecs\*.json`
  (199 файлов) + `playground.html` (тестер из браузера); `start.html` (настройка/порт).

## 8. Связь со скиллами
`SKILL_creoson_complete.md` (карта API) · `SKILL_creoson_workflow.md` (цикл/переключение) ·
`SKILL_creoson_rename_mechanism.md` (rename) · `SKILL_creoson_write_rules.md` (пишущие) ·
`SKILL_creoson_probe_method.md` (пробы) · `..\COPY\SKILL_copy_assembly_project.md` (копия) ·
`..\API\SKILL_creo_api_ecosystem.md` (каналы и JLINK) · `..\DOCS\SKILL_creo_docs_map.md` (справки).