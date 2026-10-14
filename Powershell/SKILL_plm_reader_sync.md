---
name: plm-reader-sync
system: Команды
description: Use when: синхронизация PLM Reader D:\AI\tools\agent\plm_reader → шара Z:\PTC\CREO-START\plm_reader
when: plm_reader, синхронизация, шара, sync_to_share, sync_check, Z:, CREO-START, PTС, обновление на шаре, сверка копий
date: 14.10.2026
priority: high
---

# PLM READER: СИНХРОНИЗАЦИЯ КОПИИ НА ШАРЕ

Рабочая версия инструмента — **ТОЛЬКО** `D:\AI\tools\agent\plm_reader`. Шара
`Z:\PTC\CREO-START\plm_reader` обновляется командами ниже; отдельно живёт механизм обновления
из GitHub (кнопка «Проверить обновления», `version.json` → релиз) — его не путать с ручной
синхронизацией.

```powershell
cd D:\AI\tools\agent\plm_reader
powershell -ExecutionPolicy Bypass -File sync_to_share.ps1   # код на шару
powershell -ExecutionPolicy Bypass -File sync_check.ps1      # сверка D: ↔ Z: (расхождений быть не должно)
```

ПОРЯДОК после любых правок на D::
1. `python make_version_json.py "<notes>"` — пересобрать манифест (номер версии берётся из
   `APP_VERSION` в `plm_reader.py`);
2. `sync_to_share.ps1` — выгрузить код;
3. `sync_check.ps1` — приёмка сверкой.

ГРАБЛИ: оба скрипта обязаны быть **ASCII-only** — PS 5.1 + кириллица = крах парсинга
(см. `SKILL_ps51_gotchas.md`). Правки в код — только на D:, не на шаре.
Полная рутина выпуска версии — в README инструмента; этот скилл — только команды и порядок.
