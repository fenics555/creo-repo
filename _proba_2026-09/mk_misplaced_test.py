# -*- coding: utf-8 -*-
"""Тестовое дерево для проверки уборки смещённых PDF (в полигоне, не боевые папки)."""
import os, shutil

R = r"D:\AI\PROBA\misplaced_test"
if os.path.exists(R):
    shutil.rmtree(R)

def mk(d, name, text="PDF-заглушка"):
    os.makedirs(os.path.join(R, d), exist_ok=True)
    p = os.path.join(R, d, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text + " " + name)
    return p

# 1) дубль: правильная копия рядом с чертежом + лишняя в другой папке
mk("A_оправка", "x-оправка.drw.1", "чертёж")
mk("A_оправка", "x-оправка.pdf", "правильная копия")
mk("B_чужая", "x-оправка.pdf", "лишняя копия")
# 2) смещён: чертёж тут, PDF только в другой папке (нет копии рядом)
mk("C_кондуктор", "y-кондуктор.drw.1", "чертёж")
mk("D_другая", "y-кондуктор.pdf", "смещённая единственная копия")
# 3) документация: PDF без чертежа вообще
mk("E_док", "katalog_osnastki.pdf", "документация")
# 4) порядок: чертёж + PDF рядом, копий нет
mk("F_порядок", "z-плита.drw.1", "чертёж")
mk("F_порядок", "z-плита.pdf", "правильная копия")

print("тестовое дерево создано:", R)
for dp, dn, fn in os.walk(R):
    for n in sorted(fn):
        print("   %s" % os.path.join(dp, n).replace(R, "."))