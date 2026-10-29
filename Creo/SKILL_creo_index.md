---
name: creo-index
system: INDEX
description: Use when: задача с темой Creo
when: creo, creoson, parametric, assembly, part, drawing
date: 22.09.2026
---

ЧТО ЗДЕСЬ: см. раздел «СТРУКТУРА И КАРТА СКИЛЛОВ» ниже — 8 подразделов (API, DOCS, CREOSON, COPY, STANDARDS, RELATIONS, DAVYDOVKA, INFRA).
КОГДА ОТКРЫВАТЬ: теги [CREO], [PARAMETRIC]
КОГДА ПИСАТЬ: CRASH триггеры: SKILL_creoson_probe_method, Ошибки\ERR_creoson_write_ops.md
универсальный закон — MANIFEST.md, специфика среды — в адаптерах

## ⚠️ ЗОНЫ РАБОТЫ С ФАЙЛАМИ (слово владельца, 03.10.2026) — ПЕРВОЕ, ЧТО ЧИТАТЬ
* **`D:\AI\PROBA` — можно ВСЁ** (создавать, переименовывать, удалять, пробовать, запускать Creo).
* **`Z:\PTC` — ТОЛЬКО ЧТЕНИЕ** (читать, сканировать, измерять, отчёты). Запись, ПУРГЕ, экспорт в папку
  склада, правка `config.pro`, запуск Creo с cwd на `Z:` — запрещены.
* Все пробы/опыты с Creo — **только в `PROBA`**, копия модели — под **уникальным именем**.
* Подробности: `SKILL_creo_file_reading.md` §0.

## 📌 СОСТОЯНИЕ НА 03.10.2026 (живая проверка, не пересказ)
* Инструмент чтения «в лоб» — `D:\AI\tools\agent\plm_reader\`, версия **V121** (26.10.2026; `PARSER_TAG="p23"`),
  база — `db\plm_reader_<дата>.db`. Дорожная карта инструмента и канон дома (переносимость, автообновление
  через GitHub, правило дисков) — `D:\AI\tools\agent\plm_reader\STRATEGY_PLM.md`
  (читается свежайший), настройки — `settings\settings.json`. Creo не нужен.
* Разбор чтения **деталь / сборка / чертёж** и список открытых долгов: `SKILL_creo_file_reading.md` §8.85–8.86.
* Проба чтения (живая, `PROBA`): деталь — материал/объём/роль/история; сборка — объём/история
  (параметры сборок **не читаются**, 0 %); чертёж — история (объём/обозначение **0 %** — законно).


РАЗРЕШЕНИЕ ВЛАДЕЛЬЦА (02.10.2026): CREOSON **не поднимается автоматически** (CTL его выключил
из автозапуска 23.09.2026 — он нужен только блокам на `creo_call` и поднимается по требованию),
**но по слову владельца запускается свободно**: «если нужен креосон — запускайте».
Не считай его «мёртвым» и не поднимай без надобности: инструменты класса Р (`orphan_scan`,
`config_audit`, `copy`) работают без него, он нужен только живым блокам Creo.

## ГЛАВНОЕ ОТКРЫТИЕ (22.09.2026): один `pfc*` — много каналов; CREOSON = обёртка
Управлять Creo можно **НАПРЯМУЮ, без CREOSON**:
- **Creo.JS** — JS во встроенном браузере Creo (этим идёт Давыдовка);
- **JLINK / Object TOOLKIT Java** — своя Java-программа на `com.ptc.pfc.*` (классы в `pfcasync.jar`)
  сама стартует/подключается к Creo (синхронно/асинхронно);
- **Object TOOLKIT C++ / Pro/TOOLKIT** — нативная DLL внутри процесса Creo (`protk.dat`);
- **VB API**, **Web.Link** — родственные каналы.
**CREOSON = JSON-сервер ПОВЕРХ JLINK**: `creoson-core-3.0.1.jar` = 268 классов
`com.simplifiedlogic.nitro.jlink`, а `com/ptc/pfc` в нём **0**; сами `pfc*` — в `pfcasync.jar`
(1873 класса). Разбор и пробы — `SKILL_creo_api_ecosystem.md`.
**Давыдовка** идёт каналом **Creo.JS** (мост `creojs.js` + серверные `*.creojs`) + свой
Python-сервер на 8000 (не CREOSON и не JLINK) — `SKILL_davydovka_creoson_map.md`.

## ПОДРАЗДЕЛЫ И КАРТА СКИЛЛОВ
| Подраздел | Что внутри |
|---|---|
| **`READ\`** | **чтение и правка файлов «в лоб» по частям** (03.10.2026): `SKILL_creo_read_core` (ядро формата), `_part`, `_asm`, `_drw`, `_mfg`, `_family` (семейства + библиотека `Libraries`), `_feat` (операции построения), `SKILL_creo_write_raw` (правка в лоб), `SKILL_creo_new_file` (создание файла — подготовка); карта — `READ\_INDEX.md`. Вход: `SKILL_creo_file_reading.md` (исторический конспект 1910 строк, номера §) |

### 🔴🔴 ДЕРЕВО ПОСТРОЕНИЯ И РАЗМЕРЫ — ЧИТАЙ ЭТО ПЕРВЫМ (28.10.2026)

**Порядок:** `READ\SKILL_creo_tree_jlink_etalon.md` → `READ\SKILL_creo_read_feature_types.md`
→ `READ\SKILL_creo_feature_tree.md` → `READ\SKILL_creo_feat_defs_deep_dive.md`
→ `Creo\SKILL_creo_bit_level_anatomy.md`. **Только потом лезть в байты** (грабля §86).

- **`READ\SKILL_creo_tree_jlink_etalon.md`** (новый, 28.10.2026) — **ЭТАЛОН из живого Creo**:
  `D:\AI\tools\agent\creo_export\tree_probe.bat` даёт `#FEAT <n> <feat_id> TYPE_<код> <имя>`,
  `#DIM feat=… sym=dN dimid=… val=…`, `#PARAM`. Живые эталоны: `g22033` — **9 элементов/8 размеров**,
  `ctkd_015_23_001` — **19/40**. Грабли: Creo не запущен → `XToolkitNotFound`; имя с версией →
  `XUnknownModelExtension` (подавать `x.prt`); enum `FeatureType` — номер через `getValue()`.
