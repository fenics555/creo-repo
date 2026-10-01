---
name: crash_strict_test_stamp-missing
system: CRASH
description: Use when: проверка strict_test.py проходит все вопросы, но отчёт не пишется — NameError 'STAMP' is not defined
when: strict_test, stamp, NameError, report, checks, ollama
date: 01.10.2026
executor: Cline
task: проверка моделей после возврата дефолтов (01.10.2026)
---

ОШИБКА (дословно, для grep):
NameError: name 'STAMP' is not defined
СИМПТОМ: strict_test.py проходит все вопросы (progress.log полон, оба файла done), процесс завершается
без ошибки в консоли, но report_*.md и results_*.json НЕ появляются — падение на write_reports().
ПРИЧИНА: в checks\strict_test.py отсутствует объявление STAMP, а write_reports() его использует
(в verify_prompt_test.py и speed_check.py STAMP объявлен — там молчит).
ПРОФИЛАКТИКА:
1. После прогона тест-скрипта проверять НАЛИЧИЕ report_*.md/results_*.json, а не только progress.log.
2. STAMP объявлять в каждом скрипте, где он используется (единый шаблон шапки).
3. Исправлено 01.10.2026: STAMP добавлен в strict_test.py сразу после BASE/os.makedirs.
ПОВТОРЫ: 1
