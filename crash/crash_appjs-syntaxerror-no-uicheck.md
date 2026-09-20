# CRASH: appjs-syntaxerror-no-uicheck

ОШИБКА: `app.js:125 Uncaught SyntaxError: missing ) after argument list`

ПОВТОРЫ: 1

ПРОФИЛАКТИКА: после КАЖДОЙ правки app.js или index.html нога гоняет dev\ui_check.py и цитует чистую консоль ДО отчёта о фазе; правка интерфейса без пробы консоли = нарушение.

[2026-09-20 14:40:36] ������ +1. ���������� �������������� ������ � app.js ����� �����.
