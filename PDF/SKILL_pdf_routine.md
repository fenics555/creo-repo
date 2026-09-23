---
name: pdf-routine
system: PDF
description: Use when: нужно вывести или ОБНОВИТЬ PDF чертежа Creo (главная рутина дома) — правила, конфиг оформления, инструмент creo_pdf
when: pdf, чертёж, drw, вывод pdf, обновить pdf, перепечать, форматки, MY_ESKD, table.pnt, creo_pdf
priority: critical
date: 23.09.2026
---
# РУТИНА ДОМА: ВЫВОД И ОБНОВЛЕНИЕ PDF ЧЕРТЕЖЕЙ CREO

## 1. ПРАВИЛО
Рядом с чертежом `<имя>.drw[.N]` должен лежать **`<имя>.pdf` той же папки** и быть **не старше** чертежа.
Нет PDF или PDF старее — обновить. Обход — по **всем подпапкам** выбранной папки.
Масштаб дома: в базе агента **24 607 пар** чертёж↔PDF, из них **8 687 «устарел»**.

## 2. ТРИ УСЛОВИЯ PDF (каждое проверено отказом)
| Условие | Ошибка при нарушении |
|---|---|
| модель — **чертёж**, не деталь | `pfcExceptions$XToolkitInvalidType` |
| рабочая папка Creo = папка чертежа | деталь чертежа не находится |
| **`Model.Display()`** до экспорта | `pfcExceptions$XToolkitNotDisplayed` |

**Сборочный чертёж** (`X.drw` при наличии `X.asm`) по имени не открывается — `XToolkitNotFound`;
лечение: **сначала поднять сборку** `RetrieveModel(MDL_ASSEMBLY, "X")`, затем чертёж (проверено: 0 ошибок).
`ModelDescriptor_CreateFromFileName` тут НЕ помогает (`XToolkitNotFound` / `XInvalidFileName` /
`XUnknownModelExtension` — версионный `.drw.1` не принимается).

## 3. ЧТО ДАЁТ «ПРАВИЛЬНЫЙ» PDF — КОНФИГ ДОМА
| Опция `config.pro` | Значение |
|---|---|
| `pro_format_dir` | `Z:\PTC\CREO-START\НАСТРОЙКИ\ФОРМАТЫ\` (163 форматки `a0…a4.frm`) |
| `drawing_setup_file` | `…\НАСТРОЙКИ\configs\MY_ESKD.dtl` — оформление чертежа (ЕСКД) |
| `format_setup_file` | `…\configs\MY_ESKD.dtl` в файле; в живой сессии встречается `dwgform.dtl` (настройки внутри форматки) |
| `pen_table_file` | `…\НАСТРОЙКА_ПРИНТЕРА\table.pnt` — перья/толщины линий |
| `pro_plot_config_dir` | `…\НАСТРОЙКА_ПРИНТЕРА\` |
| `pdf_use_pentable`, `use_8_plotter_pens` | `yes`, `yes` |
Боевой файл — `Z:\PTC\CREO-START\START-STD\config.pro`; Creo должен стартовать **с этой рабочей папкой**
(читает `config.pro` из рабочей папки). Локальный `D:\PTC\CREO-LOCAL-SETUP\CREO-LOCAL-START\config.pro`
этих строк **не содержит** → PDF выйдет без форматок и перьев.

## 4. ИНСТРУМЕНТ
`D:\AI\tools\agent\creo_pdf\` — `creo_pdf_gui.bat` (окно, «дизайн 2») и движок `creo_pdf.bat` (прямой JLINK, **без CREOSON**):
```
creo_pdf.bat scan   <папка>              # отчёт: где PDF нет / PDF старше (Creo НЕ нужен)
creo_pdf.bat export <папка> [лимит]      # создать недостающие/устаревшие (лимит 0 = без ограничения)
creo_pdf.bat pdf    <папка> <имя> [out]  # один чертёж
creo_pdf.bat config-scan | config-find | config-read [файл] | config-load <файл>
creo_pdf.bat creo-find | creo-start [config.pro] [--dry]
```
Внутри: `ChangeDirectory(папка)` → `ModelDescriptor_Create(MDL_DRAWING, имя)` → **`Display()`** →
`Export(<имя>.pdf, PDFExportInstructions_Create())` → **чертёж убирается из сессии** (`Model.Erase()`),
рабочая папка Creo возвращается назад. Просмотрщик PDF — по галочке «открывать PDF» (`PDFOPT_LAUNCH_VIEWER`).
В агенте: инструменты `creo_pdf_scan` (чтение) и `creo_pdf_export` (под щитом).

## 5. ПОРЯДОК РАБОТЫ (проверенный)
1. «СКАН ПДФ (отчёт)» — что устарело/отсутствует (Creo не нужен);
2. «СОЗДАТЬ / ОБНОВИТЬ ПДФ» — создать/обновить (нужен запущенный Creo);
3. «Искать дубли ПДФ и не рядом» — остатки (см. `SKILL_pdf_control.md`);
4. при необходимости — «перемещать в корзину инструмента»;
5. повторный «СКАН ПДФ» — убедиться, что чисто.

## 6. ПРИЁМКА (живые прогоны 23.09.2026)
- `…\VBMT1604 35 градусов Токарные оправки`: было 24 чертежа / 0 в порядке / 23 без PDF / 1 устарел →
  экспорт **24 из 24, 0 ошибок** → повторный скан **24 из 24 в порядке**, 24 файла `%PDF-1.7`.
- `…\000_05 Приспособления`: 90 чертежей, 16 PDF сделано, 3 отказа (сборочные) — вылечено «подъёмом сборки» до 0.
- `…\Планшайбы на серьги`: 2 «отказных» (`plshaiba-4`, `plshaiba-5`) → `PDF OK 35879 б` и `28592 б`.

## 7. ГРАБЛИ
1. Creo дописывает **суффикс версии** к экспорту (`name.pdf` → `name.pdf.1`) — проверять по префиксу.
2. 2D/DXF/DWG/PDF — **только с чертежа**; 3D-обмен (STEP/IGES/VRML/NEUTRAL) — с детали.
3. Пути с пробелами (`Creo 12.4.2.0`) ломают `-Djava.library.path` → запускать через `.bat`.
4. Кириллица: данные корректны, консоль/PowerShell искажают → Python/UTF-8, логи читать `-Encoding UTF8`.
5. Долгий прогон делить: лимит + корешки; окно можно остановить кнопкой СТОП.
6. Перед массовыми прогонами держать ОДНУ сессию Creo (иначе «more than one instance» роняет JVM-мост).

## 8. СВЯЗАННОЕ
`PDF\SKILL_pdf_control.md` (контроль пар, дубли, PDF без модели) ·
`Creo\SKILL_creo_jlink_direct.md` (прямое управление, конфиг, PDF-раздел) ·
`D:\AI\tools\agent\creo_pdf\README.md` (окно, приёмка, корзина инструмента) ·
`D:\AI\PROBA\POLYGON_NOTES.md` §22 · `D:\AI\log\reports\REPORT_pdf_routine_cline_2026-09-23.md`.