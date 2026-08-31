---
name: err-stdlib-code
when: module code has no attribute handle, AttributeError, блок не работает, конфликт имени со стандартной библиотекой
source: [EMP] 19.08.2026, клиент server
---
# ОШИБКА: module 'code' has no attribute 'handle'

## Симптом
Блок «загрузился» без сообщения «не загружен», но первая же
команда даёт AttributeError.

## Причина
Файл блока назвали code.py - это имя модуля стандартной
библиотеки Python. __import__("code") нашёл стандартный модуль,
пока своего файла в папке не было.

## Лечение
Блок переименован в advisor.py; в agent.py строка импорта
заменена на code=_imp("advisor").

## Правило на будущее
Имена блоков НЕ должны совпадать со стандартной библиотекой:
code, json, random, mail, types, time, os, re, sys, math.
Проверять перед созданием файла.