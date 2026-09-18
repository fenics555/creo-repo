---
name: skill-index
system: общее
description: Карта всех скиллов репо по доменам: что где лежит и куда смотреть
when: навигация, где что, карта скиллов, список скиллов, какой скилл, домены
priority: critical
---

# КАРТА СКИЛЛОВ РЕПО (D:\AI\repo)
Один скилл = одна зона знания. Домены не дублируют друг друга.

## НАПРАВЛЕНИЯ (первый указатель, состав по MANIFEST.md)
- Creo: Creo\SKILL_creo_index.md · PDF: PDF\SKILL_pdf_index.md · Web: Web\SKILL_web_index.md
- Инженерные: Инженерные\SKILL_eng_index.md · Трейлы: Трейлы\SKILL_trails_index.md
- Ошибки: Ошибки\SKILL_errors.md · Крахи: crash\SKILL_crash_constitution.md

## ДОМЕН 1: Creo (веб-агент, инженер)
| Скилл | Назначение |
|---|---|
| SKILL_creoson_complete | полная карта API CREOSON (critical) |
| SKILL_creoson_sessions_workdirs | сессии Creo, старт Creo/CREOSON, рабочие директории, поиск файлов/сборок/чертежей (critical) |
| SKILL_creoson_rename_mechanism | переименование модели и чертежа: onlysession + save (critical) |
| SKILL_creoson_probe_method | методика безопасных проб в CREOSON + справка (critical) |
| SKILL_davydovka_creoson_map | карта операций Давыдовки на CREOSON (что есть, чего нет) |
| SKILL_creo_commands | быстрый подбор команды под задачу |
| SKILL_creo_relations | relations: синтаксис, функции, лимиты, примеры |
| SKILL_relations_constitution | железные ПРАВИЛА relations (critical) |
| SKILL_creo_company | паспорт: единицы, шаблоны, шифры, обязательные параметры, чертежи ЕСКД |
| SKILL_creo_templates | канон-шаблоны моделей, свидетельство о рождении TPL_SOURCE |
| SKILL_curves_from_equation | кривые из уравнения (теория) |
| SKILL_curves_examples | готовые рецепты кривых |
| SKILL_spring_compression_generator | генератор пружины сжатия |
| SKILL_spring_tension_master | эталон пружины растяжения |

## ДОМЕН 2: Python / VS Code (Continue, программист)
| Скилл | Назначение |
|---|---|
| SKILL_python_standard | стандарт расчётных Python-скриптов (блоки, суффиксы, аудит A1–A15) |
| SKILL_test_first_rule | правило TEST-first для новых связок |

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

## ДОМЕН 5: общее (оба агента)
| Скилл | Назначение |
| SKILL_log_management | управление логами и автоуборка (D:\AI\log) |
|---|---|
| SKILL_tool_routing | маршрутизация запросов к инструментам (critical) |
| SKILL_agent_protocol | протокол инженера-напарника (critical) |
| company_conventions | паспорт КБ: станки, продукция, семантика трейлов |
| SKILL_web_vision_limits | что WEB и ВИЗИЯ умеют и не умеют |
| SKILL_local_agent_cline | выживание локального ИИ в Cline/VS Code: привычки, транспорт, редактор, крахи, карта дома (critical) |
| strategy | живой журнал направлений развития |
| AUDIT_rules_*.md (корень repo) | отчёты аудита правил дома (находки, варианты, вердикты) |

## ДОМЕН 6: Автогенерируемые (руками не править)
| Файл | Кто пишет |
|---|---|
| SKILL_company_config.md (корень репо) | passport_tools (живой паспорт из config.pro) |
| Трейлы/TRAIL_JOURNAL.md | trail_tools |
| Ошибки/ERR_*.md | каталог ошибок |
| Избранное/SKILL_favorites_<user>.md | избранное пользователя |

## ПРАВИЛА МАРШРУТИЗАЦИИ
- Команда CREOSON → creo_commands, детали API → creoson_complete.
- «Как написать relations» → creo_relations (синтаксис) + relations_constitution (правила).
- «Единицы/шаблоны/шифры/параметры/чертежи» → creo_company.
- «Шаблон модели / новая модель / TPL_SOURCE» → creo_templates.
- Код проекта → python_standard + test_first_rule.
- Физика/материалы → Инженерные.
- «Где деталь / когда комплект / якорь / цикл» → production_mirror.
- «Почему вылетаю / как работать в Cline / где что лежит» → local_agent_cline.