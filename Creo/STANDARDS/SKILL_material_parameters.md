# SKILL_material_parameters

- name: material-parameters
- system: Creo
- description: ПАРАМЕТРЫ МАТЕРИАЛОВ СРЕДСТВОМ Creo - каноничный словарь (HELP) + домашние PTC_* и проверка верно/нет.
- when: параметры материалов, материалы, PTC_
- source: crero_help_pma + Чугун VCh*.mat + OGV *.mtl

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

## 4. Консолидация PTC_ -> CANONICAL (по аудиту 21.10.2026)

| PTC_* (дом. префикс) | CANONICAL (HELP .mat) | Замечание |
|---|---|---|
| PTC_YOUNG_MODULUS | YOUNG_MODULUS | OK |
| PTC_POISSON_RATIO | POISSON_RATIO | OK |
| PTC_MASS_DENSITY | - | Дом. замена |
| PTC_THERMAL_EXPANSION_COEF | THERMAL_EXPANSION_COEFFICIENT | OK |
| PTC_THERMAL_CONDUCTIVITY | THERMAL_CONDUCTIVITY | OK |
| PTC_SPECIFIC_HEAT | SPECIFIC_HEAT | OK |
| PTC_HARDNESS | HARDNESS | OK |
| PTC_CONDITION | CONDITION | OK |
| PTC_INITIAL_BEND_Y_FACTOR | INITIAL_BEND_Y_FACTOR | OK |
| PTC_BEND_TABLE | BEND_TABLE | OK |
| PTC_MATERIAL_TYPE | - | Legacy, не каноничный |
| PTC_MATERIAL_SOURCE | - | Legacy, не каноничный |
| PTC_MATERIAL_ID | - | Legacy, не каноничный |

## 5. Порядок действий

- Проверять файл: имена по каноничному словарю, значения и единицы не пустые.
- Добавлять параметр: в карточку (cards) + доменный словарь + бэкап в Старые правила + указатель в SKILL_index.md.
- Не копировать наследуемые заглушки (Default=9, NONE) в реальные модули.

## 6. Источники

- D:\\AI\\repo\\Creo\\STANDARDS\\SKILL_material_parameters.md — этот спеki.
- D:\\AI\\repo\\Creo\\CREO_MAP.md, SKILLS_MAP.md — карты ветки Creo.
- Z:\\PTC\\CREO-START\\НАСТРОЙКИ\\МАТЕРИАЛЫ\\materials-library — библиотека материалов.
- Z:\\PTC\\CREO-START\\НАСТРОЙКИ\\МАТЕРИАЛЫ\\Сортамент, OGV, для фрез — каталоги материалов.
- D:\\PTC\\CREO12\\Creo 12.4.2.0\\Common Files\\creo_help_pma — **Полная справка Creo** (HTML + картинки, 1115 МБ, 97 192 файла).
- D:\\PTC\\CREO12\\Creo 12.4.2.0\\Common Files\\creo_help_pma\\russian — **Русская справка** (15 678 HTML, 569 МБ, 48 456 файлов, 35 модулей).
  - Основные модули, связанные с материалами:
    - `fundamentals` — основные концепции и определения материалов
    - `model_analysis` — анализ моделей с параметрами материалов
    - `configuration_options` — опции конфигурации материалов
    - `part_modeling` — работа с материалами при конструировании деталей
    - `detail` — параметры материалов для деталей
    - `manufacturing` — материалы в контексте производства
- crero_help_pma (D:\\PTC\\CREO13\\Creo 13.4.1.0\\creo_help_pma) — справочник Creo.
- D:\\AI\\repo\\Creo\\STANDARDS\\SKILL_creo_cards_audit_2026-10-21.md — **аудит материалов** (21.10.2026), консолидация PTC_ -> CANONICAL, статус карточек по маркам
