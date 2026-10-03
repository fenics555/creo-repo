---
name: creo-read-mfg
system: Creo
description: МАНУФАКТУРИНГ «в лоб» — операции, переходы, набор инструмента, траектории .tph, состав ASSEM_MFG, чего НЕ собираем (CL-данные)
when: mfg, мануфакчуринг, чпу, nc, операции обработки, переходы, инструмент, траектория, tph, оснастка, станок
priority: high
date: 03.10.2026
---
# МАНУФАКТУРИНГ `ASSEM_MFG` И `.tph` — ЧТЕНИЕ «В ЛОБ»

**Закон владельца: CL-данные (траектории) в ПЛМ НЕ собираем.** Берём **операции / переходы / инструмент**.

## 1. ПРИЗНАК
`#UGC:2 ASSEMBLY/ASSEM_MFG` (отличается от обычной `#UGC:2 ASSEMBLY`).
Состав мануфакчуринг-сборки (проверено на `191-9050-gr4-1.asm.1`): деталь + заготовка +
`INLBS_MFG_NC.ASM` (**оснастка/приспособление**) + `SBORKA_MFG.ASM` + `T0010.PRT` (**инструмент**) +
`HAAS_3X.ASM` (**станок**).
⚠️ Природу модели доказывают **факты Creo** (расширение `.mfg`, `ProMdlSubtypeGet`), **не** параметры
(`ТИП = Производство`, `ПАРТИЯ` — только подсказка) — см. `..\STANDARDS\SKILL_creo_model_nature.md`.

## 2. ЧТО ЧИТАЕТСЯ (таблица проверена 25.09.2026)
| Что | Как читается |
|---|---|
| **Операции** | строки `фрезерование id 687`, `Окно Фрезерования 1/2`; поля `OPERATION`×3, `NC_SEQ`×3, `op_id`, `machining` |
| **Переходы / элементы** | `ПАЗЫ`, `Отверстие 1`, `Отверстие 1 [1]`, `Отверстие 1 [47]`; поля `STEP`×199, `step_params`, `parent_ncseq_id` |
| **Набор инструмента** | `T0001`, `T0003`, `T0010`, `T0015`; поля `TOOL`×184, `tool_table`, `tool_id`; типы `FREZ/frez`, `ball`, `MILL`, `TAP`, `DRILL` |
| **Файлы траекторий** | `NCL_FILE`×36, `PTC_MFG_PRM_CL_FILE`×76, `PTC_TOOLPATH_REV_NUM`×32, `END_STOP_CONDITION`×32 |
| **Время/стоимость** | relation-строки: `время_обработки=machining_time+machining_time*.1`, `стоимость_обработки=Нормочас/60*время…` |
| **Оснастка/станок** | `INLBS_MFG_NC.ASM`, `HAAS_3X.ASM` |

## 2б. ✅ ГЛАВНОЕ МЕСТО — `NeuAsmSld` (проверено 03.10.2026 на `23-1017gri-01.asm.1`)
У мануфакчуринг-сборки эта секция = **126 991 байт, 740 уникальных идентификаторов** и содержит
**параметры обработки по операциям** — читается больше, чем считалось:
```
TOOL_ID · NCL_FILE · PRE_MACHINING_FILE · POST_MACHINING_FILE · OPERATION_NAME · OPERATION_COMMENTS
NC_SEQUENCE_NAME · tool_table · oper_type · num_of_items
SPINDLE_SPEED · MAX_SPINDLE_RPM · SPEED_CONTROL · CONST_RPM · SPINDLE_SENSE · SPINDLE_RANGE
CUT_FEED · FREE_FEED · CUT_UNITS · RETRACT_REF_OFFSET · RETRACT_UNITS · LINTOL · TOLERANCE
COOLANT_OPTION · COOLANT_PRESSURE · FIXT_OFFSET_REG · COORDINATE_OUTPUT · MACHINE_CSYS
POCKET_NUMBER · TIP_CONTROL_POINT · TLCHG_TIP_NUMBER · DESCRIPTION · MACH_COLLISION_STATUS
```
Значения-маркеры: `YES`×90 · `NONE`×108 · `DIRECT`×84 · `INITIAL`.
**Быстрый признак MFG-сборки по размеру:** `NeuAsmSld` > 100 КБ, тогда как у обычной сборки она пуста (41 б).

## 2в. ✅ ОПЕРАЦИИ, ПЕРЕХОДЫ, ИМЕНА (проверено)
| Что | Байтовая опора |
|---|---|
| Операция | `OPERATION` → `OPERATION_NAME`, `OPERATION_COMMENTS` (`@0x93a45`) |
| Последовательность | `NC_SEQ` → `NC_SEQUENCE_NAME` |
| Инструмент | `TOOL_ID` → `NCL_FILE` · `PRE_MACHINING_FILE` (связка в одном блоке) |
| Таблица инструментов | `tool_table` → `type`, `oper_type`, `num_of_items`, `name` |
| **Названия переходов** | русские строки: `6-ПОД-КОЛЬЦОМ`, `6-НАД-КОЛЬЦОМ`, `0_5-НАД-КОЛЬЦОМ`, `0_5-НАД-ПОЛКОЙ`, `2-ПОД-ПОЛКОЙ-`, `0_7-ПОД-ПОЛКОЙ-ДЛЯ-ДИСКОВОЙ`, `'отверстия` |
| Операции деталей-компонентов | видны прямо в MFG-сборке: `Вытягивание 2…20`, `Эскиз 1/2`, `Скругление 3/6/7/8`, `Сопряж Границ 1` |

⚠️ Кириллица в MFG-сборке — **1 132 строки, 171 уникальная** (у детали `din933` — 271/114).
Компьютеры-участники правок видны прямо: `FREZER-1` ×134, `FREZER-2`, `FREZER-4`, `Frezer-3`.


## 3. ФАЙЛ ТРАЕКТОРИЙ `.tph` (`#UGC:2 MFG_TOOL_PATH`)
`tool_param_arr`, `loop_type`, `loop_data`, `cut_pos_data(chain_pos_drill_cycle)`, `step_params`,
`parent_ncseq_id`, `feed`/`feedrate`, `drill`, `tool` — внутри видны шаги обработки, циклы, подачи.
Проверено на `df-stp2-gdf.tph.1`.

## 4. ИНСТРУМЕНТ
`python mfg_probe.py <файл…>` — служебные поля, `typed_data(...)`, русские строки про операции/переходы,
упоминания инструмента, ASCII-строки про NC/CL. (Скрипт урны `log\urn\cline\`.)

## 5. ГРАБЛИ
* Тип `.mfg` по JLINK **не определяется**: `Model::GetSubtype()` в нашем `pfcasync.jar` НЕТ,
  `instanceof pfcMFG.MFG` даёт **false даже для `.mfg`**, `ModelType` отдаёт 1 (как у детали).
  Опираться на **расширение** и C-API `ProMdlSubtypeGet`.
* Роль компонента (`ComponentFeat.GetCompType()`): `0` заготовка, `1` ссылочная модель, `2` оснастка,
  `10` стержень, `11` результат литья; оснастка ещё ищется по `FEATTYPE_FIXTURE_SETUP = 91`.
* В CREOSON **нет ни одной `mfg-*` функции** — мануфактуринг читается только из файла или через Creo native.
* `familytable`/сборочные вызовы не смешивать с долгими MFG-операциями в одной сессии.
