name: crash_editor_context_mismatch
system: CRASH
description: Use when editor fails due to text mismatch or size limits in large refactors.
when: editor, mismatch, large, text, too_large
date: 20.09.2026
executor: Cline
task: Implement Spec 101 (harvest_gui.py)
ОШИБКА (дословно, для grep):
Editor operation failed: No replacement performed: text not found in D:\AI\tools\agent\harvest_gui.py.
СИМПТОМ: Невозможность применить правки в файлах более 50-100 строк или при больших блоках замены.
ПРИЧИНА: Несоответствие якоря (old_text) или превышение лимита (6000 chars).
ПРОФИЛАКТИКА:
блок editor свыше 6 КБ запрещён; якорная правка с old_text не длиннее трёх строк; полная замена файла = один write_file по существующему пути (≤8 КБ) или write_file части 1 + дописывание у последней строки; insert_line по номерам строк ЗАПРЕЩЁН НАВСЕГДА (детские ошибки пункт 1); при text not found перечитать свежо и переякориться, второе несовпадение → полная перезапись; „write_file создаст новый файл" — ложь, write_file по существующему пути перезаписывает

ПОВТОРЫ: 2
