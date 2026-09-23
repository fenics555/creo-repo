---
name: creo-map
system: Creo
description: Use when: нужна КАРТА «строения» Creo — установка, слои API, каналы управления, документация, что чем делать, точки входа
when: карта, строение, архитектура creo, установка, слои, каналы, api, где что лежит, обзор
priority: high
date: 23.09.2026
---
# КАРТА СТРОЕНИЯ CREO (редакция дома, 23.09.2026)

## 1. ОДНОЙ СХЕМОЙ
```
                 Creo Parametric 12.4.2.0   (D:\PTC\CREO12\Creo 12.4.2.0)
                                │
                объектная модель  pfc*  (com.ptc.pfc.*, 1873 класса в jar)
      ┌──────────────┬──────────────┬──────────────┬────────────┬──────────────┐
   Creo.JS        OTK C++        OTK Java        VB API      Web.Link      Toolkits
  (creojs)     (protoolkit)   (otk_java_doc)   (vbapi)     (weblink)   (usrprog/PRO_APPT)
                                │
                          JLINK (Java)   ← pfcasync.jar + pfcasyncmt.dll
                                │
                 CREOSON (JSON поверх JLINK, порт 8080)
                                │
   дом: агент 8765 · copy-server 8000 · Давыдовка (Creo.JS + свой сервер)
```
**Закон:** один объектный слой `pfc*` — много каналов; выучил один — читаешь остальные.
**Доказано живьём:** `creoson-core-3.0.1.jar` не содержит `com.ptc.pfc` (только 268 классов
`nitro.jlink`), а `pfcasync.jar` = 1873 класса `com/ptc/pfc`. Значит CREOSON — JSON-слой над JLINK,
а JLINK доступен напрямую (без сервера и без сборки C++).

## 2. УСТАНОВКА — ЧТО ГДЕ ЛЕЖИТ (с числами)
| Путь (от `D:\PTC\CREO12\Creo 12.4.2.0`) | Файлов | Размер | Что это |
|---|---|---|---|
| `Common Files\creo_help_pma` | 97 192 | 1115 МБ | **полная справка Creo** (HTML + картинки) |
| `…\creo_help_pma\russian` | 48 456 | 569 МБ | русская справка (в т.ч. ~15 678 HTML) |
| `Common Files\protoolkit` | 19 897 | 651 МБ | **Object TOOLKIT C** (+`online_help`) |
| `Common Files\otk` | 506 | 950 МБ | OTK: библиотеки/заголовки |
| `Common Files\otk_cpp_doc` | 5 373 | 69 МБ | **док OTK C++** (+`online_help`), внутри `otk_methods.txt` |
| `Common Files\otk_java_doc` | 5 364 | 67 МБ | док OTK Java (+`online_help`) |
| `Common Files\otk_java_free` | 221 | 4.7 МБ | **JLINK-примеры и утилиты** (`jlinkexamples`, `jlink_servlet`, `jlink_param`, `jlink_loader`) |
| `Common Files\text\java` | 13 | 32.8 МБ | **`pfcasync.jar`** (1 205 062 б) — JLINK API |
| `Common Files\x86e_win64\{lib,obj}` | — | — | **`pfcasyncmt.dll`** (15 412 704 б), `pro_comm_msg.exe` |
| `Common Files\applications` | 28 352 | 4948 МБ | приложения (в т.ч. `gdt_home` = GD&T Advisor, 638 файлов/12 МБ) |
| `Common Files\creojs` | 2 952 | 28.8 МБ | **канал Creo.JS** (+`online_help`) — канал Давыдовки |
| `Common Files\modchk` | 354 | 2.3 МБ | **ModelCHECK** |
| `Common Files\mfg_cmdsyn` / `_ai` | 25 / 21 | 0.1 МБ | **синтаксис команд ЧПУ** (`.def` = грамматика, `.syn` = UGC-токены) |
| `Common Files\vbapi` | 2 859 | 27.5 МБ | VB API (+`online_help`) |
| `Common Files\weblink` | 3 192 | 28.8 МБ | Web.Link (+`online_help`) |
| `Common Files\templates` / `symbols` / `tol_tables` | 146 / 110 / 58 | 11 / 2.4 / 0.1 МБ | шаблоны, символы, таблицы допусков |
| `Parametric` | 121 | 89 МБ | сама программа |
| `Common Files\demos`, `formats`, `text`, `protable`, `usrprog`, `PRO_APPT` | — | — | прочее служебное |

