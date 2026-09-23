---
name: creo-skills-map
system: Creo
description: Use when: нужна КАРТА СКИЛЛОВ ветки Creo — что где лежит, какой скилл открывать под задачу, чем связаны
when: карта скиллов, индекс, навигация, какой скилл, обзор скиллов
priority: high
date: 23.09.2026
---
# КАРТА СКИЛЛОВ ВЕТКИ CREO (23.09.2026)
Корень ветки: `D:\AI\repo\Creo\` · подраздел: `CREOSON\` · общий индекс дома: `D:\AI\repo\SKILL_index.md`.

## 1. УКАЗАТЕЛИ И КАРТЫ (сюда в первую очередь)
| Файл | Что даёт |
|---|---|
| `CREO_MAP.md` | **карта строения Creo**: установка, слои, каналы, матрица задач, точки входа |
| `SKILLS_MAP.md` | этот файл — карта скиллов ветки |
| `SKILL_creo_index.md` | индекс ветки (что читать под теги `[CREO]`, `[PARAMETRIC]`) |
| `CREOSON\_INDEX.md` | указатель подраздела CREOSON |
| `README_jlink_direct.md` | полный разбор прямого управления (JLINK): пробы, среда, API, экспорт, грабли |

## 2. CREOSON — РУТИНА (подраздел `CREOSON\`)
| Скилл | О чём |
|---|---|
| `CREOSON\SKILL_creoson_routine.md` | полный практический разбор CREOSON: 18 групп, 199 функций, сценарии, грабли (кириллица, перезапуск, PID) |
| `CREOSON\SKILL_creoson_pfc_map.md` | соответствие CREOSON ↔ `pfc*`, карта JLINK-примеров |
| `CREOSON\SKILL_creoson_workflow.md` *(в stash)* | полный цикл работы: подключение, папки, переключение сессий |
| `SKILL_creoson_complete.md` | сводный справочник CREOSON (13 КБ) |
| `SKILL_creoson_probe_method.md` | КАК пробовать CREOSON (метод проб) — открывать перед любой пробой |
| `SKILL_creoson_sessions_workdirs.md` | сессии и рабочие папки (22 КБ), подъём стека `ctl.py up` |
| `SKILL_creoson_write_rules.md` | правила пишущих операций (щит согласования) |
| `SKILL_creoson_rename_mechanism.md` | механизм переименования (`onlysession` → `save`) |
| `SKILL_creoson_inbox_deepseek.md` | разбор входящих наработок по CREOSON |

## 3. ПРЯМОЕ УПРАВЛЕНИЕ CREO (JLINK/Java)
| Скилл | О чём |
|---|---|
| `SKILL_creo_jlink_direct.md` | среда, подключение/запуск/`Disconnect`, рецепты, **PDF из чертежа**, экспорт 3D, 717 классов API, грабли |
| `SKILL_creo_ecosystem.md` *(в stash: `SKILL_creo_api_ecosystem.md`)* | каналы: один `pfc*` у Creo.JS/OTK/VB/Web.Link/JLINK/CREOSON |
| `SKILL_creojs_api.md` | канал **Creo.JS** (как в Давыдовке): API и приёмы |
| `SKILL_creo_directions_mfg_gdt.md` | направления: `mfg_cmdsyn` (синтаксис ЧПУ), GD&T Advisor, `pfcSolid`/`pfcFeature` |
| `README_jlink_direct.md` | исследование целиком (наравне со скиллом) |

## 4. КОПИРОВАНИЕ, ПЕРЕИМЕНОВАНИЕ, ПРОЕКТЫ
| Скилл | О чём |
|---|---|
| `SKILL_copy_rename.md` | копирование и переименование моделей |
| `SKILL_copy_assembly_project.md` *(в stash)* | умная копия проекта: сборка+детали, деталь+чертёж, семейство, mfg |
| `SKILL_object_creoson_tests-01_asm.md` | протокол объектных испытаний на сборке |
| `SKILL_creo_templates.md` | шаблоны моделей/чертежей дома |
| `SKILL_naming_spec.md` | правила обозначений/имён (шифры) |
| `SKILL_creo_company.md`, `SKILL_company_config.md` | стандарты предприятия, `config.pro` |
| `SKILL_creostart_fleet.md` | парк запусков Creo (старт, флот, папки) |

## 5. ИНЖЕНЕРНЫЕ ДАННЫЕ: ПАРАМЕТРЫ, ОТНОШЕНИЯ, СТАНДАРТЫ
| Скилл | О чём |
|---|---|
| `SKILL_parameters_guide.md` | параметры модели: что это, как читать и писать |
| `SKILL_creo_relations.md` | отношения модели (уравнения) — рабочий справочник |
| `SKILL_relations_basics.md` | отношения: основы |
| `SKILL_relations_constitution.md` | правила дома по отношениям (конституция) |
| `SKILL_relations_examples.md` | примеры отношений |
| `SKILL_reference_limits.md` | справочные пределы и таблицы |
| `SKILL_creo_commands.md` | команды/меню Creo (шпаргалка) |
| `SKILL_creo_cards.md` + `cards\liteika_hts_mm_relations.md` | карты тем; «литейка» — 67 КБ готовых отношений |

## 6. ОФОРМЛЕНИЕ И ЧЕРТЕЖИ
| Скилл | О чём |
|---|---|
| `SKILL_drawings_eskd.md` | чертежи по ЕСКД: рамки, штампы, оформление |
| `SKILL_naming_spec.md` | обозначения и имена файлов (шифры) — сюда же для PDF-рутины |

## 7. ГЕНЕРАТОРЫ: ПРУЖИНЫ И КРИВЫЕ
| Скилл | О чём |
|---|---|
| `SKILL_spring_compression_generator.md` | генератор пружины сжатия |
| `SKILL_spring_tension_master.md` | мастер пружины растяжения |
| `SKILL_curves_from_equation.md` | кривые из уравнения |
| `SKILL_curves_examples.md` | примеры кривых |

## 8. СВЯЗКИ И ВНЕШНИЕ КАНАЛЫ
| Скилл | О чём |
|---|---|
| `SKILL_davydovka_creoson_map.md` | Давыдовка: Creo.JS + свой Python-сервер, в терминах дома |
| `SKILL_creo_docs_map.md` *(в stash)* | карта документации `D:\PTC\CREO12` (справка, 6 `online_help`, OTK, mfg, GD&T, ModelCHECK) |

## 9. КРАХ-СКИЛЛЫ ТЕМЫ (`D:\AI\repo\crash\`)
| Файл | Триггер |
|---|---|
| `SKILL_crash_git_parallel-leg-rebase-reverts-worktree.md` | чужая git-нога с rebase откатывает рабочее дерево |
| `SKILL_crash_runcommands_kill-by-name-house-services.md` | `Stop-Process -Name` сносит агент/copy-server — убивать по PID |
| `SKILL_agent-frozen.md` | агент «застыл» (порт слушает, ответов нет) |
| `SKILL_crash_agent_corruption.md` / `_agent_silence.md` / `_agent-duplicate-restart-race.md` | порча кода, молчание, двойной агент |
| `SKILL_crash_pdf-roots-two-lists.md` | два списка корней PDF |
| `SKILL_crash_editor-text-not-found.md`, `_editor-mismatch.md`, `_editor_too_large_and_non_unique_anchors.md`, `SKILL_editor_too_large.md` | правки редактором |
| `SKILL_crash_runcommands-copy-race-fake-parameter.md` | чтение файла в той же пачке, где создали |

## 10. СКИЛЛЫ ДОМА ОБ АГЕНТЕ (нужны при работе с Creo через агента)
`D:\AI\repo\SKILL_agent_protocol.md` (протокол `[TOOL]/[ANSWER]`) ·
`D:\AI\repo\SKILL_local_agent_cline.md` (выживание в Cline) ·
`D:\AI\repo\Prog\SKILL_agent_memory.md` (память/якорь) · `D:\AI\repo\PASSPORT.md` («Модули агента»).

## 11. ИНСТРУМЕНТЫ И КОНСПЕКТЫ ВНЕ РЕПО (не скиллы, но опора)
```
D:\AI\tools\agent\creo_export\   CreoExport.java + creo_export.bat + pfcasync.jar + README (экспорт/PDF)
D:\AI\PROBA\POLYGON_NOTES.md     конспект полигона, §1–22 (все пробы)
D:\AI\PROBA\jlink_direct_probe_notes.md    конспект прямого JLINK
D:\AI\PROBA\pfc_api_full_map.txt           717 классов API
D:\AI\PROBA\pfc_api_key_methods.txt        методы ключевых классов
D:\AI\PROBA\pfc_methods_by_class.txt       выгрузка по классам (первый парсер)
D:\AI\PROBA\smartcopy.py, lib_probe.py, fam_nested.py, mfg_probe.py   пробы копий/семейств/mfg
D:\AI\PROBA\ru_params_probe.py, pdf_creoson_probe.py, restore_creo_cwd.py   пробы кириллицы и PDF
D:\AI\PROBA\parse_otk_v2.py + parse_otk_methods.py   парсеры otk_methods.txt
D:\AI\PROBA\jlink_probe\{DirectProbe,DirectProbe2,DirectProbe3}.java + out\   живые пробы JLINK
D:\AI\PROBA\drw_pdf\   пара knockout_1.drw/.prt для проб PDF
D:\AI\log\reports\REPORT_creo-creoson_cline_2026-09-22.md   отчёт ноги 22.09
D:\AI\log\reports\REPORT_creo_full_cline_2026-09-23.md      полный отчёт (этот свод)
```

## 12. ЧТО ПОЯВИЛОСЬ В СЕССИИ 22–23.09.2026
`SKILL_creo_jlink_direct.md` · `SKILL_creo_directions_mfg_gdt.md` · `CREO_MAP.md` · `SKILLS_MAP.md` ·
`README_jlink_direct.md` · `CREOSON\SKILL_creoson_routine.md` · `CREOSON\SKILL_creoson_pfc_map.md` ·
`CREOSON\_INDEX.md` · правки `SKILL_creo_index.md`; в stash — `SKILL_creo_api_ecosystem.md`,
`SKILL_creo_docs_map.md`, `SKILL_copy_assembly_project.md`, `CREOSON\SKILL_creoson_workflow.md` и
реорганизация ветки в 8 подразделов.

⚠️ **Внимание:** идёт ЧУЖАЯ git-нога (rebase). Моя реорганизация и 4 скилла лежат в
`stash@{0}: parallel-leg-creo-reorg-2209` — вернутся после `git stash pop` в её завершение.
До этого ветка плоская; пути в этой карте даны для плоского вида (кроме помеченных *(в stash)*).