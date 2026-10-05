p = open('tree_fields.py', encoding='utf-8').read().split('\n')
open('tree_fields.py', 'w', encoding='utf-8').write('\n'.join(p[:196]) + '\n')
print('осталось строк:', 196)