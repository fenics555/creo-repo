# ПАРАМЕТРЫ И МАССОВЫЕ ХАРАКТЕРИСТИКИ CREO

- name: parameters_guide
- system: Creo
- description: ПАРАМЕТРЫ И МАССОВЫЕ ХАРАКТЕРИСТИКИ CREO
- when: параметры, MP_MASS, массовые, вывод на чертеж
- priority: medium
- source: parameters_guide.md

## 1. Создание

Tools > Parameters > добавить. Или прямо отношением (присвоением).
Типы: REAL, INTEGER, STRING, YES/NO.

## 2. Массовые (MP_) параметры

Анализ массовых характеристик создаёт MP_MASS (кг), MP_VOLUME, MP_COG_X/Y/Z.
Использовать в отношениях: massa = MP_MASS. Вывод на чертёж: &massa.

## 3. Вывод на чертёж

В заметке/надписи: &имя_параметра (например &shifr, &massa, &material).
Для модели в сборке: &param@COMPONENT.

## 4. Единицы компании

mmks: мм, кг, сек. Линейные и угловые — 4 знака (default_dec_places 4).

## 5. Ссылки на материалы

Смотри также: `SKILL_material_parameters.md` — каноничный словарь параметров материалов Creo.
Основные модули справки Creo 12.4.2.0 по материалам:
- `fundamentals` — основные концепции материалов
- `model_analysis` — анализ моделей с параметрами материалов
- `configuration_options` — опции конфигурации материалов