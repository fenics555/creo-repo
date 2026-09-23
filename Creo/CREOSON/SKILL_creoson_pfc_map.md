---
name: creoson-pfc-map
system: Creo
description: Use when: нужно понять, какой метод pfc* стоит за функцией CREOSON (и наоборот) — таблица соответствия из otk_methods.txt
when: creoson, pfc, соответствие, mapping, otk_methods, jlink, методы, прямое управление
priority: high
date: 22.09.2026
---
# CREOSON ↔ `pfc*`: ТАБЛИЦА СООТВЕТСТВИЯ
Источник: `D:\PTC\CREO12\…\Common Files\otk_cpp_doc\otk_methods.txt` — **4159 строк** вида
`C++ Header | C++ Class | C++ Method | Java Package | Java Class | Java Method | Exposure | Description`
+ примеры `jlinkexamples`. CREOSON зовёт PTC JLINK (`com.ptc.pfc.*`), поэтому у каждой функции
CREOSON есть родственный метод `pfc*`.

## Соответствие по группам CREOSON
| CREOSON | `pfc*` (класс) |
|---|---|
| `file:open` / `save` / `rename` / `backup` / `erase` / `display` | `pfcModel`: RetrieveModel / Save / Rename / Backup / Erase / Display |
| `file:massprops` | `pfcSolid` / `pfcModel`: GetMassProperty |
| `file:relations_get` / `relations_set` | `pfcRelations` / `pfcModel` (relations) |
| `creo:pwd` / `creo:cd` | `pfcSession`: GetCurrentDirectory / ChangeDirectory |
| `creo:get_config` / `set_config` | `pfcSession` / `pfcGlobal` (config options) |
| `creo:list_files` / `list_dirs` | `pfcSession` (файловые операции) |
| `bom:get_paths` | `pfcAssembly`: ListItems + `pfcCreateComponentPath` |
| `familytable:*` | `pfcFamily` (FamilyTable / ListRows / AddRow / SetCell) |
| `drawing:*` | `pfcDrawing`: Create / AddModel / ListViews / Regenerate |
| `parameter:*` | `pfcModelItem` / `pfcParameter`: List / Get / Set |
| `interface:export_pdf` / `export_image` / `export_file` | `pfcExport` |
| `interface:mapkey` | `pfcSession` / `pfcUI`: RunMacro |
| `dimension:*` | `pfcDimension` |
| `layer:*` | `pfcLayer` |
| `view:*` | `pfcView` |
| `note:*` | `pfcNote` |
| `feature:*` | `pfcFeature` |

## Ключевые методы `pfcModel` (прямое управление, 41)
`Backup`, `Copy`, `CopyAndRetrieve`, `Rename`, `Save`, `Erase`, `EraseWithDependencies`, `Delete`,
`Display`, `ListDependencies`, `ListDeclaredModels`, `CreateLayer`, `IsCommonNameModifiable`,
`RegeneratePostRegenerationRelations`, `DeletePostRegenerationRelations`, `CleanupDependencies`.
→ ровно эти вызовы стоят за `file:*` в CREOSON и за `Copy/CopyAndRetrieve` в Давыдовке.

## `pfcSession` (24)
`UIAddMenu`, `UICreateCommand`, `UIAddButton`, `UIDisplayMessage`, `UIOpenFile`, `UISelectDirectory`,
`UISaveFile`, `UIGetCurrentMouseStatus`, `GetCurrentSelectionBuffer`, `NavigatorPane*`,
`RibbonDefinitionfileLoad`.

## Размеры по классам (методов)
`pfcSolid` 40 · `pfcModel` 41 · `pfcFeature` 21 · `pfcWindow` 19 · `pfcSession` 24 ·
`pfcAssembly` 13 · `pfcLayer` 7 · `pfcView` 6 · `pfcModelItem` 4 · `pfcSimpRep` 3 · `pfcMFG` 1.

## Прямое управление без CREOSON → ОТДЕЛЬНЫЙ СКИЛЛ
**`SKILL_creo_jlink_direct.md`** — JLINK/Java: среда (`pfcasyncmt`, `PATH`, `PRO_COMM_MSG_EXE`, `pfcasync.jar`),
подключение/запуск/`Disconnect`, рецепты, грабли, **717 классов API**, **69 классов экспорта**.
- Живая проба: `DirectProbe2` прочитал **47 параметров** (в т.ч. русские) + `mass=0.002014…`,
  `volume=256.562…`, `area=577.847…` с `pin_splitk.prt` — конспект `D:\AI\PROBA\jlink_direct_probe_notes.md`.
- Полные карты: `D:\AI\PROBA\pfc_api_full_map.txt` (717 классов), `pfc_api_key_methods.txt`,
  `pfc_methods_by_class.txt` (скрипты `parse_otk_v2.py`, `parse_otk_methods.py`).

## ПРИМЕРЫ JLINK ПО ТЕМАМ (готовые образцы, `otk_java_free\otk_java_appls\jlinkexamples\`)
| Файл | Байт | Тема |
|---|---|---|
| `pfcDrawingExamples.java` | 57 062 | чертежи (виды, листы, размеры) — самый большой |
| `pfcExamplesMenu.java` | 56 409 | меню примеров (точка входа) |
| `pfcServerExamples.java` | 19 049 | серверные операции |
| `pfcReadBasicFeatPropertiesExamples.java` | 19 448 | чтение свойств элементов |
| `pfcComponentFeatExamples.java` | 14 064 | компоненты сборки |
| `pfcModelCheckExamples.java` | 13 904 | ModelCHECK |
| `pfcPopupExamples.java` | 13 766 | всплывающие подсказки |
| `pfcCommandExamples.java` | 8 358 | команды |
| `pfcRelationExamples.java` | 7 381 | отношения |
| `pfcExternalDataExamples.java` | 5 523 | внешние данные |
| `pfcDisplayListExamples.java` | 3 173 | display list |
| `pfcDisplayExamples.java` | 3 383 | отображение |
| `pfcNavigatorPaneExamples.java` | 3 317 | панель навигатора |
| `pfcParameterExamples.java` | 3 244 | параметры (`GetParam`/`CreateParam`/`SetValue`) |
| `pfcSelectionExamples.java` | 2 127 | выбор |
| `pfcFamilyMemberExamples.java` | 2 008 | исполнения семейств |
| `pfcSessionExamples.java` | 2 134 | сессия |
| `pfcDimensionExamples.java` | 1 112 | размеры |
| `pfcModelExamples.java` | 1 118 | retrieve модели (`ModelDescriptor_Create`+`RetrieveModel`) |
| `pfcImportFeatureExample.java` | 1 809 | импорт-элемент |
| `MakeVRMLOnEraseExample.java` | 1 799 | экспорт VRML |
| `pfcServerExamplesWF4.java` | 4 601 | сервер (WF4) |
+ каталоги `modelcheck\`, `models\`, `text\`.
Асинхронные: `..\jlinkasyncexamples\` (`pfcAsyncStartExample`, `pfcAsyncFullExample`).
Прочие приложения: `..\install_test\`, `..\jlink_servlet\`, `..\jlink_param\`, `..\jlink_loader\`,
`..\jlink_elev\`; учебные `..\..\exercises\`.