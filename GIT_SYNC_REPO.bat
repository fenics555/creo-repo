@echo off
rem GIT_SYNC_REPO.bat - autosave for D:\AI\repo (GitHub: creo-repo)
rem Usage: GIT_SYNC_REPO.bat ["commit message"]   (default: autosave repo <date> <time>)
rem Sibling of GIT_SYNC.bat which covers D:\AI\tools only. Log lives in agent\data (never committed).
set "ROOT=D:\AI\repo"
set "SLOG=D:\AI\tools\agent\data\git_sync_repo.log"
set "MSG=%~1"
if "%MSG%"=="" set "MSG=autosave repo %date% %time%"
cd /d "%ROOT%"
echo ===== %date% %time% ===== >> "%SLOG%"
echo message: %MSG% >> "%SLOG%"
git add -A
git diff --cached --quiet
if %errorlevel% equ 0 echo nothing to commit, working tree clean >> "%SLOG%"
if %errorlevel% equ 0 exit /b 0
git commit -m "%MSG%" >> "%SLOG%" 2>&1
if %errorlevel% neq 0 exit /b %errorlevel%
git push origin master >> "%SLOG%" 2>&1
exit /b %errorlevel%
