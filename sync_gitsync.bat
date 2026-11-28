@echo off
rem sync_gitsync.bat - keep GitHub copies of the house sync-scripts equal to the master.
rem MASTERs : D:\AI\GIT_SYNC_SETTINGS_ОЛЛ.bat   (root launcher: 3 pushes + rules copy)
rem           D:\AI\AGENT_SETTINGS\GIT_SYNC_SETTINGS.bat  (settings-repo autosave)
rem COPYs   : D:\AI\repo\_gitsync\*.bat  (live in the creo-repo GitHub repo)
rem Why: root files sit under D:\AI\.gitignore "/*" -> NOT in git and lost on rebuild.
rem      Copies here survive (creo-repo tracks them). Safe to run anytime.
rem NOTE: keep plain ASCII/ANSI - UTF-16/UTF-8 cyrillic breaks cmd parsing.
setlocal
set "DST=D:\AI\repo\_gitsync"
if not exist "%DST%" mkdir "%DST%"

call :one "D:\AI\GIT_SYNC_SETTINGS_ALL.bat" "%DST%\GIT_SYNC_SETTINGS_ALL.bat"
call :one "D:\AI\AGENT_SETTINGS\GIT_SYNC_SETTINGS.bat" "%DST%\GIT_SYNC_SETTINGS.bat"
call :one "D:\AI\tools\GIT_SYNC.bat" "%DST%\GIT_SYNC_tools.bat"
call :one "D:\AI\repo\GIT_SYNC_REPO.bat" "%DST%\GIT_SYNC_REPO.bat"
endlocal
exit /b 0

:one
set "SRC=%~1"
set "TGT=%~2"
if not exist "%SRC%" (
  echo gitsync: master missing: %SRC%
  exit /b 0
)
fc /b "%SRC%" "%TGT%" >nul 2>&1
if not errorlevel 1 (
  echo gitsync: already in sync: %TGT%
  exit /b 0
)
copy /Y "%SRC%" "%TGT%" >nul
if errorlevel 1 (
  echo gitsync: copy failed: %TGT%
  exit /b 1
)
echo gitsync: synced [%TGT%]
exit /b 0
