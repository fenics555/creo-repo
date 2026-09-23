---
name: agent-map
system: общее
description: Use when: нужна КАРТА строения агента дома (D:\AI\tools\agent) — модули, инструменты, данные, протокол, роли, ночь, маршруты, точки расширения
when: агент, agent.py, loop.py, http_handlers, tools_registry, карта агента, 8765, инструменты, блоки, память
priority: high
date: 23.09.2026
---
# КАРТА СТРОЕНИЯ АГЕНТА (редакция дома, 23.09.2026)
Рантайм: `D:\AI\tools\agent` · порт **8765** · пид-файл `agent.pid` · логи `D:\AI\log\agent\`.

## 1. ОДНОЙ СХЕМОЙ
```
agent.py  (тонкий вход: pid, 3 потока — HTTP 8765, ночь, сторож)
   ├─ http_handlers.py  (тело HTTP: маршруты, витрина ui/, токены, щит согласования)
   │      └─ loop.py    (голова: системный промпт, ходовый цикл, протокол [TOOL]/[ANSWER])
   │             ├─ tools_registry.py  ← автоподключение всех *_tools.py (42 блока, 147 инструментов)
   │             ├─ core.post → Ollama 11434 (/api/chat)
   │             ├─ users.py (профили, роли, токены)  ·  vision_tools.py (картинки)
   │             └─ инструменты: creo_tools/creo_ops_tools (CREOSON 8080), pdf_tools, rename/copy,…
   ├─ agent_sched.py    (ночной цикл по расписанию + сторож сервисов)
   └─ core.py           (пути, лог, трейс, alerts, sqlite-хелперы, Ollama-пост)
Данные: data\agent.sqlite (6.4 ГБ) · data\harvest.db (63 МБ) · users.json · secrets.json ·
        config.json · chains.jsonl · backups\ (28 ГБ)
