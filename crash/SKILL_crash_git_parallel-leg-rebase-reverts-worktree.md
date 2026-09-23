name: crash_git_parallel-leg-rebase-reverts-worktree
system: CRASH
description: Use when: параллельная нога делает rebase — рабочее дерево откатывается (структура/правки исчезают), своя работа оказывается в stash
when: git, rebase, parallel leg, stash, worktree revert, чужая нога, параллельная нога, git mv
date: 22.09.2026
executor: Cline
task: тема CREO — структуризация Creo\ (подразделы) + наполнение скиллов
ОШИБКА (дословно, для grep):
`interactive rebase in progress; onto 91556ce` + `stash@{0}: On master: parallel-leg-creo-reorg-2209`
СИМПТОМ: подпапки `Creo\` (API, DOCS, CREOSON, …) исчезли, новые скиллы пропали из рабочего дерева;
`git status` показал `AA PROGRESS_spec112.md` и `?? Creo/CREOSON/`.
ПРИЧИНА: параллельная нога запустила `git rebase` (выравнивание с `origin/master`) и **застэшила**
чужие правки (`parallel-leg-creo-reorg-2209`); рабочее дерево вернулось к состоянию `origin/master`,
массовые `git mv` откатились.
ПРОФИЛАКТИКА:
1. Перед крупной реорганизацией — смотреть `git status`, `git stash list`, наличие `.git\rebase-merge`;
   при живой чужой ноге НЕ двигать файлы массово.
2. Свою работу фиксировать (коммит/ветка/резервный push) ДО массовых `git mv`.
3. Наткнувшись на чужой rebase — НЕ продолжать и НЕ отменять его; свою работу достать из `stash`, доложить.
4. Срочное сохранение без `--force`: `git push origin master:refs/heads/backup-<дата>` и
   `git push origin refs/stash:refs/heads/backup-<имя>` (проверка — `git ls-remote origin`).
ПОВТОРЫ: 1