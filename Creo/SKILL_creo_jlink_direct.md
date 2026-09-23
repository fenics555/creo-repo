---
name: creo-jlink-direct
system: Creo
description: Use when: нужно УПРАВЛЯТЬ Creo напрямую из программы (Java/JLINK, pfc*), без CREOSON — подключиться к Creo, писать программку/утилиту, читать параметры/массу, экспортировать
when: jlink, j-link, java, pfcasync, pfc, otk_java_free, прямое управление, программка, утилита, приложение, programmatic, без creoson, com.ptc.pfc, otk
priority: high
date: 22.09.2026
---
# ПРЯМОЕ УПРАВЛЕНИЕ CREO ИЗ ПРОГРАММЫ (JLINK / `pfc*`) — БЕЗ CREOSON

Когда нужна **своя программа** (Java-утилита, обработчик, плагин), а не JSON-рутина:
JLINK даёт полный доступ к `pfc*` и не требует сервера.

## Когда JLINK, а когда CREOSON
| Задача | Средство |
|---|---|
| Рутина: открыть/переименовать/скопировать/параметр/BOM/картинка | **CREOSON** (JSON, дёшево) — `SKILL_creoson_routine.md` |
| Своя программа, цикл по сотням моделей, тонкая логика, экспорт пачкой, UI-команды | **JLINK** (этот скилл) |
| Уже есть сервер Давыдовки | Creo.JS (канал Creo.JS + Python-сервер 8000) |

Один слой `pfc*` — много каналов (Creo.JS, Object TOOLKIT C++/Java, VB API, Web.Link, JLINK);
**CREOSON = JSON поверх JLINK**.

## СРЕДА (без этого `UnsatisfiedLinkError: Can't find dependent libraries`)
```java
System.loadLibrary("pfcasyncmt");           // или pfcasync
```
- `PATH` += `D:\PTC\CREO12\Creo 12.4.2.0\Common Files\x86e_win64\lib` и `...\x86e_win64\obj`;
- JVM-флаг `-Djava.library.path="<те же две папки>"`;
- `PRO_COMM_MSG_EXE` = `...\x86e_win64\obj\pro_comm_msg.exe`;
- classpath: `pfcasync.jar` (`Common Files\text\java`) + `pfcasyncmt`.
  ⚠️ Пробелы в пути ломают classpath при `Start-Process` → держать `pfcasync.jar` рядом с классом, `-cp ".;pfcasync.jar"`.

## ПОДКЛЮЧЕНИЕ / ЗАПУСК / ЗАВЕРШЕНИЕ
```java
pfcAsyncConnection.Connection c =
    pfcAsyncConnection.AsyncConnection_Connect(null, null, null, 60);   // к ЗАПУЩЕННОМУ Creo
// либо запустить Creo:
// c = AsyncConnection_Start("pro -g:no_graphics -i:rpc_input", null);
Session s = c.GetSession();
s.GetCurrentDirectory();
// ... работа ...
c.Disconnect(5);   // Creo ОСТАЁТСЯ живым
// c.End();        // закрыть Creo
```
Проверено живьём (22.09.2026): Creo остаётся работать после `Disconnect`.

## РЕЦЕПТЫ
```java
// модель
ModelDescriptor d = pfcModel.ModelDescriptor_Create(ModelType.MDL_PART, "pin_splitk", null);
Model m = s.RetrieveModel(d);

// параметры
Parameters ps = ((ParameterOwner) m).ListParams();
for (int i = 0; i < ps.getarraysize(); i++) {
    Parameter p = ps.getitem(i);
    String name = p.GetName();          // может быть РУССКИМ
    // p.GetValue() → объект ParamValue: нужен типовой геттер (GetStringValue/GetDoubleValue…),
    // иначе печатается как com.ptc.pfc.Implementation.pfcModelItem$ParamValue@hash
}

// масса/объём/площадь
MassProperty mp = ((Solid) m).GetMassProperty(null);
mp.GetMass(); mp.GetVolume(); mp.GetSurfaceArea();

// файловые операции pfcModel: Backup / Save / Rename / Copy / CopyAndRetrieve / Erase / Display
// зависимости: m.ListDependencies(); m.ListDeclaredModels();
```
Живой результат: 47 параметров + `mass=0.002014…` с `pin_splitk.prt` (проба 2).

