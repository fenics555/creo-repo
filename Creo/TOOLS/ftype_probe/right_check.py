import sys
sys.path.insert(0, '.')
import creo_json as cj

d = open(r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1', 'rb').read()
g = cj.read_features(d)
print('всего записей парсера: %d' % len(g))
print('RIGHT в файле:', [x for x in g if x[1] == 'RIGHT'][:5])
print('ID=1:', [x for x in g if x[0] == 1][:8])
short = [x for x in g if len(x[1]) <= 2]
print('имена длиной <=2 символов: %d' % len(short))
print('  примеры:', [(x[0], x[1], x[2]) for x in short[:12]])