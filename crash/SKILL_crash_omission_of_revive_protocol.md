# SKILL: crash_omission_of_revive_protocol

name: crash_omission_of_revive_protocol
executor: Cline

## Description
Incident: omission of mandatory ritual steps (reading skill and providing proof string) during a REVIVE or Crash event.

## Prevention
1. Treat REVIVE/Crash as an atomic ritual, not just a diagnostic task.
2. Always include the mandatory proof string: «скилл выживания прочитан; крах-скил: <имя или нет>».
3. Always re-read `SKILL_local_agent_cline.md` in the same response as the diagnostics.
4. If the response lacks the ritual, it is a violation.

ОШИБКА: omission of ritual steps during REVIVE/Crash
