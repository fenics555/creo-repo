name: creo-index
system: INDEX
description: Use when: задача с темой Creo
when: creo, creoson, parametric, assembly, part, drawing
date: 22.09.2026
ЧТО ЗДЕСЬ: см. раздел «СТРУКТУРА И КАРТА СКИЛЛОВ» ниже — 8 подразделов (API, DOCS, CREOSON, COPY, STANDARDS, RELATIONS, DAVYDOVKA, INFRA).
КОГДА ОТКРЫВАТЬ: теги [CREO], [PARAMETRIC]
КОГДА ПИСАТЬ: CRASH триггеры: SKILL_creoson_probe_method, Ошибки\ERR_creoson_write_ops.md
универсальный закон — MANIFEST.md, специфика среды — в адаптерах

## ГЛАВНОЕ ОТКРЫТИЕ (22.09.2026): один `pfc*` — много каналов; CREOSON = обёртка
Управлять Creo можно **НАПРЯМУЮ, без CREOSON**:
- **Creo.JS** — JS во встроенном браузере Creo (этим идёт Давыдовка);
- **JLINK / Object TOOLKIT Java** — своя Java-программа на `com.ptc.pfc.*` (классы в `pfcasync.jar`)
  сама стартует/подключается к Creo (синхронно/асинхронно);
- **Object TOOLKIT C++ / Pro/TOOLKIT** — нативная DLL внутри процесса Creo (`protk.dat`);
- **VB API**, **Web.Link** — родственные каналы.
**CREOSON = JSON-сервер ПОВЕРХ JLINK**: `creoson-core-3.0.1.jar` = 268 классов
`com.simplifiedlogic.nitro.jlink`, а `com/ptc/pfc` в нём **0**; сами `pfc*` — в `pfcasync.jar`
(1873 класса). Разбор и пробы — `SKILL_creo_api_ecosystem.md`.
**Давыдовка** идёт каналом **Creo.JS** (мост `creojs.js` + серверные `*.creojs`) + свой
Python-сервер на 8000 (не CREOSON и не JLINK) — `SKILL_davydovka_creoson_map.md`.

## СТРУКТУРА (подразделы) И КАРТА СКИЛЛОВ
| Подраздел | Что внутри |
|---|---|
| `API\` | `SKILL_creojs_api.md` (Creo.JS/`pfc*`), `SKILL_creo_api_ecosystem.md` (каналы: OTK/JLINK/VB/Web.Link/CREOSON) |
| `DOCS\` | `SKILL_creo_docs_map.md` (где хелпы/PDF/API-руководства в `D:\PTC\CREO12`) |
| `CREOSON\` | `SKILL_creoson_workflow.md` (цикл, переключение папок), `SKILL_creoson_complete.md` (карта API), `SKILL_creoson_sessions_workdirs.md` (сессии/папки), `SKILL_creo_commands.md` (подбор команды), `SKILL_creoson_write_rules.md` (пишущие), `SKILL_creoson_rename_mechanism.md` (rename), `SKILL_creoson_probe_method.md` (пробы), `SKILL_creoson_inbox_deepseek.md` (долги темы) |
| `COPY\` | `SKILL_copy_assembly_project.md` (умная копия проекта), `SKILL_copy_rename.md` (методика копии/переименования) |
| `STANDARDS\` | `SKILL_creo_company.md`, `SKILL_company_config.md`, `SKILL_naming_spec.md`, `SKILL_drawings_eskd.md`, `SKILL_creo_templates.md`, `SKILL_creo_model_nature.md` (природа модели: деталь/сборка/производство), `SKILL_parameters_guide.md`, `SKILL_reference_limits.md`, `SKILL_creo_cards.md` |
| `RELATIONS\` | `SKILL_creo_relations.md`, `SKILL_relations_constitution.md`, `SKILL_relations_basics.md`, `SKILL_relations_examples.md`, `SKILL_curves_from_equation.md`, `SKILL_curves_examples.md`, `SKILL_spring_compression_generator.md`, `SKILL_spring_tension_master.md` |
| `DAVYDOVKA\` | `SKILL_davydovka_creoson_map.md` (карта Давыдовка ↔ CREOSON) |
| `INFRA\` | `SKILL_creostart_fleet.md` (флот, старт машин), `SKILL_object_creoson_tests-01_asm.md` (объектные пробы) |
| корень | этот индекс + `cards\` (карты моделей, сырые близнецы) |

## КАК ИИ НАХОДИТ СКИЛЛ (правило поиска)
1. Вход — корневой `SKILL_index.md` (домен Creo) → **этот файл**.
2. Здесь — таблица подразделов; идти прямо в файл по пути `Creo\<подраздел>\SKILL_*.md`.
3. Ключевые слова для поиска — в поле `when` шапки каждого скилла.
4. В каждом подразделе есть свой `_INDEX.md` (если агент уже внутри папки).

## ИСТОЧНИКИ ДОКУМЕНТАЦИИ (только чтение)
Все хелпы/PDF/API-руководства — в установке `D:\PTC\CREO12` (полная карта и языки —
`SKILL_creo_docs_map.md`; разбор каналов — `SKILL_creo_api_ecosystem.md`).
Копии-дубли PTC в репо удалены словом пользователя 22.09 (в гит не возвращать); справка — в установке `D:\PTC\CREO12` (карта: `SKILL_creo_docs_map.md`).
Временная папка разбора `D:\AI\ИЗУЧИТЬ\CREO` разбирается и удаляется пользователем — на неё
в скиллах не опираться.
