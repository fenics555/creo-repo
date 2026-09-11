# CREOSON: МОСТ К CREO
CREOSON — Java-сервер на порту 8080, переводит JSON-команды в API Creo. Агент говорит с ним по HTTP, тела — чистый JSON без BOM.
Сессия: connection/connect → sessionId; живёт до падения Creo или сброса.
Чтение без согласования: creo_get_active, creo_get_params, creo_get_mass, creo_get_relations, creo_list_files, creo_find_model.
Пишущие только через [СОГЛАСОВАНИЕ]: creo_save, export_pdf (внутри pdf_refresh), copy-операции через copy_server (порт 8000).
Примеры: creo_get_params name=korpus params=НАИМЕНОВАНИЕ,MASS; export_pdf file=m-a338-6-75-01.drw filename=a338-6-75.pdf dirname=Z:\PTC\Work\…
Проверка: creo_status (чип «статус Creo и открытые модели»), ctl status по портам.
Болезни: BOM в начале тела = «Invalid JSON input»; Creo выключен = ошибка connect и мёртвые трейлы;
протухшая сессия = переподключись и повтори; пишущая без согласования = нарушение контракта (approval-защита).
Полный справочник команд: D:\AI\repo\Creo\SKILL_creoson_complete.md; правила записи: SKILL_creoson_write_rules.md.