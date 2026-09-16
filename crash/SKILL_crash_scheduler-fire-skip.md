name: scheduler-fire-skip
system: CRASH
description: Use when: задача планировщика с триггером повторения не стартует в расчётный
  огонь — LASTRUN держится старым, NextRunTime перескакивает на следующую точку сетки,
  в журнале TaskScheduler/Operational нет ни одного события задачи за момент пропуска
when: scheduler, fire skipped, LASTRUN, NextRunTime, StopAtDurationEnd, репетишн, триггер, тик
date: 16.09.2026
executor: Cline (локальная модель)
task: спека-меню п.2, задача \repo-sync (автосейв D:\AI\repo)
ОШИБКА (дословно, для grep):
нет записи; отказ без события. Факты: NOW=11:03:06 LASTRUN=10:51:51 NEXT=11:30:30
(огонь 11:00:00 пропущен); в журнале нет событий 100/129/200/201 по задаче после 10:51:29.
СИМПТОМ: задача зарегистрирована, STATE=Ready, NEXT показывается корректно, но в расчётный
момент движок не предпринимает НИЧЕГО (даже попытки запуска в журнале нет), NEXT молча
переезжает на следующую точку сетки; schtasks /run при этом работает нормально.
ПРИЧИНА: подтверждено диффом XML — <StopAtDurationEnd>true</StopAtDurationEnd> внутри
Repetition триггера без Duration (эталонная задача \creo-sync без этого поля стрельнула
в 11:00:00 ровно, LASTRUN=11:00:00 RESULT=0, в ту же минуту, когда больная скипнула).
Вторичный кандидат: DisallowStartIfOnBatteries=true против false у эталона.
ПРОФИЛАКТИКА:
1. После Register-ScheduledTask читать триггер обратно (Export-ScheduledTask) и сверять
   с эталоном: StopAtDurationEnd — отсутствует или false; Duration — пустой (бесконечно).
2. Ставить StartWhenAvailable=true (New-ScheduledTaskSettingsSet -StartWhenAvailable):
   пропущенный огонь догоняется при первой возможности.
3. Батарейные условия: параметр в этом модуле называется положительно —
   -AllowStartIfOnBatteries; имени -DisallowStartIfOnBatteries НЕ существует.
4. Не верить NextRunTime как доказательству: проверять LastRunTime/LastTaskResult после
   расчётной точки или маркер-файл, который пишет само действие.
5. Соседняя ловушка того же узла: schtasks /create /ri 30 без /du даёт DURATION=PT1H
   (сторож спал бы через час); создавать через Register-ScheduledTask с Repetition
   без Duration, а конфиг ловить чтением XML обратно.
6. Рецептуру регистрации валидировать одноразовой пробой-задачей с тем же строением
   триггера и маркер-файлом (огонь через 2 мин, чанки ожидания по 20-25 с), потом убрать.
