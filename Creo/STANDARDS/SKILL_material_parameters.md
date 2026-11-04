## 1. Два поколения параметров

- Каноничные (HELP .mat): YOUNG_MODULUS, POISSON_RATIO, SHEAR_MODULUS, THERMAL_EXPANSION_COEFFICIENT, THERMAL_EXPANSION_REF_TEMPERATURE, STRUCTURAL_DAMPING_COEFFICIENT, STRESS_LIMIT_FOR_TENSION, STRESS_LIMIT_FOR_COMPRESSION, STRESS_LIMIT_FOR_SHEAR, THERMAL_CONDUCTIVITY, EMISSIVITY, SPECIFIC_HEAT, HARDNESS, CONDITION, INITIAL_BEND_Y_FACTOR, BEND_TABLE, PRO_UNIT_MASS, PRO_UNIT_LENGTH, PRO_UNIT_SYS.
- Домашние: *.mtl в materials-library / Сортамент / OGV используют PTC_* (PTC_YOUNG_MODULUS, PTC_MATERIAL_DESCRIPTION, PTC_HARDNESS_TYPE).
- Правило: PTC_ домашний префикс, не каноничный. Каноничный - без PTC_.

## 2. Каноничный словарь (HELP .mat)

| Параметр | Тип | Единицы | Назначение |
|---|---|---|---|
| YOUNG_MODULUS | Real | MPa mmks | модуль упругости |
| POISSON_RATIO | Real | безразмер | отношение поперечной деформации |
| SHEAR_MODULUS | Real | MPa | модуль сдвига |
| THERMAL_EXPANSION_REF_TEMPERATURE | K | ссылка для ТКЭ | температура отсчета коэффициента теплового расширения |
| STRUCTURAL_DAMPING_COEFFICIENT | безразмер | демпфинг | показатель затухания упругих колебаний |
| STRESS_LIMIT_FOR_TENSION | MPa | предел растяжения | предел прочности при растяжении |
| STRESS_LIMIT_FOR_COMPRESSION | MPa | предел сжатия | предел прочности при сжатии |
| STRESS_LIMIT_FOR_SHEAR | MPa | предел сдвига | предел прочности при сдвиге |
| THERMAL_CONDUCTIVITY | W/mK | теплопроводность | теплопроводность материала при 20 °C |
| EMISSIVITY | безразмер | коэффициент излучения | коэффициент теплового излучения поверхности (0-1) |
| SPECIFIC_HEAT | J/kgK | теплоёмкость | удельная теплоёмкость при 20 °C |
| HARDNESS | HB/HRC | твердость | твердость по шкале HB (брусень) или HRC (жесткое приспособление) |
| CONDITION | String | состояние/размер | состояние, толщина или размер заготовки |
| INITIAL_BEND_Y_FACTOR | - | множитель изгиба | начальный коэффициент изгиба по оси Y |
| BEND_TABLE | String | таблица изгиба | таблица коэффициентов изгиба для пластин |
| PRO_UNIT_MASS | String | εд. массы | единица массы в Creo (kg, lb, etc.) |
| PRO_UNIT_LENGTH | String | εд. длины | единица длины в Creo (mm, in, etc.) |
| PRO_UNIT_SYS | String | mm kg sec | основная система единиц Creo (mm, kg, sec) |
## 4. Три формы чисел в UGC файлах Creo (§3 основной текст)

В UGC файлах Creo числа записываются тремя формами. Важно отличать их при декодировании:

| Форма | Вид в hex | Пример | Примечание |
|-------|-----------|--------|------------|
| **BE-double IEEE** | `e0 02 <имя> 00 ed <8 байт>` | `volume`, `mtrl_volume` | Плотность, объём |
| **упакованная 3 байта** | `[2f\|48][E:F12]` | `16.5 → 2f 30 80` | Малые значения |
| **расширенная 8 байт** | `[2d][E:F12][5 байт дроби]` | `16.1235 → 2d 30 1f 9a cf fa 7e b7` | Точные значения |

**⚠️ Длина плавает 1–3 байта** → поиск по фиксированным IEEE-узорам **не работает**.
Декодеры: `packed_decode.py`, `scan_packed.py`, `decode_reals.py`.

**Правило §8.76**: За значением идёт служебный префикс `\xf7 <1 байт>` — его надо отбросить (иначе «ч&UNCX01»!).