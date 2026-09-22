name: crash_editor_too_large_and_non_unique_anchors
system: CRASH
description: Use when: editor падает из-за размера файла > 6 КБ или нескольких совпадений old_text
when: editor, too_large, multiple_matches, non_unique_anchor
date: 20.09.2026
executor: Cline
task: frontend_integration_pdfrefresh
ОШИБКА (дословно, для grep):
Editor input too large: new_text was ... characters, exceeding the recommended limit of 6000.
СИМПТОМ: цикл неудачных вызовов editor или ошибка о нескольких совпадениях.
ПРИЧИНА: попытка переписать файл целиком через editor либо неуникальный old_text в файле с дублями.
ПРОФИЛАКТИКА:
1. Большие файлы — дробить правку на несколько вызовов мелкими кусками old_text/new_text.
2. Неуникальный текст — искать уникальные якоря (окружающие строки) или перезаписывать через run_commands.
3. Сильно повреждённый файл (дубли) — восстановить из последнего чистого коммита git и писать домовым каналом (один write_file до 8 КБ либо часть 1 + дописывание строго у последней строки); PowerShell Set-Content для файлов с кириллицей запрещён — консоль её не поддерживает.
ПОВТОРЫ: 1
