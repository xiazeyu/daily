from pathlib import Path
import json
from logger import log, error
from corelibs import login, getRecordCount, doDaily, logOut, hasTodayRecord
from modData import modCount
from mail import sendMail
import sys

m = 'func'

domainPrefix = 'http://shecs.xiaze.top:5000/?key='

cwd = Path.cwd()
dataPath = cwd / 'data'


def getDatas():
  files = [x for x in dataPath.iterdir()]
  datas = []
  for x in files:
    try:
      text = x.read_text(encoding='UTF-8')
      data = json.loads(text)
      if ('username' in data) and (not data['username'] == '') and ('password' in data) and (not data['password'] == ''):
        datas.append(data)
      else:
        error(m, f'ignored: {data["key"]}')
    except:
      error(m, sys.exc_info())
      continue
  return datas


def chkValidity(obj):
  if (obj['counts'] > 0):  # 0不打卡 -1不发
    return True
  else:
    return False


def do(x):
  rs = login(x)
  if(rs[0] == False):
    rs = login(x)
    if(rs[0] == False):
      sendMail(x['email'], x["username"],
              f'<p>{x["username"]}, 登陆失败,</p><p>请检查您的用户名或密码是否有误.</p><p>剩余次数: {x["counts"]}.</p><p><a href="{domainPrefix + x["key"]}">您的神秘代码:{x["key"]}</a></p>', '[登陆失败]打卡酱')
      return [False, '登陆失败']

  s = rs[1]
  name = rs[2]

  if(not chkValidity(x)):
    if(x['counts'] == 0):
      sendMail(x['email'], name,
              f'<p>{name}, 您的打卡次数已耗尽,</p><p>请获取续期码以继续打卡。</p><p><a href="{domainPrefix + x["key"]}">您的神秘代码:{x["key"]}</a></p>', '[次数耗尽]]打卡酱')
      modCount(x['key'], -1)
    return [True, '次数耗尽']

  tdr = hasTodayRecord(s)
  if(tdr[0]):
    sendMail(x['email'], name,
            f'<p>{name}, 您在{tdr[1]}时已通过其他方式完成打卡!</p><p>剩余次数: {x["counts"]}.</p><p><a href="{domainPrefix + x["key"]}">您的神秘代码:{x["key"]}</a></p>', '[已打过卡]]打卡酱')
    return [True, '已打过卡']

  bf = getRecordCount(s)
  doDaily(s, x)
  af = getRecordCount(s)
  tdr = hasTodayRecord(s)
  logOut(s)

  if(af > bf and tdr[0]):
    modCount(x['key'], -1)
    sbxx = f'是否异常:{x["report"]["DZ_SFYC_DISPLAY"]},宁归来健康码:{x["report"]["DZ_NGLJKM_DISPLAY"]},14天内是否去过南京以外城市:{x["report"]["DZ_SFQGNJYWCS_DISPLAY"]},手机查询最近14天漫游地:{x["report"]["DZ_ZJMYD"]},次日是否返校:{x["report"]["DZ_CRSFFX_DISPLAY"]},是否在南京:{x["report"]["DZ_SFZNJ_DISPLAY"]}'
    sendMail(x['email'], name,
            f'<p>{name}, 本日健康打卡状态: 成功!</p><p>剩余次数: {x["counts"]},</p><p>您的当前申报信息: {sbxx}.</p><p>如您健康情况有变请及时更新.</p><p><a href="{domainPrefix + x["key"]}">您的神秘代码:{x["key"]}</a></p>',
            '[成功]打卡酱')
    return [True, '成功']

  else:
    sendMail(x['email'], name,
            f'<p>{name}, 本日健康打卡状态: 失败!</p><p>我们将在稍后跟踪您的打卡信息.</p><p>剩余次数: {x["counts"]}.</p><p><a href="{domainPrefix + x["key"]}">您的神秘代码:{x["key"]}</a></p>',
            '[失败]打卡酱')
    return [False, '失败']
