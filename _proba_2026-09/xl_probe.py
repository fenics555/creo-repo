# -*- coding: utf-8 -*-
"""Проба чтения XLSX модулем excel_import (для проверки окна просмотра)."""
import sys

sys.path.insert(0, r"D:\AI\tools\agent\excel")
import excel_import as i  # noqa: E402

FILES = [
    r"Z:\PTC\CREO-START\НАСТРОЙКИ\bend_tables\Коэффициенты_гибки.xlsx",
    r"Z:\PTC\CREO-START\НАСТРОЙКИ\ТАБЛИЦА_ОТВЕРСТИЙ\DIN\6698\DIN_6698_отверстия_с_велосипедной_резьбой.xlsx",
]
for f in FILES:
    try:
        d = open(f, "rb").read()
    except Exception as e:
        print("нет файла: %s (%s)" % (f, e))
        continue
    try:
        sections, rows = i.read_specification_xlsx(d)
        print("ПРОЧИТАНО: %s | разделов %d, строк %d" % (f.split("\\")[-1], len(sections), len(rows)))
        if rows:
            print("   первая строка: %s" % rows[0])
    except Exception as e:
        print("ЧЕСТНАЯ ОШИБКА на %s: %s" % (f.split("\\")[-1], e))