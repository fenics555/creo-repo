# SKILL_GRABLI: Lessons Learned

## Python Regex & Binary Data
- **Problem**: `re.PatternError: incomplete escape \x0 at position N`.
- **Cause**: Using literal `\x0` in a regex string in Python causes the parser to fail because it expects a two-digit hex code after `\x`.
- **Solution**: 
    - Use direct byte searching (`bytes.find()`) for locating keys.
    - If regex is absolutely necessary, use `re.escape()` or double-escape the sequence, or better yet, avoid raw byte escapes in the pattern string.
    - For binary data, work with `bytes` objects and avoid decoding until the value is isolated.

## Tooling Limitations
- **Editor**: When `editor` fails to replace text due to `old_text` mismatches or encoding issues, switch to creating a new file (e.g., `filename_vX.py`) to ensure a clean state.
- **Shell Encoding**: Be cautious with Cyrillic paths in shell commands. Use absolute paths and ensure encoding is handled correctly.

## ❌ КРИТИЧЕСКИЕ ОШИБКИ (Обновлено: 21.10.2026)

### 1. ПЕТЛЯ ПОИСКА (Search Loop)
- **Проблема**: Попытка найти ID через `Select-String` (текст) $\rightarrow$ `search_int` (число) $\rightarrow$ `regex` (паттерн) без изменения глубины анализа.
- **Симптом**: Инструменты возвращают 0 результатов, и агент продолжает вызывать их с другими паттернами.
- **Решение**: Если 3 попытки разными инструментами дали 0, СМЕНИТЬ МЕТОД. Переходи от «поиска значения» к «анализу структуры вокруг ключа».

### 2. ЛОЖНЫЕ ИДЕНТИФИКАТОРЫ
- **Проблема**: Принятие `id_map_info_ptr` за сам ID.
- **Инсайт**: Значение `id_map_info_ptr` — это **навигатор (offset/key)**, а не целевой ID приспособления. Поиск самого значения на диске бесполезен.


## ❌ КРИТИЧЕСКИЕ ОШИБКИ (Обновлено: 21.10.2026)

### 1. ПЕТЛЯ ПОИСКА (Search Loop)
- **Проблема**: Попытка найти ID через `Select-String` (текст) $\rightarrow$ `search_int` (число) $\rightarrow$ `regex` (паттерн) без изменения глубины анализа.
- **Симптом**: Инструменты возвращают 0 результатов, и агент продолжает вызывать их с другими паттернами.
- **Решение**: Если 3 попытки разными инструментами дали 0, СМЕНИТЬ МЕТОД. Переходи от «поиска значения» к «анализу структуры вокруг ключа».

### 2. ЛОЖНЫЕ ИДЕНТИФИКАТОРЫ
- **Проблема**: Принятие `id_map_info_ptr` за сам ID.
- **Инсайт**: Значение `id_map_info_ptr` — это **навигатор (offset/key)**, а не целевой ID приспособления. Поиск самого значения на диске бесполезен.


### 3. ОШИБКА ВЫХОДА ЗА ПРЕДЕЛЫ (Out of Bounds)
- **Проблема**: Интерпретация 16-битного указателя как 32-битного (uint32).
- **Симптом**: `Target address is out of bounds (file size: 0x...)`.
- **Решение**: Всегда проверяй, является ли указатель относительным (relative) или абсолютным. В Creo `id_map_info_ptr` — это **relative uint16**.

### 4. НАВИГАТОР (Navigator Insight)
- **Инсайт**: `id_map_info_ptr` — это **16-битное относительное смещение** (uint16) от начала блока `setup_data`.
- **Формула**: `Table_Start = setup_data_offset + (ptr_value & 0xFFFF)`.

