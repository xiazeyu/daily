import json
import requests
import re
from logger import log, error
import sys
import time

m = 'corelibs'

loginUrl = 'http://authserver.jit.edu.cn/authserver/login'
logoutUrl = 'http://authserver.jit.edu.cn/authserver/logout'
doUrl = 'http://ehallapp.jit.edu.cn/emapflow/sys/lwReportEpidemic/modules/newdailyReport/T_REPORT_EPIDEMIC_CHECKIN_SAVE.do'
indexDoUrl = 'http://ehallapp.jit.edu.cn/emapflow/sys/lwReportEpidemic/index.do'
checkUrl = 'http://ehallapp.jit.edu.cn/emapflow/sys/lwReportEpidemic/modules/newdailyReport/getMyNewDailyReportDatas.do'


def login(settings):
  try:
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    r = s.get(loginUrl, params={'service': indexDoUrl})
    lt = re.search(r'(?:name="lt" value=")(.*?)(?:"\/>)', r.text).group(1)
    execution = re.search(r'(?:name="execution" value=")(.*?)(?:"\/>)', r.text).group(1)
    payload = {'username': settings['username'],
                'password': settings['password'],
                'lt': lt,
                'dllt': 'userNamePasswordLogin',
                'execution': execution,
                '_eventId': 'submit',
                'rmShown': '1'
                }
    r = s.post(loginUrl, data=payload)
    name = re.search(r'(?:name":")(.*?)(?:")', r.text).group(1)
  except:
    error(m, sys.exc_info())
    # error(m, r.text)
    error(m, f'failed logged in as {settings["username"]}')
    return [False, s]
  log(m, f'successfully logged in as {name}')
  return [True, s, name]

def getRecordCount(s):
  r = s.get(checkUrl)
  ori = json.loads(r.text)
  oris = ori['datas']['getMyNewDailyReportDatas']['totalSize']
  log(m, f"record count: {oris}")
  return oris

def hasTodayRecord(s):
  r = s.get(checkUrl)
  ori = json.loads(r.text)
  if(len(ori['datas']['getMyNewDailyReportDatas']['rows']) == 0):
    return [False]
  oris = ori['datas']['getMyNewDailyReportDatas']['rows'][0]['CREATED_AT']
  nowDate = time.strftime('%Y-%m-%d', time.localtime())
  if(oris.find(nowDate) == 0):
    log(m, f"hasTodayRecord: {oris}")
    return [True, oris]
  else:
    return [False]

def doDaily(s, settings):
  return s.post(doUrl, data=settings['report'])

def logOut(s):
  s.get(logoutUrl)
