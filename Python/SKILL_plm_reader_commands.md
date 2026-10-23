---
name: plm-reader-commands
system: Команды
description: Use when: работа с PLM Reader (D:\AI\tools\agent\plm_reader): запуск, самопроверка, выпуск версии, CLI движка, грабли импорта
when: plm_reader, smoke, самопроверка, make_version_json, version.json, выпуск версии, APP_VERSION, манифест, engine.py, count, check, tree, changes, rename-plan, load_settings_file, circular import, folders, settings.json
date: 23.10.2026
priority: high
---

# PLM READER: ПОЛЕЗНЫЕ PYTHON-КОМАНДЫ

Полная рутина — README инструмента (`D:\AI\tools\agent\plm_reader\README.md`); здесь — быстрый вызов.

```powershell
cd D:\AI\tools\agent\plm_reader
python _smoke_v87.py                      # самопроверка без GUI-участия (граф + 5 секций GenealogyWindow)
python make_version_json.py "<notes>"     # пересобрать манифест (номер берётся из APP_VERSION в plm_reader.py)
python plm_reader.py                      # запуск окна (или plm_reader_gui.bat)
```

ВЫПУСК ВЕРСИИ — 3 обязательных шага (иначе шара обновление не увидит):
1. поднять `APP_VERSION` в `plm_reader.py`;
2. `python make_version_json.py "<кратко что нового>"`;
3. git push вместе с `version.json` (git — по `SKILL_parallel_legs.md`: только адресный `git add -- <пути>`).

ПРИЁМКА: `python _smoke_v87.py` → последняя строка `SMOKE OK`.
ГРАБЛИ: smoke устойчив к cp1251; GUI-часть проверяется программно (без дисплея) — визуал смотрит
человек. **Шара `Z:` агентами НЕ трогается** (закон владельца 14.10.2026) — `Powershell\SKILL_plm_reader_sync.md`.

---

## CLI ПРОГРАММЫ (проверено живым прогоном 23.10.2026)

Два модуля со своими аргументами:

```powershell
cd D:\AI\tools\agent\plm_reader

# движок: чтение базы / проверки (код 0 на всех, кроме tree с -n)
python engine.py count                     # 5610 моделей · связей 24820 · деталей 44609 · 0.5 с
python engine.py check                     # лежачих 23052 · правленых 41877 · 4 счёта
python engine.py where <имя>               # где лежит модель
python engine.py changes --n 5             # история изменений
python engine.py tree --depth 1            # дерево (⚠ -n НЕ принимает, см. грабли)
python engine.py rename-plan --n 3         # сухой план переименования
python engine.py count --full              # полный пересчёт

python plm_reader.py --help                # без окна: --folder --csv --max-mb --no-recurse --history --history-csv
```

## ГРАБЛИ CLI И ИМПОРТА (найдены аудитом 23.10.2026)

1. **`tree` не принимает `-n`.** `python engine.py tree --depth 1 -n 5` →
   `error: unrecognized arguments: -n` (код 2), хотя `--n` объявлен и у `changes` работает.
   **Обход:** для `tree` брать `--depth` и `-n` не передавать.
2. **Кириллица в выводе CLI при редиректе — мусор** (`?????? ?????: ????? 5610`).
   Это НЕ порча данных: запись/чтение UTF-8 верны; ломается только печать при перенаправлении.
   **Обход:** читать вывод как UTF-8 (`reconfigure`) или проверять числа, а не слова.
3. **Циклический импорт `plm_settings` ↔ `plm_reader`.** Внешний скрипт, импортирующий
   `plm_settings` **первым**, падает: `ImportError: cannot import name 'CURRENT_SETTINGS_VERSION'
   from partially initialized module 'plm_settings' (circular import)`.
   **Обход:** сначала `import plm_reader` (он регистрирует себя в `sys.modules`), затем `plm_settings`.
4. **`load_settings_file()` ПИШЕТ, а не только читает.** Функция переносит/архивирует старые файлы
   настроек (и правит живой `settings.json`). **Никогда не звать её из пробы по живому каталогу** —
   только на копии в изоляции. Живой факт 23.10.2026: проба перезаписала рабочие папки скана
   тестовыми значениями. Подробно — `repo\SKILL_edit_gotchas.md` §18.
5. **`folders`/`exclude` не приводятся к списку.** Если в файле настроек они строкой
   (`"Z:\A; Z:\B"`), программа примет строку как есть (в отличие от `db_mirror`, который чинится
   миграцией v2→v3). Проверять тип после правки файла вручную.

