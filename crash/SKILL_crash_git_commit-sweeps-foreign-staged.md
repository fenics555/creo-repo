name: crash_git_commit-sweeps-foreign-staged
system: CRASH
description: Use when: коммит без pathspec в доме с параллельными ногами уносит чужую застейдженную работу в свой коммит
when: git, commit, staged, foreign work, pathspec, parallel legs, house
date: 22.09.2026
executor: Cline (локальная модель)
task: спека 112 / Creo-нога, коммит бумаг
ОШИБКА (дословно, для grep):
[master ce81b27] spec112 creo leg: pdf removal recorded + library divergence (docs)
 35 files changed, 46 insertions(+), 20 deletions(-)
 rename Creo/{ => API}/SKILL_creojs_api.md (100%)
СИМПТОМ: мой docs-коммит (3 файла по замыслу) принёс 35 изменений: 31 rename — чужая
реорганизация папки Creo (API/, COPY/, CREOSON/, DAVYDOVKA/, DOCS/, INFRA/, RELATIONS/, STANDARDS/),
сделанная параллельной ногой и лежавшая у неё staged.
ПРИЧИНА: факт — `git add -- <свои пути>` был адресным, но `git commit -m "..."` вызван БЕЗ pathspec,
то есть коммитил ВСЁ staged; у параллельной ноги переезды были уже застейджены (git mv).
Гипотеза: правило «git add -A запрещён» закрыло половину двери; вторая половина — тот же дефект
в `commit` без путей. Контент не потерян (всё в истории), но авторство и сообщение коммита чужие.
ПРОФИЛАКТИКА:
1. В доме с параллельными ногами коммитить ТОЛЬКО с pathspec: `git commit -m "<текст>" -- <свои пути>`;
   без pathspec — лишь когда `git status --porcelain` показывает исключительно свои файлы.
2. Перед коммитом — цитата `git diff --cached --name-only` и сверка со своим списком файлов.
3. Чужое staged не разстейдживать молча (не трогать чужую подготовку); расхождение = стоп-отчёт.
4. Коммит не переписывать (rewrite истории и push --force запрещены); инцидент фиксируется строкой.
ПОВТОРЫ: 2 (первый — 6346d73 «git add -A подмёл чужое», 22.09; второй — ce81b27 «commit без pathspec», 22.09)