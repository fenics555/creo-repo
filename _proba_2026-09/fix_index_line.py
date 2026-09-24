# -*- coding: utf-8 -*-
import re
p = r"D:\AI\repo\crash\SKILL_crash_index.md"
s = open(p, encoding="utf-8").read()
s = re.sub(r"^- `crash_deleted-house-file-without-word` — .*$",
           "- `crash_deleted-house-file-without-word` — Use when: домовой файл (напр. harvest_gui.py) "
           "удалён вне data\\tmp и data\\backup без прямого слова пользователя",
           s, flags=re.M)
open(p, "w", encoding="utf-8").write(s)
print("ok")