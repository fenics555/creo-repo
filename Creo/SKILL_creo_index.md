name: creo-index
system: INDEX
description: Use when: задача с темой Creo
when: creo, creoson, parametric, assembly, part, drawing
date: 22.09.2026
ЧТО ЗДЕСЬ: SKILL_creojs_api.md, SKILL_company_config.md, SKILL_creo_docs_map.md, SKILL_creo_api_ecosystem.md, SKILL_copy_assembly_project.md, SKILL_copy_rename.md, SKILL_creoson_complete.md, SKILL_creoson_inbox_deepseek.md, SKILL_creoson_probe_method.md, SKILL_creoson_sessions_workdirs.md, SKILL_creoson_rename_mechanism.md, SKILL_creoson_workflow.md, SKILL_creoson_write_rules.md, SKILL_creostart_fleet.md, SKILL_creo_cards.md, SKILL_creo_commands.md, SKILL_creo_company.md, SKILL_creo_relations.md, SKILL_creo_templates.md, SKILL_curves_examples.md, SKILL_curves_from_equation.md, SKILL_davydovka_creoson_map.md, SKILL_drawings_eskd.md, SKILL_naming_spec.md, SKILL_object_creoson_tests-01_asm.md, SKILL_parameters_guide.md, SKILL_reference_limits.md, SKILL_relations_basics.md, SKILL_relations_constitution.md, SKILL_relations_examples.md, SKILL_spring_compression_generator.md, SKILL_spring_tension_master.md
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

## КАРТА ПО НАПРАВЛЕНИЯМ (что открывать под задачу)
- **Каналы/API**: `SKILL_creo_api_ecosystem.md`, `SKILL_creojs_api.md`.
- **Работа через CREOSON**: `SKILL_creoson_workflow.md` (цикл, переключение папок),
  `SKILL_creoson_complete.md` (карта API), `SKILL_creoson_sessions_workdirs.md` (сессии/папки),
  `SKILL_creo_commands.md` (подбор команды), `SKILL_creoson_write_rules.md` (пишущие),
  `SKILL_creoson_probe_method.md` (безопасные пробы).
- **Копия/переименование**: `SKILL_copy_assembly_project.md` (умная копия проекта),
  `SKILL_copy_rename.md` (методика), `SKILL_creoson_rename_mechanism.md` (механизм).
- **Давыдовка**: `SKILL_davydovka_creoson_map.md`.
- **Документация**: `SKILL_creo_docs_map.md` (где хелпы/PDF/API-руководства).
- **Стандарты КБ**: `SKILL_creo_company.md`, `SKILL_company_config.md`, `SKILL_naming_spec.md`,
  `SKILL_drawings_eskd.md`, `SKILL_creo_templates.md`, `SKILL_parameters_guide.md`,
  `SKILL_reference_limits.md`, `SKILL_creo_cards.md`.
- **Relations / кривые / пружины**: `SKILL_creo_relations.md`, `SKILL_relations_constitution.md`,
  `SKILL_relations_basics.md`, `SKILL_relations_examples.md`, `SKILL_curves_from_equation.md`,
  `SKILL_curves_examples.md`, `SKILL_spring_compression_generator.md`, `SKILL_spring_tension_master.md`.
- **Инфраструктура/флот**: `SKILL_creostart_fleet.md`.
- **Прочее**: `SKILL_creoson_inbox_deepseek.md`, `SKILL_object_creoson_tests-01_asm.md`.

## ИСТОЧНИКИ ДОКУМЕНТАЦИИ (только чтение)
Все хелпы/PDF/API-руководства — в установке `D:\PTC\CREO12` (полная карта и языки —
`SKILL_creo_docs_map.md`; разбор каналов — `SKILL_creo_api_ecosystem.md`).
Копии-дубли PTC в репо удалены словом пользователя 22.09 (в гит не возвращать); справка — в установке `D:\PTC\CREO12` (карта: `SKILL_creo_docs_map.md`).
Временная папка разбора `D:\AI\ИЗУЧИТЬ\CREO` разбирается и удаляется пользователем — на неё
в скиллах не опираться.
