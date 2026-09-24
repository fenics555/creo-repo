# -*- coding: utf-8 -*-
"""Проба: чем можно показать PDF в окне Tkinter на этой машине."""
import importlib
import shutil

LIBS = ["fitz", "pymupdf", "pypdfium2", "pdf2image", "PIL", "reportlab", "PyPDF2", "pypdf"]
print("=== python-библиотеки ===")
for m in LIBS:
    try:
        mod = importlib.import_module(m)
        print("   %-12s ЕСТЬ %s" % (m, getattr(mod, "__version__", "")))
    except Exception as e:
        print("   %-12s нет (%s)" % (m, type(e).__name__))

print("=== внешние программы ===")
for exe in ("gswin64c", "gswin32c", "pdftoppm", "pdftocairo", "mutool", "magick", "convert", "sumatrapdf", "AcroRd32"):
    p = shutil.which(exe)
    print("   %-12s %s" % (exe, p or "нет"))

print("=== чем открывается .pdf в системе ===")
try:
    import winreg
    k = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, r".pdf")
    print("   .pdf -> %s" % k)
    try:
        cmd = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, k + r"\shell\open\command")
        print("   команда: %s" % cmd)
    except Exception as e:
        print("   команда не прочитана: %s" % e)
except Exception as e:
    print("   реестр не прочитан: %s" % e)