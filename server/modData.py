from pathlib import Path
import json
from queryData import getSettings
import sys
from logger import error

m = 'modData'

extDays = 3

cwd = Path.cwd()
dataPath = cwd / 'data'
extendPath = cwd / 'extend.json'


def modSettings(key, settings):
  try:
    ori = getSettings(key)
    confPath = dataPath / key
    ori.update(settings)
    ori['key'] = key
    confPath.write_text(json.dumps(ori, ensure_ascii=False, sort_keys=True, indent=2), encoding='UTF-8')
    return True
  except:
    error(m, sys.exc_info())
    return False

def modCount(key, q):
  try:
    ori = getSettings(key)
    confPath = dataPath / key
    ori["counts"] = ori["counts"] + q
    confPath.write_text(json.dumps(ori, ensure_ascii=False, sort_keys=True, indent=2), encoding='UTF-8')
    return True
  except:
    error(m, sys.exc_info())
    return False

def extend(key, extend):
  extends = json.loads(extendPath.read_text(encoding='UTF-8'))
  try:
    modCount(key, extDays)
    extends.remove(extend)
    extends.append(f'{extend}_{key}')
    extendPath.write_text(json.dumps(
        extends, ensure_ascii=False, sort_keys=True, indent=2), encoding='UTF-8')
    return True
  except:
    error(m, sys.exc_info())
    return False
