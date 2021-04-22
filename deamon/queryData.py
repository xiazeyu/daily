from pathlib import Path
import json
from corelibs import login, getRecordCount, logOut

cwd = Path('/app')
dataPath = cwd / 'data'
keysPath = cwd / 'conf' / 'keys.json'
samplePath = cwd / 'conf' / 'sample.json'
extendPath = cwd / 'conf' / 'extend.json'

def keyValid(key):
  keys = json.loads(keysPath.read_text(encoding='UTF-8'))
  if key in keys:
    return True
  else:
    return False

def testExtend(key):
  extends = json.loads(extendPath.read_text(encoding='UTF-8'))
  if key in extends:
    return True
  else:
    return False

def getSettings(key):
  sample = json.loads(samplePath.read_text(encoding='UTF-8'))
  confPath = dataPath / key
  if(not confPath.exists()):
    sample['key'] = key
    return sample
  return json.loads(confPath.read_text(encoding='UTF-8'))

def testLogin(username, password):
  rs = login({"username": username, "password": password})
  if rs[0]:
    s = rs[1]
    c = getRecordCount(s)
    logOut(s)
    return {
      "status": True,
      "name": rs[2],
      "count": c,
    }
  else:
    return {
      "status": False,
    }
