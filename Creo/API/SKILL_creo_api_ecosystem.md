---
name: creo-api-ecosystem
system: Creo
description: Use when: разбор API Creo — один объектный слой pfc* у Creo.JS, Object TOOLKIT (C++/Java), VB API, Web.Link, JLINK и CREOSON; где лежат примеры и справка
when: OTK, Object TOOLKIT, JLINK, pfc, creojs, vbapi, weblink, otk_methods, jlinkexamples, api, экосистема
priority: high
date: 22.09.2026
---
# ЭКОСИСТЕМА API CREO: ОДИН `pfc*` — МНОГО КАНАЛОВ
Все каналы автоматизации Creo опираются на ОДНУ объектную модель **`pfc*`** (pfcSession, pfcModel,
pfcAssembly, pfcFamily, pfcDrawing, pfcFeature, …):
- **Creo.JS** — JS-биндинг `pfc*` (см. `SKILL_creojs_api.md`);
- **Object TOOLKIT C++** — заголовки `pfc*.h`;
- **Object TOOLKIT Java** — пакеты `com.ptc.pfc.*`;
- **VB API**, **Web.Link** — тот же pfc-слой (другие языки);
- **JLINK** — Java-привязка `pfc*` (пакет `com.ptc.jlinkexamples` в примерах);
- **CREOSON** — JSON-сервер ПОВЕРХ JLINK (`com.simplifiedlogic.nitro.jlink.*` зовёт `com.ptc.pfc.*`).
Вывод: у любой функции CREOSON есть родственник в `pfc*` — примеры OTK/JLINK это прямые подсказки.

## Раскладка по установке (`D:\PTC\CREO12\Creo 12.4.2.0\Common Files\`, только чтение)
### Object TOOLKIT — код и примеры
- `otk\otk_cpp\include\` — **122 заголовка `pfc*.h`** (+ `_s.h`): pfcSession, pfcAssembly, pfcFamily,
  pfcDrawing, pfcFeature, pfcModel, pfcSolid, pfcMFG, pfcSimpRep, pfcUnits, pfcUI, pfcWindow, …
- `otk\otk_cpp\otk_examples\` — примеры по темам: asm, cip, drw, feat, graphics, interface, main,
  model, server, solid, ui, utils; плюс `otk_async_examples\`; либы — `otk\otk_cpp\x86e_win64\`.
- `otk\otk_java\otk_java_examples\` — примеры Java (otkFamilyTable*, otkDrawing, otkRasterExport,
  otkCreateSection2D, otkWTServerExample, …) + `otkjavaexamples.jar`.
### Object TOOLKIT — справка
- `otk_cpp_doc\`: `otkug.pdf` (2.65 МБ), `OTK_Cxx_GSG.pdf`, `Otk_Cxx_RelNotes.pdf`,
  **`otk_methods.txt` (705 КБ, 4165 строк)** — таблица: `C++ Header | C++ Class | C++ Method |
  Java Package | Java Class | Java Method | Exposure | Description`; `online_help\`,
  `otk_cpp_examples_html\` (DrawingExample.html, ModelItemVisitExample.html).
- `otk_java_doc\`: `otk_javaug.pdf` (2.63 МБ), `OTK_Java_GSG.pdf`, `Otk_Java_RelNotes.pdf`,
  `otk_methods.txt` (тот же), `online_help\`.
### JLINK — примеры (тот же JLINK, что у CREOSON)
`otk_java_free\otk_java_appls\`:
- `jlinkexamples\` — `pfcDrawingExamples.java` (57 КБ), `pfcExamplesMenu.java` (56 КБ),
  `pfcModelCheckExamples`, `pfcRelationExamples`, `pfcComponentFeatExamples`, `pfcParameterExamples`,
  `pfcCommandExamples`, `pfcPopupExamples`, `pfcServerExamples`, `pfcFamilyMemberExamples` и др.
- `jlinkasyncexamples\` — `pfcAsyncStartExample.java`, `pfcAsyncFullExample.java` (АСИНХРОННЫЙ старт).
- `jlink_servlet\` (JLinkServletTest), `jlink_param\`, `jlink_loader\` (JLinkLoader), `jlink_elev\`,
  `install_test\` (pfcInstallTest, AsyncInstallTest).
- `otk_java_free\exercises\` (exercise_1_and_2/4/5/6 + solutions), `README.txt`.
### Смежное
- `apps\creojs\otk_api_spec\OTK_model.json.zip` (619 КБ) — JSON-модель OTK-API; `apps\creojs\creojsexamples\otk\`.
- `applications\creouieditor\otk_cpp_doc\creo_uifc_ug.pdf`, `otk_java_doc\creo_uifc_java_ug.pdf` (UI-editor).
- `protoolkit\otk_appls\`, `protoolkit\protk_appls\creotk_examples\`.

### Pro/TOOLKIT (C API, слой ниже pfc)
`protoolkit\`: `tkuse.pdf` (9.8 МБ — главное), `Creo_Toolkit_GSG.pdf`, `Creo_Toolkit_RelNotes.pdf`
(+ `russian\Creo_Toolkit_GSG.pdf`), `online_help\`, `includes\`, `protk_appls\`, `otk_appls\`, `protk.dat`.
### VB API / Web.Link
- `vbapi\`: `vbug.pdf`, `VB_RelNotes.pdf`, `online_help\`, `vbapi_examples\`, `vbapi_appls\`.
- `weblink\`: `weblinkug.pdf`, `Web_RelNotes.pdf`, `online_help\`, `weblinkexamples\` (+ `html\`).
### Java-библиотеки Creo (`Common Files\text\java\`)
- **`pfcasync.jar`** (1.2 МБ, 1985 записей: 1873 `com/ptc/pfc` + 56 `com/ptc/cipjava`) — **PTC JLINK (pfc*), асинхронный**;
- `otk.jar` (4.28 МБ) — Object TOOLKIT Java; `TWXCreoAnalysisProvider.jar` (28.9 МБ);
- `config.properties`, `scripts\`, `Simulator\`.
### Производство и прочее
- `mfg_cmdsyn\`, `mfg_cmdsyn_ai\` — синтаксис ЧПУ (`.syn`/`.def`/`.ndx`).
- `x86e_win64\gpost\`: `FIL_Manual.pdf`, `GPost_Manual.pdf`, `GPost_Release_Notes_V68_CIMpro_Manual.pdf`.
- `text\russian\dbatch.pdf` — Distributed Batch; `Distributed Services Manager\html` — DSM.
- `modchk\` (+ `text\{russian,usascii}\html`) — ModelCHECK; `applications\gdt_home\...\html` — GD&T;
  `applications\EZTOL\...\html` — EZTOL; `applications\simulate\html` — Simulate.

## ПРОБЫ (в `D:\AI\PROBA`, скрипты + вывод)
1. `probe_creoson_jar.py` → `creoson-core-3.0.1.jar` (289 записей): **268 `com/simplifiedlogic/nitro/jlink`**
   + 18 `nitro/util` + 1 `nitro/rpc`; `com/ptc/pfc` = 0 (pfc в этом jar нет).
2. `pfcasync.jar` (Creo, `Common Files\text\java\`) → 1985 записей: **1873 `com/ptc/pfc`** + 56 `com/ptc/cipjava`
   — это и есть JLINK (pfc*); `creoson_run.bat` добавляет его в classpath.
3. **Итог пробы:** CREOSON = свой слой `com.simplifiedlogic.nitro.jlink` ПОВЕРХ PTC JLINK
   (`pfcasync.jar`); функции CREOSON отвечают методам `com.ptc.pfc.*` (примеры `jlinkexamples`).
4. Family/mfg-пробы через CREOSON (`familytable:*`, `bom:get_paths`, копия) — фактическая проверка
   pfc-слоя (см. `..\COPY\SKILL_copy_assembly_project.md`).
Файл пробы: `D:\AI\PROBA\creoson_jar_probe.txt`.

## ПРЯМОЕ УПРАВЛЕНИЕ CREO (без CREOSON) — ЖИВАЯ ПРОБА 22.09.2026
Проба в `D:\AI\PROBA\jlink_probe` (`DirectProbe.java`): Java-программа напрямую подключилась к
запущенному Creo через JLINK, без CREOSON:
```
OK: JLINK lib pfcasyncmt loaded
OK: connected, connection=com.ptc.pfc.Implementation.pfcAsyncConnection$AsyncConnection@...
OK: session=com.ptc.pfc.Implementation.pfcSession$Session@...
OK: cwd=D:\AI\PROBA\famcopy2\
OK: disconnected (Creo left running)
```
### Рецепт (Java / JLINK)
1. Класс `com.ptc.pfc.pfcAsyncConnection.pfcAsyncConnection` (из `pfcasync.jar`), нативная либа `pfcasyncmt`.
2. Среда (иначе `UnsatisfiedLinkError: ... Can't find dependent libraries`):
   - **`PATH`** += Creo `Common Files\x86e_win64\lib` и `\obj` (как делает `creoson_run.bat`);
   - `-Djava.library.path` = те же папки;
   - `PRO_COMM_MSG_EXE` = `...\x86e_win64\obj\pro_comm_msg.exe`;
   - classpath: `pfcasync.jar` (Creo `Common Files\text\java`).
