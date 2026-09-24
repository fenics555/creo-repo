@echo off
rem Приёмка creo_export через окно-обёртку (полный путь к движку + вывод в файл).
call "D:\AI\tools\agent\creo_export\creo_export.bat" pdf "D:\AI\PROBA\mfgtest\d25.prt" "D:\AI\PROBA\out" > "D:\AI\PROBA\ce_pdf4.txt" 2>&1
echo === DONE code=%ERRORLEVEL% === >> "D:\AI\PROBA\ce_pdf3.txt"