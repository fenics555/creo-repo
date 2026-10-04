---
name: skill_creo_file_format
system: Creo
description: ПОЛНЫЙ АНАТОМИЧЕСКИЙ СКЕЛЕТ файла .prt/.asm — оглавление #UGC_TOC с именами 28+ секций, смещениями и длинами; формат записи typed_data(<КЛАСС>) с полями и длинами; история ревизий в тексте
when: анатомия файла, оглавление, TOC, секции, SolidPrimdata, AllFeatur, FeatDefs, MdlRefInfo, LargeText, typed_data, как читать файл целиком
date: 04.10.2026
executor: Cline
task: полное чтение файлов Creo «в лоб» — снятие карты секций
---

# АНАТОМИЯ ФАЙЛА CREO — ПОЛНАЯ КАРТА

## 1. Файл читается как текст. Инструмент: `read_files` / `Get-Content` / `Select-String`.

## 2. ШАПКА (строки 1–12)
```
#UGC:2 ASSEMBLY 2149 1860 804 1 1 15 4100 2023294 000002d0 \
#- VERS 0 0      #- HOST      #- LINK      #- DBID
#- REVS 0,       #- RELL 0,
#- UOBJ_ID 1730096014 80988631 1486079135
#- MACH _Windows
#- CMNM 00bmost-75.asm
#-END_OF_UGC_HEADER
#Creo  TM  10.0  (c) 2024 by PTC Inc. All Rights Reserved. 10.0.2.0
```
`#UGC:2 ASSEMBLY|PART` — тип. `_Windows` — ОС создания.

## 3. ОГЛАВЛЕНИЕ `#UGC_TOC` (строка 13) — КАРТА ФАЙЛА
Формат: `ИмяСекции  смещение  длина  размер  блок  тип  хеш1 хеш2`

| секция | смещение | длина | что внутри |
|---|---|---|---|
| `SolidPersistTable` | `0x2027` | `0x459` | таблица тел |
| **`SolidPrimdata`** | `0x2482` | `0x125` | **ГЕОМЕТРИЯ** (в сборке — 125 б, вся в деталях) |
| **`FeatDefsIndex`** | `0x25a9` | `0x43` | **индекс типов фич** |
| `BasBasData` | `0x25ee` | `0x362` | `tab_key`, `revnum_ptr`, `part_type` |
| `BasicData` | `0x2952` | `0x9769` | основные данные |
| `BasicText` | `0xc0bd` | `0x74c` | текстовые блоки |
| `Geomlists` | `0xc80b` | `0x240` | списки геометрии |
| `GeomDepen` | `0xca4d` | `0x1b1` | зависимости геометрии |
| `DispCntrl` | `0xcc00` | `0x160` | управление отображением |
| **`LargeText`** | `0xcd62` | `0x3345` | **уравнения `/*if`**, примечания |
| `Notes` | `0x100a9` | `0x2fd` | примечания |
| `FamilyInf` | `0x103a8` | `0x2d` | семейство |
| `VisibGeom` / `NovisGeom` | `0x103d7` / `0x10509` | | видимая / скрытая геометрия |
| `ActEntity` | `0x10753` | `0x56a` | сущности |
| **`AllFeatur`** | `0x10cbf` | `0x2e8d` | **ВСЕ ФИЧИ МОДЕЛИ** |
| `BasFullData` | `0x13b4e` | `0x509` | |
| `FullMData` | `0x14059` | `0x3707` | |
| `NeuPrtSld` | `0x17762` | `0x29` | нейтральное тело детали |
| `NeuAsmSld` | `0x1778d` | `0x78d` | нейтральное тело сборки |
| `MdlStatus` | `0x17f1c` | `0x665a` | статус модели |
| `PipeInfos` | `0x1e578` | `0x63` | трубопроводы |
| `Xsections` | `0x1e5dd` | `0x99b` | сечения |
| **`FeatDefs`** | `0x1ef7a` | `0x68e` | **ОПРЕДЕЛЕНИЯ ТИПОВ ФИЧ** |
| `DwgData` | `0x1f60a` | `0x185` | данные чертежа |
| **`MdlRefInfo`** | `0x1f791` | `0x153e` | **ССЫЛКИ НА ДЕТАЛИ (BOM)** |

В детали `SolidPrimdata` = **1 398 671 байт** (всё тело), в сборке — 125 б.

## 4. ФОРМАТ ЗАПИСИ — типизированный
```
typed_data(<КЛАСС>)          имя класса
   <длина> <имя поля>\0      объявление
   <длина> <значение>\0      значение
   typed_data(<вложенный>)   вложенная запись
```
Классы: `MTTyped_CreateData`, `MTTyped_ModifyData`, `TypedRedefineData`,
`Sld_FeatDefsIndex`, `Sld_BasBasData`, `Sld_BasicData`.

## 5. ФИЧИ — `created_features`
```
typed_data(MTTyped_CreateData)
   created_features
      feat_id / ft_type / comp_type / prev_feat_id
   feat_name    ВРАЩЕНИЕ 1
      pat_group_header_id / is_header
   icon_name    protrevolve
   ВЫСТУП id 103              ← связь: тип + номер
```
**Типы:** `group`, `dtmplane`, `csys`, `cutextrude`, `featround`, `protrevolve`.
Имя операции — кириллицей верхним регистром: `ВЫТЯГИВАНИЕ`, `СКРУГЛЕНИЕ`,
`ВРАЩЕНИЕ`, `МАССИВ`, `ВЫСТУП`.

## 6. ИСТОРИЯ РЕВИЗИЙ — тоже текст (`TypedRedefineData`)
```
typed_data(TypedRedefineData)  modifications  mod_type
   typed_data(MTTyped_ModifyData)  diff_dim_arr
      dim_id / dim_type / diff_detail
         diff_vals: old_val  ;2   new_val  ;2   dim_name  d22
      feat_id / ft_type / feat_name  ВЫТЯГИВАНИЕ 1
```
В `#- REVS`-блоке суффикс строки = код операции истории:
`-` удалить, `--` запретить, `!` изменить, `/` переместить, `.` пересчитать,
`: ` ограничить, `"` зависимость.

## 7. ЧЕГО В ФАЙЛЕ НЕТ
`PRO_MP_MASS` / `VOLUME` / `AREA` — 19 вхождений, 2 разных хвоста.
Значение **пересчитывается**, IEEE-754 не хранится. `null` окончательно.