- **`READ\SKILL_creo_read_feature_types.md`** — типы фич: в Creo 13 **русские имена** (`ВЫТЯГИВАНИЕ` 9,
  `СКРУГЛЕНИЕ` 4, `ВРАЩЕНИЕ` 1, `ОПОРНАЯ ПЛОСКОСТЬ` 31), английские коды (`cutextrude`) — **0**.
- **`READ\SKILL_creo_feat_defs_deep_dive.md`** — 🔴 делимитер `FB E3 F7 80` **ОПРОВЕРГНУТ**
  (97 частей против 19 элементов) — `split` по нему НЕ режет фичи.
- **`Creo\SKILL_creo_bit_level_anatomy.md`** — «**KEYS OVER WINDOWS**»: искать КЛЮЧИ
  (`type\0`, `ref_id\0`, `sub_feat_id\0`), а не окна.
| `API\` | `SKILL_creojs_api.md` (Creo.JS/`pfc*`), `SKILL_creo_api_ecosystem.md` (каналы: OTK/JLINK/VB/Web.Link/CREOSON) |
| `DOCS\` | `SKILL_creo_docs_map.md` (где хелпы/PDF/API-руководства в `D:\PTC\CREO12`) |
| `CREOSON\` | `SKILL_creoson_workflow.md` (цикл, переключение папок), `SKILL_creoson_complete.md` (карта API), `SKILL_creoson_sessions_workdirs.md` (сессии/папки), `SKILL_creo_commands.md` (подбор команды), `SKILL_creoson_write_rules.md` (пишущие), `SKILL_creoson_rename_mechanism.md` (rename), `SKILL_creoson_probe_method.md` (пробы), `SKILL_creoson_inbox_deepseek.md` (долги темы) |
| `COPY\` | `SKILL_copy_assembly_project.md` (умная копия проекта), `SKILL_copy_rename.md` (методика копии/переименования) |
| `STANDARDS\` | `SKILL_creo_company.md`, `SKILL_company_config.md`, `SKILL_naming_spec.md`, `SKILL_drawings_eskd.md`, `SKILL_creo_templates.md`, `SKILL_creo_model_nature.md` (природа модели: деталь/сборка/производство), `SKILL_parameters_guide.md`, `SKILL_reference_limits.md`, `SKILL_creo_cards.md` |
| `RELATIONS\` | `SKILL_creo_relations.md`, `SKILL_relations_constitution.md`, `SKILL_relations_basics.md`, `SKILL_relations_examples.md`, `SKILL_curves_from_equation.md`, `SKILL_curves_examples.md`, `SKILL_spring_compression_generator.md`, `SKILL_spring_tension_master.md` |

## 🔴🔴 ДОГМЫ CREO (читать ПЕРВЫМИ — закон владельца)

| Догма | Файл | Суть |
|---|---|---|
| **CREO — ТОЧНАЯ ПРОГРАММА, НИЧЕГО НЕ ОКРУГЛЯЕТ** | `SKILL_GRABLI.md` **§165** (**critical**) | «Creo — точная программа, и ничего там не округляется» (владелец, 30.10.2026). **ЗАПРЕЩЕНО:** «обрезано/округлено до N знаков» · считать `27.1953` и `27.19` одним размером (**дельта 0.0053** ⇒ РАЗНЫЕ) · приводить к сетке (`1/64`·`0.390625`·`25/128`) · «разные ревизии → разные номиналы» без точного расчёта. **ЗАМЕР:** `f32(54.3906)` = **54.39059829711914** ≠ `54.390625` (разница **2.5e-05**) ⇒ округления нет. Читать значение **как есть**, сравнивать **точно** |
| **🔴 МАССА/ОБЪЁМ/ПЛОЩАДЬ ЧИТАЮТСЯ ИЗ ФАЙЛА — ПЛМ НЕ СЧИТАЕТ** | `SKILL_GRABLI.md` **§167** (**critical**) | «Creo также считает со своими параметрами и объёмы, и массу… **ПЛМ не считает, а только СЧИТЫВАЕТ. Все параметры масс уже известны. В ПЛМ читаем ИЗ ФАЙЛА!**» (владелец). **ЗАМЕР:** `@0xC0B9 e3 32 [28] 98 00 e2 97 25 29 9f` → lead=0x3F → **0.0234408764602364** = **точно J-Link** ✅. **ФОРМАТ:** `e3 32 [тип] [7 БАЙТ] f1` (7 байт = double без старшего; восстанавливать по плотности металла). Формат дома: `READ\SKILL_creo_read_mass_double.md` (проверен **6/6** + 486 моделей). **§166 ОТМЕНЁН в этой части** |
| **🏆 ЧЕРТЁЖ `.drw`: связь с моделью + вложенные копии** | `SKILL_GRABLI.md` **§168** | `.drw.1` = **11 853** (`.dxf` 131 · `.dwg` **53** — Creo не пишет). Шапка: `CMNM` (имя) · `REVS` · `MACH` · `UOBJ_ID` · `DBID`. **Связь:** `#Dwg_Models → model_names → "BESEDKA-000-SB.ASM"` (текст!). Карта TOC **читаема текстом**. **🔥 Вложенные копии:** `#AllFeatur` · `#BasFullData` · `#DwgData` идут **×3** (`IntPrt0` · `IntPrt18`). ⚠️ Своей массы в `.drw` **нет** — законно |
| **🏆 ИСТОРИЯ В ЧЕРТЕЖЕ `.drw` — ЧИТАЕТСЯ ПО КАНОНУ** | `SKILL_GRABLI.md` **§169** | `typed_data(MdlStored)` @0x833C: **`user_name`** (`"USER"`) · **`modif_time`** (`tm_sec·min·hour·mday·mon·year−1900` ⇒ **UTC**) · **`rev_string`** (`"37"`) · **`comment`** (UTF-8 «Наименование компьютера: 'frezer-4'») · **`Proe_version`** (`"Creo 9.0.1.0"`) · `uobj_id`/`rec_uobj_id`/`gcd_uid`. **Хронология:** `e1 f6 e1 <LOGIN> 00 e2 <6 байт UTC>` (десятки записей). **ДВА счётчика:** `rev_string` (человеческая) ≠ `revnum` (внутренний). **История ×3:** чертёж + `IntPrt0` + `IntPrt18` |
| **ВЫЧИСЛЯЕМОЕ (номинал) — искать по ИМЕНАМ ПОЛЕЙ** | `SKILL_GRABLI.md` **§163/§164** | `dim_array` в `#BasFullData`: `value`·`bck_value`·`nominal_value` = **КОД** `2f 4a 00`; схема читается (`dim_type`·`feat_id`·`tol_type`·`digits`) |
| **ИМЕНА ЗАДАЁТ ЧЕЛОВЕК — СВЯЗЬ ВНУТРИ ФАЙЛА** | `SKILL_GRABLI.md` **§95** (**critical**) | фильтр по виду имени запрещён; признак — только из структуры |
| **В СИСТЕМЕ УЧЁТА НЕ МОЖЕТ БЫТЬ ДВУХ ПРАВД** | `SKILL_GRABLI.md` **§85** (**critical**) | настройки/база/скан/связи — одни |
| **ШАРУ `Z:` АГЕНТ НЕ ТРОГАЕТ** | `SKILL_GRABLI.md` **§82** (**critical**) | ни в каком виде |

