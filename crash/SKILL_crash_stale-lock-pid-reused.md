---
name: crash_stale-lock-pid-reused
system: CRASH
description: Use when: процесс не стартует, потому что «already running: PID N», но процесс с этим PID — ЧУЖОЙ (PID переиспользован)
when: lock, stale-lock, pid, reused, already-running, loop_watch, mutex, single-instance
date: 26.11.2026
executor: Cline
task: нога 4 сторожа (запуск loop_watch после перезапуска VS Code)
---

ОШИБКА (дословно, для grep):
  loop_watch already running: PID 13248 - exit (lock: D:\AI\log\urn\cline\loop_watch.lock)
  (при этом сторож НЕ работал; PID 13248 = процесс Code (VS Code))

СИМПТОМ: фоновый процесс (сторож) не запускается — в консоли «already running: PID N». Проверка `Get-Process -Id N` показывает, что процесс **жив**, но это **чужой** процесс (VS Code, другая программа). Сторож считает, что работает, — и молчит. Датчик слеп.

ПРИЧИНА: файл-замок хранит **только PID**, а проверка живости — `pid_alive(pid)` = «существует ли процесс с таким PID». Windows **переиспользует PID**: после смерти сторожа его PID занял другой процесс. Замок «залип» навсегда.

ПРОФИЛАКТИКА:
1. Проверять **не только** живость PID, но и **имя процесса-образа** (`QueryFullProcessImageNameW`) — `python.exe`/`pythonw.exe`/`py.exe`, а не «любой с тем же PID».
2. Осиротевший замок (PID жив, но это не наш процесс) — **снимать автоматически** с сообщением `stale lock: ... taking over`.
3. `--once` (разовый запуск) — **без замка** (`--no-lock`), иначе разовая проверка блокируется фоновым сторожем.
4. Альтернатива файл-замку — именованный мьютекс ОС (`CreateMutexW`), ОС сама снимает при смерти процесса.

ПОВТОРЫ: 1
