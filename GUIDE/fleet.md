# ВЕБ, ФЛОТ, GIT
fleet_tools — состояние флота: какие машины живы, кто работает; /fleet/info — хвост TRAIL_JOURNAL.
git_tools и sync_tools — GIT_SYNC: коммит и пуш репо агента; автосейв каждые ~30 минут;
пуш теперь пишет в data\tmp\git_sync.log вместо глушения в >nul.
nightly_tools — ночной прогон по расписанию (night_hour, night_minute, night_tasks): scan, index, usage, backup;
qa_night.bat — ночная QA с пре-флайтом и pidfile-замком.
web_tools — чтение страниц: web_fetch (бегло), web_study (глубоко); прокси r.jina.ai при ключе web_jina_key; Playwright при web_render.
Проверка: чипы «где склад версий и что почистить», «ночной прогон»; ctl status по портам.
Болезни: двойной ночной прогон невозможен (pidfile); упавший пуш виден в логе;
веб без ключа и без Playwright = тяжёлые JS-страницы не читаются, помечай в отчёте, не молчи.