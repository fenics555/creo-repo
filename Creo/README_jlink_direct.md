---
name: creo-jlink-direct-readme
system: Creo
description: README исследования прямого управления Creo из программы (JLINK) — пробы, среда, API, экспорт, грабли
when: jlink, прямoe управление, pfcasync, исследование, readme, java
date: 23.09.2026
---
# README: ПРЯМОЕ УПРАВЛЕНИЕ CREO ИЗ ПРОГРАММЫ (JLINK) — ПОЛНОЕ ИССЛЕДОВАНИЕ

**Полигон прогонов:** `D:\AI\PROBA\jlink_probe` · **Инструмент:** `D:\AI\tools\agent\creo_export`
**Скилл:** `SKILL_creo_jlink_direct.md` · **Даты:** 22–23.09.2026

## 0. НАЧАЛЬНАЯ ГИПОТЕЗА И ВЫВОД
Гипотеза: «управлять Creo можно только JSON-ом CREOSON».
**Опровергнуто.** CREOSON — надстройка над PTC JLINK: сам он не содержит `com.ptc.pfc`
(`creoson-core-3.0.1.jar` = 268 классов `nitro.jlink`, `com/ptc/pfc` = 0), а зовёт библиотеку PTC.
Значит **JLINK доступен напрямую** — без CREOSON, без сервера, без сборки C++.

Доказательства живьём (все три — Java-класс + `pfcasync.jar`):
| Проба | Что сделано | Результат |
|---|---|---|
| `DirectProbe.java` | подключение к УЖЕ запущенному Creo, `GetSession`, `GetCurrentDirectory`, `Disconnect` | Creo остался жив |
| `DirectProbe2.java` | чтение модели `pin_splitk.prt` | **47 параметров** (в т.ч. русские) + `mass=0.0020140154825460856`, `volume=256.5624818530046`, `area=577.8473711192212` |
| `DirectProbe3.java` | экспорт из Creo | **STEP 13 466 б**, **IGES 55 268 б**, **VRML 26 233 б**; DXF — отказ (нужен чертёж) |

## 1. СТЕК И ЖЕЛЕЗО ВОПРОСА
```
Ваша программа (Java)
  └─ pfcasync.jar      ← интерфейсы com.ptc.pfc.* + com.ptc.cipjava (JLINK API, 1873 класса)
       └─ pfcasyncmt.dll ← нативный мост (15 412 704 б)
            └─ Creo Parametric (сессия, запущенная man-ually или вами)
```
`pfcasync.jar` = `D:\PTC\CREO12\Creo 12.4.2.0\Common Files\text\java\pfcasync.jar` (1 205 062 б)
`pfcasyncmt.dll` = `...\Common Files\x86e_win64\lib\pfcasyncmt.dll` (15 412 704 б)

Тот же слой `pfc*` стоит под **всеми** каналами: Creo.JS, Object TOOLKIT (C++/Java), VB API, Web.Link,
JLINK и CREOSON. Выучил один — остальные читаются.

## 2. СРЕДА ЗАПУСКА (без неё `UnsatisfiedLinkError: Can't find dependent libraries`)
```java
System.loadLibrary("pfcasyncmt");          // или pfcasync (для простых задач)
```
| Что | Значение |
|---|---|
| `PATH` | += `...\x86e_win64\lib` **и** `...\x86e_win64\obj` |
| JVM | `-Djava.library.path="<lib>;<obj>"` |
| Переменная | `PRO_COMM_MSG_EXE=...\x86e_win64\obj\pro_comm_msg.exe` |
| classpath | `.;pfcasync.jar` (jar держать рядом с классом — пробелы в пути ломают classpath) |
| Java | Temurin `D:\AI\Java\bin\{javac,java}.exe` (Java 25: WARNING про native access — не ошибка) |

