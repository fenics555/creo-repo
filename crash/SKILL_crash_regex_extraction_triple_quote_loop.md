name: regex_extraction_triple_quote_loop
system: CRASH
description: Infinite loop during regex-based extraction of triple-quoted code blocks in agent.py logic.
when: regex, extraction, loop, triple_quote, regex_extraction
date: 17.09.2026
executor: Cline
task: F2 (raspil agent.py)
ОШИБКА (дословно, для grep):
RECURSION_ERROR: maximum recursion depth exceeded in regex engine
СИМПТОМ: Агент зацикливается при обработке кода, CPU 100%, stdout не обновляется.
ПРИЧИНА: Неправильно сконструированный regex для поиска ```...``` в сложных вложенных структурах (triple-quote loop).
ПРОФИЛАКТИКА:
1. Использовать AST-извлечение (ast.parse) вместо регулярных выражений для границ функций и блоков кода.
2. Если используется regex, обязательно ограничивать глубину поиска или использовать нерекурсивные паттерны.
ПОВТОРЫ: 1
