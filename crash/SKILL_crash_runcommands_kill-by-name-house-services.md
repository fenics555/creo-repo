name: crash_runcommands_kill-by-name-house-services
system: CRASH
description: Use when: остановка процесса по ИМЕНИ (Stop-Process -Name / taskkill /IM) в доме — сносит ЧУЖИЕ сервисы дома
when: Stop-Process, -Name, taskkill, /IM, kill by name, python, house services, порты 8000 8765 8080
date: 22.09.2026
executor: Cline
task: полигон D:\AI\PROBA, умная копия (зависший smartcopy.py)
ОШИБКА (дословно, для grep):
`Stop-Process -Name python -Force` — снёс copy-server (8000) и агент (8765) вместе со своим скриптом
СИМПТОМ: после «остановки скрипта по имени» исчез LISTENING на 8000 и 8765; агент ожил только после `ctl.py up`.
ПРИЧИНА: `python` — общее имя ВСЕХ питон-процессов дома (агент, copy-server, ночные скрипты). Остановка по имени бьёт их все — прямой аналог запрета `kill_creo` (creoson бьёт `xtop` по имени = все Creo).
ПРОФИЛАКТИКА:
1. Останавливать ТОЛЬКО по PID: `Stop-Process -Id <pid>`. PID брать из Get-Process по уникальному признаку (StartTime/CommandLine), не по имени.
2. Свой детач-скрипт запускать с `Start-Process ... -PassThru` и хранить PID; снимать — этим PID.
3. После любой остановки — приёмка портов: 8080 CREOSON, 8000 copy-server, 8765 агент, 11434 Ollama; недостающее поднять `python D:\AI\tools\agent\ctl.py up` (приёмка: ровно один LISTENING на порт).
4. Домовые процессы — не «мои»: трогать только свои PID.
ПОВТОРЫ: 1