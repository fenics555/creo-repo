---
name: index
system: общее
description: Карта всех скиллов репо по доменам: что где лежит и куда смотреть
when: навигация, где что, карта скиллов, список скиллов, какой скилл, домены
priority: critical
---

# КАРТА СКИЛЛОВ РЕПО (D:\AI\repo)
Один скилл = одна зона знания. Домены не дублируют друг друга.

## НАПРАВЛЕНИЯ (первый указатель, состав по MANIFEST.md)
- **SKILL_models_behavior.md** (priority: critical) — поведение локальных моделей, лимиты, режимы think,
  критические правила безопасности. Читать ДО выбора модели для задачи.
- **Параллельные ноги (ВСЕГДА, до любого git):** `SKILL_parallel_legs.md` — **critical**, общий закон
  общих репозиториев `D:\AI\repo` и `D:\AI\tools`: коммит только с pathspec, чужой staged не трогать,
  чужой rebase не продолжать. Читать перед первым `git commit`/`git push` в этой сессии.
- **АНТИ-ГАЛЛЮЦИНАЦИИ (новое, 11.10.2026):** `SKILL_anti_hallucination.md` — **critical**, правила
  против выдумки: источник и уровень (ФАКТ/ПРЕДПОЛОЖЕНИЕ/НЕТ ДАННЫХ), презумпция существования
  (сначала проверь — потом утверждай), запрет имитации проверки («искал в…» только если реально искал),
  безопасная деградация (отсутствие источника ≠ REVIVE), few-shot как шаблон (закон из PROMPT).
  **Читать по триггеру 3.П.5 `.clinerules` v6.22:** факт без живой цитаты (номер ГОСТ/ТУ/патента,
  путь к файлу/функции, имя переменной).
  **Живые факты v4/v5/v6 (11.10.2026):** ни одна модель не свободна от галлюцинаций; laguna и
  nemotron — худшие (выдуманные ГОСТ, пути, имитация `search_codebase`).
- Creo: Creo\SKILL_creo_index.md · PDF: PDF\SKILL_pdf_index.md · Web: Web\SKILL_web_index.md
- Инженерные: Инженерные\SKILL_engineering_index.md · Трейлы: Трейлы\SKILL_trails_index.md
- Ошибки: Ошибки\SKILL_errors.md · Крахи: crash\SKILL_crash_constitution.md (закон) + crash\SKILL_crash_index.md (список крах-скиллов)
- **НОГА (новое, 01.10.2026):** NOGA\SKILL_noga_index.md — здоровье ноги и самопередача:
  счётчик вызовов инструментов, три признака деградации, пороги, порядок эстафеты. Тело скилла —
  `AGENT_SETTINGS\NOGA\SKILL_noga_health.md`. Правило-источник: пункт «ПРЕДЕЛ НОГИ» в `.clinerules`.
