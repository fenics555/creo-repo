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
- Ошибки: Ошибки\SKILL_errors.md · Крахи: crash\SKILL_crash_constitution.md

### 1. Creo (Веб-агент, Инженер)
*Специализация на работе с CAD-системой через API и интерфейсы.*
- **API & Механизмы**: 
    - `SKILL_creoson_complete` (API CREOSON) — **critical**
    - `SKILL_creojs_api` (Creo.JS / pfc*) — **critical**
    - `SKILL_creoson_sessions_workdirs` (Сессии, директории) — **critical**
    - `SKILL_creoson_rename_mechanism` (Переименование) — **critical**
    - `SKILL_creoson_probe_method` (Безопасные пробы) — **critical**
    - `Creo\SKILL_object_creoson_tests-01_asm` (Объектные пробы CREOSON на сборках) — **normal**
    - `SKILL_creo_commands` (Подбор команд)
    - `SKILL_creo_relations` & `SKILL_relations_constitution` (Relations/Связи) — **critical**
    - `SKILL_curves_from_equation` & `SKILL_curves_examples` (Кривые)
- **Стандарты КБ**:
    - `SKILL_creo_company` (Паспорт: единицы, шаблоны, чертежи ЕСКД)
    - `SKILL_creo_templates` (Канон-шаблоны моделей)
- **Пробы и тесты** (интеграция «диких» 22.09):
    - `SKILL_object_creoson_tests-01_asm` (Объектные пробы CREOSON на сборках;
      пробы гонять по SKILL_creoson_probe_method)
- **Генераторы**:
    - `SKILL_spring_compression_generator` / `SKILL_spring_tension_master` (Пружины)

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

## ДОМЕН 7: Автогенерируемые (руками не править)
| Файл | Кто пишет |
|---|---|
| Creo/SKILL_company_config.md | passport_tools (живой паспорт из config.pro) |
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

## ИСТОЧНИКИ ПРАВДЫ
- DESIGN_davydovka_tokens.md: канон дизайна для новых инструментов.
- SKILL_tool_template.md: шаблон создания трёхрукого инструмента — **долг: файла нет** (аудит 22.09).

### 7. ДОЛГИ И ИДЕИ КАРТЫ (честность: нет файла = нет скилла)
- **PDF**: домен пуст; скиллы перепечати, миниатюр и реестра родятся из практики
  pdf_tools.py и спеки 104 — долг оживления направления.
- **Web**: в папке один сырой файл `260826_1610.md`; довести до Золотого стандарта = долг.
- **Трейлы**: индекс создан 22.09 — `Трейлы\SKILL_trails_index.md` (в гите); журнал `Трейлы/TRAIL_JOURNAL.md` gitignored как операционный поток (пишет trail_tools).
- **Prog\SKILL_prog_index.md**: закрыт решением 22.09: вход = секция 2, индекс не создаётся.
- **Избранное/**: gitignored решением 22.09: личное автогенерируемое пользователя, не память дома; `Трейлы/TRAIL_JOURNAL.md` gitignored как операционный поток, индекс направления в гите.
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

