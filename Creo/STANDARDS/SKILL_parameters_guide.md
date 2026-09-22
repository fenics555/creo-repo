---
name: parameters-mp
system: Creo
description: ПАРАМЕТРЫ И МАССОВЫЕ ХАРАКТЕРИСТИКИ CREO
when: параметры, MP_MASS, массовые, вывод на чертеж
priority: medium
source: parameters_guide.md
---
# ПАРАМЕТРЫ И МАССОВЫЕ ХАРАКТЕРИСТИКИ CREO

## Создание
Tools > Parameters > добавить. Или прямо отношением (присвоением).
Типы: REAL, INTEGER, STRING, YES/NO.

## Массовые (MP_) параметры
Анализ массовых характеристик создаёт MP_MASS (кг), MP_VOLUME, MP_COG_X/Y/Z.
Использовать в отношениях: massa = MP_MASS. Вывод на чертёж: &massa.

## Вывод на чертёж
В заметке/надписи: &имя_параметра (например &shifr, &massa, &material).
Для модели в сборке: &param@COMPONENT.

## Единицы компании
mmks: мм, кг, сек. Линейные и угловые — 4 знака (default_dec_places 4).