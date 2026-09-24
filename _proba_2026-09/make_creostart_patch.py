# -*- coding: utf-8 -*-
"""Готовим патч Z:\\PTC\\CREO-START\\START-STD\\CREO-START.bat: CREOSON убирается из автозапуска.
Z: только для чтения — патч кладём в D:\\AI\\PROBA\\CREO-START.bat (затем копирует человек)."""
import os, difflib

SRC = r"Z:\PTC\CREO-START\START-STD\CREO-START.bat"
DST = r"D:\AI\PROBA\CREO-START.bat"

old_block = [
    'if not exist "%CREOSON_BAT%" goto SRV_CREOSON_SKIP',
    'netstat -ano | findstr ":8080" | findstr "LISTENING" >nul && goto SRV_CREOSON_UP',
    'echo %time% start CREOSON >> "%LOGF%"',
    'start "" /B cmd /S /c "cd /d "%LOCAL%\\creoson" && creoson_run.bat >>"%STD%\\logs\\creoson.log" 2>&1"',
    'goto SRV_CREOSON_UP',
    ':SRV_CREOSON_SKIP',
    'echo %time% CREOSON not installed - skip >> "%LOGF%"',
    'if "%DEBUG%"=="1" echo CREOSON not installed - skip',
]

new_block = [
    'rem --- CREOSON УБРАН ИЗ АВТОЗАПУСКА 23.09.2026 ---',
    'rem Он нужен только блокам агента на creo_call и поднимается по требованию самим агентом',
    'rem (_ensure_creoson в creo_tools.py). Вернуть автозапуск: раскомментировать строки ниже.',
    'rem if not exist "%CREOSON_BAT%" goto SRV_CREOSON_SKIP',
    'rem netstat -ano | findstr ":8080" | findstr "LISTENING" >nul && goto SRV_CREOSON_UP',
    'rem echo %time% start CREOSON >> "%LOGF%"',
    'rem start "" /B cmd /S /c "cd /d "%LOCAL%\\creoson" && creoson_run.bat >>"%STD%\\logs\\creoson.log" 2>&1"',
    'rem goto SRV_CREOSON_UP',
    'rem :SRV_CREOSON_SKIP',
    'rem echo %time% CREOSON not installed - skip >> "%LOGF%"',
    'rem if "%DEBUG%"=="1" echo CREOSON not installed - skip',
]

src = open(SRC, encoding="utf-8", errors="ignore").read().replace("\r\n", "\n").split("\n")
print("строк в исходнике:", len(src))
print("меток SRV_CREOSON в файле:", sum(1 for l in src if "SRV_CREOSON" in l))

out, done = [], False
i = 0
while i < len(src):
    if not done and src[i].strip() == old_block[0]:
        block = [x.strip() for x in src[i:i + len(old_block)]]
        if block == [x.strip() for x in old_block]:
            out.extend(new_block)
            i += len(old_block)
            done = True
            continue
    out.append(src[i])
    i += 1
print("блок заменён:", done)
open(DST, "w", encoding="utf-8", newline="\r\n").write("\n".join(out))
print("патч записан:", DST, os.path.getsize(DST), "байт")

print("\n--- diff ---")
for line in difflib.unified_diff(src, out, "Z:CREO-START.bat", "патч", lineterm="", n=1):
    print(line[:150])