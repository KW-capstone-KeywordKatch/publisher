from flask import Flask
import emailSender
import db

app = Flask (__name__)

# smtp 서버 연결
@app.before_first_request
def before_first_request():
    global smtp_connect
    global conn, cursor
    smtp_connect = emailSender.connect_smtp_server()
    conn, cursor = db.connectionRDS()

@app.route('/')
def hello_world():
  return 'hello'

# email로 기사 보내는 api
@app.route('/send')
def send_request():
  smtp_server = smtp_connect
  user_list = db.getAllUserInfo(cursor)

  # user_list : user[]
  # user[n] : n번째 정보

  # user_list -> keyword -> analyze result 접근해서 정보 가져옴
  # 그 정보를 send_email에 보냄

  for user in user_list:
    emailSender.send_email(smtp_server, user[1])
    print("send:"+str(user[0]))

  return "end"
  
if __name__ == "__main__":
  app.run(host='0.0.0.0', port='5001', debug=True)