import sys
import pprint
try:
    sys.path.append(r'D:\AI\tools\agent\plm_reader')
    import creo_read
    pprint.pprint(creo_read.passport(r'D:\AI\PROBA\models\00080-03.prt'))
except Exception as e:
    print(f"Error: {e}")
