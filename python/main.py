from flask import Flask, render_template, jsonify
import src.sender.emailSender as emailSender
import src.database.db as db
import multiprocessing
import time
import os

app = Flask(__name__, static_folder="../client/build/static", template_folder="../client")

@app.route('/')
def come_to_publisher():
  return render_template("build/index.html")

# database 연결

@app.route('/connect/local')
def connect_local_db():
  global local_connect, local_cursor
  local_connect, local_cursor = db.connectLOCALRDS()

@app.route('/connect/editor')
def connect_editor_db():
  global editor_connect, editor_cursor
  editor_connect, editor_cursor = db.connectARTICLERDS()

@app.route('/connect/user')
def connect_user_db():
  global user_connect, user_cursor
  user_connect, user_cursor = db.connectUSERRDS()   


# email로 기사 보내기
@app.route('/send')
def send_request():
  with app.app_context():
    # 1. user_info 받아오기
    user_list = db.getAllUserInfo(user_cursor)

    print(user_list)
    # 2. user_info로 사용자 별 keywords 가져오기

    # 3. keywords로 db에서 기사 ids를 가져오기
    # 4. 기사 ids로 유저 별 article 정보 불러오기
    # 
    # 5,  articles로 유저 별 email_html만들기
    '''
    manager = multiprocessing.Manager()
    html_list = manager.dict()
    proc_list = []

    for i, user in enumerate(user_list):
      mp = multiprocessing.Process(target=emailSender.make_email_templet,args=(user, i, html_list))
      mp.start()
      proc_list.append(mp)
    
    for proc in proc_list:
      proc.join()

    start_send_email = int(time.time())

    # 6. 이메일 전송
    proc_list2 = []

    for i in range(len(user_list)):
      mp = multiprocessing.Process(target=emailSender.send_email,args=(user_list[i], html_list[i]))
      mp.start()
      proc_list2.append(mp)

    for proc in proc_list2:
      proc.join()

    end = int(time.time())

    print("total run time(sec) :", end - start_send_email)
    '''
    return "end"

# 유저 정보 다 가져오기
@app.route('/get/user')
def get_user():
  user_info= jsonify(db.getAllUserInfo(user_cursor))
  return user_info

if __name__ == "__main__":
  app.run(host='0.0.0.0', port='5001', debug=True)