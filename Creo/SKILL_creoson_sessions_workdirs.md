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
## 6. ЖИВЫЕ ПРОБЫ УПРАВЛЕНИЯ CREO (17.09.2026)
- `creo:cd {dirname}` переключает рабочую папку: `pwd before = D:/AI/ПРОБА/23-1017GRI 2кап…''/`
  → `pwd after = D:/AI/PROBA/23-1017GRI/`; 13 загруженных моделей остались в сессии
  (cd никого не выгружает и не перепривязывает).
- Полигон `D:\AI\PROBA\23-1017GRI` — чистая площадка: `list_files count=2` (`test.drw`,
  `test.pdf`), `*.asm -> 0`, `*.prt -> 0`, `*.drw -> 1`, `list_dirs: []`. Настоящий проект
  рядом: `D:\AI\ПРОБА\23-1017GRI 2кап чистовой BDF 5 1_2''`.
- `connection:start_creo`:
  * при живом Creo → `{"error": true, "message": "Creo is already running"}` (второй Creo
    не поднимает, пока первый отвечает);
  * имя батника валидируется: `start_command: "creoson_run.bat"` →
    `"You may only specify 'nitro_proe_remote.bat' for the startCommand parameter"`;
  * `use_desktop: true` при живом Creo → тот же отказ;
  * `nitro_proe_remote.bat` в доме НЕТ (проверено в `D:\PTC\CREO-LOCAL-SETUP\creoson`,
    `CREO-LOCAL-START`, `Z:\PTC\CREO-START\START-STD`) → чтобы поднимать Creo через API,
    этот батник надо создать обёрткой (`cd /d <папка старта>` + запуск Creo/CREO-START).
- `connection:kill_creo` (проба с прямого согласия пользователя):
  `xtop before: 3084, 13068` → `kill_creo status {"error": false}` →
  `is_creo_running: {"running": false}` → `creo:pwd: "No session found"` →
  `xtop after: <пусто>`, `nmsd after: <пусто>`, JVM creoson (PID 11660) **выжил**.
  ⚠️ Убивает `xtop.exe` и `nmsd.exe` ПО ИМЕНИ — то есть ВСЕ инстансы Creo сразу, вместе
  с рабочей сессией инженера (в пробе сессия пользователя закрылась). Без прямого слова
  пользователя не вызывать; «мягкий» выход — `connection:stop_creo`.
- После убийства Creo в доме поднялся заново (в системе снова `xtop` + `nmsd`): старт Creo
  живёт отдельно от CREOSON (CREO-START/сторож), а `kill_creo` лечится обычным стартом.

