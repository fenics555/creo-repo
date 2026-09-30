@echo off
rem sync_clinerules.bat - keep the GitHub copy of the Cline rules equal to the master.
rem MASTER : D:\AI\.clinerules        (the real one, edited by the owner)
rem COPY   : D:\AI\repo\.clinerules   (lives in the creo-repo GitHub repo)
rem Copies only when bytes differ; safe to run anytime. Keep this file ASCII-only.
setlocal
set "MASTER=D:\AI\.clinerules"
set "COPY=D:\AI\repo\.clinerules"
set "SLOG=D:\AI\tools\agent\data\clinerules_sync.log"
if not exist "%MASTER%" (
  echo master rules missing: %MASTER%
  exit /b 1
)
fc /b "%MASTER%" "%COPY%" >nul 2>&1
if not errorlevel 1 (
  echo %date% %time% already in sync >> "%SLOG%"
  echo clinerules: already in sync
  exit /b 0
)
copy /Y "%MASTER%" "%COPY%" >nul
if errorlevel 1 (
  echo %date% %time% copy failed >> "%SLOG%"
  echo clinerules: copy failed
  exit /b 1
)
echo ===== %date% %time% ===== synced from master >> "%SLOG%"
echo clinerules: synced from master
exit /b 0
