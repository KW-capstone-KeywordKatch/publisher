from flask import Flask, render_template, jsonify
import src.database.connect as connect
import src.database.user as user
import src.database.editor as editor
import src.sender.send as send
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import time
import threading

app = Flask(__name__, static_folder="../client/build/static", template_folder="../client")

app.config['TIMEZONE'] = 'Asia/Seoul'

def connect_user_db():
  global user_connect, user_cursor
  user_connect, user_cursor = connect.connectUSERRDS()

def connect_editor_db():
  global editor_connect, editor_cursor
  editor_connect, editor_cursor = connect.connectARTICLERDS()

# database 연결
@app.route('/connect/local')
def connect_local_db_api():
  global user_connect, user_cursor
  user_connect, user_cursor = connect.connectLOCALRDS()
  return "success connect with localDB"

@app.route('/connect/editor')
def connect_editor_db_api():
  connect_editor_db()
  return "success connect with EditoDB"

@app.route('/connect/user')
def connect_user_db_api():
  connect_user_db()
  return "success connect with UserDB"

# 사용자에게 email로 기사 보내기
def send_email():
  with app.app_context():
    response = send.send_email_each_time(user_cursor, editor_cursor)
    return response
  
@app.route('/send')
def send_request():
  send_email_sched_daily()
  return jsonify("true")

# 모든 유저 정보 열람
@app.route('/get/user')
def get_user():
  user_info= jsonify(user.getAllUserInfo(user_cursor))
  return user_info

# 유저 관심사 별 기사 정보 전달
@app.route('/articles/<user_id>')
def get_articles_for_user(user_id):
  # ( user_id , [관심사1, 관심사2...] )
  user_interest = user.getUsersInterest(user_cursor, [user_id])

  if len(user_interest) == 0 :
    return {}

  # {user_id : {keyword:["article_id1","article_id2"...]}, ...} : 키워드 별 기사 내용 받아 올 때 사용
  user_interest_article_id = editor.getUserInterestArticleIdDict(editor_cursor, user_interest)

  if len(user_interest_article_id) == 0:
    return {}

  # {user_id : {keyword:[[기사정보1..],[기사정보2..], ...], ...}, ...} : 사용자 별 메일 보낼 때 사용
  user_interest_article = editor.getArticleInfoDictForClient(editor_cursor,  user_interest_article_id)

  response_data = user_interest_article[int(user_id)]

  return response_data

@app.route('/')
def come_to_publisher():
  return render_template("build/index.html")

def today_send_email_sched():
    sched2 = BackgroundScheduler()
    current_time = datetime.now()
    # 미국 시간 = 한국 시간 - 9시간
    start_time = datetime(current_time.year, current_time.month, current_time.day, 21, 30)
    #start_time = datetime.now()
    end_time = start_time + timedelta(hours=12)
    #end_time = start_time + timedelta(seconds=31)
    interval = timedelta(hours=3)
    sched2.add_job(func=send_email, trigger='interval', start_date=start_time, end_date=end_time, hours=interval.seconds // 3600, id='today_send')
    print(start_time)
    print(end_time)
    sched2.start()

    time.sleep(3600*12)
        
def send_email_sched_daily():
    sched = BackgroundScheduler()
    sched.add_job(today_send_email_sched, 'interval', days=1, id='daily_send')
    print("start")
    sched.start()
    print("end")
    today_send_email_sched()
    while True:
        time.sleep(1)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port='5001', debug=True)