# -*- coding: utf-8 -*-
"""Живая проба: состав сборки ИЗ СЕССИИ Creo через навигатор (creoson дома)."""
import sys

sys.path.insert(0, r"D:\AI\tools\agent\navigator")
import navigator as n  # noqa: E402

print("word-search «turn сборки»:")
for x in n.find_words("turn блок", only_asm=True, limit=4):
    print("   слов %d/%d  %s" % (x["words_hit"], x["words_all"], x["name"]))

for model in ("haas-bmt65-25x25-v1-01.asm.1", "d25.asm.1"):
    rows, err = n.bom_live(model)
    print("\nLIVE BOM %s -> %s" % (model, ("ошибка: " + str(err)) if err else ("позиций %d" % len(rows))))
    for x in (rows or [])[:10]:
        print("   %-10s %-40s путь: %s" % (x["kind"], x["name"], (x["path"] or "—")[:70]))