```
**Идея дома:** «руки без ИИ» (детерминированные скрипты и планировщик), «ИИ рядом с руками»
(модель выбирает инструмент и проверяет результат), «деградация без пустышки» (без модели прямые
вызовы и поиск продолжают работать).

## 2. МОДУЛИ
| Модуль | Назначение |
|---|---|
| `agent.py` | тонкий вход: читает `kb_roots.txt`, пишет `agent.pid`, поднимает потоки ночи и сторожа, отдаёт HTTP |
| `core.py` | пути (`BASE`, `DB`, `CONFIG_FILE`, `REPO`), `log`/`log_tail`, `trace`, `alert(s)`, `db()`, `post()` к Ollama, факты (`save_fact`/`get_facts`/`mark_facts_stale`), `boot_report` |
| `settings.py` | **единственный хозяин** `data\config.json`; `REGISTRY` настроек (пространство/ключ/тип/дефолт/описание/UI), `get/set_val/show_all/list_ui`, персональные (`chat_mode`) |
| `tools_registry.py` | `load_all()` — импорт всех `*_tools.py`, сбор `TOOLS`, `get`, `execute` (с проверкой роли), `describe` |
| `loop.py` | системный промпт (`MANIFEST.md` + `SKILL_agent_protocol.md` + список инструментов), `_clean`, стриминг токенов, `parse_model`, `run_loop` (ходы), `ask` (режимы, прямой вызов, согласование) |
| `http_handlers.py` | маршруты GET/POST, выдача витрины `ui/`, токены, щит согласования, превью мастеров (rename/copy/pdf/purge) |
| `agent_sched.py` | `_scheduler` (ночь по `night_hour:minute`, задачи `scan,index,usage,backup,drafts,check`) и `_watchdog` (порт-сторож Ollama/CREOSON с рестартом) |
| `users.py` | пользователи (`data\users.json`), PBKDF2-хэш, роли, токены (TTL 24 ч), `role_deny` (в БД), админ из `secrets.json` |
| `creo_tools.py` | **чтение Creo через CREOSON** (статус, сессия, параметры, отношения, масса, BOM, трейл, аудит) |
| `creo_ops_tools.py` | **пишущие операции Creo** под щитом: параметры, отношения (merge/append/replace), регенерация, save/erase, rename, purge версий, PDF, mapkey, assemble, units, backup |
| `rename_tools.py`, `copy_tools.py` | умные переименование и копирование моделей (превью в витрине) |
| `scanner.py` | индекс памяти: `files` (path/mtime/size/hash/root/type) + `models` |
| `harvest.py` (+ `harvest_gui.py`, `harvest_reader.py`) | «жатва»: `models_raw`, `instances`, `pairs` (пары PDF↔чертёж), `facts_parser` — **вне процесса агента** (пункт 19) |
| `pdf_tools.py`, `pdf_refresh_*.py` | пары PDF/чертёж, вердикты свежести, окно и пакетное обновление |
| `purge_versions.py` | чистка склада версий с предохранителем |
| `backup.py` | двухуровневые бэкапы SQLite: каждые 6 ч в `data\backups\`, ротация по `retention` |
| `panel.py`, `ui\` | витрина: `index.html`, `app.js` (31 КБ), `index_rename.html`, `graph.html`, `map.html` |
| `vision_tools.py`, `vision_audit.py` | вложения-картинки и зрительный аудит |
| `ctl.py` | идемпотентный подъём стека (`up/down/restart/status/--watch`), дедупликация агентов по pid-файлу |
| `excel\excel_export.py`, `excel_import.py` | выгрузка/загрузка Excel (BOM и данные) |
| `qa\qa_run.py`, `mission_test.py`, `run_behavior.py` | приёмка и миссионные тесты; `qa_results.json` |
| `dev\` | `doctor.py` (диагностика), `skills_check.py` (проверка скиллов, зовётся ночью), `ui_check.py`, `ui_probe.py`, `perf_probe.py`, `netdiag.ps1`, `make_spec_one.py` |
| `log_clean.py`, `house_state.py`, `clean_skill.py`, `index_repo.py` | уборка логов по retention, состояние дома на старте, чистка скиллов, индексация репо |
| `data\*` | `agent.sqlite`, `harvest.db`, `config.json`, `users.json`, `secrets.json` (НЕ читать/не выводить), `chains.jsonl`, `harvest_settings.json`, `last_harvest.json`, `pdf_refresh_settings.json`, `skills_check_baseline.txt` |

## 3. ИНСТРУМЕНТЫ: 44 БЛОКА / 145 ИНСТРУМЕНТОВ (живой реестр)
Разбор исходников даёт 42 файла-блока и 147 имён (`*_tools.py`), живой реестр на 23.09.2026 — **44 блока
и 145 инструментов** (часть инструментов добавляется условиями, плюс модуль `vision_audit`).
Новые блоки этой ноги: **`creo_pdf_tools`** (2 инструмента — `creo_pdf_scan`, `creo_pdf_export`).
| Блок | Инстр. | Блок | Инстр. |
|---|---|---|---|
| `creo_tools` | 18 | `usage_tools` | 3 |
| `creo_ops_tools` | 16 | `settings_tools` | 3 |
| `diagnostic_tools` | 8 | `scanner_tools` | 3 |
| `plm_tools` | 7 | `knowledge_tools` | 3 |
| `file_hand_tools` | 6 | `find_tools` | 3 |
| `memory_tools` | 6 | `spec_tools` | 2 |
| `trail_tools` | 5 | `help_tools` | 2 |
| `sync_tools` | 5 | `rename_tools` | 2 |
| `pdf_tools` | 4 | `purge_tools` | 2 |
| `git_tools` | 4 | `fleet_tools` | 2 |
| `backup_tools` | 4 | `learn_tools` | 2 |
| `draft_tools` | 4 | `passport_tools` | 2 |
| `calc_tools` | 4 | `nightly_tools` | 2 |
| `db_tools` | 4 | `behavior,graph,vision,chat,timeline,copy,pdf_refresh,one_c,map,similar,memory_facts,predict` | по 1 |
| `role_tools`, `web_tools`, `users_tools` | 3 | `vision_audit` (модуль) | +неск. |

Полный список: `D:\AI\PROBA\agent_tools_inventory.txt`.
**Ядро частых** (в промпте с полным описанием): `creo_get_active`, `creo_status`, `creo_session`,
`creo_list_files`, `models_find`, `models_where`, `models_stats`, `usage_state`, `search_kb`, `read_file`,
`trail_predict`, `trail_problems`, `settings_show`, `help`, `tools_help`.
Остальные идут в промпт **только именами** (детали — `tools_help block=<имя>`).
**Щит согласования** — инструменты с `"approval": True` (все пишущие Creo, rename, purge, PDF, mapkey).

## 4. ДАННЫЕ (проба 23.09.2026, только чтение)
**`data\agent.sqlite` — 6 531 МБ, 25 таблиц:** `chunks` **1 330 971** · `files` 48 758 · `models` 44 154 ·
`model_embs` 40 519 · `bom` 36 811 · `usage` 2 400 · `facts` 355 · `history` 138 · `usage_meta` 53 ·
`trail_problems` 7 · `trail_scans` 3 · `role_deny` 0 · `skill_usage` 0 · `fts_index*` (FTS-поиск по чанкам) ·
пустые: `changes`, `chat`, `items`, `links`, `revisions`.
**`data\harvest.db` — 63,6 МБ, 10 таблиц:** `models_raw` **93 148** · `pairs` **24 607** (пары PDF↔чертёж) ·
`chunks_fts*` · `instances` · `facts_parser`.
**Прочее:** `users.json` 1 256 б · `secrets.json` 59 б (пароль админа — не выводить) · `chains.jsonl`
(цепочки вызовов) · `config.json` · `last_harvest.json` · `harvest_settings.json` · `pdf_refresh_settings.json` ·
`skills_check_baseline.txt`.
⚠️ **Бэкапы:** `data\backups\` + `data\backup_2026*.sqlite` = **28 ГБ** (10 файлов по 0,29–6,53 ГБ).
Ротация `backup.py` держит `retention` (7) **только по маске `agent_*.sqlite`**, поэтому
`backup_20260907_0828.sqlite` и `backup_pre_orphan_20260904.sqlite` (619 МБ) не убираются никогда.

## 5. ПРОТОКОЛ И ПОВЕДЕНИЕ ГОЛОВЫ (`loop.py`)
- **Системный промпт** = `MANIFEST.md` + `SKILL_agent_protocol.md` (или встроенный `DEFAULT_PROTO`) +
  «основные инструменты» (полные описания) + «прочие» (имена) + правила размышлений по `think_mode`.
- **Режимы:** `1` — инженер (Creo/файлы/база; свободный чат отключён), `2` — собеседник (без данных).
  Переключается префиксом `chat ` / `agent ` или персональной настройкой `chat_mode`.
- **Формат хода:** `[THINK]…[/THINK]` (по `think_mode` 0/1/2) и ровно один блок `[TOOL: имя] {json} [/TOOL]`
  либо `[ANSWER] текст [/ANSWER]`.
- **Защиты:** `_NUDGE` (формат), `_ACCESS_NUDGE` («нет доступа» → повтор), `_REFUSAL` (список отказов),
  `echo_guard`, `web_nudge` (если в задаче ссылка — сначала `web_fetch`), стоп по **повтору сигнатуры**
  вызова (антипетля), `invalid_cnt ≥ 3` → честный отказ с хвостом результата.
- **Ходы:** `steps_max` из поведения (settings `steps_max`, дефолт 6); `parallel_tools` — несколько
  `[TOOL]` за ход в потоках (до 4).
- **Прямой вызов:** если запрос = имя инструмента — вызов идёт без модели (с проверкой роли и щитом).
- **Быстрые маршруты:** `угол …` → `calc_tools.tool_angle`; `doc`-режим (ключи «подробный отчёт» и др.) →
  `num_predict=4096` и «краткость отменена».
- **Стриминг:** `_stream_post` подменяет `core.post`; токены уходят в витрину (SSE `/ask_stream`),
  `[TOOL]` не печатается, `[THINK]` идёт отдельным каналом (`LIVE_THINK`).
- **История:** последние 8 пар из таблицы `history` (обрезаются: q 500 / a 800 симв.).
- **Роли:** `_role_check` → `users.role_denied(role, tool)`; запрет возвращает «🛔 роль … не может …».
- **Согласование:** инструмент с `approval` → запись в `PENDING`, ответ «[СОГЛАСОВАНИЕ] … (id …)»,
  подтверждение — POST `/approve` (`{pid, ok}`).

## 6. РОЛИ, ДОСТУП, НОЧЬ, СТОРОЖ
- Роли (`users.ROLES`): **Инженер, CREO-Программист, Программист, Технолог, Оператор 1С, Руководитель, Администратор**.
- Пароли: PBKDF2-HMAC-SHA256, 120 000 итераций, соль 16 hex; токен `token_urlsafe(24)`, **TTL 24 ч**.
- Новых пользователей даёт POST `/register` (роль «Инженер»); админ — из `data\secrets.json`
  (дефолтного `admin/admin` нет); управление — `/admin/users` (list/role/add/delete/resetpw).
- **Ночь:** `night_enable`, `night_hour`/`night_minute`; задачи `night_tasks` (по умолчанию
  `scan,index,usage,backup,drafts,check`). `scan` и `index` **пропускаются внутри агента** (пункт 19 —
  `harvest.py` живёт вне процесса); `usage` → `usage_tools.build_usage`, `backup` → `backup._do()` +
  `housekeeping`/`drift_check`, `drafts` → `draft_tools.tool_drafts_build`, `check` → `dev\skills_check.py`.
- **Сторож:** каждые `wd_interval` (60 с) проверяет порты **11434** (Ollama) и **8080** (CREOSON);
  при падении ≤3 раз поднимает командами `wd_ollama_cmd` / `wd_creoson_cmd`, дальше — охлаждение.
- **Бэкапы:** `backup.py` каждые 6 ч (SQLite `.backup()`), ротация по `retention`.

## 7. HTTP-МАРШРУТЫ (`http_handlers.py`)
**GET:** `/status` (host, model, blocks, tools, mode, up_ollama/up_creoson/up_agent — **без токена**) ·
`/health` (по токену) · `/children`, `/graph`, `/graph/data`, `/map`, `/map/data` · `/panel` (витрина-панель) ·
`/log`, `/settings`, `/livetoks`, `/livethink`, `/livesteps` (живой ход) · `/fleet/info` ·
`/pdfpages`, `/pdfstatus`, `/pdfregistry`, `/pdfthumb`, `/pdfimg` (мир PDF) · `/ui/app.js` · всё прочее → `ui/`.
**POST (нужен вход):** `/login`, `/register` · **`/ask`**, **`/ask_stream`** (SSE токенов) · **`/approve`** (щит) ·
`/wiz_preview`, `/wiz_rename_preview`, `/wiz_pdf_preview`, `/wiz_pdf_execute`, `/wiz_pdfrefresh_preview`,
`/wiz_pdfrefresh_execute`, `/wiz_purge_preview`, `/wiz_purge_execute` (мастера с превью) ·
`/setmodel`, `/setauto`, `/setcfg`, `/setname`, `/setpw`, `/profile`, `/feedback` ·
`/scan`, `/rescan`, `/snap` · `/chat/send`, `/chat/poll` (внутренний чат) · `/admin/users` (list/role/add/delete/resetpw).

## 8. ТОЧКИ РАСШИРЕНИЯ (как принято в доме)
| Что добавить | Как |
|---|---|
| **Инструмент** | в любом `*_tools.py` добавить в список `TOOLS` запись `{"name","desc","params","approval","fn"}` — реестр подхватит сам |
| **Новый блок** | создать файл `<тема>_tools.py` с `TOOLS = [...]` (автоподключение в `tools_registry.load_all`) |
| **Настройка** | строка в `settings.REGISTRY` (пространство, ключ, тип, дефолт, описание, показывать-в-UI) → появится в `/settings` и витрине |
| **Ночная задача** | ветка в `agent_sched._scheduler` + имя в `night_tasks` |
| **Страница витрины** | файл в `ui\`; после правок прогнать `dev\ui_check.py` и `dev\ui_probe.py` |
| **Проверки** | `dev\doctor.py` (диагностика), `dev\skills_check.py` (скиллы), `qa\qa_run.py`, `qa\mission_test.py`, `dev\perf_probe.py` |
| **Безопасность правок** | бекап `data\backup\pre_<метка>_<файл>` до изменения; секреты только в `data\secrets.json` |

## 9. НАБЛЮДЕНИЯ И РИСКИ (на 23.09.2026)
1. **Вес данных.** `agent.sqlite` — **6,4 ГБ** (1,33 млн чанков, 48,7 тыс. файлов, 44 тыс. моделей);
   `data\backups\` — **28 ГБ**. Расти будет и дальше: нужен отдельный разговор о retention и о том,
   хранить ли все чанки.
   🔴 **Память процесса:** при импорте блоки `knowledge_tools` (матрица **1 330 971** фрагмента) и
   `similar_tools` (40 904 модели) поднимают свои матрицы в RAM → процесс агента держит **~12,7 ГБ**
   (замер 23.09.2026). Процесс завершался вручную (освободилось 12,42 ГБ), **но поднялся заново** —
   потому что был запущен домашний старт `Z:\PTC\CREO-START\START-STD\CREO-START.bat` (клик из проводника,
   9:19:24): он поднимает **Creo + CREOSON + агента** сразу. Задача планировщика `CREO-AGENT-UP`
   (`python ctl.py up --hidden`) — второй путь автоподъёма стека.
   **Что нужно сделать (не правил):** грузить матрицы ЛЕНИВО (по первому вызову) или через mmap/диск;
   либо дать агенту флаг «без тяжёлых блоков» для режима без витрины.
   ⚠️ Следствие домашнего старта: при живом Creo он поднимает **вторую сессию Creo**
   (23.09.2026: две — PID 8764 от 8:18 и 13000 от 9:19). Для CREOSON/JLINK это риск
   («more than one instance» → падение JVM-моста) — перед прогонами PDF держать ОДНУ сессию.
2. ⚠️ **Дыра в ротации бэкапов:** `backup.py` чистит только `agent_*.sqlite`. Два посторонних дампа
   (`backup_20260907_0828.sqlite`, `backup_pre_orphan_20260904.sqlite`, 591 МБ) **удалены 23.09.2026**,
   но маска не исправлена. Плюс сам `retention=7` × база 6,4 ГБ = **~28 ГБ** — вопрос политики.
3. **Мусор в корне:** ~125 файлов, среди них десятки одноразовых `fix_*.py`, `debug_*.py`, `harvest_part*.py`,
   `patch_*.py` — реестру не мешают (он берёт только `*_tools.py`), но читателю-человеку и ИИ мешают.
4. **Пустышка `agent.sqlite` (0 б) в корне** — посторонний файл (рабочая база живёт в `data\`).
5. **Ночной `scan`/`index` — заглушки** (пункт 19): индекс памяти наполняет `harvest.py` вне процесса агента.
   Значит «ночь» сама по себе индекс не обновляет — это надо помнить при планировании.
6. **Токены в памяти процесса:** рестарт агента = все сессии сбрасываются (нужен повторный вход).
7. **`/status` без токена** отдаёт имена модели и число блоков — удобно для проверок, но это открытый порт;
   `/health` и `/fleet/info` закрыты.
8. **Инструментов 147** — промпт держит полные описания только у 15; остальные именами. При добавлении
   инструментов важно не ломать этот баланс (иначе промпт распухнет).
9. **Щит согласования** покрывает все пишущие операции Creo (`approval: True`) — это правильная граница,
   снимать её нельзя без явного слова пользователя.

## 10. СВЯЗАННЫЕ ДОКУМЕНТЫ
`D:\AI\repo\SKILL_agent_protocol.md` (протокол `[TOOL]/[ANSWER]` для модели агента) ·
`D:\AI\repo\SKILL_local_agent_cline.md` (выживание в Cline) · `D:\AI\repo\Prog\SKILL_agent_memory.md`
(память/якорь) · `D:\AI\repo\PASSPORT.md` («Модули агента») · `D:\AI\repo\CREO_MAP.md` (как агент ходит в Creo).
Крах-скиллы: `crash\SKILL_agent-frozen.md`, `crash\SKILL_crash_agent-duplicate-restart-race.md`,
`crash\SKILL_crash_agent_corruption.md`, `crash\SKILL_crash_agent_silence.md`,
`crash\SKILL_crash_runcommands_kill-by-name-house-services.md`.
Конспект разбора: `D:\AI\PROBA\AGENT_NOTES.md`. Инвентарь инструментов: `D:\AI\PROBA\agent_tools_inventory.txt`.

## 11. ОБСЛУЖИВАНИЕ (чистка 23.09.2026)
- **Убрано 200 объектов (~592 МБ):** одноразовые `fix_*.py`/`debug_*.py`/`patch_*.py`/`harvest_part*.py`,
  логи и 0-байтные файлы, `payload.json`, тест-папки `test_purge_dir*`, `tmp\`, `__pycache__`,
  89 файлов `data\tmp`, **два посторонних дампа БД (591 МБ)**, осиротевшие `purge_versions_part*.py` и `.bak`.
- **Корень агента: 125 → 82 файла.** Живой блок `one_c_tools.py` сохранён (проверка ссылок).
- **Приёмка:** `/status` = 43 блока / 143 инструмента, все порты живы; «руками» — `creo_status` → «CREOSON жив;
  Creo запущен: ДА», `models_stats` → 44 154 модели, `usage_state` → индекс готов; «через ИИ» — вход admin,
  прямой вызов и вопрос модели («какие модели открыты в Creo?» → 3 модели, `creo_session`, 2 шага, 22 с).
- **Подробности и список «что устарело»:** `D:\AI\log\reports\REPORT_agent_cleanup_cline_2026-09-23.md`.