## КАРТА API: 717 классов (`otk_methods.txt`, 4159 строк)
Крупные: `pfcBaseSession` 87 · `pfcMaterial` 72 · `pfcModel` 41 · `pfcSolid` 40 · `pfcDisplay` 28 ·
`pfcFamilyMember` 25 · `pfcTable` 25 · `pfcSession` 24 · `pfcFeature` 21 · `pfcSelection` 21 ·
`pfcMassProperty` 21 · `pfcView2D` 20 · `pfcModel2D` 19 · `pfcWindow` 19 · `pfcServer` 19 ·
`pfcDimension2D` 18 · `pfcSheetOwner` 17 · `pfcAssembly` 13.
Полные карты: `D:\AI\PROBA\pfc_api_full_map.txt`, `pfc_api_key_methods.txt` (скрипт `parse_otk_v2.py`).

## ЭКСПОРТ/ИМПОРТ: 69 классов `*Export*`
Формат = свой класс `pfc*ExportInstructions`, передаётся в `Model.Export(...)`:
STEP 3D/2D/File, IGES 3D/New/File, DXF 2D/3D, DWG 2D/3D, PDF(8), STL ASCII/Binary, VRML(+Direct/Model),
JT 3D, Parasolid 3D, ACIS 3D, NEUTRAL, CGM(6), VDA, SET, FIAT, Medusa, Inventor, CATIA (Product/Part/CGR/
Facets/Model/Session), SolidWorks (Asm/Part), UG, CADDS, ProductView, Shrinkwrap(+Model 18), Render,
Raster(10)/Bitmap/JPEG/TIFF/EPS, BOM, FeatInfo, FeatId, Program, Material, Relation,
MFG CL / MFGFeat CL / MFGOper CL, `pfcCoordSysExportInstructions`(15), `pfcExport3DInstructions`(13).
Импорт: `pfcDWGImport2DInstructions`, `pfcSTEPImport2DInstructions`, `pfcIGES*Import*`,
`pfcConfigImportInstructions`, `pfcCableParamsImportInstructions`, `pfcConnectorParamsImportInstructions`,
`pfcSpoolImportInstructions`, `pfcProgramImportInstructions`, `pfcWireListImportInstructions`,
`pfcRelationImportInstructions`.