## ЧИСЛА БАЗЫ (на 23.10.2026, активная `plm_reader_20261002_160609.db`)

```
snapshots 46756 | links 24877 | derived 21187 | changes 122968 | folders 5590
mtime заполнен у 46756 (100%); created у 45653 (97.6%); seen — 18 меток скана
последняя правка файла на складе: 02.10.2026 16:05
правленых: месяц 931 · 3 мес 3167 · полгода 5542 · год 11432 · все 46756
новых (created): месяц 854 · 3 мес 1769 · полгода 3282 · год 45653
```
⚠️ «день» и «неделя» = **0**: склад не обновлялся 21 день. Это факт о складе, не дефект.

---

## ПОЛНЫЙ ГРАФ СВЯЗЕЙ — ТОЧНЫЕ ФОРМУЛЫ (найдено 23.10.2026, читать ДО любой правки графа)

**Источник:** `D:\AI\tools\agent\creo_reverse_engineering\src\creo_links_new.py` (13 699 б, правка 23.10.2026 06:31)
+ эталон `EXAMPLES_CONNECTIONS.md` (Gold Standard, 2 живых примера) + `test_case_170meta_links.md`.

### ШЕСТЬ типов связей графа (не четыре!)

| Тип связи | Формула поиска (живой код) | Что находит |
|---|---|---|
| `mfg_fixture_for` | `re.match(r'^\d+X\d+-\w+$', s)` | **ОСНАСТКА** (`10X1-D12`) — ⚠️ НЕ по `PSB`! |
| `mfg_tool_for` | `re.match(r'^T\d{3,4}$', s)` или `SVERLO\|FREZA\|GRAVER` | инструмент (`T0010`, `T0021`) |
| `mfg_operation_of` | `CHERN\|CHIST\|SV\|FR\|FASKA\|RASTOCHKA\|CENTROVKA\|DISKOVAYA\|STEP` | операции ЧПУ |
| `mfg_machine_for` | `re.match(r'^(MACH\|CNC\|MACHINE)\w*$', u)` | станок |
| `bom_component` | состав: имена `.PRT/.ASM` из `SolidPersistTable`/`Comp_Data` **минус BLACKLIST** | детали сборки |
| `inherit_from_master` | токены `BASE_PART` / `GENERIC` в `LargeText` | заготовка → мастер-модель |

### 🔴 BLACKLIST — обязателен, иначе в состав лезет мусор (стр. 53–57)

```python
blacklist = {"trf_arr","plcm_revnum","next_prop","merge_info_ptr","pre_roll_back",
 "post_roll_back","post_regen","parchild_table","copy_info_ptr","embed_info_ptr",
 "copy_info","embed_info","trf_arr_ptr","plcm_revnum_ptr"}
```
Это **внутренние поля Creo**, не компоненты. **Без фильтра связи врут.**

### Эндианизм (стр. 60) — одна точка правды
```python
endian = '>' if b"MACH SUN_SunOS" in raw[:1024] else '<'
```
Big-Endian = сборки ЧПУ с SunOS. Иначе `struct.error` при чтении подач/усадок.

### Параметры (стр. 205–226) — маркер + окно 128 байт
```python
b'PTC_SHRINKAGE_FACTOR' → усадка   (принимать 0.9 < val < 1.1)
b'PTC_MASS'/'PTC_VOLUME'/'PTC_DENSITY' → масса/объём/плотность (1e-6 < |val| < 1e6)
```

### Формат выхода (обязательный, `EXAMPLES_CONNECTIONS.md`)
```json
{"source":"filename_source","target":"filename_target","type":"edge_type_string",
 "metadata":{"parameter_name":1.012,"method":"binary_unpack"}}
```

### ЭТАЛОННЫЕ ПРИМЕРЫ — сверять результат по ним
```
1) ...\000_51 DF Держатели форм\23-171GR1-META 2кап черновой BDF 5 1_2''\23-171gr1-meta.asm.1
   --[bom_component]--> DF-23-171 (PART)
2) ...\171meta держатель форм\23-171gr1-meta.asm.1
   --[inherit_from_master]--> 171-otlivka.prt.1 (PART_Z / BLANK)
```

### Приёмка графа (чек-лист тест-кейса)
```
✅ SUCCESS = найдены ВСЕ типы связей (bom / inherit / tool / operation / fixture)
❌ FAIL(0 edges)        → проверить эндианизм и TOC
❌ FAIL(тип неверен)    → сигнатуры в заголовке #UGC:2, НЕ секции (SolidPersistTable есть и в .prt!)
❌ FAIL(инструмент без операции) → паттерны в LargeText
```

