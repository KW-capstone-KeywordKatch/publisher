import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import logging
import time
import src.sender.emailForm as emailForm

# smtp 기본 기능 --------------------------------------------------------

# smtp 서버와 연결
def connect_smtp_server():
  print("start connection")
  smtp_server = "smtp.gmail.com"
  smtp_port = 587
  # 보내는 사람의 email - 임시로 넣음. 나중에 따로 계정 파서 넣기
  # 구글 앱 비밀번호 - 2차 인증 - 앱 비밀번호
  # SMTP 세션 생성
  smtp_connect = smtplib.SMTP(smtp_server, smtp_port)
  smtp_connect.starttls()
  smtp_connect.login(os.getenv('ADMIN_EMAIL'), os.getenv('ADMIN_PASSWORD'))

  print("end connection")
  
  return smtp_connect

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
  # 여기에 뉴스 보내는 날짜 추가하기 ( 서버에서 같이 받기 or 현재 날짜 보내기)
  # 사용자가 받는 메일 제목
  msg["Subject"] = "오늘의 기사"
  # 표시 될 발송자 이름
  msg["From"] = formataddr(("KeywordKatch", os.getenv('ADMIN_EMAIL')))
  msg["To"] = recv_email

  # html 만들기
  html = emailForm.create_form(user[1], articles_dict);  
  
  news = MIMEText(html, "html")
  msg.attach(news)

  msg_list[idx] = msg

