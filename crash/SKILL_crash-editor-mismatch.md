name: crash-editor-mismatch
system: CRASH
description: Use when: editor падает с «text not found» из-за расхождения old_text после частичной правки или смены контекста
when: editor-mismatch, text not found, mismatch, old_text mismatch
date: 16.09.2026
executor: Cline (облако/локально)
task: правка PASSPORT.md (СПЕКА 44в)
ОШИБКА (дословно, для grep):
Editor operation failed: No replacement performed: text not found in [FILE]
СИМПТОМ: вызов editor возвращает ошибку вместо правки, хотя old_text, по мнению исполнителя, совпадает с состоянием файла.
ПРИЧИНА: old_text взят из прежнего состояния, а файл между вызовами изменился (предыдущая правка или insert_line), либо тонкие расхождения кодировки/экранирования.
ПРОФИЛАКТИКА:
1. Перед каждым вызовом editor — свежее чтение файла (read_files), чтобы old_text был актуальным.
2. Для больших файлов — проверить наличие якоря (findstr/Select-String) до замены.
3. Если расхождение держится — временный Python-скрипт с заменой по маркеру (Anchor Patch).
ПОВТОРЫ: 1