## 3. ШЕСТЬ `online_help` — СПРАВКА ПО КАНАЛАМ
`Common Files\{creojs, otk_cpp_doc, otk_java_doc, protoolkit, vbapi, weblink}\online_help` —
по одному на канал: **Creo.JS · OTK C++ · OTK Java · TOOLKIT C · VB API · Web.Link**.
Плюс: `mfg_cmdsyn` (ЧПУ), `gdt_home\...\html` (GD&T, 215 HTML), `modchk` (ModelCHECK),
`creo_help_pma\russian` (общая справка).

## 4. ЧТО ЧЕМ ДЕЛАТЬ (матрица задач дома)
| Задача | Средство | Скилл / файл |
|---|---|---|
| Открыть/закрыть/сохранить модель, узнать что открыто | **CREOSON** | `CREOSON\SKILL_creoson_routine.md` |
| Переименовать модель (с чертежом/родителями) | **CREOSON** (`onlysession` → `save`) | `SKILL_creoson_rename_mechanism.md` |
| Копия проекта (сборка+детали, деталь+чертёж, семейство, mfg) | **CREOSON** (свой сценарий) | `SKILL_copy_assembly_project.md` + `D:\AI\PROBA\smartcopy.py` |
| Параметры/отношения/масса/BOM — чтение | **CREOSON** | `SKILL_parameters_guide.md`, `SKILL_creo_relations.md` |
| Запись параметров и отношений | **CREOSON** под щитом | `CREOSON\SKILL_creoson_write_rules.md` |
| Картинка/PDF чертежа | **CREOSON** `interface:export_image` / `export_pdf` | `pdf_tools.py` агента, `SKILL_creoson_routine.md` |
| **PDF чертежа (главная рутина)** | **JLINK** (инструмент `creo_pdf`) или CREOSON `export_pdf` | `SKILL_creo_jlink_direct.md` (§PDF, §рутина) |
| PDF-рутина «PDF нет/старше чертежа» по папке | `creo_pdf.bat scan\|export` (ИИ: `creo_pdf_scan`/`creo_pdf_export`) | `SKILL_creo_jlink_direct.md` |
| Обмен 3D: STEP / IGES / VRML / NEUTRAL | **JLINK** или **CREOSON** `interface:export_file` | `SKILL_creo_jlink_direct.md` |
| Своя программа, пачка моделей, цикл по сотням | **JLINK** (Java) | `SKILL_creo_jlink_direct.md` + инструмент `D:\AI\tools\agent\creo_export` |
| Инженерные формы КБ внутри Creo | **Creo.JS** (канал Давыдовки) | `SKILL_creojs_api.md`, `SKILL_davydovka_creoson_map.md` |
| Уравнения/пружины/расчёты | скиллы дома | `SKILL_relations_*`, `SKILL_spring_*`, `SKILL_curves_*` |
| Семейства (таблицы исполнений) | **CREOSON** `familytable:*` | `SKILL_creoson_routine.md` |
| ЧПУ / траектории / CL-данные | **файловый уровень** (`mfg_cmdsyn`) | `SKILL_creo_directions_mfg_gdt.md` |
| Аудит оформления, чертежи по ЕСКД | скиллы дома | `SKILL_drawings_eskd.md`, `SKILL_naming_spec.md` |

