# crash_git-push-says-up-to-date-but-ahead — `Everything up-to-date` при реальном ahead

**Симптом (01.10.2026, 23:20, задача AGENT_SETTINGS):**
```
git commit -m "PROGRESS phase 21 ..."   -> [master dd65a72] 1 file changed, 44 insertions(+)
git push origin master && git rev-list --left-right --count origin/master...HEAD && git status -sb
-> Everything up-to-date
-> 0	1
-> ## master...origin/master [ahead 1]
```
То есть push **не состоялся**, хотя git написал «Everything up-to-date». Проверка после повторного
пуша: `git ls-remote origin refs/heads/master` = `dd65a72…`, приёмка `0 0`, статус чистый.

**Чем опасно:** «Everything up-to-date» читается как успех. Если нога закрывается на этом,
коммит остаётся только на диске — а правило регламента требует пушить удачный результат сразу
и принимать его (`ls-remote` + `rev-list == 0 0`). Тихой потери работы не должно быть.

**Вероятная причина:** состояние трека `refs/remotes/origin/master` разошлось с реальным
состоянием на сервере (например, предыдущий пуш обновил ref на стороне клиента не полностью,
либо был параллельный пуш). Git сверяется с локальным треком, а не с сервером.

**ПРАВИЛО ПРИЁМКИ (работает всегда):**
1. `git push` — не приёмка. Приёмка = `git ls-remote origin refs/heads/master` и сравнение
   с `git rev-parse HEAD` (строки должны совпасть) плюс `git rev-list --left-right --count
   origin/master...HEAD` = `0 0`.
2. Если `rev-list` показывает ahead, а push написал «up-to-date» — **повторить push** и снова
   проверить `ls-remote`. Один повтор разрешён, второй — уже петля: стоп-отчёт пользователю.
3. Не закрывать фазу по слову «up-to-date» — только по нулям в `rev-list` и совпадению ls-remote.

**Смежные подписи:** `crash_ollama-ansi-stderr-falseexit` (ложный признак успеха из stderr),
`crash_shell-mixed-cmd-and-powershell` (ложный код выхода 1 при неверной команде).
Общий вывод дома: **признак успеха проверяется вторым инструментом, а не первым.**