- **OLAMA (новое, 08.10.2026):** OLAMA\SKILL_ollama_index.md — **critical**, вход направления
  локальных моделей Ollama: раннер, `num_predict` для рассуждающих моделей, ответ vs размышление,
  стоп/rm/create и грабли ANSI в stderr. Тела: `OLAMA\SKILL_num_predict_for_reasoning_models.md`,
  `OLAMA\SKILL_answer_vs_thinking.md`; живые замеры стека — в `AGENT_SETTINGS\checks\`.
- **НАСТРОЙКИ (новое, 08.10.2026):** Prog\SKILL_settings_audit.md — **critical**, аудит настроек
  дома: `config.json`, `REGISTRY`, `set_values`, куда программа пишет и откуда читает.
  Родня: `Prog\SKILL_repo_mapping.md`.
- **Заряд скиллов** (новое, 08.10.2026): `SKILL_CHARGE.md` — **карта скиллов и заряд знаний**:
  какие скиллы обязательны к чтению, в каком объёме и когда. Стартовая выборка — `SKILL_CHARGE_START.md`.
- **Архив PLM** (новое, 08.10.2026): `Creo\SKILL_archive_plm.md` — **high**, архив и старые срезы склада:
  что где лежит, что пересобирать нельзя, как читать срез без живой сети.
- **Creo сырой читатель** (новое, 08.10.2026): `Creo\READ\SKILL_creo_raw_reader.md` — чтение `.prt/.asm/.drw`
  **напрямую, без API**: заголовки, записи полей, что в файле открытый текст, а не бинарник.
  Тела направления: `Creo\\READ\\SKILL_creo_read_*.md`, `Creo\\READ\\SKILL_creo_file_format.md`.
  **Долг шапки:** у файла нет `name`/`when` (найдено 08.10.2026) — до слова владельца строку
  не переписывать, добавление шапки = отдельная заявка.
- **ВТОРОЕ ХРАНИЛИЩЕ СКИЛЛОВ (закон навигации, 08.10.2026):** скиллы дома живут в ДВУХ корнях,
  и поиск обязан обходить оба: (1) **память** — `D:\AI\repo\` (закон, карты, крах-скиллы,
  направления); (2) **методика и инструменты** — `D:\AI\AGENT_SETTINGS\` (реестр настроек
  моделей и измеритель: `PROMPT\` — правила как инженерная система, `NOGA\` — здоровье ноги,
  `checks\` — живой стенд `loop_revive_test.py`, отчёты и маяк прогона, `config\` — поведение).
  Тело скилла второго корня **намеренно** не дублируется в `repo\`: методика и её инструменты
  обновляются вместе, память хранит указатель. **Проверка видимости обязана искать по обоим
  корням**, иначе живые скиллы ложно объявляются мёртвыми ссылками (случилось 08.10.2026:
  24 ложных дефекта из 26). Приёмка: `Get-ChildItem` по обоим корням с фильтром `SKILL_*.md`.
- **ВЕТЕРОК (04.10.2026):** `Ветерок\SKILL_veterok_index.md` — очистка сборок Creo. Живой факт: удаление
  параметров пишется на диск, а пострегенерация через CREOSON — НЕТ (правильный путь JLINK
  `pfcModel.DeletePostRegenerationRelations`). Тела: `SKILL_veterok_{postregen,creoson_gotchas,program}.md`.
- **ОКНА (03.10.2026):** `ОКНА\SKILL_WINDOWS_GUI.md` — окна программ (tkinter): каркас, закон потоков
  (`root.after(0,…)`), канон `ОКНА\02_ДИЗАЙН_И_РАСКЛАДКА.md`; проверка `python dev\design_check.py`
  (22 окна, 0 замечаний). Статус — черновик.
- **B&W (03.10.2026):** `B&W\SKILL_BW_PLUGINS.md` — плагины SMART\* к Creo: 15 модулей, канал `protkdat`;
  под CREO13 годятся 3 (главный SMARTHolechart — таблицы `.hol`). Черновик. Конспект — `B&W\README.md`.
- **PROMPT (01.10.2026):** `PROMPT\SKILL_prompt_index.md` — правила как инженерная система; тела в
  `AGENT_SETTINGS\PROMPT\` (critical): `SKILL_prompt_position_from_window`, `SKILL_fewshot_as_template`
  (few-shot = шаблон), `SKILL_section_cut_silently` (`SECTION_MAX` режет раздел молча).
- **ПЛАН ОБНОВЛЕНИЯ АГЕНТА (03.10.2026):** `D:\AI\ПЛАН_ОБНОВЛЕНИЯ_10_26\` — 9 документов (движок правил
  `rules.json`, каркас проверок, валидатор `.hol`, контракт самодостаточного инструмента). ⚠️ ЛОКАЛЬНАЯ, вне гита.
- **ВОЛНЫ 6–11 (03.10.2026):** инструменты агента `D:\AI\tools\agent` (реестр ~185 инструментов, 53 блока;
  приёмки `dev\vol<N>_check.py`). Волна 8 — `agent\plan_run\` (планы `plan.json`: шаг = `n·what·where·args·risk·rollback·verdict`).
  Волны 9–11 — витрина «Проверки дома» (`wiz_checks`), карта плагинов `agent\dev\PLUGINS.md`.
  **Законы:** контракты CREOSON (см. Creo\CREOSON); успех записи проверяется ПО ФАЙЛУ НА ДИСКЕ;
  существование папки — рекурсивным поиском по ИМЕНИ, а не по придуманному пути.

### 1. Creo (Веб-агент, Инженер)
*Специализация на работе с CAD-системой через API и интерфейсы.*
**Вход темы — `Creo\SKILL_creo_index.md`** (главный индекс Creo: открытие + структура + карта).
ГЛАВНОЕ (22.09.2026): один `pfc*` — много каналов; управлять Creo можно напрямую (Creo.JS / OTK-JLINK /
Pro-TOOLKIT / VB / Web.Link), **CREOSON = JSON-сервер поверх JLINK**; Давыдовка — канал Creo.JS + свой сервер 8000.
Подразделы `Creo\` (в каждом свой `_INDEX.md`):
- `API\` — `SKILL_creojs_api` (Creo.JS/`pfc*`), `SKILL_creo_api_ecosystem` (каналы API) — **critical**
- `DOCS\` — `SKILL_creo_docs_map` (карта документации: хелпы/PDF/API) — **high**
- `CREOSON\` — `SKILL_creoson_workflow`, `SKILL_creoson_complete`, `SKILL_creoson_sessions_workdirs`,
  `SKILL_creo_commands`, `SKILL_creoson_write_rules`, `SKILL_creoson_rename_mechanism`,
  `SKILL_creoson_probe_method`, `SKILL_creoson_inbox_deepseek` — **critical**
- `COPY\` — `SKILL_copy_assembly_project` (умная копия проекта), `SKILL_copy_rename` — **critical**
- `STANDARDS\` — `SKILL_creo_company`, `SKILL_company_config`, `SKILL_naming_spec`, `SKILL_drawings_eskd`,
  `SKILL_creo_templates`, `SKILL_creo_model_nature` (деталь/сборка/производство — `ПАРТИЯ`, мануфакчуринг),
  `SKILL_parameters_guide`, `SKILL_reference_limits`, `SKILL_creo_cards`
- `RELATIONS\` — `SKILL_creo_relations`, `SKILL_relations_constitution`, `SKILL_relations_basics`,
  `SKILL_relations_examples`, `SKILL_curves_from_equation`, `SKILL_curves_examples`,
  `SKILL_spring_compression_generator`, `SKILL_spring_tension_master` — **critical**
- `DAVYDOVKA\` — `SKILL_davydovka_creoson_map` (карта Давыдовка ↔ CREOSON)
- `INFRA\` — `SKILL_creostart_fleet` (флот/старт), `SKILL_object_creoson_tests-01_asm` (объектные пробы)
- корень `repo\` — `SKILL_archive_plm` (**архивы склада `\\Backup\Public\АРХИВЫ` → история в базу
  PLM**: RAR5-многотомники, грабли 7z и правил параметров, карта производства по срезам,
  сверка одноимённых файлов «было → стало, кто и когда», дописывание в боевую базу
  таблицами `arch_*` + `changes(kind='архив')`; конспект `ИЗУЧЕНО\Архивы PLM\STUDY_NOTES.md`) — **high**
- корень `Creo\` — `CREO_MAP` (строение Creo), `SKILLS_MAP` (карта скиллов ветки),
  `SKILL_creo_file_reading` (**чтение файлов Creo «в лоб»**: история изменений, упакованные числа, секции/параметры;
  там же инструмент дома `plm_reader`), `README_jlink_direct`
Карточки моделей — `Creo\cards\`.

### 2. Python / VS Code (Программист, папка Prog\)
*Стандарты кода, тестов и памяти агента; вход направления = эта секция,
собственный индекс-файл Prog\ = долг (см. секцию 7).*
- `Prog\SKILL_python_standard` (Стандарт расчётных скриптов: блоки, суффиксы, аудит) — **critical**
- `Prog\SKILL_tool_template` (Шаблон инструмента дома: своё окно, лог, время работы, README + кнопка
  «README», настройки, слои кнопок, версия в шапке, три руки) — **critical**
- `Prog\SKILL_test_first_rule` (Правило TEST-first) — **critical**
- `Prog\SKILL_settings_audit` (Аудит настроек: поиск по имени ВРЁТ — `model_for`/`get_for`/скрытые `ui=False`/таблицы-призраки; чем чинить и как не обмануть пробой) — **critical**
- `Prog\SKILL_tool_routing` (Маршрутизация запросов; единственная прописка здесь,
  из Core не дублировать) — **critical**
- `Prog\SKILL_agent_memory` (Память агента: что помнить, куда класть)
- `Prog\SKILL_automated_validation` (Автоматические пробы и гейты)
- `Prog\SKILL_code_parsing` (Разбор кода: ast, не regex)
- `Prog\SKILL_cursor_rules_format` (Форматы внешних правил cursor/cline)
- `Prog\\SKILL_prog_local_agent_cline` (Память и выживание в Cline) — **high**

- `Prog\SKILL_diff_and_apply` (Диффы и их применение)
- `Prog\SKILL_repo_mapping` (Карта репо и указатели)
- `Prog\SKILL_unit_testing` (Юнит-пробы на копиях)
- `Prog\SKILL_calc_script_architecture.md` (Архитектура расчётных скриптов;
  переименован 26.09.2026 из `STANDARD Engineering Calculation Script Architecture.md`)
## ДОМЕН 3: Инженерные (оба агента)
| Скилл | Назначение |
|---|---|
| SKILL_materials_reference | справочник материалов (канон) |
| SKILL_engineering_mechanics | сопромат, динамика, усталость |
| SKILL_heat_hydraulics | тепло, гидравлика, пневматика |
| SKILL_casting_hts_master | литьё в ХТС |

## ДОМЕН 4: Производство (зеркало срезов 1С)
| Скилл | Назначение |
|---|---|
| SKILL_production_mirror | производственный контур: склад, входящие, запуск, отгрузки, якорь, время цикла |

### 5. Общее (Core)
*Фундаментальные правила работы агента.*
- **Управление**: 
    - `SKILL_log_management` (Логи и автоуборка) — **долг: файла нет** (аудит 22.09; механику держит tools\agent\log_clean.py)
    - `SKILL_agent_protocol` (Протокол инженера-напарника; живёт в корне репо) — **critical**
    - маршрутизация запросов — см. `Prog\SKILL_tool_routing` — **critical**
- **Контекст**: 
    - `company_conventions.md` (Паспорт КБ: станки, семантика; живое имя без префикса SKILL_)
    - `SKILL_web_vision_limits` (Возможности WEB/Vision)
    - `SKILL_local_agent_cline` (**Выживание в Cline/VS Code**; корень репо) — **critical**
    - `strategy.md` (Журнал развития; живое имя без префикса SKILL_)
    - `SKILL_skill_craft` — **долг: файла нет** (аудит 22.09); был задуман как мета-скилл (Ремесло промтов и скиллов; priority high,
      подгружается по надобности: задача о промтах, скиллах, правилах, шаблонах)
    - `Creo\STANDARDS\SKILL_parameters` (Справочник параметров моделей; перенесён из корня по содержанию 01.10.2026)
    - `DESIGN_davydovka_tokens.md` (токены дизайна Давыдовки для окон и витрины;
      не скилл, а закон дизайна, цитируется .clinerules)
- **Аудит**: `AUDIT_rules_*.md` и `AUDIT\SKILL_audit_protocol.md` (аудит ДОМА)
- **Аудит программы** (не дома): `AUDIT\SKILL_audit_program.md` — **суть**: одна база, одни настройки,
  нет лишнего; карта «куда пишет / откуда читает»; живая проверка всех ручек **включая окно**;
  «тяжёлое» — по факту (время и охват, а не список); мусор выбрасывается сразу (своё и заведомо
  ненужное), чужие данные и единственные копии — нет. Проверено на `plm_reader` 02.10.2026 (V37).
- **Справочники и управленческие файлы** (не скиллы, в маршрутизацию не входят): `GUIDE\db.md`, `GUIDE\models.md`, `GUIDE\plm.md`, `Vericut\VERICUT_отложи_в_Vericut_260820.md`, `Ошибки\ERR_260902_web_fetch.md`, `BACKLOG_tools.md`

### 6. Agents (Автономные исполнители)
*Семь живых файлов, происхождение внешнее; priority normal; подгружаются по надобности; до первой пробы — внешний источник, не закон дома.*
- `agents\rag-architect\SKILL_rag_architect.md` + `agents\rag-architect\references\` (chunking_strategies_comparison.md, embedding_model_benchmark.md, rag_evaluation_framework.md)
- `agents\skill-security-auditor\SKILL_skill_security_auditor.md` + `agents\skill-security-auditor\references\threat-model.md`
- `agents\zero-hallucination-coder\SKILL_zero_hallucination_coder.md`
- `agents\SKILL_authoring_standard.md` (стандарт авторства скиллов; переименован 01.10.2026 — дефис ломал фильтр `skill_*`)
- `AGENT_MAP.md` (**Карта строения агента** `D:\AI\tools\agent`: модули, порт 8765, инструменты,
  данные, ночи и сторож — high; вход по тегам «агент/agent.py/loop/tools_registry/8765»)
- `SKILL_parallel_local_leg.md` — **удалён по слову пользователя 23.09.2026** (спека 113 не оправдала
  формы: правила ноги = долг, если параллельные ноги вернутся). Уроки спеки 113 сироты живут в
  `PROGRESS\PROGRESS_113_orphan_drawings.md`, раздел «ЧЕМУ УЧИТЬ НОГУ».

## ДОМЕН 7: Автогенерируемые (руками не править)
| Файл | Кто пишет |
|---|---|
| Creo/STANDARDS/SKILL_company_config.md | passport_tools (живой паспорт из config.pro) |
| Трейлы/TRAIL_JOURNAL.md | trail_tools |
| Ошибки/ERR_*.md | каталог ошибок |
| Избранное/SKILL_favorites_<user>.md | избранное пользователя (папка gitignored, решение 22.09) |

## ПРАВИЛА МАРШРУТИЗАЦИИ
- Команда CREOSON → creo_commands, детали API → creoson_complete.
- «Как написать relations» → creo_relations (синтаксис) + relations_constitution (правила).
- «Единицы/шаблоны/шифры/параметры/чертежи» → creo_company.
- «Шаблон модели / новая модель / TPL_SOURCE» → creo_templates.
- Код проекта → python_standard + test_first_rule.
- Физика/материалы → Инженерные.
- «Где деталь / когда комплект / якорь / цикл» → production_mirror.
- «Почему вылетаю / как работать в Cline / где что лежит» → SKILL_local_agent_cline (в корне) или Prog\\SKILL_prog_local_agent_cline.

- «Запетлял / встал / повторяю одно и то же» mid-task → §9.3 SKILL_local_agent_cline:
  СТОП → вслух назвать подпись краха → смена метода ИЛИ стоп-отчёт пользователю (помощь снаружи).

## ИСТОЧНИКИ ПРАВДЫ
- DESIGN_davydovka_tokens.md: канон дизайна для новых инструментов. **Долг/проверить: файла в репо нет**
  (аудит 25.09: найден только в копии `D:\AI\log\urn\cline\repo_clone\`), окна дома сейчас строятся без токенов.
- SKILL_tool_template.md → `Prog\SKILL_tool_template.md` — шаблон инструмента дома (создан 25.09.2026, долг закрыт).

### 7. ДОЛГИ И ИДЕИ КАРТЫ (честность: нет файла = нет скилла)
- **PDF**: домен ожил (26.09.2026): вход `PDF\SKILL_pdf_index.md`, рутина
  `PDF\SKILL_pdf_routine.md` (**critical**), контроль пар `PDF\SKILL_pdf_control.md` (**high**).
- **Web**: в папке один сырой файл `260826_1610.md`; довести до Золотого стандарта = долг.
- **Трейлы**: индекс создан 22.09 — `Трейлы\SKILL_trails_index.md` (в гите); журнал `Трейлы/TRAIL_JOURNAL.md` gitignored как операционный поток (пишет trail_tools).
- **Индекс Prog**: закрыт решением 22.09: вход = секция 2, отдельный индекс не создаётся.
- **Creo PDF удалены словом пользователя 22.09; источник восстановления = установка PTC и онлайн-справка, в дом не возвращать без задачи; в гит не входить.**
- **Библиотека `D:\AI\ИЗУЧИТЬ\CREO`**: на 22.09 вечером папки на диске нет (в `ИЗУЧИТЬ` остались ДАВЫДОВКА, Новые правила, Новые правила2); таблица в Creo-индексе отражает утренний замер 1 206 544 066 Б / 17 963 файла — судьбу папки решает пользователь, до его слова строку не переписывать.
- **.gitignore (решение 22.09)**: сведены два поколения; память дома (PROGRESS_*, AUDIT_*, crash/, Трейлы/TRAIL_JOURNAL.md) под гитом не игнорируется; вне гита — secrets.json, users.json, data/, log/, *.db, backup_db/, *.log, *.bak, Избранное/.
- **Журнал Трейлов (решение 22.09)**: `Трейлы/TRAIL_JOURNAL.md` — память дома о том, кто и когда работал в железе; из игнора убран (в remote уже трекается, а ignore против трекнутого файла бессилен).
- **crash\SKILL_crash_reasoning-loop.md**: указатель вместо двойника (тело = plan-loop); удаление только по слову пользователя (22.09).
- **SKILL_architect_reviewer** (идея ниже): **долг: файла нет** (аудит 22.09).
- **Переименование (закрыто 26.09.2026)**: `STANDARD Engineering Calculation Script Architecture.md` →
  `Prog\SKILL_calc_script_architecture.md`; выполнено, ссылки в карте сверены.

## ЗОЛОТОЙ СТАНДАРТ (Golden Standard Template)

Каждый новый скилл должен следовать структуре:
1. **Паспорт (Passport)**: Назначение, priority, когда применять.
2. **Домен (Domain)**: К какому направлению относится.
3. **Привычки (Habits/Rules)**: Конкретные правила работы с этим скиллом (напр. "всегда проверять X перед Y").
4. **Инструменты (Tools/Methods)**: Список методов/команд, которые использует скилл.
5. **Крах-протокол (Crash-Protocol)**: Специфические ошибки и как их фиксировать.
6. **Проба (Probe)**: Как проверить, что скилл работает (Unit tests/Manual checks).
7. **Указатель (Pointer)**: Указатель носит то же имя, что и закон, и живёт по старому пути; тело указателя = одна строка; одноимённость указателя и тела — норма, два одноимённых тела — нарушение (аудит 22.09).

## ИДЕЯ: SKILL_architect_reviewer
Предложение: создание специализированного скилла для аудита соответствия новых скиллов и планов "Золотому стандарту" и "Закону трёх линий".