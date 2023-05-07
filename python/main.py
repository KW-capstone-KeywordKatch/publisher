from flask import Flask, render_template, jsonify
import src.sender.smtp as smtp
import src.database.connect as connect
import src.database.user as user
import src.database.editor as editor
import src.sender.multiprocess as multi
import multiprocessing
import time

app = Flask(__name__, static_folder="../client/build/static", template_folder="../client")

@app.route('/')
def come_to_publisher():
  return render_template("build/index.html")

# database 연결
@app.route('/connect/local')
def connect_local_db():
  global local_connect, local_cursor
  local_connect, local_cursor = connect.connectLOCALRDS()
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
  with app.app_context():
    # 1. 사용자 별 전송할 기사 정보 받아오기
    # dict = {user_id:[email, nickname], ...} : 이메일 전송 때 사용함
    # list = [user_id1, user_id2, ...] : 사용자의 키워드 리스트 받아올 때 사용
    user_info_dict, user_id_list = user.getUserInfoDictAndUserIdList(user_cursor)
        
    # { user_id : [key1, key2, key3...], ...} : 사용자 별 키워드에 따른 기사id들을 받아 올 때 사용
    user_interest_dict = user.getUserInterestDict(user_cursor, user_id_list)

    # {user_id : {keyword:["article_id1","article_id2"...]}, ...} : 키워드 별 기사 내용 받아 올 때 사용
    user_interest_article_id_dict = editor.getUserInterestArticleIdDict(editor_cursor, user_interest_dict)
    
    # {user_id : {keyword:[[기사정보1..],[기사정보2..], ...], ...}, ...} : 사용자 별 메일 보낼 때 사용
    user_interest_article_dict = editor.getArticleInfoDict(editor_cursor,  user_interest_article_id_dict)

    sendable_user_info_dict = {}

    for user_id in user_info_dict.keys():
      if user_interest_article_dict.get(user_id) is not None:
        sendable_user_info_dict[user_id] = user_info_dict[user_id]
    
    print("user:", len(user_info_dict))
    

    # 2. 사용자 별 이메일 폼 생성
    html_list = multi.create_email_templet_using_multiprocess(sendable_user_info_dict, user_interest_article_dict)

    print("html_list:",len(html_list))

    # 3. 이메일 전송
    start_send_email = int(time.time())

    multi.send_email_using_multiprocess(html_list, sendable_user_info_dict)

    end = int(time.time())

    print("total run time(sec) :", end - start_send_email)
    return "end"

# 유저 정보 다 가져오기
@app.route('/get/user')
def get_user():
  user_info= jsonify(user.getAllUserInfo(user_cursor))
  return user_info

if __name__ == "__main__":
  app.run(host='0.0.0.0', port='5001', debug=True)