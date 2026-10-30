# SKILL: ТЕЛА И МАТЕРИАЛЫ ДЕТАЛИ — ПОЛНАЯ МОДЕЛЬ (открытие 30.10.2026)

> **§177 в `SKILL_GRABLI.md`** · подтверждено **байтами** + **скриншотами владельца** (Creo 13)
> **Слова владельца (ключевые):** «материалов в деталь можно **накидать сколько хочешь**,
> а **"задать как мастер" на всю деталь — только ОДИН**, а вот **на каждое тело можно свой
> материал назначать**!»

## 🔑 МОДЕЛЬ ДАННЫХ (подтверждена структурой файла)

```
ДЕТАЛЬ (.prt)
│
├─ body_array  f8 <N>                  ← N ТЕЛ (solid)
│   └─ тело[i]:
│       body_id · type · attrs · roll_back_attrs · cr_type
│       feat_id · consumed_by_feat_id · first_geom_ptr · outline
│       creator · users · order_num
│       └─ **gen_mass_prop_data** → mass_prop_data → mass_prop
│            volume · density · surfarea · cg · inertia    ← ★ СВОИ НА КАЖДОЕ ТЕЛО!
│
├─ material_arr  f8 <N>                ← N МАТЕРИАЛОВ (можно накидать СКОЛЬКО УГОДНО)
│   └─ материал[i]:
│       name (напр. `PTC_SYSTEM_MTRL_PROPS`) · id · type
│       └─ temp_prop_arr → property_arr:
│            **MASS_DENSITY** · YOUNG_MODULUS · POISSON_RATIO · SHEAR_MODULUS
│            THERMAL_EXPANSION_COEFFICIENT · THERMAL_CONDUCTIVITY · SPECIFIC_HEAT
│
└─ MASTER (мастер-материал)            ← ★ ОДИН на всю деталь («задать как мастер»)
     PTC_ASSIGNED_MATERIAL → PTC_MASTER_MATERIAL → (единицы `65G_MMKGS`)
```

## ✅ СООТВЕТСТВИЕ СЛОВ ВЛАДЕЛЬЦА И БАЙТОВ
| Слова владельца | Подтверждение в файле |
|---|---|
| «материалов можно накидать сколько хочешь» | **`material_arr f8 <N>`** — массив из N материалов |
| «"задать как мастер" — только один» | **`MASTER`** + `PTC_ASSIGNED_MATERIAL → PTC_MASTER_MATERIAL` |
| «на каждое тело — свой материал» | **`body_array f8 <N>`** + **`gen_mass_prop_data` у КАЖДОГО тела** |

## 📐 ФОРМАТ ЗАПИСЕЙ (замер `ctkd-kalibr-25x1x9g.prt.1`, 1 120 050 Б)

### Тело (пример — 2 тела в файле)
```
body_array  f8 02                       ← 2 ТЕЛА
  тело[0]: body_id f5 96 92 · type 62 · attrs f8 05 · cr_type · feat_id
           … topol_ref_data · creator · users · order_num 01
           gen_mass_prop_data @0x18BC4  →  mass_prop_data @0x18BC8
              volume 00 2D <7 байт> → lead 0x40 → 71302.31634915 мм³
              density 00 23 <7 байт> → lead 0x3E → 7.85e-06 кг/мм³  (СТАЛЬ)
              surfarea 00 2D <7 байт> → lead 0x40 → 13515.77373148 мм²
  тело[1]: gen_mass_prop_data @0x38FCB → mass_prop_data @0x38FCF
           (свои volume · density · surfarea)
```

### Материал
```
material_arr  f8 02                     ← 2 МАТЕРИАЛА
  материал[0]: name = "PTC_SYSTEM_MTRL_PROPS" · id 01 · type 00
      property_arr: INITIAL_BEND_Y_FACTOR · BEND_TABLE · **MASS_DENSITY** ·
                    YOUNG_MODULUS · POISSON_RATIO · SHEAR_MODULUS ·
                    THERMAL_EXPANSION_COEFFICIENT · THERMAL_CONDUCTIVITY · SPECIFIC_HEAT
```

