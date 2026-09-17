name: crash_pdf-roots-two-lists
system: CRASH
description: Поиск PDF пуст при живых парах в базе знаний (сравнение scan_roots и kb_roots)
when: pdf-search-empty, roots-mismatch, scan_roots
date: 16.09.2026
executor: Cline
task: СПЕКА 60
ОШИБКА (дословно, для grep):
None
СИМПТОМ: PDF-глаза показывают 0 пар, хотя файлы существуют в scan_roots и files.
ПРИЧИНА: В доме два списка корней с разной властью: scan_roots питает files, drift и пары, корни базы знаний питают чанки и search_kb; обратный симптом «поиск пуст при живых парах» = смотреть корни базы.
ПРОФИЛАКТИКА:
1. Использовать синхронную пробу (probe_idx.py) вместо /ask для диагностики.
2. Проверять наличие обоих списков корней в настройках (scan_roots) и kb_roots.txt.
3. Учитывать, что Popen /rescan глотает stderr — проверять синхронной пробой.
4. drift_check через /ask может таймаутиться — прямая db-проба надёжнее.
ПОВТОРЫ: 1
