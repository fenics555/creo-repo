# -*- coding: utf-8 -*-
"""Проверка буфера обмена через tkinter (как кнопка «Копировать лог»).
Пишет результат В ФАЙЛ — потому что Tk нельзя гонять в неинтерактивном потоке."""
import tkinter as tk

OUT = r"D:\AI\PROBA\clip_test_result.txt"
res = []
try:
    r = tk.Tk()
    r.withdraw()
    sample = "ПРОВЕРКА БУФЕРА CREO PDF\nстрока 2\nстрока 3 " + "X" * 20
    r.clipboard_clear()
    r.clipboard_append(sample)
    r.update()
    try:
        back = r.clipboard_get()
    except Exception as e:
        back = "<ошибка чтения: %s>" % e
    res.append("положено символов: %d" % len(sample))
    res.append("прочитано: %r" % back[:50])
    res.append("ИТОГ: " + ("СОВПАДАЕТ — копирование работает" if back == sample else "НЕ СОВПАДАЕТ"))
    r.destroy()
except Exception as e:
    import traceback
    res.append("СБОЙ: %s" % e)
    res.append(traceback.format_exc())
open(OUT, "w", encoding="utf-8").write("\n".join(res) + "\n")