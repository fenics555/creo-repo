---
name: index
system: общее
description: Карта всех скиллов репо по доменам: что где лежит и куда смотреть
when: навигация, где что, карта скиллов, список скиллов, какой скилл, домены
priority: critical
date: 13.11.2026
---

# КАРТА СКИЛЛОВ РЕПО (D:\AI\repo)
Один скилл = одна зона знания. Домены не дублируют друг друга. Ищи нужный раздел поиском (`Select-String`), не читай карту целиком без необходимости.

## ОПРЕДЕЛЕНИЕ ТЕРМИНА
**СКИЛЛ** (в этом доме) = **файл с именем `SKILL_*.md`** внутри репо (без папок `backup/`).
- «Сколько скиллов» = считать `SKILL_*.md` на диске (не по тексту этой карты).
- «Скиллы направления X» = `SKILL_*.md` внутри каталога направления X.

---

## БЫСТРАЯ МАРШРУТИЗАЦИЯ (КРИТИЧЕСКИЕ ПРАВИЛА)
- **Правка файлов и команд (ВСЕГДА перед правкой):** `SKILL_edit_gotchas.md` — **critical**, обходы граблей: BOM, EOL/CRLF, кириллица в `.ps1`, `old_text`, лимит 6 КБ, кавычки, `;`, таймауты.
- **Параллельные ноги (ВСЕГДА перед git):** `SKILL_parallel_legs.md` — **critical**, закон общих репозиториев `D:\AI\repo` и `D:\AI\tools`: коммит только с pathspec, чужой staged и rebase не трогать.
- **Анти-галлюцинации (ДО утверждений о фактах/путях):** `SKILL_anti_hallucination.md` — **critical**, уровни ФАКТ / ПРЕДПОЛОЖЕНИЕ / НЕТ ДАННЫХ, запрет имитации проверки, презумпция существования.
- **Культура файлов и адресов дома:** `CORE\CULTURE_files.md` — адреса логов, отчетов, урны (`D:\AI\log\urn\<исполнитель>\`), запрет выгрузки БД в GitHub, синхронизация `.clinerules`.
- **Выживание в Cline / VS Code:** `SKILL_local_agent_cline.md` — **critical**, работа в контексте, чек-лист перед ходом, протокол воскрешения REVIVE.
- **Здоровье ноги (самопередача):** `SKILL_noga_health.md` — **critical**, пороги вызовов (40 / 55 / 70), три признака деградации, учет сжатий контекста.
- **Эстафета (передача смены):** `SKILL_handover.md` — **critical**, обязательный состав из 10 пунктов, адрес строго `D:\AI\ЭСТАФЕТЫ\<ТЕМА>.md`.
- **Крахи и сбои:** `crash\SKILL_crash_constitution.md` (закон, шаблоны экземпляра и передачи) + `crash\SKILL_crash_index.md` (список всех крах-скиллов по группам).
- **Подсчет файлов и строк:** `Prog\SKILL_count_files_template.md` — **critical**, счет только программным счетчиком с диска.
- **Закон шары `Z:` (PLM Reader):** `Powershell\SKILL_plm_reader_sync.md` — **critical**, шару `Z:\PTC\CREO-START\plm_reader` агенты не трогают ни в каком виде.
- **Правила и грабли PLM Reader:** `Creo\SKILL_GRABLI.md` (догма единой правды, архитектура конвейера, роли моделей, форматы, приёмка на тестовом сете `STRATEGY_PLM.md`).

---

### 1. Creo (CAD-система, API, чтение файлов, стандарты)
**Главный вход направления:** `Creo\SKILL_creo_index.md`
Управление Creo идет через объектный слой `pfc*` (Creo.JS, OTK/JLINK, Pro/TOOLKIT, VB API, Web.Link) или JSON-сервер CREOSON поверх JLINK.

Подразделы `Creo\` (в каждом есть свой `_INDEX.md`):
- **`API\`:** `SKILL_creojs_api.md` (Creo.JS / `pfc*`), `SKILL_creo_api_ecosystem.md` (каналы API: OTK, JLINK, VB, Web.Link, CREOSON) — **critical**.
- **`DOCS\`:** `SKILL_creo_docs_map.md` (карта документации, хелпов и PDF в установке Creo) — **high**.
- **`CREOSON\`:** `SKILL_creoson_workflow.md`, `SKILL_creoson_complete.md`, `SKILL_creoson_sessions_workdirs.md`, `SKILL_creo_commands.md`, `SKILL_creoson_write_rules.md`, `SKILL_creoson_rename_mechanism.md`, `SKILL_creoson_probe_method.md`, `SKILL_creoson_routine.md`, `SKILL_creoson_pfc_map.md`, `SKILL_creoson_inbox_deepseek.md` — **critical**.
- **`COPY\`:** `SKILL_copy_assembly_project.md` (умная копия проекта со спутниками и семействами), `SKILL_copy_rename.md` — **critical**.
- **`READ\` (чтение и правка файлов «в лоб» без Creo):** `SKILL_creo_raw_reader.md`, `SKILL_creo_file_format.md` (анатомия `#UGC_TOC`), `SKILL_creo_read_core.md`, `SKILL_creo_read_part.md`, `SKILL_creo_read_asm.md`, `SKILL_creo_read_asm_bom.md`, `SKILL_creo_read_drw.md`, `SKILL_creo_read_family.md`, `SKILL_creo_read_feat.md`, `SKILL_creo_read_feature_types.md`, `SKILL_creo_read_mass_double.md`, `SKILL_creo_read_mfg.md`, `SKILL_creo_read_roles.md`, `SKILL_creo_write_raw.md`, `SKILL_creo_new_file.md`.
- **`STANDARDS\`:** `SKILL_creo_company.md`, `SKILL_company_config.md` (автогенерируемый паспорт), `SKILL_naming_spec.md`, `SKILL_drawings_eskd.md`, `SKILL_creo_templates.md` (`TPL_SOURCE`), `SKILL_creo_model_nature.md` (деталь / сборка / производство `ПАРТИЯ`), `SKILL_parameters.md`, `SKILL_parameters_guide.md`, `SKILL_reference_limits.md`, `SKILL_creo_cards.md`, `SKILL_material_parameters.md`, `SKILL_creo_material_designation.md`, `SKILL_creo_crosshatch_material_link.md`.
- **`RELATIONS\`:** `SKILL_creo_relations.md`, `SKILL_relations_constitution.md`, `SKILL_relations_basics.md`, `SKILL_relations_examples.md`, `SKILL_curves_from_equation.md`, `SKILL_curves_examples.md`, `SKILL_spring_compression_generator.md`, `SKILL_spring_tension_master.md` — **critical**.
- **`LIT\` (литье в Relations):** `SKILL_lit_analysis_patterns.md`, `SKILL_lit_troubleshooting.md`, `SKILL_lit_hts_aws.md`, `SKILL_lit_hts_china.md`, `SKILL_lit_hts_en.md`, `SKILL_lit_hts_turkey.md`, `SKILL_lit_hts_patents_summary.md`, `SKILL_lit_hts_patents_summary_ru.md`.
- **`DAVYDOVKA\`:** `SKILL_davydovka_creoson_map.md` (карта моста Давыдовка ↔ CREOSON).
- **`INFRA\`:** `SKILL_creostart_fleet.md`, `SKILL_object_creoson_tests-01_asm.md`, `SKILL_creo_z_drive.md`.
- **Корень `Creo\`:** `SKILL_archive_plm.md` (архивы склада `\\Backup\Public\АРХИВЫ`), `SKILL_creo_file_reading.md`, `SKILL_creo_jlink_direct.md`, `SKILL_creo_directions_mfg_gdt.md`, `SKILL_creo_bit_level_anatomy.md`, `SKILL_mfg_parameter_blocks.md`, `SKILL_parameter_graph_navigation.md`, `SKILL_materials_creo_detailed.md`, `SKILL_creo_reverse_engineering_toolkit.md`, `SKILL_GRABLI.md`, `CREO_MAP.md`, `SKILLS_MAP.md`.

---

### 2. Python / Программирование (Папка Prog\ и команды)
Вход направления = эта секция.
- `Prog\SKILL_python_standard.md` (стандарт расчетных скриптов: блоки, суффиксы единиц, аудит A1-A15) — **critical**.
- `Prog\SKILL_tool_template.md` (шаблон инструмента дома: три руки CLI/GUI/визард, лог, настройки, README) — **critical**.
- `Prog\SKILL_test_first_rule.md` (правило проверки на сыром ответе перед внедрением) — **critical**.
- `Prog\SKILL_settings_audit.md` (аудит настроек: куда пишет и откуда читает программа) — **critical**.
- `Prog\SKILL_tool_routing.md` (маршрутизация инструментов по намерениям) — **critical**.
- `Prog\SKILL_count_files_template.md` (шаблон подсчета файлов/строк счетчиком) — **critical**.
- `Prog\SKILL_agent_memory.md` (управление состоянием и памятью).
- `Prog\SKILL_automated_validation.md` (линтеры и автоматические гейты).
- `Prog\SKILL_code_parsing.md` (разбор кода через AST, без regex).
- `Prog\SKILL_cursor_rules_format.md` (форматы правил IDE).
- `Prog\SKILL_diff_and_apply.md` (применение патчей и диффов).
- `Prog\SKILL_repo_mapping.md` (карта структуры репозитория).
- `Prog\SKILL_unit_testing.md` (юнит-тесты на изолированных копиях).
- `Prog\SKILL_calc_script_architecture.md` (архитектура расчетных скриптов).
- **Указатели в `Prog\` (1 строка):** `Prog\SKILL_agent_protocol.md`, `Prog\SKILL_editor_too_large.md`, `Prog\SKILL_prog_local_agent_cline.md`.
- **Команды запуска и консоли:** `Powershell\SKILL_powershell_index.md` (`SKILL_ps51_gotchas`, `SKILL_plm_reader_sync`), `Python\SKILL_python_index.md` (`SKILL_plm_reader_commands`).

---

### 3. Инженерные и Производство
- **Инженерные (`Инженерные\`):**
  - `Инженерные\SKILL_engineering_index.md` (вход направления).
  - `Инженерные\SKILL_materials_reference.md` (справочник материалов: стали, чугуны, цветные сплавы, пластики).
  - `Инженерные\SKILL_engineering_mechanics.md` (сопромат, динамика, усталость, устойчивость).
  - `Инженерные\SKILL_heat_hydraulics.md` (теплопередача, гидравлика, пневматика).
  - `Инженерные\SKILL_casting_hts_master.md` (мастер расчета литья в ХТС).
- **Производство:**
  - `SKILL_production_mirror.md` (производственный контур по срезам 1С: номенклатура, склад, входящие, запуск, отгрузки, расчет якоря и цикла).

---

### 4. PDF, Web, Интерфейсы и Спецнаправления
- **PDF (`PDF\`):** `PDF\SKILL_pdf_index.md` (вход), `PDF\SKILL_pdf_routine.md` (**critical**, вывод и обновление PDF чертежей), `PDF\SKILL_pdf_control.md` (**high**, контроль дублей и пар).
- **Web и Визия (`Web\`):** `Web\SKILL_web_index.md`, `SKILL_web_vision_limits.md` (границы чтения сайтов и изображений).
- **Окна GUI (`ОКНА\`):** `ОКНА\SKILL_WINDOWS_GUI.md` (каркас tkinter, потоки `root.after`, дизайн-константы, проверка `design_check.py`).
- **Очистка сборок (`Ветерок\`):** `Ветерок\SKILL_veterok_index.md` (вход), `SKILL_veterok_postregen.md`, `SKILL_veterok_creoson_gotchas.md`, `SKILL_veterok_program.md`.
- **Плагины B&W (`B&W\`):** `B&W\SKILL_BW_PLUGINS.md` (модули SMART* к Creo через `protkdat`).
- **Трейлы (`Трейлы\`):** `Трейлы\SKILL_trails_index.md` (журнал сессий Creo `TRAIL_JOURNAL.md`).
- **Локальные модели (`OLAMA\`):** `OLAMA\SKILL_ollama_index.md` (**critical**, раннер Ollama), `OLAMA\SKILL_llm_answer_measurement.md`, `OLAMA\SKILL_answer_vs_thinking.md`, `OLAMA\SKILL_num_predict_for_reasoning_models.md`.
- **Проектирование промптов (`PROMPT\`):** `PROMPT\SKILL_prompt_index.md` (указатель правил проектирования промптов).

---

### 5. Общее (Core), Аудит и Автономный Агент
- **Ядро и управление (корень и `CORE\`):**
  - `SKILL_anti_hallucination.md`, `SKILL_edit_gotchas.md`, `SKILL_parallel_legs.md`, `SKILL_local_agent_cline.md`, `SKILL_noga_health.md`, `SKILL_handover.md` — **critical**.
  - `SKILL_CHARGE.md` и `SKILL_CHARGE_START.md` (автогенерируемая карта и стартовый набор).
  - `CORE\CULTURE_files.md`, `CORE\company_conventions.md`, `CORE\strategy.md`, `CORE\PASSPORT.md`, `CORE\AGENT_MAP.md`, `CORE\AGENT_WORK_MAP.md`, `CORE\BACKLOG_tools.md`.
- **Аудит (`AUDIT\`):**
  - `AUDIT\SKILL_audit_protocol.md` (правила аудита репозитория).
  - `AUDIT\SKILL_audit_program.md` (аудит программ дома: одна база, одни настройки, проверка ручек).
- **Крахи и ошибки (`crash\`, `Ошибки\`):**
  - `crash\SKILL_crash_constitution.md` (правило вылетов, шаблоны), `crash\SKILL_crash_index.md` (навигатор по всем крах-скиллам), `crash\SKILL_crash_reasoning-loop.md` (указатель).
  - `Ошибки\SKILL_errors.md` (карта ошибок), `Ошибки\ERR_creoson.md`, `Ошибки\ERR_creoson_write_ops.md`.
- **Внешние шаблоны агентов (`agents\`):**
  - `agents\SKILL_authoring_standard.md`, `agents\rag-architect\SKILL_rag_architect.md`, `agents\skill-security-auditor\SKILL_skill_security_auditor.md`, `agents\zero-hallucination-coder\SKILL_zero_hallucination_coder.md`.
- **Для автономного Python-агента (не для Cline):**
  - `MANIFEST.md` (закон Python-агента), `AGENT_index.md` (вход агента), `SKILL_agent_protocol.md` (формат `[TOOL]`/`[ANSWER]`).

---

## ЗОЛОТОЙ СТАНДАРТ НОВОГО СКИЛЛА

Каждый новый скилл `SKILL_<имя>.md` обязан следовать структуре:
1. **Паспорт (Passport):** шапка YAML (`name`, `system`, `description` с `Use when:`, `when`, `priority`, `date`).
2. **Домен (Domain):** к какому направлению относится.
3. **Привычки (Habits/Rules):** конкретные, однозначные правила работы без противоречий с `.clinerules`.
4. **Инструменты (Tools/Methods):** список методов, скриптов и команд, которые использует скилл.
5. **Крах-протокол (Crash-Protocol):** специфические ошибки и как их фиксировать.
6. **Проба (Probe):** как проверить, что скилл или инструмент работает (тесты/проверки).
7. **Указатель (Pointer):** если файл перенесен, по старому пути оставляется указатель в одну строку; дублирование тела запрещено.
