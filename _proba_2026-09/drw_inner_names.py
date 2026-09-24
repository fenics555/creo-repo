# -*- coding: utf-8 -*-
"""Что внутри спорного чертежа: имена моделей, на которые он ссылается, и его собственное имя."""
import re, os

d = r"Z:\PTC\Work\000_05 Приспособления\Планшайбы на серьги"
for name in ("plshaiba-4", "plshaiba-5", "plshaiba-3-p2", "plshaiba-2-p1"):
    p = os.path.join(d, name + ".drw.1")
    if not os.path.exists(p):
        print(name, "— файла нет"); continue
    raw = open(p, "rb").read(400000)
    strs = set(re.findall(rb"[ -~]{4,40}", raw))
    low = sorted({s.decode("ascii", "ignore") for s in strs
                  if re.match(rb"(?i).*(plshaiba|\.prt|\.asm|\.frm|\.dtl).*", s)})
    print("=== %s === ссылки (первые 14):" % name)
    for s in low[:14]:
        print("   ", s)
    # есть ли внутри собственное имя?
    hit = [s for s in low if s.lower().startswith(name.lower())]
    print("   своё имя в файле:", hit[:5] if hit else "не найдено")