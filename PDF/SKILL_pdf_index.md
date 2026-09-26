name: pdf-index
system: INDEX
description: Use when: задача с темой PDF
when: pdf, pdf_tools, pdf_img, extraction, rendering, перепечать, дубли
date: 26.09.2026
ЧТО ЗДЕСЬ (папка `D:\AI\repo\PDF`, проверено 26.09.2026):
- `SKILL_pdf_index.md` — этот вход направления;
- `SKILL_pdf_routine.md` (**critical**) — рутина дома: вывод и обновление PDF чертежей Creo,
  конфиг оформления (MY_ESKD, table.pnt), инструмент `creo_pdf`, приёмки и грабли;
- `SKILL_pdf_control.md` (**high**) — контроль хозяйства: дубли PDF, «PDF не рядом со своим
  чертежом», PDF без модели, корзина инструмента (`creo_pdf_misplaced.py`, `creo_pdf_orphans.py`).
КОГДА ОТКРЫВАТЬ: теги [PDF], [EXTRACTION]; «вывести/обновить/перепечатать PDF», «дубли PDF»,
«PDF не рядом», «PDF без модели».
КОГДА ПИСАТЬ: CRASH-триггеры → `SKILL_crash_pdf-roots-two-lists`; новое знание рутины — в
`SKILL_pdf_routine.md` / `SKILL_pdf_control.md`, вход правится только при смене состава папки.
универсальный закон — MANIFEST.md, специфика среды — в адаптерах