### 🔴 Живой замер 23.10.2026 (серии 170meta + 171meta, только чтение)
```
папок: 170meta 206 файлов + 171meta 109 файлов
уникальных моделей: 105 | с .asm: 51 | со структурой: 47
связей-кандидатов (состав без blacklist): 218
типы заголовков: ASSEMBLY/ASSEM_MFG (24) · ASSEMBLY (8) · ASSEMBLY/CAST (2 — отливки!)
```
**`ASSEMBLY/CAST`** — третий тип заголовка = отливка (в скиллах не описан).

## ДВА КЛАССА ПРОИЗВОДСТВА: ЛИТЬЁ vs МЕХООБРАБОТКА (живой замер 23.10.2026)

**Правило:** прежде чем строить цепочку — определи КЛАСС. Признаки разные, и один набор
формул не покрывает оба.

| Признак в файлах | **ЛИТЬЁ** (170meta/171meta, `000_5 401-LIT-MO`) | **МЕХООБРАБОТКА** (ЦТКД Электон, `001_15 ЦТКД`) |
|---|---|---|
| `MERGE_BASE_PART` (наследование) | ✅ есть | ❌ **0 файлов** |
| `PTC_SHRINKAGE_FACTOR` (усадка) | ✅ есть | ❌ **0 файлов** |
| Мастер-модели (`*-MASTER`) | ✅ есть | ❌ **0** |
| Отливки (`*-OTLIVKA`) | ✅ есть | ❌ **0** |
| **Приспособления** | по общему префиксу имени | ✅ **отдельная папка `CTKD-PSB-*`, 175 файлов** |
| Обработок ЧПУ (`ASSEM_MFG`) | 24 из 34 | **99 из 113** |
| Инструмент/приспособление в составе | `INLBS_MFG_NC`/`T00xx` | ✅ `INLBS_MFG_NC` — 11 из 60 |

**Вывод:** для **литья** — цепочка `деталь → отливка → мастер-модель → знаки/ящики → обработка`
(скилл `SKILL_creo_file_reading.md` §8.6). Для **мехобработки ЦТКД** — цепочка
`деталь → обработка ЧПУ → ПРИСПОСОБЛЕНИЕ → инструмент` (формула `компонент id`).

### Живой замер ЦТКД (`Z:\PTC\Work\001_15 ЦТКД Электон`, только чтение)
```
файлов: 648 | папок: 89
типы: .prt 208 | .asm 113 | .drw 81 | .tph 22 | .mfg 1
папки-эталоны: «CTKD-PSB Приспособления» (CTKD-PSB-01/02/03/04/pinol),
               «CTKD-KALIBR Калибры», «ЦТКД 437.001 Корпус», «ЦТКД 738.01.001-01 Фланец»
заголовки: ASSEMBLY/ASSEM_MFG 99 | ASSEMBLY 14
маркеры (скан 60 файлов): ASSEM_MFG 17 | INLBS_MFG_NC (приспособление) 11 | SBORKA_MFG 11
                          MERGE_BASE_PART 0 | HAAS (станок) 0 | PTC_SHRINKAGE_FACTOR 0
```

### Состав папки приспособления (эталон комплектности)
```
CTKD-PSB-01\ctkd-psb-01-01.prt.1            приспособление — ДЕТАЛЬ
CTKD-PSB-01\ctkd-psb-01-01.asm.1            приспособление — СБОРКА
CTKD-PSB-01\ctkd-psb-01-01.drw.1            ЧЕРТЁЖ приспособления
CTKD-PSB-01\ctkd-psb-01-01-01-z.prt.1       ЗАГОТОВКА приспособления (_z)
CTKD-PSB-01\ctkd-psb-01-01_old-mfg-psb.prt.1 ОБРАБОТКА приспособления
CTKD-PSB-01\CTKD-PSB-01-01.pdf|.stk|.dsn    PDF / STEP / design
```
**Правило комплектности:** деталь + сборка + чертёж + заготовка(`_z`) + обработка(`-mfg-`)
**лежат в одной папке** и различаются **суффиксом имени**, а не папкой.

