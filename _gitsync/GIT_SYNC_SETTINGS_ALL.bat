@echo off
rem GIT_SYNC_SETTINGS_ALL.bat - ONE updater: 3 pushes + rules/scripts copy.
rem   [1/5] D:\AI\repo           -> github.com/fenics555/creo-repo         (rules)
rem   [2/5] D:\AI\tools          -> github.com/fenics555/creo-agent        (code)
rem   [3/5] D:\AI\AGENT_SETTINGS -> github.com/fenics555/AI_AGENT_SETTINGS (stand)
rem   [0a/5] copy D:\AI\.clinerules -> D:\AI\repo\.clinerules  (before repo push)
rem   [0b/5] copy D:\AI\GIT_SYNC*.bat -> D:\AI\repo\_gitsync\  (backup on GitHub)
rem Usage: GIT_SYNC_SETTINGS_ALL.bat ["commit message"]
rem NOTE: keep plain ASCII/ANSI - UTF-16/UTF-8 cyrillic breaks cmd parsing.
setlocal
set "MSG=%~1"
echo ============================================================
echo  GIT SYNC ALL (repo + tools + settings)  %date% %time%
echo  message: %MSG%
echo ============================================================

echo [0a/5] sync .clinerules  =^>  repo ...
call "D:\AI\repo\sync_clinerules.bat"

echo [0b/5] sync GIT_SYNC scripts  =^>  repo\_gitsync ...
call "D:\AI\repo\sync_gitsync.bat"

echo [1/5] repo  - creo-repo ...
call "D:\AI\repo\GIT_SYNC_REPO.bat" "%MSG%"

echo [2/4] tools - creo-agent ...
call "D:\AI\tools\GIT_SYNC.bat" "%MSG%"

echo [3/4] settings - AI_AGENT_SETTINGS ...
call "D:\AI\AGENT_SETTINGS\GIT_SYNC_SETTINGS.bat" "%MSG%"

echo.
echo --- status: repo (creo-repo) ---
cd /d "D:\AI\repo"
git status -sb
git --no-pager log --oneline -1
echo --- status: tools (creo-agent) ---
cd /d "D:\AI\tools"
git status -sb
git --no-pager log --oneline -1
echo --- status: settings (AI_AGENT_SETTINGS) ---
cd /d "D:\AI\AGENT_SETTINGS"
git status -sb
git --no-pager log --oneline -1

echo.
echo Logs: D:\AI\tools\git_sync.log
echo       D:\AI\tools\agent\data\git_sync_repo.log
echo       D:\AI\tools\agent\data\git_sync_settings.log
echo       D:\AI\tools\agent\data\clinerules_sync.log
echo Note: if a parallel leg works at the same time, run "git add ^<files^>"
echo       manually instead - "add -A" would carry its unfinished work.
endlocal
