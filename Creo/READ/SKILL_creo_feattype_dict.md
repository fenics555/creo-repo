# SKILL: СЛОВАРЬ ТИПОВ ЭЛЕМЕНТОВ `pfcFEATTYPE` — ИМЯ ЧИТАЕТСЯ ИЗ ФАЙЛА

> **Дата:** 30.10.2026 · **Источник:** `D:\PTC\CREO13\Creo 13.4.1.0\Common Files\otk\otk_cpp\include\pfcFeature.h`
> **Открытие:** §171 в `SKILL_GRABLI.md`. **Снимает вопрос «текст имени не читается» (§160).**

## 🔴 ГЛАВНОЕ
`SKILL_GRABLI.md` §160 говорил: «текст имени элемента в файле ОТСУТСТВУЕТ (0 вхождений `EXTRUDE`/`ROUND`/`ВЫТЯГИВАНИЕ`)».
**Это верно только для РУССКОГО текста.** **АНГЛИЙСКОЕ имя типа — ЧИТАЕТСЯ** через словарь:

```
feat_defs_<N>  −  910  =  индекс в enum pfcFeatureType  →  ИМЯ ТИПА
```

## 📖 ИСТОЧНИК СЛОВАРЯ (установочный Creo 13)
```
D:\PTC\CREO13\Creo 13.4.1.0\Common Files\otk\otk_cpp\include\pfcFeature.h
    enum pfcFeatureType { pfcFEATTYPE_FIRST, pfcFEATTYPE_HOLE, ... pfcFeatureType_nil };
    ВСЕГО ЗНАЧЕНИЙ: 314   (индексы 0…313)
```
**API-методы (оттуда же):**
| Метод | Возврат | Смысл |
|---|---|---|
| `GetFeatType()` | `pfcFeatureType` | **числовой тип** (= `feat_defs_<N>` − 910) |
| **`GetFeatTypeName()`** | `xstring` | **★ ТЕКСТ ИМЕНИ ТИПА** |
| `GetFeatSubType()` | `xstring` | подтип |
| `GetNumber()` | `xint` | внутренний номер |
| `GetStatus()` | `pfcFeatureStatus` | **ACTIVE / SUPPRESSED / UNREGENERATED** (§172 — health!) |

## ✅ ПОДТВЕРЖДЕНО ЗАМЕРОМ J-Link (7/7)
| `feat_defs_<N>` | −910 | `pfcFeatureType` | J-Link `TYPENAME=` | ✔ |
|---|---|---|---|---|
| `feat_defs_911` | **1** | `pfcFEATTYPE_HOLE` | ОТВЕРСТИЕ | ✅ |
| `feat_defs_913` | **3** | `pfcFEATTYPE_ROUND` | СКРУГЛЕНИЕ (Общий) | ✅ |
| `feat_defs_916` | **6** | `pfcFEATTYPE_CUT` | ВЫРЕЗ (Вращать) | ✅ |
| `feat_defs_917` | **7** | `pfcFEATTYPE_PROTRUSION` | ВЫСТУП (Вытягивание) | ✅ |
| `feat_defs_923` | **13** | `pfcFEATTYPE_DATUM_PLANE` | ОПОРНАЯ ПЛОСКОСТЬ | ✅ |
| `feat_defs_926` | **16** | `pfcFEATTYPE_DATUM_AXIS` | ОПОРНАЯ ОСЬ | ✅ |
| `feat_defs_927` | **17** | `pfcFEATTYPE_DRAFT` | УКЛОН (Общий уклон) | ✅ |

## 📋 ПОЛНЫЙ СЛОВАРЬ (0…313) — ключевые
```
 0 FIRST          1 HOLE           2 SHAFT          3 ROUND          4 CHAMFER
 5 SLOT           6 CUT            7 PROTRUSION     8 NECK           9 FLANGE
10 RIB           11 EAR           12 DOME          13 DATUM_PLANE   14 LOC_PUSH
15 UDF           16 DATUM_AXIS    17 DRAFT         18 SHELL         19 DOME2
20 CORNER_CHAMFER 21 DATUM_POINT  22 IMPORT        23 COSMETIC      24 ETCH
25 MERGE         26 MOLD          27 SAW           28 TURN          29 MILL
30 DRILL         31 OFFSET        32 DATUM_SURFACE 33 REPLACE_SURFACE 34 GROOVE
35 PIPE          36 DATUM_QUILT   37 ASSEMBLY_CUT  38 UDFTHREAD     39 CURVE
40 SURFACE_MODEL 41 WALL          42 BEND          43 UNBEND        44 SHEETMETAL_CUT
45 FORM          46 THICKEN       47 BEND_BACK     48 UDFNOTCH      49 UDFPUNCH
50 INTERNAL_UDF  51 SPLIT_SURFACE 52 GRAPH         53 SMMFGPUNCH    54 SMMFGCUT
55 FLATTEN       56 SET           57 VDA           58 SMMFGFORM     59 SHEETMETAL_PUNCH_POINT
60 LIP           61 MANUAL_MILL   62 MFGGATHER     63 MFGTRIM       64 MFGUSE_VOLUME
65 CABLE_LOCATION 66 CABLE_SEGMENT 67 CABLE         68 COORD_SYS     69 CHANNEL
70 AREA_NIBBLE   71 PATCH         72 PLY           73 CORE          74 EXTRACT
75 MFGREFINE     76 SILHOUETTE_TRIM 77 SPLIT       78 EXTEND        79 SOLIDIFY
80 INTERSECT     81 ATTACH        82 CROSS_SECTION 83 UDFZONE       84 UDFCLAMP
85 DRILL_GROUP   86 ISEGMENT      87 CABLE_COSMETIC 88 SPOOL ...
```
**Полный список (314) — извлечён скриптом из `pfcFeature.h` (см. `plm_feattype.py`).**

