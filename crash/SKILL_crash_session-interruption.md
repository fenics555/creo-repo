name: crash_session-interruption
system: CRASH
description: Use when: session loss, connection interrupted, AI stopped generating mid-sentence
when: session_loss, interruption, connection_error, timeout
date: 17.09.2026
executor: Cline
task: Spec 71 (Refactor agent.py)
ОШИБКА (дословно, для grep):
None (communication loss)
СИМПТОМ: AI stopped responding or session closed unexpectedly
ПРИЧИНА: Network or platform-level interruption
ПРОФИЛАКТИКА:
1. Use the REVIVE protocol immediately upon return.
2. Check context window and recent outputs to ensure continuity.
ПОВТОРЫ: 1
