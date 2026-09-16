name: crash-runcommands-copy-race-fake-parameter
system: CRASH
description: Use when: после Copy-Item мгновенный Get-Content падает PathNotFound (гонка
записи и чтения), либо Get-Content с параметром -LineNumber падает NamedParameterNotFound
(такого параметра у Get-Content не существует)
when: run_commands, Copy-Item, Get-Content, race, PathNotFound, NamedParameterNotFound,
LineNumber, fake-parameter, PowerShell
date: 17.09.2026
executor: Cline (solar-pro4)
task: спека 60, бекап scanner.py и правка EXTS
СЧЁТЧИК ПОВТОРОВ: 1
ОШИБКА (дословно, для grep):
Get-Content : Не удается найти путь "D:\AI\tools\agent\data\backup\pre_scan_drw_scanner.py.bak",
так как он не существует.
Get-Content : Не удается найти параметр, соответствующий имени параметра "LineNumber".
СИМПТОМ: в одной пачке run_commands Copy-Item возвращает success, но следующий за ним
Get-Content того же файла падает PathNotFound (файл ещё не закрыт и не дописан);
одновременно Get-Content с -LineNumber падает NamedParameterNotFound, потому что такого
параметра у командлета нет вовсе.
ПРИЧИНА:
1. Гонка записи и чтения: файловая операция ещё не отпущена дескриптором, а чтение уже
стучится по пути; success у Copy-Item не означает «файл готов к чтению».
2. Факт о параметре взят из памяти, а не из живой цитаты (нарушение 2.5): у Get-Content
есть -TotalCount, -First, -Last, -Encoding, -Tail; -LineNumber принадлежит Select-String
и нумерацию строк даёт только он либо read_files со start_line/end_line.
ЛЕЧЕНИЕ (проверено):
1. После Copy-Item перед чтением: Test-Path или Get-Item по факту существования, при нужде
Start-Sleep 1-2; не читать файл в той же пачке команд, что его породила.
2. Вместо -LineNumber у Get-Content: -TotalCount N или -Tail N; строки с номерами —
Select-String -Pattern с контекстом; диапазоны кода — read_files start_line/end_line.
ПРОФИЛАКТИКА:
1. Команда, породившая файл, и команда, читающая его, не живут в одной пачке run_commands.
2. Перед применением любого параметра командлета — живая цитата Get-Help или Get-Command,
никогда память (2.5).
3. Падение PathNotFound сразу после успешной записи = сначала гонка, потом всё остальное.