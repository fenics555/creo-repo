---
name: creo_tree_jlink_etalon
system: Creo
description: ЭТАЛОН дерева построения, элементов и размеров из ЖИВОГО Creo через J-Link (TreeProbe) — с чем сверять разбор байтов. Когда: правка дерева/размеров/типов фич, сверка байтов с Creo.
when: дерево построения, эталон, J-Link, TreeProbe, tree_probe.bat, feat_id, dimid, dN, размеры элемента, сверка с Creo, XToolkitNotFound, XUnknownModelExtension
priority: high
date: 28.10.2026
executor: Cline
---

# ЭТАЛОН ДЕРЕВА ПОСТРОЕНИЯ ЧЕРЕЗ J-LINK (TreeProbe)

**Зачем:** разбор байтов («что на что меняется», типы фич, размеры `dN`) проверяется ТОЛЬКО
сверкой с живым Creo. Creo — законодатель, файл — копия.

## Запуск (проверено 28.10.2026, Creo 13.4.1.0)

```powershell
cd D:\AI\tools\agent\creo_export
tree_probe.bat "путь\модель.prt.1"        # Creo поднимется сам, если не запущен
mass_probe.bat "путь\модель.prt.1"        # масса/объём/площадь (эталон чисел)
```

**Файлы:** `TreeProbe.java` + `tree_probe.bat` (ASCII-текст, без кириллицы!)

## Формат вывода (машиночитаемый)

```
#MODEL <имя файла>
#FEAT-COUNT <N>                       число элементов дерева
#DIM-COUNT <M>                        число размеров модели
#FEAT <индекс> <feat_id> TYPE_<код> <имя>
#DIM feat=<feat_id> sym=dN name=dN dimid=<id размера> val=<значение>
#PARAM <имя> <значение>
#ERR ...
```

## Живые замеры (эталоны для сверки)

**`g22033.prt.1`** (шпилька, 1 043 437 Б): `#FEAT-COUNT 9` · `#DIM-COUNT 8`
```
#FEAT 0 105 TYPE_0  null      #DIM feat=105 sym=d7  dimid=7  val=8.0
#FEAT 1 472 TYPE_13 DTM5      #DIM feat=105 sym=d10 dimid=10 val=30.0
#FEAT 2 139 TYPE_13 no_name   #DIM feat=105 sym=d14 dimid=14 val=22.0
#FEAT 3 138 TYPE_7  null      ...  (d8=8.0, d13=0.625, d15=6.75, d27=6.75, d28=8.0)
#PARAM DRW_NAME Шпилька | MASS 0.014921140138664956 | DENSITY 7.8E-6
```
**`ctkd_015_23_001.prt.1`** (деталь ЦТКД, 306 378 Б): `#FEAT-COUNT 19` · `#DIM-COUNT 40`
```
#FEAT 0 1 TYPE_13 RIGHT   #FEAT 3 7 TYPE_68 PRT_CSYS_DEF
#FEAT 1 3 TYPE_13 TOP     #FEAT 6 135 TYPE_1  (...тела)
#FEAT 2 5 TYPE_13 FRONT   #FEAT 18 895 TYPE_16  A_10
```

## 🔴 ГРАБЛИ (обе пойманы живьём)

1. **`XToolkitNotFound`** — Creo не запущен. Поднять: `parametric.bat -g:no_graphics -i:rpc_input`
   (D:\PTC\CREO13\Creo 13.4.1.0\Parametric\bin), ждать процесс `xtop`, ~40 с.
2. **`XUnknownModelExtension`** — Creo не принимает имя с версией. Передавать `x.prt`,
   а не `x.prt.1` (номер версии отрезается в `TreeProbe.java`).
3. **`null` в имени / `no_name`** — норма: у элементов имя появляется только у именованных.
4. **`FeatureType` печатался как `com.ptc.pfc.pfcFeature.FeatureType@…`** — у enum нет `toString`;
   номер берётся через reflective `getValue()`/поле `__Value` → в выводе `TYPE_<номер>`.
5. **Импорт `pfcDimension.Dimension`** — классы лежат в `com/ptc/pfc/pfcDimension/`,
   а не в `pfcModelItem`; сверять по `all.txt` в каталоге инструмента, а не по памяти.
6. **У `Feature` НЕТ `ModelItemOwner`** (`ClassCastException`) — список элементов берётся у
   МОДЕЛИ: `ListItems(ModelItemType.ITEM_FEATURE)`; константы — `ITEM_*`, не `MODEL_ITEM_*`.
7. **Кириллица в `.bat` без BOM ломает парсер** — сообщения в bat писать ASCII.

## Связь с разбором БАЙТОВ (что даёт эталон)

- `dimid` из эталона = **id колонки таблицы семейства** в байтах (замер: колонки `14`, `103`
  ↔ `dimid=14`): этим и читается «что меняется в исполнении».
- `feat_id` из эталона ищется в файле как **2-байтовое LE-число** (1-байтовые — шум геометрии).
- Порядок `#FEAT 0..N` — **хронология создания**: её и искать в файле цепочкой id.
- `sym=dN` — **имя размера Creo** (`d10`), `val` — номинал; в байтах текстом `d10` НЕТ.

=== END ===