## 3. ПРОБА 1 — ПОДКЛЮЧЕНИЕ К ЖИВОМУ CREO
```java
pfcAsyncConnection.Connection c = pfcAsyncConnection.AsyncConnection_Connect(null, null, null, 60);
Session s = c.GetSession();
System.out.println(s.GetCurrentDirectory());   // D:\AI\PROBA\famcopy2\
c.Disconnect(10);                              // Creo ОСТАЁТСЯ живым
// c.End();                                    // а это закрывает Creo
```
Результат: `OK: connected`, `session`, `cwd=D:\AI\PROBA\famcopy2\`, `disconnected (Creo left running)`.
Важно: JLINK **подключается к уже идущей сессии** (тогда CREOSON и программа не мешают друг другу)
либо **сам запускает Creo**: `AsyncConnection_Start("pro -g:no_graphics -i:rpc_input", null)`.

## 4. ПРОБА 2 — ЧТЕНИЕ ДАННЫХ МОДЕЛИ
```java
ModelDescriptor d = pfcModel.ModelDescriptor_Create(ModelType.MDL_PART, "pin_splitk.prt", null);
Model m = s.RetrieveModel(d);
Parameters ps = ((ParameterOwner) m).ListParams();
for (int i = 0; i < ps.getarraysize(); i++) {
    Parameter p = ps.getitem(i);
    System.out.println(p.GetName() + " = " + p.GetValue());   // value -> типовой геттер
}
MassProperty mp = ((Solid) m).GetMassProperty(null);
System.out.println(mp.GetMass() + " " + mp.GetVolume() + " " + mp.GetSurfaceArea());
```
Живой вывод: `params=47`, среди имён — русские (`НАИМЕНОВАНИЕ`, `ТИП`, `СТАНДАРТ`…),
`mass=0.0020140154825460856 volume=256.5624818530046 area=577.8473711192212`.
Ловушка: `GetValue()` печатается как `com.ptc.pfc.Implementation.pfcModelItem$ParamValue@hash` —
значение доставать типовым геттером (`GetStringValue`/`GetDoubleValue`/…), а не `println`.

## 5. ПРОБА 3 — ЭКСПОРТ ИЗ CREO (программа реально делает дело)
```java
GeometryFlags f = pfcExport.GeometryFlags_Create();     // com.ptc.pfc.pfcExport
f.SetAsSolids(true);
m.Export(out + "pin_splitk.stp",
    pfcExport.STEP3DExportInstructions_Create(AssemblyConfiguration.EXPORT_ASM_SINGLE_FILE, f));
m.Export(out + "pin_splitk.igs",
    pfcExport.IGES3DNewExportInstructions_Create(AssemblyConfiguration.EXPORT_ASM_SINGLE_FILE, f));
m.Export("", pfcModel.VRMLModelExportInstructions_Create(out));   // VRML: имя игнорируется
m.Export(out + "pin_splitk.dxf", pfcModel.DXFExportInstructions_Create());  // ОТКАЗ на детали
```
Живой вывод:
```
cwd=D:\AI\PROBA\famcopy2\
model=pin_splitk.prt fullname=PIN_SPLITK
STEP -> OK 13466 bytes
IGES -> OK 55268 bytes
VRML -> pin_splitk_prt.wrl(26233b)
DXF FAIL: com.ptc.pfc.Implementation.pfcExceptions$XToolkitGeneralError
OK done
```
**Закон экспорта:** всегда `model.Export(путь, инструкции)`; инструкции — статические `*_Create(...)`.
**DXF/DWG/2D-форматы требуют ЧЕРТЁЖ**, на детали дают `XToolkitGeneralError`.

### Каталог `_Create` (снято `javap -classpath pfcasync.jar ...`)
| Сигнатура | Классы |
|---|---|
| `(AssemblyConfiguration, GeometryFlags)` | STEP3D, IGES3DNew, JT3D, ParaSolid3D, ACIS3D, UG3D, CATIA*(Model/Session/Part/Product/CGR), SW*(Part/Asm), VDA3D |
| `()` | DXF3D, DWG3D, CADDS, NEUTRALFile, PDF, ProductView, BOM, Material, DXF, STEP2D, DWGSetup |
| `(String)` | STLASCII, STLBinary, Inventor, CATIAFacets, Render, VRMLModel |
| `(String,String)` | VRMLDirect |
| `(GeomExportFlags)` | IGES3D, STEP, VDA, FIAT (из `pfcModel`) |
| прочее | `PrintSize/PrintPlacementOption/PrintMdlOption/PrintPrinterOption/PrinterInstructions/PDFOption_Create()` |

Пакеты (Creo 12.4.2): `com.ptc.pfc.pfcExport` (3D-обмен + печать + PDF), `com.ptc.pfc.pfcModel`
(2D/IGES/STEP/VRML/BOM), `com.ptc.pfc.pfcWindow` (`RasterImageExportInstructions`).
Перечисления: `AssemblyConfiguration.{EXPORT_ASM_SINGLE_FILE, EXPORT_ASM_MULTI_FILES, EXPORT_ASM_FLAT_FILE,
EXPORT_ASM_ASSEMBLY_PARTS}`; `GeometryFlags.SetAs{Solids,Surfaces,Wireframe,Quilts}(boolean)`.

## 5а. ПРОБА 4 — PDF ИЗ ЧЕРТЕЖА (главная рутина дома)
```java
s.ChangeDirectory("D:\\AI\\PROBA\\drw_pdf");                        // папка чертежа
Model d = s.RetrieveModel(pfcModel.ModelDescriptor_CreateFromFileName(
        "D:\\AI\\PROBA\\drw_pdf\\knockout_1.drw"));                  // чертёж по полному пути
