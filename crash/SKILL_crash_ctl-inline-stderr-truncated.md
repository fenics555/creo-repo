name: crash_ctl-inline-stderr-truncated
system: CRASH
description: Use when: рестарт или проба агента через инлайн python -c в PowerShell гибнет
с кодом 1, stderr обрезан на границе кодека, выходной файл пуст
when: ctl, restart, python -c, inline, stderr truncated, ParseException, handlers/ctl
date: 17.09.2026
executor: Cline (solar-pro4)
task: спека 57 фаза 0, рестарт агента
СЧЁТЧИК ПОВТОРОВ: 1
ОШИБКА (дословно, для grep):
[Command exited with code 1]; python : Traceback (most recent call last): — stderr обрезан;
restart.out пуст; ParseException на эскейпах [\' ... \'] в PowerShell.
СИМПТОМ: инлайн-запуск python -X utf8 -c "..." с юникодом или эскейпами через PowerShell
гибнет или теряет вывод; выходной файл пуст; исполнитель не видит строку ошибки и
повторяет попытку по неверному пути (handlers/ctl.py вместо живого D:\AI\tools\agent\ctl.py).
ПРИЧИНА: два нарушения разом: (1) правило 13.10 — питон-код в командной строке оболочки,
консольный кодек обрезал stderr; (2) правила 2.4/2.5 — путь к ctl.py из памяти, а не из
живой цитаты dir/Get-ChildItem.
ЛЕЧЕНИЕ (проверено): рестарт агента только через батник: cmd /c D:\AI\tools\agent\AI_RESTART.bat
либо Set-Location D:\AI\tools\agent и python ctl.py up из .py-файла, никогда не -c;
приёмка — NEW_PID через Get-NetTCPConnection -LocalPort 8765 и StartTime процесса.
ПРОФИЛАКТИКА:
1. Питон-код живёт только в .py-файлах (13.10); запуск cmd /c "python -X utf8 file.py > out 2>&1",
чтение вывода Get-Content -Encoding utf8.
2. Любой путь — из живой цитаты (Get-ChildItem, dir), не из памяти (2.4/2.5).
3. Verbatim-русский контент входит в файлы ТОЛЬКО через write_file/editor (10.13);
\uXXXX-эскейпы нужны лишь пробным скриптам, идущим через консоль, но НЕ содержимому
файлов, которые пишет редакторный инструмент. Перестраховка эскейпами там, где нужен
прямой write_file, и рождает плейсхолдеры «ХХХХ вместо слов».
4. Увидел обрезанный stderr — не повторяй попытку вслепую: выведи вывод в файл и прочитай
его Get-Content (13.10).
5. Рестарт агента: pid-файл живёт в `core.BASE\agent\agent.pid` (то есть
   `D:\AI\tools\agent\agent.pid`), а НЕ в `data\agent.pid`; приёмка рестарта — смена PID
   (`Get-NetTCPConnection -LocalPort 8765`) и StartTime процесса позже mtime правленого файла;
   сторож и ночной цикл живут в `sched.py`, голова и щит согласований — в `loop.py`
   (распил агента по спеке 71, фазы Ф3/Ф4 ещё открыты).
ПОВТОРЫ: 1