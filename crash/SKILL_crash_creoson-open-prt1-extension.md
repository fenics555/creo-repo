---
name: crash_creoson-open-prt1-extension
system: CRASH
description: Use when: CREOSON file:open отвечает "Unknown Model Extension" при верном существующем пути — обычно передан путь с расширением .prt.1 вместо .prt
when: CREOSON, file:open, Unknown Model Extension, prt.1, extension, .asm.1, prt.2, существование файла
date: 04.10.2026
executor: Cline
task: блицкриг — прогон blitz_final.py по 137_011_0041 после провала по is-10_001_001_003
---

ОШИБКА (дословно, для grep):
  {"status": {"error": true, "message": "Error: Unknown Model Extension"}, "data": null}

СИМПТОМ: `file:open` возвращает `Unknown Model Extension`. Файл существует, путь абсолютный,
папка в `search.pro` есть. Скрипт открывает файл на диске нормально (`open().read()` — работает).

ПРИЧИНА: ФАКТ — путь в `file:open` должен оканчиваться на `.prt`, а НЕ на `.prt.1`.
Файлы Creo на диске хранятся как `имя.prt.1`, `имя.prt.2` (ревизии), но API оперирует
именем **без номера ревизии**: `имя.prt`.

ПРОФИЛАКТИКА:
1. Собирать путь один раз: `MODEL = r'...\name.prt.1'` для чтения байтов с диска
   и `F = MODEL[:-2]` для `file:open`. Не путать эти два.
2. Для `.asm` действует то же правило: `имя.asm.1` → `имя.asm`.
3. `Unknown Model Extension` НЕ означает, что модель не открывается, — сначала проверить `.1` на конце.
4. Ранее этот отказ был ошибочно записан как «внутренний конфликт сессии»
   (см. `crash_creoson-search-pro-visibility`, ПОВТОРЫ 2).

ПОВТОРЫ: 1 (04.10.2026 — `137_011_0041`; потеряно ~4 запуска подряд
на ложной диагностике «модель заблокирована»)