d.Display();                                                        // ОБЯЗАТЕЛЬНО
d.Export(out + "knockout_1.pdf", pfcExport.PDFExportInstructions_Create());
```
Живой вывод:
```
cwd=D:\AI\PROBA\famcopy2\  →  cd=D:\AI\PROBA\drw_pdf\
model=knockout_1.drw fullname=KNOCKOUT_1
displayed
  OK knockout_1.pdf 26276 bytes
EXPORT OK
```
Материал пробы: `knockout_1.drw` + `knockout_1.prt` (пара из поставки Creo,
`Common Files\applications\emx\components\inch\knockout\`) скопированы в `D:\AI\PROBA\drw_pdf`.

**Три условия PDF** (каждое проверено отказом):
| Условие | Ошибка при нарушении |
|---|---|
| модель — ЧЕРТЁЖ, не деталь | `pfcExceptions$XToolkitInvalidType` |
| рабочая папка Creo = папка чертежа | деталь чертежа не находится |
| `Model.Display()` до экспорта | `pfcExceptions$XToolkitNotDisplayed` |

**Сверка каналов на одной модели:** JLINK `26 276 б` · CREOSON `interface:export_pdf`
(с `use_drawing_settings:true`) `26 262 б`; оба `%PDF-1.7`. Домашняя рутина (CREOSON) и прямая
программа (JLINK) дают один и тот же результат — выбирай по удобству.

**Тонкая настройка:** `PDFExportInstructions.SetOptions(PDFOptions)` ← `PDFOption{PDFOptionType, ArgValue}`;
типы: `PDFOPT_SHEET_RANGE`, `PDFOPT_SHEETS`, `PDFOPT_FONT_STROKE`, `PDFOPT_COLOR_DEPTH`,
`PDFOPT_HIDDENLINE_MODE`, `PDFOPT_SEARCHABLE_TEXT`, `PDFOPT_RASTER_DPI`, `PDFOPT_LAYER_MODE`,
`PDFOPT_PARAM_MODE`, `PDFOPT_HYPERLINKS`, `PDFOPT_BOOKMARK_*`, `PDFOPT_TITLE/AUTHOR/SUBJECT/KEYWORDS`,
`PDFOPT_PASSWORD_TO_OPEN`, `PDFOPT_MASTER_PASSWORD`, `PDFOPT_RESTRICT_OPERATIONS`; плюс `SetProfilePath`.

## 6. КАРТА API И МЕТОДОЛОГИЯ РАЗВЕДКИ (как самому найти любой метод)
1. **Справочник классов**: `D:\PTC\CREO12\...\Common Files\otk_cpp_doc\otk_methods.txt` — 4165 строк,
   **717 классов**, столбцы: `C++ Header | C++ Class | C++ Method | Java Package | Java Class | Java Method |
   Exposure | Description`. Разбор: `D:\AI\PROBA\parse_otk_v2.py` →
   `pfc_api_full_map.txt` (821 строка), `pfc_api_key_methods.txt` (704 строки).
2. **Файл НЕ полный**: у `pfcDrawing`/`pfcDrawingFormat`/`pfcUnits` методов почти нет — чертёжное API
   разложено по `pfcModel2D`(19) / `pfcView2D`(20) / `pfcSheetOwner`(17) / `pfcDimension2D`(18) /
   `pfcDrawingDimCreateInstructions`(14) / `wfcDrawingViewDisplay`(13).
3. **Истина — в jar**: `pfcasync.jar` = 1873 класса `com/ptc/pfc`. Список — открыть jar как zip и
   отфильтровать `*.class`; сигнатуры — `javap -classpath pfcasync.jar com.ptc.pfc.pfcExport.pfcExport`.
   **Статический держатель** `_Create` — вложенный класс с тем же именем: `com.ptc.pfc.pfcExport.pfcExport`,
   `com.ptc.pfc.pfcModel.pfcModel` (не `com.ptc.pfc.pfcExport`!).
4. **Готовые примеры PTC** (золото): `...\Common Files\otk_java_free\otk_java_appls\jlinkexamples\` —
   `pfcDrawingExamples`(57 КБ), `pfcExamplesMenu`(56 КБ), `pfcReadBasicFeatPropertiesExamples`(19 КБ),
   `pfcServerExamples`(19 КБ — живые вызовы `model.Export(...)`), `pfcComponentFeatExamples`(14 КБ),
   `pfcModelCheckExamples`(14 КБ), `pfcParameterExamples`, `pfcFamilyMemberExamples`, `pfcRelationExamples`,
   `pfcWindowExamples` (raster), `MakeVRMLOnEraseExample`; асинхронные — `..\jlinkasyncexamples\`,
   сервлет — `..\jlink_servlet\`, загрузчик — `..\jlink_loader\`, упражнения — `..\..\exercises\`.

### Крупные классы (число методов)
`pfcBaseSession` 87 · `pfcMaterial` 72 · `pfcModel` 41 · `pfcSolid` 40 · `pfcDisplay` 28 ·
`pfcFamilyMember` 25 · `pfcTable` 25 · `pfcSession` 24 · `pfcFeature` 21 · `pfcSelection` 21 ·
`pfcMassProperty` 21 · `pfcView2D` 20 · `pfcModel2D` 19 · `pfcModelDescriptor` 19 · `pfcComponentFeat` 19 ·
`pfcWindow` 19 · `pfcServer` 19 · `pfcDimension2D` 18 · `pfcSheetOwner` 17 · `pfcAssembly` 13 ·
`pfcSheetData` 10 · `pfcParameter` 9 · `pfcNote` 8 · `pfcLayer` 7 · `pfcFamilyTableRow` 7 ·
`pfcParameterOwner` 6 · `pfcTableCell` 5 · `pfcRelationOwner` 5 · `pfcModelItem` 4 · `pfcSimpRep` 3.

### Полезные методы `pfcBaseSession` (крупнейший класс, 87)
Модели: `ListModels`, `ListModelsByType`, `GetActiveModel`, `GetCurrentModel`, `GetModel`, `GetModelFromDescr`,
`GetModelFromFileName`, `RetrieveModel`, `RetrieveModelWithOpts`, `CreatePart`, `CreateAssembly`,
`CreateDrawingFromTemplate`, `Import2DModel`, `EraseUndisplayedModels`, `GetByRelationId`.
Окна/выбор: `CreateModelWindow`, `GetModelWindow`, `ListWindows`, `GetWindow`, `GetCurrentWindow`,
`SetCurrentWindow`, `FlushCurrentWindow`, `Select`, `OpenFile`.
Настройки/команды: `SetConfigOption`, `GetConfigOption`, `GetConfigOptionValues`, `RunMacro`,
`SetDimensionDisplayMode`, `GetDimensionDisplayMode`, `AllowDuplicateModelItems`.
Экспорт/проверки: `ExportDirectVRML`, `ExportCurrentRasterImage`, `ExportFromCurrentWS`,
`ExecuteModelCheck`, `RegisterCustomModelCheck`, `RegisterRelationFunction`, `IsConfigurationSupported`,
`IsGeometryRepSupported`.
Серверы/прочее: `RegisterServer`, `ListServers`, `GetServerByAlias/Url`, `GetActiveServer`,
`GetMessageContents`, `GetLocalizedMessageContents`, `GetConnectionId`,
`UIRegisterFileSave`, `UIRegisterFileOpen`, `UIRegisterFileOpen`.

### Прочее, что стоит знать
- `pfcModel` (файлы, 41): `Backup`, `Copy`, `CopyAndRetrieve`, `Rename`, `Save`, `Erase`,
  `EraseWithDependencies`, `Delete`, `Display`, `ListDependencies`, `ListDeclaredModels`, `CreateLayer`,
  `CleanupDependencies`, `IsCommonNameModifiable` + `Export`.
- `pfcSolid` (40): `Regenerate`, `ExecuteFeatureOps`, `EvalOutline`, `CreateLocalGroup`, `CreateNote`,
  `ListFailedFeatures`, `ListFeaturesByType`, `ListCrossSections`, `GetCrossSection`, `HasRetrievalErrors`,
  `GetFeatureByName/ById`, `CreateImportFeat`, `GetMassProperty`, `ListGroups`, `ExportShrinkwrap`,
  SimpRep-семейство (`ActivateSimpRep`, `GetActiveSimpRep`, `CreateSimpRep`, `SelectSimpRep`, `GetSimpRep`,
  `GetMasterRep`, `GetGraphicsRep`, `GetGeomRep`, `DeleteSimpRep`).
- `pfcFeature` (21): `Create{Suppress,Resume,Delete,ReorderBefore,ReorderAfter}Op`,
  `ListChildren/Parents/SubItems`, `GetFeatType/SubType/Status/Group/Pattern/GroupPattern/Number`,
  `GetIsVisible/Readonly/GroupMember/Embedded`, `GetVersionStamp`.
- `pfcComponentFeat` (19) — компоненты сборки; `pfcAssembly` (13) — сборка; `pfcFamilyMember` (25) + `pfcFamilyTableRow` (7) — семейства;
  `pfcTable`/`pfcTableCell` (25/5) — таблицы; `pfcDimension2D` (18) / `pfcNote` (8) / `pfcView2D` (20) —
  оформление чертежа; `pfcDisplay` (28) — отображение; `pfcMaterial` (72) — материалы.
- `pfcWindow` (19): `ExportRasterImage` + `Bitmap/TIFF/JPEG/EPSImageExportInstructions_Create(h, w)`.
- `wfc*` (Windchill-расширения): **`wfcWParameterOwner.ExportParameterTable` — выгрузка таблицы параметров
  в CSV/TXT** (для дома крайне полезно), `wfcWSession` (40), `wfcWSolid` (51), `wfcAppearance` (26).

## 7. ГРАБЛИ (все проверены живьём)
1. **Путь с пробелами**: `Creo 12.4.2.0` в `-Djava.library.path` — при `Start-Process` аргумент рвётся
   (`Could not find or load main class 12.4.2.0\Common`). Квотить ЦЕЛИКОМ или запускать через `.bat`.
2. **classpath**: jar держать рядом с классом (`-cp ".;pfcasync.jar"`), иначе пробелы пути ломают список.
3. **`ParamValue` — объект**, не строка: нужен типовой геттер (`GetStringValue`…).
4. **Русские имена**: данные корректны (CREOSON-проба: 23 из 47 имён кириллицей, JSON верен), но консоль
   (cp866) печатает `???` — писать результат в файл UTF-8.
5. **DXF/DWG/2D на детали** → `XToolkitGeneralError`; нужен чертёж.
6. **`com.ptc.pfc.pfcExport` — пакет**; статический держатель `_Create` — `com.ptc.pfc.pfcExport.pfcExport`.
7. **Ошибки JLINK — исключения** `pfcExceptions.*` (`jxthrowable`, `XToolkitGeneralError`,
   `pfcDrawingCreateError`…): ловить и логировать, программа не должна падать целиком.
8. **Одна сессия — один канал**: вторая программа подключиться может, но длинные операции не смешивать.
9. Java 25: `WARNING: A restricted method in java.lang.System has been called (loadLibrary)` — не ошибка.
10. **Долгие вызовы**: обрыв соединения подвешивает мост PTC (лечится сбросом Creo+CREOSON по PID).

## 8. ФАЙЛЫ И ВОСПРОИЗВЕДЕНИЕ
```
D:\AI\PROBA\jlink_probe\
    DirectProbe.java / .class      - проба 1: подключение
    DirectProbe2.java / .class     - проба 2: параметры + масса
    DirectProbe3.java / .class     - проба 3: экспорт
    pfcasync.jar                   - JLINK API (копия)
    out\                           - pin_splitk.stp / .igs / pin_splitk_prt.wrl
    out*.txt / err*.txt            - протоколы прогонов
