import json, os, sys
sys.path.insert(0, r'D:\AI\repo\Creo\TOOLS\ftype_probe')
import creo_json as cj
from plm_export import creoson_features, build_production_plm_payload

MODELS = [r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1',
          r'Z:\PTC\Work\00080\00080-03.prt.1',
          r'Z:\PTC\Work\00612\00612.prt.1']

for p in MODELS:
    if not os.path.exists(p):
        print('нет файла:', p); continue
    # ОФЛАЙН: кириллица и параметры из байтов
    res = cj.analyze(p)
    params = res.get('parameters', {})
    # ОНЛАЙН: дерево фич с типами из живого Creo
    feats = creoson_features(p)
    plm = build_production_plm_payload(p, params, feats)
    s = json.dumps(plm, ensure_ascii=False, indent=2)
    json.loads(s)
    print('=' * 62)
    print('ФАЙЛ: %s' % os.path.basename(p))
    print('JSON валиден, %d символов' % len(s))
    print('  Обозначение: %r' % plm['attributes']['designation'])
    print('  Тип:         %r' % plm['attributes']['type'])
    print('  Предприятие: %r' % plm['attributes']['enterprise'])
    print('  фич в дереве: %d' % len(plm['feature_tree']))
    print('  масса:        %r' % plm['mass_properties']['mass'])
    for f in plm['feature_tree'][:6]:
        print('     ID %-7s %-16s %s' % (f['feat_id'], f['feat_name'],
                                        f['feat_type_ru']))