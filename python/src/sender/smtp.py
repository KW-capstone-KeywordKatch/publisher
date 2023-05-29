import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import logging
import time
import src.sender.emailForm as emailForm
from flask import render_template
# smtp 기본 기능 --------------------------------------------------------

# smtp 서버와 연결
def connect_smtp_server():
  try :
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    smtp_connect = smtplib.SMTP(smtp_server, smtp_port)
    smtp_connect.starttls()
    smtp_connect.login(os.getenv('ADMIN_EMAIL'), os.getenv('ADMIN_PASSWORD'))
    
    return smtp_connect

  except Exception as e:
    logging.error("smtp connect fail:"+str(e))

# 이메일 전송
def send_email(user, msg):
  try:
      start = int(time.time())
      smtp_connect = connect_smtp_server()
      smtp_connect.sendmail(os.getenv('ADMIN_EMAIL'), user[0], msg.as_string())
      print("send user", str(user[1]),"'s run time(sec) :", int(time.time()) - start)
      smtp_connect.close()
    
  except Exception as e:
    logging.error("email send fail:"+str(e))

# 사용자 별 전달한 이메일 양식 생성
def create_email_templet(user, idx, msg_list, articles_dict:dict):
  recv_email = user[0]

  msg = MIMEMultipart("alternative")
  msg["Subject"] = "오늘의 기사"
  msg["From"] = formataddr(("KeywordKatch", os.getenv('ADMIN_EMAIL')))
  msg["To"] = recv_email

  # html 만들기
  html = emailForm.create_form(user[1], articles_dict);  
  
  news = MIMEText(html, "html")
  msg.attach(news)

  msg_list[idx] = msg

def create_test_email_templet(user):
  recv_email = user[0]

  msg = MIMEMultipart("alternative")
  msg["Subject"] = "오늘의 기사"
  msg["From"] = formataddr(("KeywordKatch", os.getenv('ADMIN_EMAIL')))
  msg["To"] = recv_email

  # html 만들기
  html = render_template('templates/initial_html.html',)  
  
  news = MIMEText(html, "html")
  msg.attach(news)

  return msg, html  