### Рабочий рецепт экспорта — ПРОВЕРЕНО ЖИВЬЁМ (22.09.2026)
```java
GeometryFlags f = pfcExport.GeometryFlags_Create();
f.SetAsSolids(true);

STEP3DExportInstructions step = pfcExport.STEP3DExportInstructions_Create(
        AssemblyConfiguration.EXPORT_ASM_SINGLE_FILE, f);
model.Export("D:\\out\\pin_splitk.stp", step);        // STEP3D  ✓ 13 466 б

IGES3DNewExportInstructions ig = pfcExport.IGES3DNewExportInstructions_Create(
        AssemblyConfiguration.EXPORT_ASM_SINGLE_FILE, f);
model.Export("D:\\out\\pin_splitk.igs", ig);          // IGES3D  ✓ 55 268 б

VRMLModelExportInstructions v = pfcModel.VRMLModelExportInstructions_Create("D:\\out\\");
model.Export("", v);                                  // VRML    ✓ pin_splitk_prt.wrl 26 233 б

DXFExportInstructions dxf = pfcModel.DXFExportInstructions_Create();
model.Export("D:\\out\\pin_splitk.dxf", dxf);          // ✗ XToolkitGeneralError —
                                                      //   DXF/2D-форматы нужен ЧЕРТЁЖ, а не деталь
```
Вывод: **программка-экспортёр на Java работает** (Creo остаётся жив после `Disconnect`).
Проба: `D:\AI\PROBA\jlink_probe\DirectProbe3.java` (+ `.class`), результат — `out6.txt`, файлы в `out\`.

### Варианты `_Create` (точные сигнатуры из `javap`)
- 3D с конфигурацией сборки: `*_Create(AssemblyConfiguration, GeometryFlags)` — STEP3D, IGES3DNew, JT3D,
  ParaSolid3D, ACIS3D, UG3D, CATIA*, SW*, VDA3D.
- Без аргументов: `DXF3DExportInstructions_Create()`, `DWG3DExportInstructions_Create()`,
  `CADDSExportInstructions_Create()`, `NEUTRALFileExportInstructions_Create()`,
  `PDFExportInstructions_Create()`, `ProductViewExportInstructions_Create()`,
  `BOMExportInstructions_Create()`, `MaterialExportInstructions_Create()`,
  `DXFExportInstructions_Create()`, `STEP2DExportInstructions_Create()`, `DWGSetupExportInstructions_Create()`.
- С именем файла: `IGESFileExportInstructions_Create()`, `STLASCIIExportInstructions_Create(String)`,
  `STLBinaryExportInstructions_Create(String)`, `InventorExportInstructions_Create(String)`,
  `CATIAFacetsExportInstructions_Create(String)`, `RenderExportInstructions_Create(String)`.
- С флагами 2D-модели: `IGES3DExportInstructions_Create(GeomExportFlags)`, `STEPExportInstructions_Create(...)`.
- `VRMLDirectExportInstructions_Create(String, String)`, `VRMLModelExportInstructions_Create(String)`.
- `AssemblyConfiguration`: `EXPORT_ASM_SINGLE_FILE` | `EXPORT_ASM_MULTI_FILES` | `EXPORT_ASM_FLAT_FILE` |
  `EXPORT_ASM_ASSEMBLY_PARTS`.
- `GeometryFlags`: `SetAsSolids/SetAsSurfaces/SetAsWireframe/SetAsQuilts(boolean)`.
- Вызов всегда: **`model.Export(путь, инструкции)`** (для VRML путь игнорируется → `""`).

## ПРИМЕРЫ PTC (готовые образцы!)
`...\otk_java_free\otk_java_appls\jlinkexamples\`: `pfcDrawingExamples`(57 КБ), `pfcExamplesMenu`(56 КБ),
`pfcReadBasicFeatPropertiesExamples`(19 КБ), `pfcServerExamples`(19 КБ), `pfcComponentFeatExamples`(14 КБ),
`pfcModelCheckExamples`(14 КБ), `pfcPopupExamples`, `pfcCommandExamples`, `pfcRelationExamples`,
`pfcExternalDataExamples`, `pfcParameterExamples`, `pfcFamilyMemberExamples`, `pfcSelectionExamples`,
`pfcSessionExamples`, `pfcDimensionExamples`, `pfcModelExamples`, `pfcDisplay*Examples`,
`MakeVRMLOnEraseExample`, `pfcServerExamplesWF4`;
асинхронные — `..\jlinkasyncexamples\`; сервлет — `..\jlink_servlet\`; загрузчик — `..\jlink_loader\`.
(Полная таблица — в `CREOSON\SKILL_creoson_pfc_map.md`.)

## КАК САМОМУ РАЗВЕДАТЬ ЛЮБОЙ МЕТОД (методология дома)
1. **Справочник**: `...\Common Files\otk_cpp_doc\otk_methods.txt` — 4165 строк, **717 классов**,
   столбцы `C++ Header | C++ Class | C++ Method | Java Package | Java Class | Java Method | Exposure | Description`.
   Разбор: `D:\AI\PROBA\parse_otk_v2.py` → `pfc_api_full_map.txt`, `pfc_api_key_methods.txt`.
2. **Файл НЕ полный**: у `pfcDrawing`/`pfcUnits` методов почти нет — чертёжное API в `pfcModel2D`(19),
   `pfcView2D`(20), `pfcSheetOwner`(17), `pfcDimension2D`(18), `pfcDrawingDimCreateInstructions`(14),
   `wfcDrawingViewDisplay`(13).
3. **Истина — в jar**: `pfcasync.jar` = 1873 класса `com/ptc/pfc`. Список: открыть jar как zip,
   фильтр `*.class`. Сигнатуры: `javap -classpath pfcasync.jar com.ptc.pfc.pfcExport.pfcExport`.
   ⚠️ **Статический держатель `_Create` — вложенный класс с тем же именем**: `com.ptc.pfc.pfcExport.pfcExport`,
   `com.ptc.pfc.pfcModel.pfcModel` (НЕ `com.ptc.pfc.pfcExport` — тот не найдётся!).
4. **Копировать приём из примеров PTC** (см. ниже) — там готовые вызовы, включая `model.Export(...)`.

## PDF ИЗ ЧЕРТЕЖА — ГЛАВНАЯ РУТИНА ДОМА (проверено живьём 23.09.2026)
```java
s.ChangeDirectory("D:\\AI\\PROBA\\drw_pdf");                        // 1) папка чертежа (его деталь рядом)
Model d = s.RetrieveModel(pfcModel.ModelDescriptor_CreateFromFileName(
        "D:\\AI\\PROBA\\drw_pdf\\knockout_1.drw"));                  // 2) чертёж по полному пути
