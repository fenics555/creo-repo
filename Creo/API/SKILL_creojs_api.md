---
name: creojs-api
system: Creo
description: Use when: работа с родным API Creo (Creo.JS / pfc*), сверка с CREOSON, разбор механизмов Давыдовки
when: Creo.JS, creojs, pfc, pfcSession, API, Давыдовка, ListItems, GetParam, ListRows, Rename, ExportRasterImage, Web.Link, VB API
priority: critical
---
# CREO.JS — РОДНОЙ API CREO (карта по официальному руководству)

## Где документация и её близнец
`D:\AI\repo\Creo\CREO_DOCS\` (официальные PDF PTC, вскрыты `pymupdf` 19.09.2026):
| Файл | Стр. | sha256-голова | Что это |
|---|---|---|---|
| `creojsug.pdf` | 315 | `571e37a3976b7e1b` | **Creo.JS User's Guide 12.4.2.0** — главный источник по API |
| `Creojs_RelNotes.pdf` | 35 | `56a2173c5c6c546c` | что менялось по версиям (Edge-браузер, новые функции) |
| `weblinkug.pdf` | — | — | Web.Link (предшественник Creo.JS, для миграции) |
| `vbug.pdf` | 346 | `7e1bf856593d7aaa` | VB API (тот же pfc-объект на VB) |
| `RUS_configoptions.pdf` | 384 | `8f1b149a3d611025` | опции конфигурации (bookmarks нет — искать по тексту) |
| `VB_RelNotes.pdf`, `Web_RelNotes.pdf` | 75 / — | — | релиз-ноты |
Полный TOC Creo.JS и выжимки разделов: `D:\AI\log\urn\cline\creojsug_toc.txt` (15638 б) и
`creojsug_excerpts.txt` (22910 б); общий TOC всех PDF — `creo_docs_toc.txt` (32450 б).

## Как это работает
- Creo.JS — JS-API внутри Creo: скрипт объявляется на странице как
  `<script type="text/creojs" src="...">`, исполняется движком Creo, даёт объекты `pfc*`.
- Корень всего — `pfcSession` (стр.40): «Any program that accesses data from Creo must first
  get a handle to the pfcSession object». Получение: `pfcGetCurrentSession()`,
  `pfcGetCurrentSessionWithCompatibility()`, `pfcGetProESession()`.
- Отладка: Chrome Remote Debugger (стр.33), MIME-тип для веб-сервера (стр.8),
  настройки безопасности браузера (стр.15), миграция с Web.Link (стр.15-20).
## КАРТА API (страницы по оглавлению `creojsug_toc.txt`)
| Раздел | Стр. | Что даёт |
|---|---|---|
| Session Objects | 40 | `pfcSession` — корень; сессия, окна, выбор, глобальные настройки |
| Session Information | 41 | данные сессии (лицензия, версия Creo) |
| Directories / File Handling | 42 | рабочие папки и файлы (`GetCurrentDirectory`, `ChangeDirectory`) |
| Configuration Options | 43 | чтение/запись опций конфигурации |
| Macros | 43 | mapkey-вызовы |
| Message Window | 47-49 | сообщения, внутренний буфер |
| Models | 59 | объект модели |
| Model Descriptors | 60 | дескриптор файла+папки (аналог `{file, dirname}` в CREOSON) |
| Retrieving Models | 61 | `RetrieveModel()` (загрузка с диска) |
| Model Information | 62 | имя, тип, папка, версия |
| **Model Operations** | 65 | **rename, save, backup, erase — пишущие операции модели** |
| ModelCHECK | 67 | `ExecuteModelCheck()` → `pfcModelCheckResults` |
| Drawings | 68-98 | создание из шаблона, модели чертежа, листы, виды, размеры, таблицы |
| Solid | 116 | тело как объект |
| **Mass Properties** | 126 | `GetMassProperty()` — масса/объём/центр масс |
| Cross Sections / Solid Bodies | 128 / 134 | сечения, тела (multibody) |
| Dimensions and Parameters | 185 | размеры и параметры |
| Parameter Objects | 187 | создание/доступ к параметрам (`GetParam`) |
| Parameter Information / Restrictions | 190 / 192 | значения, типы, ограничения |
| **Assemblies and Components** | 197 | сборка и компоненты |
| Structure of Assemblies | 198 | иерархия сборки |
| Assembly Components | 199 | компоненты, `ListItems` |
| Regenerating an Assembly Component | 201 | регенерация компонента |
| **Component Path Information** | 201 | **путь компонента (`pfcCreateComponentPath`)** |
| Assembling Components | 202-207 | сборка/переопределение компонентов |
| **Family Tables** | 209 | таблицы семейств |
| Creating FT Instances / Columns | 211 / 212 | строки и столбцы семейства |
| Setting the Family Table Instance Name | 159 | имя исполнения |
| Export Instructions | 221-243 | экспорт: PDF/U3D (228), изображения (222), фасеты, STL/VRML |
| Import and Export / File Copy | 290 / 292 | импорт-экспорт и **копия модели** |

## ФУНКЦИИ ДАВЫДОВКИ ↔ РОДНОЕ API ↔ CREOSON
| Давыдовка (`.creojs`) | Родное API (стр.) | CREOSON |
|---|---|---|
| `pfcGetCurrentSession()` | Session p.40 | `connection:connect` |
| `session.GetCurrentDirectory()` / `ChangeDirectory` | Directories p.42 | `creo:pwd` / `creo:cd` |
| `session.GetModelFromFileName()` | Models p.59-62 | `file:get_fileinfo`, `file:open` |
| `session.RetrieveModel(descriptor)` | Retrieving Models p.61 | `file:open` |
| `assembly.ListItems(ITEM_FEATURE)` | Assembly Components p.199 | `bom:get_paths` |
| `pfcCreateComponentPath(assembly,[id])` | Component Path Information p.201 | `bom:get_paths.path[]` |
| `feature.Id`, `GetFeatureById` | Features (раздел Feature) | `path[]` из `bom:get_paths` |
| `owner.GetParam(name)`, `parameter.Value` | Parameter Objects p.187 | `parameter:list` |
| `ListRows()`, `GetImmediateGenericInfo` | Family Tables p.209-212 | `file:has_instances`, `file:list_instances`, `familytable:list_tree` |
| `targetModel.Rename(name)` | Model Operations p.65 | `file:rename {onlysession:true}` |
| `targetModel.Save()`, `Backup(desc)` | Model Operations p.65 | `file:save`, `file:backup` |
| `source.Copy/CopyAndRetrieve(newBase)` | File Copy p.292 | ОС-копия + `file:open/regenerate/save` |
| `session.EraseUndisplayedModels()` | Session p.40-42 | `file:erase_not_displayed` (+ цикл `file:erase`) |
| `GetMassProperty()` | Mass Properties p.126 | `file:massprops` |
| `ExportRasterImage(file, instructions)` | Export Instructions p.221-228 | `interface:export_image` |
| `drawingModel.Rename()` | Model Operations p.65 + Drawings p.71 | `file:rename` + `drawing:regenerate` |
| Мануфактуринг (`creoRenameManufacturingInfo`, fixture) | в руководстве раздел Manufacturing/NC | в CREOSON **отсутствует** |

## Что важно помнить при сверке
- Родное API и CREOSON — два канала к **одной** сессии Creo; имена моделей/папок у них общие.
- Объект из `CurrentModel` может прийти базовым прокси без методов — перевзять
  `session.GetModelFromFileName(имя)` (ERR 2.5, урок Давыдовки).
- Методы возвращают pfc-коллекции: длину даёт `getarraysize()`/`Count`, элемент — по индексу.
- Ошибки создания чертежа у Давыдовки перечислены как `DWGCREATE_ERR_*` (p.69-70) —
  их удобно сопоставлять с ответом `drawing:create` в CREOSON.
- Web.Link и VB API (`weblinkug.pdf`, `vbug.pdf`) — родственные API того же pfc-слоя:
  полезны, когда Creo.JS молчит, но в доме канал один — CREOSON.

## Трёхслойное устройство SDK (разбор 22.09.2026, из `D:\PTC\CREO12\…\apps\creojs\creojsweb`)
Движок — **Chrome V8 внутри процесса Creo**, ECMAScript 2018. Слои:
1. **Core `creojs.js`** — глобальный объект `CreoJS`, регистрация приложения в сессии через
   `creojs_id`, жизненный цикл (Connect/Disconnect), собственная реализация `Promise`.
2. **Abstraction `browser.creojs`** — developer-API через **JS `Proxy`**: любое обращение
   `CreoJS.method()` перехватывается, имя+аргументы упаковываются в запрос (можно писать
   «родным» JS, не думая о протоколе).
3. **Bridge `creojsbridge.js`** — IPC-драйвер: `$CALLCreoModule` передаёт запрос в движок Creo
   и разрешает `CallPromise` при ответе; ошибки Creo приходят в JS.
Итог: высокоуровневый веб-API над низкоуровневым IPC; в доме канал — CREOSON, а Creo.JS
остаётся родным путём для механизмов Давыдовки (см. `SKILL_davydovka_creoson_map.md`).

## Где лежат SDK и справка
- Родной SDK: `D:\PTC\CREO12\Creo 12.4.2.0\Common Files\apps\creojs\creojsweb`
  (`creojs.js`, `browser.creojs`, `creojsbridge.js`) + примеры `…\creojsexamples\`
  (в т.ч. `otk\` — Object TOOLKIT: `test_parameters.js`, `assembly_structure.js`, `feature_tree_explore.js`).
- Веб-справка PTC (Creo Parametric TOOLKIT `api/`+`user_guide/` + Creo JS API Wizard) —
  `D:\AI\ИЗУЧИТЬ\CREO\creo_toolkit_online_help` (2950 файлов, 27.8 МБ; перенесена из репо 22.09.2026).
- **Нативная справка PTC TOOLKIT/OTK и Creo.JS SDK**: `D:\AI\ИЗУЧИТЬ\CREO\creo_toolkit_online_help` (2950 файлов, 27.8 МБ) и `D:\PTC\CREO12\Creo 12.4.2.0\Common Files\apps\creojs` (creojsexamples, creojsweb, otk_api_spec); читать по надобности диапазонами и grep, в гит не входить, в репо не копировать.
- PDF PTC (`creojsug.pdf`, `vbug.pdf`, `weblinkug.pdf`, `RUS_configoptions.pdf` и релиз-ноты, 7 файлов) остаются в `Creo\CREO_DOCS\` — они уже в истории гита, повторно не переносятся.