### Мастер-материал
```
@0x1A137  "MASTER"                        ← мастер (один)
@0x1D203  PTC_MASTER_MATERIAL → "65G_MMKGS"    (ЕДИНИЦЫ!)
@0x1F915  PTC_ASSIGNED_MATERIAL → "PTC_MASTER_MATERIAL"   (ссылка)
```

## 📌 ЧТО ЭТО МЕНЯЕТ В СХЕМЕ БАЗЫ ПЛМ

**Было (неверно):**
```
snapshots: volume · material   — ОДНО на модель
```

**Стало (правильно) — нужны ДВЕ таблицы:**
```
bodies     (path, model, body_id, order_num, feat_id, volume, density, surfarea,
            cg_x, cg_y, cg_z, mass)                 ← ★ СВОЙ НА КАЖДОЕ ТЕЛО
materials  (path, model, name, mat_id, mat_type, mass_density,
            young_modulus, poisson_ratio, ...)      ← ★ ВСЕ материалы детали
master_mat (path, model, master_material)           ← ОДИН на деталь
```

**⇒ Из детали с 2 телами получается: 2 строки в `bodies` + 2 в `materials` + 1 в `master_mat`.**

## 🔴 МАТЕРИАЛЫ: КАРТОЧКИ + МАСТЕР (замер 30.10.2026, `MdlStatus`)

**Владелец (гипотеза, проверена):** «по логике **материалы лежат отдельно со своим ID**,
а каждое тело **ссылается на его ID** — вряд ли каждое тело хранит полные карточки».

### ✅ ЧТО НАШЛОСЬ (подтверждает гипотезу)
```
@0xA995F (секция `MdlStatus`):
   materials  f8 01              ← ★ МАССИВ МАТЕРИАЛОВ (N штук!)
      name        = "65G_MMKGS"  ← ИМЯ
      description = "65G"        ← ОПИСАНИЕ (65Г!)
      properties  f8 11          ← ★ 17 СВОЙСТВ (плотность, модуль Юнга, …)
           type · value · unit · …
@0xA9AD2:
   **current_material**  f4 04  "65G_MMKGS"   ← ★ МАСТЕР (текущий материал)
```

### 🔴 ЧЕГО В ФАЙЛЕ НЕТ (проверено: 0 вхождений)
```
❌ mat_id · material_id · body_material · body_mat_id
❌ material_ptr · mat_ptr · solid_material · region_material
```
**⇒ ССЫЛКИ «тело → материал» в НЕСЖАТЫХ секциях НЕТ.**
Вероятно: хранится в **СЖАТОЙ** секции (`SolidPersistTable`/`SolidPrimdata`) или
**восстанавливается Creo** при регенерации.

### 📐 МОДЕЛЬ (для ПЛМ)
```
ДЕТАЛЬ:
   materials[]        — ВСЕ материалы (карточки: name · description · properties[17])
   current_material   — МАСТЕР (один, глобально)
   тела (body_array)  — у каждого свои mass_prop (volume·density·mass)
   ⚠️ привязка «тело → материал» — НЕ читается из файла (пока)
```

## 🔴 ЧЕГО НЕ ДЕЛАТЬ
| ❌ | ✅ |
|---|---|
| Складывать массу детали = масса одного тела | **Сумма по телам** (у каждого своя!) |
| Брать первый материал как «материал детали» | **Мастер** (`MASTER`) + **все** в `materials` |
| Считать `PTC_SYSTEM_MTRL_PROPS` материалом | **Фильтровать** (внутренний, Creo 7.0+) |
| Считать `PTC_MASTER_MATERIAL` именем материала | Это **ЕДИНИЦЫ** (`65G_MMKGS`) |
