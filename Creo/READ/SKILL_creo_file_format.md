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

## 7. ★ ГДЕ ЛЕЖИТ ДЕРЕВО И ТИПЫ — СЕКЦИЯ `MdlStatus`

**Это главная поправка.** Операции и типы лежат в `MdlStatus`, а НЕ в `AllFeatur`.

| адрес | что |
|---|---|
| `cutextrude` | `0x78e76f` |
| `ВЫТЯГИВАНИЕ` | `0x78e5fb` |
| `ОПОРНАЯ ПЛОСКОСТЬ` | `0x78dda4` |

Все три внутри `MdlStatus @0x078b668`, 69 694 байта.

### Инвентаризация типов из `MdlStatus` (модель 137_011_0041)
| код | кол-во | что это |
|---|---|---|
| **`featssrf`** | **219** | **ПОВЕРХНОСТИ, порождённые операциями** |
| `dtmplane` | 144 | базовые и датумные плоскости |
| `cutextrude` | 144 | вытягивания |
| `featround` | 144 | скругления |
| `protrevolve` | 1 | вращение |

### ГЕОМЕТРИЯ ЧИТАЕМА
`featssrf` = feature surface — **самая частая сущность модели**, каждая грань
и цилиндр от вытягивания. Лежит в `MdlStatus` **с именами**, рядом с операцией,
которая её создала. Это не сырой бинарник и не шум.

Получается за один проход по секции: **сколько операций, сколько поверхностей
от каждой, как называются**. Инвентаризация модели без Creo.

## 8. ГЕОМЕТРИЯ — ГДЕ ЧТО
| секция | размер | что |
|---|---|---|
| `SolidPrimdata` | 1 398 927 | геометрия тела (в сборке — 125 б) |
| `VisibGeom` | 1 500 102 | видимая геометрия |
| `NovisGeom` | 2 798 956 | скрытая геометрия |
| `MdlStatus` | 69 694 | **названия поверхностей и типы** |

## 9. КАК ЧИТАТЬ СЕКЦИЮ — код `creo_sections.py`
```python
from creo_sections import read_toc, section
toc, size = read_toc(path)          # {имя: (смещение, длина)} — 30 секций
blob, _, _ = section(path, 'MdlStatus')
txt = blob.decode('utf-8', 'replace')
```
Смещение и длина берутся из `#UGC_TOC`. Никакого поиска по всему файлу.

## 11. ИЗВЛЕКАТЕЛЬ — `creo_full.py` (работает)

Один прогон по 661 модели из `search.pro` даёт:
```
операций                  1105
кириллических параметров  13443
имён фич                   460
компонентов (BOM)            7
```
Результат — `plm_final.jsonl`, по строке на модель:
```json
{"file","type","size","sections","type_counts",
 "operations":[{"name","type"}],
 "surfaces":[{"name","kind","id"}],
 "features":[...], "bom":[...], "cyrillic_params":[...],
 "mass_properties":null}
```

### Модель 137_011_0041 — полная картина
```
30 секций, 10 074 903 байта
ТИПЫ: group 151 · dtmplane 144 · cutextrude 144
      featround 144 · featssrf 219 · protrevolve 1
150 операций: ВРАЩЕНИЕ 1 protrevolve, ВЫТЯГИВАНИЕ 1 cutextrude,
             СКРУГЛЕНИЕ 1 featround, МАССИВ 1 cutextrude …
78 имён фич: TOP, FRONT, DTM1…DTM11
23 кириллических параметра: ГОСТ, Деталь, КОРПУС, Круг, Материал,
                           Наименование, Нач_отдела, Обозначение
```

### BOM — два пути
1. Секция `MdlRefInfo` — если там есть ссылки.
2. **Fallback:** текстовые ссылки по файлу до начала `SolidPrimdata`.
   Сработал на `kalaud-401-02.asm` → `KALAUD-401-01.PRT`,
   `KALAUD-401-01_Z.PRT`.

### ⚠️ Известный дефект: имя поверхности смещено
Тип и ID верны (`Split_surface`, `35186`), но имя берётся не с того поля:
```
выдаёт:   LOCAL_GROUP_1 , USER
правильно: Split Surface 1
```
В записи `featssrf` имя операции стоит **перед** ссылкой на поверхность.
Чинить: брать последнее поле перед `featssrf`, а не первое совпадение.

## 12. СКВОЗНАЯ ПРИЁМКА
| модель | результат |
|---|---|
| `137_011_0041.prt` | 150 операций с типами, 78 фич, 23 параметра |
| `kalaud-401-02.asm` | BOM = 2 компонента |
| `most-75.asm` | BOM = 5 деталей (`MOST-75-001.PRT`, `-002-SB.ASM`, …) |

## 13. ЧЕГО В ФАЙЛЕ НЕТ
`PRO_MP_MASS` / `VOLUME` / `AREA` — 19 вхождений, 2 разных хвоста.
Значение **пересчитывается**, IEEE-754 не хранится. `null` окончательно.