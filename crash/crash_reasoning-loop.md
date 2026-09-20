name: crash_reasoning-loop
system: CRASH
description: Use when the agent gets stuck in a loop of repetitive, failing tool calls or reasoning without making progress.
when: loop, repeat, reasoning, same-parameters
date: 20.09.2026
executor: Cline
task: Spec 101 (harvest_gui.py)
ОШИБКА (дословно, для grep):
[The agent repeats the same tool call with the same parameters or the same reasoning pattern 3 times]
СИМПТОМ: Бесконечные попытки выполнить одну и ту же операцию, которая уже завершилась ошибкой или не дала результата.
ПРИЧИНА: Игнорирование результата предыдущей попытки или отсутствие смены метода (crash_reasoning-loop).
ПРОФИЛАКТИКА:
После первого отказа — смена метода. После второго — стоп-отчёт и изменение стратегии. Третий одинаковый вызов = петля.

ПОВТОРЫ: 1
