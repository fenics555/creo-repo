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
- Creo: Creo\SKILL_creo_index.md · PDF: PDF\SKILL_pdf_index.md · Web: Web\SKILL_web_index.md
- Инженерные: Инженерные\SKILL_engineering_index.md · Трейлы: Трейлы\SKILL_trails_index.md
- Ошибки: Ошибки\SKILL_errors.md · Крахи: crash\SKILL_crash_constitution.md (закон) + crash\SKILL_crash_index.md (список крах-скиллов)

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
Карточки моделей — `Creo\cards\`.

### 2. Python / VS Code (Программист, папка Prog\)
*Стандарты кода, тестов и памяти агента; вход направления = эта секция,
собственный индекс-файл Prog\ = долг (см. секцию 7).*
- `Prog\SKILL_python_standard` (Стандарт расчётных скриптов: блоки, суффиксы, аудит) — **critical**
- `Prog\SKILL_test_first_rule` (Правило TEST-first) — **critical**
- `Prog\SKILL_tool_routing` (Маршрутизация запросов; единственная прописка здесь,
  из Core не дублировать) — **critical**
- `Prog\SKILL_agent_memory` (Память агента: что помнить, куда класть)
- `Prog\SKILL_automated_validation` (Автоматические пробы и гейты)
- `Prog\SKILL_code_parsing` (Разбор кода: ast, не regex)
- `Prog\SKILL_cursor_rules_format` (Форматы внешних правил cursor/cline)
- `Prog\SKILL_diff_and_apply` (Диффы и их применение)
- `Prog\SKILL_repo_mapping` (Карта репо и указатели)
- `Prog\SKILL_unit_testing` (Юнит-пробы на копиях)
- `STANDARD Engineering Calculation Script Architecture.md` (Архитектура расчётных
  скриптов; прописан под живым именем из корня, переименование = долг секции 7)
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
    - `SKILL_parameters` (Справочник параметров; «дикий», интегрирован 22.09)
    - `DESIGN_davydovka_tokens.md` (токены дизайна Давыдовки для окон и витрины;
      не скилл, а закон дизайна, цитируется .clinerules)
- **Аудит**: `AUDIT_rules_*.md` и `SKILL_audit_protocol.md`
- **Справочники и управленческие файлы** (не скиллы, в маршрутизацию не входят): `GUIDE\db.md`, `GUIDE\models.md`, `GUIDE\plm.md`, `Vericut\VERICUT_отложи_в_Vericut_260820.md`, `Ошибки\ERR_260902_web_fetch.md`, `BACKLOG_tools.md`

### 6. Agents (Автономные исполнители)
*Семь живых файлов, происхождение внешнее; priority normal; подгружаются по надобности; до первой пробы — внешний источник, не закон дома.*
- `agents\rag-architect\SKILL_rag_architect.md` + `agents\rag-architect\references\` (chunking_strategies_comparison.md, embedding_model_benchmark.md, rag_evaluation_framework.md)
- `agents\skill-security-auditor\SKILL_skill_security_auditor.md` + `agents\skill-security-auditor\references\threat-model.md`
- `agents\zero-hallucination-coder\SKILL_zero_hallucination_coder.md`
- `agents\SKILL-AUTHORING-STANDARD.md` (стандарт авторства скиллов)
- `AGENT_MAP.md` (**Карта строения агента** `D:\AI\tools\agent`: модули, порт 8765, инструменты,
  данные, ночи и сторож — high; вход по тегам «агент/agent.py/loop/tools_registry/8765»)
- `SKILL_parallel_local_leg.md` — **удалён по слову пользователя 23.09.2026** (спека 113 не оправдала
  формы: правила ноги = долг, если параллельные ноги вернутся). Уроки спеки 113 сироты не потеряны:
  живут в `PROGRESS_spec113.md`, раздел «ЧЕМУ УЧИТЬ НОГУ»; в `SPEC_113_orphan_drawings.md` (строки 43, 71)
  ссылки на удалённый скилл — висячие, сама спека по закону не правится.

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
- «Почему вылетаю / как работать в Cline / где что лежит» → SKILL_local_agent_cline (в корне).
- «Запетлял / встал / повторяю одно и то же» mid-task → §9.3 SKILL_local_agent_cline:
  СТОП → вслух назвать подпись краха → смена метода ИЛИ стоп-отчёт пользователю (помощь снаружи).

## ИСТОЧНИКИ ПРАВДЫ
- DESIGN_davydovka_tokens.md: канон дизайна для новых инструментов.
- SKILL_tool_template.md: шаблон создания трёхрукого инструмента — **долг: файла нет** (аудит 22.09).

### 7. ДОЛГИ И ИДЕИ КАРТЫ (честность: нет файла = нет скилла)
- **PDF**: домен пуст; скиллы перепечати, миниатюр и реестра родятся из практики
  pdf_tools.py и спеки 104 — долг оживления направления.
- **Web**: в папке один сырой файл `260826_1610.md`; довести до Золотого стандарта = долг.
- **Трейлы**: индекс создан 22.09 — `Трейлы\SKILL_trails_index.md` (в гите); журнал `Трейлы/TRAIL_JOURNAL.md` gitignored как операционный поток (пишет trail_tools).
- **Prog\SKILL_prog_index.md**: закрыт решением 22.09: вход = секция 2, индекс не создаётся.
- **Creo PDF удалены словом пользователя 22.09; источник восстановления = установка PTC и онлайн-справка, в дом не возвращать без задачи; в гит не входить.**
- **Библиотека `D:\AI\ИЗУЧИТЬ\CREO`**: на 22.09 вечером папки на диске нет (в `ИЗУЧИТЬ` остались ДАВЫДОВКА, Новые правила, Новые правила2); таблица в Creo-индексе отражает утренний замер 1 206 544 066 Б / 17 963 файла — судьбу папки решает пользователь, до его слова строку не переписывать.
- **.gitignore (решение 22.09)**: сведены два поколения; память дома (PROGRESS_*, SPEC_*, AUDIT_*, crash/, Трейлы/TRAIL_JOURNAL.md) под гитом не игнорируется; вне гита — secrets.json, users.json, data/, log/, *.db, backup_db/, *.log, *.bak, Избранное/.
- **Журнал Трейлов (решение 22.09)**: `Трейлы/TRAIL_JOURNAL.md` — память дома о том, кто и когда работал в железе; из игнора убран (в remote уже трекается, а ignore против трекнутого файла бессилен).
- **crash\SKILL_crash_reasoning-loop.md**: указатель вместо двойника (тело = plan-loop); удаление только по слову пользователя (22.09).
- **SKILL_architect_reviewer** (идея ниже): **долг: файла нет** (аудит 22.09).
- **Переименование**: `STANDARD Engineering Calculation Script Architecture.md` →
  `Prog\SKILL_calc_script_architecture.md` — по слову пользователя, со сверкой ссылок.

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

