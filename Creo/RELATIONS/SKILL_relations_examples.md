---
name: relations-examples
system: Creo
description: ПРАКТИЧЕСКИЕ ПРИМЕРЫ ОТНОШЕНИЙ (НАШИ ДЕТАЛИ)
when: примеры отношений, масса на чертеж, обозначение, параметры сборки
priority: high
source: relations_examples.md
---
# ПРАКТИЧЕСКИЕ ПРИМЕРЫ ОТНОШЕНИЙ (НАШИ ДЕТАЛИ)

## 1. Шифр и вывод на чертёж
shifr = "МК-262"  /* строковый параметр */
В основной надписи (MY_ESKD.dtl) переменная &shifr подставит шифр.
Чертеж переименовывается вместе с моделью (rename_drawings_with_object both).

## 2. Масса на чертёж (MP-параметры)
После анализа масс создаются MP_MASS, MP_VOLUME.
massa = floor(MP_MASS * 10) / 10  /* округлить до 0.1 кг, единицы кг (mmks) */
В надписи: &massa.

## 3. IF/ENDIF по типу секции
IF tip_sekcii == "BDF"
  tolshchina_flanca = 20
ELSE
  tolshchina_flanca = 15
ENDIF

## 4. Число отверстий по шагу
n_otv = floor(360 / shag_otv)
shag_otv = 360 / n_otv

## 5. Сборка: читать параметр компонента
d0@M-A338-6-75-01-ЯЩИК-ОСНОВНАЯ — размер/параметр компонента.
vysota_sborki = d5@KORPUS + d5@KRYSHKA

## 6. Листовой металл (Y-фактор 0.7854 из config.pro)
dlina_razvertki = 2*(storona + tolshchina) - 4*tolshchina + 2*(PI*radius*0.5)

## 7. Нормоконтроль отношений
- Символы — латиницей/транслитом, без пробелов.
- Строки — в двойных кавычках.
- Не ссылаться на детали из НЕ ПОЛЬЗОВАТЬСЯ / СТАРОЕ.
- Шифр в параметре = имени файла модели.