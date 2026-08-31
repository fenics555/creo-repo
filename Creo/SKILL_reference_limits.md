---
name: creo-limits
system: Creo
description: CREO REFERENCE — ЛИМИТЫ, СИНТАКСИС, ФУНКЦИИ (Help 12.4.2.0, выверено)
when: лимиты, длина имени, степень, ROUND, синтаксис IF
priority: medium
source: reference_limits.md
---
# CREO REFERENCE — ЛИМИТЫ, СИНТАКСИС, ФУНКЦИИ (Help 12.4.2.0, выверено)

## Лимиты (глоссарий Help)
- Имя параметра: 40 символов.
- Имя модели: 63 символа (практика: держать <= 40 — Windows, Vericut, посты).
- Строковое значение: 255 символов.
- Описание параметра: 1023 символа.

## Операторы
- Арифметика: + - * /
- Возведение в степень: ^   (d0 = 2 ^ 3; объем = d ^ 3)
- Сравнение: == != > < >= <=
- Логика: & (и), | (или), ! (не)
- Склейка строк: +   (msg = "C = " + itos(c))

## IF/ELSE
Блочная форма (основная, ENDIF обязателен):
IF (A > B)
  X = A - B
ELSE
  X = B - A
ENDIF
Однострочная IF...THEN...ELSE встречается в Help для простых выражений,
но всегда пишите блочную — гарантирована во всех версиях.
Вложенные IF разрешены (см. мастер пружины).

## Функции relations
abs, sqrt, ceil, floor, sin, cos, tan, asin, acos, atan,
log, ln, exp, max, min, itos, extract, search, string.
- ROUND НЕТ! Округление: floor(x + 0.5); вверх: ceil(x).
- Тригонометрия — в ГРАДУСАХ (угловые единицы компании — градусы).
- PI — встроенная константа (в мастере пружины: LOAD_TAU_DEN = PI * d ^ 3).

## Проверенные примеры (из нашего мастера пружины)
- Вложенные IF/ELSE со строковыми вердиктами: OTK_VERDICT = "Брак" / "Норма".
- Логика: if GEOMETRY_IS_TIGHT | GEOMETRY_IS_GROUND ... endif
- Строки: OTK_REC = "Менее " + CONST_TURNS_MIN_RECOMM_S + " витков"
- max/min: GEOMETRY_P_WORK = max(GEOMETRY_P_WORK_RAW, GEOMETRY_P_TOR)
- sqrt и ^: DYNAMIC_L_WIRE_M = sqrt((PI * FORM_D_EQ)^2 + GEOMETRY_P_WORK^2)
- Конвенция префиксов: CONST_, INPUT_, GEOMETRY_, FORM_, LOAD_, DYNAMIC_, CAD_, OTK_, ERR_.
- Адаптер d#: в конце отношений присваиваются размеры модели (d44 = GEOMETRY_P_TOR).
- ОБОЗНАЧЕНИЕ = REL_MODEL_NAME (шифр = имя модели).

## Сюда — ваши живые примеры
- (вставляйте реальные relations из деталей — бот выучит ваши приёмы)