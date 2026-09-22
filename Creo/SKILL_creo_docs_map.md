---
name: creo-docs-map
system: Creo
description: Use when: нужна справка/документация Creo — где лежат хелпы, PDF и API-руководства в установке и в доме
when: документация, справка, help, хелп, PDF, Toolkit, OTK, VB API, Web.Link, Creo.JS, mfg_cmdsyn, GPost, где читать
priority: high
date: 22.09.2026
---
# КАРТА ДОКУМЕНТАЦИИ CREO (источники знаний)
Правило: `D:\PTC\CREO12` — **только чтение** (писать нельзя). Дубли в дом не тащить —
читать по месту; в `CREO_DOCS` держать только нужное/уникальное.

## 1. Полная справка Creo (русская, HTML) — главный источник
`D:\PTC\CREO12\Creo 12.4.2.0\creo_help_pma\russian\` — **15 678 HTML**, 35 модулей:
`fundamentals`, `part_modeling`, `assembly`, `detail`, `sheetmetal`, `surfacing`, `simulate`,
`manufacturing`, `mold_and_casting`, `expert_moldbase`, `welding`, `piping`, `layout`,
`data_exchange`, `datamanagement`, `configuration_options`, `model_analysis`,
`model-based_definition`, `generative_design`, `design_exploration`, `advanced_framework`,
`electrical_design`, `composite_design`, `rendering`, `routers`, `langsupport`, `connect`,
`tutorials_pma`, `whats_new_pma`, `other_modules`, `introduction`, `wwhelp`, `css`, `scripts`.
- Точка входа: `index.html`; карта справки: `creo_helpmap_pma.txt` (793 КБ).
- Каждый модуль = `МОДУЛЬ.html` + `МОДУЛЬ_sx.js` (поисковый индекс).
- Дубль: `Common Files\help\pma\`. Плюс `Common Files\help\{common,reference,russian,usascii}` и
  `Common Files\html\russian\`.

## 2. Pro/TOOLKIT (C API)
`Common Files\protoolkit\`: **`tkuse.pdf`** (9.8 МБ — главное руководство), `Creo_Toolkit_GSG.pdf`,
`Creo_Toolkit_RelNotes.pdf`, `russian\Creo_Toolkit_GSG.pdf`, `online_help\`, `includes\`,
`protk_appls\`, `otk_appls\`, `protk.dat`.

## 3. Object TOOLKIT (OTK)
- **C++**: `Common Files\otk_cpp_doc\`: `otkug.pdf` (2.65 МБ), `OTK_Cxx_GSG.pdf`,
  `Otk_Cxx_RelNotes.pdf`, `otk_methods.txt`, `online_help\`, `otk_cpp_examples_html\`.
- **Java**: `Common Files\otk_java_doc\`: `otk_javaug.pdf` (2.63 МБ), `OTK_Java_GSG.pdf`,
  `Otk_Java_RelNotes.pdf`, `otk_methods.txt`, `online_help\`.
- Код/примеры: `Common Files\otk\{otk_cpp,otk_java}`, `otk_java_free\{exercises,otk_java_appls}`.
- UI-редактор: `applications\creouieditor\otk_cpp_doc\creo_uifc_ug.pdf`,
  `otk_java_doc\creo_uifc_java_ug.pdf`.

## 4. VB API / Web.Link / Creo.JS
- VB API: `Common Files\vbapi\` — `vbug.pdf`, `VB_RelNotes.pdf`, `online_help\`, `vbapi_examples\`.
- Web.Link: `Common Files\weblink\` — `weblinkug.pdf`, `Web_RelNotes.pdf`, `online_help\`, `weblinkexamples\`.
- Creo.JS: `Common Files\creojs\` — `creojsug.pdf`, `Creojs_RelNotes.pdf`, `online_help\`,
  SDK `creojsweb\` + примеры `creojsexamples\` (см. `SKILL_creojs_api.md`).

## 5. Производство (ЧПУ) и постпроцессоры
- `Common Files\mfg_cmdsyn\`, `mfg_cmdsyn_ai\` — синтаксис команд ЧПУ (`.def`, `.syn`, `.ndx`;
  напр. `cycles.syn`, `loadtl-opstop.syn`, `gohome-lintol.syn`).
- `Common Files\text\russian\dbatch.pdf` — Creo Distributed Batch (пакетная обработка).
- `Common Files\x86e_win64\gpost\`: `FIL_Manual.pdf`, `GPost_Manual.pdf`,
  `GPost_Release_Notes_V68_CIMpro_Manual.pdf` (постпроцессор GPost).
- `applications\cma\Documents\METIS_manual_version_5.1.0.pdf`.

## 6. ModelCHECK и стандарты
- `Common Files\modchk\` (images, templates, templates_new, text) — ModelCHECK.
- `Common Files\{templates,formats,symbols,tol_tables,creo_standards}\` — шаблоны, форматы,
  символы, таблицы допусков, стандарты.
- `Common Files\demos\demo\` — демонстрации.

## 7. Уже в доме (`D:\AI\repo\Creo\CREO_DOCS\`)
`creojsug.pdf`, `Creojs_RelNotes.pdf`, `vbug.pdf`, `VB_RelNotes.pdf`, `weblinkug.pdf`,
`Web_RelNotes.pdf`, `RUS_configoptions.pdf` + `creo_toolkit_online_help\` (перенесённая справка
PTC Creo Parametric TOOLKIT + Creo JS API Wizard).

## 8. Что из установки ещё НЕ в доме (кандидаты на пополнение базы знаний)
`tkuse.pdf`, `Creo_Toolkit_GSG.pdf`/`RelNotes`, `otkug.pdf`, `OTK_Cxx/Java_*`, `otk_javaug.pdf`,
`otk_methods.txt` (×2), `FIL_Manual.pdf`/`GPost_Manual.pdf`, `dbatch.pdf`, `METIS_manual`,
полная справка `creo_help_pma\russian\` (15 678 HTML) и `Common Files\help`.

## 9. Как пользоваться
1. Справка по модулю Creo → `creo_help_pma\russian\<модуль>.html` (+ `_sx.js` — поисковый индекс).
2. Нужен API → разделы 2–4 (Toolkit/OTK/VB/Web.Link/Creo.JS).
3. Нужно ЧПУ/постпроцессор → раздел 5.
4. Тома в дом без нужды не тянуть: справка читается по месту (`D:\PTC\CREO12`, только чтение).

## 10. ВСЕ НАПРАВЛЕНИЯ СПРАВКИ (полная карта help-локаций в установке)
### Справка Creo (PMA) — ДВА языка
- `creo_help_pma\russian\` — 35 модулей (русский).
- `creo_help_pma\usascii\` — те же 35 модулей (английский).
### API `online_help` (HTML, у каждой — `wwhelp\` и `creo_toolkit\wwhelp\`)
- `Common Files\protoolkit\online_help\` — Pro/TOOLKIT
- `Common Files\otk_cpp_doc\online_help\` — OTK C++
- `Common Files\otk_java_doc\online_help\` — OTK Java
- `Common Files\vbapi\online_help\` — VB API
- `Common Files\weblink\online_help\` — Web.Link
- `Common Files\creojs\online_help\` — Creo.JS (+ Creo Toolkit)
### Прочие html-справки приложений
- `Common Files\help\` — common, `reference\pma`, russian, usascii
- `Common Files\html\russian\dsm` и `Distributed Services Manager\html` — **DSM** (Distributed Services Manager)
- `Common Files\modchk\text\{russian,usascii}\html` — **ModelCHECK**
- `Common Files\applications\gdt_home\text\resource\html` — **GD&T Advisor**
- `Common Files\applications\EZTOL\text\report\html` — **EZTOL** (допуски)
- `Common Files\applications\simulate\html` — **Creo Simulate**
- `Common Files\applications\cvadapters\prodview\doc` — **ProductView/CV adapters**
- `Common Files\apps\learning_conn\html` — **Learning Connector**
- `Common Files\weblink\weblinkexamples\html` — примеры Web.Link
Все пути — внутри `D:\PTC\CREO12\Creo 12.4.2.0\` (только чтение).