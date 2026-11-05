---
name: material-parameters
system: Creo
description: Материалы Creo: форматы .mtl/.mat/.dmt, полный словарь параметров (76 ключей .mtl, 20 ключей .mat), проверка полноты заполнения, канон PTC. Проверено живым замером 05.11.2026 по Z:\PTC\CREO-START\НАСТРОЙКИ\МАТЕРИАЛЫ\Материалы общего вида.
when: материал, материалы, PTC_MATERIAL, PTC_YOUNG_MODULUS, MASS_DENSITY, .mtl, .mat, .dmt, pro_material_dir, библиотека материалов, HARDNESS, SPECIFIC_HEAT, THERMAL_CONDUCTIVITY, ГОСТ материал, плотность материала, параметры материала
priority: high
date: 05.11.2026
executor: Cline
---

# МАТЕРИАЛЫ Creo: ФОРМАТЫ, СЛОВАРЬ, ПОЛНОТА (живой замер 05.11.2026)

> **Корень точки монтирования** — `Z:\PTC\CREO-START\НАСТРОЙКИ\МАТЕРИАЛЫ\`
> (это значение `pro_material_dir`, живой `START-STD\config.pro` стр.108).
> Предмет замера — `МАТЕРИАЛЫ\Материалы общего вида`: **628 файлов**
> (`.mtl` 411 · `.mat` 208 · `.dmt` 8 · `.txt` 1), папок 1-го уровня 23, всего 76.
> ⚠️ `Z:\PTC` — **ТОЛЬКО ЧТЕНИЕ** (`Creo\SKILL_creo_index.md` § «ЗОНЫ РАБОТЫ С ФАЙЛАМИ»).

## 1. 🔴 ГЛАВНОЕ: ТРИ ФОРМАТА — ДВА СЛОВАРЯ

| Формат | Сколько | Что это | Словарь | Вердикт |
|---|---|---|---|---|
| **`.mtl`** | **411** | **рабочий** материал (`ND_RelParSet_K01`) | **`PTC_*`** — 76 ключей | ✅ основной |
| **`.mat`** | **208** | старый материал (`MATERIAL <имя>`) | **без `PTC_`** — 20 ключей | ⚠️ устаревший слой |
| **`.dmt`** | 8 | **НЕ материал** — палитра/цвет PGL | `material_name`, `ambient_color` | цвет, не свойство |

**Эталон PTC — живая цитата** (`...\Creo 12.4.2.0\Common Files\otk_java_free\otk_java_appls\jlink_elev\st304.mat`):
```
          MATERIAL  ST304
