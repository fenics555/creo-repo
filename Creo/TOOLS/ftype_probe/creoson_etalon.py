# -*- coding: utf-8 -*-
"""ЭТАЛОН ЧЕРЕЗ CREOSON: снимает параметры живой модели (getter, не байты).
Протокол (вскрыт эмпирически 03-04.10.2026):
  POST http://127.0.0.1:8080/creoson
  sessionId — ВЕРХНИМ УРОВНЕМ (в data не работает!)
Запуск: python creoson_etalon.py <модель.prt>
"""
import json, sys, urllib.request

URL = 'http://127.0.0.1:8080/creoson'

def call(cmd, fn, sid=None, data=None):
    body = {'command': cmd, 'function': fn}
    if sid is not None:
        body['sessionId'] = sid
    body['data'] = data or {}
    req = urllib.request.Request(URL, data=json.dumps(body).encode('utf-8'),
                                 headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        return {'status': {'error': True, 'message': str(e)}, 'data': None}

def main():
    model = sys.argv[1] if len(sys.argv) > 1 else None
    c = call('connection', 'connect')
    sid = c.get('sessionId')
    print('connect:', c.get('status'), 'sessionId =', sid)
    if not sid:
        return
    print('pwd:', call('creo', 'pwd', sid).get('data'))
    if model:
        for fn in ('open', 'retrieve', 'load'):
            r = call('file', fn, sid, {'file': model})
            print('file/%s:' % fn, r.get('status'))
            if not r.get('status', {}).get('error'):
                break
    # ищем команду активации модели
    tries = [('model', 'activate'), ('model', 'current'), ('model', 'set_active'),
             ('session', 'model'), ('file', 'activate'), ('file', 'set_active'),
             ('creo', 'activate'), ('model', 'display'), ('model', 'regen'),
             ('model', 'regenerate'), ('file', 'save'), ('model', 'save')]
    for cmd, fn in tries:
        r = call(cmd, fn, sid, {'file': model} if model else {})
        err = r.get('status', {}).get('error')
        msg = r.get('status', {}).get('message', '')
        print('  проба %-8s/%-11s error=%s %s' % (cmd, fn, err, msg[:60]))
    for cmd, fn in (('parameter', 'list'), ('model', 'list'),
                    ('file', 'list'), ('feature', 'list')):
        r = call(cmd, fn, sid)
        d = r.get('data')
        s = json.dumps(d, ensure_ascii=False) if d is not None else ''
        print('\n%s/%s: %s  -> %s' % (cmd, fn, r.get('status'), s[:1500]))
        # вариант с указанием файла
        if model and s.strip() in ('[]', '{}') or 'No currently active' in str(r.get('status', {}).get('message', '')):
            r2 = call(cmd, fn, sid, {'file': model})
            s2 = json.dumps(r2.get('data'), ensure_ascii=False)
            print('   с файлом: %s -> %s' % (r2.get('status'), s2[:1200]))

if __name__ == '__main__':
    main()