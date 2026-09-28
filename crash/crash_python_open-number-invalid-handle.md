---
name: crash_python_open-number-invalid-handle
system: crash
description: Use when: Python open() падает с OSError [WinError 6] "Неверный дескриптор" при чтении/записи файла
when: WinError 6, invalid handle, open, OSError, неверный дескриптор, скрипт, bench
priority: high
---
# open() ПОЛУЧАЕТ ЧИСЛО ВМЕСТО ПУТИ → WinError 6 (28.09.2026)

## Подпись
`OSError: [WinError 6] Неверный дескриптор` на строке `open(src, 'rb')`,
хотя файл существует и читается в отдельном скрипте.

## Причина
Функция-хелпер возвращала РАЗМЕР файла, а её результат использовался как путь:
```python
def make(path, mb):
    if not os.path.exists(path):
        open(path, 'wb').write(b'\0' * (mb*1024*1024))
    return os.path.getsize(path)      # <- возвращает ЧИСЛО

src = make(os.path.join(LOCAL, 'par.bin'), 25)   # src = 26214400
payload = open(src, 'rb').read()   # open(26214400) -> число трактуется как FD
```
`open(N)` на Windows воспринимает целое как дескриптор файла → ERROR_INVALID_HANDLE.
Трассировка указывает на `open(src, ...)` — и это сбивает с толку (файл-то есть).

## Лечение
Держать путь и размер РАЗДЕЛЬНО:
```python
src_path = os.path.join(LOCAL, 'par.bin')
make(src_path, 25)
payload = open(src_path, 'rb').read()
```

## Цена
Три запуска впустую + поиск несуществующей проблемы с сетью/SMB/дескрипторами.

## Профилактика
- Хелперы не должны возвращать значение, которое путают с путём. Имя `make()` → `ensure_file()`.
- При WinError 6 сначала проверить ТИП переменной-пути (`print(type(src), src)`), а не сеть.
- Запускать тот же open в изолированном мини-скрипте: если там работает — дело в переменной, не в файле.

## Счётчик повторов: 1
