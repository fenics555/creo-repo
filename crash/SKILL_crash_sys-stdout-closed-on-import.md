---
name: crash_sys-stdout-closed-on-import
system: CRASH
description: Use when: проба падает с «ValueError: I/O operation on closed file» — модуль при импорте переназначил sys.stdout обёрткой TextIOWrapper
when: I/O operation on closed file, TextIOWrapper, sys.stdout, импорт модуля, проба, вика, ошибка вывода
date: 03.10.2026
executor: Cline
task: ПРОЕКТ_ОБНОВЛЕНИЕ_АГЕНТА, волны 3 и 5 — блоки hol_tools и checks_tools
---

ОШИБКА (дословно, для grep):
ValueError: I/O operation on closed file.
СИМПТОМ: проба падает, печатая первую же строку `ok(...)`. При этом в коде модуля есть
`sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")`
на уровне модуля (а не внутри `if __name__ == "__main__":`).
ПРИЧИНА (факт): проба сама обернула stdout в TextIOWrapper при старте. Модуль при импорте
обернул его ВТОРЫМ TextIOWrapper. Старая обёртка пришла в GC и закрыла поток, на котором
работала новая, — `print` упал. Повторилось дважды за проект (волны 3 и 5), значит это
не случайность, а закономерность.
ПРОФИЛАКТИКА:
1. **Модуль, который импортируют пробы (блоки `*_tools.py`, окна), НЕ трогает `sys.stdout`
   при импорте.** Обёртка ставится только внутри `if __name__ == "__main__":`.
2. Если обёртка нужна всегда — она обязана проверять, не обёрнут ли поток:
   `if not isinstance(sys.stdout, io.TextIOWrapper): sys.stdout = …`.
3. Кириллица в консоли: обёртка нужна в `__main__` скриптов, которые печатают отчёт.
4. Симптом-подсказка: падает ПЕРВАЯ строка вывода и только при импорте из пробы —
   ищи переназначение `sys.stdout` в импортируемом модуле.
ПОВТОРЫ: 2