---
name: plm-reader-commands
system: Команды
description: Use when: работа с PLM Reader (D:\AI\tools\agent\plm_reader): запуск, самопроверка, выпуск версии
when: plm_reader, smoke, самопроверка, make_version_json, version.json, выпуск версии, APP_VERSION, манифест
date: 14.10.2026
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
человек. Синхронизация с шарой — `Powershell\SKILL_plm_reader_sync.md`.
