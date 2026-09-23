---
name: creo-directions-mfg-gdt
system: Creo
description: Use when: разбор направлений Creo — ЧПУ-синтаксис (mfg_cmdsyn), GD&T Advisor, ключевые методы pfcSolid/pfcFeature
when: mfg_cmdsyn, cmdsyn, чпу, циклы, GD&T, gdt_home, pfcSolid, pfcFeature, направления
priority: high
date: 22.09.2026
---
# НАПРАВЛЕНИЯ CREO: ЧПУ-СИНТАКСИС, GD&T, pfcSolid/pfcFeature

## 1. `mfg_cmdsyn` / `mfg_cmdsyn_ai` — синтаксис команд ЧПУ
`D:\PTC\CREO12\Creo 12.4.2.0\Common Files\mfg_cmdsyn\` (24 файла) и `mfg_cmdsyn_ai\` (22).
- **`.def`** — ЧИТАЕМАЯ ГРАММАТИКА команд (по блоку `begin … end`). Пример (`cycles.def`):
  ```
  CYCLE{BORE} / BORE ,#depth [,IPM | ,IPR | ,MMPM | ,MMPR | ,PERMIN | ,PERREV | ,TPI] ,#feed
  [,ORIENT] [,#angle][,DWELL ,#seconds | ,REV ][,#revs]
  ```
  → параметры в `#`, опции в `[ ]`, альтернативы через `|`.
- **`.syn`** — служебный **UGC-токенный** вид (`#UGC:2 TOKEN …`, `@cmdsyn_node`, `@name`,
  `@user_name`, `@optional`, `@repeatable`, `@arg_seprator`) — машинная форма того же узла.
- **`cmdsyn.ndx`** — индекс узлов.
- Состав: `cycles`, `gohome-lintol`, `loadtl-opstop`, `origin-postn`, `ppfun-rotabl`, `probe_cycles`,
  `probe_setup`, `selctl-tmark`, `sync_pt`, `toolno-units`, `air-clrsrf`, `coolnt-from` (+ в `_ai`:
  `cl_file`, `cycle`, `cycle_auto`, `feeds`, `machine`, `motion`, `tool`).
- Применение: проверка/генерация строк CL/циклов обработки; в CREOSON mfg-функций нет — работа
  файловым уровнем + `interface:mapkey`.

## 2. GD&T Advisor — справка
`Common Files\applications\gdt_home\text\resource\html\` — **215 файлов**, языки `russian\` и `usascii\`.
Назначение: геометрические допуски и аннотации (GD&T). Для дома — справочник по допускам/оформлению.

## 3. `pfcSolid` (40 методов) — что умеет модель-деталь
`Regenerate`, `ExecuteFeatureOps`, `EvalOutline`, `CreateLocalGroup`, `CreateNote`, `ListFailedFeatures`,
`ListFeaturesByType`, `ListCrossSections`, `GetCrossSection`, `HasRetrievalErrors`, `GetFeatureByName`,
`GetFeatureById`, `CreateImportFeat`, **`GetMassProperty`**, `ListGroups`,
упрощённые представления: `ActivateSimpRep`, `GetActiveSimpRep`, `CreateSimpRep`, `SelectSimpRep`,
`GetSimpRep`, `GetMasterRep`, `GetGraphicsRep`, `GetGeomRep`, `DeleteSimpRep`.

## 4. `pfcFeature` (21 метод) — элемент
`CreateSuppressOp` / `CreateResumeOp` / `CreateDeleteOp` / `CreateReorderBeforeOp` / `CreateReorderAfterOp`,
`ListChildren` / `ListParents` / `ListSubItems`,
`GetFeatType` / `GetFeatSubType` / `GetStatus` / `GetGroup` / `GetPattern` / `GetGroupPattern`,
`GetIsVisible` / `GetIsReadonly` / `GetNumber` / `GetVersionStamp` / `GetIsGroupMember` / `GetIsEmbedded`.

## Связь
Соответствие CREOSON↔`pfc*` — `SKILL_creoson_pfc_map.md`; выгрузка методов —
`D:\AI\PROBA\pfc_methods_by_class.txt`; карта документации — `SKILL_creo_docs_map.md`.