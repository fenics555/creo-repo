name: crash_editor-text-not-found
system: CRASH
description: Use when: editor не находит точный old_text, хотя при чтении текст совпадает
when: editor, text-not-found, mismatch
date: 16.09.2026
executor: Cline
task: СПЕКА 64, ШАГ 2
ОШИБКА (дословно, для grep):
Editor operation failed: No replacement performed: text not found in D:\AI\tools\agent\ui\app.js.
СИМПТОМ: Инструмент editor сообщает, что текст не найден, хотя при чтении файла он идентичен.
ПРИЧИНА: Вероятное расхождение в невидимых символах (CRLF vs LF) или специфическая обработка многострочных блоков в инструменте.
ПРОФИЛАКТИКА:
1. Использовать более короткие якоря (anchors).
2. Использовать insert_line вместо замены больших блоков.
3. Использовать py_compile для проверки.
ПОВТОРЫ: 1