## 🔴🔴 НОГА 30.10.2026 (продолжение — приоритеты эстафеты закрыты) — ЗАКОН МЕТОДА + СВЯЗИ + ТИПЫ (ГЛАВНОЕ ЗА 4 ДНЯ)

| Тема | Где | Суть |
|---|---|---|
| **🔴 ЗАКОН МЕТОДА: читать ЛЮБОЙ файл ТОЛЬКО через `#UGC_TOC`** | `..\Creo\SKILL_GRABLI.md` **§147** | адрес любой секции — ИЗ КАРТЫ, а не перебором файла. Порядок: заголовок `#UGC:2 <ТИП> <ВЕРСИЯ>` → карта → `NEXT_TOC_ENTRY` → чтение по адресу |
| **🔴 КАРТ `#UGC_TOC` — ОТ 2 ДО 3 у каждого файла** | `SKILL_GRABLI.md` **§152** | парсить РАЗДЕЛЬНО; адрес `< размера файла`; **ДЕДУП по (имя, offset)** — иначе `SldRegenRevInfo` считается дважды |
| **🏆 КОДЫ ТИПОВ ЭЛЕМЕНТОВ: `feat_defs_<N> − 910 = pfcFEATTYPE`** | `SKILL_GRABLI.md` **§154/§156** | `911→HOLE` · `913→ROUND` · `916→CUT` · `923→DATUM_PLANE` · `927→DRAFT` · `1007→WORKCELL`. Типы = `911…1031`; `1232+` = **`id` записи**, НЕ тип (§157) |
| **СЛОВАРЬ: `pfcFeature.h` (живой)** | `D:\PTC\CREO13\...\otk\otk_cpp\include\pfcFeature.h` | 20 038 Б, enum `pfcFeatureType` = 314 имён (FEATTYPE = 280). **Три шкалы:** API 0…279 · файл 911…1031 (−910) · `TYPENUM` Creo 10…100 |
| **НАЙДЕНО: связи и статус В ФАЙЛЕ (C API не нужен)** | `SKILL_GRABLI.md` **§152** | `num_parents`/`parents_checksum` — в **`VisibGeom`** (литейка = **11 родителей**); `is_item_alive` = `01`; `ref_models_data` = ссылка (`e1`) |
| **ФОРМАТ ЧИСЕЛ: `F8 <len> <байты>` / `F4` / `F1`; `e1/e2/e3/f6` = ССЫЛКИ** | `SKILL_GRABLI.md` **§155** | значение читать **ПЕРЕД** `E0` (`<знач> E0 <тип> <ИМЯ> 00`); `f8 14` = массив 14 байт (хеш) |
| **ТИП ФАЙЛА — В ЗАГОЛОВКЕ `#UGC:2`, НЕ в расширении** | `SKILL_GRABLI.md` **§149** | `PART` · `PART/SKEL_MODEL` (скелетон) · `PART/BULK` («BLK») · `ASSEMBLY/ASSEM_MFG` · `MFG_TOOL_PATH` (`.tph`) · `INST_PART` (`.xpr`) · `DRAWING` |
| **`.tp` = `Pro/CLfile` — ЧИТАЕТСЯ ТЕКСТОМ** | `SKILL_GRABLI.md` **§149** | `MFGNO` · `OPERATION NAME` · `NC SEQUENCE NAME` · `TOOL_TYPE` · `CUTTER DIAMETER` · `SPINDL RPM` · `FEDRAT` · `GOTO/CIRCLE` |
| **ТИПЫ ЭЛЕМЕНТОВ МАНУФАКТУРИНГА (19 блоков)** | `SKILL_GRABLI.md` **§138–§144** | `DESCRIPTION` · `MACHINING_TIME` (читается!) · `SPINDLE_SPEED` · `CUTTER_DIAM` · `CUT_FEED` · `usage` · `TOOL_ID` |
| **`MACHINING_TIME` — ЧИТАЕТСЯ ИЗ ФАЙЛА** | `SKILL_GRABLI.md` **§141** | `struct.unpack('>f', байты[1:5])` → минуты (2.63…3.50); 8 байт начинаются с `F7 40` = заголовок, не double |
| **АРХИВ ФАЗ 7–14 (журнал)** | `READ\ARCHIVE\FASY_7_14_29.10.2026.md` | вынесено из `SKILL_creo_tree_jlink_etalon.md` для читаемости; итоги — сводкой в конце скилла |
| **`cadmpeg` для Creo бесполезен** | `SKILL_GRABLI.md` **§142** | Creo у него уровень `L1` (SolidWorks `L3`, Fusion `L5`); «cadmpeg» = «FFmpeg для CAD», НЕ картинки |
| **ИСТОЧНИКИ ГЕОМЕТРИИ** | **`READ\SKILL_creo_geometry_sources.md`** | `SolidPrimdata` = **тесселяция** (для показа, НЕ точные размеры); точная геометрия — `VisibGeom`/`NovisGeom` (прототипы) |
| **`srf_array` — МОСТ «элемент ↔ геометрия»** | `SKILL_GRABLI.md` **§159** | `VisibGeom.active_geom` (58) · `NovisGeom.inactive_geom` (115) · `ActDatums.act_datum_geoms` (12); поля `geom_id · geom_type · feat_id`. Схема объявлена ОДИН раз (`fb`=структура), записи — потоком (**не считать записи по числу полей**) |
| **🔴 МОСТ `feat_id` = `symbol_key` НАЙДЕН; ТЕКСТА ИМЕНИ В ФАЙЛЕ НЕТ** | `SKILL_GRABLI.md` **§160** | `srf_array.feat_id` (`00 63`) **=** `feat_defs_917.symbol_key` (`00 63`); `id` в `FeatDefs` = `fb e3` — **ссылка**; `table_id` ПУСТ; `#FeatDefsIndex` = список кодов (`f8 06`, слова по 2 байта). Имена (EXTRUDE/ROUND/«ВЫТЯГИВАНИЕ») = **0 вхождений** ⇒ **текст только J-Link** |
| **🔴 `parent_feats` = МАССИВ ID РОДИТЕЛЕЙ (литейка)** | `SKILL_GRABLI.md` **§161** | `f8 <N>` → **N СЛОВ по 2 байта** (не N байт!): `@0x28272 f8 03 → 0xA029·0x9EAA·0xA068` · `@0xADDC4 f8 02 → 0xA029·0x9F2F` · `@0x1DFA79 f8 01 → 0xA029`; `GeomOwn_feat_id_arr` → владелец `0xA029`; `owner_feat_revnum`=22. Диапазон = с `feat_id` ⇒ **шкала одна**. ⚠️ 11≠найденные 6 — нужен J-Link |
| **ГРАБЛЯ №12: СДВИГ НА 1 БАЙТ при чтении массива** | `SKILL_GRABLI.md` **§161** | данные начинаются с `m.start() + len(name) + 3` (имя+NUL+`f8`+`N`). Сдвиг дал `0x299E` вместо `0xA029` — **правдоподобная ложь**; проверять на смысл (диапазон `feat_id`) |
| **🏆 ЖИВОЙ CREO: ФОРМУЛА `−910` ПОДТВЕРЖДЕНА (8 совпадений) + ТЕКСТ ИМЁН** | `SKILL_GRABLI.md` **§162** | `#FEAT id=99 TYPENAME=ВЫСТУП SUB=Вытягивание TYPENUM=TYPE_7` = `feat_defs_917` ✅ · ОТВЕРСТИЕ TYPE_1=`911` · ВЫРЕЗ TYPE_6=`916` · ОПОРНАЯ ПЛОСКОСТЬ TYPE_13=`923` · УКЛОН TYPE_17=`927` · СКРУГЛЕНИЕ TYPE_3=`913`. **Запуск:** `tree_probe.bat` + Creo живой (`parametric.exe`, cwd `Z:\PTC\CREO-START\START-STD`). **ГРАБЛИ запуска №13–16** |
| **ПРИРОДА ТИПОВ ФАЙЛОВ (5 прогонов J-Link)** | `SKILL_GRABLI.md` **§162** | `PART`=дерево+размеры · `PART/SKEL_MODEL`=**только датумы/кривые, тел НЕТ** · `PART/BULK`=**FEAT=0, но параметры читаются** · `ASSEMBLY`=**КОМПОНЕНТ TYPE_89** + `ОБОЗНАЧЕНИЕ`/`ТИП`/`ФОРМАТ` |
| **⚠️ `ListParents()` J-Link = ПУСТО ( vs `num_parents`=11 в файле)** | `SKILL_GRABLI.md` **§162** | `parents=[]` у ВСЕХ моделей ⇒ поле `parent_feats` (§161) — **единственный рабочий источник родителей** |
| **🏆 НОМИНАЛЫ: В ФАЙЛЕ НЕТ, ЕСТЬ В J-Link + `arch_dims` (РАЗОБРАНО)** | `SKILL_GRABLI.md` **§163** | Записи `dN` в файле читаются (`dim_name`·`mod_type`·`feat_id`·`ft_type`), но **значение = ССЫЛКА**: `d45`=**8.0** и `d24`/`d34`=**16.0** имеют **ИДЕНТИЧНЫЕ байты** ⇒ не номинал. Отвергнуты замером: f32/f64/f16/текст/int/массив (0–противоречия). **ИСТИНА:** текущий номинал — **J-Link `#DIM val=52.0`**; архив — `arch_dims` (**11 855 моделей**, `{"d9":54.3906}`); **история** — `arch_dim_ch` (224 845 строк, `old_val`→`new_val`, kind='размер') |
| **🔥 РАЗНЫЕ РЕВИЗИИ = РАЗНЫЕ НОМИНАЛЫ** | `SKILL_GRABLI.md` **§163** | `CTKD_015_23_001`: `arch_dims`=**54.3906** (02.02.2023) vs J-Link=**52.0** (живой файл) ⇒ **история размеров РАБОТАЕТ**, показывать в ПЛМ |
| **ГРАБЛЯ №17: одинаковые байты у РАЗНЫХ значений = ССЫЛКА** | `SKILL_GRABLI.md` **§163** | правило дома «если одно число у всех — это ссылка» (GRABLI §136); проверено на 3 параметрах |
| **🏆 ОБЩАЯ КАРТА ФАЙЛА (48 секций) + `dim_array` РАЗОБРАНА** | `SKILL_GRABLI.md` **§164** | `#UGC:2 PART **1873**` · `#BasFullData 0x30906 → dim_array f8 44 (68)`; поля: `type`·`dim_type`(0x3E)·`feat_id`(0x63=99)·`value`·`nominal_value`·`tol_type`·`digits`·`bound`. **НОМИНАЛА НЕТ — структурно:** `value`=`bck_value`=`nominal_value` = `2f 4a 00` (ОДИНАКОВЫ у разных размеров) и `0x2F4A00` > размера файла ⇒ **КОД, не величина** |
| **ГРАБЛИ МЕТОДА №18–21 (номиналы)** | `SKILL_GRABLI.md` **§164** | ❌ искать «совпадения чисел» перебором вместо чтения **имён полей** · парсер брал байты ПЕРЕД именем (значение — **ПОСЛЕ** `e0 <len> "имя" 00`) · `f8 <N>` = **N 2-байтных слов** · смещение считать `len(name)+1` |
| **ВОССТАНОВЛЕНИЕ ДВОЙНОЙ КОДИРОВКИ** | `SKILL_GRABLI.md` **§158** | формула `chr(cp1251(байт))`, 5 шагов; **НЕ применять декод дважды** |

