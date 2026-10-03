---
name: crash_creoson-open-keeps-other-model
system: CRASH
description: Use when: CREOSON file:open по полному пути не переключает окно — запись уходит в модель с тем же стемом (копия vs боевая)
when: CREOSON, file:open, get_active, onlysession, save ok no write, same stem, copy vs battle, parametr ushel v boevuyu model, RC 4 shield
date: 03.10.2026
executor: Cline
task: волна 7 (пакетные параметры, класс Ж) — живой прогон записи на копии
ОШИБКА (дословно, для grep):
  file:save ok=True {"status": {"error": false}, "data": null}   ← а файл на диске не изменился (mtime старый)
  file:get_active -> {"data": {"file": "din439.prt", "dirname": "Z:Z:/PTC/CREO-START/Libraries/Библиотека_стандартных_изделий/Гайки/"}}
СИМПТОМ: `parameter:set` отвечает «ok», `file:save` отвечает «ok», а файл НЕ меняется;
затем выясняется, что активна другая модель с тем же именем — запись ушла в неё.
ПРИЧИНА: ФАКТ — `file:open` с полным путём НЕ гарантирует, что откроется именно эта модель:
если в сессии уже открыта модель с тем же именем, активируется она (у нас — боевая из `Z:`,
а копия лежала в `D:\AI\PROBA\vol7_copy`). Имя совпадает, поэтому сверка «по имени»
проходила. Пути CREOSON отдаёт с удвоенным диском (`Z:Z:/...`).
ПРОФИЛАКТИКА:
1. ПЕРЕД любой записью сверять `file:get_active` по ПОЛНОМУ ПУТИ (имя + папка), а не по имени.
2. Путь нормализовать: слэши в `/`, убрать удвоенный диск (`Z:Z:` → `Z:`), снять регистр.
3. Сверка идёт по имени — этого НЕДОСТАТОЧНО: стен у боевой и копии одинаковый.
4. `file:open` полезно вызывать с `activate: true`, `display: true` (поля из
   `web\assets\creoson_stuff\creoson_js\creoson_file.js`), но это НЕ заменяет сверку.
5. Ответ сервера «ok» — НЕ доказательство записи. Доказательство — файл на диске
   (читать через `creo_read`/`facts`).
6. Уже встроено: `batch_params\apply.py::ensure_active()` → отказ RC 4 `wrong_active_model`.
   Живая проба: `python dev\shield_live.py`.
ПОВТОРЫ: 1 (03.10.2026 — создан щит; сам инцидент: 8 версий `din439.prt.2…9` в боевой папке,
оригинал `.1` не тронут)