YOUNG_MODULUS = 28E6 · POISSON_RATIO = 0.29 · SHEAR_MODULUS = 11.5 · MASS_DENSITY = 501.1
THERMAL_EXPANSION_COEFFICIENT = 9.9E-6 · THERM_EXPANSION_REF_TEMPERATURE = 60
STRUCTURAL_DAMPING_COEFFICIENT = 0.33 · STRESS_LIMIT_FOR_TENSION = 60E3
STRESS_LIMIT_FOR_COMPRESSION = 60E3 · STRESS_LIMIT_FOR_SHEAR = 25E3
THERMAL_CONDUCTIVITY = 9.4 · EMISSIVITY = 0.3 · SPECIFIC_HEAT = 0.12 · HARDNESS = 120
CONDITION = N/A · INITIAL_BEND_Y_FACTOR = 0.4 · BEND_TABLE = tableSt304
```
**⇒ Правка прежней версии скилла:** правило «каноничный = без `PTC_`, `PTC_` = домашний префикс»
для `.mtl` — **НЕВЕРНО**. Правильно: **два словаря по формату файла**:
`.mat` → без `PTC_` (и у PTC так же); `.mtl` → с `PTC_*` (живой рабочий, 411 файлов).
Эталон PTC `.mtl` — `Common Files\applications\emx\components\inch\material\generic_steel.mtl`:
`PTC_MATERIAL_DESCRIPTION · TEMPERATURE · PTC_INITIAL_BEND_Y_FACTOR · PTC_BEND_TABLE ·
PTC_MATERIAL_TYPE = 9 (Locked) · PTC_FAILURE_CRITERION_TYPE = 'NONE' · PTC_FATIGUE_TYPE = 'NONE' ·
PTC_MATERIAL_SUB_TYPE = 'LINEAR' · PTC_MASS_DENSITY (lbm/in^3) · PTC_CONDITION`.
## 3а. 🔴🔴 ГЛАВНОЕ ОТКРЫТИЕ (05.11.2026): Creo ЧИТАЕТ `.mtl` ТОЛЬКО В UTF-8 **С BOM**

**Живой факт со скриншота владельца:** в папке `Чугун` 11 файлов `.mtl`, но в Creo
(окно «Материалы в библиотеке») подхватились лишь **3**: `chugun_sch21-40`, `chugun_sch21`, `chugun_sch18-36`.

**Причина — BOM, и только он.** Замер по всем 411 файлам:

| Файл | Первые 3 байта | BOM | Виден в Creo |
|---|---|---|---|
| `chugun_sch21-40.mtl` | `EF BB BF` | **✅ ЕСТЬ** | ✅ виден |
| `chugun_sch21.mtl` | `EF BB BF` | ✅ ЕСТЬ | ✅ виден |
| `chugun_sch18-36.mtl` | `EF BB BF` | ✅ ЕСТЬ | ✅ виден |
| `chugun_sch10.mtl` | `4E 44 5F` (`ND_`) | ❌ НЕТ | ❌ **НЕ виден** |
| `chugun_sch15/20/25/30/35.mtl` | `4E 44 5F` | ❌ НЕТ | ❌ не видны |
| `chugun_chvg45.mtl`, `chugun_vch50.mtl` | `EF BB BF` | ✅ ЕСТЬ | видны |

**⇒ ПРАВИЛО (проверено на 411 файлах, совпадение 100 %):**
**`.mtl` без BOM (в CP1251 или UTF-8 без BOM) Creo ИГНОРИРУЕТ — материал не появляется
в списке «Материалы в библиотеке». Файл обязан быть UTF-8 WITH BOM.**

**Замер «до»:** с BOM — **54** файла, без BOM — **357** ⇒ Creo видел лишь ~13 % библиотеки.
**После приведения:** с BOM — **411 из 411**.

**Как править (безопасно):**
```powershell
# прочитать (с учётом BOM) -> записать UTF-8 С BOM
$t = [Text.Encoding]::UTF8.GetString($b,3,$b.Length-3)   # если BOM есть
$bytes = [Text.Encoding]::UTF8.GetBytes($t)
$out = New-Object byte[] ($bytes.Length+3)
$out[0]=0xEF; $out[1]=0xBB; $out[2]=0xBF
[Array]::Copy($bytes,0,$out,3,$bytes.Length)
[IO.File]::WriteAllBytes($path,$out)
```

⚠️ **Следствие:** конвертация `.mtl` в CP1251 (что делали ранее «для порядка») — **ломает видимость
в Creo**. Кодировка библиотеки — **UTF-8 with BOM**, а не CP1251.

## 3б. Структура файла (обязательна для чтения Creo)

```
ND_RelParSet_K01 = {
                          ← пустая строка
Name = <ИМЯ>
                          ← пустая строка
PARAMETERS =
{
  Name = PTC_MATERIAL_TYPE
  Type = Integer
  Default = 9
  Access = Locked
},                        ← запятая после каждого блока, КРОМЕ последнего
{ ... },
{ ... }                   ← последний блок БЕЗ запятой
                          ← пустая строка
}                         ← закрытие PARAMETERS
                          ← пустая строка
}                         ← закрытие ND_RelParSet
```

**ГРАБЛИ СТРУКТУРЫ (получены на живых файлах 05.11.2026):**
1. **Лишняя `,` перед закрывающей `}`** — файл не парсится, материал не виден.
2. **Пустая строка на месте `}`** последнего блока — файл не парсится.
3. **Блок параметра, вставленный ПОСЛЕ закрывающей `}`** (вне `PARAMETERS`) — параметр не читается.
4. Вставка нового параметра — **ТОЛЬКО внутрь `PARAMETERS`, ПЕРЕД последней `}`**,
   с обязательной запятой у предыдущего блока:
   ```
   },      ← предыдущий блок получает запятую
   {
     Name = PTC_MATERIAL_ID
     Type = String
     Default = 'марка'
     Access = Full
   }       ← новый последний - БЕЗ запятой
   ```


## 2. СЛОВАРЬ `.mtl` — 76 ключей (живой замер по 411 файлам)

Цифра в скобках = в скольких файлах ключ **ЗАПОЛНЕН** (не просто присутствует).

**Механика (ядро):** `PTC_YOUNG_MODULUS` (329) · `PTC_POISSON_RATIO` (329) · `PTC_MASS_DENSITY` (**408**) ·
`PTC_THERMAL_EXPANSION_COEF` (324) · `PTC_THERMAL_CONDUCTIVITY` (327) · `PTC_SPECIFIC_HEAT` (328) ·
`PTC_HARDNESS` + `PTC_HARDNESS_TYPE` (97).
**Прочность:** `PTC_TENSILE_ULTIMATE_STRESS` (16) · `PTC_TENSILE_YIELD_STRESS` (47) · `PTC_COMPR_ULTIMATE_STRESS` (14).
**Усталость/удар:** `PTC_FATIGUE_STRENGTH` (47) · `PTC_IMPACT_ENERGY` (47) · `PTC_S_N_CURVE` (47) · `PTC_CYCLES` (3) ·
`PTC_FATIGUE_MATERIAL_TYPE` / `_FINISH` / `PTC_FATIGUE_STRNGTH_REDUCT_FCTR` (10).
**Идентификация:** `PTC_MATERIAL_ID` (**47**) · `PTC_MATERIAL_SOURCE` (47) · `PTC_MATERIAL_DESCRIPTION` (402).
**Служебные (Locked/системные):** `PTC_MATERIAL_TYPE` (411) · `PTC_FAILURE_CRITERION_TYPE` (411) ·
`PTC_FATIGUE_TYPE` (411) · `PTC_INITIAL_BEND_Y_FACTOR` (411) · `PTC_MATERIAL_SUB_TYPE` (54) · `TEMPERATURE` (411).
**Вид/штриховка:** `PTC_XHATCH_FILE` (402) · `PTC_DEFAULT_APPEARANCE` (**395**) · `PTC_APPEARANCE_1..7` (329 … 1).
**Единицы:** `PRO_UNIT_SYS` (87) · `PRO_UNIT_MASS` (30) · `PRO_UNIT_LENGTH` (30).
**Композит/демпфинг:** `PTC_MTRL_FABRIC_ARCHITECTURE` (29) · `PTC_MTRL_MECHANISMS_DAMPING` (13).
**Granta:** `GRANTA_DATABASE_KEY` / `_DATALINK_VERSION` / `_IDENTITY_GUID` / `_MODEL_REFERENCE` / `_VERSION_GUID` (по 3).
**Доморощенные русские:** `МАТЕРИАЛ_МАРКА` (262) · `МАТЕРИАЛ_СТАНДАРТ` (262) · `МАТЕРИАЛ` (89) ·
`Материал1` (62) · `Материал2` (6) · `Сортамент` (5) · `Профиль` (5) · `Толщина` (10) · `Диаметр` (12) ·
`ТЕМПЕРАТУРНЫЕ_УСЛОВИЯ` (12) · `Показатель_преломления` (2) · `Дисперия` (1).
Есть, но со ПУСТЫМ значением во всех файлах: `СОРТАМЕНТ_РАЗМЕР`, `СОРТАМЕНТ_СТАНДАРТ`, `ПРОКАТ` (0).

**🔴 БИТАЯ КОДИРОВКА (грабля):** **43 + 42 + 1 + 1** файла несут имена параметров в испорченной кодировке
(в выводе выглядят как `пїЅпїЅпїЅ…_пїЅпїЅпїЅпїЅпїЅ`). Имена вида `МАТЕРИАЛ_МАРКА` прочитаны НЕВЕРНОЙ кодовой
страницей. Это не ошибка чтения: имя записано в UTF-8/двойной кодировке. **В Creo такие имена покажутся
«кракозябрами».** Как отличить: прочитать файл в CP1251 и в UTF-8 — где имя читаемое, там и кодировка файла.

## 3. СЛОВАРЬ `.mat` — 20 ключей и ПОЛНОТА (живой счёт 208 файлов)

| Параметр | Заполнено | Вывод |
|---|---|---|
| `YOUNG_MODULUS` | **208** | ✅ всегда |
| `POISSON_RATIO` | **208** | ✅ всегда |
| `MASS_DENSITY` | **208** | ✅ всегда |
| `STRESS_LIMIT_FOR_TENSION` | **208** | ✅ всегда |
| `CONDITION` | **208** | ✅ всегда |
| `PRO_UNIT_SYS` | **199** | ⚠️ 9 файлов без системы единиц |
| `STRESS_LIMIT_FOR_COMPRESSION` | **68** | ⚠️ только 1/3 |
| `INITIAL_BEND_Y_FACTOR` | **43** | ⚠️ |
| `SHEAR_MODULUS` | **0** | 🔴 дыра |
| `THERMAL_EXPANSION_COEFFICIENT` | **0** | 🔴 дыра |
| `THERM_EXPANSION_REF_TEMPERATURE` | **0** | 🔴 дыра |
| `STRUCTURAL_DAMPING_COEFFICIENT` | **0** | 🔴 дыра |
| `STRESS_LIMIT_FOR_SHEAR` | **0** | 🔴 дыра |
| `THERMAL_CONDUCTIVITY` | **0** | 🔴 дыра |
| `EMISSIVITY` | **0** | 🔴 дыра |
| `SPECIFIC_HEAT` | **0** | 🔴 дыра |
| `HARDNESS` | **0** | 🔴 дыра |
| `BEND_TABLE` | **0** | 🔴 дыра |
| `PRO_UNIT_MASS` | **0** | 🔴 дыра |
| `PRO_UNIT_LENGTH` | **0** | 🔴 дыра |

**⇒ ОТВЕТ ПО СУЩЕСТВУ:** `.mat` в рабочей папке **заполнены НЕ полностью — 8 ключей из 20**;
9 физических свойств пустуют во ВСЕХ 208 файлах. Прежде чем пользоваться `.mat` — искать `.mtl` с тем же именем.

**Полнота `.mtl` по 6 ключевым свойствам (из 411):** без `PTC_MATERIAL_ID` — **364** ·
без `PTC_YOUNG_MODULUS` — **82** · без теплопроводности — **84** · без теплоёмкости — **83** ·
без `PTC_HARDNESS` — **314** · без `PTC_MASS_DENSITY` — всего **3**.


## 4. МИНИМУМ ДЛЯ РАБОЧЕГО МАТЕРИАЛА (чек-лист)

Обязательные параметры `.mtl` (набор подтверждён живым `Чугун\chugun_chvg45.mtl`, 44 параметра):

```
PTC_MATERIAL_ID · PTC_MATERIAL_SOURCE · PTC_MATERIAL_DESCRIPTION · PTC_CONDITION (или МАТЕРИАЛ)
PTC_MASS_DENSITY · PTC_YOUNG_MODULUS · PTC_POISSON_RATIO
PTC_THERMAL_EXPANSION_COEF · PTC_THERMAL_CONDUCTIVITY · PTC_SPECIFIC_HEAT
PTC_HARDNESS + PTC_HARDNESS_TYPE · PTC_TENSILE_ULTIMATE_STRESS · PTC_TENSILE_YIELD_STRESS
PTC_XHATCH_FILE · PTC_DEFAULT_APPEARANCE
PRO_UNIT_MASS · PRO_UNIT_LENGTH · PRO_UNIT_SYS
```

**Единицы — НЕ СМЕШИВАТЬ.** Три разных семейства живут в одной библиотеке:

| Где | Единицы | Живой факт |
|---|---|---|
| Паспорт компании (`STANDARDS\SKILL_company_config.md`) | **MMKS / кг** | `pro_unit_sys = MMKS` |
| `.mtl` рабочей папки | **mmGSK / грамм** | `PRO_UNIT_MASS = 'UNIT_GRAM'`, `PRO_UNIT_SYS = 'Milimeter Gram Second(mmGSK)'`, `PTC_YOUNG_MODULUS = 160000000.0 kPa` |
| `.mat` рабочей папки | **mmKs / килограмм** | `PRO_UNIT_SYS = millimeter Kilogram Sec (mmKs)` |

## 5. ПОРЯДОК ПРОВЕРКИ (по шагам)

1. Найти, ЧЕМ имя определено: `pro_material_dir` в `START-STD\config.pro` → корень точки монтирования.
2. Считать состав счётчиком (не глазами): `Get-ChildItem -Recurse -File | Group-Object Extension`.
3. Значение искать ТОЧНО по `^\s*<КЛЮЧ>\s*=`, а НЕ по любому `=` — **грабля**: `Name = ...` в шапке
   даёт ложное «заполнено» (ложный результат «208/208», где реально 8/20).
4. Отвечая «все ли параметры вписаны» — называть числа ПО КАЖДОМУ ключу, а не «вроде да».
5. Пользоваться `.mtl`; `.mat` считать устаревшим слоем; `.dmt` — палитра, не материал.
6. Проверять кодировку русских имён (десятки файлов испорчены); при правке кодировку выбирать осознанно.
7. `Z:\PTC` — только чтение: любые правки библиотеки — **сначала копия в `D:\AI\PROBA`**, потом проба.

## 6. ГРАБЛИ ЭТОЙ ТЕМЫ (живые)

1. **«Каноничный без `PTC_`»** — ошибочное правило прежней версии скилла; ломает работу с `.mtl` (411 файлов).
2. **Ложный замер полноты** через regex `=` (см. §5 п.3).
3. **Имена параметров в битой кодировке** — десятки файлов; не путать с реально отсутствующим параметром.
4. **`Латунь\global.dmt`** содержит `material_name "Стекло просветленное"` — имя папки НЕ определяет
   содержимое (догма §М.1г: связь ищем ВНУТРИ файла).
5. **`materials-library\`** (137 файлов, PTC Granta-Design, англ.) лежит внутри `pro_material_dir`, но
   **в `config.pro` НЕ объявлен** — мусорная зона внутри точки монтирования.
6. **`МАТЕРИАЛЫ.rar`** в корне `НАСТРОЙКИ\` — архив рядом с живой точкой монтирования.
7. **Скачки глубины** в дереве: `.mtl` — 1–2 уровня (171/240), `.mat` — 2–3 (128/80) ⇒ маршрут клика
   в Creo непостоянен.

## 7. СВЯЗАННЫЕ СКИЛЛЫ

- `Creo\READ\SKILL_creo_materials.md` — что читается из файла МОДЕЛИ (`PTC_SYSTEM_MTRL_PROPS`, плотность, фильтры).
- `Creo\SKILL_materials_creo_detailed.md` — конспект Simulate-параметров (модули STATIC/PLASTICITY/FATIGUE/DESTRUCTION).
- `Creo\STANDARDS\CARDS\MATERIALS_INDEX.md` — карточки 20 марок (`*.json`).
- `Creo\SKILL_creo_file_reading.md` §8.7.5 — `config.pro` и пути склада.
- Инструмент чтения дома: `D:\AI\tools\agent\plm_reader\`.

