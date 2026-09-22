---
name: errors
system: общее
description: Use when: ошибка, сбой, ERR, Traceback, «не работает» — карта базы ошибок и правила добавления
when: ошибка error err traceback сбой лечение неисправность
priority: high
---
# БАЗА ОШИБОК (карта папки Ошибки/)

Папка `Ошибки/` — единственный дом разобранных ошибок.
Каждая разобранная ошибка = файл `ERR_ГГММДД_имя.md` + строка в карте ниже.

## Как пользоваться
1. При ERR/Traceback сначала ищи по тексту ошибки здесь и через `search_kb`.
2. Нашёл — применяй «лечение» из ERR-файла, не изобретай заново.
3. Разобрал новую ошибку — создай ERR-файл и добавь строку в карту.

## Карта
| Файл | Симптом | Суть | Лечение / правило |
|---|---|---|---|
| ERR_260819_stdlib_code.md | блок «загрузился», но первая команда даёт AttributeError | имя блока совпало с модулем стандартной библиотеки Python (`code`) | блоки НЕ называть именами stdlib (code, json, random, mail, types, time, os, re, sys, math); проверять до создания файла |
| ERR_creoson_write_ops.md | backup: «No 'target_dir' parameter given»; rename: Pro/TOOLKIT General Error | async CREOSON: backup требует `target_dir`; у `file:rename` падает ДИСКОВЫЙ вызов, а параметра `rename_dependencies` в API нет | backup: `{"file":…, "target_dir":…}`; rename: `{file,new_name,onlysession:true}` → `file:save` (диск получает новое имя), старые версии — в backup; подробности: Creo/CREOSON/SKILL_creoson_rename_mechanism.md |

## Правила ERR-файла
- Имя: `ERR_ГГММДД_короткое_имя.md`.
- Внутри: СИМПТОМ / ПРИЧИНА / ЛЕЧЕНИЕ / ПРАВИЛО НА БУДУЩЕЕ.
- Статус в шапке: «ПРАВИЛО (не повторять)» или «ЛЕЧЕНИЕ (применять)».
- Непроверенное лечение помечать «гипотеза» до подтверждения тестом.