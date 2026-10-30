# SKILL: СБОРКИ (`.asm`) И МАНУФАКТУРИНГ (`.mfg`) — КАРТА И ДАННЫЕ

> **§179 в `SKILL_GRABLI.md`** · замер 30.10.2026
> **Счёт склада:** `.asm` = **10 438** · `.mfg` = **412**

## 🔴 ГЛАВНОЕ: `S2D000N` — ЭТО ВИДЫ ЧЕРТЕЖА (а не «мусор»!)

**В PART-файле (и в других) есть `S2D0001`…`S2D0007` — это ЧЕРТЁЖНЫЕ ВИДЫ:**
```
@0xB6108: "Траектория 1"  e3 S2D0007  f8 06 … color …
@0xB650B: "Сечение 1"     e3 S2D0007  f8 0c …
```
| Код | Что |
|---|---|
| **`S2D000N`** | **вид чертежа** (траектория, сечение, проекция) |
| Русские имена рядом | `Траектория 1` · `Сечение 1` · … |

**⇒ В детали есть СЕКЦИИ и ВИДЫ** — ценные данные (раньше я их «отсеивал как мусор»).

## 🗺️ КАРТА МАНУФАКТУРИНГА (`1_10.mfg.1`, 7 444 Б)

```
#UGC:2 MFG_ASSEM/ASSEM_MFG            ← ТИП ФАЙЛА

#UGC_TOC (4 секции — проще, чем у детали):
   Model_L01      335   5da   ← модель (имя, тип)
   Manufacturing  90f   4e7   ← обработка (СЖАТА)
   IndentTag      df6   859   ← ★ ЗДЕСЬ ТЕКСТ (инструменты!)
   FeatRefData    164f  74    ← ссылки на элементы
```

## 🔧 ДАННЫЕ МАНУФАКТУРИНГА (секция `IndentTag`)

```
#Manufacturing
   Mfg_Assem          ← СБОРКА ОБРАБОТКИ
   assem_ptr
   **tool_array**     ← ★ МАССИВ ИНСТРУМЕНТОВ
   **tool_id**        ← ★ `T0010` — НОМЕР ИНСТРУМЕНТА
   **tool_params**    ← ★ ПАРАМЕТРЫ (подача · обороты · …)
   data_type
   un_value(i_val)
```

## 📐 ФОРМАТ MFG: `@`-ПОЛЯ (PDM-зависимости)

```
@P_object 1 0
@depend 2 0
@model_name 3 10      3 3 1_10              ← ИМЯ МОДЕЛИ
@model_type 4 1       3 4 1                 ← ТИП
@revnum 5 1           3 5 26256             ← РЕВИЗИЯ
@bom_count 6 1        3 6 1
@dep_type 7 1         3 7 64
@stamp 8 0
@major_vers 9 0
@vers 10 1
@alias_name 11 10
@minor_vers 12 0
@reason 14 10
@dep_db 15 0
```
**⇒ Формат: `@ПОЛЕ <id> <len>` + `<тип> <id> <ЗНАЧЕНИЕ>`** (PDM-зависимости Creo).

## 🔴 ЧТО ЧИТАТЬ ИЗ `.asm` / `.mfg`
| Файл | Что искать |
|---|---|
| **`.asm` (сборка)** | `FeatDefsCmp` (компоненты) · `asm_components` · состав · `@model_name` |
| **`.mfg` (обработка)** | **`tool_array` · `tool_id` · `tool_params`** · `Mfg_Assem` · `@`-зависимости |
| **оба** | `Model_L01` (имя/тип) · `IndentTag` (текст) · `FeatRefData` |

## ⚠️ ОСОБЕННОСТЬ: СЕКЦИИ СЖАТЫ
```
Model_L01       — СЖАТА (данные модели)
Manufacturing   — СЖАТА
IndentTag       — ✅ ТЕКСТ (здесь поля и значения!)
FeatRefData     — ✅ ТЕКСТ
```
**⇒ Текст искать в `IndentTag`/`FeatRefData`, а не в `Model_L01`/`Manufacturing`.**

## 🗺️ КАРТА СБОРКИ (`ctkd-kalibr-25x1x9g.asm.1`, 622 834 Б) — 31 СЕКЦИЯ

