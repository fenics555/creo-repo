---
name: creoson-sessions-workdirs
system: Creo
description: Use when: старт Creo и CREOSON, сессии (сколько их, какую открыл, как переключаться), рабочие директории, поиск файлов/сборок/деталей/чертежей
when: сессия, session, connect, disconnect, старт Creo, start_creo, рабочий каталог, cd, pwd, list_files, list_dirs, рабочие директории
priority: critical
---
# CREOSON: СЕССИИ, СТАРТ И РАБОЧИЕ ДИРЕКТОРИИ (живые пробы 17.09.2026)
Справка-источник: `D:\PTC\CREO-LOCAL-SETUP\creoson\web\functions.html` + `…\jsonSpecs\*.json`.
Пробы выполнены при **двух запущенных Creo** (xtop PID 4488 и 13076) и одном JVM creoson (PID 11660).

## 1. СЕССИИ: что такое sessionId
Живой факт: два вызова `connection:connect` дали **разные** sessionId (`-69625…` и `-22867…`),
но **оба видят один и тот же Creo**: `creo:pwd` одинаков (`D:/AI/ПРОБА/23-1017GRI 2кап…''/`),
`file:list` одинаков (14 моделей). Значит:
- sessionId — это **ручка сессии CREOSON**, а НЕ выбор инстанса Creo;
- один JVM creoson держит JLINK-подключение к **одному** Creo; второй запущенный Creo
  этому серверу недоступен (нужен второй creoson на своём порту);
- `connection:disconnect` убивает ТОЛЬКО свою ручку: после disconnect B `creo:pwd` с B
  → `No session found`, а с A → по-прежнему `error:false`;
- `connection:is_creo_running` — sessionId **опционален и игнорируется** (спека), вернул
  `{"running": true}` без ручки; он же «дотягивается» новым подключением, если связи нет.
- Как понять, к какому Creo прицеплен: сверять `creo:pwd` + `file:list` с ожиданием
  (какая папка, какие модели обязаны быть). Если ожидаемого нет — автоматика смотрит
  в другой инстанс: правило дома «один Creo на машину» (CREO-START поднимает один).

## 2. СТАРТ/СТОП Creo через CREOSON
- `connection:start_creo {start_dir, start_command:"nitro_proe_remote.bat", retries, use_desktop}`
  — запускает ВНЕШНИЙ .bat (имя ограничено списком: `nitro_proe_remote.bat`), затем пытается
  подключиться: пауза 3 с, между попытками 10 с; **если после старта Creo показывает диалог,
  он может упасть — тогда `retries: 0`**; при `use_desktop` в .bat обязателен `cd` в нужную папку.
- `connection:stop_creo` — корректно выйти из подключённого Creo (без подключения — ничего).
- ⚠️ `connection:kill_creo` — убивает `xtop.exe` и `nmsd.exe` **по имени процесса**,
  то есть ВСЕ запущенные Creo. В работе с живой сессией инженера не вызывать.
- Своя обвязка дома: `setvars.bat` (создаёт только CreosonSetup.exe; без него
  `creoson_run.bat` падает «The setvars.bat file does not exist»), `creoson_run.bat`
  собирает classpath из локальных jar + `%PROE_COMMON%\text\java\pfcasync.jar`,
  `JAVA_HOME` = Temurin 25 (creoson 3.0.2 под Creo 13), `JSON_PORT=8080`;
  подъём — `D:\AI\tools\agent\ctl.py up` (только недостающее).

## 3. РАБОЧИЕ ДИРЕКТОРИИ (работа идёт ТОЛЬКО через них)
- `creo:pwd` → текущая рабочая папка Creo (в пробе: `D:/AI/ПРОБА/23-1017GRI 2кап…''/`).
- `creo:cd {dirname}` → сменить рабочую папку (возвращает новый dirname). НЕ перепривязывает
  уже загруженные модели: `file:open` по имени из сессии отдаёт модель ИЗ ПАМЯТИ (факт 16.09).
- `creo:list_dirs {dirname}` → подпапки рабочей папки (в пробе 3: `23-1017GRI-otlivka`,
  `Для литейщиков`, `Сборки`).
- `creo:list_files {filename}` → файлы рабочей папки. **Параметр называется `filename`**
  (не `file`!): без параметра и с `"*"` → 51 файл, с `"*.asm"` → 14 сборок. Вызов `file:"*"`
  даёт ПУСТО — это не «папка пуста», а неверное имя параметра.
- `creo:mkdir`, `creo:rmdir`, `creo:delete_files` — файловые операции (ПИШУЩИЕ, под согласование).
- `server:pwd` — только на эндпоинте **`/server`** (не `/creoson`): рабочая папка самого
  creoson (`D:/PTC/CREO-LOCAL-SETUP/creoson` в пробе), от сессии не зависит.
- Правило дома: модель ищется в рабочей папке и путях поиска (`search_path`), а не по диску;
  всё, что вне рабочей папки, подтягивается копированием (см. SKILL_copy_rename).

## 4. ПОИСК ФАЙЛОВ / СБОРОК / ДЕТАЛЕЙ / ЧЕРТЕЖЕЙ
- По рабочей папке: `creo:list_files {filename:"*маска*"}`. Расширения: `.asm` сборка,
  `.prt` деталь, `.drw` чертёж, `.frm` формат листа, `.lay/.sec` компоновка/сечение.
- В сессии: `file:list` → модели, открытые в Creo; `file:get_fileinfo {file}` → `dirname`
  (откуда загружена — единственный надёжный способ поймать подмену папки) + `revision`;
  `file:exists`, `file:open {file, dirname, display}`.
- Состав и семейства: `bom:get_paths {file, paths, skeletons}`; `file:has_instances`,
  `file:list_instances {file}`, `familytable:list_tree {file}`.
- Чертёж: `drawing:list_models {drawing}` (какая модель связана), `drawing:get_cur_model`.
- Конфиг Creo: `creo:get_config {name}` — живые значения `trail_dir`
  (`D:\PTC\CREO-LOCAL-SETUP\TEMP\trails\`), `start_model_dir` (`…\CREO-START\НАСТРОЙКИ\ШАБЛОНЫ\`),
  `pro_group_dir`, `last_session_directory_path`; несуществующий ключ → `values: []` без ошибки.
- Дом: индекс `models`/`files` (инструменты `models_find`, `models_where`), реестр PDF-пар
  `/pdfregistry` (вердикты «актуален / устарел / нет pdf» — не изобретать заново).

## 5. ТО ЖЕ ЧЕРЕЗ РОДНОЕ API (Creo.JS) — для сверки
- Сессия и папки: `pfcGetCurrentSession()`, `session.GetCurrentDirectory()`,
  `session.ChangeDirectory(dir)`, `session.GetModelFromFileName(name)`,
  `session.RetrieveModel(descriptor)`, `session.EraseUndisplayedModels()`.
- Списка моделей сессии у Creo.JS нет (только окна и `ListItems`) — поэтому источник истины
  по сессии в доме: CREOSON `file:list`.
- Урок Давыдовки: объект модели из `CurrentModel` может прийти базовым прокси без методов —
  перевзять тем же `session.GetModelFromFileName(имя)` (ERR 2.5).