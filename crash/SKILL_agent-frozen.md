# name: agent-frozen
# system: CRASH
# description: Use when: Агент (HTTP-сервис) «застыл» — порт 8765 слушает (LISTENING), но curl/requests возвращают «Connection closed without response» или «Timeout»; процесс есть, но не реагирует на запросы.
# when: frozen, hang, service stall, connection reset, port listening but no response, застыл, завис сервис
# date: 19.09.2026
# executor: Cline (локальная модель)

## СИМПТОМ:
- `netstat` показывает `LISTENING` на 8765.
- `curl` или `requests` получают `Connection reset by peer` или `Remote end closed connection without response`.
- Процесс `agent.py` существует (есть `agent.pid`), но не отвечает.

## ПРИЧИНА:
- Deadlock в Python threads/asyncio (редко для этого агента).
- Зависание на внешнем ресурсе (например, CREOSON или Ollama) в блокирующем вызове.
- Переполнение ресурсов (memory/fd) или критическая ошибка в потоке, не убившая основной процесс.

## ПРОТОКОЛ ДЕЙСТВИЙ:
1. **ДИАГНОСТИКА:**
   - Проверить порт: `netstat -ano | findstr :8765`.
   - Проверить PID: `type D:\AI\tools\agent\agent.pid`.
   - Сверить PID: `tasklist /FI "PID eq <PID>"`.
   - Попробовать простой GET: `curl -I http://127.0.0.1:8765/status`.

2. **ЛЕЧЕНИЕ (если не отвечает):**
   - **Шаг 1 (Мягкий):** Попробовать убить конкретный PID: `taskkill /F /PID <PID>`.
   - **Шаг 2 (Жесткий):** Если `taskkill` не помог или PID изменился, найти все процессы, слушающие порт, и убить их: `for /f "tokens=5" %a in ('netstat -ano ^| findstr :8765 ^| findstr LISTENING') do taskkill /F /PID %a`.
   - **Шаг 3 (Рестарт):** Запустить агент: `D:\AI\tools\agent\AI_START.bat`.

3. **ПРИЁМКА:**
   - `netstat` показывает ровно один `LISTENING` на 8765.
   - `agent.pid` соответствует живому PID.
   - Первый `curl` к `/status` возвращает `200 OK`.

## ПОВТОРЫ:
- Если после рестарта агент снова "застыл" в течение 5 минут — СТОП. Выдать отчёт о повторном краше и ждать указаний.
