from flask import Flask, request, jsonify, make_response, abort
from queryData import getSettings, testLogin, testExtend, keyValid
from modData import modSettings, extend
from logger import log
from func import getDatas
from mail import sendMail

m = 'server'

app = Flask(__name__, static_folder='static', static_url_path='/static')


@app.route('/daily/api/v1.0/status/count', methods=['GET'])
def count_status():
  return jsonify({'count': len(getDatas())})

@app.route('/daily/api/v1.0/test/key', methods=['POST'])
def key_test():
  r = request.values
  expr = ['key']
  log(m, f'got:{r}')
  for e in expr:
    if not e in r:
      abort(400)

  return jsonify({'status': keyValid(r['key'])})


@app.route('/daily/api/v1.0/test/email', methods=['POST'])
def mail_test():
  r = request.values
  expr = ['key', 'email']
  log(m, f'got:{r}')
  for e in expr:
    if not e in r:
      abort(400)

  if not keyValid(r['key']):
    abort(401)

  return jsonify({'status': sendMail(r['email'], '打卡酱用户', '尊敬的打卡酱用户: 我们今后将通过此邮箱通知您，谢谢。', '[测试]打卡酱')})

@app.route('/daily/api/v1.0/test/login', methods=['POST'])
def login_test():
  r = request.values
  expr = ['key', 'username', 'password']
  log(m, f'got:{r}')
  for e in expr:
    if not e in r:
      abort(400)

  if not keyValid(r['key']):
    abort(401)

  return jsonify(testLogin(r['username'], r['password']))

@app.route('/daily/api/v1.0/test/extend', methods=['POST'])
def extend_test():
  r = request.values
  expr = ['extend']
  log(m, f'got:{r}')
  for e in expr:
    if not e in r:
      abort(400)

  return jsonify({'status': testExtend(r['extend'])})

@app.route('/daily/api/v1.0/settings/get', methods=['POST'])
def get_settings():
  r = request.values
  expr = ['key']
  log(m, f'got:{r}')
  for e in expr:
    if not e in r:
      abort(400)

  if not keyValid(r['key']):
    abort(401)

  o = getSettings(r['key'])
  del o['password']
  return jsonify(o)

@app.route('/daily/api/v1.0/settings/mod', methods=['POST'])
def mod_settings():
  r = request.values
  expr = ['key',
          'username',
          'password',
          'DZ_SFYC',
          'DZ_NGLJKM',
          'DZ_SFQGNJYWCS',
          'DZ_ZJMYD',
          'DZ_CRSFFX',
          'DZ_SFZNJ']
  log(m, f'got:{r}')
  for e in expr:
    if not e in r:
      abort(400)

  if not keyValid(r['key']):
    abort(401)

  report = {
    "DZ_SFYC": r['DZ_SFYC'],
    "DZ_SFYC_DISPLAY": "是" if r['DZ_SFYC'] == 'YES' else "否",
    "DZ_NGLJKM": r['DZ_NGLJKM'],
    "DZ_NGLJKM_DISPLAY": "绿色" if r['DZ_NGLJKM'] == '1' else "黄色" if r['DZ_NGLJKM'] == '2' else "红色",
    "DZ_SFQGNJYWCS": r['DZ_SFQGNJYWCS'],
    "DZ_SFQGNJYWCS_DISPLAY": "是" if r['DZ_SFQGNJYWCS'] == 'YES' else "否",
    "DZ_ZJMYD": r['DZ_ZJMYD'],
    "DZ_CRSFFX": r['DZ_CRSFFX'],
    "DZ_CRSFFX_DISPLAY": "是" if r['DZ_CRSFFX'] == 'YES' else "否",
    "DZ_SFZNJ": r['DZ_SFZNJ'],
    "DZ_SFZNJ_DISPLAY": "是" if r['DZ_SFZNJ'] == 'YES' else "否",
  }
  settings = {
    'username': r['username'],
    'email': r['email'],
    'report': report,
  }
  if not r['password'] == '':
    settings['password'] = r['password']

  return jsonify({'status': modSettings(r['key'], settings)})

@app.route('/daily/api/v1.0/settings/extend', methods=['POST'])
def extend_settings():
  r = request.values
  expr = ['key', 'extend']
  log(m, f'got:{r}')
  for e in expr:
    if not e in r:
      abort(400)

  if (not keyValid(r['key'])) or (not testExtend(r['extend'])):
    abort(401)

  return jsonify({'status': extend(r['key'], r['extend'])})

@app.route('/')
def index():
    return app.send_static_file("index.html")

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
