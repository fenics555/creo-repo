# Конспект изучения: окна (GUI) программ дома

**Статус:** чтение живого кода, без правок. Начат 03.10.2026 (Cline).
**Источник:** `D:\AI\tools\agent\*\gui.py`, `creo_pdf\creo_pdf_gui.py`, `plm_reader\plm_reader.py`,
`dev\skills_check_gui.py`, `dev\ui_check.py`, `dev\stop_button_check.py`, `*_gui.bat`.
**Цель:** свести в один конспект то, как устроены окна дома, — строение, дизайн, соглашения,
проверки; и понять, чего не хватает (отдельного скилла про окна в репо нет).
**Карта скиллов дома:** `D:\AI\repo\SKILL_index.md`; шаблон инструмента —
`Prog\SKILL_tool_template`; закон трёх рук — `MANIFEST.md` п.19.

<!-- ПРОГРЕСС -->
**Ход изучения:** снят инвентарь окон (13 файлов `gui*.py` + 2 больших окна), прочитан каркас
`creo_pdf_gui.py` (образец дома), `plm_reader.py` (самое большое окно), выписаны константы
дизайна и правила потоков, найдены существующие проверки (`stop_button_check`, `ui_check`,
`js_balance`). Дальше по желанию хозяина: снять окна вживую (скриншоты), проверить гипотезу
«все окна на одном каркасе», дописать скилл `SKILL_WINDOWS_GUI` и внести в `SKILL_CHARGE`.
_обновлено 03.10.2026 (Cline)_
<!-- /ПРОГРЕСС -->

## 1. Инвентарь окон (факт)
_03.10.2026, Cline_

Живых окон (без папок `backup`, `_legacy`, `__pycache__`) — 15 окон в 14 файлах:

| Программа | Файл окна | Строк |
|---|---|---|
| plm_reader | `plm_reader\plm_reader.py` (окно внутри файла) | ~3600 |
| navigator | `navigator\gui.py` | 320 |
| orphan_scan | `orphan_scan\gui.py` | 242 |
| creo_export | `creo_export\gui.py` | 227 |
| creo_comb | `creo_comb\gui.py` | 219 |
| dup_scan | `dup_scan\gui.py` | 204 |
| cmnm_scan | `cmnm_scan\gui.py` | 200 |
| skills_check | `dev\skills_check_gui.py` | ~200 |
| config_audit | `config_audit\gui.py` | 175 |
| log_clean | `log_clean\gui.py` | 169 |
| purge_versions | `purge_gui.py` | 170 |
| copy (copy_server) | `copy\gui.py` | 149 |
| make_lst | `make_lst\gui.py` | 126 |
| excel | `excel\gui.py` | 111 |
| creo_pdf | `creo_pdf\creo_pdf_gui.py` | ~800 |

Запуск окон — `*_gui.bat` рядом (15 файлов). Типовой bat (образец `dup_scan_gui.bat`):
```
@echo off
cd /d "%~dp0"
start "" pythonw.exe gui.py
```
У `creo_pdf_gui.bat` другой стиль: `title …` + `python …` + `if errorlevel 1 pause` —
то есть **два разных способа запуска** в одном доме.

## 2. Каркас — он действительно один
_03.10.2026, Cline_

Везде одна и та же пятёрка (проверено по 14 файлам):
```
class Win(App):  def __init__(self, root):
    root.title("V1 — <ЧТО ДЕЛАЕТ>")
    root.geometry("1020x620")
    root.minsize(900, 560)          # есть не везде
    self._style()                   # только в больших
    …сборка…
if __name__ == "__main__":
    r = tk.Tk(); App(r); r.mainloop()
```
Заголовок всегда с версией: `V1 — …` у большинства, `V2` у cmnm_scan и creo_export,
`V7 … дизайн 2` у creo_pdf. То есть **версия окна видна пользователю** — это осознанно.

<!-- КРОШКИ2 -->