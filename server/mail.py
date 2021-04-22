from logger import error, log
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import sys

m = 'mail'

sender = 'twone2021@qq.com'
mail_host = "smtp.qq.com"
mail_user = "twone2021@qq.com"
mail_pass = "kuefldrpxuiudfcf"

def sendMail(distMail, distName, msg, title):
  message = MIMEText(msg, 'html', 'utf-8')
  message['From'] = Header('打卡酱', 'utf-8')
  message['To'] = Header(distName, 'utf-8')
  message['Subject'] = Header(title, 'utf-8')

  try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 587)
    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(sender, distMail, message.as_string())
  except smtplib.SMTPException:
    error(m, sys.exc_info())
    error(m, f'邮件发送失败, {distMail}, {msg}')
    return False
  log(m, f'邮件发送成功, {distMail}, {msg}')
  return True
