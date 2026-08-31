---
name: skill-index
system: общее
description: Карта всех скиллов репо по доменам: что где лежит и куда смотреть
when: навигация, где что, карта скиллов, список скиллов, какой скилл, домены
priority: critical
---

# КАРТА СКИЛЛОВ РЕПО (D:\AI\repo)
Один скилл = одна зона знания. Домены не дублируют друг друга.

## ДОМЕН 1: Creo (веб-агент, инженер)
| Скилл | Назначение |
|---|---|
| SKILL_creoson_complete | полная карта API CREOSON (critical) |
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
|---|---|
| SKILL_agent_protocol | протокол инженера-напарника (critical) |
| company_conventions | паспорт КБ: станки, продукция, семантика трейлов |
| SKILL_web_vision_limits | что WEB и ВИЗИЯ умеют и не умеют |
| strategy | живой журнал направлений развития |

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