d.Display();                                                        // 3) ОБЯЗАТЕЛЬНО показать
d.Export(out + "knockout_1.pdf", pfcExport.PDFExportInstructions_Create());   // ✓ 26 276 б
```
Живой вывод: `cd=D:\AI\PROBA\drw_pdf\`, `model=knockout_1.drw fullname=KNOCKOUT_1`, `displayed`,
`OK knockout_1.pdf 26276 bytes`, `EXPORT OK` (файл `%PDF-1.7`).

**Три условия, иначе отказ:**
- **чертёж** (не деталь): на детали `pfcExceptions$XToolkitInvalidType`;
- **рабочая папка = папка чертежа** (иначе его деталь не найдётся);
- **`Model.Display()`** до экспорта: без показа — `pfcExceptions$XToolkitNotDisplayed`.

**Сверка с домашней рутиной:** CREOSON `interface:export_pdf`
(`creo:cd` → `file:open` (display) → `export_pdf{file, filename, dirname, use_drawing_settings:true}`)
дал `knockout_1_creoson.pdf` **26 262 б** против JLINK **26 276 б** — оба `%PDF-1.7`.
Разница от `use_drawing_settings` (у CREOSON: Font Stroke = Stroke All Fonts, Color Depth = Grayscale).

**Тонкая настройка (JLINK):** `PDFExportInstructions.SetOptions(PDFOptions)` — список
`PDFOption{GetOptionType(), GetOptionValue()}`; типы `PDFOptionType`:
`PDFOPT_SHEET_RANGE`, `PDFOPT_SHEETS`, `PDFOPT_FONT_STROKE`, `PDFOPT_COLOR_DEPTH`, `PDFOPT_HIDDENLINE_MODE`,
`PDFOPT_SEARCHABLE_TEXT`, `PDFOPT_RASTER_DPI`, `PDFOPT_LAYER_MODE`, `PDFOPT_PARAM_MODE`, `PDFOPT_HYPERLINKS`,
`PDFOPT_BOOKMARK_ZONES/VIEWS/SHEETS/FLAG_NOTES`, `PDFOPT_TITLE/AUTHOR/SUBJECT/KEYWORDS`,
`PDFOPT_PASSWORD_TO_OPEN`, `PDFOPT_MASTER_PASSWORD`, `PDFOPT_RESTRICT_OPERATIONS`; плюс `SetProfilePath(...)`.
Ещё по теме: `pfcBaseSession.ChangeDirectory(String)`, `GetCurrentDirectory()`,
`ListFiles(dir, FileListOpt, mask)`, `CreateModelWindow(Model)`, `Model.DisplayInNewWindow()`.

## НАСТРОЙКА ПРАВИЛЬНОГО PDF — КОНФИГ ДОМА (проверено 23.09.2026)
PDF «по-домашнему» = форматки + стандарт оформления + перья принтера. Всё это задаётся `config.pro`:
| Опция | Значение дома | Зачем |
|---|---|---|
| `pro_format_dir` | `Z:\PTC\CREO-START\НАСТРОЙКИ\ФОРМАТЫ\` | **форматки** (163 файла `a0…a4.frm`) |
| `drawing_setup_file` | `…\НАСТРОЙКИ\configs/MY_ESKD.dtl` | стандарт оформления чертежа (ЕСКД) |
| `format_setup_file` | `…\configs/MY_ESKD.dtl` (в живой сессии — `dwgform.dtl`) | настройки формата |
| `pro_dtl_setup_dir` | `…\НАСТРОЙКИ\configs\` | папка `.dtl` |
| `pen_table_file` | `…\НАСТРОЙКА_ПРИНТЕРА/table.pnt` | **перья/толщины линий для печати и PDF** |
| `pro_plot_config_dir` | `…\НАСТРОЙКА_ПРИНТЕРА\` | папка конфигураций печати |
| `pdf_use_pentable`, `use_8_plotter_pens` | `yes`, `yes` | применять таблицу перьев в PDF |
| `pro_table_dir`, `start_model_dir`, `pro_symbol_dir`, `pro_group_dir`, `pro_material_dir`, `tolerance_table_dir`, `pro_sheet_met_dir`, `mfg_template_dir` | `…\НАСТРОЙКИ\…` | таблицы, шаблоны, символы, UDF, материалы, допуски, гибка, техпроцессы |
| `template_solidpart` / `template_designasm` / `template_drawing` | `…\ШАБЛОНЫ\mm_part.prt` / `sborka_mm.asm` / `c_drawing.drw` | стартовые шаблоны |
Боевой файл: `Z:\PTC\CREO-START\START-STD\config.pro` (17 125 б; копия в `START-Config\config.pro`).
**Старт Creo должен быть из папки с этим конфигом** (`START-STD`, скрипт `Z:\PTC\CREO-START\START-STD\CREO-START.bat`).
⚠️ У локального старта `D:\PTC\CREO-LOCAL-SETUP\CREO-LOCAL-START\config.pro` (12 761 б) этих строк **НЕТ** —
Creo оттуда даст PDF без форматок и перьев (`pro_format_dir`/`drawing_setup_file`/`pen_table_file` пусты).

**Как проверить/починить у ЖИВОЙ сессии** (загрузки файла в API нет — только по одной опции):
```
creo_pdf.bat config-read                 # что реально загружено (JLINK GetConfigOption)
creo_pdf.bat config-load "Z:\PTC\CREO-START\START-STD\config.pro"   # применить опции дома (SetConfigOption)
```
Снято живьём 23.09.2026: сессия с cwd `Z:\PTC\CREO-START\START-STD\` **уже имеет** дом: `pro_format_dir`=ФОРМАТЫ,
`drawing_setup_file`=`…configs/MY_ESKD.dtl`, `pen_table_file`=`…/table.pnt`, `pdf_use_pentable=YES`.
Отличие от файла — только `format_setup_file` (в сессии `dwgform.dtl`).

**`format_setup_file` против `drawing_setup_file`** (важно понимать): `format_setup_file` задаёт настройки,
которые **зашиты в саму форматку** (внутренний `dwgform.dtl`) и применяются, когда форматка подгружается
или создаётся; `drawing_setup_file` (= `MY_ESKD.dtl`) применяется **к чертежу** (тексты, стрелки, допуски)
и обновляется при работе с чертежом. Поэтому «обновить настройки MY_ESKD.dtl в готовом чертеже» и
«настройки внутри форматки» — две разные операции, и в PDF видно результат обеих.

## DETAIL-ОПЦИИ ЧЕРТЕЖА (.dtl): ЧТО МОЖЕТ JLINK — ПРОВЕРЕНО 23.09.2026

Вопрос: можно ли программой прочитать/дописать настройки чертежа (detail-опции) и сохранить их в `.drw`?
Ответ по фактам API (перебран весь `pfcasync.jar`, живой Creo 12):

| Что искали | Что есть на самом деле | Вывод |
|---|---|---|
| классы `*Option` для чертежа | `pfcExport$PDFOption`, `LayerExportOptions`, `DrawingCreateOptions`, `pfcSession$RetrieveModelOptions` | detail-опций чертежа в JLink НЕТ |
| `pfcDrawing.Drawing` | только размеры (`IsDimensionAssociative`, `SetDimensionLocation`, `EraseDimension`…) + наследует `Model2D` | ни чтения, ни записи `.dtl` |
| `Model.Import(path, instructions)` | это 3D-интерфейсы (STEP/IGES и т.п.) | не про `.dtl` |
| `Session.GetConfigOption` / `SetConfigOption` | это опции **config.pro**, а не detail-набор | detail-набор недоступен |
| выполнить запись mapkey из API | в jar нет ни одного класса/метода `Mapkey` | записать опции mapkey'ем нельзя |

**Итог:** JLink не умеет ни читать, ни писать detail-опции чертежа. Это умеет только C-API TOOLKIT
(`ProMdlDetailOptionSet` и родственные; у нас есть protoolkit + `creo_help_pma`), то есть отдельная
C-программа, а не JLink.

**Почему PDF-рутина дома всё равно работает:** оформление приходит в чертёж **из сессии** —
`drawing_setup_file = …\НАСТРОЙКИ\configs/MY_ESKD.dtl` применяется к открытому чертежу (тексты, стрелки,
допуски), а `format_setup_file` — к самой форматке. Поэтому правильный путь: печатать PDF из Creo,
**запущенного из папки боевого `config.pro`** (так и делает `creo_pdf`, см. `creo-find`/`creo-start`),
а не «починить каждый готовый `.drw`». Проверка настроек живой сессии — `creo_pdf.bat config-read`.

**Как программа сама узнаёт каталог Creo** — режим `config-find`:
```
creo_pdf.bat config-find
cwd сессии: Z:\PTC\CREO-START\START-STD\
  ЕСТЬ  17125 б   Z:\PTC\CREO-START\START-STD\config.pro     ← боевой (папка старта Creo)
  нет           C:\Users\User\config.pro
  нет           D:\PTC\CREO12\Creo 12.4.2.0\text\config.pro