## 🔴 РУССКИЕ ИМЕНА — ОТДЕЛЬНО (не в файле!)
```
Русский текст типов в ТЕКСТОВЫХ ресурсах НЕ найден (143 файла text\russian\ — 0 совпадений).
Хранится в скомпилированном: Common Files\text\compiled_resource\pro_menu_russian_resources.dll (2.9 МБ).
```
**⇒ ПРАВИЛО:** из файла — **АНГЛИЙСКОЕ имя** (`PROTRUSION`); русское (`ВЫСТУП`) — **перевод в UI Creo**.
Для базы ПЛМ брать **английское** (стабильно, не зависит от языка).

## 🎯 ЧТО ЭТО ДАЁТ ПЛМ
| Было (§160) | Стало (§171) |
|---|---|
| «имя элемента — только J-Link» | **имя типа читается из файла** (EN) |
| `TYPENUM` «не хранится» | `TYPENUM = feat_defs_<N> − 910` |

## 🏗️ ДЕРЕВО ПОСТРОЕНИЯ — ГДЕ ЛЕЖИТ (замер 30.10.2026)

### Схема записи элемента (найдена в файле)
```
#AllFeatur → "Sld_Features" → first_feat_ptr → ЗАПИСЬ ЭЛЕМЕНТА:
   "id"                   ← ID элемента (1 байт, напр. 0x63 = 99)
   "indep_attributes_arr" ← атрибуты (f8 04 → 4 байта)
   "feat_type_ptr" → "table_id" + "type" + "feattype_key"   ← ТИП
   "form" · "attributes" · "placement" · "intersection"
   "internal_udf_type" · "param_choice_ptr" · "blend_choice" · "depth_choice"
```
**Запись элемента есть в файле.** Список = цепочка по `first_feat_ptr`.

### ⚠️ ЧТО ИЗВЕСТНО ТОЧНО, А ЧТО НЕТ
| Факт | Статус |
|---|---|
| `feat_defs_<N>` = **объявления типов** (по 1 на тип; в замере 6 шт на 20 элементов) | ✅ доказано |
| у объявления есть **`id`** (`feat_defs_917` → `id`=**99** ✅ = J-Link) и **`symbol_key`** | ✅ доказано |
| **тип** элемента = `N − 910` → имя (7/7) | ✅ доказано |
| **список ВСЕХ элементов** с их `id` и порядком | ❌ **НЕ найден** (открыто) |
| `FeatDefsIndex` = `feat_defs_index f8 06` + **6 слов** (`0x1B83`=7043…) | ⚠️ похоже на **индекс типов**, не элементов |

### 🎯 ЧТО ОСТАЛОСЬ ДЛЯ ДЕРЕВА (задача следующей ноги)
1. Пройти цепочку **`first_feat_ptr`** внутри `#AllFeatur` (найти сам указатель и записи).
2. Сверить с J-Link `#FEAT id=…` — в замере было **19–25 элементов** на файл.
3. Собрать **порядок** (дерево) → в базу для отслеживания **+/−** элементов.

## 🏥 СТАТУС ЭЛЕМЕНТА → `health` БЕЗ CREO (задача B)
API даёт **`GetStatus()` → `pfcFeatureStatus`**:
```
pfcFEAT_ACTIVE · pfcFEAT_INACTIVE · pfcFEAT_SUPPRESSED
pfcFEAT_FAMILY_TABLE_SUPPRESSED · pfcFEAT_SIMP_REP_SUPPRESSED
pfcFEAT_PROGRAM_SUPPRESSED · pfcFEAT_UNREGENERATED
```
**Из файла** (по §157): `is_item_alive` · `num_parents` · `parents_checksum` — статус читается **без Creo**.
⇒ таблица `health` заполняется **файловым парсером** (Creo не нужен).
