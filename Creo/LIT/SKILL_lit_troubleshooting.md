

name: lit-troubleshooting
system: Creo
description: Справочник по диагностике и устранению типичных ошибок при работе с Relations в Creo Parametric для литья. Содержит коды ошибок, причины и способы их решения.
when: relations, liatie, hts, ошибки, крахи, отладка, debug
priority: critical
date: 24.09.2026
---
# SKILL_lit_troubleshooting - Диагностика ошибок в Relations (обновлено)

## 🚨 7 КРИТИЧЕСКИХ ОШИБОК

### 1. Formula is too long
**Решение:** Разбить уравнение на строки через `+`:
```relations
D1 = 4 * V / pi
D2 = D1 * H
D = sqrt(D2)
```

### 2. Variable not found
**Решение:** Проверьте регистр имен: `D_sprue` ≠ `D_Sprue` ≠ `DSPRUE`. Используйте_symb имена: `tollshchina`, `diam_otv`, `visota_styaka`.

### 3. Regeneration failed
**Решение:** Убедитесь нет циклических зависимостей A→B→A. Всегда добавляйте проверку на ноль перед делением:
```relations
IF D > 0
    RESULT = N / D
ENDIF
```

### 4. Incorrect units
**Решение:** Всегда используйте одни и те же единицы (мм для линейных, см³ для объемов). Константы перевода:
- `CONST_MM_PER_CM = 10.0`
- `CONST_MM3_PER_CM3 = 1000.0`

### 5. SAFE-block not working
**Решение:** Имена параметров в SAFE-блоке должны точно совпадать с именами в БЛОКЕ 1 (входные параметры). Проверьте spelling и регистр.

### 6. Unexpected IF structure
**Решение:** Всегда используйте структуру: `IF условие ... ELSE ... ENDIF`. Не более 5 уровней вложенности.

### 7. HOT_FACTOR not defined
**Решение:** Рассчитайте до использования: `HOT_FACTOR = 1 - (USADKA_P / 100)`. Проверьте диапазон: 0.85–0.98 (слиее — высокая усадка, больше 0.98 — ошибка ввода).

## 📋 КОДЫ ОШИБОК (E-Codes)

| Код | Название | Что делаем |
|-----|----------|------------|
| E01 | DEFINITION_ERROR | Проверьте имя параметра, правильный регистр |
| E02 | DIVISION_BY_ZERO | Добавьте `IF X > 0` перед делением |
| E03 | UNIT_MISMATCH | Приведите все размеры к мм/см³ |
| E04 | RECURSIVE_DEP | Перестройте порядок расчетов |
| E05 | FORMULA_TOO_LONG | Разбейте формулу на под-выражения |

## 🔧 БЫСТРАЯ ПРОВЕРКА (Quick Check)

```relations
QUICK = "СТАТУС ОК"
IF MASSA_OTLIVKI <= 0 QUICK = "⚠ Масса ≤ 0"
IF H0_MM <= 0 QUICK = "⚠ Высота ≤ 0"
IF SXEMA_PITANIYA < 1 OR SXEMA_PITANIYA > 4 QUICK = "⚠ Схема питания"
message "Быстрая проверка: " QUICK
```

## 📝 ЗАПИСИ
```
# ВОЗНИКНОВЕНИЕ: 24.09.2026 — Создание файла troubleshooting
# АВТОР: Cline
```
## 🚨 7 КРИТИЧЕСКИХ ОШИБОК

### 1. Formula is too long
**Решение:** Разбить уравнение на строки через `+`:
```relations
D1 = 4 * V / pi
D2 = D1 * H
## 📋 КОДЫ ОШИБОК (E-Codes)

| Код | Название | Что делаем |
|-----|----------|------------|
| E01 | DEFINITION_ERROR | Проверьте имя параметра, правильный регистр |
| E02 | DIVISION_BY_ZERO | Добавьте `IF X > 0` перед делением |
| E03 | UNIT_MISMATCH | Приведите все размеры к мм/см³ |
| E04 | RECURSIVE_DEP | Перестройте порядок расчетов |
| E05 | FORMULA_TOO_LONG | Разбейте формулу на под-выражения |

## 🔧 БЫСТРАЯ ПРОВЕРКА (Quick Check)

```relations
QUICK = "СТАТУС ОК"
IF MASSA_OTLIVKI <= 0 QUICK = "⚠ Масса ≤ 0"
IF H0_MM <= 0 QUICK = "⚠ Высота ≤ 0"
IF SXEMA_PITANIYA < 1 OR SXEMA_PITANIYA > 4 QUICK = "⚠ Схема питания"
message "Быстрая проверка: " QUICK
```
D = sqrt(D2)
```

### 2. Variable not found
**Решение:** Проверьте регистр имен: `D_sprue` ≠ `D_Sprue` ≠ `DSPRUE`. Используйте_symb имена: `tollshchina`, `diam_otv`, `visota_styaka`.

### 3. Regeneration failed
**Решение:** Убедитесь нет циклических зависимостей A→B→A. Всегда добавляйте проверку на ноль перед делением:
```relations
IF D > 0
    RESULT = N / D
ENDIF
```

### 4. Incorrect units
**Решение:** Всегда используйте одни и те же единицы (мм для линейных, см³ для объемов). Константы перевода:
- `CONST_MM_PER_CM = 10.0`
- `CONST_MM3_PER_CM3 = 1000.0`

### 5. SAFE-block not working
**Решение:** Имена параметров в SAFE-блоке должны точно совпадать с именами в БЛОКЕ 1 (входные параметры). Проверьте spelling и регистр.

### 6. Unexpected IF structure
**Решение:** Всегда используйте структуру: `IF условие ... ELSE ... ENDIF`. Не более 5 уровней вложенности.

### 7. HOT_FACTOR not defined
**Решение:** Рассчитайте до использования: `HOT_FACTOR = 1 - (USADKA_P / 100)`. Проверьте диапазон: 0.85–0.98 (слиее — высокая усадка, больше 0.98 — ошибка ввода).