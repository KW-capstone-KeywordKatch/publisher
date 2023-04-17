from flask import Flask, render_template, jsonify
import emailSender
import db
import multiprocessing
import time

app = Flask(__name__, static_folder="../index/build/static", template_folder="../index/build")

# smtp 서버 연결
@app.before_first_request
def before_first_request():
    global conn, cursor
    #conn, cursor = db.connectLOCALRDS()
    conn, cursor = db.connectUSERRDS()

@app.route('/')
def come_to_publisher():
  return render_template("index.html")
    
# email로 기사 보내는 api
@app.route('/send')
def send_request():
  with app.app_context():
    manager = multiprocessing.Manager()
    msg_list = manager.dict()
    user_list = db.getAllUserInfo(cursor)

    start_create_html = int(time.time())

    proc_list = []

    for i, user in enumerate(user_list):
      mp = multiprocessing.Process(target=emailSender.make_email_templet,args=(user, i, msg_list))
      mp.start()
      proc_list.append(mp)
    
    for proc in proc_list:
      proc.join()

    print("make form times:", int(time.time())-start_create_html)

    start_send_email = int(time.time())

    proc_list2 = []

    for i in range(len(user_list)):
      mp = multiprocessing.Process(target=emailSender.send_email,args=(user_list[i], msg_list[i]))
      mp.start()
      proc_list2.append(mp)

    for proc in proc_list2:
      proc.join()

    end = int(time.time())

    print("send run time(sec) :", end - start_send_email)
    
    print("total run time(sec) :", end - start_create_html)

    return "end"

@app.route('/get/user')
def get_user():
  user_info= jsonify(db.getAllUserInfo(cursor))
  return user_info

if __name__ == "__main__":
  app.run(host='0.0.0.0', port='5001', debug=True)