**⚠️ ГРАБЛИ НОГИ (не повторять):** `#FeatDefs` (раздел) ≠ `feat_defs_<N>` (запись); перебор баз — метод ложных
ответов (истина = совпадение со СМЫСЛОМ); `editor` с `old_text` = заголовок соседней секции ТЕРЯЕТ её
(лечение: `insert_line` + проверка `Select-String '^## '`).

## 🔴 Нога 29.10.2026 — плотность/масса и карточка материала (ЗАКРЫТО)

| Тема | Где | Суть |
|---|---|---|
| **Плотность/масса/объём из `.prt`** | `READ\SKILL_creo_read_mass_double.md` + код `TOOLS\ftype_probe\creo_full.py::mass_properties` | схема `E3 32` + 7 байт + перебор ведущего байта `0x30..0x4F`; плотность = `MASS/VOLUME` |
| **Правка кода 29.10.2026** | `creo_full.py` строки 79–84 | снята ЖЁСТКАЯ граница `6e-6…9.5e-6` («металл») → окно `1e-9…1e-2`; она отбрасывала верный ответ (чугун `10.3 г/см³` → `None`) |
| **Сверка** | J-Link `mass_probe.bat` | `din912` → файл `0.02894438244 кг / 3618.0478 мм³` = **8.0 г/см³**; J-Link `0,0289444 / 3618,05` — совпадение до 10 знаков |
| **Карточка материала В ДЕТАЛИ** | `READ\SKILL_creo_tree_jlink_etalon.md` | 30+ полей: `PTC_MASS_DENSITY`, `_YOUNG_MODULUS`, `_POISSON_RATIO`, `_HARDNESS`, `_CONDITION=STEEL`, `_MATERIAL_SOURCE`, `_MATERIAL_ID`, `PTC_UNITS_*` |
| **Наследование материала** | там же | каналы `PTC_MASTER_MATERIAL` / `_REPORTED_` / `_ASSIGNED_` ⇒ у потомка (`ctkd.prt`) карточки НЕТ — брать у родителя |
| **Имя материала** | там же | `\xe3\x33 <строка>` → `V-CH_50` (русский алиас `ВЧ-СБ-50` — отображение Creo) |
| **Грабли ноги** | `..\Creo\SKILL_GRABLI.md` §107–§112 | «мусор» запрещён (это `PRO_MP_*` = массовые свойства); вид не подписывать по интуиции (`A_1` = ОСЬ); искать готовый код в репо; «правдоподобное число» опаснее `None` |
| **ПОКРЫТИЕ ПАРСЕРА** | `READ\SKILL_creo_tree_jlink_etalon.md` | папка Электон: **324 файла → читаются 302 (93 %)**; **21 «нулевых» — ВСЕ с суффиксом `_z`/`-z`** = заготовки без дерева (парсер прав) |
| **КОДЫ `b` ПО ФАЙЛАМ + ПАРЫ** | там же | `3`=фичеры · `5`=плоскости · `21`=ОСИ · `25`=РАЗМЕР · `2`=компонент; **5 пар «фичер↔размер»: `id=N` фичер + `id=N+1` `b=25` — имя совпадает** |
| **`names_table` — ПОЛЕ ВНУТРИ `MdlStatus`** | там же | в TOC секции `names_table` **НЕТ**; есть `MdlStatus` ⇒ это поле схемы. **Мой парсер и `feat_records.py` читали одни байты** |
| **`feat_records.py` — под ДРУГУЮ версию Creo** | `TOOLS\ftype_probe\feat_records.py` | требует `featssrf`/`cutextrude` — в файлах Электона **0 вхождений** ⇒ **0 записей**. Адаптировать под маркер `\xf6` |
| **АРТЕФАКТ `\xe3` → ведущая `3`** | `READ\SKILL_creo_tree_jlink_etalon.md` | `'3M16x1.5'`=`M16x1.5` · `'3PRO_MP_CSYS'`=`PRO_MP_CSYS` · `'3GEOMETRY'`=`GEOMETRY` — потерянные имена `.prt` |
| **Грабли §113–§118** | `..\Creo\SKILL_GRABLI.md` | `editor` не сохраняет EOL · двойная кодировка · число-маркер ≠ повод менять фильтр · «секция» может быть полем · инструмент под другую версию Creo · `\xe3` в тексте = ложная `3` |
| `DAVYDOVKA\` | `SKILL_davydovka_creoson_map.md` (карта Давыдовка ↔ CREOSON) |
| `INFRA\` | `SKILL_creostart_fleet.md` (флот, старт машин), `SKILL_object_creoson_tests-01_asm.md` (объектные пробы) |
| корень | этот индекс + `cards\` (карты моделей, сырые близнецы) + `SKILL_creo_file_reading.md` (чтение файлов «в лоб»: история, упакованные числа, оглавление, параметры и отношения; §8.70–8.81 от 28–29.09.2026; инструмент `plm_reader` V24) + `CREO_MAP.md`, `SKILLS_MAP.md` |
| проверка хозяйства | **спека прогона — `D:\AI\СПЕКИ\СПЕКА_ПРОВЕРКИ_CREO.md`** (установка/настройки `CREO-START`, библиотеки `Libraries`, склад `Work`, тормоза, ошибки, предложения). Читается целиком до первого действия; живые файлы Creo не менять |
| **СТОРОННИЕ ПЛАГИНЫ** | **отдельная папка-направление `D:\AI\repo\B&W\`** (03.10.2026, Cline): набор B&W Plugins Suite — 15 модулей SMART\* от B&W Software GmbH, канал `protkdat` (как VERICUT), лицензия FlexNet:6501. Вход: `B&W\README.md`, конспект `B&W\STUDY_NOTES.md`, скилл-заготовка `B&W\SKILL_BW_PLUGINS.md`. **Ничего не установлено.** Под CREO13 есть только 3 модуля из 15: SMARTHolechart 19.4.1.0 (работает с `.hol` — прямо в тему конспекта «Таблица отверстий»), SmartMBDTools 13.0.5.0, SmartOptics 13.0.0.0 (⚠️ ломает mapkey). Ключевое: **52 проверки модели вендора** (SMARTUpdate) — готовый перечень «что контролировать» для нашего движка правил (`B&W\15_КАТАЛОГ_ПРОВЕРОК_SMARTUPDATE.md`); карта файлов распакованных тел — `B&W\14_КАРТА_ФАЙЛОВ_ПРАВИЛО.md`; что в агенте лучше — `B&W\16_ЧТО_В_АГЕНТЕ_ЛУЧШЕ.md`. Подробности про канал — `API\SKILL_creo_api_ecosystem.md` § «СТОРОННИЕ ПЛАГИНЫ» |

## КАК ИИ НАХОДИТ СКИЛЛ (правило поиска)
1. Вход — корневой `SKILL_index.md` (домен Creo) → **этот файл**.
2. Здесь — таблица подразделов; идти прямо в файл по пути `Creo\<подраздел>\SKILL_*.md`.
3. Ключевые слова для поиска — в поле `when` шапки каждого скилла.
4. В каждом подразделе есть свой `_INDEX.md` (если агент уже внутри папки).

## ИСТОЧНИКИ ДОКУМЕНТАЦИИ (только чтение)
Все хелпы/PDF/API-руководства — в установке `D:\PTC\CREO12` (полная карта и языки —
`SKILL_creo_docs_map.md`; разбор каналов — `SKILL_creo_api_ecosystem.md`).
Копии-дубли PTC в репо удалены словом пользователя 22.09 (в гит не возвращать); справка — в установке `D:\PTC\CREO12` (карта: `SKILL_creo_docs_map.md`).
Временная папка разбора `D:\AI\ИЗУЧИТЬ\CREO` разбирается и удаляется пользователем — на неё
в скиллах не опираться.