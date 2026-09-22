name: crash_session-interruption
system: CRASH
description: Use when: потеря сессии, обрыв связи, генерация оборвана на полуслове
when: session_loss, interruption, connection_error, timeout
date: 17.09.2026
executor: Cline
task: СПЕКА 71 (рефактор agent.py)
ОШИБКА (дословно, для grep):
None (потеря связи)
СИМПТОМ: ИИ перестал отвечать или сессия закрылась неожиданно.
ПРИЧИНА: обрыв на уровне сети или платформы.
ПРОФИЛАКТИКА:
1. Сразу после возврата — протокол REVIVE.
2. Проверить окно контекста и последние выходы, чтобы сохранить непрерывность.
ПОВТОРЫ: 1