3. API `pfcAsyncConnection`: `AsyncConnection_Start(cmd, textpath)` — запустить Creo
   (`"pro -g:no_graphics -i:rpc_input"` — те же скрытые ключи, что в домовой обёртке);
   `AsyncConnection_Connect(Display, UserID, TextPath, TimeoutSec)` — **подключиться к запущенному**;
   `ConnectById`, `ConnectWS`, `GetActiveConnection`; `GetSession()`; `EventProcess()` (цикл событий);
   `Disconnect(timeout)` — отцепиться (Creo жив); `End()` — закрыть Creo.
4. Дальше — весь `pfc*`: `session.GetCurrentDirectory()`, `session.RetrieveModel(descr)`, …
### Давыдовка как пример прямого управления
Давыдовка идёт ДРУГИМ прямым каналом — **Creo.JS** (JS во встроенном браузере Creo): мост `creojs.js`
+ серверные `*.creojs` зовут `pfcGetCurrentSession()` и тот же `pfc*`; свой Python-сервер на 8000
делает не-Creo работу (BOM, XLSX, PDF). То есть «прямое управление + свой сервер» — уже
реализованный образец (см. `..\DAVYDOVKA\SKILL_davydovka_creoson_map.md`).
### Сравнение каналов (итог)
| Канал | Как | Плюс | Минус |
|---|---|---|---|
| **JLINK (Java)** | своя программа: `pfcasync.jar` + `pfcasyncmt` | все `pfc*`, attach/start, колбэки | нужен Java + PATH/classpath |
| **Creo.JS** | JS в браузере Creo | без внешнего процесса, UI внутри Creo | привязка к браузеру Creo |
| **Pro/TOOLKIT (C)** | DLL (`protk.dat`) | внутри процесса Creo, скорость | C/C++, сборка |
| **CREOSON** | JSON поверх JLINK | любой язык, без сборки | только завернутые функции |