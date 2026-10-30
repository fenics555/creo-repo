# SKILL: ВНУТРЕННИЕ ПАРАМЕТРЫ `PRO_MP_*` + ОКНО «ПОСТРЕГЕНЕРАЦИИ»

> **Дата:** 30.10.2026 · **§174 в `SKILL_GRABLI.md`** · замер `ctkd_015_23_001.prt.1`
> **Владелец:** «есть внутренние параметры типа объём/масса/инерция… их можно и отдельно собирать!»
> и «уравнения нужно собирать ВСЕ — и в основном окне уравнений, и в окне **«пострегенерации»**».

## 🔥 42 ВНУТРЕННИХ ПАРАМЕТРА `PRO_MP_*` (полный список из файла)

```
МАССА/ОБЪЁМ/ПЛОЩАДЬ:  PRO_MP_MASS · PRO_MP_VOLUME · PRO_MP_AREA · PRO_MP_DENSITY · PRO_MP_SOURCE
ЦЕНТР МАСС:           PRO_MP_COGX · PRO_MP_COGY · PRO_MP_COGZ · PRO_MP_CSYS
ИНЕРЦИЯ (от начала):  PRO_MP_INERTIA_ORIGIN
МОМЕНТЫ ИНЕРЦИИ:      PRO_MP_IXX · PRO_MP_IXY · PRO_MP_IXZ · PRO_MP_IYY · PRO_MP_IYZ · PRO_MP_IZZ
МАТРИЦА ПЕРЕНОСА:     PRO_MP_TRF_11 … PRO_MP_TRF_43   (4×3 = 12 значений)
АЛЬТЕРНАТИВНЫЕ:       PRO_MP_ALT_MASS · ALT_VOLUME · ALT_AREA · ALT_COGX/Y/Z · ALT_CSYS
                      ALT_INERTIA_ORIGIN · ALT_IXX/IXY/IXZ/IYY/IYZ/IZZ
```
**⇒ Все 42 — ЧИТАЮТСЯ ИЗ ФАЙЛА.** Масса/объём/площадь — формат `e3 32 [тип] [7 байт]` (§167).

## 🔥 ОКНО «ПОСТРЕГЕНЕРАЦИИ» НАЙДЕНО — `chg_param_arr`

```
@0x36740  chg_param_arr  f8 15 …
            feat_id · feat_type · name("PRO_MP_MASS")
            sym_props_arr → props_attr
            old_state(p_val) → new_state(p_val)      ← ★ ЧТО ИЗМЕНИЛОСЬ
          далее: PRO_MP_VOLUME · PRO_MP_AREA (тот же шаблон)
```
**⇒ «ЧТО ИЗМЕНИЛОСЬ ПОСЛЕ РЕГЕНЕРАЦИИ» ЧИТАЕТСЯ ИЗ ФАЙЛА:**
- **что** — `name` (`PRO_MP_MASS` / `PRO_MP_VOLUME` / `PRO_MP_AREA` …)
- **было** → `old_state(p_val)`
- **стало** → `new_state(p_val)`
- **у какого элемента** — `feat_id` · `feat_type`

**Живой пример** (`@0x36E15`): `"ИВАНИЕ 1"` … `ADMIN` … `PRO_MP_MASS` → `old`/`new` (числа 7 байт).

## ⚠️ ВАЖНО: слов `relation`/`equation` в файле — **0**
```
замер: relation=0 · Relation=0 · equation=0 · Equation=0 · param_rel=0 · rel_model=0
```
⇒ **Уравнения в файле названы ИНАЧЕ.** Искать по: `chg_param_arr` (пострегенерация) ·
`param_restr_entry` · значения `PRO_MP_*` · `value(i_val)` / `value(d_val)`.

## 📌 ЧТО ЭТО МЕНЯЕТ В ПЛМ
| Было | Стало |
|---|---|
| `PRO_MP_MASS` — «мусор» (§107) | **отдельная таблица `mass_props`** |
| «уравнения не собираем» | **`equations`**: обычные + **пострегенерация** |
| «что изменилось — неизвестно» | **`old_state`→`new_state`** из `chg_param_arr` |
| «только `ОБОЗНАЧЕНИЕ = rel_model_name`» | **все уравнения**, правила — в настройках |

## 🏛️ КУДА ЭТО ЛОЖИТСЯ (архитектура, см. `STRATEGY_PLM.md` §0.0)
```
SCANNER (engine.py) → mass_props (42 PRO_MP_*) · equations (оба вида) · dimensions · features
```
**ПРАВИЛО:** жёсткие списки (`_PARAM_DES`/`_PARAM_NAME`/`_PARAM_MAT`) — **в настройки**, не в код
(«у каждого человека свои параметры, названы по-своему» — владелец).
