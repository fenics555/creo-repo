name: crash_deleted-house-file-without-word
system: CRASH
description: Use when: домовой файл (напр. harvest_gui.py) удалён вне data\tmp и data\backup без прямого слова пользователя
when: delete, harvest_gui, house-file, manual-deletion
date: 20.09.2026
executor: Cline
task: Spec 101 (harvest_gui.py)
ОШИБКА (дословно, для grep):
del harvest_gui.py
СИМПТОМ: Потеря домового файла в процессе работы (например, при попытке очистки или ошибки в команде).
ПРИЧИНА: Удаление файла без прямого слова пользователя в тексте задачи.
ПРОФИЛАКТИКА:
Восстановление из гита не сопровождается удалением никогда. Если файл мешает — сделай копию в .prev или data\\backup. Удаление домового файла — только по прямому слову пользователя.

ПОВТОРЫ: 1