```
#UGC:2 ASSEMBLY/ASSEM_MFG          ← ТИП: СБОРКА

Model_L05_PX         ab6    764     модель
SimpRepArray_L05     121c   175     ★ УПРОЩЁННЫЕ ПРЕДСТАВЛЕНИЯ
UnitSystemDef_L03    1393   295     единицы
StylesArray_L01      162a   153     ★ СТИЛИ ОТОБРАЖЕНИЯ
PDMTrail_L03         177f   7ec     PDM
SolidPersistTable    1f6d   4f8     ТЕЛА
SolidPrimdata        2467   4a38    ★ КОМПОНЕНТЫ (17 КБ)
FeatDefsIndex        6ea1   51
BasBasData           6ef4   40f
BasicData            7305   1e1d
BasicText            9124   7d5
Geomlists            98fb   240
GeomDepen            9b3d   1b4
DispCntrl            9cf3   4a0
LargeText            a195   30aa    текст (12 КБ)
Notes                d241   72e
FamilyInf            d971   2d
VisibGeom            d9a0   130     (в сборке — мало!)
NovisGeom            dad2   25a
ActEntity            dd2e   70e6
**AllFeatur          14e16  10040** ★ ДЕРЕВО (64 КБ)
BasFullData          24e58  58f     размеры
**FullMData          253e9  1a763** ★★ МАТЕРИАЛЫ (104 КБ!)
NeuPrtSld            3fb4e  29
**NeuAsmSld          3fb79  286d**  ★ НАСТРОЙКИ СБОРКИ
MdlStatus            423e8  a5de    статус
**PipeInfos          4c9c8  63**    ★ ТРУБОПРОВОДЫ
**Xsections          4ca2d  1107**  ★ СЕЧЕНИЯ
**FeatDefs           4db36  30c7a** ★★ ОПРЕДЕЛЕНИЯ ЭЛЕМЕНТОВ (194 КБ!)
DwgData              7e7b2  16b     чертёж
```

### 🔴 СЕКЦИИ, КОТОРЫХ НЕТ У ДЕТАЛИ (только у СБОРКИ!)
| Секция | Что |
|---|---|
| **`SimpRepArray_L05`** | **упрощённые представления** (Simp Rep) |
| **`StylesArray_L01`** | **стили отображения** |
| **`PipeInfos`** | **трубопроводы** |
| **`Xsections`** | **сечения** |
| **`NeuAsmSld`** | **настройки сборки** |
| **`FeatDefs`** (194 КБ) | **определения элементов** |

**⇒ У сборки 31 секция (у детали — 24). Разница = компоненты + трубопроводы + сечения.**

## 🔧 `tool_params` РАЗОБРАН (долг закрыт 30.10.2026)

**Замер (`1_10.mfg.1`, секция `IndentTag` @0xDF6):**
```
Manufacturing
   Mfg_Assem
      assem_ptr = "1_10"          ← сборка обработки
   tool_array  f8 04              ← ★ 4 ИНСТРУМЕНТА
      инструмент[0]:
         type        = 0x0A
         tool_id     = "T0010"    ← ★ НОМЕР ИНСТРУМЕНТА
         tool_params f8 11        ← ★ 17 ПАРАМЕТРОВ
            data_type · type · un_value(i_val) · bk_un_value(i_val) · attr ·
            un_value(d_val) · …
```

### 📐 ФОРМАТ (для парсера)
```
tool_array\x00 f8 <N> f7 .. fb e3
   e0\x01type\x00 <тип>
   e0\ntool_id\x00 <T0010>\x00          ← ИМЯ ИНСТРУМЕНТА (T + 4 цифры)
   e0\x00tool_params\x00 f8 <K> f7 .. fb e3   ← K параметров
        e0\x01data_type · e0\x01type · e0\x01un_value(i_val) · …
```

### 🎯 ЧТО ЭТО ДАЁТ ПЛМ
| Данные | Значение |
|---|---|
| **Инструменты** | `T0010`, `T0020`, … (номера!) |
| **Параметры** | 17 на инструмент (подача, обороты, глубина — по `data_type`) |
| **Сборка обработки** | `assem_ptr` (имя сборки) |

## 📌 ПРАВИЛА
1. **`.mfg` = мануфактуринг** — читать `tool_array` (инструменты: `T0010` + параметры).
2. **`.asm` = сборка** — состав в `SolidPrimdata` + `FeatDefs` + `AllFeatur`.
3. **`S2D000N` — виды чертежа** (НЕ мусор!).
4. **Сначала карта** (`#UGC_TOC`), потом секции.
5. **`.asm`/`.mfg` — тоже читать по карте** (своя структура секций!).
