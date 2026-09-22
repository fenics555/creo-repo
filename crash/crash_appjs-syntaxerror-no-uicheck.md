name: crash_appjs-syntaxerror-no-uicheck
system: CRASH
description: Use when: правка app.js/index.html ушла без пробы консоли — синтаксическая ошибка живёт до первой проверки
when: appjs, syntaxerror, ui_check, console, javascript
date: 20.09.2026
executor: Cline
task: правка app.js витрины

# CRASH: appjs-syntaxerror-no-uicheck

ОШИБКА: `app.js:125 Uncaught SyntaxError: missing ) after argument list`

ПОВТОРЫ: 2

ПРОФИЛАКТИКА: после КАЖДОЙ правки app.js или index.html нога гоняет dev\ui_check.py и цитует чистую консоль ДО отчёта о фазе; правка интерфейса без пробы консоли = нарушение.

[2026-09-20 14:40:36] ������ +1. ���������� �������������� ������ � app.js ����� �����.

Профилактика: битую строку в JS править заменой ЦЕЛИКОМ, а не добавлением отдельных скобок; после правки пересчитать баланс скобок ДО ui_check
