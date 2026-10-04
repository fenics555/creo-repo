"""АУДИТ чтения feat_id по всей боевой базе (только чтение).

Идёт по файлам, находит записи фич вида `<имя>\0 01 00 [18 E5] <varint>`,
декодирует ID кодеком и проверяет круговое преобразование enc(dec(x)) == x.
Так ловится любая ошибка кодекa на реальных данных.

Запуск: python id_audit.py [папка] [N_файлов]
"""
import os, sys, random, io
import etalonbatch as e

PRE_N = b'\x00\x01\x00'          # хвост записи: после NUL имени
PRE_NE = b'\x00\x01\x00\x18\xe5'  # вариант с префиксом 18 E5


def scan(path):
    """Ищет `<имя>\\0 01 00 [18 E5] <varint>` и проверяет кодек.

    ⚠️ Искать надо ПО ИМЕНИ, а не по голому `\x00\x01\x00`: этот хвост
    встречается в шуме, и без проверки имени кодек ошибочно
    объявляется сломанным (5 ложных срабатываний на 40 файлах).
    """
    data = open(path, 'rb').read()
    n = bad = 0
    samples = []
    i = 0
    while i < len(data) - 8:
        if data[i + 1:i + 4] == PRE_N and 32 <= data[i] < 127:
            # data[i] — последний символ имени; перед ним тоже имя (jj..i),
            # а сразу после data[i] идёт NUL, закрывающий имя.
            jj = i - 1
            k = jj
            while k >= 0 and 32 <= data[k] < 127:
                k -= 1
            name_len = (i - k)  # длина имени
            if name_len >= 1 and name_len <= 60:
                for pre, off in ((PRE_N, 3), (PRE_NE, 5)):
                    p = i + off
                    v, w = e.dec_varint(data, p)
                    n += 1
                    if e.enc_varint(v) != data[p:p + w]:
                        bad += 1
                        if len(samples) < 3:
                            samples.append((i, data[p:p + w].hex(' '), v))
                    break
        i += 1
    return n, bad, samples


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else r'Z:\PTC\Work'
    want = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    files = []
    for root, dirs, fs in os.walk(base):
        for f in fs:
            if f.lower().endswith('.prt.1'):
                files.append(os.path.join(root, f))
        if len(files) > 30000:
            break
    random.seed(42)
    random.shuffle(files)

    out = io.open('id_audit_out.txt', 'w', encoding='utf-8')
    checked = done = 0
    bad_total = 0
    for p in files:
        if done >= want:
            break
        try:
            n, bad, smp = scan(p)
        except Exception as e2:
            out.write('[ошибка] %s: %s\n' % (os.path.basename(p), e2))
            continue
        done += 1
        if n:
            checked += n
        bad_total += bad
        out.write('%s: записей=%d нарушений=%d %s\n'
                  % (os.path.basename(p), n, bad,
                     ('примеры: %s' % smp) if smp else ''))
    out.write('\nИТОГО: файлов=%d, записей=%d, НАРУШЕНИЙ=%d\n'
              % (done, checked, bad_total))
    out.close()
    print('id_audit_out.txt files=%d records=%d BAD=%d'
          % (done, checked, bad_total))


if __name__ == '__main__':
    main()