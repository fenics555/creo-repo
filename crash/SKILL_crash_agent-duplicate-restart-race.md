name: crash_agent-duplicate-restart-race
system: CRASH
description: Use when: после рестарта агента живы ДВА python agent.py и на порту два LISTENING — рестарт среагировал в гонке со сторожем ctl --watch
when: agent restart, duplicate process, double start, ctl watch, race, SO_REUSEADDR, two LISTENING
date: 17.09.2026
executor: Cline (gemma4:26b)
task: спека 66d, рестарт по прямому слову пользователя
ПОВТОРЫ: 1
ОШИБКА (дословно, для grep):
строковой ошибки нет; дословный признак (netstat -ano | findstr ':8765' | findstr 'LISTENING'):
TCP    0.0.0.0:8765           0.0.0.0:0              LISTENING       22604
TCP    0.0.0.0:8765           0.0.0.0:0              LISTENING       19580
СИМПТОМ: после рестарта живы два python.exe agent.py, оба держат 8765: ThreadingHTTPServer ставит allow_reuse_address=True, второй bind не падает; приёмка «ровно один LISTENING» провалена.
ПРИЧИНА: ctl --watch (цикл 60 с, «if not alive: up») поднимает агента при мёртвом порте параллельно с ручным рестартом — гонка в окне цикла сторожа; оба старта успевают до проверки.
ПРОФИЛАКТИКА:
1. Рестарт одним ходом: ctl.py restart (down+up), либо считать, что в окне до 60 с сторож может среагировать сам.
2. Приёмка рестарта: netstat — ровно ОДИН LISTENING на 8765; Win32_Process agent.py — ровно ОДИН процесс; agent.pid == живой PID; StartTime > mtime правленых файлов.
3. Дубль обнаружен: снять старшего по CreationDate, оставить того, кто в pidfile, перепроверить single-listener.
4. Улучшение (по слову пользователя): в ctl.watch() дебаунс — перепроверить порт через 5-10 с перед up; и/или dедуп-проверка после up.
ПРИМЕЧАНИЕ (адаптер): болезнь среды Cline/ctl дома; в контракт (MANIFEST.md) не переносится (конституция, «Маршрут приложений»).
