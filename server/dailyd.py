from pathlib import Path
from func import getDatas, do
from logger import log, error
import time
import json

m = 'dailyd'

cwd = Path.cwd()
staticPath = cwd / 'static'
rstPath = staticPath / 'result.txt'

def doRoutine():
  datas = getDatas()
  sc = []
  fc = []
  for x in datas:
    time.sleep(20)
    res = do(x)
    if res[0]:
      log(m, f'{x["key"][0:8]} succeed!!')
      sc.append(f'{x["key"][0:8]}, {res[1]}')
    else:
      error(m, f'{x["key"][0:8]} failed!!')
      fc.append(f'{x["key"][0:8]}, {res[1]}')
  log(m, f'{len(sc)} succeed, {len(fc)} failed.')
  log(m, f'{time.strftime("%Y-%m-%d", time.localtime())} finished.')
  rst = {
    'date': time.strftime('%Y-%m-%d', time.localtime()),
    'counts': {
      'success': len(sc),
      'fail': len(fc),
      'total': len(fc) + len(sc),
    },
    'success': sc,
    'fail': fc,
  }
  rstPath.write_text(json.dumps(rst, ensure_ascii=False, indent=2), encoding='UTF-8')

doRoutine()
