---
---
name: creoson-probe-method
system: Creo/CREOSON
description: Use when: проба живого CREOSON — как строить запрос, три грабли подключения, что из команд существует
when: creoson, проба, probe, sessionId, connection/connect, feature/list, живой порт 8080, метод пробы направления
priority: critical
date: 03.10.2026
---
## 📡 ПРОТОКОЛ CREOSON — ВСКРЫТ ЭМПИРИЧЕСКИ (03.10.2026, живой порт 8080)

**Формат:** `POST http://127.0.0.1:8080/creoson`, тело JSON.

### ⚠️ ТРИ ГРАБЛИ, каждая проверена на живом сервере
1. **`sessionId` — ВЕРХНИМ УРОВНЕМ, НЕ внутри `data`.**
   `data:{"sessionId":…}` → `No session found`. Работает только так:
   ```json
   {"command":"creo","function":"pwd","sessionId":"8417750630383294508","data":{}}
   ```
2. **Сначала обязателен `connection/connect`** — он возвращает `sessionId`.
   Каждый POST **stateless**, ID надо передавать вручную в следующем запросе.
3. **JSON строить через `ConvertTo-Json`**, не склейкой строк — иначе
   `Invalid JSON input` (экранирование Windows-путей).

### Что работает / что существует
| Запрос | Результат |
|---|---|
| `connection`/`connect` | ✅ `{"error":false,"sessionId":"8417750630383294508"}` |
| `creo`/`pwd` | ✅ `Z:/PTC/CREO-START/START-STD/` |
| `feature`/`list` | ✅ существует, **требует ОТКРЫТОЙ модели** |
| `file`/`open` | ✅ существует (умеет открыть) |
| `file`/`retrieve`, `file`/`info`, `status`/`is_creo_running` | ❌ `Unknown …` |

### Правила для `feature:list`
| Правило | Следствие |
|---|---|
| путь **без суффикса версии** (`.prt`, не `.prt.1`) | иначе `Unknown Model Extension` |
| модель **должна быть уже открыта** в сессии | иначе `File '…' was not open` |
| `file:open` ищет относительно `Z:\PTC\CREO-START\START-STD\` | абсолютный путь на `D:` не находит |
| кириллица в пути портится | `2ÐºÐ°Ð¿` вместо `2кап` → JSON через UTF-8 bytes |

⚠️ **Итог 03.10.2026:** эталон через CREOSON **не получен** — модель на `D:`, а сессия
CREOSON сидит в каталоге `Z:\PTC\CREO-START\START-STD\`, и модель там не открыта.
**Дальше:** либо открыть модель через `file:open` с относительным именем в этом каталоге,
либо запустить CREOSON (`ctl.py up`) так, чтобы его рабочий каталог указывал на `D:\AI\PROBA`.

---
---
name: creoson_probe_method
system: Creo
description: Use when: живая проба механики CREOSON перед правкой кода или миграцией (гейт механизма)
when: проба, probe, гейт, CREOSON, сессия, копия, tmp, толькоsession
priority: high
---
# Проба в CREOSON: как не испортить рабочие модели (урок 16.09.2026)

## Источник правды о функциях
Локальная справка CREOSON: `D:\PTC\CREO-LOCAL-SETUP\creoson\web\`
- `functions.html` — браузер спецификаций всех функций (гарантированный пример запроса/ответа);
- `assets\creoson_stuff\jsonSpecs\*.json` — полный каталог параметров (по файлу на функцию);
- `start.html` — запуск и настройка: Creo обязан быть установлен **с JLINK**; порт рекомендован
  **9056**, а 22/80/**8080**/443 просят избегать. ФАКТ ДОМА: живём на 8080 вопреки рекомендации
  и это работает годами — менять только после пробы на всём флоте;
- `playground.html` — тестер функций из браузера;
- эндпоинты: `POST http://127.0.0.1:<port>/creoson` (JSON) и `/server`;
- `RELEASE_NOTES.txt`: **версия JRE зависит от версии Creo, а не от CREOSON.**
  Строки 13 и 5 дословно: «Made compatible with Creo 12 by changing the embedded JRE to
  Java 21» и «Made compatible with Creo 13 by changing the embedded JRE to Java 25».
  Значит: **Creo 12 → Java 21**, Creo 13 → Java 25. Дома стоит Creo 12.4.2.0, поэтому
  `JAVA_HOME` обязан указывать на **JRE 21** — живой факт 03.10.2026: на Temurin 25
  CREOSON падает (`EXCEPTION_ACCESS_VIOLATION`, `hs_err_pid*.log`), на JRE 11 —
  `UnsupportedClassVersionError ... class file version 65.0` (65 = Java 21), на
  **Temurin JRE 21.0.12.1+1 — работает**: `Starting server, listening on port 8080.`
  Текущее значение: `JAVA_HOME=D:\AI\Java21\jdk-21.0.12.1+1-jre` (бекап прежней
  строки — `setvars_pre_java11.bak`). **Версию JVM не угадывают — читают RELEASE_NOTES
  или ошибку запуска.**
- `setvars.bat` создаётся ТОЛЬКО `CreosonSetup.exe`; без него `creoson_run.bat` падает дословно
  «The setvars.bat file does not exist» (крах 17.09.2026; лечение: CreosonSetup.exe либо копия
  `setvars.bat` из старого каталога creoson).
Спек у каждой функции: `file-rename.json` подтверждает, какие параметры существуют,
а какие выдуманы (пример: `rename_dependencies` в CREOSON нет).

## Порядок пробы (обязателен)
1. Чистая сессия: `file:erase_not_displayed` + цикл `file:erase` по `file:list` →
   печатать `sess_start: []`. Одного `erase_not_displayed` НЕ хватает.
2. Проба идёт на КОПИИ **С ДРУГИМ ИМЕНЕМ** или в отдельной папке, но с проверкой:
   `file:open` по имени, уже загруженному в сессию, отдаёт модель **из памяти**;
   одноимённая копия в tmp не защищает — работа уйдёт в оригинал.
3. Сразу после `file:open` — `file:get_fileinfo` и сверка `dirname` с ожидаемой папкой.
4. Фиксировать до/после: список файлов папки, `file:list`, дословные ответы каждого вызова.
5. После пробы: выгрузить загруженное, убрать tmp, `creo:cd` вернуть в рабочую папку,
   в отчёте перечислить созданные файлы и оставшиеся следы.
6. Проба-гейт отвечает на ОДИН вопрос («работает / не работает / работает только так»),
   и от ответа зависит архитектура. Правку кода до гейта не начинать.

## Чем платят за нарушение
16.09.2026 пробы на «копиях» в tmp дали следы в рабочей папке CREOSON TESTS:
`creoson_tests-01.asm.1/.2/.3`, `creoson_tests-01-1_r1.prt.1/.2` — потому что модель
уже была в сессии, а `file:save` с несуществующим именем молча сохранил активную модель.
Итог: уборка только по слову пользователя; впредь — пункты 1-3 выше.
