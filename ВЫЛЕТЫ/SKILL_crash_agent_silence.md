name: crash-agent-silence
system: CRASH
description: Use when: the agent performs reasoning but fails to emit a tool call, causing a perceived "hang" or "standstill".
when: silence, hang, standstill, no tool call, stalling
date: 15.09.2026
executor: Cline
task: Phase 3 of Spec 44v
ОШИБКА (дословно, для grep):
N/A (Silent stall)
СИМПТОМ: Пользователь видит текст рассуждений или пустой ответ без вызова инструментов, что воспринимается как остановка работы.
ПРИЧИНА: факт — модель завершила блок рассуждений, но не перешла к фазе действия (tool call). | гипотеза — нарушение цикла «План -> Действие».
ПРОФИЛАКТИКА:
1. Никогда не заканчивать ход без вызова инструмента (если задача не завершена).
2. Если план сформирован, немедленно генерировать все необходимые вызовы инструментов.
3. При длительном анализе всегда сообщать: «Анализирую [объект], сейчас вызову [инструмент]».
ПОВТОРЫ: 0

