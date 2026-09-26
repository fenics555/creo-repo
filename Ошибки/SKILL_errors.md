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
| ERR_260902_web_fetch.md | часть «не открылось»: кириллические URL падали с UnicodeEncodeError; r.jina.ai без ключа 403 и молча сливался | urllib не кодирует URL сам; прокси требует ключ | всегда `quote(url)`; fallback-цепочка (direct→allorigins→jina(ключ)→playwright) с явными статусами; вердикт «антибот» только при 401/403/498 от цели |
| ERR_creoson.md | Creo/CREOSON/агент: rename «A Pro/TOOLKIT error has occurred: General Error»; backup «No 'target_dir' parameter given»; file:save записал НЕ ту модель; «File '…' was not open» | база знаний причин и проверенного лечения по CREOSON (порт 8080), разделы 1.1–1.8 | искать по фрагменту текста ошибки; лечение из разделов; непроверенное помечать «гипотеза» |

## Правила ERR-файла
- Имя: `ERR_ГГММДД_короткое_имя.md`.
- Внутри: СИМПТОМ / ПРИЧИНА / ЛЕЧЕНИЕ / ПРАВИЛО НА БУДУЩЕЕ.
- Статус в шапке: «ПРАВИЛО (не повторять)» или «ЛЕЧЕНИЕ (применять)».
- Непроверенное лечение помечать «гипотеза» до подтверждения тестом.