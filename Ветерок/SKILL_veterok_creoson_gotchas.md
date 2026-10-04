---
name: veterok_creoson_gotchas
system: Ветерок
priority: critical
description: Use when: любая правка моделей Creo через CREOSON — грабли, найденные вживую 04.10.2026 (версии имён, активация, кэш, «ok» ≠ записано)
when: creoson, file:open, get_active, postregen, activate, display, модель не открывается, Unknown Model Extension
date: 04.10.2026
---

# ГРАБЛИ CREOSON ПРАВДЯТ МОДЕЛИ (живые, 04.10.2026)

Всё здесь проверено живыми пробами на боевой сборке `Z:\PTC\Work\00080` и на
копии в PROBA. Прежде чем писать в модель через CREOSON — прочитать этот файл.

## 1. ИМЯ МОДЕЛИ: БЕЗ НОМЕРА ВЕРСИИ
| На диске | Имя для Creo | Результат |
|---|---|---|
| `00080-03.asm.1` | `00080-03.asm.1` | **Error: Unknown Model Extension** |
| `00080-03.asm.1` | `00080-03.asm` | открывается, `revision: 1` |
| — | `00080-03` (без расширения) | Error: Invalid File Name |

Правило: имя = имя файла без хвостовых `.цифр`. Отсюда же: **маска `*.asm` по
полному имени файла не находит ничего** — сверять надо и с именем без версии.

## 2. АКТИВНАЯ МОДЕЛЬ: НУЖНО ОКНО
| Что сделали | `file:get_active` отдал |
|---|---|
| `open {display:false, activate:true}` | пустой `data` {} |
| `open {display:false}` + `file:display` | пустой `data` {} |
| `open {display:true, activate:true}` | **нужная модель** ✅ |

Правило: чтобы модель стала активной, её надо открыть **с `display:true`**
(тогда создаётся окно). Одного `activate:true` мало — это молча ловушка.

## 3. ОТКРЫТИЕ ИДЁТ ИЗ КЭША ПАМЯТИ, А НЕ ИЗ ПАПКИ
Если модель с тем же именем уже загружена из другой папки, `file:open` откроет
**ту** (в пробе — боевую из `Z:` вместо копии на `D:`). Запись ушла бы в боевую
модель. Порядок, который это снимает:
```
file:close_window {file: имя}      → убрать из окна
file:erase_not_displayed {}        → выгрузить из памяти
file:open {dirname, file, display:true, activate:true}
file:display {file: имя}
```
И ОБЯЗАТЕЛЬНО сверять `file:get_active` по полному пути (щит) — с учётом
того, что CREOSON отдаёт путь с удвоенным диском вида `D:D:/AI/...`.

## 4. «OK» ≠ ЗАПИСАНО НА ДИСК
`file:save` и `file:regenerate` отвечают `error:false` даже тогда, когда данные
не легли на диск (проверено на пострегенерации: снялось в памяти, на диске
вернулось). Правило дома, теперь обязательное для любой записи: **приёмка
только чтением с диска** — выгрузить модель из памяти (`close_window` +
`erase_not_displayed`) и прочитать заново.

## 5. ЗАЩИТА И СИСТЕМНЫЕ ПАРАМЕТРЫ
- Системные параметры `PTC_*` удалить нельзя: «Could not delete parameter
  PTC_MASTER_MATERIAL». Это ограничение Creo — программа обязана говорить об
  этом честно, а не рапортовать «успех».
- Закрыт доступ к моделям на `Z:` — программы не должны туда писать; проверять
  по пути, а не по типу диска (см. `SKILL_veterok_postregen.md`, п. 6.5).

## 6. ГДЕ СПЕКИ И ПРОБЫ
- Спеки CREOSON (истина о параметрах вызовов):
  `D:\PTC\CREO-LOCAL-SETUP\creoson\web\assets\creoson_stuff\jsonSpecs\`;
- пробы этой главы: `D:\AI\tools\agent\probe_named_read.py`,
  `probe_activate.py`, `probe_seq.py`, `probe_where.py`, `probe_save_path.py`
  (результаты — рядом, `*_out.txt`).