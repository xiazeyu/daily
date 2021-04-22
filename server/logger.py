enable = True

def log(module, msg):
  if enable: print(f'{module}: {msg}')
  
def error(module, msg):
  if enable: print(f'!Error@{module}: {msg}')
