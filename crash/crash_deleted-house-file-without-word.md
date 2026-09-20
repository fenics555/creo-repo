name: crash_deleted-house-file-without-word
system: CRASH
description: Use when a home file (like harvest_gui.py) is deleted outside data\\tmp or data\\backup without direct user instruction.
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
