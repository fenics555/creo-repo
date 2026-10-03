# -*- coding: utf-8 -*-
"""Поиск по локальной справке Creo (рус.) по ключевым словам.
Находит HTML-страницы, где встречаются термины, и вытаскивает текст.
Запуск: python helpscan.py <папка_справки> <слово1> [слово2 ...] [--max 12]
Вывод: helpscan_out.txt
"""
import os, sys, re, io, glob

def html_to_text(path):
    with open(path, 'rb') as f:
        raw = f.read()
    for enc in ('utf-8', 'cp1251', 'latin-1'):
        try:
            t = raw.decode(enc)
            break
        except Exception:
            continue
    t = re.sub(r'<script[\s\S]*?</script>', ' ', t)
    t = re.sub(r'<style[\s\S]*?</style>', ' ', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = t.replace('&nbsp;', ' ').replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&')
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

def main():
    root = sys.argv[1]
    words = [w.lower() for w in sys.argv[2:] if not w.startswith('--')]
    mx = 12
    if '--max' in sys.argv:
        mx = int(sys.argv[sys.argv.index('--max') + 1])

    files = []
    for dirpath, _, names in os.walk(root):
        for n in names:
            if n.lower().endswith(('.html', '.htm')):
                files.append(os.path.join(dirpath, n))
    files.sort()

    out = io.open('helpscan_out.txt', 'w', encoding='utf-8')
    out.write('СПРАВКА: %s\nФАЙЛОВ: %d\nИщем: %s\n\n' % (root, len(files), ', '.join(words)))

    hits = {}
    for i, f in enumerate(files):
        try:
            txt = html_to_text(f)
        except Exception:
            continue
        low = txt.lower()
        score = sum(low.count(w) for w in words)
        if score:
            hits[f] = (score, txt)

    for f, (score, txt) in sorted(hits.items(), key=lambda x: -x[1][0])[:mx]:
        out.write('=' * 78 + '\n')
        out.write('ФАЙЛ: %s\nСОВПАДЕНИЙ: %d\n' % (os.path.relpath(f, root), score))
        out.write('-' * 78 + '\n')
        low = txt.lower()
        # вырезаем вокруг первого совпадения
        pos = min([low.find(w) for w in words if low.find(w) >= 0])
        lo = max(0, pos - 200)
        out.write(txt[lo:lo + 2200] + '\n\n')

    out.write('\nВСЕГО страниц с совпадениями: %d из %d\n' % (len(hits), len(files)))
    out.close()
    print('helpscan_out.txt hits=%d/%d' % (len(hits), len(files)))

if __name__ == '__main__':
    main()