## 7. ДВЕ СЕССИИ И ЧУЖАЯ РАБОЧАЯ ПАПКА — горький урок 17.09.2026
Живой случай: в системе было **два Creo** (xtop 3084 и 13068). CREOSON был прицеплен
к инстансу с рабочей папкой полигона (`D:/AI/ПРОБА/…`), а инженер в это время работал
в **другом** инстансе с рабочей папкой
`Z:\PTC\Work\000_03 401-LIT Литейное производство\000_5 401-LIT-MO Модельная оснастка для литья\M-INSERT Комплект на отливку губок\`.
Проба `kill_creo` убила оба процесса по имени → **рабочая сессия инженера закрылась**;
несохранённые правки потеряны (файлы на диске целы).
Правила, вытекающие из случая:
1. `kill_creo` в доме НЕ применять никогда; «мягкий» выход — `stop_creo`, а закрытие Creo —
   рука пользователя. Даже с разрешения — предупреждать, что умрут ВСЕ инстансы.
2. Перед любой пишущей операцией сверять `creo:pwd` с ЦЕЛЕВОЙ рабочей папкой; если это
   не та папка — сначала `creo:cd`, потом операция. Иначе автоматика правит чужие модели.
3. Рабочие папки дома (для сверки): литейка/оснастка —
   `Z:\PTC\Work\000_03 401-LIT Литейное производство\…`; полигон проб —
   `D:\AI\PROBA\23-1017GRI` (2 файла) и проект `D:\AI\ПРОБА\23-1017GRI 2кап чистовой BDF 5 1_2''`.
4. Непонятно, к какому инстансу прицеплен CREOSON — не гадать: сверять `pwd` + `file:list`;
   два инстанса на машине = признак, что автоматику может «снести» чужая правка.

## 8. ЧТО kill_creo ДЕЛАЕТ С JVM И КАК УБИВАТЬ НУЖНЫЙ ИНСТАНС (18.09.2026)
- `connection:kill_creo` убивает `xtop.exe`+`nmsd.exe` по имени (ВСЕ инстансы) И рвёт JLINK:
  после пробы в каталоге creoson появились `hs_err_pid11660.log` (11:37:29) и
  `hs_err_pid20964.log` (11:41:40) — JVM падает нативным крахом PTC при следующем
  `is_creo_running`/connect; в `logs\json.log` последний запрос ушёл БЕЗ ответа.
  Вывод: после `kill_creo` перезапускать ОБА конца — Creo (лаунчером) и creoson (`ctl.py up`, 8080).
- Пока Creo мёртв, `is_creo_running` сам по себе рискован: именно на нём JVM и падал.
  Безопасный порядок: сначала поднять Creo, потом спрашивать состояние.
- `connection:start_creo` в доме: обёртка `nitro_proe_remote.bat` создана 18.09.2026 в
  `D:\AI\PROBA\23-1017GRI` (`cd /d D:\AI\PROBA\23-1017GRI` + `start "" parametric.exe`).
  Живые ответы API: при живом Creo — `"Creo is already running"`; чужое имя файла —
  `"You may only specify 'nitro_proe_remote.bat' for the startCommand parameter"`.
- Убить ОДИН нужный инстанс средствами CREOSON НЕЛЬЗЯ (kill бьёт по имени = все). Путь:
  1) определить прицепленный инстанс сверкой `creo:pwd` + `file:list` с ожиданием;
  2) закрыть ЧУЖОЙ процесс адресно: `Stop-Process -Id <pid>` (PID — из `Get-Process xtop`);
  3) `connection:stop_creo` закрывает ТОЛЬКО прицепленный Creo — в доме без прямого слова
     пользователя не вызывать (это может быть его рабочая сессия).
- Признак «сессия ещё не готова» (Creo стартует): `connect` проходит, но `creo:pwd` = `null`,
  `list_files` = 0, `file:list` = 0. Это НЕ ошибка: подождать и повторить, а не «лечить».
- Правило дома (после двух потерянных сессий инженера): `kill_creo` не применять;
  адресное убийство — только `Stop-Process` по PID, и только по слову пользователя.

## 9. ЭКСПЕРИМЕНТ «НЕСКОЛЬКО CREO — УБИТЬ ТОЛЬКО НУЖНЫЙ» (19.09.2026)
Полигон: свои папки `D:\AI\PROBA\23-1017GRI` и `D:\AI\PROBA\creo2` с маркерами
`marker_creo1.txt` / `marker_creo2.txt`; на Z: не ходили; согласие пользователя получено.
1. **`connection:start_creo` РАБОТАЕТ** (первая успешная проба дома): обёртка
   `nitro_proe_remote.bat` (`cd /d D:\AI\PROBA\23-1017GRI` + `start "" parametric.exe`),
   вызов `{start_dir, start_command:"nitro_proe_remote.bat", retries:0}` → `{"error": false}`,
   через ~20 с поднялся `xtop` (PID 8292, 13:12:28). При живом Creo тот же вызов отказывает:
   `"Creo is already running"`.
2. Второй инстанс поднят НАПРЯМУЮ (обёртка в `D:\AI\PROBA\creo2`) — два `xtop` (8292 и 21940).
3. **Привязка определяется только фактами**: `creo:pwd = D:/AI/PROBA/23-1017GRI/` и в
   `creo:list_files` виден `marker_creo1.txt` → CREOSON держит инстанс №1; второй ему не виден.
4. **Адресное убийство работает и безопасно**: `Stop-Process -Id 21940 -Force` убрал ТОЛЬКО
   второй инстанс; CREOSON (8080) остался жив, `is_creo_running: true`, `creo:pwd` не изменился.
   Это правильный путь вместо `kill_creo` (тот бьёт по имени процесса = все инстансы).
5. **Скрытый запуск Creo документирован официально** (подсказка пользователя, проверено в PDF):
   `vbug.pdf` стр.28-29, для асинхронного старта —
   `cAC.Start(путь + " -g:no_graphics -i:rpc_input", ".")`, где **`-g:no_graphics`** отключает
   графику, **`-i:rpc_input`** включает RPC-ввод. Для дома: добавить оба ключа в
   `nitro_proe_remote.bat` → Creo без окна, рабочая станция не загружается окнами.
   Рядом в `creojsug.pdf` есть режим `MODELCHECK_NO_GRAPHICS — batch mode`.
   **ЖИВАЯ ПРОБА 19.09.2026**: запуск обёртки с ключами дал новый `xtop` PID 4152, и его
   командная строка прямо содержит ключи: `xtop.exe -g:no_graphics -i:rpc_input -ppid 4720`
   (у обычных инстансов 8292/7872 ключей нет). Скрытый Creo работает.
   ⚠️ `MainWindowHandle` для проверки «скрыт/не скрыт» НЕ годится: у всех трёх инстансов он 0
   (моя сессия не видит их окна) — единственный надёжный признак скрытого режима это CommandLine.
8. **Часы машины скачут** (важно для приёмок): у процесса, запущенного около 16:20, `StartTime`
   показал `11:51:46`, а логи в тот же период писали 11:55 и 16:15. Значит трёхчастная приёмка
   рестарта «StartTime процесса больше mtime правленого файла» может ложно падать: при явном
   расхождении часов сверять ещё и PID/содержимое лога, а не только время.
6. **Что роняет JVM**: `kill_creo` (рвёт JLINK) и **любой запрос при мёртвом Creo**:
   `hs_err` 18.09 (`rtlcoremtz.dll`), 19.09 11:55 (`ntdll.dll`) — оба `EXCEPTION_ACCESS_VIOLATION`
   в потоке `HTTP-Dispatcher`; после падения лечится `ctl.py up` (8080 → новый PID).
7. Наблюдение: `Get-Process xtop` в моей сессии отдавал RAM 18-19 МБ вместо ~530 МБ
   (урезанные права) — честные цифры брать из `tasklist`/`Get-CimInstance`.