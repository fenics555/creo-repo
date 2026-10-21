# SKILL_material_parameters

- name: material-parameters
- system: Creo
- description: ПАРАМЕТРЫ МАТЕРИАЛОВ СРЕДСТВОМ Creo - каноничный словарь (HELP) + домашние PTC_* и проверка верно/нет.
- when: параметры материалов, материалы, PTC_
- source: crero_help_pma + Чугун VCh*.mat + OGV *.mtl

## 1. Два поколения параметров

- Каноничные (HELP 13 / .mat): YOUNG_MODULUS, POISSON_RATIO, SHEAR_MODULUS, THERMAL_EXPANSION_COEFFICIENT, THERMAL_EXPANSION_REF_TEMPERATURE, STRUCTURAL_DAMPING_COEFFICIENT, STRESS_LIMIT_FOR_TENSION, STRESS_LIMIT_FOR_COMPRESSION, STRESS_LIMIT_FOR_SHEAR, THERMAL_CONDUCTIVITY, EMISSIVITY, SPECIFIC_HEAT, HARDNESS, CONDITION, INITIAL_BEND_Y_FACTOR, BEND_TABLE, PRO_UNIT_MASS, PRO_UNIT_LENGTH, PRO_UNIT_SYS.
- Домашние: *.mtl в materials-library / Сортамент / OGV используют PTC_* (PTC_YOUNG_MODULUS, PTC_MATERIAL_DESCRIPTION, PTC_HARDNESS_TYPE).
- Правило: PTC_ домашний префикс, не каноничный. Каноничный - без PTC_.

## 2. Каноничный словарь (HELP .mat)

| Параметр | Тип | Единицы | Назначение |
|---|---|---|---|
| YOUNG_MODULUS | Real | MPa mmks | модуль упругости |
| POISSON_RATIO | Real | безразмер | отношение поперечной деформации |
| SHEAR_MODULUS | Real | MPa | модуль сдвига |
| THERMAL_EXPANSION_REF_TEMPERATURE | K | ссылка для ТКЭ | температурная точка отсчёта коэффициента теплового расширения |
| STRUCTURAL_DAMPING_COEFFICIENT | безразмер | демпфинг | показатель затухания упругих колебаний |
| STRESS_LIMIT_FOR_TENSION | MPa | предел растяжения | предел прочности при растяжении |
| STRESS_LIMIT_FOR_COMPRESSION | MPa | предел сжатия | предел прочности при сжатии |
| STRESS_LIMIT_FOR_SHEAR | MPa | предел сдвига | предел прочности при сдвиге |
| THERMAL_CONDUCTIVITY | W/mK | теплопроводность | теплопроводность материала при 20 °C |
| EMISSIVITY | безразмер | коэффициент излучения | коэффициент теплового излучения поверхности (0-1) |
| SPECIFIC_HEAT | J/kgK | теплоёмкость | удельная теплоёмкость при 20 °C |
| HARDNESS | HB/HRC | твёрдость | твёрдость по шкале HB (брусень) или HRC (жесткое приспособление) |
| CONDITION | String | состояние/размер | состояние, толщина или размер заготовки |
| INITIAL_BEND_Y_FACTOR | - | поправочный множитель изгиба | начальный коэффициент изгиба по оси Y |
| BEND_TABLE | String | таблица изгиба | таблица коэффициентов изгиба для пластин |
| PRO_UNIT_MASS | String | ед. массы | единица массы в Creo (kg, lb, etc.) |
| PRO_UNIT_LENGTH | String | ед. длины | единица длины в Creo (mm, in, etc.) |
| PRO_UNIT_SYS | String | mm kg sec | основная система единиц Creo (mm, kg, sec) |

## 3. Проверка доменных файлов

- Чугун VCh100: имена есть, значения пустые (ТЭ, теплопроводность, теплоёмкость, твёрдость, демпфинг). Это — НЕТ ДАННЫХ, не ошибочные имена.
- Сталь OGV 08x18h10: параметры есть и заполнены (E, nu, G, плотность, ТЭ, теплопроводность, теплоёмкость, твёрдость HRC) + PTC_MATERIAL_ID, PTC_MATERIAL_SOURCE.
- Наследуемые *.mtl (Legacy): упрощённые, PTC_MATERIAL_TYPE=9, FAILURE=NONE, FATIGUE=NONE — заглушки, не в продакшн.

## 4. Порядок действий

- Проверять файл: имена по каноничному словарю, значения и единицы не пустые.
- Добавлять параметр: в карточку (cards) + доменный словарь + бэкап в Старые правила + указатель в SKILL_index.md.
- Не копировать наследуемые заглушки (Default=9, NONE) в реальные модули.

## 5. Источники

- D:\AI\repo\Creo\STANDARDS\SKILL_material_parameters.md — этот спеки.
- D:\AI\repo\Creo\CREO_MAP.md, SKILLS_MAP.md — карты ветки Creo.
- Z:\PTC\CREO-START\НАСТРОЙКИ\МАТЕРИАЛЫ\materials-library — библиотека материалов.
- Z:\PTC\CREO-START\НАСТРОЙКИ\МАТЕРИАЛЫ\Сортамент, OGV, для фрез — каталоги материалов.
- crero_help_pma (D:\PTC\CREO13\Creo 13.4.1.0\creo_help_pma) — справочник Creo.