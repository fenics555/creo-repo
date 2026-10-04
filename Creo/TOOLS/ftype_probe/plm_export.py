import os

def creoson_call(cmd, fn, sid=None, data=None, host='127.0.0.1', port=8080):
    """Запрос к CREOSON-мосту (Simplified Logic). Только чтение."""
    import urllib.request, json
    body = {'command': cmd, 'function': fn}
    if sid is not None:
        body['sessionId'] = sid
    body['data'] = data or {}
    req = urllib.request.Request('http://%s:%d/creoson' % (host, port),
        data=json.dumps(body).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'})
    return json.loads(urllib.request.urlopen(req, timeout=180).read().decode('utf-8'))


def creoson_features(prt_path):
    """Дерево фич + ТИПЫ на русском из живого Creo. Источник правды."""
    api_path = prt_path[:-2] if prt_path.lower().endswith('.1') else prt_path
    sid = creoson_call('connection', 'connect')['sessionId']
    r = creoson_call('file', 'open', sid, {'file': api_path})
    if r['status']['error']:
        return None
    return (creoson_call('feature', 'list', sid, {'file': api_path})
            .get('data', {}) or {}).get('featlist') or []


def build_production_plm_payload(file_path, binary_params, creoson_features_):
    """Монолитная честная выгрузка Creo -> PLM.
    Оффлайн: кириллица и ID из байтов. Онлайн: дерево фич из CREOSON.
    Массы — строго null: JLINK-сокет изолирован, данных нет."""
    payload = {
        "file_info": {
            "name": os.path.basename(file_path),
            "type": "Assembly" if file_path.lower().endswith(('.asm', '.asm.1'))
                    else "Part",
        },
        "attributes": {
            "designation": binary_params.get("Обозначение")
                            or binary_params.get("ОБОЗНАЧЕНИЕ") or "",
            "name": binary_params.get("Наименование")
                    or binary_params.get("НАИМЕНОВАНИЕ") or "",
            "type": binary_params.get("Тип") or binary_params.get("ТИП") or "",
            "enterprise": binary_params.get("Предприятие") or "",
            "developer": binary_params.get("Разработал")
                         or binary_params.get("РАЗРАБОТАЛ") or "",
        },
        "mass_properties": {
            "volume": None, "surface_area": None, "mass": None,
            "note": ("Данные недоступны: CREOSON не отдает PRO_MP_*, "
                     "JLINK-сокет не поднят. Не выдумывать."),
        },
        "feature_tree": [
            {"feat_id": f.get("feat_id"),
             "feat_name": f.get("name"),
             "feat_type_ru": f.get("type")}
            for f in (creoson_features_ or [])
        ],
    }
    return payload