---
name: plm-reader-commands
system: Команды
description: Use when: работа с PLM Reader (D:\AI\tools\agent\plm_reader): запуск, самопроверка, выпуск версии, CLI движка, грабли импорта
when: plm_reader, smoke, самопроверка, make_version_json, version.json, выпуск версии, APP_VERSION, манифест, engine.py, count, check, tree, changes, rename-plan, load_settings_file, circular import, folders, settings.json
date: 23.10.2026
priority: high
---

# PLM READER: ПОЛЕЗНЫЕ PYTHON-КОМАНДЫ

Полная рутина — README инструмента (`D:\AI\tools\agent\plm_reader\README.md`); здесь — быстрый вызов.

```powershell
cd D:\AI\tools\agent\plm_reader
python _smoke_v87.py                      # самопроверка без GUI-участия (граф + 5 секций GenealogyWindow)
python make_version_json.py "<notes>"     # пересобрать манифест (номер берётся из APP_VERSION в plm_reader.py)
python plm_reader.py                      # запуск окна (или plm_reader_gui.bat)
```

ВЫПУСК ВЕРСИИ — 3 обязательных шага (иначе шара обновление не увидит):
1. поднять `APP_VERSION` в `plm_reader.py`;
2. `python make_version_json.py "<кратко что нового>"`;
3. git push вместе с `version.json` (git — по `SKILL_parallel_legs.md`: только адресный `git add -- <пути>`).

ПРИЁМКА: `python _smoke_v87.py` → последняя строка `SMOKE OK`.
ГРАБЛИ: smoke устойчив к cp1251; GUI-часть проверяется программно (без дисплея) — визуал смотрит
человек. **Шара `Z:` агентами НЕ трогается** (закон владельца 14.10.2026) — `Powershell\SKILL_plm_reader_sync.md`.

---

## CLI ПРОГРАММЫ (проверено живым прогоном 23.10.2026)

Два модуля со своими аргументами:

```powershell
cd D:\AI\tools\agent\plm_reader

# движок: чтение базы / проверки (код 0 на всех, кроме tree с -n)
python engine.py count                     # 5610 моделей · связей 24820 · деталей 44609 · 0.5 с
python engine.py check                     # лежачих 23052 · правленых 41877 · 4 счёта
python engine.py where <имя>               # где лежит модель
python engine.py changes --n 5             # история изменений
python engine.py tree --depth 1            # дерево (⚠ -n НЕ принимает, см. грабли)
python engine.py rename-plan --n 3         # сухой план переименования
python engine.py count --full              # полный пересчёт

python plm_reader.py --help                # без окна: --folder --csv --max-mb --no-recurse --history --history-csv
```

## ГРАБЛИ CLI И ИМПОРТА (найдены аудитом 23.10.2026)

1. **`tree` не принимает `-n`.** `python engine.py tree --depth 1 -n 5` →
   `error: unrecognized arguments: -n` (код 2), хотя `--n` объявлен и у `changes` работает.
   **Обход:** для `tree` брать `--depth` и `-n` не передавать.
2. **Кириллица в выводе CLI при редиректе — мусор** (`?????? ?????: ????? 5610`).
   Это НЕ порча данных: запись/чтение UTF-8 верны; ломается только печать при перенаправлении.
   **Обход:** читать вывод как UTF-8 (`reconfigure`) или проверять числа, а не слова.
3. **Циклический импорт `plm_settings` ↔ `plm_reader`.** Внешний скрипт, импортирующий
   `plm_settings` **первым**, падает: `ImportError: cannot import name 'CURRENT_SETTINGS_VERSION'
   from partially initialized module 'plm_settings' (circular import)`.
   **Обход:** сначала `import plm_reader` (он регистрирует себя в `sys.modules`), затем `plm_settings`.
4. **`load_settings_file()` ПИШЕТ, а не только читает.** Функция переносит/архивирует старые файлы
   настроек (и правит живой `settings.json`). **Никогда не звать её из пробы по живому каталогу** —
   только на копии в изоляции. Живой факт 23.10.2026: проба перезаписала рабочие папки скана
   тестовыми значениями. Подробно — `repo\SKILL_edit_gotchas.md` §18.
5. **`folders`/`exclude` не приводятся к списку.** Если в файле настроек они строкой
   (`"Z:\A; Z:\B"`), программа примет строку как есть (в отличие от `db_mirror`, который чинится
   миграцией v2→v3). Проверять тип после правки файла вручную.

## ЧИСЛА БАЗЫ (на 23.10.2026, активная `plm_reader_20261002_160609.db`)

```
snapshots 46756 | links 24877 | derived 21187 | changes 122968 | folders 5590
mtime заполнен у 46756 (100%); created у 45653 (97.6%); seen — 18 меток скана
последняя правка файла на складе: 02.10.2026 16:05
правленых: месяц 931 · 3 мес 3167 · полгода 5542 · год 11432 · все 46756
новых (created): месяц 854 · 3 мес 1769 · полгода 3282 · год 45653
```
⚠️ «день» и «неделя» = **0**: склад не обновлялся 21 день. Это факт о складе, не дефект.
