from flask import Flask, render_template, jsonify
import src.database.connect as connect
import src.database.user as user
import src.database.editor as editor
import src.sender.send as send
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

app = Flask(__name__, static_folder="../client/build/static", template_folder="../client")

# database 연결
@app.route('/connect/local')
def connect_local_db():
  global user_connect, user_cursor
  user_connect, user_cursor = connect.connectLOCALRDS()
  return "success connect with localDB"

@app.route('/connect/editor')
def connect_editor_db():
  global editor_connect, editor_cursor
  editor_connect, editor_cursor = connect.connectARTICLERDS()
  return "success connect with EditoDB"

@app.route('/connect/user')
def connect_user_db():
  global user_connect, user_cursor
  user_connect, user_cursor = connect.connectUSERRDS()
  return "success connect with UserDB"

# 사용자에게 email로 기사 보내기
@app.route('/send')
def send_request():
  response = send.send_email_each_time(user_cursor, editor_cursor)
  return response

# 모든 유저 정보 열람
@app.route('/get/user')
def get_user():
  user_info= jsonify(user.getAllUserInfo(user_cursor))
  return user_info

# 유저 관심사 별 기사 정보 전달
@app.route('/get/articles/<user_id>')
def get_articles_for_user(user_id):
  # ( user_id , [관심사1, 관심사2...] )
  user_interest = user.getUsersInterest(user_cursor, [user_id])

  if user_interest == None :
    return {}

  # {user_id : {keyword:["article_id1","article_id2"...]}, ...} : 키워드 별 기사 내용 받아 올 때 사용
  user_interest_article_id = editor.getUserInterestArticleIdDict(editor_cursor, user_interest)

  if user_interest_article_id == None:
    return {}

  # {user_id : {keyword:[[기사정보1..],[기사정보2..], ...], ...}, ...} : 사용자 별 메일 보낼 때 사용
  user_interest_article = editor.getArticleInfoDictForClient(editor_cursor,  user_interest_article_id)

  return user_interest_article[int(user_id)]

@app.route('/')
def come_to_publisher():
  return render_template("build/index.html")

scheduler = BackgroundScheduler()
start_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 6, 30)
end_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 18, 31)
interval = timedelta(hours=3)
scheduler.add_job(func=send_request, trigger='interval', start_date=start_time, end_date=end_time, hours=interval.seconds // 3600)
scheduler.start()

if __name__ == "__main__":
  app.run(host='0.0.0.0', port='5001', debug=True)