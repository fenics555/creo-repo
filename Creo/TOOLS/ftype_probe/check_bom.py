import json, creo_json as c
for f in [r'Z:\PTC\Work\00612\00612.prt.1',
          r'Z:\PTC\Work\00080\00080-03.prt.1',
          r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1']:
    o = c.analyze(f)
    print('%-22s params=%-3d bom=%-3d feat=%d'
          % (f.split('\\')[-1][:22], len(o['parameters']),
             len(o['bom']), len(o['features'])))