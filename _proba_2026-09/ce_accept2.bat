@echo off
call "D:\AI\tools\agent\creo_export\creo_export.bat" pdf "D:\AI\PROBA\pdftest\뢠.drw" "D:\AI\PROBA\out" > "D:\AI\PROBA\ce_pdf6.txt" 2>&1
echo === DONE code=%ERRORLEVEL% === >> "D:\AI\PROBA\ce_pdf6.txt"