## 5. ТОЧКИ ВХОДА В ДОМЕ
| Что | Адрес/команда |
|---|---|
| Creo (окно) | `CREO_START`/`CREO-LOCAL-START\Creo_LOCAL.bat`; рабочая папка `Z:\PTC\CREO-START` |
| Стек | `python D:\AI\tools\agent\ctl.py up` (Ollama 11434 · CREOSON 8080 · copy-server 8000 · агент 8765) |
| Статус | `python D:\AI\tools\agent\ctl.py status` |
| CREOSON | `http://127.0.0.1:8080/creoson`, каталог `D:\PTC\CREO-LOCAL-SETUP\creoson` |
| Агент | `http://127.0.0.1:8765` (`/status` открыт, `/health` — по токену) |
| Инструмент экспорта | `cmd /c call "D:\AI\tools\agent\creo_export\creo_export.bat" <формат> <модель>` |
| **PDF-рутина** | `cmd /c call "D:\AI\tools\agent\creo_pdf\creo_pdf.bat" scan\|export\|pdf\|config-read\|config-load …` |
| Полигон | `D:\AI\PROBA` (модели, семейства, mfg, `jlink_probe`, `drw_pdf`) |

## 6. ЧТО ПРОВЕРЕНО ЖИВЬЁМ (сводка)
| Проба | Результат |
|---|---|
| `file:backup`, `interface:export_image` | работает (CREOSON) |
| Каскад переименования `onlysession`→`save` | диск+чертёж+родители переименованы |
| Умная копия сборки+деталей (`amf75838.asm`) | все ветки сценария пройдены |
| Семейства: плоское (`df-stp2-gdf`), вложенное (`pin_split`), mfg-набор (`ст-чпу-2-mfg.asm`) | таблицы сохраняются; `list_tree` на больших семействах ВИСНЕТ |
| Прямой JLINK: подключение к живой сессии, `GetSession`, `Disconnect` | Creo остаётся жив |
| Прямой JLINK: чтение `pin_splitk.prt` | **47 параметров** (23 с кириллицей) + `mass=0.002014…`, `volume=256.562…`, `area=577.847…` |
| Прямой JLINK: экспорт `pin_splitk.prt` | STEP 13 467 б · IGES 55 268 б · VRML 26 233 б · NEUTRAL 67 100 б (`.neu.1`) |
| Прямой JLINK: **PDF** `knockout_1.drw` | **26 276 б, %PDF-1.7** (нужны: чертёж + папка + `Display()`) |
| CREOSON: **PDF** того же чертежа | 26 262 б, `%PDF-1.7` (с `use_drawing_settings`) |
| Карта API | `otk_methods.txt` = 4 159 строк / **717 классов**; в jar **121** класс `*ExportInstructions*` |
| Агент | жив: 43 блока / **143 инструмента**, модель `gemma4:26b-131k` |

## 7. ГРАНИЦЫ И ГРАБЛИ (куда смотреть)
1. **2D/DXF/DWG/PDF — только с ЧЕРТЕЖА** (на детали `XToolkitGeneralError` / `XToolkitInvalidType`);
   PDF вдобавок требует `Model.Display()` (иначе `XToolkitNotDisplayed`).
2. **Пути с пробелами** (`Creo 12.4.2.0`) ломают `-Djava.library.path` при детач-запуске — запускать через `.bat`.
3. **Кириллица**: данные корректны (JSON/файлы), но консоль (cp866) и PowerShell искажают — только Python/UTF-8.
4. **Creo дописывает суффикс версии** к экспортам (`name.neu` → `name.neu.1`).
5. **Убивать процессы только по PID** (`Stop-Process -Name python` сносит агент и copy-server).
6. Крах-скиллы темы: `crash\SKILL_crash_git_parallel-leg-rebase-reverts-worktree.md`,
   `crash_runcommands_kill-by-name-house-services.md`, `SKILL_agent-frozen.md`, `SKILL_crash_pdf-roots-two-lists.md`.

## 8. СВЯЗАННЫЕ КАРТЫ
Полный отчёт исследования — `D:\AI\log\reports\REPORT_creo_full_cline_2026-09-23.md`.
Разбор прямого управления — `README_jlink_direct.md`. Карта скиллов — `SKILLS_MAP.md`.
Индекс ветки — `SKILL_creo_index.md`; общий индекс дома — `D:\AI\repo\SKILL_index.md`.