### Цепочка литья — признаки (скилл §8.6, проверено)
```
Отливка      : MERGE_BASE_PART = ДЕТАЛЬ (наследование + техприпуски)
Мастер-модель: база для знаков/ящиков (усадка, линия разъёма, уклоны, радиусы)
Знаки/ящики/плиты/формы: наследуют от мастер-модели и друг друга
Приспособление в ASSEM_MFG: INLBS_MFG_NC.ASM
Станок в ASSEM_MFG:         HAAS_3X.ASM
Инструмент:                 T0001…T0015 (поля TOOL, tool_table, tool_id)
```
**Живая проверка (скилл §8.63):** `171META-1-02-ЯЩИК-НИЗ-SB` → оснастка `-КАМЕРА/-ЛИТНИК/-ПЛИТА`;
`1013-AZ-1` (MFG) → состав `23-1013GRI-1`, оснастка `1013-AZ-2`.
**Реализующие функции (в движке):** `engine.role_of(model)`, `engine.mfg_models(model)`,
`engine.role_bases(model)`; `_hash_like()` отсекает внутренние hex-коды.

### ⚠️ Ограничение (честно, из скилла)
У части литых деталей в файле **только внутренний код** — **имя отливки не восстановить**
(в дереве ставится пометка). Оснастка «по имени» работает через **общий префикс имени**.

### Правило владельца по данным
**CL-траектории (`.tph`) в ПЛМ не собираем** — берём **только операции / переходы / инструмент**.

```
ASSEMBLY/ASSEM_MFG → обработка ЧПУ (BOM изделия НЕТ, 220 из 245)
ASSEMBLY           → обычная сборка (BOM есть)
ASSEMBLY/CAST      → отливка
PART               → деталь (в т.ч. .prt с секциями SolidPersistTable — НЕ признак сборки!)
DRAWING            → чертёж
```


### Заполненность базы
```
links   24 877 | уникальных parent 15 897 | уникальных child 8 187  (из 46 756 моделей)
derived 21 187
changes 122 968
```
**Следствие:** «нет связей» у узла — **частая норма**, а не всегда дефект. Начинать с SQL, не с отрисовки.

### ТРИ ПРИЗРАКА «нет связей» (проверять по порядку)
1. **Связь ведёт в ШАБЛОН** → `SBORKA_MM` / `SBORKA_MFG` / `MM_PART` / `MFG_NC` вырезаны фильтром
   `plm_graph.py:545` → оба конца обрезаны → узел одинок.
   *Живой пример:* `170META-1-02-ЯЩИК-НИЗ-ЛИТНИК` имеет **ровно 1 связь** — с `SBORKA_MFG` (qty=31).
2. **Связь не собрана движком.** У `..._Z` (заготовка) `links=0`, `derived=0` — движок **не читает
   `inherit_from_master`** (мастер-модель).
3. **Обрезка лимитами:** `total > 120` / `slice(0,25)` в обходе графа.

### Словарь связей, которых ДВИЖОК НЕ СОБИРАЕТ (эталон — тест-кейс 170meta)
Источник: `tools\agent\creo_reverse_engineering\test_case_170meta_links.md` (готовый чек-лист «провал/успех»).

| Тип связи | Как искать | Признак в файле |
|---|---|---|
| `bom_component` | состав сборки | секция `SolidPersistTable` / схема `d N (имя.PRT)` — **работает только в `.asm`** |
| `inherit_from_master` | заготовка → мастер-модель | маркер **`Base_Part`** или суффикс **`_z`** |
| `mfg_tool_for` | инструмент | `T0010`, `T0005`, `FR50`, `T0001` |
| `mfg_operation_of` | операция | `CHIST`, `CENTR`, `SV10`, `OP020`, `GRAVIROVKA`, `POLUCHIST-` |
| `mfg_fixture_for` | оснастка | `10X1-D12`, `CENTROVKA.PRT`, `DISKOVAYA.PRT`, `ЦТКД_...-PSB-02.PRT` |

### Классификация роли файла (для оснастки/заготовки) — по `STRATEGY_PLM.md` §2.3/§2.4а
```
ASSEM_MFG            → CAM-процесс (обработка). Состава изделия НЕТ (220 из 245 сборок — ЧПУ)
ASSEMBLY             → обычная сборка (состав = bom_component)
Base_Part / _z       → заготовка (связь с мастер-моделью)
_otl                 → отливка
SolidPersistTable    → ⚠️ НЕ признак сборки: встречается и в .prt (ловушка)
```
**Ловушка:** `SolidPersistTable`/`NeuAsmSld` есть и в `.prt`, и в `.asm` — тип определять **по заголовку**.

### ⚠️ «Правда» из чужого HANDOVER требует проверки
`creo_reverse_engineering\HANDOVER_CURRENT.md:12` говорит «RESOLVED: THE WALL», но речь про **мок-генератор**
(`forcing the mock generator`) — это **синтетика**, не живые файлы. Оркестратор — «CONCEPTUALLY ready,
pending integration». **Брать оттуда словари и правила, не код «как работает».**
