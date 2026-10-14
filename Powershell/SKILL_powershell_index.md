---
name: powershell-index
system: Команды
description: Use when: задача про PowerShell-команды/скрипты дома (.ps1, синхронизация, шара, ExecutionPolicy)
when: powershell, ps1, .ps1, ExecutionPolicy, Bypass, NoProfile, синхронизация, шара, sync_to_share, sync_check, грабли powershell
date: 14.10.2026
---

ЧТО ЗДЕСЬ (папка `D:\AI\repo\Powershell`, создана 14.10.2026):
- `SKILL_powershell_index.md` — этот вход направления;
- `SKILL_ps51_gotchas.md` (**high**) — грабли PowerShell 5.1 дома: кириллица в UTF-8 ломает скрипт
  (решение — ASCII-only), запуск через `-NoProfile -ExecutionPolicy Bypass`;
- `SKILL_plm_reader_sync.md` (**high**) — рутина PLM Reader: выгрузка кода на шару и сверка D: ↔ Z:.

Это **ШПАРГАЛКА КОМАНД**: что запустить, что увидеть, какие грабли. Стандарты кода и тестирования —
в `Prog\`; универсальный закон — `MANIFEST.md`; git — `SKILL_parallel_legs.md`.

КОГДА ОТКРЫВАТЬ: «синхронизировать», «на шару», «.ps1 не запускается», «ExecutionPolicy»,
«кириллица в скрипте».
КОГДА ПИСАТЬ: в работе нашлась полезная PowerShell-команда или скрипт — дописывай тело скилла
по теме; новая тема = новый `SKILL_<тема>.md` + строка в этот вход. Вход правится только при
смене состава папки. Дополнять параллельно с работой — не откладывать.
