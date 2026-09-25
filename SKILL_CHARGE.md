---
name: CHARGE
system: ЗНАНИЯ
description: Use when: карта скиллов репо — что есть и когда брать (сборка dev\skills_charge.py)
when: карта скиллов, заряд знаний, какие скиллы есть, индекс скиллов
date: 25.09.2026 14:48
---

# ЗАРЯД ЗНАНИЙ АГЕНТА (карта скиллов репо)

**Собрано:** 25.09.2026 14:48 · скиллов: 145

**Как этим пользоваться (агенту).** Это КАРТА: здесь каждый скилл одной строкой — «что это и когда брать».
Тела скиллов в промпт не грузятся: нужный открывается `search_kb` (поиск) или `read_file` (по пути).
Начинать любую задачу Creo — со стартового набора `SKILL_CHARGE_START.md` (он уже в промпте).
Главное направление дома — **Creo/CREOSON**.

## Creo (55)
- `Creo\API\_INDEX.md` — Use when: подраздел API темы Creo — указатель на скиллы · когда: creo, каналы API, pfc, creojs, otk, jlink, vbapi, weblink
- `Creo\API\SKILL_creo_api_ecosystem.md` — Use when: разбор API Creo — один объектный слой pfc* у Creo.JS, Object TOOLKIT (C++/Java), VB API, Web.Link… · когда: OTK, Object TOOLKIT, JLINK, pfc, creojs, vbapi, weblink, otk_methods, jlinkexam…
- `Creo\API\SKILL_creojs_api.md` — Use when: работа с родным API Creo (Creo.JS / pfc*), сверка с CREOSON, разбор механизмов Давыдовки · когда: Creo.JS, creojs, pfc, pfcSession, API, Давыдовка, ListItems, GetParam, ListRows…
- `Creo\COPY\_INDEX.md` — Use when: подраздел COPY темы Creo — указатель на скиллы · когда: creo, копия, переименование, семейства, mfg, проект
- `Creo\COPY\SKILL_copy_assembly_project.md` — Use when: умная копия проекта/сборки через CREOSON (сборка+детали+одноимённые чертежи+спутники _mfg/_wp+экзем… · когда: копия сборки, копия проекта, умная копия, family, семейства, mfg, спутники, tem…
- `Creo\COPY\SKILL_copy_rename.md` — Use when: копия или переименование модели, семейства, сборки (временная папка, Backup, порядок операций) · когда: копия, переименование, Backup, временная папка, семейство, чертёж, mfg, заготов…
- `Creo\CREOSON\_INDEX.md` — (без описания)
- `Creo\CREOSON\SKILL_creo_commands.md` — Use when: быстрый подбор команды CREOSON под задачу · когда: creoson, команда, что вызвать, rename, regenerate, pdf, параметры
- `Creo\CREOSON\SKILL_creoson_complete.md` — (без описания)
- `Creo\CREOSON\SKILL_creoson_inbox_deepseek.md` — Use when: старт разборщика темы CREOSON/ДАВЫДОВКА — здесь остались только ДОЛГИ темы · когда: inbox, deepseek, creoson, davydovka, долги, очередь
- `Creo\CREOSON\SKILL_creoson_pfc_map.md` — Use when: нужно понять, какой метод pfc* стоит за функцией CREOSON (и наоборот) — таблица соответствия из otk… · когда: creoson, pfc, соответствие, mapping, otk_methods, jlink, методы, прямое управле…
- `Creo\CREOSON\SKILL_creoson_probe_method.md` — Use when: живая проба механики CREOSON перед правкой кода или миграцией (гейт механизма) · когда: проба, probe, гейт, CREOSON, сессия, копия, tmp, толькоsession
- `Creo\CREOSON\SKILL_creoson_rename_mechanism.md` — Use when: переименование модели и чертежа через CREOSON (rename, onlysession, General Error) · когда: rename, onlysession, переименование, General Error, чертёж, save, backup, Давыд…
- `Creo\CREOSON\SKILL_creoson_routine.md` — Use when: автоматизация рутины в Creo через CREOSON — практический разбор (зачем, стек, жизненный цикл, групп… · когда: creoson, рутина, автоматизация, без программирования, сценарий, стек, функции…
- `Creo\CREOSON\SKILL_creoson_sessions_workdirs.md` — Use when: старт Creo и CREOSON, сессии (сколько их, какую открыл, как переключаться), рабочие директории, пои… · когда: сессия, session, connect, disconnect, старт Creo, start_creo, рабочий каталог…
- `Creo\CREOSON\SKILL_creoson_workflow.md` — Use when: практическая работа в CREOSON от начала до конца — подключение, рабочие папки и ПЕРЕКЛЮЧЕНИЕ, откры… · когда: creoson, workflow, connect, sessionId, creo:pwd, creo:cd, file:open, file:erase…
- `Creo\CREOSON\SKILL_creoson_write_rules.md` — Use when: пишущие операции через CREOSON (backup, rename, копия моделей) · когда: creoson, backup, rename, копия, async
- `Creo\DAVYDOVKA\_INDEX.md` — Use when: подраздел DAVYDOVKA темы Creo — указатель на скиллы · когда: creo, давыдовка, creojs-приложение, копия сборки, семейства
- `Creo\DAVYDOVKA\SKILL_davydovka_creoson_map.md` — Use when: перенос операций Давыдовки (переименование, копия сборки, семейства, граф) на CREOSON · когда: Давыдовка, копия сборки, семейства, граф, перенос, bom, familytable, drawing, m…
- `Creo\DOCS\_INDEX.md` — Use when: подраздел DOCS темы Creo — указатель на скиллы · когда: creo, документация, справка, help, pdf
- `Creo\DOCS\SKILL_creo_docs_map.md` — Use when: нужна справка/документация Creo — где лежат хелпы, PDF и API-руководства в установке и в доме · когда: документация, справка, help, хелп, PDF, Toolkit, OTK, VB API, Web.Link, Creo.JS…
- `Creo\INFRA\_INDEX.md` — Use when: подраздел INFRA темы Creo — указатель на скиллы · когда: creo, флот, старт машин, логи, объектные пробы
- `Creo\INFRA\SKILL_creostart_fleet.md` — Use when: вопросы про старт машин КБ, CREO-START, логи, трейлы, · когда: Use when: вопросы про старт машин КБ, CREO-START, логи, трейлы,
- `Creo\INFRA\SKILL_object_creoson_tests-01_asm.md` — Use when: вопросы об объекте creoson_tests-01.asm и создание похожих · когда: Use when: вопросы об объекте creoson_tests-01.asm и создание похожих
- `Creo\LIT\SKILL_lit_analysis_patterns.md` — Шаблоны и best practices для Relations в Creo Parametric при литье. Содержит проверенные алгоритмы расчета st… · когда: relations, liatie, hts, shrinkage, weiver, pattern, черновик, оптимизация
- `Creo\LIT\SKILL_lit_hts_aws.md` — (без описания)
- `Creo\LIT\SKILL_lit_hts_china.md` — (без описания)
- `Creo\LIT\SKILL_lit_hts_en.md` — (без описания)
- `Creo\LIT\SKILL_lit_hts_patents_summary.md` — (без описания)
- `Creo\LIT\SKILL_lit_hts_patents_summary_ru.md` — (без описания)
- `Creo\LIT\SKILL_lit_hts_turkey.md` — (без описания)
- `Creo\LIT\SKILL_lit_troubleshooting.md` — Справочник по диагностике и устранению типичных ошибок при работе с Relations в Creo Parametric для литья. Со… · когда: relations, liatie, hts, ошибки, крахи, отладка, debug
- `Creo\RELATIONS\_INDEX.md` — Use when: подраздел RELATIONS темы Creo — указатель на скиллы · когда: creo, relations, уравнения, кривые, пружины
- `Creo\RELATIONS\SKILL_creo_relations.md` — Relations в Creo: синтаксис, функции, лимиты, примеры (справочник). Правила — в SKILL_relations_constitution · когда: relations, уравнения, синтаксис, функции, операторы, IF ENDIF, FOR, d-имена, ли…
- `Creo\RELATIONS\SKILL_curves_examples.md` — ГОТОВЫЕ РЕЦЕПТЫ КРИВЫХ ИЗ УРАВНЕНИЯ (НАШИ ЗАДАЧИ) · когда: спираль пружины, эвольвента, конус, синусоида
- `Creo\RELATIONS\SKILL_curves_from_equation.md` — КРИВЫЕ ИЗ УРАВНЕНИЯ В CREO PARAMETRIC (CURVE FROM EQUATION) · когда: кривая из уравнения, системы координат, радианы градусы
- `Creo\RELATIONS\SKILL_relations_basics.md` — ОТНОШЕНИЯ (УРАВНЕНИЯ) В CREO PARAMETRIC — БАЗА · когда: что такое отношения, d-имена, где писать уравнения
- `Creo\RELATIONS\SKILL_relations_constitution.md` — Железные правила написания и проверки relations: строки, имена, блоки, описания, порядок · когда: relations, уравнения, чекер, написать relations, проверить relations, именовани…
- `Creo\RELATIONS\SKILL_relations_examples.md` — ПРАКТИЧЕСКИЕ ПРИМЕРЫ ОТНОШЕНИЙ (НАШИ ДЕТАЛИ) · когда: примеры отношений, масса на чертеж, обозначение, параметры сборки
- `Creo\RELATIONS\SKILL_spring_compression_generator.md` — ГЕНЕРАТОР КОДА — Пружина сжатия (Creo Relations) · когда: пружина сжатия, сжатие, compression spring, relations, код пружины
- `Creo\RELATIONS\SKILL_spring_tension_master.md` — ЭТАЛОН: Пружина растяжения (Tension Spring). ГОСТ 13766. · когда: пружина растяжения, крючки, начальное натяжение, tension
- `Creo\SKILL_creo_directions_mfg_gdt.md` — Use when: разбор направлений Creo — ЧПУ-синтаксис (mfg_cmdsyn), GD&T Advisor, ключевые методы pfcSolid/pfcFea… · когда: mfg_cmdsyn, cmdsyn, чпу, циклы, GD&T, gdt_home, pfcSolid, pfcFeature, направлен…
- `Creo\SKILL_creo_file_reading.md` — Use when: надо прочитать данные модели/чертежа Creo НАПРЯМУЮ из файла (без запуска Creo и без CREOSON) — исто… · когда: читать файл Creo в лоб, .prt .asm .drw изнутри, история файла, mtrack, ревизия…
- `Creo\SKILL_creo_index.md` — Use when: задача с темой Creo · когда: creo, creoson, parametric, assembly, part, drawing
- `Creo\SKILL_creo_jlink_direct.md` — Use when: нужно УПРАВЛЯТЬ Creo напрямую из программы (Java/JLINK, pfc*), без CREOSON — подключиться к Creo, п… · когда: jlink, j-link, java, pfcasync, pfc, otk_java_free, прямое управление, программк…
- `Creo\STANDARDS\_INDEX.md` — Use when: подраздел STANDARDS темы Creo — указатель на скиллы · когда: creo, стандарты КБ, имена, шаблоны, чертежи, параметры, карточки
- `Creo\STANDARDS\SKILL_company_config.md` — Creo · когда: company-config
- `Creo\STANDARDS\SKILL_creo_cards.md` — Use when: карточка модели Creo (D:\AI\repo\Creo\cards) — аудит отношений, параметры, massprops, сырой близнец · когда: карточка, cards, аудит, liteika, параметры модели, сырой близнец, crc32, masspr…
- `Creo\STANDARDS\SKILL_creo_company.md` — Паспорт компании для Creo: единицы mmks, шаблоны, шифры, обязательные параметры, чертежи ЕСКД, массовые MP_ · когда: единицы, mmks, шаблоны, шифр, обязательные параметры, rel_model_name, МАТ_MARK…
- `Creo\STANDARDS\SKILL_creo_model_nature.md` — Use when: определяешь природу модели (деталь / сборка / производство-мануфакчуринг) или правишь параметр ТИП… · когда: ТИП, тип модели, производство, мануфакчуринг, ПАРТИЯ, чесалка, typcheck, оснаст…
- `Creo\STANDARDS\SKILL_creo_templates.md` — Канон-шаблоны моделей: свидетельство о рождении TPL_SOURCE, отношения-минимум, секции спецификации · когда: шаблон, новая модель, канон, TPL_SOURCE, начать модель, секция спецификации, св…
- `Creo\STANDARDS\SKILL_drawings_eskd.md` — Чертежи по ЕСКД/ГОСТ: MY_ESKD.dtl, шаблоны, даты, допуски, переименование, шифры, папки проектов · когда: чертёж, шаблон, ЕСКД, ГОСТ, оформление чертежа, дата, допуски, шифр, номер черт…
- `Creo\STANDARDS\SKILL_naming_spec.md` — ИМЕНА, ШИФРЫ и ОБЯЗАТЕЛЬНЫЕ ПАРАМЕТРЫ модели: rel_model_name, МАТ_MARK, MASS, ТИП · когда: имя модели, шифр, rel_model_name, ТИП, МАТ_MARK, переименование, rename, обязат…
- `Creo\STANDARDS\SKILL_parameters_guide.md` — ПАРАМЕТРЫ И МАССОВЫЕ ХАРАКТЕРИСТИКИ CREO · когда: параметры, MP_MASS, массовые, вывод на чертеж
- `Creo\STANDARDS\SKILL_reference_limits.md` — CREO REFERENCE — ЛИМИТЫ, СИНТАКСИС, ФУНКЦИИ (Help 12.4.2.0, выверено) · когда: лимиты, длина имени, степень, ROUND, синтаксис IF

## PDF (3)
- `PDF\SKILL_pdf_control.md` — Use when: нужно проверить PDF-хозяйство — дубли PDF, PDF не рядом со своим чертежом, PDF без модели (документ… · когда: дубли pdf, не рядом, pdf без модели, документация, корзина инструмента, пары, c…
- `PDF\SKILL_pdf_index.md` — Use when: задача с темой PDF · когда: pdf, pdf_tools, pdf_img, extraction, rendering
- `PDF\SKILL_pdf_routine.md` — Use when: нужно вывести или ОБНОВИТЬ PDF чертежа Creo (главная рутина дома) — правила, конфиг оформления, инс… · когда: pdf, чертёж, drw, вывод pdf, обновить pdf, перепечать, форматки, MY_ESKD, table…

## Web (1)
- `Web\SKILL_web_index.md` — Use when: задача с темой Web · когда: web, html, css, js, api, scraping

## Инженерные (5)
- `Инженерные\SKILL_casting_hts_master.md` — Блочный мастер расчёта литья в ХТС: ЛПС, прибыли, холодильники, ТО, экономика; сценарные ключи и паспорт спла… · когда: литьё, ХТС, отливка, стояк, шлакоуловитель, питатель, прибыль, Чворинов, усадка…
- `Инженерные\SKILL_engineering_index.md` — Use when: задача с темой Инженерные · когда: engineering, materials, mechanics, hydraulics, casting
- `Инженерные\SKILL_engineering_mechanics.md` — Сопромат, динамика, усталость: изгиб, кручение, устойчивость, контактные напряжения, критические частоты · когда: изгиб, кручение, прогиб, момент инерции, устойчивость, Эйлер, запас прочности…
- `Инженерные\SKILL_heat_hydraulics.md` — Теплопередача, гидравлика, пневматика: конвекция, излучение, охлаждение, расход, цилиндры, подбор насосов · когда: тепло, температура, нагрев, охлаждение, конвекция, излучение, тепловой поток, д…
- `Инженерные\SKILL_materials_reference.md` — Справочник материалов: стали пружинные/конструкционные/нерж., чугуны, алюминий, бронзы, пластики · когда: материал, сталь, чугун, алюминий, бронза, плотность, модуль упругости, предел п…

## Трейлы (1)
- `Трейлы\SKILL_trails_index.md` — Use when: задача о трейлах — журнал сессий, кто работал, болезни, прогнозы · когда: трейл, журнал, сессия, кто открывал

## Ошибки (5)
- `Ошибки\ERR_260819_stdlib_code.md` — (без описания) · когда: module code has no attribute handle, AttributeError, блок не работает, конфликт…
- `Ошибки\ERR_260902_web_fetch.md` — (без описания)
- `Ошибки\ERR_creoson.md` — Use when: ошибка, ERR, Traceback, «не удалось», сбой Creo/CREOSON/агента — поиск причины и проверенного лечен… · когда: ошибка error err traceback сбой лечение неисправность rename backup
- `Ошибки\ERR_creoson_write_ops.md` — Use when: пишущая операция CREOSON упала — backup без target_dir, rename General Error · когда: backup, target_dir, rename, General Error, CREOSON, запись, async
- `Ошибки\SKILL_errors.md` — Use when: ошибка, сбой, ERR, Traceback, «не работает» — карта базы ошибок и правила добавления · когда: ошибка error err traceback сбой лечение неисправность

## crash (46)
- `crash\crash_appjs-syntaxerror-no-uicheck.md` — Use when: правка app.js/index.html ушла без пробы консоли — синтаксическая ошибка живёт до первой проверки · когда: appjs, syntaxerror, ui_check, console, javascript
- `crash\crash_deleted-house-file-without-word.md` — Use when: домовой файл (напр. harvest_gui.py) удалён вне data\tmp и data\backup без прямого слова пользователя · когда: delete, harvest_gui, house-file, manual-deletion
- `crash\crash_loop_perception.md` — Use when: исполнитель принимает череду мелких нужных шагов (инвентаризация, Select-String, проверки путей) за… · когда: loop, perception, false loop, inventory, stuck, REVIVE, кажется цикл
- `crash\crash_reasoning-loop.md` — Use when the agent gets stuck in a loop of repetitive, failing tool calls or reasoning without making progres… · когда: loop, repeat, reasoning, same-parameters
- `crash\SKILL_agent-frozen.md` — (без описания)
- `crash\SKILL_crash-editor-mismatch.md` — Use when: editor падает с «text not found» из-за расхождения old_text после частичной правки или смены контек… · когда: editor-mismatch, text not found, mismatch, old_text mismatch
- `crash\SKILL_crash_agent-duplicate-restart-race.md` — Use when: после рестарта агента живы ДВА python agent.py и на порту два LISTENING — рестарт среагировал в гон… · когда: agent restart, duplicate process, double start, ctl watch, race, SO_REUSEADDR…
- `crash\SKILL_crash_agent_corruption.md` — (без описания) · когда: crash_agent_corruption
- `crash\SKILL_crash_agent_silence.md` — Use when: исполнитель «завис» — сообщение кончилось рассуждением без вызова инструмента, IDE видит простой, п… · когда: silence, hang, stall, no tool call, завис, стоял, замирал
- `crash\SKILL_crash_analysis_search_codebase.md` — Use when: search_codebase падает с ошибкой миграции контекста или повторяется · когда: Use when: search_codebase падает с ошибкой миграции контекста или повторяется
- `crash\SKILL_crash_cline_longsession_context_death.md` — Use when: окно Cline умирает молча после длинной сессии на шаге генерации длинного ответа · когда: cline, вылет, context, longsession, компакция, papers, прогресс
- `crash\SKILL_crash_command-30s-timeout.md` — Use when: run_commands падает с "Command timed out after 30000ms" — таймаут · когда: Use when: run_commands падает с "Command timed out after 30000ms" — таймаут
- `crash\SKILL_crash_constitution.md` — Документ рамок вылетов — правило, шаблон экземпляра, шаблон передачи, блок имён. · когда: Документ рамок вылетов — правило, шаблон экземпляра, шаблон передачи, блок имён.
- `crash\SKILL_crash_context-limit-interruption.md` — (без описания) · когда: crash_context-limit-interruption
- `crash\SKILL_crash_ctl-inline-stderr-truncated.md` — Use when: рестарт или проба агента через инлайн python -c в PowerShell гибнет · когда: Use when: рестарт или проба агента через инлайн python -c в PowerShell гибнет
- `crash\SKILL_crash_destructive-probe-rerun.md` — Use when: разрушительная проба (kill_creo, delete, erase, перезапись) исполнена ПОВТОРНО из оставшегося в tmp… · когда: kill_creo, destructive, probe, rerun, tmp, повтор, разрушительная проба, Creo
- `crash\SKILL_crash_editor-create-overwrote.md` — Use when: вызов editor/write_file в режиме create на СУЩЕСТВУЮЩЕМ файле перезаписал его начисто и убил тело (… · когда: editor, create, overwrite, lost content, усох файл, потерян скилл
- `crash\SKILL_crash_editor-studycheck-halfedit-undefined-name.md` — Use when: файл после правки ссылается на имя, которого нет (NameError), потому что правка оборвана до объявле… · когда: halfedit, undefined name, nameerror, skill2, study_check, оборванная правка, по…
- `crash\SKILL_crash_editor-text-not-found.md` — Use when: editor не находит точный old_text, хотя при чтении текст совпадает · когда: editor, text-not-found, mismatch
- `crash\SKILL_crash_editor_context_mismatch.md` — Use when: editor падает из-за несовпадения текста или лимита размера при крупных правках · когда: editor, mismatch, large, text, too_large
- `crash\SKILL_crash_editor_too_large_and_non_unique_anchors.md` — Use when: editor падает из-за размера файла > 6 КБ или нескольких совпадений old_text · когда: editor, too_large, multiple_matches, non_unique_anchor
- `crash\SKILL_crash_execution-loop.md` — Use when: агент зацикливается в попытках исправить ошибку, повторяя одну и ту же неудачную команду или исполь… · когда: "зациклился", "execution loop", "repeating failed command", "tooling loop"
- `crash\SKILL_crash_git_commit-sweeps-foreign-staged.md` — Use when: коммит без pathspec в доме с параллельными ногами уносит чужую застейдженную работу в свой коммит · когда: git, commit, staged, foreign work, pathspec, parallel legs, house
- `crash\SKILL_crash_git_parallel-leg-rebase-reverts-worktree.md` — Use when: параллельная нога делает rebase — рабочее дерево откатывается (структура/правки исчезают), своя раб… · когда: git, rebase, parallel leg, stash, worktree revert, чужая нога, параллельная ног…
- `crash\SKILL_crash_handling.md` — Use when: петля или зависание из-за лимитов инструментов (editor too large, длинные цепочки run_commands, edi… · когда: crash handling, tool limits, editor too large, run_commands chain, loop, hang
- `crash\SKILL_crash_index.md` — Список всех крах-скиллов папки crash (навигация); вход в тему — SKILL_crash_constitution.md · когда: крах, crash, список крахов, какой скилл, навигация по крахам
- `crash\SKILL_crash_login-stale-memory.md` — Use when: вход в агента не проходит при верном пароле — три источника правды · когда: Use when: вход в агента не проходит при верном пароле — три источника правды
- `crash\SKILL_crash_loop_economy_failure.md` — Use when: нога в петле на лимите editor - «экономия» из спеки истолкована как разрешение не читать и не дроби… · когда: economy loop, editor limit, orphan_scan, экономия, петля, limit exceeded
- `crash\SKILL_crash_missing-temp-artifacts.md` — Use when: временные артефакты tmp потеряны к моменту, когда нужны следующему шагу · когда: missing temp artifacts, tmp loss, lost files, anchor
- `crash\SKILL_crash_omission_of_revive_protocol.md` — Use when: пропуск обязательных шагов ритуала (чтение скилла и строка-доказательство) при REVIVE или крахе · когда: revive, omission, ритуал, строка-доказательство
- `crash\SKILL_crash_pdf-roots-two-lists.md` — Поиск PDF пуст при живых парах в базе знаний (сравнение scan_roots и kb_roots) · когда: pdf-search-empty, roots-mismatch, scan_roots
- `crash\SKILL_crash_plan-loop-replan-no-exec.md` — один и тот же план три и более раз в рассуждениях без исполнения · когда: plan, loop, replan, no-exec
- `crash\SKILL_crash_protocol_omission.md` — Use when: пропуск обязательной записи крах-скилла — ритуал краха выполнен частично · когда: protocol_omission, пропуск скилла, ритуал краха, диагностика без скилла
- `crash\SKILL_crash_quoted-escape-parse-failure.md` — ParseException «Отсутствует имя типа после знака "["» на \" внутри массива run_commands · когда: run_commands, quoted, escape, parse-failure
- `crash\SKILL_crash_readfiles_outdated_loop.md` — Use when: `read_files` в цикле возвращает `[outdated - see the latest file content]` · когда: readfiles, outdated, loop, tool-loop
- `crash\SKILL_crash_reasoning-loop.md` — (без описания)
- `crash\SKILL_crash_regex_extraction_triple_quote_loop.md` — Use when: бесконечный цикл при regex-извлечении блоков кода в тройных кавычках (agent.py) · когда: regex, extraction, loop, triple_quote, regex_extraction
- `crash\SKILL_crash_runcommands-copy-race-fake-parameter.md` — Use when: после Copy-Item мгновенный Get-Content падает PathNotFound (гонка · когда: Use when: после Copy-Item мгновенный Get-Content падает PathNotFound (гонка
- `crash\SKILL_crash_runcommands_kill-by-name-house-services.md` — Use when: остановка процесса по ИМЕНИ (Stop-Process -Name / taskkill /IM) в доме — сносит ЧУЖИЕ сервисы дома · когда: Stop-Process, -Name, taskkill, /IM, kill by name, python, house services, порты…
- `crash\SKILL_crash_scheduler-fire-skip.md` — Use when: задача планировщика с триггером повторения не стартует в расчётный · когда: Use when: задача планировщика с триггером повторения не стартует в расчётный
- `crash\SKILL_crash_searchcodebase-any-pattern-migration-marker.md` — Use when: search_codebase возвращает маркер миграции · когда: Use when: search_codebase возвращает маркер миграции
- `crash\SKILL_crash_searchcodebase-multipattern-migration-marker.md` — Use when: search_codebase с 3+ regex-паттернами возвращает маркер миграции · когда: Use when: search_codebase с 3+ regex-паттернами возвращает маркер миграции
- `crash\SKILL_crash_searchcodebase-timeout.md` — Use when: search_codebase зависает/таймаут или возвращает маркер миграции вместо результатов · когда: search_codebase, timeout, migration marker, result missing, hang
- `crash\SKILL_crash_session-interruption.md` — Use when: потеря сессии, обрыв связи, генерация оборвана на полуслове · когда: session_loss, interruption, connection_error, timeout
- `crash\SKILL_crash_sleep-poll-loop-after-timeout.md` — Use when: исполнитель после таймаута run_commands (30 с) ждёт детач-процесс повторными опросами «Start-Sleep… · когда: sleep-poll, петля опросов, детач-процесс, Start-Sleep, таймаут 30с, зацикливани…
- `crash\SKILL_editor_too_large.md` — Use when: editor отказывает «Editor input too large» — блок new_text выше лимита (~6000 символов) · когда: editor, too large, new_text, limit, chunking, якорь

## Prog (13)
- `Prog\SKILL_agent_memory.md` — (без описания)
- `Prog\SKILL_agent_protocol.md` — (без описания)
- `Prog\SKILL_automated_validation.md` — (без описания)
- `Prog\SKILL_code_parsing.md` — (без описания)
- `Prog\SKILL_cursor_rules_format.md` — (без описания)
- `Prog\SKILL_diff_and_apply.md` — (без описания)
- `Prog\SKILL_editor_too_large.md` — (без описания)
- `Prog\SKILL_local_agent_cline.md` — (без описания)
- `Prog\SKILL_python_standard.md` — (без описания)
- `Prog\SKILL_repo_mapping.md` — (без описания)
- `Prog\SKILL_test_first_rule.md` — (без описания)
- `Prog\SKILL_tool_routing.md` — (без описания)
- `Prog\SKILL_unit_testing.md` — (без описания)

## Прочее (16)
- `agents\rag-architect\SKILL_rag_architect.md` — "Use when the user asks to design a RAG pipeline, choose a chunking strategy or embedding model, pick a vecto… · когда: "Use when the user asks to design a RAG pipeline, choose a chunking strategy or…
- `agents\skill-security-auditor\SKILL_skill_security_auditor.md` — > · когда: >
- `agents\zero-hallucination-coder\SKILL_zero_hallucination_coder.md` — "Runs a disciplined Discuss -> Map -> Decompose -> Execute -> Verify loop that grounds code in verified struc… · когда: "Runs a disciplined Discuss -> Map -> Decompose -> Execute -> Verify loop that…
- `data\backup\pre_lang_fix\SKILL_crash-editor-mismatch.md` — Use when: editor tool fails with "text not found" due to old_text mismatch after a partial update or context… · когда: editor-mismatch, text not found, mismatch, old_text mismatch
- `data\backup\pre_lang_fix\SKILL_crash_editor_too_large_and_non_unique_anchors.md` — Use when editor fails due to file size > 6KB or multiple matches found for old_text. · когда: editor, too_large, multiple_matches, non_unique_anchor
- `data\backup\pre_lang_fix\SKILL_crash_omission_of_revive_protocol.md` — (без описания) · когда: crash_omission_of_revive_protocol
- `data\backup\pre_lang_fix\SKILL_crash_protocol_omission.md` — (без описания) · когда: crash_protocol_omission
- `data\backup\pre_lang_fix\SKILL_crash_session-interruption.md` — Use when: session loss, connection interrupted, AI stopped generating mid-sentence · когда: session_loss, interruption, connection_error, timeout
- `SKILL_agent_protocol.md` — (без описания)
- `SKILL_audit_protocol.md` — (без описания)
- `SKILL_culture_files.md` — Use when: куда положить логи, отчёты, временные файлы и конспект изучения; где правила хранения, сроки и как… · когда: культура, куда класть, логи, отчёты, урна, временное, конспект, изучение, reten…
- `SKILL_index.md` — Карта всех скиллов репо по доменам: что где лежит и куда смотреть · когда: навигация, где что, карта скиллов, список скиллов, какой скилл, домены
- `SKILL_local_agent_cline.md` — Use when: локальная модель ИИ работает в VS Code / Cline — как не вылетать, как жить в 131k контексте, где чт… · когда: Cline, локальная модель, gemma, выживание, вылет, контекст, транспорт, редактор…
- `SKILL_parameters.md` — (без описания)
- `SKILL_production_mirror.md` — Производственный контур из срезов 1С: склад, входящие, запуск, отгрузки, составы; якорь и время цикла · когда: где деталь, склад, входящие, запуск, этап, отгрузки, кто заказывал, сколько изг…
- `SKILL_web_vision_limits.md` — Что WEB (чтение сайтов) и ВИЗИЯ (чтение картинок) умеют и НЕ умеют — чтобы не выдумывать содержимое · когда: web, сайт, ссылка, читать страницу, скриншот, картинка, визия, изображение, web…
