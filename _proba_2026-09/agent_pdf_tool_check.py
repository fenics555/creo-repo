# -*- coding: utf-8 -*-
"""Проверка нового блока creo_pdf_tools: скан боевой папки через реестр агента (руками)."""
import sys
sys.path.insert(0, r"D:\AI\tools\agent")
import tools_registry as TR

print("блоков: %d | инструментов: %d" % (len(TR.BLOCKS), len(TR.TOOLS)))
print("creo_pdf_tools в реестре:", "ДА" if "creo_pdf_tools" in TR.BLOCKS else "НЕТ")
for n in ("creo_pdf_scan", "creo_pdf_export"):
    t = TR.get(n)
    print("  %-18s %s%s" % (n, "есть" if t else "НЕТ", " [СОГЛАСОВАНИЕ]" if t and t.get("approval") else ""))

print("-" * 74)
print("ПРОБА скана боевой папки (без Creo):")
r = TR.execute("creo_pdf_scan", {"folder": r"Z:\PTC\Work\000_01 Пользовательские изделия\Болты Винты"})
print(str(r)[:900])