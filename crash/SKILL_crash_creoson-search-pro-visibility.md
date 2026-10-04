---
name: crash_creoson-search-pro-visibility
system: CRASH
description: Use when: CREOSON отказывает в открытии модели из папки, которой нет в search.pro — ошибочно считается, что видимы только START-STD или 2 уровня
when: CREOSON, file:open, error true, search.pro, search_path_file, config.pro, видимость папок, START-STD, 2 уровня, Unknown Model Extension
date: 04.10.2026
executor: Cline
task: блицкриг по is-10_001_001_003 — поиск источников правды для DOUBLE
---

ОШИБКА (дословно, для grep):
  {"status": {"error": true, "message": "Error: Unknown Model Extension"}, "data": null}

СИМПТОМ: `file:open` возвращает `error: true` на вполне существующий файл `.prt`.
Ранее считалось, что причина в ограничении видимости (`START-STD` / «2 уровня папки»).

ПРИЧИНА: ФАКТ — Creo ищет модели по списку папок из `search.pro`, а не по абсолютному пути.
В `Z:\PTC\CREO-START\START-STD\config.pro` есть строка
`search_path_file Z:\PTC\Work/search.pro`. Это файл со списком из **4109 папок**
(3271 из них глубже 2 уровней). Если папки модели в списке нет — `file:open` откажет,
даже если файл существует и путь абсолютный.

ОПРОВЕРГНУТЫЕ ВЕРСИИ (проверено):
- «видны только файлы из START-STD» — НЕВЕРНО: открываются любые папки из `search.pro`;
- «видны только 2 уровня вложенности» — НЕВЕРНО: 3271 папка глубже 2 уровней.

ПРОФИЛАКТИКА:
1. Прежде чем искать причину отказа — проверять папку модели по membership в `search.pro`.
2. Пути читать из `Z:\PTC\Work\search.pro`, кавычки и пробелы учитывать (есть записи с кириллицей).
3. Рабочие копии моделей держать ВНУТРИ `Z:\PTC\Work` — иначе CREOSON их не увидит.
4. Второй по частоте источник ошибки — передавать путь с расширением `.prt.1`.
   Нужен путь БЕЗ `.1` (см. `crash_creoson-open-prt1-extension`).
5. `parametric.exe` запущен без `-p` → берётся дефолтный `config.pro` из `START-STD`.
   Проверить: `Get-CimInstance Win32_Process -Filter "Name='parametric.exe'"`.

ПОВТОРЫ: 2 (04.10.2026 — `is-10_001_001_003` и `137_011_0041`;
первый случай принят за «внутренний конфликт сессии», что было неверно)