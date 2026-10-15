# SKILL: Creo Raw Reader (Чтение «в лоб»)

**Статус:** В разработке (Прорыв достигнут, детализация не завершена).
**Направление:** Парсинг CAD-данных (Creo) без установленного ПО.

## 0. КАК ВЫЗВАТЬ (владелец, 15.10.2026) — ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ИСПОЛЬЗОВАНИЕМ

> 🔴 **`creo_read.py` — это БИБЛИОТЕКА, а не CLI-скрипт.** Прямой запуск
> `python creo_read.py <файл>` **МОЛЧИТ** (в файле нет блока `__main__`) — это НЕ ошибка, это норма.
> Правильный способ — **импорт**:

```powershell
# ПРАВИЛЬНО: импорт библиотеки и вызов функции passport()
python -c "import sys; sys.path.insert(0, r'D:\AI\tools\agent\plm_reader'); import creo_read; import pprint; pprint.pprint(creo_read.passport(r'D:\AI\PROBA\models\00080-03.prt'))"

# или скриптом (надёжнее для длинных путей):
#   creo_call.py:  import sys; sys.path.insert(0, r'D:\AI\tools\agent\plm_reader')
#                  import creo_read, pprint; pprint.pprint(creo_read.passport(r'<файл>'))
python -X utf8 creo_call.py
```

**ЗАПРЕЩЕНО:** `python creo_read.py <файл>` — молчаливый вывод = ложный «НЕТ ДАННЫХ».
**Файл:** `D:\AI\tools\agent\plm_reader\creo_read.py` (общая библиотека дома; также вложена в `plm_reader`, `batch_params`).
**Ключевые функции:** `passport(path)` — паспорт изделия (материал, размер, ревизия, автор, дата);
`parse_toc`, `params`, `real`, `last_hist`, `names`, `role`.
**Проверено 15.10.2026:** `passport('PROBA\models\00080-03.prt')` → `material=PTC_SYSTEM_MTRL_PROPS, size=61414, rev=114, author=KAMESH, revdate=05.01.24 10:15`.
**Владелец:** способ вызова инструмента — **ВСЕГДА в скилле**, иначе модель вызывает его наугад.

## 1. Описание метода (The "How")
Метод основан на прямом бинарном анализе файлов `.prt`, `.asm`, `.drw` с использованием регулярных выражений (`re`) и работы со структурами (`struct`). Это обеспечивает максимальную скорость и автономность.

### Ключевые механизмы:
*   **TOC-Parsing:** Поиск маркера `#UGC_TOC` и навигация по цепочке `NEXT_TOC_ENTRY`. Это позволяет быстро находить смещения (offsets) важных секций (например, `NeuPrtSld`).
*   **Binary Tagging:** Поиск параметров через специфические байтовые маркеры (`\xe2\x33`, `\x27\x88\x20\xe3\x33`).
*   **History Reconstruction:** Извлечение истории изменений через поиск бинарных штампов (stamps) в хвосте файла (`TAIL`).
*   **Role Detection:** Определение роли изделия (сборка, деталь, наследник) через анализ внутренних маркеров (например, `MERGE_BASE_PART`).

## 2. Выявленные «Грабли» (КРАШ-точки)
*   **DATABASE_MISMATCH:** Ошибка `sqlite3.OperationalError: no such table: arch_dims` при попытке слияния (merge) данных. Схема БД в `arch_merge.py` не содержит таблиц для хранения размерных данных.
*   **REDUNDANCY:** Попытки использования `Creoson` (тяжелый интерфейс) вместо легкого `creo_read.py`. Это создает лишние зависимости и точки отказа.
*   **DATA_TRUNCATION:** Ограничение в 20 итераций при парсинге оглавления (`parse_toc`) может привести к потере данных в очень больших или сложных файлах.

## 3. Дорожная карта (Roadmap)
1.  [ ] **Fix Schema:** Добавить создание таблиц `arch_dims` и `arch_dim_ch` в `arch_merge.py`.
2.  [ ] **Enhance Parser:** Реализовать полноценный метод `get_dimensions()` в `creo_read.py`.
3.  [ ] **Optimize TOC:** Пересмотреть лимит итераций в `parse_toc` или оптимизировать поиск.
4.  [ ] **Unified Interface:** Полностью вытеснить Creoson из пайплайна.

**Последнее обновление:** 06.10.2026 (Анализ прорыве и граблей завершен).