```
Логика: рабочая папка живой сессии (= где Creo стартовал, там его `config.pro`) → профиль пользователя →
loadpoint Creo, вычисленный из `java.library.path` (`…\Common Files\x86e_win64\lib` → вверх два уровня).

**А если сессии нет?** Режим `config-scan` ищет `config.pro` по известным местам дома **без Creo**
и сам помечает, какой годен для PDF (проверено 23.09.2026):
```
  БОЕВОЙ (годен для PDF)  17125 б   Z:\PTC\CREO-START\START-STD\config.pro
  БОЕВОЙ (годен для PDF)  17125 б   Z:\PTC\CREO-START\START-Config\config.pro
  БОЕВОЙ (годен для PDF)  17002 б   Z:\PTC\CREO-START\START-Config\lokal для Сергея\config.pro
  есть, но БЕЗ домашних путей  12761 б   D:\PTC\CREO-LOCAL-SETUP\CREO-LOCAL-START\config.pro
стартовые скрипты Creo:  ЕСТЬ Z:\PTC\CREO-START\START-STD\CREO-START.bat
```
**Нужна ли живая сессия для PDF? Да.** JLINK подключается к **уже запущенному** Creo.
**Как поднять Creo ШТАТНО (без домашнего бата):** домашний `CREO-START.bat` делает ровно `cd /d START-STD`
и `start parametric.exe` — **без ключей**. Значит достаточно запустить `parametric.exe` с **рабочей папкой =
папка боевого `config.pro`**: Creo читает `config.pro` из рабочей папки, оттуда приходят форматки,
`MY_ESKD.dtl`, `table.pnt`. Путь установки берётся из реестра Windows:
`HKLM\SOFTWARE\PTC\PTC Creo Parametric\<версия>` → `InstallDir` + `CommonFilesLocation`
(проверено 23.09.2026: `InstallDir = D:\PTC\CREO12\Creo 12.4.2.0\Parametric` → `…\bin\parametric.exe`).
Команды движка: `creo_pdf.bat creo-find` (найти установку) и `creo_pdf.bat creo-start [config.pro] [--dry]`
(запустить штатно; `--dry` — показать команду без запуска). В окне — кнопки «Найти Creo (реестр)»
и «Запустить Creo (штатно)». **Домашний `CREO-START.bat` для этого больше не нужен.**
**«Лимит»** — потолок числа чертежей, которые движок возьмёт в работу за прогон (и в отчёте `scan`,
и в `export`); страховка от многочасового прогона по большой ветке; **0 = без ограничения**.

**ОКНО для рук** (`D:\AI\tools\agent\creo_pdf\creo_pdf_gui.bat`): поля «Путь к config.pro» (с `Обзор…`,
кнопками «Из сессии» и «Применить к Creo») и «Папка проверки» (с `Обзор…`), кнопки `СКАН (отчёт)`,
`СОЗДАТЬ / ОБНОВИТЬ PDF` + лимит, `СТОП`, живой лог и итоговая строка. Обход — **по всем подпапкам**.
Приёмка 23.09.2026: `Z:\PTC\Work\000_01 Пользовательские изделия` (с подпапками) → 41 чертёж,
ок 31, **нет PDF 7, устарели 3**; после `pdf` на `mt150112` — пара стала свежей (195 157 б, `%PDF-1.7`).

## РУТИНА «PDF РЯДОМ С ЧЕРТЕЖОМ» (проверено на боевой папке)
Правило дома: рядом с `X.drw[.N]` лежит `X.pdf` **той же папки**; если PDF нет или он **старше** чертежа → обновить.
Масштаб (из `harvest.db`, таблица `pairs`): 24 607 пар, из них **8 687 помечены «устарел»**.
Проверка 23.09.2026: папка `Z:\PTC\Work\000_01 Пользовательские изделия\Болты Винты` — 6 чертежей,
5 в порядке, 1 устарел (`mt150112.pdf` старше `.drw` на 37 с); после экспорта — 6 из 6 в порядке.
**Инструмент:** `D:\AI\tools\agent\creo_pdf\creo_pdf.bat`
```
creo_pdf.bat scan   <папка>              # отчёт (Creo НЕ нужен) — где нет PDF / PDF старше
creo_pdf.bat export <папка> [лимит]      # создать недостающие/устаревшие (нужен живой Creo)
creo_pdf.bat pdf    <папка> <имя> [out]  # один чертёж
creo_pdf.bat config-read [config.pro] | config-load <config.pro>
```
Внутри: `ChangeDirectory(папка)` → `ModelDescriptor_Create(MDL_DRAWING, имя)` → `Display()` →
`Export(<имя>.pdf, PDFExportInstructions_Create())` → **cwd возвращается назад**. Код — `CreoPdf.java` (JLINK).
В агенте это инструменты **`creo_pdf_scan`** (чтение) и **`creo_pdf_export`** (под щитом согласования).

**Сборочные чертежи и уборка (проверено 23.09.2026, живой прогон «000_05 Приспособления»: 90 чертежей, 16 PDF):**
- **Сборочный чертёж** (`X.drw` при наличии `X.asm`) по имени не открывается — `pfcExceptions$XToolkitNotFound`.
  Лечение: **сначала поднять сборку** `RetrieveModel(ModelDescriptor_Create(MDL_ASSEMBLY, "X"))`, затем чертёж —
  после этого `plshaiba-4` и `plshaiba-5` дали `PDF OK` (итог: 0 ошибок вместо 3).
- Варианты `ModelDescriptor_CreateFromFileName` НЕ помогают: `XToolkitNotFound` / `XInvalidFileName` /
  `XUnknownModelExtension` (версионный `.drw.1` не принимается вовсе).
- **Уборка:** после экспорта чертёж убирается из сессии (`Model.Erase()`) — окна Creo не копятся;
  если чертёж был в сессии ДО прогона, он не трогается.
- **Просмотрщик PDF:** опция `PDFOPT_LAUNCH_VIEWER` (`PDFOption` + `pfcArgument.CreateBoolArgValue`) —
  по галочке «открывать PDF»; без галочки ничего не открывается.
- **Логи и перенос:** `creo_pdf\last_run_log.txt` + `creo_pdf\logs\run_<дата>_<время>.txt`;
  папка `creo_pdf` портативна (движок, jar, настройки `gui_settings.json`, логи — всё внутри).

## CREOSON ИЛИ БЕЗ НЕГО
Рутина PDF **не требует CREOSON**: скан делает Java (обход папки), экспорт — JLINK-ом.
CREOSON остаётся нужен инструментам агента (`creo_status`, `creo_session`, `parameter:*`, `bom:*` …),
но он — JVM-мост и падал живьём (23.09.2026 порт 8080 отвалился и поднимался заново).
Правило: **рутина дома (PDF) — прямой JLINK; CREOSON — для интерактивных инструментов агента**.

## ГРАБЛИ
1. `ParamValue` — не строка: печатать через типовой геттер (`GetStringValue`/`GetDoubleValue`).
2. Пробелы в пути к `pfcasync.jar` ломают classpath; пробелы в `-Djava.library.path` (`Creo 12.4.2.0`)
   при `Start-Process` рвут аргумент → `Could not find or load main class 12.4.2.0\Common`. Запуск — `.bat`.
3. Русские имена параметров/путей: данные корректны, но консоль (cp866) рисует `???` — писать в файл UTF-8.
4. Java 25: WARNING про native access — не ошибка.
5. Одновременно с CREOSON: если Creo один — работать можно, но не смешивать длинные операции в одной сессии.
6. Ошибки JLINK — исключения `pfcExceptions.*` (напр. `pfcDrawingCreateError`, `XToolkitGeneralError`),
   ловить по каждой операции и логировать (одна упавшая не должна убивать всю программу).
7. **DXF/DWG и все 2D-форматы на детали** дают `XToolkitGeneralError` — нужен ЧЕРТЁЖ (2D-модель).
   **PDF на детали отказывает** (`XToolkitInvalidType`) — PDF/DXF/DWG/2D только для ЧЕРТЕЖА.
   Проверенно-рабочие на детали: **STEP3D, IGES3DNew, VRML, NEUTRAL**.
   ⚠️ **Creo добавляет суффикс версии** к имени файла: просили `pin_splitk.neu` — получили `pin_splitk.neu.1`
   (повтор — `.neu.2`). Проверку наличия результата делать по префиксу, иначе ложный «FAIL».
8. `model.Export(путь, инструкции)` — имя файла для VRML игнорируется (передавать `""`).
9. Долгий вызов с обрывом соединения подвешивает мост PTC — лечится только сбросом Creo+CREOSON по PID.
10. `pfcBaseSession.CreateFeature` (и ряд других) — «not implemented in the current release»: читать описание
    перед использованием, а не верить названию.

## ГОТОВЫЙ ИНСТРУМЕНТ ДОМА
`D:\AI\tools\agent\creo_export\` — программа экспорта (не выбрасывать, расширять):
`CreoExport.java` + `creo_export.bat` (env + автокомпиляция + java) + `_test_all.bat` + `pfcasync.jar` + README.
`creo_export.bat step|iges|vrml|pdf|neutral|dxf3d|stl <модель> [папка]`, код возврата 0/1.
Живая приёмка 23.09.2026: `OK pin_splitk.stp 13467 bytes`, `EXPORT OK`.

## ФАЙЛЫ
**Разбор исследования целиком:** `D:\AI\repo\Creo\README_jlink_direct.md` (README: пробы, среда, API, экспорт, грабли).
Конспект: `D:\AI\PROBA\jlink_direct_probe_notes.md`. Пробы: `D:\AI\PROBA\jlink_probe\{DirectProbe,DirectProbe2,DirectProbe3}.java`.
Карты API: `pfc_api_full_map.txt`, `pfc_api_key_methods.txt`, `pfc_methods_by_class.txt` (скрипт `parse_otk_v2.py`).
Инструмент: `D:\AI\tools\agent\creo_export\` (+ его `README.md`).
Соответствие CREOSON↔`pfc*`: `CREOSON\SKILL_creoson_pfc_map.md`. Конспект полигона: `D:\AI\PROBA\POLYGON_NOTES.md` §17, §19, §20.