D:\AI\tools\agent\creo_export\     - ИНСТРУМЕНТ (см. его README.md)
    CreoExport.java, creo_export.bat, _test_all.bat, pfcasync.jar, out\
D:\AI\PROBA\parse_otk_v2.py        - разбор otk_methods.txt -> карты API
D:\AI\PROBA\pfc_api_full_map.txt   - 717 классов + классы экспорта/импорта
D:\AI\PROBA\pfc_api_key_methods.txt - методы ключевых классов (C++ | Java | exposure | описание)
D:\AI\PROBA\jlink_direct_probe_notes.md - конспект проб
D:\AI\PROBA\POLYGON_NOTES.md       - §17 (JLINK), §19 (карта API), §20 (экспорт)
```
**Повторить пробу:**
```
1) Поднять Creo:  CREO-START.bat   (или python D:\AI\tools\agent\ctl.py up)
2) cd D:\AI\tools\agent\creo_export
3) creo_export.bat step pin_splitk.prt        -> out\pin_splitk.stp
   creo_export.bat iges pin_splitk.prt        -> out\pin_splitk.igs
   creo_export.bat vrml pin_splitk.prt        -> out\pin_splitk_prt.wrl
```
Компиляция вручную (если нужно):
```
set "ARCH=D:\PTC\CREO12\Creo 12.4.2.0\Common Files\x86e_win64"
set PATH=%ARCH%\lib;%ARCH%\obj;%PATH%
set PRO_COMM_MSG_EXE=%ARCH%\obj\pro_comm_msg.exe
javac -cp "pfcasync.jar" CreoExport.java
java "-Djava.library.path=%ARCH%\lib;%ARCH%\obj" -cp ".;pfcasync.jar" CreoExport step pin_splitk.prt
```

## 9. ЧТО ПРОВЕРЕНО, А ЧТО НЕТ (честная карта)
**Проверено живьём (22–23.09.2026):** подключение к живой сессии и отключение без вреда Creo;
чтение `cwd`, `GetFileName`/`GetFullName`; список параметров (`ListParams`, 47 шт.) и масса/объём/площадь
(`GetMassProperty`); экспорт STEP3D / IGES3DNew / VRML / **NEUTRAL** (файлы на диске с размерами);
отказ DXF и PDF на детали; разведка сигнатур `javap`; инвентарь 717 классов и 121 класса
`*ExportInstructions*`; русские имена параметров (23/47) через CREOSON с проверкой JSON.

**Инструмент собран и принят на живом Creo:** `D:\AI\tools\agent\creo_export`
(`CreoExport.java` + `creo_export.bat` + `_test_all.bat` + `pfcasync.jar`).
Пакетная приёмка `_test_all.bat` (модель `pin_splitk.prt`):
`step` OK 13 467 б · `iges` OK 55 268 б · `vrml` OK 26 233 б · `neutral` OK 67 100 б (файл `.neu.1`) ·
`pdf` ОТКАЗ `XToolkitInvalidType`. Итог: **на детали работают STEP / IGES / VRML / NEUTRAL**.

**Грабли, пойманы при приёмке:** (а) bat надо звать по ПОЛНОМУ пути — детач-запуск с голым именем
не находит файл; (б) Creo дописывает суффикс версии к экспортируемому файлу (`name.neu` → `name.neu.1`,
повтор → `.neu.2`) — проверка наличия должна быть по префиксу; (в) PowerShell глушит stdout Java,
если та пишет WARNING в stderr — вывод забирать из файла лога.

**НЕ проверено (кандидаты на следующий прогон):**
`AsyncConnection_Start` (запуск Creo из программы); `RunMacro`/mapkey из Java;
`wfcWParameterOwner.ExportParameterTable` (CSV/TXT параметров); `pfcModel.Copy`/`CopyAndRetrieve`
(копия проекта программой); `ExportRasterImage` + JPEG/TIFF-инструкции (картинка окна);
`CreateDrawingFromTemplate` и 2D-экспорт (DXF/DWG/PDF чертежа); семейства (`pfcFamilyMember` 25);
`ExecuteModelCheck`; серверы/Windchill (`pfcServer`, `wfc*`); запись (`CreateFeature` — «not implemented»).

## 10. СРАВНЕНИЕ КАНАЛОВ (итог для дома)
| Канал | Плюсы | Минусы | Когда брать |
|---|---|---|---|
| **CREOSON** (JSON) | 18 групп / 199 функций, без сборки, из Python | лишний сервер (8080) и JVM-мост; часть операций не покрыта | рутина: открыть/переименовать/скопировать/BOM/картинка |
| **JLINK** (Java) | полный доступ (717 классов, 1873 в jar), циклы, пачки, свой UI | нужна среда (PATH/dll/jar), компиляция, класс-обёртка | своя программа/утилита, массовый экспорт |
| **Creo.JS** (Давыдовка) | HTML+JS в самом Creo, свой сервер 8000 | свой сервер, ограничен задачами дома | инженерные формы КБ |
| **OTK C++ / VB API / Web.Link** | максимальная власть внутри Creo | сборка, компилятор, порог входа | плагины внутри Creo |

**Вывод исследования:** «программка» на Java к Creo — **рабочий, проверенный путь дома**;
CREOSON и JLINK не конкуренты, а два этажа одного дома: JSON для рутины, Java — для настоящей автоматизации.